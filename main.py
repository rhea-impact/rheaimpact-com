"""Rhea Impact - Volunteer signup API + static site server."""
import os
import time
import hashlib
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime

import psycopg
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, field_validator

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Rhea Impact")

# Rate limiting: track requests per IP
rate_limit_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_REQUESTS = 5  # max requests
RATE_LIMIT_WINDOW = 300  # per 5 minutes

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rheaimpact.com",
        "https://www.rheaimpact.com",
        "https://rheaimpact.org",
        "https://www.rheaimpact.org",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


def check_rate_limit(ip: str) -> bool:
    """Check if IP is rate limited. Returns True if allowed."""
    now = time.time()
    # Clean old entries
    rate_limit_store[ip] = [t for t in rate_limit_store[ip] if now - t < RATE_LIMIT_WINDOW]

    if len(rate_limit_store[ip]) >= RATE_LIMIT_REQUESTS:
        return False

    rate_limit_store[ip].append(now)
    return True


@contextmanager
def get_db():
    """Database connection context manager."""
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="Database not configured - env var missing")
    try:
        conn = psycopg.connect(DATABASE_URL)
    except Exception as e:
        import sys
        print(f"Database connection error: {e}", file=sys.stderr)
        # Mask password in connection string for error message
        safe_url = DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'unknown'
        raise HTTPException(status_code=500, detail=f"Database connection failed to {safe_url}: {type(e).__name__}: {e}")
    try:
        yield conn
    finally:
        conn.close()


class SignupRequest(BaseModel):
    """Volunteer signup request."""
    name: str
    email: EmailStr
    location: str | None = None
    why: str | None = None
    # Honeypot field - should be empty (bots fill it)
    website: str | None = None

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Name is required')
        if len(v) > 255:
            raise ValueError('Name too long')
        return v.strip()

    @field_validator('location', 'why')
    @classmethod
    def sanitize_optional(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if len(v) > 1000:
            raise ValueError('Field too long')
        return v if v else None


class SignupResponse(BaseModel):
    """Signup response."""
    status: str
    message: str


@app.post("/signup")
async def signup(request: SignupRequest, req: Request):
    """Add a volunteer to the mailing list."""
    try:
        # Get client IP
        client_ip = req.headers.get("x-forwarded-for", req.client.host if req.client else "unknown")
        if "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()

        # Rate limiting
        if not check_rate_limit(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )

        # Honeypot check - if 'website' field is filled, it's a bot
        if request.website:
            # Silently accept but don't store (fool the bot)
            return SignupResponse(
                status="ok",
                message="You're on the list! We'll be in touch."
            )

        with get_db() as conn:
            with conn.cursor() as cur:
                # Check if email already exists
                cur.execute(
                    "SELECT id FROM rheaimpact.volunteers WHERE email = %s",
                    (request.email,)
                )
                if cur.fetchone():
                    return SignupResponse(
                        status="ok",
                        message="You're already on the list! We'll be in touch."
                    )

                # Insert new volunteer
                cur.execute(
                    """
                    INSERT INTO rheaimpact.volunteers (name, email, location, reason, created_at, ip_hash)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        request.name,
                        request.email,
                        request.location,
                        request.why,
                        datetime.utcnow(),
                        hashlib.sha256(client_ip.encode()).hexdigest()[:16]  # Store hashed IP for abuse tracking
                    )
                )
                conn.commit()

        return SignupResponse(
            status="ok",
            message="You're on the list! We'll be in touch."
        )
    except HTTPException:
        raise
    except Exception as e:
        import sys
        import traceback
        print(f"Signup error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Signup failed: {type(e).__name__}: {e}")


@app.get("/health", response_class=PlainTextResponse)
async def health():
    """Health check endpoint."""
    return "OK"


@app.get("/admin/volunteers/7x9k2m")
async def list_volunteers():
    """Admin view of volunteer signups (obscure URL)."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, email, location, reason, status, created_at
                FROM rheaimpact.volunteers
                ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
            volunteers = [
                {
                    "id": r[0],
                    "name": r[1],
                    "email": r[2],
                    "location": r[3],
                    "reason": r[4],
                    "status": r[5],
                    "created_at": r[6].isoformat() if r[6] else None
                }
                for r in rows
            ]

    # Return simple HTML page
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Rhea Impact - Volunteers</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 2rem; background: #f9fafb; }
        h1 { color: #111827; }
        .count { color: #6b7280; margin-bottom: 2rem; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #e5e7eb; }
        th { background: #f3f4f6; font-weight: 600; color: #374151; }
        tr:hover { background: #f9fafb; }
        .reason { max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .status { padding: 2px 8px; border-radius: 4px; font-size: 12px; }
        .status-pending { background: #fef3c7; color: #92400e; }
    </style>
</head>
<body>
    <h1>Volunteer Signups</h1>
    <p class="count">""" + str(len(volunteers)) + """ volunteers</p>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Location</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Signed Up</th>
            </tr>
        </thead>
        <tbody>"""

    for v in volunteers:
        status_class = f"status-{v['status']}" if v['status'] else ""
        html += f"""
            <tr>
                <td>{v['id']}</td>
                <td>{v['name']}</td>
                <td>{v['email']}</td>
                <td>{v['location'] or '-'}</td>
                <td class="reason" title="{v['reason'] or ''}">{v['reason'] or '-'}</td>
                <td><span class="status {status_class}">{v['status'] or '-'}</span></td>
                <td>{v['created_at'][:10] if v['created_at'] else '-'}</td>
            </tr>"""

    html += """
        </tbody>
    </table>
</body>
</html>"""

    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html)


# Serve static files
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
async def root():
    """Serve index.html."""
    return FileResponse("index.html")
