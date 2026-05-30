---
type: home
created: {{install_date}}
last_reviewed: {{install_date}}
---

# {{pack_name}}

Welcome to your Foothold vault.

This is the landing page for everything that follows. Use it as a daily entry point and a place to surface what matters most.

## Where to start

- **`Context/{{pack_owner}}.md`** — your operator profile. Check it reads well and revise.
- **`Context/{{pack_org}}.md`** — your organisation page. Same.
- **Read the Guides.** Every folder has a `<Folder Name> Guide.md` at its root. Knowledge Guide, Operations Guide, Context Guide, and CRM Guide are the load-bearing ones.

## Today

Open today's daily note: `Daily/{{install_date}}.md` (or whichever day you're on).

## Customer engagements in scoping

> *Dataview query suggestion. Once you have engagement pages in `Customer Engagements/scoping/`, this section can render a live list. Replace this paragraph with a Dataview block similar to:*
>
> ````markdown
> ```dataview
> table status, customer, owner
> from "Customer Engagements/scoping"
> where type = "customer-engagement"
> sort created desc
> ```
> ````

## Active customer engagements

> *Dataview query suggestion. Once you have engagement pages in `Customer Engagements/active/`, this section can render a live list. Replace this paragraph with a Dataview block similar to:*
>
> ````markdown
> ```dataview
> table status, customer, owner
> from "Customer Engagements/active"
> where type = "customer-engagement"
> sort created desc
> ```
> ````

## Open initiatives

> *Dataview query suggestion. Once you have initiative pages, this section can render a live list. Replace this paragraph with a Dataview block similar to:*
>
> ````markdown
> ```dataview
> table status, owner
> from "Initiatives/active"
> where type = "initiative"
> sort created desc
> ```
> ````

## Recent contacts

> *Dataview query suggestion. Once you have CRM contact pages with `last-contact` frontmatter, this section can show the most recent interactions:*
>
> ````markdown
> ```dataview
> table organisation, last-contact
> from "CRM/contacts/active contacts"
> where type = "contact"
> sort last-contact desc
> limit 10
> ```
> ````

## Latest published

> *Dataview query suggestion. Once you have published Marketing/Marketing Outputs/LinkedIn Posts entries, this section can show the most recent:*
>
> ````markdown
> ```dataview
> table published, published_url
> from "Marketing/Marketing Outputs/LinkedIn Posts"
> where type = "linkedin-post"
> where status = "published"
> sort published desc
> limit 5
> ```
> ````

## How this vault works

See `CLAUDE.md` at the root for the architecture and working conventions. The short version: research and curation upstream of execution, with deliberate promotion of agent-produced output into the canonical vault.
