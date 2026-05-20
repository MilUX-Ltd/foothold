---
type: guide
folder: Capabilities and Services/Internal Services
---

# Internal Services Guide

## Purpose

`Internal Services/` holds the operational functions you run internally to keep the business working. Content production, compliance, finance, recruiting, sales operations. One file per function.

Some internal services are load-bearing for other parts of the vault: `Content Pillars.md` and `Content Creation Workflow.md` feed the `Marketing/` folder; a `Compliance Service.md` page may reference standards documents elsewhere in `Resources/` or `Knowledge/`.

## Add discipline

- Add a page when an operational function becomes a repeatable thing rather than ad-hoc work. The test: are you doing this regularly enough that codifying the approach would save time? If yes, it earns a page.
- Name files descriptively, matching how you'd refer to the function in conversation (`Content Pillars.md`, not `pillars.md`).
- Keep policy, not history. Operational decisions live in `Initiatives/`; the standing definition of the function lives here.

## Frontmatter

```yaml
---
type: service
status: active | paused | retired
created: YYYY-MM-DD
customer-facing: false
last_reviewed: YYYY-MM-DD
---
```

## Related

- [[Capabilities and Services/Capabilities and Services Guide|Capabilities and Services Guide]] — parent
- [[Capabilities and Services/Customer-Facing Services/Customer-Facing Services Guide|Customer-Facing Services Guide]] — sibling
