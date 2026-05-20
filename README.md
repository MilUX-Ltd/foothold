# Foothold

Defence is hard to get into. The information sits in fragmented places. Small businesses spend months figuring out what the larger players already know. Foothold is built to short-circuit that.

Foothold is an installable Obsidian vault pack for defence-sector founders. One command lays down a working second-brain in an evening: folder structure, page templates, skills, and pre-populated open-source defence reference content. You walk into Monday with a knowledge system that already knows where the public frameworks live and which MOD body owns what.

The structure is built to slot into Anthropic's Cowork. A Foothold vault opened in Obsidian, with Cowork running alongside, gives a small defence-sector business something that, until recently, needed a dedicated team to put together.

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

3. The skill goes straight to the public Foothold repository on GitHub via a plain HTTPS request, lists what's there, compares to your installed vault, and adds any new files. It does not touch files you've already got, so your personalised content stays exactly as you left it.
4. When it finishes, you'll see a short report of what was added.

### Why this works without any setup

The `/foothold-update` skill lives at `Skills/foothold-update/SKILL.md` inside your vault. It was placed there by the initial `/foothold-setup` run. Cowork sees it the moment your vault is open. The skill makes a plain HTTPS request to the public Foothold GitHub URLs — no GitHub account, no auth, no Terminal, no Git on your machine.

### If you want the latest version of a file you've already edited

The update skill never overwrites your local edits. If you've customised a Guide or other file and you want the latest shipped version, delete your local copy first, then re-run `/foothold-update`. It will treat the file as a new addition and copy in the fresh version. Your old text is preserved in Obsidian's file-recovery / version history if you turned that on, and in any Obsidian Sync versions if you use it.

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
