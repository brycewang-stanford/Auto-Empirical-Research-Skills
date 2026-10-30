"""Tests for the README rigor-stats consistency checker."""

from __future__ import annotations

import unittest

from _helpers import ROOT, load_module

check_readme_stats = load_module("scripts/check-readme-stats.py", "aers_check_readme_stats")


class TestExpectedCounts(unittest.TestCase):
    def test_counts_match_committed_toml_files(self):
        n_tasks, n_scenarios, n_rubric, n_fixtures = check_readme_stats.expected_counts()
        self.assertEqual(n_tasks, len(list((ROOT / "benchmark" / "tasks").glob("*.toml"))))
        self.assertEqual(n_scenarios, len(list((ROOT / "eval-harness" / "scenarios").glob("*.toml"))))
        self.assertGreater(n_rubric, n_scenarios)  # every scenario has >= 1 rubric item
        # Fixtures are a subset of scenarios, counted only when the pair is complete.
        self.assertLessEqual(n_fixtures, n_scenarios)
        self.assertGreater(n_fixtures, 0)


class TestCheckReadme(unittest.TestCase):
    def setUp(self):
        self.counts = check_readme_stats.expected_counts()

    def test_committed_readmes_are_consistent(self):
        for name in check_readme_stats.READMES:
            with self.subTest(readme=name):
                problems = check_readme_stats.check_readme(ROOT / name, *self.counts)
                self.assertEqual(problems, [])

    def test_stale_bolded_count_is_caught(self):
        import tempfile
        from pathlib import Path

        n_tasks, n_scenarios, n_rubric, n_fixtures = self.counts
        stale = (
            f"| Numeric benchmark tasks | **{n_tasks + 1}** | [`benchmark/`](benchmark/) |\n"
            f"| Eval scenarios | **{n_scenarios} / {n_rubric}** | [`eval-harness/`](eval-harness/) |\n"
            f"| Proven to discriminate | **{n_fixtures}** | "
            f"[`fixtures`](eval-harness/fixtures/) |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(stale, encoding="utf-8")
            problems = check_readme_stats.check_readme(path, *self.counts)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("benchmark row says", problems[0])

    def test_stale_suffix_style_count_is_caught(self):
        import tempfile
        from pathlib import Path

        n_tasks, n_scenarios, n_rubric, n_fixtures = self.counts
        stale = (
            f"| **数值基准** | 陷阱 | [`benchmark/`](benchmark/) · {n_tasks} 任务 |\n"
            f"| **评测套件** | 失误 | [`eval-harness/`](eval-harness/) · {n_scenarios - 1} 场景 / {n_rubric} rubric |\n"
            f"| **可区分场景** | | [`fixtures`](eval-harness/fixtures/) **{n_fixtures}** |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(stale, encoding="utf-8")
            problems = check_readme_stats.check_readme(path, *self.counts)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("eval-harness row says", problems[0])

    def test_missing_rows_are_caught(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text("# empty\n", encoding="utf-8")
            problems = check_readme_stats.check_readme(path, *self.counts)
        # benchmark, eval-harness, and fixtures rows all missing.
        self.assertEqual(len(problems), 3, problems)


if __name__ == "__main__":
    unittest.main()

class TestCollectionCoverage(unittest.TestCase):
    def setUp(self):
        self.catalog_ids, self.total = check_readme_stats.catalog_facts()

    def test_catalog_facts_shape(self):
        self.assertGreaterEqual(len(self.catalog_ids), 70)
        self.assertGreater(self.total, 500)

    def test_committed_collection_tables_are_complete(self):
        for name in check_readme_stats.COLLECTION_TABLE_DOCS:
            with self.subTest(doc=name):
                problems = check_readme_stats.check_collections(
                    ROOT / name, self.catalog_ids, self.total
                )
                self.assertEqual(problems, [])

    def test_missing_collection_is_caught(self):
        import tempfile
        from pathlib import Path

        some_id = sorted(self.catalog_ids)[0]
        rows = "\n".join(
            f"| [{cid}](skills/{cid}/) |" for cid in sorted(self.catalog_ids) if cid != some_id
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(rows, encoding="utf-8")
            problems = check_readme_stats.check_collections(path, self.catalog_ids, self.total)
        self.assertTrue(any("missing 1 cataloged collection" in p for p in problems))

    def test_unknown_collection_link_is_caught(self):
        import tempfile
        from pathlib import Path

        rows = "\n".join(
            f"| [{cid}](skills/{cid}/) |" for cid in sorted(self.catalog_ids)
        ) + "\n| [gone](skills/99-deleted-collection/) |"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(rows, encoding="utf-8")
            problems = check_readme_stats.check_collections(path, self.catalog_ids, self.total)
        self.assertTrue(any("not in catalog" in p for p in problems))

    def test_widest_table_is_the_all_collections_table(self):
        # Every entry document carries the all-collections table plus smaller
        # by-theme groupings; the source column only exists on the widest one.
        for name in check_readme_stats.COLLECTION_TABLE_DOCS:
            with self.subTest(doc=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                rows = check_readme_stats.widest_collection_table(text)
                ids = {
                    m for row in rows for m in check_readme_stats.COLLECTION_LINK_RE.findall(row)
                }
                self.assertEqual(ids, self.catalog_ids)

    def test_stale_catalog_cited_total_is_caught(self):
        import tempfile
        from pathlib import Path

        rows = "\n".join(
            f"| [{cid}](skills/{cid}/) |" for cid in sorted(self.catalog_ids)
        ) + f"\n| skills | **{self.total + 1:,}** | [`catalog/skills.json`](catalog/skills.json) |"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(rows, encoding="utf-8")
            problems = check_readme_stats.check_collections(path, self.catalog_ids, self.total)
        self.assertTrue(any("stale" in p or "catalog total" in p for p in problems))


class TestSourceLinks(unittest.TestCase):
    """The 来源/Source column must stay pinned to catalog/provenance.json."""

    def setUp(self):
        self.sources = check_readme_stats.provenance_sources()

    def test_every_cataloged_collection_has_a_source_url(self):
        catalog_ids, _ = check_readme_stats.catalog_facts()
        self.assertEqual(catalog_ids - set(self.sources), set())

    def test_committed_tables_link_their_upstream(self):
        for name in check_readme_stats.COLLECTION_TABLE_DOCS:
            with self.subTest(doc=name):
                problems = check_readme_stats.check_source_links(ROOT / name, self.sources)
                self.assertEqual(problems, [])

    def test_wrong_source_url_is_caught(self):
        import tempfile
        from pathlib import Path

        cid = sorted(self.sources)[0]
        rows = "\n".join(
            f"| [{c}](skills/{c}/) | [x]({self.sources[c]}) |" if c != cid
            else f"| [{c}](skills/{c}/) | [x](https://github.com/wrong/repo) |"
            for c in sorted(self.sources)
        )
        table = "| a | b |\n|---|---|\n" + rows + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(table, encoding="utf-8")
            problems = check_readme_stats.check_source_links(path, self.sources)
        self.assertEqual(len(problems), 1)
        self.assertIn(cid, problems[0])
        self.assertIn("does not link its upstream source", problems[0])

    def test_missing_source_column_is_caught(self):
        import tempfile
        from pathlib import Path

        rows = "\n".join(f"| [{c}](skills/{c}/) |" for c in sorted(self.sources))
        table = "| a |\n|---|\n" + rows + "\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(table, encoding="utf-8")
            problems = check_readme_stats.check_source_links(path, self.sources)
        self.assertEqual(len(problems), len(self.sources))

    def test_no_collection_table_is_caught(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text("# nothing here\n", encoding="utf-8")
            problems = check_readme_stats.check_source_links(path, self.sources)
        self.assertEqual(len(problems), 1)
        self.assertIn("no collection table found", problems[0])



class TestLandingPage(unittest.TestCase):
    """`index.html` is served on GitHub Pages and carries two static numbers.

    Its stat tiles fetch `catalog/skills.json` at runtime and cannot go stale.
    The meta description and the JS fallbacks are plain text and can — and both
    had, by 1,093-vs-1,096 skills and a "16 families" fallback that was two
    families out of date.
    """

    def setUp(self):
        self.total = check_readme_stats.catalog_facts()[1]

    def _check(self, body: str):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.html"
            path.write_text(body, encoding="utf-8")
            return check_readme_stats.check_landing_page(path, self.total)

    def test_committed_landing_page_is_clean(self):
        problems = check_readme_stats.check_landing_page(
            check_readme_stats.LANDING, self.total
        )
        self.assertEqual(problems, [])

    def test_a_stale_meta_description_is_caught(self):
        problems = self._check(
            f'<meta name="description" content="{self.total - 3:,} vendored skills">'
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("meta description says", problems[0])

    def test_a_correct_meta_description_passes(self):
        self.assertEqual(
            self._check(
                f'<meta name="description" content="{self.total:,} vendored skills">'
            ),
            [],
        )

    def test_a_numeric_rigor_fallback_is_caught(self):
        problems = self._check(
            '<meta name="description" content="no numbers here">\n'
            'catch { document.getElementById("n-rigor").textContent = "16 families"; }'
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("hardcodes", problems[0])

    def test_a_non_numeric_fallback_passes(self):
        self.assertEqual(
            self._check(
                '<meta name="description" content="no numbers here">\n'
                'catch { document.getElementById("n-rigor").textContent = "see RIGOR_COVERAGE"; }'
            ),
            [],
        )


class TestFixturesRow(unittest.TestCase):
    """The discrimination count is a copied number, so it is linted like the rest.

    It is also the number most worth linting: "9 scenarios proven to
    discriminate" is a stronger claim than "41 scenarios exist", and a stronger
    claim that drifts is worse than a weaker one that does not.
    """

    def setUp(self):
        self.counts = check_readme_stats.expected_counts()

    def test_a_stale_fixtures_count_is_caught(self):
        import tempfile
        from pathlib import Path

        n_tasks, n_scenarios, n_rubric, n_fixtures = self.counts
        stale = (
            f"| tasks | **{n_tasks}** | [`benchmark/`](benchmark/) |\n"
            f"| evals | **{n_scenarios} / {n_rubric}** | [`eval-harness/`](eval-harness/) |\n"
            f"| proven | **{n_fixtures + 5}** | [`f`](eval-harness/fixtures/) |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README-test.md"
            path.write_text(stale, encoding="utf-8")
            problems = check_readme_stats.check_readme(path, *self.counts)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("fixtures row says", problems[0])

    def test_the_fixtures_link_does_not_collide_with_the_eval_harness_link(self):
        # `eval-harness/fixtures/` must not be read as the `eval-harness/` row,
        # or the two counts would lint against each other.
        row = "| proven | **9** | [`f`](eval-harness/fixtures/) |"
        self.assertIsNone(check_readme_stats.EVAL_LINK_RE.search(row))
        self.assertIsNotNone(check_readme_stats.FIXTURE_LINK_RE.search(row))
