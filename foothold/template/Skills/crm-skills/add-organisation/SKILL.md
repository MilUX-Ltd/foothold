---
name: add-organisation
description: Add a new organisation to the CRM. Pulls public information about the company, drafts an organisation page, asks the user to confirm before writing. Use when the user says "add an organisation", "add <company>", "capture <organisation>", "log this company", or runs /add-organisation. Handles defence companies, MOD bodies, non-defence companies, and academic institutions. Bakes in the rebrand pattern (former_name frontmatter for renamed orgs) and the parent-folder pattern (for MOD-body restructures).
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
---

# add-organisation

USE WHEN the user runs `/add-organisation` or asks to capture a new organisation into the CRM. Distinct from `add-contact` (people) and `add-event` (events).

## Pre-flight

Confirm you're in a Foothold pack: check that `CLAUDE.md` exists at the vault root and that `CRM/organisations/` exists. If not, suggest running `/foothold-setup` first.

If the user said something like "add an organisation" without naming the company, ask: "Which organisation would you like to add?" and wait for the name (or a website URL).

## Phase A — Gather identity

Collect:

- **Organisation name.** Required. Use the canonical legal name where possible (e.g. "QinetiQ Group plc"), with a shorter common form in the body if that's what they go by ("QinetiQ").
- **Website.** Required if known. If the user only gave a name, look up the official site or ask.
- **Sector.** Required. One of: defence, MOD, non-defence, academic-and-research.
- **Parent organisation.** Optional. If the new org is a subsidiary, child agency, or operating unit, capture the parent.
- **Former name(s).** Optional. If the org has been renamed.
- **Public LinkedIn page.** Optional but useful.
- **Public contacts.** Optional. Roles and named individuals only if they're publicly listed (About page, LinkedIn).

Accept paste: a website URL, a Companies House link, a LinkedIn company page, or free text.

## Phase B — Research

If a website was provided or you can derive one, call WebFetch on the home page and the About / Leadership pages. Extract:

- One-line description of what the company does.
- Sector (confirm against user input).
- Size signal (employee count where stated).
- Public leadership (founders, CEO, MD, named directors).
- Headquarters location.
- Recent public news where directly relevant (recent framework appointments, named partnerships).

If a Companies House URL is provided, fetch for incorporation date and registered office. If a LinkedIn company page is provided, fetch for headcount and public posts.

**Critical:** public information only. If the user wants to add private engagement context (deal value, internal contacts, NDA-bound content), do it in a separate body section, never in frontmatter, and confirm twice before writing.

## Phase C — Classify subfolder

Determine the destination subfolder.

For the defence-sector default Foothold setup:

- `CRM/organisations/defence companies/` for commercial defence suppliers, primes, defence SMEs, dual-use tech firms.
- `CRM/organisations/mod/` for MOD entities, executive agencies, NAD Group bodies, the National Armaments structure.
- `CRM/organisations/non-defence companies/` for partners, customers, suppliers outside defence.
- `CRM/organisations/academic and research/` for universities, research labs, think tanks, R&D centres.

If the user is in a non-defence sector, the subfolders may be different. Use Glob on `CRM/organisations/` to see what exists and ask the user where the new org belongs if it's not obvious.

## Phase D — Handle parent-child

If the user mentioned a parent organisation:

1. Check whether the parent exists in `CRM/organisations/`.
2. If yes, the new org goes inside the parent's folder. Pattern: `CRM/organisations/<sector>/<Parent Name>/<New Org Name>.md`. Set `parent:` in the new org's frontmatter to the parent's wikilink.
3. If no, ask the user: should the parent be created first, or should this org go at the sector top level and the parent linkage be added later? Suggest creating the parent first if the user expects more children under it.

This pattern handles MOD-body restructures cleanly: when MOD reorganises, you can add child orgs into the parent folder without renaming or splitting existing pages.

## Phase E — Handle rebrand

If the user mentioned that the org has been renamed (or you found this in the research pass):

1. Capture the new name as the canonical page name and the H1.
2. Add `former_name: "<Old Name>"` to frontmatter.
3. Add a rename callout under the H1: `> Renamed <date> from <Old Name>. Source: <citation>.`
4. Do not create a separate page for the old name. One canonical page, one current identity.

If the rebrand also means the org now sits inside a different parent (e.g. an MOD body restructure that grouped child agencies under a new parent), use the parent-folder pattern from Phase D too.

## Phase F — Draft

Draft the organisation page in memory. Use this shape:

```yaml
---
type: organisation
name: <Canonical Name>
status: active | dormant | alumni | target
website: <URL>
sector: defence | mod | non-defence | academic
created: <today, ISO>
parent: <wikilink to parent if applicable>
former_name: <old name if renamed>
tags: [<contextual tags>]
---

# <Canonical Name>

> Renamed <date> from <Old Name>. <Citation>. <If rebrand applies.>

## Company details

- **Website:** [<url-no-protocol>](<URL>)
- **Sector:** <Sector>
- **Size:** <employee band if known>
- **Headquarters:** <city / country if known>
- **Founded:** <year if known>
- **Public leadership:** <names with roles, only if publicly listed>

## What <Name> does

<One or two paragraphs of public-info description. Drawn from the company's own about page or other public sources. Plain English.>

## Recent activity

<Recent publicly-known news if directly relevant: framework appointments, named partnerships, funding announcements. Each item dated and sourced.>

## Key contacts

| Name | Role | Email |
|------|------|-------|
| [[CRM/contacts/active contacts/<Name>\|<Name>]] | <Role> | <Email if public> |

<Only include this table if there are publicly listed named individuals OR existing CRM contacts at this org. Use escaped pipes in wikilinks per R-01.>

## Source material

- <URLs cited above>

## Related

- <Sibling orgs, parent, sister bodies if relevant>
- <Frameworks they're on, programmes they support, networks they belong to>
```

Fill every field you have data for. Omit any section with no content.

## Phase G — Confirm

Show the draft to the user. Ask:

> "Here's the organisation page I'd write to `CRM/organisations/<path>/<Name>.md`. Anything to change before I save it?"

Wait for explicit confirmation or amendments.

## Phase H — Write

Write the file to the determined path. Use the canonical organisation name as the filename. For acronymic abbreviations, the convention is `Full Name (ACRONYM).md`.

## Phase I — Cross-reference

Check for related entities:

- **Contacts mentioned.** If named individuals appeared in the user's input or in the research pass, check whether they exist in `CRM/contacts/`. Suggest running `/add-contact` for any that don't.
- **Frameworks, programmes, portals.** If the user mentioned any (or the research pass surfaced public framework appointments), check whether the relevant `Intelligence/defence-landscape/...` pages exist and link to them.
- **Parent / child orgs.** If you placed the new org inside a parent folder, ensure the parent page links back to the child.

Do not auto-create related entities. Suggest the user run the relevant skill, or do it themselves.

## Guidelines

- Public information only. Private engagement context goes in a clearly-marked body section and only with double confirmation.
- One canonical page per current organisational identity. Rebrands use `former_name:`, not parallel pages.
- Use the parent-folder pattern for MOD-body restructures and other parent-child relationships.
- Confirm before writing. Never write an organisation page without explicit user confirmation.
- Cross-reference into CRM/contacts/ and Intelligence/defence-landscape/ so the graph stays connected.
