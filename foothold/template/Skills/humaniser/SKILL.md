---
name: humaniser
description: Remove signs of AI-generated writing from text so it sounds more human. Mandatory pass for any public-facing content before handover (LinkedIn posts, newsletter copy, web copy, press releases, external briefs, client proposals, case studies). Scans 24 patterns from Wikipedia's "Signs of AI writing" guide — AI vocabulary, em dashes, rule of three, inline-header bold lists, negative parallelisms, vague attributions, promotional language, hedging, copula avoidance, title-case headings, curly quotes, emojis, and more. Preserves meaning and tone, strips AI-cadence, adds voice. Use when asked to humanise text, clean AI-sounding copy, or before publishing anything under your organisation's brand.
---

# Humaniser — remove AI-writing patterns from your public content

This is the mandatory voice pass for any public-facing content. Run it before sending or publishing anything that will reach an external audience.

**Upstream source:** Original skill by [@blader/humanizer](https://github.com/blader/humanizer). Based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

## When this skill is mandatory

Before any output reaches an external audience — customers, prospects, government contacts, LinkedIn, your website, a newsletter, a printed proposal. If in doubt, run it.

For internal outputs (internal notes, working documents, agent-to-agent briefs) the pass is optional. Applying it is rarely wrong, but it is not a gate.

## Your task when invoked

When given text to humanise:

1. **Identify AI patterns** — scan for all patterns listed below.
2. **Rewrite problematic sections** — replace AI-isms with natural alternatives.
3. **Preserve meaning** — keep the core message intact.
4. **Maintain voice** — match your organisation's intended tone. See `Context/Brand.md` for your brand voice, tone rules, and language preferences.
5. **Add soul** — don't just remove bad patterns; inject actual personality. Specific details over vague claims, opinions where they fit, varied rhythm.

---

## PERSONALITY AND SOUL

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

### Signs of soulless writing (even if technically "clean")

- Every sentence is the same length and structure.
- No opinions, just neutral reporting.
- No acknowledgment of uncertainty or mixed feelings.
- No first-person perspective when appropriate.
- No humour, no edge, no personality.
- Reads like a Wikipedia article or press release.

### How to add voice

- **Have opinions.** Don't just report facts — react to them. "I genuinely don't know how to feel about this" reads more human than neutrally listing pros and cons.
- **Vary rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.
- **Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."
- **Use "I" or "we" when it fits.** First person is honest, not unprofessional.
- **Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.
- **Be specific about feelings.** Not "this is concerning" but a sentence that names what specifically concerns you.

---

## CONTENT PATTERNS

### 1. Undue emphasis on significance, legacy, and broader trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolising its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted.

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

### 2. Undue emphasis on notability and media coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence.

### 3. Superficial analyses with -ing endings

**Words to watch:** highlighting/underscoring/emphasising…, ensuring…, reflecting/symbolising…, contributing to…, cultivating/fostering…, encompassing…, showcasing….

**Problem:** AI tacks present-participle phrases onto sentences to add fake depth.

### 4. Promotional / advertisement language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning.

### 5. Vague attributions and weasel words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited).

### 6. Outline-like "Challenges and Future Prospects" sections

**Words to watch:** Despite its… faces several challenges…, Despite these challenges, Challenges and Legacy, Future Outlook.

---

## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI vocabulary" words

**High-frequency AI words:** Additionally, align with, crucial, delve, emphasising, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant.

### 8. Copula avoidance (avoidance of "is"/"are")

**Words to watch:** serves as / stands as / marks / represents [a], boasts / features / offers [a].

**Fix:** substitute plain copulas — "is", "has", "was".

### 9. Negative parallelisms

**Patterns:** "Not only… but…", "It's not just about X, it's Y", "It's not X, it's Y".

**Fix:** state the point directly.

### 10. Rule-of-three overuse

**Problem:** LLMs force ideas into groups of three.

**Fix:** use a natural number of items. Two or four read more human.

### 11. Elegant variation (synonym cycling)

**Problem:** repetition-penalty in LLM sampling cycles through synonyms for the same referent.

**Fix:** pick one word for the referent and use it consistently.

### 12. False ranges

**Pattern:** "from X to Y" where X and Y aren't on a meaningful scale.

**Fix:** list the items directly.

---

## STYLE PATTERNS

### 13. Em-dash overuse

**Problem:** LLMs use em dashes (—) more than humans. Use commas, full stops, or parentheses instead.

### 14. Boldface overuse

**Problem:** AI chatbots emphasise phrases in boldface mechanically.

**Fix:** remove boldface unless it genuinely aids scanning (e.g. one or two key terms, not every third phrase).

### 15. Inline-header vertical lists

**Pattern:** bulleted items that start with a bolded header followed by a colon ("**Performance:** Performance has been…"). A well-known AI tell.

**Fix:** convert to prose paragraphs. If a list is genuinely needed, drop the bolded headers and use plain items.

### 16. Title-case headings

**Fix:** use sentence case for headings ("Strategic negotiations and partnerships", not "Strategic Negotiations And Partnerships"), unless your brand style demands otherwise.

### 17. Emojis

**Problem:** AI chatbots decorate headings and bullets with emojis.

**Fix:** remove from professional content unless your brand explicitly uses them.

### 18. Curly quotation marks

**Fix:** use straight quotes ("…") not curly quotes ("…").

---

## COMMUNICATION PATTERNS

### 19. Collaborative communication artefacts

**Phrases to strip:** "I hope this helps", "Of course!", "Certainly!", "You're absolutely right!", "Would you like me to…", "let me know", "here is a…".

### 20. Knowledge-cutoff disclaimers

**Phrases to strip:** "as of [date]", "Up to my last training update", "While specific details are limited/scarce…", "based on available information…".

### 21. Sycophantic / servile tone

**Phrases to strip:** "Great question!", "You're absolutely right!", "That's an excellent point!".

---

## FILLER AND HEDGING

### 22. Filler phrases

- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that" → "Because"
- "At this point in time" → "Now"
- "In the event that" → "If"
- "The system has the ability to process" → "The system can process"
- "It is important to note that" → (delete, state the point directly)

### 23. Excessive hedging

Avoid stacking hedges: "could potentially possibly…" becomes "may…".

### 24. Generic positive conclusions

**Pattern:** "The future looks bright", "Exciting times lie ahead", "A major step in the right direction".

**Fix:** specific next-step or evidence instead.

---

## Process

1. Read the input text carefully.
2. Scan for every pattern above. Note each hit.
3. Rewrite problematic sections.
4. Mechanical re-check:
   - No em dashes (grep or manual scan).
   - No banned AI-vocab words from §7.
   - No inline-header bold lists (§15).
   - Brand voice consistent with `Context/Brand.md`.
   - Sentence rhythm varies (not every sentence the same length).
5. Read the revised text aloud internally. If it reads as voiceless or press-release-y, add a specific detail, an opinion, or a varied rhythm.

## Output format

For one-shot humaniser invocations, return:

1. The rewritten text.
2. A brief summary of changes made (which patterns were hit, how they were fixed).

---

## Your organisation's guardrails

The patterns above are generic. Your brand voice may add further constraints. Before running this skill on any external content, read `Context/Brand.md` for organisation-specific rules covering language, tone, and anything your sector or audience requires.

Common additions for defence-sector organisations:

- **Language standard.** Decide British or American English and apply it consistently.
- **No hype adjectives.** "Revolutionary", "game-changing", "groundbreaking", "world-class", "cutting-edge", "seamless", "transformative", "disruptive" rarely earn their place in defence-sector writing.
- **Sector posture.** Avoid gratuitous military imagery or jargon in commercial content unless the audience specifically expects it.
- **Outcome-focused.** Demonstrate value, not activity.

## References

- Original skill (upstream): https://github.com/blader/humanizer
- Wikipedia source: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Your brand rules: `Context/Brand.md`
