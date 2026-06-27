---
type: policy
status: active
created: 2026-05-20
last_reviewed: 2026-05-20
---

# Tagging Policy

The vault tag taxonomy. Foothold ships a small starter set; expand as patterns emerge from your own use.

## Why tags

Tags supplement folder structure and frontmatter `type` for queries that cross folder boundaries. They are not a primary navigation mechanism; wikilinks and Dataview queries against frontmatter usually serve better. Use tags for thematic cross-cuts, not for things a frontmatter field could capture.

## Starter taxonomy

### Status tags

- `#draft` — work in progress, not yet considered authoritative.
- `#active` — currently relevant or in use.
- `#archived` — no longer current but preserved for historical context.
- `#deprecated` — marked for retirement but still referenced.

Most pages won't need a status tag; frontmatter `status:` is the canonical source. Use the tag form when you want a tag-based query (e.g. find all draft content across the vault).

### Sensitivity tags

- `#chatham-house-rule` — applied to event notes captured under CHR. Triggers a stripping pass before public output draws on the content.
- `#confidential` — applied to pages that should never be shared outside the operator's organisation. Agents must check for this tag before any outbound use.

### Workflow tags

- `#follow-up` — applied to pages that have an outstanding action.
- `#blocked` — applied to initiatives or tasks waiting on something external.
- `#review` — applied to pages flagged for the next periodic review.

### Sector tags

Sector-specific. Adapt to your domain. Defence-sector starter set:

- `#defence` — defence-relevant content.
- `#mod` — MOD-specific content.
- `#sme` — SME-relevant content (capability programmes, accreditations).
- `#procurement` — procurement and commercial-route content.

### Data protection tags

Every contact in `CRM/contacts/` carries the UK GDPR Article 6 lawful basis on which you process their personal data. A contact has exactly one basis, recorded two ways: a canonical `lawful_basis:` frontmatter property (the source of truth) and a mirrored `lb-*` tag for filtering. Keeping the lawful basis on every contact is good practice and supports a data protection impact assessment if you need one.

- `#lb-legitimate-interests` (`lawful_basis: legitimate-interests`) — the default for B2B relationship-holding: prospects, network contacts, partners. Most contacts sit here.
- `#lb-consent` (`lawful_basis: consent`) — the person actively opted in to a specific use, e.g. a newsletter sign-up. Must be withdrawable.
- `#lb-contract` (`lawful_basis: contract`) — processing is necessary for a contract with the person, or steps before one: clients, associates, contractors.
- `#lb-legal-obligation` (`lawful_basis: legal-obligation`) — processing required by law, e.g. accounting and tax records.

The `/add-contact` skill asks which basis applies and proposes the most likely one. Update both the property and the tag if the basis changes (a prospect becomes a client, a contact subscribes).

## Conventions

- Tags are lower-case with hyphens, no spaces (`#chatham-house-rule`, not `#Chatham House Rule`).
- Apply tags in frontmatter under `tags:`, not as inline `#tag` mentions in body text. Inline tags work in Obsidian but are harder to query against and easier to mistype.
- Add a tag when you'd want to find every page with that property across the vault. If you'd only ever look for it from one folder, the folder structure is doing the work; you don't need the tag.

## Adding new tags

When a tag earns its place, add it to this file with a one-line definition. Tags without a definition here are drift; either define them or rename to fit an existing tag.

Tag changes affect the whole vault. Check what's already tagged with anything you're renaming before you commit.
