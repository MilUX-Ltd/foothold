---
type: guide
folder: Marketing/Marketing Outputs
---

# Marketing Outputs Guide

## Purpose

`Marketing Outputs/` holds the published marketing artefacts your organisation produces: LinkedIn posts, case studies, news articles, press releases. The output side of the marketing function.

Distinct from `Marketing/Newsletter/`, which holds newsletter editions and backlog. And distinct from `Capabilities and Services/Internal Services/Content Pillars.md` and `Content Creation Workflow.md`, which hold the strategy and workflow that produce these outputs.

## Subfolders

- **`LinkedIn Posts/`.** One file per published post. Date-prefixed filenames (`YYYY-MM-DD <Title>.md`) so they sort chronologically.
- **`Case Studies.md`** as an index, or `Case Studies/` as a subfolder if you have enough that an index gets unwieldy.
- **`News Articles.md`** same pattern.

Add more subfolders if you produce other artefact types regularly (white papers, podcast episodes, video scripts).

## Add discipline

- Add a page when an artefact is drafted or published. Drafts carry `status: draft`; published pieces get `published:` date and `published_url:` in frontmatter.
- For LinkedIn posts, the body of the page is the post text as it appeared on LinkedIn. Don't rewrite the publish text; preserve it.
- Promotion gate: agent-drafted content goes through review before landing here. See the parent CLAUDE.md Promotion Pattern section.

## Frontmatter

Follows the parent Marketing Guide. Common pattern:

```yaml
---
type: linkedin-post | case-study | news-article
status: draft | scheduled | published
created: YYYY-MM-DD
published: YYYY-MM-DD
published_url: https://...
tags: [...]
---
```

## Related

- [[Marketing/Marketing Guide|Marketing Guide]] — parent
- [[Marketing/Newsletter/Newsletter Guide|Newsletter Guide]] — sibling
- [[Capabilities and Services/Internal Services/Internal Services Guide|Internal Services Guide]] — for the content strategy and workflow that feed this folder
