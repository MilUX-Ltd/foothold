---
type: rules
status: active
created: 2026-05-20
last_reviewed: 2026-05-20
---

# Rules

The numbered rule list for this vault. Every rule has a stable identifier (R-01, R-02, ...). Numbers are not reused, even if a rule is later deprecated.

Foothold ships with a baseline set of rules; everything below is the default. Add your own rules below the shipped set as your operating model develops.

---

## R-01 — Escape the pipe in table-cell wikilinks

In Obsidian table cells, the pipe character separates columns. A wikilink with display text uses the pipe too. The two conflict.

When placing a wikilink with display text inside a markdown table, escape the pipe with a backslash:

```markdown
| [[CRM/contacts/active contacts/Jane Smith\|Jane Smith]] | Acme Corp | jane@example.com |
```

Outside table cells, the unescaped pipe is fine. This rule applies wherever a wikilink with display text sits inside a table.

---

## R-02 — ISO dates everywhere

Dates use ISO 8601 format: `YYYY-MM-DD`. In frontmatter, in filenames, in body text. Avoid regional formats like `DD/MM/YYYY` or `MM-DD-YYYY`. Sorting and search both depend on the convention.

For daily notes the filename is the date itself: `2026-05-20.md`. For event notes the date prefixes the filename: `2026-05-20 <Event Name>.md`.

---

## R-03 — Frontmatter on every page

Every Markdown page in this vault carries YAML frontmatter. At minimum:

```yaml
---
type: <page type>
---
```

The `type` field is non-negotiable. It lets agents and queries operate on the page reliably. Other fields are page-type-specific; see the per-folder Guide for what each page type carries. Notes still in `Inbox/` are exempt until they are filed.

---

## R-04 — Entities live in CRM, maps live in Intelligence

`CRM/` holds entities you have or might have a working relationship with: contacts, organisations, networks. Each entity has one canonical home page. Relationship knowledge accumulates there.

`Intelligence/defence-landscape/` (and similar Intelligence subfolders) holds maps of the wider sector: frameworks, portals, programmes, public reference content. These pages are not entity homes; they point at CRM entries.

Test: if the page is about one entity and carries your engagement context, it belongs in `CRM/`. If the page describes a market mechanism or public landscape feature, it belongs in `Intelligence/`.

---

## R-05 — Rebrands keep one canonical page

When an organisation, programme, or framework is renamed, the canonical page in the vault adopts the new name. The old name is preserved in frontmatter as `former_name:` and as a body-text callout. Search continues to hit the old name through frontmatter and body text; the canonical anchor is the new identity. No parallel pages for old and new.

This matters most for MOD bodies, which reorganise on a multi-year cadence. The pattern absorbs reorganisations without breaking inbound wikilinks to children.

---

## R-06 — Promotion is deliberate

Content drafted by an agent or pulled in from elsewhere (an outputs queue, a transcript, a research scrape) becomes canonical vault knowledge only via an explicit promotion step. Promotion is a decision, not an automatic action.

See `CLAUDE.md` § Promotion Pattern for the three mechanical steps.

---

## R-07 — One frontmatter convention

Every note uses the same frontmatter conventions: the common fields, links as quoted wikilinks, lists as YAML lists, and a small fixed set of lower-case status values for each note type.

**Common fields.** `type` (required, see R-03), `status`, `created` (the date the note was first written), `updated` (the date it last changed meaningfully) and `tags`. Use the ones a note type needs; a daily note has no use for a status. The Guide for each note type says which it carries, and the templates in `Templates/` start each note with them.

**Links in frontmatter** are wikilinks inside quotes: `customer: "[[CRM/organisations/Acme|Acme]]"`. Unquoted, YAML reads the double square brackets as nested lists.

**Lists** are always YAML lists, either one item per line or in square brackets (`tags: [draft, review]`). Never a comma-separated string.

**Status values** are lower-case and come from a small fixed set for each note type:

| Note type | Status values |
|---|---|
| contact | `active`, `reference`, `archived` |
| organisation | `active`, `target`, `alumni`, `dormant` |
| network | `active`, `dormant` |
| customer-engagement | `scoping`, `active`, `paused`, `completed`, `archived` |
| initiative | `active`, `paused`, `completed` |
| idea | `raw`, `incubating`, `promoted`, `discarded` |
| service | `active`, `paused`, `retired` |
| linkedin-post, news-article | `draft`, `scheduled`, `published` |
| case-study | `draft`, `published` |
| newsletter-edition | `draft`, `scheduled`, `sent` |
| event | `upcoming`, `scoping`, `attended` |
| book-note | `queued`, `in-progress`, `read`, `abandoned` |
| programme, framework, portal | `active`, `retired` |
| market, literature, daily note, meeting note, review | no status |
| any other type | `active`, `archived` |

Daily notes, meeting notes and reviews carry no status. Notes still in `Inbox/` have not been filed and may have no frontmatter yet.

**Existing field names are kept as they are.** Fields such as `last-contact`, `last_reviewed`, `published_url`, `lawful_basis` and `last_health_check` stay exactly as they are written, even where the spelling differs from the others. Dashboards and skills look fields up by name, so renaming one in existing pages breaks them. This rule governs new notes and new fields; it is not a reason to rewrite old pages.

---

## Adding new rules

When you add a new rule, take the next R-NN number. Write the rule statement in one line, followed by a paragraph of context explaining why. If the rule emerged from a hypothesis (if you keep a `hypotheses.md`, see the Knowledge Guide), reference the hypothesis that justified promotion.

If a rule is later superseded, mark it deprecated rather than deleting. Numbers are not reused.
