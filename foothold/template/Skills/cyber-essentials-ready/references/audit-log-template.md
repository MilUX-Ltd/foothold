---
type: cyber-essentials-audit-log
machine_name: <FILL_ON_FIRST_RUN>
machine_owner: <FILL_ON_FIRST_RUN>
created: <YYYY-MM-DD on first run>
maintained_by: cyber-essentials-ready skill (Foothold, MilUX)
---

# Cyber Essentials audit log

This file is the append-only history of every time the `cyber-essentials-ready` skill has run on this machine. One row per run, newest at the bottom. Do not delete or edit rows in this file by hand. If a row is wrong, add a correction row below it noting the original date and the correction.

A reviewer reading this file should be able to answer:

- When was this machine first configured for Cyber Essentials?
- How often has it been verified since?
- Have any verify checks failed (drift detected)?
- Was any drift remediated, and when?

For the current state of each control, see [compliance-status.md](compliance-status.md). For the detail of any individual run, see the dated file under `evidence/`.

## Runs

| Date | Time | Mode | Triggered by | Controls checked | Green | Amber | Red | Evidence file | Notes |
|---|---|---|---|---|---|---|---|---|---|
| <YYYY-MM-DD> | <HH:MM> | initial | user | <N> | <N> | <N> | <N> | [<filename>](evidence/<filename>) | First-time setup |
| <YYYY-MM-DD> | <HH:MM> | verify | schedule | <N> | <N> | <N> | <N> | [<filename>](evidence/<filename>) | Monthly check |
| <YYYY-MM-DD> | <HH:MM> | verify | user | <N> | <N> | <N> | <N> | [<filename>](evidence/<filename>) | User-initiated verify |
| <YYYY-MM-DD> | <HH:MM> | remediation | user | <N> | <N> | <N> | <N> | [<filename>](evidence/<filename>) | Drift remediated, see preceding verify row |

## Mode definitions

- **initial**: First-time setup, applied the controls.
- **verify**: Read-only check against the most recent recorded state.
- **remediation**: Re-applied apply mode on a subset of controls after a verify flagged drift.

## Triggered-by values

- **user**: A human asked the skill to run.
- **schedule**: The Cowork scheduled task fired (monthly cadence by default).

## Counts

- **Green**: Control matches recorded baseline or is at the required state.
- **Amber**: Could not determine state (permissions, command failed, control no longer applies after an OS upgrade). Investigate.
- **Red**: Control is looser than the recorded baseline. Requires remediation.

## Append rules for the skill

When the skill writes to this file, it:

1. Loads this file. If missing, creates it from this template (filling the frontmatter `machine_name`, `machine_owner`, `created` fields).
2. Appends one row to the table with the current run's stats.
3. Does not modify any existing row.
4. Saves the file back to `Operations/Cyber-Essentials/audit-log.md`.
