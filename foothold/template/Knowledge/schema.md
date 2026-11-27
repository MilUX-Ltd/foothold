---
type: schema
status: active
created: 2026-11-27
last_reviewed: 2026-11-27
---

# Schema

How the pages in this vault fit together: the kinds of page, the named connections between them, and what each skill reads and writes. Your AI reads this page to find its way around. The pack's own checks are written against it.

Add your own types and fields as your vault grows. The ones below are what Foothold ships with.

## Page types

Every page says what it is in its `type:` field. The defence landscape uses seven types.

| Type | What it is | Where it lives |
|---|---|---|
| `organisation` | A public body, company, investor, university or trade body | `CRM/organisations/` |
| `network` | A community or membership network | `CRM/networks/` |
| `cluster` | A regional defence and security cluster | `CRM/networks/` |
| `programme` | A defence programme | `Intelligence/defence-landscape/Programmes/` |
| `framework` | A route to market: a commercial framework or agreement | `Intelligence/defence-landscape/Frameworks/` |
| `portal` | A place where opportunities are published or suppliers register | `Intelligence/defence-landscape/Portals/` |
| `event-series` | A recurring event | `Intelligence/events/` |

Your own business uses the rest: `contact`, `initiative`, `customer-engagement`, `service`, `meeting-note` and so on. Each folder's guide lists the types that belong in it.

## Connections

A connection is a field in a page's frontmatter whose value is a link to another page. There are six.

| Field | Goes on | Links to | Means |
|---|---|---|---|
| `parent` | any page | a page of the same kind, or an index | Sits under |
| `customer` | programme, framework, portal, customer-engagement | organisation | Who the work is for |
| `operator` | framework, portal, event-series, network | organisation | Who runs it |
| `service` | programme | organisation | Which service it belongs to |
| `member_of` | organisation, cluster | network | Belongs to |
| `listed_on` | framework | portal | Where its opportunities are published |

Write the value as a link, in quotes:

```yaml
---
type: framework
name: Example Framework
customer: "[[CRM/organisations/mod/UK Ministry of Defence|UK Ministry of Defence]]"
operator: "[[CRM/organisations/government/Crown Commercial Service|Crown Commercial Service]]"
---
```

A field can hold more than one link:

```yaml
customer:
  - "[[UK Ministry of Defence]]"
  - "[[Home Office]]"
```

Three rules:

1. **Link to a page that exists.** If the organisation has no page yet, add one first, or leave the value as plain text until you do.
2. **Keep the detail in the body.** A field names the page it connects to. Anything more ("operated on its behalf by", "since 2026") belongs in the page's text.
3. **A link in the body is a mention.** It shows that one page refers to another, and no more. Use a field when the connection has one of the six meanings above.

Not every value in the shipped pages is a link yet. The pack is converting its own text values release by release.

## What a skill reads and writes

Each skill says which folders it reads from and which it writes to, in two fields at the top of its `SKILL.md`:

```yaml
reads:
  - Intelligence/defence-landscape/Frameworks
  - Context
writes:
  - Customer Engagements
```

- Each value is a folder in this vault.
- A skill that works only in the conversation and saves nothing has `writes: []`.
- When you write or change a skill, set these fields to what it really does. They are how you, and your AI, can see what a skill will touch before it runs.

Not every shipped skill carries these fields yet.

## Related

- [[Knowledge/Knowledge Guide|Knowledge Guide]]
- [[Knowledge/rules|Rules]]
- [[Knowledge/tagging-policy|Tagging Policy]]
