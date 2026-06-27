---
name: meeting-prep
description: "Prepare a briefing for an upcoming meeting. Pulls relevant context from the vault and from any connected tools (calendar, CRM, email, chat). Use when the user says 'prep me for my meeting with [person/org]', 'brief me on [person] before our call', 'what do I need to know for my [event] meeting', or runs /meeting-prep."
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
license: MIT
---

# Meeting Prep

Produce a tight, useful briefing for a specific upcoming meeting. Pulls from the vault first, then from any connected operational systems the user has wired up.

## Step 1 — Identify the meeting

Determine who the meeting is with and when. If the user named a person or organisation, use that. If vague, check today's calendar (if the user has a calendar tool connected) and ask which meeting to prep for.

## Step 2 — Vault context

Search the Obsidian vault for relevant files:

1. **Contact.** Check `CRM/contacts/` (both `active contacts/` and `reference contacts/`) for a file matching the person's name. Read it if found.
2. **Organisation.** Check `CRM/organisations/` (all sector subfolders) for a file matching the company. Read it if found.
3. **Initiatives.** If the contact or org file references a current initiative, read the relevant initiative file from `Initiatives/active/` or `Initiatives/completed/`.
4. **Past meetings.** Search `Intelligence/events/` and any meeting-note subfolders under initiatives for previous meeting notes involving this person or organisation.
5. **Network.** Check `CRM/networks/` for any network the person is associated with.

## Step 3 — External context (optional, only if tools are wired)

If the user has any of these connected via MCP or otherwise, draw on them. Skip each one cleanly if not available.

- **CRM tool** (HubSpot, Pipedrive, etc.) — search for the contact by name or email. Pull any associated deals (stage, value, last activity) and recent notes.
- **Email** — search for recent threads with this person (last 30 days). Read the most recent three to five and summarise key topics, outstanding requests, and tone.
- **Chat** (Slack, Teams) — search for recent mentions of this person or their organisation. Summarise relevant internal discussion.
- **Project tracker** — search for any pages or database entries related to this person or organisation.

If a source is unavailable or returns nothing, skip that section with a brief note. Never let one failure block the brief.

## Step 4 — Assemble the brief

Present the brief directly in the conversation. Do not create a file unless the user asks. Use this structure:

```markdown
**Meeting Prep: <Person or Org Name>**
**Date:** <meeting date and time if known>

**Who they are**
<Role, organisation, relationship to your business — from vault contact/org file. If no file exists, note that and use whatever was found from external sources.>

**Relationship history**
<Previous meetings, how they connected, key interactions — from vault meeting notes and email threads.>

**Commercial status**
<Deal information if your CRM has a record — stage, value, last activity. Or "No active deals." or "No CRM connected.">

**Recent comms**
<Summary of recent email threads and chat mentions. Key topics, outstanding asks, tone.>

**Open items**
<Any action items the user owes them, or they owe the user — from emails, vault notes, daily-note action items.>

**Talking points**
<Three to five suggested talking points based on the above. Tie back to relevant initiatives or strategic priorities from `Context/Strategy.md` where appropriate.>
```

## Notes

- Be concise and sharp. The user wants useful intel, not a novel.
- If no vault file exists for the person, offer to run `/add-contact` after the meeting.
- Link to vault files using wikilink syntax where relevant.
- Match the language and tone preferences in `Context/Brand.md` if it's populated.
