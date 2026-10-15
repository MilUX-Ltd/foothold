# Threat model

Foothold 2.1.0, October 2026. Proportionate to what the pack is: public Markdown and skills, no
server, no data of its own.

## What is worth protecting

1. **The integrity of `main`.** Every update reads it, and skills are instructions
   that Claude follows inside the user's vault, which holds their bids, customers and commercial
   detail. A malicious or careless change to a skill is the one route by which this repository
   could harm a user.
2. **The users' trust that nothing leaves their vault.** The README promises that no skill
   transmits data externally.

## Who and what could cause harm

| Source | How | Main control |
|---|---|---|
| A change merged without review | A skill gains an instruction that sends vault content somewhere, or a template file breaks updates | Protected `main`, required `checks`, CODEOWNERS, skill-safety-audit before release |
| An outside pull request | Instruction-shaped text in a contribution, or a hidden change in a large diff | Pull requests from forks run CI with a read-only token; review reads every changed template file; content is data, never instruction |
| A compromised GitHub Action | A tag moved to malicious code | Actions pinned by commit SHA; Dependabot proposes pin updates for review |
| A local file swept into a commit | A sync tool's index, Obsidian state, a key | `.gitignore`, `tools/check.py`, secret scanning with push protection |
| A third-party skill or reference | Upstream text changes meaning or licence | Third-party material is copied in at a reviewed point, attributed, not fetched live |

## Out of scope

The user's own vault, their Claude plan and their Obsidian install: the pack has no reach there
beyond the files it ships.
