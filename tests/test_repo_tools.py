"""Tests for repo tooling: frontmatter parsing + generated-artifact freshness."""

from __future__ import annotations

import subprocess
import sys
import unittest

from _helpers import ROOT, load_module

build_catalog = load_module("scripts/build-catalog.py", "aers_build_catalog")


class TestFrontmatterParser(unittest.TestCase):
    def test_scalar_fields(self):
        text = "---\nname: my-skill\ndescription: does a thing\n---\nbody\n"
        fm = build_catalog.parse_frontmatter(text)
        self.assertEqual(fm.get("name"), "my-skill")
        self.assertEqual(fm.get("description"), "does a thing")

    def test_no_frontmatter_returns_empty(self):
        self.assertEqual(build_catalog.parse_frontmatter("# just a heading\n"), {})

    def test_block_scalar_description(self):
        text = (
            "---\n"
            "name: x\n"
            "description: >\n"
            "  line one\n"
            "  line two\n"
            "---\n"
            "body\n"
        )
        fm = build_catalog.parse_frontmatter(text)
        self.assertEqual(fm.get("name"), "x")
        self.assertIn("line one", fm.get("description", ""))


class TestGeneratedArtifactsAreCurrent(unittest.TestCase):
    """Mirror of `make validate`: the committed catalog/provenance/audit must
    match what the builders regenerate, and the repo must validate clean."""

    def _run(self, *args) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, *args], cwd=ROOT,
                              capture_output=True, text=True)

    def test_validate_repo_clean(self):
        r = self._run("scripts/validate-repo.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_catalog_current(self):
        r = self._run("scripts/build-catalog.py", "--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_provenance_current(self):
        r = self._run("scripts/build-provenance.py", "--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_skill_audit_current(self):
        r = self._run("scripts/build-skill-audit.py", "--check")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
