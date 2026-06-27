# Foothold changelog

## 1.6.0, 2026-06-27

A data-protection release: founders can now produce a DPIA and record a lawful basis for every contact, plus a new validation skill. Template moves to 1.6.0. (Version note: the plugin and marketplace version files had drifted to 1.2.2 while the changelog ran to 1.5.1; they are reconciled to the changelog lineage at 1.6.0 with this release.)

Adds the `design-cheapest-test` pm-skill. It helps a founder turn a riskiest assumption into the cheapest test that could prove it wrong, with the change-my-mind result set before the test runs. The keystone of build, measure, learn, and a gap in the pm-skills set until now.

- New `Skills/pm-skills/design-cheapest-test/`: designs a small, fast, falsifiable experiment, names the metric and sample, and pre-registers the decision each result triggers (proceed, pivot, or kill). It coaches rather than authors; the founder designs the test. MIT licensed, MilUX original.
- Authored for the MilUX hackathon package and shared into Foothold, since founders validating a product need the same discipline.

Adds the `build-dpia` business skill: produces a Data Protection Impact Assessment for the founder's business from their vault. It reads existing vault context, walks the founder through any unknowns, asks about the tools they use and the types of personal data they hold, and writes a DPIA in the ICO seven-part structure to `Operations/`. It then offers to set up the quarterly lawful-basis review and to produce a PDF version. References bundle the ICO screening and lawful-basis guidance, the DPIA template, and a neutral PDF template founders can rebrand. Skill is `audited: pending`; run `skill-safety-audit` before the next tagged release (R-28).

Adds a lawful basis to the CRM so every contact records the UK GDPR Article 6 basis on which their data is processed. Good data-protection practice for founders, and the groundwork for a data protection impact assessment.

- New `lawful_basis:` frontmatter property on contacts (legitimate-interests, consent, contract, or legal-obligation), mirrored by an `lb-*` tag. Documented in `Knowledge/tagging-policy.md`, the CRM Guide and the Contacts Guide.
- The `add-contact` skill now asks which basis applies and proposes the most likely one, then writes the property and tag.
- The four shipped example contacts carry the new field.

Version note: the two version files (`plugin.json`, `marketplace.json`) currently read 1.2.2 while this changelog runs to 1.5.1. Reconcile that before the next tagged release and set the version for this change then (a minor bump, per R-22).

## 1.5.1, 2026-06-25

Adds the `red-team-investor` business skill. Template moves to 1.5.1.

- New `Skills/business-skills/red-team-investor/`: critiques any investor-facing content (pitch deck, one-pager, business plan, financial model, cold email, investment memo, teaser, data room) from a sceptical investor's point of view, calibrated to stage and content type. Organised around the market / product / execution risk triad, with a red-flag sweep, sector lenses (deep tech and TRL, regulated, marketplace, SaaS, consumer), and the hard diligence questions the content is least ready for.
- Reviews only; it does not write or improve the pitch, and contacts no one. Benchmarks cite public investor and accelerator sources (Sequoia, a16z, CRV, Y Combinator and Paul Graham, UKBAA, British Business Bank, SeedLegals) and are dated 2024 to 2026 as bands.

## Tools: Vault Viewer 1.1.0, 2026-06-23

Adds a graph view to Vault Viewer. The installed pack and template are unchanged and stay at 1.5.0; this is a repo-side tool, so `foothold-update` brings nothing new into an existing vault.

The graph is a force-directed map of the vault, drawn on a canvas in plain JavaScript so it stays offline. Nodes are notes sized by link count, edges are the links, with pan, zoom and hover. Built from feedback that new users spend their early time in the graph as they build folders from scratch.

- Click a node to isolate it with its 1st and 2nd-degree links, fading the rest, and preview the note's contents without leaving the graph.
- Labels are zoom-gated and overlap-aware, so they stay out of the way until there is room.
- Pin nodes by dragging them or shift-clicking. An optional toggle shows directional arrows for mapping networks and organisations.
- A Display panel carries the Obsidian controls (text fade, node size, link thickness) and force controls (centre, repel, link force, link distance), all remembered between sessions.
- The layout uses a Barnes-Hut quadtree, so it holds up on large vaults.
- The link index now reads both `[[wikilinks]]` and Markdown links, which also corrects backlinks in vaults that use Markdown links.

Still a single offline HTML file with the brand fonts embedded and no network requests.

## Tools: Vault Viewer 1.0.0, 2026-06-23

Adds a standalone `tools/` area at the repository root, shipping Vault Viewer v1.0.0. The installed pack and template are unchanged and stay at 1.5.0. This is a repo-side tool rather than a template addition, so running `foothold-update` brings nothing new into an existing vault.

Vault Viewer is a single HTML file that reads a Foothold vault, or any folder of Markdown notes, like a website. It needs no Obsidian and installs nothing. It removes the Obsidian dependency for the read case: hand a vault to someone who does not run Obsidian, or read your own on a machine that does not have it. It resolves wikilinks, embeds and backlinks, has full-text search and a collapsible file tree, light and dark themes, resizable columns, and an opt-in edit mode that writes back to the files. It runs fully offline and makes no network requests; the brand fonts are embedded so nothing needs downloading. The file carries no vault data, so sharing it shares the tool and none of your notes.

- New: `tools/vault-viewer/vault-viewer.html` plus a tool `README.md`.
- The root README gains a Tools section pointing to it.
- Fonts embedded under their open licences: Manrope and Bai Jamjuree (SIL OFL 1.1), Roboto Mono (Apache 2.0).

## 1.5.0, 2026-06-19

Adds the `write-sow` business skill.

- New `Skills/business-skills/write-sow/`: turns a transcript, job spec, statement of requirement, or bullet-point idea into an outcome-based Statement of Work. It shapes the contract to support an outside-IR35 position (control, substitution, mutuality, financial risk, part-and-parcel, equipment) and flags residual status risk rather than certifying status; builds a risk register scored by severity and likelihood, with a wording mitigation and a pricing response per risk; and recommends a pricing model (fixed-price per outcome, day-rate capped, or milestone-staged). Output is a branded PDF using the founder's own `Context/Brand.md` cues, plus a markdown working draft saved under `Customer Engagements/`.
- UK-focused. The IR35 content is sourced to gov.uk and HMRC and carries a not-legal-or-tax-advice boundary. The skill drafts only; signature and sending are left to the founder's own e-signature and email tools.
- Catalogued in `Skill Examples.md` (Commercial skills) and logged in the `Skills Value Register`.

## 1.4.0, 2026-06-16

Adds the pitch module and reorganises Skills into category folders.

- New `Skills/pm-skills/` set: `pitch-prep`, plus 32 product-management skills forked from phuryn/pm-skills (MIT), adapted for defence-sector founders with the proprietary method removed (see `Skills/pm-skills/NOTICE.md`).
- New pitch materials: the three-act framework (`Resources/Frameworks`), two worked example decks (`Resources/Templates`), and a public-tools reference (`Resources/Reference`).
- Skills reorganised from a flat layout into category folders (`pm-skills`, `content-skills`, `business-skills`, `crm-skills`, `meta-skills`); the Skills Guide documents the new convention.


## 1.3.0, 2026-05-30

Adds the `Customer Engagements/` top-level folder, separating work you deliver for an external organisation from work you do for yourself.

The split is binary and turns on outcome ownership: if your business owns the outcome (internal services, your own products, marketing, thought leadership, internal tooling), the work belongs in `Initiatives/`. If an external organisation owns the outcome, the work belongs in `Customer Engagements/`. Paid, sponsored, or pro-bono doesn't decide the folder; what decides it is whether there is a named external organisation on the receiving end of the delivery. Every engagement maps 1:1 to a page in `CRM/organisations/`.

Customer engagements use a three-state lifecycle (`scoping/`, `active/`, `completed/`) rather than the two-state lifecycle initiatives use. The `scoping/` subfolder is the missing piece in most early-stage workflows: it gives a real home to the work of shaping a deliverable before there is a commitment to deliver, and it absorbs the engagements that go cold without losing the CRM signal that something was once in play.

Why this matters for defence-sector founders: client work and internal product work read differently on the same dashboard. Mixing them makes "what is my current client load" harder to see than it should be, and makes case-study harvesting harder later. The split surfaces customer load cleanly, gives scoping work a defined home, and points each engagement back at the CRM organisation page that owns the relationship.

The Initiatives Guide is updated with the binary rule and a cross-link to the new Guide. The architecture doc and the template `CLAUDE.md` and `Home.md` are updated to describe both folders side by side.

## 1.2.0, 2026-05-26

Adds the `investors/` bucket to `CRM/organisations/`, pre-populated with around 120 investor entries spanning UK and European VCs, corporate VCs, fund vehicles, and government-aligned strategic investors with defence-tech or dual-use exposure.

Each entry carries the same shape: company details (HQ, founded date, fund size, stage focus, geography), an About paragraph on thesis and posture, a Key People table of named partners with verified LinkedIn URLs, a portfolio of notable defence and dual-use investments, and the framework and co-investor signals that travel with the firm. Where a partner could not be verified on LinkedIn, the entry says so rather than guessing; that honest signal is more useful in a raise than a polished gap.

The structure mirrors `defence companies/`: eight letter-based subfolders (`0-9`, `A-B`, `C-D`, `E-H`, `I-N`, `O-R`, `S-T`, `U-Z`) under the bucket, with an `Investors Index.md` at the root listing every entry and pointing to the government-aligned investors that live in `government/` (NSSIF, UK Innovation and Science Seed Fund, UKRI).

Why this matters for defence-sector founders: the investor map is the missing piece in most early-stage research workflows. Knowing which fund backs which kind of company, who the partner contact is, and which co-investors travel together is half the work of an effective raise. The bucket starts with European and UK depth because that is where most Foothold founders are raising; broadening to US and Asian funds is a later edit, not a Foothold-template task.

The Organisations Guide is updated to list the `investors/` bucket alongside the rest, with the letter-subfolder convention noted.

Thanks to inink for providing the thorough and detailed list of investors this bucket is built from.

## 1.1.0, 2026-05-24

Adds `cyber-essentials-ready`, a guided walkthrough that takes a non-IT founder through configuring their personal Mac or Windows computer to meet the UK Cyber Essentials technical controls.

Cyber Essentials is a recurring friction point for defence-sector founders selling into the MOD: it appears in supplier prequalification, in security clauses on framework agreements, and as a prerequisite for several gated frameworks. Many founders know they need it and don't know where to start. This skill closes that gap on the device side.

What the skill does:

- Walks the user through the five Cyber Essentials technical controls (firewalls, secure configuration, security update management, user access control, malware protection) one at a time, on macOS 14+ or Windows 10/11.
- Three modes: walk-through (the user clicks, the skill explains), commands (the skill stages safe commands on the clipboard, the user pastes), do-it-for-me (the skill drives System Settings via computer-use, the user retains consent per change).
- Verify mode for monthly re-checks, with drift detection (green / amber / red) and an optional remediation pass on red drift.
- Writes an evidence pack, append-only audit log, per-control compliance status snapshot, and reviewer-facing README to `Operations/Cyber-Essentials/` in the founder's vault. The pack is designed to be opened by an IASME assessor, a Cyber Advisor, or a defence customer's security team and read without further explanation.
- Registers a monthly Cowork scheduled task to keep the posture current, with a calendar-reminder fallback if scheduled tasks isn't available.

Scope is the founder's primary work computer. Mobile devices and SaaS multi-factor authentication are real Cyber Essentials requirements and the skill states up front that they are out of scope today; founders handle those separately. The skill is pinned to the IASME Montpellier question set; the pin lives in the skill's manifest, frontmatter and changelog, and gets reviewed when IASME publishes a new named release.

Skill catalogue: a new "Security and compliance skills" section in `Skills/Skill Examples.md` carries the cyber-essentials-ready entry.

Sources: NCSC Cyber Essentials overview, NCSC Platform Guides, NCSC Small Business Guide, NCSC Device Security Guidance Configuration Packs (Crown Copyright, Apache 2.0), IASME Question Set, IASME Readiness Tool, IASME Knowledge Hub, Apple Platform Security guide, Microsoft Learn.

## 1.0.0, 2026-05-23

Initial public release. Installable Obsidian vault pack for defence-sector founders, plus a Claude plugin that wires the install and update lifecycle. Includes folder structure, page templates, conventions, the `/foothold-setup` lifecycle skill, the `/foothold-update` content-update skill, and vault-bundled runtime skills: add-contact, add-organisation, add-event, prompt-master, process-interviewer, newsletter-writer, meeting-prep, late-payment-reminder. Ships pre-populated open-source defence reference content: regional defence and security clusters, public framework writeups, MOD body reference pages.
