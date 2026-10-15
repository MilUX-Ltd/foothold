---
type: guide
folder: Initiatives
---

# Initiatives Guide

## Purpose

`Initiatives/` is where work you do for yourself lives: internal services, your own products, marketing, thought leadership, operating-model change, internal tooling. Each initiative is a coherent piece of work with goals, scope, decisions, meeting notes, and outputs. Distinct from `Ideas/` (early-stage thinking) and from `Capabilities and Services/` (your standing offers).

Work you deliver for someone else, where an external organisation owns the outcome, lives in [[Customer Engagements/Customer Engagements Guide|Customer Engagements]], not here. The line is binary: who owns the outcome.

- Outcome owned by your business -> `Initiatives/`.
- Outcome owned by an external organisation -> `Customer Engagements/`.

The split exists because customer work has a different lifecycle, a different audit trail, and a different downstream artefact (a case study) than internal work.

Initiatives are knowledge artefacts with an operational layer: the page here is the canonical record; if you have a work-tracking system (Linear, Asana, Trello, Businessmap), the cards underneath are cross-linked from here.

## Structure

```
Initiatives/
├── Initiatives Guide.md            (this file)
├── active/
│   ├── <initiative-slug>/
│   │   ├── <initiative-slug>.md    (the index page)
│   │   ├── research/               (optional)
│   │   ├── meetings/               (optional)
│   │   └── decisions/              (optional)
│   └── ...
└── completed/
    └── <initiative-slug>/
        └── ...
```

**`active/`** holds initiatives in flight. One folder per initiative. The folder name is kebab-case (`customer-rollout-q3/`, `product-launch-2026/`). Inside, an index page named the same as the folder is the canonical entry point.

**`completed/`** holds finished initiatives. Move the whole folder from `active/` to `completed/` when the work wraps. Don't delete.

**Subfolders inside an initiative.** Add only when content justifies them:
- `research/` for source material specific to this initiative.
- `meetings/` for meeting notes related to the initiative.
- `decisions/` for documented decisions that need their own page.
- `attachments/` for non-Markdown artefacts (PDFs, images). Keep large or sensitive files out of the vault and link them; see the [[Attachments/Attachments Guide|Attachments Guide]].

Don't create empty subfolders. Don't replicate every initiative's structure mechanically. Match the structure to the content.

## Writing an initiative

**Adding a new initiative.** Create the folder under `active/` with a kebab-case slug. Drop in the index page using the [[Templates/Initiative|Initiative template]] (Overview, Decisions Made, Goals, Open Questions, Current Status, Key Resources, Next Steps). Cross-link to your work-tracking card if you use one.

**Documenting decisions.** Decisions worth keeping go in the index page under a "Decisions Made" section, or as their own file under `decisions/` if they need fuller context. Always carry the date, the decision, the reasoning, and (if it matters) the alternatives that were considered.

**Meeting notes.** Write each one with the [[Templates/Meeting|Meeting template]] and file it in the initiative's `meetings/` folder, named `YYYY-MM-DD <title>.md`.

**Closing out.** When an initiative wraps, move the folder from `active/` to `completed/`. Update the index page status. Write a short retrospective at the bottom: what worked, what didn't, what to carry forward.

**Don't conflate initiatives with services.** Initiatives are time-bounded. Services are standing offers. An initiative might result in a new service; the new service lives in `Capabilities and Services/`, the initiative that produced it stays in `Initiatives/completed/`.

## Lifecycle

An initiative's `status:` is `active`, `paused` or `completed`. It starts `active`, in `active/`. It becomes `completed` when the work wraps, and at that point the folder moves to `completed/`. `paused` is for work you have put on hold; the folder stays in `active/` until you restart it or finish it.

## Frontmatter

The index page:

```yaml
---
type: initiative
status: active | completed | paused
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: <name>
tracking_card: <URL to work-tracking card if you use one>
parent_initiative: "[[Initiatives/active/<parent>/<parent>|<parent>]]"  # if part of a programme
tags: []
---
```

Meeting notes carry `type: meeting-note`, `created:` and `tags:`. They take no status.

## Canonical example

Start from the [[Templates/Initiative|Initiative template]]. The canonical initiative index page carries these sections in order:

```markdown
---
type: initiative
status: active
created: YYYY-MM-DD
owner: <name>
---

# <Initiative Name>

## Overview
One paragraph: what this is, why it matters.

## Decisions Made
Decisions taken so far. Date-stamped where useful.

## Goals
What success looks like. Measurable if possible.

## Open Questions
Things still to resolve. Each one should have a date by which it needs deciding.

## Current Status
Where things stand right now.

## Key Resources
Wikilinks to relevant Context, CRM, Intelligence, or Resources pages.

## Next Steps
What needs to happen next.
```

Replace each section with real content as the work develops. Sections with no content can be omitted until they have something to carry.

## Related

- [[Customer Engagements/Customer Engagements Guide|Customer Engagements Guide]]. Sister Guide. Work for an external organisation.
- [[Ideas/Ideas Guide|Ideas Guide]]. Where early-stage thinking lives before it becomes an initiative.
- [[Templates/Templates Guide|Templates Guide]]. The Initiative and Meeting templates.
