---
name: mobilise-engagement
description: "Bootstrap a Customer Engagement during the scoping phase. Use when the user says 'mobilise <customer>', 'start scoping <customer>', 'set up the engagement with <customer>', 'onboard the <customer> engagement', 'begin mobilisation for <customer>', or asks to kick off a new piece of client work. Scaffolds the engagement folder in Customer Engagements/scoping/, creates the index page with the Outcome, Information Architecture, and delivery management sections, and drops in stakeholder map, comms plan, RAID log, outcome, and mobilisation checklist seeded from CRM. Idempotent: detects an existing scoping folder and retrofits rather than overwriting. Does not promote engagements to active — that is a deliberate manual call the user makes when the contract is signed or the start date lands."
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
license: MIT
---

# Mobilise Engagement

Sets up a new Customer Engagement during scoping. Produces just enough scaffolding to start working: an index page with the customer outcome and the per-engagement information architecture mapping, a CRM-seeded stakeholder map, a draft comms plan, a single combined RAID log, an outcome one-pager, and a mobilisation checklist running through to "on contract".

Each engagement also gets delivery management sections stubbed at scaffold time (Scope and Deliverables acceptance table, engagement-level Definition of Done, Change Control, Capacity and Availability, Reporting and Governance Cadence on the comms plan, Benefits Measurement on the outcome page, Engagement Health in the frontmatter, Data Classification on the IA table). All start as `<TBC>` and are filled during scoping conversations with the customer. Each turns into a gate on the mobilisation checklist.

## Trigger

Use this skill when the user mentions starting work with a new customer, or wants to formalise scoping for one already in pipeline. Typical phrases:

- "Mobilise the engagement with <customer>"
- "Start scoping <customer>"
- "Set up the engagement folder for <customer>"
- "Onboard the <customer> engagement"
- "Begin mobilisation for <customer>"
- "Kick off the <customer> work"

If the user names a customer plus a phrase implying setup, kickoff, scoping, mobilisation, or onboarding, this skill applies.

Do not trigger on internal initiative kickoff. Internal work uses `Initiatives/`, not `Customer Engagements/`. See `Initiatives/Initiatives Guide.md`.

## Inputs

The skill needs three facts to scaffold. Ask the user for any that are missing; do not guess.

1. **Customer organisation.** The wikilink target in `CRM/organisations/`. If the page doesn't exist, halt and suggest the `add-organisation` skill first.
2. **Customer name as it appears in the folder name.** Title case, separators as the customer's CRM page uses. The skill defaults this from the CRM org page name; confirm with the user if it differs.
3. **Engagement title.** Short, distinctive label for this piece of work (e.g. `Discovery`, `Product Support`, `Mobilisation Sprint`). The combined `<Customer> - <Engagement Title>` becomes the folder name.

Optional but useful:

- **Customer outcome.** One-sentence statement of what the customer is seeking to achieve. If the user provides it at trigger time, the skill seeds the Outcome section. Otherwise the section is stubbed for the user to complete during the customer alignment conversation.
- **Work-tracking card.** If a card already exists on a separate work-tracking system, the user names it and the skill links rather than creates.

## Step 1 — Detect existing folder

Check `Customer Engagements/scoping/<Customer> - <Engagement Title>/`.

- **No folder.** Scaffold from scratch (Step 3 onwards).
- **Folder exists with only an index file.** Retrofit: keep the existing index content, layer the new sections (Outcome, Information Architecture, delivery management blocks) on top, drop in the missing artefact files.
- **Folder exists with all artefacts.** Refresh mode: ask the user which section(s) to update (stakeholder map from current CRM, RAID seeded, checklist refreshed against current progress). Do not overwrite existing content blindly.

Retrofit is the common case for the first few invocations because engagements are often already in flight.

## Step 2 — Resolve work-tracking context

If the user uses a work-tracking system (Linear, Asana, Trello, Businessmap, etc.), the engagement should map to a card on the relevant board. This is optional. If the user does not yet use a tracking system, leave the field empty in the index and continue.

1. If the user names a card or URL, record it for the IA table.
2. If a tracking system is in use but no card exists, create one with title `<Customer> - <Engagement Title>` and a description that back-links to the Obsidian engagement index page.
3. If no tracking system is in use, the engagement page in the vault carries the operational layer itself.

## Step 3 — Scaffold folder and files

Create (or update, in retrofit mode):

```
Customer Engagements/scoping/<Customer> - <Engagement Title>/
├── <Customer> - <Engagement Title>.md                           Engagement index
├── <Customer> - <Engagement Title> - Outcome.md                 Customer outcome detail
├── <Customer> - <Engagement Title> - Stakeholder Map.md         Skeleton, seeded from CRM
├── <Customer> - <Engagement Title> - Comms Plan.md              Empty table plus Reporting Cadence
├── <Customer> - <Engagement Title> - RAID Log.md                Single combined log
└── <Customer> - <Engagement Title> - Mobilisation Checklist.md  Items, all unchecked
```

**Naming convention — title case, both folder and files.** The folder is named `<Customer> - <Engagement Title>`. The index file inside is named the same as the folder. Sibling artefact files extend the pattern: `<Customer> - <Engagement Title> - <Artefact>.md`. Title case with spaces and capitals, plain hyphen with surrounding spaces (` - `) as the separator. No em dashes.

The customer prefix matters because the same customer can have multiple engagements over time. The engagement title differentiates them. The artefact suffix makes vault search unambiguous: a bare search for `Outcome` should always resolve to one file, not several.

Use the templates in `references/`. Substitute `{{folder_name}}` (e.g. `Acme - Discovery`), `{{title}}` (the spoken form for prose use), `{{customer_wikilink}}`, `{{tracking_card_url}}`, `{{today_iso}}`, and `{{outcome}}` placeholders at write time.

**Subfolders.** The skill does not pre-create any subfolders. The canonical set (`meetings/`, `research/`, `specs/`, `decisions/`, `drafts/`, `deliverables/`, `notes/` as a rare catch-all) is documented in the Customer Engagements Guide. Folders are created the moment the first piece of content lands in each. The skill writes a hint in the engagement index Next Steps so it is obvious where the first alignment meeting note (`meetings/`) and the customer's brief or job spec (`specs/`) should land when they arrive.

**Decisions.** Material decisions go in `decisions/`, one file per decision, using the ADR template (`references/decision-template.md`). Naming: `D-NN <short title>.md` where NN increments. A decision without considered alternatives is a note, not a decision; the template enforces that distinction.

**Engagement health.** The index carries `health:` and `last_health_check:` frontmatter (default `health: green` at scaffold, refreshed at each formal status report). Home.md surfaces health across all live engagements via a Dataview block.

**Delivery management sections.** Beyond Overview / Outcome / Customer / IA / Scope / Status, the index template carries: Scope and Deliverables acceptance table, engagement-level Definition of Done, Change Control, Capacity and Availability, Engagement Health, plus a pointer to the comms plan's Reporting and Governance Cadence section and the outcome page's Benefits Measurement table. All start as `<TBC>` stubs and are filled during scoping conversations with the customer. The mobilisation checklist tracks each as a separate gate.

## Step 4 — Seed the stakeholder map from CRM

Walk `CRM/organisations/<...>/<Org>.md` and `CRM/contacts/` for contacts where `organisation == <Org>` or where the contact page wikilinks the org.

Drop each contact into the four-quadrant table at default placeholder values (Influence: TBC, Interest: TBC, Strategy: TBC). Mark each row "needs review" in a notes column.

If the org has no CRM contacts yet, leave the stakeholder rows empty and write a note at the top saying "no CRM contacts found at this org; populate during first customer conversation".

This is a skeleton, not a draft. The user sharpens it through customer conversations.

## Step 5 — Seed the RAID log

Add three default rows the skill writes for every mobilisation:

- "Outcome statement needs customer confirmation" (status: open).
- "Information architecture needs external storage paths confirmed" (status: open).
- "Stakeholder map needs user review" (status: open).

These exist to make the RAID file useful from day one rather than appearing as an empty table.

## Step 6 — Seed the Outcome page

`<...> - Outcome.md` is the one-pager that captures what the customer is seeking to achieve. It is the operational anchor for "why are we doing this work". One paragraph at the top, room underneath for refinement notes, plus the Benefits Measurement table.

If the user supplied an outcome at trigger time, write it in. If not, stub the paragraph with `<outcome to be confirmed with customer — capture in the first scoping conversation>` so the file flags its own incompleteness.

## Step 7 — Walk through the mobilisation checklist

Present the checklist contents to the user in chat, calling out which items the skill has already done (folder scaffolded, CRM seeded, tracking card linked) and which need user input next. Do not auto-tick anything the user has not explicitly confirmed.

## Step 8 — Update the engagement index

The index page is the canonical entry point. After all artefacts exist, write:

- **Overview**: one paragraph.
- **Outcome**: link to the outcome file plus a one-line summary.
- **Customer**: wikilink to CRM org plus named stakeholders (pulled from the seeded stakeholder map).
- **Information Architecture**: the table populated with the tracking card URL and stubs for any external storage systems the user uses (cloud drive, document library, reference store, accounting tool) plus a row for data classification.
- **Current Status**: one paragraph reflecting where scoping is.
- **Scope and Deliverables**: stubbed table until SoW is agreed.
- **Definition of Done**: stubbed paragraph until agreed with customer.
- **Reporting and Governance Cadence**: pointer to the comms plan.
- **Change Control**: stubbed paragraph until agreed.
- **Capacity and Availability**: stubbed paragraph.
- **Engagement Health**: green at scaffold, with reasoning.
- **Key Resources**: wikilinks to the artefact siblings plus the CRM org plus the tracking card.
- **Next Steps**: opens with "Schedule the client alignment activity" if it hasn't happened yet. The skill does not run that activity; existing meeting prep flow handles capture.

## Step 9 — Report in chat

Tell the user:

1. What was created or updated (file list, with retrofit / fresh marker per file).
2. The tracking card URL (created or linked, if applicable).
3. The checklist items the skill has already ticked.
4. The next actions the user owns (outcome confirmation, IA paths, stakeholder map review, delivery management stubs).

Keep the chat output short. The work has been done in the vault; the chat is the receipt.

## Out of scope

- **Promotion from scoping to active.** A separate skill (or a `--promote` flag here later) handles the folder move from `scoping/` to `active/`, the wikilink rewrite, and the tracking system column shift. Manual trigger, by the user, on signed contract or confirmed start date.
- **Lean UX Canvas, personas, high-level workflow mapping.** These are downstream discovery artefacts, not mobilisation. They land in `active/<...>/research/` once delivery starts.
- **Contract drafting.** The skill records that a contract is needed and where the signed version lives. It does not produce the contract.
- **Meeting capture.** Existing meeting-prep flow handles this. The skill only flags the alignment activity needs scheduling.
- **Initiatives.** This skill is customer-side only. Internal work goes through whatever pattern emerges for `Initiatives/`.

## Maintenance notes

- The skill assumes a single tracking-system swim lane or board section for service delivery. If a multi-board or per-customer lane setup emerges, the Step 2 search strategy needs revisiting.
- Template files in `references/` are the canonical structure. When a template changes, update the template here.

## Related

- [[Customer Engagements/Customer Engagements Guide|Customer Engagements Guide]]. Defines the binary scope rule, the lifecycle, and the index template this skill produces.
- [[Initiatives/Initiatives Guide|Initiatives Guide]]. Sister Guide. Internal work, not customer.
- [[CRM/CRM Guide|CRM Guide]]. Customer organisations and contacts. Every engagement maps 1:1 to an organisation here.
- `add-organisation` skill. Prerequisite when the customer org doesn't yet exist in CRM.
- `meeting-prep` skill. Used to scaffold the customer alignment activity meetings, not the activity itself.
- `late-payment-reminder` skill. Downstream, once invoicing starts.
