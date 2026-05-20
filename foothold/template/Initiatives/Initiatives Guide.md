---
type: guide
folder: Initiatives
---

# Initiatives Guide

## Purpose

`Initiatives/` is where work-in-flight and completed work lives. Each initiative is a coherent piece of work with goals, scope, decisions, meeting notes, and outputs. Distinct from `Ideas/` (early-stage thinking) and from `Capabilities and Services/` (your standing offers).

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

**`active/`** holds initiatives in flight. One folder per initiative. The folder name is kebab-case (`milux-brain/`, `client-rollout-q3/`). Inside, an index page named the same as the folder is the canonical entry point.

**`completed/`** holds finished initiatives. Move the whole folder from `active/` to `completed/` when the work wraps. Don't delete.

**Subfolders inside an initiative.** Add only when content justifies them:
- `research/` for source material specific to this initiative.
- `meetings/` for meeting notes related to the initiative.
- `decisions/` for documented decisions that need their own page.
- `attachments/` for non-Markdown artefacts (PDFs, images).

Don't create empty subfolders. Don't replicate every initiative's structure mechanically. Match the structure to the content.

## Frontmatter (the index page)

```yaml
---
type: initiative
status: active | completed | paused
created: YYYY-MM-DD
owner: <name>
tracking_card: <URL to work-tracking card if you use one>
parent_initiative: "[[Initiatives/active/<parent>/<parent>|<parent>]]"  # if part of a programme
---
```

## Add discipline

**Adding a new initiative.** Create the folder under `active/` with a kebab-case slug. Drop in the index page using the canonical template (Overview, Decisions Made, Goals, Open Questions, Current Status, Key Resources, Next Steps). Cross-link to your work-tracking card if you use one.

**Documenting decisions.** Decisions worth keeping go in the index page under a "Decisions Made" section, or as their own file under `decisions/` if they need fuller context. Always carry the date, the decision, the reasoning, and (if it matters) the alternatives that were considered.

**Closing out.** When an initiative wraps, move the folder from `active/` to `completed/`. Update the index page status. Write a short retrospective at the bottom: what worked, what didn't, what to carry forward.

**Don't conflate initiatives with services.** Initiatives are time-bounded. Services are standing offers. An initiative might result in a new service; the new service lives in `Capabilities and Services/`, the initiative that produced it stays in `Initiatives/completed/`.

## Canonical example

The canonical initiative index page carries these sections in order:

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
