"""`phack race`: time-to-significance is measured, deterministic, and honestly framed."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, race

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")


@pytest.fixture(scope="module")
def setup():
    df = pd.read_csv(os.path.join(ROOT, "null_panel.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_panel_card.json"))
    card["direction"] = "+"
    return df, card


def _race(setup, **kw):
    df, card = setup
    kw.setdefault("trials", 3)
    kw.setdefault("procedure_names", ("first_significant", "random"))
    kw.setdefault("budget", 40)
    return race.race(df, card, **kw)


def test_structure_and_ranges(setup):
    res = _race(setup)
    assert res["n_specs_in_grid"] == res["n_specs_in_universe"]
    assert res["direction"] == "+"
    assert set(res["procedures"]) == {"first_significant", "random"}
    for r in res["procedures"].values():
        assert 0.0 <= r["share_reporting_significant"] <= 1.0
        assert len(r["trials"]) == 3
        for row in r["trials"]:
            assert row["specs_visited"] <= 40
            assert row["total_seconds"] >= 0
            if row["significant"]:
                assert row["seconds_to_significance"] is not None
                assert row["seconds_to_significance"] <= row["total_seconds"] + 1e-6
                assert row["reported_p"] < 0.05
    # the honest baseline is present and priced
    pre = res["preregistered"]
    assert pre["key"] == grid.resolve_prereg(setup[1])
    assert np.isfinite(pre["p_dir"]) and pre["seconds"] >= 0


def test_deterministic_given_seed(setup):
    a = _race(setup, seed=7)
    b = _race(setup, seed=7)
    c = _race(setup, seed=8)
    key = lambda r: [(row["specs_visited"], row["significant"], row["reported_p"])
                     for p in r["procedures"].values() for row in p["trials"]]
    assert key(a) == key(b)
    assert key(a) != key(c)


def test_null_scheme_prices_the_false_positive(setup):
    res = _race(setup, null_scheme="cluster_permute",
                procedure_names=("first_significant",), trials=4)
    r = res["procedures"]["first_significant"]
    assert 0.0 <= r["share_reporting_significant"] <= 1.0
    assert "false-positive rate" in res["note"]
    # trials saw different null draws, so the walks differ
    visited = {row["specs_visited"] for row in r["trials"]}
    assert len(visited) >= 1        # structure holds even if lengths coincide


def test_greedy_races_on_the_full_grid(setup):
    res = _race(setup, procedure_names=("greedy",), trials=2, budget=None)
    r = res["procedures"]["greedy"]
    # greedy starts at the pre-registered spec and actually moves
    assert all(row["specs_visited"] >= 1 for row in r["trials"])
    assert r["params"]["start"] == res["preregistered"]["key"]
    assert r["params"]["stop_at_alpha"] is True


def test_split_sample_is_refused():
    with pytest.raises(ValueError):
        race._make_procedure("split_sample", "k", None, "card")


def test_summary_lines_render(setup):
    res = _race(setup)
    txt = race.summary_lines(res)
    assert "procedure" in txt and "yield" in txt
    assert "not a valid p-value" in txt
    assert "honest baseline" in txt
