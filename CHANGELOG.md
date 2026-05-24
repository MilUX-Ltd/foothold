# Foothold changelog

## 1.1.0, 2026-05-24

Adds `cyber-essentials-ready`, a guided walkthrough that takes a non-IT founder through configuring their personal Mac or Windows computer to meet the UK Cyber Essentials technical controls.

Cyber Essentials is a recurring friction point for defence-sector founders selling into the MOD: it appears in supplier prequalification, in security clauses on framework agreements, and as a prerequisite for several gated frameworks. Many founders know they need it and don't know where to start. This skill closes that gap on the device side.

What the skill does:

- Walks the user through the five Cyber Essentials technical controls (firewalls, secure configuration, security update management, user access control, malware protection) one at a time, on macOS 14+ or Windows 10/11.
- Three modes: walk-through (the user clicks, the skill explains), commands (the skill stages safe commands on the clipboard, the user pastes), do-it-for-me (the skill drives System Settings via computer-use, the user retains consent per change).
- Verify mode for monthly re-checks, with drift detection (green / amber / red) and an optional remediation pass on red drift.
- Writes an evidence pack, append-only audit log, per-control compliance status snapshot, and reviewer-facing README to `Operations/Cyber-Essentials/` in the founder's vault. The pack is designed to be opened by an IASME assessor, a Cyber Advisor, or a defence customer's security team and read without further explanation.
- Registers a monthly Cowork scheduled task to keep the posture current, with a calendar-reminder fallback if scheduled tasks isn't available.

Scope is the founder's primary work computer. Mobile devices and SaaS multi-factor authentication are real Cyber Essentials requirements and the skill states up front that they are out of scope today; founders handle those separately. The skill is pinned to the IASME Montpellier question set; the pin lives in the skill's manifest, frontmatter and changelog, and gets reviewed when IASME publishes a new named release.

Skill catalogue: a new "Security and compliance skills" section in `Skills/Skill Examples.md` carries the cyber-essentials-ready entry.

Sources: NCSC Cyber Essentials overview, NCSC Platform Guides, NCSC Small Business Guide, NCSC Device Security Guidance Configuration Packs (Crown Copyright, Apache 2.0), IASME Question Set, IASME Readiness Tool, IASME Knowledge Hub, Apple Platform Security guide, Microsoft Learn.

## 1.0.0, 2026-05-23

Initial public release. Installable Obsidian vault pack for defence-sector founders, plus a Claude plugin that wires the install and update lifecycle. Includes folder structure, page templates, conventions, the `/foothold-setup` lifecycle skill, the `/foothold-update` content-update skill, and vault-bundled runtime skills: add-contact, add-organisation, add-event, prompt-master, process-interviewer, newsletter-writer, meeting-prep, late-payment-reminder. Ships pre-populated open-source defence reference content: regional defence and security clusters, public framework writeups, MOD body reference pages.
