---
type: guide
folder: Intelligence/events
status: active
created: 2026-05-20
last_reviewed: 2026-05-20
tags: [guide, intelligence, events]
---

# Events Guide

## Purpose

`Intelligence/events/` holds the events you attend, run, or track. Each event is a piece of intelligence about what other organisations are doing in your sector; the notes themselves are yours.

Events serve three jobs in the vault:

- **Pipeline signal.** What's coming up in the calendar, which clusters or communities are running it, and which contacts will be there.
- **Network intelligence.** What other organisations are doing, who's speaking, what themes are being discussed. Notes capture observations and quotes (with Chatham House Rule applied where stated).
- **Relationship anchor.** Each event links back to the contacts and organisations it surfaces, so the network graph stays connected.

## Structure

Events are organised by the community or series that runs them. The structure typically mirrors `CRM/networks/` for formal networks and adds top-level folders for other communities and series.

```
Intelligence/events/
├── Events Guide.md
├── Regional Defence and Security Clusters/   (mirrors CRM/networks/.../clusters/)
│   ├── East/
│   ├── London/
│   ├── South Central/
│   └── South West/
├── <Conference Series>/                       (e.g. annual industry conferences)
├── <Meetup Series>/                           (recurring local meetups)
├── <Annual Exercise>/                         (e.g. Firebreak)
└── one-off/                                   (events not tied to a recurring series)
```

When a new community surfaces and earns repeat attendance, give it its own folder. Until then, one-off events live in `one-off/`.

## Frontmatter

```yaml
---
type: event
date: YYYY-MM-DD
community: "[[CRM/networks/.../X|X]]"   # or "[[CRM/organisations/.../Y|Y]]" for org-led events
event_series: <name>                      # e.g. SWRDSC, an industry conference, a meetup series
status: attended | upcoming | scoping
location: <venue>
chatham_house: true | false
attendees:
  - "[[CRM/contacts/active contacts/X|X]]"
organisations:
  - "[[CRM/organisations/.../Y|Y]]"
tags: []
---
```

The `community` field is the primary back-link into CRM. Where the parent isn't a formal network (e.g. a meetup), point at the organising organisation's CRM page if one exists, or leave the field as a free-text descriptor for now.

## How events link back

The connective tissue is wikilinks. Every event note carries:

- A `community` wikilink to the network or organisation that ran it.
- An `attendees` list of contacts from `CRM/contacts/`.
- An `organisations` list of orgs from `CRM/organisations/` that were represented or spoke.
- Inline mentions wikilinked to their canonical CRM entries.

Open any CRM contact or organisation and the graph back-references the events they appeared at.

## Attachments

The vault holds the event note. Large binaries (PDFs, slide decks, photos, diagrams, recordings) belong in your reference library (DEVONthink, Apple Notes, a Notion archive, your choice) and get linked from the event note. Keep the vault lean: PDFs, PNGs, SVGs, and similar are not stored in Obsidian.

If your reference library is DEVONthink, link the records using `x-devonthink-item://` URLs. If something else, use the equivalent canonical URL.

## Add discipline

- A new event lands in its community folder. If no folder exists and the community is likely to recur, create the folder. If genuinely one-off, drop in `one-off/`.
- Filenames follow `YYYY-MM-DD <Community> — <Event Name>.md`. The community in the filename is intentional redundancy and helps cross-folder search.
- Apply the Chatham House check at intake. If the event is held under CHR, set `chatham_house: true` and tag the file `chatham-house-rule`. Public output sourced from CHR-flagged material strips speaker identity and affiliation.
- Drop binary attachments into your reference library, not the vault. Link the record from the event note's "Source attachments" section.

## Pairing with a prep skill

Events typically warrant a preparation pass: who's there, what they care about, what threads are open, what you want from the encounter. That's a natural fit for a Foothold-style skill.

A simple event-prep skill would:

1. Take an event name or upcoming-event wikilink as input.
2. Resolve the event's `attendees` and `organisations` from the event note's frontmatter.
3. Pull the relevant CRM context for each (open threads, last contact, things outstanding).
4. Draft a one-page prep brief: who you're seeing, what to bring up, what to ask, what to follow up on.

See [[Skills/Skills Guide|Skills Guide]] for the skill authoring pattern. Foothold ships with a few baseline skills; an event-prep skill is a natural next addition once your vault has enough event and CRM content for it to draw on.

## Canonical examples

The Foothold defaults don't ship populated example events; you'll generate your own. As you add the first few, follow the naming convention and frontmatter shape above, and the structure will reveal itself.

## Related

- [[Intelligence/Intelligence Guide|Intelligence Guide]] — parent
- [[CRM/networks/Regional Defence and Security Clusters/Regional Defence and Security Clusters|Regional Defence and Security Clusters]] — for cluster events
- [[CRM/CRM Guide|CRM Guide]] — where the entities mentioned in events live
- [[Skills/Skills Guide|Skills Guide]] — for event-prep and other event-adjacent skills
