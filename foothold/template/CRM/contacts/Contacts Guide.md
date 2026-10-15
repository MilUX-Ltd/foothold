---
type: guide
folder: CRM/contacts
---

# Contacts Guide

## Purpose

`contacts/` holds people you have or might have a working relationship with. Split into three by relationship state: active, reference, archive.

## Structure

- **`active contacts/`.** People you currently work with or have had recent contact with. Pages carry relationship intelligence: how you met, conversations to date, things outstanding, what they care about.
- **`reference contacts/`.** People who matter to your domain but you don't have a personal working relationship with. Industry figures, named subject-matter experts, public officials. Pointer pages only; no relationship intelligence.
- **`archive/`.** People you no longer interact with. Pages preserved for search and historical context. Don't delete; move here when a relationship ends.

## Writing a contact

- Add via the `/add-contact` skill where available; it pulls public info, drafts the page, asks you to confirm before writing. To write one by hand, insert the [[Templates/Contact|Contact template]].
- Active vs reference: if you have a working relationship or a recent conversation, the page is active. If you just need a pointer page for someone you don't directly engage with, it's reference. Don't fudge the line.
- Archiving: move from `active contacts/` to `archive/` when the relationship ends. Search continuity matters; old context is often useful later.

## Lifecycle

A contact's `status:` reflects its subfolder:

- `active` for pages in `active contacts/`.
- `reference` for pages in `reference contacts/`.
- `archived` for pages in `archive/`.

A reference contact becomes `active` when you start working with them. An active contact becomes `archived` when the relationship ends; move the page and change the status together.

## Frontmatter

Follows the parent CRM Guide:

```yaml
---
type: contact
name: <full name>
organisation: "[[CRM/organisations/<category>/<org>|<org>]]"
role: <their current role>
email: <email>
linkedin: <URL>
phone: <phone>
status: active | reference | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
last-contact: YYYY-MM-DD
lawful_basis: legitimate-interests | consent | contract | legal-obligation
tags: [lb-legitimate-interests]
---
```

Every contact also carries a `lawful_basis:` property (and matching `lb-*` tag) recording the UK GDPR Article 6 basis for processing their data; the `/add-contact` skill sets this when it captures the contact.

## Canonical example

Start from the [[Templates/Contact|Contact template]]. For a finished page, see [[CRM/contacts/active contacts/Matt Odell|Matt Odell]].

## Related

- [[CRM/CRM Guide|CRM Guide]] — parent
- [[CRM/organisations/Organisations Guide|Organisations Guide]] — sibling
- [[CRM/networks/Networks Guide|Networks Guide]] — sibling
- [[Templates/Templates Guide|Templates Guide]]: the note templates
