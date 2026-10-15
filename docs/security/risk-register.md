# Risk register

Opened October 2026. Reviewed at each release.

| ID | Risk | Likelihood | Impact | Treatment | State |
|---|---|---|---|---|---|
| R1 | A harmful or broken change to `foothold/template/` or the setup skill reaches users on their next install or update, because `main` is the release channel (ADR 002) | Low | High | Protected `main` with required checks; template and setup changes reviewed as releases; skill-safety-audit before a behaviour change ships | Open, treated |
| R3 | The README says the pack is MIT licensed, but the repository has no `LICENSE` file, so the grant a user relies on is not stated where they would look for it | High (true today) | Medium | Add a `LICENSE` file once the terms and the third-party skills' licences are confirmed | Open |
| R4 | A sync tool's local index (`.context/index.sqlite`) was committed by an old scheduled job and stays in the Git history | Certain (has happened) | Low (it indexes the public pack) | Untracked and refused by `tools/check.py`; history left alone, as a rewrite would break every clone and the update skill's SHAs | Closed, accepted |
| R5 | New installs probably stop at setup Step A.2 since 2.1.0. The one-prompt install fetches the setup skill as a raw file from `main`, as designed, but the 2.1.0 skill installs only from a template under `~/.claude/plugins/` and stops if it finds none; the 1.6.0 design removed the plugin and marketplace. The update skill also reads the GitHub tree API that failed for setup (LESSONS 3) | High (found by reading; not yet run) | High | Run a fresh one-prompt install and an update in Cowork to confirm; then restore setup to the one-prompt design (fetch each template file by raw URL) | Open |

R2 is retired and its number is not reused.
