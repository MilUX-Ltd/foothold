---
type: guide
folder: Intelligence
---

# Intelligence Guide

## Purpose

`Intelligence/` is for external-facing scanning. The market you operate in, the defence-landscape entities you encounter, competitors, public literature, valley-of-death analysis. Anything you need to know about the outside.

The discipline is "this is for external scanning, not internal artefacts". Your own delivery artefacts, your own decisions, your own initiative pages do not live here. They live in `Initiatives/`, `Capabilities and Services/`, or `Context/`.

## Structure

```
Intelligence/
├── Intelligence Guide.md           (this file)
├── defence-landscape/
│   ├── Defence Landscape Index.md
│   ├── Clusters/
│   │   └── <RDSC name>.md
│   ├── Programmes/
│   │   └── <Programme name>.md
│   ├── MOD Bodies/
│   │   └── <Body name>.md
│   ├── Frameworks/
│   │   └── <Framework name>.md
│   └── Portals/
│       └── <Portal name>.md
├── market/
│   └── <Market topic>.md
├── competitors/
│   └── <Competitor name>.md
├── literature/
│   └── <Paper, report, article>.md
└── decisions/
    └── <External decision relevant to your market>.md
```

**`defence-landscape/`** holds the public reference pages: clusters, programmes, MOD bodies, frameworks, portals. The `Defence Landscape Index.md` at the root is a map page, not an entity home. Entities live in CRM (`CRM/organisations/`); the landscape pages map their relationships.

**`market/`** is broader market analysis: industry trends, sector reports, dynamics affecting your space.

**`competitors/`** is competitive analysis. One page per competitor, with public-info only. Engagement notes against competitors stay in their CRM page (if they're an organisation you also engage with directly).

**`literature/`** holds notes on public-domain papers, reports, articles you've read. Source material that informed your thinking.

**`decisions/`** holds external decisions (procurement announcements, policy changes, regulatory shifts) that affect your market. Different from internal decisions, which live with the initiative they belong to.

## Frontmatter

Frontmatter depends on the entity type. Common pattern for a defence-landscape entity:

```yaml
---
type: cluster | programme | mod-body | framework | portal
status: active | retired
created: YYYY-MM-DD
website: https://...
parent: "[[Intelligence/defence-landscape/<parent>|<parent>]]"  # for child orgs
former_name: "<old name>"  # for rebrands
last_reviewed: YYYY-MM-DD
---
```

For market and literature pages:

```yaml
---
type: market | literature
created: YYYY-MM-DD
source: <URL or citation>
tags: [...]
---
```

## Add discipline

**Public information only.** Intelligence pages should be sourceable from public material: gov.uk, MOD website, company website, LinkedIn public profile, published reports. Anything you learned through a private relationship belongs in CRM, not here.

**Maps versus entities.** Index pages and landscape diagrams are maps, not entity homes. If a page has more than one entity's information, it's a map. If it has one entity's information, it's that entity's home. Maps live in `Intelligence/defence-landscape/`; entity homes live in the relevant CRM folder.

**Defence-landscape rebrands.** When a MOD body restructures (which happens every few years), use the parent-folder pattern: a folder named after the parent organisation, with renamed children inside carrying both new acronymic title and `former_name:` frontmatter. Keep search continuity.

**Don't mirror CRM.** If you have a working relationship with a defence-landscape entity, that organisation lives in `CRM/organisations/`. The Intelligence page references the CRM page; it doesn't duplicate it.

## Canonical example

The shipped Foothold defaults include `defence-landscape/Defence Landscape Index.md` as the canonical map page. For entity pages, see the public-info shape used in the open-source content layer: short company-style page with public mission, leadership where named publicly, website, and (where relevant) parent/child relationships via frontmatter.
