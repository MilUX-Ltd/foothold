#!/usr/bin/env python3
"""MilUX session start: a Claude Code SessionStart hook. Version 0.1.3 (card 6494; 2 and 11 October 2026).

    python3 .claude/hooks/session_start.py     (matcher: startup|resume|clear)

Prints a short orientation to stdout, which Claude Code adds to the session's context:
the hook set version, the branch (with a warning if it is main), whether an UNLOCK is in
force, and the files a session reads before touching code. Never blocks. Standard library
only; Python 3.9 compatible.
"""

import json
import os
import subprocess
import sys


def sh(cmd, cwd):
    try:
        out = subprocess.run(
            cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10
        )
        return out.stdout.decode("utf-8", "replace").strip()
    except Exception:
        return ""


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {}
    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    hooks = os.path.join(root, ".claude", "hooks")
    try:
        with open(os.path.join(hooks, "VERSION")) as fh:
            version = fh.read().strip()
    except OSError:
        version = "unknown"
    branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], root) or "unknown"
    common = sh(["git", "rev-parse", "--git-common-dir"], root)
    gitdir = sh(["git", "rev-parse", "--git-dir"], root)
    in_worktree = bool(
        common
        and gitdir
        and os.path.realpath(os.path.join(root, common))
        != os.path.realpath(os.path.join(root, gitdir))
    )

    lines = []
    lines.append(
        f"MilUX agent hooks {version} active in {os.path.basename(root)} (card 6494). Refusals name the permitted route; the log is .claude/hooks/guard.log."
    )
    if branch in ("main", "master"):
        lines.append(
            f"WARNING: you are on {branch}. Take a worktree and a branch before any edit: git worktree add ../_workspaces/<repo>-<card> -b <type>/<card>-<slug> origin/main"
        )
    else:
        lines.append(
            "Branch: {}{}.".format(
                branch,
                " (own worktree)"
                if in_worktree
                else " (primary working tree; the repo's pre-commit guard may refuse an agent commit here)",
            )
        )
    unlock = os.path.join(hooks, "UNLOCK")
    if os.path.exists(unlock):
        try:
            with open(unlock) as fh:
                card = fh.read().strip() or "(empty, not an unlock)"
        except OSError:
            card = "(unreadable)"
        lines.append(
            f"UNLOCK is in force for card {card}: protected paths are editable this session. Remove .claude/hooks/UNLOCK when the change is on the pull request."
        )
    reads = []
    lessons = "LESSONS-INDEX.md" if os.path.exists(os.path.join(root, "LESSONS-INDEX.md")) else "LESSONS.md"
    for f in (lessons, "CONTEXT.md"):
        if os.path.exists(os.path.join(root, f)):
            reads.append(f)
    if reads:
        lines.append(
            "Read before touching code: {} (CLAUDE.md is already loaded). For recent movement use git log --oneline -20, not the whole CHANGELOG.md.".format(
                ", ".join(reads)
            )
        )
    lines.append(
        "Rules enforced here: no push to main, no force push, no tags, no merge or review by an agent, no deploys, no script from a URL, no unverified dependency (MILUX_ALLOW_INSTALL=<card> after verifying), no edit to workflows, CODEOWNERS, CLAUDE.md, .claude/, .githooks/ or the acceptance tests without an UNLOCK naming the card."
    )
    lines.append("Evidence: the CI run cited on the card. Your own test output has no standing.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
