---
type: guide
folder: Marketing/Newsletter
---

# Newsletter Guide

## Purpose

`Newsletter/` holds newsletter content: editions, backlog ideas, the active draft. One file per edition.

If you run multiple newsletters, each gets its own subfolder named after the newsletter, with editions inside.

## Structure

```
Newsletter/
├── Newsletter Guide.md                          (this file)
├── <Newsletter Name> — Backlog.md               (ideas, hooks and stories for future editions)
└── <Newsletter Name> — <YYYY-MM-DD> <Edition title>.md
```

One file per edition, plus a backlog file per newsletter.

## Writing a newsletter edition

- One file per edition. Naming: `<Newsletter Name> — <YYYY-MM-DD> <Edition title>.md` so editions sort by date and the newsletter name is visible in search.
- Keep a backlog file (`<Newsletter Name> — Backlog.md`) for ideas, hooks, and stories you want to use in future editions.
- After an edition sends, capture the `sent:` date and `sent_url:` in frontmatter. Useful when you later want to see what went out and when.

## Lifecycle

`status:` runs `draft` -> `scheduled` -> `sent`. An edition moves on when you schedule or send it; record `sent:` and `sent_url:` when it goes out.

## Frontmatter

```yaml
---
type: newsletter-edition
newsletter: <newsletter name>
edition: YYYY-MM-DD or issue number
status: draft | scheduled | sent
sent: YYYY-MM-DD
sent_url: https://...
---
```

## Canonical example

No example edition ships. The `/newsletter-writer` skill can save a draft here; give it the frontmatter in the shape above. A new edition's frontmatter looks like this:

```yaml
---
type: newsletter-edition
newsletter: Example Newsletter
edition: 2026-05-20
status: draft
---
```

## Related

- [[Marketing/Marketing Guide|Marketing Guide]] — parent
- [[Marketing/Marketing Outputs/Marketing Outputs Guide|Marketing Outputs Guide]] — sibling
