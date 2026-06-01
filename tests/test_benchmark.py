"""Tests for the LaLonde benchmark: golden values + anti-fabrication grading."""

from __future__ import annotations

import tomllib
import unittest

from _helpers import ROOT, load_module

lalonde = load_module("benchmark/lib/lalonde.py", "aers_lalonde")
card = load_module("benchmark/lib/card.py", "aers_card")
check_benchmark = load_module("benchmark/check_benchmark.py", "aers_check_benchmark")

DATA = ROOT / "demo-notebooks" / "_lalonde_data.csv"
CARD_DATA = ROOT / "demo-StatsPAI-skill" / "data" / "card.csv"


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
            cls.task = tomllib.load(fh)
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
            cls.task = tomllib.load(fh)
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


if __name__ == "__main__":
    unittest.main()
