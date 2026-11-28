"""Spec tests 7 to 9, and the other release rules added to tools/check.py."""

import tempfile
import unittest
from pathlib import Path

from support import PROTECTED_SKILL, ROOT, make_pack, write

import check


def run_rule(rule, *args):
    found = []
    rule(*args, found.append)
    return found


def files_under(root):
    return sorted(
        p.relative_to(root).as_posix() for p in Path(root).rglob("*") if p.is_file()
    )


class RuleCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = make_pack(Path(self._tmp.name) / "repo", version="1.2.3")

    def tearDown(self):
        self._tmp.cleanup()


class Test7NoMainAddress(RuleCase):
    def failures(self):
        return run_rule(check.check_no_main_address, self.repo, files_under(self.repo))

    def test_clean_pack_passes(self):
        self.assertEqual(self.failures(), [])

    def test_each_form_of_a_main_address_fails(self):
        for address in (
            "https://raw.githubusercontent.com/MilUX-Ltd/foothold/main/foothold/x.md",
            "https://github.com/MilUX-Ltd/foothold/blob/main/CHANGELOG.md",
            "https://github.com/milux-ltd/foothold/tree/main/foothold",
            "https://api.github.com/repos/MilUX-Ltd/foothold/git/trees/main?recursive=1",
            "https://api.github.com/repos/MilUX-Ltd/foothold/contents/x?ref=main",
        ):
            with self.subTest(address=address):
                write(self.repo / "foothold/template/Skills/x/SKILL.md", f"Fetch {address}\n")
                found = self.failures()
                self.assertEqual(len(found), 1, found)
                self.assertIn("foothold/template/Skills/x/SKILL.md", found[0])

    def test_another_repository_on_main_is_allowed(self):
        write(
            self.repo / "foothold/template/a.md",
            "https://github.com/ukncsc/Device-Security-Guidance-Configuration-Packs/tree/main/x\n",
        )
        self.assertEqual(self.failures(), [])

    def test_files_outside_foothold_are_not_this_rule(self):
        write(self.repo / "docs/history.md", "https://github.com/MilUX-Ltd/foothold/blob/main/x\n")
        self.assertEqual(self.failures(), [])

    def test_the_real_pack_passes(self):
        found = run_rule(check.check_no_main_address, ROOT, check.all_files())
        self.assertEqual(found, [])


class Test8StartHere(RuleCase):
    def failures(self):
        return run_rule(check.check_start_here, self.repo, "1.2.3")

    def test_present_and_naming_the_version_passes(self):
        self.assertEqual(self.failures(), [])

    def test_missing_fails(self):
        (self.repo / "foothold/Start Here.md").unlink()
        found = self.failures()
        self.assertEqual(len(found), 1)
        self.assertIn("Start Here.md", found[0])

    def test_naming_another_version_fails(self):
        write(self.repo / "foothold/Start Here.md", "This folder is Foothold 1.2.2.\n")
        found = self.failures()
        self.assertTrue(found)
        self.assertIn("1.2.2", " ".join(found))

    def test_naming_no_version_fails(self):
        write(self.repo / "foothold/Start Here.md", "This folder is Foothold.\n")
        self.assertTrue(self.failures())

    def test_the_real_pack_passes(self):
        found = run_rule(check.check_start_here, ROOT, check.newest_version())
        self.assertEqual(found, [])


class Test9PackOwnerFilesProtected(RuleCase):
    def failures(self):
        return run_rule(check.check_pack_owner_protected, self.repo, files_under(self.repo))

    def test_every_file_listed_passes(self):
        # CLAUDE.md in the made-up pack carries the placeholder; list it too.
        write(
            self.repo / "foothold/template/Skills/meta-skills/foothold-update/SKILL.md",
            PROTECTED_SKILL.replace("- `Home.md`", "- `Home.md`\n- `CLAUDE.md`"),
        )
        self.assertEqual(self.failures(), [])

    def test_an_unlisted_file_fails_and_is_named(self):
        found = self.failures()
        self.assertEqual(len(found), 1, found)
        self.assertIn("CLAUDE.md", found[0])

    def test_a_placeholder_in_a_filename_counts(self):
        write(
            self.repo / "foothold/template/Skills/meta-skills/foothold-update/SKILL.md",
            PROTECTED_SKILL.replace("- `Context/<pack_owner>.md`\n", "")
            .replace("- `Home.md`", "- `Home.md`\n- `CLAUDE.md`"),
        )
        found = self.failures()
        self.assertEqual(len(found), 1, found)
        self.assertIn("Context/{{pack_owner}}.md", found[0])

    def test_the_real_pack_passes(self):
        found = run_rule(check.check_pack_owner_protected, ROOT, check.all_files())
        self.assertEqual(found, [])


class TestFilenames(RuleCase):
    def test_ascii_windows_legal_names_pass(self):
        found = run_rule(check.check_filenames, files_under(self.repo))
        self.assertEqual(found, [])

    def test_bad_names_fail_with_the_name(self):
        for name in ("foothold/template/Café.md", "foothold/template/a|b.md", "x/NUL.txt"):
            with self.subTest(name=name):
                found = run_rule(check.check_filenames, [name])
                self.assertEqual(len(found), 1)
                self.assertIn(name, found[0])

    def test_the_real_repository_passes(self):
        self.assertEqual(run_rule(check.check_filenames, check.all_files()), [])


class TestReadmePrompt(RuleCase):
    def test_readme_naming_the_version_passes(self):
        self.assertEqual(run_rule(check.check_readme_prompt, self.repo, "1.2.3"), [])

    def test_readme_naming_another_version_fails(self):
        self.assertTrue(run_rule(check.check_readme_prompt, self.repo, "1.2.4"))

    def test_the_real_readme_passes(self):
        found = run_rule(check.check_readme_prompt, ROOT, check.newest_version())
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
