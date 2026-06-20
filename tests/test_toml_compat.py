"""Tests for the dependency-free TOML fallback used on Python < 3.11."""

from __future__ import annotations

import unittest

from _helpers import load_module

toml_compat = load_module("scripts/toml_compat.py", "aers_toml_compat_for_tests")


class TestTomlCompatFallback(unittest.TestCase):
    def test_parses_repo_subset(self):
        data = toml_compat._loads_fallback('''
id = "example"
weight = 3
tol = 0.05 # inline comment
required = true
context_data = []
prompt = """
line one
line two
"""

[[rubric]]
id = "r1"
patterns = [
  '(?i)\\bRD\\b',
  '12\\s?(percent|%)',
]

[[rubric]]
id = "r2"
check = "manual"
''')
        self.assertEqual(data["id"], "example")
        self.assertEqual(data["weight"], 3)
        self.assertAlmostEqual(data["tol"], 0.05)
        self.assertTrue(data["required"])
        self.assertEqual(data["context_data"], [])
        self.assertIn("line two", data["prompt"])
        self.assertEqual([r["id"] for r in data["rubric"]], ["r1", "r2"])
        self.assertEqual(data["rubric"][0]["patterns"], [r"(?i)\bRD\b", r"12\s?(percent|%)"])

    def test_rejects_unsupported_table_header(self):
        with self.assertRaises(toml_compat.TomlCompatError):
            toml_compat._loads_fallback("[nested]\nx = 1\n")


if __name__ == "__main__":
    unittest.main()
