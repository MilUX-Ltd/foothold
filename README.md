<p align="center">
  <img src="assets/foothold-banner.png" alt="Foothold" width="720">
</p>

# Foothold

A **foothold** is a secure initial position established in enemy or hostile territory. Troops use it as a base to land reinforcements, stockpile supplies, and launch further operations into the area.

For defence-sector founders, the hostile territory is the landscape itself. The MOD reorganises faster than the briefing notes can keep up. The named bodies are a thicket of acronyms (NAD Group, NA-Innov, DASA, FCI, jHub, DCTO, CSOC, IDA). The frameworks have different operators, different routes in, different gatekeepers. The information is public, but it is fragmented across hundreds of gov.uk pages, trade-body briefings, supplier directories, and Hansard transcripts. Months disappear into figuring out what the larger players already know.

Foothold gives you that secure initial position in an evening.

It is an installable Obsidian vault pack for defence-sector founders. One command lays down a working second-brain: folder structure, page templates, skills, and pre-populated open-source defence reference content. Walk into Monday with a knowledge system that already knows where the public frameworks live, which MOD body owns what, and how the pieces fit together after the post-SDR reorganisation.

The structure is built to slot into Anthropic's Cowork. A Foothold vault opened in Obsidian, with Cowork running alongside, gives a small defence-sector business something that, until recently, needed a dedicated team to put together.

The operations still have to be run. Foothold is the position you run them from.

> *"It does seem like a no brainer."*
> — an early Foothold user, by email, the day the pack was shared with them

## What changes in your first 30 days

**Day 1.** The vault is installed and knows who you are: your offer, your positioning, your voice, your priorities, all captured in an hour's guided brain dump. The defence landscape is already in it: which MOD body owns what after the reorganisation, where the frameworks and portals live, which route into procurement fits your maturity. Questions that used to cost an afternoon on gov.uk now cost a search.

**Day 15.** Your daily note writes itself each morning: what needs attention, what's rolled over, what's coming. Before every external meeting, one command briefs you from your own relationship history. A live opportunity gets a go/no-go gate before you spend a week on it, checking the cyber floor, the clearance floor, and the export position you didn't know you had to check.

**Day 30.** Drafts start sounding like you, because the vault holds your actual voice, not a description of it. Your CRM knows who's gone quiet. The sector reference pages have refreshed themselves. And the corrections you made in week one have stopped being needed, because everything you teach it stays taught.

The pattern underneath: every hour you give the vault compounds, because nothing you tell it is ever asked for twice.

**Want to look before you leap?** The [Vault Viewer](tools/vault-viewer/) reads any Foothold vault in your browser: no install, no account, no Obsidian.

## What you get

- **A landscape you don't have to research.** Pre-populated, source-cited reference content: the post-SDR MOD structure, frameworks, portals, programmes, regional clusters, plus a procurement playbook that tells you which route fits your situation, funding routes compared, and plain-English orientations on security clearance and export controls.
- **A working method, not just folders.** Guided onboarding builds your canonical pages from a brain dump; a first-week guide turns install-day enthusiasm into habit; every folder ships with a Guide explaining what goes there and why.
- **Skills that do real work.** A daily brief written for you, meeting prep from your own CRM, a pre-bid eligibility gate, a bid-response drafter built on published evaluation criteria, CRM import from wherever your contacts live now, process mapping and SOP capture, and a monthly curation sweep that keeps the vault honest.
- **A pack that stays current.** One update command pulls new content from this repo and never overwrites your own work without an explicit yes.

## Why not just ChatGPT and a folder of notes?

Because a chat forgets and a folder doesn't think. The AI you already use sees one conversation at a time; every session starts from zero, and the burden of re-explaining your business never goes away. Foothold inverts that: your context lives in the vault, permanently, and every conversation starts already briefed: your strategy, your customers, your voice, the state of every engagement. The system gets more useful every week you use it, which is precisely what a chat window never does. And unlike a bespoke setup you build yourself, it arrives with the defence landscape already researched and a maintained update path behind it.

## Audience

Founders running defence-sector businesses, including founders who are new to AI; the pack assumes no prior Obsidian or Claude experience. Free and available to all. Hands-on onboarding and ongoing support are available from MilUX as a paid service; email for current pricing.

## Getting started

This is the install walkthrough. The whole thing takes about ten minutes once you have Cowork and Obsidian open.

### What you'll need

- **A paid Claude subscription, with Cowork.** Cowork is Anthropic's desktop app for non-developers, and it runs inside a paid Claude plan. Sign up and subscribe at [claude.com](https://claude.com), then download the Claude desktop app; Cowork is a tab inside it. There is a running cost here: budget for one Claude subscription per person who will run the vault.
- **Obsidian.** Free knowledge management app. Download from [obsidian.md](https://obsidian.md). Obsidian Sync, used for keeping a vault in step across devices or people, is a paid add-on; a free alternative is covered under Scaling across a team below.

### What it costs, honestly

| Item | Cost | Ongoing effort |
|------|------|----------------|
| Foothold itself | Free, MIT licensed | — |
| Claude subscription (with Cowork) | Your Claude plan, per person ([claude.com](https://claude.com) has current pricing) | — |
| Obsidian | Free | — |
| Obsidian Sync (optional, for multi-device) | Paid add-on; free git alternative documented in the pack | — |
| Keeping the vault honest | — | Plan for about half an hour a week of review and correction, less as it learns |
| Hands-on onboarding from MilUX (optional) | Paid; email matt@milux.co.uk for current pricing | — |

The half-hour a week is the real cost, and it is also the mechanism: the corrections you make are how the vault learns your business. Skip it and the vault plateaus; do it and it compounds.

### Step 1 — Run the setup

Open a new Cowork chat and paste the following:

```
Fetch https://raw.githubusercontent.com/MilUX-Ltd/foothold/main/foothold/skills/foothold-setup/SKILL.md and follow the instructions in it exactly.
```

The skill takes over from here. It will:

1. **Lay down your vault.** Create a folder structure at `~/Obsidian/Foothold/` (or a custom path if you specify one). Silent step, takes a few seconds.
2. **Run a guided brain dump.** Two short forms covering six areas: who you are, what you sell into defence, your positioning, your voice, your current priorities, and your tool stack. Type, paste links, or upload documents against any of them; the single best input is a dictation transcript, rambled and untidied. Skip anything you like. Give it the hour it deserves; everything the vault does afterwards is built from this.
3. **Offer a context drop.** One final question inviting you to paste links, upload files, or point at a local folder of source material. The more you give it, the more personalised your vault will be.
4. **Build your canonical pages.** Silently. The skill drafts your operator profile, organisation page, brand and strategy pages, email signature, and voice notes from the answers and corpus.
5. **Offer the running rhythm.** Whether to schedule `/foothold-update` (weekly or monthly), a daily brief for weekday mornings, a monthly curation sweep, and a one-week check-in that asks what feels wrong and fixes it. All optional; all cancellable later.

When the skill finishes, it tells you where the vault was created and which schedule (if any) is now in place.

### Step 2 — Open your vault in Obsidian

1. Launch Obsidian.
2. Click "Open folder as vault".
3. Point at your new Foothold vault folder (default: `~/Obsidian/Foothold/`).
4. Click "Open".

Your vault is live. The top-level folders appear in the sidebar.

## Keeping your pack up to date

Foothold evolves. New content gets added, existing pages get sharpened, new skills land. After your initial install, all updates happen through a skill that lives inside your vault — no marketplace refreshing, no plugin reinstalling, no Cowork restarting.

### How to trigger an update

1. Open Cowork and make sure it's pointed at your Foothold vault folder. Cowork picks up the vault's skills automatically from the vault's `Skills/` folder.
2. In a Cowork chat, type:

   ```
   /foothold-update
   ```

   Or ask in natural language: "update Foothold", "pull the latest from the Foothold repo", "see if there's anything new in Foothold". Any of those triggers the same skill.

3. The skill goes straight to the public Foothold repository on GitHub via a plain HTTPS request and compares what's there to what you have. It works out the state of every file: new on GitHub, changed upstream since you last pulled, edited locally, or in conflict (you've edited and so has upstream). You're told what's safe to apply automatically and asked what to do about anything you've personalised.
4. When it finishes, you'll see a short report of what was added, what was updated, what was merged, and what was left alone.

### Why this works without any setup

The `/foothold-update` skill lives at `Skills/foothold-update/SKILL.md` inside your vault. It was placed there by the initial `/foothold-setup` run. Cowork sees it the moment your vault is open. The skill makes a plain HTTPS request to the public Foothold GitHub URLs — no GitHub account, no auth, no Terminal, no Git on your machine.

### How conflicts are handled

The update skill is a three-way reconcile. It tracks the SHA (the GitHub blob identifier) of every file at the moment it was last pulled to your vault, stored in `.foothold/config.yml` under `last_known_shas:`. On each run, it compares three things per file: what was last pulled, what's currently on GitHub, and the SHA of the version sitting in your vault right now.

That tells it which of these situations each file is in:

- **Untouched both sides.** Skip — nothing to do.
- **Upstream-only change.** You haven't edited the file; upstream has. Safe to apply, applied by default with a chance to veto.
- **Local edit only.** You've edited; upstream hasn't changed. Skip — there's nothing new to bring in.
- **New on GitHub.** Add it.
- **Conflict.** You've edited the file AND upstream has new changes. You're asked per file: take theirs (overwrite local), keep mine (skip), or merge (the skill proposes a combined version that integrates upstream's changes into your edited file and asks you to confirm before writing).

Your personalised content is never overwritten without an explicit yes from you.

## Yours, forever

Worth stating plainly, because everyone has been burned by a tool that died: **your vault does not depend on us.** It is a folder of plain Markdown files on your own machine, MIT licensed. Updates arrive over a plain HTTPS request to this public repository, with no MilUX server, account, or subscription in the loop. If Foothold stopped being maintained tomorrow, your vault would keep working exactly as it does today: static, complete, and readable by Obsidian, the Vault Viewer, or any text editor on earth. You could fork this repository and maintain your own line. There is no lock-in because there is nothing to be locked into.

## What's next

In the first hour, focus on:

1. **Open `Context/<your name>.md`.** Check the operator profile reads well. Revise anything that needs sharpening.
2. **Read the per-folder Guides.** Every folder has a `<Folder Name> Guide.md` at its root. Knowledge Guide, Operations Guide, Context Guide, and CRM Guide are the load-bearing ones.
3. **Connect Cowork to your vault.** Point Cowork at your new vault folder. Cowork and Obsidian now work against the same files; agents you run in Cowork write into the vault, and you see them in Obsidian.

## Scaling across a team

Foothold is built for a single operator. The setup interview asks who *you* are, the pages are *your* profile, and the update model assumes one person reconciling their vault against upstream. That is the right starting point for a founder. It is worth knowing what changes when a second or third person comes in, before you get there.

The main considerations:

- **One shared vault, or one per person.** A single shared vault keeps everyone on the same canonical knowledge, at the cost of coordinating edits. Separate per-person vaults stay simple individually but drift apart over time. Most small teams want a shared vault for reference content (frameworks, MOD bodies, CRM) and accept that personal working notes can live wherever suits.
- **How the vault syncs between people.** Obsidian Sync is the paid, no-setup option. A private Git repository is the free alternative and gives you version history, at the cost of a little more setup. Pick one before two people are editing, not after.
- **Who curates canonical knowledge.** Name one curator. Foothold's value is that its reference content is trustworthy; that holds only if changes go through someone. Without a curator, a shared vault fills with half-finished and contradictory pages.
- **Write boundaries.** Decide who can write where, and keep agents on a tighter rein than people. A common pattern: everyone can read everything, drafts land in a staging area, and only the curator promotes a draft into the canonical folders.
- **The update conflict model is per person.** `/foothold-update` reconciles one vault against upstream. If several people share a vault, agree that only one person runs updates, and avoid two people editing the same file in the same window, or the three-way reconcile has more to untangle.
- **One Claude subscription each.** Everyone running the vault through Cowork needs their own paid Claude plan. Factor that into the cost as the team grows.

None of this is needed on day one. Set the vault up as a single operator, get value from it, and come back to this section when a second person is ready to join.

## Tools

Standalone tools that ship with Foothold but install nothing live in [`tools/`](tools/).

- **[Vault Viewer](tools/vault-viewer/)** (v1.0.0). A single HTML file that reads a Foothold vault, or any folder of Markdown notes, like a website. No install, no cloud, no Obsidian. Wikilinks, search and backlinks all work, and it runs fully offline with no network requests. Use it to hand a vault to someone who does not have Obsidian, or to read your own on a machine that does not. Download `tools/vault-viewer/vault-viewer.html`, open it in Chrome, Edge or Brave, and point it at a folder. See the [tool README](tools/vault-viewer/README.md) for detail.

## Share back

Foothold gets better the more it knows about the landscape. If you come across something useful that isn't in here — a new MOD body, a framework or programme nobody else has documented well, a portal that's just launched, a sharper definition for an acronym, a piece of doctrine worth surfacing in the Reading List — send it to Matt. A line of LinkedIn, an email, or a screenshot of the page will do. He'll integrate it into the next update so everyone else on the network gets the benefit.

Email: matt@milux.co.uk. LinkedIn: [Matt Odell](https://www.linkedin.com/in/mattodell/).

## Troubleshooting

**The install skill leaves `{{placeholder}}` text in some files** — That's a bug. Tell Matt which files and which placeholder, and we'll fix it.

**Obsidian doesn't see the vault** — Make sure you point "Open folder as vault" at the Foothold root, not at a subfolder.

**Anything else** — Email Matt at matt@milux.co.uk or open an issue at https://github.com/MilUX-Ltd/foothold/issues.

## Help

- Email: matt@milux.co.uk
- GitHub issues: https://github.com/MilUX-Ltd/foothold/issues
- LinkedIn: [Matt Odell](https://www.linkedin.com/in/mattodell/)

## Provenance

Foothold is built by [Matt Odell](https://www.linkedin.com/in/mattodell/), founder of [MilUX](https://milux.co.uk), a defence-focused user-centred design consultancy, and a serving Army Reserve officer. Its structure, conventions, and skills are not a product designed at a whiteboard: they come from MilUX's own working vault, the system the company actually runs its business on, exported and made installable. When something in Foothold improves, it is usually because it broke or fell short in real use first. It improves with every contribution from the network too — if you find something useful that isn't in here, see [Share back](#share-back).
