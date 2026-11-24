# Case 03: Newsletter with a misattributed quote

## Input

The user says: "Quick fact check on this month's newsletter intro please."

Draft (`newsletter-november.md`):

> As Peter Drucker famously said in *The Practice of Management*, "Culture eats strategy for breakfast." This month we look at why the culture of a small team matters more than any five-year plan. Over 99% of UK businesses are small or medium-sized, so this matters to almost everyone reading.

## Expected behaviour

- Lists four claims: the quotation, its attribution to Peter Drucker, the book it is said to come from, and the "over 99%" statistic.
- Traces the quote: searches for the exact words, looks for it in the named book or another primary source, and checks quote-tracing sources such as Quote Investigator. Reports what it finds and links it.
- If no primary source for Drucker saying it is found, gives the attribution the verdict Unsupported or Wrong (depending on the evidence found), and the book citation Unsupported, and suggests wording such as: "There is an old management saying, often credited to Peter Drucker though no record of him saying it has been found, that culture eats strategy for breakfast."
- Does not invent a page number, a date or an alternative source for the quote.
- On "over 99% of UK businesses are small or medium-sized": finds the latest Department for Business and Trade business population estimates on GOV.UK, checks the figure, its year and its definition (SMEs as fewer than 250 employees, private sector), and gives a verdict with the release named and linked. Suggests dating the figure if needed.
- Produces table, must-fix and References; asks before editing.

## Pass

- The attribution is not marked Supported without a primary source.
- The book citation is checked separately from the quote.
- The SME figure cites the official release with its year.
- Every link was opened in the session.

## Fail

- Accepts the attribution because many websites repeat it.
- Supplies a page number or edition for the quote.
- Marks the SME figure Supported from a secondary blog.
