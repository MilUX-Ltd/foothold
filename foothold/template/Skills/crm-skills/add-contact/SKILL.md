---
name: add-contact
description: Add a new contact to the CRM. Pulls public information about the person, drafts a contact page, asks the user to confirm before writing. Use when the user says "add a contact", "add <name> to my CRM", "capture <name>", "I met <name>", "log this person", or runs /add-contact. Distinct from add-organisation (which handles companies and MOD bodies) and add-event (which handles events and conferences).
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
---

# add-contact

USE WHEN the user runs `/add-contact` or asks to capture a new person they've met into the CRM. Distinct from `add-organisation` (companies, MOD bodies) and `add-event` (events, conferences).

## Pre-flight

Confirm you're in a Foothold pack: check that `CLAUDE.md` exists at the vault root and that `CRM/contacts/` exists. If not, tell the user the skill needs a Foothold vault; suggest running `/foothold-setup` first.

If the user just said something like "add a contact" without naming the person, ask: "Who would you like to add?" and wait for the name (or a LinkedIn URL).

## Phase A — Gather identity

Collect the basics:

- **Full name.** Required.
- **Organisation.** Required if known. If the user only knows the company name, accept it; you'll resolve organisation existence in Phase F.
- **Role.** Required if known.
- **Email.** Optional.
- **LinkedIn URL.** Optional but strongly preferred. Unlocks the research pass.
- **Phone.** Optional.
- **How you met / context.** Optional but useful. One or two sentences.

Accept paste from the user: a forwarded email signature, a LinkedIn URL, a vCard, or a free-text "I met Jane Smith at the South Central RDSC event yesterday; she's at Acme Ltd, runs their defence division." Parse what you can.

## Phase B — Research

If a LinkedIn URL was provided, call WebFetch on the URL. Extract publicly available fields:

- Headline (one-line professional positioning).
- About section.
- Current role.
- Location.
- Mutual connection count (if visible).
- Any publicly featured posts or articles.

If a company website was provided or you can derive one, fetch the About / Leadership page to confirm the person's role and any public bio.

**Critical:** use only publicly visible information. Do not infer or fabricate personal details. If a field is unknown, leave it out rather than guess.

If no public-source URL was provided, skip the research pass and work from what the user told you.

## Phase C — Classify

Determine whether the contact is **active** or **reference**.

Ask if not obvious from context:

> "Is this someone you have a working relationship with, or someone you need a pointer page for but don't directly engage with?"

- **Active** if the user has a working relationship or recent conversation.
- **Reference** if it's a domain figure or named expert with no personal engagement.

Default to active if the user has just said "I met them" or otherwise indicated direct contact.

## Phase C2 — Lawful basis

Every contact records the UK GDPR Article 6 lawful basis on which their personal data is processed. Ask the user which applies, using the AskUserQuestion tool, and **present the most likely basis first as the recommended option**. Infer the recommendation from what you already know:

- The person is a **client contact, an associate, a contractor, or someone you have or are about to have a contract with** → recommend **contract**.
- The person has **actively opted in to a specific use** (newsletter, marketing list) → recommend **consent**.
- The contact exists for an **accounting or tax record** you must keep by law → recommend **legal-obligation**.
- **Otherwise** (prospects, network contacts, partners, most additions) → recommend **legitimate-interests**. This is the default for B2B relationship-holding.

Offer the four bases as options, recommended one first:

1. `legitimate-interests` — B2B relationship-holding; the usual default.
2. `consent` — they actively opted in; withdrawable.
3. `contract` — necessary for a contract with them, or steps before one.
4. `legal-obligation` — required by law, e.g. accounting records.

Carry the chosen value into the frontmatter as `lawful_basis:` and the matching `lb-*` tag in Phase D. See `Knowledge/tagging-policy.md` for the full definitions.

## Phase D — Draft

Draft the contact page in memory before writing. Use this shape:

```yaml
---
type: contact
name: <Full Name>
organisation: <Org name or wikilink>
role: <Role>
email: <email if known>
linkedin: <URL if known>
phone: <phone if known>
status: active | reference
created: <today, ISO>
last-contact: <today, ISO, if user has just met them>
lawful_basis: <basis chosen in Phase C2>
tags: [<any contextual tags>, lb-<basis chosen in Phase C2>]
---

# <Full Name>

## Contact details

- **Organisation:** [[CRM/organisations/<category>/<org>|<Org>]] — <Role>
- **Email:** <email>
- **LinkedIn:** <URL>
- **Location:** <location if known>
- **Known since:** <date or context>

## About

<One or two paragraphs of public-info biography. Lead with their current role. Include the LinkedIn headline if it was captured. Keep it factual.>

## How we met

<One short paragraph: when, where, what was discussed. Drawn from what the user told you. Leave the section out if no context was given.>

## Conversation history

<Reverse-chronological list. The first entry is today's interaction if the user has just met them. One bullet per touchpoint with date, channel, and a one-line note.>

## Outstanding

<Anything the user owes them or expects from them. Use a tick-list if there are concrete tasks; leave the section out if nothing is open.>

## Related

- [[CRM/organisations/<category>/<org>|<Org>]] — their organisation
- <Any other contacts or organisations they were mentioned alongside>
```

Fill every field you have data for. Omit any section that has no content. Never write placeholder text like `<location if known>` into the output.

## Phase E — Confirm

Show the draft to the user. Ask:

> "Here's the contact page I'd write to `CRM/contacts/<active|reference> contacts/<Full Name>.md`. Anything to change before I save it?"

Wait for explicit confirmation or amendments. If the user wants changes, apply them and re-show.

If the user asks for changes that pull in non-public information (private email, anything not on LinkedIn or their company site), confirm twice: "This isn't on a public source. Are you sure you want me to write it in?"

## Phase F — Write

Write the file to the appropriate path:

- `CRM/contacts/active contacts/<Full Name>.md` for active contacts.
- `CRM/contacts/reference contacts/<Full Name>.md` for reference contacts.

Use the person's full canonical name as the filename. If two people share a name, append a disambiguator (`Jane Smith (Acme)`).

## Phase G — Cross-reference

Check whether the contact's organisation exists in `CRM/organisations/`. Use Glob to search.

- **If the org exists:** ensure the contact page links to it via the canonical wikilink. If the org page has a "Key Contacts" table, suggest adding the new contact to that table (ask before editing the org page).
- **If the org does not exist:** tell the user, and offer to run `/add-organisation` for them.

Suggest any other obvious follow-ups (event capture, calendar reminder for next touchpoint) but do not auto-create.

## Guidelines

- Public information only. If a field is unknown, leave it out.
- The user is the source of truth for relationship context; you are the source of truth for public-record content.
- Confirm before writing. Never write a contact page without explicit user confirmation.
- One file per person. Use the canonical full name. Disambiguate with parenthesised org if there's a collision.
- Cross-reference into CRM/organisations/ so the graph stays connected.
