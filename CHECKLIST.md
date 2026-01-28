# Rhea Impact System Buildout Checklist

> Track progress on making rheaimpact.com a trusted AI-readable resource

---

## 1. AI-Friendly Infrastructure (rheaimpact.com)

- [x] **llms.txt** - Structured content map at site root
  - Link to key pages (mission, volunteer, research)
  - Link to github.io for technical reference docs
- [ ] **llms-full.txt** - Full Markdown export for LLMs with limited context
- [x] **robots.txt** - Explicitly allow AI crawlers (GPTBot, ClaudeBot, PerplexityBot)
- [ ] **.md endpoints** - Serve Markdown versions at `.md` URLs
- [ ] **JSON-LD schema** - Organization, Article, SoftwareApplication markup
- [ ] **RSS feed** - Full content feed at `/feed.xml`

---

## 2. LLM-Centric Site (rhea-impact.github.io)

> **Goal: Get to the top of the leaderboard** - Make this the go-to reference AI agents cite

- [ ] **Optimize for AI consumption** - Dense, structured, machine-readable
- [ ] **Expand research coverage**:
  - [x] Hybrid Search with RRF
  - [x] Embedding Limitations
  - [x] Transcription Glossary Pipeline
  - [x] Triage Workflow Pattern
  - [ ] AI Crawling Standards (llms.txt, RSL, ai.txt comparison)
  - [ ] MCP Explained
  - [ ] Agent Authentication Standards
- [ ] **Cross-link from rheaimpact.com** - llms.txt should point here for technical depth
- [ ] **Structured frontmatter** - Problem/context/solution format for each doc
- [ ] **Citation-ready summaries** - 40-60 word blocks AI can quote directly
- [ ] **Monitor AI citations** - Track when Claude/GPT reference our docs

---

## 3. Research Wing (rheaimpact.com)

> Editorial/magazine style research for human readers

- [ ] **Create /research route** - Index page listing all articles
- [ ] **Research article template** - Schema.org markup, citation blocks
- [ ] **First article: AI Crawling Standards** - Research is complete, needs writeup
- [ ] **Future articles**:
  - [ ] Humanoid Robot Arrival Timeline
  - [ ] MCP Explainer (human-readable version)
  - [ ] Agent Authentication Standards

---

## 4. Software Section

- [x] Taskr card with GitHub link
- [x] Space Hog card with GitHub link
- [ ] Add to navigation
- [ ] Add to footer

---

## 5. Navigation & Footer Updates

- [x] Add "Research" link to nav (points to github.io)
- [x] Add "Software" link to nav (anchor to #software section)
- [x] Update footer with Research, Software, GitHub links

---

## Architecture Decision

**Two sites, two audiences:**

| Site | Audience | Content Style |
|------|----------|---------------|
| rheaimpact.com | Humans (donors, volunteers, press) | Magazine editorial |
| rhea-impact.github.io | AI agents + engineers | Dense technical reference |

The main site links to github.io for technical depth. This maximizes both human engagement and AI citability.

---

---

## 6. Mesh Network Strategy

> Ways for people to DISCOVER and SHARE what Rhea Impact is up to. Don't rely on the website alone.

### Discovery Channels (How People Find Us)

| Channel | Audience | Status |
|---------|----------|--------|
| **Google/SEO** | Everyone searching | [ ] Needs JSON-LD, sitemap |
| **AI assistants** | Claude/GPT users | [x] llms.txt, robots.txt done |
| **GitHub** | Developers | [x] Taskr, Space Hog repos |
| **Social media** | General public | [ ] Not started |
| **Press/media** | General public | [ ] Need press kit, pitch |
| **YouTube** | Visual learners | [ ] Robot demo videos |
| **Podcasts** | Tech/nonprofit audiences | [ ] Founder interviews |
| **Local DFW events** | Community | [ ] Meetups, demos |
| **Newsletter** | Engaged supporters | [ ] Email signup |
| **Word of mouth** | Everyone | Ongoing |

### Sharing Mechanics (How People Spread the Word)

| Content Type | Share Trigger | Platform |
|--------------|---------------|----------|
| Robot deployment update | "This is cool/heartwarming" | Twitter/X, LinkedIn, TikTok |
| Research article | "My coworkers should see this" | Slack, email, LinkedIn |
| Volunteer spotlight | "I know someone who'd do this" | Facebook, text |
| Demo video | "You have to see this robot" | YouTube, all social |
| Mission statement | "This nonprofit gets it" | LinkedIn, nonprofit networks |

### Social Media (TODO)

> Necessary evil for visibility. Keep it low-effort, high-signal.

- [ ] **Platform choice**:
  - LinkedIn: Professional credibility, nonprofit/tech crossover
  - X/Twitter: Tech crowd, AI community, fast news
  - TikTok: Reach, robot videos go viral here
  - YouTube: Evergreen demo content, SEO value
- [ ] **Content calendar**: Robot updates, volunteer spotlights, research drops
- [ ] **Automation**: AI drafts posts from devlogs → human reviews → publish
- [ ] **Shareability**: Make every post easy to reshare (clear message, good visual)

### Press/Media (TODO)

- [ ] **Press kit**: One-pager, founder bio, high-res photos, key stats
- [ ] **Story angles**:
  - "Nonprofit brings robots to single moms" (human interest)
  - "What happens when robots help people who need them most" (think piece)
  - "DFW organization democratizing humanoid robots" (local news)
- [ ] **Target outlets**: Local DFW news, nonprofit tech blogs, robotics press

### Newsletter/Email (TODO)

- [ ] Email signup on site (already have volunteer form - add general signup?)
- [ ] Monthly update: Deployment progress, volunteer stories, research highlights
- [ ] Shareable format: "Forward to a friend"

### Key Principle

Every piece of content should be:
1. **Valuable standalone** - Worth consuming even without context
2. **Shareable** - Easy to forward/repost with clear message
3. **Connected** - Links back to rheaimpact.com or volunteer signup

### Tracking

- [ ] Add "Built by Rhea Impact" to all repo READMEs
- [x] github.io links to rheaimpact.com
- [ ] Track referral sources (where do signups come from?)
- [ ] Monitor AI citations (when Claude/GPT mention us)

---

*Last updated: January 28, 2026*
