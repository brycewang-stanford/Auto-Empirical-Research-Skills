"""Grid v2: thinning keeps the anchor, prereg resolves, new axes materialise, DiD estimators work."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import core, grid, search

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")


def test_thin_keeps_prereg_and_is_even():
    card = grid.load_card(os.path.join(ROOT, "null_panel_card.json"))
    full = grid.enumerate_specs(card)
    pre = grid.resolve_prereg(card, full)
    th = grid.thin(full, 200, keep_keys=[pre])
    assert 200 <= len(th) <= 201 and any(s.key() == pre for s in th)
    assert grid.thin(full, None) is not full and len(grid.thin(full, None)) == len(full)


def test_prereg_resolution_from_block_and_key():
    card = grid.load_card(os.path.join(ROOT, "null_panel_card.json"))
    key = grid.resolve_prereg(card)
    assert isinstance(key, str) and len(key) == 12
    card2 = dict(card, preregistered=key)
    assert grid.resolve_prereg(card2) == key
    # a partial block resolves: unpinned axes default to the card's FIRST level
    key3 = grid.resolve_prereg(dict(card, preregistered={"outcome": "y_alt"}))
    s3 = [s for s in grid.enumerate_specs(card) if s.key() == key3][0]
    assert s3.outcome == "y_alt" and s3.vcov == card["vcov"][0] and s3.controls == ()
    with pytest.raises(ValueError):          # matches nothing in the grid
        grid.resolve_prereg(dict(card, preregistered={"controls": ["x9"]}))
    with pytest.raises(KeyError):
        grid.resolve_prereg(dict(card, preregistered={"bandwith": 1}))
    assert grid.resolve_prereg(dict(card, preregistered="free text note")) is None


def test_axis_distance_and_index_neighbours():
    card = grid.load_card(os.path.join(ROOT, "null_iv_card.json"))
    specs = grid.enumerate_specs(card)
    idx = grid.SpecIndex(specs)
    s = specs[0]
    for a in idx.varying:
        for nb in idx.neighbours(s, a):
            d, diff = grid.axis_distance(s, nb)
            assert d == 1 and diff == [a]


def test_weights_are_applied():
    rng = np.random.default_rng(0); n = 500
    df = pd.DataFrame({"y": rng.normal(size=n), "d": rng.normal(size=n),
                       "w": rng.uniform(0.1, 5, n)})
    card = grid.load_card({"outcomes": ["y"], "treatment": "d", "weights": [None, "w"]})
    led = search.run(df, card)
    w = led["weight"].tolist()
    assert pd.isna(w[0]) and w[1] == "w"          # None vs NaN differs across pandas versions
    assert abs(led.loc[0, "coef"] - led.loc[1, "coef"]) > 1e-6     # WLS differs from OLS


def test_residual_outlier_basis_and_discretisers():
    rng = np.random.default_rng(1); n = 400
    x = rng.normal(size=n); y = 0.5 * x + rng.normal(size=n); y[:5] += 15
    df = pd.DataFrame({"y": y, "x": x})
    card = grid.load_card({"outcomes": ["y"], "treatment": "x", "outlier_rules": ["none", "sd3"],
                           "outlier_basis": "residual",
                           "treatment_transforms": ["level", "median_split", "tercile_extremes"]})
    led = search.run(df, card)
    assert (led["status"] == "ok").all()
    trimmed = led[(led.outlier_rule == "sd3") & (led.d_transform == "level")].iloc[0]
    assert trimmed["n"] < n and trimmed["n"] >= n - 10
    ext = led[led.d_transform == "tercile_extremes"].iloc[0]
    assert ext["n"] < 0.75 * n                                    # middle tercile dropped


def _stag(seed=5, n_unit=90, n_t=14, effect=0.0):
    rng = np.random.default_rng(seed)
    coh = rng.choice([0, 4, 7, 10], size=n_unit)
    rows = []
    for i in range(n_unit):
        a = rng.normal()
        for t in range(n_t):
            tr = float(coh[i] > 0 and t >= coh[i])
            rows.append(dict(unit=i, year=t, treat=tr, x=rng.normal(),
                             y=a + 0.1 * t + effect * tr + rng.normal(0, .6)))
    return pd.DataFrame(rows)


def test_did_estimators_enumerate_and_agree_under_homogeneous_effect():
    df = _stag(effect=1.0)
    card = grid.load_card({"design": "did", "outcomes": ["y"], "treatment": "treat",
                           "fixed_effects": [["unit", "year"], ["year"]], "vcov": ["cluster"],
                           "cluster": ["unit"], "did_estimators": ["twfe", "did2s", "stacked"],
                           "comparison_groups": ["all", "drop_never_treated", "drop_always_treated"],
                           "stack_window": [3, 3], "panel_unit": "unit", "panel_time": "year"})
    specs = grid.enumerate_specs(card)
    # non-TWFE estimators collapse the FE axis: 2 FE x twfe + 1 x did2s + 1 x stacked, x 3 groups
    assert len(specs) == (2 + 1 + 1) * 3
    led = search.flag_pathologies(search.run(df, card), card)
    assert (led["status"] == "ok").all()
    ok = led[led.fe != "year"]
    assert np.all(np.abs(ok["coef"] - 1.0) < 4 * ok["se"])       # all recover the constant effect
    st = led[led.did_estimator == "stacked"].set_index("comparison_group")
    assert st.loc["all", "n_stacks"] >= 2
    # dropping never-treated units leaves the last cohorts without clean controls
    assert st.loc["drop_never_treated", "n_stacks"] == 1 and st.loc["drop_never_treated", "flag_single_stack"]


def test_did_estimators_diverge_under_heterogeneous_dynamics():
    rng = np.random.default_rng(3); n_unit, n_t = 120, 16
    coh = rng.choice([0, 5, 8, 11], size=n_unit); rows = []
    for i in range(n_unit):
        a = rng.normal()
        for t in range(n_t):
            tr = float(coh[i] > 0 and t >= coh[i])
            tau = (1 + 0.3 * (t - coh[i])) * (1.5 if coh[i] == 5 else 1) if tr else 0
            rows.append(dict(unit=i, year=t, treat=tr, y=a + 0.1 * t + tau + rng.normal(0, .5), tau=tau))
    df = pd.DataFrame(rows); truth = df.loc[df.treat == 1, "tau"].mean()
    card = grid.load_card({"design": "did", "outcomes": ["y"], "treatment": "treat",
                           "fixed_effects": [["unit", "year"]], "vcov": ["cluster"], "cluster": ["unit"],
                           "did_estimators": ["twfe", "did2s"], "panel_unit": "unit", "panel_time": "year"})
    led = search.run(df, card).set_index("did_estimator")
    assert abs(led.loc["did2s", "coef"] - truth) < 0.15
    assert led.loc["twfe", "coef"] < truth - 0.5                 # the textbook TWFE bias


def test_staggered_card_ships_and_resolves():
    card = grid.load_card(os.path.join(ROOT, "null_staggered_card.json"))
    assert grid.universe_size(card)["n_specs"] == 3456
    assert grid.resolve_prereg(card) is not None


def test_rdd_new_axes_enumerate_and_fit():
    df = pd.read_csv(os.path.join(ROOT, "null_rdd.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_rdd_card.json"))
    specs = [s for s in grid.enumerate_specs(card) if s.donut == 0.0 and s.poly == 1
             and s.bandwidth == 1.0 and s.outcome == "share_detained" and s.y_transform == "level"
             and s.outlier_rule == "none" and not s.controls and s.vcov == "hc1"]
    led = search.flag_pathologies(search.run(df, card, specs=specs), card)
    assert (led["status"] == "ok").all()
    assert set(led["bw_selector"]) == {"rot", "ik"} and set(led["rdd_inference"]) == {"conventional", "bias_corrected", "robust"}
    assert led.loc[led.bw_selector == "ik", "bandwidth"].iloc[0] != led.loc[led.bw_selector == "rot", "bandwidth"].iloc[0]
    assert led["flag_bc_without_robust_se"].sum() == (led.rdd_inference == "bias_corrected").sum()
    bc = led[(led.kernel == "triangular") & (led.bw_selector == "ik")].set_index("rdd_inference")
    assert bc.loc["bias_corrected", "coef"] == pytest.approx(bc.loc["robust", "coef"])
    assert bc.loc["bias_corrected", "se"] == pytest.approx(bc.loc["conventional", "se"])
    assert bc.loc["robust", "se"] > bc.loc["conventional", "se"]


def test_iv_ar_p_recorded_and_flag_exists():
    df = pd.read_csv(os.path.join(ROOT, "null_iv.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_iv_card.json"))
    led = search.flag_pathologies(search.run(df, card, specs=grid.enumerate_specs(card)[::20]), card)
    assert led["ar_p"].between(0, 1).all() and "flag_ar_disagrees" in led


def test_ik_bandwidth_is_finite_and_scales_with_n():
    rng = np.random.default_rng(0)
    x = rng.uniform(-1, 1, 3000); y = 0.5 * (x >= 0) + x + rng.normal(0, .5, 3000)
    h_big = core.ik_bandwidth(y, x); h_small = core.ik_bandwidth(y[:500], x[:500])
    assert 0 < h_big < 2 and h_small > h_big * 0.8
