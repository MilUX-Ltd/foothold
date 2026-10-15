#!/usr/bin/env python3
"""check.py: the repository's gate.

Runs on every pull request and on main (.github/workflows/checks.yml), and locally before a
commit. Standard library only, Python 3.9 or later. Exit 0 when every check passes, 1 otherwise.

    python3 tools/check.py

What it checks, and why (the reasons are in LESSONS.md and docs/adr/):

1. Nothing local is tracked: a sync tool's local index (.context/), Obsidian's
   per-user workspace state, the Obsidian trash, macOS .DS_Store files, SQLite files.
2. Every tracked JSON file parses.
3. No tracked text file outside .claude/ carries an absolute home-folder path (/Users/...).
4. The versions agree: the newest released heading in CHANGELOG.md, the plugin manifest and
   the marketplace entry, where the repository has them.
5. LESSONS-INDEX.md is in step with LESSONS.md.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN = [
    (re.compile(r"(^|/)\.context/"), "a sync tool's local index (LESSONS 2)"),
    (re.compile(r"(^|/)\.obsidian/(workspace[^/]*\.json|cache[^/]*)$"), "Obsidian per-user state"),
    (re.compile(r"(^|/)\.trash/"), "the Obsidian trash"),
    (re.compile(r"(^|/)\.DS_Store$"), "a macOS .DS_Store file"),
    (re.compile(r"\.(sqlite|sqlite3|db)$"), "a database file"),
]
HOME_PATH = re.compile(r"/Users/[A-Za-z0-9._-]+/")
RELEASED = re.compile(r"^## (\d+\.\d+\.\d+)\b", re.M)
LESSON = re.compile(r"^(\d+)\. \*\*(.+?)\*\*(?:\s*\(([^)]*)\))?", re.M)

failures = []


def fail(message):
    failures.append(message)


def tracked():
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode()
    return [p for p in out.split("\0") if p]


def read_text(path):
    try:
        return (ROOT / path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return None


def check_forbidden(files):
    for path in files:
        for pattern, what in FORBIDDEN:
            if pattern.search(path):
                fail(f"{path}: {what} must not be tracked")


def check_json(files):
    for path in files:
        if path.endswith(".json"):
            try:
                json.loads((ROOT / path).read_text(encoding="utf-8"))
            except (ValueError, UnicodeDecodeError) as exc:
                fail(f"{path}: not valid JSON ({exc})")


def check_home_paths(files):
    for path in files:
        if path == "tools/check.py":
            continue
        text = read_text(path)
        if text and HOME_PATH.search(text):
            fail(f"{path}: carries an absolute /Users/ path")


def check_versions(files):
    changelog = read_text("CHANGELOG.md") or ""
    released = RELEASED.findall(changelog)
    if not released:
        fail("CHANGELOG.md: no released version heading (## x.y.z, date)")
        return
    newest = released[0]
    for path in files:
        if path.endswith(".claude-plugin/plugin.json"):
            version = json.loads(read_text(path)).get("version")
            if version != newest:
                fail(f"{path}: version {version} does not match CHANGELOG.md {newest}")
        elif path.endswith(".claude-plugin/marketplace.json"):
            for plugin in json.loads(read_text(path)).get("plugins", []):
                if plugin.get("version") != newest:
                    fail(
                        f"{path}: plugin {plugin.get('name')} version {plugin.get('version')} "
                        f"does not match CHANGELOG.md {newest}"
                    )


def check_lessons_index():
    lessons = read_text("LESSONS.md")
    index = read_text("LESSONS-INDEX.md")
    if lessons is None or index is None:
        fail("LESSONS.md and LESSONS-INDEX.md must both exist at the root")
        return
    want = []
    for num, title, ref in LESSON.findall(lessons):
        title = title.strip().rstrip(".")
        want.append(f"{num}. {title}" + (f" ({ref})" if ref else ""))
    have = [line for line in index.splitlines() if re.match(r"^\d+\. ", line)]
    if want != have:
        fail("LESSONS-INDEX.md is out of step with LESSONS.md (run lessons-index.py)")


def main():
    files = tracked()
    check_forbidden(files)
    check_json(files)
    check_home_paths(files)
    check_versions(files)
    check_lessons_index()
    if failures:
        print(f"check.py: {len(failures)} problem(s)")
        for message in failures:
            print(f"  - {message}")
        return 1
    print(f"check.py: all checks pass ({len(files)} tracked files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
