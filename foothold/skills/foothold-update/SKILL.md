---
name: foothold-update
description: Pull new content from the public Foothold GitHub repository into the user's installed pack. Fetches the latest file tree from GitHub directly, compares to the user's vault, and adds any files that are new. Never overwrites existing files. Use when the user says "update Foothold", "/foothold-update", "pull the latest from Foothold", "check the Foothold repo for changes", "is there anything new in Foothold", "refresh my pack", "see if there are any updates", or any similar phrasing. Does NOT require plugin reinstall, marketplace sync, or terminal access.
---

# Foothold — Update (GitHub fetch)

USE WHEN the user wants to pull the latest content from the public Foothold repo into their installed pack, without re-running setup and without touching the plugin install mechanism.

This skill fetches directly from the public GitHub repo at `MilUX-Ltd/foothold`. It does not rely on the local plugin install's template directory; that directory is only refreshed when the plugin upgrades, which is a slow path. Going to GitHub directly is fast and always current.

## What this skill does

For every file in the latest `foothold/template/` directory on GitHub:

- **If the file does not yet exist in the user's vault:** fetch the raw content, run placeholder substitution, write it in.
- **If the file already exists in the user's vault:** leave it alone.

Then report what was added.

## What this skill does NOT do

- Does not overwrite existing files. If the user wants to refresh a file they've edited, they delete the local copy first, then re-run.
- Does not delete files. If a file has been removed from the upstream template, the local copy stays.
- Does not re-run onboarding. Operator profile and personalised pages are left alone.

## Pre-flight

Confirm the user is in a Foothold pack:

- Look for `.foothold/config.yml` at the vault root (or at the user's chosen target if they specified one).
- If absent, tell the user: "This folder doesn't look like a Foothold pack. If you want to install Foothold here, run `/foothold-setup` first."
- If present, read the substitution values: `pack_owner`, `pack_owner_first`, `pack_owner_email`, `pack_owner_linkedin`, `pack_owner_phone`, `pack_org`, `pack_org_slug`, `pack_org_website`, plus today's date for `install_date`. These will be substituted into any new files copied in.

## Step 1 — Fetch the latest file tree from GitHub

Call the GitHub tree API:

```
GET https://api.github.com/repos/MilUX-Ltd/foothold/git/trees/main?recursive=1
```

Use the WebFetch tool. Public repo, no auth required.

The response contains a `tree` array. Each entry has `path`, `type` (`blob` for files, `tree` for directories), and `sha`.

Filter the entries to those where:

- `type == "blob"` (it's a file, not a directory)
- `path` starts with `foothold/template/`

These are the files that ship to the user's vault.

## Step 2 — Identify what's missing locally

For each shipping file:

1. Compute the corresponding vault path. Strip the `foothold/template/` prefix from the GitHub path.
   - Example: `foothold/template/Knowledge/rules.md` → `Knowledge/rules.md`.
2. Apply placeholder substitution to the filename. For each `{{...}}` token in the filename, replace with the corresponding value from `.foothold/config.yml`.
   - Example: `foothold/template/Context/{{pack_owner}}.md` → `Context/Jane Smith.md` (where `pack_owner: Jane Smith`).
3. Check if the file exists at that path in the user's vault. Use the Read tool with offset=0/limit=1 (or Glob); the cheapest way to check existence.
4. If the file does NOT exist, mark it for fetch. If it does, skip it.

## Step 3 — Fetch and write missing files

For each missing file:

1. Fetch the raw content from GitHub:

   ```
   GET https://raw.githubusercontent.com/MilUX-Ltd/foothold/main/<full-path>
   ```

   Use the WebFetch tool. The full path is the original GitHub path (including the `foothold/template/` prefix). Public repo, no auth required.

2. Apply placeholder substitution to the content. For each `{{...}}` token in the body, replace with the corresponding value from `.foothold/config.yml`.

3. Create any missing parent directories at the target path.

4. Write the file to the target vault path.

5. Record the path as "added".

## Step 4 — Update `.foothold/config.yml`

After all files are processed, update the config file with the new sync date:

```yaml
foothold:
  installed_at: <unchanged>
  version: <fetched from foothold/.claude-plugin/plugin.json at the latest commit>
  last_synced: <today's ISO date>
  pack_name: <unchanged>
  pack_slug: <unchanged>
  pack_owner: <unchanged>
  pack_owner_email: <unchanged>
  pack_org: <unchanged>
  pack_org_slug: <unchanged>
  pack_org_website: <unchanged>
```

Only `version` and `last_synced` change. Everything else is preserved.

## Step 5 — Report

Tell the user:

- One-line summary: "Updated Foothold. Added N file(s). Skipped M existing files." (Drop the "skipped" count if everything was new.)
- List of paths added, grouped by top-level folder. If N is zero, say: "No new content. Your pack is already up to date as of the latest published version."
- If any added files were canonical reference pages worth a look (new Guide, new defence-landscape entity, new skill), call out three to five at the bottom under "Worth a look:"

Example output when there are new files:

```
Updated Foothold. Added 3 files. Skipped 95 existing files.

Added:
- Intelligence/defence-landscape/Frameworks/<new framework>.md
- Resources/Reference/<new reference>.md
- Skills/<new skill>/SKILL.md

Worth a look:
- Intelligence/defence-landscape/Frameworks/<new framework>.md — new procurement framework reference page
- Skills/<new skill>/SKILL.md — try this in Cowork once it's synced
```

Example output when there's nothing new:

```
No new content. Your pack is already up to date with the latest Foothold (version <version>, checked <today>).
```

## Failure modes

- **GitHub API rate limit hit.** Unauthenticated requests are limited to 60 per hour per IP. If the user has run this skill many times in the last hour, the rate limit can hit during the per-file fetch phase. If so, stop, report which files were added before the limit hit, and tell the user to retry in an hour.
- **GitHub down or repo unreachable.** Report that, do not write anything.
- **A specific file fetch fails.** Skip it, record it in a "failed" list at the end of the report, continue with the rest. Do not abort the whole run on one file failure.
- **`.foothold/config.yml` malformed.** Report the problem and ask the user to confirm the substitution values before continuing. Do not guess.

## Guidelines

- Additive only. Never overwrite, never delete.
- Always fetch from GitHub, never from the local plugin install's template directory. The whole point of this skill is to bypass the plugin-refresh round trip.
- Public repo, no auth — keeps the skill simple.
- Placeholder substitution runs on every new file (filename and body).
- Report concisely. Lead with the one-line summary, then the list of added paths, then the "worth a look" pointer at the most useful new content.
- If nothing was added, say so plainly. "Your pack is up to date" is a perfectly good outcome.
