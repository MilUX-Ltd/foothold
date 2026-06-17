---
name: prioritization-frameworks
description: "Reference guide for selecting and applying a prioritisation method. Leads with the economic methods, Cost of Delay and CD3 (Cost of Delay Divided by Duration), then covers Opportunity Score, ICE, RICE, Kano, MoSCoW and the rest with formulas and when-to-use guidance. Use when sequencing work, choosing a prioritisation method, or comparing approaches. Fits a Kanban, flow-first delivery practice."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-execution/prioritization-frameworks), MIT. Copyright (c) 2026 Pawel Huryn. Cost of Delay and CD3 section added in this fork. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: delivery-coaching
---

# Prioritisation Frameworks Reference

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-execution/prioritization-frameworks`, MIT, copyright Pawel Huryn). This fork leads with Cost of Delay and CD3, consistent with a Kanban, flow-first practice, and keeps the upstream nine-framework reference below as the wider toolkit. MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## Core principle

Prioritise problems (opportunities), not features. And sequence by the economics of delay, not by gut feel or by who shouts loudest.

## Cost of Delay and CD3

For a Kanban, flow-first practice, the default sequencing method is the economic one.

- **Cost of Delay (CoD)** is the value lost per unit of time that a piece of work is not done: the money, capability, or risk-reduction you forgo by it sitting in the queue. Estimate it honestly in money-over-time or a clear proxy; an order-of-magnitude CoD beats a precise made-up number. The four CoD shapes (linear, fixed-date, expedite, intangible) usually cover defence work, where a fixed-date or expedite profile (an exercise window, a bid deadline, a mandated capability date) is common.
- **CD3 (Cost of Delay Divided by Duration)** sequences the queue: **CD3 = Cost of Delay / Duration**. Do the work with the highest CD3 first. It captures the same instinct as WSJF (the SAFe cousin) but stays in flow terms. This is a strong default for ordering a backlog or a set of bids.

Use CoD and CD3 when work competes for the same capacity and you can estimate the value of sooner. When you cannot estimate CoD at all, fall back to one of the methods below, and treat that as a signal to go and find the missing economic information.

## Opportunity Score (Dan Olsen)

The recommended method for prioritising customer problems. Survey customers on Importance and Satisfaction per need, normalised 0 to 1.

- Current value = Importance x Satisfaction
- Opportunity Score = Importance x (1 - Satisfaction)
- Customer value created = Importance x (S2 - S1)

High importance and low satisfaction is the best opportunity.

## ICE and RICE

- **ICE** = Impact x Confidence x Ease. Quick prioritisation of ideas and initiatives.
- **RICE** = (Reach x Impact x Confidence) / Effort. ICE with Reach split out, for more granularity at scale.

## The nine at a glance

| Framework | Best for | Key insight |
|---|---|---|
| Cost of Delay / CD3 | Sequencing competing work | CD3 = CoD / Duration; highest first. |
| Eisenhower Matrix | Personal tasks | Urgent vs important. |
| Impact vs Effort | Quick triage | Simple 2x2; not rigorous for strategy. |
| Risk vs Reward | Initiatives | Impact vs effort with uncertainty. |
| Opportunity Score | Customer problems | Importance x (1 - Satisfaction). |
| Kano Model | Understanding expectations | Must-be, performance, attractive. For understanding, not ranking. |
| Weighted Decision Matrix | Multi-factor decisions | Weighted criteria; good for stakeholder buy-in. |
| ICE | Ideas/initiatives | Impact x Confidence x Ease. |
| RICE | Ideas at scale | (Reach x Impact x Confidence) / Effort. |
| MoSCoW | Requirements | Must/Should/Could/Won't. Project-management origin; use with care. |

## Notes

- Be explicit about which method you used and why; the method is part of the decision record.
- Pairs with `prioritization-frameworks` where classes of service and replenishment use the same economics.

## References and further reading

- Joshua Arnold, Black Swan Farming, on Cost of Delay and CD3.
- David Anderson / Kanban University: classes of service, Triage Tables, Cost of Delay profiles.
- Don Reinertsen, *The Principles of Product Development Flow*, on the economics of queues.
- Dan Olsen, *The Lean Product Playbook*, on the Opportunity Score.
