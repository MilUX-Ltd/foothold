---
type: guide
folder: Ideas
---

# Ideas Guide

## Purpose

`Ideas/` is your capture-quickly, process-later inbox. Sparks, half-thoughts, "I should look into this" notes that aren't yet ready to be filed under a specific folder. The point is friction-free capture.

It is not a junk drawer. It works because you process it on a cadence and move things to their permanent home (`Initiatives/`, `Capabilities and Services/`, `Knowledge/hypotheses.md`, or the bin).

## Structure

```
Ideas/
├── Ideas Guide.md          (this file)
└── <YYYY-MM-DD> <Short title>.md
```

Flat folder. One file per idea. Filename starts with the date you captured it, so they sort chronologically. Title after the date is short and descriptive.

Examples:
- `2026-05-20 Foothold MCP layer pricing model.md`
- `2026-05-18 Defence SME training programme via cluster network.md`

Don't introduce subfolders here. Subfolders signal that an idea has graduated to a real thing, which means it belongs elsewhere.

## Frontmatter

```yaml
---
type: idea
status: raw | incubating | promoted | discarded
created: YYYY-MM-DD
---
```

Optional:
- `tags:` for thematic grouping.
- `promoted_to:` (wikilink) when an idea graduates. Records where it ended up.

## Add discipline

**Capture, don't curate.** When an idea hits, write it down fast. Title, two sentences, what triggered it. You'll process it later.

**Process on a cadence.** Once a week (or whenever the folder gets unwieldy), walk through and decide for each idea:

- **Promote.** It deserves its own initiative, service, or hypothesis. Move it to `Initiatives/active/`, `Capabilities and Services/`, or `Knowledge/hypotheses.md`. Set `status: promoted` and `promoted_to: [[wikilink]]` before you delete the idea file, or leave the file in place as a record (your choice).
- **Incubate.** Not ready yet but not dead. Leave it in `Ideas/`, set `status: incubating`. Revisit next time.
- **Discard.** Doesn't survive contact with reality. Set `status: discarded`. Keep the file (the thinking is the value), don't delete.

**The test for promotion.** Has the idea survived two reviews without being discarded? If yes, it's worth a real home. If it's still in `Ideas/` after three reviews, either promote it or discard it. Indecision costs more than action.

**Don't add half-formed plans here.** If you're already at the "this is the plan" stage, it's an initiative, not an idea. Skip straight to `Initiatives/active/<initiative-name>/`.

## Canonical example

A raw idea, captured at speed:

```markdown
---
type: idea
status: raw
created: 2026-05-20
---
# Foothold MCP layer pricing model

Subscription for live content updates that don't ship in the Brain pack. Could be price-anchored to the Cowork sub. Worth checking whether other plugin authors gate content behind a paid tier in the marketplace.
```

Three sentences. Filename and frontmatter do the rest of the work.
