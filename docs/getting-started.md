# Getting Started with Foothold

This guide walks you through installing Foothold from scratch, from "what is this?" to a working second-brain you can use the same day.

Read it once end-to-end before you start. The whole install takes about 30 minutes if you already have a GitHub account, longer if you're setting one up.

## What you'll need

- A Mac running macOS Sonoma or later.
- A Claude account with Cowork access. If you don't have Cowork yet, ask Matt and he'll get you on the list.
- A GitHub account.
- An invitation to the `MilUX-Ltd/foothold` private repository. If you don't have one, ask Matt.
- About 30 minutes.

## Step 1 — Accept the GitHub invite

Foothold is distributed via a private GitHub repository. Before you can install, you need to be added as a collaborator.

1. Matt sends you an invite. It arrives by email from `noreply@github.com` with the subject "MilUX-Ltd has invited you to MilUX-Ltd/foothold".
2. Click the link in the email, or go directly to https://github.com/MilUX-Ltd/foothold.
3. Click "Accept invitation".

If you can see the repository at https://github.com/MilUX-Ltd/foothold after accepting, you're in.

## Step 2 — Install Claude Cowork

Cowork is the Anthropic desktop app that runs the Foothold install skill.

1. Download Cowork from the link Matt sends you (Cowork is currently a research preview and not yet on the public download page).
2. Open the downloaded `.dmg` and drag Cowork to your Applications folder.
3. Launch Cowork. Sign in with your Claude account.
4. If prompted, grant Cowork access to your file system so it can create the Foothold vault on your Mac.

## Step 3 — Install Obsidian

Obsidian is where you'll work in your Foothold vault day to day. You don't need to create a vault yet — Foothold's install skill does that.

1. Go to https://obsidian.md and download Obsidian for Mac.
2. Open the downloaded file and drag Obsidian to your Applications folder.
3. Launch Obsidian. If it asks to create or open a vault, click "Cancel" or close the dialog. You'll point Obsidian at your Foothold vault after the install completes.

## Step 4 — Set up GitHub access on your Mac

For the Foothold install to clone the private repository, your Mac needs to be authenticated with GitHub. The easiest way is the GitHub CLI.

1. Open Terminal (Cmd+Space, type "Terminal", press Enter).
2. Install Homebrew if you don't already have it:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   This may take a few minutes. Follow any prompts about adding Homebrew to your PATH.

3. Install the GitHub CLI:

   ```bash
   brew install gh
   ```

4. Authenticate:

   ```bash
   gh auth login
   ```

   When prompted, choose:
   - "GitHub.com"
   - "HTTPS"
   - "Yes" to authenticate Git with your credentials
   - "Login with a web browser"

   Copy the one-time code shown in Terminal, press Enter, and a browser window opens. Paste the code, sign in to GitHub, authorise.

5. Verify it worked:

   ```bash
   gh auth status
   ```

   You should see a green tick and your GitHub username.

## Step 5 — Add the Foothold marketplace and install the plugin

Open Cowork. In a fresh Cowork session, you're going to add the MilUX marketplace, install the Foothold plugin, then run the install skill.

1. In Cowork's chat input, type:

   ```
   /plugin marketplace add MilUX-Ltd/foothold
   ```

   Press Enter. Cowork clones the marketplace metadata from the private repo. Because you authenticated with `gh auth login` in Step 4, the clone uses your credentials and succeeds.

2. Once the marketplace is added, install the plugin:

   ```
   /plugin install foothold@milux
   ```

   Press Enter. Cowork installs the Foothold plugin, which makes the `foothold-setup` skill available.

## Step 6 — Run the setup skill

In the same Cowork session:

```
/foothold-setup
```

The skill takes over from here. It will:

1. **Bootstrap.** Create a folder structure at `~/Obsidian/Foothold/` (or a custom path if you specify one), copy the templated vault content, run placeholder substitution. Silent step, takes a few seconds.
2. **Ask six onboarding questions.** One at a time. Each has a few quick-pick archetype options plus an "Other" option where you can type freely or paste a link. You can skip any question by picking Skip, or skip all by typing "skip all" at any point. The questions cover:
   - Who you are and your defence background.
   - What you sell into defence and who buys it.
   - Your wedge and positioning.
   - Your voice.
   - Your current priorities and engagements.
   - Your tool stack and attention drains.
3. **Offer a context drop.** One final question inviting you to paste links, upload files, or point at a local folder full of source material. The more you give it, the more personalised your vault will be. Skip if you'd rather start lean.
4. **Build your canonical pages.** Silently. The skill drafts content for your operator profile, organisation page, brand and strategy pages, email signature, and voice notes using the answers and corpus it collected.

When the skill finishes, it tells you where the vault was created and suggests opening it in Obsidian.

## Step 7 — Open your new vault in Obsidian

1. Launch Obsidian (if it's not already open).
2. Click "Open folder as vault".
3. Navigate to the folder Foothold created (default: `~/Obsidian/Foothold/`, or wherever you told it to install).
4. Click "Open".

Your vault is now live. You'll see the top-level folders (Capabilities and Services, Context, CRM, Daily, Ideas, Initiatives, Intelligence, Knowledge, Marketing, Operations, Resources, Skills) in the sidebar.

Start by opening `Context/<Your Name>.md` to check the operator profile reads well. Then `Context/<Your Organisation>.md`. The setup skill drafted these from your answers; revise anything that needs sharpening.

## What's next

Now you have a working vault, here are the things worth doing in the first hour:

1. **Read the per-folder Guides.** Each top-level folder has a `<Folder Name> Guide.md` at its root. The Guides are the contract for what belongs in each folder. Read Knowledge Guide, Operations Guide, Context Guide, and CRM Guide first; they're the load-bearing ones.
2. **Create your first daily note.** `Daily/<today's date>.md`. The Daily Guide tells you the convention.
3. **Add your first real contact.** The CRM already has Matt, Gabi, James, and inink as examples. Add someone you've met recently with the `/add-contact` skill (once available — landing in a future release).
4. **Connect Cowork to your vault.** In Cowork, point at your new vault folder. Now Cowork and Obsidian are working against the same files; agents you run in Cowork write into the vault, and you see them in Obsidian.

## Troubleshooting

**"Could not find marketplace MilUX-Ltd/foothold"** — Your GitHub auth probably isn't set up correctly. Re-run `gh auth status` and confirm you see a green tick. If you don't, run `gh auth login` again and choose HTTPS + browser auth.

**"Permission denied" when the install tries to clone** — Same issue as above. The most common cause is that you skipped the "authenticate Git with your credentials" step inside `gh auth login`. Run it again and pick Yes when asked.

**The install skill runs but no folder is created** — Check the path the skill chose. The default is `~/Obsidian/Foothold/`. If you don't see anything there, the bootstrap probably failed silently. Re-run `/foothold-setup` and watch for error output.

**Obsidian doesn't see the vault** — Make sure you point "Open folder as vault" at the Foothold root, not at a subfolder. The `.obsidian/` config sits at the root.

**The skill leaves `{{placeholder}}` text in files** — That's a bug. Tell Matt which files and where, and we'll fix the install skill.

**Anything else** — Email Matt at matt@milux.co.uk or open an issue at https://github.com/MilUX-Ltd/foothold/issues.

## Help

- Email: matt@milux.co.uk
- GitHub issues: https://github.com/MilUX-Ltd/foothold/issues
- LinkedIn: [Matt Odell](https://www.linkedin.com/in/mattodell/)
