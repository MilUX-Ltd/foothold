# A worked example

An invented run, to show the rhythm. The business and people are made up.

**User (dictated on a phone):**

> Right, so, we do kitchens and extensions mostly, and we send out maybe forty quotes a month and honestly about half of them we just never hear back, nothing, and I don't chase because it feels pushy and my dad, he writes these really long emails that nobody reads. I want something short I can send after, I don't know, ten days? That doesn't sound desperate. And it needs to sound like us, we're a family firm.

**Skill:** So the job is a short follow-up email for customers who asked for a quote and went quiet after about ten days, friendly rather than pushy, sounding like a family firm. Will you reuse it for each quiet quote? I'd guess yes.

**User:** Yes.

**Skill:** Which AI tool will you paste the prompt into?

**User:** Claude on my phone.

**Skill:** Which model is it set to? I'd suggest checking now: in Claude it's the model name next to the send button. If you can't tell, I'll write the detailed version, which works on any model.

**User:** Not sure which model.

**Skill:** Fine, I'll write the detailed version. One question: have you got an email you were happy with that I can use as an example of your style? Paste it if so, with any customer details taken out.

**User:** Not really. Just keep it warm and short.

**Skill:** One more: is there anything it must never say? I'd suggest no discounts and no "offer ends" deadlines.

**User:** Yes, that. And don't mention prices.

**Skill:** (writes the small-model prompt from `model-scale.md`, adding "Never mention prices" to the rules, "We're a family firm" to the first line, and an example slot because she has no example yet, then:)

**What I changed and why**
- Put the job first, in one sentence (a new colleague needs to know the task before the detail).
- Added who it's for and why: quiet quotes cost you work, so it should feel easy to reply to (the reason sets the tone).
- Turned "short" into "under 120 words" and gave the shape: subject line, email, one question (smaller models need the format spelled out).
- Numbered the three things the email must do (step by step keeps a smaller model on course).
- Added your rules: no prices, no discounts, no deadlines (limits stated plainly are kept more often than limits implied).
- Added "draft for me to check" and "don't send or change anything" (anything for customers stays with you until you send it).

**Tip for next time:** talk for a minute before you type. You said more in that ramble than most people put in a page.

**Next step offered:** "If you switch to a larger model later, I can give you the short version too."
