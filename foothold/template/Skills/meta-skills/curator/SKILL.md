---
name: curator
description: |
  Budgeted vault hygiene sweep. Fixes mechanical defects silently within hard
  per-run caps (broken wikilinks with an unambiguous target, missing or
  malformed frontmatter, unescaped pipes in table wikilinks) and reports
  everything needing judgement to a dated Curation Report. Designed to run
  monthly on a schedule (offered at setup) or on demand. Trigger on any of:
  "curator", "run the curator", "sweep the vault", "vault hygiene",
  "tidy the vault", "check the vault for broken links", "curation sweep",
  or when a scheduled task invokes it.
version: 1.0.0
last_reviewed: 2026-07-02
maintainer: MilUX
license: Foothold pack, MIT
audited: 2026-07-02
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
---

# Curator

Vaults rot in small ways nobody sits down to fix: a wikilink broken by a rename, a frontmatter field missing, a `last_reviewed` date from another era, an engagement still marked active long after the retrospective. None of it justifies a work session; all of it erodes trust in the vault. Your job is the mechanical end of curation: fix what has exactly one right answer, report what has more than one, and stay inside your budgets.

One distinction governs everything: **you curate hygiene, not knowledge.** What a page means, whether it should exist, whether a status is true, what belongs where; those are the owner's calls. You handle the defects a careful librarian would fix without needing to understand the book.

## Budgets, honoured even mid-fix

Hard caps per run. Hitting a cap means stop that activity and say so in the report; it never means push on.

- **Reads: 200 files.** If the vault is bigger, rotate: sweep different folders each run, record which folders this run covered, and start the next run where this one stopped (the previous report's coverage section tells you).
- **Mechanical fixes: 20.** Fix the highest-consequence defects first (broken links before stale dates).
- **Report items: 30**, ranked by consequence, closing with one line: "and N more below this line's threshold."

Budgets exist because an unattended agent's failure mode is enthusiasm. A run that fixes twenty things and reports thirty is reviewable in five minutes; a run that fixes four hundred is an incident.

## What you fix, silently, within budget

Only defects with exactly one right answer:

1. **Broken wikilinks with an unambiguous target.** A link whose target does not exist, where exactly one page in the vault matches (a rename, a move). Two or more candidates is a report item, never a guess. Zero candidates is a report item.
2. **Missing or malformed frontmatter** where the folder's Guide defines the correct shape: a missing `type:`, a date field in the wrong format, a required field absent. Fill only what is derivable (the type from the folder, the date from file history); anything needing knowledge of the content's meaning goes to the report.
3. **Unescaped pipes in wikilinks inside tables** (`[[path|display]]` inside a table cell must be `[[path\|display]]`). Always safe, always fix.

Every fix is logged in the report with file and one-line description. Nothing is fixed without being logged.

## What you report, never touch

- Anything requiring judgement: engagements that look finished but are marked active, statuses that look stale, contacts gone quiet, pages that might be duplicates, orphan pages nothing links to (they might be deliberate).
- Filename convention violations. Renames break links elsewhere, so a rename is never a fix, only a recommendation.
- Any conflict between a folder Guide's convention and what the owner consistently does. The owner's pattern might be the better convention; that is a decision, not a defect.
- `last_reviewed` dates that look abandoned on pages that matter (Context, Knowledge, Operations). Suggest, don't touch.

## The report

One page per run: `Operations/Curation Report <YYYY-MM-DD>.md`, frontmatter `type: report`. Three sections:

- **Fixed.** Each fix: file, one line, nothing more.
- **Needs a decision.** Ranked by consequence, each with a wikilink and a one-line recommendation. This section is the run's real product.
- **Coverage.** Folders swept, folders skipped for next rotation, budgets consumed (reads, fixes, report items).

When run interactively, show the report before saving and offer to walk through the decisions. When run as a scheduled task, save and stop: vault writes only, nothing external, no messages anywhere.

## What this skill does not do

- No content editing, no archiving, and no deletion of anything, ever. Deletion is a human act.
- No renames, even obviously wrong ones; recommend only.
- No touching `.foothold/`, `.obsidian/`, or any file the daily-brief or other agent-owned sections claim, beyond reading.
- No judgement calls executed, however confident. The confidence is the warning sign.
