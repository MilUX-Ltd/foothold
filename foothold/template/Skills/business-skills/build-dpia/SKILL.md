---
name: build-dpia
description: |
  Build a Data Protection Impact Assessment (DPIA) for the founder's business from
  their Foothold vault, walking them through any unknowns. The skill reads what the
  vault already knows (business context, CRM, tools, lawful basis), asks about the
  tools they use and the types of personal data they hold, and produces a DPIA in
  the ICO seven-part structure stored in their Operations folder. It then offers to
  set up a quarterly lawful-basis review and to produce a PDF version. Trigger on:
  "build a DPIA", "create a DPIA", "data protection impact assessment", "do I need
  a DPIA", "DPIA for my business", "GDPR impact assessment", or when the founder
  asks to assess the data-protection risk of how they process personal data.
version: 1.0.0
framework: "ICO DPIA template (UK GDPR Article 35)"
last_reviewed: 2026-06-27
maintainer: MilUX
license: Foothold pack, MIT
audited: 2026-06-27
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
---

# Build a DPIA

This is a guided walkthrough for a founder with limited or no data-protection background. Your job is to be a calm, plain-English helper who produces a credible Data Protection Impact Assessment (DPIA) for their business, drawing as much as possible from what their vault already knows so the founder answers as few questions as possible.

You are not a lawyer and this is not legal advice. You produce a working DPIA following the structure the UK Information Commissioner's Office (ICO) publishes. For genuinely high-risk processing, tell the founder to take professional advice and, where residual high risk remains, to consult the ICO before starting. The ICO DPIA guidance is at https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/.

## What a DPIA is, in one line

A DPIA is a documented assessment of how a project or business processes personal data, the risks that creates for people, and what is done to reduce them. Under UK GDPR Article 35 it is mandatory for "high-risk" processing, and good practice more widely.

## The hard rules

1. **Vault first, questions second.** Read what the vault already knows before asking the founder anything. Only ask about genuine gaps. See Step 2.
2. **Ask, do not invent.** If a fact is not in the vault and the founder has not told you, ask. Never fabricate a tool, a data type, a retention period, or a lawful basis.
3. **One basis per processing activity.** Lawful basis is recorded per activity, and per contact in the CRM. Use the four in `references/lawful-basis-and-screening.md`.
4. **Consent before writing or scheduling.** Show the founder the DPIA before you save it. Ask before you register any scheduled task. Ask before you generate a PDF.
5. **Plain English. British English. No em dashes. No jargon without a definition.**
6. **Not legal advice.** Say so. Flag high residual risk for professional or ICO review.

## The procedure

### Step 1. Version check

Read the local `manifest.json` next to this `SKILL.md`, then fetch the `manifest_url` it lists and compare `version`. If the remote is newer, tell the founder to run `/foothold-update` first and stop. If you cannot reach the manifest, say so and ask whether to proceed.

### Step 2. Read the vault

Before asking anything, gather what the vault already holds. Read, where they exist:

- `CLAUDE.md` at the vault root, for who the founder is, what the business does, and how it operates.
- `Context/` for the company profile, brand, and strategy.
- `CRM/contacts/` and `CRM/organisations/` to see the categories of people whose data is held, and the `lawful_basis` already recorded on contacts (the Foothold CRM default; see `Knowledge/tagging-policy.md`).
- `Knowledge/tagging-policy.md` for the lawful-basis convention.
- `Resources/` and `Operations/` for any existing tool list, connector inventory, privacy notice, or prior compliance work.
- Any existing `Operations/Data Protection Impact Assessment.md` (see Step 3).

Build a private working picture: controller identity, business purpose, the categories of personal data, the data subjects, the tools that hold personal data, retention, and any controls already in place. You will confirm this with the founder, not present it as settled.

### Step 3. New or update

If `Operations/Data Protection Impact Assessment.md` already exists, tell the founder when it was last updated and ask whether they want to review and update it, or start fresh. If it does not exist, this is a first build. Either way, continue.

### Step 4. Screen for the need

Walk the founder through the ICO high-risk screening in `references/lawful-basis-and-screening.md`. Use AskUserQuestion where a point is not already clear from the vault. Record which triggers apply. A DPIA is mandatory for high-risk processing and good practice otherwise, so you build one regardless; the screening sets the tone of Part 1.

### Step 5. Walk through the unknowns

This is the heart of the skill. For each part of the DPIA, take what you found in the vault and fill the gaps by asking. Keep questions few and concrete; offer your best answer first so the founder can simply confirm. Use the AskUserQuestion tool.

Cover, at minimum:

- **Controller and contact.** Legal entity name, the data-protection contact, and whether they have appointed a DPO (most small businesses have not, and are below the threshold; do not claim a DPO that does not exist).
- **What the business does and why it processes data.** The purposes.
- **Tools (ask explicitly).** Present the tools you found in the vault and ask the founder to confirm and add any others that hold personal data. Prompt across the common categories: email and calendar, file storage, CRM, accounting, payments, e-signature and contracts, scheduling, messaging, video and meeting capture, analytics, marketing and newsletters, AI-assisted tools, and any sector-specific systems. For each, note what personal data it holds and whether it sits outside the UK.
- **Types of data (ask explicitly).** Identity and contact data, financial and payment data, content of communications, and anything sensitive. Ask specifically whether they process any special category data (health, race, ethnicity, religion, sexual orientation, political opinions, trade union membership, genetic or biometric data), criminal offence data, or children's data. If they do, flag that extra conditions and care apply.
- **Data subjects.** Clients, prospects, suppliers, partners, employees or associates, research or study participants, and anyone whose data is gathered from public sources.
- **International transfers.** Any tool or party that processes personal data outside the UK, and the safeguard relied on.
- **Retention.** How long each kind of data is kept, and why.
- **Lawful basis.** Per processing activity, using the four bases in the reference. Note that the CRM already records a basis per contact.
- **Existing controls.** Access control, credential storage, device security, backups, who can see what.

### Step 6. Build the DPIA

Using `references/dpia-template.md`, write the DPIA into `Operations/Data Protection Impact Assessment.md` (a vault-relative path; resolve against the founder's vault root). Follow the ICO seven-part structure:

1. Identify the need for a DPIA (the screening result).
2. Describe the processing (nature, scope, context, purposes; the tools and data types from Step 5).
3. Consultation (who was consulted; the founder, any co-director, processors' terms).
4. Necessity and proportionality (lawful basis per activity; data minimisation; individual rights).
5. Identify and assess risks (each risk scored on likelihood by severity, giving low / medium / high).
6. Measures to reduce risk (mapped to each risk).
7. Sign-off and outcomes (residual risk, approval, review date).

Fill every field you have an answer for. Where something is still unknown, write it as an explicit open action in Part 7 rather than guessing. Set a review date twelve months out.

Show the founder the draft and ask for changes before and after saving. Apply British English and no em dashes.

### Step 7. Offer the quarterly review

Tell the founder that the lawful basis recorded against each contact should be checked periodically, and offer to set up the same quarterly review used as the reference pattern: a check on the first of January, April, July and October that confirms every contact has a valid lawful basis, sense-checks it, and flags anything to change.

Ask first. If they say yes, register it with `mcp__scheduled-tasks__create_scheduled_task`:

- Cron `0 6 1 1,4,7,10 *` (06:00 on the first of those months, local time), or another time the founder prefers.
- A self-contained prompt that: scans `CRM/contacts/`, checks each contact has a valid `lawful_basis` property and matching `lb-*` tag, sense-checks the basis against the contact's relationship and recency, flags data-minimisation candidates, and writes a dated review to `Operations/DPIA Reviews/` (or another folder the founder names) for the founder to act on. The task proposes only; it never edits contacts and never sends personal data anywhere external.

If `mcp__scheduled-tasks__create_scheduled_task` is unavailable or fails, fall back to writing a reminder note at `Operations/DPIA Reviews/next-review.md` with the next date, and offer to add a calendar reminder. Tell the founder which outcome happened.

Also offer to set a one-off reminder for the annual DPIA review on the review date in Part 7.

### Step 8. Offer a PDF

Ask the founder whether they want a PDF version of the DPIA. If yes, build one from `references/pdf-template.html`:

1. Convert the DPIA markdown body to HTML (pandoc if available), strip any vault wikilinks to plain text, and place it inside the template, filling the cover fields (document title, the controller, the author, the date, the review date).
2. If the founder has a brand (colours, logo, fonts) recorded in their vault, apply it. Otherwise use the clean neutral style in the template.
3. Render to PDF with WeasyPrint: `python3 -c "from weasyprint import HTML; HTML('dpia.html').write_pdf('...')"`, writing the PDF next to the markdown in `Operations/`.
4. If WeasyPrint is not installed, offer to install it (`pip install weasyprint --break-system-packages`), or fall back to leaving the styled HTML file so the founder can print to PDF from a browser. Tell the founder honestly which happened.

### Step 9. Close out

Tell the founder, in plain English, where everything is: the DPIA markdown, the PDF if made, and the review schedule or reminder. Remind them:

- This is a working DPIA, not legal advice. For high-risk processing, take professional advice, and where high residual risk remains, consult the ICO before starting.
- The DPIA is a living document. Re-run this skill, or update it directly, whenever the processing changes: a new tool, a new kind of data, a new product, or an incident.

## Consent and audit footer

This skill is maintained by MilUX as part of the Foothold pack. It does not phone home, send telemetry, or collect any data about the founder or their business. It reads the founder's own vault to draft the DPIA, writes only to the founder's `Operations/` folder (and, with consent, registers a scheduled task), and makes no external calls except the version check and, if the founder asks, fetching public ICO guidance. Every write and every schedule is made with the founder's explicit consent.
