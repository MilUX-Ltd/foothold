---
name: design-system-setup
description: "Build a complete, token-based design system for a founder's brand from a short interview: colour, type, spacing, a generated showcase page, and starter templates (PDF, slide, letterhead). Use when the user says 'set up a design system', 'create our brand system', 'build our design tokens', 'I need a brand/design system', 'scaffold our brand', 'give us a style guide with code', or runs /design-system-setup. Produces a self-contained folder the user can open, edit, and build every surface from."
audited: 2026-06-18
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
license: MIT
category: brand
---

# Design System Setup

Turn a founder's brand into a working design system: one canonical token file, a stylesheet every surface links, a generated showcase page, written guidance, and starter templates. The structure follows a system proven in production; the values are the founder's own.

A founder should come out of this with the thing most never build for themselves: a single source of truth for colour, type and spacing, so every document, deck and page is consistent without hand-styling each one.

## What this is, and what it is not

This builds the **foundation and the starter surfaces**, not a finished brand. It does not design a logo, choose the founder's colours for them, or write their copy. It takes the decisions the founder has already made (or can make in a few minutes) and turns them into a real, editable system. The output is plain HTML and CSS with no build step and no dependencies, so it opens in any browser and renders offline.

It is deliberately self-contained. The generated folder depends on nothing in the vault and nothing external except the web fonts, which fall back to a system stack if blocked.

## When to reach for it

The user wants a brand or design system, design tokens, a coded style guide, or a consistent set of templates, and does not yet have one. If they already have a system and want to *apply* it to a new surface, that is a different job; use their existing tokens, do not scaffold a new system over the top.

## Inputs — the interview

Gather these before generating. Use a short sequence of `AskUserQuestion` calls, one decision at a time, with sensible defaults offered. Do not ask everything at once.

1. **Brand name and strapline.** The name is required. The strapline is optional and sets the lede on the showcase and cover.
2. **Primary colour.** The brand colour and the signature dark surface. Ask for a hex. This is the one colour everything else is derived around.
3. **Accent colour.** Used as a rule, an eyebrow underline, a small mark. Ask for a hex.
4. **Neutral temperature.** Warm (cream paper, warm ink) or cool (grey paper). One choice.
5. **Type.** A display face, a body face, and a mono face. Offer two or three tasteful pairings as defaults (for example Manrope / Inter / Roboto Mono, or Fraunces / Source Sans / IBM Plex Mono). All must be Google Fonts so they load without a kit. Ask whether the display face is set in capitals.
6. **Voice.** Three or four "do" rules and three "don't" rules, in the founder's words. These populate the guidance and the showcase.

If the user wants to move fast, the example config at `references/brand.config.example.json` shows every field; you can fill it from a single message and skip the step-by-step.

## How to run it

1. Write the answers to a `brand.config.json`. The shape is in `references/brand.config.example.json`; the full field reference is in `references/structure.md`. Only `brand.name`, `colors.primary` and `colors.accent` are required; everything else has a sensible default.
2. Decide where the system should live and confirm it with the user. A natural home is a `Brand/` or `code/brand/` folder they own. Do not write outside a folder the user has chosen.
3. Run the scaffolder:

   ```
   node scripts/scaffold.mjs --config <path to brand.config.json> --out <chosen output folder>
   ```

   It prints every file it writes. It only ever writes inside `--out`.
4. Tell the user to open `index.html` from the output folder in a browser to see the whole system. To render a PDF from the report template, the README in the output folder has the WeasyPrint one-liner.

## What it produces

```
<out>/
├── css/colors_and_type.css   canonical tokens — the source of truth
├── css/styles.css            the one stylesheet a surface links
├── index.html                generated showcase: colour, type, components, voice
├── BRAND-GUIDANCE.md          written voice and usage rules
├── templates/
│   ├── pdf/report-template.html
│   ├── slides/slide-template.html
│   └── stationery/letterhead.html
└── README.md                  how the folder fits together
```

Colour tints (deep, soft, warm, light) and a six-stop chart palette are derived from the two brand colours, with derived chart accents held muted so they stay harmonious whatever the inputs are. Type scale, spacing and radii are an editorial default the founder can tune.

## After producing

- Walk the user through the showcase page so they can see their system rendered, and point them at `css/colors_and_type.css` as the one place to change a value.
- To revise, edit the config and re-run, or edit the token file directly. The token file is the source of truth either way.
- If the founder will publish copy from the guidance, remind them the written brand voice still takes a `humaniser` pass before anything goes out.

## Notes

- **Tokens only.** The whole point is that surfaces never carry raw hex or raw px. Keep generated and hand-built surfaces consistent: pull from the tokens.
- **No network, no dependencies.** The scaffolder is plain Node and writes only inside the output folder. It fetches nothing and runs nothing it generates.
- This skill scaffolds the foundation. A logo, a full slide deck, and richer templates are the founder's next steps, built on the tokens this lays down.
