"""Shared set-up for the release tests: paths, and a small made-up pack to build from.

Standard library only. Nothing here touches the network.
"""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
UPDATE_SKILL_DIR = ROOT / "foothold/template/Skills/meta-skills/foothold-update"
UPDATE_SKILL = UPDATE_SKILL_DIR / "SKILL.md"
HELPER = UPDATE_SKILL_DIR / "scripts/foothold_changes.py"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def load_helper():
    """Import the update skill's helper from where it ships in the template."""
    spec = importlib.util.spec_from_file_location("foothold_changes", HELPER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["foothold_changes"] = module
    spec.loader.exec_module(module)
    return module


START_HERE = (
    "# Start here\n\n"
    "This folder is Foothold {version}: folders, notes and AI skills.\n\n"
    "## Checking the download\n\n"
    "This is release {version} of github.com/MilUX-Ltd/foothold.\n"
)

PROTECTED_SKILL = """---
name: foothold-update
---

# Update

## Protected files

- `Context/<pack_owner>.md`
- `Home.md`

## Next section
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8")


def make_pack(root, version="1.2.3", start_here_version=None, extra=None):
    """Lay down a minimal pack repository at root and return root.

    extra maps a repository-relative path to text, added after the defaults.
    """
    root = Path(root)
    shv = version if start_here_version is None else start_here_version
    files = {
        "CHANGELOG.md": f"# Foothold changelog\n\n## {version}, 2026-11-27\n\nNotes.\n",
        "LICENSE": "MIT License\n\nCopyright (c) 2026 MilUX Ltd\n",
        "README.md": f"Get foothold-{version}.zip from the latest release.\n",
        ".claude-plugin/marketplace.json": json.dumps(
            {"name": "milux", "plugins": [{"name": "foothold", "version": version}]}
        ),
        "foothold/.claude-plugin/plugin.json": json.dumps({"name": "foothold", "version": version}),
        "foothold/Start Here.md": START_HERE.format(version=shv),
        "foothold/skills/foothold-setup/SKILL.md": "---\nname: foothold-setup\n---\n# Setup\n",
        "foothold/skills/foothold-setup/LICENSE": "MIT License\n",
        "foothold/template/CLAUDE.md": "# Vault for {{pack_owner}}\n",
        "foothold/template/Home.md": "Home of {{pack_owner}}\n",
        "foothold/template/Context/{{pack_owner}}.md": "# {{pack_owner}}\n",
        "foothold/template/Context/.gitkeep": "",
        "foothold/template/Ideas/.gitkeep": "",
        "foothold/template/Intelligence/a.md": "Reference page.\n",
        "foothold/template/.obsidian/app.json": "{}\n",
        "foothold/template/Skills/meta-skills/foothold-update/SKILL.md": PROTECTED_SKILL,
    }
    files.update(extra or {})
    for rel, text in files.items():
        write(root / rel, text)
    return root
