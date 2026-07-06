#!/usr/bin/env python3
"""Matrix-completion demo: factor confounding breaks DiD; imputation fixes it.

A runnable companion to docs/methods-reference.md and the aer-identification
skill. It simulates the setting of Athey et al. (2021) and Xu (2017): control
outcomes follow a low-rank factor structure (interactive fixed effects), and
treated units load MORE heavily on a trending factor. Parallel trends then
fails by construction -- treated units would have trended up even without
treatment -- so two-way-fixed-effects DiD is biased upward. A KNOWN constant
treatment effect (tau = 1) makes the bias visible and testable.

The matrix-completion counterfactual treats the treated-by-post block of the
outcome matrix as MISSING, estimates the low-rank structure from the observed
entries (hard-impute: alternate a rank-k truncated SVD with re-imputing the
missing block, initialized from a two-way fixed-effects fit), and reads the
treatment effect off the gap between observed treated outcomes and their
imputed counterfactuals. Because the factor paths are recoverable from the
observed entries, the imputation removes the factor confounding that DiD
cannot.

Two cautionary notes are built into the demo rather than asserted: the
placebo pass (a world with no treatment) must show a ~zero effect, and the
rank is FIXED at the oracle value -- the script prints how the estimate
degrades when the rank is over-set, the practical failure mode alternating
imputation is known for (regularized/cross-validated variants such as
MC-NNM exist precisely for this; see Athey et al. 2021).

Run:  python3 matrix_completion_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: athey_etal_2021 and xu_2017 in ../../references.bib.
See ../../docs/methods-reference.md for the per-stack tooling and
../../skills/aer-identification/SKILL.md for the design context.
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

SEED = 20260702
N, T = 100, 40            # panel dimensions
N_TREATED, T_TREAT = 25, 28   # treated block: units 0..24, periods 28..39
RANK_TRUE = 2             # latent factors
RANK_FIT = 4              # oracle fitting rank: factors + unit/time means
TAU_TRUE = 1.0            # the truth: constant treatment effect
NOISE_SD = 0.3            # idiosyncratic noise
LOADING_SHIFT = 1.0       # treated units' extra loading on the trending factor
REPS = 25                 # Monte Carlo panels
IMPUTE_ITERS = 300        # hard-impute iterations
OUT = Path(__file__).resolve().parent / "output"


def make_panel(rng: np.random.Generator,
               treat: bool) -> tuple[np.ndarray, np.ndarray]:
    """Outcome matrix and treatment mask under interactive fixed effects."""
    loadings = rng.normal(0.0, 1.0, (N, RANK_TRUE))
    loadings[:N_TREATED, 0] += LOADING_SHIFT     # the confounding: treated
    t = np.arange(T)                             # load more on the trend
    factors = np.vstack([0.08 * t + np.sin(t / 3.0), np.cos(t / 5.0)])
    alpha = rng.normal(0.0, 1.0, N)[:, None]
    beta = rng.normal(0.0, 0.5, T)[None, :]
    y0 = loadings @ factors + alpha + beta + rng.normal(0.0, NOISE_SD, (N, T))
    treated = np.zeros((N, T), dtype=bool)
    treated[:N_TREATED, T_TREAT:] = True
    return y0 + (TAU_TRUE * treated if treat else 0.0), treated


def did_twfe(y: np.ndarray, treated: np.ndarray) -> float:
    """Two-way FE DiD: double-demean outcome and dummy, then one OLS slope."""
    yy = y - y.mean(axis=1, keepdims=True)
    yy -= yy.mean(axis=0, keepdims=True)
    dd = treated.astype(float)
    dd -= dd.mean(axis=1, keepdims=True)
    dd -= dd.mean(axis=0, keepdims=True)
    return float((dd * yy).sum() / (dd * dd).sum())


def twoway_fill(y: np.ndarray, observed: np.ndarray) -> np.ndarray:
    """Two-way FE fit on the observed entries (initialization for imputation)."""
    masked = np.where(observed, y, np.nan)
    mu = float(y[observed].mean())
    a = np.zeros(N)
    b = np.zeros(T)
    for _ in range(20):
        a = np.nanmean(masked - mu - b[None, :], axis=1)
        b = np.nanmean(masked - mu - a[:, None], axis=0)
    return mu + a[:, None] + b[None, :]


def matrix_completion_att(y: np.ndarray, treated: np.ndarray,
                          rank: int = RANK_FIT) -> float:
    """Hard-impute the treated block, then average observed-minus-imputed."""
    observed = ~treated
    completed = np.where(observed, y, twoway_fill(y, observed))
    l_hat = completed
    for _ in range(IMPUTE_ITERS):
        u, s, vt = np.linalg.svd(completed, full_matrices=False)
        l_hat = (u[:, :rank] * s[:rank]) @ vt[:rank]
        completed = np.where(observed, y, l_hat)
    return float((y[treated] - l_hat[treated]).mean())


def run_montecarlo(rng: np.random.Generator) -> dict:
    acc: dict[str, list[float]] = {"did": [], "mc": [], "placebo": []}
    for _ in range(REPS):
        y, treated = make_panel(rng, treat=True)
        acc["did"].append(did_twfe(y, treated))
        acc["mc"].append(matrix_completion_att(y, treated))
        y0, treated0 = make_panel(rng, treat=False)
        acc["placebo"].append(matrix_completion_att(y0, treated0))
    return {k: float(np.mean(v)) for k, v in acc.items()}


def make_figure(rng: np.random.Generator) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    y, treated = make_panel(rng, treat=True)
    observed = ~treated
    completed = np.where(observed, y, twoway_fill(y, observed))
    l_hat = completed
    for _ in range(IMPUTE_ITERS):
        u, s, vt = np.linalg.svd(completed, full_matrices=False)
        l_hat = (u[:, :RANK_FIT] * s[:RANK_FIT]) @ vt[:RANK_FIT]
        completed = np.where(observed, y, l_hat)

    treated_mean = y[:N_TREATED].mean(axis=0)
    imputed_mean = l_hat[:N_TREATED].mean(axis=0)
    control_mean = y[N_TREATED:].mean(axis=0)

    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    t = np.arange(T)
    ax.plot(t, treated_mean, color="firebrick", label="treated units (observed)")
    ax.plot(t, imputed_mean, color="black", linestyle="--",
            label="imputed counterfactual (matrix completion)")
    ax.plot(t, control_mean, color="steelblue", alpha=0.7,
            label="control units (observed)")
    ax.axvline(T_TREAT - 0.5, color="grey", linestyle=":",
               label="treatment starts")
    ax.set_xlabel("Period")
    ax.set_ylabel("Mean outcome")
    ax.set_title("Factor confounding: treated units trend by construction; "
                 "imputation recovers the counterfactual")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    pdf = OUT / "matrix_completion.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "matrix_completion.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    m = run_montecarlo(rng)

    print("=" * 70)
    print("Matrix completion vs DiD under interactive fixed effects")
    print(f"  N={N}  T={T}  treated block={N_TREATED}x{T - T_TREAT}"
          f"  tau_true={TAU_TRUE}  rank_true={RANK_TRUE}  seed={SEED}")
    print("=" * 70)
    print(f"  two-way FE DiD               tau_hat = {m['did']:.3f}"
          f"   (parallel trends fails by design)")
    print(f"  matrix-completion imputation tau_hat = {m['mc']:.3f}"
          f"   (the truth is {TAU_TRUE})")
    print(f"  placebo (no treatment)       tau_hat = {m['placebo']:+.3f}")

    y, treated = make_panel(rng, treat=True)
    print("\n  rank sensitivity on one panel (why regularized MC-NNM exists):")
    for rank in (3, RANK_FIT, 6):
        est = matrix_completion_att(y, treated, rank=rank)
        tag = "  <- oracle rank" if rank == RANK_FIT else ""
        print(f"    rank {rank}: tau_hat = {est:.3f}{tag}")

    pdf = make_figure(rng)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known target and emits a
    # NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("two-way FE DiD is biased upward under factor confounding",
                  m["did"], lo=TAU_TRUE + 0.40)
    numeric_check("matrix-completion imputation recovers tau", m["mc"],
                  target=TAU_TRUE, tol=0.08)
    numeric_check("placebo world shows no effect", m["placebo"],
                  target=0.0, tol=0.08)
    numeric_check("imputation removes most of the DiD bias",
                  abs(m["did"] - TAU_TRUE) - abs(m["mc"] - TAU_TRUE), lo=0.40)
    print("\nAll assertions passed: when treated units load differently on a")
    print("trending factor, DiD is structurally biased and the low-rank")
    print("imputation recovers the truth.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
