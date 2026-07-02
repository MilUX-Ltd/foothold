---
type: guide
folder: Daily
---

# Daily Guide

## Purpose

`Daily/` is your daily-notes folder. One file per working day. The day's notes, what happened, what was decided, what's outstanding. The closest thing your vault has to a working journal.

Daily notes are the entry point for agents that run on a cadence (morning briefings, signal scans, weekly reviews) and for you when you want a quick "what was I doing last Tuesday?" lookup.

## Structure

```
Daily/
├── Daily Guide.md          (this file)
├── 2026-05-20.md           (today's daily note)
├── 2026-05-19.md
└── ...
```

Flat folder. One file per day, named `YYYY-MM-DD.md`. ISO date format only. The flatness matters: Dataview and similar plugins query daily notes much more easily when they share a single folder.

Some operators add subfolders for weekly or monthly reviews (`Daily/Reviews/2026-W21.md`). That's fine if the cadence justifies it. Keep daily notes themselves at the root.

## Frontmatter

```yaml
---
type: daily-note
date: YYYY-MM-DD
---
```

Optional fields:
- `tags:` for thematic flagging.
- `weather:` if you like that kind of thing.
- Per-agent runtime fields (`signal_scan_completed: true`) for scheduled tasks that write to the note.

## Add discipline

**One file per working day.** The `/daily-brief` skill can create it for you each morning, with the day's brief already written from what you are working on; you then add to it through the day. If you prefer to start it by hand, that works too. Either way, close out at the end with what's still open.

**Sections that work well.** Most operators converge on something like:
- Top of the file: today's focus, in one or two lines.
- Through the day: a running log of what happened, decisions made, things to follow up.
- Bottom of the file: what's outstanding to roll into tomorrow.

**Don't recreate other folders' content here.** Daily notes are working memory, not canonical knowledge. Decisions worth keeping move into `Initiatives/`, `Knowledge/`, or the relevant Context page. Contacts you met today go into `CRM/contacts/`. Daily notes link out; they don't try to own everything.

**Scheduled-task output.** If you have agents that write to daily notes (a morning briefing skill, a signal scan), they should write into specific sections rather than overwriting the file. Convention: agent-written sections use a `## ` header that the agent owns, like `## Morning Briefing` or `## Signal Scan`. You write everywhere else.

## Canonical example

A minimal daily note:

```markdown
---
type: daily-note
date: 2026-05-20
---
# 2026-05-20

## Focus

Foothold v1 install testing.

## Notes

- Pushed v0.2.0 to the marketplace. MilUX organisation page added.
- /foothold-update worked end-to-end. New file appeared, existing content untouched.
- Next: finish the remaining per-folder Guides.

## Outstanding

- Write the remaining 8 Guides.
- Push the canonical example content (Initiative, daily note, LinkedIn post, Idea).
```

Plain and short. The discipline is daily, not detailed.
