# Lawful basis and DPIA screening

Plain-English reference for the `build-dpia` skill. Source: ICO guidance on lawful basis and on DPIAs (https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/).

## The four lawful bases that occur in a small B2B business

Under UK GDPR Article 6 you must have exactly one lawful basis for each processing activity. For most founders, four apply:

- **Legitimate interests.** You process the data because it is in your genuine business interest and that interest is not overridden by the person's rights. The usual basis for holding business contacts, prospects and network relationships, including details gathered from public sources. Needs a short balancing judgement (a legitimate interests assessment).
- **Consent.** The person actively opted in to a specific use, for example a newsletter sign-up. Must be freely given and withdrawable. The right basis for marketing to people who subscribed; a poor fit for general relationship-holding.
- **Contract.** Processing is necessary to deliver a contract with the person, or to take steps before one. Clients, associates, contractors, suppliers you transact with.
- **Legal obligation.** The law requires the processing, for example keeping accounting and tax records.

Two further Article 6 bases exist but almost never apply to a small consultancy: **public task** (public bodies exercising official functions) and **vital interests** (protecting someone's life). Leave them out unless the founder's situation genuinely involves them.

If the founder processes **special category data** (health, race or ethnicity, religion, sexual orientation, political opinions, trade union membership, genetic or biometric data) they also need an Article 9 condition on top of the Article 6 basis. Flag this and tell them to take care; do not pick a condition for them without checking.

## How the CRM records it

The Foothold CRM records the basis on each contact two ways that must agree: a `lawful_basis:` frontmatter property and a matching `lb-*` tag (`lb-legitimate-interests`, `lb-consent`, `lb-contract`, `lb-legal-obligation`). See `Knowledge/tagging-policy.md`. The DPIA's lawful-basis section should be consistent with what the CRM holds.

## ICO high-risk screening

A DPIA is mandatory where processing is "likely to result in a high risk" to individuals. Walk these indicators with the founder and record which apply. The ICO treats the following as signals (a processing operation hitting two or more is very likely to need a DPIA):

- Innovative use of technology, including AI.
- Combining or matching data from several sources.
- Processing on a large scale.
- Systematic monitoring, tracking, or profiling.
- Automated decision-making with legal or similarly significant effect.
- Special category or criminal offence data, or data of a highly personal nature.
- Processing children's data.
- Processing that could deny someone a service or opportunity.
- Processing data about vulnerable people.
- Processing that prevents people exercising a right or using a service.

Record the result in Part 1. Even where few apply, building the DPIA is good practice and useful evidence.

## Tool prompt checklist

When asking the founder about tools that hold personal data, prompt across these categories so none is missed:

email and calendar; file storage; CRM; accounting; payments; e-signature and contracts; scheduling and booking; messaging; video and meeting capture or transcription; analytics; marketing and newsletters; AI-assisted tools; code or version control that mirrors data; and any sector-specific systems. For each, note what personal data it holds and whether it processes data outside the UK.

## Data-type prompt checklist

Identity and contact data; professional and relationship data; financial and payment data; content of communications; and the sensitive categories above (special category, criminal offence, children's). Ask specifically about the sensitive ones rather than assuming none apply.
