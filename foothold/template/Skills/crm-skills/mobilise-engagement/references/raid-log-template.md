---
type: raid-log
engagement: "[[Customer Engagements/scoping/{{folder_name}}/{{folder_name}}|{{title}}]]"
customer: "{{customer_wikilink}}"
status: open
created: {{today_iso}}
---

# {{title}} — RAID

Single combined log. Risks, actions, issues, dependencies. Whatever needs addressing for this engagement goes here. The distinction between types doesn't matter; what matters is that it's tracked and worked.

## Log

| ID | Date raised | Description | Owner | Status | Due | Notes |
|----|-------------|-------------|-------|--------|-----|-------|
| R-1 | {{today_iso}} | Outcome statement needs customer confirmation | `<owner>` | Open | First scoping call | Seeded by mobilisation |
| R-2 | {{today_iso}} | Information Architecture needs external storage paths confirmed | `<owner>` | Open | Before first artefact created | Seeded by mobilisation |
| R-3 | {{today_iso}} | Stakeholder map skeleton needs review | `<owner>` | Open | Before customer alignment | Seeded by mobilisation |

## Status values

- **Open.** Live, not yet actioned.
- **In progress.** Being worked.
- **Resolved.** Closed out. Keep the row for audit.
- **Parked.** Deferred, with a date and reason. Review at the next scoping or weekly pass.

## Adding new entries

Increment the ID (`R-4`, `R-5`, ...). Date raised. One-line description. Owner. Status. Due date if there is one. Notes.

When an entry resolves, set status to Resolved and add the resolution to Notes. Do not delete.
