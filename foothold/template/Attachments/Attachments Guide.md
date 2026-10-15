---
type: guide
folder: Attachments
---

# Attachments Guide

## Purpose

`Attachments/` is where Obsidian saves the files you paste or drop into a note: a screenshot, a photo of a whiteboard, a small PDF. Keeping them in one place stops them scattering through the vault.

The vault is for notes. It syncs and backs up everywhere you use it, so everything in it travels with you. Keep this folder small and keep the right things out of it.

## Structure

```
Attachments/
├── Attachments Guide.md    (this file)
└── <attachment files>
```

A flat folder with no subfolders. The file name does the organising, and the note that embeds the file gives it context.

## Writing an attachment name

Obsidian names pasted images "Pasted image" followed by a timestamp, which tells you nothing a year later. Rename each attachment when you add it, so the name says what it is: a date, then a short description (`2026-05-20 Kickoff whiteboard.png`).

**Keep large or sensitive files out of the vault.** Link them instead.

- *Large*: anything more than a few megabytes, such as recordings, slide decks, scans and long PDFs. They slow sync and bloat backups.
- *Sensitive*: anything holding personal data, customer-confidential material, contracts or credentials. Not every device that syncs your vault needs to hold them.

Keep these in your document store, shared drive or reference library, and put a link in the note. See [[Resources/Ways of Working/Where Your Data Lives|Where Your Data Lives]] and [[Resources/Ways of Working/Sync and Backup|Sync and Backup]] for how to decide.

## Lifecycle

Statuses do not apply: an attachment is a file, not a note. It stays for as long as a note needs it. Before you remove one, check that no note still links to it. If you delete a note that was the only link to its attachment, remove the attachment too.

## Frontmatter

None. Attachments are not notes. The note that embeds or links the file carries the frontmatter.

## Canonical example

Embedding a small image in a note, and linking a large file that lives elsewhere:

```markdown
![[2026-05-20 Kickoff whiteboard.png]]

Signed contract: [Acme services agreement](https://example.com/shared/acme-agreement.pdf)
```

## Related

- [[Inbox/Inbox Guide|Inbox Guide]]: where new notes land.
- [[Resources/Ways of Working/Where Your Data Lives|Where Your Data Lives]]: what belongs in the vault and what does not.
- [[Resources/Ways of Working/Sync and Backup|Sync and Backup]]: how the vault travels between devices.
