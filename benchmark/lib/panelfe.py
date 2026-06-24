#!/usr/bin/env python3
"""Pure-stdlib panel fixed-effects computations.

Deterministic, noiseless balanced panel whose untreated potential outcome is
additive in unit and time effects. Treatment turns on and off WITHIN units
(not a one-shot adoption) and is correlated with the unit effects, so a pooled
OLS that ignores unit heterogeneity is biased, while a two-way fixed-effects
estimator recovers the true effect. The untreated potential outcome y0 ships as
a column the estimators never read, so the checker can recompute the true effect.
"""

from __future__ import annotations

import csv
from pathlib import Path

import lalonde  # sibling module in benchmark/lib

UNITS = 40
PERIODS = 6
BETA = 2.0  # true within-unit treatment effect


def _unit_fe(unit: int) -> float:
    # Units 1..20 are high-type and are the ones that get treated; 21..40 low-type
    # and never treated -> treatment is correlated with the unit effect (selection).
    base = 4.0 if unit <= 20 else -3.0
    return round(base + (unit % 3), 4)


def _time_fe(period: int) -> float:
    return round(0.5 * period, 4)


def _treated(unit: int, period: int) -> int:
    # On/off within unit: high-type units are treated in even periods only.
    return 1 if unit <= 20 and period % 2 == 0 else 0


def generate() -> list[dict]:
    rows: list[dict] = []
    for unit in range(1, UNITS + 1):
        for period in range(1, PERIODS + 1):
            d = _treated(unit, period)
            y0 = _unit_fe(unit) + _time_fe(period)
            y = y0 + (BETA if d else 0.0)
            rows.append({
                "unit": unit,
                "time": period,
                "treat": d,
                "y0": round(y0, 4),
                "y": round(y, 4),
            })
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["unit", "time", "treat", "y0", "y"])
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def true_att(rows: list[dict]) -> float:
    """Average treatment effect on the treated, from the unread y0 column."""
    diffs = [_num(r, "y") - _num(r, "y0") for r in rows if round(_num(r, "treat")) == 1]
    return sum(diffs) / len(diffs)


def pooled_att(rows: list[dict]) -> float:
    """OLS of y on treat with NO fixed effects (biased: ignores unit selection)."""
    X = [[1.0, _num(r, "treat")] for r in rows]
    y = [_num(r, "y") for r in rows]
    return lalonde.ols(X, y)[1]


def twoway_fe_att(rows: list[dict]) -> float:
    """Two-way (unit + time) fixed-effects coefficient on treat (recovers BETA)."""
    units = sorted({int(_num(r, "unit")) for r in rows})
    periods = sorted({int(_num(r, "time")) for r in rows})
    unit_cols, period_cols = units[1:], periods[1:]
    design, outcome = [], []
    for r in rows:
        unit, period = int(_num(r, "unit")), int(_num(r, "time"))
        x = [1.0]
        x += [1.0 if unit == v else 0.0 for v in unit_cols]
        x += [1.0 if period == v else 0.0 for v in period_cols]
        x.append(_num(r, "treat"))
        design.append(x)
        outcome.append(_num(r, "y"))
    return lalonde.ols(design, outcome)[-1]


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-panel-fe.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
