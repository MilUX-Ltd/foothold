# Foothold changelog

## 2.5.0, 2026-11-28

Foothold now comes as a release you can download, and updates ask before they change anything that instructs your AI. Run `/foothold-update` to bring this release in; this once, it will ask about more files than usual.

**New**

- **Releases.** Each version is a GitHub release holding `foothold-2.5.0.zip`, its checksum, and a list of every file in it with its checksum. Unzip it and give your AI tool `Start Here.md`, or paste the prompt from the release page into your AI tool.
- **`Start Here.md`.** The way in, for you and for your AI tool. It sets the rules your AI follows: work from the folder, ask before writing, send nothing anywhere, and set up no scheduled job without a yes.
- **A licence file.** `LICENSE` (MIT, MilUX Ltd) and `THIRD-PARTY-NOTICES.md` are now at the top of the repository.
- **The zip carries its own file list.** `release-files.txt` is inside the zip as well as beside it, the same file. If you update from a zip you downloaded, the update's helper checks every file in the unzipped folder against that list and works exactly as it does for a download from the release: your own details filled in do not count as changes, a change you said no to is asked about again, and a page you kept is not. The list shows whether anything was damaged; it does not show who made the zip. Your own check of the zip's checksum against the release page does that, and the update can now work your zip's checksum out for you to compare.
- **A company page and a `Knowledge/domains/` folder.** The template now has the organisation page setup fills in, `Context/<your organisation>.md`, and the folder setup writes your brand notes into.

**Changed**

- **`/foothold-update` reads the latest release, never a branch.** It checks every file against its checksum before showing it to you, and writes the copy it checked. Reference pages under `Intelligence/` and `CRM/` are listed and need one yes. Every other change, including any skill, instruction file such as `CLAUDE.md`, guide, script or settings file, is shown file by file and needs its own yes. A new skill is shown in full, every file of it, and added only if you say yes. The update tells you if a file holds characters you cannot see.
- **The update leaves `.obsidian/` alone.** Your Obsidian settings are yours. It never adds or changes any other dot-file or dot-folder either, such as `.claude/` or `.mcp.json`.
- **The update's helper takes no file name from the release on its command line.** Your AI gives it only folders, the downloaded file list and item numbers. The helper downloads each file from the release's tag, checks it, shows it to you a page at a time, and works out what to record afterwards. A file too long to show in full is left unchanged, for you to read in the zip. Before it records anything, it checks that each file your AI says it wrote is the release's copy, and that each file you kept is not. Without Python, your AI updates nothing file by file: it offers the downloaded zip instead, which you check yourself, and then uses only its own file reading and writing.
- **If you keep your own version of a page, or merge, it stays yours.** When a later release changes that page, the update shows you the difference and asks again.
- **`Founder's Procurement Playbook` is now the file `Founders Procurement Playbook.md`.** The page and its title are the same; links point to the new name. The update adds it as a new page and leaves your old copy where it is, so you can delete the old one.
- **The update no longer replaces itself and runs again.** A change to it is shown like any other skill change, written last, after everything else is written and recorded, and takes effect the next time.
- **A scheduled update only reports.** It lists what a new release would change and changes nothing.
- **A file with no record of what it held is treated as yours.** The update shows you the difference and asks, instead of overwriting it.
- **Setup works from the release folder** as well as from the Claude plugin. Forms and scheduled jobs are optional: an AI tool without them asks in the conversation and carries on. Setup asks once before it writes anything.
- **Setup asks first, then builds.** In the same message as where to put the vault, it asks for your name, your role, your organisation, its website and your email (the last two can be left blank), and the interview does not ask for them again. It then copies the template, fills in your details, takes the checksums of your vault before it builds anything, builds your pages from the interview, and writes its record once, at the end. A page the build wrote into is then yours: a later release asks about it instead of replacing it. It fills in only its own placeholders, from a fixed list, and leaves those that belong to other skills alone. A page with nothing to put in it says so in one line instead of keeping its example text.
- **Scheduled update checks report in fixed words**, in the job's own output, never in your vault. If you name a downloaded folder when you ask for an update, the update still tries once to download the release's file list, and if it arrives, the folder must match it. Before it asks you anything, it tells you which release it found and which version your vault is on.
- **Your page and your organisation's page always get file names that work.** A name with an accent, a slash or an apostrophe keeps its exact spelling in the page and gets a plain file name, and a sole trader whose business has their own name gets two pages, not one. If setup stopped before it finished, running it again offers to finish.
- **`Getting Started - Your First Week.md` names no particular AI product.** It says "your AI tool" where it said Cowork.
- **`build-dpia` and `cyber-essentials-ready` no longer check for updates over the internet.** Each tells you its version and when it was last reviewed.
- **Five more pages are protected from updates:** `Getting Started - Your First Week.md`, the two `write-sow` assets that carry your name, `Knowledge/domains/brand.md` and the organisation page setup writes in `Context/`.

**For vaults set up before 2.5.0**

- Until you run `/foothold-update` once, your vault keeps the old update skill. The old skill reads `main` of the repository, not a release, and adds new files and applies changes without asking about each one, including when it runs on a schedule. Run the update yourself once, and accept the change to the update skill, to move to the new behaviour. If you set up a scheduled update, cancel it before then.

**For maintainers**

- Vaults set up before 2.5.0 still read `main` until their update skill is replaced (ADR 003). Review every merge to `main` as if it were a release until those vaults have moved.
- A release is a tag `vX.Y.Z` on `main` (ADR 003, which supersedes ADR 002). `.github/workflows/release.yml` refuses a tag that does not match the version records or is not on `main`, runs every check, builds the release with `tools/build_release.py` and publishes it. The zip is the same bytes every time for the same tree.
- The only zips that may be offered to users are those the release workflow builds from a tag.
- File names in the pack may use only letters, digits, space and `- _ . ( ) & { }`, and no two may differ only in capitals. An apostrophe is not allowed. Nothing under `foothold/template/` may begin with a dot, other than `.obsidian/` at its top and `.gitkeep` files. `tools/check.py`, `tools/build_release.py` and the update's helper all refuse anything else. The build takes its files from Git's tracked files only, so an ignored file can never enter a release; `--from-tree` walks the folder instead, for test builds outside Git only; it needs `--allow-dirty` as well and warns that its zip is not a release build. `tools/build_release.py` also refuses to build when `foothold/` has uncommitted changes, unless `--allow-dirty` is passed for a local or test build.
- `tools/check.py` now also checks that filenames are ASCII and legal on Windows, that nothing under `foothold/` points at `main` of this repository, that `Start Here.md` names the version, that every file carrying the `pack_owner` placeholder is protected from updates, and that the README names the current zip.
- Unit tests for the release tooling and the update's sorting are in `tests/`: `python3 -m unittest discover -s tests`.
- `tools/build_release.py` puts `release-files.txt` at the top of the zip's folder, listing every other file in the zip; the published `release-files.txt` is the same bytes. The update's helper takes the unzipped release folder wherever it takes `release-files.txt`, reads the list inside it, and refuses the folder if any file in it is missing, extra or different; `fetch` from a folder uses no network. A downloaded list still comes first. The new `zip-checksum` command prints the SHA-256 of the zip file the person names, for them to compare; it never compares.
- `tools/check.py` now also checks that every placeholder written as a name in double curly brackets in the template is on one of the setup skill's two lists (the placeholders setup fills, and those that are not setup's), that every name setup fills is in the record it writes, and that every page setup builds is protected from updates. It also fails on a placeholder written with spaces, `-` or `.` inside the brackets, on one in a file that is not UTF-8, on `<` or `>` in a template file name, on another skill's placeholder used outside that skill's folder, and when the helper's list of setup's placeholders is not the setup skill's.
- The update's helper refuses a release older than the vault's recorded version, saves a checked copy that is text as `files/000N.txt` (`.bin` only for one that is not), lets `record` accept a file only when it is the release's copy with setup's placeholders filled from the vault's record and nothing else, uses the file-name forms `pack_owner_file` and `pack_org_file` in paths, refuses two files that would land in one place (the person's and the organisation's pages included), and opens the person's zip without blocking. Setup takes `vault_hashes` straight after the copy and fill (fifth safety audit, V1). Setup runs the helper only from the template it installs from, never from the target folder; the helper stops when either version is not X.Y.Z, and works out the file-name forms by setup's rules for a record that has none (sixth safety audit, W1, W5, W6).

## 2.4.0, 2026-11-27

The vault now says how its pages fit together. Run `/foothold-update` to bring it in.

**New**

- **`Knowledge/schema.md`.** One page that sets out the page types, six named connections between pages (`parent`, `customer`, `operator`, `service`, `member_of`, `listed_on`) and two fields each skill uses to say which folders it reads and writes. Your AI reads it to find its way around the vault.

- **Five organisation pages the pack was missing:** the British Army, the Royal Air Force, the Defence Science and Technology Laboratory (Dstl), UK Defence Innovation (UKDI) and Innovate UK. Each says what the body is, how it is organised, and how a small supplier engages with it, from public sources.

- **Four routes.** A route is a job that takes more than one skill, written down in order: a tender lands; you meet someone at an event; a customer asks about your data handling; Monday morning. They are pages in `Skills/Routes/`, and you can add your own.

**Changed**

- **Connections are now links.** On programme, framework, portal, event and organisation pages, the `customer`, `operator`, `service` and `parent` fields now link to the page for the organisation they name, where the pack has one. "UK MOD", "UK MoD" and eleven other wordings all become one link to the UK Ministry of Defence page. Where the old text said more than a name, it is kept beside the link in a note field, such as `customer_note`.
- **`service` on a programme** is a link to the service, or one of three words where no single service owns it: `Joint`, `Civil` or `Industry`.
- **`audience` is new.** Twelve pages described who something is for in the `customer` field ("defence supplier community"). That text has moved to `audience`, so `customer` always names an organisation.
- Three older field names (`parent_programme`, `parent-org`, `operated_by`) are folded into `parent` and `operator`.

- **Every skill now says what it touches.** Each `SKILL.md` carries two new fields, `reads` and `writes`, listing the vault folders it reads from and writes to. 23 skills work on your vault; the other 41, mostly the thinking tools, work only in the conversation and say so. No skill behaves differently: the fields describe what each one already did.

If you have edited any of these pages, `/foothold-update` will show you the change and ask before touching them.

**Fixed**

- One link in the Investors Index that pointed at nothing.

**For maintainers**

- `tools/build_map.py` builds `data/foothold-map.json` from the template: the organisations, programmes, frameworks, portals and events with their connections; the folders and skills with what each skill reads and writes; and the routes. It copies no page text and no field that names a person, and leaves out contact pages and companies. `tools/check.py` fails if the file is out of date. Run `python3 tools/build_map.py --write` after changing the template.
- `tools/check.py` now checks the template against the schema: a connection written as a link must point at a page that exists, each field sits only on the page types the schema allows, and the counts of unfinished work (text values not yet turned into links, skills without declarations) cannot rise.

## 2.3.1, 2026-11-27

Privacy corrections found by a safety audit of the pack. Run `/foothold-update` to bring them in.

**Removed**

- Personal detail about named individuals from the European Defence Tech Hub network page and the European Defence Tech Hackathon event page. Each page now names the organisation's public face only.
- A security clearance level from one reference contact page.
- One line without its own public source from the Programme Cortisone page.

No skill changed in this release.

## 2.3.0, 2026-11-24

Four skills for thinking things through and checking your work before it goes out, all written by MilUX and released under the MIT licence like the rest of the pack. Run `/foothold-update` to bring them in.

**New skills**

- **`process-interviewer`** (`Skills/meta-skills/`). Asks you one question at a time, each with a suggested answer, until an idea or process is clear enough to build, then drafts the plan, skill, SOP or hand-off brief it needs. It only drafts: a new skill gets a safety audit before you use it, and this skill never installs one. If you kept the earlier `process-interviewer` from before 2.2.0, the update offers this version in its place.
- **`prompt-builder`** (`Skills/meta-skills/`). Turns a rough request into a clear prompt for Claude, ChatGPT, Gemini or Copilot by asking about the gaps first.
- **`decision-check`** (`Skills/business-skills/`). Helps you make one real decision well and record it: effort sized to the stakes, options including doing nothing, common thinking traps, a short pre-mortem and a decision note. Raises UK points to check (VAT, IR35, employment, data protection) and says when you need an accountant, solicitor or HR adviser. Not legal or tax advice.
- **`fact-check`** (`Skills/content-skills/`). Checks the factual claims in a draft against UK primary sources first, and flags marketing claims that the CAP Code, the CMA Green Claims Code or price rules would require you to prove. Writes a report beside the draft and changes nothing without your yes.

**Retired**

- **`prompt-master`** is replaced by `prompt-builder`. If you kept the earlier copy, the update offers a short note in its place that points to `prompt-builder`; you can then delete the folder. The update never deletes files itself.

**Skills catalogue**

- `Skills/Skill Examples.md` has a new section, "Thinking and checking skills", listing all four.

Each new skill had an independent safety audit before release, recorded in its frontmatter.

## 2.2.0, 2026-10-15

A full refresh of the defence landscape, checked against public sources from May to October 2026, and the vault brought up to how a small firm actually keeps one going. Run `/foothold-update` to bring it in; nothing you have written is overwritten without your say. A dated summary of what changed is in the new page `Intelligence/defence-landscape/Defence Landscape Updates.md` ("What's New in the Defence Landscape").

**Landscape**

- **Government changes.** DSIT broken up: science and innovation moved to the renamed Department for Business, Innovation, Science and Trade (BIST), with UKRI, ARIA, the UK Space Agency and the Export Control Joint Unit; digital to the Department for Digital, Culture, Media and Sport; AI to the Cabinet Office. New BIST page; the DSIT and Department for Business and Trade pages now point to where the work went. The Investment Security Unit (National Security and Investment Act) is moving to BIST.
- **Renamed bodies.** DASA is now UK Defence Innovation (UKDI); Crown Commercial Service is now the Government Commercial Agency; Strategic Command is now Cyber & Specialist Operations Command. Old names are kept once per page so searches still find them.
- **Defence Investment Plan 2026.** New page reading the June 2026 plan as a demand signal: £298bn over four years, the main lines and what it cancelled. Plan figures added to programme pages.
- **Programmes.** New pages: Taskforce RAID, Hybrid Navy, Project CORVUS, Project NYX, Counter-drone (PRESAGIUM and PANOPTES), Digital Targeting Web. Multi-Role Strike Ship marked cancelled; Type 83 and Type 32 replaced by the Hybrid Navy; SKYNET 6 narrowband not proceeding; NavyX merged into DCTO; GCAP and AUKUS Pillar 2 updated. Programmes Index broken links fixed.
- **Money and routes.** New pages: UKDI: How to Engage; Commercial X and Defence Unicorns (contracts up to £50m and under two years, with Defence Unicorns aimed at firms new to the MOD); Single-Source Contract Rules. Funding Routes adds UK Export Finance's Defence Export Fund, the National Wealth Fund, the Sovereign AI Fund, Innovate UK's defence package and NATO DIANA 2027. The Defence Open Call has not reopened and Defence Innovation Loans are paused; the Security Open Call is open. Founder's Procurement Playbook rewritten for 2026, including the MOD SME Action Plan.
- **Frameworks.** G-Cloud 15, DOS7, Technology Services 4 and the Government Commercial Agency; NVFi corrected to an MOD framework; end dates from the MOD routes-to-market page.
- **Export controls and clearance.** F680 on LITE, the new low-value open licence, the paused classification service; notes on the vetting review and UK Security Vetting's planned move.
- **Events.** DPRTE is at Farnborough (the pack previously said Cardiff); DSEI UK runs 7 to 10 September 2027; next-edition dates in the calendar.
- **Consistency.** MOD Structure brought into line with the gov.uk NAD Group page and the NAD Group pages; contradictions between pages resolved; named office-holders removed so pages do not go stale at a reshuffle; review dates set to 2026-10-15 on reviewed pages.
- Two new programme pages under `Intelligence/defence-landscape/Programmes/`, from the Dstl case study "Developing drone technology for future warfare" (GOV.UK, 27 July 2026): **Project VANAHEIM** (UK-US counter-drone initiative led by the RAPSTONE Task Force; soldier-judged trials in Germany, Poland and, from summer 2026, Lithuania under US Project FLYTRAP) and **Project ANVIL** (first soldier-led development of computer vision models; FIGS ground control station within Initial Experimentation Systems; AUKUS RAAIT lineage; foundation for UK swarming UAS). Both added to the Programmes Index Army table, with a pointer added to the name-only Rapstone entry.

**Vault**

- **Note templates.** A new `Templates/` folder with templates for contacts, organisations, customer engagements, initiatives, ideas, daily notes, weekly reviews, meetings, marketing pieces and services. Title and date fields are left blank for you to fill in.
- **A one-minute Obsidian set-up**, in the Templates Guide. The pack does not change your Obsidian settings for you, so your own theme and plugins are never touched by an update.
- **New `Inbox/` and `Attachments/` folders**, each with a short Guide.
- **Every folder Guide follows one shape:** Purpose, Structure, Writing a note, Lifecycle, Frontmatter, Canonical example, Related. The Knowledge and Intelligence Guides now say plainly which folders ship and which are optional.
- **One frontmatter convention**, rule R-07 in `Knowledge/rules.md`. Existing field names are not renamed. Rule R-03 now says notes still in `Inbox/` need no frontmatter until they are filed.
- **Removed: `process-interviewer` and `prompt-master`**, because their licences do not allow us to redistribute them. The update does not delete files, so if you already have them they stay in your vault; `/process-map` covers getting a process out of your head.
- **Skills.** The curator leaves `Inbox/` and `Templates/` alone (1.0.1); `process-map` and `bid-response` have wording-only changes (1.0.1); the Cyber Essentials audit note no longer points at a private location.

`CLAUDE.md` and `Home.md` are never changed by an update, so existing vaults keep their own copies; new installs get the versions that mention the new folders and the What's New page.

## 2.1.0, 2026-07-15

Fixes a setup skill that could not enumerate its own files. `foothold-setup` Step A.2 called the GitHub `git/trees` API to list the template, but that endpoint returns JSON, which the Cowork WebFetch tool cannot read, so the file list came back empty and the install stalled before writing anything. The individual raw-file fetches worked, which hid the real cause.

- **Setup now installs from the template bundled in the plugin, not over the network.** Phase A locates the plugin's own `template/` directory (a sibling of `skills/`), enumerates it with Glob, and reads each file with the file tools. No GitHub API at install, and no separate manifest to keep in step. The plugin is the versioned artifact; whatever version was installed is what gets laid down, and `/foothold-update` reconciles to the latest published content as before.
- **The `last_known_shas` baseline is preserved.** Each entry is now the source file's blob SHA computed locally with `git hash-object`, which is identical to the SHA a GitHub tree fetch recorded, so `/foothold-update`'s three-way reconcile is unaffected.
- The header, intro, Phase A and Guidelines are reworded to match: setup is an offline, deterministic step; `/foothold-update` is the one path that talks to GitHub.
- The same fix is applied to `footing-setup` in the Footing repo.
- Plugin manifest bumped to 2.1.0. It had drifted at 2.0.0 while the changelog ran to 2.0.2.

Note: the skill's `skill-safety-audit` frontmatter still reads the 2026-07-02 pass. This change alters skill behaviour, so a re-audit is due before the next release per R-28.

## 2.0.2, 2026-07-02

Answers the questions the ICP review surfaced, in Matt's words.

- The one-line description is now "an integrated AI operating model and second brain for defence businesses", matching the launch graphic. It says what the pack became at 2.0.0; "a folder structure with reference content" undersold it.
- `docs/architecture.md` rewritten to match the pack as it is: the stale bash-CLI commands section replaced with the real skill-based setup and update flow, the agent-stack section reframed honestly as "one operator, agents with boundaries", the four-skill v1 list replaced with the current seven-category set, the placeholder table completed, and the content-layer summary updated with the playbook, funding routes and compliance orientations.
- Retired the offline zip installer (`installer/`). The zips had drifted seven releases behind the template, no documentation pointed at the path, and the one-line GitHub fetch has been the sole documented install since 1.6.0. Anyone needing an offline install can clone the repo; the template is all in it.

- New README section, Support from MilUX: the first hour of setup consulting is complimentary, then the pack runs without us; AI enablement beyond the pack; trusted-partner referrals for Cyber Essentials and business setup; scaling support; and the UK-wide Claude associate network. The audience line and cost table updated to match.
- Provenance now says the associates in MilUX's Claude Partner Network run the pack too.
- The ChatGPT objection section notes the pack sits alongside existing AI use, adding the agentic side with policies, integration and orchestration worked out.
- `bid-response` gains "Can AI-drafted content go in a submission?": yes, with the human final pass non-negotiable and honesty if a buyer asks.

## 2.0.1, 2026-07-02

- README gains "Prefer a different stack?": a short note that the pack is plain Markdown and can be configured for open-source tools such as OpenCowork, self-hosted or already-owned models, and other sync arrangements, as bespoke work through MilUX.

## 2.0.0, 2026-07-02

The onboarding release, and a major version because it changes what installing Foothold feels like. Informed by a competitive benchmark of a comparable vault-pack product; the patterns were rebuilt, not copied, and in each case improved: their form-based onboarding is Cowork-only, ours degrades to plain questions anywhere; their operator concept writes externally unattended, our adaptations stay review-gated and vault-only.

- **The small-firm questions answered.** New `Resources/Ways of Working/Where Your Data Lives.md`: what stays local, what Claude sees and under whose terms, what never goes in the vault (classified material, export-controlled data, caveated client material, personal data without a basis), how the setup sits inside a Cyber Essentials posture, and what to say to a prime's security questionnaire. The README gains a matching section, and its team section is rewritten as "Running Foothold in a small firm": a month-by-month adoption path, the curator as a role a firm can delegate, honest per-seat maths (readers need the free Vault Viewer, not a subscription), and a "what to bring, what to leave" rule.
- **README rewritten around outcomes.** A "what changes in your first 30 days" section, the ChatGPT-and-folders objection answered, an honest cost-and-effort table, a "Yours, forever" ownership clause, a maintainer provenance paragraph, an early-user quote, and the Vault Viewer promoted to the try-before-you-install path.
- **Onboarding is now a guided brain dump.** `foothold-setup` Phase B replaces six sequential questions with two rich forms (six categories, same substance): per category a brain-dump box, a links-and-paths field, and file upload, with dictation transcripts explicitly recommended as the highest-yield input. Bullets are inspiration, not required fields; blank skips; everything offered is ingested greedily into the build corpus. Falls back to the question flow where the form surface isn't available.
- **Re-running setup is now discovery-first.** The re-run flow reads config and Context silently, presents a "discovered from your vault" summary, and asks only "what's changed, or what did I get wrong?". The skill never asks for a value the vault already holds.
- **Probe, don't ask.** `import-relationships` detects and read-only-probes CRM connectors before asking anything, reporting exact errors with a skip-or-fix choice; `daily-brief` does the same for the calendar, and reports a failing connector once rather than daily.
- **The first-week check-in became a personalisation loop.** "A week in — what feels wrong, missing, or harder than it should be? I'll change it." Smallest change, confirm, ask what else, and park unreached wants in `Ideas/` for the next session.
- **New `Skills/ops-skills/` category, four skills, replicated from Footing 2.0.0.** `process-map`, `sop-capture`, `service-blueprint`, and `ai-readiness`. Foothold founders are new to AI too, and defence founders sell services; the original plan to hold two of these back was wrong and is recorded as such. Same content as Footing's, pack licence line aside.
- **Setup now creates the structural folders explicitly** (Step A.3b, canonical list in the skill). Git carries no empty directories, so the tree fetch alone never could; this closes the gap where a fresh install arrived without the `Customer Engagements/` states, `Ideas/`, `Initiatives/`, or `Daily/`.
- **New `Skills/meta-skills/curator/`: the budgeted curation sweep.** Fixes mechanical defects with exactly one right answer (broken wikilinks with an unambiguous target, missing frontmatter derivable from the folder Guide, unescaped pipes in table wikilinks) within hard per-run caps: 200 reads, 20 fixes, 30 report items, folder rotation for larger vaults. Everything needing judgement goes to a dated Curation Report instead of being touched; no renames, no archiving, no deletion, ever. Setup offers a monthly schedule (3rd of the month). The skill curates hygiene, not knowledge; meaning stays with the owner. MIT licensed, MilUX original.
- Plugin and marketplace manifests reconciled to 2.0.0 (they had drifted to 1.6.0 while the changelog ran to 1.10.0).

## 1.10.0, 2026-07-02

- New `How to Use This Vault.md` at the vault root: the four working habits that make the system compound. Brief Claude like an intern in its first week (it never forgets a good briefing, because the briefing lives in the vault); describe your processes, because a process you can describe is a process you can automate; watch for repeatable patterns worth turning into a skill or a schedule, and tell Claude to watch too; and review both the work (self-review against the brief before anything is called done) and the working (regular retrospectives whose output is always a permanent change: a rule, an amended skill, a corrected Context page). Home.md and the first-week guide both link to it.

## 1.9.0, 2026-07-02

Kills the write-three-lines daily-note ritual shipped earlier today in 1.8.0. Asking the user to report what happened yesterday is a scrum anti-pattern; the vault already knows.

- New `Skills/meta-skills/daily-brief/`: writes the day's note as a brief FOR the user, generated from engagements, initiatives, items rolled forward from previous notes, upcoming events, and (where a calendar connector exists) today's meetings. Owns a `## Daily Brief` section per the Daily Guide convention and never touches the user's own writing. Hard cap of seven needs-attention items; a quiet day gets a short brief, honestly. MIT licensed, MilUX original.
- `foothold-setup` Phase C now offers to schedule `/daily-brief` for weekday mornings at 08:00.
- `Getting Started - Your First Week.md` Day 3 rewritten: run the brief, schedule it if it earns its place. The standup ritual is gone.
- `Daily Guide.md` updated: the note can be created by the brief each morning; the user writes everywhere else.

## 1.8.0, 2026-07-02

The first-week release: the pack now walks a new user from install day into a working habit, and the vault they land in has a live front door.

- New `Getting Started - Your First Week.md` at the vault root: one small win a day (foundations, CRM import or seeding, the daily-note habit, design system, landscape orientation), then week two onwards. Home.md now leads with it.
- `foothold-setup` Phase C now offers a one-off check-in scheduled seven days after install, revisiting the first-week list with the user.
- `Home.md` rewritten: the Dataview query suggestions are now live query blocks (engagements in scoping and active, open initiatives, recent contacts, latest published), with a one-line pointer to installing the free Dataview plugin. Panels fill themselves as the vault grows.
- New `Intelligence/defence-landscape/Funding Routes.md`: DASA/UKDI competitions, Defence Innovation Loans, Innovate UK/SBRI, DTEP, NSSIF, ARIA and venture capital compared on size, time to money and equity cost, with the three questions that choose between them and a warning about grant-chaining.
- New `Resources/Reading List.md`: policy and reports first (SDR 2025, Defence Industrial Strategy 2025, Defence Investment Plan, NAD Group pages), then practitioner guides (the Hitchhiker's Guide to the Valley of Death, DASA proposal guidance), then a deliberately short book shelf. Deliberately not filed under Books, because the most important reading here is not books.
- New `Resources/Ways of Working/Sync and Backup.md`: Obsidian Sync, git, iCloud, OneDrive/Dropbox/Google Drive and Syncthing compared honestly, including the iOS limitation on generic cloud drives, plus the sync-is-not-backup discipline and a warning against stacking sync systems.
- New `Skills/business-skills/bid-response/`: structures and drafts a tender or competition response around the opportunity's own published evaluation criteria, compliance matrix first, evidence-only claims, social value as a scored section, and an assessor-lens red-team before submission. Doctrine sourced from published gov.uk guidance (DASA assessment criteria, MOD Commercial toolkit, Selling to government, the Procurement Act 2023 MAT basis, the Social Value Model) and the APMP body of knowledge. MIT licensed, MilUX original.
- New `Skills/crm-skills/import-relationships/`: back-ported from Footing 1.2.0. Seeds the CRM from a live CRM connector, a CSV export, or a guided interview, with triage before import and a preview gate before any batch write. Adapted to Foothold's organisation buckets and its pre-populated MOD pages (link, don't duplicate).

## 1.7.0, 2026-07-02

The procurement navigation release: the landscape pages told you what exists, this release tells you which route fits your situation and whether you can clear the walls before you bid.

- New `Intelligence/defence-landscape/Founder's Procurement Playbook.md`: the decision layer over the Frameworks, Portals and Programmes catalogues. Routes by maturity (funded R&D at TRL 1 to 4, proof and access at 5 to 7, the three procurement doors at 8 plus, and a separate services path), by timeline, then route-independent hygiene and the common failure modes. Written against the 2026 landscape: NAD Group fully established April 2026, UKDI inside NA-Innov, the DASA Open Call closed pending reopening around UKDI FOC, DOSBG as the SME front door.
- New `Intelligence/defence-landscape/Security Clearance Primer.md`: clearance levels (BPSS through eDV), personnel versus Facility Security Clearance, realistic 2026 timescales, and the founder traps (no self-sponsorship, clearance in bid qualification). Published UKSV and MOD positions only; no folklore.
- New `Intelligence/defence-landscape/Export Controls Orientation.md`: the UK regime in one page (control lists, ECJU, SPIRE, licence types, the Dual-Use OGEL in force 25 June 2026), the transfer-counts-as-export trap including US-origin ITAR/EAR contamination, and a five-question screening checklist. Orientation, not legal advice, and it says so.
- New `Skills/business-skills/eligibility-check/`: a pre-bid go/no-go gate. Four walls in kill order (cyber floor per Def Stan 05-138 Issue 4, clearance floor, export position, commercial basics), verdict page written to the engagement folder, and a mandate to say no. MIT licensed, MilUX original.
- Fixed: `MOD Structure.md` dated the NAD Group's establishment to April 2026; it was established March 2025 and declared fully established April 2026. The Defence Landscape Index and MOD Structure now agree.
- `Defence Landscape Index.md` topical maps list now leads with the playbook.

## 1.6.0, 2026-07-01

Removes the marketplace install step from the getting-started flow.

The previous flow required users to add the Foothold GitHub repo as a Cowork marketplace, install the plugin, and then run `/foothold-setup`. The marketplace step caused friction — particularly on Windows — and added no value that the skill itself does not provide. The setup skill fetches directly from GitHub, so the plugin was only ever a delivery wrapper for a URL.

The new flow is a single step: paste one line into a Cowork chat and the skill runs. No marketplace, no plugin install, no slash command required.

- README rewritten: Steps 1 and 2 (Add marketplace, Install plugin) replaced with a single prompt-based step.
- Troubleshooting entry for marketplace errors removed.

## 1.6.0, 2026-06-27

A data-protection release: founders can now produce a DPIA and record a lawful basis for every contact, plus a new validation skill. Template moves to 1.6.0. (Version note: the plugin and marketplace version files had drifted to 1.2.2 while the changelog ran to 1.5.1; they are reconciled to the changelog lineage at 1.6.0 with this release.)

Adds the `design-cheapest-test` pm-skill. It helps a founder turn a riskiest assumption into the cheapest test that could prove it wrong, with the change-my-mind result set before the test runs. The keystone of build, measure, learn, and a gap in the pm-skills set until now.

- New `Skills/pm-skills/design-cheapest-test/`: designs a small, fast, falsifiable experiment, names the metric and sample, and pre-registers the decision each result triggers (proceed, pivot, or kill). It coaches rather than authors; the founder designs the test. MIT licensed, MilUX original.
- Authored for the MilUX hackathon package and shared into Foothold, since founders validating a product need the same discipline.

Adds the `build-dpia` business skill: produces a Data Protection Impact Assessment for the founder's business from their vault. It reads existing vault context, walks the founder through any unknowns, asks about the tools they use and the types of personal data they hold, and writes a DPIA in the ICO seven-part structure to `Operations/`. It then offers to set up the quarterly lawful-basis review and to produce a PDF version. References bundle the ICO screening and lawful-basis guidance, the DPIA template, and a neutral PDF template founders can rebrand. Skill is `audited: pending`; run `skill-safety-audit` before the next tagged release (R-28).

Adds a lawful basis to the CRM so every contact records the UK GDPR Article 6 basis on which their data is processed. Good data-protection practice for founders, and the groundwork for a data protection impact assessment.

- New `lawful_basis:` frontmatter property on contacts (legitimate-interests, consent, contract, or legal-obligation), mirrored by an `lb-*` tag. Documented in `Knowledge/tagging-policy.md`, the CRM Guide and the Contacts Guide.
- The `add-contact` skill now asks which basis applies and proposes the most likely one, then writes the property and tag.
- The four shipped example contacts carry the new field.

Version note: the two version files (`plugin.json`, `marketplace.json`) currently read 1.2.2 while this changelog runs to 1.5.1. Reconcile that before the next tagged release and set the version for this change then (a minor bump, per R-22).

## 1.5.1, 2026-06-25

Adds the `red-team-investor` business skill. Template moves to 1.5.1.

- New `Skills/business-skills/red-team-investor/`: critiques any investor-facing content (pitch deck, one-pager, business plan, financial model, cold email, investment memo, teaser, data room) from a sceptical investor's point of view, calibrated to stage and content type. Organised around the market / product / execution risk triad, with a red-flag sweep, sector lenses (deep tech and TRL, regulated, marketplace, SaaS, consumer), and the hard diligence questions the content is least ready for.
- Reviews only; it does not write or improve the pitch, and contacts no one. Benchmarks cite public investor and accelerator sources (Sequoia, a16z, CRV, Y Combinator and Paul Graham, UKBAA, British Business Bank, SeedLegals) and are dated 2024 to 2026 as bands.

## Tools: Vault Viewer 1.1.0, 2026-06-23

Adds a graph view to Vault Viewer. The installed pack and template are unchanged and stay at 1.5.0; this is a repo-side tool, so `foothold-update` brings nothing new into an existing vault.

The graph is a force-directed map of the vault, drawn on a canvas in plain JavaScript so it stays offline. Nodes are notes sized by link count, edges are the links, with pan, zoom and hover. Built from feedback that new users spend their early time in the graph as they build folders from scratch.

- Click a node to isolate it with its 1st and 2nd-degree links, fading the rest, and preview the note's contents without leaving the graph.
- Labels are zoom-gated and overlap-aware, so they stay out of the way until there is room.
- Pin nodes by dragging them or shift-clicking. An optional toggle shows directional arrows for mapping networks and organisations.
- A Display panel carries the Obsidian controls (text fade, node size, link thickness) and force controls (centre, repel, link force, link distance), all remembered between sessions.
- The layout uses a Barnes-Hut quadtree, so it holds up on large vaults.
- The link index now reads both `[[wikilinks]]` and Markdown links, which also corrects backlinks in vaults that use Markdown links.

Still a single offline HTML file with the brand fonts embedded and no network requests.

## Tools: Vault Viewer 1.0.0, 2026-06-23

Adds a standalone `tools/` area at the repository root, shipping Vault Viewer v1.0.0. The installed pack and template are unchanged and stay at 1.5.0. This is a repo-side tool rather than a template addition, so running `foothold-update` brings nothing new into an existing vault.

Vault Viewer is a single HTML file that reads a Foothold vault, or any folder of Markdown notes, like a website. It needs no Obsidian and installs nothing. It removes the Obsidian dependency for the read case: hand a vault to someone who does not run Obsidian, or read your own on a machine that does not have it. It resolves wikilinks, embeds and backlinks, has full-text search and a collapsible file tree, light and dark themes, resizable columns, and an opt-in edit mode that writes back to the files. It runs fully offline and makes no network requests; the brand fonts are embedded so nothing needs downloading. The file carries no vault data, so sharing it shares the tool and none of your notes.

- New: `tools/vault-viewer/vault-viewer.html` plus a tool `README.md`.
- The root README gains a Tools section pointing to it.
- Fonts embedded under their open licences: Manrope and Bai Jamjuree (SIL OFL 1.1), Roboto Mono (Apache 2.0).

## 1.5.0, 2026-06-19

Adds the `write-sow` business skill.

- New `Skills/business-skills/write-sow/`: turns a transcript, job spec, statement of requirement, or bullet-point idea into an outcome-based Statement of Work. It shapes the contract to support an outside-IR35 position (control, substitution, mutuality, financial risk, part-and-parcel, equipment) and flags residual status risk rather than certifying status; builds a risk register scored by severity and likelihood, with a wording mitigation and a pricing response per risk; and recommends a pricing model (fixed-price per outcome, day-rate capped, or milestone-staged). Output is a branded PDF using the founder's own `Context/Brand.md` cues, plus a markdown working draft saved under `Customer Engagements/`.
- UK-focused. The IR35 content is sourced to gov.uk and HMRC and carries a not-legal-or-tax-advice boundary. The skill drafts only; signature and sending are left to the founder's own e-signature and email tools.
- Catalogued in `Skill Examples.md` (Commercial skills) and logged in the `Skills Value Register`.

## 1.4.0, 2026-06-16

Adds the pitch module and reorganises Skills into category folders.

- New `Skills/pm-skills/` set: `pitch-prep`, plus 32 product-management skills forked from phuryn/pm-skills (MIT), adapted for defence-sector founders with the proprietary method removed (see `Skills/pm-skills/NOTICE.md`).
- New pitch materials: the three-act framework (`Resources/Frameworks`), two worked example decks (`Resources/Templates`), and a public-tools reference (`Resources/Reference`).
- Skills reorganised from a flat layout into category folders (`pm-skills`, `content-skills`, `business-skills`, `crm-skills`, `meta-skills`); the Skills Guide documents the new convention.


## 1.3.0, 2026-05-30

Adds the `Customer Engagements/` top-level folder, separating work you deliver for an external organisation from work you do for yourself.

The split is binary and turns on outcome ownership: if your business owns the outcome (internal services, your own products, marketing, thought leadership, internal tooling), the work belongs in `Initiatives/`. If an external organisation owns the outcome, the work belongs in `Customer Engagements/`. Paid, sponsored, or pro-bono doesn't decide the folder; what decides it is whether there is a named external organisation on the receiving end of the delivery. Every engagement maps 1:1 to a page in `CRM/organisations/`.

Customer engagements use a three-state lifecycle (`scoping/`, `active/`, `completed/`) rather than the two-state lifecycle initiatives use. The `scoping/` subfolder is the missing piece in most early-stage workflows: it gives a real home to the work of shaping a deliverable before there is a commitment to deliver, and it absorbs the engagements that go cold without losing the CRM signal that something was once in play.

Why this matters for defence-sector founders: client work and internal product work read differently on the same dashboard. Mixing them makes "what is my current client load" harder to see than it should be, and makes case-study harvesting harder later. The split surfaces customer load cleanly, gives scoping work a defined home, and points each engagement back at the CRM organisation page that owns the relationship.

The Initiatives Guide is updated with the binary rule and a cross-link to the new Guide. The architecture doc and the template `CLAUDE.md` and `Home.md` are updated to describe both folders side by side.

## 1.2.0, 2026-05-26

Adds the `investors/` bucket to `CRM/organisations/`, pre-populated with around 120 investor entries spanning UK and European VCs, corporate VCs, fund vehicles, and government-aligned strategic investors with defence-tech or dual-use exposure.

Each entry carries the same shape: company details (HQ, founded date, fund size, stage focus, geography), an About paragraph on thesis and posture, a Key People table of named partners with verified LinkedIn URLs, a portfolio of notable defence and dual-use investments, and the framework and co-investor signals that travel with the firm. Where a partner could not be verified on LinkedIn, the entry says so rather than guessing; that honest signal is more useful in a raise than a polished gap.

The structure mirrors `defence companies/`: eight letter-based subfolders (`0-9`, `A-B`, `C-D`, `E-H`, `I-N`, `O-R`, `S-T`, `U-Z`) under the bucket, with an `Investors Index.md` at the root listing every entry and pointing to the government-aligned investors that live in `government/` (NSSIF, UK Innovation and Science Seed Fund, UKRI).

Why this matters for defence-sector founders: the investor map is the missing piece in most early-stage research workflows. Knowing which fund backs which kind of company, who the partner contact is, and which co-investors travel together is half the work of an effective raise. The bucket starts with European and UK depth because that is where most Foothold founders are raising; broadening to US and Asian funds is a later edit, not a Foothold-template task.

The Organisations Guide is updated to list the `investors/` bucket alongside the rest, with the letter-subfolder convention noted.

Thanks to inink for providing the thorough and detailed list of investors this bucket is built from.

## 1.1.0, 2026-05-24

Adds `cyber-essentials-ready`, a guided walkthrough that takes a non-IT founder through configuring their personal Mac or Windows computer to meet the UK Cyber Essentials technical controls.

Cyber Essentials is a recurring friction point for defence-sector founders selling into the MOD: it appears in supplier prequalification, in security clauses on framework agreements, and as a prerequisite for several gated frameworks. Many founders know they need it and don't know where to start. This skill closes that gap on the device side.

What the skill does:

- Walks the user through the five Cyber Essentials technical controls (firewalls, secure configuration, security update management, user access control, malware protection) one at a time, on macOS 14+ or Windows 10/11.
- Three modes: walk-through (the user clicks, the skill explains), commands (the skill stages safe commands on the clipboard, the user pastes), do-it-for-me (the skill drives System Settings via computer-use, the user retains consent per change).
- Verify mode for monthly re-checks, with drift detection (green / amber / red) and an optional remediation pass on red drift.
- Writes an evidence pack, append-only audit log, per-control compliance status snapshot, and reviewer-facing README to `Operations/Cyber-Essentials/` in the founder's vault. The pack is designed to be opened by an IASME assessor, a Cyber Advisor, or a defence customer's security team and read without further explanation.
- Registers a monthly Cowork scheduled task to keep the posture current, with a calendar-reminder fallback if scheduled tasks isn't available.

Scope is the founder's primary work computer. Mobile devices and SaaS multi-factor authentication are real Cyber Essentials requirements and the skill states up front that they are out of scope today; founders handle those separately. The skill is pinned to the IASME Montpellier question set; the pin lives in the skill's manifest, frontmatter and changelog, and gets reviewed when IASME publishes a new named release.

Skill catalogue: a new "Security and compliance skills" section in `Skills/Skill Examples.md` carries the cyber-essentials-ready entry.

Sources: NCSC Cyber Essentials overview, NCSC Platform Guides, NCSC Small Business Guide, NCSC Device Security Guidance Configuration Packs (Crown Copyright, Apache 2.0), IASME Question Set, IASME Readiness Tool, IASME Knowledge Hub, Apple Platform Security guide, Microsoft Learn.

## 1.0.0, 2026-05-23

Initial public release. Installable Obsidian vault pack for defence-sector founders, plus a Claude plugin that wires the install and update lifecycle. Includes folder structure, page templates, conventions, the `/foothold-setup` lifecycle skill, the `/foothold-update` content-update skill, and vault-bundled runtime skills: add-contact, add-organisation, add-event, prompt-master, process-interviewer, newsletter-writer, meeting-prep, late-payment-reminder. Ships pre-populated open-source defence reference content: regional defence and security clusters, public framework writeups, MOD body reference pages.
