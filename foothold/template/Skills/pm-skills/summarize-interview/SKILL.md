---
name: summarize-interview
description: "Summarise a research interview transcript into a structured synthesis: jobs to be done, current solution, what works and what does not, satisfaction signals, key insights and dated action items. Use when processing discovery interview recordings or transcripts. Defence-aware and worked only from the raw transcript, never a tool's auto-summary."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-product-discovery/summarize-interview), MIT. Copyright (c) 2026 Pawel Huryn. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: discovery-gtm
---

# Summarise Customer Interview

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-product-discovery/summarize-interview`, MIT, copyright Pawel Huryn). MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## What this is, and is not

The synthesis partner to `interview-script`: it turns a research-interview transcript into structured discovery evidence that feeds the personas, the journey map and the value proposition. It is for research interviews, not meeting debriefs.

## Two rules that override the upstream

- **Work only from the raw transcript.** Never derive the summary or actions from any tool's auto-produced summary, outline or action list. Those tools cannot tell which engagement a remark belongs to. Read the transcript and synthesise from it, applying your own context.
- **Handling.** The transcript and summary carry the interviewee's data. Keep it within your own handling boundaries; do not route it to another channel without explicit confirmation.

## Method

1. **Read the full transcript** before summarising.
2. **Fill the template,** using "-" where information is absent and qualitative descriptions where a number is not available:

   - **Date** and time of the interview.
   - **Participants:** names and roles. Note whether each is a customer (selects) or a user (operates).
   - **Background** on the interviewee.
   - **Current solution** they use today.
   - **What works about it:** job to be done, desired outcome, importance, satisfaction.
   - **Problems with it:** job, outcome, importance, satisfaction.
   - **Key insights:** unexpected findings or notable quotes.
   - **Action items:** date, owner, action. Per action, identify which engagement or customer it belongs to, and scrub anything that belongs to a different engagement before the output goes anywhere near it.

3. **Plain language.** Write so anyone on the team can follow it.

Save as markdown.

## Notes

- Pairs with `interview-script`, `user-personas`, `customer-journey-map`.
