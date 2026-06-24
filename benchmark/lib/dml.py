#!/usr/bin/env python3
"""Pure-stdlib double/debiased machine learning (partialling-out) computations.

Deterministic, noiseless data: the outcome is exactly linear in the treatment and
a set of controls, and the treatment is correlated with those controls. A naive
OLS of outcome on treatment alone is biased by the omitted controls, while a
cross-fitted partialling-out estimator (residualize Y and D on the controls using
out-of-fold predictions, then regress the residuals) recovers the true effect.

With linear nuisance and no noise the cross-fitted estimate equals the
fully-controlled coefficient by construction, so the benchmark exercises the
cross-fitting machinery and the omitted-control bias rather than regularization
bias (which the eval scenario covers). Reuses the Gauss-Jordan OLS in lalonde.py.
"""

from __future__ import annotations

import csv
from pathlib import Path

import lalonde  # sibling module in benchmark/lib

N = 120
FOLDS = 4
THETA = 1.5  # true treatment effect
CONTROLS = ["x1", "x2", "x3", "x4"]


def _x(i: int) -> dict:
    return {
        "x1": float(i % 5),
        "x2": float((i * 3) % 7),
        "x3": float((i % 4) - 1.5),
        "x4": float((i * 2) % 3),
    }


def _m(x: dict) -> float:
    """Treatment mean function (shares controls with the outcome, same signs)."""
    return 0.6 * x["x1"] + 0.5 * x["x2"] + 0.4 * x["x3"]


def _g(x: dict) -> float:
    """Outcome control function (aligned with _m so omitting it biases upward)."""
    return 1.2 * x["x1"] + 1.0 * x["x2"] + 0.8 * x["x3"] + 0.4 * x["x4"]


def generate() -> list[dict]:
    rows: list[dict] = []
    for i in range(1, N + 1):
        x = _x(i)
        v = ((i % 9) - 4) * 0.12  # small treatment component independent of the controls
        d = _m(x) + v
        y = THETA * d + _g(x)
        row = {"id": i, "d": round(d, 6), "y": round(y, 6)}
        row.update({k: x[k] for k in CONTROLS})
        rows.append(row)
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["id", "d", "y"] + CONTROLS
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def _design(rows: list[dict]) -> list[list[float]]:
    return [[1.0] + [_num(r, k) for k in CONTROLS] for r in rows]


def _predict(beta: list[float], r: dict) -> float:
    x = [1.0] + [_num(r, k) for k in CONTROLS]
    return sum(beta[j] * x[j] for j in range(len(beta)))


def true_theta(rows: list[dict]) -> float:
    """Fully-controlled OLS coefficient on d (recovers THETA by construction)."""
    X = [[1.0, _num(r, "d")] + [_num(r, k) for k in CONTROLS] for r in rows]
    y = [_num(r, "y") for r in rows]
    return lalonde.ols(X, y)[1]


def naive_theta(rows: list[dict]) -> float:
    """OLS of y on d with no controls (biased by the omitted controls)."""
    X = [[1.0, _num(r, "d")] for r in rows]
    y = [_num(r, "y") for r in rows]
    return lalonde.ols(X, y)[1]


def dml_theta(rows: list[dict]) -> float:
    """Cross-fitted partialling-out estimate of the treatment effect."""
    n = len(rows)
    folds = [[rows[i] for i in range(n) if i % FOLDS == f] for f in range(FOLDS)]
    num = den = 0.0
    for f in range(FOLDS):
        test = folds[f]
        train = [r for g in range(FOLDS) if g != f for r in folds[g]]
        # Out-of-fold linear nuisance models for E[Y|X] and E[D|X].
        beta_y = lalonde.ols(_design(train), [_num(r, "y") for r in train])
        beta_d = lalonde.ols(_design(train), [_num(r, "d") for r in train])
        for r in test:
            ry = _num(r, "y") - _predict(beta_y, r)
            rd = _num(r, "d") - _predict(beta_d, r)
            num += rd * ry
            den += rd * rd
    return num / den


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-dml.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
