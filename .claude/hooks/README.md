# MilUX agent hooks

Version 0.1.3, 11 October 2026, card 6494. Master copy: `~/Argos/.claude/hooks/`, deployed
into each product repository's `.claude/hooks/` by `~/Argos/bin/deploy-claude-hooks.sh`; the
repository's `.claude/settings.json` wires them in. Edit the master, bump `VERSION`, redeploy.

What runs, and when:

| Hook | Event | Does |
|---|---|---|
| `session_start.py` | SessionStart | Prints the branch, warns on `main`, says whether an UNLOCK is in force, names the files to read first. Never blocks. |
| `guard.py pre-bash` | PreToolUse, Bash | Refuses pushes to `main`, force and bulk pushes, tags, `gh pr merge` and `gh pr review`, GitHub API writes, deploys, release builds and registry publishing, scripts fetched from the network, unverified dependency installs, and shell writes into protected paths. Follows `cd`, `bash -c`, `eval`, subshells and wrappers such as `sudo` and `timeout`. |
| `guard.py pre-edit` | PreToolUse, Edit, Write, MultiEdit, NotebookEdit | Refuses edits to protected paths. |
| `post_edit.py` | PostToolUse, Edit, Write, MultiEdit | Syntax or lint check on the edited file; a failure comes back to the agent. Silent on success. |

A refusal always names the permitted route. Two overrides exist and both are logged:
`MILUX_ALLOW_INSTALL=<card number>` written immediately in front of an install command, after the
package has been verified on the real registry and recorded on the card (a value that is not a
card number, or one placed anywhere else in the command, does not count); and a file `UNLOCK` in
this directory holding a card number, written by Matt for the session, which permits edits to
protected paths for a change that card names. Remove `UNLOCK` when the change is on the pull
request. Neither override is the agent's to create: `UNLOCK` sits inside a protected path and the
guard refuses the shell writes that would create it, including after a `cd`.

Protected paths are the defaults in `guard.py` plus the lines in `protected-paths.txt`, which is
where a repository declares the directory that holds its committed acceptance tests. Matching is
case-insensitive because the Macs run a case-insensitive file system.

`python3 .claude/hooks/test_guard.py` runs the acceptance tests for every rule above against a
throwaway repository. The deploy script runs them before it commits.

`ruff.toml` beside the scripts is their own lint and format configuration. Ruff applies the closest
configuration to each file, so a repository that runs `ruff check .` or `ruff format --check .`
over its whole tree judges the hooks by this file and its own code by its own; 0.1.0 had no such
file and went red in southcentralrdsc's CI for that reason. The hook set passes `ruff check` and
`ruff format --check` under it.

0.1.3 (11 October 2026): two gaps closed in `guard.py`, found in a product session. **A worktree of the project is the project:** paths were judged against the project folder alone, so in a git worktree outside it (where card work happens) no protected path was protected; now a path in any worktree of the same repository is judged against that worktree, and every worktree's `protected-paths.txt` counts. **A program is read:** a program run through python, node, perl or ruby (a heredoc, `-c` or `-e` text, or a script file named on the line) that writes files and names a protected path as a string of its own is refused as a shell write would be; a shell heredoc (`bash <<EOF`) is judged as commands. A path inside a sentence does not count. Also fixed: `session_start.py` had kept the lines 0.1.2 replaced and did not run. New acceptance test `test_worktrees_and_programs`, red on 0.1.2's guard.

0.1.2 (2 October 2026): `session_start.py` names `LESSONS-INDEX.md` where a repository has one and points to `git log` rather than the whole changelog; `settings.template.json` sets Sonnet 5 as the repository default model and `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` for sub-agents that name no model (an agent's own `model:` line and a model named in the call still win). Guard rules and acceptance tests unchanged.

0.1.1 (13 September 2026): ruff.toml added, sources formatted by ruff and cleaned under E, F, I, B,
UP and SIM; no change in behaviour, every acceptance test unchanged and passing.

## The log

Every refusal, override and fault is appended to `.claude/hooks/guard.log` (gitignored) and
mirrored to `~/.milux/guard/<repository>.log`, which survives a `git clean -fdx`. Values of
`KEY=value` words and common token shapes are redacted before writing, so a command that carried a
secret does not put it in the log.

## Failure modes, stated

- Unreadable hook input allows and logs a NOTE: the guard refuses on evidence, never on doubt.
- An internal fault allows, logs a FAULT and prints a line telling the agent to tell Matt (exit 1).
- If `python3` is missing, the hooks never run and nothing says so beyond the SessionStart line
  being absent. If `guard.py` is missing, every Bash and Edit call is refused, which looks like a
  broken session; redeploy the hook set.
- `post_edit.py` parses Python with `.venv/bin/python` when the repository has one, otherwise
  with the interpreter running the hook (3.9 on the Mac Mini), so newer syntax can be reported
  as an error there; JavaScript is checked only where `node` is on the PATH; TypeScript only
  where an eslint config exists.
- A hook that exceeds its timeout (20 seconds; 90 for post-edit) is treated by Claude Code as
  allowing.

## Known limits, by design

The guard reads commands, not intent. The layers behind it are branch protection with required
checks, CODEOWNERS and the pull-request review. It does not see: code run through an interpreter
(`python3 -c`, `node -e`, `perl -e`) or a shell fed from a string or a file (`echo '...' | bash`,
`bash <<< '...'`, `bash script.sh`, `source x.sh`); shell variables, command substitution and process
substitution that resolve at run time (`git push origin $BRANCH`, `> >(tee file)`); `xargs`, `find -exec`, archives and patches that write
files; raw HTTP calls to the GitHub API with a token read from the keychain; `.git/hooks/`
written directly; branches other than `main` and `master`; a deploy tool, package runner or
piped interpreter it does not know by name (`deno`, `pwsh`, `gcloud`, `vercel`); a subcommand of a
known tool it does not list; a scripted editor (`ed`, `ex`); or a tag created by a route it does
not watch and pushed under a name that neither looks like a version nor exists locally at hook
time. Where it is unsure whether a write lands on a protected path (a wildcard beside one, a
`cd` it cannot follow), it refuses and asks for the files by name.
