---
type: guide
folder: Resources/Methods
---

# Methods Guide

## Purpose

`Methods/` holds methodology theory: Kanban, Scrum, Lean, agile, Cost of Delay, methodology-adjacent frameworks. The theory layer.

Distinct from `Resources/Ways of Working/`, which is your own internal practice on top of methodology, and from `Resources/Frameworks/`, which is sense-making frameworks (Cynefin, Wardley, etc.).

## Structure

A flat folder, with a subfolder for any methodology that has several pages (`Kanban/Kanban Method.md`, `Kanban/Cost of Delay.md`, etc.).

## Writing a method note

- One file per methodology, or a subfolder if the methodology has multiple pages.
- Keep theory neutral: how the method works in general, not your particular interpretation of it. Your interpretation goes in `Ways of Working/`.
- If reading a method sparked an operating idea you want to test, note it in your hypotheses page, if you keep one (see the [[Knowledge/Knowledge Guide|Knowledge Guide]]).

## Lifecycle

Statuses are optional here. A method note is `status: active` and changes by being edited; set it to `archived` if you stop using the method, and keep the page.

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

## Canonical example

No example ships. Your first note, with the frontmatter above and a short account of what the method is and when it applies, sets the pattern.

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Resources/Ways of Working/Ways of Working Guide|Ways of Working Guide]] — sibling (practice layer)
- [[Resources/Frameworks/Frameworks Guide|Frameworks Guide]] — sibling (sense-making frameworks)
