"""Robustness theatre: a selected table is detected, a random one is not."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, search, theatre

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")


@pytest.fixture(scope="module")
def led():
    df = pd.read_csv(os.path.join(ROOT, "null_staggered.csv"))
    card = grid.load_card(os.path.join(ROOT, "null_staggered_card.json"))
    specs = grid.enumerate_specs(card)[::6]
    return search.flag_pathologies(search.run(df, card, specs=specs), card)


def test_build_table_selects_agreeing_neighbours(led):
    ok = led[led.status == "ok"]
    best = ok.loc[ok["p"].idxmin(), "key"]
    t = theatre.build_table(led, best, k=8)
    tab = t["table"]
    assert tab.iloc[0]["key"] == best and len(tab) <= 8
    assert (tab["p"] < 0.05).all() and (np.sign(tab["coef"]) == np.sign(tab.iloc[0]["coef"])).all()
    assert tab["choices_from_reported"].is_monotonic_increasing
    assert t["share_of_ledger_agreeing"] < 0.5 and t["n_in_ledger"] == len(ok)


def test_audit_flags_selected_table_and_passes_random_one(led):
    ok = led[led.status == "ok"]
    best = ok.loc[ok["p"].idxmin(), "key"]
    shown = theatre.build_table(led, best, k=8)["table"]["key"].tolist()
    a = theatre.audit_table(led, shown, B=500)
    assert a["p_share_significant"] < 0.05 and a["verdict"].startswith(("robustness theatre", "selective"))
    assert a["hidden"]["share_significant"] < a["shown"]["share_significant"]
    rnd = ok.sample(8, random_state=3)["key"].tolist()
    b = theatre.audit_table(led, rnd, B=500)
    assert b["p_share_significant"] > 0.05 or b["shown"]["share_significant"] == 0.0


def test_audit_handles_unknown_keys(led):
    assert "note" in theatre.audit_table(led, ["nope"])
