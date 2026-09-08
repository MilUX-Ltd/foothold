# cyber-essentials-ready, changelog

## 1.1.0, 2026-09-08

Repointed the skill from the Montpellier question set to **Danzell**, the question set that applies to Cyber Essentials assessment accounts created after 26 April 2026, and to the NCSC's **Requirements for IT Infrastructure v3.3** (April 2026). An assessment account opened before 26 April 2026 has six months from that date to certify against the previous requirements, so the skill now asks rather than assumes.

The five technical controls are unchanged. Danzell changed the marking and the wording, and the skill changed with it.

Added:

- **Auto-fail handling throughout.** Danzell introduced the scheme's first automatic failure conditions: MFA missing on a cloud service where it is available, question A6.4 (operating systems and router or firewall firmware, high-risk or critical updates inside 14 days), and question A6.5 (applications including associated files and extensions, same window). Any one fails the whole assessment. The skill names all three in its opening briefing and carries the warning through the control steps, the evidence pack, the compliance status page and the reviewer README.
- **Step 6b, the auto-fail items this skill does not cover.** A short structured conversation before the evidence pack is written: list the cloud services and confirm MFA on each, confirm other in-scope devices and routers are patched, review browser extensions. The answers are recorded in the evidence pack under an "Auto-fail items" heading, and any no or unknown caps the run at amber.
- **Browser extensions as in-scope software.** Requirements v3.3 defines software to include extensions, so both platform reference files now walk the user through their browser extensions page and record what was removed.
- **Passwordless authentication.** v3.3 gives passkeys, FIDO2 authenticators, biometrics, security keys, push notifications and one-time codes a section of their own, and treats a FIDO2 authenticator as MFA in its own right. Mentioned on both platforms, not configured by this skill.
- **New glossary entries:** Auto-fail, Cloud service, CVSS, Danzell (replacing Montpellier), Passkey, Passwordless authentication, Requirements for IT Infrastructure.
- **"What changed in Danzell" section** in `references/controls.md`, covering the cloud service definition, the scope wording, the software development section and the Software Security Code of Practice, the repositioned backups guidance, and "point in time" now meaning the date the certificate is issued.

Changed:

- Password guidance on both platforms restated from v3.3: MFA, or 12 characters minimum, or 8 characters with common-password blocking; brute-force protection of no more than 10 guesses in 5 minutes or a lock after 10 attempts; no password expiry and no complexity rules, which v3.3 explicitly advises against.
- Unsupported operating systems now framed against the new "point in time" definition. The certificate issue date is the date that matters.
- Verify mode re-asks the auto-fail questions on every run, and treats an auto-fail condition as red on its own. The monthly cadence is now tied to the April 2026 change to the signed director's declaration, which acknowledges staying compliant across the whole certification period.
- `manifest.json` carries `requirements_doc` and `question_set_effective` alongside the question set name, and the out-of-scope list names cloud service MFA as an auto-fail item.

Re-audited with `skill-safety-audit` v3 on 8 September 2026 under R-28, both pack copies, verdict **PASS**. Report in the MilUX vault at `Skills/Skill Safety Audit - cyber-essentials-ready 1.1.0 2026-09-08.md`.

Two findings were raised and fixed during that audit, before this version was issued:

- **Medium.** Step 6b asked the user to list the business's cloud services and say which lacked MFA, and wrote that list to a file the reviewer README invites third parties to read, with no guidance on what not to capture. Step 6b now says service name and yes or no only, no account names or anything resembling a credential; warns the user that this is the most sensitive thing the skill writes and to close out the "no" answers before sharing the folder; and offers to record only a count and a date instead. The evidence template carries a matching sensitivity note.
- **Low.** The audit footer claimed the skill never writes outside `Operations/Cyber-Essentials/`, while the Windows password-policy check stages a `secedit /export` that writes to `C:\temp`. The footer now states the exception and tells the user to delete the file after the check. Pre-existing at 1.0.0, not introduced here.

Sources for this release: NCSC Cyber Essentials Requirements for IT Infrastructure v3.3 (https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf) and IASME's announcement of the April 2026 changes (https://iasme.co.uk/articles/important-update-changes-to-cyber-essentials-for-april-2026/).

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
