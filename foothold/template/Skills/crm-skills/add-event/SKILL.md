---
name: add-event
description: Capture a new event into the vault. Logs attendance, attendees, organisations represented, and key threads. Applies the Chatham House Rule check at intake. Files the event into the right community folder. Use when the user says "add an event", "log an event", "capture an event", "I attended <event>", "we just ran <event>", or runs /add-event. Distinct from add-contact (people) and add-organisation (companies). For RDSC events specifically, this skill handles them naturally; if a future version of the pack ships a more specialised /add-cluster-event skill, fall back to it.
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
license: MIT
---

# add-event

USE WHEN the user runs `/add-event` or asks to capture a new event (conference, cluster meeting, meetup, workshop, exercise) into the vault. Distinct from `add-contact` (people) and `add-organisation` (companies).

## Pre-flight

Confirm you're in a Foothold pack: `CLAUDE.md` at vault root, `Intelligence/events/` exists. If not, suggest `/foothold-setup` first.

If the user said something generic like "add an event" without details, ask: "Which event? Give me the name, the date, and who ran it."

## Phase A — Gather identity

Collect:

- **Event name.** Required. The name as it was advertised.
- **Date.** Required. ISO format (YYYY-MM-DD). If the event spans multiple days, use the start date and note the span in the body.
- **Community / organiser.** Required. Which network, organisation, or series ran it. Examples: a specific RDSC, a named conference series, a meetup community, a one-off run by a specific organisation.
- **Location.** Required if attended in person. Venue name and city is enough.
- **Status.** Required. Is the user reporting on something they attended, or scoping something upcoming?
  - `attended` — past, the user was there.
  - `upcoming` — scheduled, the user plans to attend.
  - `scoping` — being investigated, no commitment yet.

## Phase B — Chatham House check

Apply the Chatham House Rule check at intake. Ask:

> "Was this event held under the Chatham House Rule, or is any of it CHR-flagged?"

If yes, set `chatham_house: true` in frontmatter and tag the file `#chatham-house-rule`. Add a one-line banner under the title:

> *Held under the Chatham House Rule. Speaker identity and affiliation should be stripped from any public output drawn from this note.*

If no, set `chatham_house: false`.

This affects how downstream skills (LinkedIn writers, briefing skills) process the content. The flag is non-negotiable; better to over-flag than under-flag.

## Phase C — Classify subfolder

Determine where the event note lives. Use this logic:

1. **If the community is a formal network with a folder in `Intelligence/events/`**, use that folder. For RDSC events, that's `Intelligence/events/Regional Defence and Security Clusters/<Region>/`.
2. **If the community has a recurring series folder that exists** (`Intelligence/events/<Series Name>/`), use it.
3. **If the community is likely to recur but doesn't yet have a folder**, ask the user: "I'll create `Intelligence/events/<Community>/` as the home for future events from this community. OK?" If yes, create the folder and use it.
4. **If genuinely one-off**, drop it in `Intelligence/events/one-off/`.

Use Glob on `Intelligence/events/` to see what folders exist before asking.

## Phase D — Gather attendees and organisations

Ask the user:

> "Who was there that's worth noting? List the people (names and orgs if you can) and the organisations represented."

Parse the user's response into two lists:

- **Attendees** — named individuals.
- **Organisations** — companies, MOD bodies, academic institutions that had a presence.

For each attendee and organisation, check whether they exist in CRM:

- Use Glob on `CRM/contacts/active contacts/` and `CRM/contacts/reference contacts/` to find existing contacts.
- Use Glob on `CRM/organisations/` (recursive) to find existing orgs.

If a person or org isn't in CRM, surface that to the user at the end of the skill (in Phase I) rather than blocking the event capture. Suggest running `/add-contact` or `/add-organisation` for the missing ones.

## Phase E — Gather threads and outstanding actions

Ask:

> "Anything worth capturing from the event? Key conversations, decisions, things you committed to follow up, observations on the room?"

Parse the response into:

- **Key threads.** Substantive conversations or observations. Each gets a short heading.
- **Outstanding actions.** Things the user owes someone, or expects from someone. These should be tick-listed.

If the event is `upcoming` or `scoping`, threads and actions probably don't apply yet; the event note carries the pre-event prep instead. Adjust the body sections accordingly.

## Phase F — Draft

Draft the event note in memory.

For an attended event:

```yaml
---
type: event
date: <YYYY-MM-DD>
community: <wikilink to network or organisation>
event_series: <named series if applicable>
status: attended
location: <venue>
chatham_house: true | false
attendees:
  - <wikilink for each contact who's in CRM>
  - <plain text for any not yet in CRM>
organisations:
  - <wikilink for each org in CRM>
tags: [<contextual tags, including chatham-house-rule if applicable>]
---

# <YYYY-MM-DD> <Community> — <Event Name>

> *Held under the Chatham House Rule. Speaker identity and affiliation should be stripped from any public output drawn from this note.* <If CHR applies.>

## Overview

<One or two paragraphs: what the event was, where, who ran it, the audience.>

## Attendees worth noting

<Bullet list of named individuals the user flagged. Wikilinked into CRM/contacts/ where they exist. Each gets a one-line note on context if the user gave one.>

## Organisations represented

<Bullet list of orgs the user flagged. Wikilinked into CRM/organisations/ where they exist.>

## Key threads

### <Thread title>

<One paragraph capturing the substance of the thread.>

<Repeat per thread.>

## Outstanding actions

- [ ] <Action with owner and date if known.>

## Source attachments

<Links to any binary attachments in the reference library (DEVONthink or equivalent). Use `x-devonthink-item://...` URLs if DEVONthink, or the equivalent canonical URL for other systems.>
```

For an upcoming or scoping event, drop the "Key threads" and "Outstanding actions" sections, and add a "Pre-event prep" section instead.

## Phase G — Confirm

Show the draft. Ask:

> "Here's the event note I'd write to `Intelligence/events/<path>/<filename>.md`. Anything to change before I save it?"

Wait for explicit confirmation.

## Phase H — Write

Filename convention: `YYYY-MM-DD <Community> — <Event Name>.md`. The community in the filename is intentional redundancy and helps cross-folder search.

Write to the determined path.

## Phase I — Cross-reference and follow-ups

After writing:

1. **Missing CRM entries.** List any attendees or organisations the user mentioned that aren't yet in CRM. Suggest running `/add-contact` or `/add-organisation` for each.
2. **Reference-library attachments.** If the user mentioned slides, photos, recordings, or other binaries, prompt them to file these in their reference library and add the link to the event note's "Source attachments" section.
3. **Follow-ups to action.** Surface the outstanding actions back to the user as a closing recap.

## Guidelines

- Chatham House check is mandatory at intake. Never skip it.
- One file per event. Date in filename. Community in filename.
- Wikilink attendees and organisations into CRM where they exist; flag missing ones for the user to add.
- Binary attachments go in the reference library, not the vault. Link them from the event note.
- Confirm before writing.
