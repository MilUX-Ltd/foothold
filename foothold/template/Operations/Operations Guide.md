---
type: guide
folder: Operations
---

# Operations Guide

## Purpose

`Operations/` carries the policy and runtime assets your agents read at message-send time. Email signature stubs, kill-switch files, runtime guards, per-channel messaging rules. These files are load-bearing: they govern how your agents represent you to the outside world.

The folder is small by design. The scope test is simple: would removing this file break a live agent flow? If yes, it belongs here. If no, it belongs somewhere else.

## Structure

```
Operations/
├── Operations Guide.md         (this file)
├── agent-pause.md              (AI autonomy kill-switch)
├── email-signature.md          (canonical signature payload)
└── agent-messaging-policy.md   (per-channel rules, optional)
```

**agent-pause.md.** The AI autonomy kill-switch. Any agent sending a message on your behalf must check this file first. If the file contains anything other than a clear "go" signal, the agent stops and reports rather than sending. This gives you a one-line override when you need to silence the stack quickly.

The filename is conventional. If you want to scope the kill-switch to a specific named agent, rename the file (`<agent-name>-pause.md`), but every messaging skill in `Skills/` needs to be updated in lockstep.

**email-signature.md.** The canonical signature payload your agents append to outbound email. Single source of truth. The messaging skill loads this file, applies its content, and signs every message identically. Direct calls to the email send API outside the skill are a defect: the API send path typically bypasses the email client's signature settings.

**agent-messaging-policy.md.** Optional. If you have multiple messaging channels (LinkedIn, WhatsApp, Gmail, Slack) with different rules per channel, this file documents what each agent may and may not do on each. Approval-tier matrices, audit posture, send vs draft default. Only worth maintaining if you have meaningful per-channel divergence.

## Frontmatter

Required fields per file type.

**agent-pause.md** carries no formal frontmatter; the file body is the signal. By convention the file content reads either:

```
go
```

(or empty) when the stack is live, and a clear stop message when paused (e.g. `PAUSED 2026-05-20 — investigating spurious LinkedIn invitations`).

**email-signature.md:**

```yaml
---
type: policy
status: active
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
---
```

**agent-messaging-policy.md:**

```yaml
---
type: policy
status: active
created: YYYY-MM-DD
last_reviewed: YYYY-MM-DD
review_cycle: quarterly
---
```

## Add discipline

**In-scope test.** Before adding a file to `Operations/`, ask: would removing this file break a live agent flow? If yes, it belongs here. If no, it doesn't.

**Out of scope.** These do not belong in `Operations/`, even though they're "operational" in a loose sense.

- **Scheduled-task outputs.** Daily briefings, Aurora scans, signal scrapes. These belong in the outputs queue or get-and-discard with the summary surfaced at run time. They are not policy files.
- **Strategy and planning.** Business strategy, content strategy, marketing planning. Lives in `Capabilities and Services/Internal Services/` or `Marketing/`.
- **Agent infrastructure docs.** Deploy keys, server runbooks, agent stack architecture. Lives in your code repository or a private runbook, not the vault.
- **Initiative pages.** Initiative-level work lives in `Initiatives/`.

If you're not sure whether something belongs, default to "no". Operations is meant to be small.

**Changes are load-bearing.** Editing `email-signature.md` changes how every outbound message looks. Edit deliberately, commit with a clear message, and check the affected messaging skills still load it correctly.

**Kill-switch hygiene.** Flip `agent-pause.md` to a paused state when investigating any issue with agent behaviour. The cost of an unnecessary pause is zero; the cost of an unpaused stack misbehaving in public is not.

## Canonical example

See `email-signature.md` for the canonical pattern. The file contains a single signature block, plus any required legal disclaimer, in the exact form the messaging skill should append. No prose around it, no instructions — the file body is the payload.
