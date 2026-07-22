#!/usr/bin/env python3
"""Power/MDE demo: ex-ante design discipline and the underpowered-study trap.

A runnable companion to docs/methods-reference.md and the aer-preregistration
skill. It makes two points a pre-analysis plan must settle before any data are
collected. First, the minimum detectable effect (MDE) formula is not folklore:
the analytic MDE for a two-arm trial,

    MDE = (z_power + z_{1-alpha/2}) * sigma * sqrt(1 / (p (1 - p) N)),

is exactly the true effect at which a design attains its target power, and a
Monte Carlo confirms it to the third decimal. Second -- and this is why AEA
referees care -- an *underpowered* design is not merely "less likely to find the
effect." Conditional on reaching significance, its estimates are inflated: the
Type-M (exaggeration) ratio of Gelman and Carlin. A study powered at 28% does
not just miss most of the time; when it "wins," it overstates the effect by a
large factor. Pre-registration and honest power calculations exist to keep that
winner's curse out of the published record.

Every claim is checked by simulation against the analytic target. The script
asserts, over a Monte Carlo, that (1) the analytic MDE delivers the target 80%
power, (2) a design at half the MDE is badly underpowered, (3) the test holds
its nominal size under the null, and (4) the underpowered design exaggerates the
effect among significant estimates while the well-powered one barely does. It
exits non-zero on any failure, so the demo doubles as a regression test.

Run:  python3 power_mde_demo.py
Deps: numpy, scipy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: mckenzie_2012 and duflo_glennerster_kremer_2007 in
../../references.bib. See ../../docs/methods-reference.md for the per-stack
tooling and ../../skills/aer-preregistration/SKILL.md for where power sits in the
pre-analysis plan.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")  # headless: write files, never open a window
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _aer_numeric_check import numeric_check  # noqa: E402

SEED = 20260101                       # repository-wide fixed seed
N = 1000                              # total sample size (two arms)
SIGMA = 1.0                           # outcome standard deviation
P_TREAT = 0.5                         # treatment allocation share
ALPHA = 0.05                          # two-sided test size
TARGET_POWER = 0.80                   # conventional power target
REPS = 4000                           # Monte Carlo repetitions
OUT = Path(__file__).resolve().parent / "output"


def analytic_mde() -> float:
    """Minimum detectable effect for a two-arm difference in means at
    TARGET_POWER and ALPHA, equal-variance normal outcomes."""
    z_power = stats.norm.ppf(TARGET_POWER)
    z_alpha = stats.norm.ppf(1.0 - ALPHA / 2.0)
    se_unit = SIGMA * np.sqrt(1.0 / (P_TREAT * (1.0 - P_TREAT) * N))
    return (z_power + z_alpha) * se_unit


def simulate(rng: np.random.Generator, delta: float) -> tuple[float, float]:
    """Monte Carlo a two-arm trial at true effect ``delta``. Returns
    (rejection rate, exaggeration ratio), where the exaggeration ratio is the
    mean absolute estimate among significant replications divided by the true
    effect (undefined -> NaN when delta is 0 or nothing is significant)."""
    z_alpha = stats.norm.ppf(1.0 - ALPHA / 2.0)
    rejections = 0
    sig_abs_estimates: list[float] = []
    for _ in range(REPS):
        treat = rng.random(N) < P_TREAT
        y = delta * treat + rng.normal(0.0, SIGMA, N)
        y1, y0 = y[treat], y[~treat]
        diff = float(y1.mean() - y0.mean())
        se = np.sqrt(y1.var(ddof=1) / y1.size + y0.var(ddof=1) / y0.size)
        if abs(diff / se) > z_alpha:
            rejections += 1
            sig_abs_estimates.append(abs(diff))
    power = rejections / REPS
    if delta == 0.0 or not sig_abs_estimates:
        return power, float("nan")
    return power, float(np.mean(sig_abs_estimates)) / delta


def make_figure(mde: float, grid: np.ndarray, powers: np.ndarray) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(grid / mde, powers, marker="o", color="black",
            label="Simulated power")
    ax.axhline(TARGET_POWER, color="firebrick", linestyle=":", linewidth=1.2,
               label=f"Target power = {TARGET_POWER:.0%}")
    ax.axvline(1.0, color="grey", linestyle="--", linewidth=1.0)
    ax.annotate("MDE", (1.0, 0.05), textcoords="offset points", xytext=(6, 0),
                fontsize=9, color="grey")
    ax.axhline(ALPHA, color="darkorange", linestyle=":", linewidth=1.0,
               label=f"Size under null = {ALPHA:.2f}")
    ax.set_xlabel("True effect as a multiple of the MDE")
    ax.set_ylabel("Power (simulated rejection rate)")
    ax.set_ylim(0, 1.02)
    ax.set_title("The analytic MDE is exactly the 80%-power effect")
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.tight_layout()
    pdf = OUT / "power_mde.pdf"
    fig.savefig(pdf)                        # vector, for inclusion in a paper
    fig.savefig(OUT / "power_mde.png", dpi=150)  # raster, for the README
    plt.close(fig)
    return pdf


def main() -> int:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    mde = analytic_mde()

    power_mde, exag_mde = simulate(rng, mde)
    power_half, exag_half = simulate(rng, 0.5 * mde)
    power_null, _ = simulate(rng, 0.0)

    # Power curve for the figure (fresh rng draws along a grid).
    grid = mde * np.array([0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
    powers = np.array([simulate(rng, float(d))[0] for d in grid])

    print("=" * 70)
    print("Power and the minimum detectable effect (two-arm trial)")
    print(f"  N={N}  sigma={SIGMA}  p={P_TREAT}  alpha={ALPHA}  "
          f"target power={TARGET_POWER}")
    print(f"  reps={REPS}  seed={SEED}")
    print("=" * 70)
    print(f"  Analytic MDE                         : {mde:.4f}")
    print(f"  Simulated power at the MDE           : {power_mde:.3f}  "
          f"(target {TARGET_POWER:.2f})")
    print(f"  Simulated power at half the MDE      : {power_half:.3f}  "
          f"(underpowered)")
    print(f"  Rejection rate under the null        : {power_null:.3f}  "
          f"(size {ALPHA:.2f})")
    print()
    print(f"  Exaggeration (Type-M) ratio at MDE   : {exag_mde:.2f}x")
    print(f"  Exaggeration ratio at half the MDE   : {exag_half:.2f}x")
    print("    -> the underpowered design, WHEN significant, overstates the")
    print("       effect substantially: the winner's curse a pre-analysis plan")
    print("       and an honest power calculation are meant to prevent.")

    pdf = make_figure(mde, grid, powers)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    numeric_check("analytic MDE delivers the target 80% power",
                  power_mde, target=TARGET_POWER, tol=0.03)
    numeric_check("a design at half the MDE is badly underpowered",
                  power_half, hi=0.40)
    numeric_check("the test holds its nominal size under the null",
                  power_null, target=ALPHA, tol=0.02)
    numeric_check("the underpowered design exaggerates the effect (Type-M)",
                  exag_half, lo=1.4)
    numeric_check("the well-powered design barely exaggerates",
                  exag_mde, hi=1.25)
    print(f"\nAll assertions passed in {time.time() - t0:.1f}s: the analytic MDE "
          "attains target power,\nand the underpowered design inflates the effect "
          "it manages to detect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
