# ADR 001: This repository is the only source of the pack

Status: accepted, October 2026.

## Context

For a time Foothold was edited in a separate working copy and pushed to this repository by a
scheduled job. When the job stopped, nothing said so, and there were two copies with no rule
about which one won.

## Decision

`MilUX-Ltd/foothold` on GitHub is the only source. The pack is changed like any other code: in a
clone, on a branch, merged by pull request. No other copy is kept, and no scheduled job pushes to
it.

## Consequences

- One copy, with history, review and CI on every change.
- Editing the pack needs a clone and a pull request rather than an Obsidian window. To see it as
  a vault, open the clone (or `foothold/template/`) in Obsidian; local state stays out of Git.
- Nothing publishes by accident: a change reaches users only when a pull request merges.
