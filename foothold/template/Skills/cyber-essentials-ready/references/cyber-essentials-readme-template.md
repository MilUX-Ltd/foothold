# Cyber Essentials, this folder

This folder holds the compliance record for this machine against the UK Cyber Essentials technical controls. The folder is created and maintained by the `cyber-essentials-ready` skill that ships in the Foothold pack. The machine owner ran that skill on first setup, and the same skill runs monthly in verify mode to confirm the controls are still in place.

This is the owner's own record. It is not an IASME-issued Cyber Essentials certificate. The certificate is awarded by IASME or an IASME-licensed Certification Body following a separate self-assessment. This folder is what helps the owner answer that assessment with dates, states and evidence.

## For anyone reviewing this folder

If you are an IASME assessor, a Cyber Advisor, a defence-customer security team reviewing this supplier, or any reviewer who has opened this folder to understand the device posture:

1. Start with **compliance-status.md**. That is the latest snapshot. It shows green, amber or red per control with the date last verified.
2. Read **audit-log.md** next. That is the append-only history of every run, including the first setup and every monthly verify since.
3. If you want detail on any one run, open the matching file under **evidence/**. Each evidence file records, per control: state before, action taken (if any), state after, verification command output, and reversal path.

The user has not edited any of these files by hand. The skill writes them.

## What you should expect to see

- An initial-setup run is present.
- Verify runs are present at roughly monthly intervals since.
- The most recent run is recent (within the last month, ideally).
- The current compliance status is green across the board, or amber / red with a note explaining why and what remediation is planned or has been done.

If any of the above is missing (no initial run, gaps in the monthly cadence longer than 60 days, persistent red controls without remediation), ask the owner about it. The skill cannot run while the machine is off; reasonable explanations include holidays, illness, or the machine being out of service for a period.

## What is not in this folder

Cyber Essentials applies to more than one machine. This folder covers only the device named in `compliance-status.md`. For the rest of the organisation's Cyber Essentials evidence, ask the owner where the following live:

- Other in-scope devices (laptops, desktops, servers).
- Mobile devices used for business.
- Multi-factor authentication on cloud services.
- Network boundary controls (the router or firewall).
- The organisation's submitted IASME Question Set responses.

A typical answer is that those evidence pages live elsewhere in the owner's Foothold vault or in their organisation's own document store. The skill does not gather any of that.

## How the skill works, in two paragraphs

The `cyber-essentials-ready` skill walks the owner through the five Cyber Essentials technical controls on their primary computer (Mac or Windows). On first run it produces an evidence pack capturing the state of every control, applies changes the owner consents to one at a time, and offers to register a Cowork scheduled task that re-runs the skill monthly in verify mode. Every run, initial or verify, writes a dated evidence file under `evidence/`, appends a row to `audit-log.md`, and overwrites `compliance-status.md` with the latest snapshot.

The skill does not phone home, does not collect telemetry, and does not write anywhere outside this folder and the user's local computer. The skill is maintained by MilUX as part of the Foothold pack. Source available at the Foothold GitHub repo. Skill version, question-set version, and last-reviewed dates are recorded in the manifest that ships with the skill.

## Useful external links

- NCSC Cyber Essentials overview: <https://www.ncsc.gov.uk/cyberessentials/overview>
- IASME Knowledge Hub (current question set, guidance): <https://ce-knowledge-hub.iasme.co.uk/>
- NCSC Cyber Advisor scheme (find help): <https://www.ncsc.gov.uk/schemes/cyber-advisor/introduction>

## Created and maintained by

- Created on first run by `cyber-essentials-ready` skill, Foothold pack.
- Maintainer of the skill: MilUX, <https://milux.co.uk>.
- Maintainer of this folder's contents: the owner of this machine.
