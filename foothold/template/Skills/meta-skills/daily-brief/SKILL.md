---
name: daily-brief
description: |
  Write today's daily note as a brief FOR the user, generated from everything
  they are working on: engagements, initiatives, outstanding items rolled from
  previous notes, upcoming events and deadlines. The user reads the brief;
  they do not fill in a form. Designed to run on a weekday-morning schedule or
  on demand. Trigger on any of: "daily-brief", "morning brief", "what's on
  today", "write my daily note", "brief me", "start my day", or when a
  scheduled task invokes it.
version: 1.0.0
last_reviewed: 2026-07-02
maintainer: MilUX
license: Foothold pack, MIT
audited: 2026-07-02
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
---

# Daily Brief

The daily note is working memory, and the expensive part of working memory is assembling it. That is your job, not the user's. You read the vault, work out what today actually looks like, and write it down. No standup ceremony, no "what did you do yesterday" ritual, no form to fill. The user's only obligations are to read the brief and to jot things during the day if they want to; everything else is generated.

## What to read

Work from the vault as it is, not from questions to the user. When run interactively, ask nothing unless something is genuinely ambiguous.

1. **The last daily note** (most recent file in `Daily/`): anything under an outstanding or open section rolls forward until it is done or the user kills it.
2. **`Customer Engagements/active/` and `scoping/`**: current state, next actions, anything with a date attached (deadlines, decision dates from eligibility checks, submission dates from bids). Flag anything that has not moved in two weeks.
3. **`Initiatives/`** with `status: active`: same treatment.
4. **`Intelligence/events/`**: anything in the next four weeks worth preparation, and anything this week worth attending.
5. **`CRM/contacts/active contacts/`**: relationships going quiet, where `last-contact` is drifting past the kind of interval the engagement implies. At most two nudges a day; a brief that nags is a brief that gets ignored.
6. **Calendar: probe, don't ask.** Inspect the session's tools for a calendar-shaped connector and, if found, run one read-only probe for today's events. On success, include today's meetings, each with a one-line "who and why it matters" from the CRM. If no connector exists, skip without comment; do not ask the user to dictate their diary. If a connector exists but the probe fails, add one line under Worth knowing naming the error, and only if yesterday's brief did not already carry the same line; a brief that repeats a nag trains the user to stop reading it.

## What to write

Write into today's note (`Daily/YYYY-MM-DD.md`), creating it with the Daily Guide's frontmatter if it does not exist. Per the Daily Guide convention, own the `## Daily Brief` section and never touch anything else in the file; the rest of the note is the user's through the day.

The section, in order, and only the parts that have content today:

- **Today.** Meetings and time-fixed items, each one line.
- **Needs attention.** Deadlines approaching, engagements stalled, decisions waiting on the user. Each one line with a wikilink to where the work lives. Hard cap of seven items; if there are more, the top seven by consequence, and one line saying what was cut.
- **Rolled forward.** Still-open items from previous notes, with the date they first appeared. An item rolling for a week gets flagged as "kill or commit".
- **Worth knowing.** Anything from recent scan notes, new vault content, or events landing later this month. Two or three lines at most.

The whole brief reads in under two minutes. Write like a good chief of staff: declarative, specific, wikilinked, no motivational padding, no emoji, and silence where there is nothing to say. A quiet day's brief is short, and that is a feature.

## Scheduled versus interactive

- **Scheduled** (the normal mode, offered at setup): write the section and stop. Vault writes only; nothing external, no messages sent anywhere.
- **Interactive**: write the section, then offer exactly one follow-up: "want to start on any of these?"

## What this skill does not do

- It does not ask the user to report what they did yesterday. The vault already knows, and if it does not, that is a curation gap, not a ritual gap.
- It does not overwrite or edit the user's own writing in the daily note, ever.
- It does not duplicate canonical content into the note; it links out, per the Daily Guide.
- It does not manufacture urgency. If nothing needs attention, it says so in one line.
