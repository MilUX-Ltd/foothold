---
type: guide
status: active
created: 2026-07-02
last_reviewed: 2026-07-02
tags: [sync, backup, ways-of-working]
---

# Sync and Backup

Two different problems, often confused. **Sync** puts the same vault on your other devices. **Backup** lets you recover when something goes wrong, including when sync cheerfully replicates a mistake to every device you own. You need an answer to both before this vault becomes irreplaceable, which is roughly week two.

## Sync options

**Obsidian Sync** (paid, around £8 a month). The simplest answer and the only one that handles mobile properly with no ceremony. End-to-end encrypted, selective sync, works on iOS and Android. If you are small and busy, buy this and move on.

**Git** (free). A repository on GitHub or similar, with the vault as the working tree. You get version history and diffs as well as sync, which for a knowledge vault is genuinely valuable: every change is recoverable. The cost is setup and the occasional merge conflict. Best on desktop; mobile git sync is possible but fiddly. If you or Cowork are comfortable with git, this is the strongest free option, and Cowork can set it up for you.

**iCloud Drive** (free tier, Apple only). Put the vault in iCloud and Obsidian on Mac, iPhone and iPad sees it. Genuinely easy, with two caveats: iCloud can lag or produce "conflicted copy" files if you edit on two devices in quick succession, and files can be evicted from local storage at inconvenient moments. Acceptable for a single-person, mostly-one-device pattern.

**OneDrive, Dropbox, Google Drive** (free tiers). All workable on desktop: put the vault in the synced folder and let the client do its thing. Same conflict caveat as iCloud, and one hard limitation: **Obsidian on iOS cannot open a vault from these drives directly**, so your phone becomes read-nothing unless you add another tool. Fine if mobile access does not matter to you; if it does, use Obsidian Sync or iCloud.

**Syncthing or a NAS** (free, self-hosted). Peer-to-peer sync with nothing in anyone's cloud. The right answer for the privacy-first, and the most setup of any option here.

## Choosing

- Mobile access matters and you value your time: **Obsidian Sync**.
- Version history matters, comfortable with git or happy to let Cowork drive: **git**.
- All-Apple, one main device, minimal cost: **iCloud**.
- Desktop-only and already living in OneDrive/Dropbox/Google Drive: use what you have, accept the mobile gap.

## Backup, regardless of sync

Sync is not backup. A deletion syncs just as faithfully as an edit.

- **If you chose git**, history is your backup; push regularly and you are covered.
- **Otherwise**, two cheap habits: keep your machine's own backup running (Time Machine or File History includes the vault), and once a month zip the vault folder somewhere separate (a different cloud drive counts). Cowork can do the zip on a schedule if you ask.
- **Test one restore.** A backup you have never restored from is a hope, not a backup. Pull one file out of your history or archive once, so you know the path works.

## One warning

Never point two sync systems at the same vault folder (for example iCloud and git together without care, or Obsidian Sync plus Dropbox). Sync systems fight, and the loser is your notes.
