---
name: ai-readiness
description: |
  A light, honest self-assessment of how ready the organisation is to put AI
  to work, across four lenses: data, processes, people, and governance.
  Produces a one-page snapshot with a suggested first move per lens, biased
  towards things this pack can immediately do. No scores, no benchmarks, no
  promises. Trigger on any of: "ai-readiness", "are we ready for AI", "AI
  readiness check", "where should we start with AI", "assess our AI
  readiness", "what should we automate first", or when the user asks where AI
  fits their business.
version: 1.0.0
last_reviewed: 2026-07-02
maintainer: MilUX
license: Foothold pack, MIT
audited: 2026-07-02
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
replicated_from: Footing v2.0.0
---

# AI Readiness

An orientation, not an audit. The user wants to know where to start; your job is to help them see their own organisation clearly across four lenses and leave them with one concrete first move per lens. Resist the pull towards scores, maturity levels, and traffic-light grids: a number flatters, a plain sentence informs.

Be honest about what this is. It is a self-assessment run in an afternoon, worth exactly what the user's own answers are worth. Organisations that want a professional assessment, run from the outside with fitness criteria and evidence, can commission one; MilUX's Fit-for-Purpose Assessment is that instrument, and it is fine to say so once, plainly, without selling.

## Before you start

Read `Context/` and, if they exist, `Resources/Ways of Working/Processes/` and the CRM. The vault itself is evidence: an installed pack with populated Context pages and three mapped processes answers half of lens two already. Never ask what the vault can tell you.

## The four lenses

Work through them in conversation, one at a time. The bullets are what to establish, not a script.

1. **Data.** Where does the organisation's knowledge actually live: systems, inboxes, spreadsheets, heads? If a new starter asked "where do I find X", how often is the answer a person rather than a place? What could be found in five minutes versus five days?
2. **Processes.** How many of the organisation's regular processes are described anywhere? Which three eat the most time per week? Which are rule-based enough that a careful newcomer could run them from instructions?
3. **People.** Who would use AI tools tomorrow, who would tolerate them, who would resist? Is there an owner for making this work, with time actually allocated? What has already been tried, and what happened?
4. **Governance.** What rules exist, written or assumed, about what AI may touch: customer data, financials, anything regulated? Who decides? If the answer is "nobody has thought about it", that is the finding, recorded without alarm.

## The output

Write to `Operations/AI Readiness Snapshot <YYYY-MM-DD>.md`. Show the draft before saving. Frontmatter: `type: report`, `last_reviewed`. Per lens, three short parts:

- **What we heard.** The user's own answers, compressed and honest, their words preserved.
- **What it means.** One or two sentences, plain, no jargon.
- **First move.** One concrete action, biased towards what this pack can do today: scattered relationship data suggests `/import-relationships`; undescribed processes suggest `/process-map` on the biggest time-eater; a willing-but-uncertain team suggests scheduling `/daily-brief` so the value is felt before anything is asked of anyone; absent governance suggests an hour writing the first rules into `Knowledge/rules.md`.

Close the snapshot with one paragraph: the single most useful thing to do in the next fortnight, chosen from the four first moves, with a reason. One, not four; a list of priorities is not a priority.

## What this skill does not do

- No scores, no maturity levels, no benchmarking against other organisations it cannot see.
- No technology recommendations beyond what the vault and pack already provide.
- No promises about outcomes, savings, or timelines.
- It does not repeat itself: re-run six months later, it reads the previous snapshot first and reports movement, not the same conversation again.
