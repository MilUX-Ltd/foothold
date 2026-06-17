---
name: opportunity-solution-tree
description: "Build an Opportunity Solution Tree (Teresa Torres): map a single desired outcome to customer opportunities, candidate solutions, and the experiments that would validate them. Use when structuring discovery, organising opportunities, or deciding what to build or test next. Defence-aware: the outcome is a capability or mission effect, opportunities are customer and user needs."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-product-discovery/opportunity-solution-tree), MIT. Copyright (c) 2026 Pawel Huryn. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: discovery-gtm
---

# Opportunity Solution Tree

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-product-discovery/opportunity-solution-tree`, MIT, copyright Pawel Huryn). Based on Teresa Torres, *Continuous Discovery Habits*. MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## What this is

It structures discovery so a team maps the opportunity space before jumping to solutions. It consumes interview evidence (`interview-script`, `summarize-interview`) and feeds the roadmap and experiments.

## Structure (four levels)

1. **Desired outcome** (top): a single, measurable outcome. In defence this is usually a capability or mission effect expressed as a metric the customer would recognise, drawn from the strategy, not a vanity number.
2. **Opportunities:** customer and user needs and pains from research, framed from their side ("I struggle to..."), not features. Score with the Opportunity Score, Importance x (1 - Satisfaction), normalised 0 to 1; this is the same gap as underservice against something the customer values.
3. **Solutions:** at least three per prioritised opportunity. Ideate across roles, not just the PM; in a defence context that means the operator and the engineer in the room, not only the commercial lead.
4. **Experiments:** fast, cheap tests, with skin in the game over opinion. State hypothesis, method, metric, success threshold.

## Principles

- One outcome at a time.
- Opportunities (problems), not features.
- Generate three solutions before choosing; avoid the first-idea trap.
- Discovery is not linear: loop back, kill what does not validate, open new branches.
- Continuous: update the tree as interviews, analytics and experiments land.

## Method

1. Define or confirm the single desired outcome.
2. Map 3 to 7 opportunities from the research; group related ones.
3. Prioritise the top 2 to 3 by Opportunity Score or judgement.
4. Generate 3+ solutions per prioritised opportunity.
5. Design 1 to 2 experiments for the most promising solutions.
6. Present the full tree in a clear hierarchy; render a visual where it helps.

Save as markdown.

## Notes

- Pairs with `interview-script`, `summarize-interview`, `user-personas`.

## Further reading

- Teresa Torres, *Continuous Discovery Habits*, the source of the OST.
- Dan Olsen, *The Lean Product Playbook*, for the Opportunity Score (Importance x (1 - Satisfaction)).
- Alberto Savoia, *The Right It*, for the skin-in-the-game experiments at the bottom of the tree.
