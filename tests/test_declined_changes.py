"""Tests for a declined change counting as settled (maintainer's decision, 28 November 2026).

A "no" is recorded in its own list, declined_by_person; the same release does not ask again; a
later release that changes the file again asks about it singly, never from a list; a "no" never
writes the file; and the person can take what they declined. Standard library only, no network.
"""

import io
import json
import re
import tempfile
import unittest
from unittest import mock
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from urllib.parse import unquote

from support import UPDATE_SKILL, load_helper, write

changes = load_helper()


class _EveryItem:
    def __contains__(self, number):
        return True


def setUpModule():
    # Seventh audit, X3: record now refuses a show-and-ask-each item or a conflict whose last page
    # show never printed. These tests are about record's other checks, so every item counts as
    # shown here; tests/test_fix_round_8.py tests the rule itself.
    global _shown
    _shown = mock.patch.object(changes, "_shown_items", lambda temp: _EveryItem())
    _shown.start()


def tearDownModule():
    _shown.stop()

SMALL_SKILL = "## Protected files\n\n- `Home.md`\n\n## End\n"
SKILL_A, SKILL_B, PAGE = "Skills/a/SKILL.md", "Skills/b/SKILL.md", "CRM/Page.md"
OLD = {SKILL_A: "a v1\n", SKILL_B: "b v1\n", PAGE: "page v1\n"}


def sha256(text):
    return changes.sha256_bytes(text if isinstance(text, bytes) else text.encode("utf-8"))


def flat(text):
    return " ".join(text.split())


def apply_record(vault, out):
    """Write record's output into config.yml the way Step 8 says."""
    cfg = changes.read_vault_config(vault)
    block = None
    for line in out.splitlines():
        if line in ("release_hashes:", "vault_hashes:", "kept_by_person, add:",
                    "kept_by_person, remove:", "declined_by_person, add:",
                    "declined_by_person, remove:"):
            block = line
            continue
        if not line.startswith("  ") or block is None:
            continue
        if block in ("release_hashes:", "vault_hashes:"):
            key, digest = line.strip().rsplit(": ", 1)
            table = cfg.release_hashes if block == "release_hashes:" else cfg.vault_hashes
            table[json.loads(key)] = digest
        else:
            path = json.loads(line.strip()[2:])
            target = cfg.kept if block.startswith("kept") else cfg.declined
            if block.endswith("add:"):
                target.append(path)
            elif path in target:
                target.remove(path)
    for name in ("pack_owner_file", "pack_org_file"):
        cfg.values.pop(name, None)  # worked out on reading; never written by Step 8
    write(Path(vault) / ".foothold/config.yml", changes.render_config(cfg))


class Run(unittest.TestCase):
    """A vault on 2.5.0, as setup left it, and releases built from dicts."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.vault = self.tmp / "vault"
        for path, body in OLD.items():
            write(self.vault / path, body)
        cfg = changes.Config(values={"version": "2.5.0", "pack_owner": "Jane Smith"},
                             vault_hashes={p: sha256(b) for p, b in OLD.items()},
                             release_hashes={p: sha256(b) for p, b in OLD.items()})
        write(self.vault / ".foothold/config.yml", changes.render_config(cfg))
        self.skill = self.tmp / "SKILL.md"
        self.skill.write_text(SMALL_SKILL, encoding="utf-8")
        self.runs = 0

    def tearDown(self):
        self._tmp.cleanup()

    def release(self, version, files):
        self.files = dict(files)
        listed = self.tmp / f"release-files-{version}.txt"
        listed.write_text("".join(f"{sha256(b)}  foothold-{version}/template/{p}\n"
                                  for p, b in files.items()), encoding="utf-8")
        self.listed, self.version = listed, version
        return listed

    def download(self, url):
        name = "/".join(unquote(p) for p in url.split("/foothold/template/", 1)[1].split("/"))
        return self.files[name].encode("utf-8")

    def fetch(self, take_declined=False):
        self.runs += 1
        self.temp = self.tmp / f"dl{self.runs}"
        self.temp.mkdir()
        with redirect_stdout(io.StringIO()):
            items = changes.fetch(self.vault, self.listed, self.temp, self.skill,
                                  download=self.download, take_declined=take_declined)
        return {i["path"]: i for i in items}

    def sort(self, take_declined=False):
        return changes.sort_from_paths(self.vault, self.listed, self.skill,
                                       take_declined=take_declined)

    def record(self, written=(), **kwargs):
        return changes.record(self.vault, self.listed, self.temp, list(written),
                              skill_md=self.skill, **kwargs)

    def take(self, items, path):
        write(self.vault / path, self.files[path])
        return items[path]["number"]

    def first_run(self):
        """2.5.1 changes two skills and a page; take skill a and the page, decline skill b."""
        self.release("2.5.1", {SKILL_A: "a v2\n", SKILL_B: "b v2\n", PAGE: "page v2\n"})
        items = self.fetch()
        a, page = self.take(items, SKILL_A), self.take(items, PAGE)
        out = self.record([a, page], declined=[items[SKILL_B]["number"]])
        apply_record(self.vault, out)
        return items, out


class DeclinedIsRecorded(Run):
    def test_record_prints_the_decline_in_its_own_list(self):
        _, out = self.first_run()
        added = out[out.index("declined_by_person, add:"):out.index("declined_by_person, remove:")]
        self.assertIn(f'  - "{SKILL_B}"', added)
        rel = out[out.index("release_hashes:"):out.index("vault_hashes:")]
        self.assertIn(f'"{SKILL_B}": {sha256("b v2" + chr(10))}', rel)
        vlt = out[out.index("vault_hashes:"):out.index("kept_by_person, add:")]
        self.assertNotIn(SKILL_B, vlt)

    def test_the_same_release_does_not_ask_again_and_does_not_lose_it(self):
        self.first_run()
        result = self.sort()
        self.assertEqual(result[SKILL_B].category, changes.DECLINED)
        self.assertNotIn(changes.DECLINED, changes.TO_LOOK_AT)
        self.assertEqual(self.fetch(), {})

    def test_the_record_holds_the_list_and_reads_it_back(self):
        self.first_run()
        cfg = changes.read_vault_config(self.vault)
        self.assertEqual(cfg.declined, [SKILL_B])
        text = (self.vault / ".foothold/config.yml").read_text(encoding="utf-8")
        self.assertIn(f'declined_by_person:\n  - "{SKILL_B}"', text)

    def test_a_bad_path_in_the_list_refuses_the_record(self):
        text = changes.render_config(changes.Config(values={"version": "2.5.0"},
                                                    declined=["CRM/a' & echo x & '.md"]))
        with self.assertRaises(changes.ChangesError):
            changes.parse_config(text)


class ANoNeverWrites(Run):
    def setUp(self):
        super().setUp()
        self.release("2.5.1", {SKILL_A: "a v2\n", PAGE: "page v2\n", "Skills/new/SKILL.md": "n\n"})

    def test_declined_is_refused_when_the_vault_holds_the_releases_copy(self):
        items = self.fetch()
        n = self.take(items, SKILL_A)
        with self.assertRaises(changes.ChangesError) as caught:
            self.record(declined=[n])
        self.assertIn("release's copy", str(caught.exception))

    def test_declined_is_refused_when_the_vault_changed_since_fetch(self):
        items = self.fetch()
        write(self.vault / SKILL_A, "something else\n")
        with self.assertRaises(changes.ChangesError):
            self.record(declined=[items[SKILL_A]["number"]])

    def test_a_declined_new_file_must_still_be_absent(self):
        items = self.fetch()
        n = self.take(items, "Skills/new/SKILL.md")
        with self.assertRaises(changes.ChangesError):
            self.record(declined=[n])

    def test_applied_is_refused_when_the_file_was_not_written(self):
        items = self.fetch()
        with self.assertRaises(changes.ChangesError):
            self.record([items[SKILL_A]["number"]])

    def test_a_conflict_cannot_be_declined(self):
        write(self.vault / PAGE, "my own edits\n")
        items = self.fetch()
        self.assertEqual(items[PAGE]["group"], changes.CONFLICT)
        with self.assertRaises(changes.ChangesError):
            self.record(declined=[items[PAGE]["number"]])

    def test_a_number_given_twice_is_refused(self):
        items = self.fetch()
        n = items[SKILL_A]["number"]
        with self.assertRaises(changes.ChangesError):
            self.record([n], declined=[n])

    def test_a_new_declined_file_is_not_asked_again(self):
        items = self.fetch()
        apply_record(self.vault, self.record(declined=[items["Skills/new/SKILL.md"]["number"]]))
        self.assertEqual(self.sort()["Skills/new/SKILL.md"].category, changes.DECLINED)

    def test_too_long_to_show_cannot_be_declined(self):
        big = "x" * (changes.SHOW_CAP + 10)
        self.release("2.5.1", {SKILL_A: big})
        items = self.fetch()
        with self.assertRaises(changes.ChangesError):
            self.record(declined=[items[SKILL_A]["number"]])


class ALaterReleaseAsksSingly(Run):
    def test_a_declined_skill_changed_again_comes_back_shown_singly(self):
        self.first_run()
        self.release("2.5.2", {SKILL_A: "a v2\n", SKILL_B: "b v3\n", PAGE: "page v2\n"})
        self.assertEqual(self.sort()[SKILL_B].category, changes.ASK_EACH)

    def test_a_declined_page_changed_again_is_never_list_and_ask_once(self):
        self.release("2.5.1", {PAGE: "page v2\n"})
        items = self.fetch()
        self.assertEqual(items[PAGE]["group"], changes.ASK_ONCE)
        apply_record(self.vault, self.record(declined=[items[PAGE]["number"]]))
        self.release("2.5.2", {PAGE: "page v3\n"})
        self.assertEqual(self.sort()[PAGE].category, changes.ASK_EACH)
        items = self.fetch()
        self.assertEqual(items[PAGE]["group"], changes.ASK_EACH)
        n = self.take(items, PAGE)
        out = self.record([n])
        self.assertIn(f'  - "{PAGE}"', out[out.index("declined_by_person, remove:"):])

    def test_a_planted_list_and_ask_once_group_is_refused(self):
        self.release("2.5.1", {PAGE: "page v2\n"})
        items = self.fetch()
        apply_record(self.vault, self.record(declined=[items[PAGE]["number"]]))
        self.release("2.5.2", {PAGE: "page v3\n"})
        self.fetch()
        index = json.loads((self.temp / changes.MANIFEST).read_text(encoding="utf-8"))
        index["items"][0]["group"] = changes.ASK_ONCE
        (self.temp / changes.MANIFEST).write_text(json.dumps(index), encoding="utf-8")
        write(self.vault / PAGE, "page v3\n")
        with self.assertRaises(changes.ChangesError):
            self.record([1])

    def test_a_declined_file_the_person_then_edited_is_a_conflict(self):
        self.first_run()
        write(self.vault / SKILL_B, "b v1, my edit\n")
        self.release("2.5.2", {SKILL_B: "b v3\n"})
        self.assertEqual(self.sort()[SKILL_B].category, changes.CONFLICT)


class TakeWhatIDeclined(Run):
    def test_the_take_route_sorts_them_back_into_their_groups(self):
        self.first_run()
        self.assertEqual(self.sort(take_declined=True)[SKILL_B].category, changes.ASK_EACH)
        items = self.fetch(take_declined=True)
        self.assertEqual(list(items), [SKILL_B])
        page = changes.show(self.vault, self.listed, self.temp, items[SKILL_B]["number"],
                            self.skill)
        self.assertIn("| + b v2", page)
        n = self.take(items, SKILL_B)
        out = self.record([n])
        apply_record(self.vault, out)
        self.assertIn(f'  - "{SKILL_B}"', out[out.index("declined_by_person, remove:"):])
        self.assertEqual(changes.read_vault_config(self.vault).declined, [])
        self.assertEqual(self.sort()[SKILL_B].category, changes.UNCHANGED)

    def test_on_the_command_line(self):
        self.first_run()
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = changes.main(["sort", str(self.vault), str(self.listed), "--skill",
                                 str(self.skill), "--take-declined"])
        self.assertEqual(code, 0, err.getvalue())
        self.assertIn(SKILL_B, out.getvalue().split("show and ask each")[1].split("list")[0])

    def test_record_on_the_command_line_takes_declined(self):
        self.release("2.5.1", {SKILL_A: "a v2\n"})
        self.fetch()
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = changes.main(["record", str(self.vault), str(self.listed), str(self.temp),
                                 "--declined", "1", "--skill", str(self.skill)])
        self.assertEqual(code, 0, err.getvalue())
        self.assertIn("declined_by_person, add:", out.getvalue())


class SkillWording(unittest.TestCase):
    def setUp(self):
        self.text = UPDATE_SKILL.read_text(encoding="utf-8")
        self.flat = flat(self.text)

    def test_the_exact_wording(self):
        for line in ('"Yes, take it"', '"No, keep what I have"',
                     "Left as it is. I will not ask about this file again until a later release "
                     "changes it.",
                     'You said no to `<n>` change(s): `<paths>`. To take them later, say '
                     '"update Foothold and take the changes I declined".'):
            with self.subTest(line=line[:30]):
                self.assertIn(line, self.flat)

    def test_the_version_moves_when_everything_is_settled(self):
        step8 = flat(self.text[self.text.index("## Step 8"):self.text.index("## Step 9")])
        self.assertIn("applied, kept, merged or declined", step8)
        self.assertNotIn("If the person said no to some, leave `foothold.version` as it was",
                         step8)

    def test_record_takes_declined_and_the_route_to_take_them(self):
        self.assertIn("--declined <number>", self.text)
        self.assertIn("--take-declined", self.text)
        self.assertIn("update Foothold and take the changes I declined", self.flat)

    def test_without_the_helper_says_a_no_is_asked_again(self):
        without = flat(self.text[self.text.index("## Without the helper"):
                                 self.text.index("## Scheduled or unattended runs")])
        self.assertIn("a change the person says no to is asked about again next time", without)

    def test_the_scheduled_count_leaves_declined_out(self):
        sched = flat(self.text[self.text.index("## Scheduled or unattended runs"):
                               self.text.index("## Step 1")])
        self.assertIn("Declined files are not counted", sched)


if __name__ == "__main__":
    unittest.main()
