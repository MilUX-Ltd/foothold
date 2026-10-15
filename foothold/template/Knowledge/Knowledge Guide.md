---
type: guide
folder: Knowledge
---

# Knowledge Guide

## Purpose

`Knowledge/` is the policy layer of the vault. It carries the rules, conventions, and operating principles your agents read at runtime, plus, if you choose to keep them, the in-progress thinking that hasn't yet earned promotion to a rule.

This folder is distinct from `Resources/`. Resources is your practitioner reference library: methodologies, frameworks, books, templates that you read for ideas. Knowledge is the operating policy: rules that agents and {{pack_owner_first}} follow when working in the vault.

The discipline is binary. If an agent should behave a certain way every time, the rule lives in `Knowledge/`. If a piece of thinking might earn that status but hasn't been validated yet, you can keep it as a hypothesis until evidence accumulates.

## Structure

Two files ship with the pack. The rest are optional: create them when you need them, not before.

```
Knowledge/
├── Knowledge Guide.md          (this file)
├── rules.md                    (numbered rules, R-01, R-02, ...)
├── tagging-policy.md           (vault tag taxonomy)
├── hypotheses.md               (optional: ideas under test, not yet rules)
├── domains/                    (optional: per-domain operating notes)
│   ├── brand.md
│   ├── voice.md
│   └── ...
└── reviews/                    (optional: review digests)
    ├── 2026-W20.md
    └── ...
```

**rules.md.** The numbered rule list. Every rule has a stable identifier (R-01, R-02, ...). Numbers are not reused. Rules carry a one-line statement and a paragraph of context. Deprecation marks the rule as no-longer-active but keeps the identifier reserved.

**tagging-policy.md.** The vault tag taxonomy. Documents what each tag means, what it does not mean, and the conventions for applying tags across page types.

**hypotheses.md (optional).** Operating ideas that might become rules but aren't there yet. Each hypothesis has a date, a statement, and an evidence trail that grows as observations accumulate. Promotion to a rule happens at review time. Create the file when you have your first hypothesis worth tracking.

**domains/ (optional).** Per-domain operating notes. One file per domain that has standing operating concerns: brand voice, agent messaging, content workflow, security posture. These are reference for agents, updated as the domain evolves. Create the folder when your first domain earns a page. Setup writes `domains/brand.md` from your brand answers when you give it enough to go on.

**reviews/ (optional).** Periodic review digests. Weekly review surfaces patterns across the last seven days; monthly looks at cross-week patterns; quarterly aligns the rule set with accumulated evidence. Each review is a durable record in the vault. Create the folder when you start writing reviews that feed your rules; work reviews can live in `Daily/Reviews/` instead (see the [[Daily/Daily Guide|Daily Guide]]).

## Writing a rule

**New rule.** Take the next R-NN number. Write the rule in `rules.md` with its identifier as header. State the rule in one line; follow with a paragraph of context explaining why. Reference the hypothesis or observation that justified promotion if one exists.

**Tagging policy update.** Edit `tagging-policy.md`. Update `last_reviewed`. Tag changes affect the whole vault; check what's already tagged with anything you're renaming before you commit.

**New hypothesis (if you keep a hypotheses file).** Add to `hypotheses.md` with the next H-NN number. State the hypothesis. Note the date. Add evidence as it accumulates. Hypotheses without movement after a quarter should be archived or formally rejected.

**New domain note (if you keep a domains folder).** Create `domains/<domain>.md` only when a domain has standing operating concerns that need persistent reference. One-off thinking belongs in a hypothesis until it earns its place.

**Review (if you keep a reviews folder).** Written on cadence (weekly, monthly, quarterly), starting from the [[Templates/Weekly Review|Weekly Review template]]. Cluster observations from the outputs queue, propose rule promotions or hypothesis archives, action the result. The digest is the durable audit record.

If you find yourself adding policy outside this folder, it probably belongs here.

## Lifecycle

Statuses are optional for most of what lives here.

- **Rules.** A rule is active until you deprecate it. Mark it deprecated in place and keep its identifier reserved; never delete it or reuse the number.
- **Hypotheses.** Each one is tracked until it is promoted to a rule, or archived or formally rejected. Anything without movement after a quarter should be one or the other.
- **Policy and domain pages** carry `status: active` and move to `archived` when retired.
- **Reviews** are records of their period and carry no status.

## Frontmatter

Required fields per file type.

**rules.md:** No file-level frontmatter; each rule is a section with its identifier as header (e.g. `## R-01 — Rule name`).

**hypotheses.md:** Same pattern; each hypothesis is a section with a tracking identifier (`## H-01 — Hypothesis statement`).

**tagging-policy.md:**

```yaml
---
type: policy
status: active
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
---
```

**domains/<name>.md:**

```yaml
---
type: domain
status: active
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
review_cycle: monthly
---
```

**reviews/<period>.md:**

```yaml
---
type: review
review_cycle: weekly | monthly | quarterly
period: YYYY-Www | YYYY-MM | YYYY-Qn
created: YYYY-MM-DD
---
```

The frontmatter convention that applies across the vault is rule R-07 in `rules.md`.

## Canonical example

See `rules.md` for the canonical rule pattern. R-01 in the shipped Foothold defaults is the wikilink-in-tables escape rule (`[[Path\|Display]]` in table cells), included as the simplest worked example of the form: identifier, one-line statement, paragraph of context. For a review, start from the [[Templates/Weekly Review|Weekly Review template]].

## Related

- [[Daily/Daily Guide|Daily Guide]]: where work reviews can live
- [[Templates/Templates Guide|Templates Guide]]: the Weekly Review template
- [[Resources/Resources Guide|Resources Guide]]: the reference library, distinct from policy
