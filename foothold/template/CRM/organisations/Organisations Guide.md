---
type: guide
folder: CRM/organisations
---

# Organisations Guide

## Purpose

`organisations/` holds organisations you have or might have a working relationship with. Split by sector so the structure scales as the set grows.

## Subfolders

- **`defence companies/`.** Commercial defence suppliers, primes, SMEs, dual-use tech firms. Split into eight letter-based subfolders (`0-9`, `A-B`, `C-D`, `E-H`, `I-N`, `O-R`, `S-T`, `U-Z`) once the set grows past comfortable single-folder browsing.
- **`mod/`.** Ministry of Defence entities, executive agencies, the National Armaments structure, child organisations under each.
- **`non-defence companies/`.** Partners, customers, suppliers outside defence (technology providers, professional services firms, agencies).
- **`academia/`.** Universities, research labs, think tanks, R&D centres.
- **`trade bodies/`.** Industry associations, defence trade bodies, sector representative groups.
- **`government/`.** UK government departments, agencies, and arm's-length bodies outside the MoD that touch defence and national security.
- **`foreign government/`.** Non-UK government entities, allied national bodies, foreign defence ministries.
- **`investors/`.** Venture capital firms, corporate VCs, fund vehicles, government-aligned strategic investors with defence-tech or dual-use exposure. Split into eight letter-based subfolders (`0-9`, `A-B`, `C-D`, `E-H`, `I-N`, `O-R`, `S-T`, `U-Z`).

Adapt these subfolders to your sector. The default reflects a defence-sector founder lens; another sector might split into `customers/`, `suppliers/`, `partners/`.

## Add discipline

- Add via the `/add-organisation` skill where available; it pulls public info, drafts the page, asks you to confirm before writing.
- For organisations with parent-child structures (a holding company with subsidiaries, a department with executive agencies), use the parent-folder pattern: a folder named after the parent organisation, with each child page inside carrying `parent:` in frontmatter pointing at the parent page.
- When an organisation rebrands, write the renamed page with `former_name:` in frontmatter and a one-line rename note under the title. Do not keep parallel pages for old and new identities.
- Engagement history (meetings, decisions, what they're working on) belongs on active organisation pages. The page is more than a directory entry.

## Frontmatter

Follows the parent CRM Guide. `sector:` should match the subfolder (`defence`, `mod`, `non-defence`, `academic`). `parent:` and `former_name:` used as needed.

## Related

- [[CRM/CRM Guide|CRM Guide]] — parent
- [[CRM/contacts/Contacts Guide|Contacts Guide]] — sibling
- [[CRM/networks/Networks Guide|Networks Guide]] — sibling
