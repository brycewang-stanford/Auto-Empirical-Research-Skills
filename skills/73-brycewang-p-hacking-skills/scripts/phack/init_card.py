"""
Draft a design card from a dataset.

The hardest step for a new user is not running the search, it is writing the
JSON card. This module looks at a table and proposes one: panel keys, the
treatment, the outcome, a control pool, the fixed-effect and clustering
menus, and the conventional specification as the pre-registered anchor.
Everything it guesses is listed in `notes`, and the card is meant to be
edited before `phack size` -- a card is a claim about which analyses are
defensible, and only the analyst can make that claim.
"""
from __future__ import annotations

import re
import numpy as np
import pandas as pd

UNIT_HINTS = ("unit", "id", "firm", "state", "county", "country", "region", "city", "school",
              "household", "person", "pid", "hhid", "village", "plant", "bank", "fips", "isin")
TIME_HINTS = ("year", "time", "period", "t", "date", "month", "quarter", "wave", "yr")
TREAT_HINTS = ("treat", "treated", "policy", "d", "exposed", "post", "reform", "law", "adopt", "eligible")
WEIGHT_HINTS = ("pop", "weight", "wt", "w", "population", "pweight", "aweight")
CLUSTER_HINTS = ("region", "state", "county", "district", "province", "industry", "sector")


def _is_binary(s):
    v = pd.Series(s).dropna().unique()
    return len(v) == 2 and set(np.round(v.astype(float), 8)) <= {0.0, 1.0}


def _hint(cols, hints):
    for h in hints:
        for c in cols:
            if re.fullmatch(rf"{h}(_?id|_?code)?", c.lower()) or c.lower() == h:
                return c
    for h in hints:
        for c in cols:
            if h in c.lower():
                return c
    return None


def detect_panel(df):
    cols = list(df.columns)
    unit = _hint(cols, UNIT_HINTS); time = _hint(cols, TIME_HINTS)
    n = len(df)
    if unit is None or time is None:
        ints = [c for c in cols if pd.api.types.is_integer_dtype(df[c]) or df[c].dtype == object]
        for u in ints:
            nu = df[u].nunique()
            if not (3 <= nu <= n / 2):
                continue
            for t in ints:
                if t == u:
                    continue
                nt = df[t].nunique()
                if 2 <= nt <= 200 and not df.duplicated([u, t]).any() and nu * nt >= 0.5 * n:
                    return u, t
        return unit, time
    return unit, time


def draft_card(df: pd.DataFrame, *, design=None, outcome=None, treatment=None, unit=None, time=None,
               running=None, cutoff=0.0, instruments=None, name="draft", data_path=None):
    notes = []
    cols = list(df.columns)
    num = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    u, t = detect_panel(df)
    unit = unit or u; time = time or t
    if unit: notes.append(f"panel unit guessed as {unit!r}" if not u or unit != u else f"panel unit: {unit!r}")
    if time: notes.append(f"panel time: {time!r}")
    if instruments:
        design = design or "iv"
    if running:
        design = design or "rdd"
    # treatment
    if treatment is None and design != "rdd":
        cand = [c for c in num if _is_binary(df[c]) and c not in (unit, time)]
        treatment = _hint(cand, TREAT_HINTS) or (cand[0] if cand else None)
        if treatment: notes.append(f"treatment guessed as {treatment!r} (binary column)")
    # outcome
    if outcome is None:
        floats = [c for c in num if pd.api.types.is_float_dtype(df[c]) and c not in (unit, time, treatment, running)
                  and not _is_binary(df[c]) and c not in (instruments or [])]
        floats = [c for c in floats if not any(h == c.lower() for h in WEIGHT_HINTS)]
        outcome = floats[0] if floats else None
        if outcome: notes.append(f"outcome guessed as {outcome!r} (first continuous column); alternatives: {floats[1:4]}")
    if outcome is None:
        raise ValueError("could not guess an outcome; pass --outcome")
    alt_outcomes = [c for c in num if c != outcome and pd.api.types.is_float_dtype(df[c]) and not _is_binary(df[c])
                    and c not in (unit, time, treatment, running) and c not in (instruments or [])
                    and re.sub(r"[^a-z]", "", c.lower()).startswith(re.sub(r"[^a-z]", "", outcome.lower())[:3])][:2]
    weight = _hint(cols, WEIGHT_HINTS)
    weight = weight if weight in num and weight not in (outcome, treatment) else None
    cluster2 = _hint([c for c in cols if c not in (unit, time, outcome, treatment)], CLUSTER_HINTS)
    if cluster2 and df[cluster2].nunique() > 200:
        cluster2 = None
    excluded = {outcome, treatment, unit, time, running, weight, cluster2, *(instruments or []), *alt_outcomes}
    controls = [c for c in num if c not in excluded and not _is_binary(df[c]) or (c not in excluded and _is_binary(df[c]) and c != treatment)]
    controls = [c for c in controls if c not in excluded][:6]
    if controls: notes.append(f"control pool: {controls} (numeric columns not otherwise used; trim it)")
    # design
    if design is None:
        if unit and time and treatment:
            design = "did"
        elif treatment:
            design = "ols"
        else:
            design = "ols"
    absorbing = False
    if design == "did" and unit and treatment:
        paths = df.sort_values([unit, time]).groupby(unit)[treatment]
        absorbing = bool(all((np.diff(g.to_numpy()) >= 0).all() for _, g in paths))
        notes.append("treatment is absorbing (staggered adoption): estimator and comparison-group axes added"
                     if absorbing else "treatment switches on and off within units: TWFE axes only")
    pos = bool(df[outcome].dropna().min() > 0)
    card = {
        "name": name, "design": design, "direction": None,
        "outcomes": [outcome, *alt_outcomes],
        "treatment": treatment if design != "rdd" else None,
        "controls_pool": controls, "control_policy": "all_subsets" if len(controls) <= 4 else "nested",
        "outcome_transforms": ["level", "log"] if pos else ["level", "std"],
        "outlier_rules": ["none", "sd3"],
        "imputation": ["listwise"] if not df[[outcome, *controls]].isna().any().any() else ["listwise", "mean"],
        "vcov": ["hc1", "cluster"], "cluster": [None, unit] if unit else [None],
        "weights": [None, weight] if weight else [None],
        "notes": "DRAFT written by `phack init`; every axis is a guess about what is defensible -- edit before use.",
    }
    if design == "rdd":
        card.pop("treatment")
        card.update(running=running, cutoff=cutoff, bandwidth_selectors=["rot", "ik"],
                    bandwidth_multipliers=[0.5, 0.75, 1.0, 1.5, 2.0], kernels=["triangular", "uniform"],
                    poly_orders=[1, 2], donuts=[0.0], rdd_inference=["conventional", "robust"],
                    cluster=[None, cluster2] if cluster2 else [None])
        card["preregistered"] = {"outcome": outcome, "controls": [], "bandwidth": 1.0, "bw_selector": "ik",
                                 "kernel": "triangular", "poly": 1, "rdd_inference": "robust",
                                 "vcov": "cluster" if cluster2 else "hc1", "cluster": cluster2}
    elif design == "iv":
        card.update(instruments_pool=list(instruments), instrument_policy="all_subsets" if len(instruments) <= 4 else "nested",
                    iv_estimators=["2sls", "liml"], fixed_effects=[[]] + ([[unit]] if unit else []),
                    vcov=["hc1", "cluster"], cluster=[None, cluster2 or unit] if (cluster2 or unit) else [None])
        card["preregistered"] = {"outcome": outcome, "instruments": list(instruments), "iv_estimator": "2sls",
                                 "controls": controls, "fe": [unit] if unit else [], "vcov": "cluster" if (cluster2 or unit) else "hc1",
                                 "cluster": cluster2 or unit}
    else:
        fes = [[]]
        if unit: fes.append([unit])
        if unit and time: fes.append([unit, time])
        if cluster2 and time: fes.append([cluster2, time])
        card.update(fixed_effects=fes)
        if unit and time:
            card.update(panel_unit=unit, panel_time=time)
            med = float(df[time].median())
            card["subsamples"] = {"early": f"{time} < {med:g}", "late": f"{time} >= {med:g}"}
            if cluster2:
                card["cluster"] = [None, unit, cluster2]
        if absorbing:
            card.update(did_estimators=["twfe", "did2s", "stacked"],
                        comparison_groups=["all", "drop_never_treated"])
        card["preregistered"] = {"outcome": outcome, "controls": controls, "fe": [unit, time] if unit and time else [],
                                 "vcov": "cluster" if unit else "hc1", "cluster": unit,
                                 "y_transform": "level", "outlier_rule": "none", "subsample": "full", "weight": None}
    if data_path:
        card["notes"] += f" Drafted from {data_path}."
    notes.append("pre-registered specification set to the conventional choice (level outcome, full controls, "
                 "unit+time FE, clustered by unit); change it to what you would actually have committed to")
    return card, notes
