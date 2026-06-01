"""Tests for the LaLonde benchmark: golden values + anti-fabrication grading."""

from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest

from _helpers import ROOT, load_module

lalonde = load_module("benchmark/lib/lalonde.py", "aers_lalonde")
card = load_module("benchmark/lib/card.py", "aers_card")
simdid = load_module("benchmark/lib/simdid.py", "aers_simdid")
check_benchmark = load_module("benchmark/check_benchmark.py", "aers_check_benchmark")
toml_compat = load_module("scripts/toml_compat.py", "aers_toml_compat")

DATA = ROOT / "demo-notebooks" / "_lalonde_data.csv"
CARD_DATA = ROOT / "demo-StatsPAI-skill" / "data" / "card.csv"
SIMDID_DATA = ROOT / "benchmark" / "data" / "sim-staggered-did.csv"


class TestLalondeNumbers(unittest.TestCase):
    """Golden-value regression tests grounded in the vendored dataset."""

    @classmethod
    def setUpClass(cls):
        cls.rows = lalonde.load(DATA)

    def test_sample_sizes(self):
        t, c = lalonde.split(self.rows, "treat")
        self.assertEqual((len(t), len(c)), (185, 429))

    def test_naive_att_is_negative_known_value(self):
        v = lalonde.naive_att(self.rows, "treat", "re78")
        self.assertLess(v, 0)
        self.assertAlmostEqual(v, -635.0, delta=1.0)

    def test_adjusted_att_recovers_positive_near_benchmark(self):
        v = lalonde.adjusted_att(self.rows, "treat", "re78")
        self.assertGreater(v, 0)
        self.assertAlmostEqual(v, 1548.0, delta=5.0)

    def test_imbalance_count(self):
        smd = lalonde.smd_table(self.rows, "treat")
        big = [k for k, val in smd.items() if abs(val) > 0.25]
        self.assertGreaterEqual(len(big), 3)
        self.assertIn("black", big)
        self.assertAlmostEqual(smd["black"], 1.668, delta=0.01)

    def test_ols_matches_known_solution(self):
        # y = 2 + 3*x exactly -> intercept 2, slope 3.
        X = [[1.0, float(i)] for i in range(5)]
        y = [2 + 3 * i for i in range(5)]
        b = lalonde.ols(X, y)
        self.assertAlmostEqual(b[0], 2.0, places=6)
        self.assertAlmostEqual(b[1], 3.0, places=6)


class TestBenchmarkGrading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "benchmark" / "tasks" / "lalonde-recovery.toml").open("rb") as fh:
            cls.task = toml_compat.load(fh)
        rows = lalonde.load(DATA)
        cls.truth = {
            "naive_att": lalonde.naive_att(rows, "treat", "re78"),
            "smd": lalonde.smd_table(rows, "treat"),
        }

    def _good_candidate(self):
        rows = lalonde.load(DATA)
        return {
            "naive_att": round(lalonde.naive_att(rows, "treat", "re78"), 1),
            "adjusted_att": round(lalonde.adjusted_att(rows, "treat", "re78"), 1),
            "balance": {k: round(v, 3) for k, v in lalonde.smd_table(rows, "treat").items()},
        }

    def test_reference_candidate_passes_all(self):
        graded = check_benchmark.grade(self.task, self._good_candidate(), self.truth)
        req_fail = [g["id"] for g in graded if g["required"] and not g["passed"]]
        self.assertEqual(req_fail, [])

    def test_fabricated_balance_is_caught(self):
        cand = self._good_candidate()
        cand["naive_att"] = 2000.0                       # claim positive naive
        cand["balance"] = {k: 0.01 for k in cand["balance"]}  # claim perfect balance
        graded = check_benchmark.grade(self.task, cand, self.truth)
        req_fail = [g["id"] for g in graded if g["required"] and not g["passed"]]
        self.assertIn("honest-reported-numbers", req_fail)
        self.assertIn("surfaces-imbalance", req_fail)


class TestBenchmarkSpecValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "benchmark" / "tasks" / "lalonde-recovery.toml").open("rb") as fh:
            cls.task = toml_compat.load(fh)
        cls.task_path = ROOT / "benchmark" / "tasks" / "lalonde-recovery.toml"

    def test_current_task_specs_are_valid(self):
        for task_path in sorted((ROOT / "benchmark" / "tasks").glob("*.toml")):
            with task_path.open("rb") as fh:
                task = toml_compat.load(fh)
            with self.subTest(task=task_path.name):
                self.assertEqual(check_benchmark.validate_task(task, task_path), [])

    def test_task_id_must_match_file_stem(self):
        task = copy.deepcopy(self.task)
        task["id"] = "wrong-task"
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("match file stem" in p for p in problems))

    def test_unknown_gold_check_is_invalid(self):
        task = copy.deepcopy(self.task)
        task["gold"][0]["check"] = "not-a-real-check"
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("unknown check" in p for p in problems))

    def test_unsupported_task_id_is_invalid(self):
        task = copy.deepcopy(self.task)
        task["id"] = "new-benchmark"
        problems = check_benchmark.validate_task(task, self.task_path.with_name("new-benchmark.toml"))
        self.assertTrue(any("unsupported task id" in p for p in problems))

    def test_duplicate_gold_ids_are_invalid(self):
        task = copy.deepcopy(self.task)
        task["gold"][1]["id"] = task["gold"][0]["id"]
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("duplicate id" in p for p in problems))

    def test_required_and_weight_types_are_checked(self):
        task = copy.deepcopy(self.task)
        task["gold"][0]["required"] = "yes"
        task["gold"][0]["weight"] = 0
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("required" in p and "boolean" in p for p in problems))
        self.assertTrue(any("weight" in p and "positive" in p for p in problems))

    def test_task_specific_fields_are_checked(self):
        task = copy.deepcopy(self.task)
        task.pop("experimental_tol")
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("experimental_tol" in p and "numeric" in p for p in problems))

    def test_data_path_must_be_repo_relative_file(self):
        self.assertEqual(
            check_benchmark.validate_repo_relative_file(
                "demo-notebooks/_lalonde_data.csv",
                "data",
            ),
            [],
        )

        task = copy.deepcopy(self.task)
        task["data"] = "/tmp/lalonde.csv"
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("repo-relative" in p for p in problems))

        task["data"] = "../outside.csv"
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("inside the repository" in p for p in problems))

        task["data"] = "demo-notebooks"
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("must be a file" in p for p in problems))

    def test_reference_candidate_dir_name_is_checked(self):
        task = copy.deepcopy(self.task)
        task["reference_candidate"] = "../outside"
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("reference_candidate" in p and "single directory" in p for p in problems))

    def test_candidate_override_dir_name_is_checked(self):
        self.assertEqual(check_benchmark.validate_candidate_dir_name("run-1.2_ok"), [])
        problems = check_benchmark.validate_candidate_dir_name("../outside", "candidate")
        self.assertTrue(any("single directory" in p for p in problems))

        with contextlib.redirect_stderr(io.StringIO()):
            code, failed = check_benchmark.grade_task(
                self.task_path,
                "../outside",
                strict=True,
                fail_on_partial=True,
            )
        self.assertEqual(code, 1)
        self.assertEqual(failed, ["lalonde-recovery"])

    def test_check_specific_fields_are_checked(self):
        task = copy.deepcopy(self.task)
        task["gold"][2].pop("min_swing")
        task["gold"][4].pop("smd_tol")
        problems = check_benchmark.validate_task(task, self.task_path)
        self.assertTrue(any("min_swing" in p for p in problems))
        self.assertTrue(any("smd_tol" in p for p in problems))

    def test_candidate_task_must_match_benchmark_task(self):
        candidate = {"task": "card-iv-recovery"}
        problems = check_benchmark.validate_candidate(
            self.task,
            candidate,
            ROOT / "benchmark" / "candidates" / "bad" / "results.json",
        )
        self.assertEqual(
            problems,
            ["candidate task 'card-iv-recovery' does not match benchmark task 'lalonde-recovery'"],
        )

    def test_candidate_must_be_json_object(self):
        problems = check_benchmark.validate_candidate(
            self.task,
            ["not", "an", "object"],
            ROOT / "benchmark" / "candidates" / "bad" / "results.json",
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("must contain a JSON object", problems[0])

    def test_current_reference_candidates_are_valid(self):
        for task_path in sorted((ROOT / "benchmark" / "tasks").glob("*.toml")):
            with task_path.open("rb") as fh:
                task = toml_compat.load(fh)
            candidate_path = (
                ROOT / "benchmark" / "candidates" / task["reference_candidate"] / "results.json"
            )
            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
            with self.subTest(task=task["id"]):
                self.assertEqual(
                    check_benchmark.validate_candidate(task, candidate, candidate_path),
                    [],
                )

    def test_candidate_numeric_fields_are_checked(self):
        candidate = {
            "task": "lalonde-recovery",
            "naive_att": "-635",
            "adjusted_att": 1548.2,
        }
        problems = check_benchmark.validate_candidate(
            self.task,
            candidate,
            ROOT / "benchmark" / "candidates" / "bad" / "results.json",
        )
        self.assertIn("candidate field 'naive_att' must be numeric", problems)

    def test_candidate_numeric_map_fields_are_checked(self):
        candidate = {
            "task": "lalonde-recovery",
            "naive_att": -635.0,
            "adjusted_att": 1548.2,
            "balance": {"age": "0.2"},
        }
        problems = check_benchmark.validate_candidate(
            self.task,
            candidate,
            ROOT / "benchmark" / "candidates" / "bad" / "results.json",
        )
        self.assertIn("candidate field 'balance.age' must be numeric", problems)

        candidate["balance"] = []
        problems = check_benchmark.validate_candidate(
            self.task,
            candidate,
            ROOT / "benchmark" / "candidates" / "bad" / "results.json",
        )
        self.assertIn("candidate field 'balance' must be an object of numeric values", problems)

    def test_fail_on_partial_exit_logic(self):
        self.assertEqual(
            check_benchmark.exit_code_for_failures([], [], strict=True, fail_on_partial=True),
            0,
        )
        self.assertEqual(
            check_benchmark.exit_code_for_failures(["required"], [], strict=True, fail_on_partial=False),
            1,
        )
        self.assertEqual(
            check_benchmark.exit_code_for_failures(["required"], [], strict=False, fail_on_partial=False),
            0,
        )
        self.assertEqual(
            check_benchmark.exit_code_for_failures([], ["optional"], strict=True, fail_on_partial=False),
            0,
        )
        self.assertEqual(
            check_benchmark.exit_code_for_failures([], ["optional"], strict=True, fail_on_partial=True),
            1,
        )

    def test_orphan_result_files_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            results_dir = check_benchmark.Path(tmp)
            (results_dir / "lalonde-recovery.json").write_text("{}", encoding="utf-8")
            (results_dir / "old-task.json").write_text("{}", encoding="utf-8")
            (results_dir / "README.md").write_text("not a result", encoding="utf-8")

            orphans = check_benchmark.orphan_result_files(
                results_dir,
                {"lalonde-recovery", "card-iv-recovery"},
            )
            self.assertEqual([path.name for path in orphans], ["old-task.json"])


class TestCardNumbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = card.load(CARD_DATA)

    def test_sample_size(self):
        self.assertEqual(len(self.rows), 3010)

    def test_ols_return_known(self):
        self.assertAlmostEqual(card.ols_return(self.rows), 0.0747, delta=0.002)

    def test_iv_exceeds_ols(self):
        ols, iv = card.ols_return(self.rows), card.iv_return(self.rows)
        self.assertGreater(iv, ols)
        self.assertAlmostEqual(iv, 0.1315, delta=0.005)

    def test_first_stage_F_known(self):
        coef, f = card.first_stage(self.rows)
        self.assertGreater(coef, 0)
        self.assertAlmostEqual(f, 13.26, delta=0.5)


class TestCardGrading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "benchmark" / "tasks" / "card-iv-recovery.toml").open("rb") as fh:
            cls.task = toml_compat.load(fh)
        cls.truth = check_benchmark.compute_truth(cls.task)

    def _good(self):
        rows = card.load(CARD_DATA)
        coef, f = card.first_stage(rows)
        return {"ols_return": round(card.ols_return(rows), 4),
                "iv_return": round(card.iv_return(rows), 4),
                "first_stage_F": round(f, 2), "first_stage_coef": round(coef, 4)}

    def test_reference_passes(self):
        graded = check_benchmark.grade(self.task, self._good(), self.truth)
        self.assertEqual([g["id"] for g in graded if g["required"] and not g["passed"]], [])

    def test_iv_below_ols_fails(self):
        cand = self._good()
        cand["iv_return"] = 0.05  # claim IV < OLS, contradicting the data
        graded = check_benchmark.grade(self.task, cand, self.truth)
        req_fail = [g["id"] for g in graded if g["required"] and not g["passed"]]
        self.assertIn("iv-exceeds-ols", req_fail)
        self.assertIn("honest-reported-numbers", req_fail)


class TestStaggeredDidNumbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = simdid.load(SIMDID_DATA)

    def test_sample_size(self):
        self.assertEqual(len(self.rows), 600)

    def test_twfe_is_biased_downward(self):
        true = simdid.true_att(self.rows)
        twfe = simdid.twfe_att(self.rows)
        self.assertAlmostEqual(true, 2.9091, delta=0.001)
        self.assertAlmostEqual(twfe, 1.4545, delta=0.001)
        self.assertGreater(abs(true - twfe), 0.5)

    def test_group_time_recovers_true_att(self):
        gt = simdid.group_time_att(self.rows)
        self.assertEqual(len(gt), 11)
        self.assertAlmostEqual(simdid.cs_att(self.rows), simdid.true_att(self.rows), delta=0.001)


class TestStaggeredDidGrading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "benchmark" / "tasks" / "did-staggered-recovery.toml").open("rb") as fh:
            cls.task = toml_compat.load(fh)
        cls.truth = check_benchmark.compute_truth(cls.task)

    def _good(self):
        rows = simdid.load(SIMDID_DATA)
        return {
            "true_att": round(simdid.true_att(rows), 4),
            "twfe_att": round(simdid.twfe_att(rows), 4),
            "cs_att": round(simdid.cs_att(rows), 4),
        }

    def test_reference_passes(self):
        graded = check_benchmark.grade(self.task, self._good(), self.truth)
        self.assertEqual([g["id"] for g in graded if g["required"] and not g["passed"]], [])

    def test_using_twfe_as_robust_estimate_fails(self):
        cand = self._good()
        cand["cs_att"] = cand["twfe_att"]
        graded = check_benchmark.grade(self.task, cand, self.truth)
        req_fail = [g["id"] for g in graded if g["required"] and not g["passed"]]
        self.assertIn("robust-recovers-true-att", req_fail)
        self.assertIn("honest-reported-numbers", req_fail)


if __name__ == "__main__":
    unittest.main()
