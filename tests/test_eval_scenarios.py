"""Tests for scenario loading/validation and the grader (evals/run_evals.py)."""

from __future__ import annotations

import unittest

from _helpers import load_module

run_evals = load_module("evals/run_evals.py", "aers_run_evals")


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


class TestValidationCatchesBadScenarios(unittest.TestCase):
    def _base(self):
        return {
            "id": "x", "_path": "evals/scenarios/x.toml", "skill": "skills",
            "title": "t", "category": "c", "severity": "high", "prompt": "p",
            "rubric": [{"id": "r", "check": "regex_any", "pattern": "a", "description": "d"}],
        }

    def test_missing_required_field(self):
        s = self._base(); del s["prompt"]
        self.assertTrue(any("prompt" in p for p in run_evals.validate_scenario(s)))

    def test_bad_severity(self):
        s = self._base(); s["severity"] = "urgent"
        self.assertTrue(any("severity" in p for p in run_evals.validate_scenario(s)))

    def test_stem_must_match_id(self):
        s = self._base(); s["_path"] = "evals/scenarios/other.toml"
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


class TestGrader(unittest.TestCase):
    def test_example_candidates_discriminate(self):
        scenarios = run_evals.load_scenarios()
        by_id = {s["id"]: s for s in scenarios}
        cand = run_evals.ROOT / "evals" / "candidates" / "_example"

        # The deliberately weak weak-IV answer must be gated.
        weak = run_evals.grade_candidate(by_id["statspai-weak-iv"], cand)
        self.assertEqual(weak["status"], "fail-required")
        self.assertIn("flags-weak-instrument", weak["required_failed"])

        # The good staggered-DiD answer must pass its required items.
        good = run_evals.grade_candidate(by_id["statspai-staggered-did"], cand)
        self.assertEqual(good["status"], "pass")


if __name__ == "__main__":
    unittest.main()
