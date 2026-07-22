#!/usr/bin/env python3
"""Referee-simulation calibration harness.

The `aer-referee-sim` skill scores a manuscript on the seven dimensions of
`docs/referee-report-rubric.md` and maps those scores to a verdict. That mapping
is a *floor, not an average*: one fatal dimension rejects a paper with six
excellent ones. This harness makes the mapping executable, so a worked referee
run cannot silently drift from the rubric it claims to follow.

It does three things:

  * parses every scored run (`RUBRIC SCORES: ...` + `VERDICT: ...`) out of a
    referee-report file,
  * recomputes the verdict from the scores using the rubric's Verdict Mapping,
    and
  * fails if a stated verdict disagrees with the recomputed one, if a dimension
    is missing or out of the 0-5 range, or if the verdict string is unknown.

Run against the shipped worked example (the default) so the example stays
self-consistent with the rubric; or point it at a fresh simulation to grade it.

Usage:

    python3 scripts/referee_calibration.py                 # check the worked example
    python3 scripts/referee_calibration.py path/to/run.md  # check another run
    python3 scripts/referee_calibration.py --selftest      # hermetic unit gate
    python3 scripts/referee_calibration.py --json          # machine-readable
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPORT = ROOT / "examples" / "referee-report-example.md"

# The seven rubric dimensions, in the canonical order of the rubric.
DIMENSIONS = (
    "contribution", "identification", "data", "robustness",
    "magnitudes", "exposition", "integrity",
)
SCORE_MIN, SCORE_MAX = 0, 5

# Verdicts the mapping can issue. Acceptance is intentionally not issuable by
# simulation (the rubric caps the ceiling at minor R&R).
VERDICTS = ("reject", "minor r&r", "major r&r")

_SCORES_RE = re.compile(r"RUBRIC SCORES:\s*(.+?)(?:\n\s*\n|VERDICT:)", re.DOTALL)
_VERDICT_RE = re.compile(r"VERDICT:\s*([^\n]+)")
_PAIR_RE = re.compile(r"([a-z][a-z&/ -]*?)\s+([0-5])\b", re.IGNORECASE)


def normalize_verdict(text: str) -> str:
    """Canonicalize a verdict string: lowercase, collapse whitespace, and map
    'R and R' / 'RR' spellings onto 'r&r'."""
    v = text.strip().lower()
    v = re.sub(r"\s+", " ", v)
    v = v.replace(" and ", " & ")
    v = re.sub(r"\br\s*&\s*r\b", "r&r", v)
    v = re.sub(r"\brr\b", "r&r", v)
    return v.strip()


def compute_verdict(scores: dict[str, int]) -> str:
    """The rubric's Verdict Mapping, applied as a precedence ladder (floor, not
    average). Reject conditions veto first; a clean sweep at >= 4 earns minor
    R&R; the general publishable case earns major R&R; anything left rejects."""
    vals = {d: scores[d] for d in DIMENSIONS}
    lowest = min(vals.values())
    # 1. Any fatal dimension vetoes.
    if (lowest <= 1
            or vals["identification"] <= 2
            or vals["integrity"] <= 2
            or vals["contribution"] <= 2):
        return "reject"
    # 2. A clean sweep with no blocking comments -> minor R&R.
    if all(v >= 4 for v in vals.values()):
        return "minor r&r"
    # 3. Publishable contribution with adequate identification -> major R&R.
    if lowest >= 2 and vals["contribution"] >= 3 and vals["identification"] >= 3:
        return "major r&r"
    # 4. Fallthrough.
    return "reject"


def parse_runs(text: str) -> list[dict]:
    """Extract every scored run from a referee-report document. Returns a list
    of {'scores': {...}, 'verdict': str} in document order. Runs without a
    RUBRIC SCORES block (e.g. a Stage 1 desk reject) are skipped."""
    runs: list[dict] = []
    for score_match in _SCORES_RE.finditer(text):
        block = score_match.group(1)
        scores: dict[str, int] = {}
        for name, value in _PAIR_RE.findall(block):
            key = name.strip().lower()
            if key in DIMENSIONS:
                scores[key] = int(value)
        verdict_match = _VERDICT_RE.search(text, score_match.end() - 8)
        verdict = normalize_verdict(verdict_match.group(1)) if verdict_match else ""
        runs.append({"scores": scores, "verdict": verdict})
    return runs


def check_run(run: dict, index: int) -> list[str]:
    """Return a list of calibration errors for one scored run (empty = clean)."""
    errors: list[str] = []
    label = f"run {index}"
    scores = run["scores"]
    missing = [d for d in DIMENSIONS if d not in scores]
    if missing:
        errors.append(f"{label}: missing dimension(s) {', '.join(missing)}")
    for dim, value in scores.items():
        if not SCORE_MIN <= value <= SCORE_MAX:
            errors.append(f"{label}: {dim} score {value} out of range 0-5")
    stated = run["verdict"]
    if stated not in VERDICTS:
        errors.append(f"{label}: unknown or unissuable verdict {stated!r}")
    if missing:
        return errors  # cannot recompute without all seven dimensions
    computed = compute_verdict(scores)
    if stated in VERDICTS and computed != stated:
        errors.append(
            f"{label}: stated verdict {stated!r} != rubric mapping {computed!r} "
            f"for scores {scores}")
    return errors


def verify_text(text: str) -> tuple[list[dict], list[str]]:
    runs = parse_runs(text)
    errors: list[str] = []
    if not runs:
        errors.append("no scored runs found (expected a 'RUBRIC SCORES:' block)")
    for i, run in enumerate(runs, 1):
        errors.extend(check_run(run, i))
    return runs, errors


# --------------------------------------------------------------------------- #
# Self-test: hermetic cases exercising every branch of the mapping.
# --------------------------------------------------------------------------- #

def _scores(**kw) -> dict[str, int]:
    base = {d: 4 for d in DIMENSIONS}
    base.update(kw)
    return base


SELFTEST_CASES = [
    # (label, scores, expected verdict)
    ("all fours -> minor", _scores(), "minor r&r"),
    ("worked example -> major", _scores(identification=3, robustness=3,
                                        magnitudes=3), "major r&r"),
    ("fatal identification vetoes six good dims", _scores(identification=2),
     "reject"),
    ("fatal integrity vetoes", _scores(integrity=2), "reject"),
    ("a single 1 vetoes", _scores(exposition=1), "reject"),
    ("weak contribution is a field-journal reject", _scores(contribution=2),
     "reject"),
    ("publishable floor -> major", _scores(contribution=3, identification=3,
                                           data=2, robustness=2, magnitudes=2,
                                           exposition=2, integrity=3),
     "major r&r"),
]

_MISMATCH_DOC = """
RUBRIC SCORES: contribution 4, identification 2, data 4, robustness 4,
magnitudes 4, exposition 4, integrity 4
VERDICT: major R&R
"""

_CLEAN_DOC = """
RUBRIC SCORES: contribution 4, identification 3, data 4, robustness 3,
magnitudes 3, exposition 4, integrity 4
VERDICT: major R&R
"""


def run_selftest() -> int:
    failures = 0
    total = 0
    for label, scores, expected in SELFTEST_CASES:
        total += 1
        got = compute_verdict(scores)
        if got != expected:
            failures += 1
            print(f"  FAIL mapping[{label}]: expected {expected!r}, got {got!r}")
    # A verdict that contradicts its own scores must be caught.
    total += 1
    _, errs = verify_text(_MISMATCH_DOC)
    if not errs:
        failures += 1
        print("  FAIL: mismatched verdict not flagged")
    # A self-consistent run must pass clean.
    total += 1
    _, errs = verify_text(_CLEAN_DOC)
    if errs:
        failures += 1
        print(f"  FAIL: clean run flagged: {errs}")
    # Verdict normalization variants.
    total += 1
    if normalize_verdict("Major R and R") != "major r&r":
        failures += 1
        print("  FAIL: verdict normalization")
    status = "PASS" if failures == 0 else "FAIL"
    print(f"referee-calibration selftest {status}: {total} cases, "
          f"{failures} failure(s)")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", type=Path, default=DEFAULT_REPORT,
                        help="referee-report markdown file to grade")
    parser.add_argument("--selftest", action="store_true",
                        help="run the hermetic mapping/parse gate")
    parser.add_argument("--json", action="store_true",
                        help="emit machine-readable JSON")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.selftest:
        return run_selftest()

    if not args.report.is_file():
        print(f"error: {args.report} not found", file=sys.stderr)
        return 2
    text = args.report.read_text(encoding="utf-8")
    runs, errors = verify_text(text)

    if args.json:
        print(json.dumps({
            "report": str(args.report.relative_to(ROOT))
            if args.report.is_relative_to(ROOT) else str(args.report),
            "runs": [{"scores": r["scores"], "stated_verdict": r["verdict"],
                      "computed_verdict": compute_verdict(r["scores"])
                      if all(d in r["scores"] for d in DIMENSIONS) else None}
                     for r in runs],
            "errors": errors,
        }, indent=2))
    else:
        for r in runs:
            done = all(d in r["scores"] for d in DIMENSIONS)
            computed = compute_verdict(r["scores"]) if done else "?"
            print(f"scored run: verdict={r['verdict']!r} "
                  f"(rubric mapping: {computed!r})")
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        if not errors:
            print(f"referee calibration PASS: {len(runs)} scored run(s) "
                  "consistent with docs/referee-report-rubric.md")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
