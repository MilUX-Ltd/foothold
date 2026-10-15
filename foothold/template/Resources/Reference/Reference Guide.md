---
type: guide
folder: Resources/Reference
---

# Reference Guide

## Purpose

`Reference/` holds general reference material that doesn't fit any other Resources subfolder. The catch-all. Use sparingly.

## Structure

A flat folder. The Foothold defaults ship three substantive defence-reference pages:

- [[Resources/Reference/Defence Acronyms|Defence Acronyms]] — quick-lookup glossary of the acronyms you'll meet every week in UK defence.
- [[Resources/Reference/Defence Reading List|Defence Reading List]] — curated UK defence publications worth reading early.
- [[Resources/Reference/MOD Policy Library|MOD Policy Library]] — navigation surface for JSPs, Def Stans, JDPs, and the wider MOD policy library.

## Writing a reference page

- Only land things here when none of the more specific buckets fit (`Methods/`, `Ways of Working/`, `Books/`, `Business/`, `Frameworks/`, `Templates/`).
- The test: if something stays in `Reference/` for more than six months without finding a more specific home, the subfolder structure may need a new entry. Add the new subfolder and move the file.
- This folder should stay small. If it's bigger than the others combined, that's a sign of structural drift.

## Lifecycle

Statuses are optional here. A reference page is `status: active` and changes by being edited; set it to `archived` when it is out of date and you do not plan to refresh it, and keep the page.

## Frontmatter

```yaml
---
type: reference
status: active
created: YYYY-MM-DD
tags: [...]
---
```

## Canonical example

See [[Resources/Reference/Defence Acronyms|Defence Acronyms]]: a single-purpose reference page you scan rather than read.

## Related

- [[Resources/Resources Guide|Resources Guide]] — parent
