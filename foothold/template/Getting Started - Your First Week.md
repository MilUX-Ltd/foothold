---
type: guide
created: {{install_date}}
last_reviewed: {{install_date}}
tags: [getting-started, onboarding]
---

# Getting Started: Your First Week

The vault is installed and your Context pages are written. This page turns that into a working habit, one small win a day. Nothing here takes more than half an hour. Tick things off as you go; this page is yours to edit.

If you asked setup to schedule a check-in, Cowork will nudge you in a week. If you did not, tell it now: "remind me in a week to review my Getting Started progress".

## Day 1: check the foundations

- [ ] Read `Context/{{pack_owner}}.md` and `Context/{{pack_org}}.md`. Onboarding wrote these from your answers; fix anything it got wrong. Everything agents do for you starts from these pages, so accuracy here pays compound interest.
- [ ] Skim the four load-bearing Guides: Knowledge, Operations, Context, CRM. Ten minutes total; you now know where everything lives.

## Day 2: bring your relationships in

Pick the option that matches your reality:

- **You already run a CRM** (HubSpot, Salesforce, Pipedrive, a spreadsheet with pretensions). Run `/import-relationships`. If your CRM has a Cowork connector it reads directly; otherwise a CSV export works. It triages with you first, so only living relationships come in.
- **You want to keep your current CRM.** Fine; the vault CRM then holds relationship knowledge (what was said, what matters to them) rather than pipeline. Add people as you meet them with `/add-contact`.
- **You are starting from scratch.** After every real conversation this week, run `/add-contact`. Five contacts entered well beats fifty entered badly.

## Day 3: your daily brief and your first meeting

- [ ] Run `/daily-brief`. It reads everything you are working on (engagements, initiatives, items rolled from previous days, upcoming events) and writes today's note in `Daily/` for you. You read it; you do not fill in a form.
- [ ] If it earns its place, put it on a schedule: "run /daily-brief every weekday at 08:00". The brief is then waiting before you are. Setup may already have offered this.
- [ ] Before your next external meeting, run `/meeting-prep`. It reads your CRM and briefs you. This is the moment the vault starts paying you back.

## Day 4: look the part

- [ ] Run `/design-system-setup`. It builds your design system from your brand answers, so every deck and one-pager you produce from here looks like one company made it.
- [ ] Check `Context/Brand.md` still sounds like you after onboarding.

## Day 5: learn the landscape

- [ ] Read the [[Intelligence/defence-landscape/Founder's Procurement Playbook|Founder's Procurement Playbook]], then the [[Intelligence/defence-landscape/Defence Landscape Index|Defence Landscape Index]].
- [ ] Register on the [[Intelligence/defence-landscape/Portals/Defence Sourcing Portal|Defence Sourcing Portal]] and set alerts. Free, ten minutes, and every MOD tender over £10k now finds you.
- [ ] Skim the [[Resources/Reading List|Reading List]] and pick one thing to read this month.

## Week 2 and on

- Read [[How to Use This Vault]]. Ten minutes on the four habits that decide whether this system compounds or plateaus.
- Got a live opportunity? Run `/eligibility-check` before you commit a week to it, and `/bid-response` after a GO.
- Start one initiative in `Initiatives/`, not three. The Initiatives Guide shows the shape.
- Decide your [[Resources/Ways of Working/Sync and Backup|sync and backup]] approach before the vault becomes irreplaceable.
- If someone sends you a skill, audit it with `/skill-safety-audit` before running it. Always.

## When something feels missing

Every folder has a Guide explaining what goes there and why. If the answer is not in a Guide, the architecture doc in the repo and `CLAUDE.md` at the vault root carry the reasoning. And the pack updates over time: `/foothold-update` pulls new content without touching yours.
