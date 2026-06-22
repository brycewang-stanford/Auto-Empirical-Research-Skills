#!/usr/bin/env python3
"""Weak-instrument demo: why "first-stage F > 10" is not enough.

A runnable companion to docs/methods-reference.md section 2 ("Instrumental
variables") and the aer-identification skill. It shows, by Monte Carlo with a
KNOWN true coefficient (beta = 0), that as the instrument weakens:

  * the conventional 2SLS t-test rejects a TRUE null far more than 5% of the
    time (size distortion that "F > 10" does not fix), while
  * the Anderson-Rubin (AR) test keeps its nominal 5% size at every instrument
    strength.

It then fits one weak-instrument sample with `linearmodels` to show the real
first-stage F, the (too-narrow) 2SLS confidence interval, and the (correct) AR
confidence set.

The script asserts the size results and exits non-zero if the claim fails to
reproduce, so it doubles as a regression test of the skill stack's IV advice.

Run:  python3 iv_weak_instrument_demo.py
Deps: numpy, pandas, scipy, linearmodels, matplotlib
      (linearmodels is pinned in ../../templates/python/requirements.txt)

References (keys in ../../references.bib): montielolea_pflueger_2013,
andrews_stock_sun_2019, lee_mccrary_moreira_porter_2022, stock_yogo_2005.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from linearmodels.iv import IV2SLS

SEED = 20260101
N = 200
REPS = 3000
TRUE_BETA = 0.0
CHI2_95 = stats.chi2.ppf(0.95, 1)
# instrument strengths: first-stage coefficient pi (endogeneity held fixed)
STRENGTHS = {"strong": 1.0, "moderate": 0.30, "weak": 0.10, "very weak": 0.05}
OUT = Path(__file__).resolve().parent / "output"


def simulate(pi: float, rng: np.random.Generator, n: int = N) -> tuple:
    """One sample with endogenous d, instrument z, and true beta = 0."""
    z = rng.normal(size=n)
    u = rng.normal(size=n)
    v = rng.normal(size=n)
    eps = u                      # structural error
    nu = 0.8 * u + 0.6 * v       # first-stage error correlated with eps
    d = pi * z + nu              # first stage
    y = TRUE_BETA * d + eps      # structural equation, beta = 0
    return y, d, z


def first_stage_f(d: np.ndarray, z: np.ndarray) -> float:
    """First-stage F for a single instrument (= t^2 on z)."""
    zt = z - z.mean()
    dt = d - d.mean()
    b = (zt @ dt) / (zt @ zt)
    resid = dt - b * zt
    se = np.sqrt((resid @ resid) / (len(d) - 2) / (zt @ zt))
    return float((b / se) ** 2)


def tsls_reject(y, d, z) -> bool:
    """Does the conventional just-identified 2SLS t-test reject H0: beta=0?"""
    zt, dt = z - z.mean(), d - d.mean()
    b = (zt @ (y - y.mean())) / (zt @ dt)
    e = y - b * d
    sigma2 = (e @ e) / (len(y) - 1)
    se = np.sqrt(sigma2 * (zt @ zt)) / np.abs(zt @ dt)
    return abs(b / se) > 1.96


def ar_reject(y, d, z, beta0: float = TRUE_BETA) -> bool:
    """Anderson-Rubin test of H0: beta = beta0 (correct size for any strength).
    Just-identified AR statistic = n * corr(z, y - beta0*d)^2 ~ chi2(1)."""
    r = y - beta0 * d
    zt, rt = z - z.mean(), r - r.mean()
    corr = (zt @ rt) / np.sqrt((zt @ zt) * (rt @ rt))
    return len(y) * corr ** 2 > CHI2_95


def run_size_study() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows = []
    for label, pi in STRENGTHS.items():
        f_vals, tsls_rej, ar_rej = [], 0, 0
        for _ in range(REPS):
            y, d, z = simulate(pi, rng)
            f_vals.append(first_stage_f(d, z))
            tsls_rej += tsls_reject(y, d, z)
            ar_rej += ar_reject(y, d, z)
        rows.append({
            "instrument": label,
            "pi": pi,
            "mean_first_stage_F": float(np.mean(f_vals)),
            "tsls_reject_rate": tsls_rej / REPS,
            "ar_reject_rate": ar_rej / REPS,
        })
    return pd.DataFrame(rows)


def illustrate_one() -> dict:
    """One weak-instrument sample fitted with linearmodels + an AR set."""
    rng = np.random.default_rng(SEED + 1)
    y, d, z = simulate(STRENGTHS["very weak"], rng)
    df = pd.DataFrame({"y": y, "d": d, "z": z})
    res = IV2SLS.from_formula("y ~ 1 + [d ~ z]", df).fit()
    f_stat = float(res.first_stage.diagnostics.loc["d", "f.stat"])
    ci = res.conf_int().loc["d"]
    tsls_ci = (float(ci["lower"]), float(ci["upper"]))
    # AR 95% confidence set by grid inversion. A near-irrelevant instrument
    # gives a set that runs to the grid edge -- i.e. AR honestly reports that
    # beta is unbounded, rather than a falsely precise 2SLS interval.
    lo, hi = -50.0, 50.0
    grid = np.linspace(lo, hi, 4001)
    keep = [b for b in grid if not ar_reject(y, d, z, beta0=b)]
    if not keep:
        ar_set, ar_unbounded = None, False
    else:
        ar_set = (min(keep), max(keep))
        ar_unbounded = ar_set[0] <= lo + 1e-6 or ar_set[1] >= hi - 1e-6
    return {"f_stat": f_stat, "tsls_ci": tsls_ci, "ar_set": ar_set,
            "ar_unbounded": ar_unbounded,
            "tsls_covers": tsls_ci[0] <= TRUE_BETA <= tsls_ci[1],
            "ar_covers": ar_set is not None and ar_set[0] <= TRUE_BETA <= ar_set[1]}


def make_figure(tbl: pd.DataFrame) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    x = tbl["mean_first_stage_F"]
    ax.plot(x, 100 * tbl["tsls_reject_rate"], "o-", color="firebrick",
            label="2SLS t-test")
    ax.plot(x, 100 * tbl["ar_reject_rate"], "s-", color="black",
            label="Anderson-Rubin")
    ax.axhline(5, linestyle="--", color="grey", label="nominal 5%")
    ax.axvline(10, linestyle=":", color="grey")
    ax.text(10, ax.get_ylim()[1] * 0.9, " F = 10", color="grey", fontsize=8)
    ax.set_xscale("log")
    ax.set_xlabel("Mean first-stage F (log scale)")
    ax.set_ylabel("Rejection rate of a TRUE null (%)")
    ax.set_title("Weak instruments break the 2SLS t-test, not AR")
    ax.legend(frameon=False)
    fig.tight_layout()
    pdf = OUT / "iv_size.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "iv_size.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    tbl = run_size_study()
    one = illustrate_one()

    pd.set_option("display.float_format", lambda v: f"{v:9.3f}")
    print("=" * 70)
    print("Weak instruments: 2SLS t-test size vs Anderson-Rubin")
    print(f"  n={N}  reps={REPS}  true beta={TRUE_BETA}  seed={SEED}")
    print("=" * 70)
    print(tbl.to_string(index=False))
    print()
    print("One 'very weak' sample fitted with linearmodels:")
    print(f"  first-stage F            = {one['f_stat']:.2f}")
    print(f"  2SLS 95% CI              = [{one['tsls_ci'][0]:.2f}, {one['tsls_ci'][1]:.2f}]"
          f"  (covers truth: {one['tsls_covers']})")
    if one["ar_set"] and one["ar_unbounded"]:
        print("  Anderson-Rubin 95% set   = unbounded (instrument too weak to "
              "identify beta -- AR says so honestly)")
    elif one["ar_set"]:
        print(f"  Anderson-Rubin 95% set   = [{one['ar_set'][0]:.2f}, {one['ar_set'][1]:.2f}]"
              f"  (covers truth: {one['ar_covers']})")
    pdf = make_figure(tbl)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test ----
    strong = tbl.set_index("instrument").loc["strong"]
    weakest = tbl.set_index("instrument").loc["very weak"]
    assert strong["tsls_reject_rate"] < 0.08, "2SLS should be ~5% with a strong instrument"
    assert weakest["tsls_reject_rate"] > 0.10, "2SLS should over-reject when weak"
    assert (tbl["ar_reject_rate"] < 0.075).all(), "AR should keep ~nominal size everywhere"
    print("\nAll assertions passed: 2SLS size explodes when weak; AR stays at nominal.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
