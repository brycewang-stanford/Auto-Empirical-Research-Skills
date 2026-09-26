"""Strategy simulator recovers nominal alpha and the published ordering."""
import sys, os, warnings
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pytest
from phack import simulate as sim

warnings.filterwarnings("ignore")


@pytest.mark.parametrize("name", list(sim.STRATEGIES))
def test_nominal_alpha_recovered(name):
    r = sim.false_positive_rate(name, n_sims=600, seed=7)
    assert 0.02 <= r["fpr_original"] <= 0.09
    assert r["fpr_hacked"] >= r["fpr_original"] - 0.01


def test_modest_and_ambitious_reject_identically():
    a = sim.false_positive_rate("01_selective_dv", n_sims=500, seed=1)
    b = sim.false_positive_rate("01_selective_dv", n_sims=500, seed=1, ambitious=True)
    assert a["fpr_hacked"] == b["fpr_hacked"]
    assert b["mean_attempts"] >= a["mean_attempts"]


def test_strong_strategies_beat_weak_ones():
    strong = sim.false_positive_rate("07_transformation", n_sims=800, seed=2)["fpr_hacked"]
    weak = sim.false_positive_rate("05_covariates", n_sims=800, seed=2)["fpr_hacked"]
    assert strong > 0.15 > weak


def test_workflow_is_cumulative_with_diminishing_returns():
    w = sim.workflow(["09_alternative_tests", "01_selective_dv", "11_subgroup",
                      "04_outlier_exclusion"], n_sims=400, seed=5)
    c = w["cumulative_fpr"]
    assert all(np.diff(c) >= 0)
    assert c[-1] > 0.3


def test_selective_continuation_is_not_p_hacking_until_the_pilot_is_pooled():
    main = sim.false_positive_rate("26_selective_continuation", n_sims=1500, seed=3, report="main")
    pooled = sim.false_positive_rate("26_selective_continuation", n_sims=1500, seed=3, report="pooled")
    best = sim.false_positive_rate("26_selective_continuation", n_sims=1500, seed=3, report="best")
    assert 0.03 <= main["fpr_hacked"] <= 0.075            # a fresh confirmatory sample keeps its size
    assert pooled["fpr_hacked"] > 0.12                    # the pilot's luck inside the reported test
    assert best["fpr_hacked"] > pooled["fpr_hacked"]      # selective reporting across stages
    assert main["mean_attempts"] > 5                      # ~1/go pilots run per continued project
    with pytest.raises(KeyError):
        sim.run_strategy("26_selective_continuation", np.random.default_rng(0), report="pilot")


def test_continuation_shift_moves_the_share_significant_between_phases():
    pop = sim.continuation_shift(n_projects=3000, seed=1)
    assert pop["share_significant_main_all"] > pop["share_significant_pilot"] + 0.05
    assert pop["z_main_reported"].size == pop["n_reported"] == pop["n_continued"]
    hid = sim.continuation_shift(n_projects=3000, seed=1, conceal=0.5)
    assert hid["n_reported"] < hid["n_continued"]
    assert hid["share_significant_main_reported"] > pop["share_significant_main_reported"]
    assert np.array_equal(hid["z_pilot"], pop["z_pilot"])   # same projects, different reporting
