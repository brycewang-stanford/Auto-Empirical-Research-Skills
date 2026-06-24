#!/usr/bin/env python3
"""Pure-stdlib synthetic-control computations.

Deterministic, noiseless panel: one treated unit and three donor units over eight
periods (four pre, four post). The treated unit's untreated potential outcome is,
by construction, an exact convex combination of the donors (0.5, 0.3, 0.2), so a
synthetic control that fits donor weights on the pre-period recovers that
combination and the post-period gap equals the true effect. The untreated
potential outcome ships as a column the estimators never read. A naive
equal-weight donor average does not match the pre-period and is biased.

Weights are fit by a coarse grid search over the simplex (step 0.01) minimizing
pre-period squared error -- enough for three donors, no optimizer dependency.
"""

from __future__ import annotations

import csv
from pathlib import Path

T0 = 5  # first post-treatment period (periods 1..4 pre, 5..8 post)
PERIODS = 8
TAU = 3.0  # true post-treatment effect
TRUE_W = (0.5, 0.3, 0.2)  # true donor weights (A, B, C)

DONOR_A = [10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0]
DONOR_B = [20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0]
DONOR_C = [5.0, 8.0, 6.0, 9.0, 7.0, 10.0, 8.0, 11.0]


def generate() -> list[dict]:
    rows: list[dict] = []
    for t in range(1, PERIODS + 1):
        a, b, c = DONOR_A[t - 1], DONOR_B[t - 1], DONOR_C[t - 1]
        y0 = TRUE_W[0] * a + TRUE_W[1] * b + TRUE_W[2] * c
        post = 1 if t >= T0 else 0
        y = y0 + (TAU if post else 0.0)
        rows.append({
            "time": t,
            "post": post,
            "treated_y": round(y, 6),
            "donor_a": a,
            "donor_b": b,
            "donor_c": c,
            "treated_y0": round(y0, 6),  # latent; estimators never read this
        })
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["time", "post", "treated_y", "donor_a", "donor_b", "donor_c", "treated_y0"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def _is_post(row: dict) -> bool:
    return round(_num(row, "post")) == 1


def true_effect(rows: list[dict]) -> float:
    """Mean post-period (treated_y - treated_y0), from the unread latent column."""
    diffs = [_num(r, "treated_y") - _num(r, "treated_y0") for r in rows if _is_post(r)]
    return sum(diffs) / len(diffs)


def fit_weights(rows: list[dict]) -> tuple[float, float, float]:
    """Grid search over the simplex (step 0.01) minimizing pre-period SSE."""
    pre = [r for r in rows if not _is_post(r)]
    best_w, best_sse = (1.0, 0.0, 0.0), None
    for ia in range(0, 101):
        for ib in range(0, 101 - ia):
            wa, wb = ia / 100.0, ib / 100.0
            wc = 1.0 - wa - wb
            sse = 0.0
            for r in pre:
                synth = wa * _num(r, "donor_a") + wb * _num(r, "donor_b") + wc * _num(r, "donor_c")
                resid = _num(r, "treated_y") - synth
                sse += resid * resid
            if best_sse is None or sse < best_sse:
                best_sse, best_w = sse, (wa, wb, wc)
    return best_w


def sc_effect(rows: list[dict]) -> float:
    """Synthetic-control post gap using donor weights fit on the pre-period."""
    wa, wb, wc = fit_weights(rows)
    diffs = []
    for r in rows:
        if _is_post(r):
            synth = wa * _num(r, "donor_a") + wb * _num(r, "donor_b") + wc * _num(r, "donor_c")
            diffs.append(_num(r, "treated_y") - synth)
    return sum(diffs) / len(diffs)


def naive_effect(rows: list[dict]) -> float:
    """Equal-weight donor average post gap (ignores pre-period fit; biased)."""
    diffs = []
    for r in rows:
        if _is_post(r):
            synth = (_num(r, "donor_a") + _num(r, "donor_b") + _num(r, "donor_c")) / 3.0
            diffs.append(_num(r, "treated_y") - synth)
    return sum(diffs) / len(diffs)


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-synth.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
