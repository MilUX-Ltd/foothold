#!/usr/bin/env python3
"""foothold_changes.py: sort a Foothold release's changes before anything is written.

Part of the foothold-update skill. It reads; it never writes to the vault and never uses the
network. Standard library only, Python 3.9 or later. SKILL.md, beside this folder, states the
same rules in words, for AI tools that cannot run Python.

    python3 foothold_changes.py sort <vault folder> <release-files.txt or release folder>
        [--release-files <release-files.txt>]
    python3 foothold_changes.py verify <release-files.txt> <download folder>
    python3 foothold_changes.py hidden <file or folder> [...]
    python3 foothold_changes.py hash-folder <folder>
    python3 foothold_changes.py hash <file> [<file> ...]

Every argument is a folder or file the person named, or one you made: the vault, a temporary
folder, the downloaded release-files.txt. No command takes a path read from the release, so a
file name in the release never reaches a command line. Pass every path as its own argument.

Every path in a release must pass path_problem(): letters, digits, space and - _ . ( ) & { } '
only, with / between parts. The whole list is refused if one path fails, or if two paths differ
only in capitals. Names are compared without regard to capitals throughout, because the default
file systems on macOS and Windows do the same.

`sort` puts each file in the release into one group:

- show and ask each: anything not in the next group. Show the difference for each one and ask
  about each one.
- list and ask once: a .md page under Intelligence/ or CRM/ that is not a guide or an
  instruction file and has no part beginning with a dot. List them by name and ask once.
- conflict: the file in the vault was changed by the person, has no stored checksum, or
  matches the release path only without regard to capitals. Show the difference and ask: keep
  mine, take the release's, or merge.
- local only: the person changed it and the release did not. Nothing to do.
- unchanged: the vault already matches. Nothing to do.
- protected: on the protected list in SKILL.md. Never touched.
- excluded: under .obsidian/. Never touched.

A path that would land outside the vault stops the whole run.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
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

# Names compared after casefold(). A file with one of these names is always show and ask each.
INSTRUCTION_NAMES = {
    "claude.md", "agents.md", "agent.md", "gemini.md", "readme.md", "skill.md",
    "start here.md", "copilot-instructions.md",
}
ASK_ONCE_FOLDERS = {"intelligence", "crm"}
EXCLUDED_FOLDER = ".obsidian"

# The allow-list for every path a release can carry. tools/build_release.py holds the same
# rule (bad_name) and tests/test_safety_fixes.py checks that the two agree.
SAFE_CHARACTER = re.compile(r"[A-Za-z0-9 ._()&{}'-]")
RESERVED_NAME = re.compile(r"^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(\..*)?$", re.I)
MAX_PART = 200
MAX_PATH = 400
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


def path_problem(path):
    """Return why a release path is not allowed, or None if it is fine.

    Allowed: ASCII letters and digits, space, and - _ . ( ) & { } ' with / only between parts.
    No part may be empty, '.' or '..', begin or end with a space, end with a dot, begin with
    '-', or be a Windows reserved name. No part over 200 characters, no path over 400.
    """
    if not path:
        return "an empty path"
    if len(path) > MAX_PATH:
        return f"longer than {MAX_PATH} characters"
    for ch in path:
        if ch != "/" and not SAFE_CHARACTER.fullmatch(ch):
            return f"the character {ch!r} is not allowed"
    for part in path.split("/"):
        if part in ("", ".", ".."):
            return f"an empty, '.' or '..' part"
        if part.startswith(" ") or part.endswith(" "):
            return f"the part {part!r} begins or ends with a space"
        if part.endswith("."):
            return f"the part {part!r} ends with a dot"
        if part.startswith("-"):
            return f"the part {part!r} begins with '-'"
        if RESERVED_NAME.match(part):
            return f"the part {part!r} is a reserved name on Windows"
        if len(part) > MAX_PART:
            return f"a part is longer than {MAX_PART} characters"
    return None


def _safe_parts(path, what):
    why = path_problem(path)
    if why:
        raise ChangesError(f"{what} {path!r}: not allowed ({why}); refusing the whole list")
    return path.split("/")


def _no_case_twins(paths, what):
    seen = {}
    for path in paths:
        key = path.casefold()
        if key in seen:
            raise ChangesError(
                f"{what}: {seen[key]!r} and {path!r} differ only in capitals or are the same "
                "path twice; refusing the whole list"
            )
        seen[key] = path


def parse_release_files(text):
    """Read release-files.txt. Only lines under foothold-X.Y.Z/template/ are kept."""
    version, files, seen, every = None, {}, 0, []
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
        every.append(path)
        if len(parts) > 2 and parts[1] == "template":
            files["/".join(parts[2:])] = digest
    if not seen:
        raise ChangesError("release-files.txt: empty")
    _no_case_twins(every, "release-files.txt")
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
    _no_case_twins(files, f"{folder.name}/template")
    return Release(version=top.group(1), files=files)


def check_folder_against_list(folder_release, listed):
    """Refuse a release folder unless it holds exactly the files release-files.txt lists."""
    if folder_release.version != listed.version:
        raise ChangesError(
            f"the folder is release {folder_release.version} but release-files.txt is "
            f"{listed.version}; refusing"
        )
    problems = []
    for path in sorted(set(folder_release.files) | set(listed.files)):
        have, want = folder_release.files.get(path), listed.files.get(path)
        if want is None:
            problems.append(f"{path}: in the folder but not in release-files.txt")
        elif have is None:
            problems.append(f"{path}: in release-files.txt but not in the folder")
        elif have != want:
            problems.append(f"{path}: does not match its checksum in release-files.txt")
    if problems:
        raise ChangesError(
            "the release folder does not match release-files.txt; refusing:\n  "
            + "\n  ".join(problems)
        )


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


def _value(name, values):
    """A placeholder's value from config.yml, checked before it goes into a path."""
    if name not in values:
        return "{{" + name + "}}"
    value = values[name]
    why = None if value else "it is empty"
    if why is None and ("/" in value or value.startswith(".")):
        why = "it holds '/' or begins with a dot"
    why = why or path_problem(value)
    if why:
        raise ChangesError(
            f"the value of {name} in .foothold/config.yml, {value!r}, cannot be used in a file "
            f"name ({why}); stopping, nothing was changed"
        )
    return value


def substitute(path, values):
    """Fill placeholders in a template path with the vault's values, and check the result."""
    filled = PLACEHOLDER.sub(lambda m: _value(m.group(1), values), path)
    why = path_problem(filled)
    if why:
        raise ChangesError(f"{path!r} becomes {filled!r}, which is not a safe vault path ({why})")
    return filled


def kind(path):
    """ASK_ONCE only for a plain .md page under Intelligence/ or CRM/; ASK_EACH for the rest.

    Deny by default: a file is list and ask once only if all of these hold, compared without
    regard to capitals. It is under Intelligence/ or CRM/. Its extension is .md. Its name is not
    a guide (* Guide.md) or an instruction file (CLAUDE.md, AGENTS.md, AGENT.md, GEMINI.md,
    README.md, SKILL.md, *.local.md). No part of its path begins with a dot.
    """
    parts = path.split("/")
    name = parts[-1].casefold()
    if len(parts) < 2 or parts[0].casefold() not in ASK_ONCE_FOLDERS:
        return ASK_EACH
    if not name.endswith(".md"):
        return ASK_EACH
    if name in INSTRUCTION_NAMES or name == "guide.md" or name.endswith(" guide.md"):
        return ASK_EACH
    if name.endswith(".local.md"):
        return ASK_EACH
    if any(part.startswith(".") for part in parts):
        return ASK_EACH
    return ASK_ONCE


def excluded(path):
    return path.split("/")[0].casefold() == EXCLUDED_FOLDER


def _on_disk(vault_root, vpath):
    """How vpath stands in the vault, comparing names exactly, part by part.

    'exact': every part exists with exactly this name. 'absent': some part does not exist in any
    capitals. 'case': some part exists only with other capitals (on macOS and Windows that is
    the same file). 'blocked': a part that should be a folder is a file.
    """
    here = Path(vault_root)
    parts = vpath.split("/")
    for i, part in enumerate(parts):
        if not here.is_dir() or here.is_symlink() and i:
            return "blocked"
        names = os.listdir(here)
        if part not in names:
            if any(n.casefold() == part.casefold() for n in names):
                return "case"
            return "absent"
        here = here / part
    return "exact"


def _inside(vault_root, path):
    try:
        path.resolve().relative_to(vault_root.resolve())
        return True
    except ValueError:
        return False


def classify(release, config, vault_root, protected):
    """Sort every file in the release. Returns {template path: Change}."""
    vault_root = Path(vault_root)
    protected_template = {item.casefold() for item in protected}
    protected_vault = set()
    for item in protected:
        try:
            protected_vault.add(substitute(item, config.values).casefold())
        except ChangesError:
            pass
    result, vault_paths = {}, {}
    for tpath, rsha in sorted(release.files.items()):
        if excluded(tpath):
            result[tpath] = Change(EXCLUDED, tpath)
            continue
        if tpath.casefold() in protected_template:
            try:
                shown = substitute(tpath, config.values)
            except ChangesError:
                shown = tpath
            result[tpath] = Change(PROTECTED, shown)
            continue
        vpath = substitute(tpath, config.values)
        if excluded(vpath):
            result[tpath] = Change(EXCLUDED, vpath)
            continue
        if vpath.casefold() in protected_vault:
            result[tpath] = Change(PROTECTED, vpath)
            continue
        twin = vault_paths.setdefault(vpath.casefold(), tpath)
        if twin != tpath:
            raise ChangesError(
                f"{twin!r} and {tpath!r} both become {vpath!r} in the vault; stopping, nothing "
                "was changed"
            )
        local = vault_root / vpath
        if not _inside(vault_root, local):
            raise ChangesError(
                f"{tpath!r} would be written at {vpath!r}, which is outside the vault (a "
                "linked folder, or a name that leaves it); stopping, nothing was changed"
            )
        sort_kind = ASK_EACH if ASK_EACH in (kind(tpath), kind(vpath)) else ASK_ONCE
        state = _on_disk(vault_root, vpath)
        if state in ("case", "blocked"):
            result[tpath] = Change(CONFLICT, vpath)
            continue
        if state == "absent" and not local.is_symlink():
            result[tpath] = Change(sort_kind, vpath, new=True)
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
                category = UNCHANGED if same_release else sort_kind
            else:
                category = LOCAL_ONLY if same_release else CONFLICT
        elif vpath in config.legacy:
            category = sort_kind if blob_sha1(data) == config.legacy[vpath] else CONFLICT
        else:
            category = CONFLICT
        result[tpath] = Change(category, vpath)
    return result


def read_release_files(path):
    return parse_release_files(Path(path).read_text(encoding="utf-8"))


def load_release(source, release_files=None):
    """Read a release from release-files.txt or from an unzipped folder.

    For a folder, the checksums are worked out from the folder's own files, which proves
    nothing about where they came from. Give release_files, when it can be had, and the folder
    is refused unless it matches it exactly.
    """
    source = Path(source)
    if source.is_dir():
        release = release_from_folder(source)
        if release_files is not None:
            check_folder_against_list(release, read_release_files(release_files))
        return release
    return read_release_files(source)


def sort_from_paths(vault, release_source, skill_md, release_files=None):
    vault = Path(vault)
    config_file = vault / ".foothold/config.yml"
    if not config_file.is_file():
        raise ChangesError(f"{config_file}: not found; this does not look like a Foothold vault")
    config = parse_config(config_file.read_text(encoding="utf-8"))
    protected = read_protected(Path(skill_md).read_text(encoding="utf-8"))
    return classify(load_release(release_source, release_files), config, vault, protected)


def _files_under(folder):
    """Every file under folder as (relative posix path, Path), refusing links."""
    folder = Path(folder)
    if not folder.is_dir():
        raise ChangesError(f"{folder}: not a folder")
    found = []
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ChangesError(f"{path}: a link; not trusted")
        if path.is_file() and path.name not in SKIP_NAMES:
            found.append((path.relative_to(folder).as_posix(), path))
    return found


def verify_folder(release, folder):
    """Check each file in a download folder, laid out by template path, against the list.

    Returns {template path: 'ok' | 'failed' | 'not in the release'}.
    """
    results = {}
    for rel, path in _files_under(folder):
        want = release.files.get(rel)
        if want is None:
            results[rel] = "not in the release"
        elif sha256_bytes(path.read_bytes()) == want:
            results[rel] = "ok"
        else:
            results[rel] = "failed"
    return results


def _hidden(ch):
    code = ord(ch)
    if ch in "\t\r\n":
        return False
    if unicodedata.category(ch) in ("Cc", "Cf", "Co", "Cn", "Zl", "Zp"):
        return True
    if unicodedata.category(ch) == "Zs" and ch != " ":
        return True
    return 0xFE00 <= code <= 0xFE0F or 0xE0100 <= code <= 0xE01EF


def hidden_characters(data):
    """Characters in UTF-8 text that do not display: control, zero-width, direction-changing,
    Tag and variation characters, odd spaces. Returns [(line, column, 'U+XXXX', name)].

    Raises ChangesError if the bytes are not UTF-8 text.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChangesError(f"cannot be shown as text (not UTF-8 at byte {exc.start})")
    found, line, column = [], 1, 0
    for ch in text:
        if ch == "\n":
            line, column = line + 1, 0
            continue
        column += 1
        if _hidden(ch):
            found.append((line, column, f"U+{ord(ch):04X}", unicodedata.name(ch, "no name")))
    return found


def _hidden_report(targets):
    """Print what hidden_characters finds in each file or folder. True if anything was found."""
    any_found = False
    for target in targets:
        target = Path(target)
        if target.is_dir():
            items = _files_under(target)
        else:
            items = [(target.name, target)]
        for rel, path in items:
            try:
                found = hidden_characters(path.read_bytes())
            except ChangesError as exc:
                print(f"{rel}: {exc}")
                any_found = True
                continue
            for line, column, code, name in found:
                print(f"{rel}:{line}:{column} {code} {name}")
                any_found = True
    if not any_found:
        print("No characters that do not display, and every file is text.")
    return any_found


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
    s.add_argument("--release-files", help="with a release folder: refuse it unless it matches")
    v = sub.add_parser("verify", help="check a download folder against release-files.txt")
    v.add_argument("release_files")
    v.add_argument("folder", help="a temporary folder holding the downloads by template path")
    d = sub.add_parser("hidden", help="report characters that do not display")
    d.add_argument("targets", nargs="+", help="files or folders")
    f = sub.add_parser("hash-folder", help="print the SHA-256 of every file under a folder")
    f.add_argument("folder")
    h = sub.add_parser("hash", help="print the SHA-256 of each file")
    h.add_argument("files", nargs="+")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2
    try:
        if args.command == "sort":
            result = sort_from_paths(args.vault, args.release, args.skill, args.release_files)
            _report(args.release, result, args.json)
        elif args.command == "verify":
            results = verify_folder(read_release_files(args.release_files), args.folder)
            words = {"ok": "OK", "failed": "FAILED its checksum",
                     "not in the release": "NOT IN THE RELEASE"}
            for rel, outcome in results.items():
                print(f"{words[outcome]}: {rel}")
            if not results:
                print("No files found in the folder.")
                return 1
            return 0 if all(o == "ok" for o in results.values()) else 1
        elif args.command == "hidden":
            return 1 if _hidden_report(args.targets) else 0
        elif args.command == "hash-folder":
            for rel, path in _files_under(args.folder):
                print(f"{sha256_bytes(path.read_bytes())}  {rel}")
        else:
            for name in args.files:
                print(f"{sha256_bytes(Path(name).read_bytes())}  {name}")
    except (ChangesError, OSError, ValueError) as exc:
        print(f"foothold_changes.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
