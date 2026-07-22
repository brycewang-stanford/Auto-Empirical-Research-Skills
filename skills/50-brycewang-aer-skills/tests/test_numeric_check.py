"""Unit tests for examples/_aer_numeric_check.py (the NUMERIC-CHECK protocol)."""

from __future__ import annotations

import pytest

from _aer_numeric_check import PROTOCOL_PREFIX, numeric_check


class TestTargetTolerance:
    def test_within_tolerance_passes_and_returns_float(self):
        result = numeric_check("beta", 0.02, target=0.0, tol=0.03)
        assert result == pytest.approx(0.02)
        assert isinstance(result, float)

    def test_exact_boundary_passes(self):
        # abs(got - target) == tol is accepted (tolerance is inclusive).
        assert numeric_check("edge", 1.1, target=1.0, tol=0.1) == pytest.approx(1.1)

    def test_outside_tolerance_raises_assertion_error(self):
        with pytest.raises(AssertionError, match="numeric check failed"):
            numeric_check("beta", 0.5, target=0.0, tol=0.01)

    def test_negative_deviation_within_tolerance_passes(self):
        assert numeric_check("neg", -0.02, target=0.0, tol=0.03) == pytest.approx(-0.02)

    def test_target_without_tol_raises_value_error(self):
        with pytest.raises(ValueError, match="'target' requires 'tol'"):
            numeric_check("bad-spec", 1.0, target=1.0)


class TestBounds:
    def test_lo_bound_at_boundary_passes(self):
        assert numeric_check("coverage", 0.94, lo=0.94) == pytest.approx(0.94)

    def test_lo_bound_below_raises(self):
        with pytest.raises(AssertionError):
            numeric_check("coverage", 0.93, lo=0.94)

    def test_hi_bound_at_boundary_passes(self):
        assert numeric_check("rate", 1.0, hi=1.0) == pytest.approx(1.0)

    def test_hi_bound_above_raises(self):
        with pytest.raises(AssertionError):
            numeric_check("rate", 1.01, hi=1.0)

    def test_lo_hi_band_pass(self):
        assert numeric_check("band", 0.5, lo=0.1, hi=1.0) == pytest.approx(0.5)

    def test_lo_hi_band_fails_below(self):
        with pytest.raises(AssertionError):
            numeric_check("band", 0.05, lo=0.1, hi=1.0)

    def test_lo_hi_band_fails_above(self):
        with pytest.raises(AssertionError):
            numeric_check("band", 1.5, lo=0.1, hi=1.0)

    def test_no_spec_at_all_raises_value_error(self):
        with pytest.raises(ValueError, match="pass either target"):
            numeric_check("no-spec", 1.0)


class TestProtocolLine:
    def test_pass_line_format_target_tol(self, capsys):
        numeric_check("my check", 1.2345678, target=1.23, tol=0.01)
        out = capsys.readouterr().out
        assert out == "NUMERIC-CHECK | my check | got=1.2346 | target=1.23 tol=0.01 | PASS\n"

    def test_pass_line_format_lo_hi(self, capsys):
        numeric_check("rate", 0.5, lo=0.1, hi=1.0)
        out = capsys.readouterr().out
        assert out == "NUMERIC-CHECK | rate | got=0.5000 | >=0.1 <=1 | PASS\n"

    def test_lo_only_spec(self, capsys):
        numeric_check("cov", 0.95, lo=0.94)
        assert "| >=0.94 | PASS" in capsys.readouterr().out

    def test_fail_line_is_printed_before_the_raise(self, capsys):
        with pytest.raises(AssertionError):
            numeric_check("drifted", 9.0, target=0.0, tol=0.1)
        out = capsys.readouterr().out
        assert out.startswith(PROTOCOL_PREFIX + " | drifted | got=9.0000 |")
        assert out.rstrip().endswith("FAIL")

    def test_prefix_constant_matches_smoke_runner_contract(self):
        # scripts/run_example_smoke.py greps for this exact prefix.
        assert PROTOCOL_PREFIX == "NUMERIC-CHECK"

    def test_numeric_string_input_is_coerced(self, capsys):
        assert numeric_check("coerced", "0.5", lo=0.0) == pytest.approx(0.5)
        assert "got=0.5000" in capsys.readouterr().out
