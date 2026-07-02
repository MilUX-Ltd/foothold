---
type: guide
created: {{install_date}}
last_reviewed: {{install_date}}
tags: [getting-started, ways-of-working]
---

# How to Use This Vault

[[Getting Started - Your First Week]] tells you what to do in week one. This page tells you how to work so the system keeps getting better after that. Four principles, all learned the hard way by people running vaults like this one. None of them is complicated; all of them compound.

## 1. Treat Claude like an intern in its first week

A bright intern on day two knows nothing about your business, and everything they produce reflects that until you brief them. Claude is the same, with one enormous difference: **it never forgets a good briefing**, because the briefing lives in this vault.

So do what you would do with the intern. Clearly articulate what you are trying to achieve, not just the task. Describe how you like to work. Explain why the customer matters, what the constraint really is, where the last attempt failed. When something comes back wrong, say what wrong looks like and why. Every explanation lands in Context pages, daily notes, engagement records and rules, and every future piece of work draws on it. Two weeks of generous explanation buys you months of an assistant that already knows.

The tell that you are under-explaining: you keep correcting the same kind of mistake. The fix is never "try again"; it is "here is what you were missing", written somewhere permanent.

## 2. If you can describe a process, you can automate it

The intern principle has a payoff beyond better answers. The moment you can describe how you do something, step by step, with what goes in and what comes out, that process can become a **skill** (run on demand, same procedure every time) or a **schedule** (runs without you asking). This pack ships with examples of both: `/meeting-prep` is a described process made repeatable; `/daily-brief` on weekday mornings is one put on a clock.

So take the time to explore what you are actually trying to achieve and how you would go about it, and explain that. Talk Claude through your bid process, your event follow-up routine, your monthly invoicing sweep. Even if you never automate it, the vault now knows it. When you do automate it, the description is the specification.

## 3. Watch for patterns worth capturing

Some automation is planned; most is noticed. The habit that finds it: when you catch yourself asking for the same shape of thing a second or third time, stop and ask whether it should be a skill or a schedule. Ask Claude directly: "we've done this three times now, should this be a skill?" The `/process-interviewer` skill exists for exactly this moment: it extracts the complete process from your head before anything gets built. And anything that arrives from outside goes through `/skill-safety-audit` first, no exceptions.

The same watchfulness works in reverse: tell Claude to flag repetition to you. An assistant that says "this is the third Tuesday running you've asked for this, want it scheduled?" is doing its job.

## 4. Review the work, and review the working

Two review habits, one small and constant, one weekly.

**Self-review before completion.** Before any piece of work is finished, ask Claude to review it against what you actually asked for and offer improvements: "before we call this done, check it against the brief and tell me what you'd improve." It routinely catches what the first pass missed, and it costs one sentence. For anything going to a customer or the public, you are the final gate; nothing external should ship without your eyes on it.

**Retrospectives.** Once a week or so, look back with Claude: what went well, what did not, and what one improvement follows. The output is never just a feeling; it is a change somewhere permanent: a new rule in `Knowledge/rules.md`, an amended skill, a schedule adjusted, a Context page corrected. An improvement that is neither made nor written down is lost, and the next retrospective finds the same problem waiting.

## Where this ends up

Follow these four habits and the trajectory is predictable. In week one the vault is a well-organised filing system. By month one it drafts in something like your voice and preps your meetings from real history. By month three it runs briefs and scans without being asked, flags its own improvement candidates, and the corrections you make are getting rarer because the misunderstandings are getting rarer. The system is never finished, and that is the point: it is fit for your purpose, and it keeps being refit as your purpose moves.

## Related

- [[Getting Started - Your First Week]] for week one, day by day.
- `CLAUDE.md` at the vault root for the working conventions the agents follow.
- The per-folder Guides for where everything lives and why.
