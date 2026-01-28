# ROADMAP2: AI-Friendly Website & Research Platform

> Vision: Make rheaimpact.com a trusted AI-readable resource on humanoid robotics and AI infrastructure, with original research that both humans and LLMs can cite.

---

## 1. AI-Friendly Site Architecture

### 1.1 Implement llms.txt

Create `/llms.txt` at site root with structured content map:

```markdown
# Rhea Impact

> Nonprofit placing humanoid robots in homes of single parents, seniors, and people with limited mobility in Dallas-Fort Worth. Also publishes free software for AI coding agents.

## About
- [Mission](/about): Our approach to democratizing humanoid robot access
- [Volunteer](/volunteer): Join the DFW volunteer network

## Research
- [AI Crawling Standards](/research/ai-crawling-standards): Analysis of llms.txt, RSL, ai.txt
- [Humanoid Robot Timeline](/research/humanoid-timeline): When general-purpose robots arrive

## Software
- [Taskr](https://github.com/rhea-impact/taskr): AI-native task management for Claude Code
- [Space Hog](https://github.com/rhea-impact/space-hog): Disk cleanup CLI for macOS
```

**Status:** TODO

### 1.2 Create llms-full.txt

Full Markdown export of all site content for LLMs with limited context windows.

**Status:** TODO

### 1.3 Add .md Endpoints

Serve Markdown versions of pages at `.md` URLs (e.g., `/about.md`, `/research/ai-crawling-standards.md`).

**Status:** TODO

### 1.4 JSON-LD Schema Markup

Add structured data to all pages:
- `Organization` schema for Rhea Impact
- `Article` schema for research pieces  
- `SoftwareApplication` schema for Taskr/Space Hog
- `FAQPage` for common questions

**Status:** TODO

### 1.5 robots.txt for AI Crawlers

Explicitly allow AI crawlers:

```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot  
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: *
Allow: /
```

**Status:** TODO

---

## 2. Research Section

### 2.1 AI Crawling Standards (READY TO WRITE)

**File:** `/research/ai-crawling-standards.md`

**Summary:** Analysis of competing standards for AI content discovery and access control.

**Key Findings:**

| Standard | Purpose | Status | Enforcement |
|----------|---------|--------|-------------|
| llms.txt | Guide LLMs to key content (Markdown) | Proposed, limited adoption | Honor system only |
| RSL (Robots Source Language) | Extension of robots.txt with AI-specific directives | Official Dec 2025, backed by Yahoo, Ziff Davis, Cloudflare, Akamai | CDN-level enforcement |
| ai.txt | Permission controls for AI training/scraping | Proposed by Spawning | Integrated with Hugging Face |
| agents.txt | Agent-to-agent service discovery | Proposed | None |

**Key Insight:** RSL is the real contender because Cloudflare/Akamai can enforce it at the network level. llms.txt remains advisory-only.

**Practical Recommendations:**
1. Implement llms.txt anyway (low effort, potential upside)
2. Monitor RSL adoption—may need robots.txt updates
3. Focus on semantic HTML and JSON-LD (actually works today)
4. Structure content with 40-60 word "citation blocks" at section starts

**Status:** RESEARCH COMPLETE, NEEDS WRITEUP

---

### 2.2 Humanoid Robot Arrival Timeline

**File:** `/research/humanoid-timeline.md`

**Questions to Answer:**
- When will 1X Neo ship to consumers?
- What's the realistic timeline for household-capable humanoids?
- Price trajectory projections
- Which companies are closest to general-purpose home robots?

**Status:** TODO - NEEDS RESEARCH

---

### 2.3 MCP (Model Context Protocol) Explainer

**File:** `/research/mcp-explained.md`

**Summary:** What MCP is, what it isn't, and why it matters for AI tool integration.

**Key Points:**
- MCP ≠ web crawling (common misconception)
- MCP = runtime protocol for AI apps to connect to configured servers
- Use cases: database access, API integration, tool calling
- Relevance to Rhea Impact's Taskr project

**Status:** TODO - NEEDS WRITEUP

---

### 2.4 AI Agent Authentication Standards

**File:** `/research/agent-authentication.md`

**Questions to Answer:**
- How will AI agents prove identity to services?
- What's the timeline for standardized agent auth (projected 2026-2028)?
- Implications for content licensing

**Status:** TODO - NEEDS RESEARCH

---

## 3. Site Structure Changes

### 3.1 Add /research Route

Create research index page listing all research articles with:
- Title
- Summary (40-60 words, quotable)
- Date published
- Tags

**Status:** TODO

### 3.2 Research Article Template

Standardized template for research pieces:

```html
<article itemscope itemtype="https://schema.org/Article">
  <h1 itemprop="headline">[Title]</h1>
  <p class="citation-block" itemprop="description">
    [40-60 word summary that LLMs can quote directly]
  </p>
  <meta itemprop="datePublished" content="YYYY-MM-DD">
  <meta itemprop="author" content="Rhea Impact">
  
  [Content with proper heading hierarchy]
</article>
```

**Status:** TODO

### 3.3 RSS Feed with Full Content

Provide RSS/Atom feed at `/feed.xml` with complete article content (not excerpts) for AI systems that consume feeds.

**Status:** TODO

---

## 4. Technical Implementation Notes

### For Claude Code Handoff:

1. **Priority order:**
   - llms.txt (quick win)
   - robots.txt update
   - JSON-LD schema on existing pages
   - /research route + first article (AI Crawling Standards)

2. **File locations:**
   - `/llms.txt` - static file at root
   - `/robots.txt` - static file at root  
   - `/research/index.html` - research listing page
   - `/research/ai-crawling-standards.html` - first research article

3. **Content for AI Crawling Standards article is ready** - see section 2.1 above

4. **Keep same visual style** as current site (editorial/magazine aesthetic)

---

## 5. Future Ideas (Backlog)

- [ ] IndexNow integration for signaling fresh content
- [ ] Sitemap with priority hints
- [ ] OpenAPI spec for any future APIs
- [ ] Consider ai.txt if training opt-out becomes important
- [ ] Monitor RSL adoption for robots.txt updates
- [ ] Research piece on humanoid robot safety standards
- [ ] Research piece on robot-human interaction design
- [ ] Case studies from actual robot deployments (once we have them)

---

*Last updated: January 28, 2026*
