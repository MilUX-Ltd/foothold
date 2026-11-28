"""Spec tests 11 to 13: the update skill and its helper for sorting changes."""

import hashlib
import re
import tempfile
import unittest
from pathlib import Path

from support import UPDATE_SKILL, load_helper, write

changes = load_helper()

VERSION = "2.5.0"
TOP = f"foothold-{VERSION}"


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def blob_sha1(text):
    data = text.encode("utf-8")
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


class Test11SkillReadsReleasesOnly(unittest.TestCase):
    def setUp(self):
        self.text = UPDATE_SKILL.read_text(encoding="utf-8")
        self.helper = changes.__file__ and Path(changes.__file__).read_text(encoding="utf-8")

    def test_no_branch_address(self):
        for text, name in ((self.text, "SKILL.md"), (self.helper, "helper")):
            for pattern in (
                r"/main\b",
                r"trees/main",
                r"blob/main",
                r"heads/",
                r"ref=",
                r"api\.github\.com",
            ):
                with self.subTest(file=name, pattern=pattern):
                    self.assertIsNone(re.search(pattern, text), pattern)

    def test_names_the_latest_release_as_its_source(self):
        self.assertIn(
            "https://github.com/MilUX-Ltd/foothold/releases/latest/download/release-files.txt",
            self.text,
        )

    def test_every_address_is_the_latest_release_or_pinned_to_its_tag(self):
        allowed = (
            r"https://github\.com/MilUX-Ltd/foothold/releases/latest/download/[A-Za-z0-9._-]+",
            r"https://github\.com/MilUX-Ltd/foothold/releases/latest",
            r"https://raw\.githubusercontent\.com/MilUX-Ltd/foothold/v<version>/foothold/template/<path>",
        )
        for url in re.findall(r"https?://[^\s`)\"']+", self.text):
            url = url.rstrip(".,;:")
            with self.subTest(url=url):
                self.assertTrue(any(re.fullmatch(a, url) for a in allowed), url)

    def test_the_rules_are_stated_in_the_prose(self):
        lowered = self.text.lower()
        for phrase in (
            ".obsidian/",
            "if you cannot ask the person, do nothing and report",
            "show and ask each",
            "list and ask once",
            "skill-safety-audit",
            "takes effect the next time",
            "report only",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, lowered)

    def test_the_skill_does_not_replace_itself_and_run_again(self):
        lowered = self.text.lower()
        self.assertNotIn("re-invoke", lowered)
        self.assertNotIn("skill tool to call", lowered)


class FixtureCase(unittest.TestCase):
    """An old vault, as left by the last update, and a new release."""

    OLD = {
        "Skills/meta-skills/foothold-update/SKILL.md": "update v1\n",
        "Skills/business-skills/write-sow/SKILL.md": "sow v1\n",
        "Skills/business-skills/write-sow/scripts/run.py": "print('v1')\n",
        "Skills/Skills Guide.md": "guide v1\n",
        "CLAUDE.md": "rules v1\n",
        "AGENTS.md": "agents v1\n",
        "Knowledge/rules.md": "R-01 v1\n",
        "Resources/Templates/deck.html": "<p>v1</p>\n",
        "Operations/settings.json": '{"a": "v1"}\n',
        "Operations/config.yml": "a: v1\n",
        "Intelligence/defence-landscape/Army.md": "army v1\n",
        "Resources/Reference/Acronyms.md": "acronyms v1\n",
        "Templates/Contact.md": "contact v1\n",
        ".obsidian/app.json": "{}\n",
        ".obsidian/graph.json": "{}\n",
        "Home.md": "home v1\n",
        "Context/{{pack_owner}}.md": "profile\n",
        "Daily/Daily Guide.md": "daily v1\n",
    }
    NEW = {path: text.replace("v1", "v2") for path, text in OLD.items()}
    NEW[".obsidian/app.json"] = '{"theme": "dark"}\n'
    NEW[".obsidian/new.json"] = "{}\n"
    NEW["Skills/pm-skills/new-skill/SKILL.md"] = "brand new skill\n"
    NEW["Resources/Reference/New page.md"] = "brand new page\n"
    NEW["Daily/Daily Guide.md"] = "daily v1\n"  # unchanged upstream

    PROTECTED = {"Home.md", "Context/{{pack_owner}}.md"}
    VALUES = {"pack_owner": "Jane Smith"}

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self._tmp.name) / "vault"
        stored_vault, stored_release = {}, {}
        for path, text in self.OLD.items():
            vault_path = path.replace("{{pack_owner}}", "Jane Smith")
            write(self.vault / vault_path, text)
            stored_vault[vault_path] = sha256(text)
            stored_release[vault_path] = sha256(text)
        self.config = changes.Config(
            values=dict(self.VALUES),
            vault_hashes=stored_vault,
            release_hashes=stored_release,
            legacy={},
        )
        lines = [f"{sha256(t)}  {TOP}/template/{p}" for p, t in sorted(self.NEW.items())]
        lines.append(f"{sha256('x')}  {TOP}/Start Here.md")
        lines.append(f"{sha256('y')}  {TOP}/setup/SKILL.md")
        self.release = changes.parse_release_files("\n".join(lines) + "\n")

    def tearDown(self):
        self._tmp.cleanup()

    def sort(self, config=None):
        return changes.classify(self.release, config or self.config, self.vault, self.PROTECTED)


class Test12Sorting(FixtureCase):
    ASK_EACH = {
        "Skills/meta-skills/foothold-update/SKILL.md",
        "Skills/business-skills/write-sow/SKILL.md",
        "Skills/business-skills/write-sow/scripts/run.py",
        "Skills/Skills Guide.md",
        "Skills/pm-skills/new-skill/SKILL.md",
        "CLAUDE.md",
        "AGENTS.md",
        "Knowledge/rules.md",
        "Resources/Templates/deck.html",
        "Operations/settings.json",
        "Operations/config.yml",
    }
    ASK_ONCE = {
        "Intelligence/defence-landscape/Army.md",
        "Resources/Reference/Acronyms.md",
        "Templates/Contact.md",
        "Resources/Reference/New page.md",
    }

    def test_release_version_is_read_from_the_file_list(self):
        self.assertEqual(self.release.version, VERSION)
        self.assertNotIn("Start Here.md", self.release.files)

    def test_every_change_is_sorted_into_the_right_kind(self):
        result = self.sort()
        got_each = {p for p, c in result.items() if c.category == changes.ASK_EACH}
        got_once = {p for p, c in result.items() if c.category == changes.ASK_ONCE}
        self.assertEqual(got_each, self.ASK_EACH)
        self.assertEqual(got_once, self.ASK_ONCE)

    def test_nothing_under_obsidian_is_offered(self):
        result = self.sort()
        for path in (".obsidian/app.json", ".obsidian/graph.json", ".obsidian/new.json"):
            self.assertEqual(result[path].category, changes.EXCLUDED, path)

    def test_protected_and_unchanged_files_are_not_offered(self):
        result = self.sort()
        self.assertEqual(result["Home.md"].category, changes.PROTECTED)
        self.assertEqual(result["Context/{{pack_owner}}.md"].category, changes.PROTECTED)
        self.assertEqual(result["Daily/Daily Guide.md"].category, changes.UNCHANGED)

    def test_new_files_are_marked_new_and_mapped_to_vault_paths(self):
        result = self.sort()
        self.assertTrue(result["Skills/pm-skills/new-skill/SKILL.md"].new)
        self.assertFalse(result["CLAUDE.md"].new)
        self.assertEqual(result["Home.md"].vault_path, "Home.md")

    def test_a_local_edit_with_an_upstream_change_is_a_conflict(self):
        write(self.vault / "Intelligence/defence-landscape/Army.md", "my own notes\n")
        self.assertEqual(
            self.sort()["Intelligence/defence-landscape/Army.md"].category, changes.CONFLICT
        )

    def test_a_local_edit_with_no_upstream_change_is_left_alone(self):
        write(self.vault / "Daily/Daily Guide.md", "my own daily guide\n")
        self.assertEqual(self.sort()["Daily/Daily Guide.md"].category, changes.LOCAL_ONLY)

    def test_a_release_read_from_an_unzipped_folder_sorts_the_same(self):
        folder = Path(self._tmp.name) / TOP
        for path, text in self.NEW.items():
            write(folder / "template" / path, text)
        write(folder / "Start Here.md", f"This folder is Foothold {VERSION}.\n")
        from_folder = changes.release_from_folder(folder)
        self.assertEqual(from_folder.version, VERSION)
        self.assertEqual(from_folder.files, self.release.files)

    def test_the_sorting_from_the_command_line(self):
        rel = Path(self._tmp.name) / "release-files.txt"
        lines = [f"{sha256(t)}  {TOP}/template/{p}" for p, t in sorted(self.NEW.items())]
        rel.write_text("\n".join(lines) + "\n", encoding="utf-8")
        write(self.vault / ".foothold/config.yml", changes.render_config(self.config))
        skill = Path(self._tmp.name) / "SKILL.md"
        skill.write_text("## Protected files\n\n- `Home.md`\n- `Context/<pack_owner>.md`\n\n## End\n")
        result = changes.sort_from_paths(self.vault, rel, skill)
        self.assertEqual(
            {p for p, c in result.items() if c.category == changes.ASK_EACH}, self.ASK_EACH
        )


class Test13NoStoredChecksum(FixtureCase):
    def without_record(self, vault_path):
        cfg = self.config
        return changes.Config(
            values=cfg.values,
            vault_hashes={k: v for k, v in cfg.vault_hashes.items() if k != vault_path},
            release_hashes={k: v for k, v in cfg.release_hashes.items() if k != vault_path},
            legacy={},
        )

    def test_a_file_with_no_stored_checksum_is_a_conflict(self):
        for path in ("Resources/Reference/Acronyms.md", "Skills/business-skills/write-sow/SKILL.md"):
            with self.subTest(path=path):
                result = self.sort(self.without_record(path))
                self.assertEqual(result[path].category, changes.CONFLICT)

    def test_an_old_style_record_that_still_matches_is_offered(self):
        path = "Resources/Reference/Acronyms.md"
        cfg = self.without_record(path)
        cfg.legacy[path] = blob_sha1(self.OLD[path])
        self.assertEqual(self.sort(cfg)[path].category, changes.ASK_ONCE)

    def test_an_old_style_record_that_no_longer_matches_is_a_conflict(self):
        path = "Resources/Reference/Acronyms.md"
        cfg = self.without_record(path)
        cfg.legacy[path] = blob_sha1("something else\n")
        self.assertEqual(self.sort(cfg)[path].category, changes.CONFLICT)

    def test_a_file_already_the_same_as_the_release_needs_nothing(self):
        path = "Resources/Reference/Acronyms.md"
        write(self.vault / path, self.NEW[path])
        self.assertEqual(self.sort(self.without_record(path))[path].category, changes.UNCHANGED)


class TestHostileInput(unittest.TestCase):
    def test_paths_that_leave_the_release_are_refused(self):
        for bad in (
            f"{TOP}/template/../../.ssh/authorized_keys",
            "/etc/passwd",
            f"{TOP}/template/a\\b.md",
            f"{TOP}/template/./a.md",
            "other-1.0.0/template/a.md",
        ):
            with self.subTest(path=bad):
                with self.assertRaises(changes.ChangesError):
                    changes.parse_release_files(f"{'0' * 64}  {bad}\n")

    def test_a_bad_checksum_line_is_refused(self):
        with self.assertRaises(changes.ChangesError):
            changes.parse_release_files(f"xyz  {TOP}/template/a.md\n")

    def test_two_versions_in_one_list_are_refused(self):
        text = f"{'0' * 64}  {TOP}/template/a.md\n{'0' * 64}  foothold-2.6.0/template/b.md\n"
        with self.assertRaises(changes.ChangesError):
            changes.parse_release_files(text)

    def test_a_substituted_name_that_leaves_the_vault_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            release = changes.parse_release_files(
                f"{'0' * 64}  {TOP}/template/Context/{{{{pack_owner}}}}.md\n"
            )
            cfg = changes.Config(values={"pack_owner": "../../x"}, vault_hashes={},
                                 release_hashes={}, legacy={})
            with self.assertRaises(changes.ChangesError):
                changes.classify(release, cfg, Path(tmp), set())

    def test_protected_list_is_read_from_the_shipped_skill(self):
        protected = changes.read_protected(UPDATE_SKILL.read_text(encoding="utf-8"))
        for path in (
            "Context/{{pack_owner}}.md",
            "Context/Brand.md",
            "Context/Strategy.md",
            "Context/Team.md",
            "Context/Stakeholders.md",
            "Operations/email-signature.md",
            "CLAUDE.md",
            "Home.md",
            "Context/Context Guide.md",
            "Getting Started - Your First Week.md",
            "Skills/business-skills/write-sow/assets/sow-brand.html",
            "Skills/business-skills/write-sow/assets/sow-template.md",
            "Knowledge/domains/brand.md",
            "Context/{{pack_org}}.md",
        ):
            self.assertIn(path, protected)

    def test_config_round_trip(self):
        cfg = changes.Config(
            values={"pack_owner": "Jane Smith", "pack_org": "Acme: Defence"},
            vault_hashes={"Resources/C# notes.md": "a" * 64, "Home.md": "b" * 64},
            release_hashes={"Resources/C# notes.md": "c" * 64},
            legacy={"Old: page.md": "d" * 40},
        )
        parsed = changes.parse_config(changes.render_config(cfg))
        self.assertEqual(parsed, cfg)


if __name__ == "__main__":
    unittest.main()
