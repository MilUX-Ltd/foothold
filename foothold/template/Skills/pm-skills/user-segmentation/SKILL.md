---
name: user-segmentation
description: "Segment an existing user base from feedback and usage data into 3 or more distinct behaviour- and needs-based segments, grounded in the job each group is doing rather than demographics. Use when analysing diverse user feedback, building a segmentation model, or finding hidden user groups. The user-side companion to market-segments."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-market-research/user-segmentation), MIT. Copyright (c) 2026 Pawel Huryn. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: discovery-gtm
---

# User Segmentation

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-market-research/user-segmentation`, MIT, copyright Pawel Huryn). MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## What this is, and is not

For segmenting an existing **user** base by behaviour and need. It is the companion to `market-segments`, which segments the **customer** market by purpose. Use this when you have user feedback or usage data and want to find the distinct groups inside it; use `market-segments` when you are mapping who would hire the offering and why. The two should produce compatible segments: a user segment sits inside a purpose-segment.

## The defence move

Ground the segmentation in the job each user group is doing and the conditions they do it under, not in rank or unit. The user judges the offering on the experience of operating it under real conditions, so segment on that. Keep the user segments tied to the customer-side segmentation so the people who select can see the operators they are selecting for.

## Method

1. **Prepare the data:** feedback, interviews, support tickets, usage logs, surveys.
2. **Extract behaviour:** usage modes, journeys, proficiency, how the thing fits the wider workflow.
3. **Analyse needs:** the job each user is doing, the outcomes wanted, the pains.
4. **Cluster** into distinct, non-overlapping segments by behaviour and need.
5. **Validate** for coherence and actionability.
6. **Characterise** each with representative quotes.

## For each segment (minimum 3)

- **Name and overview:** a descriptive identifier, an estimated size, a one-line characterisation.
- **Behaviour:** how they use the thing; the journey; proficiency; workflow integration.
- **Purpose and motivation:** the job, the outcome, the context, what success looks like.
- **Needs and pains:** unmet needs, obstacles, workarounds, severity.
- **Current fit:** how well the thing serves them now; what they value; the gaps; churn risk.
- **What would improve fit:** the change that would move the experience, and what it serves.
- **Prioritisation:** strategic importance against ease of serving; invest, maintain, or de-prioritise.

## Notes

- Behaviour and need, not demographics. Quote real users.
- Flag segments thin in the data.
- Pairs with `market-segments`, `user-personas`, `customer-journey-map`.
