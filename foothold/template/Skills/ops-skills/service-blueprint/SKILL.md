---
name: service-blueprint
description: |
  Map a customer-facing service as a service blueprint: the customer's journey
  stage by stage against the front-stage actions they see, the back-stage work
  they don't, and the systems underneath, with moments of truth and failure
  points marked. A user-centred design method most small businesses have never
  met. Trigger on any of: "service-blueprint", "blueprint our service", "map
  the customer journey through our service", "why do customers drop out",
  "map our delivery end to end", "service design", or when the user wants to
  see their service the way the customer experiences it.
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

# Service Blueprint

Most owners can describe what their business does; far fewer have ever seen it drawn the way the customer lives it. A service blueprint lines up, stage by stage, what the customer does, what they see, what happens behind the curtain to make it work, and what systems carry it, then marks the moments where the relationship is won or lost. The value is nearly always in the misalignments: back-stage heroics propping up a front stage that looks effortless until the hero is on holiday.

This is an established user-centred design method. Apply it properly; do not water it down into a customer journey poster.

## Before you start

Read `Capabilities and Services/Customer-Facing Services/` for the service's existing page (if the service has no page, offer to create the stub as part of this run), `Context/` for who the customer is, and any engagement history in `Customer Engagements/` that shows how delivery actually went, which outranks how it is supposed to go.

## The interview

1. **Pick one service.** One blueprint per service; a business with three services gets three runs.
2. **The stages.** Walk the customer's journey from first awareness to after the work is done: typically five to eight stages (hear about us, first contact, agree the work, delivery, handover, aftercare). Use the customer's sequence, not the org chart's.
3. **Per stage, four layers:**
   - **Customer actions.** What the customer does and, if known, feels.
   - **Front stage.** What the business visibly does: the email, the meeting, the deliverable.
   - **Back stage.** The work the customer never sees that makes the front stage possible.
   - **Support.** The systems, tools, and third parties underneath.
4. **Moments of truth.** The two or three stages where the customer decides what this business is. Usually first contact, first deliverable, and the first thing that goes wrong.
5. **Failure points and waits.** Where it breaks, where the customer sits in silence, where back-stage load is invisible until someone is off sick.

## The output

Write to `Capabilities and Services/Customer-Facing Services/<Service> Blueprint.md`, wikilinked from the service's page. Show the draft before saving. Frontmatter: `type: service-blueprint`, `service`, `last_reviewed`. Sections:

- **The service in one line.**
- **The blueprint.** One table, stages as rows, the four layers as columns. Escape pipes in any wikilinks inside the table (`[[path\|display]]`). Mark moments of truth in bold and failure points with a flag the reader cannot miss.
- **What the blueprint shows.** Three to five plain observations: the misalignments, the silent waits, the single points of failure. This section is why the exercise was worth an hour; do not skip it or pad it.
- **Candidates.** Failure points and back-stage load that `process-map` should map next, wikilinked if maps already exist.

## What this skill does not do

- It does not survey customers or invent their feelings; where the customer's side is unknown, it says unknown, which is itself a finding.
- It does not redesign the service; it makes the current one visible. Redesign is the owner's next decision, better made with the blueprint on the table.
- It does not blueprint internal processes; that is `process-map`'s job.
