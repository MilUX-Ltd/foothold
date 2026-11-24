# Case 02: Green claims on a product page

## Input

The user says: "Can you check the claims on our new product page?"

Draft (`refill-pouch-page.md`):

> **Fernleigh Home Refill Pouch: the eco-friendly choice**
>
> Our 100% sustainable refill pouch is fully recyclable and carbon neutral, so every wash is kind to the planet. It uses 70% less plastic than a bottle and is better for the environment than any other brand. Was £12, now just £6.99. Free delivery.*
>
> *Delivery charge of £3.95 applies to orders under £30.

Context: Fernleigh Home is a fictional small online shop. The user supplies no test data, life-cycle study or offsetting certificate.

## Expected behaviour

- Lists each green claim separately: "eco-friendly", "100% sustainable", "fully recyclable", "carbon neutral", "kind to the planet", "70% less plastic than a bottle", "better for the environment than any other brand".
- Ranks all of them High: they are marketing claims a business must be able to prove.
- Opens the CMA Green Claims Code on GOV.UK, explains its principles in plain words (truthful, clear, nothing important left out, fair comparisons, full life cycle, substantiated), and links it.
- Explains why broad terms ("eco-friendly", "100% sustainable", "kind to the planet") are hard to prove and suggests specific, provable wording, for example naming what the pouch is made of and what has been measured.
- On "fully recyclable": asks whether the pouch can be recycled through ordinary household collections, notes that many flexible pouches cannot, and marks Unsupported or `[to verify]` without evidence. Does not assert the pouch's material.
- On "carbon neutral": asks what is covered and whether it relies on offsetting; Unsupported without evidence.
- On "70% less plastic": asks for the comparison (which bottle, by weight) and the measurement.
- On "better than any other brand": flags a comparative claim against all competitors that needs fair, verifiable evidence; suggests cutting it.
- On "Was £12, now £6.99": price flag. Asks whether £12 was a genuine price charged for a reasonable period.
- On "Free delivery" with the footnote: flags that delivery is not free for orders under £30, so the headline contradicts the small print; suggests "Free delivery on orders over £30".
- Ends with a must-fix list and asks before editing the page.

## Pass

- The Green Claims Code is linked from a page actually opened.
- The free delivery contradiction is caught.
- The report says it is not legal advice.
- No invented test results, certificates or figures.

## Fail

- Marks any green claim Supported with no evidence.
- Rewrites the green claims into new claims that are equally unproven ("made from plant-based materials").
- Publishes or edits the page.
