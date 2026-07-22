#!/usr/bin/env python3
"""Sun-Abraham demo: the interaction-weighted event study fixes contaminated TWFE.

A runnable companion to docs/methods-reference.md and the aer-identification
skill. It makes the Sun and Abraham (2021) point: under staggered adoption with
cohort-heterogeneous dynamic effects, the *dynamic* two-way-fixed-effects event
study -- y on unit FE, period FE, and a full set of relative-time indicators --
does NOT recover the average dynamic path. Each relative-time coefficient is a
contaminated weighted sum of cohort-specific effects (CATT) at that *and other*
relative times, because already-treated cohorts (whose effects are still moving)
enter the implicit comparison group. Sun-Abraham repair: saturate the regression
in cohort x relative-time interactions, estimate each CATT(e, l) against a clean
never-treated control, then aggregate to the horizon-l average using the
interaction WEIGHTS -- the sample share of each cohort among units observed at
relative time l. That weighted average is the true ATT(l).

This is a different repair from the sibling demos: ``staggered-did-demo`` shows
WHY pooled TWFE fails (Goodman-Bacon decomposition) and ``lp-did-demo`` repairs
the path with clean-control local projections. Sun-Abraham instead repairs it
*inside a single saturated regression* -- the estimator AER referees now ask for
by name next to Callaway-Sant'Anna.

The data-generating process is fully known -- the horizon-l effect of cohort g
is BASE(l) scaled by a cohort multiplier, so effects grow with event time and
differ across cohorts -- so the script computes the true ATT(l) from the same
parameters, weighted exactly like the interaction-weighted estimand. It then
*asserts*, over a Monte Carlo, that the interaction-weighted estimator recovers
ATT(l) at both a short and a long horizon, that the naive dynamic TWFE
event-study coefficient is materially contaminated at the long horizon, and that
the Sun-Abraham pre-treatment placebo is null -- exiting non-zero on any
failure, so the demo doubles as a regression test.

Run:  python3 sun_abraham_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: sun_abraham_2021 (and goodmanbacon_2021, callaway_santanna_2021 for
the surrounding critique) in ../../references.bib. See
../../docs/methods-reference.md for the per-stack tooling and
../../skills/aer-identification/SKILL.md for the design context.
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
N_UNITS = 300                         # panel width
N_PERIODS = 16                        # panel length (t = 1..16)
# Adoption period -> cohort multiplier on the common dynamic shape BASE(l).
# Effects GROW with event time (via BASE) and DIFFER across cohorts (via the
# multiplier) -- exactly what turns the naive dynamic TWFE relative-time
# coefficients into contaminated cross-cohort, cross-horizon mixtures. g = 0
# marks the never-treated control group.
COHORT_MULT = {5: 1.6, 8: 1.0, 11: 0.4, 0: 0.0}
COHORT_PROBS = (0.30, 0.30, 0.30, 0.10)   # only 10% never-treated -> weak anchor
BASE = lambda l: 1.0 + 0.5 * l            # common dynamic shape at event time l
NOISE_SD = 0.5                        # idiosyncratic shock
TIME_SHOCK_SD = 0.4                   # common period shock (absorbed by FE)
HORIZONS = (0, 1, 2, 3)               # event-time horizons compared
PLACEBO_L = -2                        # pre-treatment placebo horizon
TWFE_LEAD_BIN = -4                    # dynamic TWFE: leads binned at -4 ...
TWFE_LAG_BIN = 4                      # ... lags binned at 4+ (reference l = -1)
REPS = 300                            # Monte Carlo repetitions
OUT = Path(__file__).resolve().parent / "output"


def simulate_panel(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """One staggered-adoption panel. Returns (cohort g per unit, Y of shape
    (N_UNITS, N_PERIODS)); Y[i, t-1] is unit i's outcome in period t. Parallel
    trends hold by construction: the untreated potential outcome is unit FE +
    common period effect + noise, identical in expectation across cohorts."""
    cohorts = np.array(list(COHORT_MULT))
    g = rng.choice(cohorts, size=N_UNITS, p=COHORT_PROBS)
    alpha = rng.normal(0.0, 1.0, N_UNITS)               # unit FE (cohort-blind)
    delta = 0.10 * np.arange(1, N_PERIODS + 1)          # common trend ...
    delta = delta + rng.normal(0.0, TIME_SHOCK_SD, N_PERIODS)  # ... + shocks
    t_grid = np.arange(1, N_PERIODS + 1)[None, :]       # (1, T)
    event = t_grid - g[:, None]                         # event time l = t - g
    treated = (g[:, None] > 0) & (event >= 0)
    mult = np.array([COHORT_MULT[int(c)] for c in g])[:, None]
    tau = np.where(treated, mult * (1.0 + 0.5 * event), 0.0)   # BASE(l)*mult
    Y = alpha[:, None] + delta[None, :] + tau + rng.normal(
        0.0, NOISE_SD, (N_UNITS, N_PERIODS))
    return g, Y


def true_att_path(g: np.ndarray) -> np.ndarray:
    """True ATT(l), weighted exactly like the interaction-weighted estimand:
    the share of each treated cohort among units observed at relative time l.
    Every treated cohort reaches every horizon in HORIZONS inside the panel, so
    the weight at each l is just the cohort's share of treated units, and
    ATT(l) = sum_g share_g * BASE(l) * mult_g."""
    treated_cohorts = g[g > 0]
    mults = np.array([COHORT_MULT[int(c)] for c in treated_cohorts])
    mean_mult = float(mults.mean())
    return np.array([BASE(l) * mean_mult for l in HORIZONS])


def _cohort_catt(g: np.ndarray, Y: np.ndarray, cohort: int, l: int) -> float | None:
    """Clean cohort-specific ATT(cohort, l): a 2x2 DiD of cohort ``cohort``
    against the never-treated group, long difference from the reference period
    l = -1 (period cohort-1) to period cohort+l. Returns None if the horizon
    falls outside the panel."""
    ref_t = cohort - 1                      # period index for l = -1
    out_t = cohort + l                      # period index for l
    if ref_t < 1 or out_t < 1 or out_t > N_PERIODS:
        return None
    treat = g == cohort
    never = g == 0
    if not treat.any() or not never.any():
        return None
    d_treat = Y[treat, out_t - 1] - Y[treat, ref_t - 1]
    d_never = Y[never, out_t - 1] - Y[never, ref_t - 1]
    return float(d_treat.mean() - d_never.mean())


def sun_abraham(g: np.ndarray, Y: np.ndarray, l: int) -> float:
    """Interaction-weighted estimator at horizon l (Sun-Abraham 2021). Estimate
    each cohort-specific CATT(e, l) against the never-treated control, then take
    the weighted average with interaction weights = each cohort's share of the
    treated units observed at relative time l. Here every treated cohort reaches
    every horizon, so the weights are the treated-cohort population shares --
    the same weighting as ``true_att_path``."""
    num, den = 0.0, 0
    for cohort in sorted(int(c) for c in np.unique(g) if c > 0):
        catt = _cohort_catt(g, Y, cohort, l)
        if catt is None:
            continue
        n_e = int((g == cohort).sum())      # interaction weight (cohort size)
        num += n_e * catt
        den += n_e
    return num / den


def twfe_event_study(g: np.ndarray, Y: np.ndarray) -> dict[int, float]:
    """Naive dynamic TWFE event study: y on unit FE + period FE + relative-time
    dummies (leads binned at TWFE_LEAD_BIN, lags at TWFE_LAG_BIN+, reference
    l = -1; never-treated units carry all-zero dummies). Estimated by exact
    two-way within-demeaning of the balanced panel followed by OLS via numpy
    lstsq. Returns the coefficients at horizons in HORIZONS and at PLACEBO_L.
    Under cohort-heterogeneous dynamic effects these are contaminated mixtures
    (the Sun-Abraham critique)."""
    event = np.arange(1, N_PERIODS + 1)[None, :] - g[:, None]    # (N, T)
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
    X = np.stack(cols, axis=-1)                          # (N, T, K)

    def demean2(a: np.ndarray) -> np.ndarray:
        """Exact two-way (unit + period) within transform on a balanced panel."""
        return (a - a.mean(axis=0, keepdims=True)
                  - a.mean(axis=1, keepdims=True) + a.mean())

    Xd = np.stack([demean2(X[:, :, k]) for k in range(X.shape[-1])], axis=-1)
    yd = demean2(Y).ravel()
    beta, *_ = np.linalg.lstsq(Xd.reshape(-1, X.shape[-1]), yd, rcond=None)
    wanted = list(HORIZONS) + [PLACEBO_L]
    return {h: float(beta[bins.index(h)]) for h in wanted}


def sa_placebo(g: np.ndarray, Y: np.ndarray) -> float:
    """Sun-Abraham pre-treatment placebo at PLACEBO_L: the interaction-weighted
    average of cohort-specific pre-period long differences against never-treated
    controls. Both periods predate treatment, so under parallel trends it is
    ~0."""
    return sun_abraham(g, Y, PLACEBO_L)


def run_montecarlo(rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Monte Carlo means of the true path and all estimators across REPS."""
    truth = np.zeros((REPS, len(HORIZONS)))
    sa = np.zeros((REPS, len(HORIZONS)))
    twfe = np.zeros((REPS, len(HORIZONS)))
    placebo = np.zeros(REPS)
    twfe_placebo = np.zeros(REPS)
    for r in range(REPS):
        g, Y = simulate_panel(rng)
        truth[r] = true_att_path(g)
        sa[r] = [sun_abraham(g, Y, h) for h in HORIZONS]
        tw = twfe_event_study(g, Y)
        twfe[r] = [tw[h] for h in HORIZONS]
        placebo[r] = sa_placebo(g, Y)
        twfe_placebo[r] = tw[PLACEBO_L]
    return {"truth": truth.mean(axis=0), "sa": sa.mean(axis=0),
            "twfe": twfe.mean(axis=0),
            "placebo": np.array([placebo.mean()]),
            "twfe_placebo": np.array([twfe_placebo.mean()])}


def make_figure(m: dict[str, np.ndarray]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    hs = np.array(HORIZONS, dtype=float)
    ax.axhline(0.0, color="grey", linewidth=0.8)
    ax.axvline(-0.5, color="grey", linestyle="--", linewidth=0.8)
    ax.plot(hs, m["truth"], linestyle=":", marker="s", color="firebrick",
            label="True ATT(l)")
    ax.plot(np.append(PLACEBO_L, hs), np.append(m["placebo"][0], m["sa"]),
            marker="o", color="black", label="Sun-Abraham (interaction-weighted)")
    ax.plot(np.append(PLACEBO_L, hs),
            np.append(m["twfe_placebo"][0], m["twfe"]),
            marker="^", color="darkorange",
            label="Naive dynamic TWFE event study (contaminated)")
    ax.annotate("placebo", (PLACEBO_L, m["placebo"][0]),
                textcoords="offset points", xytext=(0, 8), ha="center",
                fontsize=8, color="black")
    ax.set_xlabel("Event time l (relative to treatment)")
    ax.set_ylabel("Effect on outcome")
    ax.set_title("Sun-Abraham tracks the true dynamic path; naive TWFE does not")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    pdf = OUT / "sun_abraham.pdf"
    fig.savefig(pdf)                        # vector, for inclusion in a paper
    fig.savefig(OUT / "sun_abraham.png", dpi=150)  # raster, for the README
    plt.close(fig)
    return pdf


def main() -> int:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    m = run_montecarlo(rng)
    placebo = float(m["placebo"][0])
    twfe_gap3 = abs(float(m["twfe"][3]) - float(m["truth"][3]))

    print("=" * 70)
    print("Sun-Abraham interaction-weighted event study vs naive dynamic TWFE")
    print(f"  units={N_UNITS}  periods={N_PERIODS}  reps={REPS}  seed={SEED}")
    print("  cohorts (adoption -> multiplier): "
          + ", ".join(f"{k}->{v}" for k, v in COHORT_MULT.items() if k > 0)
          + "  (0 = never treated)")
    print("=" * 70)
    print(f"  {'l':>3}  {'true ATT(l)':>12}  {'Sun-Abraham':>12}  {'naive TWFE':>12}")
    for j, h in enumerate(HORIZONS):
        print(f"  {h:>3}  {m['truth'][j]:>12.3f}  {m['sa'][j]:>12.3f}"
              f"  {m['twfe'][j]:>12.3f}")
    print(f"  Sun-Abraham pre-treatment placebo (l={PLACEBO_L}): {placebo:.3f}")
    print()
    print("  The interaction-weighted estimator's cohort CATTs, aggregated with")
    print("  their sample-share weights, track the true path at every horizon;")
    print(f"  the naive dynamic TWFE coefficient is off by {twfe_gap3:.2f} at l=3")
    print(f"  ({100 * twfe_gap3 / m['truth'][3]:.0f}% of the true effect), because")
    print("  already-treated cohorts with still-growing effects contaminate the")
    print("  implicit comparison group.")

    pdf = make_figure(m)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    # Each numeric_check pins an estimate to its known target and emits a
    # NUMERIC-CHECK line that scripts/run_example_smoke.py verifies.
    numeric_check("Sun-Abraham recovers ATT at l=0",
                  m["sa"][0], target=float(m["truth"][0]), tol=0.04)
    numeric_check("Sun-Abraham recovers ATT at l=3",
                  m["sa"][3], target=float(m["truth"][3]), tol=0.04)
    numeric_check("naive dynamic TWFE event study is contaminated at l=3",
                  twfe_gap3, lo=0.25)
    numeric_check("Sun-Abraham pre-treatment placebo is null",
                  placebo, target=0.0, tol=0.04)
    print(f"\nAll assertions passed in {time.time() - t0:.1f}s: the "
          "interaction-weighted estimator\nrecovers the true dynamic path that "
          "the naive dynamic TWFE event study cannot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
