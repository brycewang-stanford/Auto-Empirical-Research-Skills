"""Search procedures: deterministic given the rng, replayable, and each stops for the right reason."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, search, procedures

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")


@pytest.fixture(scope="module")
def setup():
    df = pd.read_csv(os.path.join(ROOT, "null_panel.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_panel_card.json"))
    card["direction"] = "+"
    specs = grid.thin(grid.enumerate_specs(card), 400, keep_keys=[grid.resolve_prereg(card)])
    return df, card, specs


def _walk(setup, proc, seed=0):
    df, card, specs = setup
    fit = search.make_fitter(df, card)
    return proc.walk(specs, fit, rng=np.random.default_rng(seed), alpha=0.05, direction=1), fit


def test_exhaustive_visits_everything_and_reports_best(setup):
    w, fit = _walk(setup, procedures.Exhaustive())
    assert len(w.visited) == len(setup[2])
    best = min(setup[2], key=lambda s: procedures._objective(fit(s), 1))
    assert w.reported.key() == best.key()


def test_first_significant_stops_early_and_is_modest(setup):
    w, fit = _walk(setup, procedures.FirstSignificant(order="card"))
    r = fit(w.reported)
    if "first significant" in w.stopped:
        assert procedures._objective(r, 1) < 0.05
        assert len(w.visited) < len(setup[2])
        # everything before the reported spec was NOT significant
        assert all(procedures._objective(fit(s), 1) >= 0.05 for s in w.visited[:-1])
    else:
        assert w.reported.key() == w.visited[0].key()      # honest fallback


def test_random_budget_respects_budget_and_is_deterministic(setup):
    w1, _ = _walk(setup, procedures.RandomBudget(budget=25), seed=3)
    w2, _ = _walk(setup, procedures.RandomBudget(budget=25), seed=3)
    w3, _ = _walk(setup, procedures.RandomBudget(budget=25), seed=4)
    assert len(w1.visited) == 25
    assert [s.key() for s in w1.visited] == [s.key() for s in w2.visited]
    assert [s.key() for s in w1.visited] != [s.key() for s in w3.visited]


def test_greedy_moves_one_axis_at_a_time_and_improves(setup):
    df, card, specs = setup
    pre = grid.resolve_prereg(card, specs)
    w, fit = _walk(setup, procedures.GreedyCoordinate(start=pre, stop_at_alpha=False, max_rounds=2))
    assert w.visited[0].key() == pre
    idx = grid.SpecIndex(specs)
    for step in w.path:                                    # every move changes exactly one axis
        assert step["axis"] in idx.varying
        assert step["p_to"] < step["p_from"]
    p0 = procedures._objective(fit(w.visited[0]), 1)
    assert procedures._objective(fit(w.reported), 1) <= p0


def test_hill_climb_never_accepts_a_worse_move(setup):
    w, fit = _walk(setup, procedures.HillClimb(budget=40, stop_at_alpha=False, patience=10), seed=1)
    ps = [step["p_to"] for step in w.path]
    assert all(np.diff(ps) < 0) if len(ps) > 1 else True
    assert len(w.visited) <= 40


def test_run_with_procedure_marks_reported_and_records_walk(setup):
    df, card, specs = setup
    led = search.run(df, card, specs=specs, procedure=procedures.RandomBudget(budget=20), seed=0)
    assert len(led) == 20 and led["reported"].sum() == 1
    assert led["order"].tolist() == list(range(20))
    assert led.attrs["walk"]["procedure"] == "random"


def test_procedure_null_replay_gives_false_positive_rate(setup):
    df, card, specs = setup
    proc = procedures.FirstSignificant(order="random", budget=40)
    nd = search.null_calibration(df, card, B=12, scheme="cluster_permute", specs=specs,
                                 max_specs=60, procedure=proc, walk_specs=specs, seed=2)
    assert nd.reported_p_null.shape == (12,) and nd.n_visited_null.shape == (12,)
    assert np.all(nd.n_visited_null <= 40)
    led = search.flag_pathologies(search.run(df, card, specs=specs, procedure=proc, seed=2), card)
    a = search.audit(led, null=nd, alpha=0.05)
    assert "procedure_test" in a and 0 <= a["procedure_test"]["null_share_reporting_significant"] <= 1
    assert 0 < a["procedure_test"]["honest_p"] <= 1


def test_make_filters_unknown_params():
    p = procedures.make("greedy", budget=10, order="random", nonsense=1)
    assert isinstance(p, procedures.GreedyCoordinate) and p.budget == 10
    with pytest.raises(KeyError):
        procedures.make("teleport")


# ---- two-stage: pilot search, then holdout / pooled / pilot report

def test_split_sample_reports_the_stage_it_is_told_to(setup):
    df, card, specs = setup
    fit = search.make_fitter(df, card)
    walks = {}
    for stage in ("holdout", "pooled", "pilot"):
        proc = procedures.SplitSample(inner="exhaustive", stage=stage)
        walks[stage] = proc.walk(specs, fit, rng=np.random.default_rng(0), alpha=0.05, direction=1)
    keys = {s: w.reported.key() for s, w in walks.items()}
    assert len(set(keys.values())) == 1                       # same split, same pilot choice
    assert walks["pooled"].reported_result is None            # the full-data fit is the report
    assert walks["holdout"].reported_result["n"] < fit(walks["pooled"].reported)["n"]
    assert walks["pilot"].reported_result["n"] < fit(walks["pooled"].reported)["n"]
    assert walks["holdout"].path[0]["n_pilot_rows"] + walks["holdout"].path[0]["n_holdout_rows"] == len(df)
    assert all(k in walks["holdout"].stage_results[keys["holdout"]] for k in ("p_pilot", "coef_pilot"))


def test_split_sample_ledger_carries_pilot_p_and_the_stage_estimate(setup):
    df, card, specs = setup
    proc = procedures.SplitSample(inner="random", budget=15, stage="holdout")
    led = search.run(df, card, specs=specs, procedure=proc, seed=1)
    assert len(led) == 15 and "p_pilot" in led and led["p_pilot"].notna().all()
    rep = led[led["reported"]].iloc[0]
    full = search.make_fitter(df, card)(grid.SpecIndex(specs).by_key[rep["key"]])
    assert rep["n"] < full["n"] and rep["p"] != full["p"]    # the holdout estimate, not the pooled one
    assert led.attrs["walk"]["path"][0]["reported_stage"] == "holdout"


def test_split_sample_abandons_when_the_pilot_is_not_promising(setup):
    df, card, specs = setup
    fit = search.make_fitter(df, card)
    proc = procedures.SplitSample(inner="exhaustive", stage="holdout", continue_at=1e-9)
    w = proc.walk(specs, fit, rng=np.random.default_rng(0), alpha=0.05, direction=1)
    assert w.reported is None and "abandoned" in w.stopped and w.path[0]["continued"] is False
    led = search.run(df, card, specs=specs, procedure=proc, seed=0)
    assert not led["reported"].any()


def test_split_sample_null_replay_holdout_keeps_size_pooled_does_not(setup):
    df, card, specs = setup
    small = grid.thin(specs, 60, keep_keys=[grid.resolve_prereg(card, specs)])
    fpr = {}
    for stage in ("holdout", "pooled"):
        proc = procedures.SplitSample(inner="exhaustive", stage=stage)
        nd = search.null_calibration(df, card, B=30, scheme="cluster_permute", specs=small,
                                     max_specs=60, procedure=proc, walk_specs=small, seed=4)
        led = search.flag_pathologies(search.run(df, card, specs=small, procedure=proc, seed=4), card)
        pt = search.audit(led, null=nd, alpha=0.05)["procedure_test"]
        assert pt["null_share_reporting_any"] == 1.0
        fpr[stage] = pt["null_share_reporting_significant"]
    assert fpr["holdout"] <= 0.25                                 # nominal 0.05 on 30 draws
    assert fpr["pooled"] > fpr["holdout"]


def test_split_sample_continuation_rule_counts_only_what_was_reported(setup):
    df, card, specs = setup
    small = grid.thin(specs, 40, keep_keys=[grid.resolve_prereg(card, specs)])
    proc = procedures.SplitSample(inner="random", budget=10, stage="holdout", continue_at=0.10)
    nd = search.null_calibration(df, card, B=20, scheme="cluster_permute", specs=small,
                                 max_specs=40, procedure=proc, walk_specs=small, seed=5)
    assert 0 < np.isfinite(nd.reported_p_null).mean() < 1
    led = search.flag_pathologies(search.run(df, card, specs=small, procedure=proc, seed=5), card)
    a = search.audit(led, null=nd, alpha=0.05)
    pt = a["procedure_test"]
    assert pt["null_share_reporting_any"] == np.isfinite(nd.reported_p_null).mean()
    assert ("honest_p" in pt) == bool(led["reported"].any())


def test_make_builds_split_sample_and_rejects_bad_stage():
    p = procedures.make("split_sample", inner="greedy", stage="holdout", budget=5, continue_at=0.1)
    assert isinstance(p, procedures.SplitSample) and p._inner().name == "greedy" and p.budget == 5
    with pytest.raises(KeyError):
        procedures.SplitSample(stage="confirmatory")
    with pytest.raises(ValueError):
        procedures.SplitSample(inner="split_sample")
