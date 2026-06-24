#!/usr/bin/env python3
"""Staggered-DiD demonstration: why the modern estimator replaces TWFE.

This is a *runnable* companion to ``docs/methods-reference.md`` and the
``aer-identification`` skill. It simulates a staggered-adoption panel with a
KNOWN true effect, then shows — with real numbers, not assertion — that:

  1. Naive two-way fixed effects (TWFE) is badly biased, because late-treated
     cohorts with small effects get used as controls for early-treated cohorts
     with large, growing effects (the Goodman-Bacon "forbidden comparison").
  2. A heterogeneity-robust estimator (Borusyak-Jaravel-Spiess / Gardner
     two-stage, ``did2s``) recovers the true ATT.
  3. A clean event study (treated-vs-never-treated) recovers the true *dynamic*
     path with flat pre-trends.

The data-generating process is fully known, so the script *asserts* the result
and exits non-zero if the modern estimator fails to recover the truth or TWFE is
not materially biased — i.e. it doubles as a regression test of the claim the
whole skill stack is built on.

Run:  python3 staggered_did_demo.py
Deps: numpy, pandas, pyfixest, matplotlib
      (see ../../templates/python/requirements.txt)

References (keys are in ../../references.bib):
  goodmanbacon_2021, borusyak_jaravel_spiess_2024, sun_abraham_2021,
  callaway_santanna_2021, dechaisemartin_dhaultfoeuille_2020
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # headless: write files, never open a window
import matplotlib.pyplot as plt

import pyfixest as pf

SEED = 20260101                       # repository-wide fixed seed
OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

# Cohort -> per-period treatment-effect slope. The early cohort (treated at
# t=5) has a large, growing effect; the late cohort (t=9) a small one; the
# third group is never treated. This heterogeneity is exactly what biases TWFE.
COHORTS = {5: 2.0, 9: 0.5, 0: 0.0}    # 0 == never treated
N_UNITS = 300
N_PERIODS = 12
NOISE_SD = 0.5


def simulate_panel(seed: int = SEED) -> pd.DataFrame:
    """A staggered-adoption panel with dynamic, cohort-heterogeneous effects."""
    rng = np.random.default_rng(seed)
    cohort = rng.choice(list(COHORTS), size=N_UNITS, p=[1 / 3, 1 / 3, 1 / 3])
    alpha = rng.normal(0, 1, N_UNITS)          # unit fixed effects
    rows = []
    for i in range(N_UNITS):
        g = int(cohort[i])
        for t in range(1, N_PERIODS + 1):
            treated_now = int(g != 0 and t >= g)
            tau = COHORTS[g] * (t - g + 1) if treated_now else 0.0  # dynamic
            y = alpha[i] + 0.10 * t + tau + rng.normal(0, NOISE_SD)
            rows.append((i, t, g, treated_now, tau, y))
    df = pd.DataFrame(rows, columns=["unit", "time", "cohort", "treated_now", "tau", "y"])
    # event time; never-treated parked at the reference bin (-1) so they act as
    # pure controls identified through the time fixed effects.
    df["rel_time"] = np.where(df["cohort"] == 0, -1, df["time"] - df["cohort"])
    return df


def true_simple_att(df: pd.DataFrame) -> float:
    """Average of the deterministic effect over all treated unit-periods."""
    return float(df.loc[df["treated_now"] == 1, "tau"].mean())


def att_scalar(model) -> tuple[float, float, float]:
    """Pull (estimate, ci_low, ci_high) from a single-coefficient pyfixest fit."""
    t = model.tidy()
    row = t.iloc[0]
    return float(row["Estimate"]), float(row["2.5%"]), float(row["97.5%"])


def fit_estimators(df: pd.DataFrame) -> dict:
    """TWFE (biased) and did2s (heterogeneity-robust) aggregate ATTs."""
    twfe = pf.event_study(df, yname="y", idname="unit", tname="time",
                          gname="cohort", estimator="twfe", att=True)
    did2s = pf.event_study(df, yname="y", idname="unit", tname="time",
                           gname="cohort", estimator="did2s", att=True)
    return {"twfe": att_scalar(twfe), "did2s": att_scalar(did2s)}


def clean_event_study(df: pd.DataFrame) -> pd.DataFrame:
    """Event study for the early cohort vs never-treated controls (unbiased,
    since the control group is never treated). Returns one row per event time."""
    sub = df[df["cohort"].isin([5, 0])].copy()
    sub["rel_time"] = np.where(sub["cohort"] == 0, -1, sub["time"] - 5).clip(-4, 7)
    m = pf.feols("y ~ i(rel_time, ref=-1) | unit + time", data=sub,
                 vcov={"CRV1": "unit"})
    t = m.tidy().reset_index()
    t["e"] = t["Coefficient"].str.extract(r"rel_time::(-?\d+\.?\d*)").astype(float)
    t = t.dropna(subset=["e"]).sort_values("e")
    out = t[["e", "Estimate", "2.5%", "97.5%"]].rename(
        columns={"Estimate": "estimate", "2.5%": "ci_lo", "97.5%": "ci_hi"})
    # add the reference period explicitly and the known truth for cohort 5
    ref = pd.DataFrame([{"e": -1.0, "estimate": 0.0, "ci_lo": 0.0, "ci_hi": 0.0}])
    out = pd.concat([out, ref]).sort_values("e").reset_index(drop=True)
    out["truth"] = np.where(out["e"] >= 0, COHORTS[5] * (out["e"] + 1), 0.0)
    return out


def make_figure(true_att: float, agg: dict, es: pd.DataFrame) -> Path:
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10, 4.2))

    # Panel A: aggregate ATT, TWFE vs did2s, against the known truth.
    labels = ["TWFE\n(naive)", "did2s\n(robust)"]
    ests = [agg["twfe"][0], agg["did2s"][0]]
    los = [agg["twfe"][1], agg["did2s"][1]]
    his = [agg["twfe"][2], agg["did2s"][2]]
    x = np.arange(len(labels))
    axL.errorbar(x, ests, yerr=[np.array(ests) - np.array(los),
                                np.array(his) - np.array(ests)],
                 fmt="o", color="black", capsize=4, markersize=7)
    axL.axhline(true_att, linestyle="--", color="grey")
    axL.text(1.05, true_att, f" true ATT = {true_att:.2f}", va="center",
             color="grey", fontsize=9)
    axL.set_xticks(x)
    axL.set_xticklabels(labels)
    axL.set_ylabel("Aggregate ATT")
    axL.set_title("A. TWFE misses the truth; did2s recovers it")
    axL.margins(x=0.3)

    # Panel B: clean event study vs the known dynamic path.
    pre = es["e"] < 0
    axR.axhline(0, color="grey", linewidth=0.8)
    axR.axvline(-0.5, color="grey", linestyle="--", linewidth=0.8)
    axR.errorbar(es.loc[pre, "e"], es.loc[pre, "estimate"],
                 yerr=[es.loc[pre, "estimate"] - es.loc[pre, "ci_lo"],
                       es.loc[pre, "ci_hi"] - es.loc[pre, "estimate"]],
                 fmt="o", color="grey", capsize=2, label="Pre (estimated)")
    axR.errorbar(es.loc[~pre, "e"], es.loc[~pre, "estimate"],
                 yerr=[es.loc[~pre, "estimate"] - es.loc[~pre, "ci_lo"],
                       es.loc[~pre, "ci_hi"] - es.loc[~pre, "estimate"]],
                 fmt="o", color="black", capsize=2, label="Post (estimated)")
    axR.plot(es["e"], es["truth"], linestyle=":", color="firebrick", label="True effect")
    axR.set_xlabel("Event time (years relative to treatment)")
    axR.set_ylabel("Effect on outcome")
    axR.set_title("B. Clean event study tracks the true path")
    axR.legend(frameon=False, fontsize=8, loc="upper left")

    fig.tight_layout()
    pdf = OUT / "event_study.pdf"
    fig.savefig(pdf)                       # vector, for inclusion in a paper
    fig.savefig(OUT / "event_study.png", dpi=150)  # raster, for the README
    plt.close(fig)
    return pdf


def main() -> int:
    df = simulate_panel()
    true_att = true_simple_att(df)
    agg = fit_estimators(df)
    es = clean_event_study(df)

    twfe_att = agg["twfe"][0]
    did2s_att = agg["did2s"][0]
    twfe_bias = (twfe_att - true_att) / true_att
    did2s_bias = (did2s_att - true_att) / true_att

    table = pd.DataFrame({
        "estimator": ["TRUE (simulated)", "TWFE (naive)", "did2s (robust)"],
        "att": [true_att, twfe_att, did2s_att],
        "ci_low": [np.nan, agg["twfe"][1], agg["did2s"][1]],
        "ci_high": [np.nan, agg["twfe"][2], agg["did2s"][2]],
        "pct_bias_vs_true": [0.0, 100 * twfe_bias, 100 * did2s_bias],
    })
    table.to_csv(OUT / "results.csv", index=False)

    pd.set_option("display.float_format", lambda v: f"{v:8.3f}")
    print("=" * 64)
    print("Staggered DiD: TWFE vs heterogeneity-robust estimator")
    print(f"  units={N_UNITS}  periods={N_PERIODS}  seed={SEED}")
    print("=" * 64)
    print(table.to_string(index=False))
    print()
    print(f"TWFE understates the true effect by {-100 * twfe_bias:.0f}%.")
    print(f"did2s is within {abs(100 * did2s_bias):.1f}% of the truth.")
    pdf = make_figure(true_att, agg, es)
    print(f"Figure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: this demo is also a test of the core claim ----
    assert abs(did2s_bias) < 0.05, f"did2s should recover truth, bias={did2s_bias:.3f}"
    assert twfe_bias < -0.25, f"TWFE should be badly biased down, bias={twfe_bias:.3f}"
    assert (es.loc[es["e"] < 0, "estimate"].abs() < 0.3).all(), "pre-trends not flat"
    print("\nAll assertions passed: modern estimator recovers truth; TWFE does not.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
