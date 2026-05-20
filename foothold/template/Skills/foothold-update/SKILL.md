---
name: foothold-update
description: Pull the latest content from the public Foothold GitHub repo into the user's installed pack and reconcile it with anything they've edited locally. Compares each shipping file three ways — what was last pulled, what's currently on GitHub, and what the user has locally — and uses that to categorise files as in-sync / new / upstream-only-changed / locally-edited-only / conflicted. New and upstream-only files are added or updated. Conflicts are surfaced to the user with take-theirs / keep-mine / merge options. Use when the user says "update Foothold", "/foothold-update", "pull the latest from Foothold", "check for changes", "is there anything new in Foothold", "refresh my pack", "see if there are any updates", or any similar phrasing. Does NOT require plugin reinstall, marketplace sync, or terminal access.
---

# Foothold — Update (three-way reconcile)

USE WHEN the user wants to pull the latest content from the public Foothold repo into their installed pack, reconcile it with anything they've edited, and decide what to apply.

This skill fetches directly from the public GitHub repo at `MilUX-Ltd/foothold`. It does not rely on the local plugin install's template directory; that directory is only refreshed when the plugin upgrades, which is a slow path. Going to GitHub directly is fast and always current.

## What changed from earlier versions

Earlier versions of this skill were **additive only**: they fetched files that didn't exist locally and never touched anything that already did. That kept users' edits safe but meant they never got upstream updates to files they'd personalised.

This version does a **three-way reconcile** using GitHub blob SHAs:

- Every file shipped from Foothold is tracked in `.foothold/config.yml` under `last_known_shas:` — the GitHub blob SHA at the moment the file was last pulled to the user's vault.
- On each update run, the skill compares three SHAs per file: the last-known SHA (stored locally), the current remote SHA (from the GitHub tree API), and the locally-recomputed SHA (`git hash-object` equivalent on the current local content).
- The combination of those three tells the skill exactly what state each file is in, and what action is safe to take.

The user stays in control of every conflict.

## What this skill does

For every file in the latest `foothold/template/` directory on GitHub, work out which category it falls into and act:

| Category | Triggered by | Action |
|---|---|---|
| **NEW** | File doesn't exist in the vault yet | Add it (no prompt — it's net new) |
| **IN_SYNC** | Stored SHA == local SHA == remote SHA | Skip — nothing to do |
| **UPSTREAM_ONLY** | Stored SHA == local SHA, remote SHA different | Eligible for safe update — the user hasn't touched the file, upstream has changed. Apply by default, but show the list and let the user veto specific files |
| **LOCAL_ONLY** | Stored SHA == remote SHA, local SHA different | Skip — user has edited the file, no upstream change to bring |
| **CONVERGED** | Stored SHA differs from both, but local SHA == remote SHA | Update the stored SHA only — file content is already in sync, just the tracking is stale |
| **CONFLICT** | All three SHAs differ | Per-file prompt: take theirs / keep mine / merge |

Then report what was done.

## What this skill still does NOT do

- Does not delete files. If a file has been removed from the upstream template, the local copy stays.
- Does not re-run onboarding. Operator profile and personalised pages are left alone unless they show up as upstream changes the user explicitly accepts.
- Does not touch files outside the Foothold shipping set. Anything the user has added that wasn't in Foothold to begin with is untouched.

## Pre-flight

Confirm the user is in a Foothold pack:

- Look for `.foothold/config.yml` at the vault root (or at the user's chosen target if they specified one).
- If absent, tell the user: "This folder doesn't look like a Foothold pack. If you want to install Foothold here, run `/foothold-setup` first."
- If present, read:
  - The substitution values: `pack_owner`, `pack_owner_first`, `pack_owner_email`, `pack_owner_linkedin`, `pack_owner_phone`, `pack_org`, `pack_org_slug`, `pack_org_website`, plus today's date for `install_date`.
  - The current `last_known_shas:` map (may be empty on first-ever update run; treat missing as "no prior pull recorded").

## Step 1 — Fetch the latest file tree from GitHub

Call the GitHub tree API:

```
GET https://api.github.com/repos/MilUX-Ltd/foothold/git/trees/main?recursive=1
```

Use the WebFetch tool. Public repo, no auth required.

The response contains a `tree` array. Each entry has `path`, `type` (`blob` for files, `tree` for directories), and **`sha`** (the GitHub blob SHA — this is the value we'll compare).

Filter to entries where:

- `type == "blob"` (it's a file, not a directory)
- `path` starts with `foothold/template/`

These are the files that ship to the user's vault. Hold this list in memory along with each file's remote SHA.

## Step 2 — Compute current local SHAs

For each shipping file:

1. Compute the corresponding vault path. Strip the `foothold/template/` prefix from the GitHub path.
2. Apply placeholder substitution to the filename. For each `{{...}}` token in the filename, replace with the corresponding value from `.foothold/config.yml`.
3. Check if the file exists at that path in the user's vault.
4. If it exists, compute its **git-blob SHA** — same algorithm GitHub uses for blob hashes:

   ```
   sha1("blob " + str(len(content_bytes)) + "\0" + content_bytes)
   ```

   Use the Bash tool. Either:
   - `git hash-object <file>` if git is available
   - Or a Python one-liner:
     ```
     python3 -c 'import sys,hashlib;b=open(sys.argv[1],"rb").read();print(hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest())' "<path>"
     ```

   The result is the file's current local blob SHA — the same identifier GitHub uses.

5. Look up the **stored SHA** for this path in `.foothold/config.yml` under `last_known_shas:`. May be absent if the file was added before the SHA-tracking version of the skill landed, or on first-ever update run.

## Step 3 — Categorise each file

For each shipping file, using `stored = last_known_shas[path]`, `local = locally-computed SHA`, `remote = SHA from the GitHub tree`:

| Condition | Category |
|---|---|
| File doesn't exist locally | NEW |
| `stored == local == remote` | IN_SYNC |
| `stored == local` and `stored != remote` | UPSTREAM_ONLY |
| `stored == remote` and `stored != local` | LOCAL_ONLY |
| `stored != local` and `stored != remote` and `local == remote` | CONVERGED |
| `stored != local` and `stored != remote` and `local != remote` | CONFLICT |

Special case: if `stored` is missing (first run after the SHA-tracking version, or a file that was added by an earlier additive-only run), treat as if `stored == local` for the purpose of categorisation. The file is considered "as-pulled" — IN_SYNC if `local == remote`, UPSTREAM_ONLY otherwise.

## Step 4 — Present the summary and ask the user

Show a summary, then ask the user how to proceed:

```
Foothold update — what changed since your last pull:

  N new files          (will be added automatically)
  M upstream-only      (your file matches what was pulled; safe to update)
  K conflicts          (you've edited these AND upstream has new changes)
  X local-only edits   (you've edited; no upstream change — nothing to do)
  Y already in sync    (no action)
```

Then use the AskUserQuestion tool with these questions, in this order, only asking the ones that are relevant:

1. **If M > 0:** "Apply the M upstream-only updates?"
   - Options: Apply all (recommended) / Review each individually / Skip all
2. **If K > 0:** Run through the conflict list one-by-one. For each:
   - Show the file path.
   - Show a short diff summary (you can use the Bash tool to compute one — `diff` between the current local file and a temp file containing the freshly-fetched remote content).
   - Ask: Take theirs (overwrite local) / Keep mine (skip) / Merge (show me both versions and help me combine).

If the user picks **Merge** on a conflict, Claude is exactly the right tool to drive it: read both versions, identify which sections the user changed vs which sections upstream changed, propose a merged version that keeps both sets of changes where they don't overlap, and ask the user to confirm before writing.

## Step 5 — Apply changes

For each file the user has agreed to update or add:

1. Fetch the raw remote content from GitHub:

   ```
   GET https://raw.githubusercontent.com/MilUX-Ltd/foothold/main/<full-path>
   ```

   Use the WebFetch tool. The full path is the original GitHub path including the `foothold/template/` prefix. Public repo, no auth required.

2. Apply placeholder substitution to the content. For each `{{...}}` token in the body, replace with the corresponding value from `.foothold/config.yml`.

3. Create any missing parent directories at the target path.

4. Write the file to the target vault path.

For each file in CONVERGED (no content change needed, just stale tracking): no write needed.

## Step 6 — Update `.foothold/config.yml`

After all files are processed, update the config file. For every shipping file that's now in the user's vault (NEW that was added, IN_SYNC, CONVERGED, UPSTREAM_ONLY that was applied, CONFLICT where the user took theirs, CONFLICT where the user kept mine, CONFLICT where the user merged), set:

```yaml
last_known_shas:
  <vault-relative path>: <SHA the user now has locally>
```

That is:

- For NEW that was just added → remote SHA.
- For IN_SYNC → unchanged.
- For UPSTREAM_ONLY that was applied → remote SHA.
- For UPSTREAM_ONLY the user vetoed → unchanged (still the stored SHA; user gets reminded next run).
- For LOCAL_ONLY → leave as the existing stored SHA (we still record the "as-pulled" baseline).
- For CONVERGED → update to remote SHA (= local SHA, since they match).
- For CONFLICT take-theirs → remote SHA.
- For CONFLICT keep-mine → unchanged.
- For CONFLICT merge → re-compute the merged file's SHA locally and record that. The merged result is a new baseline; next run, if upstream changes again, it'll be a fresh comparison from this point.

Also update:

```yaml
foothold:
  version: <fetched from foothold/.claude-plugin/plugin.json at the latest commit>
  last_synced: <today's ISO date>
  # everything else preserved
```

## Step 7 — Report

Tell the user, in this order:

1. **One-line summary**: e.g. "Foothold update complete. Added 3, updated 5, merged 1, skipped 2 conflicts, 207 already in sync."
2. **Added** — paths grouped by top-level folder.
3. **Updated (upstream-only)** — paths the user approved.
4. **Merged** — paths where the user chose merge, with a one-line note on what was integrated.
5. **Skipped conflicts** — paths the user chose to keep their own version of. Tell them they can re-run later to bring upstream in.
6. **Skipped LOCAL_ONLY** — paths the user has edited where there's no upstream change. Mostly silent unless the user wants to see the list.
7. **Worth a look** — three to five paths from the added / updated set that are most likely to be useful (new Guides, new defence-landscape entities, new skills, new acronyms, new programme pages).

If nothing changed at all:

```
No changes. Your pack is in sync with Foothold version <version> as of <today>.
```

## Failure modes

- **GitHub API rate limit hit.** Unauthenticated requests are limited to 60 per hour per IP. The skill makes one tree-API call plus one raw-content fetch per file that needs to be added or updated. If the limit hits during the per-file fetch phase, stop, report what was applied so far, persist `last_known_shas:` for those files, and tell the user to retry in an hour. Partial progress is preserved.
- **GitHub down or repo unreachable.** Report that, do not write anything.
- **A specific file fetch fails mid-run.** Skip it, record it in a "failed" list at the end of the report, continue with the rest. Do not abort the whole run on one file failure.
- **`.foothold/config.yml` malformed.** Report the problem and ask the user to confirm the substitution values before continuing. Do not guess.
- **`git hash-object` and Python both unavailable.** Fall back to the additive-only behaviour for that run (categorise only NEW vs not-NEW; can't safely categorise the rest). Tell the user.

## Guidelines

- The user is always in control of conflicts. Never overwrite an edited file without explicit consent.
- Be honest about what's safe and what's risky in the summary. UPSTREAM_ONLY is genuinely safe (user hasn't touched the file). CONFLICT genuinely isn't safe to auto-resolve.
- For merge, propose a concrete merged version and ask for confirmation before writing — don't ask the user to merge mentally.
- Public repo, no auth — keeps the skill simple.
- Placeholder substitution runs on every new or updated file (filename and body).
- The `last_known_shas:` map is the single source of truth for tracking. Keep it tidy: only the paths that actually ship from Foothold, no orphans.
- Report concisely. Lead with the one-line summary, then the action lists, then "worth a look".
- If nothing changed, say so plainly. "Your pack is in sync" is a good outcome.
