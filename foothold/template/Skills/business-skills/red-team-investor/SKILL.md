---
name: red-team-investor
description: |
  Critique any investor-facing content from the point of view of a sceptical, experienced investor, so you see the weaknesses before a real investor does. Works on any form: a pitch deck, a one-pager, an executive summary, a full business plan, a financial model, a cold email or intro, an investment memo, a teaser, or a data room. Use this skill whenever you say any of: "red team this", "red-team investor", "review this deck", "review this pitch", "what would an investor make of this", "poke holes in this", "where are the gaps", "review the pitch deck", "review this business plan", "review this model", "is this fundable", "what would a VC say", "due diligence this", "tear this apart", or hand over founder or investor material and ask for a critical read. It does NOT write or improve the pitch (that is a separate drafting job); it reviews. The output is a structured, honest critique calibrated to your stage and the content type, mapping each weakness to the underlying risk and listing the hard questions a sharp investor would ask. Default output is in the conversation; saving it into your vault happens only when you ask, and nothing is ever sent to an investor on your behalf.
audited: 2026-06-25
audit_verdict: pass
audited_with: skill-safety-audit
origin: built
maintainer: MilUX
license: MIT
---

# Red-Team Investor

Read a piece of investor-facing content the way a sharp, sceptical investor reads it: find the weakest link, name the risk it maps to, and surface the questions you are least ready for. The job is to make your own read better than the room you are about to walk into, whether you are the founder, an adviser inside the company, or assessing a deal you might back.

## The one idea under everything

An investor is not buying a business. They are pricing risk and underwriting a return. Every lens below is really a question about which risk dominates and whether it has been retired or merely hidden. Three master risks recur across the investor canon:

- **Market risk** — is there a large, growing market that actually wants this.
- **Product or technical risk** — can this team build something compelling and defensible.
- **Execution or team risk** — can they acquire and keep customers profitably at scale.

A good review can always name which of the three a given weakness belongs to. If you cannot map a criticism to a risk, it is probably style, not substance.

## Step 1: Establish context before you judge

Do not review in a vacuum. Settle these first, from the material or by asking:

1. **Content type.** Deck, one-pager, exec summary, full business plan, financial model, cold email or intro, investment memo, teaser, data room. This sets what is fair to expect and what is reasonable to be absent (Step 2 table).
2. **Stage.** Pre-seed, seed, Series A or later. This sets the bar. Demanding Series A metrics of a pre-seed deck is as much an error as excusing a Series A deck with no cohort data.
3. **Sector.** Deep tech or hardware, regulated (defence, gov, health, fintech), marketplace, SaaS, consumer, services. This changes which risk dominates (Step 5).
4. **Audience and purpose.** Who is it going to (angels, a specific VC, a grant body), and what is the content trying to do (get a meeting, close a round, brief a partner).
5. **Your relationship to it.** Are you the founder, an adviser named inside the company, or an outside assessor. If you are inside the tent, say so in the output: it is an inside read, not a cold investor read, and the cold view is the one worth having. Flag any conflict of interest plainly.
6. **Depth wanted.** A fast gut-check or a full diligence-grade teardown. Default to a full structured review unless a quick read is asked for.

## Step 2: Calibrate the bar to stage and content type

Hold the content to the right standard. Two calibrations run through the whole review.

**By stage (what investors actually underwrite):**

- **Pre-seed** underwrites the founder. Vision, grit, founder-market fit, technical depth. Revenue, GTM, even the finished product can be unproven. A prototype plus a sharp, earned insight is often enough. Metrics are rarely expected.
- **Seed** underwrites an early product-market-fit signal. Expect real users, early retention, a validated GTM hypothesis, directional unit economics, and some evidence: design partners, LOIs, a waitlist, first customers. Full repeatability and scale are not yet required.
- **Series A and later** underwrites a proven, scalable model. Metrics, not potential. Expect cohort retention, real unit economics, and a trajectory. Little is allowed to be hand-waved.

**By content type (what is fair to expect, what is reasonable to be absent):**

| Content type | Prioritise / expect | Reasonable to be absent |
|---|---|---|
| Pitch deck | Story arc, one point per slide, the insight, traction proof, a clean ask | Granular financials, full cohort tables, legal detail |
| One-pager / teaser | The hook, problem, wedge, one or two proof points, the ask | Almost all detail; judge whether it earns a second look |
| Executive summary | The above plus a crisp team and market line | Models, appendices |
| Full business plan | Internal consistency end to end, defensible assumptions, GTM detail, a real risk section | Little; completeness is fair to demand here |
| Financial model | Bottom-up build, driver logic, reconciled unit economics, loaded cost base, base / upside / downside, burn and runway | Narrative polish |
| Cold email / intro | One-line why-it-matters, a traction hook, a specific ask, relevance to that investor, brevity | Everything else; over-stuffing is itself a flag |
| Investment memo | Risk framing, bull and bear case, what has to be true, terms and valuation justification, the key falsifiable assumption | Nothing; a memo is the analysis, so flag if it has no bear case |
| Data room | Completeness and consistency: cap table, financials reconciling to the model, customer and cohort data, contracts, IP, compliance | Polish; judge for gaps and inconsistencies |

The cross-cutting rule: **calibrate severity by stage and content type.** A missing downside case is fatal in a financial model and irrelevant in a cold email. Absent cohort data is fine at pre-seed and disqualifying at Series A.

## Step 3: Work the lenses

Go through the lenses that apply to the content. For each, decide whether the material is strong, thin, or a red flag, and note which master risk it maps to. Do not force every lens onto a one-pager; do hold a full plan to all of them.

**Team and founders** (highest weight early). Strong: demonstrable founder-market fit, an insight earned through direct experience, a complete team or a credible named-hire plan to fill the gap, evidence they can attract talent, clear and honest thinking. Weak: a solo founder with an unaddressed capability gap, a polished deck with no domain background, no answer to "why you, why now", exaggeration (investors discount for spin).

**Problem.** Strong: a specific, acute, frequently felt pain with a named customer, and a clear account of how it is solved today and why that falls short. Weak: a vitamin not a painkiller, an abstract or assumed problem, solution-first pitches that never establish the pain.

**Market.** How it is sized matters more than the headline number. Strong: bottom-up sizing from real segments, price and realistic penetration, named and sourced figures, a genuine "why now" (a recent shift in technology, regulation, behaviour or cost). Weak: top-down "we only need 1% of a huge market", unsourced numbers, TAM, SAM and SOM that are indistinguishable. Rule of thumb: a market number with no named source should be treated as fabricated.

**Product and differentiation.** Strong: a one-sentence value proposition, a working product or demo, differentiation that is structural not cosmetic. Weak: feature lists as a mission, differentiation any competitor could copy in a sprint, a roadmap that passes planned features off as current capability.

**Traction and evidence** (stage-dependent). Strong: real usage and revenue with growth rate and retention attached, cohort retention curves that flatten, consistent month-on-month growth. Weak: **vanity metrics** (cumulative sign-ups, downloads, registered users, press, raw pipeline), top-line growth shown to hide flat retention, no cohort data.

**Business model and unit economics.** Strong: economics shown from real cohort data, internally consistent, with margin, CAC, LTV and payback reconciling, plus a sensitivity view. Weak: LTV on optimistic lifetimes and gross rather than contribution margin, CAC that excludes blended sales and marketing cost, figures that contradict between deck and model. Benchmarks to test against (SaaS, as of 2024 to 2026, treat as bands not thresholds): LTV:CAC 3:1 healthy floor; CAC payback under 12 months strong, 12 to 18 typical, over 24 a hard question in normal markets and segment-dependent; software gross margin 70 to 85%; net revenue retention above 100% is the line, 110%+ competitive, below 100% is a leaking bucket; burn multiple around 1.6x at Series A; Rule of 40 for later stages.

**Go-to-market.** Strong: a single proven wedge, one channel with real CAC evidence and a scaling signal. Weak: a list of every conceivable channel, which usually means none is proven, and naivety about enterprise or regulated sales cycles.

**Competition and moat.** Strong: honest naming of direct and indirect competitors and the status quo (doing nothing is a competitor), a credible plan to win, and a moat mechanism (network effects, switching costs, proprietary data, IP, brand, cost advantage), ideally stacked. At seed, judge the architecture for a future moat, not proven durability. Weak: "we have no competitors" (read as no research or no market), a first-mover claim dressed as a moat, a 2x2 that conveniently leaves the company alone top-right.

**Financials and projections.** Strong: a bottom-up build with explicit drivers, a base, upside and downside case, a fully loaded cost base, and a source for every assumption. Weak, the five that recur: a hockey stick with no mechanism for the inflection, assumptions that do not survive scrutiny, missing or muddled unit economics or numbers that do not reconcile across tabs, ignoring burn and runway, and bull-case-only with no scenario planning.

**The ask and use of funds.** Strong: a specific amount tied to specific milestones that de-risk the next round, with 18 to 24 months of runway after the raise. Weak: a round sized to "give us 18 months" with no milestone logic, a tidy equal-thirds split, padded founder comp, or a raise too small to reach any milestone.

**Valuation and terms** (where the content includes them). Strong: a valuation justified by comparables and metrics, post-money clearly stated, a sensible option pool. Founder-side red flags to surface in a memo or term-sheet read: liquidation preference above 1x or participating preferred, full-ratchet anti-dilution, an option pool created pre-money, and pre or post-money ambiguity. UK note: SEIS/EIS investors cannot take more than 30%, and scheme eligibility is often a gating diligence item.

**Risk.** Strong: risks named honestly with mitigations and a downside case owned by the team. Weak: no risk section, or risks that are all external and none owned.

## Step 4: Red-flag sweep

Call these out explicitly wherever they appear. Each maps to a risk; say which.

- No bottom-up market sizing; unsourced or indistinguishable TAM, SAM, SOM.
- Vanity metrics; growth shown to mask flat retention; no cohorts.
- Single founder with an unaddressed capability gap, or no founder-market fit.
- Unrealistic projections; hockey stick with no mechanism; bull-case-only.
- "No competitors."
- Thin moat; first-mover dressed as defensibility.
- Unclear use of funds; no milestone link; runway too short to reach a de-risking event.
- Inconsistent numbers across deck and model (a near-fatal credibility hit).
- Regulatory or route-to-market naivety.
- Missing financials or no real cost base.
- Term red flags (above 1x or participating preference, full ratchet, pre-money pool, pre/post ambiguity).
- Founder behaviour flags: exaggeration, evasiveness on hard questions, no downside thinking.

## Step 5: Sector lens

Add the nuance that matters for the sector.

- **Deep tech or hardware.** Risk is often binary and technical, not just commercial. Use **Technology Readiness Levels (TRL 1 to 9)** as the spine: what TRL now, what TRL after this round. Many deep-tech investors will not look at Series A below TRL 6. Watch capital intensity, long timelines against fund life, and the TRL 4 to 7 valley of death. The sharp question: how do you reach a working prototype without burning a fortune.
- **Regulated markets (defence, gov, health, fintech).** Weight regulatory and route-to-market risk heavily. Approval pathways, certification timelines, partner-bank or procurement dependencies, accreditation, and reference-customer dependency dominate. For defence and gov: long procurement cycles and political exposure. Naivety here reads as existential.
- **Marketplaces.** Liquidity, GMV, take rate, and above all GMV retention by cohort. Watch GMV bought with subsidy and a take rate too thin to be a business.
- **SaaS.** The benchmark-heavy world above. Watch services revenue dressed as SaaS and "ARR" that includes non-recurring contracts.
- **Consumer.** Engagement and retention over revenue early (DAU/MAU, D1/D7/D30, organic versus paid mix). Watch paid-acquisition-dependent growth with no organic pull.

## Step 6: The hard questions

End the analysis by listing the diligence questions this specific content is least ready for. Draw on the bank below and tailor them to what you found:

- Show me retention by cohort. Do the curves flatten, or does everyone churn out.
- Can we talk to your customers without you on the call.
- Where does every assumption in this model come from.
- What happens to profitability if CAC rises 15% or churn improves 10%.
- How is CAC actually calculated, and is LTV on gross or contribution margin.
- Why now, and why hasn't someone already done this.
- Which single channel works, and what is its CAC and payback.
- What is the one thing that has to be true for this to be a fund-returner, and what would falsify it.
- What did you learn that made you change the plan.

## Step 7: Output

Default to the conversation, in plain, direct, honest prose, no padding. Structure:

1. **Snapshot.** One or two lines: what it is, stage, the raise or ask if stated, and the single sentence a sceptical investor would form.
2. **Investability lean.** An honest read of whether, and for whom, this is fundable as it stands. Not a fake score; a judgement with a reason.
3. **Strengths.** What genuinely works. Be fair; a red team that only attacks is not useful.
4. **Red flags, by severity, each mapped to a risk.** Lead with what would stop a cheque. Calibrate severity to stage and content type per Step 2.
5. **Lens notes.** The applicable lenses from Step 3, kept tight, only where there is something to say.
6. **The hard questions** the content is least ready for.
7. **Polish.** Typos, inconsistent numbers, and clarity problems that cost credibility, especially anything that contradicts across the document.
8. **Recommended fixes**, only if asked, kept separate from the critique so the review stays a review.

If a scoring frame is named (Scorecard, Berkus, Risk Factor Summation, TRL), structure around it and say so. Otherwise score the lenses qualitatively, name the dominant risk, and calibrate to stage and content type rather than producing a hollow single number.

## Boundaries

- This skill reviews; it does not rewrite the pitch or speak to an investor. Improvements are a separate, opt-in step, and nothing here is ever sent to an investor or any third party.
- Saving the review into your vault happens only when you ask; the default is the conversation.
- Never fabricate a benchmark or a fact to land a point. If a market or metric claim is unsourced, the finding is "unsourced", not a counter-number invented to rebut it.
- Benchmarks age. The numeric bands here are as of 2024 to 2026; the qualitative framing (the risk triad, the red-flag patterns, the questions) is durable. State the band as a band, and re-check the numbers if a review turns on a threshold.
- Where you are named in or attached to the company, say so in the output. An inside read is not a cold investor read, and the cold view is the one worth having.

## Provenance

Built from research into how investors evaluate companies and what trips founders up in diligence, drawing on public investor and accelerator writing: Sequoia Capital, Paul Graham and Y Combinator, Andreessen Horowitz (a16z), Charles River Ventures (CRV), the UK Business Angels Association and the British Business Bank, SeedLegals, and published SaaS-benchmark sources. The a16z market / product / execution risk triad is the organising idea. The numeric benchmarks reflect 2024 to 2026 data and should be treated as bands, not fixed thresholds.
