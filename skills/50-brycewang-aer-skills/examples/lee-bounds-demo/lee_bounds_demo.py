#!/usr/bin/env python3
"""Lee-bounds demo: differential attrition breaks point ID; trimming bounds it.

A runnable companion to docs/methods-reference.md and the aer-robustness /
aer-identification skills. It makes the Lee (2009) point: when a randomized
treatment changes who is *observed* -- differential attrition, or selection into
employment in the training-program example -- the naive contrast of observed
outcomes across arms is biased for any causal effect, because the selected
samples are no longer comparable. Randomization does not save you: it balances
the arms at assignment, not among survivors.

Lee's fix is *partial* identification. Under a monotonicity assumption -- the
treatment moves selection in one direction only, so there is a well-defined
subpopulation ("always-selected") observed in both arms -- the effect on that
subpopulation is bounded, not point-identified. Construction: the arm with the
higher selection rate contains a known share q of extra, marginal units. Trim
the q fraction of that arm's outcome distribution from one tail to get each
bound -- trim the low tail for the upper bound, the high tail for the lower
bound -- and difference against the other arm's selected mean. The width of the
interval is the honest price of the attrition.

The data-generating process is fully known -- always-takers with a true effect
of 2.0, plus low-outcome marginal units that appear only under treatment -- so
the script computes the truth analytically and *asserts*, over a Monte Carlo,
that (1) the Lee interval covers the true always-taker effect, (2) the naive
observed-outcome contrast misses it by a wide margin, (3) the interval has
strictly positive width (this is partial, not point, identification), and
(4) a placebo world with symmetric attrition collapses the interval back to
point identification. It exits non-zero on any failure, so the demo doubles as
a regression test.

Run:  python3 lee_bounds_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: lee_2009 in ../../references.bib. See ../../docs/methods-reference.md
for the per-stack tooling (`leebounds` in Stata) and
../../skills/aer-robustness/SKILL.md for where attrition sits in the referee
checklist.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")  # headless: write files, never open a window
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _aer_numeric_check import numeric_check  # noqa: E402

SEED = 20260101                       # repository-wide fixed seed
N = 4000                              # sample size per replication
# Population shares of the three latent selection types. Always-takers are
# observed regardless of assignment; marginals are observed ONLY under
# treatment (treatment weakly increases selection -- the Lee monotonicity
# assumption); never-observed units never enter the outcome sample.
SHARE_ALWAYS = 0.50
SHARE_MARGINAL = 0.25
# Outcome means. The always-taker effect is the estimand Lee bounds target;
# marginals appear only when treated and are LOW-outcome units (the classic
# "marginal workers pulled into employment earn little" pattern), so the naive
# contrast is biased downward.
MU_ALWAYS_CONTROL = 0.0
MU_ALWAYS_TREAT = 2.0                 # -> true always-taker effect = 2.0
MU_MARGINAL_TREAT = -1.0
OUTCOME_SD = 1.0
TRUE_EFFECT = MU_ALWAYS_TREAT - MU_ALWAYS_CONTROL
REPS = 300                            # Monte Carlo repetitions
OUT = Path(__file__).resolve().parent / "output"


def simulate(rng: np.random.Generator, share_marginal: float
             ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One randomized sample. Returns (T, S, Y): assignment, selection/observed
    indicator, and outcome (NaN where not observed). ``share_marginal`` lets the
    placebo turn differential attrition off."""
    share_never = 1.0 - SHARE_ALWAYS - share_marginal
    T = rng.integers(0, 2, N)                              # random assignment
    grp = rng.choice([0, 1, 2], size=N,
                     p=[SHARE_ALWAYS, share_marginal, share_never])
    # 0 = always-selected, 1 = marginal (selected iff treated), 2 = never.
    S = np.where(grp == 0, 1, np.where((grp == 1) & (T == 1), 1, 0))
    Y = np.full(N, np.nan)
    always = grp == 0
    Y[always] = np.where(T[always] == 1, MU_ALWAYS_TREAT, MU_ALWAYS_CONTROL)
    Y[always] += rng.normal(0.0, OUTCOME_SD, int(always.sum()))
    marg = (grp == 1) & (T == 1)
    Y[marg] = MU_MARGINAL_TREAT + rng.normal(0.0, OUTCOME_SD, int(marg.sum()))
    return T, S, Y


def lee_bounds(T: np.ndarray, S: np.ndarray, Y: np.ndarray
               ) -> tuple[float, float, float]:
    """Lee (2009) trimming bounds and the naive observed contrast. Assumes
    treatment weakly increases selection (s1 >= s0), so the treated arm holds
    the extra marginal units and gets trimmed. Returns (lower, upper, naive)."""
    s1 = S[T == 1].mean()
    s0 = S[T == 0].mean()
    keep = min(1.0, s0 / s1)               # share of treated-selected to keep
    y1 = Y[(T == 1) & (S == 1)]            # treated, observed
    y0_mean = float(Y[(T == 0) & (S == 1)].mean())   # control, observed
    naive = float(y1.mean()) - y0_mean
    if keep >= 1.0:                        # no differential attrition -> point ID
        return naive, naive, naive
    lo_cut = np.quantile(y1, keep)         # keep the bottom `keep` fraction
    hi_cut = np.quantile(y1, 1.0 - keep)   # keep the top `keep` fraction
    lower = float(y1[y1 <= lo_cut].mean()) - y0_mean
    upper = float(y1[y1 >= hi_cut].mean()) - y0_mean
    return lower, upper, naive


def run_montecarlo(rng: np.random.Generator, share_marginal: float
                   ) -> tuple[float, float, float]:
    """Monte Carlo means of (lower, upper, naive) across REPS."""
    lows = np.empty(REPS)
    ups = np.empty(REPS)
    naives = np.empty(REPS)
    for r in range(REPS):
        T, S, Y = simulate(rng, share_marginal)
        lows[r], ups[r], naives[r] = lee_bounds(T, S, Y)
    return float(lows.mean()), float(ups.mean()), float(naives.mean())


def make_figure(lower: float, upper: float, naive: float) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.axvline(TRUE_EFFECT, color="firebrick", linestyle=":", linewidth=1.4,
               label=f"True always-taker effect = {TRUE_EFFECT:.1f}")
    ax.plot([lower, upper], [1, 1], color="black", linewidth=3,
            solid_capstyle="butt", label="Lee bounds [LB, UB]")
    ax.plot([lower, upper], [1, 1], "|", color="black", markersize=16,
            markeredgewidth=2)
    ax.plot(naive, 0.6, "^", color="darkorange", markersize=11,
            label="Naive observed-outcome contrast (biased)")
    ax.set_yticks([])
    ax.set_ylim(0.2, 1.4)
    ax.set_xlabel("Treatment effect on the outcome")
    ax.set_title("Lee bounds bracket the truth that differential attrition hides")
    ax.legend(frameon=False, fontsize=9, loc="lower center",
              bbox_to_anchor=(0.5, -0.02), ncol=1)
    fig.tight_layout()
    pdf = OUT / "lee_bounds.pdf"
    fig.savefig(pdf)                        # vector, for inclusion in a paper
    fig.savefig(OUT / "lee_bounds.png", dpi=150)  # raster, for the README
    plt.close(fig)
    return pdf


def main() -> int:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    lower, upper, naive = run_montecarlo(rng, SHARE_MARGINAL)
    # Placebo: symmetric attrition (no marginals) -> selection is balanced,
    # the monotonicity trim is zero, and the bounds collapse to point ID.
    lower0, upper0, naive0 = run_montecarlo(rng, 0.0)

    print("=" * 70)
    print("Lee (2009) trimming bounds under differential attrition")
    print(f"  N={N}  reps={REPS}  seed={SEED}")
    print(f"  always-selected share={SHARE_ALWAYS}  marginal share={SHARE_MARGINAL}")
    print(f"  true always-taker effect = {TRUE_EFFECT:.2f}")
    print("=" * 70)
    print(f"  Naive observed-outcome contrast : {naive:.3f}  "
          f"(bias {naive - TRUE_EFFECT:+.3f})")
    print(f"  Lee bounds                      : [{lower:.3f}, {upper:.3f}]  "
          f"(width {upper - lower:.3f})")
    print(f"  Truth inside the interval       : "
          f"{lower <= TRUE_EFFECT <= upper}")
    print()
    print(f"  Placebo (symmetric attrition)   : [{lower0:.3f}, {upper0:.3f}]  "
          f"(width {upper0 - lower0:.3f})")
    print("  With no differential attrition the trim is zero and the interval")
    print("  collapses to the point-identified experimental effect.")

    pdf = make_figure(lower, upper, naive)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known target and emits a
    # NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("Lee lower bound sits at or below the truth",
                  lower, hi=TRUE_EFFECT + 0.05)
    numeric_check("Lee upper bound sits at or above the truth",
                  upper, lo=TRUE_EFFECT - 0.05)
    numeric_check("naive attrition-biased contrast misses the truth",
                  abs(naive - TRUE_EFFECT), lo=0.5)
    numeric_check("Lee interval has positive width (partial identification)",
                  upper - lower, lo=0.3)
    numeric_check("placebo with symmetric attrition collapses toward point ID",
                  (upper0 - lower0) / (upper - lower), hi=0.05)
    print(f"\nAll assertions passed in {time.time() - t0:.1f}s: the trimming "
          "bounds bracket the true\neffect that the naive observed-outcome "
          "contrast cannot recover under attrition.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
