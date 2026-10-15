# Risk register

Opened October 2026. Reviewed at each release.

| ID | Risk | Likelihood | Impact | Treatment | State |
|---|---|---|---|---|---|
| R1 | A harmful or broken change to `foothold/template/` reaches users on their next update, because `main` is the release channel (ADR 002) | Low | High | Protected `main` with required checks; template changes reviewed as releases; skill-safety-audit before a behaviour change ships | Open, treated |
| R2 | The README says the pack is MIT licensed, but the repository has no `LICENSE` file, so the grant a user relies on is not stated where they would look for it | High (true today) | Medium | Add a `LICENSE` file once the terms and the third-party skills' licences are confirmed | Open |
| R3 | A sync tool's local index (`.context/index.sqlite`) was committed by an old scheduled job and stays in the Git history | Certain (has happened) | Low (it indexes the public pack) | Untracked and refused by `tools/check.py`; history left alone, as a rewrite would break every clone and the update skill's SHAs | Closed, accepted |
