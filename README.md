# rheaimpact.com

The main website for [Rhea Impact](https://rheaimpact.com), a Dallas-Fort Worth nonprofit placing humanoid robots in homes of single parents, seniors, and people with limited mobility.

## Stack

- **Frontend**: Static HTML with vanilla CSS (editorial/magazine aesthetic)
- **Backend**: Python (FastAPI) for volunteer signup form
- **Hosting**: HostRound (legacy) - migration to Railway planned

## Current Hosting

**Status:** Currently on HostRound (legacy), planned migration to Railway.

| Property | Value |
|----------|-------|
| IP | `162.220.24.23` |
| Provider | HostRound |
| Server | uvicorn |

**Target:** Railway project "Rhea-Impact" in Rhea AI workspace.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py
```

Site runs at `http://localhost:8000`

## Files

| File | Purpose |
|------|---------|
| `index.html` | Main site content |
| `main.py` | FastAPI backend (signup form handler) |
| `llms.txt` | AI content map for LLM crawlers |
| `robots.txt` | Search engine and AI crawler permissions |
| `images/` | Site images |

## AI-Friendly Features

This site is optimized for AI assistant discovery:

- **llms.txt** - Structured content map pointing to mission, research, and software
- **robots.txt** - Explicitly allows GPTBot, ClaudeBot, PerplexityBot
- **Research** - Technical docs at [rhea-impact.github.io](https://rhea-impact.github.io)

## Related Repos

| Repo | Purpose |
|------|---------|
| [rhea-impact.github.io](https://github.com/rhea-impact/rhea-impact.github.io) | AI reference docs (technical research) |
| [taskr](https://github.com/rhea-impact/taskr) | AI-native task management MCP server |
| [space-hog](https://github.com/rhea-impact/space-hog) | Disk cleanup CLI for macOS |
| [501c3](https://github.com/rhea-impact/501c3) | Nonprofit formation docs (private) |

## License

Content is proprietary to Rhea Impact. Contact hello@rheaimpact.com for permissions.
