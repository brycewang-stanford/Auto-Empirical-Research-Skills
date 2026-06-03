"""Tests for tracked-file hygiene checks."""

from __future__ import annotations

import contextlib
import io
import unittest

from _helpers import load_module

hygiene = load_module("scripts/check-repo-hygiene.py", "aers_check_repo_hygiene")


class TestRepoHygiene(unittest.TestCase):
    def test_forbidden_artifact_patterns(self):
        bad = [
            ".DS_Store",
            "docs/.DS_Store",
            "Thumbs.db",
            "scripts/__pycache__/x.cpython-313.pyc",
            "tests/test.pyc",
            ".pytest_cache/v/cache/nodeids",
            "pkg/.ruff_cache/content",
        ]
        for path in bad:
            with self.subTest(path=path):
                self.assertTrue(hygiene.is_forbidden_artifact(path))

    def test_allowed_paths(self):
        allowed = [
            "README.md",
            "demo-notebooks/Stata_skill_lalonde_full_pipeline.log",
            "benchmark/results/lalonde-recovery.json",
            "skills/50-brycewang-aer-skills/skills/aer-workflow/SKILL.md",
        ]
        for path in allowed:
            with self.subTest(path=path):
                self.assertFalse(hygiene.is_forbidden_artifact(path))

    def test_scan_current_tracked_files(self):
        self.assertEqual(hygiene.forbidden_tracked_files(hygiene.tracked_files()), [])

    def test_cli_passes_on_current_repo(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(hygiene.main([]), 0)

    def test_makefile_exposes_local_cache_cleanup(self):
        makefile = (hygiene.ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("hygiene:", makefile)
        self.assertIn("clean:", makefile)
        for token in (".DS_Store", "__pycache__", "*.pyc", "*.pyo"):
            with self.subTest(token=token):
                self.assertIn(token, makefile)


if __name__ == "__main__":
    unittest.main()
