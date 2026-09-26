"""Detection battery is calibrated on known ground truth."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np
from scipy import stats
from phack import detect


def _honest(seed=11, n=600, ncp=2.8):
    z = np.abs(np.random.default_rng(seed).normal(ncp, 1, n))
    return 2 * stats.norm.sf(z)


def _hacked(seed=11, n=3000):
    rng = np.random.default_rng(seed)
    zn = np.abs(rng.normal(0, 1, n))
    zh = np.where((zn > 1.5) & (zn < 1.96), zn + rng.uniform(.05, .6, n), zn)
    return 2 * stats.norm.sf(zh[zh > 1.35])


def test_honest_literature_not_flagged():
    r = detect.report(pvals=_honest(), seed=1)
    assert r["shape_tests_flagging"] == []
    assert r["bunching_tests_flagging"] == []          # counterfactual, not naive
    assert r["verdict"].startswith("no distributional")
    pw = [t for t in r["tests"] if t["test"] == "pcurve_power"][0]
    assert 0.7 < pw["estimated_power"] < 0.9         # true power at ncp 2.8 ~ .80


def test_naive_caliper_would_have_false_positived():
    cal = detect.caliper_test(stats.norm.isf(_honest() / 2))
    assert cal["naive_p_value"] < 0.05                 # the classic test fails here
    assert cal["p_value"] > 0.05                       # the counterfactual does not


def test_hacked_null_is_caught():
    r = detect.report(pvals=_hacked(), seed=1)
    assert len(r["shape_tests_flagging"]) >= 3
    assert r["verdict"].startswith("strong")
    pw = [t for t in r["tests"] if t["test"] == "pcurve_power"][0]
    assert pw["estimated_power"] < 0.10


def test_lcm_is_a_concave_majorant():
    x = np.linspace(0, 1, 50); y = np.sin(3 * x) + 0.2 * np.random.default_rng(0).normal(size=50)
    m = detect._lcm(x, y)
    assert np.all(m >= y - 1e-12)
    assert np.all(np.diff(m, 2) <= 1e-9)


def test_small_samples_return_notes_not_pvalues():
    r = detect.report(pvals=np.array([0.01, 0.02, 0.03]))
    for t in r["tests"]:
        assert "note" in t or "p_value" in t or "p_left_skew" in t


# ---- threshold signatures and the across-stages battery (Adda, Decker & Ottaviani 2020)

def _selective_reporting(seed=3, n=4000, drop=0.5):
    """Half of the non-significant results are never reported: a level shift at 1.96, no spike."""
    rng = np.random.default_rng(seed)
    z = np.abs(rng.normal(1.2, 1.2, n))
    return z[~((z < 1.96) & (rng.random(n) < drop))]


def _pushed_across(seed=5, n=1500):
    """Half of the results just below the line are pushed just past it: a spike, no missing mass beyond."""
    rng = np.random.default_rng(seed)
    z = np.abs(rng.normal(1.0, 1.2, n))
    push = (z > 1.6) & (z < 1.96) & (rng.random(n) < 0.5)
    return np.where(push, 1.96 + rng.uniform(0, 0.15, n), z)


def test_density_jump_has_size_on_a_rising_density():
    rej = [detect.density_jump_test(stats.norm.isf(_honest(s) / 2), B=150, seed=s)["p_value"] < 0.05
           for s in range(30)]
    assert np.mean(rej) <= 0.17                        # nominal 0.05; 30 draws


def test_density_jump_sees_a_level_shift_and_spike_test_does_not():
    z = _selective_reporting()
    j = detect.density_jump_test(z, seed=1)
    assert j["jump"] > 0 and j["p_value"] < 0.01
    assert detect.spike_test(z)["p_value"] > 0.05
    r = detect.report(zstats=z, seed=1)
    assert "density_jump" in r["flagged_by"] and "spike" not in r["flagged_by"]
    assert r["threshold_signature"].startswith("discontinuity at the threshold without a spike")


def test_spike_test_sees_results_pushed_across():
    z = _pushed_across()
    assert detect.spike_test(z)["p_value"] < 0.01
    assert detect.report(zstats=z, seed=1)["threshold_signature"].startswith("spike")


def test_spike_test_size_under_the_null_and_a_mixture():
    rej = []
    for s in range(30):
        rng = np.random.default_rng(s)
        rej.append(detect.spike_test(np.abs(rng.normal(0, 1, 3000)))["p_value"] < 0.05)
        z = np.abs(np.where(rng.random(1800) < 0.5, rng.normal(0, 1, 1800), rng.normal(2.5, 1, 1800)))
        rej.append(detect.spike_test(z)["p_value"] < 0.05)
    assert np.mean(rej) <= 0.15


def test_phase_shift_and_dominance():
    rng = np.random.default_rng(0)
    early = np.abs(rng.normal(0.8, 1, 2000)); late = np.abs(rng.normal(1.6, 1, 800))
    r = detect.phase_shift_test(early, late)
    assert r["share_significant_late"] > r["share_significant_early"]
    assert r["p_value"] < 1e-6 and r["ks_dominance_p"] < 1e-6
    same = detect.phase_shift_test(early, np.abs(rng.normal(0.8, 1, 800)))
    assert same["p_value"] > 0.01


def test_continuation_explains_selection_but_not_concealment():
    """Rates over seeds, not one fixture: each threshold test has a 5% false-alarm rate by design."""
    from phack import simulate as sim
    explained, clean = [], []
    for seed in range(8):
        pop = sim.continuation_shift(n_projects=6000, conceal=0.0, seed=seed)
        r = detect.phase_report(pop["z_pilot"], pop["z_main_reported"], continued=pop["continued"], seed=1)
        c = r["continuation"]
        assert c["logit"]["beta_z"] > 0 and c["logit"]["p_z"] < 1e-6      # continuation rises in the pilot z
        assert r["phase_shift"]["p_value"] < 1e-6                            # phase III has more significant results
        explained.append(c["explained_share"])
        clean.append(r["signature"].startswith("more significant results in the later stage, no threshold "
                                               "signature, and the continuation rule explains"))
    assert 0.8 <= np.mean(explained) <= 1.2                                  # ... and the rule explains it
    assert sum(clean) >= 6                                                   # no threshold signature, no residual
    hidden, shifted = [], []
    for seed in range(4):
        pop = sim.continuation_shift(n_projects=6000, conceal=0.5, seed=seed)
        r = detect.phase_report(pop["z_pilot"], pop["z_main_reported"], continued=pop["continued"], seed=1)
        c = r["continuation"]
        hidden.append(c["unexplained_pp"] > 10 and c["p_value"] < 0.01)      # concealment is left unexplained
        shifted.append(r["late"]["density_jump"]["p_value"] < 0.05)           # and shows as a level shift
        assert r["signature"].startswith(("discontinuity at the threshold in the later stage with no spike",
                                          "spike past the threshold"))
    assert all(hidden) and all(shifted)


def test_deterministic_continuation_is_flagged_as_unidentified():
    rng = np.random.default_rng(1)
    z1 = np.abs(rng.normal(0.5, 1, 2000)); cont = z1 > 1.3; z2 = np.abs(rng.normal(0.9, 1, int(cont.sum())))
    r = detect.continuation_decomposition(z1, cont, z2, B=30)
    assert "note" in r
