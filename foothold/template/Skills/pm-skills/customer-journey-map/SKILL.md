---
name: customer-journey-map
description: "Build an end-to-end customer journey map: the stages a customer or user moves through, the touchpoints, what they do, think and feel, where the friction is, and what to improve. Use when mapping a customer or user experience, finding friction in a buying or in-service journey, or improving onboarding or integration. Defence-aware: separates the customer who selects and pays from the user who operates, and maps the acquisition journey, not a consumer marketing funnel."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-market-research/customer-journey-map), MIT. Copyright (c) 2026 Pawel Huryn. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: discovery-gtm
---

# Customer Journey Map

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-market-research/customer-journey-map`, MIT, copyright Pawel Huryn). MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## What this is

You map a real journey, as a piece of discovery or design work.

## Read before you start

Hold to a consistent vocabulary so a journey map means the same thing each time:

- **Customer and user are different people.** The **customer** selects and pays; the **user** operates. In defence they are routinely separate: a commercial officer or capability lead selects, a soldier or operator uses. Each travels a different journey and judges the offering on different criteria. Decide at the outset whose journey you are mapping, name them with the same persona definition the `user-personas` work uses, and map a second lane if both matter.
- **The journey is where the experience of being served is felt.** Frame pain points and opportunities in terms of the acquiring and in-service experience, lead time, predictability, responsiveness, not as generic UX friction.
- **Moments of truth are decision points.** Where a customer commits or abandons is where a real selection criterion, and its threshold, lives. Capture them as such so they carry into later work.

## Context

You are creating a journey map for **$ARGUMENTS**.

If material is provided (interview transcripts, survey data, complaint logs, win/loss notes, support tickets, an existing process map, analytics), read it first. The map is only as good as the evidence under it; be honest on the artefact about what is evidenced and what is assumed.

## Instructions

1. **Name the traveller.** Customer or user, which segment, and the purpose they are pursuing (the job they are hiring the service for). Use a specific persona with its job to be done, not a generic "user". If both customer and user matter, run two lanes.

2. **Map the journey stages.** Adapt to the situation; do not force a consumer funnel onto a procurement reality. For a defence **customer (acquisition) journey** the stages are usually nearer to:

   | Stage | Description |
   |---|---|
   | **Need / capability gap** | How the requirement first surfaces, and who owns it |
   | **Requirement definition** | What gets specified, and the constraints (security, standards, accreditation) |
   | **Market engagement** | How they find and assess suppliers; DSP, frameworks, primes, direct |
   | **Procurement / competition** | The route to contract and what they actually select on |
   | **Contract / mobilisation** | Award, onboarding the supplier, security and access set-up |
   | **Integration** | Getting the thing into service alongside what already exists |
   | **In-service use** | The user's day-to-day; sustainment, support, training |
   | **Through-life / recompete** | Upgrades, renewal, the decision to extend or re-tender |

   For a **user (operator) journey** the stages are the operational task the thing supports, from first use through reliance to working around its limits. Choose the frame that fits the traveller.

3. **For each stage, document:**
   - **Touchpoints:** where the traveller meets the supplier, the product, or the team.
   - **Actions:** what they do at this stage.
   - **Thoughts and questions:** what is on their mind ("can this clear accreditation?", "what is the through-life cost?", "will it work without comms?").
   - **Emotions:** how they feel, rated simply so the low points are visible.
   - **Pain points:** friction, delay, confusion, the risk of deselection.
   - **Opportunities:** how to improve the experience, and what it would move.

4. **Identify the critical moments:**
   - **Value moment:** when the traveller first gets the thing they came for.
   - **Moments of truth:** the decision points where they commit or abandon. Note the threshold that would tip them.
   - **Drop-off / deselection risks:** where they most commonly walk away, and why.

5. **Assemble the map.** Produce it as a table, and render an interactive view of the journey to react to and iterate. Columns:

   | Stage | Touchpoint | Action | Emotion | Pain point | Opportunity |
   |---|---|---|---|---|---|

6. **Recommend prioritised improvements.** Which pain points carry the highest risk of deselection or the highest through-life cost; the quick wins; the deeper investments with the biggest payoff.

## Notes

- Keep the customer and user lanes distinct; collapsing them hides the user's needs from the people who select, which is itself a common finding.
- A journey map built on three complaints and one interview is a hypothesis, not a measurement. Say which it is on the artefact.
- Pairs with `user-personas` (the traveller).

## Further reading

Upstream references from the original author (software product context, method transfers):

- [User Journey Mapping 101](https://www.productcompass.pm/p/user-journey-mapping-101)
- [Funnel Analysis 101](https://www.productcompass.pm/p/funnel-analysis)
- [Market Research: Advanced Techniques](https://www.productcompass.pm/p/market-research-advanced-techniques)
