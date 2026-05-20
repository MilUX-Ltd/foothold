---
name: foothold-setup
description: Install Foothold — bootstrap the vault structure and run conversational onboarding. Fetches the latest template directly from the public Foothold GitHub repo, creates folders at the user's chosen path, substitutes placeholders, then interviews the user via six sequential AskUserQuestion calls to personalise the canonical pages. Use when the user says "set up Foothold", "install Foothold", "onboard me", or runs /foothold-setup. Does NOT require terminal access.
---

# Foothold — Install and Onboarding (GitHub fetch)

USE WHEN the user runs `/foothold-setup` or asks to install Foothold, set up a new pack, or onboard themselves into a fresh Foothold vault.

This skill fetches directly from the public GitHub repo at `MilUX-Ltd/foothold`. It does not rely on the local plugin install's template directory, so installs are always against the latest published content.

Four-phase process:

- **Phase A: Bootstrap.** Silent. Resolve target path, fetch the template tree from GitHub, substitute placeholders, write files.
- **Phase B: Onboarding.** Six sequential questions via AskUserQuestion, one per call.
- **Phase B+: Context drop.** One optional question inviting files, links, or folder paths to deepen personalisation.
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

Phase A is fully automated. No user input. Lay down the vault structure from the latest GitHub state, then move to Phase B.

### Step A.1: Resolve target directory

Default target: `~/Obsidian/{{pack_name}}/`. If `{{pack_name}}` is not yet set, default to `~/Obsidian/Foothold/`.

If the target directory already contains files, verify with the user before continuing. Do not overwrite without consent.

### Step A.2: Fetch the latest file tree from GitHub

Call the GitHub tree API:

```
GET https://api.github.com/repos/MilUX-Ltd/foothold/git/trees/main?recursive=1
```

Use the WebFetch tool. Public repo, no auth required.

Filter the response to entries where `type == "blob"` and `path` starts with `foothold/template/`.

### Step A.3: Fetch and write the template

For each shipping file (collected in Step A.2):

1. Compute the corresponding target path. Strip the `foothold/template/` prefix from the GitHub path.
2. Apply placeholder substitution to the filename (any `{{...}}` token gets replaced with the value the user provides in Phase B, or a sensible default).
3. Fetch the raw content from GitHub:

   ```
   GET https://raw.githubusercontent.com/MilUX-Ltd/foothold/main/<full-path>
   ```

4. Apply placeholder substitution to the file content.
5. Create any missing parent directories at the target.
6. Write the file.

Order doesn't matter; the tree fetch gives you the full list in one call, then per-file fetches can run in parallel where convenient.

### Step A.4: Write `.foothold/config.yml`

Create `.foothold/config.yml` at the target root with the substitution values used **and** a baseline `last_known_shas:` map keyed by vault-relative path, set to the GitHub blob SHA each file came from in the tree fetch:

```yaml
foothold:
  installed_at: <today's ISO date>
  version: <from foothold/.claude-plugin/plugin.json at latest commit>
  last_synced: <today's ISO date>
  pack_name: <value>
  pack_slug: <value>
  pack_owner: <value>
  pack_owner_email: <value>
  pack_owner_linkedin: <value or empty>
  pack_owner_phone: <value or empty>
  pack_org: <value>
  pack_org_slug: <value>
  pack_org_website: <value>

last_known_shas:
  Knowledge/rules.md: <sha from tree fetch>
  Knowledge/tagging-policy.md: <sha from tree fetch>
  # ...one entry per shipping file, keyed by post-substitution vault-relative path
```

The SHA map is the source of truth for the three-way reconcile in future `/foothold-update` runs. It tells the update skill exactly which version each file is "at" when the user runs it, so the skill can distinguish between an unedited file the user is happy to overwrite and a file the user has personalised.

### Step A.5: Confirm bootstrap

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
3. For each uploaded file or local file path: read directly with Read (or Bash with pandoc for docx/pptx).
4. For a local folder path: use Glob to enumerate, then read each file.
5. Maintain a context corpus in working memory — every fact, name, number, quote, URL. Tag each by likely target page.
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
| `Context/<pack_owner>.md` | Q1 (name, role, background), Q3 (POV), Q6 (drains) + corpus | `name`, `role`, `email`, `linkedin`, `created` |
| `Context/<pack_org>.md` | Q2 (offer, customer), Q5 (engagements) + corpus | `name`, `website`, `founded`, `created` |
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

- A one-line summary of what was created.
- "Open this folder in Obsidian to see your vault."
- "If you want to pull new content from Foothold later, just run `/foothold-update` here in Cowork. No need to reinstall anything."
- Suggest one concrete next action based on the user's Q answers.

---

## Guidelines

- Always fetch from GitHub, never from the local plugin install's template directory. The plugin only delivers the skills; GitHub is the source of truth for content.
- Phase A is fully silent. No user input.
- Phase B is exactly six questions, asked one at a time via AskUserQuestion. No follow-ups inside a question. No batching.
- Phase B+ is one final AskUserQuestion offering files / links / folders. Always ask, even if Q1–Q6 looked rich.
- For every link the user pastes, fetch it (WebFetch / WebSearch). For every file or folder, read it (Read / Glob). Merge into a single corpus before building.
- Templates are scaffolds, never outputs. Replace every placeholder. If a section has no data after exhausting answers + corpus, omit it.
- Preserve specificity. Use the user's exact names, numbers, URLs, and phrasing.
- Only create canonical pages that have real content. Don't populate empty templates.
- Don't narrate file-by-file. Build silently. Summarise at the end.
