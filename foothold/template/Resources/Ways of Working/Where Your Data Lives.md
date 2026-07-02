---
type: guide
status: active
created: 2026-07-02
last_reviewed: 2026-07-02
tags: [data-handling, security, ways-of-working]
---

# Where Your Data Lives

This vault will end up holding your bid thinking, your customer relationships, your pricing instincts and your view of the landscape. Before it does, you should be able to answer, for yourself and for anyone who asks, where that data actually goes. This page is the straight answer. Where it and Anthropic's own documentation disagree, their documentation wins; check it rather than trusting a summary that may have aged.

## The short version

The vault is a folder of plain files on your own machine. It has no server side. Nothing in the pack transmits your data anywhere: the skills are plain-text instructions you can open and read, they write only to the vault, and the update mechanism is a one-way fetch from a public GitHub repository. The one party that processes your content is Anthropic, when you work with the vault through Claude, and that relationship is governed by your own plan's terms, not by anything Foothold controls.

## What Claude sees

When you (or a scheduled task) work in Cowork, the content used in that session is sent to Anthropic for processing, like any cloud AI tool. What Anthropic may do with it depends on your plan and your settings. Do the diligence you would do on any processor: read the [privacy policy](https://www.anthropic.com/legal/privacy) and your plan's commercial terms, and check your account's settings on whether conversations may be used for model improvement. If your firm has a data protection officer or an IT policy, this is the paragraph to show them.

Two practical consequences. First, Claude sees what a session touches, not the whole vault by default; a conversation about one engagement does not upload your CRM. Second, the scheduled tasks this pack offers (daily brief, sector scan, curation sweep) run on your machine through your own Cowork and write only to the vault; none of them posts, emails or sends anything anywhere.

## What never goes in the vault

Whatever your plan's terms say, some material does not belong in this system at all:

- Anything carrying a **classification marking**, at any level. This vault is not an accredited system and never will be.
- Anything subject to **export control**: controlled technical data in an AI processing pipeline is a transfer question you do not want to answer after the fact. See [[Intelligence/defence-landscape/Export Controls Orientation|Export Controls Orientation]].
- **Client material under handling caveats or NDAs** beyond what the client would knowingly expect you to process with a cloud AI tool. When in doubt, ask them; the conversation is easier before than after.
- **Personal data beyond business-contact basics** without a recorded lawful basis. The CRM convention tracks lawful bases per contact, and the `build-dpia` skill exists for anything heavier.

## Sitting inside a Cyber Essentials posture

The vault is business data on an end-user device, and your CE controls apply to it like anything else: full-disk encryption on, screen lock on, the machine inside your patching and malware scope, and backups per [[Resources/Ways of Working/Sync and Backup|Sync and Backup]]. Claude and Obsidian are installed software, so they belong in your software inventory. The `cyber-essentials-ready` skill walks the device controls if you have not done them.

## When a prime's security questionnaire asks

The honest answers, which are also good answers: business data is held as files on company-controlled, encrypted devices; the AI processor is Anthropic under a paid commercial plan, terms available; no third-party or pack-operated servers hold the data; the automation is plain-text instruction files, auditable on request; and updates are pulled from a public repository with nothing flowing back. Firms fail these questionnaires by not knowing, more than by any particular answer.

## Related

- [[Resources/Ways of Working/Sync and Backup|Sync and Backup]]
- [[Intelligence/defence-landscape/Export Controls Orientation|Export Controls Orientation]]
- [[Knowledge/tagging-policy|Tagging policy]] for the lawful-basis convention
