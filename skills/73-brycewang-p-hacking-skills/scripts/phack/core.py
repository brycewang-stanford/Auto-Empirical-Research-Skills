"""
Estimation core for the p-hacking skills toolkit.

Deliberately small and dependency-light: (weighted) OLS with multi-way
fixed-effect absorption, HC0-HC3 robust and one/two-way cluster-robust
variance, local-polynomial RDD with rule-of-thumb and Imbens-Kalyanaraman
bandwidths and conventional / bias-corrected / robust inference, 2SLS and LIML
with the Anderson-Rubin test, plus the data transforms that the p-hacking
literature identifies as researcher degrees of freedom (Stefan & Schoenbrodt
2023, strategies 4/6/7/8/10).

Everything returns a plain dict so results are trivially serialisable into the
specification ledger. Arrays (full coefficient vector, full covariance) are
returned only when `full=True` and never reach the ledger.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

__all__ = [
    "TRANSFORMS", "DISCRETIZERS", "OUTLIER_RULES", "KERNELS",
    "apply_transform", "flag_outliers", "absorb", "fit_ols", "impute",
    "rot_bandwidth", "ik_bandwidth", "fit_rdd", "fit_2sls", "fit_lincom",
]

# --------------------------------------------------------------------------
# Variable transforms (researcher degree of freedom: "variable transformation")
# --------------------------------------------------------------------------

def _log(x: np.ndarray) -> np.ndarray:
    shift = 0.0
    finite = x[np.isfinite(x)]
    if finite.size and finite.min() <= 0:
        shift = 1.0 - finite.min()
    return np.log(x + shift)


def _median_split(x):
    return (x > np.nanmedian(x)).astype(float)


def _tercile_extremes(x):
    """Top tercile vs bottom tercile; the middle is dropped (NaN). The
    extreme-group design of strategy 8, which also discards the centre of the
    distribution and so inflates the apparent effect."""
    lo, hi = np.nanpercentile(x, [100 / 3, 200 / 3])
    out = np.full(x.shape, np.nan)
    out[x <= lo] = 0.0
    out[x >= hi] = 1.0
    return out


def _quartile_top(x):
    return (x >= np.nanpercentile(x, 75)).astype(float)


TRANSFORMS = {
    "level":  lambda x: x,
    "log":    _log,
    "log1p":  lambda x: np.log1p(np.clip(x, -0.999999, None)),
    "asinh":  np.arcsinh,
    "sqrt":   lambda x: np.sqrt(np.clip(x - np.nanmin(x), 0, None)),
    "std":    lambda x: (x - np.nanmean(x)) / (np.nanstd(x, ddof=1) or 1.0),
    "rank":   lambda x: stats.rankdata(x, nan_policy="omit") / np.sum(np.isfinite(x)),
    "inv":    lambda x: 1.0 / np.where(np.abs(x) < 1e-9, np.nan, x),
    "square": lambda x: x ** 2,
    "winsor1": lambda x: np.clip(x, np.nanpercentile(x, 1), np.nanpercentile(x, 99)),
    "winsor5": lambda x: np.clip(x, np.nanpercentile(x, 5), np.nanpercentile(x, 95)),
    # discretisations (strategy 8): each cutoff is a fresh test
    "median_split":     _median_split,
    "above_mean":       lambda x: (x > np.nanmean(x)).astype(float),
    "tercile_extremes": _tercile_extremes,
    "quartile_top":     _quartile_top,
}

DISCRETIZERS = ("median_split", "above_mean", "tercile_extremes", "quartile_top")


def apply_transform(x: pd.Series, name: str) -> pd.Series:
    if name not in TRANSFORMS:
        raise KeyError(f"unknown transform {name!r}; known: {sorted(TRANSFORMS)}")
    return pd.Series(TRANSFORMS[name](x.to_numpy(dtype=float)), index=x.index)


# --------------------------------------------------------------------------
# Outlier rules (researcher degree of freedom: "outlier exclusion")
# --------------------------------------------------------------------------

def _sd(x, k):
    m, s = np.nanmean(x), np.nanstd(x, ddof=1)
    return np.abs(x - m) > k * s


def _iqr(x, k):
    q1, q3 = np.nanpercentile(x, 25), np.nanpercentile(x, 75)
    iqr = q3 - q1
    return (x < q1 - k * iqr) | (x > q3 + k * iqr)


def _mad(x, k):
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med)) * 1.4826
    return np.abs(x - med) > k * (mad or 1.0)


OUTLIER_RULES = {
    "none":  lambda x: np.zeros(len(x), dtype=bool),
    "sd2":   lambda x: _sd(x, 2.0),
    "sd2.5": lambda x: _sd(x, 2.5),
    "sd3":   lambda x: _sd(x, 3.0),
    "iqr1.5": lambda x: _iqr(x, 1.5),
    "iqr3":  lambda x: _iqr(x, 3.0),
    "mad3":  lambda x: _mad(x, 3.0),
    "pct1":  lambda x: (x < np.nanpercentile(x, 1)) | (x > np.nanpercentile(x, 99)),
    "pct5":  lambda x: (x < np.nanpercentile(x, 5)) | (x > np.nanpercentile(x, 95)),
}


def flag_outliers(x, rule: str) -> np.ndarray:
    if rule not in OUTLIER_RULES:
        raise KeyError(f"unknown outlier rule {rule!r}; known: {sorted(OUTLIER_RULES)}")
    x = x.to_numpy(dtype=float) if hasattr(x, "to_numpy") else np.asarray(x, float)
    return OUTLIER_RULES[rule](x)


def studentized_residuals(y, X, weights=None):
    """Internally studentised residuals of an OLS fit; the basis for
    residual-based outlier rules (Cook / studentised-residual trimming)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    if weights is not None:
        sw = np.sqrt(np.asarray(weights, float)); y = y * sw; X = X * sw[:, None]
    XtXi = np.linalg.pinv(X.T @ X)
    beta = XtXi @ (X.T @ y)
    u = y - X @ beta
    h = np.einsum("ij,jk,ik->i", X, XtXi, X)
    dof = max(y.size - X.shape[1], 1)
    s = np.sqrt((u @ u) / dof)
    return u / (s * np.sqrt(np.clip(1 - h, 1e-10, None)))


# --------------------------------------------------------------------------
# Missing-data handling (researcher degree of freedom: "favourable imputation")
# --------------------------------------------------------------------------

def impute(df: pd.DataFrame, cols, method: str) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c not in out or not out[c].isna().any():
            continue
        s = out[c]
        if method == "listwise":
            continue
        elif method == "mean":
            out[c] = s.fillna(s.mean())
        elif method == "median":
            out[c] = s.fillna(s.median())
        elif method == "zero":
            out[c] = s.fillna(0.0)
        elif method == "ffill":
            out[c] = s.ffill().bfill()
        elif method == "interp":
            out[c] = s.interpolate(limit_direction="both")
        else:
            raise KeyError(f"unknown imputation {method!r}")
    return out


# --------------------------------------------------------------------------
# Multi-way fixed-effect absorption by alternating projections
# --------------------------------------------------------------------------

def absorb(M: np.ndarray, groups: list[np.ndarray], tol=1e-9, maxiter=200,
           weights=None):
    """Within-transform M on one or more grouping vectors.

    Returns (residualised M, number of absorbed parameters). One-way is exact
    in a single pass; multi-way iterates (Guimaraes-Portugal / Correia). With
    `weights`, group means are weighted means, which is what WLS with dummies
    would do.
    """
    if not groups:
        return M, 0
    M = np.asarray(M, dtype=float).copy()
    w = None if weights is None else np.asarray(weights, float)
    codes = [pd.factorize(g)[0] for g in groups]
    ncat = [int(c.max()) + 1 for c in codes]
    for _ in range(maxiter):
        prev = M.copy()
        for c, k in zip(codes, ncat):
            sums = np.zeros((k, M.shape[1]))
            if w is None:
                np.add.at(sums, c, M)
                counts = np.bincount(c, minlength=k).astype(float)[:, None]
            else:
                np.add.at(sums, c, M * w[:, None])
                counts = np.bincount(c, weights=w, minlength=k)[:, None]
            M -= sums[c] / np.clip(counts[c], 1e-12, None)
        if len(codes) == 1 or np.max(np.abs(M - prev)) < tol:
            break
    k_absorbed = ncat[0] + sum(n - 1 for n in ncat[1:])
    return M, k_absorbed


# --------------------------------------------------------------------------
# OLS / WLS with robust / clustered variance
# --------------------------------------------------------------------------

def _meat_cluster(X: np.ndarray, u: np.ndarray, g: np.ndarray):
    codes, uniq = pd.factorize(g)
    G = len(uniq)
    k = X.shape[1]
    Xu = X * u[:, None]
    sums = np.zeros((G, k))
    np.add.at(sums, codes, Xu)
    return sums.T @ sums, G


def _vcov(X, u, vcov, cluster, dof):
    """Sandwich for a (possibly sqrt-weight-scaled) design. Returns (V, dfree, g_eff)."""
    n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    if vcov in ("cluster", "twoway"):
        if cluster is None:
            raise ValueError("cluster vcov requested without cluster variable")
        if vcov == "cluster":
            meat, G = _meat_cluster(X, u, np.asarray(cluster))
            adj = (G / max(G - 1, 1)) * ((n - 1) / dof)
            V = adj * (XtXi @ meat @ XtXi)
            g_eff = G
        else:
            g1, g2 = cluster
            g1, g2 = np.asarray(g1), np.asarray(g2)
            m1, G1 = _meat_cluster(X, u, g1)
            m2, G2 = _meat_cluster(X, u, g2)
            inter = pd.factorize(pd.Series(list(zip(g1, g2))))[0]
            m12, _ = _meat_cluster(X, u, inter)
            Gm = min(G1, G2)
            adj = (Gm / max(Gm - 1, 1)) * ((n - 1) / dof)
            V = adj * (XtXi @ (m1 + m2 - m12) @ XtXi)
            g_eff = Gm
        return V, max(g_eff - 1, 1), g_eff
    if vcov == "iid":
        return ((u @ u) / dof) * XtXi, dof, None
    h = np.einsum("ij,jk,ik->i", X, XtXi, X)
    if vcov == "hc0":
        w = u ** 2
    elif vcov == "hc1":
        w = u ** 2 * (n / dof)
    elif vcov == "hc2":
        w = u ** 2 / np.clip(1 - h, 1e-10, None)
    elif vcov == "hc3":
        w = u ** 2 / np.clip(1 - h, 1e-10, None) ** 2
    else:
        raise KeyError(f"unknown vcov {vcov!r}")
    return XtXi @ (X.T * w) @ X @ XtXi, dof, None


def fit_ols(y: np.ndarray, X: np.ndarray, *, vcov="hc1", cluster=None,
            k_absorbed=0, target=0, weights=None, full=False):
    """OLS (or WLS with `weights`) of y on X. X must already include a constant
    unless fixed effects were absorbed.

    vcov: 'iid' | 'hc0' | 'hc1' | 'hc2' | 'hc3' | 'cluster' | 'twoway'
    cluster: array, or (array, array) for two-way.
    target: column index of X whose coefficient is the estimand.
    full: also return the whole coefficient vector and covariance matrix.
    """
    y = np.asarray(y, dtype=float).ravel()
    X = np.asarray(X, dtype=float)
    if weights is not None:
        sw = np.sqrt(np.clip(np.asarray(weights, float), 0, None))
        y = y * sw; X = X * sw[:, None]
    n, k = X.shape
    XtXi = np.linalg.pinv(X.T @ X)
    beta = XtXi @ (X.T @ y)
    u = y - X @ beta
    dof = max(n - k - k_absorbed, 1)
    V, dfree, g_eff = _vcov(X, u, vcov, cluster, dof)
    diag = np.diag(V)
    psd_ok = bool(np.all(diag > 0) and np.all(np.linalg.eigvalsh((V + V.T) / 2) > -1e-10))
    se = np.sqrt(np.clip(diag, 0, None))
    b = float(beta[target])
    s = float(se[target]) if se[target] > 0 else float("nan")
    t = b / s if s and np.isfinite(s) else float("nan")
    p = float(2 * stats.t.sf(abs(t), dfree)) if np.isfinite(t) else float("nan")
    crit = stats.t.ppf(0.975, dfree)
    out = {
        "coef": b, "se": s, "t": t, "p": p,
        "ci_low": b - crit * s, "ci_high": b + crit * s,
        "n": int(n), "df": int(dfree), "k": int(k + k_absorbed),
        "resid_var": float((u @ u) / dof),
        "psd_ok": psd_ok,
    }
    if g_eff is not None:
        out["n_clusters"] = int(g_eff)
    if full:
        out["beta_all"] = beta; out["vcov_all"] = V; out["resid"] = u
    return out


def fit_lincom(y, X, a, *, vcov="hc1", cluster=None, k_absorbed=0, weights=None):
    """OLS, then the estimand a'beta with variance a'Va. Used for event-study
    aggregates (average post-period effect, a single lag, the pre-trend)."""
    r = fit_ols(y, X, vcov=vcov, cluster=cluster, k_absorbed=k_absorbed, weights=weights, full=True)
    a = np.asarray(a, float)
    b = float(a @ r["beta_all"]); v = float(a @ r["vcov_all"] @ a)
    s = float(np.sqrt(v)) if v > 0 else float("nan")
    t = b / s if s and np.isfinite(s) else float("nan")
    crit = stats.t.ppf(0.975, r["df"])
    out = {k: r[k] for k in ("n", "df", "k", "resid_var", "psd_ok")}
    if "n_clusters" in r:
        out["n_clusters"] = r["n_clusters"]
    out.update(coef=b, se=s, t=t, p=float(2 * stats.t.sf(abs(t), r["df"])) if np.isfinite(t) else float("nan"),
               ci_low=b - crit * s, ci_high=b + crit * s)
    return out


# --------------------------------------------------------------------------
# Regression discontinuity: local polynomial with kernel weights
# --------------------------------------------------------------------------

KERNELS = {
    "triangular":   lambda u: np.clip(1 - np.abs(u), 0, None),
    "uniform":      lambda u: (np.abs(u) <= 1).astype(float),
    "epanechnikov": lambda u: np.clip(0.75 * (1 - u ** 2), 0, None),
}


def rot_bandwidth(x: np.ndarray) -> float:
    """Silverman rule-of-thumb pilot bandwidth. Deliberately *not* rdrobust's
    MSE-optimal choice: the point of the grid is to walk multiples of a
    defensible pilot, and every multiple in [0.5, 2] is citable somewhere."""
    x = x[np.isfinite(x)]
    iqr = np.subtract(*np.percentile(x, [75, 25]))
    s = min(np.std(x, ddof=1), iqr / 1.349) if iqr > 0 else np.std(x, ddof=1)
    return float(1.84 * s * x.size ** (-0.2))


def ik_bandwidth(y, x, cutoff=0.0) -> float:
    """Imbens & Kalyanaraman (2012) MSE-optimal bandwidth for the sharp RD
    local-linear estimator with the edge (triangular) kernel.

    Follows their section 4.2 step by step. This is the single most-cited
    "optimal" bandwidth, and in a search it is one *option* next to CCT and
    multiples of either -- which is exactly how it gets used in practice.
    """
    y = np.asarray(y, float); x = np.asarray(x, float) - cutoff
    ok = np.isfinite(y) & np.isfinite(x)
    y, x = y[ok], x[ok]
    N = x.size
    # step 1: pilot density and conditional variances at the cutoff
    h1 = rot_bandwidth(x)
    in1 = np.abs(x) <= h1
    left1, right1 = in1 & (x < 0), in1 & (x >= 0)
    n1l, n1r = left1.sum(), right1.sum()
    if n1l < 3 or n1r < 3:
        return float(h1)
    f_c = (n1l + n1r) / (2.0 * N * h1)
    s2l = np.var(y[left1], ddof=1); s2r = np.var(y[right1], ddof=1)
    # step 2: global cubic for the third derivative, then pilot bandwidths
    D = (x >= 0).astype(float)
    Z = np.column_stack([np.ones(N), D, x, x ** 2, x ** 3])
    b3 = np.linalg.lstsq(Z, y, rcond=None)[0][4]
    m3 = 6.0 * b3
    Nl, Nr = int((x < 0).sum()), int((x >= 0).sum())
    denom = max(f_c * m3 ** 2, 1e-12)
    h2l = 3.56 * (s2l / denom) ** (1 / 7) * Nl ** (-1 / 7)
    h2r = 3.56 * (s2r / denom) ** (1 / 7) * Nr ** (-1 / 7)

    def second_deriv(side_mask, h2):
        sel = side_mask & (np.abs(x) <= h2)
        if sel.sum() < 4:
            return 0.0, int(sel.sum())
        Zq = np.column_stack([np.ones(sel.sum()), x[sel], x[sel] ** 2])
        b = np.linalg.lstsq(Zq, y[sel], rcond=None)[0]
        return 2.0 * b[2], int(sel.sum())
    m2l, n2l = second_deriv(x < 0, h2l)
    m2r, n2r = second_deriv(x >= 0, h2r)
    # step 3: regularisation terms
    rl = 2160.0 * s2l / max(n2l * h2l ** 4, 1e-12)
    rr = 2160.0 * s2r / max(n2r * h2r ** 4, 1e-12)
    # step 4: the optimal bandwidth (C_K = 3.4375 for the edge kernel)
    h = 3.4375 * ((s2l + s2r) / (f_c * ((m2r - m2l) ** 2 + rl + rr))) ** 0.2 * N ** (-0.2)
    if not np.isfinite(h) or h <= 0:
        return float(h1)
    return float(h)


def _rdd_fit(y, x, h, kernel, poly, controls, vcov, cluster, weights=None):
    D = (x >= 0).astype(float)
    cols = [np.ones(x.size), D]
    for k in range(1, poly + 1):
        cols += [x ** k, D * x ** k]
    if controls is not None and np.size(controls):
        cols += list(np.atleast_2d(np.asarray(controls, float)).T
                     if np.asarray(controls).shape[0] != x.size else np.asarray(controls, float).T)
    X = np.column_stack(cols)
    w = KERNELS[kernel](x / h)
    if weights is not None:
        w = w * np.asarray(weights, float)
    return fit_ols(y, X, vcov=vcov, cluster=cluster, target=1, weights=w)


def fit_rdd(y, x, *, h, kernel="triangular", poly=1, donut=0.0, cutoff=0.0,
            controls=None, vcov="hc1", cluster=None, inference="conventional",
            weights=None):
    """Sharp RDD by weighted local polynomial. Estimand: jump at the cutoff.

    inference:
      'conventional'   local polynomial of order `poly`, its own SE
      'bias_corrected' point estimate bias-corrected with a (poly+1) fit on the
                       same bandwidth, but the *conventional* SE -- the
                       under-covering combination CCT (2014) warn against, and
                       therefore a lever a search will find
      'robust'         Calonico-Cattaneo-Titiunik robust bias-corrected
                       inference with b = h, which is numerically the (poly+1)
                       estimate with its own SE
    """
    y = np.asarray(y, float); x = np.asarray(x, float) - cutoff
    keep = (np.abs(x) <= h) & (np.abs(x) > donut) & np.isfinite(y) & np.isfinite(x)
    if keep.sum() < 4 * (poly + 2) + 2:
        raise ValueError(f"only {int(keep.sum())} observations inside bandwidth {h:.3g}")
    y, x = y[keep], x[keep]
    ctl = None
    if controls is not None and np.size(controls):
        C = np.atleast_2d(np.asarray(controls, float))
        C = C.T if C.shape[0] != keep.size else C
        ctl = C[keep]
    cl = None if cluster is None else np.asarray(cluster)[keep]
    wt = None if weights is None else np.asarray(weights, float)[keep]
    r = _rdd_fit(y, x, h, kernel, poly, ctl, vcov, cl, wt)
    if inference != "conventional":
        r_hi = _rdd_fit(y, x, h, kernel, poly + 1, ctl, vcov, cl, wt)
        if inference == "robust":
            r = r_hi
        elif inference == "bias_corrected":
            b, s, df = r_hi["coef"], r["se"], r["df"]
            t = b / s if s > 0 else float("nan")
            crit = stats.t.ppf(0.975, df)
            r.update(coef=b, t=t,
                     p=float(2 * stats.t.sf(abs(t), df)) if np.isfinite(t) else float("nan"),
                     ci_low=b - crit * s, ci_high=b + crit * s)
        else:
            raise KeyError(f"unknown rdd inference {inference!r}")
    D = x >= 0
    r.update(n_left=int((~D).sum()), n_right=int(D.sum()), bandwidth=float(h),
             rdd_inference=inference)
    return r


# --------------------------------------------------------------------------
# Two-stage least squares / LIML with Anderson-Rubin
# --------------------------------------------------------------------------

def fit_2sls(y, d, Z, *, controls=None, vcov="hc1", cluster=None, estimator="2sls",
             weights=None, beta0=0.0):
    """IV for a single endogenous regressor d, instruments Z, exogenous controls.

    Returns the structural coefficient on d, the first-stage F on the excluded
    instruments (itself a searchable object), and the Anderson-Rubin p-value
    for H0: beta = beta0, which is the weak-instrument-robust statement a
    search cannot inflate by conditioning on the first stage.
    """
    y = np.asarray(y, float); d = np.asarray(d, float)
    Z = np.atleast_2d(np.asarray(Z, float)); Z = Z.T if Z.shape[0] != y.size else Z
    n = y.size
    W = np.ones((n, 1))
    if controls is not None and np.size(controls):
        C = np.atleast_2d(np.asarray(controls, float)); C = C.T if C.shape[0] != n else C
        W = np.column_stack([W, C])
    if weights is not None:
        sw = np.sqrt(np.clip(np.asarray(weights, float), 0, None))
        y, d, Z, W = y * sw, d * sw, Z * sw[:, None], W * sw[:, None]
    X = np.column_stack([W, d])                 # structural regressors, d last
    Zf = np.column_stack([W, Z])                # full instrument matrix
    g, *_ = np.linalg.lstsq(Zf, d, rcond=None)
    dhat = Zf @ g
    u1 = d - dhat
    g0, *_ = np.linalg.lstsq(W, d, rcond=None)
    u0 = d - W @ g0
    q = Z.shape[1]; df2 = n - Zf.shape[1]
    F = float(((u0 @ u0 - u1 @ u1) / q) / ((u1 @ u1) / max(df2, 1)))
    if estimator == "liml":
        Y = np.column_stack([y, d])
        MW = Y - W @ np.linalg.lstsq(W, Y, rcond=None)[0]
        MZ = Y - Zf @ np.linalg.lstsq(Zf, Y, rcond=None)[0]
        from scipy import linalg as _sl
        ev = _sl.eigvals(MW.T @ MW, MZ.T @ MZ)
        ev = ev[np.isfinite(ev)].real
        kappa = float(ev.min()) if ev.size else 1.0
        kappa = max(kappa, 1.0)
    else:
        kappa = 1.0
    Xhat = np.column_stack([W, kappa * dhat + (1 - kappa) * d])
    XhX = Xhat.T @ X
    beta = np.linalg.solve(XhX, Xhat.T @ y)
    u = y - X @ beta
    k = X.shape[1]; dof = max(n - k, 1)
    A = np.linalg.inv(XhX)
    if vcov == "iid":
        V = (u @ u) / dof * A @ (Xhat.T @ Xhat) @ A.T
        dfree = dof
    elif vcov in ("hc0", "hc1"):
        scale = n / dof if vcov == "hc1" else 1.0
        V = scale * A @ (Xhat.T * (u ** 2)) @ Xhat @ A.T
        dfree = dof
    elif vcov == "cluster":
        meat, G = _meat_cluster(Xhat, u, np.asarray(cluster))
        V = (G / max(G - 1, 1)) * ((n - 1) / dof) * A @ meat @ A.T
        dfree = max(G - 1, 1)
    else:
        raise KeyError(f"2SLS supports iid/hc0/hc1/cluster, not {vcov!r}")
    j = k - 1
    b = float(beta[j]); s = float(np.sqrt(max(V[j, j], 0)))
    t = b / s if s > 0 else float("nan")
    crit = stats.t.ppf(0.975, dfree)
    # Anderson-Rubin: regress y - beta0*d on [W, Z]; joint test on Z with the same vcov
    ar = fit_ols(y - beta0 * d, Zf, vcov=vcov, cluster=cluster, target=W.shape[1], full=True)
    bz = ar["beta_all"][W.shape[1]:]; Vz = ar["vcov_all"][W.shape[1]:, W.shape[1]:]
    try:
        wald = float(bz @ np.linalg.solve(Vz, bz))
        ar_p = float(stats.f.sf(wald / q, q, ar["df"]))
    except np.linalg.LinAlgError:
        ar_p = float("nan")
    return {"coef": b, "se": s, "t": t,
            "p": float(2 * stats.t.sf(abs(t), dfree)) if np.isfinite(t) else float("nan"),
            "ci_low": b - crit * s, "ci_high": b + crit * s, "n": int(n),
            "df": int(dfree), "k": int(k), "resid_var": float((u @ u) / dof),
            "psd_ok": bool(V[j, j] > 0), "first_stage_F": F, "n_instruments": int(q),
            "kappa": kappa, "ar_p": ar_p}
