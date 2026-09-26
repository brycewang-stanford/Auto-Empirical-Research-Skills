"""
Monte Carlo for the twelve p-hacking strategies of Stefan & Schoenbrodt (2023),
"Big little lies: a compendium and simulation of p-hacking strategies",
Royal Society Open Science 10:220346.

Their reference implementation is the R package phackR. This is an independent
Python re-implementation so the strategies can be exercised inside an agent
evaluation without an R round-trip. Data are always generated under a TRUE NULL,
so every rejection counted here is a false positive by construction.

Each strategy returns (p_original, p_hacked, n_attempts).

Strategy 26 is not from the compendium. It is the across-stages selection
that Adda, Decker & Ottaviani (2020, PNAS) study on ClinicalTrials.gov:
continue from a pilot to a confirmatory study only after a promising pilot.
With a fresh confirmatory sample that is not p-hacking at all -- the
confirmatory test keeps its size -- and the strategy is here to make that
point measurable, and to measure what happens once the pilot is pooled in.
`continuation_shift` simulates the population version: heterogeneous true
effects, a continuation rule, optional concealment, and the phase II / phase
III distributions the detection module is then asked to tell apart.
"""
from __future__ import annotations

import numpy as np
from scipy import stats

__all__ = ["STRATEGIES", "run_strategy", "false_positive_rate", "sweep",
           "workflow", "continuation_shift"]


# ---------------------------------------------------------------- helpers ---

def _corr_normal(rng, n, k, r):
    """k columns with equicorrelation r."""
    if k == 1:
        return rng.normal(size=(n, 1))
    common = rng.normal(size=(n, 1))
    idio = rng.normal(size=(n, k))
    w = np.sqrt(max(r, 0.0))
    return w * common + np.sqrt(1 - max(r, 0.0)) * idio


def _ttest(a, b):
    return float(stats.ttest_ind(a, b, equal_var=True).pvalue)


def _ols_p(y, x, extra=None):
    X = [np.ones(len(y)), np.asarray(x, float)]
    if extra is not None and np.size(extra):
        E = np.atleast_2d(np.asarray(extra, float))
        if E.shape[0] != len(y):
            E = E.T
        X.extend(E.T)
    X = np.column_stack(X)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    u = y - X @ b
    dof = len(y) - X.shape[1]
    if dof <= 0:
        return 1.0
    s2 = (u @ u) / dof
    V = s2 * np.linalg.pinv(X.T @ X)
    se = np.sqrt(max(V[1, 1], 1e-300))
    return float(2 * stats.t.sf(abs(b[1] / se), dof))


def _pick(p_orig, cands, alpha, ambitious=False):
    """Reporting rule -> (p_original, p_reported, n_attempts).

    Default is 'modest' p-hacking: stop at the first significant result.
    `ambitious=True` keeps searching and reports the smallest p-value found,
    which does not change the false-positive rate but does change which
    estimate gets published (Stefan & Schoenbrodt, section 6).
    """
    allp = [float(p) for p in (p_orig, *cands) if np.isfinite(p)]
    if not allp:
        return float(p_orig), float(p_orig), 1
    if ambitious:
        return float(p_orig), float(min(allp)), len(allp)
    for i, p in enumerate(allp):
        if p < alpha:
            return float(p_orig), float(p), i + 1
    return float(p_orig), float(p_orig), len(allp)


# ------------------------------------------------------------ strategies ---

def s01_selective_dv(rng, n=100, k=5, r=0.6, alpha=0.05, ambitious=False, **_):
    """1. Selective reporting of the dependent variable."""
    g = np.r_[np.zeros(n), np.ones(n)]
    Y = _corr_normal(rng, 2 * n, k, r)
    ps = [_ttest(Y[g == 0, j], Y[g == 1, j]) for j in range(k)]
    return _pick(ps[0], ps[1:], alpha, ambitious)


def s02_selective_iv(rng, n=200, k=5, r=0.6, alpha=0.05, ambitious=False, **_):
    """2. Selective reporting of the independent variable."""
    y = rng.normal(size=n)
    X = _corr_normal(rng, n, k, r)
    ps = [_ols_p(y, X[:, j]) for j in range(k)]
    return _pick(ps[0], ps[1:], alpha, ambitious)


def s03_optional_stopping(rng, n_min=20, n_max=100, step=5, alpha=0.05,
                          ambitious=False, **_):
    """3. Optional stopping: peek after every `step` new observations."""
    a = rng.normal(size=n_max); b = rng.normal(size=n_max)
    ps = [_ttest(a[:m], b[:m]) for m in range(n_min, n_max + 1, step)]
    return _pick(ps[0], ps[1:], alpha, ambitious)


def s04_outlier_exclusion(rng, n=100, alpha=0.05, ambitious=False, **_):
    """4. Outlier exclusion under several defensible rules."""
    a, b = rng.normal(size=n), rng.normal(size=n)
    p0 = _ttest(a, b)
    ps = []
    for k in (2.0, 2.5, 3.0):
        ka = np.abs(a - a.mean()) <= k * a.std(ddof=1)
        kb = np.abs(b - b.mean()) <= k * b.std(ddof=1)
        ps.append(_ttest(a[ka], b[kb]))
    for k in (1.5, 3.0):
        def keep(x):
            q1, q3 = np.percentile(x, [25, 75]); i = q3 - q1
            return (x >= q1 - k * i) & (x <= q3 + k * i)
        ps.append(_ttest(a[keep(a)], b[keep(b)]))
    return _pick(p0, ps, alpha, ambitious)


def s05_covariates(rng, n=200, k=3, r=0.3, alpha=0.05, ambitious=False, **_):
    """5. Controlling for covariates, entered in every combination."""
    import itertools
    g = rng.integers(0, 2, n).astype(float)
    C = _corr_normal(rng, n, k, r)
    y = rng.normal(size=n) + 0.3 * C[:, 0]
    p0 = _ols_p(y, g)
    ps = []
    for rr in range(1, k + 1):
        for combo in itertools.combinations(range(k), rr):
            ps.append(_ols_p(y, g, C[:, list(combo)]))
    return _pick(p0, ps, alpha, ambitious)


def s06_scale_redefinition(rng, n=100, n_items=5, r=0.5, max_drop=3,
                           alpha=0.05, ambitious=False, **_):
    """6. Scale redefinition: drop items from a composite score."""
    import itertools
    g = np.r_[np.zeros(n), np.ones(n)]
    I = _corr_normal(rng, 2 * n, n_items, r)
    p0 = _ttest(I[g == 0].mean(1), I[g == 1].mean(1))
    ps = []
    for d in range(1, max_drop + 1):
        for drop in itertools.combinations(range(n_items), d):
            keep = [j for j in range(n_items) if j not in drop]
            if not keep:
                continue
            s = I[:, keep].mean(1)
            ps.append(_ttest(s[g == 0], s[g == 1]))
    return _pick(p0, ps, alpha, ambitious)


def s07_transformation(rng, n=200, alpha=0.05, ambitious=False, **_):
    """7. Variable transformation of predictor and/or outcome."""
    x = rng.lognormal(0, 1, n); y = rng.lognormal(0, 1, n)
    tf = {"level": lambda v: v, "log": lambda v: np.log(v),
          "sqrt": lambda v: np.sqrt(v),
          "rank": lambda v: stats.rankdata(v),
          "inv": lambda v: 1 / v}
    p0 = _ols_p(y, x)
    ps = [_ols_p(fy(y), fx(x)) for ny, fy in tf.items() for nx, fx in tf.items()
          if not (ny == "level" and nx == "level")]
    return _pick(p0, ps, alpha, ambitious)


def s08_discretize(rng, n=200, alpha=0.05, ambitious=False, **_):
    """8. Discretising a continuous predictor at convenient cutoffs."""
    x = rng.normal(size=n); y = rng.normal(size=n)
    p0 = _ols_p(y, x)
    ps = []
    for q in (25, 33, 40, 50, 60, 67, 75):
        c = np.percentile(x, q)
        d = (x > c).astype(float)
        if 5 < d.sum() < n - 5:
            ps.append(_ttest(y[d == 0], y[d == 1]))
    lo, hi = np.percentile(x, 33), np.percentile(x, 67)   # extreme-group split
    ps.append(_ttest(y[x <= lo], y[x >= hi]))
    return _pick(p0, ps, alpha, ambitious)


def s09_alternative_tests(rng, n=100, alpha=0.05, ambitious=False, **_):
    """9. Exploiting alternative hypothesis tests on the same data."""
    a, b = rng.normal(size=n), rng.normal(size=n)
    p0 = _ttest(a, b)
    ps = [
        float(stats.ttest_ind(a, b, equal_var=False).pvalue),      # Welch
        float(stats.mannwhitneyu(a, b, alternative="two-sided").pvalue),
        float(stats.ks_2samp(a, b).pvalue),
        float(stats.median_test(a, b).pvalue) if hasattr(
            stats.median_test(a, b), "pvalue") else float(stats.median_test(a, b)[1]),
        float(stats.ttest_ind(stats.rankdata(np.r_[a, b])[:n],
                              stats.rankdata(np.r_[a, b])[n:]).pvalue),
    ]
    return _pick(p0, ps, alpha, ambitious)


def s10_imputation(rng, n=200, miss=0.1, alpha=0.05, ambitious=False, **_):
    """10. Favourable imputation of missing values."""
    x = rng.normal(size=n); y = rng.normal(size=n)
    m = rng.random(n) < miss
    xm = x.copy(); xm[m] = np.nan
    p0 = _ols_p(y[~m], xm[~m])                                  # listwise
    ps = []
    for fill in (np.nanmean(xm), np.nanmedian(xm), 0.0):
        xi = np.where(m, fill, xm); ps.append(_ols_p(y, xi))
    xi = xm.copy()                                              # random draws
    for _ in range(3):
        z = xi.copy(); z[m] = rng.choice(x[~m], m.sum())
        ps.append(_ols_p(y, z))
    # regression imputation on a correlated auxiliary
    aux = 0.5 * x + rng.normal(size=n)
    bb = np.polyfit(aux[~m], x[~m], 1)
    ps.append(_ols_p(y, np.where(m, np.polyval(bb, aux), xm)))
    return _pick(p0, ps, alpha, ambitious)


def s11_subgroup(rng, n=200, n_groups=3, alpha=0.05, ambitious=False, **_):
    """11. Subgroup analyses on binary moderators."""
    g = rng.integers(0, 2, n).astype(float)
    y = rng.normal(size=n)
    mods = rng.integers(0, 2, (n, n_groups))
    p0 = _ols_p(y, g)
    ps = []
    for j in range(n_groups):
        for lvl in (0, 1):
            sel = mods[:, j] == lvl
            if sel.sum() > 20 and 5 < g[sel].sum() < sel.sum() - 5:
                ps.append(_ols_p(y[sel], g[sel]))
    return _pick(p0, ps, alpha, ambitious)


def s12_rounding(rng, n=100, level=0.06, alpha=0.05, **_):
    """12. Incorrect rounding: a p just above the line is reported as under it.

    `level` is how far above alpha the researcher is willing to round down,
    e.g. 0.06 means "p = .06, marginally significant" is written up as a
    rejection. The effective type I error becomes `level` rather than `alpha`.
    """
    a, b = rng.normal(size=n), rng.normal(size=n)
    p0 = _ttest(a, b)
    reported = alpha * 0.999 if alpha <= p0 < level else p0
    return float(p0), float(reported), 1


def s26_selective_continuation(rng, n1=50, n2=100, go=0.10, report="pooled",
                               alpha=0.05, ambitious=False, max_pilots=200, **_):
    """26. Selective continuation across stages (Adda, Decker & Ottaviani 2020).

    A pilot of n1 per arm decides whether the confirmatory study of n2 per arm
    is run: continue only if the pilot's p < `go`. What a registry of
    confirmatory results sees is the population *conditional on continuation*,
    so pilots are redrawn until one clears the bar (`n_attempts` counts them).
    Then the project reports:

        'main'    the confirmatory sample alone. A valid test: the false-positive
                  rate stays at alpha. Selective continuation is not p-hacking.
        'pooled'  pilot + confirmatory analysed as one study. The favourable
                  pilot draw is inside the reported statistic: optional stopping
                  with one lenient interim look.
        'best'    the best of pilot-only, main-only and pooled: selective
                  reporting across the stages.

    Returns (p_main, p_reported, n_pilots): p_main is the honest confirmatory p.
    """
    for k in range(1, max_pilots + 1):
        a1, b1 = rng.normal(size=n1), rng.normal(size=n1)
        p1 = _ttest(a1, b1)
        if p1 < go:
            break
    a2, b2 = rng.normal(size=n2), rng.normal(size=n2)
    p_main = _ttest(a2, b2)
    if report == "main":
        return float(p_main), float(p_main), k
    p_pool = _ttest(np.r_[a1, a2], np.r_[b1, b2])
    if report == "pooled":
        return float(p_main), float(p_pool), k
    if report == "best":
        return float(p_main), float(min(p1, p_main, p_pool)), k
    raise KeyError(f"report must be 'main', 'pooled' or 'best', not {report!r}")


def continuation_shift(n_projects=4000, n1=60, n2=60, share_null=0.5, effect_sd=0.35,
                       logit_a=-2.5, logit_b=1.2, signal_sd=1.0, conceal=0.0,
                       threshold=1.96, seed=0) -> dict:
    """The population version: incentives shaping the distribution across phases.

    Each project has a true effect delta (zero with probability `share_null`,
    else half-normal with sd `effect_sd`), a registered pilot z (n1 per arm)
    and, if continued, a fresh confirmatory z (n2 per arm). The sponsor
    continues with probability logistic(a + b * |s|) where s is its own read
    of the pilot -- the same signal plus independent noise of sd `signal_sd`
    -- so the registered z is a noisy public reflection of what drove the
    decision. That is the assumption behind the paper's counterfactual
    (expected later-stage z equals the earlier-stage z, conditional on
    continuing), and it makes `detect.continuation_decomposition` exact in
    expectation on this DGP. `conceal` is the probability that a
    non-significant confirmatory result goes unreported: the small-sponsor
    pattern, which the decomposition should leave *unexplained* and the
    density-jump test should see.

    Returns the arrays the detection module wants plus the shares by stage.
    """
    rng = np.random.default_rng(seed)
    N = int(n_projects)
    delta = np.where(rng.random(N) < share_null, 0.0, np.abs(rng.normal(0, effect_sd, N)))
    z_pilot = delta * np.sqrt(n1 / 2) + rng.normal(size=N)
    signal = delta * np.sqrt(n1 / 2) + rng.normal(0, signal_sd, N)
    pi = 1 / (1 + np.exp(-(logit_a + logit_b * np.abs(signal))))
    continued = rng.random(N) < pi
    z_main = np.full(N, np.nan)
    z_main[continued] = delta[continued] * np.sqrt(n2 / 2) + rng.normal(size=int(continued.sum()))
    reported = continued & ~((np.abs(z_main) < threshold) & (rng.random(N) < conceal))
    zl = z_main[reported]
    return {
        "z_pilot": z_pilot, "continued": continued, "z_main": z_main, "reported": reported,
        "z_main_reported": zl, "delta": delta,
        "share_null": share_null, "n_projects": N, "n_continued": int(continued.sum()),
        "n_reported": int(reported.sum()), "mean_continuation": float(continued.mean()),
        "share_significant_pilot": float(np.mean(np.abs(z_pilot) > threshold)),
        "share_significant_main_all": float(np.mean(np.abs(z_main[continued]) > threshold)),
        "share_significant_main_reported": float(np.mean(np.abs(zl) > threshold)),
        "false_positive_share_main_reported": float(np.mean(
            (np.abs(zl) > threshold) & (delta[reported] == 0))) if reported.any() else np.nan,
    }


STRATEGIES = {
    "01_selective_dv": s01_selective_dv,
    "02_selective_iv": s02_selective_iv,
    "03_optional_stopping": s03_optional_stopping,
    "04_outlier_exclusion": s04_outlier_exclusion,
    "05_covariates": s05_covariates,
    "06_scale_redefinition": s06_scale_redefinition,
    "07_transformation": s07_transformation,
    "08_discretize": s08_discretize,
    "09_alternative_tests": s09_alternative_tests,
    "10_imputation": s10_imputation,
    "11_subgroup": s11_subgroup,
    "12_rounding": s12_rounding,
    "26_selective_continuation": s26_selective_continuation,
}


def run_strategy(name, rng, **kw):
    return STRATEGIES[name](rng, **kw)


def false_positive_rate(name, n_sims=2000, alpha=0.05, seed=0, ambitious=False, **kw):
    rng = np.random.default_rng(seed)
    hacked = np.empty(n_sims); orig = np.empty(n_sims); tries = np.empty(n_sims)
    for i in range(n_sims):
        p0, ph, k = run_strategy(name, rng, alpha=alpha, ambitious=ambitious, **kw)
        orig[i], hacked[i], tries[i] = p0, ph, k
    return {
        "strategy": name, "n_sims": n_sims, "alpha": alpha,
        "ambitious": bool(ambitious),
        "fpr_original": float(np.mean(orig < alpha)),
        "fpr_hacked": float(np.mean(hacked < alpha)),
        "fpr_multiplier": float(np.mean(hacked < alpha) / max(np.mean(orig < alpha), 1e-9)),
        "mean_attempts": float(tries.mean()),
        "median_p_hacked": float(np.median(hacked)),
    }


def sweep(n_sims=2000, alpha=0.05, seed=0, ambitious=False, **kw):
    return [false_positive_rate(n, n_sims=n_sims, alpha=alpha, seed=seed + i,
                                ambitious=ambitious, **kw)
            for i, n in enumerate(STRATEGIES)]


def workflow(sequence, n_sims=2000, alpha=0.05, seed=0):
    """Apply strategies one after another, as a real p-hacking session would.

    Reports the cumulative false-positive rate after each additional step,
    reproducing figure 13 of Stefan & Schoenbrodt: the rate climbs, but with
    sharply diminishing returns per added strategy.
    """
    rng = np.random.default_rng(seed)
    hit = np.zeros((n_sims, len(sequence)), dtype=bool)
    for i in range(n_sims):
        done = False
        for j, name in enumerate(sequence):
            if not done:
                _, ph, _ = run_strategy(name, rng, alpha=alpha)
                done = ph < alpha
            hit[i, j] = done
    cum = hit.mean(axis=0)
    return {"sequence": list(sequence), "alpha": alpha, "n_sims": n_sims,
            "cumulative_fpr": [float(c) for c in cum],
            "marginal_gain": [float(cum[0])] + [float(cum[i] - cum[i - 1])
                                                for i in range(1, len(cum))]}
