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


# Serve static files
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
async def root():
    """Serve index.html."""
    return FileResponse("index.html")
