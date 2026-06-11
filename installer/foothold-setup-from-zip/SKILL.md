---
name: foothold-setup-from-zip
description: Install Foothold from a downloaded content zip — find or take the zip, lay down the vault structure, then run conversational onboarding. The template ships as a separate plain .zip the user downloads; this skill is tiny and just drives the install. No GitHub access or terminal needed. Use when the user says "set up Foothold", "install Foothold", "install Foothold from the zip", "onboard me", or runs /foothold-setup-from-zip.
---

# Foothold — Install from Content Zip

USE WHEN the user runs `/foothold-setup-from-zip` or asks to install Foothold and has (or can download) the Foothold content zip.

This skill is the **thin installer**. It carries no vault content itself. The Foothold template ships as a separate plain zip the user downloads — typically named `foothold-template-v<version>.zip`. The skill's job is to locate that zip, unpack it, lay down the vault, substitute install-time placeholders, and run onboarding.

Why this design: a skill bundle that embedded the whole template proved unreliable to import. Separating the content into an ordinary download the user unzips, and keeping the skill tiny, removes the failure. Do not try to fetch content from GitHub during install; the zip is the source.

Five-phase process:

- **Phase Z: Locate and unpack the content zip.** Find the zip, confirm it, unzip it to a working area.
- **Phase A.0: Identity.** One quick question so files are named correctly.
- **Phase A: Bootstrap.** Silent. Copy the unpacked template into the target vault folder, substitute install-time placeholders, write files.
- **Phase B: Onboarding.** Six sequential questions via AskUserQuestion, one per call.
- **Phase B+: Context drop.** One optional question inviting files, links, or folder paths.
- **Phase B Build:** Populate the canonical pages from the corpus assembled across Phase B and Phase B+.

---

## Phase Z: Locate and unpack the content zip

The content zip is a normal file the user downloaded. It is **not** uploaded as a skill and **not** inside this skill. Find it in this order, stopping at the first hit:

1. **Files attached to this chat.** If the user has uploaded a `.zip` into the conversation, it is in the session uploads directory. Look there first.
2. **The selected / working folder.** If the user has a folder open in this session, search it (and one level down) for a zip matching `foothold*template*.zip`, then any `*.zip` that unzips to a tree containing a `Context/` and `CRM/` folder.
3. **The Downloads folder, if accessible.** Only if the user has granted access to a folder that is or contains Downloads. Do not assume Downloads is readable; most sessions cannot see it.

**If no zip is found**, ask the user with a short plain message (not AskUserQuestion):

> "I need the Foothold content zip to install from. Two easy ways: drag the `foothold-template-...zip` file straight into this chat, or move it into the folder you've opened in this session and tell me. Which would you like?"

Then wait. When they upload or point to it, resume.

**Once located:**

1. Note the zip path. Unzip it to a fresh working directory outside the target vault (for example a temp dir, or a `.foothold-unpack/` folder you delete afterwards). Use the Bash tool's `unzip`, or read and expand it however is available.
2. Find the template root inside the unpacked tree. The archive's top level is a single folder (for example `foothold-template/`) whose immediate children are the vault folders (`Context/`, `CRM/`, `Intelligence/`, `Resources/`, `Skills/`, `Home.md`, `CLAUDE.md`, `.obsidian/`, and so on). That folder is the **template root**. If the archive has the vault folders at its very top level instead, the archive itself is the template root.
3. Sanity-check: the template root must contain at least `Context/` and `CRM/`. If it does not, tell the user the zip does not look like a Foothold content pack and stop.

Now proceed to Phase A.0.

---

## Phase A.0: Identity

Before laying down files, ask one AskUserQuestion:

- Question: "Before I build the vault, three basics: your full name, your organisation's name, and your work email. Pick an option or type all three under 'Other' (e.g. 'Kevin Watkins, K39 Consulting, kevin@example.com')."
- Header: `Identity`
- Options:
  - `I'll type them` — "Name, organisation, email under 'Other'"
  - `Use placeholders for now` — "Build with generic names; I'll rename later"
  - `Skip` — "Same as placeholders"

From the answer derive the install-time substitution values:

| Token | Value |
|-------|-------|
| `{{pack_owner}}` | Full name (default: `Owner`) |
| `{{pack_owner_first}}` | First name |
| `{{pack_owner_email}}` | Email (default: empty) |
| `{{pack_org}}` | Organisation name (default: `My Organisation`) |
| `{{pack_org_slug}}` | Organisation name lowercased, hyphenated |
| `{{pack_name}}` | Organisation name + ` Foothold` (or just `Foothold`) |
| `{{pack_slug}}` | Pack name lowercased, hyphenated |
| `{{install_date}}` / `{{today_iso}}` | Today's ISO date |
| `{{pack_owner_linkedin}}`, `{{pack_owner_phone}}`, `{{pack_owner_role}}`, `{{pack_org_website}}` | Empty unless volunteered; Phase B may fill them, in which case update the affected pages during Build |

**Substitute only the tokens in this table.** All other `{{...}}` tokens in the template (for example `{{customer_wikilink}}`, `{{title}}`, `{{folder_name}}`, `{{outcome}}`) belong to working page templates used later by the vault's own skills. Leave them exactly as they are.

---

## Phase A: Bootstrap

Phase A is fully automated after A.0. No further user input. Lay down the vault structure from the unpacked template root, then move to Phase B.

### Step A.1: Resolve target directory

Default target: the folder the user has selected in this Cowork session, in a subfolder named after `{{pack_name}}` if the selected folder is not empty, or the selected folder directly if it is empty or clearly intended as the vault root. If no folder is selected, ask the user to select one before continuing.

If the target directory already contains a `CLAUDE.md` at its exact root, the vault is already set up — offer to re-run the interview, full reset (confirm twice), or cancel, then act accordingly. Otherwise proceed.

### Step A.2: Copy and substitute

For each file under the template root (enumerate with Glob or `find`; this is the complete shipping set, around 450 files, including the `.obsidian/` folder so the vault opens cleanly):

1. Compute the target path: strip the template-root prefix, keep the rest of the relative path.
2. Apply install-time substitution (Phase A.0 table only) to the filename. The one templated filename is `Context/{{pack_owner}}.md`.
3. Copy the file, apply install-time substitution to text content, create missing parent directories, write the file. Copy binary files (images, `.obsidian` assets) untouched.

A bulk copy of the template root into the target followed by an in-place substitution pass over text files is fine, provided only the Phase A.0 tokens are replaced and binaries are left alone.

### Step A.3: Write `.foothold/config.yml`

Create `.foothold/config.yml` at the target root:

```yaml
foothold:
  installed_at: <today's ISO date>
  version: <version from the zip name or the bundled docs, e.g. 1.2.0>
  install_source: offline-zip
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
```

### Step A.4: Tidy and confirm

Delete the temporary unpack directory if you created one inside the target. Then tell the user briefly:
- "Vault structure created at `<target path>`."
- List the top-level folders.
- "Now I'll ask six quick questions to personalise the canonical pages, then offer you a chance to upload any extra files or links."

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
- After each answer, move to the next question. No commentary, no recap between questions.
- If the user picks `Skip` or leaves `Other` empty, treat the question as skipped and move on.

**Before Q1, send one short orienting message** (no AskUserQuestion yet):

> "Six quick questions to personalise your vault, then I'll ask if you want to drop in extra files or links for deeper context. Each question has shortcut options — pick 'Other' to type or paste a link. Skip any you want. Reply 'skip all' to proceed with defaults."

If the user replies "skip all" at any point, stop asking and proceed to Phase B+.

### Q1 — You. Header: `You`

- Question: "Quick intro. Your role and the defence background that brings you to this work. What would you want a respected peer to say about you in a defence-sector room?"
- Options:
  - `Founder / Operator` — "Running my own thing in defence"
  - `Consultant / Practitioner` — "Working with defence clients"
  - `Reservist + civilian role` — "Day job in defence plus reservist post"
  - `Skip` — "Skip this question"

Capture: role, defence background, peer-positioning quote.

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
2. For each link: call WebFetch (or WebSearch if the URL is a search). Extract relevant content. Links need network access; if offline, note them in the Daily note for later.
3. For each uploaded file or local file path: read directly with Read (or Bash with pandoc for docx/pptx).
4. For a local folder path: use Glob to enumerate, then read each file.
5. Maintain a context corpus in working memory — every fact, name, number, quote, URL. Tag each by likely target page.
6. After ingestion, briefly tell the user what you pulled. One sentence. Then proceed to Build.

**If the user picks `No` or `Skip`**: proceed straight to Build with only the Q1–Q6 answers.

---

## Phase B Build: Populate canonical pages

Build everything you can from the identity answer, the Q answers, and the context corpus. Work silently. Don't narrate each file.

### Critical rule: scaffolds, not outputs

The templated stubs you wrote in Phase A are **scaffolds** showing the section structure. They are **not** the output. Do not commit a page with bracketed placeholders or italicised hint text intact.

For every file you populate:

1. **Read the existing templated stub** to learn the section structure.
2. **Replace every placeholder** (`{{...}}`, `[bracketed text]`, *italicised hint text*) with real data from A.0 + Q1–Q6 + the context corpus. Files under `Resources/Templates/` are exempt — they are working templates and keep their tokens.
3. **If a section has zero supporting data** after exhausting both Q answers and the corpus: **omit the entire section**. Never leave placeholders behind.
4. **If only some items in a section have data**: keep the section, drop the empty items.
5. **Use the user's actual words, names, numbers, URLs, and quotes** wherever the corpus has them. Preserve specificity.
6. **Cross-reference**: a single fact may belong in multiple files. Place it everywhere it's relevant.
7. **Frontmatter `last_reviewed:`** = today's date.

A finished canonical page should read like a human-written document about the user. If it reads like a fillable form, go back and fill it.

### Pages to populate

For each file below, populate from A.0 + Q answers + corpus. Skip files where there is no supporting data.

| File | Sources | Frontmatter to set |
|------|---------|--------------------|
| `Context/<pack_owner>.md` | A.0, Q1 (role, background), Q3 (POV), Q6 (drains) + corpus | `name`, `role`, `email`, `linkedin`, `created` |
| `Context/<pack_org>.md` | A.0, Q2 (offer, customer), Q5 (engagements) + corpus | `name`, `website`, `founded`, `created` |
| `Context/Brand.md` | Q3 (positioning), Q4 (voice) + corpus | `last_reviewed` |
| `Context/Strategy.md` | Q5 (priorities, initiatives, engagements) + corpus | `last_reviewed` |
| `Context/Team.md` | Q1 + corpus (if user mentions a team) | `last_reviewed` |
| `Context/Stakeholders.md` | Corpus (only if user has named external stakeholders) | `last_reviewed` |
| `Operations/email-signature.md` | A.0, Q1 (role), corpus | none |
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

Foothold pack set up today from the offline content zip. Onboarding complete: canonical pages drafted from the install interview.

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
- "This vault was installed from an offline content zip. To pull newer Foothold content later, run the `/foothold-update` skill in your vault's `Skills/` folder; that step needs internet access."
- Suggest one concrete next action based on the user's Q answers.

---

## Guidelines

- The content lives in a separate downloaded zip, never inside this skill and never fetched from GitHub at install time. Phase Z always runs first.
- If the zip cannot be found, ask for it plainly (upload to chat, or move into the open folder). Do not guess a path or proceed without it.
- Phase A.0 is exactly one question. Phase A is then fully silent.
- Phase B is exactly six questions, asked one at a time via AskUserQuestion. No follow-ups inside a question. No batching.
- Phase B+ is one final AskUserQuestion offering files / links / folders. Always ask.
- Substitute only the Phase A.0 token table at install time. All other `{{...}}` tokens are working-template machinery; leave them intact.
- Templates are scaffolds, never outputs. Replace every placeholder outside `Resources/Templates/`. If a section has no data after exhausting answers + corpus, omit it.
- Preserve specificity. Use the user's exact names, numbers, URLs, and phrasing.
- Don't narrate file-by-file. Build silently. Summarise at the end.
