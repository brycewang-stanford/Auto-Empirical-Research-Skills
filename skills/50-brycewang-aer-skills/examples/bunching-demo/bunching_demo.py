#!/usr/bin/env python3
"""Bunching demo: recovering an elasticity from excess mass at a kink.

A runnable companion to docs/methods-reference.md and the aer-identification
skill. It simulates the Saez (2010) kink design: earnings respond to the
net-of-tax rate with a KNOWN iso-elastic elasticity e, the marginal tax rate
rises from t0 to t1 at a kink z*, and every worker whose counterfactual
earnings would fall in (z*, z* + dz*] bunches at the kink, where

    dz*/z* = ((1 - t0)/(1 - t1))**e - 1     (exact in the iso-elastic model).

The excess mass b at the kink, normalized by the counterfactual density,
estimates dz*, and inverting the identity recovers the elasticity:

    e_hat = log(1 + b/z*) / log((1 - t0)/(1 - t1)).

Three passes run on the same simulated earnings distributions:

  1. Oracle -- the exact bunching mass (we know who bunched in simulation)
     normalized by the true no-kink density. This isolates the Saez formula:
     its only remaining error is the small-kink approximation itself (the
     counterfactual density is not flat across the bunching segment), which
     is why the check allows e_hat a few points below the truth.
  2. Feasible estimator -- the standard empirical pipeline: bin the observed
     earnings, fit a polynomial to the bin counts EXCLUDING a window around
     the kink, take the fitted counts as the counterfactual (Kleven 2016).
  3. Falsification passes -- the same pipeline on a world with NO kink
     (placebo) and on a kinked world with ZERO elasticity. Both must show
     no excess mass: the pipeline may not invent bunching.

Because the elasticity, the kink, and the tax rates are all chosen by us,
the demo doubles as a regression test and exits non-zero if any check drifts.

Run:  python3 bunching_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: saez_2010 and kleven_2016 in ../../references.bib.
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
N = 200_000               # workers per Monte Carlo panel
REPS = 30                 # Monte Carlo panels
E_TRUE = 0.5              # the truth: compensated earnings elasticity
T0, T1 = 0.20, 0.24       # marginal tax below / above the kink (small kink)
KINK = 40_000.0           # kink location z*
MU, SIGMA = 10.35, 0.55   # lognormal ability scale
NOISE_SD = 0.006          # optimization-friction noise (log points)
BIN_W = 400.0             # histogram bin width
FIT_LO, FIT_HI = 25_000.0, 60_000.0   # fitting range
EXCL_LO, EXCL_HI = -4, 6  # excluded bins around the kink bin
POLY_DEG = 6              # counterfactual polynomial degree
OUT = Path(__file__).resolve().parent / "output"

LOG_NTR = np.log((1.0 - T0) / (1.0 - T1))     # log net-of-tax-rate change
DZ_STAR = KINK * (((1.0 - T0) / (1.0 - T1)) ** E_TRUE - 1.0)


def simulate_earnings(rng: np.random.Generator,
                      elasticity: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Observed earnings, the no-kink counterfactual, and the buncher mask."""
    n_ability = rng.lognormal(MU, SIGMA, size=N)
    z0 = n_ability * (1.0 - T0) ** elasticity     # choice if t0 applied everywhere
    z1 = n_ability * (1.0 - T1) ** elasticity     # choice if t1 applied everywhere
    bunched = (z0 > KINK) & (z1 <= KINK)
    z = np.where(z0 <= KINK, z0, np.where(z1 > KINK, z1, KINK))
    noise = np.exp(rng.normal(0.0, NOISE_SD, size=N))
    return z * noise, z0 * noise, bunched


def bin_counts(z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    edges = np.arange(FIT_LO, FIT_HI + BIN_W, BIN_W)
    counts, _ = np.histogram(z, bins=edges)
    centers = edges[:-1] + BIN_W / 2.0
    return centers, counts.astype(float)


def elasticity_from_dz(dz: float) -> float:
    """Invert the iso-elastic bunching identity: bunching window -> elasticity."""
    return float(np.log1p(max(dz, 0.0) / KINK) / LOG_NTR)


def window_density(centers: np.ndarray, cf_counts: np.ndarray,
                   kink: float) -> float:
    """Counterfactual density averaged over the exclusion window.

    Expressed per dollar as a share of ALL N workers, so it is directly
    comparable to worker-share masses (the exact buncher share in the oracle
    pass uses the same denominator)."""
    k = int(np.argmin(np.abs(centers - kink)))
    window = slice(k + EXCL_LO, k + EXCL_HI + 1)
    return float(cf_counts[window].mean()) / N / BIN_W


def window_excess(centers: np.ndarray, counts: np.ndarray,
                  cf_counts: np.ndarray, kink: float) -> tuple[float, float]:
    """Excess mass share in the window and the normalized excess dz-hat."""
    k = int(np.argmin(np.abs(centers - kink)))
    window = slice(k + EXCL_LO, k + EXCL_HI + 1)
    excess = float((counts[window] - cf_counts[window]).sum()) / N
    h0 = window_density(centers, cf_counts, kink)
    return excess, excess / max(h0, 1e-300)


def polynomial_counterfactual(centers: np.ndarray, counts: np.ndarray,
                              kink: float) -> np.ndarray:
    """Standard bunching counterfactual: polynomial fit excluding the window."""
    k = int(np.argmin(np.abs(centers - kink)))
    mask = np.ones_like(counts, dtype=bool)
    mask[k + EXCL_LO:k + EXCL_HI + 1] = False
    x = (centers - kink) / 10_000.0            # scale for polynomial stability
    coef = np.polyfit(x[mask], counts[mask], POLY_DEG)
    return np.clip(np.polyval(coef, x), 0.0, None)


def run_montecarlo(rng: np.random.Generator) -> dict:
    acc: dict[str, list[float]] = {"oracle": [], "feasible": [],
                                   "placebo": [], "zero_e": []}
    for _ in range(REPS):
        z, z0, bunched = simulate_earnings(rng, E_TRUE)
        centers, counts = bin_counts(z)
        _, cf_true = bin_counts(z0)

        # Oracle: exact bunching mass over the true counterfactual density.
        h0 = window_density(centers, cf_true, KINK)
        dz_oracle = float(bunched.mean()) / h0
        acc["oracle"].append(elasticity_from_dz(dz_oracle))

        # Feasible: polynomial counterfactual from the observed bins alone.
        cf_fit = polynomial_counterfactual(centers, counts, KINK)
        _, dz_fit = window_excess(centers, counts, cf_fit, KINK)
        acc["feasible"].append(elasticity_from_dz(dz_fit))

        # Placebo: same pipeline on the smooth no-kink world.
        c0, counts0 = bin_counts(z0)
        cf_plac = polynomial_counterfactual(c0, counts0, KINK)
        _, dz_plac = window_excess(c0, counts0, cf_plac, KINK)
        acc["placebo"].append(dz_plac / KINK)

        # Zero-elasticity world: a kink with e = 0 must show no bunching.
        z_e0, _, _ = simulate_earnings(rng, 0.0)
        ce, counts_e0 = bin_counts(z_e0)
        cf_e0 = polynomial_counterfactual(ce, counts_e0, KINK)
        _, dz_e0 = window_excess(ce, counts_e0, cf_e0, KINK)
        acc["zero_e"].append(dz_e0 / KINK)
    return {k: float(np.mean(v)) for k, v in acc.items()}


def make_figure(rng: np.random.Generator) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    z, z0, _ = simulate_earnings(rng, E_TRUE)
    centers, counts = bin_counts(z)
    _, cf_true = bin_counts(z0)
    cf_fit = polynomial_counterfactual(centers, counts, KINK)

    lo, hi = KINK - 8_000, KINK + 8_000
    sel = (centers >= lo) & (centers <= hi)
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    ax.bar(centers[sel], counts[sel], width=BIN_W * 0.9, color="lightsteelblue",
           label="observed earnings (kinked schedule)")
    ax.plot(centers[sel], cf_true[sel], color="black", linewidth=1.4,
            label="true counterfactual (no kink)")
    ax.plot(centers[sel], cf_fit[sel], color="firebrick", linestyle="--",
            linewidth=1.4, label="polynomial counterfactual (excl. window)")
    ax.axvline(KINK, color="grey", linestyle=":", label=f"kink z* = {KINK:,.0f}")
    ax.axvspan(KINK, KINK + DZ_STAR, color="orange", alpha=0.2,
               label="theoretical bunching segment dz*")
    ax.set_xlabel("Earnings")
    ax.set_ylabel("Workers per bin")
    ax.set_title("Bunching at a kink: excess mass over the counterfactual identifies e")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    pdf = OUT / "bunching.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "bunching.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    m = run_montecarlo(rng)

    print("=" * 70)
    print("Bunching at a kink: excess mass -> elasticity (Saez identification)")
    print(f"  N={N:,}  reps={REPS}  e_true={E_TRUE}  t0={T0}  t1={T1}"
          f"  z*={KINK:,.0f}  seed={SEED}")
    print("=" * 70)
    print(f"  theoretical bunching segment dz* = {DZ_STAR:,.0f}"
          f"  ({DZ_STAR / KINK:.2%} of z*)")
    print(f"  oracle (exact mass, true density)   e_hat = {m['oracle']:.3f}")
    print(f"  feasible polynomial pipeline        e_hat = {m['feasible']:.3f}")
    print(f"  placebo (no-kink world)     dz-hat/z* = {m['placebo']:+.4f}")
    print(f"  zero-elasticity kinked world dz-hat/z* = {m['zero_e']:+.4f}")
    print()
    print("  the oracle's small shortfall from 0.5 is the small-kink")
    print("  approximation itself (the density declines across the bunching")
    print("  segment) -- the estimation caveat catalogued in Kleven (2016).")

    pdf = make_figure(rng)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known target and emits a
    # NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("oracle bunching formula recovers e (small-kink approx)",
                  m["oracle"], target=E_TRUE, tol=0.06)
    numeric_check("feasible polynomial pipeline recovers e", m["feasible"],
                  target=E_TRUE, tol=0.10)
    numeric_check("no-kink placebo shows no bunching", m["placebo"],
                  target=0.0, tol=0.01)
    numeric_check("zero-elasticity kink shows no bunching", m["zero_e"],
                  target=0.0, tol=0.01)
    print("\nAll assertions passed: the excess-mass formula recovers the true")
    print("elasticity, and both falsification worlds show no invented bunching.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
