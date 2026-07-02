---
name: process-map
description: |
  Map one business process through a structured interview and write it up as a
  process page: the steps, who does each, inputs and outputs, pain points, and
  a candidates section flagging what could be automated and what must stay
  human. The foundation skill of the ops wing; sop-capture and ai-readiness
  build on its output. Trigger on any of: "process-map", "map a process",
  "map how we do X", "document this process", "how does X actually work
  around here", "walk through our process for X", or when the user describes
  a repetitive workflow and wants it captured properly.
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

# Process Map

A process that lives only in someone's head cannot be improved, handed over, or automated. Your job is to get one process out of the owner's head and onto a page accurate enough that all three become possible. One process per run; a process map that tries to cover everything covers nothing.

The pack's thesis applies here with full force: a process you can describe is a process you can automate. This skill is the describing, made systematic. The `process-interviewer` meta-skill carries the interviewing craft; use its posture (relentless about specifics, comfortable with silence, never accepting "it depends" as a final answer) without re-reading it ceremonially.

## Before you start

Read `Context/` for what the organisation does, and check `Resources/Ways of Working/Processes/` for an existing map of this process; if one exists, offer to update it rather than duplicate it.

## The interview

Work through these, one at a time, in plain language. Push for the real answer, not the official one; the gap between the documented process and the actual process is usually where the pain lives.

1. **The trigger.** What starts this process? An email, a date, a customer action, a feeling that it's about time?
2. **The steps.** Walk it end to end. For each step: who does it, what they need to start (inputs), what exists when they finish (outputs), what tool it happens in, and roughly how long it takes. Expect five to twelve steps; more means the process wants splitting.
3. **The handoffs.** Where does it pass between people or tools? Handoffs are where processes fail; name each one.
4. **The pain.** Which step gets skipped when busy? Which one produces the errors? Where does it sit waiting?
5. **The volume.** How often does this run: daily, weekly, per customer? Volume decides whether automating is worth it.

## The output

Write to `Resources/Ways of Working/Processes/<Process Name>.md`. Show the draft before saving. Frontmatter: `type: process`, `owner`, `frequency`, `last_reviewed`. Sections:

- **Purpose and trigger.** Two lines.
- **The map.** A Mermaid flowchart of the steps and handoffs (Obsidian renders these natively), followed by a step table: step, who, inputs, outputs, tool, time. Escape pipes in any wikilinks inside the table (`[[path\|display]]`).
- **Pain points.** The honest list from the interview, each tied to a step.
- **Automation candidates.** Steps that are repetitive, rule-based, or high-volume, each with a recommendation: a skill (invoked, stable procedure, varying input), a schedule (time-triggered), or both. Reference the pattern in `How to Use This Vault`.
- **Keep human.** Steps that involve judgement, relationships, or accountability. Naming these is as valuable as naming the automation candidates; it is the answer to "what do I keep to myself".

## What this skill does not do

- It does not map more than one process per run.
- It does not implement any automation it recommends; that is a follow-on decision, usually via `skill-creator` or a scheduled task, taken by the owner.
- It does not write the official version. If the actual process embarrasses the documented one, the page records the actual one, flagged as such; fixing the gap is the owner's call.
