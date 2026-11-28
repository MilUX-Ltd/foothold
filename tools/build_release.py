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

The build stops with a message naming the file if any name in the zip is not plain ASCII or
not legal on Windows, or if Start Here names a version other than the one being built.
"""

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "MilUX-Ltd/foothold"
FIXED_DATE = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644
SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
SKIP_DIRS = {"__pycache__", ".git"}
WINDOWS_ILLEGAL = set('<>:"\\|?*')
WINDOWS_DEVICES = re.compile(r"^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(\..*)?$", re.I)
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
ANY_VERSION = re.compile(r"(?<!\d)(?<!\d\.)\d+\.\d+\.\d+(?!\.?\d)")


class ReleaseError(Exception):
    """The release cannot be built; the message says why and names the file."""


def bad_name(path):
    """Return why a zip path is not allowed, or None if it is fine.

    Allowed: printable ASCII only; no character Windows refuses; no part that is a Windows
    device name or ends in a dot or a space.
    """
    for ch in path:
        if not (32 <= ord(ch) < 127):
            return f"{path!r}: not plain ASCII"
        if ch in WINDOWS_ILLEGAL:
            return f"{path!r}: the character {ch!r} is not allowed in a Windows filename"
    for part in path.split("/"):
        if part == "":
            return f"{path!r}: empty path part"
        if WINDOWS_DEVICES.match(part):
            return f"{path!r}: {part!r} is a reserved name on Windows"
        if part.endswith(".") or part.endswith(" "):
            return f"{path!r}: {part!r} ends in a dot or a space, which Windows drops"
    return None


def pack_version(root):
    manifest = Path(root) / "foothold/.claude-plugin/plugin.json"
    version = json.loads(manifest.read_text(encoding="utf-8")).get("version", "")
    if not VERSION.match(version or ""):
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


def _walk(base):
    """Every file under base, as (relative posix path, Path), leaving out OS clutter."""
    found = []
    for path in sorted(base.rglob("*")):
        rel = path.relative_to(base)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            raise ReleaseError(f"{path}: symbolic links are not allowed in a release")
        if path.is_file() and path.name not in SKIP_NAMES and not path.name.endswith(".pyc"):
            found.append((rel.as_posix(), path))
    return found


def _drop_needless_gitkeep(files):
    """Leave out a .gitkeep whose folder holds anything else."""
    kept = []
    for rel, path in files:
        if path.name == ".gitkeep":
            others = [p for p in path.parent.iterdir() if p.name != ".gitkeep"]
            others = [p for p in others if p.name not in SKIP_NAMES and p.name not in SKIP_DIRS]
            if others:
                continue
        kept.append((rel, path))
    return kept


def collect(root, version):
    """The zip's entries as a sorted list of (zip path, bytes)."""
    root = Path(root)
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
        for rel, path in _drop_needless_gitkeep(_walk(base)):
            entries[f"{top}/{target}/{rel}"] = path.read_bytes()

    problems = [why for why in (bad_name(name) for name in entries) if why]
    if problems:
        raise ReleaseError("names not allowed in a release:\n  " + "\n  ".join(problems))
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


def build(root, out_dir, version=None):
    """Build the release files into out_dir and return their paths and the zip checksum."""
    root = Path(root)
    found = pack_version(root)
    if version is not None and version != found:
        raise ReleaseError(f"asked to build {version}, but the plugin manifest says {found}")
    version = found
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    entries = collect(root, version)
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
    args = parser.parse_args(argv)
    try:
        result = build(ROOT, Path(args.out), args.version)
    except ReleaseError as exc:
        print(f"build_release.py: {exc}", file=sys.stderr)
        return 1
    print(f"foothold-{result['version']}.zip: {result['count']} files, sha256 {result['zip_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
