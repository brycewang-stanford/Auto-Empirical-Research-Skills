"""
Detection: given a *collection* of reported test statistics, is this literature
(or this agent's output) p-hacked?

Implements the testable implications of no-p-hacking on the p-curve from
Elliott, Kudrin & Wuethrich (2022, Econometrica) -- non-increasing density,
continuity at the threshold -- plus the classical p-curve tools of Simonsohn,
Nelson & Simmons and the caliper test of Gerber & Malhotra.

Also the threshold tests of Adda, Decker & Ottaviani (2020, PNAS), who ran
them on 12,621 primary-outcome p-values from ClinicalTrials.gov: a local
polynomial density-jump test at z = 1.96 (Cattaneo, Jansson & Ma 2020), the
phase II vs phase III comparison of the share significant, and the
selective-continuation decomposition -- how much of a later stage's excess
significance a continuation rule estimated on the earlier stage explains.

Three signatures at the threshold, and they are not the same thing:
  spike just past the line       -> individual results pushed across (p-hacking)
  level shift, no spike          -> results below the line missing (selective reporting)
  neither, but a later stage has -> selection between stages (continuation),
  more significant results          which no threshold test can see

Every test here is a test of the *distribution across studies*. None of them
can convict a single paper; that is a property of the method, not a limitation
of the implementation, and the report says so.
"""
from __future__ import annotations

import numpy as np
from scipy import stats

__all__ = ["binomial_test", "fisher_test", "stouffer_test", "lcm_test",
           "discontinuity_test", "caliper_test", "pcurve_power", "report",
           "density_jump_test", "spike_test", "phase_shift_test",
           "continuation_decomposition", "phase_report"]


def _significant(p, alpha):
    p = np.asarray(p, float)
    p = p[np.isfinite(p)]
    return p[(p > 0) & (p < alpha)]


# --------------------------------------------------------------------------
# 1. Binomial: under no p-hacking the p-curve is non-increasing, so among
#    significant results at least half should fall below alpha/2.
# --------------------------------------------------------------------------

def binomial_test(pvals, alpha=0.05) -> dict:
    ps = _significant(pvals, alpha)
    n = ps.size
    if n < 5:
        return {"test": "binomial", "n": int(n), "note": "too few significant results"}
    k = int(np.sum(ps < alpha / 2))
    # one-sided against p-hacking: TOO FEW small p-values (left-skew)
    p_left = stats.binomtest(k, n, 0.5, alternative="less").pvalue
    return {
        "test": "binomial", "n": int(n), "n_below_half_alpha": k,
        "share_below_half_alpha": k / n,
        "p_value": float(p_left),
        "reads": "small p_value => left-skewed p-curve => p-hacking / no evidential value",
    }


# --------------------------------------------------------------------------
# 2/3. Fisher and Stouffer aggregation of the *conditional* p-curve.
# --------------------------------------------------------------------------

def _pp(ps, alpha):
    """pp-values: position of each p within (0, alpha) under the null."""
    return np.clip(ps / alpha, 1e-12, 1 - 1e-12)


def fisher_test(pvals, alpha=0.05) -> dict:
    ps = _significant(pvals, alpha)
    if ps.size < 5:
        return {"test": "fisher", "n": int(ps.size), "note": "too few significant results"}
    pp = _pp(ps, alpha)
    chi = -2 * np.sum(np.log(pp))
    right = float(stats.chi2.sf(chi, 2 * ps.size))          # right-skew: evidential
    left = float(stats.chi2.cdf(chi, 2 * ps.size))          # left-skew: p-hacked
    return {"test": "fisher", "n": int(ps.size), "chi2": float(chi),
            "p_right_skew": right, "p_left_skew": left,
            "reads": "small p_left_skew => p-hacking; small p_right_skew => genuine effect"}


def stouffer_test(pvals, alpha=0.05) -> dict:
    ps = _significant(pvals, alpha)
    if ps.size < 5:
        return {"test": "stouffer", "n": int(ps.size), "note": "too few significant results"}
    z = stats.norm.ppf(_pp(ps, alpha))
    Z = float(np.sum(z) / np.sqrt(z.size))
    return {"test": "stouffer", "n": int(ps.size), "Z": Z,
            "p_right_skew": float(stats.norm.cdf(Z)),
            "p_left_skew": float(stats.norm.sf(Z))}


# --------------------------------------------------------------------------
# 4. Monotonicity via the least concave majorant (Elliott et al. 2022).
#    Under no p-hacking the density of p on (0, alpha) is non-increasing, so the
#    CDF is concave. Distance between the empirical CDF and its LCM is the
#    statistic; the null distribution is bootstrapped under the least favourable
#    null (uniform), which is the boundary of the concave cone.
# --------------------------------------------------------------------------

def _lcm(x, y):
    """Least concave majorant of the points (x, y), returned at the x grid."""
    pts = [(x[0], y[0])]
    for i in range(1, len(x)):
        while len(pts) >= 2:
            (x0, y0), (x1, y1) = pts[-2], pts[-1]
            if (y1 - y0) * (x[i] - x0) <= (y[i] - y0) * (x1 - x0):
                pts.pop()
            else:
                break
        pts.append((x[i], y[i]))
    px, py = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
    return np.interp(x, px, py)


def lcm_test(pvals, alpha=0.05, B=2000, seed=0) -> dict:
    ps = np.sort(_significant(pvals, alpha))
    n = ps.size
    if n < 15:
        return {"test": "lcm_monotonicity", "n": int(n), "note": "too few significant results"}
    u = ps / alpha
    def stat(v):
        v = np.sort(v)
        m = v.size
        ecdf = np.arange(1, m + 1) / m
        return float(np.max(_lcm(v, ecdf) - ecdf) * np.sqrt(m))
    obs = stat(u)
    rng = np.random.default_rng(seed)
    null = np.array([stat(rng.uniform(size=n)) for _ in range(B)])
    return {"test": "lcm_monotonicity", "n": int(n), "stat": obs,
            "p_value": float((1 + np.sum(null >= obs)) / (B + 1)),
            "reads": "small p_value => p-curve is NOT non-increasing => p-hacking"}


# --------------------------------------------------------------------------
# 5. Discontinuity of the p-curve at the threshold (bunching just below 0.05).
# --------------------------------------------------------------------------

def _counterfactual_counts(x, cutoff, lo, hi, nbins, donut, degree=2):
    """Poisson log-linear fit of the density away from the cutoff.

    A 50/50 null for bunching is only right when the underlying density is
    locally flat. Under a genuine effect the density of |z| RISES through 1.96,
    so a naive caliper test flags honest literatures. We instead fit a smooth
    counterfactual on bins outside a donut around the cutoff and compare the
    observed count in the donut against it.
    """
    x = x[(x >= lo) & (x <= hi)]
    edges = np.linspace(lo, hi, nbins + 1)
    counts, _ = np.histogram(x, bins=edges)
    centers = (edges[:-1] + edges[1:]) / 2
    outside = np.abs(centers - cutoff) > donut
    if outside.sum() < 4 or counts[outside].sum() < 10:
        return None
    # polynomial (default quadratic) in the bin centre, fitted by Poisson IRLS
    # on the outside bins
    k = int(degree) + 1
    Z = np.column_stack([(centers[outside] - cutoff) ** j for j in range(k)])
    y = counts[outside].astype(float)
    beta = np.zeros(k)
    beta[0] = np.log(max(y.mean(), 1e-6))
    for _ in range(50):
        mu = np.clip(np.exp(Z @ beta), 1e-8, None)
        W = np.diag(mu)
        try:
            step = np.linalg.solve(Z.T @ W @ Z + 1e-8 * np.eye(k), Z.T @ (y - mu))
        except np.linalg.LinAlgError:
            return None
        beta += step
        if np.max(np.abs(step)) < 1e-8:
            break
    Zall = np.column_stack([(centers - cutoff) ** j for j in range(k)])
    pred = np.exp(Zall @ beta)
    _counterfactual_counts.last_cov = np.linalg.pinv(Z.T @ np.diag(np.clip(np.exp(Z @ beta), 1e-8, None)) @ Z)
    _counterfactual_counts.last_Z = Zall
    return counts, pred, centers, edges


def discontinuity_test(pvals, cutoff=0.05, window=0.04, nbins=16, donut=0.005) -> dict:
    """Excess mass just below the p-value threshold, against a smooth counterfactual."""
    p = np.asarray(pvals, float)
    p = p[np.isfinite(p)]
    res = _counterfactual_counts(p, cutoff, max(cutoff - window, 1e-6),
                                 cutoff + window, nbins, donut)
    if res is None:
        return {"test": "discontinuity", "note": "too few results near the cutoff"}
    counts, pred, centers, _ = res
    inner_below = (centers < cutoff) & (np.abs(centers - cutoff) <= donut)
    obs = float(counts[inner_below].sum())
    exp = float(pred[inner_below].sum())
    if exp < 5:
        return {"test": "discontinuity", "note": "counterfactual too thin to test"}
    pval = float(stats.poisson.sf(obs - 1, exp))
    return {"test": "discontinuity", "n": int(counts.sum()), "cutoff": cutoff,
            "observed_just_below": obs, "counterfactual_just_below": round(exp, 2),
            "excess_mass_ratio": round(obs / exp, 3), "p_value": pval,
            "reads": "excess_mass_ratio >> 1 with small p_value => bunching just below the threshold"}


# --------------------------------------------------------------------------
# 6. Caliper test on z-statistics (Gerber & Malhotra; Brodeur et al.).
# --------------------------------------------------------------------------

def caliper_test(zstats, center=1.96, caliper=0.20, window=1.0,
                 nbins=20, naive=True) -> dict:
    """Gerber-Malhotra caliper, reported both naively and against a counterfactual.

    The naive form tests share_above == 0.5 inside the caliper. That null is
    correct only if the density of |z| is locally flat, which it is not when a
    real effect is present. The counterfactual form is the one to trust.
    """
    z = np.abs(np.asarray(zstats, float))
    z = z[np.isfinite(z)]
    band = z[(z >= center - caliper) & (z <= center + caliper)]
    n = band.size
    out = {"test": "caliper", "n": int(n), "center": center, "caliper": caliper}
    if n < 20:
        return {**out, "note": "too few statistics in the caliper"}
    above = int(np.sum(band > center))
    if naive:
        out["naive_share_above"] = above / n
        out["naive_p_value"] = float(
            stats.binomtest(above, n, 0.5, alternative="greater").pvalue)
    res = _counterfactual_counts(z, center, center - window, center + window,
                                 nbins, caliper)
    if res is None:
        return {**out, "p_value": out.get("naive_p_value"),
                "note": "counterfactual unavailable; naive result reported"}
    counts, pred, centers, _ = res
    inner_above = (centers > center) & (np.abs(centers - center) <= caliper)
    obs = float(counts[inner_above].sum())
    exp = float(pred[inner_above].sum())
    if exp < 5:
        return {**out, "p_value": out.get("naive_p_value"),
                "note": "counterfactual too thin; naive result reported"}
    out.update({
        "observed_just_above": obs, "counterfactual_just_above": round(exp, 2),
        "excess_mass_ratio": round(obs / exp, 3),
        "p_value": float(stats.poisson.sf(obs - 1, exp)),
        "reads": "excess_mass_ratio >> 1 => statistics pushed over the significance line",
    })
    return out


def spike_test(zstats, center=1.96, caliper=0.20, window=0.8, nbins=16, degree=1) -> dict:
    """Excess mass in [center, center + caliper] against a counterfactual fitted
    on the right side of the threshold ONLY (beyond the caliper).

    The caliper test's counterfactual runs *through* the threshold, so it
    flags any discontinuity there -- a spike or a level shift alike. This one
    asks whether the density just past the line is out of line with the
    density further past it. A spike says results were pushed across
    (p-hacking); a clean spike test with a positive density jump says the
    results below the line are missing (selective reporting).
    """
    z = np.abs(np.asarray(zstats, float))
    z = z[np.isfinite(z)]
    out = {"test": "spike", "center": center, "caliper": caliper, "window": window}
    res = _counterfactual_counts(z, center, center, center + window, nbins, caliper, degree=degree)
    if res is None:
        return {**out, "note": "too few statistics past the threshold"}
    counts, pred, centers, _ = res
    cov, Zall = _counterfactual_counts.last_cov, _counterfactual_counts.last_Z
    inner = (centers > center) & (centers - center <= caliper)
    obs = float(counts[inner].sum()); exp = float(pred[inner].sum())
    out["n"] = int(counts.sum())
    if exp < 5:
        return {**out, "note": "counterfactual too thin to test"}
    # the counterfactual is an extrapolated estimate, not a known quantity:
    # delta-method variance of the predicted inner total, added to the Poisson
    # variance of the observed count
    g = (pred[inner][:, None] * Zall[inner]).sum(axis=0)
    var_exp = float(g @ cov @ g)
    T = (obs - exp) / np.sqrt(exp + var_exp)
    out.update({
        "observed_just_above": obs, "counterfactual_just_above": round(exp, 2),
        "counterfactual_se": round(float(np.sqrt(var_exp)), 2),
        "excess_mass_ratio": round(obs / exp, 3), "z": round(float(T), 3),
        "p_value": float(stats.norm.sf(T)),
        "reads": ("excess_mass_ratio >> 1 => a spike just past the line relative to the density beyond "
                  "it: results pushed across (p-hacking), as opposed to a level shift"),
    })
    return out


# --------------------------------------------------------------------------
# 7. Simonsohn's p-curve power estimate.
# --------------------------------------------------------------------------

def pcurve_power(pvals, alpha=0.05) -> dict:
    ps = _significant(pvals, alpha)
    if ps.size < 5:
        return {"test": "pcurve_power", "n": int(ps.size), "note": "too few significant results"}
    zc = stats.norm.isf(alpha / 2)

    def loss(ncp):
        pp = stats.norm.sf(zc - ncp) + stats.norm.cdf(-zc - ncp)
        ppv = np.clip((stats.norm.sf(stats.norm.isf(ps / 2) - ncp)
                       + stats.norm.cdf(-stats.norm.isf(ps / 2) - ncp)) / pp, 1e-9, 1)
        return float(np.mean(ppv) - 0.5) ** 2

    grid = np.linspace(0, 6, 601)
    ncp = float(grid[np.argmin([loss(g) for g in grid])])
    power = float(stats.norm.sf(zc - ncp) + stats.norm.cdf(-zc - ncp))
    return {"test": "pcurve_power", "n": int(ps.size), "implied_ncp": ncp,
            "estimated_power": power,
            "reads": "power near alpha => the significant findings carry no evidential value"}


# --------------------------------------------------------------------------
# 8. Density jump at the threshold. The local polynomial density estimator of
#    Cattaneo, Jansson & Ma (2020): on each side of the cutoff, regress the
#    empirical CDF on a polynomial in (x - c) with triangular kernel weights;
#    the density at c is the fitted slope. No pre-binning, so no bin-alignment
#    knob. This is the test Adda, Decker & Ottaviani (2020) run on registered
#    trial results, and it answers a different question from the caliper: not
#    "is there a spike just past the line" but "is the density on the two
#    sides of the line the same". A jump with no spike is what strategic
#    non-reporting of results below the line looks like.
# --------------------------------------------------------------------------

def _lp_density_side(x, F, c, h, side, poly=2):
    """Local polynomial density at c from one side. Returns (f, n_used)."""
    if side > 0:
        m = (x >= c) & (x <= c + h)
    else:
        m = (x < c) & (x >= c - h)
    n = int(m.sum())
    if n < poly + 2:
        return np.nan, n
    u = (x[m] - c) / h
    w = np.sqrt(1.0 - np.abs(u))                      # triangular kernel, sqrt for WLS
    d = x[m] - c
    Z = np.column_stack([d ** k for k in range(poly + 1)])
    beta, *_ = np.linalg.lstsq(Z * w[:, None], F[m] * w, rcond=None)
    return float(beta[1]), n


def _default_h(x):
    n = x.size
    return float(np.clip(2.0 * np.std(x) * n ** (-0.2), 0.4, 1.5))


def density_jump_test(zstats, center=1.96, h=None, poly=2, B=300, seed=0, min_side=30) -> dict:
    """Is the density of |z| continuous at the significance threshold?

    `jump` = f(c+) - f(c-), with a bootstrap standard error. `p_value` is
    one-sided against an UPWARD jump (more mass just past the line than just
    before it), which is the direction both p-hacking and selective reporting
    predict; `p_two_sided` is also given. Bandwidth defaults to
    2 sd(|z|) n^(-1/5), clipped to [0.4, 1.5]; pass `h` to check sensitivity.
    """
    x = np.abs(np.asarray(zstats, float))
    x = x[np.isfinite(x)]
    n = x.size
    out = {"test": "density_jump", "center": center, "n": int(n)}
    if n < 2 * min_side:
        return {**out, "note": "too few statistics for a density estimate"}
    h = float(h) if h is not None else _default_h(x)
    out["h"] = round(h, 4)

    def both(v):
        F = stats.rankdata(v, method="average") / v.size
        fl, nl = _lp_density_side(v, F, center, h, -1, poly)
        fr, nr = _lp_density_side(v, F, center, h, +1, poly)
        return fl, fr, nl, nr

    fl, fr, nl, nr = both(x)
    out.update({"n_left": nl, "n_right": nr})
    if nl < min_side or nr < min_side or not (np.isfinite(fl) and np.isfinite(fr)):
        return {**out, "note": f"fewer than {min_side} statistics within h on one side"}
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(B):
        v = x[rng.integers(0, n, n)]
        bl, br, _, _ = both(v)
        if np.isfinite(bl) and np.isfinite(br):
            boots.append(br - bl)
    boots = np.asarray(boots)
    if boots.size < 50:
        return {**out, "note": "bootstrap failed on most draws"}
    se = float(boots.std(ddof=1))
    jump = float(fr - fl)
    T = jump / se if se > 0 else np.nan
    out.update({
        "f_left": round(fl, 5), "f_right": round(fr, 5), "jump": round(jump, 5),
        "log_ratio": round(float(np.log(max(fr, 1e-9) / max(fl, 1e-9))), 4),
        "se": round(se, 5), "z": round(float(T), 3),
        "p_value": float(stats.norm.sf(T)),
        "p_two_sided": float(2 * stats.norm.sf(abs(T))),
        "reads": ("upward jump => the density of |z| is higher just past the line than just before it: "
                  "results below the line are missing (selective reporting) or were pushed across "
                  "(p-hacking); read together with the caliper spike test"),
    })
    return out


# --------------------------------------------------------------------------
# 9. Across stages. Adda, Decker & Ottaviani compare phase II with phase III:
#    the share of significant results rises from 45.7% to 70.6% for industry
#    sponsors with NO discontinuity at 1.96 in phase II -- the distribution
#    shifts smoothly, because firms continue to phase III only after promising
#    phase II results. Selection between stages is invisible to every
#    threshold test above, so it needs its own comparison.
# --------------------------------------------------------------------------

def phase_shift_test(z_early, z_late, threshold=1.96) -> dict:
    """Share significant in a later stage against an earlier one, with a
    two-proportion test and a one-sided Kolmogorov-Smirnov test that the
    later stage's |z| stochastically dominates the earlier one's."""
    a = np.abs(np.asarray(z_early, float)); a = a[np.isfinite(a)]
    b = np.abs(np.asarray(z_late, float)); b = b[np.isfinite(b)]
    out = {"test": "phase_shift", "threshold": threshold, "n_early": int(a.size), "n_late": int(b.size)}
    if a.size < 20 or b.size < 20:
        return {**out, "note": "too few results in a stage"}
    s1, s2 = float(np.mean(a > threshold)), float(np.mean(b > threshold))
    pool = (np.sum(a > threshold) + np.sum(b > threshold)) / (a.size + b.size)
    se = float(np.sqrt(pool * (1 - pool) * (1 / a.size + 1 / b.size)))
    zst = (s2 - s1) / se if se > 0 else np.nan
    # scipy: alternative='less' tests F_data1(x) < F_data2(x) somewhere, i.e.
    # data1 (the later stage) is stochastically LARGER
    ks = stats.ks_2samp(b, a, alternative="less", method="asymp")
    out.update({
        "share_significant_early": round(s1, 4), "share_significant_late": round(s2, 4),
        "difference_pp": round(100 * (s2 - s1), 2), "z": round(float(zst), 3),
        "p_value": float(stats.norm.sf(zst)) if np.isfinite(zst) else np.nan,
        "ks_dominance_stat": round(float(ks.statistic), 4), "ks_dominance_p": float(ks.pvalue),
        "reads": ("small p_value => the later stage has more significant results than the earlier one. "
                  "That is selection or manipulation between stages, not evidence of either on its own: "
                  "run continuation_decomposition to see how much a continuation rule explains"),
    })
    return out


def _logit_fit(X, y, ridge=1e-8, iters=60):
    X = np.asarray(X, float); y = np.asarray(y, float)
    beta = np.zeros(X.shape[1])
    H = None
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ beta, -30, 30)))
        W = np.clip(p * (1 - p), 1e-10, None)
        H = X.T @ (X * W[:, None]) + ridge * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        beta = beta + step
        if np.max(np.abs(step)) < 1e-9:
            break
    return beta, np.linalg.inv(H)


def continuation_decomposition(z_early, continued, z_late, threshold=1.96,
                               covariates=None, B=200, seed=0) -> dict:
    """How much of a later stage's excess significance a continuation rule explains.

    Adda, Decker & Ottaviani (2020), section "Selective continuation": fit
    continuation ~ logistic(alpha + beta |z_early| + x'gamma) on the early-stage
    results, reweight the early-stage distribution by the fitted continuation
    probabilities, and compare the reweighted share significant with the
    later stage's actual share. The part of (late - early) the reweighting
    reproduces is *explained* by selection on early results; the remainder is
    *unexplained* -- selective reporting, manipulation, or true improvement
    between stages that the early result does not predict.

    z_early and continued are aligned over early-stage projects; z_late holds
    the later-stage results that were reported (any length). Standard errors
    by bootstrap over projects.
    """
    z1 = np.abs(np.asarray(z_early, float))
    c = np.asarray(continued, float)
    m = np.isfinite(z1) & np.isfinite(c)
    z1, c = z1[m], c[m]
    Xc = None
    if covariates is not None:
        Xc = np.atleast_2d(np.asarray(covariates, float))
        Xc = Xc.T if Xc.shape[0] != len(m) else Xc
        Xc = Xc[m]
    z2 = np.abs(np.asarray(z_late, float)); z2 = z2[np.isfinite(z2)]
    out = {"test": "continuation_decomposition", "threshold": threshold,
           "n_early": int(z1.size), "n_continued": int(c.sum()), "n_late": int(z2.size)}
    if z1.size < 30 or z2.size < 20 or c.sum() < 10 or c.sum() > z1.size - 10:
        return {**out, "note": "too few projects, or no variation in continuation"}

    def design(z, X):
        cols = [np.ones_like(z), z]
        if X is not None:
            cols.extend(X.T)
        return np.column_stack(cols)

    def decompose(z1_, c_, X_, z2_):
        beta, cov = _logit_fit(design(z1_, X_), c_)
        pi = 1 / (1 + np.exp(-np.clip(design(z1_, X_) @ beta, -30, 30)))
        s1 = float(np.mean(z1_ > threshold)); s2 = float(np.mean(z2_ > threshold))
        s_cf = float(np.sum(pi * (z1_ > threshold)) / np.sum(pi))
        return beta, cov, pi, s1, s2, s_cf

    beta, cov, pi, s1, s2, s_cf = decompose(z1, c, Xc, z2)
    actual, explained, unexplained = s2 - s1, s_cf - s1, s2 - s_cf
    if np.max(np.abs(beta)) > 25:
        out["note"] = ("continuation is (nearly) a deterministic function of the early z: the logit sits "
                       "at the separation boundary and the reweighting counterfactual is not credible")
    rng = np.random.default_rng(seed)
    bu, be = [], []
    for _ in range(B):
        i = rng.integers(0, z1.size, z1.size); j = rng.integers(0, z2.size, z2.size)
        try:
            _, _, _, b1, b2, bcf = decompose(z1[i], c[i], None if Xc is None else Xc[i], z2[j])
        except np.linalg.LinAlgError:
            continue
        bu.append(b2 - bcf); be.append(bcf - b1)
    bu, be = np.asarray(bu), np.asarray(be)
    se_u = float(bu.std(ddof=1)) if bu.size > 20 else np.nan
    zu = unexplained / se_u if se_u and se_u > 0 else np.nan
    grid_z = [1.0, 1.96, 3.0]
    out.update({
        "logit": {"beta_z": round(float(beta[1]), 4), "se_z": round(float(np.sqrt(cov[1, 1])), 4),
                  "p_z": float(2 * stats.norm.sf(abs(beta[1] / np.sqrt(cov[1, 1])))),
                  "mean_continuation": round(float(pi.mean()), 4),
                  "continuation_at_z": {str(g): round(float(1 / (1 + np.exp(-np.clip(beta[0] + beta[1] * g, -30, 30)))), 4)
                                        for g in grid_z}},
        "share_significant_early": round(s1, 4),
        "share_significant_late": round(s2, 4),
        "share_significant_counterfactual": round(s_cf, 4),
        "difference_pp": round(100 * actual, 2),
        "explained_pp": round(100 * explained, 2),
        "unexplained_pp": round(100 * unexplained, 2),
        "explained_share": (round(float(explained / actual), 3) if abs(actual) > 1e-9 else None),
        "unexplained_se_pp": round(100 * se_u, 2) if np.isfinite(se_u) else None,
        "unexplained_ci95_pp": ([round(100 * float(q), 2) for q in np.percentile(bu, [2.5, 97.5])]
                                if bu.size > 20 else None),
        "p_value": float(2 * stats.norm.sf(abs(zu))) if np.isfinite(zu) else np.nan,
        "reads": ("explained_share is the part of the late-stage excess that continuing only after good "
                  "early results reproduces; a significant unexplained_pp is what remains to be accounted "
                  "for by selective reporting or manipulation between the stages"),
    })
    return out


def phase_report(z_early, z_late, continued=None, threshold=1.96, seed=0) -> dict:
    """The across-stages battery: threshold tests on each stage, the phase
    shift, and -- when the early stage's continuation flags are known -- the
    selective-continuation decomposition."""
    out = {
        "early": {"n": int(np.isfinite(np.asarray(z_early, float)).sum()),
                  "density_jump": density_jump_test(z_early, center=threshold, seed=seed),
                  "caliper": caliper_test(z_early, center=threshold),
                  "spike": spike_test(z_early, center=threshold)},
        "late": {"n": int(np.isfinite(np.asarray(z_late, float)).sum()),
                 "density_jump": density_jump_test(z_late, center=threshold, seed=seed),
                 "caliper": caliper_test(z_late, center=threshold),
                 "spike": spike_test(z_late, center=threshold)},
        "phase_shift": phase_shift_test(z_early, z_late, threshold),
    }
    if continued is not None:
        out["continuation"] = continuation_decomposition(z_early, continued, z_late, threshold, seed=seed)
    late_jump = out["late"]["density_jump"].get("p_value", 1.0) < 0.05
    late_spike = out["late"]["spike"].get("p_value", 1.0) < 0.05
    shift = out["phase_shift"].get("p_value", 1.0) < 0.05
    cont = out.get("continuation", {})
    unexpl = cont.get("p_value", 1.0) < 0.05 if "p_value" in cont else None
    if late_spike:
        sig = "spike past the threshold in the later stage: individual results pushed across (p-hacking)"
    elif late_jump:
        sig = ("discontinuity at the threshold in the later stage with no spike beyond it: results "
               "below the line are missing (selective reporting)")
    elif shift and unexpl is False:
        sig = ("more significant results in the later stage, no threshold signature, and the continuation "
               "rule explains the rise: selection between stages, not manipulation")
    elif shift and unexpl:
        sig = ("more significant results in the later stage, no threshold signature, and the continuation "
               "rule does NOT explain the rise: selective reporting between stages is the remaining candidate")
    elif shift:
        sig = ("more significant results in the later stage and no threshold signature; supply the "
               "continuation flags to separate selection from reporting")
    else:
        sig = "no across-stage or threshold signature"
    out["signature"] = sig
    out["caveat"] = ("These are tests on the distribution across many projects. They cannot establish "
                     "that any individual result was p-hacked or withheld.")
    return out


def report(pvals=None, zstats=None, alpha=0.05, seed=0) -> dict:
    """Run the full detection battery. Supply p-values, z-statistics, or both."""
    if pvals is None and zstats is None:
        raise ValueError("supply pvals or zstats")
    if pvals is None:
        pvals = 2 * stats.norm.sf(np.abs(np.asarray(zstats, float)))
    if zstats is None:
        zstats = stats.norm.isf(np.asarray(pvals, float) / 2)
    out = {
        "n_total": int(np.isfinite(np.asarray(pvals, float)).sum()),
        "n_significant": int(_significant(pvals, alpha).size),
        "tests": [
            binomial_test(pvals, alpha), fisher_test(pvals, alpha),
            stouffer_test(pvals, alpha), lcm_test(pvals, alpha, seed=seed),
            discontinuity_test(pvals), caliper_test(zstats),
            density_jump_test(zstats, seed=seed), spike_test(zstats),
            pcurve_power(pvals, alpha),
        ],
    }
    SHAPE = {"binomial", "fisher", "stouffer", "lcm_monotonicity"}
    def _flags(t):
        return ((isinstance(t.get("p_value"), float) and t["p_value"] < 0.05)
                or (isinstance(t.get("p_left_skew"), float) and t["p_left_skew"] < 0.05))
    flags = [t["test"] for t in out["tests"] if _flags(t)]
    shape_flags = [t for t in flags if t in SHAPE]
    bunch_flags = [t for t in flags if t not in SHAPE]
    out["n_tests_flagging"] = len(flags)
    out["flagged_by"] = flags
    out["shape_tests_flagging"] = shape_flags
    out["bunching_tests_flagging"] = bunch_flags
    # Shape tests carry clean nulls; bunching tests alone are weak evidence
    # because a rising density around the threshold mimics bunching.
    out["verdict"] = (
        "strong evidence of p-hacking / selective reporting"
        if len(shape_flags) >= 2 else
        "moderate evidence of p-hacking" if shape_flags and bunch_flags else
        "weak / ambiguous signal -- bunching only, shape tests clean"
        if bunch_flags else
        "some evidence of p-hacking" if shape_flags else
        "no distributional evidence of p-hacking")
    spike = "spike" in bunch_flags
    shift = "density_jump" in bunch_flags
    out["threshold_signature"] = (
        "spike just past the threshold: individual results pushed across the line (p-hacking)"
        if spike else
        "discontinuity at the threshold without a spike beyond it: results below the line are "
        "missing rather than pushed across (selective reporting)"
        if shift else
        "no threshold signature; a rise in the share significant between stages of a project, "
        "if present, is selection (continuation) and needs phase_report, not a threshold test")
    out["caveat"] = ("These are tests on the distribution across many studies. "
                     "They cannot establish that any individual result was p-hacked.")
    return out
