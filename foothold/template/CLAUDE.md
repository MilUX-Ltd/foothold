# Architecture and Working Conventions

This document describes how {{pack_owner}}'s Foothold pack is organised. It carries the conventions that make the pack work, and it scales: solo founders working alone use the same shape as teams running multi-agent stacks. Where a pattern only matters once you add agents, that's called out.

## Who works in this vault

By default, just you. The pack is built for solo operation first and grows as you add agents.

If and when you bring agents into your workflow:

- **You ({{pack_owner}})** are the only person who commits to canonical knowledge. Everything else happens in support of that.
- **Research and curation agents** help you shape, define, research, and refine work before you commit it. They may write into the vault under your supervision.
- **Execution agents** do downstream work on briefs you (or your curation agents) prepare. They write to operational systems (code repositories, messaging tools, outputs queues), never directly into the vault.

You can run with zero, one, or many agents in each role. The conventions below hold either way.

## Three kinds of work

Whether one person or one team does the work, three kinds of work happen against this vault.

**Research and curation.** Reading source material, talking to people, sense-making, drafting. Output lands in the vault.

**Execution.** Producing deliverables based on a brief: a piece of content, a code change, a sent message, a deck. Output lands in operational systems and gets logged back into the vault when it's worth keeping.

**Coordination.** Tracking what's in flight, what's blocked, what's done. If you have a separate work-tracking system, that's where coordination lives. If you don't, the `Initiatives/` folder and a daily note are enough.

The conventions in this document apply to all three.

## What lives where

Foothold assumes Obsidian as the primary knowledge base. Everything else is optional and only relevant if you have or add the tool.

**Obsidian (this vault).** The primary knowledge base. Long-form notes, meeting context, contact knowledge, initiative pages, CRM-style records. This is the source of truth.

**Optional — a reference library.** Source material, PDFs, web captures, binary assets, long-term research archives that don't earn a place in the active vault. DEVONthink, Apple Notes, a Notion archive, even a simple Downloads folder. Your choice.

**Optional — a work-tracking system.** Linear, Asana, Trello, Businessmap, your choice. Lives outside the vault. Tracks cycle time, WIP, and ownership. Cross-linked to initiative pages here when relevant.

**Optional — a structured outputs queue.** Where downstream agents deposit work for your review before it gets promoted into the vault. Notion database, Airtable base, similar. Only needed once you have agents producing material.

**Optional — code and versioned artefacts.** Git-hosted code and scripts. You may have your own.

**Optional — messaging integrations.** For agents that send messages on your behalf. See `Operations/` for the runtime policy that governs how that works.

The pattern: Obsidian is the canonical record. Other systems serve specific operational roles. Knowledge stays in the vault; operation stays in its operational system.

## Write boundaries

These rules apply when you have agents working in the vault. If you're operating solo, you write everything yourself and these rules are background.

1. **Execution agents write to operational systems only.** Never directly to the vault. Enforce this at the tool layer (deploy-key restrictions, write-scoped credentials) rather than relying on instruction alone.
2. **Research and curation agents may write into the vault** as part of normal work with you, with your supervision.
3. **You may write anywhere.**
4. **Promotion from an outputs queue into the vault is always a deliberate step.** It's the gate between agent-produced output and your vetted knowledge base.

If you're solo, only rule 3 applies and everything else is on the road map for when you scale.

## Workflow patterns

These patterns scale from solo work up to a multi-agent stack. Use as much or as little of them as your setup justifies.

### Research → Decide → Capture (the solo baseline)

1. You research using the vault, the web, your reference library.
2. You decide what's worth keeping.
3. You write the decision into the vault.

The vault grows by deliberate addition. Drift comes from un-decided content sitting around. Decide and capture, or skip and move on.

### Research → Execute → Promote (the scaled version)

Once you have agents in the stack, the workflow distributes:

1. Research lands in the vault or in an outputs queue.
2. Execution happens against a written brief (see below).
3. Output gets reviewed and promoted into the vault where worth keeping.
4. Work-tracking system gets updated at each stage.

### Brief template

When you're handing work to anyone (an agent or a person who doesn't have vault access), structure the brief like this:

- **Context.** Why this work is happening and what it fits into.
- **Constraints.** Time, scope, dependencies, things to avoid.
- **Source material.** The actual content needed, copied into the brief rather than referenced out. The recipient may not be able to reach your reference library.
- **Specific ask.** The concrete output expected, including format, length, and destination.
- **Out of scope.** Things not to do, even if they seem adjacent.

Useful even when you're briefing yourself. Writing it down sharpens it.

### Promotion

When something agent-produced or externally-drafted needs to become canonical vault knowledge:

1. Write the vault note at the path the content type implies (LinkedIn post → `Marketing/Marketing Outputs/LinkedIn Posts/<Title>.md`, initiative research → the relevant initiative folder).
2. Update the source (outputs queue row, draft document) with the vault destination so the trail stays clear.
3. Log on the work-tracking system if you use one.

Reversal exists: if a promoted item needs to come back out, archive or delete the vault note, flip the source back to draft, log it. Rare but defined.

## Initiatives, projects, and customer engagements

Your work splits into two top-level folders:

- **`Initiatives/`**. Work you do for yourself. Internal services, your own products, marketing, thought leadership, operating-model change, internal tooling. See `Initiatives/Initiatives Guide.md`.
- **`Customer Engagements/`**. Work you deliver for an external organisation that owns the outcome. Each engagement maps 1:1 to an organisation page in `CRM/organisations/`. See `Customer Engagements/Customer Engagements Guide.md`.

The rule is binary: outcome ownership decides the folder. Outcome owned by your business -> Initiative. Outcome owned by an external organisation -> Customer Engagement. Paid, sponsored, or pro-bono doesn't decide it.

Both folders share the same operational pattern:

- **Obsidian.** Canonical home for each initiative or engagement. Scope, goals, acceptance criteria, meeting notes, decisions, retrospectives.
- **Work-tracking system (optional).** The cards underneath. Cycle time and WIP tracked there.
- **Outputs queue (optional).** Where derivative outputs land for review before promotion.

If you don't have a work-tracking system yet, the index page in the vault carries the workload itself: a status section, a tasks section, a decisions log. Add the tracking system when scale justifies it.

Customer Engagements add a `scoping/` subfolder alongside `active/` and `completed/` for engagements being shaped but not yet a commitment to deliver. Initiatives just use `active/` and `completed/`.

## Operations and policy

`Operations/` carries the runtime policy files your agents read at message-send time: your email signature stub, the AI autonomy kill-switch.

If you don't have message-sending agents yet, these files just sit there. When you do add them, they become load-bearing. They govern how your agents represent you to the outside world.

The AI autonomy kill-switch file (`Operations/agent-pause.md` by default) is a hard safety mechanism. Any agent sending a message on your behalf must check this file first; if it has been flipped, the agent stops and reports rather than sending. Your one-line override when you need to silence the stack quickly.

## Skill safety

A skill is instructions your agent follows, plus any files bundled with it. That makes an untrusted skill a way to run someone else's instructions or code with your agent's access to your files, your messages, and your accounts. Treat every skill you did not write as untrusted until you have checked it.

Before you import, install, fork, or first run any skill, from a marketplace, a GitHub repo, a peer, or a file someone sends you, audit it with the `skill-safety-audit` skill in this pack's `Skills/` folder. It reads every file in the skill, flags hidden instructions, data exfiltration, risky scripts, and the like, and gives you a clear PASS, PASS WITH CAUTIONS, or FAIL with a recommended action.

Act on the verdict. A FAIL is not installed: delete it, and note the source so you do not get caught by it again. A PASS WITH CAUTIONS runs only once you understand and accept the cautions. A clean PASS means nothing obvious was found, not that the skill is guaranteed safe, so keep sensible habits: give skills the least access they need, keep credentials out of reach, and re-audit a skill whenever it updates, because a clean version can be replaced by a malicious one. The responsibility for sourcing skills safely stays with you: prefer reputable, identifiable suppliers, and if in doubt, build your own with `skill-creator` rather than run an unknown one.

Each skill in this pack records its check and its origin in frontmatter: `audited` (date), `audit_verdict`, and `audited_with`, alongside `origin` (built, forked, or shared), `source`, and `maintainer`. That is how you know what has been checked, when, and who made it.

## Frontmatter conventions

Every page in the vault carries YAML frontmatter. Required fields depend on the page type; see the per-folder Guide for specifics. Common patterns:

- `type:` — the page type (contact, organisation, initiative, meeting, framework, etc.).
- `status:` — the page's current state (active, completed, archived, draft).
- `created:` — ISO date the page was first written.
- `tags:` — vault-wide taxonomy. See `Knowledge/tagging-policy.md`.

## Naming conventions

- **Folders.** Title Case for major folders (`Customer-Facing Services/`), kebab-case for initiative folders (`my-initiative/`), Title Case for canonical organisations and people.
- **Files.** Match the canonical name of the entity. Acronyms in parentheses where useful: `National Armaments Materiel (NA-M).md`.
- **Wikilinks.** Use display text for readability: `[[CRM/contacts/Jane Smith|Jane Smith]]`.
- **Wikilinks in table cells** must escape the pipe: `[[CRM/contacts/Jane Smith\|Jane Smith]]`. Obsidian otherwise treats the pipe as a column separator and the table breaks.

## Per-folder Guides

Every top-level folder ships with a `<Folder Name> Guide.md` at its root. The Guide is the contract for what belongs in the folder. Five sections:

1. **Purpose.** What this folder is for.
2. **Structure.** What each subfolder means.
3. **Frontmatter.** Required and optional fields per page type.
4. **Add discipline.** How to add new content. Points at the relevant skill if one exists.
5. **Canonical example.** A worked reference page so you can see what good looks like.

When you're not sure where something goes, read the relevant Guide.

## Adapting this pack

Foothold is opinionated. The conventions in this document and the per-folder Guides are the defaults that make the pack work. Adapt where you need to, but adapt deliberately:

- Add folders if you have a domain not covered by the defaults.
- Don't rename folders without checking what links into them. Record any deviations in `Knowledge/rules.md`.
- Don't add agents to research and curation without enforcing the write boundaries at the tool layer.

The pack works because the conventions are kept tight. Drift is the fastest way to break it.
