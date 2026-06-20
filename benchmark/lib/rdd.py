#!/usr/bin/env python3
"""Pure-stdlib sharp regression-discontinuity (RD) computations.

The simulated running variable is deterministic and noiseless. Untreated
potential outcomes are linear in the running variable but with DIFFERENT slopes
on either side of the cutoff, and treatment adds a constant jump at the cutoff.
Because the data is exactly piecewise-linear and noiseless, the true
discontinuity (the treatment effect at the cutoff) is known by construction, and
three estimators have sharply different behavior:

* a naive across-cutoff mean difference confounds the jump with the running-
  variable trend and is badly biased;
* a global common-slope OLS (the textbook ``y ~ 1 + D + x`` specification) is
  still biased because it forces one slope on two genuinely different slopes;
* local linear regression on each side at the cutoff recovers the true jump.

This encodes the standard RD lesson (Imbens & Lemieux 2008; Lee & Lemieux 2010;
Gelman & Imbens 2019 on preferring local linear/quadratic fits over global
high-order polynomials; Cattaneo, Idrobo & Titiunik 2019 practical guide).
"""

from __future__ import annotations

import csv
from pathlib import Path

import lalonde  # sibling module in benchmark/lib

# Deterministic noiseless DGP constants. The cutoff is 0; treatment is sharp.
CUTOFF = 0.0
N_POINTS = 101          # symmetric grid x in [-1, 1] including x = 0 (treated side)
INTERCEPT = 0.0         # untreated level at the cutoff (left limit)
SLOPE_LEFT = 1.0        # untreated slope below the cutoff
SLOPE_RIGHT = 4.0       # untreated slope at or above the cutoff (genuinely steeper)
TAU = 3.0               # true treatment effect (jump) at the cutoff
BANDWIDTH = 0.5         # local-linear bandwidth used by the reference estimator


def _grid() -> list[float]:
    # x_i = -1 + 2 i / (N - 1); with N = 101 this includes x = 0 exactly.
    return [round(-1.0 + 2.0 * i / (N_POINTS - 1), 4) for i in range(N_POINTS)]


def generate() -> list[dict]:
    rows: list[dict] = []
    for x in _grid():
        treated = 1 if x >= CUTOFF else 0
        slope = SLOPE_RIGHT if treated else SLOPE_LEFT
        y0 = INTERCEPT + slope * x
        y = y0 + (TAU if treated else 0.0)
        rows.append({
            "x": round(x, 4),
            "treat": treated,
            "y0": round(y0, 4),
            "y": round(y, 4),
        })
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["x", "treat", "y0", "y"])
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def true_tau(rows: list[dict]) -> float:
    """True jump recomputed from the shipped y0 counterfactual at the cutoff.

    The right limit of the untreated mean function at the cutoff is the y0 of the
    treated unit sitting exactly on the cutoff; the left limit is the linear
    extrapolation of the just-below points. Both reduce to INTERCEPT here, so the
    jump equals mean(y - y0) over treated rows, which is TAU by construction.
    """
    treated = [r for r in rows if r["treat"] in ("1", "1.0")]
    return sum(_num(r, "y") - _num(r, "y0") for r in treated) / len(treated)


def naive_jump(rows: list[dict]) -> float:
    """Across-cutoff difference in mean outcomes, ignoring the running variable."""
    above = [_num(r, "y") for r in rows if r["treat"] in ("1", "1.0")]
    below = [_num(r, "y") for r in rows if r["treat"] not in ("1", "1.0")]
    return sum(above) / len(above) - sum(below) / len(below)


def global_att(rows: list[dict]) -> float:
    """Global common-slope OLS: y ~ 1 + D + x. Biased under differing slopes."""
    design, outcome = [], []
    for r in rows:
        treated = 1.0 if r["treat"] in ("1", "1.0") else 0.0
        design.append([1.0, treated, _num(r, "x")])
        outcome.append(_num(r, "y"))
    return lalonde.ols(design, outcome)[1]  # coefficient on D


def _intercept_at_cutoff(rows: list[dict], side: str, bandwidth: float) -> float:
    """Local linear fit y ~ 1 + (x - cutoff) on one side within the bandwidth.

    Returns the intercept, i.e. the predicted outcome at the cutoff. Because each
    side is exactly linear, the fit is exact for any positive bandwidth.
    """
    design, outcome = [], []
    for r in rows:
        x = _num(r, "x")
        treated = r["treat"] in ("1", "1.0")
        on_side = treated if side == "right" else not treated
        if on_side and abs(x - CUTOFF) <= bandwidth:
            design.append([1.0, x - CUTOFF])
            outcome.append(_num(r, "y"))
    return lalonde.ols(design, outcome)[0]


def local_att(rows: list[dict], bandwidth: float = BANDWIDTH) -> float:
    """Local-linear RD estimate: difference of side-specific intercepts at the cutoff."""
    right = _intercept_at_cutoff(rows, "right", bandwidth)
    left = _intercept_at_cutoff(rows, "left", bandwidth)
    return right - left


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-rdd.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
    rows = load(data_path)
    print(f"  n={len(rows)} true_tau={true_tau(rows):.4f} "
          f"naive_jump={naive_jump(rows):.4f} global_att={global_att(rows):.4f} "
          f"local_att={local_att(rows):.4f}")
