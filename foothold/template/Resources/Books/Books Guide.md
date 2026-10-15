---
type: guide
folder: Resources/Books
---

# Books Guide

## Purpose

`Books/` holds book notes and a reading-list index. The index file (`Library.md`) is the canonical list of books on your radar, what you've read, and what's queued.

## Structure

```
Books/
├── Books Guide.md          (this file)
├── Library.md              (the index; create it with your first book note)
└── <Author> — <Title>.md   (one file per book worth notes on)
```

## Writing a book note

- One file per book worth notes on: `<Author> — <Title>.md` or just `<Title>.md` if the title is unambiguous.
- `Library.md` carries the index: each entry pointing to its book-note page if one exists, or a one-liner if you haven't taken notes yet.
- Insights worth elevating from a book note to an operating idea belong in your hypotheses page, if you keep one (see the [[Knowledge/Knowledge Guide|Knowledge Guide]]), with a back-reference to the book note.

## Lifecycle

A book note's `status:` is `queued`, `in-progress`, `read` or `abandoned`. A book starts `queued`, moves to `in-progress` when you start it, and ends `read` when you finish or `abandoned` when you stop. Keep the note either way; what you thought of it is the value.

## Frontmatter

```yaml
---
type: book-note
status: read | queued | in-progress | abandoned
created: YYYY-MM-DD
author: <author>
title: <title>
source: <citation or URL>
tags: [...]
---
```

## Canonical example

No example ships. Your first book note, with the frontmatter above, a line on why you read it and the three things worth keeping, sets the pattern.

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Knowledge/Knowledge Guide|Knowledge Guide]] — for promoting book insights into hypotheses
