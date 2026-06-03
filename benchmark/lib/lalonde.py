#!/usr/bin/env python3
"""Pure-stdlib LaLonde computations shared by the reference pipeline and checker.

No numpy / pandas / statsmodels: the benchmark must run in CI with only the
standard library. The OLS solver is a small Gaussian elimination on the normal
equations, which is plenty for a 614x10 design matrix.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

COVARIATES = ["age", "educ", "black", "hispan", "married", "nodegree", "re74", "re75"]


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        # Derive race dummies used as covariates.
        r["black"] = "1" if r.get("race") == "black" else "0"
        r["hispan"] = "1" if r.get("race") == "hispan" else "0"
    return rows


def _num(r: dict, k: str) -> float:
    return float(r[k])


def _mean(group: list[dict], k: str) -> float:
    return sum(_num(r, k) for r in group) / len(group)


def _sd(group: list[dict], k: str) -> float:
    m = _mean(group, k)
    return math.sqrt(sum((_num(r, k) - m) ** 2 for r in group) / (len(group) - 1))


def split(rows: list[dict], treatment: str) -> tuple[list[dict], list[dict]]:
    treated = [r for r in rows if r[treatment] in ("1", "1.0", "True", "true")]
    control = [r for r in rows if r not in treated]
    return treated, control


def naive_att(rows: list[dict], treatment: str, outcome: str) -> float:
    t, c = split(rows, treatment)
    return _mean(t, outcome) - _mean(c, outcome)


def smd_table(rows: list[dict], treatment: str) -> dict[str, float]:
    t, c = split(rows, treatment)
    out: dict[str, float] = {}
    for k in COVARIATES:
        mt, mc = _mean(t, k), _mean(c, k)
        st, sc = _sd(t, k), _sd(c, k)
        pooled = math.sqrt((st ** 2 + sc ** 2) / 2)
        out[k] = (mt - mc) / pooled if pooled else 0.0
    return out


def ols(X: list[list[float]], y: list[float]) -> list[float]:
    """Solve (X'X) b = X'y by Gauss-Jordan with partial pivoting."""
    n, p = len(X), len(X[0])
    xtx = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(p)] for a in range(p)]
    xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(p)]
    aug = [xtx[i][:] + [xty[i]] for i in range(p)]
    for c in range(p):
        piv = max(range(c, p), key=lambda r: abs(aug[r][c]))
        aug[c], aug[piv] = aug[piv], aug[c]
        d = aug[c][c]
        if d == 0:
            raise ValueError("singular design matrix")
        aug[c] = [v / d for v in aug[c]]
        for r in range(p):
            if r != c:
                f = aug[r][c]
                aug[r] = [aug[r][j] - f * aug[c][j] for j in range(p + 1)]
    return [aug[i][p] for i in range(p)]


def adjusted_att(rows: list[dict], treatment: str, outcome: str) -> float:
    """Regression-adjusted ATT = treatment coefficient with full controls."""
    X, y = [], []
    for r in rows:
        X.append([1.0, _num(r, treatment)] + [_num(r, k) for k in COVARIATES])
        y.append(_num(r, outcome))
    beta = ols(X, y)
    return beta[1]
