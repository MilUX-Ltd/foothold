---
type: home
created: {{install_date}}
last_reviewed: {{install_date}}
---

# {{pack_name}}

Welcome to your Foothold vault.

This is the landing page for everything that follows. Use it as a daily entry point and a place to surface what matters most.

## Where to start

- **[[Getting Started - Your First Week]]** — one small win a day for your first week. Start here.
- **[[How to Use This Vault]]** — the four working habits that make the system compound: brief it like an intern, describe processes so they can be automated, watch for repeatable patterns, review the work and the working.
- **`Context/{{pack_owner}}.md`** — your operator profile. Check it reads well and revise.
- **`Context/{{pack_org}}.md`** — your organisation page. Same.
- **Read the Guides.** Every folder has a `<Folder Name> Guide.md` at its root. Knowledge Guide, Operations Guide, Context Guide, and CRM Guide are the load-bearing ones.

## Today

Open today's daily note: `Daily/{{install_date}}.md` (or whichever day you're on).

---

> [!info] The panels below are live queries. They need the free **Dataview** community plugin: Settings → Community plugins → Browse → Dataview → Install and Enable. Until then they display as code; once Dataview is on, they fill themselves as your vault grows. Empty panels just mean no pages of that kind yet.

## Customer engagements in scoping

```dataview
table status, customer, owner
from "Customer Engagements/scoping"
where type = "customer-engagement"
sort created desc
```

## Active customer engagements

```dataview
table status, customer, owner
from "Customer Engagements/active"
where type = "customer-engagement"
sort created desc
```

## Open initiatives

```dataview
table status, owner
from "Initiatives"
where type = "initiative" and status != "completed"
sort created desc
```

## Recent contacts

```dataview
table organisation, last-contact
from "CRM/contacts/active contacts"
where type = "contact"
sort last-contact desc
limit 10
```

## Latest published

```dataview
table published, published_url
from "Marketing/Marketing Outputs"
where status = "published"
sort published desc
limit 5
```

## How this vault works

See `CLAUDE.md` at the root for the architecture and working conventions. The short version: research and curation upstream of execution, with deliberate promotion of agent-produced output into the canonical vault.
