#!/usr/bin/env python3
"""build_release.py: build the release files for one version of the pack.

The release workflow (.github/workflows/release.yml) runs this on a tag; anyone can run it to
check a published zip against the repository. Standard library only, Python 3.9 or later.

    python3 tools/build_release.py --out dist

It writes four files into the output folder:

- foothold-X.Y.Z.zip: one folder, foothold-X.Y.Z/, holding Start Here.md, LICENSE, template/
  (from foothold/template/) and setup/ (from foothold/skills/foothold-setup/). No plugin
  manifest. Empty-folder markers (.gitkeep) are left out where the folder has other content.
- SHA256SUMS.txt: the zip's SHA-256, in the format `sha256sum -c` reads.
- release-files.txt: one line per file in the zip, its SHA-256, two spaces, then its path.
  The update skill reads this from the latest release.
- release-notes.md: the body of the release page, with the install prompt that names this
  version and the zip's checksum. The prompt lives here and not in the zip or the README,
  because a file cannot carry the checksum of the zip it is inside.

The zip is the same bytes every time for the same tree: entries in name order, a fixed date,
fixed permissions, no extra fields, and stored without compression, so the bytes do not depend
on the zlib library of the machine that builds it.

The build takes its files from Git: only files Git tracks can enter a release, so an ignored or
untracked file never does. It stops with a message naming the file if any name in the zip is
outside the allow-list (bad_name), if two names differ only in capitals, if the template holds a
dot-file or dot-folder other than .obsidian/ at its top and .gitkeep files, or if Start Here names
a version other than the one being built. It also stops if foothold/ has changes Git has not
committed, so a published zip can always be rebuilt from its tag; --allow-dirty lets a local or
test build go ahead. --from-tree walks the folder instead of asking Git, for a test build in a
folder that is not a Git checkout; it is refused unless --allow-dirty is also given, and it warns
that the result is not a release build. The release workflow passes neither.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "MilUX-Ltd/foothold"
FIXED_DATE = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644
SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
SKIP_DIRS = {"__pycache__", ".git"}
# The allow-list for every path a release can carry. The update skill's helper
# (foothold_changes.path_problem) holds the same rule for the person's computer, and
# tests/test_safety_fixes.py checks that the two agree.
SAFE_CHARACTER = re.compile(r"[A-Za-z0-9 ._()&{}-]")
WINDOWS_DEVICES = re.compile(r"^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(\..*)?$", re.I)
MAX_PART = 200
MAX_PATH = 400
VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")  # used with fullmatch
ANY_VERSION = re.compile(r"(?<!\d)(?<!\d\.)\d+\.\d+\.\d+(?!\.?\d)")


class ReleaseError(Exception):
    """The release cannot be built; the message says why and names the file."""


def bad_name(path):
    """Return why a path is not allowed in a release, or None if it is fine.

    Allowed characters: ASCII letters and digits, space, and - _ . ( ) & { } with / only
    between parts. Everything else is refused, including the apostrophe, shell characters such
    as $ ` " ' ; |, and anything that is not ASCII. No part may be empty, '.' or '..', begin or end with a
    space, end with a dot (Windows drops both), begin with '-' (it would read as an option), or
    be a Windows reserved name. No part over 200 characters and no path over 400.
    """
    if not path:
        return "'': an empty path"
    if len(path) > MAX_PATH:
        return f"{path!r}: longer than {MAX_PATH} characters"
    for ch in path:
        if ch != "/" and not SAFE_CHARACTER.fullmatch(ch):
            if not (32 <= ord(ch) < 127):
                return f"{path!r}: not plain ASCII (the character {ch!r})"
            return f"{path!r}: the character {ch!r} is not allowed in a release path"
    for part in path.split("/"):
        if part in ("", ".", ".."):
            return f"{path!r}: an empty, '.' or '..' path part"
        if part.startswith(" ") or part.endswith(" "):
            return f"{path!r}: {part!r} begins or ends with a space, which Windows drops"
        if part.endswith("."):
            return f"{path!r}: {part!r} ends in a dot, which Windows drops"
        if part.startswith("-"):
            return f"{path!r}: {part!r} begins with '-', which a command would read as an option"
        if WINDOWS_DEVICES.match(part):
            return f"{path!r}: {part!r} is a reserved name on Windows"
        if len(part) > MAX_PART:
            return f"{path!r}: a part is longer than {MAX_PART} characters"
    return None


def case_twins(paths):
    """Pairs of paths that differ only in capitals: one file on macOS and Windows."""
    seen, twins = {}, []
    for path in sorted(paths):
        key = path.casefold()
        if key in seen:
            twins.append((seen[key], path))
        else:
            seen[key] = path
    return twins


def check_case_collisions(entries):
    twins = case_twins(entries)
    if twins:
        raise ReleaseError(
            "names that differ only in capitals, which are one file on macOS and Windows:\n  "
            + "\n  ".join(f"{a!r} and {b!r}" for a, b in twins)
        )


def refuse_if_dirty(root):
    """Stop if foothold/ has changes Git has not committed, or if Git cannot say."""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", "foothold"],
            cwd=root, capture_output=True, text=True,
        )
    except OSError as exc:
        raise ReleaseError(f"cannot run git to check for uncommitted changes ({exc})")
    if out.returncode != 0:
        raise ReleaseError(
            "cannot tell whether foothold/ has uncommitted changes (git status failed: "
            f"{out.stderr.strip()}); use --allow-dirty only for a local or test build"
        )
    changed = [line for line in out.stdout.splitlines() if line.strip()]
    if changed:
        shown = "\n  ".join(changed[:10]) + ("\n  ..." if len(changed) > 10 else "")
        raise ReleaseError(
            "foothold/ has uncommitted changes, so this zip could not be rebuilt from a tag:\n  "
            f"{shown}\nCommit them, or pass --allow-dirty for a local or test build."
        )


def pack_version(root):
    manifest = Path(root) / "foothold/.claude-plugin/plugin.json"
    version = json.loads(manifest.read_text(encoding="utf-8")).get("version", "")
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        raise ReleaseError(f"{manifest}: version {version!r} is not X.Y.Z")
    return version


def zip_url(version):
    return f"https://github.com/{REPOSITORY}/releases/download/v{version}/foothold-{version}.zip"


def install_prompt(version, checksum):
    """The prompt a person pastes into their AI tool (spec section 6.2, route 2)."""
    return (
        f"Download {zip_url(version)}. Check that its SHA-256 checksum is {checksum}. "
        "If it is not, stop and tell me. If it is, unzip it and read Start Here.md inside."
    )


def fill_start_here(text, version):
    text = text.replace("{version}", version)
    named = set(ANY_VERSION.findall(text))
    others = sorted(named - {version})
    if version not in named:
        also = f" (it names {', '.join(others)})" if others else ""
        raise ReleaseError(f"foothold/Start Here.md: does not name version {version}{also}")
    if others:
        raise ReleaseError(
            f"foothold/Start Here.md: names {', '.join(others)}, not only {version}"
        )
    return text


def tracked(root, paths):
    """The files Git tracks under paths, relative to root, which must be the top of a checkout."""
    root = Path(root)
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root,
                             capture_output=True, text=True)
        out = subprocess.run(["git", "ls-files", "-z", "--", *paths], cwd=root,
                             capture_output=True)
    except OSError as exc:
        raise ReleaseError(f"cannot run git to list the files it tracks ({exc})")
    if top.returncode != 0 or out.returncode != 0 or \
            Path(top.stdout.strip()).resolve() != root.resolve():
        raise ReleaseError(
            f"{root} is not the top of a Git checkout, so the files Git tracks cannot be listed; "
            "use --from-tree only for a test build outside Git"
        )
    return sorted(p for p in out.stdout.decode("utf-8").split("\0") if p)


def _keep(rel, path):
    if any(part in SKIP_DIRS for part in rel.split("/")):
        return False
    if path.is_symlink():
        raise ReleaseError(f"{path}: symbolic links are not allowed in a release")
    return path.name not in SKIP_NAMES and not path.name.endswith(".pyc")


def _walk(root, source, from_tree):
    """Every file under root/source, as (relative posix path, Path), leaving out OS clutter.

    From Git's list of tracked files, or with from_tree from the folder itself.
    """
    base = Path(root) / source
    found = []
    if from_tree:
        for path in sorted(base.rglob("*")):
            rel = path.relative_to(base).as_posix()
            if _keep(rel, path) and path.is_file():
                found.append((rel, path))
        return found
    for name in tracked(root, [source]):
        path = Path(root) / name
        rel = path.relative_to(base).as_posix()
        if not _keep(rel, path):
            continue
        if not path.is_file():
            raise ReleaseError(f"{name}: Git tracks it but it is not a file on disk")
        found.append((rel, path))
    return found


def _drop_needless_gitkeep(files):
    """Leave out a .gitkeep whose folder holds anything else that is being shipped."""
    rels = [rel for rel, _ in files]
    kept = []
    for rel, path in files:
        if path.name == ".gitkeep":
            folder = rel[: -len(".gitkeep")]
            if any(other != rel and other.startswith(folder) for other in rels):
                continue
        kept.append((rel, path))
    return kept


def template_dot_path(rel):
    """Why a template path is not allowed for its dot parts, or None.

    The template may hold .obsidian/ at its top (for a first install; the update never touches
    it) and files named .gitkeep. Any other part beginning with a dot is refused: a release must
    never carry .claude/, .mcp.json, .git/, .foothold/, .vscode/ or anything like them.
    """
    parts = rel.split("/")
    for i, part in enumerate(parts):
        if not part.startswith("."):
            continue
        if i == 0 and part == ".obsidian" and len(parts) > 1:
            continue
        if i == len(parts) - 1 and part == ".gitkeep":
            continue
        return f"{rel!r}: a dot-file or dot-folder other than .obsidian/ and .gitkeep"
    return None


def collect(root, version, from_tree=False):
    """The zip's entries as a sorted list of (zip path, bytes)."""
    root = Path(root)
    if not from_tree:
        missing = sorted({"foothold/Start Here.md", "LICENSE"}
                         - set(tracked(root, ["foothold/Start Here.md", "LICENSE"])))
        if missing:
            raise ReleaseError(f"{', '.join(missing)}: not tracked by Git")
    top = f"foothold-{version}"
    entries = {}

    start_here = root / "foothold/Start Here.md"
    if not start_here.is_file():
        raise ReleaseError("foothold/Start Here.md: missing")
    entries[f"{top}/Start Here.md"] = fill_start_here(
        start_here.read_text(encoding="utf-8"), version
    ).encode("utf-8")

    licence = root / "LICENSE"
    if not licence.is_file():
        raise ReleaseError("LICENSE: missing at the repository root")
    entries[f"{top}/LICENSE"] = licence.read_bytes()

    for source, target in (("foothold/template", "template"),
                           ("foothold/skills/foothold-setup", "setup")):
        base = root / source
        if not base.is_dir():
            raise ReleaseError(f"{source}/: missing")
        found = _walk(root, source, from_tree)
        if target == "template":
            dots = [why for why in (template_dot_path(rel) for rel, _ in found) if why]
            if dots:
                raise ReleaseError("not allowed in the template:\n  " + "\n  ".join(dots))
        for rel, path in _drop_needless_gitkeep(found):
            entries[f"{top}/{target}/{rel}"] = path.read_bytes()

    problems = [why for why in (bad_name(name) for name in entries) if why]
    if problems:
        raise ReleaseError("names not allowed in a release:\n  " + "\n  ".join(problems))
    check_case_collisions(entries)
    return sorted(entries.items())


def write_zip(entries, target):
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_STORED) as zf:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.create_version = 20
            info.extract_version = 20
            info.external_attr = FILE_MODE << 16
            zf.writestr(info, data)


def release_notes(version, checksum):
    return (
        f"# Foothold {version}\n\n"
        "To install, either download the zip below, unzip it and give your AI tool the Start "
        "Here file inside, or paste this prompt into your AI tool:\n\n"
        f"    {install_prompt(version, checksum)}\n\n"
        f"SHA-256 of `foothold-{version}.zip`: `{checksum}`\n\n"
        "`release-files.txt` lists every file in the zip with its SHA-256. The update skill "
        "reads it to see what has changed.\n\n"
        f"What changed is in CHANGELOG.md under {version}.\n"
    )


def build(root, out_dir, version=None, from_tree=False):
    """Build the release files into out_dir and return their paths and the zip checksum.

    The files come from Git's list of tracked files; from_tree walks the folder instead, for a
    test build outside Git. The release workflow never uses it.
    """
    root = Path(root)
    found = pack_version(root)
    if version is not None and version != found:
        raise ReleaseError(f"asked to build {version}, but the plugin manifest says {found}")
    version = found
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    entries = collect(root, version, from_tree)
    zip_path = out / f"foothold-{version}.zip"
    write_zip(entries, zip_path)
    checksum = hashlib.sha256(zip_path.read_bytes()).hexdigest()

    sums = out / "SHA256SUMS.txt"
    sums.write_text(f"{checksum}  {zip_path.name}\n", encoding="utf-8", newline="\n")
    listing = out / "release-files.txt"
    listing.write_text(
        "".join(f"{hashlib.sha256(data).hexdigest()}  {name}\n" for name, data in entries),
        encoding="utf-8",
        newline="\n",
    )
    notes = out / "release-notes.md"
    notes.write_text(release_notes(version, checksum), encoding="utf-8", newline="\n")
    return {
        "version": version,
        "zip": zip_path,
        "zip_sha256": checksum,
        "sums": sums,
        "files": listing,
        "notes": notes,
        "count": len(entries),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the release files for the pack.")
    parser.add_argument("--out", required=True, help="folder to write the release files into")
    parser.add_argument("--version", help="refuse to build unless the pack is this version")
    parser.add_argument(
        "--allow-dirty", action="store_true",
        help="build even if foothold/ has uncommitted changes (local and test builds only)",
    )
    parser.add_argument(
        "--from-tree", action="store_true",
        help="walk the folder instead of taking Git's tracked files (test builds outside Git only)",
    )
    args = parser.parse_args(argv)
    if args.from_tree and not args.allow_dirty:
        print("build_release.py: --from-tree walks the folder, so it can take files Git ignores; "
              "it is for test builds only and needs --allow-dirty as well", file=sys.stderr)
        return 1
    if args.from_tree:
        print("build_release.py: warning: --from-tree build. This is not a release build; never "
              "offer its zip to users.", file=sys.stderr)
    try:
        if not args.allow_dirty:
            refuse_if_dirty(ROOT)
        result = build(ROOT, Path(args.out), args.version, args.from_tree)
    except ReleaseError as exc:
        print(f"build_release.py: {exc}", file=sys.stderr)
        return 1
    print(f"foothold-{result['version']}.zip: {result['count']} files, sha256 {result['zip_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
