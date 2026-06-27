---
type: operations
category: compliance
status: draft
created: { today, ISO }
owner: { founder name }
review_due: { today + 12 months, ISO }
tags: [compliance, data-protection, dpia, gdpr]
---

# Data Protection Impact Assessment

> Skeleton for the `build-dpia` skill. Fill every `{ ... }` placeholder from the vault and the founder's answers. Delete any row or section that genuinely does not apply. Keep British English, no em dashes. This is a working DPIA, not legal advice.

This is a Data Protection Impact Assessment for { business }, following the ICO seven-part structure. It is a living document, updated whenever the processing changes.

**Controller:** { legal entity }. **Contact:** { data-protection contact, email }. **DPO:** { none appointed, below threshold / named DPO }.

## Part 1 — Identify the need for a DPIA

A DPIA is mandatory under Article 35 UK GDPR for high-risk processing, and good practice otherwise. Screening result:

| ICO high-risk indicator | Applies? | Why |
|---|---|---|
| { indicator } | { yes / no / partial } | { reason } |

Conclusion: { which triggers apply, and that the DPIA proceeds }.

## Part 2 — Describe the processing

**Nature.** { what data, collected how, used how, stored where, deleted when }.

**Scope.**

| Dimension | Detail |
|---|---|
| Categories of data | { identity and contact; financial; communications; any sensitive } |
| Special category data | { not processed / what and the Article 9 condition } |
| Criminal offence / children's data | { not processed / detail } |
| Volume and frequency | { } |
| Geographical extent | { } |
| Retention | { per data type } |

**Categories of data subject.**

| Group | Source | Primary purpose |
|---|---|---|
| { clients, prospects, suppliers, associates, participants } | { } | { } |

**Processors and sub-processors.** Every tool that holds personal data.

| Processor | Role / data | Transfer position |
|---|---|---|
| { tool } | { what it does, what data } | { UK / outside UK and the safeguard } |

**Purposes.** { the outcomes the processing serves }.

## Part 3 — Consultation

| Stakeholder | How their views are considered |
|---|---|
| { founder, co-director, processors, data subjects } | { } |

## Part 4 — Necessity and proportionality

**Lawful basis** (one per activity; see `references/lawful-basis-and-screening.md`).

| Processing activity | Lawful basis (Art 6) | Note |
|---|---|---|
| { CRM and business development } | { legitimate interests } | { } |
| { client delivery } | { contract } | { } |
| { marketing } | { consent / legitimate interests } | { PECR for electronic marketing } |
| { accounting and tax } | { legal obligation } | { } |

**Necessity and proportionality.** { could the purpose be achieved another way; data minimisation; data quality }.

**Individual rights.** { how access, rectification, erasure, restriction, objection, and portability are supported; whether any solely automated decision-making with significant effect occurs }.

## Part 5 — Identify and assess risks

Score each on likelihood (remote / possible / probable) by severity (minimal / significant / severe), giving low / medium / high.

| # | Risk to individuals | Likelihood | Severity | Overall |
|---|---|---|---|---|
| 1 | { } | { } | { } | { } |

## Part 6 — Measures to reduce risk

| # | Measure(s) | Residual |
|---|---|---|
| 1 | { control mapped to the risk } | { } |

## Part 7 — Sign off and outcomes

**Residual risk.** { overall level after measures; whether any high residual risk remains and so whether ICO consultation is needed }.

**Outstanding actions.**

| Action | Owner | Status |
|---|---|---|
| { } | { } | Open |

**Approval.**

| Field | Entry |
|---|---|
| Measures approved by | { founder } |
| Date | { } |
| Residual risk accepted by | { founder } |
| Review by | { review_due } |
