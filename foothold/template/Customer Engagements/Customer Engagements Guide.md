---
type: guide
folder: Customer Engagements
---

# Customer Engagements Guide

## Purpose

`Customer Engagements/` is where work you deliver for someone else lives: a paying customer, a sponsoring partner, a pro-bono engagement with an external organisation that owns the outcome.

This sits alongside `Initiatives/`, which is for work you do for yourself: internal services, your own products, marketing, thought leadership, operating-model change, internal tooling.

The line is binary: who owns the outcome.

- Outcome owned by your business -> `Initiatives/`.
- Outcome owned by an external organisation -> `Customer Engagements/`.

Paid, sponsored, or pro-bono doesn't decide the folder. What decides it is whether there is a named external organisation on the receiving end of the delivery. If there is, and that organisation has a page in `CRM/organisations/`, the work belongs here.

## Why split them

Customer work and internal work have different rhythms, different audit trails, and different downstream artefacts. Customer engagements typically produce a case study at the end; internal initiatives typically produce a new service, product, or capability. Mixing the two makes "what is my current client load" harder to read than it should be, and makes case-study harvesting harder later.

## Lifecycle

Engagements move through three states, each with its own subfolder:

1. **`scoping/`**. Conversations underway, deliverable being shaped, no commitment to deliver yet. Sales pipeline territory. A scoping engagement may end in a proposal accepted (hand-off to `active/`), in a quiet "no", or in a hand-off that never lands.
2. **`active/`**. Scope agreed, by verbal commitment, purchase order, or signed proposal. You are delivering.
3. **`completed/`**. Delivery finished. Kept for reference, case studies, and historical context.

Engagements that go cold during scoping and don't recover stay in `scoping/` with `status: archived` rather than being deleted. Useful CRM signal for future conversations with the same organisation.

## Structure

```
Customer Engagements/
├── Customer Engagements Guide.md   (this file)
├── scoping/
│   └── <Customer> - <Engagement Title>/
│       ├── <Customer> - <Engagement Title>.md                          (index)
│       ├── <Customer> - <Engagement Title> - Outcome.md                (sibling)
│       ├── <Customer> - <Engagement Title> - Stakeholder Map.md
│       ├── <Customer> - <Engagement Title> - Comms Plan.md
│       ├── <Customer> - <Engagement Title> - RAID Log.md
│       ├── <Customer> - <Engagement Title> - Mobilisation Checklist.md
│       └── specs/                                                       (optional)
├── active/
│   └── <Customer> - <Engagement Title>/
│       ├── <Customer> - <Engagement Title>.md                          (index)
│       ├── research/                                                    (optional)
│       ├── meetings/                                                    (optional)
│       ├── decisions/                                                   (optional)
│       └── deliverables/                                                (optional)
└── completed/
    └── <Customer> - <Engagement Title>/
        └── ...
```

Subfolders inside an engagement are added when content justifies them, not as empty scaffolding.

## Subfolders

Create only when content justifies. Don't pre-scaffold empty folders.

- **`meetings/`**. Anything `type: meeting-note`. One file per meeting, filename prefixed with the ISO date (e.g. `2026-05-27 client kickoff.md`). All meeting notes for the engagement live here, never in `notes/`.
- **`research/`**. Desk research, captures, briefing notes, research packs sourced for the engagement.
- **`specs/`**. Briefs, job specs, SoW drafts, signed contracts.
- **`decisions/`**. Material decisions documented with reasoning and the alternatives considered.
- **`drafts/`**. Work products being drafted.
- **`deliverables/`**. Final outputs handed over to the customer.
- **`notes/`**. Catch-all for free-text working notes that don't fit any of the above. Should be rare. If a note has a meeting context, it belongs in `meetings/`.

The rule that matters: `type: meeting-note` lives in `meetings/`. Vault Dataview queries and any meeting-prep flow you wire up rely on this.

## File naming convention

Folder, index, and sibling artefact files all use **title case** with a plain hyphen separator and surrounding spaces (` - `). No em dashes.

The pattern is `<Customer> - <Engagement Title> - <Artefact>.md` for siblings, and `<Customer> - <Engagement Title>.md` for the index. So a Discovery engagement with a customer called Acme looks like:

- `Acme - Discovery.md` (index)
- `Acme - Discovery - Outcome.md`
- `Acme - Discovery - Stakeholder Map.md`
- `Acme - Discovery - Comms Plan.md`
- `Acme - Discovery - RAID Log.md`
- `Acme - Discovery - Mobilisation Checklist.md`

The customer prefix matters because the same customer can have multiple engagements over time. The engagement title differentiates them. The artefact suffix makes vault search unambiguous: a bare search for `Outcome` should always resolve to one file.

Use the customer's name as it appears in their CRM organisation page; whatever capitalisation or separator the CRM page uses, mirror it here. The engagement title is short and distinctive (`Discovery`, `Product Support`, `Mobilisation Sprint`).

## Delivery management sections

Every engagement carries a set of sections beyond Overview / Customer / Status to make delivery management explicit:

- **Outcome and Benefits Measurement.** What success looks like and how the customer will know it has landed.
- **Scope and Deliverables.** A table per deliverable: deliverable, acceptance criteria, sign-off owner, due date.
- **Definition of Done.** Engagement-level. When the engagement is complete and how it is closed.
- **Reporting and Governance Cadence.** Formal status, retros, steering. Distinct from day-to-day comms.
- **Change Control.** How a change to scope, timeline, or budget is raised, agreed, and recorded.
- **Capacity and Availability.** Your agreed time on the engagement, blackouts, and competing commitments.
- **Engagement Health.** `health: green | amber | red` plus `last_health_check:` in the index frontmatter. Surfaced on Home.md.
- **Data classification.** A row in the Information Architecture table stating the data classification appropriate to the customer and sector.
- **Decisions.** ADR-style log in the `decisions/` subfolder, one file per decision, naming `D-NN <short title>.md`. A decision without considered alternatives is a note, not a decision.

Each of these turns into a gate on the mobilisation checklist when scoping is complete.

## Frontmatter (the index page)

```yaml
---
type: customer-engagement
status: scoping | active | paused | completed | archived
health: green | amber | red
last_health_check: YYYY-MM-DD
customer: "[[CRM/organisations/<Org>|<Org>]]"
created: YYYY-MM-DD
owner: <name>
tracking_card: <URL to work-tracking card if you use one>
---
```

The `customer:` field is a wikilink to the matching organisation page in `CRM/organisations/`. Every engagement should map 1:1 to an organisation page. If the organisation doesn't have a page yet, create one before the engagement page.

## Canonical example

The canonical engagement index page carries these sections in order:

```markdown
---
type: customer-engagement
status: scoping
customer: "[[CRM/organisations/<Org>|<Org>]]"
created: YYYY-MM-DD
owner: <name>
---

# <Customer> — <Engagement Name>

## Overview
One paragraph: what this is, why the customer wants it.

## Customer
Link to the CRM organisation page and the named stakeholders.

## Current Status
Where things stand right now.

## Scope and Deliverables
What you are delivering. Acceptance criteria where appropriate.

## Decisions Made
Decisions taken so far. Date-stamped.

## Open Questions
Things still to resolve.

## Key Resources
Wikilinks to the brief, the contract, related Intelligence pages, related contacts.

## Next Steps
What needs to happen next.
```

Sections with no content can be omitted until they have something to carry.

## Add discipline

**Adding a new engagement.** Create the folder under `scoping/` with a kebab-case slug. Drop in the index page using the canonical template. Wikilink the `customer:` field to the matching `CRM/organisations/` page (create the org page first if it doesn't exist).

**Moving between states.** When the engagement moves between states, move its folder to the matching subfolder and update the index `status:`.

- `scoping/` -> `active/` when scope is agreed (verbal, PO, or signed proposal).
- `active/` -> `completed/` when delivery is finished.
- `scoping/` engagements that go cold stay in `scoping/` with `status: archived`.

Wikilinks elsewhere in the vault need updating to reflect the new path.

**Closing out.** When an engagement wraps, move the folder from `active/` to `completed/`. Update the index `status:`. Write a short retrospective at the bottom of the index page: what worked, what didn't, what to carry forward. A case study in `Capabilities and Services/` typically follows.

**Don't conflate engagements with services.** Engagements are time-bounded. Services are standing offers. An engagement might result in a refined service description in `Capabilities and Services/`; the engagement itself stays in `Customer Engagements/`.

## Related

- [[Initiatives/Initiatives Guide|Initiatives Guide]]. Sister Guide. Internal work, not customer-led.
- [[CRM/CRM Guide|CRM Guide]]. Customer organisations and contacts. Each engagement links 1:1 to an organisation here.
