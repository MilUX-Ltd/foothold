---
name: newsletter-writer
description: "Draft a newsletter edition following the operator's brand voice and structure. Use when the user says 'write the next newsletter', 'draft an edition on [topic]', 'newsletter on [topic]', 'help me write a newsletter', or runs /newsletter-writer. Pulls from the operator's Content Pillars and Brand pages for voice and themes."
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
license: MIT
---

# Newsletter Writer

Draft a newsletter edition. One topic per issue or a multi-topic round-up; format and length set by the user's brief.

## Quick start

Open with the quick-start line if the user is starting fresh:

> "Let's do option [single topic / multi-topic], with [tone: formal / conversational / educational], and [length: short / standard / extended]."

Remember the last option, tone, and length used; suggest them as defaults next session.

## Inputs

Before drafting, confirm:

- **Topic.** The substantive idea(s) the edition addresses.
- **Format.** Single topic, or multi-topic round-up.
- **Tone.** Formal / leadership, conversational, or educational.
- **Length.** Short (~500 words, channel-optimised), standard (full newsletter shape), or extended (long-form deep dive).
- **Channel.** Where the newsletter publishes (LinkedIn, Substack, owned mailing list, etc.).
- **Audience.** The reader you're writing for, in one sentence.

Read `Context/Brand.md` and `Capabilities and Services/Internal Services/Content Pillars.md` (if present) before drafting. The brand voice and the content pillars are the load-bearing references.

## Roles

- **Copywriter** (default). Optimises clarity, flow, and persuasive style.
- **Marketing partner** (end review). Checks for promotion opportunities, channel optimisation, and SEO / keyword improvements.

The user can switch roles by asking, e.g. "give me the marketing-partner review on this draft".

## Per-topic structure

For each topic in the edition:

1. **Theory.** The underlying concept. General unless explicitly sector-specific.
2. **Insight.** The broader practical lesson the theory points at.
3. **Application.** Tailored to the operator's sector and audience.
4. **Example.** A worked example from the operator's own experience. Ask the user for one; if not available, propose two or three options from related projects, initiatives, or case studies in the vault.

## Output structure

For every edition draft, produce:

- **Title** with at least two variants for the user to choose from.
- **Opening.** Two or three variant openings (the first paragraph that decides whether the reader keeps reading).
- **Body.** Topics in the structure above, in the chosen order.
- **Closing.** Two or three variants: each a clear call to action or reflective takeaway.
- **Visual suggestions.** One or two image or diagram suggestions if the channel supports them.
- **Channel promo post.** A short companion post (catchy, hook-forward, hashtag-ready) for promoting the edition on the user's primary social channel.
- **Executive summary.** One line for internal use.

## House style

- The user's house style is in `Context/Brand.md`. If it's populated, follow it. If not, ask the user to confirm before drafting.
- British English unless the operator's brand specifies otherwise.
- Balance thought leadership with practical value.
- Step-by-step, structured, readable. Never overwhelming.
- Avoid AI-tropes flagged in the operator's brand voice (typically: delve, leverage, robust, ecosystem, landscape, paradigm, foster, navigate, holistic, comprehensive, multifaceted, seamless).
- No rule-of-three flourishes used purely for rhythm.
- No "not X, but Y" parallelism.

## Archive

Each edition gets a one-line summary added to the running archive. The archive is used to:

- Avoid repetition.
- Suggest reuse of previous content.
- Spot underexplored areas and propose new angles.

The archive lives in `Marketing/Newsletter/<Newsletter Name> — Backlog.md` (or wherever the user keeps it; check the `Marketing/` folder for a backlog file before creating one).

## After delivery

Tell the user:

- "Draft ready. Want me to push it as a draft into Marketing/Newsletter/, or hand it back here for review?"
- Offer to: (a) save as a draft file in `Marketing/Newsletter/`, (b) regenerate the opening with a different hook, (c) add a companion social post variant, (d) summarise for the archive.
