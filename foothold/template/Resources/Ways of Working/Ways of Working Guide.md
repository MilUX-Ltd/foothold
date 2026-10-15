---
type: guide
folder: Resources/Ways of Working
---

# Ways of Working Guide

## Purpose

`Ways of Working/` holds your own internal practices: meeting agreements, task-writing conventions, working norms, retro rituals. The practice layer on top of methodology.

Distinct from `Resources/Methods/`, which holds methodology theory in general. Methodology is "Kanban explained"; Ways of Working is "this is how we run our Kanban".

## Structure

A flat folder. One file per practice (`Meeting Agreements.md`, `Task Writing Guidelines.md`, `Retrospective Format.md`). The pack also ships two pages about handling the vault itself: `Sync and Backup.md` and `Where Your Data Lives.md`.

## Writing a ways-of-working page

- One file per practice.
- These pages get referenced often, so keep them tight. The recipient is usually scanning for a specific rule, not reading the page end-to-end.
- Review on a cadence (quarterly is a sensible default). Practices drift; the page should reflect what you actually do, not what you started with.

## Lifecycle

Statuses are optional here. A practice page is `status: active` while the practice is in use; set `last_reviewed:` each time you check it still matches what you do, and set `status: archived` when you stop the practice.

## Frontmatter

```yaml
---
type: ways-of-working
status: active
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
---
```

## Canonical example

Your first practice page, with the frontmatter above, sets the pattern. For the tone to aim for, see [[Resources/Ways of Working/Where Your Data Lives|Where Your Data Lives]]: it opens with the short answer, then covers detail in short sections.

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Resources/Methods/Methods Guide|Methods Guide]] — sibling (theory layer)
