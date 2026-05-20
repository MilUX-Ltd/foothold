---
type: guide
folder: Resources/Methods
---

# Methods Guide

## Purpose

`Methods/` holds methodology theory: Kanban, Scrum, Lean, agile, Cost of Delay, methodology-adjacent frameworks. The theory layer.

Distinct from `Resources/Ways of Working/`, which is your own internal practice on top of methodology, and from `Resources/Frameworks/`, which is sense-making frameworks (Cynefin, Wardley, etc.).

## Add discipline

- One file per methodology, or a subfolder if the methodology has multiple pages (`Kanban/Kanban Method.md`, `Kanban/Cost of Delay.md`, etc.).
- Keep theory neutral: how the method works in general, not your particular interpretation of it. Your interpretation goes in `Ways of Working/`.
- Cross-reference into `Knowledge/hypotheses.md` if reading a method sparked an operating idea you want to test.

## Frontmatter

```yaml
---
type: method
status: active
created: YYYY-MM-DD
source: <citation or URL>
tags: [...]
---
```

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Resources/Ways of Working/Ways of Working Guide|Ways of Working Guide]] — sibling (practice layer)
- [[Resources/Frameworks/Frameworks Guide|Frameworks Guide]] — sibling (sense-making frameworks)
