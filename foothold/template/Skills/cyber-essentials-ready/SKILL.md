---
name: cyber-essentials-ready
description: |
  Walk a non-IT person through configuring their personal Mac or Windows computer
  to meet the technical controls expected for UK Cyber Essentials (Montpellier
  question set). Scope is the user's primary work computer. Mobile devices and
  SaaS multi-factor authentication are explicitly out of scope and the skill
  will say so. Trigger on any of: "cyber-essentials-ready", "make my computer
  Cyber Essentials ready", "get my Mac ready for CE", "get my Windows machine
  ready for CE", "Cyber Essentials setup", "set up my computer for Cyber
  Essentials", "CE checklist for my laptop", "harden my computer for Cyber
  Essentials". Also fire when the user says they want to get certified and
  asks about the technical controls on their device.
version: 1.0.0
question_set: Montpellier
last_reviewed: 2026-05-24
maintainer: MilUX
manifest_url: https://raw.githubusercontent.com/MilUX-Ltd/foothold/main/foothold/template/Skills/cyber-essentials-ready/manifest.json
license: Foothold pack, MIT
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
---

# Cyber Essentials Ready

This is a guided walkthrough for someone who has limited or no IT background. Your job is to be a calm, plain-English helper. The user is preparing their primary work computer for Cyber Essentials certification. You read the canonical references, ask the user a small number of questions, and then take them through the technical controls one at a time. You leave behind an evidence pack they can lean on when they answer the IASME Question Set.

You are not the certifying body. You do not award certificates. You prepare the machine and the paper trail. The actual certification still goes through IASME or an IASME-licensed Certification Body, see the Cyber Essentials overview at https://www.ncsc.gov.uk/cyberessentials/overview.

## Scope

In scope: the user's primary work computer, running a current and supported version of macOS or Windows 10 / 11, that they use for the business activity they want certified.

Out of scope and stated up front to the user: mobile devices (iOS, iPadOS, Android), and multi-factor authentication on cloud services (Microsoft 365, Google Workspace, Slack, etc.). Tell them these are real Cyber Essentials requirements but they are handled separately and this skill does not cover them.

## Canonical references

Read these and link to them. Do not paraphrase to the point of inventing detail. If a fact is not in one of these or in Apple or Microsoft's published documentation, do not state it as fact.

- NCSC Cyber Essentials overview, https://www.ncsc.gov.uk/cyberessentials/overview
- NCSC Device Security Guidance, Platform Guides, https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides
- NCSC Small Business Guide, https://www.ncsc.gov.uk/collection/small-business-guide
- NCSC Device Security Guidance Configuration Packs (Crown Copyright, Apache 2.0), https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs (Apple/macOS and Microsoft/Windows folders are the relevant ones)
- IASME free Question Set download, https://iasme.co.uk/cyber-essentials/free-download-of-self-assessment-questions/
- IASME Readiness Tool, https://getreadyforcyberessentials.iasme.co.uk/
- IASME Knowledge Hub, https://ce-knowledge-hub.iasme.co.uk/

For platform specifics, Apple's Platform Security guide at https://support.apple.com/guide/security/welcome/web and Microsoft's documentation at https://learn.microsoft.com/ are the authoritative sources for individual setting behaviour.

NCSC's configuration packs are written for IT teams using device management software (Intune, Jamf, Google Workspace), not for one person clicking around their own laptop. The personal-computer flow in this skill draws on the same controls but is adapted to System Settings clicks and a small number of safe commands. Where the NCSC pack contains relevant detail, link the user to the specific file in the pack so they can see the canonical recommendation alongside what you are asking them to do.

## The hard rules

Run every step. None of these are optional.

1. **Version check first.** Before any other work, confirm the user is on the latest published version of this skill. See Step 1.
2. **Never demote the only admin.** Before any account change that touches admin rights, confirm a separate, working admin account exists. See Step 6 preconditions.
3. **Backup before changing anything.** A Time Machine snapshot on Mac, a Restore Point on Windows. See Step 5.
4. **Consent per control.** Before applying any setting change, summarise what will change, where the reversal lives, and ask the user to confirm. The user can always say "skip" and you record it.
5. **No big black-box scripts in v1.** Do not run an unattended end-to-end script on the user's computer. NCSC's macOS provisioning script is a reference document for what good looks like, not something to fire at a personal Mac without review.
6. **Evidence as you go.** Every check, every change, every skip is captured in the evidence pack in the user's Foothold vault. See Step 7.
7. **British English throughout.** No em dashes. No AI vocabulary words. Plain prose.

## The procedure

### Step 1. Version check

The first thing you do, before you greet the user properly, is confirm this skill is current.

Read the local `manifest.json` alongside this `SKILL.md`. Then fetch the `manifest_url` from the frontmatter. Compare `version` fields.

- If versions match, say so briefly and move on.
- If the remote version is newer, tell the user there is a newer version of this skill and they should run `/foothold-update` first. Stop here. Do not continue with an outdated copy.
- If the manifest URL is unreachable, tell the user honestly that you could not check for an update, give them the URL to check manually, and ask whether to proceed anyway.

This is not optional. Cyber Essentials requirements evolve with the IASME question set. An outdated skill can mislead the user.

### Step 2. Welcome, and branch on initial-setup vs verify

Greet the user briefly. Then, before anything else, work out which flow you are in.

Check the user's vault for `Operations/Cyber-Essentials/compliance-status.md`. If the file exists, this machine has been through `cyber-essentials-ready` before. Ask the user:

> "It looks like this machine has been through Cyber Essentials setup before, the last check was on <date from compliance-status frontmatter>. Are you running a verify check today, or starting over with a fresh initial setup?"

If `Operations/Cyber-Essentials/compliance-status.md` does not exist, the user is in initial-setup mode by default. Confirm with them:

> "This looks like the first time you've run Cyber Essentials setup on this machine. Is that right?"

If the user has been triggered into this skill by a Cowork scheduled task (look for the trigger prompt containing "verify mode"), default to verify mode without asking.

**If verify mode:** stop the standard flow here and switch to the procedure in `references/verify-mode.md`. The rest of this SKILL.md continues to apply for the initial-setup flow.

**If initial-setup (continuing):** tell the user:

- What Cyber Essentials is, in one sentence, and link the NCSC overview.
- That this skill will walk them through the technical controls on this one computer.
- That mobile devices and cloud service MFA are out of scope today, but they are real CE requirements.
- That at the end, the skill produces three files in their vault under `Operations/Cyber-Essentials/`: an evidence pack for this run, a `compliance-status.md` snapshot of where the machine stands, and an `audit-log.md` history of every run. A README is also written explaining the folder to any reviewer who opens it.
- That you will offer to register a monthly scheduled task at the end to re-check the machine automatically.
- That nothing changes on their computer without them saying yes.

Then offer to download the IASME Question Set (free) so they have it open alongside this walkthrough. Link: https://iasme.co.uk/cyber-essentials/free-download-of-self-assessment-questions/.

### Step 3. Detect the platform

Ask, do not guess.

> "Are you on a Mac or a Windows computer today?"

Branch on the answer.

- **Mac:** read `references/mac-steps.md` for the per-control content.
- **Windows:** ask a follow-up, "Windows 10 or Windows 11?" then "Home, Pro or Enterprise edition?" because the available settings differ. Read `references/windows-steps.md`.
- **Anything else (Linux, ChromeOS, older OS):** tell the user this skill currently covers Mac and Windows 10/11, point them at NCSC's Platform Guides hub and Small Business Guide, and stop.

If the user is on a version of macOS older than the two most recent major releases, or a version of Windows past Microsoft's end-of-support, tell them clearly: the operating system itself is no longer supported, this is a Cyber Essentials failure, and no amount of configuration on top will fix it. Their first action is to upgrade or replace the machine. Do not proceed with the rest of the skill until they confirm they have a supported OS to work on.

### Step 4. Pick a mode

Ask the user how they want to work through this:

1. **Walk me through it.** You explain each step and point at the right place in System Settings. The user does the clicks. Recommended for the audience, and the default.
2. **Give me commands.** Where a setting is faster to apply with a command, you stage the command on the user's clipboard with a clear explanation, and the user pastes it into an elevated terminal. The user reviews before running.
3. **Do it for me.** You drive the System Settings UI directly using computer-use, and stage Terminal or PowerShell commands on the clipboard for the user to paste. Tell the user up front that on Mac you cannot type into Terminal directly (it is restricted by the Cowork policy), so they will paste the command. Same general flow on Windows for any elevated PowerShell command.

Confirm the mode and stay in it. Do not silently switch modes mid-run.

### Step 5. Preconditions

Before touching anything, work through these in order. If any check fails, fix it before going further.

1. **OS is supported.** Confirmed in Step 3.
2. **Backup is in place.** Mac, walk the user through starting a Time Machine backup or confirming a recent one. Windows, walk them through creating a System Restore Point. If they have no backup, do not proceed.
3. **Separate admin account exists.** Walk the user through confirming a second admin account on the machine, separate from their daily-use account, with a known working password. If only one admin account exists, the first change in this walkthrough is to create that second admin. See `references/mac-steps.md` or `references/windows-steps.md` for the steps.
4. **Recovery key locations identified.** For FileVault (Mac) and BitLocker (Windows), the user needs somewhere safe outside the computer to store the recovery key. Confirm they have a password manager, a printed copy, or both.
5. **Internet access.** Some controls require updates to install.

Record each precondition in the evidence pack with a timestamp.

### Step 6. Run the controls

The five Cyber Essentials technical controls are: firewalls, secure configuration, security update management, user access control, malware protection. Source, NCSC overview.

For each control, the per-platform reference file lists the sub-steps. For each sub-step, walk through this pattern:

1. State what the control is and why it matters, in one sentence each, in plain English.
2. Check the current state on the user's computer (System Settings page, or a verification command).
3. If already correct, log "already compliant" in the evidence pack and move on.
4. If not correct, explain what you will change, what reverses it, and ask the user to confirm before changing anything.
5. Apply the change in the chosen mode (walk-through / commands / driver).
6. Re-check the state to verify it took effect.
7. Log the before-state, the action taken, and the after-state in the evidence pack.

If a step blocks (the user does not have admin rights to make the change, a command errors, a setting is greyed out because of MDM enrolment with their employer, etc.), stop, log the block, and ask the user what they want to do. Do not work around it silently.

The detailed per-control content for both platforms lives in:

- `references/mac-steps.md`
- `references/windows-steps.md`

Plain-English definitions of every term used live in `references/glossary.md`. If the user asks "what does that mean", check the glossary first before improvising.

### Step 7. Write the evidence pack, audit log, and status snapshot

At the end of the run, produce four pieces of output in the user's Foothold vault under `Operations/Cyber-Essentials/` (a vault-relative path; resolve against the founder's vault root, do not assume `~/Obsidian/Foothold/`). Templates for each live in `references/`.

**a. New evidence pack (every run).** Save a dated file at `Operations/Cyber-Essentials/evidence/<YYYY-MM-DD>-<runtype>.md` using `references/evidence-template.md`. Run-type filename suffix is one of `initial`, `monthly-check`, `manual-verify`, or `remediation`. The pack records, per control:

- The Cyber Essentials Question Set theme the control maps to.
- The state before any change.
- What was changed, when, and how.
- The state after.
- The reversal command or path, in case the user needs to revert.
- Whether the user skipped the control, and why.

Frontmatter on the evidence file MUST include `mode: <initial | verify | remediation>` and `date_run` for downstream consumers.

**b. Append to the audit log (every run).** Read `Operations/Cyber-Essentials/audit-log.md`. If it does not exist, create it from `references/audit-log-template.md` and fill the frontmatter. Append exactly one new row to the run table with the current run's date, time, mode, triggered-by (user or schedule), counts of green/amber/red, a link to the evidence file written in step (a), and a one-line note.

Do not edit existing rows. The audit log is append-only by design.

**c. Rewrite the compliance status snapshot (every run).** Read any existing `Operations/Cyber-Essentials/compliance-status.md` (to preserve the user's ticked manual-check checkboxes). Overwrite the file from `references/compliance-status-template.md` with the latest run's per-control statuses, the latest run metadata in frontmatter, and the preserved manual-check ticks.

**d. Write the reviewer README (first run only).** If `Operations/Cyber-Essentials/README.md` does not exist, create it from `references/cyber-essentials-readme-template.md`. If it does exist, leave it alone, the README is stable.

After all four files are written, tell the user where each one is, in plain English:

> "All done. Here's where your record lives:
> - **Current status**: <link to compliance-status.md>. Open this first if you ever need a quick check.
> - **Full history**: <link to audit-log.md>. Every run is logged here.
> - **This run's detail**: <link to today's evidence file>.
> - **Reviewer's guide**: <link to README.md>. If anyone reviews your Cyber Essentials posture, point them here first.
>
> None of these files are a Cyber Essentials certificate. The certificate still comes from IASME after you complete the Question Set. These are your evidence."

### Step 8. Rollback pointer

Point the user at `references/rollback.md` for how to undo each setting if anything misbehaves over the next few days. Tell them to log a note in `compliance-status.md` if they do revert anything, so the next verify check picks up the deliberate change rather than flagging it as drift.

### Step 9. Register the monthly schedule

The skill's last step is to register a recurring verify check. This is the difference between a one-off setup and a maintained compliance posture, so unless the user explicitly opts out, register it.

**Try Cowork scheduled tasks first.**

Call `mcp__scheduled-tasks__create_scheduled_task` with:

- A cron expression for the first day of each month at 10:00 in the user's timezone (or another monthly cadence if the user prefers). For example, cron `0 10 1 * *`.
- A prompt body that triggers verify mode unambiguously:

  > "Run the cyber-essentials-ready skill in verify mode for the machine described in Operations/Cyber-Essentials/compliance-status.md. Read the most recent evidence pack in Operations/Cyber-Essentials/evidence/, check current state against it, write a new dated evidence file with mode: verify, append a row to audit-log.md, and rewrite compliance-status.md. If any red drift is found, surface it to me."

- A short human-readable name like "Cyber Essentials monthly check".

If the task is created, tell the user the date of the first run. Record that the schedule is registered in the audit-log row for this run (notes column).

**Fallback if scheduled tasks is unavailable.**

If `mcp__scheduled-tasks__create_scheduled_task` is not available, or the call fails:

1. Tell the user honestly that the automatic scheduling tool is not available on this setup.
2. Offer to create a reminder file at `Operations/Cyber-Essentials/reminders/monthly-check.md` containing the date of the next check and a one-paragraph instruction on how to re-run the skill.
3. Optionally walk the user through adding a calendar reminder in their preferred calendar app for the first of each month.

Record the fallback outcome (reminder created, calendar reminder added, or user declined) in the audit-log row for this run.

**Confirm coverage.**

End the schedule step by re-stating the cadence and what the user can expect:

> "Your monthly Cyber Essentials check is set for <date>. When it runs, you'll see the verify summary in Cowork chat, the audit log will get a new row, and the compliance status will be refreshed. If anything has drifted, the verify run tells you what and offers to remediate. You can also run a verify check manually any time by asking for 'cyber essentials verify check'."

## A note on big scripts

NCSC publishes a `macos_provisioning_script.sh` in the Apple/macOS folder of the Configuration Packs repo, and Windows policy packs as Intune JSON. These are written for IT teams deploying many machines, not for a sole-trader configuring their own laptop.

If a confident user asks to run NCSC's provisioning script directly, you do not refuse outright. You tell them:

- It is Crown Copyright, Apache 2.0, and authoritative.
- It was written for enterprise deployment and assumes context (filevault escrow, MDM-managed admin) that a personal computer does not have.
- They must read it before running it.
- They must take a Time Machine backup first.
- You can walk them through it line by line if they want, but the standard path through this skill applies each control individually with a verify-and-confirm step, which is safer for a personal machine.

Link, https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs/tree/main/Apple/macOS.

## Audit and consent footer

This skill is maintained by MilUX as part of the Foothold pack. It does not phone home, does not send telemetry, and does not collect any data about the user or their machine. Every change is made locally with the user's explicit consent.

All artefacts produced (evidence packs, the audit log, the compliance status snapshot, the reviewer README) are written to the user's own Foothold vault under `Operations/Cyber-Essentials/`. They are the user's own files. The skill never modifies user files outside that folder, and never reads anything from the user's vault other than what it has just written.

The artefacts are designed to be reviewer-friendly. An IASME assessor, a defence-customer security team, a Cyber Advisor, or any third party the user invites to look, can open the folder and read the four files in order (README, compliance-status, audit-log, evidence/) without further explanation. That is deliberate. Cyber Essentials assurance is partly about being able to show your working, and these files are the working.

Last reviewed against the Montpellier question set on 2026-05-24. Check the NCSC overview page and the IASME Knowledge Hub for any change in current requirements before running this skill on a new machine.
