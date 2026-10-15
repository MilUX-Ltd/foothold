---
type: guide
folder: Capabilities and Services/Customer-Facing Services
---

# Customer-Facing Services Guide

## Purpose

`Customer-Facing Services/` holds the offers your organisation sells. One file per service offer.

## Structure

A flat folder. One file per service, named `<Name> Service.md` (e.g. `Training and Coaching Service.md`, `Capability Audit Service.md`). The trailing "Service" makes the role of the page unmistakable in any search.

## Writing a customer-facing service

- Create a page when an offer is real enough to sell, starting from the [[Templates/Service|Service template]]. Include value proposition, target customer, scope, deliverables, pricing approach, and how it's delivered.
- If the offer is still being shaped, capture it in `Ideas/` first. Promote to a service page when it stabilises.
- Retire rather than delete: set `status: retired` on offers you've discontinued. Keeps institutional memory intact.

## Lifecycle

`status:` is `active`, `paused` or `retired`. See the parent [[Capabilities and Services/Capabilities and Services Guide|Capabilities and Services Guide]].

## Frontmatter

```yaml
---
type: service
status: active | paused | retired
created: YYYY-MM-DD
updated: YYYY-MM-DD
customer-facing: true
last_reviewed: YYYY-MM-DD
tags: []
---
```

## Canonical example

Start from the [[Templates/Service|Service template]]. No example offer ships, because your offers are yours; your first real one will set the pattern.

## Related

- [[Capabilities and Services/Capabilities and Services Guide|Capabilities and Services Guide]] — parent
- [[Capabilities and Services/Internal Services/Internal Services Guide|Internal Services Guide]] — sibling
- [[Templates/Templates Guide|Templates Guide]]: the Service template
