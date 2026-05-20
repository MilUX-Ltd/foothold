---
type: guide
folder: Resources/Templates
---

# Templates Guide

## Purpose

`Templates/` holds reusable document templates: meeting agendas, decision records, retrospective formats, brief structures, onboarding checklists. Templates you fill in, not policies you follow.

Distinct from `Knowledge/` (policy you act on) and from `Skills/<skill>/references/` (templates a specific skill consumes at runtime).

## Add discipline

- One file per template (`Meeting Agenda Template.md`, `Decision Record Template.md`, `Retro Template.md`).
- A template is text you copy and fill in. If it's already filled in for a specific thing, it's not a template; it's that thing.
- When you find yourself rewriting the same structure from scratch for the third time, that's the moment to make it a template.
- Templates referenced by a skill (e.g. a brief structure the `/foothold-setup` skill uses) typically belong in that skill's `references/` folder, not here.

## Frontmatter

```yaml
---
type: template
status: active
created: YYYY-MM-DD
tags: [...]
---
```

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Skills/Skills Guide|Skills Guide]] — for skill-specific template references
