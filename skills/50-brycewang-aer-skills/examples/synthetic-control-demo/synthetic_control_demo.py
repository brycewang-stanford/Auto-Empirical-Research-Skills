#!/usr/bin/env python3
"""Synthetic-control demo: why placebo/permutation inference, not visual fit.

A runnable companion to docs/methods-reference.md section 5 ("Synthetic
control") and the aer-identification skill. It makes one point that the
methods reference and the skill both insist on: a synthetic control that
tracks the treated unit beautifully in the pre-period is *not* evidence of
an effect. The inference comes from the **placebo-in-space permutation
distribution** (Abadie-Diamond-Hainmueller 2010), summarized by the
post/pre RMSPE ratio, not from the eyeball fit.

The script demonstrates this three ways, with a KNOWN data-generating
process (a linear factor model in which a convex combination of donors can
reproduce the treated unit):

  1. POWER. With a real post-treatment effect, the treated unit's post/pre
     RMSPE ratio sits in the extreme tail of the placebo distribution, so
     the permutation p-value is small.
  2. SIZE. With NO effect, a Monte Carlo over many panels shows the
     permutation test rejects a true null at about its nominal rate -- the
     inferential guarantee that "the synthetic unit tracks well" cannot
     give you.
  3. FIT IS NOT INFERENCE. Placebo (never-treated) donors routinely achieve
     pre-period fit as tight as the treated unit's. Excellent pre-fit is a
     precondition for SCM, never a test statistic.

The script asserts the power and size results and exits non-zero if the
claim fails to reproduce, so it doubles as a regression test of the skill
stack's synthetic-control advice.

Run:  python3 synthetic_control_demo.py
Deps: numpy, pandas, scipy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References (keys in ../../references.bib): abadie_diamond_hainmueller_2010,
abadie_gardeazabal_2003, abadie_2021.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 20260101
N_DONORS = 30            # size of the donor pool
T = 30                   # total periods
T0 = 20                  # last pre-treatment period (20 pre, 10 post)
K = 3                    # number of common factors
SIGMA = 0.30             # idiosyncratic noise
DELTA = 1.50             # true post-treatment effect (power scenario)
SIZE_REPS = 150          # Monte Carlo reps for the size study
SIZE_N_DONORS = 24       # smaller pool keeps the size study fast
SIZE_T = 24
SIZE_T0 = 16
ALPHA = 0.10             # nominal level for the size study
OUT = Path(__file__).resolve().parent / "output"


def fit_weights(y_pre: np.ndarray, X_pre: np.ndarray) -> np.ndarray:
    """Abadie synthetic-control weights on the unit simplex.

    Minimize ||y_pre - X_pre @ w||^2 subject to w >= 0 and sum(w) = 1 --
    the constraint set that forces the synthetic unit to be a weighted
    average (no extrapolation) of the donors.
    """
    n = X_pre.shape[1]

    def obj(w):
        r = X_pre @ w - y_pre
        return float(r @ r)

    def grad(w):
        return 2.0 * X_pre.T @ (X_pre @ w - y_pre)

    w0 = np.full(n, 1.0 / n)
    res = minimize(
        obj, w0, jac=grad, method="SLSQP",
        bounds=[(0.0, 1.0)] * n,
        constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1.0,
                      "jac": lambda w: np.ones_like(w)}],
        options={"maxiter": 500, "ftol": 1e-10},
    )
    w = np.clip(res.x, 0.0, None)
    s = w.sum()
    return w / s if s > 0 else w0


def unit_gap(Y: np.ndarray, idx: int, t0: int) -> np.ndarray:
    """Treatment-minus-synthetic gap over all periods for unit `idx`.

    The synthetic control is built from every *other* unit, fitting weights
    on the pre-period only, then projected over the whole horizon.
    """
    donors = [j for j in range(Y.shape[0]) if j != idx]
    X = Y[donors].T                       # periods x donors
    w = fit_weights(Y[idx, :t0], X[:t0])
    synthetic = X @ w
    return Y[idx] - synthetic


def placebo_inference(Y: np.ndarray, treated: int, t0: int) -> dict:
    """Placebo-in-space permutation test (Abadie et al. 2010).

    Treat every unit in turn as if it were the treated unit, collect the
    post/pre RMSPE ratios, and rank the real treated unit against the
    placebo distribution. The one-sided permutation p-value is the share of
    units whose ratio is at least as large as the treated unit's.
    """
    n_units = Y.shape[0]
    ratios = np.empty(n_units)
    pre_fits = np.empty(n_units)
    gaps = {}
    for i in range(n_units):
        g = unit_gap(Y, i, t0)
        pre, _post, ratio = rmspe_ratio(g, t0)
        ratios[i] = ratio
        pre_fits[i] = pre
        gaps[i] = g
    treated_ratio = ratios[treated]
    p_value = float(np.mean(ratios >= treated_ratio))
    return {
        "ratios": ratios,
        "pre_fits": pre_fits,
        "gaps": gaps,
        "treated_ratio": float(treated_ratio),
        "treated_rank": int(np.sum(ratios >= treated_ratio)),
        "p_value": p_value,
        "n_units": n_units,
    }


def rmspe_ratio(gap: np.ndarray, t0: int) -> tuple[float, float, float]:
    """Pre-RMSPE, post-RMSPE, and Abadie's post/pre ratio for one unit."""
    pre = float(np.sqrt(np.mean(gap[:t0] ** 2)))
    post = float(np.sqrt(np.mean(gap[t0:] ** 2)))
    ratio = post / pre if pre > 0 else np.inf
    return pre, post, ratio


def simulate(rng: np.random.Generator, n_donors: int, t: int, t0: int,
             k: int, sigma: float, delta: float, treated: int = 0) -> np.ndarray:
    """Factor-model panel where a convex mix of donors can track the treated.

    Y_it = lambda_i . F_t + eps_it, with the treated unit's loadings drawn
    inside the donors' convex hull so a good synthetic control exists. A
    post-treatment effect `delta` is added to the treated unit from t0 on.
    """
    n_units = n_donors + 1
    # smooth common factors (random walks) so pre-period fit is informative
    F = np.cumsum(rng.normal(scale=0.5, size=(t, k)), axis=0)
    loadings = rng.uniform(0.0, 1.0, size=(n_units, k))
    # treated loadings: a convex combination of several donors (in the hull)
    mix = rng.dirichlet(np.ones(n_donors))
    loadings[treated] = mix @ loadings[[j for j in range(n_units) if j != treated]]
    Y = loadings @ F.T + rng.normal(scale=sigma, size=(n_units, t))
    Y[treated, t0:] += delta
    return Y


def run_size_study() -> float:
    """False-positive rate of the permutation test under a true null (delta=0)."""
    rng = np.random.default_rng(SEED + 7)
    rejections = 0
    for _ in range(SIZE_REPS):
        Y = simulate(rng, SIZE_N_DONORS, SIZE_T, SIZE_T0, K, SIGMA,
                     delta=0.0, treated=0)
        res = placebo_inference(Y, treated=0, t0=SIZE_T0)
        rejections += int(res["p_value"] <= ALPHA)
    return rejections / SIZE_REPS


def make_figure(res: dict, t0: int, t: int) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))

    periods = np.arange(t)
    for i, g in res["gaps"].items():
        if i == 0:
            continue
        ax1.plot(periods, g, color="0.75", linewidth=0.8)
    ax1.plot(periods, res["gaps"][0], color="black", linewidth=2.0,
             label="Treated unit")
    ax1.axhline(0, color="grey", linestyle="--", linewidth=0.8)
    ax1.axvline(t0 - 0.5, color="grey", linestyle=":", linewidth=0.8)
    ax1.set_xlabel("Period")
    ax1.set_ylabel("Treated minus synthetic gap")
    ax1.set_title("Gaps: treated (black) vs placebo donors (grey)")
    ax1.legend(frameon=False, loc="upper left")

    ax2.hist(res["ratios"], bins=15, color="0.8", edgecolor="white")
    ax2.axvline(res["treated_ratio"], color="firebrick", linewidth=2.0,
                label=f"Treated ratio (p={res['p_value']:.3f})")
    ax2.set_xlabel("Post/pre RMSPE ratio")
    ax2.set_ylabel("Number of units")
    ax2.set_title("Permutation distribution of the test statistic")
    ax2.legend(frameon=False)

    fig.tight_layout()
    pdf = OUT / "synthetic_control.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "synthetic_control.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)

    # ---- 1. POWER: a real effect lands in the tail -------------------
    Y = simulate(rng, N_DONORS, T, T0, K, SIGMA, DELTA, treated=0)
    res = placebo_inference(Y, treated=0, t0=T0)
    treated_pre = res["pre_fits"][0]
    median_placebo_pre = float(np.median(res["pre_fits"][1:]))
    best_placebo_pre = float(np.min(res["pre_fits"][1:]))

    print("=" * 70)
    print("Synthetic control: placebo/permutation inference, not visual fit")
    print(f"  donors={N_DONORS}  periods={T}  pre={T0}  post={T - T0}"
          f"  true effect delta={DELTA}  seed={SEED}")
    print("=" * 70)
    print("POWER scenario (a real post-treatment effect is present):")
    print(f"  treated post/pre RMSPE ratio = {res['treated_ratio']:.2f}")
    print(f"  rank among {res['n_units']} units   = {res['treated_rank']} "
          f"(1 = most extreme)")
    print(f"  permutation p-value          = {res['p_value']:.3f}")
    print()
    print("FIT IS NOT INFERENCE:")
    print(f"  treated pre-period RMSPE     = {treated_pre:.3f}")
    print(f"  best placebo pre-RMSPE       = {best_placebo_pre:.3f}")
    print(f"  median placebo pre-RMSPE     = {median_placebo_pre:.3f}")
    print("  -> placebo donors fit the pre-period about as tightly as the")
    print("     treated unit; pre-fit alone identifies nothing.")
    print()

    # ---- 2. SIZE: no effect rejects at about the nominal rate --------
    fpr = run_size_study()
    print("SIZE scenario (Monte Carlo, true effect = 0):")
    print(f"  reps={SIZE_REPS}  nominal level alpha={ALPHA}")
    print(f"  empirical false-positive rate = {fpr:.3f}")
    print("  -> the permutation test controls size; visual fit offers no")
    print("     such guarantee.")

    pdf = make_figure(res, T0, T)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    assert res["treated_rank"] <= 2, (
        "a real effect should put the treated unit in the extreme tail")
    assert res["p_value"] <= 2.0 / res["n_units"] + 1e-9, (
        "permutation p-value should be significant when an effect is present")
    assert best_placebo_pre <= 1.5 * treated_pre, (
        "placebo donors should achieve pre-fit comparable to the treated unit")
    assert fpr <= 0.20, (
        f"permutation test should control size near {ALPHA}, got {fpr:.3f}")
    print("\nAll assertions passed: a real effect lands in the tail, the test "
          "controls size,\nand good pre-fit is not evidence of an effect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
