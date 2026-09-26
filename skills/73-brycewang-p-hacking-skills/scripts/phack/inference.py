"""
Honest inference for a search that has already happened.

The whole point of this toolkit: if an agent walked S specifications and
reported the best one, the reported p-value is not a p-value. These functions
recover an inferentially valid statement from the same ledger.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

__all__ = ["bonferroni", "sidak", "bh_fdr", "romano_wolf", "min_p_test",
           "effective_tests", "spec_curve_stats"]


def bonferroni(pvals) -> np.ndarray:
    p = np.asarray(pvals, float)
    return np.clip(p * np.isfinite(p).sum(), 0, 1)


def sidak(pvals) -> np.ndarray:
    p = np.asarray(pvals, float)
    m = np.isfinite(p).sum()
    return 1 - (1 - np.clip(p, 0, 1)) ** m


def bh_fdr(pvals) -> np.ndarray:
    p = np.asarray(pvals, float)
    ok = np.isfinite(p)
    q = np.full_like(p, np.nan)
    pv = p[ok]
    m = pv.size
    order = np.argsort(pv)
    ranked = pv[order] * m / np.arange(1, m + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(m)
    out[order] = np.clip(ranked, 0, 1)
    q[ok] = out
    return q


def effective_tests(tstats_null: np.ndarray) -> float:
    """Li & Ji (2005) effective number of independent specifications.

    tstats_null: (B, S) null draws of the specification t-statistics.
    Specifications in a multiverse are heavily correlated -- they reuse the same
    rows and the same treatment -- so Bonferroni over S badly over-corrects.
    Meff = sum_i [ 1{lambda_i >= 1} + (lambda_i - floor(lambda_i)) ] over the
    eigenvalues of the specification correlation matrix.
    """
    T = np.asarray(tstats_null, float)
    T = T[:, ~np.all(~np.isfinite(T), axis=0)]
    if T.shape[1] < 2:
        return float(max(T.shape[1], 1))
    C = np.nan_to_num(pd.DataFrame(T).corr().to_numpy(), nan=0.0)
    np.fill_diagonal(C, 1.0)
    ev = np.clip(np.linalg.eigvalsh(C), 0, None)
    meff = np.sum((ev >= 1).astype(float) + (ev - np.floor(ev)))
    return float(np.clip(meff, 1.0, C.shape[0]))


def meff_adjusted_p(p: float, meff: float) -> float:
    """Sidak correction using the effective, not the nominal, test count."""
    return float(1 - (1 - min(max(p, 0.0), 1.0)) ** max(meff, 1.0))


def romano_wolf(t_obs, t_null, two_sided=True):
    """Romano-Wolf stepdown adjusted p-values.

    t_obs: (S,) observed t-statistics.
    t_null: (B, S) t-statistics under the null (bootstrap or permutation).
    Controls FWER across the whole specification family and, unlike Bonferroni,
    exploits the dependence between specifications.
    """
    t_obs = np.asarray(t_obs, float).copy()
    t_null = np.asarray(t_null, float).copy()
    if two_sided:
        t_obs, t_null = np.abs(t_obs), np.abs(t_null)
    B, S = t_null.shape
    if t_obs.size != S:
        raise ValueError(f"t_obs has {t_obs.size} entries but t_null has {S} columns")
    # A specification that failed contributes no evidence in either direction.
    # Left as NaN it silently defeats the max() and every p collapses to 1/(B+1).
    finite_obs = np.isfinite(t_obs)
    t_obs_f = np.where(finite_obs, t_obs, -np.inf)
    t_null_f = np.where(np.isfinite(t_null), t_null, -np.inf)

    order = np.argsort(-t_obs_f, kind="stable")
    padj = np.ones(S)
    running = 0.0
    for step, j in enumerate(order):
        if not finite_obs[j]:
            padj[j] = np.nan
            continue
        cols = order[step:]
        cols = cols[finite_obs[cols]]
        maxnull = t_null_f[:, cols].max(axis=1)
        valid = np.isfinite(maxnull)
        if not valid.any():
            padj[j] = np.nan
            continue
        p = (1.0 + np.sum(maxnull[valid] >= t_obs[j])) / (valid.sum() + 1.0)
        running = max(running, p)          # stepdown monotonicity
        padj[j] = min(running, 1.0)
    return padj


def min_p_test(p_obs_min: float, p_null_min: np.ndarray) -> dict:
    """The headline number.

    p_obs_min: smallest p-value the search actually reported.
    p_null_min: (B,) smallest p-value obtained by re-running the *identical*
    search on data where the null is true by construction.
    """
    p_null_min = np.asarray(p_null_min, float)
    p_null_min = p_null_min[np.isfinite(p_null_min)]
    B = p_null_min.size
    honest = (1.0 + np.sum(p_null_min <= p_obs_min)) / (B + 1.0)
    return {
        "reported_p": float(p_obs_min),
        "honest_p": float(honest),
        "inflation_factor": float(honest / p_obs_min) if p_obs_min > 0 else float("inf"),
        "null_min_p_median": float(np.median(p_null_min)) if B else float("nan"),
        "null_min_p_q05": float(np.quantile(p_null_min, 0.05)) if B else float("nan"),
        "n_null_draws": int(B),
    }


def spec_curve_stats(coefs, pvals, alpha=0.05, sign=None) -> dict:
    """Descriptives of the specification curve (Simonsohn, Simmons & Nelson)."""
    c = np.asarray(coefs, float)
    p = np.asarray(pvals, float)
    ok = np.isfinite(c) & np.isfinite(p)
    c, p = c[ok], p[ok]
    if c.size == 0:
        return {"n": 0}
    sign = sign if sign is not None else np.sign(np.median(c))
    sig = p < alpha
    return {
        "n": int(c.size),
        "median_coef": float(np.median(c)),
        "mean_coef": float(np.mean(c)),
        "min_coef": float(c.min()),
        "max_coef": float(c.max()),
        "iqr_coef": float(np.subtract(*np.percentile(c, [75, 25]))),
        "share_significant": float(sig.mean()),
        "share_sig_dominant_sign": float((sig & (np.sign(c) == sign)).mean()),
        "share_sign_flips": float((np.sign(c) != sign).mean()),
        "coef_range_over_median_se": float((c.max() - c.min()) / abs(np.median(c)))
        if np.median(c) else float("inf"),
    }


# --------------------------------------------------------------------------
# Direction-aware p-values and the Simonsohn-Simmons-Nelson joint tests
# --------------------------------------------------------------------------

def one_sided_p(t, p_two, direction):
    """One-sided p in `direction` (+1/-1) from a two-sided p and the sign of t.
    Exact for any symmetric reference distribution, so no df is needed."""
    t = np.asarray(t, float); p_two = np.asarray(p_two, float)
    if direction is None:
        return p_two
    same = np.sign(t) == direction
    return np.where(same, p_two / 2.0, 1.0 - p_two / 2.0)


def ssn_joint_tests(coef_obs, t_obs, p_obs, coef_null, t_null, p_null,
                    alpha=0.05, direction=None) -> dict:
    """Specification-curve joint inference (Simonsohn, Simmons & Nelson 2020).

    Three summaries of the observed curve are compared with their distribution
    across B null re-runs of the same curve:
      * median effect            -- is the typical estimate unusual?
      * share significant        -- are unusually many specifications < alpha?
      * share sig., dominant sign-- ...in the direction the curve leans (or the
                                    declared direction)?
    plus a Stouffer aggregate of the signed t-statistics. All four use the same
    null draws the min-p test uses, so they cost nothing extra and, unlike the
    min-p test, they describe the *whole* curve rather than its best point.
    """
    c = np.asarray(coef_obs, float); t = np.asarray(t_obs, float); p = np.asarray(p_obs, float)
    C = np.asarray(coef_null, float); T = np.asarray(t_null, float); P = np.asarray(p_null, float)
    ok = np.isfinite(c) & np.isfinite(t) & np.isfinite(p)
    c, t, p, C, T, P = c[ok], t[ok], p[ok], C[:, ok], T[:, ok], P[:, ok]
    if c.size == 0 or C.shape[0] == 0:
        return {"note": "nothing to test"}
    sign = direction if direction is not None else (np.sign(np.median(c)) or 1.0)
    B = C.shape[0]

    def _p(obs, null, larger=True):
        null = null[np.isfinite(null)]
        if null.size == 0:
            return float("nan")
        return float((1.0 + np.sum(null >= obs if larger else null <= obs)) / (null.size + 1.0))

    med_obs = float(np.median(c)); med_null = np.nanmedian(C, axis=1)
    share_obs = float(np.mean(p < alpha)); share_null = np.nanmean(P < alpha, axis=1)
    dom_obs = float(np.mean((p < alpha) & (np.sign(c) == sign)))
    dom_null = np.nanmean((P < alpha) & (np.sign(C) == sign), axis=1)
    z_obs = float(np.sum(t) / np.sqrt(t.size)); z_null = np.nansum(T, axis=1) / np.sqrt(t.size)
    return {
        "n_specs": int(c.size), "n_null_draws": int(B), "dominant_sign": int(sign),
        "median_effect": {"observed": med_obs, "null_median": float(np.nanmedian(med_null)),
                          "p_value": _p(sign * med_obs, sign * med_null)},
        "share_significant": {"observed": share_obs, "null_median": float(np.nanmedian(share_null)),
                              "null_q95": float(np.nanquantile(share_null, 0.95)),
                              "p_value": _p(share_obs, share_null)},
        "share_significant_dominant_sign": {"observed": dom_obs,
                                            "null_median": float(np.nanmedian(dom_null)),
                                            "p_value": _p(dom_obs, dom_null)},
        "stouffer_z": {"observed": z_obs, "p_value": _p(sign * z_obs, sign * z_null)},
        "reads": ("small p_value on share_significant with a large min-p honest p means the "
                  "curve leans one way everywhere but no single specification is unusual; "
                  "the reverse means one corner of the grid did all the work"),
    }
