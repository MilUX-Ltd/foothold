# cyber-essentials-ready, changelog

## 1.0.0, 2026-05-24

Initial release. Walks a non-IT user through configuring a single personal Mac or Windows computer to meet the technical controls expected for UK Cyber Essentials (Montpellier question set).

Includes:

- `SKILL.md`, orchestration: version check, initial-setup vs verify branching, OS detect, mode picker (walk-through / commands / driver), preconditions, control-by-control walkthrough, evidence pack generation, audit log append, compliance status snapshot, reviewer README on first run, monthly schedule registration via Cowork scheduled-tasks (with calendar-reminder fallback), rollback pointer.
- `manifest.json`, version pin and pointer to the published manifest for runtime version checking.
- `references/controls.md`, plain-English summary of the five Cyber Essentials technical controls and what is out of scope (mobile, SaaS MFA, network boundary).
- `references/mac-steps.md`, ten per-control steps for macOS 14+, including firewall, FileVault, auto-updates, account separation, lock screen, password strength, built-in malware protection (Gatekeeper / XProtect / SIP), sharing services, guest user, app installation source.
- `references/windows-steps.md`, thirteen per-control steps for Windows 10 and 11, including firewall, BitLocker, Windows Update, account separation, UAC, lock screen, password policy, Defender, SmartScreen, Remote Desktop, AutoPlay, guest account verification, SMBv1.
- `references/verify-mode.md`, the verify-only flow used for scheduled monthly checks and manual re-runs. Defines mode-selection triggers, what verify mode skips, drift detection (green / amber / red), and what gets written.
- `references/evidence-template.md`, the template the skill populates per run to give the user an audit trail for their IASME submission.
- `references/audit-log-template.md`, the append-only history table written to the user's vault on first run and appended to every run thereafter.
- `references/compliance-status-template.md`, the latest-snapshot status page rewritten on every run, with per-control green / amber / red emoji and a list of manual checks the user is responsible for between runs.
- `references/cyber-essentials-readme-template.md`, the reviewer-facing README written to the user's vault on first run only, explaining the folder for any third party (IASME assessor, defence-customer security team, Cyber Advisor) opening it.
- `references/rollback.md`, how to undo each control if anything misbehaves.
- `references/glossary.md`, plain-English definitions of every term used.

The skill writes to a single dedicated folder in the user's vault, `Operations/Cyber-Essentials/`, holding `README.md`, `compliance-status.md`, `audit-log.md`, and `evidence/<dated files>`. The skill never modifies user files outside that folder.

Sources of truth:

- NCSC Cyber Essentials overview, NCSC Platform Guides, NCSC Small Business Guide.
- NCSC Device Security Guidance Configuration Packs (Crown Copyright, Apache 2.0), https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs.
- IASME free Question Set, IASME Readiness Tool, IASME Knowledge Hub.
- Apple Platform Security guide.
- Microsoft Learn documentation.

Out of scope in this release: mobile devices, multi-factor authentication on SaaS services, network boundary controls. The skill states these out-of-scope items at the start of every run.
