---
type: guide
folder: CRM/contacts
---

# Contacts Guide

## Purpose

`contacts/` holds people you have or might have a working relationship with. Split into three by relationship state: active, reference, archive.

## Subfolders

- **`active contacts/`.** People you currently work with or have had recent contact with. Pages carry relationship intelligence: how you met, conversations to date, things outstanding, what they care about.
- **`reference contacts/`.** People who matter to your domain but you don't have a personal working relationship with. Industry figures, named subject-matter experts, public officials. Pointer pages only; no relationship intelligence.
- **`archive/`.** People you no longer interact with. Pages preserved for search and historical context. Don't delete; move here when a relationship ends.

## Add discipline

- Add via the `/add-contact` skill where available; it pulls public info, drafts the page, asks you to confirm before writing.
- Active vs reference: if you have a working relationship or a recent conversation, the page is active. If you just need a pointer page for someone you don't directly engage with, it's reference. Don't fudge the line.
- Archiving: move from `active contacts/` to `archive/` when the relationship ends. Search continuity matters; old context is often useful later.

## Frontmatter

Follows the parent CRM Guide. Status field reflects the subfolder: `active` for `active contacts/`, `reference` for `reference contacts/`, `archived` for `archive/`. Every contact also carries a `lawful_basis:` property (and matching `lb-*` tag) recording the UK GDPR Article 6 basis for processing their data; the `/add-contact` skill sets this when it captures the contact.

## Related

- [[CRM/CRM Guide|CRM Guide]] — parent
- [[CRM/organisations/Organisations Guide|Organisations Guide]] — sibling
- [[CRM/networks/Networks Guide|Networks Guide]] — sibling
