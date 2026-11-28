# Security

## Reporting a problem

Email `matt@milux.co.uk` (the address under Help in the README) with "Security: Foothold" in
the subject. Please don't open a public issue for a security problem.

## What Foothold is, from a security point of view

Foothold is a folder of Markdown files and Claude skills. It runs no server and holds no data of
its own. A user's vault lives on their own computer; the update skill reads the latest release of
this public repository over HTTPS and sends nothing back.

## What protects the pack

- A release is a tag on `main` (ADR 003). The release workflow refuses a tag whose version does
  not match the version records or whose commit is not on `main`, then builds the release the
  same way every time, so a published zip can be checked against the repository.
- Users receive only releases. Setup works from the release folder and fetches no instructions;
  the update reads the latest release, checks every file against its SHA-256, and asks before
  changing anything that instructs an AI. Nothing a user receives points at `main`, and
  `tools/check.py` fails if it does.
- The only zips that may be offered to users are those the release workflow builds from a tag.
- `main` is protected: changes arrive by pull request with the `checks` job passing.
- Every GitHub Action is pinned by commit SHA and Dependabot proposes pin updates. The workflow
  token is read-only in every job except the one release job, which may write a release.
- Secret scanning with push protection is on.
- `tools/check.py` refuses local tool state and absolute home-folder paths.
- Skills that change behaviour are audited with `skill-safety-audit` before release.
- The threat model and risk register are in `docs/security/`.
