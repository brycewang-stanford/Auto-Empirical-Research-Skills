#!/usr/bin/env python3
"""RDD demo: why high-order global polynomials are not the default.

A runnable companion to docs/methods-reference.md section 4 ("Regression
discontinuity") and the aer-identification skill. With a KNOWN jump at the
cutoff, it shows (Gelman-Imbens 2019) that a 4th-order *global* polynomial:

  * is badly biased at the boundary when the true regression function is not
    itself a low-order polynomial, and
  * has a conventional confidence interval that almost never covers the truth,

while `rdrobust` (local-linear, MSE-optimal bandwidth, robust bias-corrected CI)
recovers the true jump with correct coverage.

The script asserts both facts and exits non-zero if they fail to reproduce, so
it doubles as a regression test of the skill stack's RDD advice.

Run:  python3 rdd_polynomial_demo.py
Deps: numpy, pandas, statsmodels, rdrobust, matplotlib
      (pinned in ../../templates/python/requirements.txt)

References (keys in ../../references.bib): gelman_imbens_2019,
calonico_cattaneo_titiunik_2014, cattaneo_jansson_ma_2020.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rdrobust import rdrobust

SEED = 20260101
N = 1000
REPS = 400
TAU = 0.75          # true jump at the cutoff
CUTOFF = 0.0
NOISE_SD = 0.30
POLY_ORDER = 4
OUT = Path(__file__).resolve().parent / "output"


def m(x: np.ndarray) -> np.ndarray:
    """Smooth, non-polynomial conditional mean a 4th-order global fit can't
    capture -- high frequency relative to the support."""
    return 0.4 * np.sin(8.0 * x) + 0.5 * x


def simulate(rng: np.random.Generator, n: int = N) -> tuple:
    x = rng.uniform(-1, 1, n)
    treat = (x >= CUTOFF).astype(float)
    y = m(x) + TAU * treat + rng.normal(0, NOISE_SD, n)
    return x, y, treat


def global_poly_jump(x, y, treat, p: int = POLY_ORDER) -> tuple[float, float]:
    """Jump from a single interacted global polynomial: coef on the treatment
    indicator in y ~ treat + poly(x,p) + treat:poly(x,p). Returns (est, se)."""
    cols = [np.ones(len(x)), treat]
    cols += [x ** k for k in range(1, p + 1)]
    cols += [treat * x ** k for k in range(1, p + 1)]
    res = sm.OLS(y, np.column_stack(cols)).fit(cov_type="HC1")
    return float(res.params[1]), float(res.bse[1])


def rdrobust_jump(x, y) -> dict:
    r = rdrobust(y, x, c=CUTOFF)
    est = float(r.coef.loc["Conventional"].iloc[0])
    ci = r.ci.loc["Robust"]
    return {"est": est, "ci": (float(ci.iloc[0]), float(ci.iloc[1])),
            "h": float(r.bws.loc["h"].iloc[0])}


def run_study() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    gp_est, gp_cov, rd_est, rd_cov = [], 0, [], 0
    for _ in range(REPS):
        x, y, treat = simulate(rng)
        b, se = global_poly_jump(x, y, treat)
        gp_est.append(b)
        gp_cov += (b - 1.96 * se <= TAU <= b + 1.96 * se)
        rd = rdrobust_jump(x, y)
        rd_est.append(rd["est"])
        rd_cov += (rd["ci"][0] <= TAU <= rd["ci"][1])
    return pd.DataFrame([
        {"method": f"Global polynomial (order {POLY_ORDER})",
         "mean_estimate": float(np.mean(gp_est)), "bias": float(np.mean(gp_est)) - TAU,
         "ci_coverage": gp_cov / REPS},
        {"method": "rdrobust (local-linear, RBC CI)",
         "mean_estimate": float(np.mean(rd_est)), "bias": float(np.mean(rd_est)) - TAU,
         "ci_coverage": rd_cov / REPS},
    ])


def make_figure() -> Path:
    """One sample: binned means, the global-poly fit (boundary overshoot), and
    the local-linear fit near the cutoff."""
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED + 7)
    x, y, treat = simulate(rng)
    rd = rdrobust_jump(x, y)
    h = rd["h"]

    # binned means for the scatter
    bins = np.linspace(-1, 1, 41)
    idx = np.digitize(x, bins)
    bx = [x[idx == i].mean() for i in range(1, len(bins)) if (idx == i).any()]
    by = [y[idx == i].mean() for i in range(1, len(bins)) if (idx == i).any()]

    # global polynomial fitted curve each side
    cols = [np.ones(len(x)), treat] + [x ** k for k in range(1, POLY_ORDER + 1)]
    cols += [treat * x ** k for k in range(1, POLY_ORDER + 1)]
    beta = sm.OLS(y, np.column_stack(cols)).fit().params

    def gp_curve(grid, side):
        c = [np.ones_like(grid), np.full_like(grid, side)]
        c += [grid ** k for k in range(1, POLY_ORDER + 1)]
        c += [side * grid ** k for k in range(1, POLY_ORDER + 1)]
        return np.column_stack(c) @ beta

    gl = np.linspace(-1, -1e-6, 200)
    gr = np.linspace(1e-6, 1, 200)

    # local-linear fit within the rdrobust bandwidth
    def ll(side_mask, grid):
        xs, ys = x[side_mask], y[side_mask]
        b = np.polyfit(xs, ys, 1)
        return np.polyval(b, grid)
    ll_l = np.linspace(-h, -1e-6, 50)
    ll_r = np.linspace(1e-6, h, 50)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(bx, by, s=14, color="grey", alpha=0.7, label="binned means")
    ax.plot(gl, gp_curve(gl, 0), color="firebrick", lw=1.8)
    ax.plot(gr, gp_curve(gr, 1), color="firebrick", lw=1.8,
            label=f"global poly (order {POLY_ORDER})")
    ax.plot(ll_l, ll((x < 0), ll_l), color="black", lw=2.4)
    ax.plot(ll_r, ll((x >= 0), ll_r), color="black", lw=2.4,
            label=f"local-linear (|x|<{h:.2f})")
    ax.axvline(CUTOFF, linestyle="--", color="grey", lw=0.8)
    ax.set_xlabel("Running variable")
    ax.set_ylabel("Outcome")
    ax.set_title("Global polynomial overshoots at the cutoff; local-linear does not")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    pdf = OUT / "rd_fit.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "rd_fit.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    tbl = run_study()
    pd.set_option("display.float_format", lambda v: f"{v:9.3f}")
    print("=" * 70)
    print("RDD: high-order global polynomial vs local-linear (rdrobust)")
    print(f"  n={N}  reps={REPS}  true jump={TAU}  seed={SEED}")
    print("=" * 70)
    print(tbl.to_string(index=False))
    print()
    gp = tbl.iloc[0]
    rdr = tbl.iloc[1]
    print(f"The global polynomial is biased by {gp['bias']:+.2f} and its 95% CI "
          f"covers the truth only {100 * gp['ci_coverage']:.0f}% of the time.")
    print(f"rdrobust is within {abs(rdr['bias']):.2f} of the truth with "
          f"{100 * rdr['ci_coverage']:.0f}% coverage.")
    pdf = make_figure()
    print(f"Figure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions ----
    assert abs(gp["bias"]) > 0.20, "global polynomial should be materially biased"
    assert gp["ci_coverage"] < 0.50, "global-poly CI should badly under-cover"
    assert abs(rdr["bias"]) < 0.10, "rdrobust should recover the jump"
    assert rdr["ci_coverage"] > 0.90, "rdrobust RBC CI should cover near nominal"
    print("\nAll assertions passed: the global polynomial misleads; rdrobust does not.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
