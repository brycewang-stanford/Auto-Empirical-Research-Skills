"""Grid enumeration, search ledger, pathology flags, honest inference."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, search, inference

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "eval", "data", "null_panel.csv")
CARD = os.path.join(ROOT, "eval", "data", "null_panel_card.json")


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA)


@pytest.fixture(scope="module")
def card():
    return grid.load_card(CARD)


def test_universe_size_is_documented_number(card):
    assert grid.universe_size(card)["n_specs"] == 25920


def test_card_rejects_unknown_keys():
    with pytest.raises(KeyError):
        grid.load_card({"outcomes": ["y"], "treatment": "d", "controlz": []})


def test_cluster_vcov_pairing_enforced(card):
    for s in grid.enumerate_specs(card):
        if s.vcov in ("cluster", "twoway"):
            assert s.cluster is not None
        else:
            assert s.cluster is None
        if s.vcov == "twoway":
            assert isinstance(s.cluster, tuple)


def test_ledger_is_complete_and_flagged(df, card):
    specs = grid.enumerate_specs(card)[::200]
    led = search.flag_pathologies(search.run(df, card, specs=specs), card)
    assert len(led) == len(specs)
    assert (led["status"] == "ok").all()
    assert {"flag_nonpsd_vcov", "flag_few_clusters", "n_flags"} <= set(led.columns)


def test_search_finds_significance_on_true_null(df, card):
    """The headline demonstration: a large grid on a zero effect yields p < .01."""
    specs = grid.enumerate_specs(card)[::40]
    led = search.run(df, card, specs=specs)
    assert led["p"].min() < 0.01


def test_min_p_test_recovers_null(df, card):
    """...and the null-calibrated p-value says so."""
    specs = grid.enumerate_specs(card)[::120]
    led = search.run(df, card, specs=specs)
    mp, tn, used = search.null_calibration(df, card, B=40, scheme="cluster_permute",
                                           specs=specs, seed=1)
    a = search.audit(led, min_p_null=mp, t_null=tn)
    # honest p is uniform on a true null, so no single dataset can be held to a
    # high threshold; the calibration property itself is tested by
    # scripts/calibrate_engine.py. Here: the search reported something far more
    # significant than the null-calibrated value, and Romano-Wolf does not reject.
    assert a["min_p_test"]["honest_p"] > 0.02
    assert a["min_p_test"]["inflation_factor"] > 5
    # with B = 40 the finest Romano-Wolf p is 1/41; it must stay well above the raw p
    assert a["romano_wolf_p_of_best"] > 0.02 and a["romano_wolf_p_of_best"] > 10 * a["best_spec"]["p"]
    assert 1 <= a["effective_tests"] <= len(used)


def test_romano_wolf_is_monotone_and_nan_robust():
    rng = np.random.default_rng(3)
    f = rng.normal(size=(2000, 1)); tn = 0.9 * f + 0.44 * rng.normal(size=(2000, 30))
    tobs = np.r_[4.5, rng.normal(size=29)]
    rw = inference.romano_wolf(tobs, tn)
    order = np.argsort(-np.abs(tobs))
    assert np.all(np.diff(rw[order]) >= -1e-12)
    assert np.nansum(rw < 0.05) <= 2
    tn2 = tn.copy(); tn2[:, 5] = np.nan; tobs2 = tobs.copy(); tobs2[7] = np.nan
    rw2 = inference.romano_wolf(tobs2, tn2)
    assert np.isnan(rw2[7]) and np.isfinite(rw2[0])
    assert rw2[0] < 0.05


def test_effective_tests_bounds():
    rng = np.random.default_rng(4)
    ind = rng.normal(size=(3000, 40))
    assert inference.effective_tests(ind) > 35
    f = rng.normal(size=(3000, 1)); dep = 0.95 * f + 0.31 * rng.normal(size=(3000, 40))
    assert inference.effective_tests(dep) < 15


def test_bh_fdr_monotone():
    p = np.array([0.001, 0.01, 0.02, 0.03, 0.5, 0.9])
    q = inference.bh_fdr(p)
    assert np.all(np.diff(q) >= 0) and q[0] <= 0.006 + 1e-12
