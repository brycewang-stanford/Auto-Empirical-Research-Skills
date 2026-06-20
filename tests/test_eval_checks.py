"""Unit tests for the eval check primitives (eval-harness/lib/checks.py)."""

from __future__ import annotations

import unittest

from _helpers import load_module

checks = load_module("eval-harness/lib/checks.py", "aers_checks")


def run(item, text):
    return checks.run_check(item, text)


class TestRegexChecks(unittest.TestCase):
    def test_regex_any_pass_and_fail(self):
        item = {"id": "x", "check": "regex_any", "patterns": ["foo", "bar"], "description": "d"}
        self.assertEqual(run(item, "has a bar in it").status, "pass")
        self.assertEqual(run(item, "nothing here").status, "fail")

    def test_regex_all(self):
        item = {"id": "x", "check": "regex_all", "patterns": ["foo", "bar"], "description": "d"}
        self.assertEqual(run(item, "foo and bar").status, "pass")
        self.assertEqual(run(item, "only foo").status, "fail")

    def test_regex_none_forbidden(self):
        item = {"id": "x", "check": "regex_none", "patterns": ["TWFE is fine"], "description": "d"}
        self.assertEqual(run(item, "we avoid TWFE").status, "pass")
        self.assertEqual(run(item, "TWFE is fine here").status, "fail")

    def test_single_pattern_field(self):
        item = {"id": "x", "check": "regex_any", "pattern": "callaway", "description": "d"}
        self.assertEqual(run(item, "use Callaway-Santanna").status, "pass")

    def test_bad_regex_is_error(self):
        item = {"id": "x", "check": "regex_any", "pattern": "(", "description": "d"}
        self.assertEqual(run(item, "x").status, "error")


class TestCountChecks(unittest.TestCase):
    def test_regex_count_max(self):
        item = {"id": "x", "check": "regex_count_max", "pattern": "因此", "target": 1, "description": "d"}
        self.assertEqual(run(item, "因此 a 因此 b").status, "fail")  # 2 > 1
        self.assertEqual(run(item, "因此 only once").status, "pass")

    def test_regex_count_per_chars(self):
        # target 1 per 5 chars; text len 10 -> allowed 2
        item = {"id": "x", "check": "regex_count_max", "pattern": "a",
                "target": 1, "per_chars": 5, "description": "d"}
        self.assertEqual(run(item, "aaXXXXXXXX").status, "pass")   # 2 a's, allowed 2
        self.assertEqual(run(item, "aaaXXXXXXX").status, "fail")   # 3 a's, allowed 2


class TestWordCount(unittest.TestCase):
    def test_word_count_max(self):
        item = {"id": "x", "check": "word_count_max", "target": 3, "description": "d"}
        self.assertEqual(run(item, "one two three").status, "pass")
        self.assertEqual(run(item, "one two three four").status, "fail")

    def test_cjk_counted_as_words(self):
        item = {"id": "x", "check": "word_count_max", "target": 2, "description": "d"}
        # 3 CJK chars -> 3 words > 2
        self.assertEqual(run(item, "数字经济").status, "fail")

    def test_section_scoping(self):
        item = {"id": "x", "check": "word_count_max", "target": 2,
                "section": r"(?is)abstract[:\s]*(.+)", "description": "d"}
        # Only the abstract section ("a b") is counted, not the heading.
        self.assertEqual(run(item, "Title here\nAbstract: a b").status, "pass")


class TestNumericChecks(unittest.TestCase):
    def test_numeric_tolerance(self):
        item = {"id": "x", "check": "numeric_tolerance", "extract": r"ATT\s*=\s*(-?[0-9.]+)",
                "expected": 1794, "tol": 300, "description": "d"}
        self.assertEqual(run(item, "ATT = 1548").status, "pass")
        self.assertEqual(run(item, "ATT = 100").status, "fail")
        self.assertEqual(run(item, "no number").status, "fail")

    def test_numeric_sign(self):
        item = {"id": "x", "check": "numeric_sign", "extract": r"naive\s*=\s*(-?[0-9.]+)",
                "sign": "negative", "description": "d"}
        self.assertEqual(run(item, "naive = -635").status, "pass")
        self.assertEqual(run(item, "naive = 200").status, "fail")


class TestManualAndUnknown(unittest.TestCase):
    def test_manual_is_manual(self):
        item = {"id": "x", "check": "manual", "description": "d", "guidance": "judge it"}
        self.assertEqual(run(item, "anything").status, "manual")

    def test_unknown_check_errors(self):
        item = {"id": "x", "check": "nope", "description": "d"}
        self.assertEqual(run(item, "anything").status, "error")


if __name__ == "__main__":
    unittest.main()
