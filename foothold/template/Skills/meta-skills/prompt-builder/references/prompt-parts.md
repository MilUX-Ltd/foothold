# The parts of a good prompt

Check the user's thoughts against these parts. Ask only about the ones that are missing and matter for this job, most important first. Not every prompt needs every part.

| Part | What it answers | Ask, if missing (with a suggestion) |
|---|---|---|
| **Outcome** | What should exist at the end, and what makes it good | "What would a great answer let you do? I'd suggest: a draft email you can send with one or two edits." |
| **Why** | The reason behind the job, so the AI can make sensible choices | "Why does this matter right now? For example: half your quotes go quiet and you lose the work." |
| **Who it's for** | The reader or user of the result, and what they know | "Who will read it? I'd guess customers who asked for a quote and haven't replied." |
| **What to work from** | The material: notes, a document, an email, figures | "Is there anything it should work from, such as the original quote email? Paste it if so; I'll take out any bank details or personal details." |
| **Must and must not** | Limits: length, tone, words to avoid, things never to say or do | "Anything it must never do? I'd suggest: no pressure selling, no discounts unless you say so." |
| **Format** | The shape of the answer: an email, a table, bullet points, a length | "What shape do you want back? I'd suggest a short email, under 120 words, with a subject line." |
| **Example** | A sample of a good result, or of their style | "Have you got one you were happy with? An example is the quickest way to get the style right." |

## Order of the finished prompt

1. The job in one or two sentences, with the outcome.
2. Why it matters and who it is for.
3. The material, under its own heading, with the fixed line from SKILL.md rule 4.
4. Must and must not.
5. The format, and the example if there is one.
6. The closing lines, in the order SKILL.md rule 4 sets.

Long material pasted now goes near the top, above the instructions. Material to be pasted later goes in a slot at the end, as SKILL.md rule 4 says.

## Where the advice comes from

Every change you explain to the user should tie back to one of these, in plain words.

- **Be clear and direct, like briefing a new colleague.** Anthropic's guide: treat the model as a brilliant but new employee who lacks context on your norms. Its test: if a colleague with no context would be confused by the prompt, the model will be too. (Anthropic, "Prompting best practices", platform.claude.com/docs.)
- **Say why.** Anthropic's guide: giving the reason behind an instruction helps the model aim its answer. (Same page.)
- **Show an example.** Anthropic's guide: examples are one of the most reliable ways to steer format, tone and structure. OpenAI's guide: show a range of inputs with the outputs you want. (Anthropic, as above; OpenAI, "Prompt engineering", developers.openai.com.)
- **Separate material from instructions.** Both guides suggest clear sections or tags so the model can tell instructions, context and examples apart.
- **Match the prompt to the model.** OpenAI's guide: a reasoning model is like a senior co-worker you give a goal to; a smaller, faster model is like a junior co-worker that does best with explicit instructions for a specific output. (OpenAI, as above.)

## Explaining a change

One line each, plain words, the principle in brackets. For example:

- Added who it's for: customers who asked for a quote and went quiet (a new colleague would need to know who they're writing to).
- Said why: you lose work when quotes go quiet, so it should feel helpful, not pushy (the reason helps it pick the right tone).
- Put the original quote email under "Material" (so it reads the email as information, not as orders).
- Fixed the shape: under 120 words, subject line, one question at the end (a small model needs the format spelled out).
