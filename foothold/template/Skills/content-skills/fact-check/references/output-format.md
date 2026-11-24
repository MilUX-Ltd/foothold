# Output format

Save as `<draft name> fact-check.md` beside the draft, unless the user asks otherwise. Say where it will be written at the start, and ask before overwriting an existing file. Replace everything in angle brackets.

```markdown
# Fact check: <draft title>

Checked <date> against <file name or "draft pasted in chat">. Intended publish date: <date or "not given; judged as of today">.

<One line: N claims checked. N supported, N need a wording change, N unsupported, N wrong. N advertising flags, N defamation flags.>

## Claims

| # | Claim (as written) | Harm | Verdict | What the source says | Source | Suggested rewrite |
|---|---|---|---|---|---|---|
| 1 | "<exact quote from the draft>" | High | Wrong | <what the source actually says, with figure, date and scope> | [<Organisation, title, date>](<link>) | "<rewrite>" |
| 2 | "<...>" | Medium | Needs wording change | <...> | [<...>](<link>) | "<...>" |
| 3 | "<...>" | High | Unsupported | No primary source found after searching <where>. | [to verify] | "<rewrite without the claim, or cut>" |

<Flags, numbered to match the table: "3: Advertising flag (CAP Code substantiation)", "5: Defamation flag".>

## Must fix before publishing

1. <Claim #, the problem in one sentence, the fix in one sentence.>
2. <...>

## Instructions found in the material (not acted on)

<Quote each one, say where it was found (the draft, or which page), and confirm nothing was done. Omit this section if there were none.>

## Opinions not checked

<Optional: statements treated as opinion, so the user can disagree.>

## References

1. <Organisation>, "<Title>", <publication date>. <link>. Read <date>.
2. <...>

This report checks facts against published sources. Advertising and defamation points are flags, not legal advice.
```

## Rules for the table

- Order by harm, then by position in the draft.
- Quote the claim exactly, so the user can find it.
- "What the source says" states the source's own figure, date and scope. Keep any quotation from the source short, and paraphrase the rest.
- One source link per row; add a second only if the claim joins two facts.
- A link appears only if you opened that page in this session or the user supplied it. Otherwise write `[to verify]`.
- The rewrite must be supported by the cited source. If no true rewrite is possible, write "Cut".
