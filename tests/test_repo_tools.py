"""Tests for repo tooling: frontmatter parsing + generated-artifact freshness."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest

from _helpers import ROOT, load_module

build_catalog = load_module("scripts/build-catalog.py", "aers_build_catalog")
validate_repo = load_module("scripts/validate-repo.py", "aers_validate_repo")


class TestFrontmatterParser(unittest.TestCase):
    def test_scalar_fields(self):
        text = "---\nname: my-skill\ndescription: does a thing\n---\nbody\n"
        fm = build_catalog.parse_frontmatter(text)
        self.assertEqual(fm.get("name"), "my-skill")
        self.assertEqual(fm.get("description"), "does a thing")

    def test_no_frontmatter_returns_empty(self):
        self.assertEqual(build_catalog.parse_frontmatter("# just a heading\n"), {})

    def test_frontmatter_after_html_comment_banner(self):
        # Regression: vendored snapshots prepend a CoPaper.AI banner before the
        # YAML frontmatter; the parser must skip it (was 32 false "missing").
        text = (
            "<!--\n  vendored provenance banner\n  source: github.com/x/y\n-->\n\n"
            "---\nname: hypothesis-generation\ndescription: does X\n---\n\n# Title\n"
        )
        fm = build_catalog.parse_frontmatter(text)
        self.assertEqual(fm.get("name"), "hypothesis-generation")
        self.assertEqual(fm.get("description"), "does X")

    def test_comment_then_no_frontmatter_is_empty(self):
        text = "<!-- banner -->\n\n# Just a heading\nbody\n"
        self.assertEqual(build_catalog.parse_frontmatter(text), {})

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


class TestCatalogSnapshotConsistency(unittest.TestCase):
    def test_current_catalog_summary_matches_skills_tree(self):
        errors, warnings = validate_repo.validate_catalog_snapshot()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_catalog_snapshot_mismatch_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = validate_repo.Path(tmp) / "skills.json"
            path.write_text(
                '{"summary":{"skill_files":0,"top_level_collections":0},'
                '"skills":[],"collections":[]}\n',
                encoding="utf-8",
            )
            errors, _ = validate_repo.validate_catalog_snapshot(path)
        self.assertTrue(any("skill_files" in error for error in errors))
        self.assertTrue(any("top_level_collections" in error for error in errors))


class TestMarkdownLinkValidation(unittest.TestCase):
    def test_fenced_code_detection(self):
        text = "before [ok](README.md)\n```markdown\n[example](missing.md)\n```\nafter\n"
        self.assertFalse(validate_repo.is_in_fenced_code(text, text.index("[ok]")))
        self.assertTrue(validate_repo.is_in_fenced_code(text, text.index("[example]")))

    def test_code_fence_links_are_ignored_for_expansion_doc(self):
        errors, _ = validate_repo.validate_markdown_links()
        self.assertFalse(
            [
                error
                for error in errors
                if "EMPIRICAL_SKILLS_EXPANSION_2026-06.md" in error
            ]
        )


class TestLocalAndCiGates(unittest.TestCase):
    def test_quality_workflow_uses_non_writing_gates(self):
        text = (ROOT / ".github" / "workflows" / "quality-evals.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python3 benchmark/check_benchmark.py --lint", text)
        self.assertIn("python3 benchmark/reference_pipeline.py --check", text)
        self.assertNotIn("python3 benchmark/reference_pipeline.py\n", text)
        self.assertIn("--no-write", text)

    def test_pre_commit_uses_non_writing_benchmark_gate(self):
        text = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        self.assertIn("python3 benchmark/check_benchmark.py --lint", text)
        self.assertIn("python3 benchmark/reference_pipeline.py --check", text)
        self.assertNotIn("python3 benchmark/reference_pipeline.py >/dev/null", text)
        self.assertIn("aers-tracked-file-hygiene", text)
        self.assertIn("python3 scripts/check-repo-hygiene.py", text)

    def test_maintainer_docs_point_to_full_local_gate(self):
        docs = [
            ".github/pull_request_template.md",
            "CONTRIBUTING.md",
            "docs/SKILL_SUBMISSION_GUIDE.md",
            "README-zh.md",
        ]
        for rel_path in docs:
            with self.subTest(path=rel_path):
                text = (ROOT / rel_path).read_text(encoding="utf-8")
                self.assertIn("make check", text)
        trust = (ROOT / "docs" / "TRUST.md").read_text(encoding="utf-8")
        self.assertIn("--fail-on-orphans --fail-on-partial --no-write", trust)


if __name__ == "__main__":
    unittest.main()
