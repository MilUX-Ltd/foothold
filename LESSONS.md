# Lessons

Mistakes already paid for on this pack, so nobody pays for them twice: what happened, why, and
the rule that came out of it. `LESSONS-INDEX.md` lists them one line each and must change in the
same commit; `tools/check.py` fails when the two are out of step.

1. **A working copy pushed on a timer is not a source** (October 2026)
   For a time the pack was edited in a separate working copy and pushed to `main` by a scheduled
   job. When the job stopped, nothing said so, and for two weeks there were two copies with no
   rule about which one won. Rule: this repository is the only source (ADR 001). Change it in a
   clone, by pull request, and never reintroduce a scheduled push.

2. **A scheduled `git add -A` published a local index** (October 2026)
   The scheduled job added everything in the folder, so a desktop sync tool's local index
   (`.context/index.sqlite`, a full-text copy of the notes) was committed along with the pack.
   Rule: `.context/` is ignored and `tools/check.py` refuses it, with the other local files
   (Obsidian workspace state, `.trash/`, `.DS_Store`, database files). Add files by name.

3. **Setup fetched the template as JSON it could not read** (Foothold 2.1.0)
   `foothold-setup` listed the template through the GitHub `git/trees` API, which returns JSON
   that the Cowork WebFetch tool cannot read. The file list came back empty and the install
   stalled before writing anything, while single raw-file fetches worked and hid the cause.
   The 2.1.0 fix made setup read a template bundled in an installed plugin, but 1.6.0 had
   already removed the plugin install in favour of one prompt, so the fix swapped one broken
   route for another (risk R5). Rule: setup and update fetch plain files by raw URL, never JSON
   through WebFetch; check any change to setup against the one-prompt design in
   `docs/architecture.md` before it ships.

4. **The plugin version drifted from the changelog** (Foothold 2.1.0)
   The plugin manifest sat at 2.0.0 while the changelog ran to 2.0.2, and the marketplace entry
   was still at 2.0.0 when 2.1.0 shipped. Rule: a release moves `CHANGELOG.md`, `plugin.json`
   and `marketplace.json` together; `tools/check.py` fails when they disagree.
