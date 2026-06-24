"""Tests for repo tooling: frontmatter parsing + generated-artifact freshness."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest

from _helpers import ROOT, load_module

build_catalog = load_module("scripts/build-catalog.py", "aers_build_catalog")
validate_repo = load_module("scripts/validate-repo.py", "aers_validate_repo")
build_provenance = load_module("scripts/build-provenance.py", "aers_build_provenance")


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


class TestProvenanceNeverFabricatesSource(unittest.TestCase):
    """Regression: provenance must never invent a source URL from the folder
    name. A descriptive folder ("game-theory-paper-writer") once produced the
    bogus 404 "github.com/game/theory-paper-writer", which failed the weekly
    external-links CI."""

    def test_descriptive_folder_name_yields_unknown(self):
        url, confidence = build_provenance.infer_source_url(
            "65-game-theory-paper-writer", ""
        )
        self.assertIsNone(url)
        self.assertEqual(confidence, "unknown")

    def test_owner_repo_shaped_folder_name_yields_unknown(self):
        # Even a folder that *looks* like "owner-repo" must not be fabricated
        # into a URL without an in-text source line or an explicit override.
        url, confidence = build_provenance.infer_source_url("99-foo-bar", "")
        self.assertIsNone(url)
        self.assertEqual(confidence, "unknown")

    def test_in_text_source_line_is_still_honored(self):
        url, confidence = build_provenance.infer_source_url(
            "12-whatever", "Source: https://github.com/real-owner/real-repo\n"
        )
        self.assertEqual(url, "https://github.com/real-owner/real-repo")
        self.assertEqual(confidence, "high")

    def test_low_confidence_urls_are_pinned_in_overrides(self):
        # Any committed "low"-confidence source_url must trace to an explicit
        # OVERRIDES entry, never to a silent heuristic guess.
        import json

        data = json.loads(
            (ROOT / "catalog" / "provenance.json").read_text(encoding="utf-8")
        )
        for record in data["collections"]:
            if record.get("source_confidence") == "low" and record.get("source_url"):
                with self.subTest(collection=record["id"]):
                    self.assertIn(record["id"], build_provenance.OVERRIDES)


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

    def test_github_heading_slug_examples(self):
        cases = {
            "🆕 Changelog": "-changelog",
            "🚨 Anti-AIGC Detection & De-AI Academic Writing (Highlighted)": (
                "-anti-aigc-detection--de-ai-academic-writing-highlighted"
            ),
            "🚨 降 AIGC 检测率 & 学术去 AI 味（重点推荐）": (
                "-降-aigc-检测率--学术去-ai-味重点推荐"
            ),
            "Skill 聚合平台与发现工具": "skill-聚合平台与发现工具",
        }
        for heading, slug in cases.items():
            with self.subTest(heading=heading):
                self.assertEqual(validate_repo.github_heading_slug(heading), slug)

    def test_markdown_anchors_include_duplicate_suffixes(self):
        anchors = validate_repo.markdown_anchors("# Methods\n## Methods\n")
        self.assertIn("methods", anchors)
        self.assertIn("methods-1", anchors)

    def test_code_fence_links_are_ignored_for_expansion_doc(self):
        errors, _ = validate_repo.validate_markdown_links()
        self.assertFalse(
            [
                error
                for error in errors
                if "EMPIRICAL_SKILLS_EXPANSION_2026-06.md" in error
            ]
        )

    def test_missing_markdown_anchor_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = validate_repo.Path(tmp)
            readme = root / "README.md"
            readme.write_text(
                "# Existing Heading\n"
                "[ok](#existing-heading)\n"
                "[bad](#missing-heading)\n"
                "```markdown\n"
                "[ignored](#also-missing)\n"
                "```\n",
                encoding="utf-8",
            )

            old_root = validate_repo.ROOT
            try:
                validate_repo.ROOT = root
                errors, warnings = validate_repo.validate_markdown_links()
            finally:
                validate_repo.ROOT = old_root

        self.assertEqual(warnings, [])
        self.assertTrue(any("missing-heading" in error for error in errors))
        self.assertFalse(any("also-missing" in error for error in errors))

    def test_cross_document_markdown_anchor_is_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = validate_repo.Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "CHOOSING.md").write_text(
                "[methods](TAXONOMY.md#methods)\n[bad](TAXONOMY.md#missing)\n",
                encoding="utf-8",
            )
            (docs / "TAXONOMY.md").write_text("# Taxonomy\n## Methods\n", encoding="utf-8")

            old_root = validate_repo.ROOT
            try:
                validate_repo.ROOT = root
                errors, warnings = validate_repo.validate_markdown_links()
            finally:
                validate_repo.ROOT = old_root

        self.assertEqual(warnings, [])
        self.assertTrue(any("TAXONOMY.md#missing" in error for error in errors))
        self.assertFalse(any("TAXONOMY.md#methods" in error for error in errors))


class TestLocalAndCiGates(unittest.TestCase):
    def test_quality_workflow_uses_non_writing_gates(self):
        text = (ROOT / ".github" / "workflows" / "quality-evals.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("make python-compat", text)
        self.assertIn("python3 benchmark/check_benchmark.py --lint", text)
        self.assertIn("python3 benchmark/reference_pipeline.py --check", text)
        self.assertNotIn("python3 benchmark/reference_pipeline.py\n", text)
        self.assertIn("--no-write", text)

    def test_pre_commit_uses_non_writing_benchmark_gate(self):
        text = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        self.assertIn("python3 benchmark/check_benchmark.py --lint", text)
        self.assertIn("python3 benchmark/reference_pipeline.py --check", text)
        self.assertNotIn("python3 benchmark/reference_pipeline.py >/dev/null", text)
        self.assertIn("aers-python-compat", text)
        self.assertIn("make python-compat", text)
        self.assertIn("aers-tracked-file-hygiene", text)
        self.assertIn("python3 scripts/check-repo-hygiene.py", text)

    def test_make_check_includes_python_compatibility_compile(self):
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("python-compat:", text)
        self.assertIn("python3 -m py_compile scripts/*.py", text)
        self.assertRegex(text, r"check:\s+validate\s+python-compat\s+test")

    def test_maintainer_docs_point_to_full_local_gate(self):
        docs = [
            ".github/pull_request_template.md",
            "CONTRIBUTING.md",
            "docs/SKILL_SUBMISSION_GUIDE.md",
            "README.md",
        ]
        for rel_path in docs:
            with self.subTest(path=rel_path):
                text = (ROOT / rel_path).read_text(encoding="utf-8")
                self.assertIn("make check", text)
        trust = (ROOT / "docs" / "TRUST.md").read_text(encoding="utf-8")
        self.assertIn("--fail-on-orphans --fail-on-partial --no-write", trust)

    def test_sync_workflows_run_full_gate_before_pr(self):
        # Regression: an upstream auto-sync once clobbered local invariants and
        # reached main because GITHUB_TOKEN-opened PRs do not trigger CI. Each
        # sync workflow must check out submodules, regenerate the catalog, run
        # the full `make check` gate, and fail the run (labelling the PR
        # needs-fix) when the synced tree breaks.
        for name in ("sync-statspai-skill.yml", "sync-aer-skills.yml"):
            with self.subTest(workflow=name):
                text = (ROOT / ".github" / "workflows" / name).read_text(
                    encoding="utf-8"
                )
                self.assertIn("submodules: recursive", text)
                self.assertIn("actions/setup-python@", text)
                self.assertIn("make catalog && make check", text)
                self.assertIn("needs-fix", text)
                self.assertIn("steps.gate.outputs.status != '0'", text)


if __name__ == "__main__":
    unittest.main()
