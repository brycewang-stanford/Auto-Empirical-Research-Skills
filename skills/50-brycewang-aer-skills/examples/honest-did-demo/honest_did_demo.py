#!/usr/bin/env python3
"""Honest-DiD demo: why a flat-looking pre-trend does not license parallel trends.

A runnable companion to docs/methods-reference.md section 1 (the parallel-trends
row: "joint pre-test + Honest DiD bounds") and the aer-identification skill. It
makes the Rambachan-Roth (2023) point: a difference-in-differences event study
whose pre-period coefficients are individually small can still hide a
differential trend that continues into the post period and biases the effect.
Standard parallel-trends inference -- a confidence interval that assumes the
trend stops at treatment -- then UNDER-COVERS the true effect. Honest DiD instead
reports a confidence set valid under the assumption that the post-period
violation is at most M times the pre-period violation (the relative-magnitudes
restriction); for the right M it COVERS the truth.

The script uses a KNOWN data-generating process with a linear differential trend
that continues at the same rate after treatment (so M = 1 is exactly true) plus a
real treatment effect. It is framed as a coverage experiment -- the natural
self-test for a confidence set:

  1. The naive parallel-trends CI covers the true effect far below 95%.
  2. The relative-magnitudes honest CI reaches >= 95% coverage by M = 1, the true
     relative magnitude.

This is the single-coefficient relative-magnitudes case (one pre-period
violation bounds one post-period bias). The general multi-period FLCI is in the
HonestDiD package; the intuition and the coverage behavior are identical.

The script asserts the coverage results and exits non-zero if the claim fails to
reproduce, so it doubles as a regression test of the skill stack's honest-DiD
advice.

Run:  python3 honest_did_demo.py
Deps: numpy, scipy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: Rambachan & Roth (2023), "A more credible approach to parallel
trends." See ../../docs/methods-reference.md section 1 for the per-stack tooling
(honestdid, HonestDiD) and ../../skills/aer-identification/SKILL.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _aer_numeric_check import numeric_check  # noqa: E402

SEED = 20260101
G = 0.10                 # differential linear trend per period (the violation)
TAU = 0.20               # true post-treatment effect
SE = 0.05                # standard error of each event-study coefficient
REPS = 4000              # Monte Carlo panels
M_GRID = np.linspace(0.0, 2.0, 21)
Z = stats.norm.ppf(0.975)
OUT = Path(__file__).resolve().parent / "output"


def _event_study(rng: np.random.Generator) -> tuple[float, float, float]:
    """One event study; event time -1 is the normalized reference (=0).

    True coefficients: beta_e = G*(e+1) + TAU*1{e>=0}. The pre-period slope G
    continues into the post period, so the post coefficient is biased by exactly
    one pre-period first-difference -- relative magnitude M = 1.
    """
    b_m3 = -2 * G + rng.normal(scale=SE)      # event time -3
    b_m2 = -1 * G + rng.normal(scale=SE)      # event time -2
    b_0 = G + TAU + rng.normal(scale=SE)      # event time  0 (post)
    return b_m3, b_m2, b_0


def coverage(rng: np.random.Generator) -> dict:
    """Coverage of the true effect by the naive and honest CIs across M."""
    hits_by_m = np.zeros(len(M_GRID))
    naive_hits = 0
    breakdowns = []
    for _ in range(REPS):
        b_m3, b_m2, b_0 = _event_study(rng)
        # largest pre-period first-difference (reference at -1 is exactly 0)
        max_pre = max(abs(b_m2 - b_m3), abs(0.0 - b_m2))
        # naive parallel-trends CI assumes the trend stops: half-width = z*SE
        naive_lo, naive_hi = b_0 - Z * SE, b_0 + Z * SE
        naive_hits += int(naive_lo <= TAU <= naive_hi)
        # honest relative-magnitudes CI: allow post bias up to M * max_pre
        for j, m in enumerate(M_GRID):
            half = m * max_pre + Z * SE
            hits_by_m[j] += int(b_0 - half <= TAU <= b_0 + half)
        if b_0 > Z * SE and max_pre > 0:
            breakdowns.append((b_0 - Z * SE) / max_pre)
    return {
        "naive": naive_hits / REPS,
        "by_m": hits_by_m / REPS,
        "breakdown": float(np.mean(breakdowns)),
    }


def make_figure(cov: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(M_GRID, 100 * cov["by_m"], "o-", color="black",
            label="honest relative-magnitudes CI")
    ax.axhline(95, linestyle="--", color="grey", label="nominal 95%")
    ax.axvline(1.0, linestyle=":", color="steelblue",
               label="true relative magnitude M = 1")
    ax.plot(0, 100 * cov["naive"], "s", color="firebrick", markersize=8,
            label="naive parallel-trends CI (M = 0)")
    ax.set_xlabel("Relative-magnitudes bound M")
    ax.set_ylabel("Coverage of the true effect (%)")
    ax.set_title("Honest DiD: a continuing pre-trend breaks naive coverage")
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    pdf = OUT / "honest_did.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "honest_did.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    cov = coverage(rng)
    cov_at_1 = float(cov["by_m"][np.argmin(np.abs(M_GRID - 1.0))])

    print("=" * 70)
    print("Honest DiD: a flat-looking pre-trend does not license parallel trends")
    print(f"  trend G={G}  true effect TAU={TAU}  coef SE={SE}  reps={REPS}"
          f"  seed={SEED}")
    print("=" * 70)
    print(f"  naive parallel-trends CI coverage of the truth = "
          f"{cov['naive']:.3f}   (target 0.95)")
    print(f"  honest relative-magnitudes CI coverage at M=1   = "
          f"{cov_at_1:.3f}   (target >= 0.95)")
    print(f"  average breakdown M-bar (effect becomes insignificant) = "
          f"{cov['breakdown']:.2f}")
    print()
    print("  The post coefficient is biased by one continuing pre-period")
    print("  first-difference, so the naive CI -- which assumes the trend stops --")
    print("  misses the truth; allowing the post violation to be M=1 times the")
    print("  pre violation restores honest coverage.")

    pdf = make_figure(cov)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    numeric_check("naive CI under-covers under a continuing pre-trend", cov["naive"], hi=0.90)
    numeric_check("honest-DiD coverage at M=1 restores ~nominal", cov_at_1, lo=0.94)
    numeric_check("honest-DiD M=0 equals naive coverage",
                  abs(cov["by_m"][0] - cov["naive"]), hi=1e-9)
    numeric_check("coverage is non-decreasing in M", cov["by_m"][-1], lo=cov_at_1)
    print("\nAll assertions passed: a continuing pre-trend breaks naive "
          "parallel-trends\ncoverage; the relative-magnitudes honest CI restores "
          "it by M = 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
