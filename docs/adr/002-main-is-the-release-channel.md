# ADR 002: `main` is the release channel, so it is protected

Status: accepted, 15 October 2026 (card 7020). Records how the pack already works.

## Context

`/foothold-update` reads the file tree of `main` from the GitHub API and pulls every changed
file under `foothold/template/` into the user's vault. There is no release branch, tag or staging
copy between a merge and a user's next update.

## Decision

Treat `main` as the release channel. It is protected: changes arrive by pull request only, the
`checks` job must pass, force pushes and deletion are refused, and the rule applies to
administrators too. A change to `foothold/template/` is reviewed as a release would be.

## Consequences

- A broken template file reaches users on their next update, so the review of a template change
  is the release review.
- Files outside `foothold/template/` (this documentation, `tools/`, `.github/`, `.claude/`) are
  never copied into a user's vault, so repository housekeeping does not reach users.
- If a staging step is ever wanted, the update skill would read a tag or a release branch
  instead of `main`; that is a new decision superseding this one.
