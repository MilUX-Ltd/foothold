---
type: guide
folder: CRM/networks
---

# Networks Guide

## Purpose

`networks/` holds networks of people you belong to or engage with. A network is distinct from an organisation because the relationship runs through a group identity rather than a single corporate entity.

## Three flavours of network

Each subfolder under `networks/` represents a single network. They typically fall into one of three flavours:

- **Formal networks.** Defined memberships with a coordinator and a clear list. Regional defence and security clusters, named industry working groups, formal advisory boards. Often have a website, an admin contact, and published terms.
- **Peer networks.** Informal but recurring groupings of founders and operators. Peer learning groups, founder dinners, mastermind cohorts. No formal membership, but a coordinator and a regular cadence.
- **Identity networks.** Groupings based on shared identity. Veterans, Reservists, alumni networks, professional certifications. Powerful for trust-based introductions; light on formal coordination.

## Subfolder layout per network

Each network gets its own subfolder named for the network. Inside:

- An index page named the same as the folder (the network's canonical entry point).
- Optional sub-pages for sub-networks, member-clubs, or events specific to that network.

## Add discipline

- Add a network entry deliberately. The test: is there a coordinator, a platform where the network communicates, and identifiable members? If all three, it earns a network entry. A loose Slack channel of acquaintances does not.
- Use the `flavour:` frontmatter field to mark which kind of network it is. Helps queries and tagging later.
- Cross-reference into the relevant defence-landscape page in `Intelligence/defence-landscape/` if the network operates against a public landscape mechanism (e.g. a formal cluster).

## Frontmatter

Follows the parent CRM Guide. `flavour: formal | peer | identity` is the network-specific field.

## Related

- [[CRM/CRM Guide|CRM Guide]] — parent
- [[CRM/contacts/Contacts Guide|Contacts Guide]] — sibling
- [[CRM/organisations/Organisations Guide|Organisations Guide]] — sibling
