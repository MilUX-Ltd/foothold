# brand.config.json — field reference

The scaffolder reads one JSON file. Only three fields are required; the rest fall back to sensible defaults.

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `brand.name` | yes | — | Used in the title, hero, covers, guidance. |
| `brand.strapline` | no | none | One line. Sets the lede on the showcase and the report cover. |
| `colors.primary` | yes | `#113308` | Hex. The brand colour and the signature dark surface. |
| `colors.accent` | yes | `#B5B171` | Hex. A rule, an eyebrow underline, a small mark. |
| `colors.neutral` | no | `warm` | `warm` (cream paper) or `cool` (grey paper). |
| `fonts.display` | no | `Manrope` | Google Fonts family name. Display / headings. |
| `fonts.body` | no | `Bai Jamjuree` | Google Fonts family name. Body / UI. |
| `fonts.mono` | no | `Roboto Mono` | Google Fonts family name. Data / dates. |
| `style.displayUppercase` | no | `true` | Set the display face in capitals. |
| `voice.do` | no | three defaults | Array of short "do" rules. |
| `voice.dont` | no | three defaults | Array of short "don't" rules. |

## Derived values

From `colors.primary` and `colors.accent` the scaffolder derives:

- **Primary scale:** `--c-primary-deep` (headings on light), `--c-primary-soft` (hover).
- **Accent scale:** `--c-accent-warm` (hover), `--c-accent-deep` (accent on light, for legibility), `--c-accent-light`.
- **Chart palette:** six stops, including two muted rotations (`--c-accent-b`, `--c-accent-c`) held to a tasteful saturation and mid lightness so they stay harmonious for any input.
- **Neutrals:** paper, paper-2, rule, rule-strong, ink, ink-2, ink-3 from the warm/cool choice.

All derivation is plain HSL maths in `scripts/scaffold.mjs`, no dependencies.

## Type scale, spacing, radii

These are an editorial default (a 4px spacing base, an editorial type scale, restrained radii of 2/4px plus a pill). They are written into the token file so the founder can tune them in one place.

## Re-running

Editing the config and re-running regenerates the folder. The token file is the source of truth; once generated, editing it directly is equally valid.
