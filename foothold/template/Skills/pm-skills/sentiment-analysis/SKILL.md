---
name: sentiment-analysis
description: "Analyse a body of user feedback at scale to surface segments, sentiment scores, jobs to be done and satisfaction patterns, with prioritised recommendations. Use when you have reviews, surveys, support tickets or social listening to synthesise. Defence-aware and handling-conscious; needs a real corpus of feedback to run on."
audited: 2026-06-13
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: forked
maintainer: MilUX
source: "phuryn/pm-skills v2.0.0 (pm-market-research/sentiment-analysis), MIT. Copyright (c) 2026 Pawel Huryn. Licence retained in this folder as LICENSE."
modified_by: "MilUX Ltd, 2026"
changes: "Adapted for defence-sector founders; MilUX proprietary framing and internal references removed for public release."
category: discovery-gtm
---

# Sentiment Analysis

Forked from [phuryn/pm-skills](https://github.com/phuryn/pm-skills) v2.0.0 (`pm-market-research/sentiment-analysis`, MIT, copyright Pawel Huryn). MIT licence text retained in `LICENSE` alongside this file. **Modified by MilUX:** adapted for defence-sector founders and reframed in plain language for public release; the original method and attribution are retained. Modifications copyright 2026 MilUX Ltd, released under the same MIT licence.

## What this is, and when it applies

Synthesis of a body of feedback into segments, sentiment and satisfaction. It needs a real corpus (reviews, surveys, support tickets, social listening) to be worth running; on a handful of comments it is a hypothesis, not a measurement.

## Method

1. **Ingest** all feedback sources; inventory what you have.
2. **Identify segments:** at least three, by behaviour and need (see `user-segmentation`), not demographics.
3. **Thematic analysis:** recurring themes, pains and positives per segment.
4. **Sentiment scoring:** an overall score (-1 to +1) per segment, with the drivers and detractors.
5. **Impact:** prioritise by frequency, severity and consequence.
6. **Synthesise** segment profiles.

## Output, per segment

Profile and size; jobs to be done; sentiment score and satisfaction (read as how well the offering fits what the segment selects on); top positive themes; top pains with quotes; product-segment fit and churn risk; two to three highest-impact recommendations.

## Notes

- Ground every finding in the feedback; cite sources; flag thin samples.
- Keep feedback data within your own handling boundaries.
- Pairs with `user-segmentation`, `user-personas`, `customer-journey-map`.
