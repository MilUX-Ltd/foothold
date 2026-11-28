"""Spec tests 1 to 6: the release script (tools/build_release.py)."""

import hashlib
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from support import ROOT, make_pack, write

import build_release


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class BuildCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = make_pack(self.tmp / "repo", version="1.2.3")

    def tearDown(self):
        self._tmp.cleanup()

    def build(self, name="out", repo=None):
        out = self.tmp / name
        result = build_release.build(repo or self.repo, out)
        return out, result


class Test1SameBytes(BuildCase):
    def test_two_builds_of_the_same_tree_are_identical(self):
        out_a, _ = self.build("a")
        # Change file times between builds: they must not reach the zip.
        later = 2_000_000_000
        for path in (self.repo / "foothold").rglob("*"):
            os.utime(path, (later, later))
        out_b, _ = self.build("b")
        a = (out_a / "foothold-1.2.3.zip").read_bytes()
        b = (out_b / "foothold-1.2.3.zip").read_bytes()
        self.assertEqual(sha256(a), sha256(b))
        self.assertEqual(a, b)

    def test_the_real_repository_builds_the_same_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = build_release.build(ROOT, Path(tmp) / "a")
            second = build_release.build(ROOT, Path(tmp) / "b")
            self.assertEqual(first["zip_sha256"], second["zip_sha256"])

    def test_entries_are_in_name_order_with_fixed_metadata(self):
        out, _ = self.build()
        with zipfile.ZipFile(out / "foothold-1.2.3.zip") as zf:
            infos = zf.infolist()
            names = [i.filename for i in infos]
            self.assertEqual(names, sorted(names))
            for info in infos:
                self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(info.extra, b"")
                self.assertEqual(info.external_attr >> 16, 0o100644)
                self.assertEqual(info.create_system, 3)


class Test2Layout(BuildCase):
    def test_one_top_folder_with_the_four_items_and_no_plugin_manifest(self):
        out, _ = self.build()
        with zipfile.ZipFile(out / "foothold-1.2.3.zip") as zf:
            names = zf.namelist()
        tops = {n.split("/", 1)[0] for n in names}
        self.assertEqual(tops, {"foothold-1.2.3"})
        second = {n.split("/")[1] for n in names}
        self.assertEqual(second, {"Start Here.md", "LICENSE", "template", "setup"})
        self.assertIn("foothold-1.2.3/setup/SKILL.md", names)
        self.assertIn("foothold-1.2.3/template/CLAUDE.md", names)
        self.assertIn("foothold-1.2.3/template/.obsidian/app.json", names)
        for name in names:
            self.assertNotIn(".claude-plugin", name)
            self.assertFalse(name.endswith("plugin.json"), name)

    def test_gitkeep_left_out_only_where_the_folder_has_other_content(self):
        out, _ = self.build()
        with zipfile.ZipFile(out / "foothold-1.2.3.zip") as zf:
            names = zf.namelist()
        self.assertNotIn("foothold-1.2.3/template/Context/.gitkeep", names)
        self.assertIn("foothold-1.2.3/template/Ideas/.gitkeep", names)

    def test_os_clutter_is_left_out(self):
        write(self.repo / "foothold/template/.DS_Store", b"\0junk")
        out, _ = self.build()
        with zipfile.ZipFile(out / "foothold-1.2.3.zip") as zf:
            self.assertFalse(any(n.endswith(".DS_Store") for n in zf.namelist()))


class Test3FileList(BuildCase):
    def test_every_file_is_listed_with_a_matching_checksum_and_nothing_else(self):
        out, _ = self.build()
        lines = (out / "release-files.txt").read_text(encoding="utf-8").splitlines()
        listed = {}
        for line in lines:
            digest, sep, path = line.partition("  ")
            self.assertEqual(sep, "  ", line)
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
            listed[path] = digest
        self.assertEqual(len(listed), len(lines), "a path is listed twice")
        with zipfile.ZipFile(out / "foothold-1.2.3.zip") as zf:
            in_zip = {n: sha256(zf.read(n)) for n in zf.namelist() if not n.endswith("/")}
        self.assertEqual(listed, in_zip)


class Test4Sums(BuildCase):
    def test_sha256sums_matches_the_zip(self):
        out, result = self.build()
        zip_bytes = (out / "foothold-1.2.3.zip").read_bytes()
        self.assertEqual(
            (out / "SHA256SUMS.txt").read_text(encoding="utf-8"),
            f"{sha256(zip_bytes)}  foothold-1.2.3.zip\n",
        )
        self.assertEqual(result["zip_sha256"], sha256(zip_bytes))


class Test5NamesVersionAndChecksum(BuildCase):
    def test_start_here_in_the_zip_names_the_version(self):
        out, _ = self.build()
        with zipfile.ZipFile(out / "foothold-1.2.3.zip") as zf:
            text = zf.read("foothold-1.2.3/Start Here.md").decode("utf-8")
        self.assertIn("Foothold 1.2.3", text)
        self.assertIn("release 1.2.3", text)
        self.assertNotIn("{version}", text)

    def test_a_version_placeholder_in_start_here_is_filled(self):
        write(self.repo / "foothold/Start Here.md", "This folder is Foothold {version}.\n")
        out, _ = self.build()
        with zipfile.ZipFile(out / "foothold-1.2.3.zip") as zf:
            text = zf.read("foothold-1.2.3/Start Here.md").decode("utf-8")
        self.assertEqual(text, "This folder is Foothold 1.2.3.\n")

    def test_start_here_naming_another_version_fails_the_build(self):
        write(self.repo / "foothold/Start Here.md", "This folder is Foothold 9.9.9.\n")
        with self.assertRaises(build_release.ReleaseError) as caught:
            self.build()
        self.assertIn("9.9.9", str(caught.exception))

    def test_the_install_prompt_names_the_version_and_the_real_checksum(self):
        out, result = self.build()
        zip_sum = sha256((out / "foothold-1.2.3.zip").read_bytes())
        notes = (out / "release-notes.md").read_text(encoding="utf-8")
        self.assertIn(
            "https://github.com/MilUX-Ltd/foothold/releases/download/v1.2.3/foothold-1.2.3.zip",
            notes,
        )
        self.assertIn(zip_sum, notes)
        prompt = build_release.install_prompt("1.2.3", zip_sum)
        self.assertIn(prompt, notes)
        self.assertEqual(
            prompt,
            "Download https://github.com/MilUX-Ltd/foothold/releases/download/v1.2.3/"
            f"foothold-1.2.3.zip. Check that its SHA-256 checksum is {zip_sum}. If it is not, "
            "stop and tell me. If it is, unzip it and read Start Here.md inside.",
        )


class Test6BadNames(BuildCase):
    def assert_refused(self, rel, shown):
        write(self.repo / "foothold/template" / rel, "x\n")
        with self.assertRaises(build_release.ReleaseError) as caught:
            self.build()
        self.assertIn(shown, str(caught.exception))

    def test_non_ascii_name_fails_with_the_name(self):
        self.assert_refused("Café notes.md", "Café notes.md")

    def test_windows_reserved_character_fails_with_the_name(self):
        self.assert_refused("a:b.md", "a:b.md")

    def test_windows_reserved_device_name_fails(self):
        self.assert_refused("CON.md", "CON.md")

    def test_trailing_dot_fails(self):
        self.assert_refused("Notes/trailing.", "trailing.")

    def test_names_the_pack_uses_today_are_allowed(self):
        for name in (
            "Context/{{pack_owner}}.md",
            "Keen D&S Tech Fund.md",
            "Defence AI Centre (DAIC).md",
            "Pitch Deck Example - Apple (light).html",
        ):
            self.assertIsNone(build_release.bad_name("foothold-1.2.3/template/" + name), name)


if __name__ == "__main__":
    unittest.main()
