# Lessons

Mistakes already paid for on this pack, so nobody pays for them twice: what happened, why, and
the rule that came out of it. `LESSONS-INDEX.md` lists them one line each; regenerate it with
`python3 Workspace/agent-config/scripts/lessons-index.py <repository>` in the same commit.
`tools/check.py` fails when the two are out of step.

1. **A synced vault copy pushed by a timer is not a source** (card 7020)
   Until September 2026 the pack was edited in an Obsidian vault and a launchd job committed
   whatever it found and pushed it to `main` every four hours, with an `auto:` message. When the
   Macs were reorganised on 29 September the job's paths vanished and it stopped without a
   word; the vault copy carried on under synoia in `Open/Packs` for two weeks with nothing
   publishing it. Nothing was lost only because no one had edited it. Rule: GitHub is the only
   source (ADR 001). Work in a clone, change by pull request, and never reintroduce a sync job.

2. **The timer published a local index to a public repository** (card 7020)
   The job ran `git add -A`, so synoia's local index of the folder, `.context/index.sqlite`
   (a full-text copy of the notes with sync identifiers), was committed and pushed with
   everything else. Rule: `.context/` is ignored and `tools/check.py` refuses it, with the other
   local files (Obsidian workspace state, `.trash/`, `.DS_Store`, database files). Add files by
   name, not with `git add -A` over a folder something else also writes to.

3. **Setup fetched the template as JSON it could not read** (Foothold 2.1.0)
   `foothold-setup` listed the template through the GitHub `git/trees` API, which returns JSON
   that the Cowork WebFetch tool cannot read. The file list came back empty and the install
   stalled before writing anything, while single raw-file fetches worked and hid the cause.
   Rule: setup installs from the template bundled in the plugin, offline; only the update skill
   talks to GitHub. The documented install has not been proven against this since (risk R5).

4. **The plugin version drifted from the changelog** (Foothold 2.1.0)
   The plugin manifest sat at 2.0.0 while the changelog ran to 2.0.2, and the marketplace entry
   was still at 2.0.0 when 2.1.0 shipped. Rule: a release moves `CHANGELOG.md`, `plugin.json`
   and `marketplace.json` together; `tools/check.py` fails when they disagree.
