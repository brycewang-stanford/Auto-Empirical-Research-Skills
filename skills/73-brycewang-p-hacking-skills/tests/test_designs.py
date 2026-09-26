"""RDD and IV: estimators recover truth, grids enumerate, nulls calibrate."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import core, grid, search

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")


def test_rdd_recovers_jump():
    rng = np.random.default_rng(0); n = 4000
    x = rng.uniform(-1, 1, n); y = 0.5 * (x >= 0) + 0.8 * x + rng.normal(0, .5, n)
    h = core.rot_bandwidth(x)
    for k in core.KERNELS:
        r = core.fit_rdd(y, x, h=h, kernel=k, poly=1)
        assert abs(r["coef"] - 0.5) < 3 * r["se"]
    assert core.fit_rdd(y, x, h=h, donut=0.05)["n"] < core.fit_rdd(y, x, h=h)["n"]


def test_2sls_matches_linearmodels_and_beats_ols():
    rng = np.random.default_rng(1); n = 3000
    z = rng.normal(size=(n, 2)); e = rng.normal(size=n)
    d = z @ [1, .5] + e + rng.normal(size=n); y = 1.0 * d + 2 * e + rng.normal(size=n)
    r = core.fit_2sls(y, d, z, vcov="hc1")
    assert abs(r["coef"] - 1.0) < 3 * r["se"] and r["first_stage_F"] > 100
    ols = core.fit_ols(y, np.column_stack([np.ones(n), d]), target=1)
    assert abs(ols["coef"] - 1.0) > 0.3
    lm = pytest.importorskip("linearmodels.iv")
    m = lm.IV2SLS(y, np.ones((n, 1)), d, z).fit(cov_type="robust")
    assert abs(r["coef"] - float(m.params.iloc[-1])) < 1e-8
    assert abs(r["se"] - float(m.std_errors.iloc[-1])) / r["se"] < 1e-3


def test_liml_kappa_near_one_when_strong():
    rng = np.random.default_rng(2); n = 2000
    z = rng.normal(size=(n, 3)); e = rng.normal(size=n); v = rng.normal(size=n)
    d = z @ [1, 1, 1] + e + v; y = d + e + rng.normal(size=n)
    r = core.fit_2sls(y, d, z, estimator="liml")
    assert 1.0 <= r["kappa"] < 1.01                  # k-class kappa -> 1 as F -> inf
    assert abs(r["coef"] - 1.0) < 3 * r["se"]
    # kappa - 1 is an overidentification statistic, not a strength measure, so no
    # ordering against a weak-instrument case is asserted here; the weak case is
    # covered by flag_weak_instruments in test_iv_grid_and_weak_flag.


def test_rdd_grid_and_null():
    df = pd.read_csv(os.path.join(ROOT, "null_rdd.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_rdd_card.json"))
    assert grid.universe_size(card)["n_specs"] == 20736
    specs = grid.enumerate_specs(card)[::60]
    assert all(s.fe == () and s.vcov != "twoway" for s in specs)
    led = search.flag_pathologies(search.run(df, card, specs=specs), card)
    assert (led["status"] == "ok").all() and "flag_thin_rdd_side" in led
    mp, tn, _ = search.null_calibration(df, card, B=15, specs=specs, seed=0)
    a = search.audit(led, min_p_null=mp, t_null=tn)
    assert a["min_p_test"]["honest_p"] > 0.05


def test_iv_grid_and_weak_flag():
    df = pd.read_csv(os.path.join(ROOT, "null_iv.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_iv_card.json"))
    assert grid.universe_size(card)["n_specs"] == 672
    specs = grid.enumerate_specs(card)[::12]
    led = search.flag_pathologies(search.run(df, card, specs=specs), card)
    assert (led["status"] == "ok").all()
    assert led["flag_weak_instruments"].any()               # z3 alone is weak
    assert led.loc[led["instruments"] == "z3", "first_stage_F"].max() < 10
    assert led["iv_estimator"].isin(["2sls", "liml"]).all()


def test_card_validation_for_designs():
    with pytest.raises(ValueError):
        grid.load_card({"design": "rdd", "outcomes": ["y"]})
    with pytest.raises(ValueError):
        grid.load_card({"design": "iv", "outcomes": ["y"], "treatment": "d"})
