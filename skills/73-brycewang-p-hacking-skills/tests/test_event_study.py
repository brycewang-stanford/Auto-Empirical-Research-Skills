"""Event-study axes: window, reference period and estimand move the estimate; lags recover truth."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, search

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")


def _dyn(seed=4, n_unit=100, n_t=16):
    rng = np.random.default_rng(seed)
    coh = rng.choice([0, 6, 9], size=n_unit); rows = []
    for i in range(n_unit):
        a = rng.normal()
        for t in range(n_t):
            tr = float(coh[i] > 0 and t >= coh[i]); r = t - coh[i] if coh[i] else -99
            tau = (0.5 + 0.25 * r) if tr else 0.0
            rows.append(dict(unit=i, year=t, treat=tr, y=a + 0.1 * t + tau + rng.normal(0, .5)))
    return pd.DataFrame(rows)


def _card(**kw):
    base = {"design": "did", "outcomes": ["y"], "treatment": "treat", "fixed_effects": [["unit", "year"]],
            "vcov": ["cluster"], "cluster": ["unit"], "panel_unit": "unit", "panel_time": "year"}
    base.update(kw); return grid.load_card(base)


def test_lags_recover_dynamic_truth_and_pretrend_is_null():
    card = _card(event_windows=[[3, 4]], reference_periods=[-1],
                 event_estimands=["lag0", "lag2", "avg_post", "avg_pre"])
    led = search.flag_pathologies(search.run(_dyn(), card), card).set_index("ev_estimand")
    assert (led["status"] == "ok").all()
    assert abs(led.loc["lag0", "coef"] - 0.5) < 3 * led.loc["lag0", "se"]
    assert abs(led.loc["lag2", "coef"] - 1.0) < 3 * led.loc["lag2", "se"]
    assert led.loc["avg_pre", "p"] > 0.05 and led.loc["avg_pre", "flag_event_misuse"]
    assert not led.loc["avg_post", "flag_event_misuse"]


def test_reference_period_and_window_are_axes():
    card = _card(event_windows=[[3, 4], [5, 6]], reference_periods=[-1, -2, -3],
                 event_estimands=["avg_post"])
    specs = grid.enumerate_specs(card)
    assert len(specs) == 7 and grid.universe_size(card)["dimensions"] == {"ev_window": 3, "ev_ref": 4, "ev_estimand": 2}
    led = search.run(_dyn(), card); ev = led[led.ev_window.notna()]
    assert ev["coef"].max() - ev["coef"].min() > 0.1          # the lever moves the estimate
    assert led["label"].str.contains("es=w3/4/ref-1/avg_post", regex=False).any()


def test_event_axes_collapse_for_non_twfe_and_prereg_resolves():
    card = _card(event_windows=[[3, 3]], did_estimators=["twfe", "did2s"],
                 preregistered={"ev_window": [3, 3], "ev_ref": -1, "ev_estimand": "avg_post"})
    specs = grid.enumerate_specs(card)
    assert all(s.did_estimator == "twfe" for s in specs if s.ev_window is not None)
    assert sum(s.ev_window is None for s in specs) == 2       # static twfe + did2s
    assert grid.resolve_prereg(card, specs) is not None


def test_bad_reference_period_is_recorded_not_raised():
    card = _card(event_windows=[[2, 2]], reference_periods=[5])
    led = search.run(_dyn(), card)
    assert led.loc[led.ev_window.notna(), "status"].str.startswith("error").all()


def test_shipped_event_card():
    card = grid.load_card(os.path.join(ROOT, "null_staggered_event_card.json"))
    assert grid.universe_size(card)["n_specs"] == 1200
    assert grid.resolve_prereg(card) is not None
    df = pd.read_csv(os.path.join(ROOT, "null_staggered.csv"))
    led = search.flag_pathologies(search.run(df, card, specs=grid.enumerate_specs(card)[::48]), card)
    assert (led["status"] == "ok").all()
