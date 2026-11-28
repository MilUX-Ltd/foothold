"""schema_check.py: checks the vault template against Knowledge/schema.md.

Called by check.py. Standard library only.

The schema names a small set of relationship fields. A value written as a wikilink must point
at a page that exists, and a field may only be used on the page types the schema allows.

Three counts are held to a ceiling in tools/schema-baseline.json. They record work not yet
done, so they may only go down:

- relationship values still written as plain text and not as links;
- wikilinks in page bodies that point at nothing;
- skills that do not yet declare what they read and write.

When a count falls, lower the ceiling in the same change. A count above or below its ceiling
fails the check, so the file always states the true position.
"""

import json
import re
from pathlib import Path

TEMPLATE = "foothold/template"
BASELINE = "tools/schema-baseline.json"

# field -> page types it may appear on (None means any type)
RELATIONSHIPS = {
    "parent": None,
    "customer": {"programme", "framework", "portal", "customer-engagement"},
    "operator": {"framework", "portal", "event-series", "network", "organisation"},
    "service": {"programme"},
    "member_of": {"organisation", "cluster"},
    "listed_on": {"framework"},
}
# plain words the service field may hold beside links, for programmes no one service owns
SERVICE_WORDS = {"Joint", "Civil", "Industry"}
# earlier spellings, to be folded into the fields above
RETIRED_FIELDS = {"parent_programme": "parent", "parent-org": "parent", "operated_by": "operator"}

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
KEY = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
ITEM = re.compile(r"^\s+-\s+(.*)$")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
FENCE = re.compile(r"^(```|~~~).*?^\1\s*$", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def _unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text):
    """A small reader for the frontmatter the pack uses: scalars, inline lists, dash lists."""
    match = FRONTMATTER.match(text)
    fields = {}
    if not match:
        return fields, text
    key = None
    for line in match.group(1).split("\n"):
        found = KEY.match(line)
        if found:
            key, raw = found.group(1), found.group(2).strip()
            if raw.startswith("[") and raw.endswith("]") and not raw.startswith("[["):
                fields[key] = [_unquote(v) for v in raw[1:-1].split(",") if v.strip()]
            elif raw == "":
                fields[key] = []
            else:
                fields[key] = [_unquote(raw)]
            continue
        item = ITEM.match(line)
        if item and key is not None:
            fields[key].append(_unquote(item.group(1)))
    return fields, text[match.end():]


def link_target(inner):
    """The page a wikilink names: drop the display text, the heading and a table-cell escape."""
    return inner.split("|")[0].split("#")[0].rstrip("\\").strip()


class Vault:
    def __init__(self, root):
        self.root = Path(root) / TEMPLATE
        self.pages = {}
        self.by_name = {}
        self.files = set()
        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(self.root).as_posix()
            self.files.add(rel)
            self.by_name.setdefault(path.name.lower(), []).append(rel)
            if path.suffix == ".md":
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                self.pages[rel] = parse_frontmatter(text)
                self.by_name.setdefault(path.stem.lower(), []).append(rel)

    def resolves(self, target):
        if not target or "{{" in target:
            return True  # a placeholder that setup fills in
        if target in self.files or target + ".md" in self.files:
            return True
        name = target.rsplit("/", 1)[-1].lower()
        return name in self.by_name

    def is_skill(self, rel):
        return rel.startswith("Skills/")


def check_schema(root, fail):
    vault = Vault(root)
    unlinked = 0
    dangling = 0
    undeclared = 0

    for rel, (fields, body) in vault.pages.items():
        if vault.is_skill(rel):
            if rel.endswith("/SKILL.md"):
                declared = "reads" in fields and "writes" in fields
                if not declared:
                    undeclared += 1
                for key in ("reads", "writes"):
                    for folder in fields.get(key, []):
                        if not (vault.root / folder).is_dir():
                            fail(f"{TEMPLATE}/{rel}: {key} names a folder that does not exist: {folder}")
            continue

        page_type = (fields.get("type") or [""])[0]

        for old, new in RETIRED_FIELDS.items():
            if old in fields:
                unlinked += len(fields[old]) or 1

        for field, allowed in RELATIONSHIPS.items():
            if field not in fields:
                continue
            if allowed is not None and page_type not in allowed:
                fail(f"{TEMPLATE}/{rel}: '{field}' is not used on a page of type '{page_type}' (see Knowledge/schema.md)")
            for value in fields[field]:
                links = WIKILINK.findall(value)
                if not links:
                    if not value.strip() or (field == "service" and value in SERVICE_WORDS):
                        continue
                    unlinked += 1
                    continue
                for inner in links:
                    if not vault.resolves(link_target(inner)):
                        fail(f"{TEMPLATE}/{rel}: '{field}' links to a page that does not exist: [[{inner}]]")

        prose = INLINE_CODE.sub("", FENCE.sub("", body))
        for inner in WIKILINK.findall(prose):
            if not vault.resolves(link_target(inner)):
                dangling += 1

    counts = {
        "unlinked_relationship_values": unlinked,
        "dangling_body_links": dangling,
        "skills_without_declarations": undeclared,
    }
    try:
        baseline = json.loads((Path(root) / BASELINE).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        fail(f"{BASELINE}: missing or not valid JSON")
        return counts
    for name, actual in counts.items():
        ceiling = baseline.get(name)
        if ceiling is None:
            fail(f"{BASELINE}: no ceiling for {name}")
        elif actual > ceiling:
            fail(f"schema: {name} rose to {actual} (ceiling {ceiling}); fix the new ones")
        elif actual < ceiling:
            fail(f"schema: {name} fell to {actual}; lower the ceiling in {BASELINE} from {ceiling}")
    return counts
