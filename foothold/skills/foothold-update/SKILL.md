---
name: foothold-update
description: Pull new content from the Foothold plugin into an existing installed pack without re-running the onboarding interview. Adds new files from the latest plugin template to your vault and leaves anything you've edited or written yourself untouched. Use when the marketplace has been updated and you want the new content to land in your vault, or when the user says "update foothold", "pull foothold updates", or runs /foothold-update.
---

# Foothold — Update

USE WHEN the user runs `/foothold-update` or asks to pull new content from the Foothold plugin into their existing pack.

This skill is for content updates after install. It does not re-run the interview, does not overwrite anything you've edited, and does not delete files.

## What this skill does

For every file in the latest plugin template:

- **If the file does not yet exist in your vault:** copy it in. Run placeholder substitution. Report it as added.
- **If the file already exists in your vault:** leave it alone. Whatever you (or earlier you) wrote stays.

Then update `.foothold/config.yml` to record the new sync.

## What this skill does NOT do

- It does not overwrite existing files. If you want to refresh a file you've previously edited, delete the local copy first, then re-run `/foothold-update`.
- It does not delete files. If the template no longer ships a file, your local copy stays.
- It does not re-run the onboarding interview. Your operator profile and personalised pages are left alone.
- It does not merge conflicting edits. Three-way merge is a v1.1 feature; for now, the rule is "additions only".

## Pre-flight

Check the target directory.

- If `.foothold/config.yml` is missing, this is not a Foothold-installed pack. Tell the user: "This folder doesn't look like a Foothold pack. If you want to install Foothold here, run `/foothold-setup` instead."
- If `.foothold/config.yml` is present, read it. Capture the current `pack_owner`, `pack_org`, and other substitution values. You'll need these for placeholder substitution on copied files.

## Method

### Step 1: Resolve plugin bundle paths

This SKILL.md lives at `skills/foothold-update/SKILL.md` inside the Foothold plugin bundle. The latest templated vault content lives at `template/` at the plugin root.

```bash
# Find the Foothold plugin root.
find / -type d -name "foothold" -path "*/plugins/*" 2>/dev/null | head -1
```

Cache the result. The template content is at `<plugin_root>/template/`.

### Step 2: Walk the template and detect additions

For every file under `<plugin_root>/template/` (including hidden files like `.obsidian/`), compute the corresponding target path:

```
<plugin_root>/template/Context/Brand.md  →  <target>/Context/Brand.md
<plugin_root>/template/CRM/organisations/defence companies/MilUX.md  →  <target>/CRM/organisations/defence companies/MilUX.md
```

Apply placeholder substitution to the target path (filenames containing `{{...}}` get substituted using the values from `.foothold/config.yml`).

Check whether the target file exists.

### Step 3: Copy additions, skip existing

For each template file:

- **If the target file does not exist:** copy the template file to the target path. Run placeholder substitution on the file contents (every `{{...}}` token gets substituted using `.foothold/config.yml` values). Record the path as "added".
- **If the target file exists:** skip it. Record the path as "skipped (existing)".

Create any missing parent directories along the way.

### Step 4: Update `.foothold/config.yml`

After all files are processed, update the config file:

```yaml
foothold:
  installed_at: <unchanged>
  version: <new version from plugin's manifest>
  last_synced: <today's ISO date>
  pack_name: <unchanged>
  pack_slug: <unchanged>
  pack_owner: <unchanged>
  pack_owner_email: <unchanged>
  pack_org: <unchanged>
  pack_org_slug: <unchanged>
  pack_org_website: <unchanged>
```

Only the `version` and `last_synced` fields change. Everything else is preserved.

### Step 5: Report

Tell the user:

- One-line summary: "Updated Foothold. Added N file(s). Skipped M existing files."
- List of paths added, grouped by top-level folder. Skip the list if N is zero.
- If any added files were canonical pages the user might want to review (e.g. new Guide pages, new CRM contacts, new Intelligence reference content), call them out at the bottom: "Worth a look:" and list 3-5 of the most useful additions.

Example output:

```
Updated Foothold. Added 1 file. Skipped 47 existing files.

Added:
- CRM/organisations/defence companies/MilUX.md

Worth a look:
- CRM/organisations/defence companies/MilUX.md (new reference page for MilUX, the Foothold maintainer)
```

## Guidelines

- Additive only. Never overwrite, never delete.
- Placeholder substitution runs on every new file, so the user's name, organisation, and email get filled in correctly in newly-added content.
- Report concisely. Single one-line summary, list of added paths, optional "worth a look" pointer at the most useful new content.
- If nothing was added, say "No new content. Your pack is up to date as of <date of last sync on plugin side>."
