"""Tests for the fixes after the sixth safety audit (W1 to W7), 28 November 2026.

Built on audit6/demo/e1 and e2. Standard library only. Nothing here touches the network.
"""

import io
import os
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from support import ROOT, UPDATE_SKILL, load_helper, write

changes = load_helper()

SETUP_SKILL = ROOT / "foothold/skills/foothold-setup/SKILL.md"
SMALL_SKILL = "## Protected files\n\n- `Context/<pack_owner>.md`\n- `Context/<pack_org>.md`\n\n## End\n"


def flat(text):
    return " ".join(text.split())


def run_cli(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = changes.main([str(a) for a in argv])
    return code, out.getvalue(), err.getvalue()


# ---- W1: setup never runs a program found in the target folder ---------------------------------

class W1SetupRunsOnlyTheReleasesHelper(unittest.TestCase):
    def setUp(self):
        self.text = SETUP_SKILL.read_text(encoding="utf-8")

    def test_every_python3_line_runs_the_helper_from_the_template(self):
        lines = [l.strip() for l in self.text.splitlines() if "python3" in l]
        self.assertTrue(lines)
        for line in lines:
            with self.subTest(line=line):
                program = re.match(r'python3 "([^"]+)"', line)
                self.assertIsNotNone(program, line)
                self.assertTrue(program.group(1).startswith("<TEMPLATE_ROOT>/"), line)
                self.assertNotIn("<target>/", program.group(1))
                self.assertNotIn("<vault>", program.group(1))

    def test_a_numbered_rule_near_the_top_says_so(self):
        top = flat(self.text[:self.text.index("## Phase A")])
        self.assertIn("1. **Never run anything that was in the target folder before setup wrote "
                      "it.**", top)
        self.assertIn("Never run the helper from the vault during setup", top)


# ---- W2 and W3: the finish route, and lost checksums ------------------------------------------

class W2W3FinishRoute(unittest.TestCase):
    def setUp(self):
        self.text = flat(SETUP_SKILL.read_text(encoding="utf-8"))

    def test_the_finish_route_records_only_files_that_are_the_templates_copy(self):
        self.assertNotIn("will then be treated as untouched", self.text)
        self.assertIn("record `vault_hashes` only for files that are byte for byte the "
                      "template's copy", self.text)
        self.assertIn("pages changed since the copy will be asked about at the next update",
                      self.text)

    def test_step_a7_saves_the_checksums_at_once_and_says_what_to_do_if_lost(self):
        raw = SETUP_SKILL.read_text(encoding="utf-8")
        step = flat(raw[raw.index("### Step A.7"):raw.index("### Step A.8")])
        self.assertIn("save what it prints at once to a file outside the vault", step)
        self.assertIn("If you no longer have them when you write the record", step)
        self.assertIn("as on the finish route", step)


# ---- W4: which check was made -----------------------------------------------------------------

class W4WhichCheck(unittest.TestCase):
    def setUp(self):
        self.text = flat(UPDATE_SKILL.read_text(encoding="utf-8"))

    def test_arrives_is_defined_and_a_refused_list_stops(self):
        self.assertIn("It arrives when the download completed and the helper accepted the list",
                      self.text)
        self.assertIn("A list that downloads but that the helper refuses stops the run", self.text)

    def test_the_person_is_told_which_check_ran(self):
        self.assertIn("The folder matched the published file list.", self.text)
        self.assertIn("I could not reach the published list, so only the list inside your zip "
                      "was checked; your checksum check is the only check of where it came from.",
                      self.text)


# ---- W5: versions that are not X.Y.Z stop the run ---------------------------------------------

class Lab(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.vault = self.tmp / "vault"
        self.vault.mkdir()
        self.skill = self.tmp / "SKILL.md"
        self.skill.write_text(SMALL_SKILL, encoding="utf-8")
        self.listed = self.tmp / "release-files.txt"

    def tearDown(self):
        self._tmp.cleanup()

    def config(self, **values):
        write(self.vault / ".foothold/config.yml",
              changes.render_config(changes.Config(values=values)))

    def release(self, version="2.5.0", files=None):
        files = files or {"Intelligence/a.md": "a\n"}
        self.listed.write_text("".join(
            f"{changes.sha256_bytes(b.encode())}  foothold-{version}/template/{p}\n"
            for p, b in files.items()), encoding="utf-8")

    def sort(self):
        return changes.sort_from_paths(self.vault, self.listed, self.skill)


class W5VersionForms(Lab):
    def test_a_vault_version_not_in_x_y_z_form_stops(self):
        self.release("2.5.0")
        for bad in ("2.6", "v2.6.0", "2.6.0-rc1", "", "9" * 5000 + ".0.0"):
            with self.subTest(version=bad[:20]):
                self.config(pack_owner="Jane Smith", version=bad)
                with self.assertRaises(changes.ChangesError) as caught:
                    self.sort()
                self.assertIn("X.Y.Z", str(caught.exception))

    def test_a_missing_vault_version_stops(self):
        self.release("2.5.0")
        self.config(pack_owner="Jane Smith")
        with self.assertRaises(changes.ChangesError) as caught:
            self.sort()
        self.assertIn("version", str(caught.exception))

    def test_a_release_version_with_too_many_digits_stops_cleanly(self):
        self.release("1234567890.0.0")
        self.config(pack_owner="Jane Smith", version="2.5.0")
        with self.assertRaises(changes.ChangesError) as caught:
            self.sort()
        self.assertIn("X.Y.Z", str(caught.exception))

    def test_a_good_version_still_works(self):
        self.release("2.10.0")
        self.config(pack_owner="Jane Smith", version="2.9.0")
        self.sort()


# ---- W6: a record without file-name forms -----------------------------------------------------

class W6DerivedForms(Lab):
    FILES = {"Context/{{pack_owner}}.md": "o\n", "Context/{{pack_org}}.md": "g\n",
             "Context/Brand.md": "b\n", "Intelligence/{{pack_org}} brief.md": "x\n"}

    def test_a_sole_trader_without_forms_carries_on(self):
        self.release("2.5.0", self.FILES)
        self.config(version="2.5.0", pack_owner="Jane Smith", pack_org="Jane Smith")
        result = self.sort()
        self.assertEqual(result["Context/{{pack_org}}.md"].vault_path,
                         "Context/Jane Smith (organisation).md")
        self.assertEqual(result["Intelligence/{{pack_org}} brief.md"].vault_path,
                         "Intelligence/Jane Smith (organisation) brief.md")

    def test_forms_are_derived_by_setups_rules(self):
        self.assertEqual(changes.file_name_form("Zoë Brand"), "Zoe Brand")
        self.assertEqual(changes.file_name_form("Maersk A/S"), "Maersk A S")
        self.assertEqual(changes.file_name_form("Ann O'Neill"), "Ann O Neill")
        self.assertEqual(changes.file_name_form("  -Acme: Defence. "), "Acme Defence")
        self.assertEqual(changes.file_name_form("Brand"), "Brand (profile)")
        self.assertEqual(changes.file_name_form("///", org=True), "Organisation")
        self.assertEqual(changes.file_name_form("Jane", org=True, owner_form="jane"),
                         "Jane (organisation)")

    def test_an_owner_named_brand_without_forms_carries_on(self):
        self.release("2.5.0", self.FILES)
        self.config(version="2.5.0", pack_owner="Brand", pack_org="Acme")
        self.assertEqual(self.sort()["Context/{{pack_owner}}.md"].vault_path,
                         "Context/Brand (profile).md")

    def test_an_unsafe_derived_form_stops_and_says_how_to_fix_it(self):
        self.release("2.5.0", self.FILES)
        self.config(version="2.5.0", pack_owner="Jane Smith", pack_org="x" * 250)
        with self.assertRaises(changes.ChangesError) as caught:
            self.sort()
        message = str(caught.exception)
        self.assertIn("pack_org_file", message)
        self.assertIn('pack_org_file: "', message)

    def test_a_derived_form_never_holds_an_apostrophe(self):
        self.release("2.5.0", {"CRM/{{pack_owner}} & echo PWNED & x.md": "y\n"})
        self.config(version="2.5.0", pack_owner="Ann O'Neill")
        result = self.sort()
        self.assertEqual(result["CRM/{{pack_owner}} & echo PWNED & x.md"].vault_path,
                         "CRM/Ann O Neill & echo PWNED & x.md")

    def test_recorded_forms_still_win(self):
        self.release("2.5.0", self.FILES)
        self.config(version="2.5.0", pack_owner="Jane Smith", pack_org="Acme",
                    pack_owner_file="J Smith", pack_org_file="Acme Ltd")
        result = self.sort()
        self.assertEqual(result["Context/{{pack_owner}}.md"].vault_path, "Context/J Smith.md")


# ---- W7: the zip is opened in binary mode on every platform -----------------------------------

class W7BinaryOpen(unittest.TestCase):
    def test_the_open_asks_for_binary_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            zipfile = Path(tmp) / "foothold.zip"
            zipfile.write_bytes(b"PK\r\n\x1a bytes")
            seen = []
            real = os.open

            def spy(path, flags, *args, **kwargs):
                seen.append(flags)
                return real(path, flags & ~0x40000000, *args, **kwargs)

            with mock.patch.object(changes.os, "O_BINARY", 0x40000000, create=True), \
                    mock.patch.object(changes.os, "open", spy):
                digest = changes.zip_checksum(str(zipfile))
            self.assertEqual(digest, changes.sha256_bytes(zipfile.read_bytes()))
            self.assertTrue(seen and seen[0] & 0x40000000)


if __name__ == "__main__":
    unittest.main()
