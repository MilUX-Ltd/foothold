---
type: cyber-essentials-compliance-status
machine_name: <FILL_ON_FIRST_RUN>
machine_owner: <FILL_ON_FIRST_RUN>
machine_os: <FILL_ON_FIRST_RUN>
question_set: Montpellier
last_run_date: <YYYY-MM-DD>
last_run_mode: <initial | verify | remediation>
last_run_evidence: <relative link to evidence file>
overall_status: <green | amber | red>
---

# Cyber Essentials compliance status

> Single-page snapshot of where this machine stands against the Cyber Essentials technical controls, as of the last time the `cyber-essentials-ready` skill ran. This file is rewritten on every run. For the full history, see [audit-log.md](audit-log.md). For the detail of the latest run, see the linked evidence file in the frontmatter.

**Machine:** <machine_name>, <machine_os>
**Owner:** <machine_owner>
**Last checked:** <YYYY-MM-DD>, <mode>
**Overall status:** <green | amber | red>

If the overall status is red, the user has compliance drift and should remediate before any external review.
If amber, one or more controls could not be determined and need a manual look.
If green, the machine matches the recorded Cyber Essentials baseline as of the last check.

## Per-control status

| Control | CE theme | Status | Last verified | Notes |
|---|---|---|---|---|
| Firewall | Firewalls | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | <one-line note> |
| Full-disk encryption | Secure configuration | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Automatic updates | Security update management | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Separate admin account | User access control | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Lock screen and timeout | Secure configuration | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Password policy | User access control | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Built-in malware protection | Malware protection | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Sharing / remote services | Secure configuration | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Guest user | User access control | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| App source / installation control | Secure configuration | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |

Windows-only additions, included when the machine is Windows:

| Control | CE theme | Status | Last verified | Notes |
|---|---|---|---|---|
| User Account Control (UAC) | User access control | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| SmartScreen | Malware protection | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| Remote Desktop | Secure configuration | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| AutoPlay | Secure configuration | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |
| SMBv1 disabled | Secure configuration | <🟢 / 🟠 / 🔴> | <YYYY-MM-DD> | |

## Items needing a manual check between runs

These cannot be auto-verified by the skill. The user is responsible for re-confirming at each verify cycle.

- [ ] All business-critical third-party applications are still on supported versions and set to auto-update.
- [ ] Microsoft account / Apple ID password is still strong, unique, and protected by 2-step verification (if applicable).
- [ ] No unsupported software added since the last check.
- [ ] BitLocker / FileVault recovery key is still accessible (test by retrieving from password manager).
- [ ] Second admin account password is still known and works (sign in to it at least once between verify runs).

## Out of scope on this machine

The following Cyber Essentials requirements are not covered by this skill and the user handles them separately:

- Mobile devices (iOS, iPadOS, Android phones and tablets used for business).
- Multi-factor authentication on cloud services (Microsoft 365, Google Workspace, etc.).
- Network boundary controls (home / office router or firewall).

Record where evidence for those items lives, so a reviewer reading this status page can find them:

- Mobile devices: <link or note>
- SaaS MFA: <link or note>
- Network boundary: <link or note>

## Rewrite rules for the skill

When the skill writes this file, it:

1. Loads this template if the file does not exist, otherwise overwrites the existing file.
2. Populates frontmatter with the latest run's metadata.
3. Sets the per-control status emoji based on the latest run's findings.
4. Preserves the "Items needing a manual check" checkboxes if any were ticked by the user previously (read existing file before overwrite, preserve checked items).
5. Saves the file back to `Operations/Cyber-Essentials/compliance-status.md`.
