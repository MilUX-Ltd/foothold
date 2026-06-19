# Risk register and pricing

How to find the risk in a SOW, score it, and turn it into a pricing decision. Outcome-based work moves delivery risk onto you, so the price has to carry the risk that the scope cannot remove.

## Risk taxonomy

Walk every category. For each, ask: what here could cost time or money you have not been paid for?

1. **Scope ambiguity.** Deliverables or acceptance criteria that are vague, open-ended, or interpretable two ways. The most common and most expensive risk. Every "etc.", "as required", "including but not limited to" is a flag.
2. **Acceptance subjectivity.** Sign-off resting on opinion rather than criteria; no named approver; no review window; unlimited revision rounds. Drives rework you cannot bill.
3. **Client dependencies.** Anything you need from the client to deliver: access, data, environments, decisions, people, security clearance. Each dependency that can slip is a schedule and cost risk. Defence access and clearance timelines are a classic slip.
4. **IR35 / status.** Facts (not just wording) that point inside, or an end-client SDS that may land inside. A status risk is a financial and reputational risk; it belongs here even though Step 4 handles the wording.
5. **Timeline.** Fixed end dates with little float; milestones dependent on client actions; defence approval gates and procurement cycles.
6. **Technical / delivery.** Unproven approach, integration with systems you cannot see yet, classified environments limiting your tooling, dependence on third parties.
7. **Commercial / payment.** Long payment terms, payment not tied to acceptance, no cap on expenses, currency exposure, a client with a poor payment record.
8. **OPSEC / classification (defence).** Classified material, export control, security caveats limiting how and where you can work. Both a delivery constraint and a compliance risk.

## Scoring

Score each risk on severity (impact if it happens) and likelihood, each 1 to 3, and multiply for a 1 to 9 score. RAG by score:

| Score | RAG | Meaning |
|-------|-----|---------|
| 1-2 | Green | Accept; note it, no price action needed. |
| 3-4 | Amber | Mitigate in the SOW wording and/or add modest contingency. |
| 6-9 | Red | Mitigate hard: tighten scope, add a dependency-slip clause, load contingency, change the pricing model, or decline to price until resolved. |

Severity: 1 minor rework, 2 a milestone's margin, 3 the engagement's margin or a status / reputation hit. Likelihood: 1 unlikely, 2 plausible, 3 likely on current information.

## From risk to price

Each material risk gets two responses: a wording mitigation (in the SOW) and a pricing response. They work together; wording reduces the likelihood, price covers the residual.

- **Scope ambiguity:** tighten the deliverable and acceptance criteria (wording); add a contingency percentage scaled to how much ambiguity remains (price). Rough guide: tight scope 0-5%, some ambiguity 5-15%, materially uncertain 15-30% or move off fixed price.
- **Acceptance subjectivity:** objective criteria, named approver, review window, one remedy round then change control (wording); small contingency for the residual (price).
- **Client dependencies:** list each with a date and a "dates and price assume these are met; slippage handled under change control" clause (wording); price the most likely slip into the estimate or expose it as a stated assumption (price).
- **IR35 status:** strip inside language, confirm substitution and financial-risk clauses (wording); if facts still point borderline, run CEST and take professional review, and consider pricing the status risk or declining day-rate-only terms (price).
- **Timeline:** milestone the work so a slip in one phase does not cascade (wording); add schedule contingency or stage the price (price).
- **Technical / delivery:** a discovery or spike phase priced separately before committing to a fixed build price (wording and price); or a cap rather than a fixed price.
- **Commercial / payment:** payment tied to acceptance, milestone invoicing, expenses capped, VAT explicit (wording); for a weak payer, stage payments and front-load (price).
- **OPSEC / classification:** state the security constraints and who provides the secure environment (wording); price the inefficiency of working in a constrained environment (price).

## Choosing the pricing model

The risk profile points to the model:

- **Fixed-price per outcome.** Use when scope is tight and acceptance is objective, and when the outside-IR35 position matters most (a fixed fee plus defect-remedy-at-own-cost is the strongest financial-risk signal). You keep the upside on efficiency and carry the overrun risk, so the scope and contingency must be right. Default for clean, well-understood engagements.
- **Day-rate, capped.** Use when scope is genuinely uncertain and a fixed price would be guesswork. Cap it so the client has cost certainty and you are not open-ended. Weaker on IR35 than fixed-price, so pair it with deliverable acceptance and a defined end, never pure time-billing.
- **Milestone / staged.** Use for longer engagements, where trust is being built, or where a weak payer or a long approval cycle makes cash flow a risk. Payment tied to milestone acceptance shifts risk back toward the client and protects your exposure. Combines well with a discovery phase priced before the build.

## Presenting the register

Deliver a short table: risk, category, severity x likelihood, RAG, SOW mitigation, pricing response. Then a one-line pricing recommendation: model, headline number or band, and contingency shown separately so you can see what the risk is costing and decide whether to absorb it, expose it, or push it back to the client. Decide whether the register goes in the client PDF or stays an internal annex (internal by default).
