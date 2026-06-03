#!/usr/bin/env python3
"""Pure-stdlib good-vs-bad-control computations (post-treatment / mediator bias).

The simulated cross-section is deterministic and noiseless. Treatment ``d`` is
assigned orthogonally to the pre-treatment covariate ``x`` (so there is NO
omitted-variable confounding), and a mediator ``m`` sits on the causal path
``d -> m -> y``. Because the data is exactly linear and noiseless, the true total
effect of ``d`` on ``y`` is known by construction and shipped as a pair of
potential-outcome columns (``y0``, ``y1``) the estimators never read.

The encoded trap is the "bad control" / post-treatment-bias lesson (Cinelli,
Forney & Pearl 2022, *A Crash Course in Good and Bad Controls*; Angrist &
Pischke, *Mostly Harmless Econometrics*, on bad controls): conditioning on a
descendant of the treatment (here the mediator ``m``) violates the back-door
criterion and biases the estimate away from the total effect toward the direct
effect. Controlling for the *pre-treatment* covariate ``x`` is harmless here,
which is the point: it is not "all post-treatment variables are bad" but
specifically that conditioning on a mediator changes the estimand.

Structural equations (noiseless):
    m = 1.0*d + 0.5*x + e            # mediator: caused by treatment and x
    y = 0.5*d + 2.0*m + 1.0*x        # outcome
=> total effect of d on y = 0.5 (direct) + 2.0 * 1.0 (through m) = 2.5
   direct effect of d on y = 0.5 (what y ~ d + x + m recovers)
"""

from __future__ import annotations

import csv
from pathlib import Path

import lalonde  # sibling module in benchmark/lib

N_UNITS = 120                  # multiple of lcm(2, 6, 5) = 30 so d _|_ (x, e) in-sample
DIRECT_EFFECT = 0.5            # d -> y direct
MEDIATOR_FROM_D = 1.0          # d -> m
MEDIATOR_FROM_X = 0.5          # x -> m
OUTCOME_FROM_M = 2.0           # m -> y
OUTCOME_FROM_X = 1.0           # x -> y
TOTAL_EFFECT = DIRECT_EFFECT + OUTCOME_FROM_M * MEDIATOR_FROM_D  # 2.5 (informational)


def _exog(i: int) -> float:
    # Centered exogenous component of the mediator, independent of d and x.
    return round(((i % 5) - 2) * 0.3, 4)


def generate() -> list[dict]:
    rows: list[dict] = []
    for i in range(N_UNITS):
        x = (i // 2) % 3            # pre-treatment covariate, orthogonal to d
        d = i % 2                  # treatment, alternating
        e = _exog(i)
        # Potential mediators / outcomes under each treatment status.
        m1 = MEDIATOR_FROM_D * 1 + MEDIATOR_FROM_X * x + e
        m0 = MEDIATOR_FROM_D * 0 + MEDIATOR_FROM_X * x + e
        y1 = DIRECT_EFFECT * 1 + OUTCOME_FROM_M * m1 + OUTCOME_FROM_X * x
        y0 = DIRECT_EFFECT * 0 + OUTCOME_FROM_M * m0 + OUTCOME_FROM_X * x
        m = m1 if d == 1 else m0
        y = y1 if d == 1 else y0
        rows.append({
            "x": x,
            "d": d,
            "m": round(m, 4),
            "y": round(y, 4),
            "y0": round(y0, 4),
            "y1": round(y1, 4),
        })
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["x", "d", "m", "y", "y0", "y1"])
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def true_total(rows: list[dict]) -> float:
    """True average total effect recomputed from the shipped potential outcomes."""
    diffs = [_num(r, "y1") - _num(r, "y0") for r in rows]
    return sum(diffs) / len(diffs)


def _effect(rows: list[dict], regressors: list[str]) -> float:
    """OLS coefficient on d for y ~ 1 + d + regressors."""
    design, outcome = [], []
    for r in rows:
        design.append([1.0, _num(r, "d")] + [_num(r, k) for k in regressors])
        outcome.append(_num(r, "y"))
    return lalonde.ols(design, outcome)[1]  # index 0 intercept, 1 is d


def naive_effect(rows: list[dict]) -> float:
    """y ~ d, no controls. Unbiased here because treatment is unconfounded."""
    return _effect(rows, [])


def good_control_effect(rows: list[dict]) -> float:
    """y ~ d + x, controlling for the pre-treatment covariate. Recovers the total effect."""
    return _effect(rows, ["x"])


def bad_control_effect(rows: list[dict]) -> float:
    """y ~ d + x + m, conditioning on the post-treatment mediator. Biased for the total effect."""
    return _effect(rows, ["x", "m"])


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-badcontrol.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
    rows = load(data_path)
    print(f"  n={len(rows)} true_total={true_total(rows):.4f} "
          f"naive={naive_effect(rows):.4f} good={good_control_effect(rows):.4f} "
          f"bad={bad_control_effect(rows):.4f}")
