# Verify-only mode

When the `cyber-essentials-ready` skill runs in verify mode, it checks the current state of every control on the user's computer, compares it against the most recent evidence pack, and reports drift. Verify mode never changes anything on the machine without a deliberate user decision to switch to apply mode afterwards.

Verify mode is the routine compliance posture for a machine that has already been through an initial setup. The monthly scheduled check runs in verify mode. The user can also invoke verify mode manually any time they want a fresh status.

## How verify mode is selected

Three triggers:

1. **Scheduled task.** The Cowork scheduled task created in Step 9 of the initial setup fires with the prompt "Run cyber-essentials-ready in verify mode for <user>." The skill sees that prompt and runs verify.
2. **User asks.** Any of: "verify my CE compliance", "monthly CE check", "check my Cyber Essentials posture", "audit my computer against my last CE run", "is my computer still compliant".
3. **Skill asks at intake.** In Step 2 of the standard flow, the skill asks "Is this your initial setup, or a verify check?" If the user picks verify, the skill switches modes.

If there is no prior evidence pack in `Operations/Cyber-Essentials/evidence/`, verify mode is not valid. Tell the user there's nothing to compare against and offer to run the initial setup instead.

## What verify mode skips

- Step 2 (welcome, full version) becomes a one-line greeting and a reminder of when the last run was.
- Step 3 (platform detect) reads the platform from the most recent evidence pack rather than asking.
- Step 4 (mode picker) is not asked. Verify mode is the mode.
- Step 5 (preconditions) skips the backup precondition because no changes will be made. The "separate admin account still exists" check IS still run; loss of the second admin is itself a compliance drift.
- Step 6 (run the controls) is verify-only: per control, only the check-state and verify parts run; the apply path is not offered.
- Step 7 (evidence pack) still writes a new dated evidence file, but the file is tagged `mode: verify` in its frontmatter.
- Step 8 (rollback) is not surfaced; nothing has been changed.
- Step 9 (schedule registration) runs only on initial setup, not on verify runs.

## Drift detection

For each control, compare current state against the most recent evidence pack:

- **Match.** Current state matches the last recorded state. Status: green. Log "no drift".
- **Drift, looser.** Current state is less strict than the recorded baseline (e.g. firewall now off, FileVault now off, daily account now admin again, lock screen timeout extended past 15 minutes). Status: red. Surface to user immediately at the end of the run as a finding requiring action.
- **Drift, stricter.** Current state is more strict than the recorded baseline (rare; happens if the user manually tightened something). Status: green. Update the baseline going forward.
- **Indeterminate.** Cannot read the current state (permissions error, command unavailable, OS upgraded and the check no longer applies). Status: amber. Log the reason.

At the end of the per-control loop, summarise the drift count to the user:

> "Verify run complete. <N> controls checked. <X> green, <Y> red, <Z> amber. <full evidence file at link>. <compliance-status updated>."

If any red drift is found, ask the user whether to re-run in apply mode now to remediate. If they say yes, switch modes, walk through only the drifted controls, and write a new evidence pack tagged `mode: remediation`.

## Where verify mode writes

Every verify run produces three writes to the user's vault, same as initial setup:

- A new dated file in `Operations/Cyber-Essentials/evidence/` (file name format `YYYY-MM-DD-monthly-check.md` or `YYYY-MM-DD-manual-verify.md` depending on trigger).
- An append to `Operations/Cyber-Essentials/audit-log.md`, one row per run.
- An overwrite of `Operations/Cyber-Essentials/compliance-status.md` reflecting the latest snapshot.

The reviewer README at `Operations/Cyber-Essentials/README.md` is written on first run only.

## What the user sees at the end of a verify run

A short summary in chat:

> "Verify check complete on <date>. <N> controls green, <X> amber, <Y> red. <If green only:> Your machine still matches your initial Cyber Essentials setup. <If amber or red:> The following controls have drifted and need a look: <list>. Full evidence file: <link>. Compliance status: <link>."

If red drift was found and the user agreed to remediate, the standard apply flow resumes for those controls only, and the summary at the end of remediation says so.

## Frequency

The scheduled task runs verify mode monthly by default. The user can also run verify mode any time they want: ahead of a customer security review, after a major OS update, before submitting an IASME self-assessment. There is no harm in running it more often.
