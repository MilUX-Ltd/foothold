---
type: guide
folder: Resources/Books
---

# Books Guide

## Purpose

`Books/` holds book notes and a reading-list index. The index file (`Library.md`) is the canonical list of books on your radar, what you've read, and what's queued.

## Add discipline

- One file per book worth notes on: `<Author> — <Title>.md` or just `<Title>.md` if the title is unambiguous.
- `Library.md` carries the index: each entry pointing to its book-note page if one exists, or a one-liner if you haven't taken notes yet.
- Insights worth elevating from a book note to an operating idea belong in `Knowledge/hypotheses.md` with a back-reference to the book note.

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

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
- [[Knowledge/Knowledge Guide|Knowledge Guide]] — for promoting book insights into hypotheses
