---
name: strategy-red-team
description: "Red-team a bid, capture plan, business case, roadmap or strategy by attacking its load-bearing assumptions before reality does. Steelmans each claim, then attacks it, ranks failure modes by impact, likelihood and cheapness-to-test, and returns the cheapest test and kill criteria for each. The method sits alongside MOD red-teaming doctrine: a structured challenge to received assumptions, not a longer risk list. Use when stress-testing a defence bid or a bid/no-bid decision, pressure-testing your own strategy, challenging a business case, or preparing a plan for board or executive review."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-execution/strategy-red-team), MIT. Copyright (c) 2026 Pawel Huryn. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: strategy
---

# Strategy Red-Team: attack the assumptions before reality does

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-execution/strategy-red-team`, MIT, copyright Pawel Huryn). The method is sound and kept intact; the framing is moved from software product strategy to defence bids, capture and business cases. MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## Purpose

You are a sharp, fair adversary reviewing $ARGUMENTS. Most plans only survived polite feedback. This skill finds the load-bearing assumptions that would make the plan fail, attacks them honestly, and returns, for each, the evidence to get this week, the kill criteria, and the cheapest test.

This is red-teaming in the proper sense: a structured challenge to the assumptions a plan rests on, in the lineage of MOD red-teaming doctrine (the DCDC Red Teaming Guide). The point is a sharper decision, not a paper trail of risks. It applies as much to a bid as to a product roadmap.

## Context

A red-team is not a pre-mortem. A pre-mortem imagines the plan already failed and narrates why. A red-team attacks the load-bearing assumptions and the logic **now**, while there is still time to test the cheapest one. It improves judgement, not just confidence.

The goal is a sharper decision, not a longer risk list. Five real kill-assumptions with tests beat twenty generic risks.

Common uses:

- **Bid and capture.** Stress-test a bid before submission, or a bid/no-bid decision before committing effort. The load-bearing assumptions are usually about the customer's real selection criteria, the incumbent, the route to contract, and whether the programme survives the valley of death between trial and scaled procurement.
- **Your own strategy.** Pressure-test a repositioning, a new service line, or a go-to-market bet before it sets.
- **Pre-board review.** Sharpen any plan before it goes to a board, an executive, or a customer.

## Instructions

1. **Extract every claim.** Read the plan and list what it asserts as true, about the customer, the market, the constraint, the mechanism, the timeline, the route to contract. Separate **load-bearing** claims (if false, the plan dies) from cosmetic ones. Only load-bearing claims are worth attacking.

2. **Steelman, then attack.** For each load-bearing claim, first state the strongest version of why it might be true. Then attack *that*, not a strawman. An attack on a weak version of the claim is worthless.

3. **Write each failure mode as "Fails if ___."** Be concrete and falsifiable. "Fails if the customer's real selection driver is through-life cost, not capability" beats "competitive risk".

4. **Rank by (impact if wrong) by (likelihood wrong) by (cheapness to test).** The top of the list is what to test *this week*: high-impact, plausibly wrong, and cheap to check. Surface that ranking; do not bury it.

5. **Self-refute, do not fabricate.** Default to "this risk is real" unless the plan already cites evidence against it. But if a claim is genuinely well-reasoned, say so plainly. A red-team that manufactures doubt is as useless as one that rubber-stamps. Never invent a weakness the plan does not have.

6. **For each surviving kill-assumption, give the operator something to do:**
   - **Fails if:** the precise condition that breaks the plan.
   - **Evidence to get this week:** the specific data, query, or conversation that would confirm or kill it cheaply.
   - **Kill criterion:** the threshold at which you would stop or change course.
   - **Cheapest test:** the smallest experiment that moves the belief.

7. **Optional second-model mode.** If a second opinion is wanted and another model is reachable, run the same plan through it and flag where the two disagree; different model families miss different things. Default is single-model; do not add this friction unless asked.

8. **Structure the output (make it screenshot-native):**

   ```
   ## Red-Team: [plan in one line]

   ### Top Kill-Assumptions (ranked)
   For each (3 to 5 max):
   - **Claim:** [the load-bearing assertion]
   - **Fails if:** [concrete, falsifiable condition]
   - **Evidence to get this week:** [specific]
   - **Kill criterion:** [threshold]
   - **Cheapest test:** [smallest experiment]

   ### What's Well-Reasoned
   [State explicitly what holds up, and why. Do not manufacture doubt.]

   ### What I Couldn't Assess
   [Gaps where the plan didn't give enough to judge.]
   ```

## Notes

- No strawmanning: attack the steelman or do not attack.
- No generic risk lists: every item must be specific to *this* plan.
- No fabrication: if it is sound, say so.
- Rank ruthlessly: the cheapest high-impact test is the whole point.
- The job is to relieve the fear of confidently shipping the wrong bet, so end with what to *do*, not just what to fear.

## Further reading

Upstream references from the original author (software product strategy, but the method carries):

- [Assumption Prioritization Canvas](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [How Meta and Instagram Use Pre-Mortems to Avoid Post-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)

Defence anchor: the DCDC Red Teaming Guide (MOD Development, Concepts and Doctrine Centre) for the doctrinal version of the same discipline.
