"""Unit tests for scripts/referee_calibration.py.

Covers the rubric verdict mapping (every branch of the floor-not-average
ladder), scored-run parsing, verdict normalization, and the end-to-end check
against the shipped worked example --- all hermetic.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import referee_calibration as rc

REPO_ROOT = Path(__file__).resolve().parents[1]


def _scores(**kw) -> dict:
    base = {d: 4 for d in rc.DIMENSIONS}
    base.update(kw)
    return base


@pytest.mark.parametrize("scores, expected", [
    (_scores(), "minor r&r"),                                    # clean sweep
    (_scores(identification=3, robustness=3, magnitudes=3), "major r&r"),
    (_scores(identification=2), "reject"),                       # fatal ident
    (_scores(integrity=2), "reject"),                            # fatal integrity
    (_scores(exposition=1), "reject"),                           # any 1 vetoes
    (_scores(contribution=2), "reject"),                         # field-journal
    (_scores(contribution=3, identification=3, data=2, robustness=2,
             magnitudes=2, exposition=2, integrity=3), "major r&r"),
])
def test_verdict_mapping(scores, expected):
    assert rc.compute_verdict(scores) == expected


def test_minor_requires_full_sweep():
    # A single 3 anywhere drops minor R&R down to major R&R.
    assert rc.compute_verdict(_scores(data=3)) == "major r&r"


def test_veto_beats_six_good_dimensions():
    # Six 5s cannot rescue a fatal identification score.
    scores = {d: 5 for d in rc.DIMENSIONS}
    scores["identification"] = 2
    assert rc.compute_verdict(scores) == "reject"


@pytest.mark.parametrize("raw, norm", [
    ("major R&R", "major r&r"),
    ("Major R and R", "major r&r"),
    ("  minor   r&r ", "minor r&r"),
    ("Reject", "reject"),
])
def test_normalize_verdict(raw, norm):
    assert rc.normalize_verdict(raw) == norm


def test_parse_runs_extracts_scores_and_verdict():
    doc = (
        "RUBRIC SCORES: contribution 4, identification 3, data 4, robustness 3,\n"
        "magnitudes 3, exposition 4, integrity 4\n\nVERDICT: major R&R\n"
    )
    runs = rc.parse_runs(doc)
    assert len(runs) == 1
    assert runs[0]["scores"]["identification"] == 3
    assert runs[0]["verdict"] == "major r&r"


def test_mismatched_verdict_is_flagged():
    doc = (
        "RUBRIC SCORES: contribution 4, identification 2, data 4, robustness 4,\n"
        "magnitudes 4, exposition 4, integrity 4\nVERDICT: major R&R\n"
    )
    _, errors = rc.verify_text(doc)
    assert any("!=" in e for e in errors)


def test_missing_dimension_is_flagged():
    doc = "RUBRIC SCORES: contribution 4, identification 3\nVERDICT: reject\n"
    _, errors = rc.verify_text(doc)
    assert any("missing dimension" in e for e in errors)


def test_no_scored_run_is_flagged():
    _, errors = rc.verify_text("A desk reject with no scores.\n")
    assert any("no scored runs" in e for e in errors)


def test_worked_example_is_self_consistent():
    text = (REPO_ROOT / "examples" / "referee-report-example.md").read_text(
        encoding="utf-8")
    runs, errors = rc.verify_text(text)
    assert runs, "worked example should contain at least one scored run"
    assert errors == []


def test_selftest_passes():
    assert rc.run_selftest() == 0
