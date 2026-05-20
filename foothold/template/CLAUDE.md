# Architecture and Working Conventions

This document describes how {{pack_owner}}'s Foothold pack is organised and the rules for how agents operate within it. Any agent working on {{pack_owner_first}}'s behalf should read this before acting.

## The Agents

This pack assumes a multi-agent stack with clearly separated roles. The Foothold default runs this stack inside Anthropic's Cowork; you can adapt it to other AI tools without changing the structural conventions below.

- **{{pack_owner}}** — human, the only person who commits to canonical knowledge.
- **Upstream agents** — research and curation. Work with {{pack_owner_first}} to shape, define, research, and refine work before it is committed. May write directly to the vault as part of normal work.
- **Downstream agents** — execution. Operate on self-contained briefs prepared upstream. Write only to operational systems (the outputs queue, code repositories, messaging), never to the vault.

The number of agents in each tier is your choice. The pattern is what matters: research and curation upstream, execution downstream, explicit handoffs between.

## Three-Tier Architecture

**Upstream tier — research, curation, vault writes.**
{{pack_owner}} and upstream agents. Read everything. Write to the vault.

**Execution tier — downstream work on curated briefs.**
Downstream agents. Operate on self-contained briefs. Write to operational systems only.

**Coordination tier — work tracking and audit.**
A coordination system (Businessmap, Linear, Asana, Trello, your choice) sits above the other tiers as the work-tracking and audit layer. Every agent posts a progress comment on the relevant card after completing a unit of work, referencing the resulting artefact.

## Tool Roles

The pack assumes the following classes of tool. The specific product in each slot is your call; the role each plays in the system is the structural commitment.

**Obsidian (this vault).** The primary knowledge base. Holds long-form notes, meeting context, contact knowledge, initiative and project pages, CRM-style records. Synced across your machines via your chosen method.

**Reference library.** A separate system for source material, PDFs, web captures, binary assets, long-term research archives. Anything that doesn't earn a place in the active vault. DEVONthink, Apple Notes, Notion, or similar. Accessed by upstream agents only.

**Structured outputs queue.** The staging area between agents and the vault. Downstream agents deposit here; upstream agents curate from here into the vault. Notion database, Linear project, Airtable base, or similar.

**Coordination layer.** Work tracking and audit. Businessmap, Linear, Asana, or similar.

**Code and versioned artefacts.** Git-hosted code and scripts. GitHub, GitLab, or similar.

**Messaging integration.** For agents that send messages on your behalf. Unipile, native API integrations, or similar. See `Operations/` for the runtime policy that governs how agents represent you in messages.

## Write Boundaries — The Core Rule

1. **Downstream agents write to operational systems only.** Never to the vault. Enforce this at the tool level (deploy-key restrictions, etc.) rather than relying on instruction alone.
2. **Upstream agents may write directly to the vault** as part of normal work with {{pack_owner_first}}.
3. **{{pack_owner}} may write anywhere.**
4. **Promotion from the outputs queue into the vault is a deliberate curation step** performed by {{pack_owner}} or an upstream agent. This step is the gate between agent-produced output and canonical knowledge.

## Workflow Patterns

### Research → Execute → Promote

1. Upstream does the research using the reference library, the vault, and the web.
2. Research lands in the outputs queue as a structured brief.
3. Downstream picks up the brief and executes the work.
4. {{pack_owner_first}} or an upstream agent reviews and promotes the result into the vault where appropriate.
5. The coordination card is updated with progress comments at each stage.

### Research Brief Template

Use this structure when preparing a brief for a downstream agent. Downstream agents typically cannot reach the reference library or private vault paths, so the brief must be self-contained.

- **Context.** Why this work is happening and what it fits into.
- **Constraints.** Time, scope, dependencies, things to avoid.
- **Source material.** The actual content needed, copied into the brief rather than referenced out.
- **Specific ask.** The concrete output expected, including format, length, and destination.
- **Out of scope.** Things not to do, even if they seem adjacent.

### Coordination Card Convention

After completing a work unit:

- Post a progress comment on the relevant card linking to the produced artefact (vault path, code repository commit, outputs queue row).
- Move the card forward if the workflow step has advanced.
- When handing off downstream, the comment should include the brief's location so the next agent can find it.

## Initiatives and Projects

Initiatives are knowledge artefacts with an operational layer. They live in Obsidian under `Initiatives/active/` and `Initiatives/completed/`. See `Initiatives/Initiatives Guide.md` for the folder layout and index-page template.

- **Obsidian.** Canonical home for each initiative. Scope, goals, acceptance criteria, meeting notes, decisions, retrospectives, and wiki-links into contacts, intelligence, and resources.
- **Coordination layer.** The cards underneath. Cycle time and WIP are tracked here, not in the vault.
- **Outputs queue.** Used as an interface layer when an initiative needs to share derivative output with collaborators who don't have vault access.

The Obsidian page and the coordination cards are cross-linked by URL in both directions.

## Operations and Policy

`Operations/` carries the policy and runtime assets agents read at message-send time: your email signature stub, your kill-switch file, runtime guards.

These files are load-bearing. They govern how your agents represent you to the outside world. Treat changes to them with the same care you'd apply to a public-facing biography.

The AI autonomy kill-switch file (`Operations/agent-pause.md` by default) is a hard safety mechanism. Any agent sending a message on your behalf must check this file first; if it has been flipped, the agent stops and reports rather than sending. This gives you a one-line override when you need to silence the stack quickly.

## Promotion Pattern

Promotion is the moment an agent-produced output crosses from the outputs queue into the canonical vault. It is the explicit gate between "drafted by an agent" and "{{pack_owner_first}}'s vetted knowledge base."

**Three mechanical steps per item promoted:**

1. **Write the vault note** at the destination path implied by the content type (e.g. `Marketing/Marketing Outputs/LinkedIn Posts/<Title>.md` for a LinkedIn post, the relevant initiative folder for initiative-destined research).
2. **Flip the outputs queue row** from "ready for review" to "promoted", noting the vault destination path.
3. **Log on the coordination card** with the vault path and any outstanding items (typically a publish date or a published URL).

**Reversal ("unpromote").** If you later want to unpromote, archive or delete the vault note, flip the outputs queue row back to "ready for review" or "archived", and post a reversal comment on the coordination card. Unpromotion should be rare; it exists as a defined escape hatch, not a routine move.

## Frontmatter Conventions

Every page in the vault carries YAML frontmatter. The required fields depend on the page type; see the per-folder Guide for specifics. Common patterns:

- `type:` — the page type (contact, organisation, initiative, meeting, framework, etc.).
- `status:` — the page's current state (active, completed, archived, draft).
- `created:` — ISO date the page was first written.
- `tags:` — vault-wide taxonomy. See `Knowledge/tagging-policy.md`.

## Naming Conventions

- **Folders.** Title Case for major folders (`Customer-Facing Services/`), kebab-case for initiative folders (`milux-brain/`), Title Case for canonical organisations and people.
- **Files.** Match the canonical name of the entity. Acronyms in parentheses where useful: `National Armaments Materiel (NA-M).md`.
- **Wikilinks.** Use display text for readability: `[[CRM/contacts/Jane Smith|Jane Smith]]`.
- **Wikilinks in table cells** must escape the pipe: `[[CRM/contacts/Jane Smith\|Jane Smith]]`. Obsidian otherwise treats the pipe as a column separator and the table breaks.

## Per-Folder Guides

Every top-level folder ships with a `<Folder Name> Guide.md` at its root. The Guide is the contract for what belongs in the folder. Five sections:

1. **Purpose.** What this folder is for.
2. **Structure.** What each subfolder means.
3. **Frontmatter.** Required and optional fields per page type.
4. **Add discipline.** How to add new content. Points at the relevant skill if one exists.
5. **Canonical example.** A worked reference page so you can see what good looks like.

When you're not sure where something goes, read the relevant Guide.

## Adapting This Pack

Foothold is opinionated. The conventions in this document and in the per-folder Guides are the load-bearing defaults that make the pack work. Adapt where you need to, but adapt deliberately:

- Add folders if you have a domain not covered by the defaults.
- Don't rename folders without checking what links into them. Use `Knowledge/rules.md` to record any deviations from the defaults.
- Don't add agents to the upstream tier without enforcing the write boundaries at the tool layer.

The pack works because the conventions are kept tight. Drift is the fastest way to break it.
