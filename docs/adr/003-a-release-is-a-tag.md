# ADR 003: A release is a tag

Status: accepted, November 2026 (Foothold 2.5.0). Supersedes ADR 002.

## Context

ADR 002 made `main` the release channel: `/foothold-update` read the file tree of `main`, and
the README told a new user's AI tool to fetch the setup skill from `main` and follow it exactly.
A safety audit in November 2026 found both risky. Whatever was on `main` at the moment a person
asked was what their AI tool obeyed, with nothing to check it against, and an update applied
most changes after one yes without showing them. ADR 002 said that reading a tag instead would
be a new decision superseding it. This is that decision.

## Decision

- A release is a tag `vX.Y.Z` on `main`. Only the maintainer makes one.
- On a tag, `.github/workflows/release.yml` refuses the tag unless its version matches the
  four version records (`CHANGELOG.md`, `foothold/.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `data/foothold-map.json`) and its commit is on `main`
  (`tools/release_guard.py`). It then runs every check and the unit tests, builds the release
  with `tools/build_release.py`, and publishes a GitHub release holding three files:
  `foothold-X.Y.Z.zip`, `SHA256SUMS.txt` and `release-files.txt`.
- The zip is built the same way every time, so the same tag gives the same bytes and anyone can
  check a published zip against the repository.
- The release job is the only job with permission to write. Every other job is read-only.
- Setup works from the release folder the person was given (or the Claude plugin) and never
  fetches instructions from the internet. The update reads the latest release's
  `release-files.txt` and fetches each file from the address pinned to that tag, checking each
  against its checksum. Nothing a user receives points at `main`; `tools/check.py` fails if it
  does.
- The only zips that may be offered to users are those the release workflow builds from a tag.
  No zip is built by hand or committed to the repository.

## Consequences

- Merging to `main` no longer reaches users. A change reaches them when the maintainer tags a
  release, so the review of a release tag is the release review. `main` stays protected as
  ADR 002 set out, because every release is cut from it.
- A release needs tag protection, so a tag cannot be moved once published. That is a
  repository setting only an owner can turn on.
- Vaults installed before 2.5.0 hold Git blob SHA-1 checksums (`last_known_shas`). The update
  reads them once and records SHA-256 checksums from then on.
- Whether a given AI tool can download a release file has to be walked through by a person on
  that tool. Where it cannot, the update falls back to the person downloading the zip.
