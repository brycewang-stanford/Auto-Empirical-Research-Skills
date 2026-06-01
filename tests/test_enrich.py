"""Tests for the catalog enrichment layer (scripts/build-catalog-enrich.py)."""

from __future__ import annotations

import subprocess
import sys
import unittest

from _helpers import ROOT, load_module

enrich = load_module("scripts/build-catalog-enrich.py", "aers_enrich")


class TestDeriveDescription(unittest.TestCase):
    def test_prose_after_frontmatter(self):
        text = "---\nname: x\n---\n\n# Title\n\nThis skill does a useful thing for researchers.\n"
        self.assertTrue(enrich.derive_description(text).startswith("This skill does a useful thing"))

    def test_skips_banner_and_frontmatter(self):
        text = ("<!-- banner -->\n---\nname: x\n---\n\n"
                "## Overview\n\nA second sentence appears here. And more.\n")
        out = enrich.derive_description(text)
        self.assertEqual(out, "A second sentence appears here.")

    def test_heading_fallback_when_only_code(self):
        text = "# Academic Proofreader\n\n```\nyou are a proofreader\n```\n"
        self.assertEqual(enrich.derive_description(text), "Academic Proofreader")


class TestAssignTags(unittest.TestCase):
    def test_method_and_language_tags(self):
        hay = "stata difference-in-differences with staggered callaway and first-stage f".lower()
        tags = enrich.assign_tags(hay)
        self.assertIn("stata", tags.get("language", []))
        self.assertIn("did", tags.get("method", []))
        self.assertIn("staggered-did", tags.get("method", []))
        self.assertIn("iv", tags.get("method", []))

    def test_no_false_positive_on_empty(self):
        self.assertEqual(enrich.assign_tags("a plain sentence about nothing"), {})


class TestScore(unittest.TestCase):
    def test_full_score_when_clean(self):
        skill = {"has_frontmatter": True, "has_name": True, "line_count": 120}
        desc = "A sufficiently long and descriptive frontmatter description for a skill."
        score, flags = enrich.score_skill(skill, desc, "frontmatter", True)
        self.assertEqual(score, 100)
        self.assertEqual(flags, [])

    def test_penalties_accumulate(self):
        skill = {"has_frontmatter": False, "has_name": False, "line_count": 1900}
        score, flags = enrich.score_skill(skill, "", "none", False)
        self.assertLess(score, 50)
        self.assertIn("no-frontmatter", flags)
        self.assertIn("very-long-no-references", flags)

    def test_long_first_party_flagged(self):
        skill = {"has_frontmatter": True, "has_name": True, "line_count": 1900}
        score, flags = enrich.score_skill(skill, "desc " * 10, "frontmatter", False)
        self.assertIn("very-long-no-references", flags)


class TestBuildAndFreshness(unittest.TestCase):
    def test_build_is_deterministic(self):
        a, b = enrich.build(), enrich.build()
        self.assertEqual(a, b)

    def test_every_skill_has_effective_description(self):
        payload = enrich.build()
        missing = [s["path"] for s in payload["skills"] if not s["description_effective"]]
        self.assertEqual(missing, [], f"skills without effective description: {missing}")

    def test_outputs_are_current(self):
        r = subprocess.run([sys.executable, "scripts/build-catalog-enrich.py", "--check"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
