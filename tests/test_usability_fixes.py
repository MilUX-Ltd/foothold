"""Tests for the usability fixes G1, G2 and G5 (Pack Usability Fix Proposal, 28 November 2026).

G1: the zip carries its own release-files.txt; the helper runs from a vouched folder's own list,
and works out a zip file's SHA-256 for the person to compare. G2: setup asks, copies, fills,
builds and records in that order, from a fixed list of placeholders that tools/check.py
enforces. G5: a scheduled run reports in fixed words and writes nothing.

Standard library only. Nothing here touches the network: every test that could reach it
replaces the downloader with one that fails the test.
"""

import hashlib
import io
import os
import re
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from support import ROOT, UPDATE_SKILL, load_helper, make_pack, write

import build_release
import check

changes = load_helper()

SETUP_SKILL = ROOT / "foothold/skills/foothold-setup/SKILL.md"
TEMPLATE = ROOT / "foothold/template"
VERSION = "1.2.3"
TOP = f"foothold-{VERSION}"
SMALL_SKILL = "## Protected files\n\n- `Home.md`\n- `Context/<pack_owner>.md`\n\n## End\n"


def sha256(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def run_cli(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = changes.main([str(a) for a in argv])
    return code, out.getvalue(), err.getvalue()


def no_network(*args, **kwargs):
    raise AssertionError("nothing on the folder route may use the network")


def flat(text):
    return " ".join(text.split())


# ---- G1: the zip carries its own list --------------------------------------------------------

class ReleaseBuild(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = make_pack(self.tmp / "repo", version=VERSION)

    def tearDown(self):
        self._tmp.cleanup()

    def build(self, name="out"):
        out = self.tmp / name
        return out, build_release.build(self.repo, out, from_tree=True)


class G1ListInsideTheZip(ReleaseBuild):
    def test_the_zip_holds_release_files_txt_at_the_top_of_its_folder(self):
        out, _ = self.build()
        with zipfile.ZipFile(out / f"{TOP}.zip") as zf:
            self.assertIn(f"{TOP}/release-files.txt", zf.namelist())

    def test_the_list_inside_is_the_published_list_byte_for_byte(self):
        out, _ = self.build()
        with zipfile.ZipFile(out / f"{TOP}.zip") as zf:
            inside = zf.read(f"{TOP}/release-files.txt")
        self.assertEqual(inside, (out / "release-files.txt").read_bytes())

    def test_the_list_names_every_other_file_and_not_itself(self):
        out, _ = self.build()
        with zipfile.ZipFile(out / f"{TOP}.zip") as zf:
            in_zip = {n: sha256(zf.read(n)) for n in zf.namelist()}
        listed = {}
        for line in (out / "release-files.txt").read_text(encoding="utf-8").splitlines():
            digest, _, path = line.partition("  ")
            listed[path] = digest
        del in_zip[f"{TOP}/release-files.txt"]
        self.assertEqual(listed, in_zip)

    def test_two_builds_are_still_the_same_bytes(self):
        a, first = self.build("a")
        b, second = self.build("b")
        self.assertEqual(first["zip_sha256"], second["zip_sha256"])
        self.assertEqual((a / f"{TOP}.zip").read_bytes(), (b / f"{TOP}.zip").read_bytes())

    def test_the_release_notes_say_the_list_is_also_inside_the_zip(self):
        out, _ = self.build()
        notes = (out / "release-notes.md").read_text(encoding="utf-8")
        self.assertIn("The same file is inside the zip", notes)


class Unzipped(ReleaseBuild):
    """A built release, unzipped into its own folder, and a vault set up from it."""

    def setUp(self):
        super().setUp()
        out, _ = self.build()
        self.unzip_root = self.tmp / "unzipped"
        with zipfile.ZipFile(out / f"{TOP}.zip") as zf:
            zf.extractall(self.unzip_root)
        self.folder = self.unzip_root / TOP
        self.published = out / "release-files.txt"
        self.vault = self.tmp / "vault"
        self.vault.mkdir()
        cfg = changes.Config(values={"version": "1.2.3", "pack_owner": "Jane Smith"})
        write(self.vault / ".foothold/config.yml", changes.render_config(cfg))
        self.skill = self.tmp / "SKILL.md"
        self.skill.write_text(SMALL_SKILL, encoding="utf-8")
        self.temp = self.tmp / "dl"
        self.temp.mkdir()

    def fetch(self, *args, **kwargs):
        with redirect_stdout(io.StringIO()):
            return changes.fetch(self.vault, *args, skill_md=self.skill, download=no_network,
                                 **kwargs)


class G1HelperRunsFromTheFoldersOwnList(Unzipped):
    def test_the_folder_list_is_read_and_the_folder_checked(self):
        release = changes.folder_list(self.folder)
        self.assertEqual(release.version, VERSION)
        self.assertIn("Intelligence/a.md", release.files)
        self.assertTrue(release.lines["Intelligence/a.md"] > 0)

    def test_sort_on_the_folder_uses_its_list(self):
        code, out, err = run_cli("sort", self.vault, self.folder, "--skill", self.skill)
        self.assertEqual(code, 0, err)
        self.assertIn("Intelligence/a.md", out)

    def test_fetch_show_and_record_work_from_the_folder_with_no_network(self):
        with mock.patch.object(changes, "https_download", no_network), \
                mock.patch.object(changes.urllib.request, "urlopen", no_network):
            items = self.fetch(self.folder, self.temp)
            self.assertTrue(items)
            self.assertTrue(all(i["status"] == "ok" for i in items), items)
            number = next(i["number"] for i in items if i["path"] == "Intelligence/a.md")
            page = changes.show(self.vault, self.folder, self.temp, number, self.skill)
            self.assertIn("| Reference page.", page)
            write(self.vault / "Intelligence/a.md", "Reference page.\n")
            out = changes.record(self.vault, self.folder, self.temp, [number],
                                 skill_md=self.skill)
        self.assertIn('"Intelligence/a.md": ', out)
        self.assertIn(sha256("Reference page.\n"), out)

    def test_fetch_from_the_folder_on_the_command_line(self):
        with mock.patch.object(changes, "https_download", no_network):
            code, out, err = run_cli("fetch", self.vault, self.folder, self.temp,
                                     "--skill", self.skill)
        self.assertEqual(code, 0, err)
        self.assertIn("checked", out)

    def test_a_template_file_changed_after_unzipping_is_refused(self):
        write(self.folder / "template/Intelligence/a.md", "tampered\n")
        with self.assertRaises(changes.ChangesError) as caught:
            self.fetch(self.folder, self.temp)
        self.assertIn("does not match", str(caught.exception))
        self.assertEqual(list(self.temp.iterdir()), [])

    def test_a_file_outside_the_template_is_checked_too(self):
        write(self.folder / "setup/SKILL.md", "tampered setup\n")
        with self.assertRaises(changes.ChangesError):
            changes.folder_list(self.folder)

    def test_an_extra_file_is_refused_without_naming_it(self):
        write(self.folder / "template/Skills/evil/SKILL.md", "added\n")
        with self.assertRaises(changes.ChangesError) as caught:
            changes.folder_list(self.folder)
        self.assertNotIn("evil", str(caught.exception))

    def test_a_missing_file_is_refused(self):
        (self.folder / "Start Here.md").unlink()
        with self.assertRaises(changes.ChangesError):
            changes.folder_list(self.folder)

    def test_a_link_in_the_folder_is_refused(self):
        os.symlink(self.tmp / "vault", self.folder / "template/linked")
        with self.assertRaises(changes.ChangesError):
            changes.folder_list(self.folder)

    def test_the_list_itself_is_excepted_but_must_be_a_plain_file(self):
        changes.folder_list(self.folder)  # its own line is not required
        listed = self.folder / "release-files.txt"
        text = listed.read_text(encoding="utf-8")
        listed.unlink()
        os.symlink(self.published, listed)
        with self.assertRaises(changes.ChangesError):
            changes.folder_list(self.folder)
        listed.unlink()
        listed.write_text(text, encoding="utf-8")
        changes.folder_list(self.folder)

    def test_a_bad_line_in_the_folders_list_refuses_the_folder(self):
        listed = self.folder / "release-files.txt"
        listed.write_text(listed.read_text(encoding="utf-8")
                          + f"{'0' * 64}  {TOP}/template/a' & echo x & '.md\n", encoding="utf-8")
        with self.assertRaises(changes.ChangesError) as caught:
            changes.folder_list(self.folder)
        self.assertIn("U+0027", str(caught.exception))

    def test_a_list_for_another_version_is_refused(self):
        renamed = self.unzip_root / "foothold-9.9.9"
        self.folder.rename(renamed)
        with self.assertRaises(changes.ChangesError):
            changes.folder_list(renamed)

    def test_the_folder_and_release_folder_option_together_are_refused(self):
        with self.assertRaises(changes.ChangesError):
            self.fetch(self.folder, self.temp, release_folder=self.folder)

    def test_a_folder_with_no_list_is_a_defined_refusal(self):
        (self.folder / "release-files.txt").unlink()
        with self.assertRaises(changes.ChangesError) as caught:
            self.fetch(self.folder, self.temp)
        message = str(caught.exception)
        self.assertIn("no release-files.txt", message)
        self.assertIn("older", message)

    def test_show_rechecks_the_folder(self):
        items = self.fetch(self.folder, self.temp)
        write(self.folder / "setup/SKILL.md", "tampered later\n")
        with self.assertRaises(changes.ChangesError):
            changes.show(self.vault, self.folder, self.temp, items[0]["number"], self.skill)


class G1ADownloadedListStillComesFirst(Unzipped):
    def test_the_downloaded_list_with_the_folder_works(self):
        items = self.fetch(self.published, self.temp, release_folder=self.folder)
        self.assertTrue(all(i["status"] == "ok" for i in items))

    def test_the_folder_must_match_the_downloaded_list_outside_the_template_too(self):
        write(self.folder / "setup/SKILL.md", "tampered setup\n")
        with self.assertRaises(changes.ChangesError):
            self.fetch(self.published, self.temp, release_folder=self.folder)

    def test_the_folders_own_list_must_be_the_downloaded_list(self):
        listed = self.folder / "release-files.txt"
        listed.write_text(listed.read_text(encoding="utf-8") + "\n\n", encoding="utf-8")
        with self.assertRaises(changes.ChangesError) as caught:
            self.fetch(self.published, self.temp, release_folder=self.folder)
        self.assertIn("not the same", str(caught.exception))

    def test_sort_with_the_downloaded_list_checks_the_whole_folder(self):
        write(self.folder / "LICENSE", "changed\n")
        with self.assertRaises(changes.ChangesError):
            changes.sort_from_paths(self.vault, self.folder, self.skill,
                                    release_files=self.published)


# ---- G1: the zip's checksum, for the person to compare ----------------------------------------

class G1ZipChecksum(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.zip = self.tmp / "Downloads" / "foothold-2.5.0 (1).zip"
        write(self.zip, b"PK\x03\x04 not really a zip, but bytes all the same")

    def tearDown(self):
        self._tmp.cleanup()

    def test_it_prints_the_sha256_and_does_not_compare(self):
        with mock.patch.object(changes, "https_download", no_network):
            code, out, err = run_cli("zip-checksum", self.zip)
        self.assertEqual(code, 0, err)
        self.assertIn(sha256(self.zip.read_bytes()), out)
        self.assertIn("does not compare", out)
        self.assertNotIn("match", out.lower().replace("does not compare", ""))

    def test_a_link_is_refused(self):
        link = self.tmp / "Downloads" / "link.zip"
        os.symlink(self.zip, link)
        code, out, err = run_cli("zip-checksum", link)
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("link", err)

    def test_a_folder_is_refused(self):
        folder = self.tmp / "folder.zip"
        folder.mkdir()
        code, out, _ = run_cli("zip-checksum", folder)
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")

    def test_a_name_with_a_character_outside_the_rule_asks_to_move_or_rename(self):
        for name in ("O'Neill.zip", "a$b.zip", "café.zip", "x;y.zip", "a`b.zip"):
            with self.subTest(name=name):
                path = self.tmp / name
                write(path, b"x")
                code, out, err = run_cli("zip-checksum", path)
                self.assertNotEqual(code, 0)
                self.assertEqual(out, "")
                self.assertIn("move or rename", err)
                self.assertNotIn(name, err)

    def test_dot_dot_and_a_leading_dash_are_refused(self):
        for path in (str(self.tmp / "Downloads" / ".." / "Downloads" / self.zip.name),
                     "-rf.zip", "relative/-x.zip"):
            with self.subTest(path=path):
                code, out, _ = run_cli("zip-checksum", path)
                self.assertNotEqual(code, 0)
                self.assertEqual(out, "")

    def test_only_a_zip_file(self):
        other = self.tmp / "notes.txt"
        write(other, b"x")
        code, out, _ = run_cli("zip-checksum", other)
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")

    def test_a_file_over_the_cap_is_refused(self):
        with mock.patch.object(changes, "MAX_ZIP", 10):
            code, out, err = run_cli("zip-checksum", self.zip)
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("larger", err)

    def test_a_missing_file_is_refused(self):
        code, out, _ = run_cli("zip-checksum", self.tmp / "gone.zip")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")


# ---- G1 and G5: the update skill's words ------------------------------------------------------

G1_ASK = ("Before I use this folder: did you compare the zip's checksum with the one on the "
          "release page? If you have not, I can work out your zip's checksum now and show it to "
          "you, and you compare the two.")
G1_SHOW = ("Your zip's SHA-256 is: `<checksum>`. Open "
           "https://github.com/MilUX-Ltd/foothold/releases/latest and find the SHA-256 beside "
           "the zip. Do they match exactly?")
G1_YES = ("Thank you. Your check is the only check of where this zip came from. I will also "
          "check every file in the folder against the list inside it, which shows whether "
          "anything was damaged.")
G1_CANNOT = ("I cannot use this folder without that check, and nothing in your vault has "
             "changed. You can download the zip again and check it, or leave the update for now.")
G5_UP_TO_DATE = "Your vault is on Foothold `<version>`, the latest release. Nothing was changed."
G5_WAITING = ("Foothold `<new>` is out; your vault is on `<old>`. It changes `<n>` files. Nothing "
              "was changed. Say \"update Foothold\" when you are at your computer.")
G5_NOT_REACHED = ("This check could not reach the Foothold release, so it cannot say what is new. "
                  "Nothing was changed.")


class G1UpdateSkillWording(unittest.TestCase):
    def setUp(self):
        self.text = UPDATE_SKILL.read_text(encoding="utf-8")
        self.flat = flat(self.text)

    def test_the_four_lines_are_used_exactly(self):
        for line in (G1_ASK, G1_SHOW, G1_YES, G1_CANNOT):
            with self.subTest(line=line[:30]):
                self.assertIn(line, self.flat)

    def test_it_says_what_the_list_inside_the_zip_does_not_show(self):
        self.assertIn("no proof of who made the zip", self.flat)

    def test_the_checksum_command_is_named_with_the_zip_file_the_person_gave(self):
        self.assertIn('foothold_changes.py" zip-checksum "<zip file>"', self.text)

    def test_rule_6_adds_exactly_the_zip_file(self):
        rule6 = re.search(r"\n6\. \*\*.*", self.text).group(0)
        self.assertIn("the zip file the person gave you", rule6)

    def test_fetch_show_and_record_run_from_the_folder(self):
        for command in ('fetch "<vault>" "<release folder>" "<temporary folder>"',
                        'show "<vault>" "<release folder>" "<temporary folder>" <number>',
                        'record "<vault>" "<release folder>" "<temporary folder>"'):
            with self.subTest(command=command):
                self.assertIn(command, self.text)

    def test_the_no_list_folder_is_a_defined_case(self):
        without = self.text[self.text.index("## Without the helper"):
                            self.text.index("## Step 1")]
        self.assertIn("has no `release-files.txt`", without)
        self.assertIn("cannot run Python", without)


class G5ScheduledRuns(unittest.TestCase):
    def setUp(self):
        self.text = UPDATE_SKILL.read_text(encoding="utf-8")
        self.flat = flat(self.text)

    def section(self):
        start = self.text.index("## Scheduled or unattended runs")
        return flat(self.text[start:self.text.index("\n## ", start + 5)])

    def test_the_section_exists_with_the_three_reports_exactly(self):
        section = self.section()
        for line in (G5_UP_TO_DATE, G5_WAITING, G5_NOT_REACHED):
            with self.subTest(line=line[:30]):
                self.assertIn(line, section)

    def test_the_report_goes_to_the_jobs_own_output_never_the_vault(self):
        section = self.section()
        self.assertIn("the job's own output", section)
        self.assertIn("never into the vault", section)

    def test_a_scheduled_run_may_not_fetch_show_or_record(self):
        section = self.section()
        for word in ("`fetch`", "`show`", "`record`"):
            self.assertIn(word, section)
        self.assertIn("may not", section)

    def test_a_folder_named_in_the_request_still_tries_the_list_once(self):
        self.assertIn("If the person names the folder in their request, still try once", self.flat)


# ---- G2: setup's order, values and placeholder list -------------------------------------------

STAKEHOLDERS_EMPTY = ("Nothing here yet. Add the people and organisations that matter to your "
                      "business as you meet them.")


class G2SetupOrder(unittest.TestCase):
    def setUp(self):
        self.text = SETUP_SKILL.read_text(encoding="utf-8")
        self.flat = flat(self.text)

    def at(self, needle):
        self.assertIn(needle, self.text)
        return self.text.index(needle)

    def test_the_essentials_are_asked_with_where_before_anything_is_copied(self):
        ask = self.at("### Step A.1")
        copy = self.at("### Step A.4")
        section = self.text[ask:copy]
        for word in ("name", "role", "organisation", "website", "email"):
            self.assertIn(word, section)
        self.assertIn("Shall I set Foothold up at", section)

    def test_ask_copy_fill_build_record_in_that_order(self):
        order = [self.at("### Step A.1"), self.at("### Step A.5"), self.at("### Step A.7"),
                 self.at("## Phase B Build"), self.at("## Write the record")]
        self.assertEqual(order, sorted(order))

    def test_the_record_is_written_once_at_the_end(self):
        record = self.text[self.at("## Write the record"):self.at("## Phase D")]
        self.assertIn("once, after the schedule questions", flat(record))
        self.assertNotIn("Step A.4: Write `.foothold/config.yml`", self.text)

    def test_the_interview_does_not_ask_for_name_or_role_again(self):
        q1 = self.text[self.at("**Q1"):self.at("**Q2")]
        self.assertNotIn("Your name, role", q1)
        self.assertIn("already have your name and role", flat(q1))

    def test_no_any_token_rule(self):
        self.assertNotIn("any `{{...}}` token", self.text)

    def test_every_value_has_a_source(self):
        for phrase in ("First word of the name", "Foothold\" unless the person asks",
                       "company suffix", "The day setup runs", "Empty unless the person offers"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.flat)

    def test_the_record_schema_lists_every_setup_placeholder(self):
        fills, _ = check.setup_placeholder_lists(self.text)
        for name in fills:
            with self.subTest(name=name):
                self.assertRegex(self.text, rf"(?m)^  {name}: ")

    def test_an_empty_page_says_so_and_stakeholders_uses_the_given_words(self):
        self.assertIn(STAKEHOLDERS_EMPTY, self.text)
        self.assertNotIn("Only create canonical pages that have real content", self.text)
        self.assertNotIn("Skip files where there is no supporting data", self.text)

    def test_one_shape_for_the_schedule_record(self):
        self.assertNotIn("same shape as the update schedule", self.text)
        for key in ("update:", "daily_brief:", "curator:", "check_in:"):
            self.assertRegex(self.text, rf"(?m)^  {key}")

    def test_the_initiatives_folders_are_created(self):
        self.assertIn("Initiatives/active", self.text)
        self.assertIn("Initiatives/completed", self.text)

    def test_the_check_in_offer_says_where_it_sits(self):
        self.assertNotIn("After the update-schedule question, offer one more thing", self.text)


class G2Template(unittest.TestCase):
    def test_the_company_page_stub_exists_like_the_operator_page(self):
        page = TEMPLATE / "Context/{{pack_org}}.md"
        self.assertTrue(page.is_file())
        text = page.read_text(encoding="utf-8")
        self.assertIn("type: organisation", text)
        self.assertIn("# {{pack_org}}", text)
        self.assertIn("website: {{pack_org_website}}", text)

    def test_the_domains_folder_ships(self):
        self.assertTrue((TEMPLATE / "Knowledge/domains").is_dir())
        self.assertTrue(any((TEMPLATE / "Knowledge/domains").iterdir()))

    def test_the_company_page_is_protected(self):
        protected = changes.read_protected(UPDATE_SKILL.read_text(encoding="utf-8"))
        self.assertIn("Context/{{pack_org}}.md", protected)

    def test_getting_started_names_no_particular_ai_product(self):
        text = (TEMPLATE / "Getting Started - Your First Week.md").read_text(encoding="utf-8")
        self.assertNotIn("Cowork", text)


SETUP_WITH_LISTS = """# Setup

### The placeholders setup fills

- `{{pack_owner}}`: the name.
- `{{install_date}}`: the day.

### Placeholders that are not setup's

- mobilise-engagement: `{{title}}`
- write-sow: `{{DATE}}`

```yaml
foothold:
  pack_owner: <value>
  pack_owner_file: <value>
  install_date: <value>
```

| File | Sources |
|---|---|
| `Context/<pack_owner>.md` | Q1 |
"""


def run_rule(rule, *args):
    found = []
    rule(*args, found.append)
    return found


class G2CheckEnforcesTheList(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = make_pack(Path(self._tmp.name) / "repo", version=VERSION, extra={
            "foothold/skills/foothold-setup/SKILL.md": SETUP_WITH_LISTS,
        })

    def tearDown(self):
        self._tmp.cleanup()

    def files(self):
        return sorted(p.relative_to(self.repo).as_posix()
                      for p in self.repo.rglob("*") if p.is_file())

    def failures(self):
        return run_rule(check.check_setup_placeholders, self.repo, self.files())

    def test_a_pack_using_only_listed_placeholders_passes(self):
        write(self.repo / "foothold/template/Skills/crm-skills/mobilise-engagement/x.md",
              "{{title}} {{n x n}}\n")
        write(self.repo / "foothold/template/Skills/business-skills/write-sow/x.md", "{{DATE}}\n")
        self.assertEqual(self.failures(), [])

    def test_a_new_placeholder_not_on_either_list_fails(self):
        write(self.repo / "foothold/template/Home.md", "Home of {{pack_owner_nickname}}\n")
        found = self.failures()
        self.assertEqual(len(found), 1, found)
        self.assertIn("pack_owner_nickname", found[0])

    def test_a_new_placeholder_in_a_file_name_fails(self):
        write(self.repo / "foothold/template/Context/{{pack_team}}.md", "x\n")
        self.assertTrue(any("pack_team" in f for f in self.failures()))

    def test_a_setup_placeholder_missing_from_the_record_fails(self):
        text = SETUP_WITH_LISTS.replace("  install_date: <value>\n", "")
        write(self.repo / "foothold/skills/foothold-setup/SKILL.md", text)
        self.assertTrue(any("install_date" in f for f in self.failures()))

    def test_another_skills_placeholder_that_is_a_record_key_fails(self):
        text = SETUP_WITH_LISTS.replace("  install_date: <value>\n",
                                        "  install_date: <value>\n  title: <value>\n")
        write(self.repo / "foothold/skills/foothold-setup/SKILL.md", text)
        self.assertTrue(any("title" in f for f in self.failures()))

    def test_a_page_setup_builds_must_be_protected(self):
        text = SETUP_WITH_LISTS + "| `Context/Brand.md` | Q3 |\n"
        write(self.repo / "foothold/skills/foothold-setup/SKILL.md", text)
        found = self.failures()
        self.assertTrue(any("Context/Brand.md" in f and "protected" in f for f in found), found)

    def test_missing_lists_fail(self):
        write(self.repo / "foothold/skills/foothold-setup/SKILL.md", "# Setup\n")
        self.assertTrue(self.failures())

    def test_the_real_pack_passes(self):
        self.assertEqual(run_rule(check.check_setup_placeholders, ROOT, check.all_files()), [])


if __name__ == "__main__":
    unittest.main()
