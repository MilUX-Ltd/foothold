# Foothold — Structure and How It Works

This document explains what's inside a Foothold pack, how it's organised, and how setup and updates work. Read it once at install time so you know what you're working with.

## What you get

A Foothold pack is a working Obsidian vault. Open it in Obsidian and the structure is already in place: folders for your operator profile, your contacts and organisations, your initiatives, your reference library, and an external-scanning intelligence layer pre-populated with defence-sector reference content. You don't start from a blank vault. You start from one that already knows where the public frameworks live, which MOD body owns what, and which procurement route fits which stage of maturity.

The pack ships in three layers.

**Structure.** Folder layout, page templates, frontmatter conventions, and skills. The load-bearing part. It changes slowly and you inherit it as an opinionated default.

**Open-source content.** Pre-populated reference material you don't have to research from scratch: the post-SDR MOD structure, frameworks, portals, programmes, regional cluster pages, a procurement playbook, funding routes compared, and plain-English orientations on security clearance and export controls.

**Stubs and rules.** Empty page templates plus a documented rule, per folder, for how you grow your own knowledge base.

## The folder structure

```
Your Pack/
├── CLAUDE.md
├── Home.md
├── Getting Started - Your First Week.md
├── How to Use This Vault.md
├── Capabilities and Services/
├── Context/
├── CRM/
├── Customer Engagements/
├── Daily/
├── Ideas/
├── Initiatives/
├── Intelligence/
├── Knowledge/
├── Marketing/
├── Operations/
├── Resources/
└── Skills/
```

The pack is a flat top-level. No nested namespaces. Wikilink paths stay short and the mental model stays simple. Home.md is the live dashboard (its panels need the free Dataview plugin); the two root guides carry the first week and the working habits.

### Per-folder intent

**Capabilities and Services.** What your organisation sells and what it runs internally. Splits into `Customer-Facing Services/` for paid offers and `Internal Services/` for operational functions like Content Pillars, Content Creation Workflow, and Compliance Service. Ships with a Guide explaining the split and a canonical example service stub.

**Context.** Your own profile, your organisation, brand, strategy, team, stakeholders. The root files are templated stubs populated with your details at install time. Each ships with a worked example so you see what a well-formed page looks like.

**CRM.** Contacts, organisations, networks. The MOD-body subfolder pattern (parent organisation as folder, child organisations inside with `parent:` frontmatter and `former_name:` for rebrands) ships as the canonical pattern for absorbing MOD reorganisations without breaking your search. Ships pre-populated with the MOD structure, the regional clusters, the defence networks, and an investor reference set.

**Daily.** Standard Obsidian daily-notes pattern. The `/daily-brief` skill can write each day's note for you as a generated brief; a Guide explains the conventions, including the agent-owned-section rule.

**Ideas.** A capture-quickly, process-later inbox. Ships with a Guide that defines what belongs (early-stage ideas, sparks) and what doesn't (anything with a natural home elsewhere), so it doesn't drift into a junk drawer.

**Customer Engagements.** Work you deliver for someone else. Each engagement maps 1:1 to an organisation page in `CRM/organisations/`. Three-state lifecycle (`scoping/`, `active/`, `completed/`) reflecting how customer work actually moves: shaped, agreed, delivered. Ships with `Customer Engagements Guide.md` carrying the canonical Guide pattern and the binary rule that distinguishes engagements from initiatives.

**Initiatives.** Work you do for yourself. Internal services, your own products, marketing, thought leadership, operating-model change, internal tooling. Two-state lifecycle (`active/`, `completed/`). The split rule is binary: outcome owned by your business → Initiative, outcome owned by an external organisation → Customer Engagement.

**Intelligence.** External-facing scanning: the defence landscape (MOD structure, frameworks, portals, programmes, the procurement playbook, funding routes, the clearance and export-control orientations), events, market, competitors. The Guide codifies the "this is for external scanning, not internal artefacts" rule so the folder stays clean.

**Knowledge.** Operating rules: the rules file, frontmatter conventions, hypotheses, tagging policy. Distinct from Resources, which is your practitioner reference library. Knowledge files are policy documents your agents read at runtime.

**Marketing.** Marketing Outputs (published artefacts and active drafts) and Newsletter content. Strategy lives in `Capabilities and Services/Internal Services/Content Pillars.md`, workflow in `Content Creation Workflow.md`, and outputs here. Marketing is a function you run.

**Operations.** Runtime policy your agents read as they work: your email-signature stub, the agent-pause kill switch, messaging policy. The Guide spells out the in-scope test ("would removing it break a live agent flow?") and lists what doesn't belong here.

**Resources.** Your practitioner reference library: `Methods/`, `Ways of Working/` (including Sync and Backup and Where Your Data Lives), `Books/`, `Business/`, `Frameworks/`, `Reference/`, `Templates/`, plus the Reading List. Each subfolder has its own Guide.

**Skills.** The agent skills that ship with the pack, organised into `meta-skills/`, `crm-skills/`, `business-skills/`, `pm-skills/`, `ops-skills/`, `brand-skills/`, and `content-skills/`. Skills are executable. The content they draw on lives elsewhere in the vault.

## The Guide pattern

Every major folder ships with a `<Folder Name> Guide.md` at its root. The Guide is the contract for what belongs in the folder.

Every Guide carries five sections:

1. **Purpose.** One paragraph. What this folder is for.
2. **Structure.** What each subfolder means.
3. **Frontmatter.** Required and optional fields per page type.
4. **Add discipline.** How to add new content. Points at the relevant skill if one exists.
5. **Canonical example.** A worked reference page so you can see what good looks like.

When you're not sure where something goes, read the relevant Guide. When you can't decide between two folders, the Guide tells you.

## Templating

Foothold uses placeholders for everything specific to you. The `foothold-setup` skill fills them in during install, from your answers to the onboarding brain dump.

| Placeholder | Meaning |
|-------------|---------|
| `{{pack_name}}` | The display name of your pack |
| `{{pack_slug}}` | Slugified pack name for paths |
| `{{pack_owner}}` | Your full name |
| `{{pack_owner_first}}` | Your first name |
| `{{pack_owner_email}}` | Your primary email |
| `{{pack_owner_linkedin}}` | Your LinkedIn URL (optional) |
| `{{pack_owner_phone}}` | Your phone number (optional) |
| `{{pack_org}}` | Your organisation |
| `{{pack_org_slug}}` | Slugified organisation name |
| `{{pack_org_website}}` | Your organisation's website |
| `{{install_date}}` | The install date |

A small `.foothold/config.yml` in the pack root tracks the current substitution values, your schedule choices, and the SHA of every file as last pulled from GitHub, used by `/foothold-update`'s three-way reconcile.

## How setup and updates work

There is no bash installer and no separate plugin. Both setup and update are Cowork skills that fetch plain files over HTTPS from the public GitHub repo. See the README for the full walkthrough; in outline:

**`foothold-setup`** (run once, via the one-line prompt in the README). Lays down the folder structure, runs a guided brain dump across six categories (two rich forms, or plain questions where forms aren't available), offers a context drop for files and links, builds your canonical pages from everything you gave it, and offers the running rhythm: scheduled updates, a weekday daily brief, a monthly curation sweep, and a one-week check-in. Re-running it later is discovery-first: it reads what the vault already knows and asks only what has changed.

**`/foothold-update`** (run any time, manually or on a schedule). Compares your vault against the current state of the GitHub repo using the SHA history in `.foothold/config.yml`, and reconciles file by file: applies upstream-only changes automatically, leaves your own edits alone, adds anything new, and asks you to resolve genuine conflicts. Your personalised content is never overwritten without an explicit yes.

## One operator, agents with boundaries

Foothold is built for a single operator working with Cowork, and that is how it should be run first. What ships alongside that is a set of conventions that keep agent work disciplined as you add more of it: operating rules in `Knowledge/` that agents read at runtime, policy and signature assets in `Operations/`, agent-owned sections in daily notes, and a drafts-then-promotion pattern for anything that becomes canonical. When a second person or a second agent arrives, the same conventions carry the write boundaries; the README's small-firm section describes that path. The conventions work directly with Cowork and can be adapted to other AI tools without changing the structure; how you wire your agents in is your choice. Foothold is opinionated about the boundaries, and the implementation underneath is yours.

## The skill set

Around sixty skills ship with the pack, in seven categories. The high points:

- **meta-skills.** The pack's own lifecycle and hygiene: `foothold-setup`, `foothold-update`, `daily-brief` (writes your morning brief), `curator` (a budgeted monthly hygiene sweep), `skill-safety-audit` (run on any skill from outside before it runs, no exceptions), `skill-value-review`, `prompt-master`, `process-interviewer`.
- **crm-skills.** The high-frequency adds and their payoff: `add-contact`, `add-organisation` (carries the MOD-rebrand pattern), `add-event` (with a Chatham House Rule check at intake), `meeting-prep`, `mobilise-engagement`, and `import-relationships` for bringing your existing CRM across, connector-first, with triage.
- **business-skills.** The defence-commercial spine: `eligibility-check` (a pre-bid go/no-go gate), `bid-response` (drafting against published evaluation criteria), `write-sow`, `cyber-essentials-ready`, `build-dpia`, `red-team-investor`, `late-payment-reminder`.
- **pm-skills.** Twenty-six business-method reference skills: positioning, market sizing, pricing, personas, pre-mortems, and the rest of the standard toolkit.
- **ops-skills.** The operations wing: `process-map`, `sop-capture`, `service-blueprint`, `ai-readiness`.
- **brand-skills.** `design-system-setup`, which builds your design system from your onboarding answers.
- **content-skills.** `newsletter-writer` and `humaniser`.

Every skill carries audit frontmatter (`audited`, `audit_verdict`, `origin`, `maintainer`), and the audit discipline applies to anything you add from elsewhere.

## What ships in the open-source content layer

Pre-populated reference content sourced from publicly available material only.

- **The decision layer.** The Founder's Procurement Playbook (which route fits your maturity, timeline and offer) and Funding Routes (DASA/UKDI competitions, loans, SBRI, DTEP, NSSIF, ARIA and venture capital compared).
- **The compliance orientations.** Security Clearance Primer and Export Controls Orientation, published positions only, no folklore.
- **The landscape.** The current National Armaments structure and its visible child organisations with parent linkage, regional defence and security cluster pages, public framework writeups (DOS, G-Cloud, EDP, NGAP, DTEP and more), MOD-facing portals, and visible defence programmes (TEMPEST/GCAP, SKYNET, ZODIAC and others).
- **The reading list.** Policy and reports first (SDR 2025, the Defence Industrial Strategy, the Defence Investment Plan), then practitioner guides.

The content audit rule is binary: if the source lives in a publicly searchable place (gov.uk, MOD website, company website, LinkedIn public profile), it ships. If it would have to come from a relationship, it doesn't.

## Growing your pack

The discipline is simple. Per-folder Guides are the contract. Skills cover the high-frequency adds. The long tail follows the conventions documented in each Guide, and `How to Use This Vault.md` carries the four working habits that make the whole system improve with use.

When in doubt:

- Read the Guide for the folder you're working in.
- Copy the shape of the canonical example referenced in the Guide.
- If you can't place something, ask your agent.

The pack works because the conventions are kept tight. Adding things off-pattern is the fastest way to break it.
