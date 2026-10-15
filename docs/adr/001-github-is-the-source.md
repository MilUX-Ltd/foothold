# ADR 001: GitHub is the only source of the pack

Status: accepted, 15 October 2026 (card 7020). Decided by Matt Odell.

## Context

Until September 2026 Foothold was edited as an Obsidian vault and pushed to this repository
every four hours by a launchd job on one Mac (`auto:` commits). After the Macs were reorganised
on 29 September the job stopped, and the folder carried on under synoia in `MilUX/Open/Packs`
with nothing publishing it. The vault copy and `main` happened to match on 15 October, but there
were two copies with no rule about which one won.

## Decision

The repository on GitHub, `MilUX-Ltd/foothold`, is the only source. It is worked like any other
MilUX code: cloned into `MilUX/Restricted/Code/foothold`, changed on a branch, merged by pull
request. The `Open/Packs` copy was removed on 15 October 2026 and no sync job replaces it.

## Consequences

- One copy, with history, review and CI on every change.
- Editing the pack needs a clone and a pull request rather than an Obsidian window. To see it as
  a vault, open the clone (or `foothold/template/`) in Obsidian; local state stays out of Git.
- Nothing publishes by accident: a change reaches users only when a pull request merges.
