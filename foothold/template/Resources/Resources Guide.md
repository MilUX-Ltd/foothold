---
type: guide
folder: Resources
---

# Resources Guide

## Purpose

`Resources/` is your practitioner reference library. Methodologies, frameworks, ways of working, books, templates, business reference material. The stuff you read for ideas and patterns.

Three folders share adjacent territory; the distinction matters:

- **Resources** (here): methodology and reference. The theory and templates you draw on.
- **Knowledge** (`Knowledge/`): your operating policy. Rules, hypotheses, tagging policy, domain notes that agents read at runtime.
- **Intelligence** (`Intelligence/`): external scanning. The market, the defence landscape, competitors, literature.

If it's a method or framework you apply to your work, it's in Resources. If it's a rule about how the vault or agents work, it's in Knowledge. If it's information about the outside world, it's in Intelligence.

## Structure

```
Resources/
├── Resources Guide.md              (this file)
├── Methods/
│   ├── Methods Guide.md
│   ├── Kanban/
│   ├── Scrum/
│   └── ...
├── Ways of Working/
│   ├── Ways of Working Guide.md
│   ├── Meeting Agreements.md
│   ├── Task Writing Guidelines.md
│   └── ...
├── Books/
│   ├── Books Guide.md
│   ├── Library.md
│   └── <Book Note>.md
├── Business/
│   ├── Business Guide.md
│   └── <Business reference>.md
├── Frameworks/
│   ├── Frameworks Guide.md
│   ├── Cynefin/
│   └── ...
├── Reference/
│   ├── Reference Guide.md
│   └── <General reference material>.md
└── Templates/
    ├── Templates Guide.md
    └── <Template name>.md
```

**Methods.** Methodology theory: Kanban, Scrum, Lean, Agile, Cost of Delay, methodology-adjacent frameworks. Theory, not practice.

**Ways of Working.** Your own internal practices that govern how you work. Meeting agreements, task-writing conventions, working norms. The practice layer on top of methodology.

**Books.** Book notes, reading lists, library inventory. `Library.md` is the canonical reading list index.

**Business.** Business reference material: pricing strategy, sales playbooks, generic business doctrine that informs how you run the company.

**Frameworks.** Sense-making and decision-making frameworks: Cynefin, Wardley Mapping, OKRs, others. Tools you reach for to think through specific kinds of problems.

**Reference.** General reference material that doesn't fit the other buckets. Use sparingly. If something belongs in Reference for more than six months without finding a more specific home, the subfolder structure may need a new entry.

**Templates.** Reusable document templates: meeting agendas, decision records, retrospective formats. Templates you fill in, not policies you follow.

## Frontmatter

```yaml
---
type: method | framework | book-note | template | reference
status: active
created: YYYY-MM-DD
source: <citation or URL>
tags: [...]
---
```

## Add discipline

**The in-scope test.** Resources is a practitioner reference library. If you'd read this material to learn something, it belongs here. If it tells agents how to behave, it belongs in `Knowledge/`. If it's market data, it belongs in `Intelligence/`.

**Avoid the eclectic-mix anti-pattern.** Resources can drift into a junk drawer if you let any unstructured material land here. Use the seven subfolders. If something doesn't fit any of them, it probably doesn't belong in Resources.

**Don't put service offerings here.** Training and coaching offerings, even if methodology-flavoured, are customer-facing services. They belong in `Capabilities and Services/Customer-Facing Services/`.

**Book notes.** One file per book. Title, author, source link, your notes. Cross-reference into `Knowledge/hypotheses.md` if the book sparked an operating idea worth testing.

## Canonical example

The shipped Foothold defaults include the seven-subfolder structure plus a `Library.md` index in Books. Add your own methodology notes, framework writeups, and book notes as you go. The structure tells you where each piece belongs.
