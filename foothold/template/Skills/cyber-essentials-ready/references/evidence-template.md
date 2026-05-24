---
type: cyber-essentials-evidence
question_set: Montpellier
generated_by: cyber-essentials-ready skill (v1.0.0)
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
> Skill version: 1.0.0. Question set: Montpellier. Run by: cyber-essentials-ready skill, maintained by MilUX as part of the Foothold pack.

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

## Items that need a manual check between runs

These are things the skill cannot fully verify automatically, but Cyber Essentials still expects you to confirm. The next scheduled monthly check should re-ask these.

- [ ] All business-critical third-party applications are set to auto-update, or you check for updates manually within 14 days of release.
- [ ] Microsoft account / Apple ID password is strong and unique, and 2-step verification is enabled (if applicable).
- [ ] No unsupported software remains installed (vendor still releases security updates).
- [ ] Removable storage encrypted or controlled per your data-handling needs.

## Cross-reference to Cyber Essentials Question Set

The IASME Question Set is the authoritative checklist. Download the current version at https://iasme.co.uk/cyber-essentials/free-download-of-self-assessment-questions/. The table below is a rough crosswalk between the controls in this pack and the question-set themes. The exact question numbers shift between question-set releases (Beacon, Montpellier, Willow, etc.), so use the theme as the anchor.

| Control in this pack | Question-set theme | Where it sits |
|---|---|---|
| Firewall | Firewalls | Software firewall on the device |
| FileVault / BitLocker | Secure configuration | Encryption of removable and fixed media |
| Auto-updates | Security update management | Vendor updates applied within 14 days |
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
