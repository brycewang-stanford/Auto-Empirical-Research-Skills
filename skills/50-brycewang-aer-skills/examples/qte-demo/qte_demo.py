#!/usr/bin/env python3
"""Quantile-treatment-effects demo: the ATE can hide everything.

A runnable companion to docs/methods-reference.md and the aer-robustness skill.
It builds the distributional-effects exhibit referees ask for when the mean is
a wash: a treatment that leaves the AVERAGE outcome exactly unchanged while
spreading the distribution -- harming the bottom of the outcome distribution
and helping the top. OLS (the ATE) reports a precise zero and calls the
program a nothing-burger; quantile regression of Y on the treatment indicator
(Koenker and Bassett 1978) traces out the whole quantile-treatment-effect
curve and shows the action the mean averages away.

The data-generating process makes the truth ANALYTIC. Treatment is randomized
(so quantile regression on a constant and D identifies unconditional QTEs),
Y0 ~ Normal(MU, SIGMA0^2) and Y1 ~ Normal(MU, SIGMA1^2) with SIGMA1 > SIGMA0.
Then the true ATE is exactly 0 while the true QTE curve is

    QTE(tau) = (SIGMA1 - SIGMA0) * Phi^{-1}(tau),

negative below the median, zero at it, positive above. The script runs a
Monte Carlo, estimates QTE(tau) by statsmodels QuantReg at five quantiles,
and asserts that the OLS/ATE estimate is (correctly but uselessly) zero, that
the median effect is null, and that the estimated tails match the analytic
QTE values -- exiting non-zero if any check fails, so the demo doubles as a
regression test of the quantile-regression pipeline.

Run:  python3 qte_demo.py
Deps: numpy, matplotlib, statsmodels
      (all pinned in ../../templates/python/requirements.txt)

References: koenker_bassett_1978 in ../../references.bib.
See ../../docs/methods-reference.md for the per-stack tooling (qreg, sqreg,
quantreg, QuantReg) and ../../skills/aer-robustness/SKILL.md for when a
distributional-effects exhibit is expected alongside the headline ATE.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from statsmodels.regression.quantile_regression import QuantReg
# QuantReg's IRLS can bump its iteration cap on some Monte Carlo draws without
# materially moving the estimates at this scale; keep the summary readable.
from statsmodels.tools.sm_exceptions import IterationLimitWarning
warnings.simplefilter("ignore", IterationLimitWarning)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _aer_numeric_check import numeric_check  # noqa: E402

SEED = 20260401
N = 2000                 # observations per Monte Carlo panel
REPS = 300               # Monte Carlo panels
MU = 10.0                # common mean of Y0 and Y1 (the ATE is exactly zero)
SIGMA0 = 1.0             # control-outcome spread
SIGMA1 = 2.0             # treated-outcome spread (treatment widens the tails)
P_TREAT = 0.5            # randomized treatment probability
TAUS = np.array([0.10, 0.25, 0.50, 0.75, 0.90])   # quantiles to estimate
OUT = Path(__file__).resolve().parent / "output"


def norm_ppf(p: np.ndarray) -> np.ndarray:
    """Standard-normal inverse CDF Phi^{-1}(p), vectorized in pure numpy.

    Acklam's rational approximation (relative error < 1.2e-9), so we get the
    analytic QTE targets without importing scipy.
    """
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p = np.asarray(p, dtype=float)
    x = np.empty_like(p)
    p_low, p_high = 0.02425, 1.0 - 0.02425

    lo = p < p_low
    hi = p > p_high
    mid = ~(lo | hi)
    if lo.any():
        q = np.sqrt(-2.0 * np.log(p[lo]))
        x[lo] = ((((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
                 / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0))
    if hi.any():
        q = np.sqrt(-2.0 * np.log(1.0 - p[hi]))
        x[hi] = -((((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
                  / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0))
    if mid.any():
        q = p[mid] - 0.5
        r = q * q
        x[mid] = ((((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
                  / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0))
    return x


def true_qte(taus: np.ndarray) -> np.ndarray:
    """Analytic QTE(tau) = (SIGMA1 - SIGMA0) * Phi^{-1}(tau) under the DGP."""
    return (SIGMA1 - SIGMA0) * norm_ppf(taus)


def _panel(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """One randomized experiment: Y0 ~ N(MU, SIGMA0^2), Y1 ~ N(MU, SIGMA1^2)."""
    D = (rng.random(N) < P_TREAT).astype(float)
    eps = rng.normal(size=N)
    Y = MU + (SIGMA0 + (SIGMA1 - SIGMA0) * D) * eps    # mean unchanged by D
    return D, Y


def ols_ate(D: np.ndarray, Y: np.ndarray) -> float:
    """OLS of Y on [1, D]; the coefficient on D is the ATE estimate."""
    Z = np.column_stack([np.ones_like(Y), D])
    coef, *_ = np.linalg.lstsq(Z, Y, rcond=None)
    return float(coef[1])


def qte_curve(D: np.ndarray, Y: np.ndarray, taus: np.ndarray) -> np.ndarray:
    """Quantile regression of Y on [1, D] at each tau; slope on D is QTE(tau)."""
    Z = np.column_stack([np.ones_like(Y), D])
    model = QuantReg(Y, Z)
    return np.array([float(model.fit(q=tau).params[1]) for tau in taus])


def run_montecarlo(rng: np.random.Generator) -> dict:
    ates = np.empty(REPS)
    qtes = np.empty((REPS, len(TAUS)))
    for r in range(REPS):
        D, Y = _panel(rng)
        ates[r] = ols_ate(D, Y)
        qtes[r] = qte_curve(D, Y, TAUS)
    return {
        "ate_mean": float(ates.mean()),
        "qte_mean": qtes.mean(axis=0),
        "qte_lo": np.percentile(qtes, 2.5, axis=0),
        "qte_hi": np.percentile(qtes, 97.5, axis=0),
    }


def make_figure(m: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    grid = np.linspace(0.05, 0.95, 181)
    ax.plot(grid, true_qte(grid), color="grey", linewidth=1.5,
            label=r"analytic QTE$(\tau)=(\sigma_1-\sigma_0)\,\Phi^{-1}(\tau)$")
    ax.fill_between(TAUS, m["qte_lo"], m["qte_hi"], color="steelblue",
                    alpha=0.25, label="Monte Carlo 95% band")
    ax.plot(TAUS, m["qte_mean"], marker="o", color="steelblue",
            label="estimated QTE (QuantReg, MC mean)")
    ax.axhline(0.0, linestyle="--", color="firebrick",
               label=f"ATE = 0 (OLS mean = {m['ate_mean']:.3f})")
    ax.set_xlabel(r"quantile $\tau$")
    ax.set_ylabel("Treatment effect on outcome quantile")
    ax.set_title("QTE: the mean is a wash, the distribution is not")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    pdf = OUT / "qte_curve.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "qte_curve.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    m = run_montecarlo(rng)
    truth = true_qte(TAUS)
    max_dev = float(np.max(np.abs(m["qte_mean"] - truth)))

    print("=" * 70)
    print("Quantile treatment effects: the ATE can hide everything")
    print(f"  N={N}  reps={REPS}  Y0~N({MU:.0f},{SIGMA0:.0f}^2)"
          f"  Y1~N({MU:.0f},{SIGMA1:.0f}^2)  true ATE=0  seed={SEED}")
    print("=" * 70)
    print(f"  OLS / ATE (MC mean)           = {m['ate_mean']:+.3f}"
          "   (a precise, useless zero)")
    print()
    print("   tau    QTE-hat    analytic QTE")
    for tau, est, tru in zip(TAUS, m["qte_mean"], truth):
        print(f"  {tau:4.2f}   {est:+7.3f}   {tru:+7.3f}")
    print()
    print(f"  max |QTE-hat - analytic| across taus = {max_dev:.3f}")
    print("  the treatment HARMS the bottom decile by about "
          f"{-truth[0]:.2f} and HELPS")
    print(f"  the top decile by about {truth[-1]:.2f}, yet the ATE is exactly "
          "zero: any")
    print("  welfare or targeting claim needs the quantile curve, not the mean.")

    pdf = make_figure(m)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known analytic target and
    # emits a NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("OLS/ATE misses the action", m["ate_mean"],
                  target=0.0, tol=0.02)
    numeric_check("QTE at tau=0.9 matches the analytic value",
                  m["qte_mean"][-1], target=float(truth[-1]), tol=0.03)
    numeric_check("QTE at tau=0.1 matches the analytic value",
                  m["qte_mean"][0], target=float(truth[0]), tol=0.03)
    numeric_check("median effect is null", m["qte_mean"][2],
                  target=0.0, tol=0.02)
    numeric_check("whole QTE curve tracks the analytic curve (max abs dev)",
                  max_dev, hi=0.03)
    print("\nAll assertions passed: OLS reports a true-but-empty zero while "
          "quantile\nregression recovers the analytic QTE curve -- report the "
          "distribution when\nthe mean is a wash.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
