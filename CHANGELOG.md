# Foothold changelog

## 2.0.2, 2026-07-02

Answers the questions the ICP review surfaced, in Matt's words.

- The one-line description is now "an integrated AI operating model and second brain for defence businesses", matching the launch graphic. It says what the pack became at 2.0.0; "a folder structure with reference content" undersold it.

- New README section, Support from MilUX: the first hour of setup consulting is complimentary, then the pack runs without us; AI enablement beyond the pack; trusted-partner referrals for Cyber Essentials and business setup; scaling support; and the UK-wide Claude associate network. The audience line and cost table updated to match.
- Provenance now says the associates in MilUX's Claude Partner Network run the pack too.
- The ChatGPT objection section notes the pack sits alongside existing AI use, adding the agentic side with policies, integration and orchestration worked out.
- `bid-response` gains "Can AI-drafted content go in a submission?": yes, with the human final pass non-negotiable and honesty if a buyer asks.

## 2.0.1, 2026-07-02

- README gains "Prefer a different stack?": a short note that the pack is plain Markdown and can be configured for open-source tools such as OpenCowork, self-hosted or already-owned models, and other sync arrangements, as bespoke work through MilUX.

## 2.0.0, 2026-07-02

The onboarding release, and a major version because it changes what installing Foothold feels like. Informed by a competitive benchmark of a comparable vault-pack product; the patterns were rebuilt, not copied, and in each case improved: their form-based onboarding is Cowork-only, ours degrades to plain questions anywhere; their operator concept writes externally unattended, our adaptations stay review-gated and vault-only.

- **The small-firm questions answered.** New `Resources/Ways of Working/Where Your Data Lives.md`: what stays local, what Claude sees and under whose terms, what never goes in the vault (classified material, export-controlled data, caveated client material, personal data without a basis), how the setup sits inside a Cyber Essentials posture, and what to say to a prime's security questionnaire. The README gains a matching section, and its team section is rewritten as "Running Foothold in a small firm": a month-by-month adoption path, the curator as a role a firm can delegate, honest per-seat maths (readers need the free Vault Viewer, not a subscription), and a "what to bring, what to leave" rule.
- **README rewritten around outcomes.** A "what changes in your first 30 days" section, the ChatGPT-and-folders objection answered, an honest cost-and-effort table, a "Yours, forever" ownership clause, a maintainer provenance paragraph, an early-user quote, and the Vault Viewer promoted to the try-before-you-install path.
- **Onboarding is now a guided brain dump.** `foothold-setup` Phase B replaces six sequential questions with two rich forms (six categories, same substance): per category a brain-dump box, a links-and-paths field, and file upload, with dictation transcripts explicitly recommended as the highest-yield input. Bullets are inspiration, not required fields; blank skips; everything offered is ingested greedily into the build corpus. Falls back to the question flow where the form surface isn't available.
- **Re-running setup is now discovery-first.** The re-run flow reads config and Context silently, presents a "discovered from your vault" summary, and asks only "what's changed, or what did I get wrong?". The skill never asks for a value the vault already holds.
- **Probe, don't ask.** `import-relationships` detects and read-only-probes CRM connectors before asking anything, reporting exact errors with a skip-or-fix choice; `daily-brief` does the same for the calendar, and reports a failing connector once rather than daily.
- **The first-week check-in became a personalisation loop.** "A week in — what feels wrong, missing, or harder than it should be? I'll change it." Smallest change, confirm, ask what else, and park unreached wants in `Ideas/` for the next session.
- **New `Skills/ops-skills/` category, four skills, replicated from Footing 2.0.0.** `process-map`, `sop-capture`, `service-blueprint`, and `ai-readiness`. Foothold founders are new to AI too, and defence founders sell services; the original plan to hold two of these back was wrong and is recorded as such. Same content as Footing's, pack licence line aside.
- **Setup now creates the structural folders explicitly** (Step A.3b, canonical list in the skill). Git carries no empty directories, so the tree fetch alone never could; this closes the gap where a fresh install arrived without the `Customer Engagements/` states, `Ideas/`, `Initiatives/`, or `Daily/`.
- **New `Skills/meta-skills/curator/`: the budgeted curation sweep.** Fixes mechanical defects with exactly one right answer (broken wikilinks with an unambiguous target, missing frontmatter derivable from the folder Guide, unescaped pipes in table wikilinks) within hard per-run caps: 200 reads, 20 fixes, 30 report items, folder rotation for larger vaults. Everything needing judgement goes to a dated Curation Report instead of being touched; no renames, no archiving, no deletion, ever. Setup offers a monthly schedule (3rd of the month). The skill curates hygiene, not knowledge; meaning stays with the owner. MIT licensed, MilUX original.
- Plugin and marketplace manifests reconciled to 2.0.0 (they had drifted to 1.6.0 while the changelog ran to 1.10.0).

## 1.10.0, 2026-07-02

- New `How to Use This Vault.md` at the vault root: the four working habits that make the system compound. Brief Claude like an intern in its first week (it never forgets a good briefing, because the briefing lives in the vault); describe your processes, because a process you can describe is a process you can automate; watch for repeatable patterns worth turning into a skill or a schedule, and tell Claude to watch too; and review both the work (self-review against the brief before anything is called done) and the working (regular retrospectives whose output is always a permanent change: a rule, an amended skill, a corrected Context page). Home.md and the first-week guide both link to it.

## 1.9.0, 2026-07-02

Kills the write-three-lines daily-note ritual shipped earlier today in 1.8.0. Asking the user to report what happened yesterday is a scrum anti-pattern; the vault already knows.

- New `Skills/meta-skills/daily-brief/`: writes the day's note as a brief FOR the user, generated from engagements, initiatives, items rolled forward from previous notes, upcoming events, and (where a calendar connector exists) today's meetings. Owns a `## Daily Brief` section per the Daily Guide convention and never touches the user's own writing. Hard cap of seven needs-attention items; a quiet day gets a short brief, honestly. MIT licensed, MilUX original.
- `foothold-setup` Phase C now offers to schedule `/daily-brief` for weekday mornings at 08:00.
- `Getting Started - Your First Week.md` Day 3 rewritten: run the brief, schedule it if it earns its place. The standup ritual is gone.
- `Daily Guide.md` updated: the note can be created by the brief each morning; the user writes everywhere else.

## 1.8.0, 2026-07-02

The first-week release: the pack now walks a new user from install day into a working habit, and the vault they land in has a live front door.

- New `Getting Started - Your First Week.md` at the vault root: one small win a day (foundations, CRM import or seeding, the daily-note habit, design system, landscape orientation), then week two onwards. Home.md now leads with it.
- `foothold-setup` Phase C now offers a one-off check-in scheduled seven days after install, revisiting the first-week list with the user.
- `Home.md` rewritten: the Dataview query suggestions are now live query blocks (engagements in scoping and active, open initiatives, recent contacts, latest published), with a one-line pointer to installing the free Dataview plugin. Panels fill themselves as the vault grows.
- New `Intelligence/defence-landscape/Funding Routes.md`: DASA/UKDI competitions, Defence Innovation Loans, Innovate UK/SBRI, DTEP, NSSIF, ARIA and venture capital compared on size, time to money and equity cost, with the three questions that choose between them and a warning about grant-chaining.
- New `Resources/Reading List.md`: policy and reports first (SDR 2025, Defence Industrial Strategy 2025, Defence Investment Plan, NAD Group pages), then practitioner guides (the Hitchhiker's Guide to the Valley of Death, DASA proposal guidance), then a deliberately short book shelf. Deliberately not filed under Books, because the most important reading here is not books.
- New `Resources/Ways of Working/Sync and Backup.md`: Obsidian Sync, git, iCloud, OneDrive/Dropbox/Google Drive and Syncthing compared honestly, including the iOS limitation on generic cloud drives, plus the sync-is-not-backup discipline and a warning against stacking sync systems.
- New `Skills/business-skills/bid-response/`: structures and drafts a tender or competition response around the opportunity's own published evaluation criteria, compliance matrix first, evidence-only claims, social value as a scored section, and an assessor-lens red-team before submission. Doctrine sourced from published gov.uk guidance (DASA assessment criteria, MOD Commercial toolkit, Selling to government, the Procurement Act 2023 MAT basis, the Social Value Model) and the APMP body of knowledge. MIT licensed, MilUX original.
- New `Skills/crm-skills/import-relationships/`: back-ported from Footing 1.2.0. Seeds the CRM from a live CRM connector, a CSV export, or a guided interview, with triage before import and a preview gate before any batch write. Adapted to Foothold's organisation buckets and its pre-populated MOD pages (link, don't duplicate).

## 1.7.0, 2026-07-02

The procurement navigation release: the landscape pages told you what exists, this release tells you which route fits your situation and whether you can clear the walls before you bid.

- New `Intelligence/defence-landscape/Founder's Procurement Playbook.md`: the decision layer over the Frameworks, Portals and Programmes catalogues. Routes by maturity (funded R&D at TRL 1 to 4, proof and access at 5 to 7, the three procurement doors at 8 plus, and a separate services path), by timeline, then route-independent hygiene and the common failure modes. Written against the 2026 landscape: NAD Group fully established April 2026, UKDI inside NA-Innov, the DASA Open Call closed pending reopening around UKDI FOC, DOSBG as the SME front door.
- New `Intelligence/defence-landscape/Security Clearance Primer.md`: clearance levels (BPSS through eDV), personnel versus Facility Security Clearance, realistic 2026 timescales, and the founder traps (no self-sponsorship, clearance in bid qualification). Published UKSV and MOD positions only; no folklore.
- New `Intelligence/defence-landscape/Export Controls Orientation.md`: the UK regime in one page (control lists, ECJU, SPIRE, licence types, the Dual-Use OGEL in force 25 June 2026), the transfer-counts-as-export trap including US-origin ITAR/EAR contamination, and a five-question screening checklist. Orientation, not legal advice, and it says so.
- New `Skills/business-skills/eligibility-check/`: a pre-bid go/no-go gate. Four walls in kill order (cyber floor per Def Stan 05-138 Issue 4, clearance floor, export position, commercial basics), verdict page written to the engagement folder, and a mandate to say no. MIT licensed, MilUX original.
- Fixed: `MOD Structure.md` dated the NAD Group's establishment to April 2026; it was established March 2025 and declared fully established April 2026. The Defence Landscape Index and MOD Structure now agree.
- `Defence Landscape Index.md` topical maps list now leads with the playbook.

## 1.6.0, 2026-07-01

Removes the marketplace install step from the getting-started flow.

The previous flow required users to add the Foothold GitHub repo as a Cowork marketplace, install the plugin, and then run `/foothold-setup`. The marketplace step caused friction — particularly on Windows — and added no value that the skill itself does not provide. The setup skill fetches directly from GitHub, so the plugin was only ever a delivery wrapper for a URL.

The new flow is a single step: paste one line into a Cowork chat and the skill runs. No marketplace, no plugin install, no slash command required.

- README rewritten: Steps 1 and 2 (Add marketplace, Install plugin) replaced with a single prompt-based step.
- Troubleshooting entry for marketplace errors removed.

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
