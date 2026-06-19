---
type: register
status: active
---

# Skills Value Register

The adoption decision log. For every skill you review with `skill-value-review`, this records the value decision (use as is, fork and adapt, find an alternative, or build your own), the safety verdict it was gated on, where the skill came from, the date, and the one-line reasoning.

Keep it separate from any safety record you hold. A safety check answers "is this safe to run". This register answers "was it worth taking on, and what did we decide to do about it". A skill can pass the safety audit and still be a skip here.

## How to read it

Two kinds of row, marked in the **For** column:

- **You (internal)** — an adoption decision for your own use. You were deciding whether to take the skill on.
- **External — [recipient]** — a review you delivered to someone else as advice. You did not adopt it; you assessed it for them. Recorded so you remember you reviewed it and what you said, not as something you run.

Re-review and update the row whenever a skill you adopted changes materially, or when you revisit a recommendation.

## Register

| Skill | For | Source | Safety | Decision | Date | Reasoning |
|---|---|---|---|---|---|---|
| `pm-skills` (32 forked) | You (internal) | github.com/phuryn/pm-skills via MilUX (MIT) | PASS | Use as is (generic public cut) | 2026-06-16 | Forked from MilUX's adopted set; MilUX-internal references and the F4P method removed for public release. Attribution and MIT retained, see NOTICE.md. |
| `write-sow` | You (internal) | Built by MilUX (MIT) | PASS | Use as is | 2026-06-19 | Built for the pack: outcome-based, outside-IR35-shaped SOW drafting with a risk-to-price register. IR35 content sourced to gov.uk and HMRC. Reads documents only, no network sends; signature and sending left to the founder's own tools. |

## Decisions, in brief

- **Use as is** — adopted unchanged; the job fits and nothing material needed changing.
- **Fork and adapt** — taken on with named edits; see the skill's own change history.
- **Find an alternative** — not adopted; the job was real but this was the wrong tool.
- **Build your own** — not adopted; you built or will build your own with `skill-creator`.

For external rows the recipient-facing wording is used instead (use as is / adapt before use / choose an alternative / commission a purpose-built skill), but the meaning maps one-to-one.
