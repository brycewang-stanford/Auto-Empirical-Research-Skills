"""Tests for the progressive-disclosure splitter (scripts/split-skill.py)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _helpers import load_module

split = load_module("scripts/split-skill.py", "aers_split")

SKILL = """---
name: demo
description: a demo skill
---

## Intro

Short intro section.

## Big Section

""" + "\n".join(f"line {i}" for i in range(120)) + """

## Tiny

one line
"""


class TestParsing(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(split.slugify("Step 4 — Main Results!"), "step-4-main-results")

    def test_frontmatter_preserved(self):
        front, body = split.split_frontmatter(SKILL)
        self.assertIn("name: demo", front)
        self.assertNotIn("name: demo", body)

    def test_sections_split_at_h2(self):
        _, body = split.split_frontmatter(SKILL)
        secs = dict((t, c) for t, c in split.sections(body))
        self.assertIn("Big Section", secs)
        self.assertIn("Tiny", secs)


class TestPlanAndApply(unittest.TestCase):
    def _write_skill(self, d: Path) -> Path:
        p = d / "SKILL.md"
        p.write_text(SKILL, encoding="utf-8")
        return p

    def test_big_section_is_moved(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write_skill(Path(d))
            plan = split.plan(p, threshold=80)
            actions = {r["title"]: r["action"] for r in plan["rows"]}
            self.assertEqual(actions["Big Section"], "move")
            self.assertEqual(actions["Tiny"], "keep")
            self.assertLess(plan["projected_spine"], plan["total"])

    def test_apply_preserves_content_and_source(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write_skill(Path(d))
            before = p.read_text(encoding="utf-8")
            out = Path(d) / "out"
            split.apply_split(split.plan(p, 80), out)
            # Source untouched.
            self.assertEqual(p.read_text(encoding="utf-8"), before)
            # Spine keeps frontmatter + a link to the moved section.
            spine = (out / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("name: demo", spine)
            self.assertIn("references/", spine)
            # The moved section's body lives in a reference file.
            ref_text = "\n".join((f).read_text(encoding="utf-8")
                                 for f in (out / "references").glob("*.md"))
            self.assertIn("line 119", ref_text)


if __name__ == "__main__":
    unittest.main()
