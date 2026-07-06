#!/usr/bin/env python3
"""Oster-delta demo: coefficient stability is not evidence against OVB.

A runnable companion to docs/methods-reference.md section 6 (the Oster-delta /
bounding row) and the aer-robustness skill. It makes the Oster (2019) point that
"the coefficient barely moved when I added controls, so omitted-variable bias is
small" is not a valid argument on its own: coefficient movement is only
informative when scaled by how much the R-squared moved. Weak controls that
barely raise the R-squared cannot certify robustness no matter how stable the
coefficient looks.

The script uses a KNOWN data-generating process in which the true effect is
ZERO and an UNOBSERVED confounder W is exactly as related to the treatment and
the outcome as the OBSERVED control X (proportional selection with delta = 1).
The observed-controls estimate stays biased away from zero; Oster's R-squared-
scaled adjustment, assuming unobservables are as important as observables
(delta = 1) with the true R-squared, recovers the truth.

This is also the demo's internal correctness check: Oster's identity is
constructed so that beta*(delta = delta_true, R_max = R_full) equals the
full-controls coefficient. The script asserts that the adjustment recovers the
true zero and that the implied delta-for-zero is about 1, and exits non-zero if
either fails -- so it doubles as a regression test of the bounding formula.

Run:  python3 oster_ovb_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: Oster (2019), "Unobservable selection and coefficient stability."
See ../../docs/methods-reference.md section 6 for the per-stack tooling (psacalc,
robomit) and ../../skills/aer-identification/SKILL.md for the design context.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _aer_numeric_check import numeric_check  # noqa: E402

SEED = 20260101
N = 2000                 # observations
A_LOAD = 1.0             # equal loading of X and W into the treatment
C_LOAD = 1.0             # equal effect of X and W on the outcome (=> delta=1)
SIGMA_D = 1.0            # treatment noise
SIGMA_Y = 1.0            # outcome noise
BETA_TRUE = 0.0          # the truth: no treatment effect (the "effect" is OVB)
REPS = 400               # Monte Carlo panels
OUT = Path(__file__).resolve().parent / "output"


def ols_beta_r2(y: np.ndarray, cols: list[np.ndarray]) -> tuple[float, float]:
    """OLS of y on [1, *cols]; return the coefficient on cols[0] and the R^2."""
    Z = np.column_stack([np.ones_like(y)] + cols)
    coef, *_ = np.linalg.lstsq(Z, y, rcond=None)
    resid = y - Z @ coef
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float(resid @ resid) / sst
    return float(coef[1]), r2          # coef[0] is the intercept


def oster_beta_star(b_short: float, b_med: float, r_short: float,
                    r_med: float, r_max: float, delta: float = 1.0) -> float:
    """Oster (2019) bias-adjusted coefficient beta*(delta, R_max)."""
    return b_med - delta * (b_short - b_med) * (r_max - r_med) / (r_med - r_short)


def oster_delta_for_zero(b_short: float, b_med: float, r_short: float,
                         r_med: float, r_max: float) -> float:
    """The delta that drives the adjusted coefficient to zero."""
    return b_med * (r_med - r_short) / ((b_short - b_med) * (r_max - r_med))


def _panel(rng: np.random.Generator) -> tuple[np.ndarray, ...]:
    X = rng.normal(size=N)
    W = rng.normal(size=N)                       # unobserved confounder
    D = A_LOAD * (X + W) + rng.normal(scale=SIGMA_D, size=N)
    Y = BETA_TRUE * D + C_LOAD * (X + W) + rng.normal(scale=SIGMA_Y, size=N)
    return D, X, W, Y


def run_montecarlo(rng: np.random.Generator) -> dict:
    keys = ["short", "med", "full", "oster", "delta0"]
    acc = {k: [] for k in keys}
    for _ in range(REPS):
        D, X, W, Y = _panel(rng)
        b_short, r_short = ols_beta_r2(Y, [D])
        b_med, r_med = ols_beta_r2(Y, [D, X])
        b_full, r_full = ols_beta_r2(Y, [D, X, W])
        b_oster = oster_beta_star(b_short, b_med, r_short, r_med, r_full, 1.0)
        d0 = oster_delta_for_zero(b_short, b_med, r_short, r_med, r_full)
        for k, v in zip(keys, [b_short, b_med, b_full, b_oster, d0]):
            acc[k].append(v)
    return {k: float(np.mean(v)) for k, v in acc.items()}


def make_figure(m: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    labels = ["short\n(no controls)", "controlled\n(observed X)",
              "Oster beta*\n(delta=1, R_full)", "full\n(infeasible: +W)"]
    vals = [m["short"], m["med"], m["oster"], m["full"]]
    colors = ["firebrick", "darkorange", "black", "steelblue"]
    ax.bar(labels, vals, color=colors)
    ax.axhline(BETA_TRUE, linestyle="--", color="grey",
               label=f"true effect = {BETA_TRUE:.0f}")
    ax.set_ylabel("Estimated treatment effect")
    ax.set_title("Oster: controlled estimate stays biased; R^2-scaled adjustment recovers truth")
    ax.legend(frameon=False)
    fig.tight_layout()
    pdf = OUT / "oster_ovb.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "oster_ovb.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    m = run_montecarlo(rng)
    pct_move = abs(m["med"] - m["short"]) / abs(m["short"]) * 100

    print("=" * 70)
    print("Oster delta: coefficient stability is not evidence against OVB")
    print(f"  N={N}  reps={REPS}  true effect={BETA_TRUE:.0f}  delta_true=1  seed={SEED}")
    print("=" * 70)
    print(f"  short  (no controls)        beta = {m['short']:.3f}")
    print(f"  controlled (observed X)     beta = {m['med']:.3f}"
          f"   (still far from the truth)")
    print(f"  full   (infeasible: +W)     beta = {m['full']:.3f}   (the truth)")
    print(f"  Oster  beta*(delta=1,R_full) = {m['oster']:.3f}"
          f"   (recovers the truth)")
    print()
    print(f"  adding observed controls moved beta by {pct_move:.0f}% -- a naive")
    print(f"  reader might call that 'fairly stable', yet the effect is entirely")
    print(f"  OVB. Oster's delta-for-zero = {m['delta0']:.2f}: selection on")
    print(f"  unobservables only as strong as on observables already kills it.")

    pdf = make_figure(m)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known target and emits a
    # NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("full model recovers true zero", m["full"], target=BETA_TRUE, tol=0.03)
    numeric_check("observed-controls estimate stays biased", m["med"], lo=0.15)
    numeric_check("Oster beta*(delta=1, R_max=R_full) recovers zero",
                  m["oster"], target=BETA_TRUE, tol=0.03)
    numeric_check("delta-for-zero ~ 1 under proportional selection",
                  m["delta0"], lo=0.85, hi=1.15)
    print("\nAll assertions passed: the controlled estimate stays biased, while "
          "Oster's\nR^2-scaled adjustment (delta=1) recovers the truth -- "
          "stability alone proves nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
