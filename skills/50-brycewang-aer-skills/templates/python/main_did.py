"""
main_did.py
Staggered DiD using the `differences` package (Bernardo Dionisi), a Python
implementation of Callaway-Sant'Anna (2021).

Produces:
  * Main results table (TWFE vs CSDID) -- output/tables/tab_main_did.tex
  * Event-study figure                  -- output/figures/fig_event_study.pdf
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
import pyfixest as pf                # high-dim FE OLS, AER-style etable
from differences import ATTgt        # Callaway-Sant'Anna in Python
import matplotlib.pyplot as plt

import setup

log = logging.getLogger(__name__)

# `differences` returns MultiIndex column tuples; name the ones we read.
_ATT = ("EventAggregation", "", "ATT")
_LO  = ("EventAggregation", "pointwise conf. band", "lower")
_HI  = ("EventAggregation", "pointwise conf. band", "upper")


def _load() -> pd.DataFrame:
    df = pd.read_parquet(setup.INTERMEDIATE / "analytic.parquet")
    return df


def run() -> None:
    df = _load()
    log.info(f"Loaded analytic data: {df.shape[0]:,} rows, {df.shape[1]} cols")

    # ===============================================================
    # 1. Naive TWFE -- COMPARISON ONLY
    # ===============================================================
    twfe = pf.feols(
        "outcome ~ treat + x1 + x2 | unit_id + year",
        data    = df,
        vcov    = {"CRV1": "unit_id"},
    )

    # ===============================================================
    # 2. Callaway-Sant'Anna ATT(g,t) -- PREFERRED ESTIMATOR
    #    `differences` expects an (entity, time) MultiIndex and the
    #    never-treated cohort coded as NaN (not 0). The estimator and
    #    control group are arguments to .fit(), not the constructor.
    # ===============================================================
    panel = df.copy()
    panel["treat_year"] = panel["treat_year"].where(panel["treat_year"] > 0, np.nan)
    panel = panel.set_index(["unit_id", "year"])

    cs = ATTgt(data=panel, cohort_column="treat_year")
    cs.fit(
        formula       = "outcome ~ x1 + x2",
        est_method    = "dr",                 # doubly-robust
        control_group = "not_yet_treated",    # avoids forbidden comparisons
        n_jobs        = 1,
        progress_bar  = False,
    )

    simple     = cs.aggregate("simple")
    simple_att = float(simple[("SimpleAggregation", "", "ATT")].iloc[0])
    simple_se  = float(simple[("SimpleAggregation", "analytic", "std_error")].iloc[0])
    log.info(f"Simple ATT: {simple_att:.4f} (SE {simple_se:.4f})")

    # ===============================================================
    # 3. Event-study plot
    # ===============================================================
    ev   = cs.aggregate("event")
    e    = ev.index.get_level_values("relative_period").to_numpy(dtype=float)
    est  = ev[_ATT].to_numpy()
    lo   = ev[_LO].to_numpy()
    hi   = ev[_HI].to_numpy()
    pre  = e < 0

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(0, color="grey", linestyle="--", linewidth=0.8)
    ax.axvline(-0.5, color="grey", linestyle="--", linewidth=0.8)
    ax.errorbar(e[pre], est[pre],
                yerr=[est[pre] - lo[pre], hi[pre] - est[pre]],
                fmt="o", color="grey", capsize=2, label="Pre-treatment")
    ax.errorbar(e[~pre], est[~pre],
                yerr=[est[~pre] - lo[~pre], hi[~pre] - est[~pre]],
                fmt="o", color="black", capsize=2, label="Post-treatment")
    ax.set_xlabel("Years relative to treatment")
    ax.set_ylabel("ATT estimate")
    ax.legend(frameon=False, loc="upper left")

    fig.savefig(setup.FIGURES / "fig_event_study.pdf")
    plt.close(fig)
    log.info("Wrote fig_event_study.pdf")

    # ===============================================================
    # 4. Main results table (TWFE vs CSDID)
    # ===============================================================
    pf.etable(
        models    = [twfe],
        type      = "tex",
        file_name = str(setup.TABLES / "tab_twfe.tex"),
        signif_code = [0.01, 0.05, 0.10],
        notes     = (
            "Standard errors clustered at the unit level. "
            "TWFE shown for comparison only; preferred estimate is Callaway-Sant'Anna "
            "(see Table A.X). *** p<0.01, ** p<0.05, * p<0.10."
        ),
    )

    # The CS aggregate is not a pyfixest model object, so write the
    # TWFE-vs-CS comparison as a small booktabs table directly. (Building
    # the string avoids a jinja2 dependency that pandas.to_latex now needs.)
    rows = [
        ("TWFE (biased)",      float(twfe.coef()["treat"]), float(twfe.se()["treat"])),
        ("Callaway-Sant'Anna", simple_att,                  simple_se),
    ]
    lines = [r"\begin{tabular}{lcc}", r"\toprule",
             r"Estimator & ATT & Std. error \\", r"\midrule"]
    lines += [f"{name} & {est:.3f} & ({se:.3f}) \\\\" for name, est, se in rows]
    lines += [r"\bottomrule", r"\end{tabular}", ""]
    (setup.TABLES / "tab_main_did.tex").write_text("\n".join(lines))
    log.info("Wrote tab_main_did.tex")
