#!/usr/bin/env python3
"""MilUX post-edit check: a Claude Code PostToolUse hook. Version 0.1.1 (card 6494).

    python3 .claude/hooks/post_edit.py      (matcher: Edit|Write|MultiEdit)

After an edit, run the cheapest deterministic check the file type allows and feed a failure
back to the agent (exit 2, message on stderr). Success is silent. This is the fast sensor;
the full suite runs in CI, which is the only evidence that counts on the card.

Checks by extension:
  .py            a parse with the project's interpreter (.venv/bin/python if present, else this one), then ruff check if ruff is on PATH
  .sh .bash      bash -n
  .json          json.load (JSONC files are exempt: tsconfig*, jsconfig, .vscode/*, devcontainer, *.jsonc)
  .js .mjs .cjs  node --check if node is on PATH
  .ts .tsx       eslint via npx --no-install if the project has it; otherwise skipped
  .toml          tomllib (Python 3.11+) or skipped
Anything else is skipped. Each check has a 60 second limit; a timeout is reported, not hidden.
Standard library only; Python 3.9 compatible.
"""

import json
import os
import shutil
import subprocess
import sys

VERSION = "0.1.1"
TIMEOUT = 60


def run(cmd, cwd):
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=TIMEOUT
        )
        return proc.returncode, proc.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {TIMEOUT}s: {' '.join(cmd)}"
    except OSError:
        return 0, ""  # tool not runnable here: skip, do not fail the edit


def fail(path, output):
    sys.stderr.write(f"MilUX post-edit check failed for {path}\n{output.strip()[:4000]}\n")
    sys.exit(2)


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        return
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    if not isinstance(path, str) or not os.path.isfile(path):
        return
    root = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    ext = os.path.splitext(path)[1].lower()
    rel = os.path.relpath(path, root) if os.path.isabs(path) else path

    if ext == ".py":
        interp = sys.executable
        for cand in (
            os.path.join(root, ".venv", "bin", "python"),
            os.path.join(root, "venv", "bin", "python"),
        ):
            if os.path.exists(cand):
                interp = cand
                break
        code, out = run(
            [
                interp,
                "-c",
                "import ast,sys; ast.parse(open(sys.argv[1], encoding='utf-8').read(), sys.argv[1])",
                path,
            ],
            root,
        )
        if code != 0:
            fail(rel, out)
        if shutil.which("ruff"):
            code, out = run(["ruff", "check", "--quiet", path], root)
            if code not in (0,) and out.strip():
                fail(rel, out)
    elif ext in (".sh", ".bash"):
        code, out = run(["bash", "-n", path], root)
        if code != 0:
            fail(rel, out)
    elif ext == ".json":
        base = os.path.basename(path).lower()
        if (
            base.startswith("tsconfig")
            or base
            in (
                "jsconfig.json",
                "devcontainer.json",
                "settings.json",
                "launch.json",
                "extensions.json",
            )
            and ".vscode" in path.replace(os.sep, "/")
            or "/.vscode/" in path.replace(os.sep, "/")
            or "/.devcontainer/" in path.replace(os.sep, "/")
        ):
            return
        try:
            with open(path, encoding="utf-8") as fh:
                json.load(fh)
        except ValueError as exc:
            fail(rel, f"invalid JSON: {exc}")
    elif ext in (".js", ".mjs", ".cjs"):
        if shutil.which("node"):
            code, out = run(["node", "--check", path], root)
            if code != 0:
                fail(rel, out)
    elif ext == ".jsonc":
        return
    elif ext in (".ts", ".tsx"):
        has_eslint = any(
            os.path.exists(os.path.join(root, f))
            for f in (
                "eslint.config.js",
                "eslint.config.mjs",
                "eslint.config.cjs",
                ".eslintrc",
                ".eslintrc.js",
                ".eslintrc.cjs",
                ".eslintrc.json",
                ".eslintrc.yml",
            )
        )
        if has_eslint and shutil.which("npx"):
            code, out = run(["npx", "--no-install", "eslint", "--max-warnings=0", path], root)
            if (
                code not in (0,)
                and "command not found" not in out
                and "could not determine executable" not in out.lower()
            ):
                fail(rel, out)
    elif ext == ".toml":
        try:
            import tomllib  # Python 3.11+
        except ImportError:
            return
        try:
            with open(path, "rb") as fh:
                tomllib.load(fh)
        except Exception as exc:
            fail(rel, f"invalid TOML: {exc}")


if __name__ == "__main__":
    main()
