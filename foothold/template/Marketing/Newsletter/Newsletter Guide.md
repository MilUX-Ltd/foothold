---
type: guide
folder: Marketing/Newsletter
---

# Newsletter Guide

## Purpose

`Newsletter/` holds newsletter content: editions, backlog ideas, the active draft. One file per edition.

If you run multiple newsletters, each gets its own subfolder named after the newsletter, with editions inside.

## Add discipline

- One file per edition. Naming: `<Newsletter Name> — <YYYY-MM-DD> <Edition title>.md` so editions sort by date and the newsletter name is visible in search.
- Keep a backlog file (`<Newsletter Name> — Backlog.md`) for ideas, hooks, and stories you want to use in future editions.
- After an edition sends, capture the `sent:` date and `sent_url:` in frontmatter. Useful when you later want to see what went out and when.

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

## Related

- [[Marketing/Marketing Guide|Marketing Guide]] — parent
- [[Marketing/Marketing Outputs/Marketing Outputs Guide|Marketing Outputs Guide]] — sibling
