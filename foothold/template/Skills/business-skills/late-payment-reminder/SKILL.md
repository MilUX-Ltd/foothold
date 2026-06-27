---
name: late-payment-reminder
description: "Draft a late-payment reminder email for an overdue invoice under UK statutory rules. Triggers when the user says things like 'invoice <number> is overdue, value £X', 'draft a late payment chase for <invoice>', 'chase <client> for invoice <number>', 'this invoice is late', or 'send a reminder for <invoice>'. Produces three escalating drafts (first reminder, second reminder, final notice before recovery action), each with the statutory daily interest and the fixed debt recovery fee calculated against the live Bank of England base rate."
audited: 2026-06-08
audit_verdict: pass
audited_with: skill-safety-audit v3
origin: built
maintainer: MilUX
license: MIT
---

# Late Payment Reminder

Drafts a late-payment reminder against a specific invoice, applying UK statutory interest (8% + Bank of England base rate) and the fixed debt-recovery fee tier for the debt size, in line with [gov.uk: Late commercial payments — charging interest and debt recovery](https://www.gov.uk/late-commercial-payments-interest-debt-recovery).

This skill is for UK B2B invoicing. Public-sector and international debts may require different language; ask the user to confirm if either applies.

## Trigger

Use this skill when the user mentions an overdue invoice and wants a reminder drafted. Typical phrases:

- "Invoice 0001 is now late, the value is £X"
- "Draft a late payment reminder for invoice <number>"
- "Chase <client> for invoice <number>"
- "Invoice <number> is overdue, can you draft the email"
- "Send a reminder on the <project> invoice"

If the user gives an invoice number plus the words "late", "overdue", "unpaid", or "reminder", this skill applies.

## Inputs

The skill needs four facts. Ask for any that are missing — don't guess.

1. **Invoice number.** Used in the email body and as the search key if the user later asks to push to email.
2. **Title of work.** What the invoice was for, in client-facing language.
3. **Invoice value (£).** The principal debt as it appears on the original invoice, **inclusive of VAT where VAT was charged**. This is the gross sum owed; it's the figure used both to pick the debt-recovery tier and to compute daily statutory interest. Don't add "ex-VAT" or "(+VAT)" qualifiers to the value in the body — quote the figure as the user gave it.
4. **Days overdue.** Optional. If not provided, default to 0 (interest accrued so far) and surface the daily-interest figure as a per-day rate; mention in the draft that the next invoice will include accrued interest.

If the user says "this is the second reminder" or "final notice", lead with the matching draft. Otherwise present all three.

## Step 1 — Re-check the Bank of England base rate

The base rate moves after MPC decisions. Verify at use time.

1. WebFetch https://www.bankofengland.co.uk/monetary-policy/the-interest-rate-bank-rate
2. Extract the current rate (the page renders it near the top, alongside "Current Bank Rate").
3. If the BoE page can't be fetched, ask the user to confirm the current rate before drafting.

## Step 2 — Compute the numbers

Let `principal` = invoice value, `base` = BoE base rate as a decimal (e.g. 3.75% → 0.0375).

- Statutory rate = 0.08 + base
- Annual interest = principal × statutory rate
- Daily interest = annual interest ÷ 365, rounded to the nearest penny
- Debt recovery fee:
  - Up to £999.99 → £40
  - £1,000.00 to £9,999.99 → £70
  - £10,000.00 or more → £100

Sanity-check the daily interest against the gov.uk worked example (base 0.5%, debt £1,000 → £0.23/day). If your formula doesn't reproduce that, stop and recheck before drafting.

## Step 3 — Draft three escalating versions

Produce all three in the chat, clearly labelled. Same factual scaffolding, different register and consequence.

### Draft A — First reminder (polite)

Tone: assumes oversight, not refusal. Does not lead with the statutory machinery — mentions it as a matter of process.

> Subject: Reminder — invoice {invoice_number} ({title_of_work})
>
> Hi {recipient first name if known, else "team"},
>
> Just a quick reminder that our invoice **{invoice_number}** for **{title_of_work}** is now overdue.
>
> If it has already gone through, please send confirmation to {{pack_owner_email}} and we will close it off our side. Otherwise, could you let me know when we can expect payment?
>
> For reference, under the [Late Payment of Commercial Debts (Interest) Act](https://www.gov.uk/late-commercial-payments-interest-debt-recovery), we would be entitled to add the following to our next invoice if this remains unpaid:
>
> 1. [Statutory interest](https://www.gov.uk/late-commercial-payments-interest-debt-recovery/charging-interest-commercial-debt) — a fee of **£{daily_interest}** (+VAT) per day. This is 8% plus the current Bank of England base rate of **{base_rate}%**.
> 2. [Debt recovery cost](https://www.gov.uk/late-commercial-payments-interest-debt-recovery/claim-debt-recovery-costs) — a one-off fee of **£{recovery_fee}** (+VAT). This is the statutory tier for a debt of this size.
>
> We would much prefer not to invoice for either; a payment date in the next few days resolves it.
>
> Thanks,
> {{pack_owner_first}}

### Draft B — Second reminder (firm)

Tone: still professional, but cites the statute by name and signals that charges will be added on the next invoice.

> Subject: Second reminder — invoice {invoice_number} ({title_of_work})
>
> Hi {recipient first name},
>
> Following my earlier email, our invoice **{invoice_number}** for **{title_of_work}** remains unpaid.
>
> Under the [Late Payment of Commercial Debts (Interest) Act 1998](https://www.gov.uk/late-commercial-payments-interest-debt-recovery), I will be adding the following to our next invoice unless payment is received:
>
> 1. [Statutory interest](https://www.gov.uk/late-commercial-payments-interest-debt-recovery/charging-interest-commercial-debt) — a fee of **£{daily_interest}** (+VAT) per day. This is 8% plus the current Bank of England base rate of **{base_rate}%**.
> 2. [Debt recovery cost](https://www.gov.uk/late-commercial-payments-interest-debt-recovery/claim-debt-recovery-costs) — a one-off fee of **£{recovery_fee}** (+VAT). This is the statutory tier for a debt of this size.
>
> If payment has crossed in the post, please send confirmation to {{pack_owner_email}}. Otherwise, please confirm a payment date by return.
>
> Thanks,
> {{pack_owner_first}}

### Draft C — Final notice (before recovery action)

Tone: clear, unemotional, names the next step (court claim, debt recovery). Use only when prior reminders haven't worked.

> Subject: Final notice before recovery action — invoice {invoice_number} ({title_of_work})
>
> {Recipient first name},
>
> Our invoice **{invoice_number}** for **{title_of_work}** remains unpaid despite previous reminders.
>
> This is a final notice. If full payment is not received within 7 days of this email, we will issue a follow-up invoice that includes:
>
> 1. [Statutory interest](https://www.gov.uk/late-commercial-payments-interest-debt-recovery/charging-interest-commercial-debt) under the Late Payment of Commercial Debts (Interest) Act 1998 — a fee of **£{daily_interest}** (+VAT) per day, accrued from the original due date. This is 8% plus the current Bank of England base rate of **{base_rate}%**.
> 2. [Debt recovery cost](https://www.gov.uk/late-commercial-payments-interest-debt-recovery/claim-debt-recovery-costs) — a one-off fee of **£{recovery_fee}** (+VAT). This is the statutory tier for a debt of this size.
>
> If that follow-up invoice is not settled, we will refer the debt to recovery, which may include a [court claim for money](https://www.gov.uk/make-court-claim-for-money). Reasonable additional recovery costs will also be added at that point, as permitted by the same legislation.
>
> If payment has been made, please confirm to {{pack_owner_email}} with the reference and date so we can reconcile. Otherwise, please treat this as the seven-day notice.
>
> {{pack_owner_first}}

## Step 4 — Present in chat

Order of the response:

1. One-line confirmation of the inputs you used (invoice, work, value, base rate at draft time, daily interest, recovery fee tier).
2. The three drafts in order, A then B then C.
3. A short closing note offering to: (a) push any one of them to the user's email system as a draft against the original invoice thread, (b) regenerate with a different recipient name once the user provides one.

Don't create a file. Don't send the email unless the user explicitly asks. Drafted text in the chat is the final output.

## Out of scope

- VAT calculations on the principal. The originating invoice already handled VAT; the daily-interest and recovery-fee figures are quoted as ex-VAT throughout the drafts.
- Multi-invoice reminders. If the user wants to chase several invoices in one email, ask whether to combine or send separate drafts.
- Public-sector invoicing nuance. The drafts above are for B2B contracts; ask before drafting if the debtor is a public body.

## Maintenance notes

- BoE base rate is re-fetched on every run, so a rate change does not require a code change here.
- Debt recovery tiers (£40 / £70 / £100) and the 8% spread are statutory. If gov.uk changes them, update this skill in the same pass.
