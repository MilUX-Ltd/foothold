---
type: customer-engagement
status: scoping
health: green
last_health_check: {{today_iso}}
customer: "{{customer_wikilink}}"
created: {{today_iso}}
tags: [customer-engagement, scoping, {{folder_name}}]
tracking_card: "{{tracking_card_url}}"
---

# {{title}}

## Overview

{{overview_paragraph}}

## Outcome

{{outcome_one_liner}}

Full outcome detail, including benefits measurement: [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - Outcome|outcome]].

## Customer

- **Organisation:** {{customer_wikilink}}.
- **Primary contact:** {{primary_contact_wikilink}}.
- **Other stakeholders:** see [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - Stakeholder Map|stakeholder map]].

## Information Architecture

Where artefacts for this engagement live, by type. Populated during mobilisation.

| Artefact type | Location for this engagement |
|---|---|
| All in-vault artefacts (index, outcome, stakeholder map, comms plan, RAID, mobilisation checklist, meetings, research, specs, decisions, drafts, deliverables) | This Obsidian folder; subfolders per the Customer Engagements Guide |
| Long-form reference docs, captures, PDFs | Your document archive `<TBC>` |
| Shared working documents, drafts | Your shared drive `<TBC>` |
| Work coordination, comms | Tracking card {{tracking_card_url}} |
| Accounting, invoices | Your accounting system reference `<TBC>` |
| Signed contract, NDA, PO | `<TBC>` |
| Data classification for this engagement | `<TBC — e.g. confidential, restricted, public, sector-specific classification>` |
| Other (per engagement) | `<add as needed>` |

When an external location is confirmed, replace `<TBC>` with the path or URL. Agents working on the engagement read this table to decide where new artefacts land and how to handle the data.

## Current Status

{{current_status_paragraph}}

## Scope and Deliverables

{{scope_paragraph}}

| Deliverable | Acceptance criteria | Sign-off owner | Due |
|-------------|---------------------|----------------|-----|
| `<TBC>` | `<TBC>` | `<TBC>` | `<TBC>` |

Each deliverable should land here with measurable acceptance criteria and a named customer sign-off. Populate during scoping conversations; the table is the contractual basis for "done".

## Definition of Done (engagement level)

`<TBC — one paragraph: when is this engagement complete, what signals it, who confirms it. Distinct from per-deliverable acceptance criteria.>`

## Reporting and Governance Cadence

Formal status reporting, retros, and steering rhythm. Lives separately from the day-to-day comms plan because it informs invoicing milestones and customer governance. See [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - Comms Plan|comms plan]] Reporting Cadence section for the table.

## Change Control

`<TBC — how does a change to scope, timeline, or budget get raised, agreed, and recorded for this engagement. Lightweight is fine: email plus a decision log entry plus a tracking card update. Agree with customer during mobilisation.>`

## Capacity and Availability

`<TBC — agreed days per week on this engagement, blackout periods, holiday windows, and other commitments competing for the same time. State plainly so it is not hidden in conversation history.>`

## Engagement Health

- **Current status:** {{health_status}}.
- **Last health check:** {{today_iso}}.
- **Why this status:** `<TBC — one or two lines explaining the current colour, or "no concerns" when green.>`

Health is reviewed at each formal status report and updated here.

## Key Resources

- [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - Outcome|Outcome]].
- [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - Stakeholder Map|Stakeholder map]].
- [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - Comms Plan|Comms plan]].
- [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - RAID Log|RAID log]].
- [[Customer Engagements/scoping/{{folder_name}}/{{folder_name}} - Mobilisation Checklist|Mobilisation checklist]].
- `decisions/` subfolder. ADR-style decision log; one file per decision using the decisions template.
- {{customer_wikilink}} (CRM organisation).
- Tracking card: {{tracking_card_url}}.

## Next Steps

- Schedule the client alignment activity (workshop, call, or series of conversations). The meeting note will land in `meetings/`.
- Confirm the outcome statement with the customer.
- Fill the Information Architecture table (external storage paths, data classification).
- Walk the stakeholder map with the customer.
- Drop the customer's brief, job spec, or SoW draft into `specs/` when it arrives.
- Agree change control mechanism, invoicing schedule, capacity statement, and reporting cadence with the customer.
- Populate the Scope and Deliverables table with acceptance criteria.
- Work the mobilisation checklist through to "contract signed".
