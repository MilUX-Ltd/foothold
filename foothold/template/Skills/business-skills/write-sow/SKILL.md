---
name: write-sow
description: |
  Turn a client conversation into an outcome-based, outside-IR35-shaped Statement of Work, with clearly defined deliverables, measurable acceptance criteria, a risk register, and a pricing recommendation. Use this skill whenever the user says any of: "write a SOW", "draft a statement of work", "turn this into a SOW", "SOW for X", "scope of work for X", "make a statement of work from this transcript / job spec / statement of requirement", "scope this engagement", or names a client and asks for a statement of work, scope, or engagement document. The input can be a meeting transcript, a job specification, a statement of requirement (SoR), or a few bullet points. The skill classifies the input, interviews the user to fill the gaps the SOW needs, drafts an outcome-based SOW that supports an outside-IR35 position, builds a risk register scored by severity and likelihood with a pricing recommendation against it (fixed-price, day-rate capped, or milestone), and produces a branded PDF in the founder's own brand plus a markdown working draft. It does not execute the contract or send anything; signature goes through the user's e-signature tool and sending through the user's email.
version: 1.0.0
audited: 2026-06-19
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
maintainer_url: https://milux.co.uk
license: MIT
last_reviewed: 2026-06-19
category: comms-crm-ops
---

# Write SOW

Turns whatever you have from a client conversation into a Statement of Work that does three jobs at once: defines the work by outcome rather than by time, is shaped to support an outside-IR35 position, and tells you where the commercial risk sits so you can price for it.

This skill is built for UK defence-sector founders trading through a limited company. The IR35 content is UK-specific. If you trade in another jurisdiction, treat the IR35 sections as not applicable and use the rest.

## Why this skill exists

Founders scope engagements from messy inputs: a call transcript, a prime's job spec, a Statement of Requirement, or three bullets in a note. The translation from that to a clean SOW is the same job every time, and three things are easy to get wrong under time pressure:

1. **Drafting by activity, not outcome.** "I'll work three days a week on the design" reads as disguised employment and prices your time, not your result. The SOW must define what good looks like and let your company decide how to deliver it.
2. **Leaving an inside-IR35 shape in the contract.** Off-payroll status turns on control, substitution, financial risk and being in business on your own account. A SOW that gives the client control over how and when the work is done, or that reads like an open-ended staffing arrangement, undermines the outside position before HMRC or the end client's status determination ever looks at it.
3. **Pricing a fixed scope without pricing its risk.** Outcome-based work moves delivery risk onto you. If the scope is ambiguous, the dependencies sit with the client, or acceptance is subjective, the price has to carry that. Most fixed-price pain is scope creep that was visible at SOW stage and never costed.

This skill makes all three deliberate steps, in order, every time.

## Hard rules

- **British English. Avoid em dashes** unless your own brand voice uses them; use commas, full stops, or semicolons. Check `Context/Brand.md` for your voice.
- **Outcome-led, not time-led.** Deliverables are defined by the result and its acceptance criteria, never by hours or days present. A day rate may appear in the pricing section as a basis of estimate; it must not define the scope.
- **The SOW supports an outside-IR35 position; it does not guarantee one.** Never tell yourself or the client the engagement "is outside IR35". Status is a question of fact about the real working relationship, and for medium and large clients (most defence primes and the MOD) the end client makes the determination under the off-payroll rules and issues a Status Determination Statement. This skill removes inside-IR35 language from the contract and flags remaining risk; it does not certify status. Carry the disclaimer in `references/ir35-outside-checklist.md` into the SOW.
- **Use your own brand.** The PDF reads brand cues (primary colour, typeface) from `Context/Brand.md`. If that page is still placeholder hint text, the PDF falls back to a neutral professional palette. Do not invent a brand.
- **Never invent commercial terms.** Price, payment schedule, dates, named client contacts, IP position, and the liability cap are yours to set. If the input does not carry them, ask. A placeholder ("To be confirmed") is acceptable only if you choose it.
- **You own the send and the signature.** This skill drafts. It does not email the SOW and it does not create the executable contract. Stop at the branded PDF and hand back. Send it from your own email; execute it through your own e-signature tool.
- **Work from the source.** If the input is a transcript, derive scope only from the transcript itself. Do not use a transcript tool's auto-generated summary or action list; those flatten everything said in a room into one list and cannot tell which client a remark belongs to. If the transcript mentions more than one client or engagement, scrub anything that belongs to a different one before it reaches this SOW.

## Inputs the skill accepts

Any one of, or a mix of:

- **Transcript** of a discovery or scoping call. Richest input; mine it for the client's stated outcome, constraints, dependencies, and success language.
- **Job specification** from a prime or client. Often written as a role, which is an inside-IR35 shape; the skill's job is to convert role-and-hours language into outcome-and-deliverable language.
- **Statement of Requirement (SoR)** from a defence customer. Usually outcome-friendly already; map requirements to deliverables and acceptance criteria.
- **Bullet-point idea** from you. Thinnest input; the interview in Step 2 carries most of the load.

## Step 1: Ingest and classify

Read everything provided. If files were uploaded or named, read them. Then state back, in three or four lines: which input type(s) you have; the client and the engagement (and the matching `CRM/organisations/` page if one exists); the core outcome the client is buying, in one sentence, in their words where you have them; and the biggest gaps the SOW needs filled. Confirm the read is right, then interview. Do not start drafting.

## Step 2: Interview to fill the gaps

Work through the checklist below with the user, batched into a few questions at a time (group related items; do not fire twenty single questions). Skip only what the input already answers cleanly.

1. **Outcome and definition of done.** What measurable change are you delivering? How will the client know it has been delivered? Who signs it off?
2. **Deliverables.** The concrete artefacts or results. Aim for the rule of thumb: roughly three core outcomes, three primary deliverables, three KPIs per workstream. More than that, split into phases.
3. **Acceptance criteria per deliverable.** Objective and checkable without debate. See `references/metrics-library.md` for patterns by service type.
4. **Out of scope.** What you are explicitly not doing. The single best defence against scope creep; be generous with it.
5. **Client dependencies.** Access, data, people, decisions, environments you need and by when. Each one is a risk if it can slip.
6. **Timeline and milestones.** Phase or milestone dates, not a weekly attendance pattern.
7. **Commercials.** Pricing model preference (the skill supports fixed-price per outcome, day-rate capped, and milestone-staged; let the input and `references/risk-register.md` guide), price or estimate, payment schedule, expenses, VAT.
8. **IR35-relevant facts.** Can you send a substitute? Who controls how and when the work is done? Are you carrying financial risk (fixing defects at your own cost, a fixed fee)? Is this one defined piece of work or open-ended? See `references/ir35-outside-checklist.md`.
9. **Contract frame.** Is there an existing MSA or framework this SOW sits under, or is it standalone? IP ownership and liability position.

## Step 3: Draft the outcome-based SOW

Build the SOW from `assets/sow-template.md`, following `references/outcome-sow-structure.md`. Write each deliverable as an outcome with its acceptance criteria attached. Convert any role-and-hours language from a job spec into deliverable-and-result language. Put everything not being done into "Out of scope". Include a change-control clause so additional work is a priced change, not a free extension.

## Step 4: IR35 outside-status pass

Run the draft against `references/ir35-outside-checklist.md`. For each factor (control, substitution, mutuality of obligation, financial risk, in business on own account, part-and-parcel, equipment) either confirm the SOW supports the outside position or flag the clause that does not, and rewrite it where the wording is the problem. Where the facts (not the wording) point inside, that is a risk for Step 5, not something to paper over. Add the IR35 disclaimer and, for higher-value engagements, the recommendation to run HMRC CEST against the real working terms and take professional review.

## Step 5: Risk register and pricing recommendation

Using `references/risk-register.md`: identify the risks across the standard taxonomy (scope ambiguity, acceptance subjectivity, client dependencies, IR35 status, timeline, technical or delivery, commercial and payment, OPSEC or classification for defence work); score each by severity x likelihood with a RAG rating; for each material risk recommend the SOW-wording mitigation and the pricing response (a contingency percentage, a wider estimate band, a milestone weighting, or a hard exclusion); and recommend the pricing model that best fits the risk profile, with the headline number or band and the contingency shown separately so you can see what the risk is costing. The risk register is your working tool; by default it is an internal annex you can strip before the SOW goes out. Ask whether it goes in the client PDF or stays separate.

## Step 6: Produce the outputs

1. **Markdown working draft** saved under the matching `Customer Engagements/` folder (`scoping/` while you are still shaping it), or `Customer Engagements/scoping/` if no engagement folder exists yet. This is the editable source of truth.
2. **Branded PDF** rendered from `assets/sow-brand.html`, using the brand cues from `Context/Brand.md` (neutral fallback if that page is unfilled). If a PDF renderer is unavailable in your environment, say so and emit the markdown only.
3. **Hand back** with a tight summary: the core outcome, the pricing recommendation with contingency, the top three risks, and any IR35 flags that need your decision. Then stop. Sending and signing are yours.

## References and assets

- `references/ir35-outside-checklist.md`: the IR35 factors, what the SOW must show for each, red-flag language, off-payroll context, CEST note, the disclaimer text, and named public sources.
- `references/outcome-sow-structure.md`: the section-by-section SOW structure, outcome-vs-activity rules, acceptance-criteria patterns, change control.
- `references/metrics-library.md`: measurable acceptance criteria and KPI patterns by service type.
- `references/risk-register.md`: risk taxonomy, severity-x-likelihood scoring, pricing-contingency mapping, and the three pricing models.
- `assets/sow-template.md`: the fillable SOW markdown template.
- `assets/sow-brand.html`: branded HTML template for the PDF.

## Boundaries

This skill is a drafting tool. It is not legal or tax advice. IR35 status and contract enforceability are ultimately questions of fact and law; take professional review for high-value or borderline engagements. Signature and sending are done with your own tools, not by this skill.
