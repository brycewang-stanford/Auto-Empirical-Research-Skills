#!/usr/bin/env python3
"""Pure-stdlib conjugate Bayesian (Normal-Normal) computations.

Deterministic data symmetric around a known mean, with a known observation
variance. The conjugate posterior mean is a closed-form weighted average of the
prior mean and the data mean. A weakly-informative prior recovers the data mean
(the truth); an overconfident, miscalibrated prior drags the posterior far from
it -- the prior-sensitivity lesson. No randomness; everything is closed form.
"""

from __future__ import annotations

import csv
from pathlib import Path

N = 20
TRUE_MEAN = 2.0
SIGMA2 = 4.0  # assumed known observation variance
# Prior (mu0, tau0^2): weakly-informative recovers the data; strong+wrong biases.
WEAK_PRIOR = (0.0, 10000.0)
STRONG_WRONG_PRIOR = (10.0, 0.25)


def generate() -> list[dict]:
    rows: list[dict] = []
    for i in range(1, N + 1):
        # Symmetric offsets around TRUE_MEAN so the sample mean is exactly TRUE_MEAN.
        y = TRUE_MEAN + (i - (N + 1) / 2) * 0.2
        rows.append({"id": i, "y": round(y, 6)})
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["id", "y"])
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _ybar(rows: list[dict]) -> float:
    ys = [float(r["y"]) for r in rows]
    return sum(ys) / len(ys)


def data_mean(rows: list[dict]) -> float:
    """Sample mean == the true mean by construction (the recovery target)."""
    return _ybar(rows)


def posterior_mean(rows: list[dict], prior: tuple[float, float]) -> float:
    """Conjugate Normal-Normal posterior mean for a known-variance sample."""
    mu0, tau02 = prior
    n = len(rows)
    ybar = _ybar(rows)
    num = mu0 / tau02 + n * ybar / SIGMA2
    den = 1.0 / tau02 + n / SIGMA2
    return num / den


def posterior_weak(rows: list[dict]) -> float:
    return posterior_mean(rows, WEAK_PRIOR)


def posterior_strong(rows: list[dict]) -> float:
    return posterior_mean(rows, STRONG_WRONG_PRIOR)


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-bayesian.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
