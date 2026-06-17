# Value Rubric and Report Templates

The fixed scoring rubric for `skill-value-review`, plus the report templates for both modes. Score every skill on the same five dimensions so two reviews are comparable. Do not add ad-hoc criteria.

## Contents

- The five dimensions
- Scoring scale
- Weighting
- The four decisions
- Report template: for you
- Report template: for someone else
- Portfolio roll-up (repos)

## The five dimensions

### 1. Job-to-be-done

Is this a real, recurring job for the intended user, or a solution looking for a problem? The strongest skills do a job the user does often enough that automating it earns its keep. A clever skill for a job nobody has is worthless however well built.

- Score high: a frequent, well-defined job with a clear trigger.
- Score low: a vague or one-off job, or one already handled some other way.

### 2. Overlap

Does the skill duplicate or conflict with something the user already has? A second skill for a job already covered adds maintenance burden and trigger ambiguity. Conflicting triggers are worse than redundancy.

- Score high: fills a genuine gap, no overlap.
- Score low: duplicates an existing skill, or would fire on the same triggers as one.

In for-you mode, check against your `Skills/Skills Guide.md`. In for-someone-else mode, check against what the recipient has told you they run.

### 3. Instruction quality

Are the instructions clear, scoped, and maintainable, or vague and brittle? Look at the description (the trigger), the body (the procedure), and the bundled files. Good skills are specific about when they fire, ordered in their steps, and honest about their limits.

- Score high: tight description, ordered procedure, clear output format, sensible use of references.
- Score low: woolly trigger, hand-wavy steps, no output spec, everything crammed into one file, or contradictory instructions.

### 4. Provenance and maintenance risk

Who made it, can it be trusted to stay current, and what does it depend on? Pull the safety audit's findings in here: PASS WITH CAUTIONS items, unpinned dependencies, and supply-chain conditions all raise maintenance risk even when they are not safety-fatal.

- Score high: identifiable reputable author, active maintenance, few or pinned dependencies, clean audit.
- Score low: anonymous or unverifiable source, abandoned, heavy unpinned dependencies, or audit cautions.

### 5. Convention fit

Does the skill match the intended user's standards? In for-you mode that means your own conventions: your verbal-identity rules and banned words from `Context/Brand.md`, your tone, any agent boundaries you keep, and your vault structure. In for-someone-else mode, judge against the recipient's stated standards, or general good practice where you know none.

- Score high: already matches, or a trivial edit away.
- Score low: would need rework to fit, or embeds assumptions that clash with the user's setup.

## Scoring scale

Score each dimension Strong / Adequate / Weak, with a one-line reason. Avoid false precision; the reasoning matters more than the label.

## Weighting

Not all dimensions weigh equally.

- **The safety gate is absolute.** A FAIL ends the review before scoring. Nothing outscores safety.
- **Job-to-be-done is the heaviest value dimension.** A skill that does not do a job the user has cannot be rescued by quality. Weak here points to find-alternative or build-your-own regardless of the other scores.
- **Overlap, instruction quality, provenance, and convention fit** are roughly equal and inform which of fork, find, or build is right once the job is established as real.

## The four decisions

Map the scores to one decision.

- **Use as is** — job Strong, overlap clear, quality Adequate or better, provenance acceptable, convention fit Strong. Nothing material to change.
- **Fork and adapt** — job Strong, core quality sound, but convention fit Weak, a caution to remove, or a scope trim needed. Name the edits. This is where most decent third-party skills land.
- **Find an alternative** — job Strong but this skill is weak where it counts (quality or provenance) and forking would be more work than it saves. Say what a better one needs.
- **Build your own** — job Strong and worth owning, and the skill is unsafe, low quality, or a poor fit; or simply that owning it cleanly beats adapting someone else's. The default when the safety audit failed but the job still matters, and the safe choice whenever in doubt.

## Report template: for you

```markdown
# Skill Value Review — [skill name]

**Decision: [Use as is / Fork and adapt / Find an alternative / Build your own]**
Reviewed: [date] · For: your own use · Source: [folder / .skill / repo URL]
Safety: [PASS / PASS WITH CAUTIONS / FAIL] (skill-safety-audit, gated)

## What it does
[One or two sentences: the job and who it is for.]

## Scores
| Dimension | Score | Reason |
|---|---|---|
| Job-to-be-done | [Strong/Adequate/Weak] | [one line] |
| Overlap | [...] | [vs your catalogue] |
| Instruction quality | [...] | [one line] |
| Provenance / maintenance | [...] | [incl. audit cautions] |
| Convention fit | [...] | [vs your conventions] |

## Strengths
[What is good, briefly.]

## Weaknesses
[What is weak or risky, briefly.]

## Alternatives considered
[Other skills or approaches for the same job, and why this one wins or loses.]

## Improvements
[Concrete, specific edits that would raise the score. For a fork, these become the change list.]

## Recommendation
[The decision, the reasoning tied to the scores, and the next step offered
(skill-creator to fork or build, find-skills to search).]
```

## Report template: for someone else

The external report drops your internal framing. It advises the recipient; it does not record an adoption decision for you. When rendered as a PDF it is a branded artefact.

```markdown
# Skill Review — [skill name]
### Prepared by {{pack_org}} for [recipient]

**Recommendation: [Use as is / Adapt before use / Choose an alternative / Commission a purpose-built skill]**
Reviewed: [date] · Source: [folder / .skill / repo URL]
Safety check: [PASS / PASS WITH CAUTIONS / FAIL]

## What it does
[Plain-English summary of the job and who it suits.]

## Assessment
| Dimension | Score | Reason |
|---|---|---|
| Fit for the job | [...] | [against the recipient's need] |
| Overlap with what you have | [...] | [or "not assessed — setup unknown"] |
| Instruction quality | [...] | [one line] |
| Trustworthiness and upkeep | [...] | [provenance, dependencies, audit] |
| Fit with your standards | [...] | [or general good practice] |

## Strengths
[...]

## Weaknesses and risks
[Including any safety cautions in plain terms.]

## Alternatives
[Other options worth their attention.]

## What we would change
[Improvements, framed as advice.]

## Our recommendation
[The recommendation and the reasoning, written for the recipient.]
```

External-mode wording note: use recipient-facing decision labels (Use as is / Adapt before use / Choose an alternative / Commission a purpose-built skill) rather than the internal use/fork/find/build labels, since the recipient is not deciding what *you* do.

## Portfolio roll-up (repos)

After reviewing each skill in a repo, add a roll-up:

```markdown
## Portfolio roll-up — [repo name]
Reviewed [n] skills.

| Skill | Safety | Decision | One-line reason |
|---|---|---|---|
| [...] | [...] | [...] | [...] |

**Adopt:** [shortlist]
**Skip:** [list, with the headline reason]
**Overlaps:** [where two skills do the same job, so only one is needed]
**Worth a closer look:** [borderline cases]
```
