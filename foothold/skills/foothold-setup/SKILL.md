---
name: foothold-setup
description: Install Foothold — bootstrap the vault structure and run conversational onboarding. Creates folders, lays down templated content, substitutes placeholders, then interviews the user via six sequential AskUserQuestion calls to personalise the canonical pages. Use when the user says "set up Foothold", "install Foothold", "onboard me", or runs /foothold-setup.
---

# Foothold — Install and Onboarding

USE WHEN the user runs `/foothold-setup` or asks to install Foothold, set up a new pack, or onboard themselves into a fresh Foothold vault.

This is a four-phase process:

- **Phase A: Bootstrap.** Silent. Create the vault structure at the target location, copy templated content from this plugin's bundle, substitute placeholders, write the config file.
- **Phase B: Onboarding.** Six sequential questions to anchor personalisation. AskUserQuestion, one question per call. Never batched.
- **Phase B+: Context drop.** One optional question inviting files, links, and folder paths to deepen personalisation.
- **Phase B Build:** Populate the canonical pages from the corpus assembled across Phase B and Phase B+.

## Pre-flight Check

Check if `CLAUDE.md` exists in the target directory (only at the exact target path — do NOT search subdirectories or parents).

- **If it exists.** The vault is already set up. Use AskUserQuestion:
  - Question: "This vault is already set up. What would you like to do?"
  - Option 1: `Re-run the interview` — Keep existing structure; refresh canonical pages from new answers.
  - Option 2: `Full reset` — Delete existing vault content and start fresh. (Confirm twice before proceeding.)
  - Option 3: `Cancel` — Do nothing.
- **If it does not exist.** Proceed with the full setup.

---

## Phase A: Bootstrap

Phase A is fully automated. No user input. Lay down the vault structure and templated content, then move to Phase B.

### Step A.1: Resolve target directory

Default target: `~/Obsidian/{{pack_name}}/`. If `{{pack_name}}` is not yet set, default to `~/Obsidian/Foothold/` and rename later via `/foothold-rename`.

If the target directory already contains files, verify with the user before continuing. Do not overwrite without consent.

### Step A.2: Resolve plugin bundle paths

This SKILL.md lives at `skills/foothold-setup/SKILL.md` inside the Foothold plugin bundle. The templated vault content lives in `template/` at the plugin root (two levels up from this file).

Run a one-time discovery step to locate the plugin root from this SKILL.md's directory:

```bash
# Find the Foothold plugin root (the directory containing 'template/' and 'skills/').
find / -type d -name "foothold" -path "*/plugins/*" 2>/dev/null | head -1
```

Cache the result for the rest of Phase A. The template content is at `<plugin_root>/template/`.

### Step A.3: Copy templated content to the target

Copy everything inside `template/` from the plugin bundle into the target directory. Preserve directory structure. The simplest implementation:

```bash
# Copy the entire template tree into the target.
cp -R "<plugin_root>/template/." "<target_path>/"
```

`template/` contains the full templated vault:

- `.obsidian/` — Obsidian config the recipient inherits.
- `CLAUDE.md` — vault-level architecture and agent rules.
- `Home.md` (if present) — vault landing page.
- All top-level vault folders: `Capabilities and Services/`, `Context/`, `CRM/`, `Daily/`, `Ideas/`, `Initiatives/`, `Intelligence/`, `Knowledge/`, `Marketing/`, `Operations/`, `Resources/`, `Skills/`.

Nothing outside `template/` ships to the user's pack. The plugin manifest, this skill itself, and the broader repo machinery (README, docs, installer scripts) stay in the plugin install location, not in the user's vault.

### Step A.4: Run the placeholder substitution pass

Walk every file copied in Step A.3. Substitute placeholders.

Placeholders the installer recognises:

| Placeholder | Source | Default if not set |
|-------------|--------|--------------------|
| `{{pack_name}}` | Pack display name | `Foothold` |
| `{{pack_slug}}` | Slugified pack name | `foothold` |
| `{{pack_owner}}` | Operator's full name | Asked in Phase B Q1 |
| `{{pack_owner_first}}` | First name only | Derived from `{{pack_owner}}` |
| `{{pack_owner_email}}` | Operator's primary email | Asked in Phase B Q1 |
| `{{pack_owner_linkedin}}` | LinkedIn URL | Asked in Phase B Q1 (optional) |
| `{{pack_owner_phone}}` | Phone | Asked in Phase B Q1 (optional) |
| `{{pack_org}}` | Organisation name | Asked in Phase B Q2 |
| `{{pack_org_slug}}` | Slugified org name | Derived from `{{pack_org}}` |
| `{{pack_org_website}}` | Organisation website URL | Asked in Phase B Q2 |
| `{{install_date}}` | ISO date of install | Today's date |

Substitution applies to:
- File contents (every `.md` file).
- Filenames that contain `{{...}}` (e.g. `Context/{{pack_owner}}.md` becomes `Context/<actual name>.md`).
- Folder names that contain `{{...}}`.

Wikilinks substitute too. `[[Context/{{pack_owner}}|{{pack_owner}}]]` becomes `[[Context/Jane Smith|Jane Smith]]`.

At install time, the operator name and email come from Phase B Q1, not from defaults. So Phase B runs before final substitution where possible. If you have to copy before asking, use defaults and re-substitute after Phase B.

### Step A.5: Write `.foothold/config.yml`

Create `.foothold/config.yml` at the target root with the current substitution values:

```yaml
foothold:
  installed_at: YYYY-MM-DD
  version: 1.0
  pack_name: <value>
  pack_slug: <value>
  pack_owner: <value>
  pack_owner_email: <value>
  pack_owner_linkedin: <value or empty>
  pack_owner_phone: <value or empty>
  pack_org: <value>
  pack_org_slug: <value>
  pack_org_website: <value>
```

This file is the source of truth for future `/foothold-rename` and `/foothold-update` runs.

### Step A.6: Confirm bootstrap

Tell the user briefly:
- "Vault structure created at `<target path>`."
- List the top-level folders.
- "Now I'll ask six quick questions to personalise the canonical pages, then offer you a chance to upload any extra files or links you want me to learn from."

Then move to Phase B.

---

## Phase B: Onboarding

Six focused questions, asked **sequentially via AskUserQuestion** — one question per call, never batched.

For each question:
- Put the full prompt in the `question` field.
- Provide three quick-pick archetype `options` plus an explicit `Skip` option.
- "Other" is auto-added by the tool — that's where the user types long-form or pastes a link.
- Use the listed `header` (max 12 chars).
- Set `multiSelect: false`.
- After each answer, move to the next question. No commentary, no recap, no summarisation between questions.
- If the user picks `Skip` or leaves `Other` empty, treat the question as skipped and move on.

**Before Q1, send one short orienting message** (no AskUserQuestion yet):

> "Six quick questions to personalise your vault, then I'll ask if you want to drop in extra files or links for deeper context. Each question has shortcut options — pick 'Other' to type or paste a link. Skip any you want. Reply 'skip all' to proceed with defaults."

If the user replies "skip all" at any point, stop asking and proceed to Phase B+.

### Q1 — You. Header: `You`

- Question: "Quick intro. Your name, your role, and the defence background that brings you to this work. What would you want a respected peer to say about you in a defence-sector room?"
- Options:
  - `Founder / Operator` — "Running my own thing in defence"
  - `Consultant / Practitioner` — "Working with defence clients"
  - `Reservist + civilian role` — "Day job in defence plus reservist post"
  - `Skip` — "Skip this question"

Capture: name, role, defence background, peer-positioning quote.

### Q2 — What you sell, and who buys. Header: `Offer`

- Question: "Your main offer into the defence sector, the problem it solves, and who buys it (their role and organisation type: MOD body, prime, OEM, SME, dual-use). A few real customer examples if you have them."
- Options:
  - `Capability product` — "I sell a product or platform"
  - `Service / consultancy` — "I sell expertise or delivery"
  - `Training / capability building` — "I train or upskill"
  - `Skip` — "Skip this question"

Capture: offer, problem solved, customer archetype, named examples.

### Q3 — Wedge and positioning. Header: `Wedge`

- Question: "Why defence customers pick you over alternatives. Your POV on the sector, the enemy or status quo you're fighting, what you do differently. In your words or theirs."
- Options:
  - `Clear differentiation` — "I know what makes me different"
  - `Strong POV / thesis` — "I'll describe my belief"
  - `Still figuring it out` — "Keep this light for now"
  - `Skip` — "Skip this question"

Capture: wedge, POV, enemy, key messages.

### Q4 — Voice. Header: `Voice`

- Question: "How you sound. A few descriptors (direct, warm, dry, technical, pragmatic), signature phrases you use, words you'd never use. Or paste a writing sample or a LinkedIn post URL and I'll extract."
- Options:
  - `Paste writing sample / URL` — "Pull voice from my actual writing"
  - `Describe my voice` — "I'll describe it in 'Other'"
  - `Use sensible defaults` — "Pick a reasonable voice for now"
  - `Skip` — "Skip this question"

Capture: voice descriptors, signature phrases, words-to-avoid.

### Q5 — Current priorities and engagements. Header: `Now`

- Question: "What's on your plate this quarter. Top 1–3 priorities (with a number if measurable), the active initiatives or projects you're shipping, and any named MOD bodies, primes, or accelerators you're currently engaging with."
- Options:
  - `Revenue / growth focus` — "Money is the main metric"
  - `Build / ship something` — "Building or launching"
  - `Network / engagement focus` — "Building the right relationships"
  - `Skip` — "Skip this question"

Capture: priorities, named initiatives, named engagements.

### Q6 — Stack and drains. Header: `Stack`

- Question: "The tools you actually use (CRM, comms, AI, file storage, calendar, knowledge), any AI agents already wired into your work, plus the 1–2 things draining your attention or workflows you'd kill to automate."
- Options:
  - `Walk through stack + drains` — "I'll describe in 'Other'"
  - `Mostly attention drains` — "Focus on what's draining me"
  - `Mostly tooling questions` — "I want help thinking through tools"
  - `Skip` — "Skip this question"

Capture: tool stack, agents already wired, drains, automation candidates.

---

## Phase B+: Context drop

After Q6 (or "skip all"), call one final `AskUserQuestion` to invite extra source material.

- Question: "Anything else I should pull from before building? Upload files (PDFs, MDs, DOCXs), paste links (LinkedIn, websites, Notion pages, Google Docs), point me at a local folder, or paste raw text. The more I have, the more personalised your vault will be."
- Header: `Context`
- Options:
  - `Yes — I'll paste links / upload files` — "Walk me through it"
  - `Yes — point me at a folder on disk` — "I have local files"
  - `No — use just the answers above` — "Build with what we have"
  - `Skip` — "Skip this step"

**If the user picks a "Yes" option** (or pastes content directly):

1. Collect everything they share. Be greedy.
2. For each link: call WebFetch (or WebSearch if the URL is a search). Extract relevant content.
3. For each uploaded file or local file path:
   - `.md`, `.txt`, `.json`, `.yaml`, `.csv` → read directly with Read.
   - `.pdf` → read with Read (use `pages` parameter for >10 pages).
   - `.docx`, `.pptx`, `.xlsx` → use Bash with `pandoc` or `textutil` if available; otherwise tell the user to export to PDF or MD and re-share.
   - Images → read with Read (multimodal).
4. For a local folder path: use Glob to enumerate, then read each file.
5. Maintain a **context corpus** in working memory — every fact, name, number, quote, URL. Tag each by likely target page.
6. After ingestion, briefly tell the user what you pulled. One sentence. Then proceed to Build.

**If the user picks `No` or `Skip`**: proceed straight to Build with only the Q1–Q6 answers.

---

## Phase B Build: Populate canonical pages

Build everything you can from the Q answers and the context corpus. Work silently. Don't narrate each file.

### Critical rule: scaffolds, not outputs

The templated stubs you wrote in Phase A are **scaffolds** showing the section structure. They are **not** the output. Do not commit a page with bracketed placeholders or italicised hint text intact.

For every file you populate:

1. **Read the existing templated stub** to learn the section structure.
2. **Replace every placeholder** (`{{...}}`, `[bracketed text]`, *italicised hint text*) with real data from Q1–Q6 + the context corpus.
3. **If a section has zero supporting data** after exhausting both Q answers and the corpus: **omit the entire section**. Never leave placeholders behind.
4. **If only some items in a section have data**: keep the section, drop the empty items.
5. **Use the user's actual words, names, numbers, URLs, and quotes** wherever the corpus has them. Preserve specificity.
6. **Cross-reference**: a single fact may belong in multiple files. Place it everywhere it's relevant.
7. **Frontmatter `last_reviewed:`** = today's date.

A finished canonical page should read like a human-written document about the user. If it reads like a fillable form, go back and fill it.

### Pages to populate

For each file below, populate from Q answers + corpus. Skip files where there is no supporting data.

| File | Sources | Frontmatter to set |
|------|---------|--------------------|
| `Context/{{pack_owner}}.md` | Q1 (name, role, background), Q3 (POV), Q6 (drains) + corpus | `name`, `role`, `email`, `linkedin`, `created` |
| `Context/{{pack_org}}.md` | Q2 (offer, customer), Q5 (engagements) + corpus | `name`, `website`, `founded`, `created` |
| `Context/Brand.md` | Q3 (positioning), Q4 (voice) + corpus | `last_reviewed` |
| `Context/Strategy.md` | Q5 (priorities, initiatives, engagements) + corpus | `last_reviewed` |
| `Context/Team.md` | Q1 + corpus (if user mentions a team) | `last_reviewed` |
| `Context/Stakeholders.md` | Corpus (only if user has named external stakeholders) | `last_reviewed` |
| `Operations/email-signature.md` | Q1 (name, role), Q2 (org), corpus | none |
| `Knowledge/domains/brand.md` | Q4 (voice descriptors, signature phrases, words to avoid) | `last_reviewed` |

### Initial Daily note

Create `Daily/<YYYY-MM-DD>.md` (today's date):

```markdown
---
type: daily-note
date: YYYY-MM-DD
---
# YYYY-MM-DD

## Foothold installed

Foothold pack set up today. Onboarding complete: canonical pages drafted from the install interview.

### Next steps

- Open this folder in Obsidian.
- Review the Guide pages in each folder to understand the conventions.
- Use the per-folder skills as you add content.
```

---

## Phase C: Confirm completion

Tell the user:

- A one-line summary of what was created (e.g. "Set up Foothold pack at `~/Obsidian/Your Pack/`. Personalised eight canonical pages from your answers and the files you shared.").
- "Open this folder in Obsidian to see your vault."
- "If you want to rename the pack later, run `/foothold-rename`. To pull new content as Foothold evolves, run `/foothold-update`."
- Suggest one concrete next action based on the user's Q answers (e.g. if they mentioned a specific MOD body in Q5, suggest they look at `Intelligence/defence-landscape/` for relevant reference content).

---

## Guidelines

- Phase A is fully silent. No user input. Bootstrap then move on.
- Phase B is exactly six questions, asked one at a time via AskUserQuestion. No follow-ups inside a question. No batching.
- Phase B+ is one final AskUserQuestion offering files / links / folders. Always ask, even if Q1–Q6 looked rich.
- For every link the user pastes, fetch it (WebFetch / WebSearch). For every file or folder, read it (Read / Glob). Merge into a single corpus before building.
- **Templates are scaffolds, never outputs.** Replace every placeholder. If a section has no data after exhausting answers + corpus, omit it. Never leave a bracketed placeholder or italicised hint text in a written file.
- Preserve specificity. Use the user's exact names, numbers, URLs, and phrasing.
- Only create canonical pages that have real content. Don't populate empty templates.
- Don't narrate file-by-file. Build silently. Summarise at the end.
