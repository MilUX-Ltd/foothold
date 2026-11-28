#!/usr/bin/env python3
"""release_guard.py: refuse a release tag that is not a release.

The release workflow (.github/workflows/release.yml) runs this before it builds anything.
Standard library only, Python 3.9 or later. Exit 0 when the tag may be released, 1 otherwise.

    python3 tools/release_guard.py --tag v2.5.0 --commit HEAD --main-ref origin/main

A tag is refused when:

1. it is not of the form vX.Y.Z;
2. its version is not the one in all four version records: the newest heading in
   CHANGELOG.md, foothold/.claude-plugin/plugin.json, .claude-plugin/marketplace.json and
   the pack_version in data/foothold-map.json;
3. its commit is not on main (docs/adr/003).

The checks are in problems(), which takes the values in, so they can be tested without Git.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
RELEASED = re.compile(r"^## (\d+\.\d+\.\d+)\b", re.M)
RECORDS = (
    "CHANGELOG.md",
    "foothold/.claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "data/foothold-map.json",
)


def problems(tag, records, on_main):
    """Every reason the tag may not be released; an empty list means it may."""
    found = []
    match = TAG.match(tag or "")
    if not match:
        found.append(f"tag {tag!r} is not of the form vX.Y.Z")
        version = None
    else:
        version = tag[1:]
    if version:
        for name in RECORDS:
            have = records.get(name)
            if have is None:
                found.append(f"{name}: no version found")
            elif have != version:
                found.append(f"{name}: version {have} does not match the tag {tag}")
    if not on_main:
        found.append(f"tag {tag!r}: its commit is not on main")
    return found


def _json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def read_records(root):
    """The pack version as each of the four records holds it (None where it is missing)."""
    root = Path(root)
    records = {}
    try:
        changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    except OSError:
        changelog = ""
    released = RELEASED.findall(changelog)
    records["CHANGELOG.md"] = released[0] if released else None
    records["foothold/.claude-plugin/plugin.json"] = _json(
        root / "foothold/.claude-plugin/plugin.json"
    ).get("version")
    plugins = _json(root / ".claude-plugin/marketplace.json").get("plugins", [])
    versions = {p.get("version") for p in plugins if p.get("name") == "foothold"}
    records[".claude-plugin/marketplace.json"] = versions.pop() if len(versions) == 1 else None
    records["data/foothold-map.json"] = _json(root / "data/foothold-map.json").get("pack_version")
    return records


def is_on_main(root, commit, main_ref):
    """True when commit is main_ref or an ancestor of it."""
    if commit.startswith("-") or main_ref.startswith("-"):
        return False
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, main_ref],
        cwd=root,
        capture_output=True,
    )
    return result.returncode == 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Refuse a tag that is not a release.")
    parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--main-ref", default="origin/main")
    args = parser.parse_args(argv)
    found = problems(args.tag, read_records(ROOT), is_on_main(ROOT, args.commit, args.main_ref))
    if found:
        print(f"release_guard.py: {args.tag!r} may not be released")
        for message in found:
            print(f"  - {message}")
        return 1
    print(f"release_guard.py: {args.tag} may be released")
    return 0


if __name__ == "__main__":
    sys.exit(main())
