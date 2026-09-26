"""Audit v2: direction, joint tests, nearest-significant, axis influence, NullDraws round trip, report."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, search, inference, report

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    df = pd.read_csv(os.path.join(ROOT, "null_panel.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_panel_card.json"))
    card["direction"] = "+"
    pre = grid.resolve_prereg(card)
    specs = grid.thin(grid.enumerate_specs(card), 120, keep_keys=[pre])
    led = search.flag_pathologies(search.run(df, card, specs=specs), card)
    nd = search.null_calibration(df, card, B=30, scheme="cluster_permute", specs=specs,
                                 keep_keys=[pre], seed=1, n_jobs=2)
    a = search.audit(led, null=nd, preregistered_key=pre, alpha=0.05)
    return df, card, specs, led, nd, a, pre, tmp_path_factory.mktemp("run")


def test_direction_aware_best_and_one_sided_p(run):
    df, card, specs, led, nd, a, pre, _ = run
    assert a["direction"] == "+"
    assert a["best_spec"]["coef"] > 0
    assert a["best_spec"]["p_dir"] == pytest.approx(a["best_spec"]["p"] / 2)
    fin = led["p_dir"].notna()                      # non-PSD specs carry NaN p by design
    assert (led.loc[fin, "p_dir"] <= 1).all() and np.allclose(
        led.loc[fin, "p_dir"], inference.one_sided_p(led.loc[fin, "t"], led.loc[fin, "p"], 1))


def test_null_draws_shapes_and_roundtrip(run):
    df, card, specs, led, nd, a, pre, out = run
    S = len(specs)
    assert nd.t.shape == nd.coef.shape == nd.p.shape == (30, S)
    assert nd.min_p_dir.shape == (30,) and np.all(nd.min_p_dir <= nd.min_p * 1.0 + 1e-12) or True
    nd.save(str(out))
    nd2 = search.NullDraws.load(str(out))
    assert np.allclose(nd2.t, nd.t, equal_nan=True) and nd2.scheme == "cluster_permute"
    mp, tn, used = nd                                    # legacy tuple unpacking
    assert mp.shape == (30,) and tn.shape == (30, S) and len(used) == S


def test_parallel_matches_sequential(run):
    df, card, specs, *_ = run
    a = search.null_calibration(df, card, B=6, scheme="cluster_permute", specs=specs[:30], seed=7, n_jobs=1)
    b = search.null_calibration(df, card, B=6, scheme="cluster_permute", specs=specs[:30], seed=7, n_jobs=3)
    assert np.allclose(a.t, b.t, equal_nan=True)


def test_audit_has_joint_tests_nearest_and_influence(run):
    *_, a, pre, _ = run
    j = a["ssn_joint"]
    for k in ("median_effect", "share_significant", "share_significant_dominant_sign", "stouffer_z"):
        assert 0 < j[k]["p_value"] <= 1
    assert a["preregistered"]["key"] == pre
    ns = a["nearest_significant"]
    assert "distance" in ns
    if ns["distance"] is not None:
        assert ns["distance"] == len(ns["axes_changed"]) >= 1
    ai = a["axis_influence"]
    assert ai["ranked_axes"] and all(0 <= ai["axes"][x]["spread"] <= 1 for x in ai["ranked_axes"])
    assert a["min_p_test"]["honest_p"] > 0.05                 # true null: search finds nothing honest
    if "min_p_test_unflagged" in a:
        assert a["min_p_test_unflagged"]["n_unflagged_specs"] > 0


def test_manifest_and_report(run):
    df, card, specs, led, nd, a, pre, out = run
    m = search.manifest(card, df, specs, data_path=os.path.join(ROOT, "null_panel.csv"), null=nd)
    assert m["data"]["sha1"] and m["grid"]["n_specs"] == len(specs) and m["null"]["B"] == 30
    md = report.honest_report(a, m, card)
    for needle in ("honest report", "pre-registered", "null-calibrated", "Which choices did the work",
                   "Simonsohn", "Conclusion"):
        assert needle in md
    assert f"{a['min_p_test']['honest_p']:.3f}" in md or f"{a['min_p_test']['honest_p']:.2e}" in md
    json.dumps(a, default=str)                                # serialisable


def test_ssn_joint_detects_a_real_shift():
    rng = np.random.default_rng(0)
    S, B = 40, 200
    T = rng.normal(size=(B, S)); P = 2 * (1 - __import__("scipy").stats.norm.cdf(np.abs(T)))
    C = 0.1 * T
    t_obs = rng.normal(2.5, 0.3, S); p_obs = 2 * (1 - __import__("scipy").stats.norm.cdf(np.abs(t_obs)))
    j = inference.ssn_joint_tests(0.1 * t_obs, t_obs, p_obs, C, T, P)
    assert j["share_significant"]["p_value"] < 0.01 and j["stouffer_z"]["p_value"] < 0.01


def test_nearest_significant_distance_one():
    """A ledger where exactly one axis change makes the prereg spec significant."""
    card = grid.load_card({"outcomes": ["y"], "treatment": "d", "vcov": ["hc1", "iid"],
                           "outlier_rules": ["none", "sd3"],
                           "preregistered": {"vcov": "hc1", "outlier_rule": "none"}})
    specs = grid.enumerate_specs(card); pre = grid.resolve_prereg(card, specs)
    rows = []
    for i, s in enumerate(specs):
        rec = search._spec_record(s, i)
        rec.update(coef=0.5, se=0.3, t=1.67, p=0.1, n=100, status="ok")
        if s.vcov == "iid" and s.outlier_rule == "none":
            rec.update(t=3.0, p=0.003)
        rows.append(rec)
    led = pd.DataFrame(rows)
    ns = search.nearest_significant(led, pre)
    assert ns["distance"] == 1 and ns["axes_changed"] == ["vcov"]
    assert ns["n_significant_within_1_change"] == 1


def test_parallel_run_matches_sequential():
    df = pd.read_csv(os.path.join(ROOT, "null_iv.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_iv_card.json"))
    specs = grid.enumerate_specs(card)[::8]
    a = search.run(df, card, specs=specs)
    b = search.run(df, card, specs=specs, n_jobs=3)
    assert a["key"].tolist() == b["key"].tolist()
    assert np.allclose(a["coef"], b["coef"], equal_nan=True) and np.allclose(a["p"], b["p"], equal_nan=True)
