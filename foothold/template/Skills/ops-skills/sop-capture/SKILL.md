---
name: sop-capture
description: |
  Turn a mapped or described process into a runnable standard operating
  procedure: numbered steps a competent person could follow cold, explicit
  decision points, and a what-good-looks-like check at the end. Reads the
  process page from process-map where one exists. Trigger on any of:
  "sop-capture", "write an SOP", "write this up as a procedure", "document
  this so someone else can do it", "standard operating procedure",
  "turn this process into an SOP", or when the user wants a process made
  handover-ready.
version: 1.0.0
last_reviewed: 2026-07-02
maintainer: MilUX
license: Foothold pack, MIT
audited: 2026-07-02
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
replicated_from: Footing v2.0.0
---

# SOP Capture

A process map says what happens; an SOP says exactly how to do it, written for the person who was not in the room. The test of a good SOP is brutal and simple: could a competent newcomer follow it cold, without asking the author anything? Every choice you make while writing serves that test.

## Before you start

Check `Resources/Ways of Working/Processes/` for a process-map page covering this process. If one exists, it is your primary source; the interview then only fills gaps. If none exists, offer to run `/process-map` first (the happy path, because the map surfaces the pain points an SOP should design around), or proceed from the user's raw description if they prefer speed.

## What to establish beyond the map

1. **The audience.** Who will actually run this: the owner on a bad day, a new hire, a virtual assistant, an agent? Write to the least-context reader named.
2. **The exact how of each step.** The map says "invoice the client"; the SOP says which system, which template, which fields, what the subject line is, and what to do when the client is new. Push for screenshots-in-words precision.
3. **The decision points.** Every place the path forks gets an explicit if/then. An SOP with hidden judgement calls is a map wearing an SOP's clothes.
4. **The failure recoveries.** For the two or three most likely things to go wrong: what does the runner do, and who do they tell?

## The output

Write to `Resources/Ways of Working/SOPs/<Process Name> SOP.md`. Show the draft before saving. Frontmatter: `type: sop`, `owner`, `audience`, `review_date` (six months out by default; an SOP without a review date is a future lie). Sections:

- **Purpose.** One line: what this procedure achieves and when to run it.
- **Before you begin.** Access, tools, and inputs the runner must have.
- **The procedure.** Numbered imperative steps. One action per step. Decision points as indented if/then. No step may depend on knowledge that is not in the SOP or linked from it.
- **What good looks like.** The completion check: the observable state that means it worked.
- **When it goes wrong.** The recovery paths from the interview.

## The quiet payoff

Tell the user this at the end, once: an SOP written to this shape is most of a skill specification. If this procedure runs often and the steps are stable, the same content can become a skill the vault executes rather than a page a human follows; the pattern-watching habit in `How to Use This Vault` covers when that jump is worth making.

## What this skill does not do

- It does not invent steps the user did not describe; a gap is recorded as a gap, flagged for the owner.
- It does not write policy (what people are allowed to do); it writes procedure (how a thing is done). Policy belongs in `Knowledge/`.
- It does not automate anything itself.
