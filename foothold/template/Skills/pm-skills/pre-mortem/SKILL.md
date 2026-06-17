---
name: pre-mortem
description: "Run a pre-mortem on a plan, bid, launch or mobilisation: imagine it has failed and work back to the real risks. Sorts risks into Tigers (real), Paper Tigers (overblown) and Elephants (unspoken), classifies Tigers as blocking, fast-follow or track, and writes action plans for the blockers. Use when stress-testing a plan before committing. The forward complement to strategy-red-team."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-execution/pre-mortem), MIT. Copyright (c) 2026 Pawel Huryn. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: strategy
---

# Pre-Mortem

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-execution/pre-mortem`, MIT, copyright Pawel Huryn). MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## What this is, and how it pairs with strategy-red-team

A pre-mortem imagines the plan has already failed and works backward to why. It is the **forward complement** to `strategy-red-team`: the red-team attacks the load-bearing assumptions now; the pre-mortem assumes failure and surfaces what the team is not saying. Use the red-team to test whether the logic holds; use the pre-mortem near a commit point (a bid submission, a launch, a mobilisation) to catch the hidden worries while there is still time to act.

## Method

1. **Read the plan.** A bid, a launch plan, a mobilisation plan, a PRD. Understand the objective, the assumptions, the timeline. Use web research on the market or competition where it helps.

2. **Imagine the failure.** Picture the thing going live in 14 days, then picture it failing: the customer does not adopt, the bid loses, the mobilisation slips, reputation takes a hit. What went wrong? What did the team miss or under-execute? What were they overconfident about?

3. **Sort the risks:**
   - **Tigers:** real problems you can see, backed by evidence or experience. They need action.
   - **Paper Tigers:** concerns others raise that you judge overblown. Document them to align stakeholders, do not spend on them.
   - **Elephants:** unspoken worries nobody is validating. Could be real; investigate before commit.

4. **Classify each Tiger:** blocking (must fix before commit), fast-follow (fix within 30 days), or track (monitor, fix if it bites).

5. **Action plans for blocking Tigers:** the risk, a concrete mitigation, the best owner, a decision or completion date.

6. **Structure the output:** Tigers, Paper Tigers, Elephants, then action plans for the blockers.

Save as markdown.

## Notes

- Constructive, not blame. Default to Tiger when unsure; better to address a risk early.
- Bring cross-functional and operator perspectives in, not just the commercial view.
- Revisit two to three weeks before the commit to check mitigations are on track.
- Pairs with `strategy-red-team` and `stakeholder-map`.

## Further reading

- Gary Klein on the pre-mortem technique.
- [How Meta and Instagram use pre-mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template).
