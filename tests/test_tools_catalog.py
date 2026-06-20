"""Tests for the tools catalog: schema validity + generated-view freshness."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest

from _helpers import ROOT, load_module

build_tools = load_module("scripts/build-tools-catalog.py", "aers_build_tools_catalog")

TOOLS_JSON = ROOT / "tools" / "tools.json"


def _load_tools() -> list[dict]:
    return json.loads(TOOLS_JSON.read_text(encoding="utf-8"))["tools"]


class TestToolsJsonSchema(unittest.TestCase):
    def setUp(self):
        self.tools = _load_tools()

    def test_nonempty(self):
        self.assertGreater(len(self.tools), 0)

    def test_validate_clean(self):
        self.assertEqual(build_tools.validate(self.tools), [])

    def test_categories_in_enum(self):
        for t in self.tools:
            with self.subTest(tool=t.get("id")):
                self.assertIn(t["category"], build_tools.CATEGORIES)

    def test_ids_and_urls_unique(self):
        ids = [t["id"] for t in self.tools]
        urls = [(t["url"] or "").rstrip("/").lower() for t in self.tools]
        self.assertEqual(len(ids), len(set(ids)), "duplicate ids")
        self.assertEqual(len(urls), len(set(urls)), "duplicate urls")

    def test_sorted_by_category_then_name(self):
        expected = sorted(self.tools, key=lambda x: (x["category"], x["name"].lower()))
        self.assertEqual(
            [t["id"] for t in self.tools],
            [t["id"] for t in expected],
            "tools.json must be sorted by (category, name); run the builder",
        )

    def test_mcp_entries_have_data_source_key(self):
        for t in self.tools:
            if t["category"] == "mcp-server":
                with self.subTest(tool=t["id"]):
                    self.assertIn("data_source", t)

    def test_bad_record_is_rejected(self):
        bad = dict(self.tools[0])
        bad["category"] = "not-a-real-category"
        errors = build_tools.validate([bad])
        self.assertTrue(any("unknown category" in e for e in errors))


class TestGeneratedViewsFresh(unittest.TestCase):
    def test_check_mode_passes(self):
        r = subprocess.run(
            [sys.executable, "scripts/build-tools-catalog.py", "--check"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_catalog_and_readme_summary_render_deterministically(self):
        tools = _load_tools()
        summary = build_tools.summary_tables(tools)
        catalog = build_tools.render_catalog(tools)
        self.assertIn(summary, catalog)
        readme = (ROOT / "tools" / "README.md").read_text(encoding="utf-8")
        self.assertIn(build_tools.SUMMARY_BEGIN, readme)
        self.assertIn(build_tools.SUMMARY_END, readme)


if __name__ == "__main__":
    unittest.main()
