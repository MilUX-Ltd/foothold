#!/usr/bin/env node
/**
 * scaffold.mjs — generate a complete design system from a brand config.
 *
 * Reads a brand.config.json (the founder's answers) and writes a full,
 * self-contained design-system folder:
 *
 *   css/colors_and_type.css   canonical tokens (palette, type, spacing, radii)
 *   css/styles.css            the one stylesheet a surface links
 *   index.html                a generated showcase of the whole system
 *   BRAND-GUIDANCE.md         written voice and usage rules
 *   templates/pdf/…           A4 report / case-study starter
 *   templates/slides/…        16:9 slide starter
 *   templates/stationery/…    letterhead starter
 *   README.md                 how the folder fits together
 *
 * The architecture mirrors the MilUX design system. The values are the
 * founder's own. No network, no dependencies, writes only inside --out.
 *
 * Usage:
 *   node scaffold.mjs --config ./brand.config.json --out ./brand
 *
 * Defaults: --config ./brand.config.json, --out ./brand
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, resolve, join } from "node:path";

/* ---- args --------------------------------------------------------------- */
const args = process.argv.slice(2);
const argOf = (flag, dflt) => {
  const i = args.indexOf(flag);
  return i >= 0 && args[i + 1] ? args[i + 1] : dflt;
};
const configPath = resolve(process.cwd(), argOf("--config", "brand.config.json"));
const outDir = resolve(process.cwd(), argOf("--out", "brand"));

if (!existsSync(configPath)) {
  console.error(`No config at ${configPath}. Pass --config <path>.`);
  process.exit(1);
}
const cfg = JSON.parse(readFileSync(configPath, "utf8"));

/* ---- colour helpers (dependency-free hex <-> hsl) ----------------------- */
const clamp = (n, lo, hi) => Math.min(hi, Math.max(lo, n));
const hexToRgb = (h) => {
  const x = h.replace("#", "").trim();
  const v = x.length === 3 ? x.split("").map((c) => c + c).join("") : x;
  return [0, 2, 4].map((i) => parseInt(v.slice(i, i + 2), 16));
};
const rgbToHex = (r, g, b) =>
  "#" + [r, g, b].map((n) => clamp(Math.round(n), 0, 255).toString(16).padStart(2, "0")).join("").toUpperCase();
const rgbToHsl = (r, g, b) => {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h = 0, s = 0; const l = (max + min) / 2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    if (max === r) h = (g - b) / d + (g < b ? 6 : 0);
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    h /= 6;
  }
  return [h * 360, s * 100, l * 100];
};
const hslToRgb = (h, s, l) => {
  h /= 360; s /= 100; l /= 100;
  if (s === 0) { const v = l * 255; return [v, v, v]; }
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;
  const hue = (t) => {
    if (t < 0) t += 1; if (t > 1) t -= 1;
    if (t < 1 / 6) return p + (q - p) * 6 * t;
    if (t < 1 / 2) return q;
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  };
  return [hue(h + 1 / 3) * 255, hue(h) * 255, hue(h - 1 / 3) * 255];
};
const adjust = (hex, { dl = 0, ds = 0, dh = 0 } = {}) => {
  let [h, s, l] = rgbToHsl(...hexToRgb(hex));
  h = (h + dh + 360) % 360; s = clamp(s + ds, 0, 100); l = clamp(l + dl, 0, 100);
  return rgbToHex(...hslToRgb(h, s, l));
};
// Keep a derived hue tasteful and on-brand: cap saturation, hold lightness mid.
const muted = (hex) => {
  let [h, s, l] = rgbToHsl(...hexToRgb(hex));
  s = clamp(s, 0, 42); l = clamp(l, 44, 60);
  return rgbToHex(...hslToRgb(h, s, l));
};

/* ---- derive the palette ------------------------------------------------- */
const primary = cfg.colors?.primary || "#113308";
const accent  = cfg.colors?.accent  || "#B5B171";
const neutralWarm = (cfg.colors?.neutral || "warm").toLowerCase() !== "cool";

const palette = {
  primary,
  primaryDeep: adjust(primary, { dl: -6, ds: +4 }),
  primarySoft: adjust(primary, { dl: +10 }),
  accent,
  accentWarm: adjust(accent, { dl: +6 }),
  accentDeep: adjust(accent, { dl: -14, ds: +4 }),
  accentLight: adjust(accent, { dl: +12, ds: -6 }),
  // a third and fourth accent for charts / callouts: muted rotations so they
  // stay harmonious whatever the brand colours are.
  accentB: muted(adjust(primary, { dh: +185, dl: +24 })),
  accentC: muted(adjust(accent, { dh: -26 })),
  paper:   neutralWarm ? "#F7F6EB" : "#F5F7F8",
  paper2:  neutralWarm ? "#E9E7D6" : "#E7ECEF",
  rule:    neutralWarm ? "#DDDAC4" : "#D8DEE2",
  ruleStrong: neutralWarm ? "#C0BCA2" : "#B9C2C8",
  ink:  "#1A1A1A",
  ink2: "#4A4A47",
  ink3: "#7A7A75",
};

const fonts = {
  display: cfg.fonts?.display || "Manrope",
  body:    cfg.fonts?.body    || "Bai Jamjuree",
  mono:    cfg.fonts?.mono    || "Roboto Mono",
};
const googleFamily = (name, weights) =>
  `family=${name.replace(/ /g, "+")}:wght@${weights}`;
const fontImport =
  "https://fonts.googleapis.com/css2?" +
  [
    googleFamily(fonts.display, "300;400;500;600;700;800"),
    googleFamily(fonts.body, "300;400;500;600;700"),
    googleFamily(fonts.mono, "400;500;600"),
  ].join("&") +
  "&display=swap";

const brandName = cfg.brand?.name || "Your brand";
const strapline = cfg.brand?.strapline || "";
const allCapsDisplay = cfg.style?.displayUppercase !== false;
const uppercase = allCapsDisplay ? "uppercase" : "none";

/* ---- file writer -------------------------------------------------------- */
const write = (rel, content) => {
  const p = join(outDir, rel);
  mkdirSync(dirname(p), { recursive: true });
  writeFileSync(p, content);
  return rel;
};
const written = [];
const emit = (rel, content) => written.push(write(rel, content));

/* ---- css/colors_and_type.css ------------------------------------------- */
emit("css/colors_and_type.css", `/* ${brandName} — Colors & Type.
   Generated by design-system-setup. Edit values here; this is the source of truth. */
@import url("${fontImport}");

:root {
  /* ---- Brand palette --------------------------------------------------- */
  --c-primary:       ${palette.primary};
  --c-primary-deep:  ${palette.primaryDeep};   /* headings on light */
  --c-primary-soft:  ${palette.primarySoft};   /* hover on primary surfaces */

  --c-accent:        ${palette.accent};
  --c-accent-warm:   ${palette.accentWarm};    /* hover lift */
  --c-accent-deep:   ${palette.accentDeep};    /* accent on light, for legibility */
  --c-accent-light:  ${palette.accentLight};

  /* Secondary accents — charts and callouts only, never primary surfaces */
  --c-accent-b:      ${palette.accentB};
  --c-accent-c:      ${palette.accentC};

  /* Neutrals */
  --c-paper:         ${palette.paper};
  --c-paper-2:       ${palette.paper2};
  --c-rule:          ${palette.rule};
  --c-rule-strong:   ${palette.ruleStrong};
  --c-ink:           ${palette.ink};
  --c-ink-2:         ${palette.ink2};
  --c-ink-3:         ${palette.ink3};

  /* Semantic tokens */
  --fg-1: var(--c-ink);
  --fg-2: var(--c-ink-2);
  --fg-3: var(--c-ink-3);
  --fg-on-primary:   var(--c-paper);
  --fg-on-primary-2: rgba(255,255,255,0.72);
  --fg-on-primary-3: rgba(255,255,255,0.50);

  --bg-1: var(--c-paper);
  --bg-2: var(--c-paper-2);
  --bg-primary: var(--c-primary);

  --accent:        var(--c-accent-deep);   /* on light */
  --accent-strong: var(--c-accent);        /* on primary */
  --rule:          var(--c-rule);
  --rule-strong:   var(--c-rule-strong);

  /* Chart palette */
  --chart-1: var(--c-primary);
  --chart-2: var(--c-accent-deep);
  --chart-3: var(--c-accent-b);
  --chart-4: var(--c-accent-c);
  --chart-5: var(--c-accent-light);
  --chart-6: var(--c-primary-soft);

  /* ---- Type families --------------------------------------------------- */
  --font-display: "${fonts.display}", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-sans:    "${fonts.body}", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono:    "${fonts.mono}", ui-monospace, "SF Mono", Menlo, Consolas, monospace;

  /* ---- Type scale ------------------------------------------------------ */
  --fs-display:  clamp(48px, 6vw, 88px);
  --fs-h1:       clamp(36px, 4vw, 56px);
  --fs-h2:       clamp(28px, 3vw, 40px);
  --fs-h3:       22px;
  --fs-h4:       18px;
  --fs-body-lg:  19px;
  --fs-body:     17px;
  --fs-body-sm:  15px;
  --fs-caption:  13px;
  --fs-eyebrow:  12px;

  --lh-display: 1.05;
  --lh-tight:   1.15;
  --lh-snug:    1.3;
  --lh-body:    1.55;
  --lh-loose:   1.7;

  --tr-display: -0.02em;
  --tr-tight:   -0.01em;
  --tr-normal:  0;
  --tr-eyebrow: 0.14em;

  /* ---- Spacing (4px base) --------------------------------------------- */
  --sp-1: 4px;  --sp-2: 8px;  --sp-3: 12px; --sp-4: 16px; --sp-5: 24px;
  --sp-6: 32px; --sp-7: 48px; --sp-8: 64px; --sp-9: 96px; --sp-10: 128px;

  /* ---- Radii — restrained --------------------------------------------- */
  --r-xs: 2px; --r-sm: 4px; --r-md: 6px; --r-pill: 999px;

  /* ---- Borders -------------------------------------------------------- */
  --border-hair: 1px solid var(--rule);
  --border:      1px solid var(--rule-strong);
  --border-ink:  1px solid var(--c-ink);

  /* ---- Elevation — flat first ----------------------------------------- */
  --shadow-none: none;
  --shadow-edge: 0 0 0 1px var(--rule);
  --shadow-soft: 0 1px 2px rgba(0,0,0,0.06), 0 1px 1px rgba(0,0,0,0.04);

  /* ---- Layout --------------------------------------------------------- */
  --container: 1200px;
  --container-narrow: 760px;
  --gutter: 24px;
}

/* =========================================================================
   Semantic element styles — apply via class so the system is portable.
   ========================================================================= */
html, body {
  background: var(--bg-1); color: var(--fg-1);
  font-family: var(--font-sans); font-size: var(--fs-body);
  line-height: var(--lh-body); font-weight: 400;
  -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility;
}
.display, h1.display {
  font-family: var(--font-display); font-size: var(--fs-display); font-weight: 700;
  line-height: var(--lh-display); letter-spacing: var(--tr-tight);
  color: var(--c-primary-deep); text-transform: ${uppercase}; text-wrap: balance;
}
h1, .h1 { font-family: var(--font-display); font-size: var(--fs-h1); font-weight: 700;
  line-height: var(--lh-tight); letter-spacing: -0.005em; color: var(--c-primary-deep);
  text-transform: ${uppercase}; text-wrap: balance; }
h2, .h2 { font-family: var(--font-display); font-size: var(--fs-h2); font-weight: 700;
  line-height: var(--lh-tight); color: var(--c-primary-deep); text-transform: ${uppercase}; }
h3, .h3 { font-family: var(--font-display); font-size: var(--fs-h3); font-weight: 600;
  line-height: var(--lh-snug); color: var(--c-primary-deep); text-transform: ${uppercase}; letter-spacing: 0.01em; }
h4, .h4 { font-family: var(--font-sans); font-size: var(--fs-h4); font-weight: 600;
  line-height: var(--lh-snug); color: var(--c-primary-deep); }
p, .p { font-size: var(--fs-body); line-height: var(--lh-body); color: var(--fg-1); max-width: 64ch; }
.lede, p.lede { font-size: var(--fs-body-lg); line-height: var(--lh-body); color: var(--fg-2); max-width: 60ch; }
.small, small { font-size: var(--fs-body-sm); color: var(--fg-2); }
.caption { font-size: var(--fs-caption); color: var(--fg-3); line-height: var(--lh-snug); }
.eyebrow { font-family: var(--font-display); font-size: var(--fs-eyebrow); font-weight: 600;
  letter-spacing: var(--tr-eyebrow); text-transform: uppercase; color: var(--c-accent-deep); }
code, .code, kbd, samp { font-family: var(--font-mono); font-size: 0.92em; background: var(--bg-2);
  padding: 0.1em 0.35em; border-radius: var(--r-xs); color: var(--c-primary-deep); }
a { color: var(--c-primary); text-decoration: underline; text-underline-offset: 3px;
  text-decoration-thickness: 1px; text-decoration-color: var(--rule-strong);
  transition: text-decoration-color 120ms ease, color 120ms ease; }
a:hover { text-decoration-color: var(--c-primary); }
hr { border: 0; border-top: 1px solid var(--rule); margin: var(--sp-7) 0; }
::selection { background: var(--c-accent); color: var(--c-primary-deep); }

.surface-paper   { background: var(--bg-1); color: var(--fg-1); }
.surface-paper2  { background: var(--bg-2); color: var(--fg-1); }
.surface-primary { background: var(--bg-primary); color: var(--fg-on-primary); }
.surface-primary h1, .surface-primary h2, .surface-primary h3, .surface-primary h4,
.surface-primary .display { color: var(--c-paper); }
.surface-primary .eyebrow { color: var(--c-accent); }
.surface-primary a { color: var(--c-accent-warm); text-decoration-color: rgba(255,255,255,0.4); }
`);

/* ---- css/styles.css ----------------------------------------------------- */
emit("css/styles.css", `/* ${brandName} design system — canonical entry point.
   Link this ONE file to get the full token set + base element styles:
       <link rel="stylesheet" href="css/styles.css" />
*/
@import url("colors_and_type.css");
`);

/* ---- index.html (generated showcase) ------------------------------------ */
const voiceDo = cfg.voice?.do || ["Plain language.", "Sentence case.", "Specific over abstract."];
const voiceDont = cfg.voice?.dont || ["Jargon and hype.", "Exclamation marks.", "Filler."];

const swatch = (label, varName) =>
  `<figure class="sw"><div class="chip" style="background:var(${varName})"></div>
     <figcaption><b>${label}</b><code>${varName}</code></figcaption></figure>`;

emit("index.html", `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${brandName} design system</title>
<link rel="stylesheet" href="css/styles.css">
<style>
  body { margin: 0; }
  .wrap { max-width: 1080px; margin: 0 auto; padding: 0 var(--gutter) var(--sp-9); }
  header.hero { position: relative; padding: var(--sp-7) 0 var(--sp-6); margin-bottom: var(--sp-1);
    background-color: var(--c-primary);
    background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 56px 56px; }
  header.hero .eyebrow::after { content:""; display:block; width:48px; height:1px; background:var(--c-accent); margin-top:var(--sp-1); }
  header.hero h1 { margin: var(--sp-3) 0 var(--sp-2); }
  header.hero .lede { color: var(--fg-on-primary-2); max-width: 640px; }
  h2 { font-size: var(--fs-h3); margin: var(--sp-8) 0 var(--sp-4); padding-top: var(--sp-4); border-top: 2px solid var(--c-accent); }
  .swatches { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px,1fr)); gap: var(--sp-4); }
  .sw { margin: 0; } .sw .chip { height: 64px; border: 1px solid var(--rule); }
  .sw figcaption { display: flex; flex-direction: column; gap: 2px; margin-top: var(--sp-2); font-size: var(--fs-caption); }
  .sw code { font-size: 11px; }
  .specimen > * { margin: 0 0 var(--sp-3); }
  .row { display: flex; flex-wrap: wrap; gap: var(--sp-4); align-items: center; }
  .btn { font-family: var(--font-sans); font-weight: 600; font-size: var(--fs-body-sm);
    padding: 10px 18px; border: 1px solid var(--c-primary); cursor: pointer; }
  .btn-primary { background: var(--c-primary); color: var(--c-paper); }
  .btn-secondary { background: transparent; color: var(--c-primary); }
  .card { border: 1px solid var(--rule-strong); padding: var(--sp-5); max-width: 320px; }
  .card.on-primary { background: var(--c-primary); color: var(--c-paper); border-color: transparent; }
  .card.on-primary .eyebrow { color: var(--c-accent); }
  .do-dont { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-5); }
  .do-dont ul { margin: var(--sp-2) 0 0; padding-left: 1.1em; }
  footer { margin-top: var(--sp-8); color: var(--fg-3); font-size: var(--fs-caption); }
</style>
</head>
<body>
<header class="hero surface-primary">
  <div class="wrap">
    <p class="eyebrow">${brandName} design system</p>
    <h1>Tokens, type and components<br>in one place.</h1>
    <p class="lede">${strapline ? strapline + " " : ""}The canonical colour, type and spacing for every ${brandName} surface. Built from <code>css/colors_and_type.css</code>.</p>
  </div>
</header>
<div class="wrap">
  <section>
    <h2>Colour</h2>
    <div class="swatches">
      ${swatch("Primary", "--c-primary")}
      ${swatch("Primary deep", "--c-primary-deep")}
      ${swatch("Accent", "--c-accent")}
      ${swatch("Accent deep", "--c-accent-deep")}
      ${swatch("Accent light", "--c-accent-light")}
      ${swatch("Paper", "--c-paper")}
      ${swatch("Paper 2", "--c-paper-2")}
      ${swatch("Rule", "--c-rule")}
      ${swatch("Ink", "--c-ink")}
      ${swatch("Chart B", "--c-accent-b")}
      ${swatch("Chart C", "--c-accent-c")}
    </div>
  </section>
  <section>
    <h2>Type</h2>
    <div class="specimen">
      <p class="eyebrow">Eyebrow · ${fonts.display}</p>
      <h1 class="display">Display headline</h1>
      <h2>Heading two</h2>
      <h3>Heading three</h3>
      <p class="lede">Lede paragraph in ${fonts.body}. The first line of a section, a touch larger than body, carrying the main claim.</p>
      <p>Body paragraph in ${fonts.body}. ${strapline || "Plain, readable, calm."} Sentence case, normal tracking, comfortable line height for reading.</p>
      <p><code>${fonts.mono} for dates, data and file paths</code></p>
    </div>
  </section>
  <section>
    <h2>Components</h2>
    <div class="row">
      <button class="btn btn-primary">Primary action</button>
      <button class="btn btn-secondary">Secondary</button>
    </div>
    <div class="row" style="margin-top:var(--sp-5)">
      <div class="card"><p class="eyebrow">Service</p><h3 style="margin:var(--sp-2) 0">Paper card</h3><p class="caption">Hairline border, no shadow. The default card.</p></div>
      <div class="card on-primary"><p class="eyebrow">Service</p><h3 style="margin:var(--sp-2) 0">Primary card</h3><p class="caption" style="color:var(--fg-on-primary-2)">Same shape on the brand colour.</p></div>
    </div>
  </section>
  <section>
    <h2>Voice</h2>
    <div class="do-dont">
      <div><p class="eyebrow">Do</p><ul>${voiceDo.map((v) => `<li>${v}</li>`).join("")}</ul></div>
      <div><p class="eyebrow">Don't</p><ul>${voiceDont.map((v) => `<li>${v}</li>`).join("")}</ul></div>
    </div>
  </section>
  <section>
    <h2>Templates</h2>
    <p class="caption">Starter surfaces built on these tokens. Open, copy, edit.</p>
    <div class="row" style="margin-top:var(--sp-3)">
      <a href="templates/pdf/report-template.html" target="_blank" rel="noopener">PDF / report ↗</a>
      <a href="templates/slides/slide-template.html" target="_blank" rel="noopener">Slide ↗</a>
      <a href="templates/stationery/letterhead.html" target="_blank" rel="noopener">Letterhead ↗</a>
    </div>
  </section>
  <footer>Written guidance: <a href="BRAND-GUIDANCE.md">BRAND-GUIDANCE.md</a>. Canonical tokens: <code>css/colors_and_type.css</code>.</footer>
</div>
</body>
</html>
`);

/* ---- BRAND-GUIDANCE.md --------------------------------------------------- */
emit("BRAND-GUIDANCE.md", `# ${brandName} — brand guidance

${strapline ? `**Strapline:** ${strapline}\n` : ""}
The source of truth for values is \`css/colors_and_type.css\`. This file is the written layer: voice, usage, and the rules most often broken.

## Foundations

- **Primary:** \`${palette.primary}\`. The brand colour and the signature dark surface.
- **Accent:** \`${palette.accent}\`. A rule, an eyebrow underline, a small mark. Never a fill behind body text.
- **Neutrals:** ${neutralWarm ? "warm" : "cool"} paper \`${palette.paper}\` and ink \`${palette.ink}\`. Never pure white or pure black.
- **Type:** ${fonts.display} (display${allCapsDisplay ? ", set in caps" : ""}), ${fonts.body} (body, sentence case), ${fonts.mono} (data).

## Hard rules

- **Tokens only.** No raw hex, no raw px in surfaces. Values come from the tokens.
- **Backgrounds are paper or primary.** No gradients behind text, no stock photos, restrained radii (≤ 4px), flat by default.
- **Accent is never a fill behind text.** It is a 1px rule, an underline, a small mark.

## Voice

**Do:** ${voiceDo.join(" ")}

**Don't:** ${voiceDont.join(" ")}

## Build from

- Reports and PDFs: \`templates/pdf/\`.
- Slides: \`templates/slides/\`.
- Letters: \`templates/stationery/\`.
- The whole system at a glance: open \`index.html\`.
`);

/* ---- templates ---------------------------------------------------------- */
const templateHead = (title) => `<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<link rel="stylesheet" href="../../css/styles.css">`;

emit("templates/pdf/report-template.html", `${templateHead(brandName + " — report")}
<style>
  @page { size: A4; margin: 20mm 18mm; }
  body { margin: 0; }
  .cover { background: var(--c-primary); color: var(--c-paper); padding: 40mm 18mm; }
  .cover .eyebrow { color: var(--c-accent); }
  .cover h1 { color: var(--c-paper); margin: 12px 0 8px; }
  main { padding: 16mm 18mm; }
  .meta { font-family: var(--font-mono); font-size: 12px; color: var(--c-ink-3); }
</style></head>
<body>
  <section class="cover surface-primary">
    <p class="eyebrow">Report</p>
    <h1 class="display">Title goes here</h1>
    <p class="lede" style="color:var(--fg-on-primary-2)">${strapline || "One-line summary of the document."}</p>
    <p class="meta" style="color:var(--fg-on-primary-3); margin-top:24px">${brandName} · {date}</p>
  </section>
  <main>
    <h2>Section heading</h2>
    <p class="lede">Lede paragraph introducing the section.</p>
    <p>Body copy. Replace this with the document content. Headings, type, colour and spacing all come from the tokens.</p>
  </main>
</body></html>
`);

emit("templates/slides/slide-template.html", `${templateHead(brandName + " — slide")}
<style>
  body { margin: 0; }
  .slide { width: 1280px; height: 720px; position: relative; overflow: hidden; }
  .title { background: var(--c-primary); color: var(--c-paper);
    background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
                     linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 64px 64px; padding: 96px; }
  .title .eyebrow { color: var(--c-accent); }
  .title h1 { color: var(--c-paper); font-size: 72px; margin: 16px 0 0; }
</style></head>
<body>
  <section class="slide title surface-primary">
    <p class="eyebrow">${brandName}</p>
    <h1 class="display">Title slide</h1>
    <p class="lede" style="color:var(--fg-on-primary-2); margin-top:24px">${strapline || "Subtitle or supporting line."}</p>
  </section>
</body></html>
`);

emit("templates/stationery/letterhead.html", `${templateHead(brandName + " — letterhead")}
<style>
  @page { size: A4; margin: 0; }
  body { margin: 0; }
  .sheet { width: 210mm; min-height: 297mm; background: var(--c-paper); padding: 24mm; box-sizing: border-box; }
  header { display: flex; justify-content: space-between; border-bottom: 1px solid var(--rule); padding-bottom: 8mm; margin-bottom: 12mm; }
  .mark { font-family: var(--font-display); font-weight: 700; text-transform: ${uppercase}; color: var(--c-primary-deep); font-size: 20px; }
  .sender { text-align: right; font-family: var(--font-mono); font-size: 11px; color: var(--c-ink-3); line-height: 1.6; }
  .signoff { margin-top: 16mm; }
</style></head>
<body>
  <div class="sheet">
    <header>
      <div class="mark">${brandName}</div>
      <div class="sender">${brandName}<br>address line<br>email · web</div>
    </header>
    <p>Dear {name},</p>
    <p>Body of the letter. Type and colour come from the tokens, so every letter is consistent.</p>
    <div class="signoff"><p>Regards,</p><p><b>{your name}</b><br><span class="caption">{role}</span></p></div>
  </div>
</body></html>
`);

/* ---- README.md ---------------------------------------------------------- */
emit("README.md", `# ${brandName} design system

Generated by the \`design-system-setup\` skill. The structure:

- \`css/colors_and_type.css\` — canonical tokens. The source of truth for every value.
- \`css/styles.css\` — the one stylesheet a surface links.
- \`index.html\` — a showcase of the whole system. Open it in a browser.
- \`BRAND-GUIDANCE.md\` — written voice and usage rules.
- \`templates/\` — starter surfaces (PDF report, slide, letterhead) built on the tokens.

## Edit

Change a value in \`css/colors_and_type.css\` and every surface follows. To re-run setup from a config, use the skill again with an updated \`brand.config.json\`.

## Render a PDF

\`\`\`
pip install weasyprint --break-system-packages
cd templates/pdf
python3 -c "from weasyprint import HTML; HTML('report-template.html').write_pdf('out.pdf')"
\`\`\`
`);

/* ---- done --------------------------------------------------------------- */
console.log(`Scaffolded "${brandName}" design system into ${outDir}`);
for (const f of written) console.log("  + " + f);
