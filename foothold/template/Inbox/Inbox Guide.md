---
type: guide
folder: Inbox
---

# Inbox Guide

## Purpose

`Inbox/` is where new things land before you decide where they belong. Capture comes first; filing comes later. A thought, a call note, a clipped page, a half-formed plan: write it down now, in whatever shape it comes, and sort it out when you have a moment.

Obsidian is set up to create new notes here. Nothing lives in the Inbox for good. If a note is still here a week later, it is either ready to be filed or it was never worth keeping.

## Structure

```
Inbox/
├── Inbox Guide.md          (this file)
└── <any new note>.md
```

A flat folder with no subfolders. A subfolder would be a decision about where something belongs, and that is the job of filing, not capture.

`Inbox/` is different from `Ideas/`. The Inbox takes anything. `Ideas/` takes ideas you have decided are worth keeping and revisiting.

## Writing a quick note

Open a new note and write. Give it a title that will make sense next week. You do not need frontmatter, sections or links yet; the point is that capturing costs you nothing.

When you file the note, that is when it gets its shape: move it to its home folder, insert the matching template from `Templates/`, and add the frontmatter the Guide for that folder asks for.

## Lifecycle

Statuses are optional here. A note in the Inbox is simply unfiled. Once a week, or when the folder gets long, go through it and for each note do one of three things:

- **File it.** Move it to the folder where it belongs and give it the right template and frontmatter.
- **Make it an idea.** If it is a spark worth keeping, move it to `Ideas/` and use the Idea template.
- **Discard it.** If it has no value now, remove it. That is your decision, never an assistant's.

An empty Inbox is a good sign, and so is a short one.

## Frontmatter

None is required while a note is in the Inbox. Frontmatter is added when the note is filed, from the template for its kind. See [[Knowledge/rules|rule R-07]] for the convention.

## Canonical example

A note as captured, with no ceremony:

```markdown
# Ask Jane about the retainer

She mentioned a budget freeze in the new year. Worth raising before the proposal goes in.
```

Filed later, it becomes a line in Jane's contact page under "Outstanding", and the note is gone from the Inbox.

## Related

- [[Templates/Templates Guide|Templates Guide]]: the templates you apply when you file.
- [[Ideas/Ideas Guide|Ideas Guide]]: for sparks worth keeping.
- [[Attachments/Attachments Guide|Attachments Guide]]: where files you drop into a note are kept.
