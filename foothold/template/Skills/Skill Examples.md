---
type: reference
status: active
created: 2026-05-20
last_reviewed: 2026-05-20
---

# Real-life examples of skills you can create

Foothold ships with a starter set of skills. As your vault grows, you'll find yourself doing things repeatedly that could be automated. Each of those is a skill candidate.

This page is a catalogue of skills the Foothold authors and users have built and found useful. None of them ship by default; they're listed here to give you ideas for skills you might write for your own vault. Some you'll want to keep generic; others will be deeply specific to how you work.

## Operator system skills

- **/prompt-master** — Generates a production-ready prompt for a specific AI tool (Claude, Cursor, GPT-5, reasoning models, computer-use agents, research orchestrators). Routes per-tool, applies the right structural conventions, removes fabrication-prone patterns. Ships with Foothold.
- **/process-interviewer** — Relentless one-question-at-a-time interviewer that extracts a complete, unambiguous plan before any work starts. Useful for scoping initiatives, designing new skills, stress-testing your own thinking. Ships with Foothold.
- **/update-claude-context** — Refreshes the working-memory context that Claude sees about your vault. Useful when your strategy or brand has moved on and you want the agent to catch up without you re-explaining.
- **/triage-downloads** — Walks your Downloads folder, classifies each file, suggests filing into the right place in your reference library or vault.

## Content production skills

- **/newsletter-writer** — Drafts newsletter editions following your brand voice and structure. Pulls from `Context/Brand.md` and `Capabilities and Services/Internal Services/Content Pillars.md`. Ships with Foothold.
- **/linkedin-writer** — Drafts LinkedIn posts in your voice. Reads from your published archive in `Marketing/Marketing Outputs/LinkedIn Posts/` to stay consistent. Useful patterns: hook generator, comment-bait variant, before-and-after pattern.
- **/linkedin-sweep** — Scans your LinkedIn engagement (notifications, DMs, comments on posts) and surfaces actions: replies owed, follow-ups due, connection requests to consider.
- **/thank-new-connections** — Drafts thank-you messages for people who recently accepted your LinkedIn connection request. Personalised from their public profile.

## Meeting and event skills

- **/meeting-prep** — Produces a briefing for an upcoming meeting. Pulls vault context (contact, organisation, history) plus external sources if connected (CRM, email, chat). Ships with Foothold.
- **/narration-prep** — For events where you're speaking or chairing. Drafts your talking notes from the event brief and the audience profile.
- **/comms-catch-up** — End-of-day sweep across your inbound channels (email, chat, LinkedIn). Surfaces what changed, what's overdue, what's worth attending to.

## Knowledge and reading skills

- **/book-recommend** — Recommends a book from your reading list based on a topic or problem you're chewing on. Reads `Resources/Books/Library.md` and your existing book notes.
- **/business-novel** — Pulls a relevant passage or concept from one of the business novels in your library (e.g. *The Goal*, *The Phoenix Project*) when it would illuminate a current problem.
- **/goldratt-story** — Tells a Theory-of-Constraints story for the situation you're describing, in the style of Goldratt's novels.

## CRM and event skills

- **/add-contact** — Captures a new contact into the CRM. Public info only, confirms before writing. Ships with Foothold.
- **/add-organisation** — Captures a new organisation. Handles rebrands (`former_name:` frontmatter) and parent-child folder pattern. Ships with Foothold.
- **/add-event** — Logs an event into `Intelligence/events/`. Includes Chatham House check at intake. Ships with Foothold.

## Commercial skills

- **/write-sow** — Turns a transcript, job spec, statement of requirement, or bullet-point idea into an outcome-based Statement of Work. Shapes the contract to support an outside-IR35 position and flags residual status risk, builds a risk register scored by severity and likelihood with a pricing response per risk, and recommends a pricing model (fixed-price, day-rate capped, or milestone). Produces a branded PDF in your own brand plus a markdown draft. UK-focused; not legal or tax advice. Ships with Foothold.
- **/mobilise-engagement** — Bootstraps a Customer Engagement during scoping. Scaffolds the folder under `Customer Engagements/scoping/`, drops in the index page with Outcome, Information Architecture, Scope and Deliverables, Definition of Done, Change Control, Capacity, Engagement Health, plus a CRM-seeded stakeholder map, comms plan with reporting cadence, single combined RAID log, outcome one-pager with benefits measurement, and a mobilisation checklist running through to "contract signed". Promotion from scoping to active is a manual call, not an automatic checklist consequence. Ships with Foothold.
- **/late-payment-reminder** — Drafts a UK-statutory late-payment chase email at three escalation levels (polite reminder, firm reminder, final notice). Calculates daily interest against the live Bank of England base rate. Ships with Foothold.
- **/book-train-ticket** — Books a National Rail ticket via a computer-use agent. The pattern: agent reads your calendar for the upcoming meeting, suggests trains, asks for confirmation before purchase.

## Security and compliance skills

- **/cyber-essentials-ready**. Walks a non-IT user through configuring their personal Mac or Windows computer to meet the UK Cyber Essentials technical controls (Montpellier question set). Initial setup, monthly verify mode, append-only audit log, dated evidence packs, and a reviewer-facing README written to `Operations/Cyber-Essentials/`. Registers a monthly Cowork scheduled task to keep the posture current. Ships with Foothold.

## Setup and tooling skills

- **/artifact-planner** — Walks a sketched artefact (a deck, a diagram, a document) into a step-by-step plan before you ask an agent to produce it.
- **/gridfinity-builder** — Generates Gridfinity bin specifications for 3D printing, given a description of what you want to organise. (Niche, but a good example of a hobbyist skill that lives alongside the working skills.)

## How to use this list

This is inspiration, not instruction. Each skill above solves a specific recurring problem in a specific operator's vault. When you write your own:

1. Notice the third time you're doing the same thing.
2. Write the skill before the fourth time.
3. Keep it focused. One job per skill. Skills with too many jobs are hard for the agent to match against your trigger phrases.
4. Use `/process-interviewer` to scope a new skill before writing it. The interview surfaces gaps you wouldn't see otherwise.

See `Skills/Skills Guide.md` for the canonical skill-authoring shape (SKILL.md frontmatter, structure, conventions).
