# Getting Started with Foothold

This guide walks you through installing Foothold from scratch. The whole thing takes about ten minutes once you have Cowork and Obsidian open.

## What you'll need

- **Cowork.** Anthropic's desktop app for non-developers. Sign up at [claude.com](https://claude.com) and download Cowork from there.
- **Obsidian.** Free knowledge management app. Download from [obsidian.md](https://obsidian.md).
- **Access to the Foothold beta.** Matt will have invited you directly. You don't need to ask for an invitation; if you're reading this guide, you already have one.

## Step 1 — Add the Foothold marketplace

Open Cowork. In a new chat, type:

```
/plugin marketplace add MilUX-Ltd/foothold
```

Press Enter. Cowork fetches the marketplace metadata. You should see a confirmation that the marketplace has been added.

## Step 2 — Install the Foothold plugin

In the same chat:

```
/plugin install foothold@milux
```

Press Enter. Cowork installs the plugin, which makes the Foothold skills available.

## Step 3 — Run the setup skill

In the same chat:

```
/foothold-setup
```

The skill takes over from here. It will:

1. **Lay down your vault.** Create a folder structure at `~/Obsidian/Foothold/` (or a custom path if you specify one). Silent step, takes a few seconds.
2. **Ask six quick questions.** One at a time. Each has a few quick-pick options plus an "Other" option where you can type freely or paste a link. Skip any you want. The questions cover:
    - Who you are and your defence background.
    - What you sell into defence and who buys it.
    - Your positioning and what makes you different.
    - Your voice.
    - Your current priorities and engagements.
    - Your tool stack and what's draining your attention.
3. **Offer a context drop.** One final question inviting you to paste links, upload files, or point at a local folder full of source material. The more you give it, the more personalised your vault will be. Skip if you'd rather start lean.
4. **Build your canonical pages.** Silently. The skill drafts your operator profile, organisation page, brand and strategy pages, email signature, and voice notes using the answers and material you've shared.

When the skill finishes, it tells you where the vault was created.

## Step 4 — Open your vault in Obsidian

1. Launch Obsidian.
2. Click "Open folder as vault".
3. Point at your new Foothold vault folder (default: `~/Obsidian/Foothold/`).
4. Click "Open".

Your vault is now live. The top-level folders (Capabilities and Services, Context, CRM, Daily, Ideas, Initiatives, Intelligence, Knowledge, Marketing, Operations, Resources, Skills) appear in the sidebar.

## What's next

In the first hour, focus on:

1. **Open `Context/<your name>.md`.** Check the operator profile reads well. Revise anything that needs sharpening.
2. **Open the Guide pages.** Every folder has a `<Folder Name> Guide.md` at its root. Knowledge Guide, Operations Guide, Context Guide, and CRM Guide are the load-bearing ones. Read those first.
3. **Connect Cowork to your vault.** In Cowork, point at your new vault folder. Cowork and Obsidian now work against the same files; agents you run in Cowork write into the vault, and you see them in Obsidian.

## Troubleshooting

**"Could not find marketplace MilUX-Ltd/foothold"** — Most likely a private-repo authentication issue. If you've been invited to the beta and accepted, but Cowork still can't fetch the marketplace, email Matt and he'll help.

**The install skill leaves `{{placeholder}}` text in some files** — That's a bug. Tell Matt which files and which placeholder, and we'll fix it.

**Obsidian doesn't see the vault** — Make sure you point "Open folder as vault" at the Foothold root, not at a subfolder.

**Anything else** — Email Matt at matt@milux.co.uk or open an issue at https://github.com/MilUX-Ltd/foothold/issues.

## Help

- Email: matt@milux.co.uk
- GitHub issues: https://github.com/MilUX-Ltd/foothold/issues
- LinkedIn: [Matt Odell](https://www.linkedin.com/in/mattodell/)
