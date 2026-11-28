"""Spec test 10: the release workflow's guard refuses a bad tag (tools/release_guard.py)."""

import tempfile
import unittest
from pathlib import Path

from support import ROOT, make_pack, write

import release_guard

GOOD = {
    "CHANGELOG.md": "2.5.0",
    "foothold/.claude-plugin/plugin.json": "2.5.0",
    ".claude-plugin/marketplace.json": "2.5.0",
    "data/foothold-map.json": "2.5.0",
}


class Test10Guard(unittest.TestCase):
    def test_a_matching_tag_on_main_passes(self):
        self.assertEqual(release_guard.problems("v2.5.0", GOOD, on_main=True), [])

    def test_a_tag_that_does_not_match_the_records_is_refused(self):
        found = release_guard.problems("v2.5.1", GOOD, on_main=True)
        self.assertTrue(found)
        self.assertIn("2.5.1", " ".join(found))

    def test_one_record_out_of_step_is_refused_and_named(self):
        records = dict(GOOD, **{"data/foothold-map.json": "2.4.0"})
        found = release_guard.problems("v2.5.0", records, on_main=True)
        self.assertEqual(len(found), 1, found)
        self.assertIn("data/foothold-map.json", found[0])

    def test_a_missing_record_is_refused(self):
        records = dict(GOOD, **{".claude-plugin/marketplace.json": None})
        self.assertTrue(release_guard.problems("v2.5.0", records, on_main=True))

    def test_a_tag_not_on_main_is_refused(self):
        found = release_guard.problems("v2.5.0", GOOD, on_main=False)
        self.assertEqual(len(found), 1, found)
        self.assertIn("main", found[0])

    def test_malformed_tags_are_refused(self):
        for tag in ("2.5.0", "v2.5", "v2.5.0-rc1", "v2.5.0 ", "release-2.5.0", "v02.5.0", ""):
            with self.subTest(tag=tag):
                self.assertTrue(release_guard.problems(tag, GOOD, on_main=True))

    def test_records_are_read_from_a_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_pack(Path(tmp), version="1.2.3")
            write(repo / "data/foothold-map.json", '{\n  "pack_version": "1.2.3"\n}\n')
            records = release_guard.read_records(repo)
        self.assertEqual(set(records), set(GOOD))
        self.assertEqual(set(records.values()), {"1.2.3"})

    def test_the_real_records_agree_with_each_other(self):
        records = release_guard.read_records(ROOT)
        self.assertEqual(len(set(records.values())), 1, records)
        self.assertEqual(records["CHANGELOG.md"], "2.5.0")


if __name__ == "__main__":
    unittest.main()
