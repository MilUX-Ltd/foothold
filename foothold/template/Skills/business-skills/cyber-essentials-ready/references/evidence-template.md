---
type: cyber-essentials-evidence
question_set: Danzell
requirements_doc: Cyber Essentials Requirements for IT Infrastructure v3.3
generated_by: cyber-essentials-ready skill (v1.1.0)
machine_name: <FILL>
machine_owner: <FILL>
machine_os: <FILL>
date_run: <YYYY-MM-DD>
date_run_iso: <YYYY-MM-DDTHH:MM>
status: complete | partial | aborted
---

# Cyber Essentials evidence pack

> This file is your record of what was checked, what was changed, and what was deliberately left as it was. It is not a Cyber Essentials certificate. The assessor at IASME (or your chosen Certification Body) may ask about any of these items, and this pack helps you answer with the dates and verifications.
>
> Skill version: 1.1.0. Question set: Danzell, Requirements for IT Infrastructure v3.3. Run by: cyber-essentials-ready skill, maintained by MilUX as part of the Foothold pack.

## Summary

- Total controls considered: <N>
- Applied: <N>
- Already compliant: <N>
- Skipped (with reason): <N>
- Blocked (with reason): <N>

## Preconditions

| Item | Status | Note |
|---|---|---|
| OS supported | <pass / fail> | <macOS or Windows version> |
| Backup in place | <pass / fail> | <Time Machine snapshot timestamp, or Restore Point timestamp> |
| Separate admin account exists | <pass / fail> | <admin account username, logged in successfully on YYYY-MM-DD> |
| Recovery key location identified | <pass / fail> | <password manager / printed / other> |
| Internet access | <pass / fail> | |

## Controls

Repeat this block per control. The example below is for a single control; the skill produces one block per control it walks through.

### Control: <name>

- **Cyber Essentials theme:** <firewalls | secure configuration | security update management | user access control | malware protection>
- **State before:** <what was seen on the machine before any change>
- **Action taken:** <walk-through clicks, commands run, or "none, already compliant", or "skipped">
- **State after:** <what was seen after the change>
- **Verification:** <command output, screenshot location, or System Settings location and value>
- **Reversal:** <pointer to rollback.md section, or in-line reversal note>
- **Outstanding follow-up:** <e.g. "user to confirm third-party app auto-update settings", or "none">
- **Timestamp:** <YYYY-MM-DD HH:MM>

## Auto-fail items

Danzell introduced automatic failure conditions. Any one of these fails the whole assessment on its own, however good the rest of the answers are. Record the position on each, with the date it was checked. Two of the three are outside the scope of this skill; they are recorded here so a reviewer can see they were put to the machine owner and answered.

> **Sensitivity.** This section names services and says which of them do not yet have MFA, which makes it the most sensitive part of this pack. Service name and yes or no only. No account names, no email addresses, no usernames, nothing resembling a credential. Close out the "no" answers before handing this folder to anyone outside the business.

**Cloud service MFA (not covered by this skill; cloud services cannot be excluded from scope).**

| Cloud service | MFA on for every account? | Date confirmed | Note |
|---|---|---|---|
| <e.g. Microsoft 365> | <yes / no> | <YYYY-MM-DD> | |

**Question A6.4, operating systems and router and firewall firmware, high-risk or critical updates inside 14 days.**

- This machine: <pass / fail / unknown>, evidence in Control 3 above.
- Other in-scope devices, routers and firewalls: <list, and the position on each, or "none in scope">

**Question A6.5, applications including associated files and extensions, high-risk or critical updates inside 14 days.**

- Applications set to auto-update: <list>
- Applications checked manually: <list, with the date last checked>
- Browser extensions reviewed on <YYYY-MM-DD>: <removed / kept, with names>

**Overall auto-fail position for this run:** <clear / at risk / failing>. If anything above is no or unknown, the overall status for the run is amber at best.

## Items that need a manual check between runs

These are things the skill cannot fully verify automatically, but Cyber Essentials still expects you to confirm. The next scheduled monthly check should re-ask these.

- [ ] All business-critical third-party applications are set to auto-update, or you check for updates manually within 14 days of release.
- [ ] Browser extensions reviewed; nothing unused, unrecognised or abandoned by its developer is installed.
- [ ] MFA still on for every cloud service in use.
- [ ] Microsoft account / Apple ID password is strong and unique, and 2-step verification is enabled (if applicable).
- [ ] No unsupported software remains installed (vendor still releases security updates).
- [ ] Removable storage encrypted or controlled per your data-handling needs.

## Cross-reference to Cyber Essentials Question Set

The IASME Question Set is the authoritative checklist. The current set is Danzell, which applies to assessment accounts created after 26 April 2026 and pairs with the NCSC's Requirements for IT Infrastructure v3.3. Download the current version at https://iasme.co.uk/cyber-essentials/free-download-of-self-assessment-questions/.

The table below is a rough crosswalk between the controls in this pack and the question-set themes. Question numbers shift between question-set releases (Beacon, Evendine, Montpellier, Willow, Danzell), so use the theme as the anchor. The two update questions are named here because Danzell makes them automatic fails and their numbers are stated in the IASME announcement.

| Control in this pack | Question-set theme | Where it sits |
|---|---|---|
| Firewall | Firewalls | Software firewall on the device |
| FileVault / BitLocker | Secure configuration | Encryption of removable and fixed media |
| Auto-updates, operating system | Security update management | A6.4, high-risk or critical updates within 14 days, automatic fail |
| Auto-updates, applications and extensions | Security update management | A6.5, high-risk or critical updates within 14 days, automatic fail |
| Separate admin / standard user | User access control | Use of administrative accounts |
| UAC (Windows) | User access control | Privilege escalation prompts |
| Lock screen and timeout | Secure configuration | Auto-lock on inactivity |
| Password policy | User access control | Password length and lockout |
| Gatekeeper / SIP / Defender / SmartScreen | Malware protection | Malware protection on user devices |
| Sharing services off / Remote Desktop off | Secure configuration | Default-deny services posture |
| Guest account off | User access control | Removal of default and unused accounts |
| SMBv1 disabled (Windows) | Secure configuration | Insecure protocols disabled |

## Signatures and ownership

- Machine owner confirms this pack reflects the state of the machine on the date run: <name, date>
- Where another person (an IT helper, a consultant, a family member) ran the skill, record their name here too: <name, role, date>
