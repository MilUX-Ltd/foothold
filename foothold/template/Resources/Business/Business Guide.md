---
type: guide
folder: Resources/Business
---

# Business Guide

## Purpose

`Business/` holds business reference material: pricing strategy notes, sales playbooks, generic business doctrine, deal patterns, commercial conventions. The reading-and-reference layer for how to run a business.

Distinct from `Capabilities and Services/Internal Services/`, which holds your specific operational functions. Business is "general doctrine"; Internal Services is "what we do".

## Structure

A flat folder. One file per topic (`Pricing Strategy.md`, `Sales Process.md`, `Term Sheet Patterns.md`).

## Writing a business reference note

- One file per topic.
- Reference material, not policy. Policy that governs how you act lives in `Knowledge/`; documents you read for ideas live here.
- If a Business page becomes a thing you operationally rely on, promote the operational piece into `Internal Services/` and keep the reference reading here.

## Lifecycle

Statuses are optional here. A reference page is `status: active` and changes by being edited; set it to `archived` when it is out of date and you have no plan to refresh it, and keep the page.

## Frontmatter

```yaml
---
type: reference
status: active
created: YYYY-MM-DD
source: <citation or URL>
tags: [...]
---
```

## Canonical example

Your first page sets the pattern: a short summary at the top, the reference material, and the source named in the frontmatter.

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Capabilities and Services/Internal Services/Internal Services Guide|Internal Services Guide]] — for operational functions you actually run
