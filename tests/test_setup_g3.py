"""Tests for G3, into the content first (Pack Usability Fix Proposal, approved 28 November 2026).

Setup asks six things in one message, builds a working vault from those answers, records it and
lands the person on it; the long interview and the schedules are optional offers after that.
These are tests of the setup skill's text, because setup's behaviour is its instructions.
"""

import json
import re
import unittest

from support import ROOT

SETUP_SKILL = ROOT / "foothold/skills/foothold-setup/SKILL.md"
START_HERE = ROOT / "foothold/Start Here.md"
README = ROOT / "README.md"
FIRST_WEEK = ROOT / "foothold/template/Getting Started - Your First Week.md"
OWNER_STUB = ROOT / "foothold/template/Context/{{pack_owner}}.md"

OPENING = ("To set Foothold up I need six things. Where should your vault go? What is your name "
           "and your role? What is your organisation called? Its website and your work email are "
           "useful but can wait.")
READY = ("Your vault is ready at `<path>`. Start with Home, then your own page and your "
         "organisation's page.")
OFFER = ("The more Foothold knows about your business, the more useful it is. I can ask you about "
         "it now, which takes up to an hour, or you can say \"tell Foothold about my business\" "
         "whenever you like.")
SCHEDULES = ("Foothold can check for new releases, write a daily note and tidy up monthly. None "
             "is set up unless you ask. Would you like any of them now?")


def flat(text):
    return " ".join(text.split())


class Setup(unittest.TestCase):
    def setUp(self):
        self.text = SETUP_SKILL.read_text(encoding="utf-8")
        self.flat = flat(self.text)

    def at(self, needle):
        self.assertIn(needle, self.text)
        return self.text.index(needle)

    def section(self, start, end):
        return self.text[self.at(start):self.at(end)]


class OneMessageBeforeAnythingIsWritten(Setup):
    def test_the_opening_is_the_approved_wording_with_the_consent_folded_in(self):
        a1 = flat(self.section("### Step A.1", "### Step A.2"))
        self.assertIn(OPENING, a1)
        self.assertIn("Shall I set Foothold up at `<target path>`, or somewhere else?", a1)
        self.assertIn("`~/Obsidian/Foothold/`", a1)
        self.assertIn("one message", a1)

    def test_the_only_questions_before_the_copy_are_the_opening_message(self):
        before = self.section("### Step A.1", "### Step A.5")
        a2 = self.section("### Step A.2", "### Step A.3")
        normal = before.replace(a2, "")
        asked = [q for q in re.findall(r'"([^"]*\?[^"]*)"', normal)]
        allowed = OPENING + " Shall I set Foothold up at `<target path>`, or somewhere else?"
        for question in asked:
            with self.subTest(question=question[:40]):
                self.assertIn(flat(question), allowed)


class TheVaultIsReadyBeforeTheOffers(Setup):
    def test_build_record_land_then_the_interview_offer_then_the_schedules(self):
        order = [self.at("### Step A.7"), self.at("## First build"), self.at("## Write the record"),
                 self.at("## Your vault is ready"), self.at("## The interview, if they want it"),
                 self.at("## Phase B: Onboarding"), self.at("## Phase C")]
        self.assertEqual(order, sorted(order))

    def test_the_first_build_uses_the_six_answers_and_leaves_no_hint_or_dead_link(self):
        build = flat(self.section("## First build", "## Write the record"))
        self.assertIn("from the six answers", build)
        self.assertIn("says so in one line", build)
        self.assertIn("Write a link only to a page that exists", build)
        self.assertIn("`Knowledge/domains/brand`", build)

    def test_the_landing_and_the_offer_use_the_approved_words(self):
        self.assertIn(READY, self.flat)
        self.assertIn(OFFER, self.flat)

    def test_pages_the_interview_fills_are_the_persons(self):
        offer = flat(self.section("## The interview, if they want it", "## Phase B: Onboarding"))
        self.assertIn("are the person's own from then on", offer)
        self.assertIn("If they say not now", offer)


class SchedulesAreOneOptionalQuestion(Setup):
    def test_the_one_question_and_each_job_still_needs_its_own_yes(self):
        c = flat(self.section("## Phase C", "## Phase D"))
        self.assertIn(SCHEDULES, c)
        self.assertIn("each job still needs its own yes", c)
        self.assertIn("nothing is scheduled", c)
        for question in ("Want your daily note written for you each weekday morning?",
                         "Want the curator to sweep the vault monthly?",
                         "Want me to check in with you in a week"):
            self.assertIn(question, c)

    def test_the_record_holds_the_schedule_with_nothing_scheduled_by_default(self):
        record = flat(self.section("## Write the record", "## Your vault is ready"))
        self.assertIn("nothing scheduled", record)
        self.assertIn("written once, here", record)
        self.assertIn("only its `schedule:` section", flat(self.text))


class TheInterviewLater(Setup):
    def test_the_description_names_the_phrase(self):
        front = self.text.split("---", 2)[1]
        self.assertIn("tell Foothold about my business", front)

    def test_the_already_set_up_route_runs_the_interview_without_copying(self):
        a2 = flat(self.section("### Step A.2", "### Step A.3"))
        self.assertIn('"tell Foothold about my business"', a2)
        self.assertIn("without copying anything", a2)
        self.assertIn("checksum lists", a2)


class SmallContradictions(Setup):
    def test_one_frontmatter_rule(self):
        build = flat(self.section("## Phase B Build", "## Phase C"))
        self.assertNotIn("**Frontmatter `last_reviewed:`** = today's date.", build)
        self.assertIn("set `last_reviewed:` to today wherever the page has that key", build)
        stub = OWNER_STUB.read_text(encoding="utf-8")
        self.assertIn("name: {{pack_owner}}", stub)
        self.assertIn("role: {{pack_owner_role}}", stub)

    def test_the_description_says_what_python_is_for(self):
        front = self.text.split("---", 2)[1]
        self.assertNotIn("Does NOT require terminal access", front)
        self.assertIn("Python", front)


class ElsewhereInThePack(unittest.TestCase):
    def test_start_here_step_3(self):
        text = START_HERE.read_text(encoding="utf-8")
        self.assertIn("3. Answer six short questions. Your vault is ready in a few minutes; "
                      "telling it about your business can follow.", text)
        self.assertNotIn("Allow about an hour", text)

    def test_the_readme_no_longer_says_setup_takes_the_hour(self):
        text = README.read_text(encoding="utf-8")
        self.assertNotIn("Give it the hour it deserves", text)
        self.assertIn("tell Foothold about my business", text)

    def test_the_first_week_guide_nudges_back_to_the_interview(self):
        text = FIRST_WEEK.read_text(encoding="utf-8")
        self.assertIn('"tell Foothold about my business"', text)
        self.assertNotIn("Onboarding wrote these from your answers", text)


if __name__ == "__main__":
    unittest.main()
