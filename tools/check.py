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
6. The vault template agrees with its schema (Knowledge/schema.md): relationship links
   resolve, fields sit on the right page types, and the counts of unfinished work do not
   rise (tools/schema_check.py, tools/schema-baseline.json).
7. The map data file (data/foothold-map.json) is what tools/build_map.py builds today, names
   no person, and has no edge or route step pointing at something that is not there.

Release rules (docs/adr/003). These look at tracked files and at new files not yet added, so
they catch a problem before the commit as well as in CI:

8. Every filename passes the release allow-list: ASCII letters and digits, space, and
   - _ . ( ) & { } only, so no shell character, the apostrophe included, can reach a command an
   AI tool builds from a file name; legal on Windows; no part beginning with '-'. No two paths
   differ only in capitals, because macOS and Windows treat them as one file (non-ASCII names
   broke installs at 1.2.1 and 1.2.2; the 2.5.0 safety audits, H1 and H2; tools/build_release.py
   refuses the same names).
9. No file under foothold/ holds an address on main of this repository. Users receive only
   what a release tag holds, never what main holds at the moment they ask.
10. foothold/Start Here.md exists and names the pack's version and no other.
11. Every template file containing the pack_owner placeholder is on the protected list in the
    update skill, so an update never overwrites a page setup filled in with the person's name.
12. The README's install prompt names the current version's zip.
13. Nothing under foothold/template/ is a dot-file or dot-folder other than .obsidian/ at its top
    and files named .gitkeep, so a release can never carry .claude/, .mcp.json, .git/ or the
    like (second 2.5.0 safety audit, N7; tools/build_release.py refuses the same).
14. Every placeholder in the template written as a name in double curly brackets (letters,
    digits and _ only), in a file's name or its text, is on one of the two lists in the setup
    skill: the placeholders setup fills, or those that are not setup's. So a new install-time
    placeholder cannot be added without joining setup's list. Every name on setup's list is a key
    of the foothold: block in the record setup writes, no name on the other list is, and every
    page setup builds is on the update skill's protected list (usability fixes, G2; finding S5).
    Placeholders written with spaces, '-' or '.' inside the brackets, or with angle brackets in
    a file name, fail; files that are not UTF-8 are read too. A name on the not-setup's list may
    be used only inside its own skill's folder. Every name setup fills that goes into a file
    name has its file-name form (<name>_file) in the record, and the update's helper holds
    setup's list exactly (fifth safety audit, V6, V8, V10).
15. In the template's text, {{pack_owner}} and {{pack_org}} never name a page: not in a wikilink's
    target and not directly before .md. Text that names the person's or the organisation's page
    uses {{pack_owner_file}} or {{pack_org_file}}, the file-name forms the page is saved under;
    the names themselves are for what a reader sees (seventh safety audit, X4).
"""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_check import check_schema  # noqa: E402
import build_map  # noqa: E402
import build_release  # noqa: E402

FORBIDDEN = [
    (re.compile(r"(^|/)\.context/"), "a sync tool's local index (LESSONS 2)"),
    (re.compile(r"(^|/)\.obsidian/(workspace[^/]*\.json|cache[^/]*)$"), "Obsidian per-user state"),
    (re.compile(r"(^|/)\.trash/"), "the Obsidian trash"),
    (re.compile(r"(^|/)\.DS_Store$"), "a macOS .DS_Store file"),
    (re.compile(r"\.(sqlite|sqlite3|db)$"), "a database file"),
]
MAIN_ADDRESS = re.compile(
    r"milux-ltd/foothold\b[^\s\"'<>()\[\]`]*?[/=@]main(?![\w-])(?!\.\w)", re.I
)
ANY_VERSION = re.compile(r"(?<!\d)(?<!\d\.)\d+\.\d+\.\d+(?!\.?\d)")
ZIP_NAME = re.compile(r"foothold-(\d+\.\d+\.\d+)\.zip")
PACK_OWNER = "{{" + "pack_owner" + "}}"
UPDATE_SKILL = "foothold/template/Skills/meta-skills/foothold-update/SKILL.md"
UPDATE_HELPER = "foothold/template/Skills/meta-skills/foothold-update/scripts/foothold_changes.py"
SETUP_SKILL = "foothold/skills/foothold-setup/SKILL.md"
NAMED_PLACEHOLDER = re.compile(r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}")
LOOSE_PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_.-]*)\s*\}\}")
SETUP_FILLS = "### The placeholders setup fills"
NOT_SETUPS = "### Placeholders that are not setup's"
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


def all_files():
    """Tracked files, and new files not yet added that Git does not ignore."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode()
    return sorted({p for p in out.split("\0") if p and (ROOT / p).is_file()})


def read_text(path, root=ROOT):
    try:
        return (Path(root) / path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
        return None


def newest_version():
    released = RELEASED.findall(read_text("CHANGELOG.md") or "")
    return released[0] if released else None


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


def check_filenames(files, fail):
    for path in files:
        why = build_release.bad_name(path)
        if why:
            fail(f"{path}: filename not allowed ({why})")


def check_case_collisions(files, fail):
    for first, second in build_release.case_twins(files):
        fail(f"{first} and {second}: differ only in capitals, which is one file on macOS and Windows")


def check_template_dot_paths(files, fail):
    prefix = "foothold/template/"
    for path in files:
        if path.startswith(prefix):
            why = build_release.template_dot_path(path[len(prefix):])
            if why:
                fail(f"{path}: {why}")


def check_no_main_address(root, files, fail):
    for path in files:
        if not path.startswith("foothold/"):
            continue
        text = read_text(path, root)
        match = text and MAIN_ADDRESS.search(text)
        if match:
            fail(f"{path}: holds an address on main of this repository ({match.group(0)})")


def check_start_here(root, version, fail):
    text = read_text("foothold/Start Here.md", root)
    if text is None:
        fail("foothold/Start Here.md: missing")
        return
    named = set(ANY_VERSION.findall(text))
    if version not in named:
        fail(f"foothold/Start Here.md: does not name the pack's version {version}")
    others = sorted(named - {version})
    if others:
        fail(f"foothold/Start Here.md: names {', '.join(others)}, not only {version}")


def _load_helper(root):
    path = Path(root) / UPDATE_HELPER
    if not path.is_file():
        path = ROOT / UPDATE_HELPER
    spec = importlib.util.spec_from_file_location("foothold_changes", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_pack_owner_protected(root, files, fail):
    skill = read_text(UPDATE_SKILL, root)
    if skill is None:
        fail(f"{UPDATE_SKILL}: missing, so the protected list cannot be read")
        return
    helper = _load_helper(root)
    try:
        protected = helper.read_protected(skill)
    except helper.ChangesError as exc:
        fail(f"{UPDATE_SKILL}: {exc}")
        return
    prefix = "foothold/template/"
    for path in files:
        if not path.startswith(prefix):
            continue
        rel = path[len(prefix):]
        text = read_text(path, root) or ""
        if (PACK_OWNER in rel or PACK_OWNER in text) and rel not in protected:
            fail(
                f"{path}: carries the pack_owner placeholder but is not on the protected list "
                f"in {UPDATE_SKILL}"
            )


def _section(text, heading):
    """The lines under a heading, up to the next heading of any level, or None if it is absent."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == heading:
            body = []
            for rest in lines[i + 1:]:
                if rest.startswith("#"):
                    break
                body.append(rest)
            return "\n".join(body)
    return None


def setup_placeholder_lists(text):
    """The two lists in the setup skill, as (setup fills, not setup's), each in the order given.
    A list that is missing comes back as None."""
    out = []
    for heading in (SETUP_FILLS, NOT_SETUPS):
        body = _section(text, heading)
        if body is None:
            out.append(None)
            continue
        names = []
        for line in body.splitlines():
            if line.lstrip().startswith("- "):
                for code in re.findall(r"`([^`]+)`", line):
                    match = NAMED_PLACEHOLDER.fullmatch(code)
                    if match and match.group(1) not in names:
                        names.append(match.group(1))
        out.append(names)
    return tuple(out)


def not_setup_owners(text):
    """{name: the skill it belongs to}, from lines of the not-setup's list written
    '- <skill>: `{{name}}`, ...'."""
    owners = {}
    for line in (_section(text, NOT_SETUPS) or "").splitlines():
        match = re.match(r"^\s*-\s+([a-z0-9-]+):", line)
        if not match:
            continue
        for code in re.findall(r"`([^`]+)`", line):
            name = NAMED_PLACEHOLDER.fullmatch(code)
            if name:
                owners[name.group(1)] = match.group(1)
    return owners


def helper_setup_names(root):
    """The update helper's own list of setup's placeholders, or None if root has no helper."""
    if not (Path(root) / UPDATE_HELPER).is_file():
        return None
    return list(_load_helper(root).SETUP_PLACEHOLDERS)


def _template_text(root, path):
    try:
        return (Path(root) / path).read_bytes().decode("utf-8", errors="replace")
    except (FileNotFoundError, IsADirectoryError):
        return ""


def record_keys(text):
    """The keys of the foothold: block in the setup skill's example of .foothold/config.yml."""
    match = re.search(r"```yaml\nfoothold:\n((?:  .*\n)*)", text)
    if not match:
        return None
    return [line.split(":", 1)[0].strip() for line in match.group(1).splitlines() if ":" in line]


def built_pages(text):
    """The pages in the setup skill's "Pages to populate" table, in template form."""
    pages = []
    for line in text.splitlines():
        match = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        if match and "/" in match.group(1) and match.group(1).endswith(".md"):
            pages.append(helper_angle(match.group(1)))
    return pages


def helper_angle(path):
    return re.sub(r"<([a-z_]+)>", lambda m: "{{" + m.group(1) + "}}", path)


def check_setup_placeholders(root, files, fail):
    setup = read_text(SETUP_SKILL, root)
    if setup is None:
        fail(f"{SETUP_SKILL}: missing, so the list of setup's placeholders cannot be read")
        return
    fills, others = setup_placeholder_lists(setup)
    if not fills or others is None:
        fail(f"{SETUP_SKILL}: needs the two lists '{SETUP_FILLS[4:]}' and '{NOT_SETUPS[4:]}'")
        return
    both = sorted(set(fills) & set(others))
    if both:
        fail(f"{SETUP_SKILL}: on both lists: {', '.join(both)}")
    keys = record_keys(setup)
    if keys is None:
        fail(f"{SETUP_SKILL}: no example of the foothold: block of .foothold/config.yml")
        keys = []
    for name in fills:
        if name not in keys:
            fail(f"{SETUP_SKILL}: setup fills {name}, but the record's foothold: block does not "
                 "list it")
    for name in others:
        if name in keys:
            fail(f"{SETUP_SKILL}: {name} is not setup's, but it is a key of the record's "
                 "foothold: block, so the update would fill it")
    helper_names = helper_setup_names(root)
    if helper_names is not None and sorted(helper_names) != sorted(fills):
        fail(f"{UPDATE_HELPER}: SETUP_PLACEHOLDERS is not the list of the placeholders setup "
             f"fills in {SETUP_SKILL}; the helper must hold exactly that list")
    owners = not_setup_owners(setup)
    known = set(fills) | set(others)
    prefix = "foothold/template/"
    in_names = set()
    for path in files:
        if not path.startswith(prefix):
            continue
        rel = path[len(prefix):]
        if "<" in rel or ">" in rel:
            fail(f"{path}: a file name in the template may not hold < or >")
        text = _template_text(root, path)
        for where in (rel, text):
            for match in LOOSE_PLACEHOLDER.finditer(where):
                name = match.group(1)
                if match.group(0) != "{{" + name + "}}" or not NAMED_PLACEHOLDER.fullmatch(
                        match.group(0)):
                    fail(f"{path}: the placeholder {match.group(0)!r} is not written as a name "
                         "of letters, digits and _ in double curly brackets with no spaces")
        names_here = set(NAMED_PLACEHOLDER.findall(rel))
        in_names |= names_here
        found = names_here | set(NAMED_PLACEHOLDER.findall(text))
        for name in sorted(found - known):
            fail(f"{path}: the placeholder {name} is on neither list in {SETUP_SKILL}; add it to "
                 "the placeholders setup fills, or to those that are not setup's")
        for name in sorted(found & set(others)):
            owner = owners.get(name)
            if owner and f"/{owner}/" not in "/" + rel:
                fail(f"{path}: the placeholder {name} belongs to {owner}, but this file is not in "
                     f"{owner}'s folder; only {owner} may use it")
    for name in sorted(in_names & set(fills)):
        if name + "_file" not in keys:
            fail(f"{SETUP_SKILL}: {name} goes into a file name, but the record's foothold: block "
                 f"does not list its file-name form, {name}_file")
    update = read_text(UPDATE_SKILL, root)
    if update is None:
        return
    helper = _load_helper(root)
    try:
        protected = helper.read_protected(update)
    except helper.ChangesError as exc:
        fail(f"{UPDATE_SKILL}: {exc}")
        return
    for page in built_pages(setup):
        if page not in protected:
            fail(f"{SETUP_SKILL}: setup builds {page}, but it is not on the protected list in "
                 f"{UPDATE_SKILL}")


PAGE_BY_VALUE = re.compile(
    r"\[\[[^\]|]*\{\{pack_(?:owner|org)\}\}|\{\{pack_(?:owner|org)\}\}\.md")


def check_page_links(root, files, fail):
    prefix = "foothold/template/"
    for path in files:
        if not path.startswith(prefix):
            continue
        for number, line in enumerate(_template_text(root, path).splitlines(), 1):
            match = PAGE_BY_VALUE.search(line)
            if match:
                fail(f"{path}: line {number} names a page by {match.group(0)!r}; a link target or "
                     "a .md path takes {{pack_owner_file}} or {{pack_org_file}}, the page's "
                     "file-name form")


def check_readme_prompt(root, version, fail):
    text = read_text("README.md", root)
    if text is None:
        fail("README.md: missing")
        return
    if f"foothold-{version}.zip" not in text:
        fail(f"README.md: the install prompt does not name foothold-{version}.zip")
    others = sorted(set(ZIP_NAME.findall(text)) - {version})
    if others:
        fail(f"README.md: names the zip for {', '.join(others)}, not only {version}")


def check_map_data():
    data = build_map.build(ROOT)
    for fault in build_map.problems(data):
        fail(fault)
    current = read_text(build_map.OUTPUT)
    if current is None:
        fail(f"{build_map.OUTPUT}: missing; run python3 tools/build_map.py --write")
    elif current != build_map.render(data):
        fail(f"{build_map.OUTPUT}: out of date; run python3 tools/build_map.py --write")


def main():
    files = tracked()
    check_forbidden(files)
    check_json(files)
    check_home_paths(files)
    check_versions(files)
    check_lessons_index()
    check_schema(ROOT, fail)
    check_map_data()
    every = all_files()
    version = newest_version()
    check_filenames(every, fail)
    check_case_collisions(every, fail)
    check_template_dot_paths(every, fail)
    check_no_main_address(ROOT, every, fail)
    check_start_here(ROOT, version, fail)
    check_pack_owner_protected(ROOT, every, fail)
    check_readme_prompt(ROOT, version, fail)
    check_setup_placeholders(ROOT, every, fail)
    check_page_links(ROOT, every, fail)
    if failures:
        print(f"check.py: {len(failures)} problem(s)")
        for message in failures:
            print(f"  - {message}")
        return 1
    print(f"check.py: all checks pass ({len(files)} tracked files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
