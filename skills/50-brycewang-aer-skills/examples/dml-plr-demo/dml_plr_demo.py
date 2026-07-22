#!/usr/bin/env python3
"""Double machine learning demo: why orthogonalization + cross-fitting matter.

A runnable companion to docs/methods-reference.md and the aer-identification
skill. It reproduces, in miniature, the core contrast of Chernozhukov et al.
(2018): when nuisance functions are estimated with flexible (regularized)
learners, plugging their predictions into a NON-orthogonal moment condition
leaves a first-order bias, while the Neyman-orthogonal partialling-out moment
of Robinson (1988), combined with cross-fitting, removes it.

The data-generating process is a partially linear model with a KNOWN effect:

    Y = theta * D + g(X) + eps        theta = 0.5 (the truth)
    D = m(X) + v

with nonlinear nuisances g and m that share components, so a linear-controls
regression is confounded by design. Three estimators run on the same
Monte Carlo panels:

  1. OLS with linear controls -- misspecifies g, biased upward by design.
  2. Naive ML plug-in -- learn E[Y|X] with a flexible ridge learner, then
     regress (Y - Ehat[Y|X]) on the RAW treatment D. The moment is not
     orthogonal to the D equation, so the estimate is attenuated by the
     predictable share of D (a known factor var(v)/var(D) here).
  3. DML partialling-out -- residualize BOTH Y and D on X with the same
     learner under 5-fold cross-fitting, then regress residual on residual.
     Recovers the truth, with valid coverage.

Because every bias in this design has a known sign and magnitude, the demo is
also a regression test: it pins the linear-OLS bias floor, the plug-in
attenuation ceiling, the DML point estimate to the truth, and the DML
confidence-interval coverage, and exits non-zero if any check fails.

Run:  python3 dml_plr_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: chernozhukov_etal_2018 and robinson_1988 in ../../references.bib.
See ../../docs/methods-reference.md for the per-stack tooling (the StatsPAI
`dml` tool, DoubleML in R/Python) and ../../skills/aer-identification/SKILL.md
for the design context.
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

SEED = 20260701
N = 1000                  # observations per Monte Carlo panel
DIM_X = 5                 # covariates
THETA_TRUE = 0.5          # the truth
SIGMA_V = 1.0             # treatment noise
SIGMA_EPS = 1.0           # outcome noise
REPS = 400                # Monte Carlo panels
FOLDS = 5                 # cross-fitting folds
RIDGE_LAMBDA = 1e-3       # small penalty; the basis is rich but low-dimensional
OUT = Path(__file__).resolve().parent / "output"


def g_fun(X: np.ndarray) -> np.ndarray:
    """Outcome nuisance: nonlinear in x1, x2; linear in x3."""
    return 2.0 * np.sin(X[:, 0]) + 0.5 * X[:, 1] ** 2 + X[:, 2]


def m_fun(X: np.ndarray) -> np.ndarray:
    """Treatment nuisance: shares the nonlinear components of g (confounding)."""
    return np.sin(X[:, 0]) + 0.25 * X[:, 1] ** 2


def make_panel(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    X = rng.normal(size=(N, DIM_X))
    D = m_fun(X) + rng.normal(scale=SIGMA_V, size=N)
    Y = THETA_TRUE * D + g_fun(X) + rng.normal(scale=SIGMA_EPS, size=N)
    return X, D, Y


def basis(X: np.ndarray) -> np.ndarray:
    """Flexible feature map: levels, squares, sin, cos of each covariate."""
    return np.column_stack(
        [np.ones(X.shape[0]), X, X**2, np.sin(X), np.cos(X)]
    )


def ridge_fit_predict(Z_train: np.ndarray, y_train: np.ndarray,
                      Z_test: np.ndarray) -> np.ndarray:
    """Ridge regression on the feature map (intercept unpenalized via centering)."""
    p = Z_train.shape[1]
    penalty = RIDGE_LAMBDA * len(y_train) * np.eye(p)
    penalty[0, 0] = 0.0  # do not penalize the intercept column
    coef = np.linalg.solve(Z_train.T @ Z_train + penalty, Z_train.T @ y_train)
    return Z_test @ coef


def crossfit_predict(Z: np.ndarray, y: np.ndarray,
                     rng: np.random.Generator) -> np.ndarray:
    """Out-of-fold nuisance predictions under K-fold cross-fitting."""
    n = len(y)
    fold_of = rng.permutation(np.repeat(np.arange(FOLDS), int(np.ceil(n / FOLDS)))[:n])
    pred = np.empty(n)
    for k in range(FOLDS):
        test = fold_of == k
        train = ~test
        pred[test] = ridge_fit_predict(Z[train], y[train], Z[test])
    return pred


def ols_slope(y: np.ndarray, d: np.ndarray) -> tuple[float, float]:
    """Bivariate OLS slope of y on d (with intercept) and its robust (HC0) SE."""
    d_c = d - d.mean()
    y_c = y - y.mean()
    s_dd = float(d_c @ d_c)
    slope = float(d_c @ y_c) / s_dd
    resid = y_c - slope * d_c
    se = float(np.sqrt((d_c**2 * resid**2).sum())) / s_dd
    return slope, se


def linear_ols_theta(X: np.ndarray, D: np.ndarray, Y: np.ndarray) -> float:
    """OLS of Y on [1, D, X] -- linear controls, misspecified g."""
    Z = np.column_stack([np.ones(len(Y)), D, X])
    coef, *_ = np.linalg.lstsq(Z, Y, rcond=None)
    return float(coef[1])


def run_montecarlo(rng: np.random.Generator) -> dict:
    acc: dict[str, list[float]] = {"ols": [], "plugin": [], "dml": [], "covered": []}
    for _ in range(REPS):
        X, D, Y = make_panel(rng)
        Z = basis(X)

        acc["ols"].append(linear_ols_theta(X, D, Y))

        # Naive plug-in: learn E[Y|X], regress the outcome residual on RAW D.
        # The moment ignores the D equation, so the predictable share of D
        # attenuates the estimate toward var(v)/var(D) * theta.
        y_hat = crossfit_predict(Z, Y, rng)
        plugin, _ = ols_slope(Y - y_hat, D)
        acc["plugin"].append(plugin)

        # DML / Robinson partialling-out: residualize BOTH equations,
        # cross-fitted, then residual-on-residual OLS (orthogonal moment).
        d_hat = crossfit_predict(Z, D, rng)
        theta, se = ols_slope(Y - y_hat, D - d_hat)
        acc["dml"].append(theta)
        acc["covered"].append(
            float(theta - 1.96 * se <= THETA_TRUE <= theta + 1.96 * se)
        )
    return {k: np.asarray(v) for k, v in acc.items()}


def attenuation_factor() -> float:
    """Population var(v)/var(D): the plug-in's known attenuation factor."""
    var_m = np.var(m_fun(np.random.default_rng(0).normal(size=(200_000, DIM_X))))
    return SIGMA_V**2 / (SIGMA_V**2 + float(var_m))


def make_figure(mc: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    bins = np.linspace(0.1, 0.9, 61)
    specs = [
        ("ols", "OLS, linear controls", "firebrick"),
        ("plugin", "naive ML plug-in", "darkorange"),
        ("dml", "DML partialling-out", "steelblue"),
    ]
    for key, label, color in specs:
        ax.hist(mc[key], bins=bins, alpha=0.55, color=color,
                label=f"{label} (mean {mc[key].mean():.3f})")
    ax.axvline(THETA_TRUE, linestyle="--", color="black",
               label=f"true effect = {THETA_TRUE}")
    ax.set_xlabel("Estimated treatment effect")
    ax.set_ylabel("Monte Carlo frequency")
    ax.set_title("Non-orthogonal moments stay biased; DML cross-fitting recovers the truth")
    ax.legend(frameon=False)
    fig.tight_layout()
    pdf = OUT / "dml_plr.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "dml_plr.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    mc = run_montecarlo(rng)
    means = {k: float(mc[k].mean()) for k in ("ols", "plugin", "dml")}
    coverage = float(mc["covered"].mean())
    atten = attenuation_factor()

    print("=" * 70)
    print("Double ML: orthogonalization + cross-fitting vs. naive alternatives")
    print(f"  N={N}  reps={REPS}  true theta={THETA_TRUE}  folds={FOLDS}  seed={SEED}")
    print("=" * 70)
    print(f"  OLS, linear controls        theta = {means['ols']:.3f}"
          f"   (misspecified g: biased up)")
    print(f"  naive ML plug-in            theta = {means['plugin']:.3f}"
          f"   (non-orthogonal: attenuated)")
    print(f"  DML partialling-out         theta = {means['dml']:.3f}"
          f"   (the truth is {THETA_TRUE})")
    print(f"  DML 95% CI coverage         {coverage:.3f}")
    print()
    print(f"  the plug-in's attenuation is not noise: ignoring the D equation")
    print(f"  scales theta by var(v)/var(D) = {atten:.2f}, so it converges to")
    print(f"  ~{atten * THETA_TRUE:.2f} no matter how large the sample gets.")

    pdf = make_figure(mc)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known target and emits a
    # NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("linear-controls OLS is biased upward", means["ols"],
                  lo=THETA_TRUE + 0.10)
    numeric_check("naive plug-in attenuates toward var(v)/var(D)*theta",
                  means["plugin"], target=atten * THETA_TRUE, tol=0.05)
    numeric_check("plug-in stays below the truth by a margin", means["plugin"],
                  hi=THETA_TRUE - 0.10)
    numeric_check("DML partialling-out recovers the truth", means["dml"],
                  target=THETA_TRUE, tol=0.02)
    numeric_check("DML 95% CI coverage is honest", coverage, lo=0.90, hi=0.99)
    print("\nAll assertions passed: only the orthogonal, cross-fitted moment "
          "recovers the\ntruth -- flexible prediction alone is not causal "
          "inference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
