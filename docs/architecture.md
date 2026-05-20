# Foothold — Structure and How It Works

This document explains what's inside a Foothold pack, how it's organised, and how to use the install, rename, and update commands. Read it once at install time so you know what you're working with.

## What you get

A Foothold pack is a working Obsidian vault. Open it in Obsidian and the structure is already in place: folders for your operator profile, your contacts and organisations, your initiatives, your reference library, and an external-scanning intelligence layer pre-populated with defence-sector reference content. You don't start from a blank vault. You start from one that already knows where the public frameworks live and which MOD body owns what.

The pack ships in three layers.

**Structure.** Folder layout, page templates, frontmatter conventions, and skills. The load-bearing part. It changes slowly and you inherit it as opinionated default.

**Open-source content.** Pre-populated reference material you don't have to research from scratch: regional defence and security cluster pages with their public links, public framework writeups, MOD body reference pages.

**Stubs and rules.** Empty page templates plus a documented rule, per folder, for how you grow your own knowledge base.

## The folder structure

```
Your Pack/
├── CLAUDE.md
├── Home.md
├── Capabilities and Services/
├── Context/
├── CRM/
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

The pack is a flat top-level. No nested namespaces. Wikilink paths stay short and the mental model stays simple.

### Per-folder intent

**Capabilities and Services.** What your organisation sells and what it runs internally. Splits into `Customer-Facing Services/` for paid offers and `Internal Services/` for operational functions like Content Pillars, Content Creation Workflow, and Compliance Service. Ships with a Guide explaining the split and a canonical example service stub.

**Context.** Your own profile, your organisation, brand, strategy, team, stakeholders. The root files are templated stubs populated with your details at install time. Each ships with a worked example so you see what a well-formed page looks like.

**CRM.** Contacts, organisations, networks, programmes, portals, frameworks. The MOD-body subfolder pattern (parent organisation as folder, child organisations inside with `parent:` frontmatter and `former_name:` for rebrands) ships as the canonical pattern for absorbing MOD reorganisations without breaking your search.

**Daily.** Standard Obsidian daily-notes pattern. Ships with a daily-note template and a Guide explaining how to use it. Wire up daily briefings or signal scans as you add agent integrations of your own.

**Ideas.** A capture-quickly, process-later inbox. Ships with a Guide that defines what belongs (early-stage ideas, sparks) and what doesn't (anything with a natural home elsewhere), so it doesn't drift into a junk drawer.

**Initiatives.** Active and completed initiative pages following the Foothold pattern. Ships with `Initiatives Guide.md` carrying the canonical Guide pattern and one fully-worked example initiative as a scaffold.

**Intelligence.** External-facing scanning: market, defence-landscape (clusters, programmes, MOD bodies, frameworks, portals), competitor analysis, literature. The Guide codifies the "this is for external scanning, not internal artefacts" rule so the folder stays clean.

**Knowledge.** Agent operating rules: the rules file, frontmatter conventions, hypotheses, tagging policy, domain notes. Distinct from Resources, which is your practitioner reference library. Knowledge files are policy documents your agents read at runtime.

**Marketing.** Marketing Outputs (published artefacts and active drafts) and Newsletter content. Foothold's three-layer marketing pattern keeps strategy in `Capabilities and Services/Internal Services/Content Pillars.md`, workflow in `Capabilities and Services/Internal Services/Content Creation Workflow.md`, and outputs here in Marketing. Marketing is a function you run.

**Operations.** Load-bearing for the agent stack. Ships pre-populated with your email-signature stub and runtime policy files your agents read at message-send time. The Guide spells out the in-scope test ("would removing it break a live agent flow?") and lists what doesn't belong here.

**Resources.** Your practitioner reference library. Ships with a six-subfolder structure: `Methods/`, `Ways of Working/`, `Books/`, `Business/`, `Frameworks/`, `Reference/`, `Templates/`. Each subfolder has its own Guide explaining what belongs.

**Skills.** The agent skills that ship with the pack. Skills are executable. The content they draw on lives elsewhere in the vault.

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

Foothold uses placeholders for everything specific to you. The installer fills them in at install time. You can re-substitute at any point via `foothold rename`.

| Placeholder | Meaning |
|-------------|---------|
| `{{pack_name}}` | The display name of your pack |
| `{{pack_slug}}` | Slugified pack name for paths |
| `{{pack_owner}}` | Your full name |
| `{{pack_owner_first}}` | Your first name |
| `{{pack_owner_email}}` | Your primary email |
| `{{pack_org}}` | Your organisation |
| `{{pack_org_slug}}` | Slugified organisation name |

A small `.foothold/config.yml` in the pack root tracks the current substitution values. `foothold rename` reads from it before writing new values, so renaming is safe from any state.

## The three commands

### `foothold install`

One bash command. Lays down the pack, runs the templating pass, writes `.foothold/config.yml` to track your substitution values, optionally initialises a git repo in the pack folder. Prints next-step instructions.

### `foothold rename <new-name>`

Re-runnable. Replaces every templated value, renames any folder containing a placeholder in its name, refuses to run if you have uncommitted changes so you can roll back if anything looks wrong. This is how you take your pack from "Foothold" to your own brand name cleanly.

### `foothold update`

Pulls the latest open-source content updates, new skills, and structural improvements. Prints a summary before applying. Per-group confirmation, so you can accept some changes and skip others. Manual command in v1. A scheduled-task version arrives in v1.1.

## The agent stack

Foothold ships with a multi-agent stack pattern. The structure carries clear write boundaries between research, curation, and execution, with explicit handoffs between them. You bring your own agents and plug them into the structure.

The pattern works directly with Anthropic's Cowork, which is where Foothold is most at home. It can be adapted to other AI tools without changing the structural conventions.

The pack ships the supporting pieces:

- Agent operating rules in `Knowledge/`.
- Runtime policy and signature assets in `Operations/`.
- A structured outputs pattern for upstream-to-downstream handoffs.

How you wire your agents into the structure is your choice. Foothold is opinionated about the boundaries. The implementation underneath is yours.

## Skills that ship in v1

- **add-contact.** Pulls public information about a contact you've met, drafts a contact page, asks you to confirm before writing.
- **add-organisation.** Same, for an organisation. Carries the MOD-body rebrand pattern (one page per current identity with `former_name:` frontmatter, parent linkage) so MOD restructures don't break your CRM.
- **add-event.** For cluster events, conferences, talks. Captures the event flow including a Chatham House Rule check at intake.
- **add-cluster-event.** Specialisation for RDSC events.

## What ships in the open-source content layer

Pre-populated reference content sourced from publicly available material only.

- **Regional Defence and Security Clusters.** All nine UK RDSC pages with their public links and member-club lists where public.
- **Public frameworks.** UK gov frameworks (DOS, G-Cloud, EDP, NGAP), MOD acquisition portals, defence-relevant procurement instruments.
- **MOD body reference pages.** The current National Armaments structure (NA-Intl, NA-C&I, NA-P&P, NA-Innov, NA-M, NA-C, NA-L&S, NA-D&D, DIO, plus the National Armaments Delivery Executive) and the visible child organisations with parent linkage.
- **MOD-facing portals.** Five of the most useful, with public-facing entry points.
- **Visible defence programmes.** TEMPEST/GCAP, SKYNET, ZODIAC, MORPHEUS Test & Reference Centre, and others.

The content audit rule is binary: if the source lives in a publicly searchable place (gov.uk, MOD website, company website, LinkedIn public profile), it ships. If it would have to come from a relationship, it doesn't.

## Growing your pack

The discipline is simple. Per-folder Guides are the contract. Skills cover the high-frequency adds (contacts, organisations, events). The long tail follows the conventions documented in each Guide.

When in doubt:

- Read the Guide for the folder you're working in.
- Copy the shape of the canonical example referenced in the Guide.
- If you can't place something, ask your agent.

The pack works because the conventions are kept tight. Adding things off-pattern is the fastest way to break it.
