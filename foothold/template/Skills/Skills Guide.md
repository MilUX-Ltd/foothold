---
type: guide
folder: Skills
---

# Skills Guide

## Purpose

`Skills/` holds the executable skills your agents use when working in this vault. Each skill is a folder containing a `SKILL.md` (the executable definition) and an optional `references/` subfolder for source material the skill needs.

Skills are different from policies. Policy lives in `Knowledge/` (rules agents follow always). Skills live here (procedures agents execute on demand). The pattern: a skill is a thing you can "run", whereas a policy is a thing you must "respect".

## Structure

```
Skills/
├── Skills Guide.md                 (this file)
└── <skill-name>/
    ├── SKILL.md                    (executable definition with YAML frontmatter)
    └── references/                 (optional source material the skill reads)
        └── <reference file>.md
```

One folder per skill. The folder name is kebab-case (`add-contact/`, `weekly-review/`, `linkedin-writer/`).

Inside each skill folder:

- **`SKILL.md`** is the executable definition. It carries YAML frontmatter with `name` and `description`, followed by Markdown instructions the agent reads when the skill runs.
- **`references/`** holds any source material the skill needs to read at runtime (templates, examples, lookup data). The skill resolves paths relative to its own `SKILL.md` to find these.

## Frontmatter

The `SKILL.md` frontmatter is the skill's interface to the agent runtime:

```yaml
---
name: skill-name
description: One or two sentences describing when this skill should be used. Include trigger phrases the agent can match against ("Use when the user says ..."). The description is what the agent uses to decide whether to invoke this skill.
---
```

The description is the most important field. Agents read it to decide whether to run the skill. Be specific about when the skill should fire and when it should not.

## Add discipline

**Skills are executable. Reference is not.** If the page is a thing your agent does (a procedure with steps), it's a skill. If the page is reference material your agent reads (a framework, a methodology, a contact list), it belongs in `Resources/`, `Knowledge/`, or the relevant content folder.

**One job per skill.** A skill should do one identifiable thing well. Multi-purpose skills are hard for the agent runtime to match against; users describe what they want in plain English, and a skill with a focused job gets picked up reliably.

**Trigger phrases in the description.** Include the phrases an agent might match the skill against ("Use when the user says 'add a contact', 'capture a new contact', 'log this person'..."). The agent's selection of which skill to run depends on this matching, so it's worth being explicit.

**Templates and source material in `references/`.** When a skill needs a template (e.g. a structured brief format, a frontmatter pattern), put the template in `references/` next to the SKILL.md and have the skill read it at runtime rather than embedding the content in the SKILL.md body. Easier to maintain.

**Don't write skills for things you only do once.** Skills earn their keep when they automate a recurring task. One-off work doesn't justify the codification.

## Canonical example

The shipped Foothold defaults include `foothold-setup` (the install-and-onboarding skill that lays your pack down) and `foothold-update` (the additive content-update skill). Both follow the same shape: YAML frontmatter declaring the skill name and description, then phased Markdown instructions the agent reads at runtime. Use them as patterns when you write your own.
