#!/usr/bin/env python3
"""Pure-stdlib event-study (dynamic difference-in-differences) computations.

Deterministic, noiseless balanced panel: one treated cohort adopts at t0 with
GROWING dynamic effects, plus a never-treated control group, and parallel trends
hold by construction (the untreated potential outcome is additive in unit and
time effects). An event-study regression with unit and time fixed effects
recovers the dynamic path: post-period event coefficients equal the true dynamic
effects and pre-period (placebo) coefficients are zero. A naive treated-only
before/after comparison is biased by the common time trend. y0 ships as a column
the estimators never read so the checker can recompute the truth.
"""

from __future__ import annotations

import csv
from pathlib import Path

import lalonde  # sibling module in benchmark/lib

UNITS = 30
PERIODS = 8
T0 = 4                      # adoption period for the treated cohort
TREATED_UNITS = range(1, 16)  # units 1..15 treated; 16..30 never treated
# Dynamic effect by event time k = t - T0 (k >= 0). True post ATT = mean = 3.0.
TAU = {0: 1.0, 1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0}


def _unit_fe(unit: int) -> float:
    return round((unit % 5) * 1.5 - 3.0, 4)


def _time_fe(period: int) -> float:
    return round(0.6 * period, 4)


def _is_treated_unit(unit: int) -> bool:
    return unit in TREATED_UNITS


def _tau(unit: int, period: int) -> float:
    if not _is_treated_unit(unit) or period < T0:
        return 0.0
    return TAU.get(period - T0, 0.0)


def generate() -> list[dict]:
    rows: list[dict] = []
    for unit in range(1, UNITS + 1):
        for period in range(1, PERIODS + 1):
            post = 1 if _is_treated_unit(unit) and period >= T0 else 0
            y0 = _unit_fe(unit) + _time_fe(period)
            y = y0 + _tau(unit, period)
            rows.append({
                "unit": unit,
                "time": period,
                "treated_unit": 1 if _is_treated_unit(unit) else 0,
                "post": post,
                "y0": round(y0, 4),
                "y": round(y, 4),
            })
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["unit", "time", "treated_unit", "post", "y0", "y"]
        )
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def _is_treated(row: dict) -> bool:
    return round(_num(row, "treated_unit")) == 1


def true_att(rows: list[dict]) -> float:
    """True average post-adoption effect on the treated, from the unread y0."""
    diffs = [
        _num(r, "y") - _num(r, "y0")
        for r in rows
        if _is_treated(r) and int(_num(r, "time")) >= T0
    ]
    return sum(diffs) / len(diffs)


def _event_keys() -> list[int]:
    """Relative event times present for the treated cohort, dropping k=-1 baseline."""
    return [t - T0 for t in range(1, PERIODS + 1) if (t - T0) != -1]


def event_study_coefs(rows: list[dict]) -> dict[int, float]:
    """OLS with unit + time fixed effects and treated x relative-time dummies."""
    units = sorted({int(_num(r, "unit")) for r in rows})
    periods = sorted({int(_num(r, "time")) for r in rows})
    unit_cols, period_cols = units[1:], periods[1:]
    keys = _event_keys()

    design, outcome = [], []
    for r in rows:
        unit, period = int(_num(r, "unit")), int(_num(r, "time"))
        x = [1.0]
        x += [1.0 if unit == v else 0.0 for v in unit_cols]
        x += [1.0 if period == v else 0.0 for v in period_cols]
        for k in keys:
            x.append(1.0 if (_is_treated(r) and (period - T0) == k) else 0.0)
        design.append(x)
        outcome.append(_num(r, "y"))
    beta = lalonde.ols(design, outcome)
    event_betas = beta[-len(keys):]
    return {k: event_betas[i] for i, k in enumerate(keys)}


def es_att(rows: list[dict]) -> float:
    """Average of the estimated post-period (k>=0) event coefficients."""
    coefs = event_study_coefs(rows)
    post = [v for k, v in coefs.items() if k >= 0]
    return sum(post) / len(post)


def es_pre_max(rows: list[dict]) -> float:
    """Largest absolute pre-period (k<0) event coefficient (placebo; ~0)."""
    coefs = event_study_coefs(rows)
    pre = [abs(v) for k, v in coefs.items() if k < 0]
    return max(pre) if pre else 0.0


def naive_before_after(rows: list[dict]) -> float:
    """Treated-only post-minus-pre mean (biased by the common time trend)."""
    post = [_num(r, "y") for r in rows if _is_treated(r) and int(_num(r, "time")) >= T0]
    pre = [_num(r, "y") for r in rows if _is_treated(r) and int(_num(r, "time")) < T0]
    return sum(post) / len(post) - sum(pre) / len(pre)


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-event-study.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
