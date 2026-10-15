# Security

## Reporting a problem

Email `matt@milux.co.uk` (the address under Help in the README) with "Security: Foothold" in
the subject. Please don't open a public issue for a security problem.

## What Foothold is, from a security point of view

Foothold is a folder of Markdown files and Claude skills. It runs no server and holds no data of
its own. A user's vault lives on their own computer; the update skill reads this public
repository over HTTPS and send nothing back.

## What protects the pack

- `main` is protected: changes arrive by pull request with the `checks` job passing, and `main`
  is what every update reads (ADR 002).
- Every GitHub Action is pinned by commit SHA, the workflow token is read-only, and Dependabot
  proposes pin updates.
- Secret scanning with push protection is on.
- `tools/check.py` refuses local tool state and absolute home-folder paths.
- Skills that change behaviour are audited with `skill-safety-audit` before release.
- The threat model and risk register are in `docs/security/`.
