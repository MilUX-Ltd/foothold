---
type: guide
folder: Marketing
---

# Marketing Guide

## Purpose

`Marketing/` holds the marketing artefacts your organisation produces and ships: published posts, case studies, news articles, newsletter content. The function that creates them and the strategy behind them live elsewhere; this folder is for the outputs themselves.

The three-layer pattern Foothold ships:

- **Strategy.** Themes, pillars, positioning. Lives in `Capabilities and Services/Internal Services/Content Pillars.md`.
- **Workflow.** The production process. Lives in `Capabilities and Services/Internal Services/Content Creation Workflow.md`.
- **Outputs.** The published artefacts. Live here in `Marketing/`.

Marketing is a function you run, not a service you sell. If you sell marketing services to your customers, those service definitions go in `Capabilities and Services/Customer-Facing Services/`, not here.

## Structure

```
Marketing/
├── Marketing Guide.md              (this file)
├── Marketing Outputs/
│   ├── Marketing Outputs Guide.md
│   ├── LinkedIn Posts/
│   │   └── YYYY-MM-DD <Title>.md
│   ├── Case Studies.md             (index) or Case Studies/ (folder)
│   └── News Articles.md            (index) or News Articles/ (folder)
└── Newsletter/
    ├── Newsletter Guide.md
    ├── <Newsletter Name>.md        (newsletter index)
    └── <Edition slug>.md           (individual editions)
```

**`Marketing Outputs/`** holds published artefacts: LinkedIn posts, case studies, news articles. Each artefact is a file. LinkedIn posts use date-prefixed filenames so they sort chronologically.

**`Newsletter/`** holds newsletter content: editions, backlog, drafts. One file per edition.

## Frontmatter

LinkedIn post:

```yaml
---
type: linkedin-post
status: draft | scheduled | published
created: YYYY-MM-DD
published: YYYY-MM-DD
published_url: https://www.linkedin.com/...
tags: [...]
---
```

Case study:

```yaml
---
type: case-study
client: <client name or "anonymised">
status: draft | published
created: YYYY-MM-DD
tags: [...]
---
```

Newsletter edition:

```yaml
---
type: newsletter-edition
newsletter: <newsletter name>
edition: YYYY-MM-DD or issue number
status: draft | scheduled | sent
sent: YYYY-MM-DD
---
```

## Add discipline

**The promotion gate.** Marketing output that's been drafted by an agent or pulled in from elsewhere goes through a promotion step before it lands here. Promotion is a deliberate decision, not an automatic action. See the `CLAUDE.md` Promotion Pattern section.

**Publish dates matter.** Once a piece is published, capture the publish date and the public URL in the frontmatter. Future queries (Dataview, search) depend on this.

**Don't drift into strategy.** Strategy and themes belong in `Capabilities and Services/Internal Services/Content Pillars.md`. The artefact files in `Marketing/` should be the published thing, not the thinking behind it.

**Index pages versus folder.** For artefact types with few items (case studies, news articles), an index file works fine: `Marketing Outputs/Case Studies.md` listing each item. When the list gets long enough to feel cramped, promote to a subfolder (`Case Studies/`) with one file per item.

## Canonical example

A LinkedIn post:

```markdown
---
type: linkedin-post
status: published
created: 2026-05-15
published: 2026-05-15
published_url: https://www.linkedin.com/posts/<id>
tags: [defence, ai, second-brain]
---

# 2026-05-15 — Why founders should build a second brain before they hire

[Post body, in your voice, as it appeared on LinkedIn.]
```

Filename matches the date prefix and a short title. The frontmatter is the canonical record; the body is the published artefact.
