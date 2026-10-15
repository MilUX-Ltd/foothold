---
type: guide
folder: Capabilities and Services
---

# Capabilities and Services Guide

## Purpose

`Capabilities and Services/` is where your organisation's offers and operational functions live. Two clean halves: what you sell to customers, and what you run internally to keep the business working.

Distinct from `Marketing/`, which holds the published outputs (LinkedIn posts, case studies, newsletter content) that the marketing function produces. The function lives here; the artefacts live there.

## Structure

```
Capabilities and Services/
├── Capabilities and Services Guide.md     (this file)
├── Customer-Facing Services/
│   ├── Customer-Facing Services Guide.md
│   └── <Service Name>.md
└── Internal Services/
    ├── Internal Services Guide.md
    ├── Content Pillars.md                 (optional; create when you start producing content)
    ├── Content Creation Workflow.md       (optional; same)
    └── <Other internal services>.md
```

**Customer-Facing Services.** What your organisation sells. One file per service offer, named for the service (`Training and Coaching Service.md`, `Capability Audit Service.md`). The page carries the offer's positioning, scope, deliverables, pricing approach, and who it's for.

**Internal Services.** Operational functions you run internally to make the business work. Content production, compliance, finance, recruiting, sales operations. One file per function. Some functions are load-bearing for other parts of the vault (`Content Pillars.md` and `Content Creation Workflow.md` feed `Marketing/`).

## Writing a service

**Start from the template.** Insert the [[Templates/Service|Service template]]. It works for both halves; set `customer-facing: false` for an internal service.

**Adding a customer-facing service.** Create the page when the offer is real enough to sell. Include the value proposition, target customer, scope, deliverables, pricing approach, and how it gets delivered. If the offer is still being shaped, capture it in `Ideas/` first and promote to a service page when it stabilises.

**Adding an internal service.** Add a page when an operational function becomes a repeatable thing rather than ad-hoc work. The test: are you doing this regularly enough that codifying the approach would save time? If yes, it's an internal service.

**Naming.** Services get `<Name> Service.md`. Internal functions get descriptive names that match how you'd refer to them in conversation (`Content Pillars.md`, not `pillars.md`).

## Lifecycle

A service's `status:` is `active`, `paused` or `retired`. A service starts `active` when it is real enough to sell or run. `paused` is for a service you have put on hold. `retired` is for one you have stopped; keep the page for institutional memory and don't delete it unless the offer never existed in practice.

Set `last_reviewed:` whenever you check that the page still describes what you do.

## Frontmatter

```yaml
---
type: service
status: active | paused | retired
created: YYYY-MM-DD
updated: YYYY-MM-DD
customer-facing: true | false
last_reviewed: YYYY-MM-DD
tags: []
---
```

`customer-facing: true` for files under `Customer-Facing Services/`. `customer-facing: false` for files under `Internal Services/`. `updated` is when the page last changed; `last_reviewed` is when you last confirmed it is still right.

## Canonical example

Start from the [[Templates/Service|Service template]]. A content pillars page and a content creation workflow page in `Internal Services/` are the canonical pattern for an internal service that feeds another part of the vault (`Marketing/`). They don't ship; create them when you start producing content. For customer-facing, populate your first real offer and the structure will be self-evident.

## Related

- [[Capabilities and Services/Customer-Facing Services/Customer-Facing Services Guide|Customer-Facing Services Guide]]: what you sell
- [[Capabilities and Services/Internal Services/Internal Services Guide|Internal Services Guide]]: what you run internally
- [[Templates/Templates Guide|Templates Guide]]: the Service template
