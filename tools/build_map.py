#!/usr/bin/env python3
"""build_map.py: build the map data file from the vault template.

    python3 tools/build_map.py            # print a summary, write nothing
    python3 tools/build_map.py --write    # write data/foothold-map.json

The file is what a site or a connector reads to draw the vault as a map. It holds two
layers and the routes across them:

- the defence layer: organisations, networks, clusters, programmes, frameworks, portals and
  event series, with the named connections between them (Knowledge/schema.md);
- the business layer: the vault's folders and the skills, with what each skill reads and
  writes;
- the routes: jobs that take more than one skill, in order.

Rules the build keeps, and check.py enforces:

- Every edge is one an author wrote: a frontmatter field, a link in a page's body, a skill's
  reads and writes, or a step in a route. Nothing is inferred.
- No contact page and no field that names a person leaves the vault. Only the fields listed
  in NODE_FIELDS are copied, and no body text is copied at all.
- Companies are not part of the pack's map; the one exception is the pack's own worked
  example.
- The output is the same on every run for the same input.

Standard library only.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import schema_check as sc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = "data/foothold-map.json"
SCHEMA_VERSION = "1.0.0"

DEFENCE_TYPES = {"organisation", "network", "cluster", "programme", "framework", "portal", "event-series"}
COMPANY_FOLDERS = ("CRM/organisations/defence companies/", "CRM/organisations/non-defence companies/")
EXAMPLE_BUSINESS = "CRM/organisations/defence companies/MilUX"
# the only frontmatter fields copied onto a node
NODE_FIELDS = ("name", "acronym", "abbreviation", "status", "category", "website", "region", "audience")
FORBIDDEN_KEYS = {"email", "phone", "linkedin", "led_by", "role", "lawful_basis", "last-contact", "organisation"}
BLOCK = re.compile(r"^description:\s*[|>][+-]?\s*\n((?:[ \t]+.*\n?)+)", re.M)
INLINE = re.compile(r"^description:\s*(.+)$", re.M)


def node_id(rel):
    return rel[:-3] if rel.endswith(".md") else rel


def first(fields, key):
    values = fields.get(key) or []
    return values[0] if values else None


def skill_description(text):
    match = sc.FRONTMATTER.match(text)
    if not match:
        return ""
    front = match.group(1) + "\n"
    block = BLOCK.search(front)
    if block:
        raw = " ".join(line.strip() for line in block.group(1).splitlines())
    else:
        inline = INLINE.search(front)
        raw = sc._unquote(inline.group(1)) if inline else ""
    raw = re.sub(r"\s+", " ", raw).strip()
    # the first sentence says what the skill does; the rest is trigger phrases
    cut = re.search(r"(?<=[.!?])\s", raw)
    return (raw[: cut.start()] if cut else raw)[:300]


class Resolver:
    def __init__(self, vault):
        self.vault = vault
        self.by_stem = {}
        for rel in sorted(vault.pages):
            self.by_stem.setdefault(Path(rel).stem.lower(), []).append(rel)

    def page(self, target):
        """The page a wikilink target names, or None."""
        if not target or "{{" in target:
            return None
        if target + ".md" in self.vault.pages:
            return target + ".md"
        if target in self.vault.pages:
            return target
        found = self.by_stem.get(target.rsplit("/", 1)[-1].lower())
        return found[0] if found else None


def build(root=ROOT):
    root = Path(root)
    vault = sc.Vault(root)
    resolve = Resolver(vault)
    nodes, edges, routes = {}, set(), []

    def add_edge(source, target, kind, origin):
        if source != target:
            edges.add((source, target, kind, origin))

    # ---- defence layer -------------------------------------------------------------
    included = {}
    for rel, (fields, _body) in vault.pages.items():
        if vault.is_skill(rel):
            continue
        kind = first(fields, "type")
        if kind not in DEFENCE_TYPES:
            continue
        ident = node_id(rel)
        if rel.startswith(COMPANY_FOLDERS) and ident != EXAMPLE_BUSINESS:
            continue
        node = {"id": ident, "layer": "defence", "kind": kind, "path": rel}
        if ident == EXAMPLE_BUSINESS:
            node["kind"] = "example-business"
        for key in NODE_FIELDS:
            value = first(fields, key)
            if value:
                node[key] = value
        node.setdefault("name", Path(rel).stem)
        words = [v for v in fields.get("service", []) if v in sc.SERVICE_WORDS]
        if words:
            node["service"] = words
        nodes[ident] = node
        included[rel] = ident

    for rel, ident in included.items():
        fields, body = vault.pages[rel]
        for field in sc.RELATIONSHIPS:
            for value in fields.get(field, []):
                for inner in sc.WIKILINK.findall(value):
                    target = resolve.page(sc.link_target(inner))
                    if target in included:
                        add_edge(ident, included[target], field, "field")
        prose = sc.INLINE_CODE.sub("", sc.FENCE.sub("", body))
        for inner in sc.WIKILINK.findall(prose):
            target = resolve.page(sc.link_target(inner))
            if target in included:
                add_edge(ident, included[target], "mentions", "body")

    # ---- business layer: folders ---------------------------------------------------
    def add_folder(path):
        if path == ".":
            nodes.setdefault(".", {"id": ".", "layer": "business", "kind": "vault", "name": "The whole vault", "path": "."})
            return "."
        parts = path.split("/")
        for depth in range(1, len(parts) + 1):
            sub = "/".join(parts[:depth])
            if sub not in nodes:
                nodes[sub] = {"id": sub, "layer": "business", "kind": "folder", "name": parts[depth - 1], "path": sub}
            if depth > 1:
                add_edge(sub, "/".join(parts[: depth - 1]), "parent", "folder")
        return path

    for entry in sorted(vault.root.iterdir()):
        if entry.is_dir() and not entry.name.startswith("."):
            add_folder(entry.name)
    for rel, (fields, _body) in vault.pages.items():
        if first(fields, "type") == "guide" and not vault.is_skill(rel):
            folder = str(Path(rel).parent.as_posix())
            if folder != ".":
                add_folder(folder)
                nodes[folder]["guide"] = rel

    # each defence page sits in a folder: tie the two layers together
    for rel, ident in included.items():
        folder = str(Path(rel).parent.as_posix())
        while folder not in nodes and "/" in folder:
            folder = folder.rsplit("/", 1)[0]
        if folder in nodes:
            add_edge(ident, folder, "in_folder", "path")

    # ---- business layer: skills ----------------------------------------------------
    skills = {}
    for rel, (fields, _body) in vault.pages.items():
        if not (vault.is_skill(rel) and rel.endswith("/SKILL.md")):
            continue
        ident = node_id(rel)[: -len("/SKILL")]
        name = first(fields, "name") or Path(ident).name
        text = (vault.root / rel).read_text(encoding="utf-8")
        nodes[ident] = {
            "id": ident, "layer": "business", "kind": "skill", "name": name, "path": rel,
            "category": Path(ident).parent.name, "description": skill_description(text),
        }
        skills[name] = ident
        for key in ("reads", "writes"):
            for folder in fields.get(key, []):
                add_edge(ident, add_folder(folder), key, "skill")

    # ---- routes --------------------------------------------------------------------
    for rel, (fields, _body) in sorted(vault.pages.items()):
        if first(fields, "type") != "route":
            continue
        ident = node_id(rel)
        steps = []
        for line in fields.get("steps", []):
            skill, _, does = line.partition(":")
            steps.append({"skill": skill.strip(), "skill_id": skills.get(skill.strip()), "does": does.strip()})
        name = first(fields, "name") or Path(rel).stem
        nodes[ident] = {"id": ident, "layer": "business", "kind": "route", "name": name, "path": rel}
        routes.append({"id": ident, "name": name, "steps": steps})
        for step in steps:
            if step["skill_id"]:
                add_edge(ident, step["skill_id"], "step", "route")

    manifest = json.loads((root / "foothold/.claude-plugin/plugin.json").read_text(encoding="utf-8"))
    return {
        "schema_version": SCHEMA_VERSION,
        "pack_version": manifest.get("version"),
        "nodes": [nodes[key] for key in sorted(nodes)],
        "edges": [
            {"from": s, "to": t, "type": k, "origin": o} for s, t, k, o in sorted(edges)
        ],
        "routes": sorted(routes, key=lambda r: r["id"]),
    }


def render(data):
    return json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def problems(data):
    """Faults in a built map. An empty list means it is fit to publish."""
    out = []
    ids = {node["id"] for node in data["nodes"]}
    for node in data["nodes"]:
        if node["kind"] == "contact":
            out.append(f"map: a contact page reached the data: {node['id']}")
        bad = FORBIDDEN_KEYS & set(node)
        if bad:
            out.append(f"map: {node['id']} carries a field that can name a person: {sorted(bad)}")
    for edge in data["edges"]:
        if edge["from"] not in ids or edge["to"] not in ids:
            out.append(f"map: an edge points at a node that is not there: {edge['from']} -> {edge['to']}")
    for route in data["routes"]:
        if not route["steps"]:
            out.append(f"map: route {route['id']} has no steps")
        for step in route["steps"]:
            if not step["skill_id"]:
                out.append(f"map: route {route['id']} names a skill that does not exist: {step['skill']}")
            if not step["does"]:
                out.append(f"map: route {route['id']} step {step['skill']} does not say what it does")
    return out


def main():
    data = build()
    faults = problems(data)
    kinds = {}
    for node in data["nodes"]:
        kinds[node["kind"]] = kinds.get(node["kind"], 0) + 1
    types = {}
    for edge in data["edges"]:
        types[edge["type"]] = types.get(edge["type"], 0) + 1
    print(f"nodes {len(data['nodes'])}: {dict(sorted(kinds.items()))}")
    print(f"edges {len(data['edges'])}: {dict(sorted(types.items()))}")
    print(f"routes {len(data['routes'])}")
    for fault in faults:
        print("  -", fault)
    if "--write" in sys.argv and not faults:
        target = ROOT / OUTPUT
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(data), encoding="utf-8")
        print(f"wrote {OUTPUT}")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
