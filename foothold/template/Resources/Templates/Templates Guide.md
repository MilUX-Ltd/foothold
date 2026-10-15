---
type: guide
folder: Resources/Templates
---

# Templates Guide

## Purpose

`Templates/` holds reusable document templates: meeting agendas, decision records, retrospective formats, brief structures, onboarding checklists. Templates you fill in, not policies you follow.

Distinct from `Knowledge/` (policy you act on) and from `Skills/<skill>/references/` (templates a specific skill consumes at runtime).

Note templates, the ones Obsidian inserts to start a contact, an engagement, a daily note and so on, live in the root `Templates/` folder, not here. See the [[Templates/Templates Guide|note Templates Guide]].

## Structure

A flat folder of template files, with this Guide at the root.

## Writing a template

- One file per template (`Meeting Agenda Template.md`, `Decision Record Template.md`, `Retro Template.md`).
- A template is text you copy and fill in. If it's already filled in for a specific thing, it's not a template; it's that thing.
- When you find yourself rewriting the same structure from scratch for the third time, that's the moment to make it a template.
- Templates referenced by a skill (e.g. a brief structure the `/foothold-setup` skill uses) typically belong in that skill's `references/` folder, not here.

## Lifecycle

Statuses are optional here. A template is `status: active` while you use it; set it to `archived` when you replace or stop using it, and keep the file.

## Frontmatter

```yaml
---
type: template
status: active
created: YYYY-MM-DD
tags: [...]
---
```

## Canonical example

The pitch deck examples in this folder show the shape: a finished, reusable document you copy and fill in rather than start from nothing.

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Skills/Skills Guide|Skills Guide]] — for skill-specific template references
- [[Templates/Templates Guide|Templates Guide (note templates)]]: the root `Templates/` folder
