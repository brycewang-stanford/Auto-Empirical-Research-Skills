#!/usr/bin/env python3
"""Pure-stdlib staggered difference-in-differences computations.

The simulated panel is deterministic and noiseless. Its untreated potential
outcome is additive in unit and time effects, while treatment effects are
cohort-heterogeneous and dynamic. This makes naive TWFE biased and lets the
benchmark check whether a group-time estimator with not-yet-treated controls
recovers the true ATT.
"""

from __future__ import annotations

import csv
from pathlib import Path

import lalonde  # sibling module in benchmark/lib

UNITS = 60
PERIODS = 10
COHORTS = {4: range(1, 21), 7: range(21, 41)}
DELTA = {4: 1.0, 7: 0.4}


def _unit_fe(unit: int) -> float:
    return round((unit % 7) * 1.3 - 2.0, 4)


def _time_fe(period: int) -> float:
    return round(0.5 * period, 4)


def _cohort_of(unit: int) -> int:
    for cohort, units in COHORTS.items():
        if unit in units:
            return cohort
    return 0


def _tau(cohort: int, period: int) -> float:
    if cohort == 0 or period < cohort:
        return 0.0
    return DELTA[cohort] * (period - cohort + 1)


def generate() -> list[dict]:
    rows: list[dict] = []
    for unit in range(1, UNITS + 1):
        cohort = _cohort_of(unit)
        for period in range(1, PERIODS + 1):
            treated = 1 if cohort != 0 and period >= cohort else 0
            y0 = _unit_fe(unit) + _time_fe(period)
            y = y0 + (_tau(cohort, period) if treated else 0.0)
            rows.append({
                "unit": unit,
                "time": period,
                "cohort": cohort,
                "treat": treated,
                "y0": round(y0, 4),
                "y": round(y, 4),
            })
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["unit", "time", "cohort", "treat", "y0", "y"])
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def true_att(rows: list[dict]) -> float:
    diffs = [_num(row, "y") - _num(row, "y0") for row in rows if row["treat"] in ("1", "1.0")]
    return sum(diffs) / len(diffs)


def twfe_att(rows: list[dict]) -> float:
    units = sorted({int(_num(row, "unit")) for row in rows})
    periods = sorted({int(_num(row, "time")) for row in rows})
    unit_cols = units[1:]
    period_cols = periods[1:]

    design, outcome = [], []
    for row in rows:
        unit, period = int(_num(row, "unit")), int(_num(row, "time"))
        x = [1.0]
        x += [1.0 if unit == value else 0.0 for value in unit_cols]
        x += [1.0 if period == value else 0.0 for value in period_cols]
        x.append(_num(row, "treat"))
        design.append(x)
        outcome.append(_num(row, "y"))
    return lalonde.ols(design, outcome)[-1]


def _mean_y(rows: list[dict], cohort: int | None, period: int) -> float | None:
    vals = [
        _num(row, "y")
        for row in rows
        if int(_num(row, "time")) == period
        and (cohort is None or int(_num(row, "cohort")) == cohort)
    ]
    return sum(vals) / len(vals) if vals else None


def _pooled_ctrl_mean(rows: list[dict], ctrl_cohorts: set[int], period: int) -> float | None:
    vals = [
        _num(row, "y")
        for row in rows
        if int(_num(row, "time")) == period and int(_num(row, "cohort")) in ctrl_cohorts
    ]
    return sum(vals) / len(vals) if vals else None


def group_time_att(rows: list[dict]) -> dict[tuple[int, int], float]:
    cohorts = sorted({int(_num(row, "cohort")) for row in rows} - {0})
    last_period = max(int(_num(row, "time")) for row in rows)
    out: dict[tuple[int, int], float] = {}
    for cohort in cohorts:
        base = cohort - 1
        for period in range(cohort, last_period + 1):
            ctrl_cohorts = {
                int(_num(row, "cohort"))
                for row in rows
                if int(_num(row, "cohort")) == 0 or int(_num(row, "cohort")) > period
            }
            yg_t = _mean_y(rows, cohort, period)
            yg_b = _mean_y(rows, cohort, base)
            yc_t = _pooled_ctrl_mean(rows, ctrl_cohorts, period)
            yc_b = _pooled_ctrl_mean(rows, ctrl_cohorts, base)
            if None in (yg_t, yg_b, yc_t, yc_b):
                continue
            out[(cohort, period)] = (yg_t - yg_b) - (yc_t - yc_b)
    return out


def cs_att(rows: list[dict]) -> float:
    cell_atts = group_time_att(rows)
    cohort_size: dict[int, set[int]] = {}
    for row in rows:
        cohort = int(_num(row, "cohort"))
        if cohort != 0:
            cohort_size.setdefault(cohort, set()).add(int(_num(row, "unit")))
    numerator = denominator = 0.0
    for (cohort, _period), att in cell_atts.items():
        weight = len(cohort_size[cohort])
        numerator += att * weight
        denominator += weight
    return numerator / denominator if denominator else 0.0


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-staggered-did.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
