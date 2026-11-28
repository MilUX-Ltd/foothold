#!/usr/bin/env python3
"""foothold_changes.py: sort a Foothold release's changes before anything is written.

Part of the foothold-update skill. It reads; it never writes to the vault and never uses the
network. Standard library only, Python 3.9 or later. SKILL.md, beside this folder, states the
same rules in words, for AI tools that cannot run Python.

    python3 foothold_changes.py sort <vault folder> <release-files.txt or release folder>
    python3 foothold_changes.py hash <file> [<file> ...]
    python3 foothold_changes.py check <release-files.txt> <template path> <downloaded file>

Pass every path as its own argument. Never join paths or file text into a command.

`sort` puts each file in the release into one group:

- show and ask each: skills, instruction files, scripts and settings. Show the difference
  for each one and ask about each one.
- list and ask once: everything else. List them by name and ask once.
- conflict: the file in the vault was changed by the person, or has no stored checksum. Show
  the difference and ask: keep mine, take the release's, or merge.
- local only: the person changed it and the release did not. Nothing to do.
- unchanged: the vault already matches. Nothing to do.
- protected: on the protected list in SKILL.md. Never touched.
- excluded: under .obsidian/. Never touched.
"""

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ASK_EACH = "show and ask each"
ASK_ONCE = "list and ask once"
CONFLICT = "conflict"
LOCAL_ONLY = "local only"
UNCHANGED = "unchanged"
PROTECTED = "protected"
EXCLUDED = "excluded"
ORDER = (ASK_EACH, ASK_ONCE, CONFLICT, LOCAL_ONLY, UNCHANGED, PROTECTED, EXCLUDED)

INSTRUCTION_NAMES = {
    "claude.md", "agents.md", "gemini.md", "start here.md", "copilot-instructions.md",
    ".cursorrules", ".windsurfrules", ".clinerules",
}
INSTRUCTION_FOLDERS = {"Skills", "Knowledge"}
SCRIPT_EXT = {
    ".py", ".sh", ".bash", ".zsh", ".fish", ".js", ".mjs", ".cjs", ".ts", ".ps1", ".psm1",
    ".bat", ".cmd", ".vbs", ".rb", ".pl", ".php", ".html", ".htm", ".svg", ".applescript",
    ".scpt", ".command", ".exe", ".app", ".jar",
}
SETTINGS_EXT = {
    ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".conf", ".env", ".plist", ".xml",
}
LINE = re.compile(r"^([0-9a-f]{64})  (.+)$")
TOP = re.compile(r"^foothold-(\d+\.\d+\.\d+)$")
PLACEHOLDER = re.compile(r"\{\{([a-z_]+)\}\}")
ANGLE = re.compile(r"<([a-z_]+)>")
CONFIG_BLOCKS = {"foothold", "release_hashes", "vault_hashes", "last_known_shas"}
SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


class ChangesError(Exception):
    """The input cannot be trusted or read; the message says why."""


@dataclass
class Release:
    version: str
    files: dict  # template path -> SHA-256


@dataclass
class Config:
    values: dict = field(default_factory=dict)  # the foothold: block, e.g. pack_owner
    vault_hashes: dict = field(default_factory=dict)  # vault path -> SHA-256 as written
    release_hashes: dict = field(default_factory=dict)  # vault path -> SHA-256 of its source
    legacy: dict = field(default_factory=dict)  # vault path -> git blob SHA-1 (last_known_shas)


@dataclass
class Change:
    category: str
    vault_path: str
    new: bool = False


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def blob_sha1(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _safe_parts(path, what):
    if not path or "\\" in path or "\0" in path or path.startswith("/"):
        raise ChangesError(f"{what} {path!r}: not a safe relative path")
    if any(not (32 <= ord(ch) < 127) for ch in path):
        raise ChangesError(f"{what} {path!r}: not plain ASCII")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ChangesError(f"{what} {path!r}: not a safe relative path")
    return parts


def parse_release_files(text):
    """Read release-files.txt. Only lines under foothold-X.Y.Z/template/ are kept."""
    version, files, seen = None, {}, 0
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        match = LINE.match(raw)
        if not match:
            raise ChangesError(f"release-files.txt line {number}: not '<sha256>  <path>'")
        digest, path = match.groups()
        parts = _safe_parts(path, f"release-files.txt line {number}:")
        top = TOP.match(parts[0])
        if not top:
            raise ChangesError(f"release-files.txt line {number}: {path!r} is outside foothold-X.Y.Z/")
        if version is None:
            version = top.group(1)
        elif top.group(1) != version:
            raise ChangesError(f"release-files.txt line {number}: more than one version")
        seen += 1
        if len(parts) > 2 and parts[1] == "template":
            files["/".join(parts[2:])] = digest
    if not seen:
        raise ChangesError("release-files.txt: empty")
    return Release(version=version, files=files)


def release_from_folder(folder):
    """Read an unzipped release folder, foothold-X.Y.Z/, that the person downloaded."""
    folder = Path(folder)
    top = TOP.match(folder.name)
    if not top:
        raise ChangesError(f"{folder.name!r}: expected a folder named foothold-X.Y.Z")
    base = folder / "template"
    if not base.is_dir():
        raise ChangesError(f"{folder}: no template folder")
    files = {}
    for path in sorted(base.rglob("*")):
        if path.is_symlink():
            raise ChangesError(f"{path}: a link inside the release; not trusted")
        if path.is_file() and path.name not in SKIP_NAMES:
            rel = path.relative_to(base).as_posix()
            _safe_parts(rel, "release file")
            files[rel] = sha256_bytes(path.read_bytes())
    return Release(version=top.group(1), files=files)


def _scalar(text):
    text = text.strip()
    if text.startswith('"'):
        end = _closing_quote(text)
        return json.loads(text[: end + 1])
    if text.startswith("'"):
        end = 1
        out = []
        while end < len(text):
            if text[end] == "'":
                if text[end + 1 : end + 2] == "'":
                    out.append("'")
                    end += 2
                    continue
                break
            out.append(text[end])
            end += 1
        return "".join(out)
    cut = text.find(" #")
    return (text[:cut] if cut >= 0 else text).strip()


def _closing_quote(text):
    i = 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == '"':
            return i
        i += 1
    raise ChangesError(f"unclosed quote in {text!r}")


def _split_key(body, by_last_colon):
    if body.startswith('"'):
        end = _closing_quote(body)
        key = json.loads(body[: end + 1])
        rest = body[end + 1 :].lstrip()
        if not rest.startswith(":"):
            raise ChangesError(f"config line {body!r}: no ':' after the key")
        return key, rest[1:]
    if by_last_colon:
        key, sep, value = body.rpartition(":")
    else:
        key, sep, value = body.partition(": ")
        if not sep and body.endswith(":"):
            key, sep, value = body[:-1], ":", ""
    if not sep:
        raise ChangesError(f"config line {body!r}: no ':'")
    return key.strip(), value


def parse_config(text):
    """Read the parts of .foothold/config.yml the update needs. Other parts are ignored."""
    config = Config()
    target = {
        "foothold": config.values,
        "release_hashes": config.release_hashes,
        "vault_hashes": config.vault_hashes,
        "last_known_shas": config.legacy,
    }
    block = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw.startswith(" "):
            key, _, rest = raw.partition(":")
            key = key.strip()
            block = key if key in CONFIG_BLOCKS and rest.strip() in ("", "{}") else None
            continue
        if block is None:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent != 2:
            continue
        hashes = block != "foothold"
        key, value = _split_key(raw.strip(), by_last_colon=hashes)
        value = _scalar(value)
        if hashes:
            value = value.lower()
            if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
                continue
        target[block][key] = value
    return config


def render_config(config):
    """The four blocks as YAML, with every key and value quoted."""
    out = ["foothold:"]
    out += [f"  {key}: {json.dumps(value)}" for key, value in config.values.items()]
    for name, table in (
        ("release_hashes", config.release_hashes),
        ("vault_hashes", config.vault_hashes),
        ("last_known_shas", config.legacy),
    ):
        out.append(f"{name}:" if table else f"{name}: {{}}")
        out += [f"  {json.dumps(key)}: {value}" for key, value in sorted(table.items())]
    return "\n".join(out) + "\n"


def read_protected(skill_text):
    """The paths in the '## Protected files' section of SKILL.md, in template form."""
    protected, inside = set(), False
    for line in skill_text.splitlines():
        if line.startswith("## "):
            inside = line.strip().lower().startswith("## protected files")
            continue
        if inside:
            match = re.match(r"^\s*[-*]\s+`([^`]+)`", line)
            if match:
                protected.add(ANGLE.sub(lambda m: "{{" + m.group(1) + "}}", match.group(1)))
    if not protected:
        raise ChangesError("SKILL.md: no protected files found; stopping to be safe")
    return protected


def substitute(path, values):
    """Fill placeholders in a template path with the vault's values, and check the result."""
    filled = PLACEHOLDER.sub(lambda m: values.get(m.group(1), m.group(0)), path)
    if not filled or "\\" in filled or "\0" in filled or filled.startswith("/"):
        raise ChangesError(f"{path!r} becomes {filled!r}, which is not a safe vault path")
    if any(part in ("", ".", "..") for part in filled.split("/")):
        raise ChangesError(f"{path!r} becomes {filled!r}, which is not a safe vault path")
    return filled


def kind(path):
    """ASK_EACH for anything that instructs an AI or changes settings, else ASK_ONCE."""
    parts = path.split("/")
    name = parts[-1].lower()
    suffix = Path(name).suffix
    if parts[0] in INSTRUCTION_FOLDERS:
        return ASK_EACH
    if name in INSTRUCTION_NAMES:
        return ASK_EACH
    if any(part.startswith(".") for part in parts[:-1]):
        return ASK_EACH
    if name.startswith(".") and name != ".gitkeep":
        return ASK_EACH
    if suffix in SCRIPT_EXT or suffix in SETTINGS_EXT:
        return ASK_EACH
    return ASK_ONCE


def excluded(path):
    return path == ".obsidian" or path.startswith(".obsidian/")


def _inside(vault_root, path):
    try:
        path.resolve().relative_to(vault_root.resolve())
        return True
    except ValueError:
        return False


def classify(release, config, vault_root, protected):
    """Sort every file in the release. Returns {template path: Change}."""
    vault_root = Path(vault_root)
    protected_vault = set()
    for item in protected:
        try:
            protected_vault.add(substitute(item, config.values))
        except ChangesError:
            pass
    result = {}
    for tpath, rsha in sorted(release.files.items()):
        vpath = substitute(tpath, config.values)
        if excluded(tpath) or excluded(vpath):
            result[tpath] = Change(EXCLUDED, vpath)
            continue
        if tpath in protected or vpath in protected_vault:
            result[tpath] = Change(PROTECTED, vpath)
            continue
        local = vault_root / vpath
        if not _inside(vault_root, local):
            result[tpath] = Change(CONFLICT, vpath)
            continue
        if not local.exists() and not local.is_symlink():
            result[tpath] = Change(kind(tpath), vpath, new=True)
            continue
        if local.is_symlink() or not local.is_file():
            result[tpath] = Change(CONFLICT, vpath)
            continue
        data = local.read_bytes()
        lsha = sha256_bytes(data)
        if lsha == rsha:
            result[tpath] = Change(UNCHANGED, vpath)
            continue
        written = config.vault_hashes.get(vpath)
        source = config.release_hashes.get(vpath)
        same_release = source is not None and source == rsha
        if written is not None:
            if lsha == written:
                category = UNCHANGED if same_release else kind(tpath)
            else:
                category = LOCAL_ONLY if same_release else CONFLICT
        elif vpath in config.legacy:
            category = kind(tpath) if blob_sha1(data) == config.legacy[vpath] else CONFLICT
        else:
            category = CONFLICT
        result[tpath] = Change(category, vpath)
    return result


def load_release(source):
    source = Path(source)
    if source.is_dir():
        return release_from_folder(source)
    return parse_release_files(source.read_text(encoding="utf-8"))


def sort_from_paths(vault, release_source, skill_md):
    vault = Path(vault)
    config_file = vault / ".foothold/config.yml"
    if not config_file.is_file():
        raise ChangesError(f"{config_file}: not found; this does not look like a Foothold vault")
    config = parse_config(config_file.read_text(encoding="utf-8"))
    protected = read_protected(Path(skill_md).read_text(encoding="utf-8"))
    return classify(load_release(release_source), config, vault, protected)


def check_file(release_files, template_path, downloaded):
    release = parse_release_files(Path(release_files).read_text(encoding="utf-8"))
    want = release.files.get(template_path)
    if want is None:
        raise ChangesError(f"{template_path!r} is not in the release")
    return sha256_bytes(Path(downloaded).read_bytes()) == want


def _report(release_source, result, as_json):
    if as_json:
        print(json.dumps(
            {p: {"group": c.category, "vault_path": c.vault_path, "new": c.new}
             for p, c in result.items()},
            indent=2,
        ))
        return
    print(f"Release: {release_source}")
    for group in ORDER:
        items = [(p, c) for p, c in result.items() if c.category == group]
        print(f"\n{group} ({len(items)})")
        if group in (UNCHANGED, EXCLUDED):
            continue
        for tpath, change in items:
            mark = "[new] " if change.new else ""
            print(f"  {mark}{change.vault_path}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("sort", help="sort the release's changes against the vault")
    s.add_argument("vault")
    s.add_argument("release", help="release-files.txt, or an unzipped foothold-X.Y.Z folder")
    s.add_argument("--skill", default=str(Path(__file__).resolve().parent.parent / "SKILL.md"))
    s.add_argument("--json", action="store_true")
    h = sub.add_parser("hash", help="print the SHA-256 of each file")
    h.add_argument("files", nargs="+")
    c = sub.add_parser("check", help="check a downloaded file against release-files.txt")
    c.add_argument("release_files")
    c.add_argument("template_path")
    c.add_argument("downloaded")
    args = parser.parse_args(argv)
    try:
        if args.command == "sort":
            _report(args.release, sort_from_paths(args.vault, args.release, args.skill), args.json)
        elif args.command == "hash":
            for name in args.files:
                print(f"{sha256_bytes(Path(name).read_bytes())}  {name}")
        else:
            if not check_file(args.release_files, args.template_path, args.downloaded):
                print(f"MISMATCH: {args.downloaded} is not {args.template_path} from the release")
                return 1
            print(f"OK: {args.downloaded} matches {args.template_path}")
    except (ChangesError, OSError, ValueError) as exc:
        print(f"foothold_changes.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
