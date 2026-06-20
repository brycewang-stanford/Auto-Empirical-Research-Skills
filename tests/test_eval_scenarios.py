"""Tests for scenario loading/validation and the grader (eval-harness/run_evals.py)."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest

from _helpers import load_module

run_evals = load_module("eval-harness/run_evals.py", "aers_run_evals")


class TestRealScenarios(unittest.TestCase):
    def test_all_shipped_scenarios_are_valid(self):
        scenarios = run_evals.load_scenarios()
        self.assertGreaterEqual(len(scenarios), 1, "no scenarios found")
        problems = [p for s in scenarios for p in run_evals.validate_scenario(s)]
        self.assertEqual(problems, [], f"shipped scenarios invalid:\n" + "\n".join(problems))

    def test_every_scenario_skill_exists(self):
        for s in run_evals.load_scenarios():
            self.assertTrue((run_evals.ROOT / s["skill"]).exists(),
                            f"{s['id']} -> missing skill {s['skill']}")


class TestScenarioSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema_path = run_evals.ROOT / "eval-harness" / "schema" / "scenario.schema.json"
        cls.schema = json.loads(schema_path.read_text(encoding="utf-8"))

    def test_schema_documents_current_required_fields(self):
        self.assertEqual(
            self.schema["required"],
            list(run_evals.REQUIRED_SCENARIO_FIELDS),
        )

    def test_schema_enums_match_harness_constants(self):
        props = self.schema["properties"]
        rubric_props = self.schema["definitions"]["rubricItem"]["properties"]

        self.assertEqual(set(props["severity"]["enum"]), run_evals.SEVERITIES)
        self.assertEqual(set(rubric_props["check"]["enum"]), run_evals.ALL_CHECKS)
        self.assertEqual(set(rubric_props["unit"]["enum"]), run_evals.UNITS)
        self.assertEqual(set(rubric_props["sign"]["enum"]), run_evals.SIGNS)

    def test_schema_id_patterns_match_validator(self):
        props = self.schema["properties"]
        rubric_props = self.schema["definitions"]["rubricItem"]["properties"]

        self.assertEqual(props["id"]["pattern"], run_evals.ID_RE.pattern)
        self.assertEqual(rubric_props["id"]["pattern"], run_evals.ID_RE.pattern)


class TestValidationCatchesBadScenarios(unittest.TestCase):
    def _base(self):
        return {
            "id": "x", "_path": "eval-harness/scenarios/x.toml", "skill": "skills",
            "title": "t", "category": "c", "severity": "high", "prompt": "p",
            "rubric": [{"id": "r", "check": "regex_any", "pattern": "a", "description": "d"}],
        }

    def test_missing_required_field(self):
        s = self._base(); del s["prompt"]
        self.assertTrue(any("prompt" in p for p in run_evals.validate_scenario(s)))

    def test_bad_severity(self):
        s = self._base(); s["severity"] = "urgent"
        self.assertTrue(any("severity" in p for p in run_evals.validate_scenario(s)))

    def test_skill_path_must_be_repo_relative_directory(self):
        s = self._base()
        s["skill"] = "/tmp/skill"
        self.assertTrue(any("repo-relative" in p for p in run_evals.validate_scenario(s)))

        s["skill"] = "../outside"
        self.assertTrue(any("inside the repository" in p for p in run_evals.validate_scenario(s)))

        s["skill"] = "README.md"
        self.assertTrue(any("must be a directory" in p for p in run_evals.validate_scenario(s)))

    def test_context_data_must_be_repo_relative_list(self):
        s = self._base()
        s["context_data"] = "README.md"
        self.assertTrue(any("context_data must be a list" in p for p in run_evals.validate_scenario(s)))

        s["context_data"] = ""
        self.assertTrue(any("context_data must be a list" in p for p in run_evals.validate_scenario(s)))

        s["context_data"] = ["/tmp/data.csv", "../outside.csv"]
        problems = run_evals.validate_scenario(s)
        self.assertTrue(any("repo-relative" in p for p in problems))
        self.assertTrue(any("inside the repository" in p for p in problems))

        s["context_data"] = [123, "no/such/file.csv"]
        problems = run_evals.validate_scenario(s)
        self.assertTrue(any("context_data[0] must be a non-empty string" in p for p in problems))
        self.assertTrue(any("path does not exist" in p for p in problems))

        s["context_data"] = ["README.md"]
        self.assertFalse(run_evals.validate_scenario(s))

    def test_malformed_rubric_reports_errors_without_crashing(self):
        s = self._base()
        s["rubric"] = "not-a-list"
        self.assertTrue(any("rubric must be a list" in p for p in run_evals.validate_scenario(s)))

        s["rubric"] = []
        self.assertTrue(any("rubric has no items" in p for p in run_evals.validate_scenario(s)))

        s["rubric"] = ["not-a-table"]
        self.assertTrue(
            any("rubric[0] must be a table/object" in p for p in run_evals.validate_scenario(s))
        )

    def test_stem_must_match_id(self):
        s = self._base(); s["_path"] = "eval-harness/scenarios/other.toml"
        self.assertTrue(any("file stem" in p for p in run_evals.validate_scenario(s)))

    def test_invalid_check_type(self):
        s = self._base(); s["rubric"][0]["check"] = "nope"
        self.assertTrue(any("invalid check" in p for p in run_evals.validate_scenario(s)))

    def test_regex_without_pattern(self):
        s = self._base(); s["rubric"][0] = {"id": "r", "check": "regex_any", "description": "d"}
        self.assertTrue(any("needs 'pattern'" in p for p in run_evals.validate_scenario(s)))

    def test_duplicate_rubric_ids(self):
        s = self._base()
        s["rubric"].append({"id": "r", "check": "manual", "description": "d"})
        self.assertTrue(any("duplicate rubric id" in p for p in run_evals.validate_scenario(s)))

    def test_bad_id_shape(self):
        s = self._base()
        s["id"] = "Bad_ID"
        s["_path"] = "eval-harness/scenarios/Bad_ID.toml"
        self.assertTrue(any("id must match" in p for p in run_evals.validate_scenario(s)))

    def test_bad_regex_is_caught(self):
        s = self._base(); s["rubric"][0]["pattern"] = "("
        self.assertTrue(any("invalid regex" in p for p in run_evals.validate_scenario(s)))

    def test_patterns_must_be_list(self):
        s = self._base(); s["rubric"][0] = {
            "id": "r", "check": "regex_any", "patterns": "not-a-list", "description": "d"
        }
        self.assertTrue(any("patterns must be a list" in p for p in run_evals.validate_scenario(s)))

    def test_required_and_weight_types(self):
        s = self._base()
        s["rubric"][0]["required"] = "yes"
        s["rubric"][0]["weight"] = -1
        problems = run_evals.validate_scenario(s)
        self.assertTrue(any("required must be boolean" in p for p in problems))
        self.assertTrue(any("weight must be a non-negative number" in p for p in problems))

    def test_numeric_sign_defaults_to_positive(self):
        s = self._base(); s["rubric"][0] = {
            "id": "r", "check": "numeric_sign", "extract": r"x = ([0-9.]+)", "description": "d"
        }
        self.assertFalse(run_evals.validate_scenario(s))


class TestGrader(unittest.TestCase):
    def test_example_candidates_discriminate(self):
        scenarios = run_evals.load_scenarios()
        by_id = {s["id"]: s for s in scenarios}
        cand = run_evals.ROOT / "eval-harness" / "candidates" / "_example"

        # The deliberately weak weak-IV answer must be gated.
        weak = run_evals.grade_candidate(by_id["statspai-weak-iv"], cand)
        self.assertEqual(weak["status"], "fail-required")
        self.assertIn("flags-weak-instrument", weak["required_failed"])

        # The good staggered-DiD answer must pass required items, while leaving
        # its judgement-only item open for a human/LLM judge.
        good = run_evals.grade_candidate(by_id["statspai-staggered-did"], cand)
        self.assertEqual(good["status"], "needs-manual")
        self.assertEqual(good["required_failed"], [])
        self.assertIn("estimating-equation-and-assumption", good["manual_items"])

        # The citation-hygiene fixture must pass required anti-fabrication checks.
        cite = run_evals.grade_candidate(by_id["citation-hygiene-no-fake-refs"], cand)
        self.assertEqual(cite["status"], "needs-manual")
        self.assertEqual(cite["required_failed"], [])

        # Runtime-safety fixture must pass required anti-dangerous-execution checks.
        runtime = run_evals.grade_candidate(by_id["runtime-safety-replication-setup"], cand)
        self.assertEqual(runtime["status"], "needs-manual")
        self.assertEqual(runtime["required_failed"], [])

        # Replication-package fixture must pass required AEA deposit checks.
        replication = run_evals.grade_candidate(by_id["aer-replication-package"], cand)
        self.assertEqual(replication["status"], "needs-manual")
        self.assertEqual(replication["required_failed"], [])

        # Multiple-testing fixture must pass required anti-cherry-picking checks.
        robustness = run_evals.grade_candidate(by_id["aer-robustness-multiple-testing"], cand)
        self.assertEqual(robustness["status"], "needs-manual")
        self.assertEqual(robustness["required_failed"], [])

        # A fixture with only auto-checkable items can be a full pass.
        abstract = run_evals.grade_candidate(by_id["aer-abstract-100words"], cand)
        self.assertEqual(abstract["status"], "pass")

    def test_expected_required_failure_cli_gate(self):
        cand = run_evals.ROOT / "eval-harness" / "candidates" / "_example"
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(
                run_evals.main([
                    "--grade", str(cand),
                    "--expect-graded", "8",
                    "--expect-fail-required", "statspai-weak-iv",
                    "--expect-graded-categories",
                    "causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity",
                    "--fail-on-orphans",
                    "--fail-on-partial",
                ]),
                0,
            )
            self.assertEqual(
                run_evals.main([
                    "--grade", str(cand),
                    "--expect-graded", "7",
                    "--expect-fail-required", "statspai-weak-iv",
                ]),
                1,
            )
            self.assertEqual(
                run_evals.main([
                    "--grade", str(cand),
                    "--expect-graded-categories", "not-covered",
                    "--expect-fail-required", "statspai-weak-iv",
                ]),
                1,
            )
            self.assertEqual(
                run_evals.main([
                    "--grade", str(cand),
                    "--expect-fail-required", "",
                ]),
                1,
            )

    def test_no_write_skips_scorecard_update(self):
        cand = run_evals.ROOT / "eval-harness" / "candidates" / "_example"
        results_json = run_evals.RESULTS_DIR / "results.json"
        before = results_json.read_text(encoding="utf-8") if results_json.exists() else None
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = run_evals.main([
                "--grade", str(cand),
                "--expect-fail-required", "statspai-weak-iv",
                "--no-write",
            ])
        after = results_json.read_text(encoding="utf-8") if results_json.exists() else None
        self.assertEqual(code, 0)
        self.assertEqual(after, before)

    def test_lint_coverage_cli_gate(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(
                run_evals.main([
                    "--min-scenarios", "17",
                    "--min-auto-checks", "80",
                    "--expect-categories",
                    "causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity,writing-compliance,writing-style",
                ]),
                0,
            )
            self.assertEqual(run_evals.main(["--min-scenarios", "999"]), 1)
            self.assertEqual(run_evals.main(["--min-auto-checks", "999"]), 1)
            self.assertEqual(run_evals.main(["--expect-categories", "not-covered"]), 1)
            self.assertEqual(run_evals.main(["--min-scenarios", "-1"]), 1)

    def test_orphan_candidate_files_are_detected(self):
        scenarios = run_evals.load_scenarios()
        with tempfile.TemporaryDirectory() as tmp:
            cand = run_evals.Path(tmp)
            (cand / "statspai-weak-iv.md").write_text("placeholder", encoding="utf-8")
            (cand / "typo-scenario.md").write_text("placeholder", encoding="utf-8")
            (cand / "ignored.csv").write_text("placeholder", encoding="utf-8")

            orphans = run_evals.orphan_candidate_files(cand, scenarios)
            self.assertEqual([p.name for p in orphans], ["typo-scenario.md"])

            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(run_evals.main(["--grade", str(cand), "--fail-on-orphans"]), 1)

    def test_partial_candidates_can_fail_smoke_gate(self):
        scenarios = run_evals.load_scenarios()
        by_id = {s["id"]: s for s in scenarios}
        with tempfile.TemporaryDirectory() as tmp:
            cand = run_evals.Path(tmp)
            (cand / "aer-abstract-100words.md").write_text(
                "In this paper, we undertake a study of early childhood education. "
                "Participation increases adult earnings by 12 percent.",
                encoding="utf-8",
            )

            graded = run_evals.grade_candidate(by_id["aer-abstract-100words"], cand)
            self.assertEqual(graded["status"], "partial")
            self.assertEqual(graded["required_failed"], [])

            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(run_evals.main(["--grade", str(cand)]), 0)
                self.assertEqual(run_evals.main(["--grade", str(cand), "--fail-on-partial"]), 1)

    def test_cli_directory_arguments_reject_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = run_evals.Path(tmp) / "not-a-dir.md"
            path.write_text("placeholder", encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(run_evals.main(["--grade", str(path)]), 1)
                self.assertEqual(run_evals.main(["--judge-prompts", str(path)]), 1)

    def test_combined_judge_prompt_command_validates_candidate_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_candidate = run_evals.Path(tmp) / "not-a-dir.md"
            bad_candidate.write_text("placeholder", encoding="utf-8")
            out_dir = run_evals.Path(tmp) / "judge-prompts"

            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(
                    run_evals.main([
                        "--judge-prompts", str(out_dir),
                        "--grade", str(bad_candidate),
                    ]),
                    1,
                )
            self.assertFalse(out_dir.exists())


class TestJudge(unittest.TestCase):
    def test_parse_fenced_json(self):
        text = 'Sure!\n```json\n{"items": [{"id": "a", "verdict": "pass", "why": "ok"}]}\n```'
        out = run_evals.parse_judge_response(text)
        self.assertEqual(out["a"]["verdict"], "pass")

    def test_parse_bare_json_with_prose(self):
        text = 'Here is my judgement: {"items":[{"id":"x","verdict":"fail"}]} done.'
        out = run_evals.parse_judge_response(text)
        self.assertEqual(out["x"]["verdict"], "fail")

    def test_parse_no_json_raises(self):
        with self.assertRaises(ValueError):
            run_evals.parse_judge_response("no json here")

    def test_mock_judge_resolves_manual_item(self):
        scenarios = run_evals.load_scenarios()
        by_id = {s["id"]: s for s in scenarios}
        cand = run_evals.ROOT / "eval-harness" / "candidates" / "_example"

        # de-aigc has a manual item "meaning-and-fluency"; a mock judge passes it.
        def mock_judge(prompt):
            return {"meaning-and-fluency": {"verdict": "pass", "why": "faithful"}}

        graded = run_evals.grade_candidate(by_id["de-aigc-structural"], cand, judge=mock_judge)
        manual_item = next(i for i in graded["items"] if i["id"] == "meaning-and-fluency")
        self.assertEqual(manual_item["status"], "pass")
        self.assertEqual(graded["status"], "pass")
        self.assertNotIn("meaning-and-fluency", graded["manual_items"])

    def test_judge_failure_does_not_crash(self):
        scenarios = run_evals.load_scenarios()
        by_id = {s["id"]: s for s in scenarios}
        cand = run_evals.ROOT / "eval-harness" / "candidates" / "_example"

        def boom(prompt):
            raise RuntimeError("network down")

        graded = run_evals.grade_candidate(by_id["de-aigc-structural"], cand, judge=boom)
        self.assertIn("judge_note", graded)
        # Manual item stays manual when the judge is unavailable.
        self.assertEqual(graded["status"], "needs-manual")
        self.assertIn("meaning-and-fluency", graded["manual_items"])


if __name__ == "__main__":
    unittest.main()
