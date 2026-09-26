"""Estimation core: transforms, outliers, FE absorption, OLS variance."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import core


def _panel(seed=0, n_unit=40, n_t=10):
    rng = np.random.default_rng(seed)
    g = np.repeat(np.arange(n_unit), n_t); t = np.tile(np.arange(n_t), n_unit)
    x = rng.normal(size=g.size)
    y = 0.5 * x + 0.3 * g + 0.1 * t + rng.normal(size=g.size)
    return y, x, g, t


def test_absorb_oneway_matches_dummies():
    y, x, g, t = _panel()
    M, ka = core.absorb(np.column_stack([y, x]), [g])
    r = core.fit_ols(M[:, 0], M[:, 1:], vcov="iid", k_absorbed=ka)
    D = pd.get_dummies(g).to_numpy(float)
    X = np.column_stack([x, D])
    r2 = core.fit_ols(y, X, vcov="iid", target=0)
    assert abs(r["coef"] - r2["coef"]) < 1e-9
    assert abs(r["se"] - r2["se"]) < 1e-9          # dof accounting is right


def test_absorb_twoway_matches_dummies():
    y, x, g, t = _panel()
    M, ka = core.absorb(np.column_stack([y, x]), [g, t])
    r = core.fit_ols(M[:, 0], M[:, 1:], vcov="iid", k_absorbed=ka)
    X = np.column_stack([x, pd.get_dummies(g).to_numpy(float),
                         pd.get_dummies(t).to_numpy(float)[:, 1:]])
    r2 = core.fit_ols(y, X, vcov="iid", target=0)
    assert abs(r["coef"] - r2["coef"]) < 1e-8
    assert abs(r["se"] - r2["se"]) < 1e-8


def test_hc1_matches_statsmodels():
    sm = pytest.importorskip("statsmodels.api")
    y, x, g, t = _panel()
    X = np.column_stack([np.ones(y.size), x])
    r = core.fit_ols(y, X, vcov="hc1", target=1)
    m = sm.OLS(y, X).fit(cov_type="HC1")
    assert abs(r["se"] - m.bse[1]) < 1e-9


def test_cluster_matches_statsmodels():
    sm = pytest.importorskip("statsmodels.api")
    y, x, g, t = _panel()
    X = np.column_stack([np.ones(y.size), x])
    r = core.fit_ols(y, X, vcov="cluster", cluster=g, target=1)
    m = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": g})
    assert abs(r["se"] - m.bse[1]) / m.bse[1] < 1e-6


def test_twoway_psd_flag_exists():
    y, x, g, t = _panel()
    X = np.column_stack([np.ones(y.size), x])
    r = core.fit_ols(y, X, vcov="twoway", cluster=(g, t), target=1)
    assert "psd_ok" in r and isinstance(r["psd_ok"], bool)


def test_transforms_and_outliers_registered():
    s = pd.Series(np.random.default_rng(1).lognormal(size=200))
    for name in core.TRANSFORMS:
        out = core.apply_transform(s, name)
        assert len(out) == 200
    for rule in core.OUTLIER_RULES:
        f = core.flag_outliers(s, rule)
        assert f.dtype == bool and f.shape == (200,)
    assert not core.flag_outliers(s, "none").any()
