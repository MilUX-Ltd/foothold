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
| `operator` | framework, portal, event-series, network, organisation | organisation | Who runs it |
| `service` | programme | organisation, or one of three words | Which service it belongs to |
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

A field can hold more than one link, written as a list.

Five rules:

1. **Link to a page that exists.** If the organisation has no page yet, add one first, or leave the value as plain text until you do. The pack holds public bodies and not companies, so a company that runs a framework or portal stays as plain text.
2. **Keep the detail beside the link.** A field names the page it connects to. Anything more ("on its behalf", "since 2026", "initial phase") goes in a note field with the same name and `_note` on the end, or in the page's text.
3. **A programme no one service owns.** `service` may hold one of three plain words in place of a link: `Joint`, `Civil` or `Industry`.
4. **Who it is for is not who buys it.** `customer` is always an organisation. When a page is for a group and not an organisation ("defence supplier community"), say so in the plain-text field `audience`.
5. **A link in the body is a mention.** It shows that one page refers to another, and no more. Use a field when the connection has one of the six meanings above.

```yaml
customer:
  - "[[CRM/organisations/mod/UK Ministry of Defence|UK Ministry of Defence]]"
  - "[[CRM/organisations/mod/NAD Group/National Armaments Materiel (NA-M)|National Armaments Materiel]]"
customer_note: "UK MOD / DE&S (via EDP)"
service: Joint
audience: "Defence supplier community"
```

## What a skill reads and writes

Each skill says which folders it reads from and which it writes to, in two fields at the top of its `SKILL.md`:

```yaml
reads:
  - Intelligence/defence-landscape/Frameworks
  - Context
writes:
  - Customer Engagements
```

- Each value is a folder in this vault. A single full stop, `.`, means the whole vault, for the few skills that sweep or update everything.
- A skill that works only in the conversation has `reads: []` and `writes: []`. Most of the thinking tools are like this: they work from what you tell them.
- When you write or change a skill, set these fields to what it really does. They are how you, and your AI, can see what a skill will touch before it runs.

Every shipped skill carries these fields.

## Routes

A route is a job that takes more than one skill. Each route is a page in `Skills/Routes/` with `type: route` and an ordered `steps` list. Every step is one line: the skill's name, a colon, and what the skill does at that point.

```yaml
---
type: route
name: A tender lands
steps:
  - "eligibility-check: Checks the opportunity before you spend a week on it."
  - "bid-response: Drafts the response against the published criteria."
---
```

## Related

- [[Knowledge/Knowledge Guide|Knowledge Guide]]
- [[Knowledge/rules|Rules]]
- [[Knowledge/tagging-policy|Tagging Policy]]
