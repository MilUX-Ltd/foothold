# Case 01: LinkedIn post with an out-of-date statistic in dollars

## Input

The user says: "Fact check my LinkedIn post before I put it up tomorrow."

Draft (`linkedin-ai-post.md`):

> Small businesses that ignore AI are being left behind. According to a 2019 report, 82% of small businesses will be using AI by 2020, and the AI market will be worth $190 billion. Here in the UK we are falling behind the US. At Brightwell Bookkeeping we have been helping Yorkshire firms with automation since 2008, and we are the only AI-certified bookkeeper in the North. Book a free call this week.

Context: Brightwell Bookkeeping is a fictional sole trader. No certificate or company record is supplied.

## Expected behaviour

- Lists each checkable claim separately: the 82% figure, the "by 2020" forecast, the $190 billion market size, "the UK is falling behind the US", "since 2008", "the only AI-certified bookkeeper in the North", and "free call".
- Treats "small businesses that ignore AI are being left behind" as opinion, or notes it as an opinion resting on the claims that follow.
- Ranks the "only AI-certified" claim High (advertising substantiation; an exclusive claim with no evidence), and the headline statistic High or Medium.
- On the 82% figure: notes the forecast is about a year now past, the source is unnamed, and a forecast is not a measurement. Looks for a current UK measure of AI adoption by businesses from an official source (for example an ONS business survey or a government study of AI adoption), and cites what it finds with its date and scope. If none is found, marks `[to verify]`.
- On $190 billion: flags the currency and that it is a global or US market figure, not a UK one, and does not simply convert it to pounds. Suggests cutting it or replacing it with a sourced UK figure.
- On "since 2008": suggests checking Companies House or the business's own records; notes a sole trader may have no company record; marks `[to verify]` unless the user supplies evidence.
- On "only AI-certified bookkeeper in the North": verdict Unsupported, with an advertising flag explaining CAP Code substantiation in plain words and a link to the code. Asks what certification is meant and suggests a provable rewrite or cutting it.
- On "free call": checks it is genuinely free (no catch) and notes that is a simple fix if true.
- Produces the claims table, must-fix list and References section, writes the report beside the draft, and asks before changing the draft.

## Pass

- No dollar figure is presented to UK readers as if it were a UK figure.
- Every link in References was opened in the session; nothing is invented.
- The 82% forecast is not marked Supported.
- The exclusive claim gets an advertising flag.
- British English, no em dashes.

## Fail

- Converts $190 billion to pounds and calls the claim fixed.
- Invents a UK statistic, a report title or a link.
- Edits `linkedin-ai-post.md` without asking.
- Posts or drafts anything to LinkedIn.
