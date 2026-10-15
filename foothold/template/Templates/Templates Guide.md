---
type: guide
folder: Templates
---

# Templates Guide

## Purpose

`Templates/` holds the note templates that Obsidian's Templates plugin inserts: one for each kind of note the Guides define. A template gives a new note the right frontmatter and section headings from the start, so notes of one kind look alike, and the dashboard on `Home.md` and the skills can rely on them.

Two folders have similar names. This one holds **note templates**, small and filled in often. `Resources/Templates/` holds **document templates** such as a deck or a meeting agenda; see [[Resources/Templates/Templates Guide|its Guide]].

## Structure

```
Templates/
├── Templates Guide.md          (this file)
├── Contact.md
├── Organisation.md
├── Customer Engagement.md
├── Initiative.md
├── Idea.md
├── Daily Note.md
├── Weekly Review.md
├── Meeting.md
├── Marketing Output.md
└── Service.md
```

| Template | `type:` | Where the note lives | Guide |
|---|---|---|---|
| Contact | `contact` | `CRM/contacts/` | [[CRM/contacts/Contacts Guide\|Contacts Guide]] |
| Organisation | `organisation` | `CRM/organisations/` | [[CRM/organisations/Organisations Guide\|Organisations Guide]] |
| Customer Engagement | `customer-engagement` | `Customer Engagements/` | [[Customer Engagements/Customer Engagements Guide\|Customer Engagements Guide]] |
| Initiative | `initiative` | `Initiatives/` | [[Initiatives/Initiatives Guide\|Initiatives Guide]] |
| Idea | `idea` | `Ideas/` | [[Ideas/Ideas Guide\|Ideas Guide]] |
| Daily Note | `daily-note` | `Daily/` | [[Daily/Daily Guide\|Daily Guide]] |
| Weekly Review | `review` | `Daily/Reviews/` | [[Daily/Daily Guide\|Daily Guide]] |
| Meeting | `meeting-note` | the `meetings/` folder of an engagement or initiative | [[Customer Engagements/Customer Engagements Guide\|Customer Engagements Guide]] |
| Marketing Output | `linkedin-post`, `case-study` or `news-article` | `Marketing/Marketing Outputs/` | [[Marketing/Marketing Outputs/Marketing Outputs Guide\|Marketing Outputs Guide]] |
| Service | `service` | `Capabilities and Services/` | [[Capabilities and Services/Capabilities and Services Guide\|Capabilities and Services Guide]] |

## Writing a note from a template

**Set Obsidian up once (about a minute).** In Obsidian, open Settings:
- **Core plugins:** turn on Templates and Daily notes.
- **Templates:** set "Template folder location" to `Templates`.
- **Daily notes:** set "New file location" to `Daily`, "Template file location" to `Templates/Daily Note`, and "Date format" to `YYYY-MM-DD`.
- **Files and links:** set "Default location for new notes" to `Inbox` and "Default location for new attachments" to `Attachments`.

The pack does not change your Obsidian settings for you, so your own theme and plugins are never overwritten by an update.

1. Create the note where it belongs, using the table above, and name it as the Guide says. If you just want to capture something quickly, let it land in `Inbox/` and file it later.
2. Open the command palette and run **Templates: Insert template**, then pick the template.
3. Fill in the title, today's date in `created` and `updated` (YYYY-MM-DD), and what else you know. Delete a section that has nothing to say yet; an empty heading is clutter.

Daily notes are the exception: once the Daily notes plugin points at the Daily Note template, opening today's daily note creates it from the template. Its `date:` field and heading start blank, like every template; fill them in, or ask your assistant to.

A few templates stand in for a family of notes. Change `type:` on the Marketing Output template to `case-study` or `news-article` when that is what you are writing. Set `customer-facing: false` on the Service template for an internal service. Put a meeting note in the `meetings/` folder of the engagement or initiative it belongs to, named `YYYY-MM-DD <title>.md`.

This Guide sits in the same folder, so it appears in the Insert template list too; just skip it.

**Dates and titles are blank on purpose.** The templates leave the title and date fields empty for you (or your assistant) to fill in when you create the note, so nothing is stamped with the wrong date.

## Lifecycle

Templates are not notes, so they carry no status. Editing a template changes only the notes you create from it afterwards; notes you have already written keep the frontmatter they have. Change a template when the Guide for its note type changes, and keep the two in step.

The statuses a note can take belong to the note type, not the template. Each template starts a note at the first status for its type (a contact is `active`, an engagement is `scoping`, an idea is `raw`). The allowed values are in the Guide for the type and in rule R-07 in `Knowledge/rules.md`.

`/curator` leaves this folder alone, because a template's frontmatter is deliberately unfinished.

## Frontmatter

Every template carries the common fields that suit its note type (`type`, `status`, `created`, `updated`, `tags`) and then the fields its own Guide defines, for example `customer` and `health` on an engagement or `lawful_basis` on a contact. Nothing is invented here: if a field is in a template, it is in the Guide.

Some values are left empty for you to fill in. Links go in quotes, as wikilinks (`customer: "[[CRM/organisations/Acme|Acme]]"`), and lists are YAML lists. The full convention is rule R-07 in `Knowledge/rules.md`.

## Canonical example

The Contact template, filled in for a new note called `Jane Smith`:

```yaml
---
type: contact
name: "Jane Smith"
organisation: ""
role: ""
email:
linkedin:
phone:
status: active
created: 2026-05-20
updated: 2026-05-20
last-contact: 2026-05-20
lawful_basis: legitimate-interests
tags:
  - lb-legitimate-interests
---
```

Fill in `organisation` with a quoted wikilink, and change `lawful_basis` and its matching `lb-` tag together if the default does not fit.

## Related

- [[Knowledge/rules|Rules]]: R-07 sets the frontmatter convention the templates follow.
- [[Resources/Templates/Templates Guide|Resources Templates Guide]]: document templates, which are a different thing.
- [[Inbox/Inbox Guide|Inbox Guide]]: where new notes land before you file them.
