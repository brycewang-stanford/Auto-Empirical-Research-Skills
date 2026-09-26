"""
Robustness theatre: build the table a launderer would show, and audit the
table a write-up did show.

A robustness table with twenty specifications, all significant, all similar,
looks like a multiverse and is the opposite of one: the twenty were chosen
*because* they agree with the headline. The specifications that disagreed are
not in the table. This module makes both directions mechanical:

  build_table()  -- red team: from a ledger and a reported specification,
                    select the k nearest specifications that agree with it,
                    and report the denominator that the table hides
  audit_table()  -- blue team: given the specifications a write-up shows,
                    compare them with the ledger they were drawn from and
                    test whether the shown set is more favourable than a
                    random subset of the same size would be
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import grid

__all__ = ["build_table", "audit_table"]


def _axes_of(row):
    return {a: (tuple(v) if isinstance(v, list) else v)
            for a, v in json.loads(row["spec_json"]).items() if a in grid.AXES}


def _dist(a, b):
    return sum(a[k] != b[k] for k in grid.AXES if k in a and k in b)


def build_table(ledger: pd.DataFrame, reported_key: str, k=12, alpha=0.05,
                require_significant=True, same_sign=True) -> dict:
    """The table a launderer would print: the reported specification plus the
    k-1 specifications nearest to it in analytical choices that agree with it.

    Returns the table and, more importantly, the denominator: how many
    specifications the ledger holds, what share agree, and what the reader
    would have seen had the table been drawn at random.
    """
    ok = ledger[ledger["status"] == "ok"] if "status" in ledger else ledger
    rep = ok[ok["key"] == reported_key]
    if rep.empty:
        raise KeyError(f"reported key {reported_key} not in ledger")
    rep = rep.iloc[0]
    sign = np.sign(rep["coef"])
    agree = pd.Series(True, index=ok.index)
    if require_significant:
        agree &= ok["p"] < alpha
    if same_sign:
        agree &= np.sign(ok["coef"]) == sign
    pool = ok[agree & (ok["key"] != reported_key)]
    a0 = _axes_of(rep)
    d = pool.apply(lambda r: _dist(a0, _axes_of(r)), axis=1) if len(pool) else pd.Series(dtype=int)
    chosen = pool.assign(_d=d).sort_values(["_d", "p"]).head(k - 1)
    table = pd.concat([rep.to_frame().T.assign(_d=0), chosen])
    cols = [c for c in ["key", "label", "coef", "se", "t", "p", "n", "_d"] if c in table]
    table = table[cols].rename(columns={"_d": "choices_from_reported"})
    n = len(ok)
    return {
        "table": table.reset_index(drop=True),
        "n_shown": int(len(table)),
        "n_in_ledger": int(n),
        "share_shown": round(len(table) / n, 4),
        "share_of_ledger_agreeing": round(float(agree.mean()), 4),
        "share_of_ledger_significant": round(float((ok["p"] < alpha).mean()), 4),
        "share_of_ledger_same_sign": round(float((np.sign(ok["coef"]) == sign).mean()), 4),
        "median_coef_shown": float(table["coef"].median()),
        "median_coef_ledger": float(ok["coef"].median()),
        "reads": (f"the table shows {len(table)} of {n} specifications; "
                  f"{100 * float(agree.mean()):.0f}% of the ledger agrees with the headline, "
                  f"so a random table of this size would have contained about "
                  f"{len(table) * float(agree.mean()):.1f} agreeing rows, not {len(table)}"),
    }


def audit_table(ledger: pd.DataFrame, shown_keys, alpha=0.05, B=2000, seed=0) -> dict:
    """Audit a robustness table against the ledger it was drawn from.

    Tests whether the shown specifications are more favourable than a random
    subset of the same size (share significant; mean |t|), by drawing B random
    subsets of the ledger. A tiny p-value means the table was selected on the
    result. Also reports what the reader was not shown: the share of
    specifications outside the table that are insignificant or flip sign.
    """
    ok = ledger[ledger["status"] == "ok"] if "status" in ledger else ledger
    shown = ok[ok["key"].isin(set(shown_keys))]
    if shown.empty:
        return {"note": "none of the shown keys is in the ledger"}
    hidden = ok[~ok["key"].isin(set(shown_keys))]
    k = len(shown)
    sig_all = (ok["p"] < alpha).to_numpy(); abs_t = ok["t"].abs().to_numpy()
    obs_sig = float((shown["p"] < alpha).mean()); obs_t = float(shown["t"].abs().mean())
    rng = np.random.default_rng(seed)
    idx = np.arange(len(ok))
    sims_sig = np.empty(B); sims_t = np.empty(B)
    for b in range(B):
        pick = rng.choice(idx, size=k, replace=False)
        sims_sig[b] = sig_all[pick].mean(); sims_t[b] = np.nanmean(abs_t[pick])
    sign = np.sign(shown["coef"].median())
    out = {
        "n_shown": int(k), "n_in_ledger": int(len(ok)), "share_shown": round(k / len(ok), 4),
        "shown": {"share_significant": obs_sig, "mean_abs_t": obs_t,
                  "median_coef": float(shown["coef"].median()),
                  "share_same_sign_as_median": float((np.sign(shown["coef"]) == sign).mean())},
        "hidden": {"n": int(len(hidden)),
                   "share_significant": float((hidden["p"] < alpha).mean()) if len(hidden) else float("nan"),
                   "share_sign_flips": float((np.sign(hidden["coef"]) != sign).mean()) if len(hidden) else float("nan"),
                   "median_coef": float(hidden["coef"].median()) if len(hidden) else float("nan")},
        "random_table": {"share_significant_median": float(np.median(sims_sig)),
                         "share_significant_q95": float(np.quantile(sims_sig, 0.95)),
                         "mean_abs_t_median": float(np.median(sims_t))},
        "p_share_significant": float((1 + np.sum(sims_sig >= obs_sig)) / (B + 1)),
        "p_mean_abs_t": float((1 + np.sum(sims_t >= obs_t)) / (B + 1)),
        "selection_ratio": (float(obs_sig / max(np.median(sims_sig), 1e-9))
                            if np.median(sims_sig) > 0 else float("inf")),
        "reads": ("p_share_significant is the probability that a random table of this size from "
                  "the same ledger is at least this favourable; selection_ratio is how many times "
                  "more significant the shown table is than a random one"),
    }
    out["verdict"] = (
        "robustness theatre: the shown set is far more favourable than a random draw"
        if out["p_share_significant"] < 0.01 else
        "selective: the shown set is more favourable than a random draw"
        if out["p_share_significant"] < 0.05 else
        "consistent with an unselected table")
    return out
