---
type: guide
folder: Knowledge
---

# Knowledge Guide

## Purpose

`Knowledge/` is the policy layer of the vault. It carries the rules, conventions, and operating principles your agents read at runtime, plus the in-progress thinking that hasn't yet earned promotion to a rule.

This folder is distinct from `Resources/`. Resources is your practitioner reference library: methodologies, frameworks, books, templates that you read for ideas. Knowledge is the operating policy: rules that agents and {{pack_owner_first}} follow when working in the vault.

The discipline is binary. If an agent should behave a certain way every time, the rule lives in `Knowledge/`. If a piece of thinking might earn that status but hasn't been validated yet, it lives as a hypothesis until evidence accumulates.

## Structure

```
Knowledge/
├── Knowledge Guide.md          (this file)
├── rules.md                    (numbered rules, R-01, R-02, ...)
├── hypotheses.md               (ideas under test, not yet rules)
├── tagging-policy.md           (vault tag taxonomy)
├── domains/                    (per-domain operating notes)
│   ├── brand.md
│   ├── voice.md
│   └── ...
└── reviews/                    (weekly, monthly, quarterly review digests)
    ├── 2026-W20.md
    └── ...
```

**rules.md.** The numbered rule list. Every rule has a stable identifier (R-01, R-02, ...). Numbers are not reused. Rules carry a one-line statement and a paragraph of context. Deprecation marks the rule as no-longer-active but keeps the identifier reserved.

**hypotheses.md.** Operating ideas that might become rules but aren't there yet. Each hypothesis has a date, a statement, and an evidence trail that grows as observations accumulate. Promotion to a rule happens at review time.

**tagging-policy.md.** The vault tag taxonomy. Documents what each tag means, what it does not mean, and the conventions for applying tags across page types.

**domains/.** Per-domain operating notes. One file per domain that has standing operating concerns: brand voice, agent messaging, content workflow, security posture. These are reference for agents, updated as the domain evolves.

**reviews/.** Periodic review digests. Weekly review surfaces patterns across the last seven days; monthly looks at cross-week patterns; quarterly aligns the rule set with accumulated evidence. Each review is a durable record in the vault.

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

## Add discipline

**New rule.** Take the next R-NN number. Write the rule in `rules.md` with its identifier as header. State the rule in one line; follow with a paragraph of context explaining why. Reference the hypothesis or observation that justified promotion if one exists.

**New hypothesis.** Add to `hypotheses.md` with the next H-NN number. State the hypothesis. Note the date. Add evidence as it accumulates. Hypotheses without movement after a quarter should be archived or formally rejected.

**Tagging policy update.** Edit `tagging-policy.md`. Update `last_reviewed`. Tag changes affect the whole vault; check what's already tagged with anything you're renaming before you commit.

**New domain note.** Create `domains/<domain>.md` only when a domain has standing operating concerns that need persistent reference. One-off thinking belongs in a hypothesis until it earns its place.

**Review.** Written on cadence (weekly, monthly, quarterly). Cluster observations from the outputs queue, propose rule promotions or hypothesis archives, action the result. The digest is the durable audit record.

If you find yourself adding policy outside this folder, it probably belongs here.

## Canonical example

See `rules.md` for the canonical rule pattern. R-01 in the shipped Foothold defaults is the wikilink-in-tables escape rule (`[[Path\|Display]]` in table cells), included as the simplest worked example of the form: identifier, one-line statement, paragraph of context.
