"""
Specification-curve figure (Simonsohn, Simmons & Nelson) from a ledger.

Top panel: every estimate sorted by size, with its confidence interval,
coloured by significance; the pre-registered specification and the reported
one are marked. Bottom panel: which analytical choice each specification made,
so the reader can see what drives the curve. Optional: the null-calibrated
min-p line so the reported p-value can be seen against what the search would
find on a true null.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

AXES = ["outcome", "controls", "fe", "vcov", "cluster", "y_transform", "d_transform",
        "outlier_rule", "imputation", "subsample", "weight", "did_estimator",
        "comparison_group", "ev_window", "ev_ref", "ev_estimand", "bw_selector", "bw_multiplier", "kernel", "poly", "donut",
        "rdd_inference", "instruments", "iv_estimator"]


def spec_curve(ledger: pd.DataFrame, out: str, *, alpha=0.05,
               reported_key=None, prereg_key=None, honest_p=None,
               title=None, max_axes=6, dpi=150):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ok = ledger[ledger["status"] == "ok"].copy() if "status" in ledger else ledger.copy()
    ok = ok[np.isfinite(ok["coef"]) & np.isfinite(ok["p"])]
    ok = ok.sort_values("coef").reset_index(drop=True)
    S = len(ok)
    if S == 0:
        raise ValueError("nothing to plot")

    # keep only axes that actually vary
    axes = [a for a in AXES if a in ok and ok[a].astype(str).nunique() > 1][:max_axes]
    nrow_bottom = sum(min(ok[a].astype(str).nunique(), 8) for a in axes)
    fig_h = 4.2 + 0.18 * nrow_bottom + 0.4 * len(axes)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, fig_h), sharex=True,
                                   gridspec_kw={"height_ratios": [4, max(1, nrow_bottom * 0.28)]})

    sig = ok["p"] < alpha
    xs = np.arange(S)
    col = np.where(sig, "#c0392b", "#7f8c8d")
    if "ci_low" in ok:
        ax1.vlines(xs, ok["ci_low"], ok["ci_high"], color=col, alpha=0.25, lw=0.8)
    ax1.scatter(xs, ok["coef"], c=col, s=10, zorder=3)
    ax1.axhline(0, color="k", lw=0.8)
    ax1.axhline(ok["coef"].median(), color="#2980b9", lw=1, ls="--",
                label=f"median = {ok['coef'].median():.3g}")

    def _mark(key, marker, label, colr):
        if key is None or "key" not in ok:
            return
        hit = ok.index[ok["key"] == key]
        if len(hit):
            i = int(hit[0])
            ax1.scatter([i], [ok.loc[i, "coef"]], marker=marker, s=160, facecolors="none",
                        edgecolors=colr, linewidths=2, zorder=5, label=label)
    _mark(prereg_key, "s", "pre-registered", "#27ae60")
    _mark(reported_key, "*", "reported", "#f39c12")

    txt = (f"S = {S} specifications   |   {sig.mean():.0%} significant at {alpha:g}   |   "
           f"{(np.sign(ok['coef']) != np.sign(ok['coef'].median())).mean():.0%} flip sign")
    if honest_p is not None:
        txt += f"   |   null-calibrated p of best = {honest_p:.2f}"
    fig.suptitle(title or "Specification curve", x=0.01, ha="left", fontsize=12, weight="bold")
    ax1.set_title(txt, loc="left", fontsize=8.5, color="#444", pad=6)
    ax1.set_ylabel("estimate")
    ax1.legend(loc="upper left", fontsize=8, frameon=False)
    ax1.spines[["top", "right"]].set_visible(False)

    # bottom: choice indicators
    yt, yl = [], []
    y = 0
    for a in axes:
        vals = ok[a].astype(str)
        levels = list(vals.value_counts().index[:8])
        for lv in levels:
            m = (vals == lv).to_numpy()
            ax2.scatter(xs[m], np.full(m.sum(), y), s=4, c=np.where(sig[m], "#c0392b", "#7f8c8d"))
            yt.append(y); yl.append(f"{a} = {lv[:28]}")
            y += 1
        y += 0.6
    ax2.set_yticks(yt); ax2.set_yticklabels(yl, fontsize=7)
    ax2.set_xlabel("specifications, sorted by estimate")
    ax2.invert_yaxis()
    ax2.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    return out
