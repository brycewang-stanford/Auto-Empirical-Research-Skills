"""Polyglot: export writes a runnable contract, ingest reads it back, parity compares, runners run where available."""
import sys, os, json, shutil, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, search, polyglot

ROOT = os.path.join(os.path.dirname(__file__), "..", "eval", "data")
PY = sys.executable


def _export(tmp_path, data, card, lang, k=12, B=2, scheme="permute", **kw):
    df = pd.read_csv(os.path.join(ROOT, data)); c = grid.load_card(os.path.join(ROOT, card))
    c.update(kw)
    full = grid.enumerate_specs(c); pre = grid.resolve_prereg(c, full)
    specs = grid.thin(full, k, keep_keys=[pre])
    out = polyglot.export(df, c, specs, str(tmp_path / f"{lang}_{data[:-4]}"), lang=lang,
                          data_path=os.path.join(ROOT, data), null_B=B, null_scheme=scheme)
    return out, specs, c, df


def test_specs_table_is_language_neutral_and_keys_match(tmp_path):
    out, specs, card, df = _export(tmp_path, "null_rdd.csv", "null_rdd_card.json", "python", k=10, B=0)
    tab = pd.read_csv(os.path.join(out["dir"], "specs.csv"))
    assert list(tab["key"]) == [s.key() for s in specs]
    assert set(polyglot.SPEC_COLS) <= set(tab.columns)
    assert tab["bw_abs"].notna().all() and (tab["bw_abs"] > 0).all()       # bandwidths resolved
    assert tab["design"].eq("rdd").all() and tab["running"].eq("vote_share").all()


def test_null_columns_reproduce_engine_draws(tmp_path):
    out, specs, card, df = _export(tmp_path, "null_panel.csv", "null_panel_card.json", "r", k=6, B=3,
                                   scheme="cluster_permute")
    nulls = pd.read_csv(os.path.join(out["dir"], "null_columns.csv"))
    assert {"__row", "treat__1", "treat__2", "treat__3"} <= set(nulls.columns)
    rng = np.random.default_rng(0)
    d1 = search._draw_null(df, card, rng, "cluster_permute")
    assert np.array_equal(d1["treat"].to_numpy(), nulls["treat__1"].to_numpy())


@pytest.mark.parametrize("lang", list(polyglot.LANGUAGES))
def test_every_runner_is_written(tmp_path, lang):
    out, *_ = _export(tmp_path, "null_iv.csv", "null_iv_card.json", lang, k=5, B=1)
    assert os.path.exists(out["runner"]) and os.path.getsize(out["runner"]) > 2000
    meta = json.load(open(os.path.join(out["dir"], "export.json")))
    assert meta["lang"] == lang and meta["null_vars"] == ["z1", "z2", "z3"]


def test_ingest_roundtrip_from_engine_ledger(tmp_path):
    """A raw ledger written from the engine's own numbers ingests to an identical audit."""
    out, specs, card, df = _export(tmp_path, "null_panel.csv", "null_panel_card.json", "stata", k=15, B=2,
                                   scheme="cluster_permute")
    led = search.run(df, card, specs=specs)
    raw = led[["key", "label", "coef", "se", "t", "p", "n", "status"]].astype(object).copy()
    raw.loc[raw.index[0], ["coef", "se", "t", "p", "status"]] = [".", ".", ".", ".", "error: r(2000)"]   # Stata-style missing
    raw.to_csv(os.path.join(out["dir"], "ledger_raw.csv"), index=False)
    ns = []
    nd = search.null_calibration(df, card, B=2, scheme="cluster_permute", specs=specs, seed=0)
    for b in range(2):
        for j, s in enumerate(specs):
            ns.append({"draw": b + 1, "key": s.key(), "coef": nd.coef[b, j], "t": nd.t[b, j], "p": nd.p[b, j]})
    pd.DataFrame(ns).to_csv(os.path.join(out["dir"], "null_stats.csv"), index=False)
    aud = polyglot.ingest(out["dir"], with_parity=False)
    assert aud["n_specs_estimated"] == len(specs) - 1 and aud["n_specs_failed"] == 1
    assert aud["language"] == "stata" and "min_p_test" in aud and "preregistered" in aud
    led2 = pd.read_csv(os.path.join(out["dir"], "ledger.csv"))
    assert "spec_json" in led2 and "n_flags" in led2 and "p_dir" in led2
    m = led2[led2["status"] == "ok"].merge(led, on="key", suffixes=("_in", "_eng"))
    assert len(m) == len(specs) - 1
    assert np.allclose(m["coef_in"], m["coef_eng"]) and np.allclose(m["p_in"], m["p_eng"])
    assert os.path.exists(os.path.join(out["dir"], "report.md"))


def test_python_runner_executes_and_matches_engine(tmp_path):
    pytest.importorskip("statsmodels")
    out, specs, card, df = _export(tmp_path, "null_panel.csv", "null_panel_card.json", "python", k=10, B=1,
                                   scheme="cluster_permute")
    r = subprocess.run([PY, "run_specs.py"], cwd=out["dir"], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr[-800:]
    p = polyglot.parity(out["dir"])
    assert p["n_compared"] >= 8 and p["max_abs_coef_gap"] < 1e-3 and p["max_rel_se_gap"] < 0.1
    assert os.path.exists(os.path.join(out["dir"], "null_stats.csv"))
    aud = polyglot.ingest(out["dir"])
    assert aud["min_p_test"]["n_null_draws"] == 1


@pytest.mark.skipif(shutil.which("Rscript") is None, reason="R not installed")
def test_r_runner_executes(tmp_path):
    chk = subprocess.run(["Rscript", "-e", "cat(requireNamespace('fixest', quietly=TRUE))"], capture_output=True, text=True)
    if "TRUE" not in chk.stdout:
        pytest.skip("fixest not installed")
    out, specs, card, df = _export(tmp_path, "null_panel.csv", "null_panel_card.json", "r", k=8, B=1,
                                   scheme="cluster_permute")
    r = subprocess.run(["Rscript", "run_specs.R"], cwd=out["dir"], capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stderr[-800:]
    p = polyglot.parity(out["dir"])
    assert p["n_compared"] >= 6 and p["max_abs_coef_gap"] < 1e-2


def test_statspai_runner_executes(tmp_path):
    pytest.importorskip("statspai")
    out, specs, card, df = _export(tmp_path, "null_iv.csv", "null_iv_card.json", "statspai", k=6, B=0)
    r = subprocess.run([PY, "run_specs_statspai.py"], cwd=out["dir"], capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stderr[-800:]
    raw = pd.read_csv(os.path.join(out["dir"], "ledger_raw.csv"))
    assert raw["status"].astype(str).str.match("ok|unsupported").all()
    p = polyglot.parity(out["dir"])
    if p["n_compared"]:
        assert p["max_abs_coef_gap"] < 1e-3
