#!/usr/bin/env python3
"""Pure-stdlib Card (1995) returns-to-schooling computations: OLS, 2SLS with the
near-4-year-college instrument, and the first-stage F. No numpy/statsmodels.

Reuses the Gauss-Jordan OLS solver in lalonde.py and adds a matrix inverse so we
can report standard errors (needed for the first-stage F).
"""

from __future__ import annotations

import csv
from pathlib import Path

import lalonde  # sibling module in benchmark/lib

# Standard Card wage equation controls available in the dataset.
CONTROLS = ["exper", "expersq", "black", "south", "smsa", "smsa66",
            "reg662", "reg663", "reg664", "reg665", "reg666", "reg667", "reg668", "reg669"]
INSTRUMENT = "nearc4"
ENDOG = "educ"
OUTCOME = "lwage"


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("lwage") not in (None, "", "NA")]


def _col(rows, k):
    return [float(r[k]) for r in rows]


def _design(rows, regressors):
    return [[1.0] + [float(r[k]) for k in regressors] for r in rows]


def _invert(mat):
    """Inverse of a square matrix via Gauss-Jordan."""
    n = len(mat)
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(mat)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[piv] = a[piv], a[c]
        d = a[c][c]
        if d == 0:
            raise ValueError("singular matrix")
        a[c] = [v / d for v in a[c]]
        for r in range(n):
            if r != c:
                f = a[r][c]
                a[r] = [a[r][j] - f * a[c][j] for j in range(2 * n)]
    return [row[n:] for row in a]


def _ols_with_se(X, y):
    n, p = len(X), len(X[0])
    xtx = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(p)] for a in range(p)]
    xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(p)]
    inv = _invert(xtx)
    beta = [sum(inv[a][b] * xty[b] for b in range(p)) for a in range(p)]
    resid = [y[i] - sum(X[i][j] * beta[j] for j in range(p)) for i in range(n)]
    sigma2 = sum(e * e for e in resid) / (n - p)
    se = [(sigma2 * inv[j][j]) ** 0.5 for j in range(p)]
    return beta, se


def ols_return(rows) -> float:
    """OLS coefficient on educ (return to schooling)."""
    X = _design(rows, [ENDOG] + CONTROLS)
    beta = lalonde.ols(X, _col(rows, OUTCOME))
    return beta[1]  # index 0 is intercept, 1 is educ


def first_stage(rows) -> tuple[float, float]:
    """Return (coef on instrument, first-stage F for the single instrument)."""
    X = _design(rows, [INSTRUMENT] + CONTROLS)
    beta, se = _ols_with_se(X, _col(rows, ENDOG))
    coef, se_z = beta[1], se[1]
    f = (coef / se_z) ** 2  # single-instrument first-stage F = t^2
    return coef, f


def iv_return(rows) -> float:
    """2SLS coefficient on educ instrumented by nearc4 (manual two-stage)."""
    # Stage 1: educ ~ instrument + controls -> fitted educ.
    X1 = _design(rows, [INSTRUMENT] + CONTROLS)
    b1 = lalonde.ols(X1, _col(rows, ENDOG))
    educ_hat = [sum(X1[i][j] * b1[j] for j in range(len(b1))) for i in range(len(rows))]
    # Stage 2: lwage ~ educ_hat + controls.
    X2 = [[1.0, educ_hat[i]] + [float(rows[i][k]) for k in CONTROLS] for i in range(len(rows))]
    b2 = lalonde.ols(X2, _col(rows, OUTCOME))
    return b2[1]
