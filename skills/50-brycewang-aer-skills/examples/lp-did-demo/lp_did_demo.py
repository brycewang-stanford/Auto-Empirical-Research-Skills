#!/usr/bin/env python3
"""LP-DiD demo: local projections with clean controls fix the pooled event study.

A runnable companion to docs/methods-reference.md and the aer-identification
skill. It makes the Dube-Girardi-Jorda-Taylor (2023) point: under staggered
adoption with dynamic, cohort-heterogeneous treatment effects, the pooled
distributed-lag TWFE event study is NOT an average of the true dynamic effects.
Already-treated units (whose effects are still growing) sneak into the implicit
control group -- the Goodman-Bacon "forbidden comparison" -- and the lag
coefficients become non-convex weighted mixtures of effects at *other* horizons
and cohorts. LP-DiD repairs this with the local-projection idea of Jorda
(2005): for each horizon h, regress the long difference y_{t+h} - y_{t-1} on
the treatment-switch indicator using ONLY clean controls (units not yet
treated through t+h, including never-treated), absorbing period effects. Each
horizon is its own clean 2x2 comparison, so no forbidden comparison can
contaminate it.

The data-generating process is fully known -- effects grow with event time and
differ across cohorts, exactly the pattern that breaks pooled TWFE -- so the
script computes the true average dynamic path ATT(h) from the same parameters,
weighted the same way the equally-weighted LP-DiD estimand weights (equally
across treated (unit, event-time-h) observations that enter the estimator). It
then *asserts*, over a Monte Carlo, that LP-DiD recovers ATT(h) at both short
and long horizons, that the pooled TWFE event study is materially contaminated
at the long horizon, and that the LP-DiD pre-treatment placebo (the long
difference y_{t-2} - y_{t-1} on switchers) is null -- exiting non-zero on any
failure, so the demo doubles as a regression test.

Run:  python3 lp_did_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: dube_girardi_jorda_taylor_2023 and jorda_2005 in
../../references.bib. See ../../docs/methods-reference.md for the per-stack
tooling and ../../skills/aer-identification/SKILL.md for the design context.
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
N_UNITS = 200                         # panel width
N_PERIODS = 20                        # panel length (t = 1..20)
# Adoption period -> per-event-time effect slope: cohort g's true effect at
# event time h is SLOPE[g] * (h + 1). Effects GROW with event time and DIFFER
# across cohorts -- exactly what turns pooled TWFE lags into contaminated
# mixtures. g = 0 marks the never-treated group.
COHORT_SLOPES = {6: 1.5, 10: 0.5, 14: 0.1, 0: 0.0}
COHORT_PROBS = (0.25, 0.25, 0.25, 0.25)
NOISE_SD = 0.5                        # idiosyncratic shock
TIME_SHOCK_SD = 0.5                   # common period shock (absorbed by FE)
HORIZONS = (0, 1, 2, 3)               # LP-DiD / comparison horizons
TWFE_LEAD_BIN = -5                    # TWFE event study: leads binned at -5
TWFE_LAG_BIN = 8                      # ... and lags binned at 8+ (ref = -1)
REPS = 200                            # Monte Carlo repetitions
OUT = Path(__file__).resolve().parent / "output"


def simulate_panel(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """One staggered-adoption panel. Returns (cohort g per unit, Y of shape
    (N_UNITS, N_PERIODS)); Y[i, t-1] is unit i's outcome in period t."""
    cohorts = np.array(list(COHORT_SLOPES))
    g = rng.choice(cohorts, size=N_UNITS, p=COHORT_PROBS)
    alpha = rng.normal(0.0, 1.0, N_UNITS) + 0.25 * g   # unit FE, cohort-shifted
    delta = 0.10 * np.arange(1, N_PERIODS + 1)         # common trend ...
    delta = delta + rng.normal(0.0, TIME_SHOCK_SD, N_PERIODS)  # ... + shocks
    t_grid = np.arange(1, N_PERIODS + 1)[None, :]      # (1, T)
    event = t_grid - g[:, None]                        # event time t - g
    treated = (g[:, None] > 0) & (event >= 0)
    slope = np.array([COHORT_SLOPES[int(c)] for c in g])[:, None]
    tau = np.where(treated, slope * (event + 1), 0.0)  # dynamic true effect
    Y = alpha[:, None] + delta[None, :] + tau + rng.normal(
        0.0, NOISE_SD, (N_UNITS, N_PERIODS))
    return g, Y


def true_att_path(g: np.ndarray) -> np.ndarray:
    """True ATT(h) for h in HORIZONS, weighted exactly like the equally-
    weighted LP-DiD estimand: equally across treated (unit, event-time-h)
    observations that enter the estimator. Every treated cohort here reaches
    every horizon inside the panel with never-treated clean controls, so each
    treated unit contributes one horizon-h observation and
    ATT(h) = mean over treated units of SLOPE[g_i] * (h + 1)."""
    slopes = np.array([COHORT_SLOPES[int(c)] for c in g[g > 0]])
    return np.array([float(slopes.mean()) * (h + 1) for h in HORIZONS])


def lp_did(g: np.ndarray, Y: np.ndarray, h: int) -> float:
    """Equally-weighted LP-DiD at horizon h (Dube et al. 2023). For each
    switch period t, take the long difference y_{t+h} - y_{t-1} for units
    switching into treatment at t versus CLEAN controls only (never-treated or
    not yet treated through t+h). Period fixed effects are absorbed by
    demeaning within t: the within-period switcher-vs-clean difference in
    means IS the period-FE regression, and averaging those differences with
    switcher-count weights gives the estimator that weights every treated
    (unit, h) observation equally -- the same weighting as true_att_path."""
    num, den = 0.0, 0
    for t in sorted(int(c) for c in np.unique(g) if c > 0):
        if t - 1 < 1 or t + h > N_PERIODS:
            continue                       # long difference must fit the panel
        switch = g == t
        clean = (g == 0) | (g > t + h)     # not yet treated through t+h
        if not switch.any() or not clean.any():
            continue
        dy = Y[:, t + h - 1] - Y[:, t - 2]           # y_{t+h} - y_{t-1}
        num += switch.sum() * float(dy[switch].mean() - dy[clean].mean())
        den += int(switch.sum())
    return num / den


def lp_did_placebo(g: np.ndarray, Y: np.ndarray) -> float:
    """Pre-treatment placebo: the long difference y_{t-2} - y_{t-1} on
    switchers at t vs clean controls (not yet treated through t). Both periods
    predate treatment for everyone in the sample, so under parallel trends the
    estimate is ~0."""
    num, den = 0.0, 0
    for t in sorted(int(c) for c in np.unique(g) if c > 0):
        if t - 2 < 1:
            continue
        switch = g == t
        clean = (g == 0) | (g > t)
        if not switch.any() or not clean.any():
            continue
        dy = Y[:, t - 3] - Y[:, t - 2]               # y_{t-2} - y_{t-1}
        num += switch.sum() * float(dy[switch].mean() - dy[clean].mean())
        den += int(switch.sum())
    return num / den


def twfe_event_study(g: np.ndarray, Y: np.ndarray) -> dict[int, float]:
    """Pooled distributed-lag TWFE event study: y on unit FE + time FE + lead
    and lag dummies (leads binned at TWFE_LEAD_BIN, lags at TWFE_LAG_BIN+,
    reference event time -1; never-treated units carry all-zero dummies).
    Estimated by exact two-way within-demeaning of the balanced panel followed
    by OLS via numpy lstsq. Returns the lag-h coefficients for h in HORIZONS.
    Under cohort-heterogeneous dynamic effects these coefficients are
    contaminated mixtures (the DGJT / Sun-Abraham critique)."""
    event = np.arange(1, N_PERIODS + 1)[None, :] - g[:, None]   # (N, T)
    is_tr = g[:, None] > 0
    bins = [b for b in range(TWFE_LEAD_BIN, TWFE_LAG_BIN + 1) if b != -1]
    cols = []
    for b in bins:
        if b == TWFE_LEAD_BIN:
            d = is_tr & (event <= b)
        elif b == TWFE_LAG_BIN:
            d = is_tr & (event >= b)
        else:
            d = is_tr & (event == b)
        cols.append(d.astype(float))
    X = np.stack(cols, axis=-1)                       # (N, T, K)

    def demean2(a: np.ndarray) -> np.ndarray:
        """Exact two-way (unit + time) within transform on a balanced panel."""
        return (a - a.mean(axis=0, keepdims=True)
                  - a.mean(axis=1, keepdims=True) + a.mean())

    Xd = np.stack([demean2(X[:, :, k]) for k in range(X.shape[-1])], axis=-1)
    yd = demean2(Y).ravel()
    beta, *_ = np.linalg.lstsq(Xd.reshape(-1, X.shape[-1]), yd, rcond=None)
    return {h: float(beta[bins.index(h)]) for h in HORIZONS}


def run_montecarlo(rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Monte Carlo means of the true path and all estimators across REPS."""
    truth = np.zeros((REPS, len(HORIZONS)))
    lp = np.zeros((REPS, len(HORIZONS)))
    twfe = np.zeros((REPS, len(HORIZONS)))
    placebo = np.zeros(REPS)
    for r in range(REPS):
        g, Y = simulate_panel(rng)
        truth[r] = true_att_path(g)
        lp[r] = [lp_did(g, Y, h) for h in HORIZONS]
        tw = twfe_event_study(g, Y)
        twfe[r] = [tw[h] for h in HORIZONS]
        placebo[r] = lp_did_placebo(g, Y)
    return {"truth": truth.mean(axis=0), "lp": lp.mean(axis=0),
            "twfe": twfe.mean(axis=0), "placebo": np.array([placebo.mean()])}


def make_figure(m: dict[str, np.ndarray]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    hs = np.array(HORIZONS, dtype=float)
    ax.axhline(0.0, color="grey", linewidth=0.8)
    ax.axvline(-0.5, color="grey", linestyle="--", linewidth=0.8)
    ax.plot(hs, m["truth"], linestyle=":", marker="s", color="firebrick",
            label="True ATT(h)")
    ax.plot(hs, m["lp"], marker="o", color="black",
            label="LP-DiD (clean controls)")
    ax.plot(np.append(-2.0, hs), np.append(m["placebo"][0], m["lp"]),
            linestyle="", marker="o", color="black")
    ax.annotate("placebo", (-2.0, m["placebo"][0]), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=8, color="black")
    ax.plot(hs, m["twfe"], marker="^", color="darkorange",
            label="Pooled TWFE event study (contaminated)")
    ax.set_xlabel("Horizon h (event time relative to treatment)")
    ax.set_ylabel("Effect on outcome")
    ax.set_title("LP-DiD tracks the true dynamic path; pooled TWFE does not")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    pdf = OUT / "lp_did.pdf"
    fig.savefig(pdf)                        # vector, for inclusion in a paper
    fig.savefig(OUT / "lp_did.png", dpi=150)  # raster, for the README
    plt.close(fig)
    return pdf


def main() -> int:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    m = run_montecarlo(rng)
    placebo = float(m["placebo"][0])
    twfe_gap3 = abs(float(m["twfe"][3]) - float(m["truth"][3]))

    print("=" * 70)
    print("LP-DiD (Dube-Girardi-Jorda-Taylor) vs pooled TWFE event study")
    print(f"  units={N_UNITS}  periods={N_PERIODS}  reps={REPS}  seed={SEED}")
    print(f"  cohorts (adoption -> slope): "
          + ", ".join(f"{k}->{v}" for k, v in COHORT_SLOPES.items() if k > 0)
          + "  (0 = never treated)")
    print("=" * 70)
    print(f"  {'h':>3}  {'true ATT(h)':>12}  {'LP-DiD':>10}  {'pooled TWFE':>12}")
    for j, h in enumerate(HORIZONS):
        print(f"  {h:>3}  {m['truth'][j]:>12.3f}  {m['lp'][j]:>10.3f}"
              f"  {m['twfe'][j]:>12.3f}")
    print(f"  LP-DiD pre-treatment placebo (y_t-2 - y_t-1): {placebo:.3f}")
    print()
    print("  LP-DiD's clean-control long differences track the true path at")
    print("  every horizon; the pooled TWFE lag coefficients are contaminated")
    print(f"  mixtures (off by {twfe_gap3:.2f} at h=3, "
          f"{100 * twfe_gap3 / m['truth'][3]:.0f}% of the true effect),")
    print("  because already-treated units with still-growing effects enter")
    print("  the implicit control group (the forbidden comparison).")

    pdf = make_figure(m)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known target and emits a
    # NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("LP-DiD recovers ATT at h=0",
                  m["lp"][0], target=float(m["truth"][0]), tol=0.03)
    numeric_check("LP-DiD recovers ATT at h=3",
                  m["lp"][3], target=float(m["truth"][3]), tol=0.03)
    numeric_check("pooled TWFE event study is contaminated at long horizons",
                  twfe_gap3, lo=0.25)
    numeric_check("LP-DiD pre-treatment placebo is null",
                  placebo, target=0.0, tol=0.03)
    print(f"\nAll assertions passed in {time.time() - t0:.1f}s: LP-DiD's "
          "clean-control local projections\nrecover the true dynamic path "
          "that the pooled TWFE event study cannot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
