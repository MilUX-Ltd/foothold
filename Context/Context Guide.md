---
type: guide
folder: Context
---

# Context Guide

## Purpose

`Context/` is who you are in this vault. Your operator profile, your organisation, your brand, your strategy, your team, your stakeholders. The pages here are the source of truth that the rest of the vault and your agents refer back to when they need to know about you.

Context is small and stable. The seven canonical files at the root of this folder are the ones agents read most often and the ones {{pack_owner_first}} updates least often. Treat changes deliberately.

## Structure

```
Context/
├── Context Guide.md            (this file)
├── {{pack_owner}}.md           (operator profile)
├── {{pack_org}}.md             (organisation page)
├── Brand.md
├── Strategy.md
├── Team.md
└── Stakeholders.md
```

**{{pack_owner}}.md.** Your own profile. Biography, current role, history, capabilities, public-facing one-liner, contact details. Agents read this when they need to introduce you, draft something in your voice, or answer a question about your background. Sharable-by-design content only; this page may end up referenced in outbound messages.

**{{pack_org}}.md.** Your organisation. Mission, strapline, services at a one-line summary, founder team, current engagements, public links (website, LinkedIn). The canonical "what does this company do" page.

**Brand.md.** Brand positioning. What the brand stands for, who it's for, the value proposition, the strapline, any verbal-identity rules (preferred words, banned words, tone notes). Brand voice deviations or evolving conventions that agents need to internalise belong in `Knowledge/domains/brand.md` rather than here; this page is the public-facing positioning.

**Strategy.md.** Current strategic posture. Where the organisation is going, what bets it's making, the BHAG if you have one. Updated quarterly at most. Agents read this when they need to align a piece of work to current direction.

**Team.md.** Who works in the organisation, in what role. Roles and responsibilities. The page is small because the organisation is small; if it grows past a handful of people, consider splitting team biographies into `Context/team/` as a subfolder.

**Stakeholders.md.** People outside the organisation who shape its work: investors, advisors, mentors, board members. Distinct from CRM contacts because the relationship is structural rather than transactional.

## Frontmatter

Required fields per page.

**{{pack_owner}}.md:**

```yaml
---
type: operator
status: active
created: YYYY-MM-DD
linkedin: https://...
email: ...
---
```

**{{pack_org}}.md:**

```yaml
---
type: organisation
status: active
created: YYYY-MM-DD
website: https://...
founded: YYYY-MM-DD
---
```

**Brand.md, Strategy.md, Team.md, Stakeholders.md:**

```yaml
---
type: brand | strategy | team | stakeholders
status: active
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
---
```

## Add discipline

**Don't add files lightly.** Context is the operator's stable foundation. If something is operationally important but changes weekly, it probably belongs in `Operations/` or `Knowledge/`. If something is reference material you read for ideas, it belongs in `Resources/`. If something is a person you have a working relationship with, it belongs in `CRM/contacts/`.

**Editing the canonical seven.** Updates here have downstream impact: agents that read the operator profile or brand positioning will start drawing on new content immediately. Edit deliberately, commit with a clear message, and verify any messaging skills still produce sensible output afterwards.

**Adding subfolders.** Two patterns earn a subfolder.

- `Context/team/` if the team grows beyond what a single file represents well. One file per team member, each carrying the same frontmatter pattern as `{{pack_owner}}.md`.
- `Context/programmes/` if your organisation runs named internal programmes that aren't customer-facing services. These are organisational identity, not delivery.

Anything else should be challenged: does it really belong in Context, or does it have a natural home elsewhere?

**Public-versus-private discipline.** Content in `Context/` is referenced by outbound-facing skills (messages, biographies, introductions). Assume any content here may end up in front of someone outside the organisation. Confidential strategy or in-progress positioning lives in `Strategy.md` only if you would say it out loud to a stakeholder. If not, keep it in your private notes or in the outputs queue until it stabilises.

## Canonical example

See `{{pack_owner}}.md` for the canonical operator-profile shape: one-paragraph biography, current role, capabilities, history, contact details, public links. The Foothold default ships with worked content as a worked example. Replace the content with yours and the structure tells you what good looks like.
