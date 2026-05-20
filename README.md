# Foothold

A **foothold** in military terms is a secure initial position established in enemy or hostile territory. Troops use it as a base to land reinforcements, stockpile supplies, and launch further operations into the area.

For defence-sector founders, the hostile territory is the landscape itself. The MOD reorganises faster than the briefing notes can keep up. The named bodies are a thicket of acronyms (NAD Group, NA-Innov, DASA, FCI, jHub, DCTO, CSOC, IDA). The frameworks have different operators, different routes in, different gatekeepers. The information is public, but it is fragmented across hundreds of gov.uk pages, trade-body briefings, supplier directories, and Hansard transcripts. Months disappear into figuring out what the larger players already know.

Foothold gives you that secure initial position in an evening.

It is an installable Obsidian vault pack for defence-sector founders. One command lays down a working second-brain: folder structure, page templates, skills, and pre-populated open-source defence reference content. Walk into Monday with a knowledge system that already knows where the public frameworks live, which MOD body owns what, and how the pieces fit together after the post-SDR reorganisation.

The structure is built to slot into Anthropic's Cowork. A Foothold vault opened in Obsidian, with Cowork running alongside, gives a small defence-sector business something that, until recently, needed a dedicated team to put together.

The operations still have to be run. Foothold is the position you run them from.

## What you get

- A Claude plugin that installs the whole pack with one command.
- A re-runnable `rename` step that whitelabels the pack to your name.
- A manual `update` command for pulling new content as Foothold evolves.
- Skills for the high-frequency adds: events, contacts, organisations.
- Open-source defence reference content: regional cluster pages, public framework writeups, MOD body reference pages.

## Audience

Founders running defence-sector businesses, in MilUX's network. Curated handoff, not a public download. v1 is beta; install access is by invitation.

## Getting started

This is the install walkthrough. The whole thing takes about ten minutes once you have Cowork and Obsidian open.

### What you'll need

- **Cowork.** Anthropic's desktop app for non-developers. Sign up at [claude.com](https://claude.com) and download Cowork from there.
- **Obsidian.** Free knowledge management app. Download from [obsidian.md](https://obsidian.md).

### Step 1 — Add the Foothold marketplace

1. Open the Claude desktop app and switch to the **Cowork** tab.
2. Click **Customize** in the left sidebar. This is where Cowork keeps your plugins, skills, and connectors.
3. Click the **+** button.
4. Select **Add marketplace from GitHub**.
5. Enter the repository URL: `https://github.com/MilUX-Ltd/foothold`
6. Confirm.

### Step 2 — Install the Foothold plugin

Once the marketplace is added, Cowork lists the plugins available in it. Find **Foothold** in the list and click **Install**. The plugin activates automatically; its skills become available in any Cowork chat.

### Step 3 — Run the setup skill

In a new Cowork chat, type:

```
/foothold-setup
```

The skill takes over from here. It will:

1. **Lay down your vault.** Create a folder structure at `~/Obsidian/Foothold/` (or a custom path if you specify one). Silent step, takes a few seconds.
2. **Ask six quick questions.** One at a time. Each has quick-pick options plus an "Other" option for free text. Skip any you want. The questions cover who you are, what you sell into defence, your positioning, your voice, your current priorities, and your tool stack.
3. **Offer a context drop.** One final question inviting you to paste links, upload files, or point at a local folder of source material. The more you give it, the more personalised your vault will be.
4. **Build your canonical pages.** Silently. The skill drafts your operator profile, organisation page, brand and strategy pages, email signature, and voice notes from the answers and corpus.

When the skill finishes, it tells you where the vault was created.

### Step 4 — Open your vault in Obsidian

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

## What's next

In the first hour, focus on:

1. **Open `Context/<your name>.md`.** Check the operator profile reads well. Revise anything that needs sharpening.
2. **Read the per-folder Guides.** Every folder has a `<Folder Name> Guide.md` at its root. Knowledge Guide, Operations Guide, Context Guide, and CRM Guide are the load-bearing ones.
3. **Connect Cowork to your vault.** Point Cowork at your new vault folder. Cowork and Obsidian now work against the same files; agents you run in Cowork write into the vault, and you see them in Obsidian.

## Troubleshooting

**"Could not find marketplace MilUX-Ltd/foothold"** — Cowork couldn't fetch the marketplace metadata. Try `/plugin marketplace add MilUX-Ltd/foothold` again. If it still fails, email Matt.

**The install skill leaves `{{placeholder}}` text in some files** — That's a bug. Tell Matt which files and which placeholder, and we'll fix it.

**Obsidian doesn't see the vault** — Make sure you point "Open folder as vault" at the Foothold root, not at a subfolder.

**Anything else** — Email Matt at matt@milux.co.uk or open an issue at https://github.com/MilUX-Ltd/foothold/issues.

## Help

- Email: matt@milux.co.uk
- GitHub issues: https://github.com/MilUX-Ltd/foothold/issues
- LinkedIn: [Matt Odell](https://www.linkedin.com/in/mattodell/)

## Provenance

Foothold is built by [MilUX](https://milux.co.uk). Its structure, conventions, and skills come from MilUX's own working vault.
