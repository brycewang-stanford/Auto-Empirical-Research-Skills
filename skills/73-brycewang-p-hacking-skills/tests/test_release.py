"""Release surface: io formats, init drafts a valid card, schema, verify, bench, summary."""
import sys, os, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import numpy as np, pandas as pd, pytest
from phack import grid, search, io as _io, init_card, verify, bench, report, cli

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "eval", "data")


def test_read_table_formats(tmp_path):
    df = pd.read_csv(os.path.join(DATA, "null_iv.csv")).head(50)
    df.to_csv(tmp_path / "a.csv", index=False); df.to_csv(tmp_path / "a.tsv", sep="\t", index=False)
    df.to_stata(tmp_path / "a.dta", write_index=False); df.to_json(tmp_path / "a.json", orient="records")
    for f in ("a.csv", "a.tsv", "a.dta", "a.json"):
        got = _io.read_table(tmp_path / f)
        assert list(got.columns) == list(df.columns) and len(got) == 50
    with pytest.raises(ValueError):
        _io.read_table(tmp_path / "a.xyz")


def test_init_drafts_valid_cards():
    df = pd.read_csv(os.path.join(DATA, "null_panel.csv"))
    card, notes = init_card.draft_card(df, name="t")
    assert card["design"] == "did" and card["treatment"] == "treat" and card["panel_unit"] == "unit"
    c = grid.load_card(card)                      # passes schema + loader
    assert grid.resolve_prereg(c) is not None and grid.universe_size(c)["n_specs"] > 10
    st = pd.read_csv(os.path.join(DATA, "null_staggered.csv"))
    card2, _ = init_card.draft_card(st, name="s")
    assert "did_estimators" in card2                 # absorbing treatment detected
    rd = pd.read_csv(os.path.join(DATA, "null_rdd.csv"))
    card3, _ = init_card.draft_card(rd, running="vote_share", outcome="share_detained")
    assert card3["design"] == "rdd" and grid.resolve_prereg(grid.load_card(card3))
    iv = pd.read_csv(os.path.join(DATA, "null_iv.csv"))
    card4, _ = init_card.draft_card(iv, instruments=["z1", "z2"], treatment="d", outcome="y")
    assert card4["design"] == "iv" and grid.load_card(card4)["instruments_pool"] == ["z1", "z2"]


def test_schema_file_matches_code_and_rejects_bad_cards():
    on_disk = json.load(open(os.path.join(ROOT, "schema", "design-card.schema.json")))
    assert on_disk == grid.card_schema()
    pytest.importorskip("jsonschema")
    assert grid.validate_card({"outcomes": ["y"], "treatment": "d"}) == []
    assert grid.validate_card({"outcomes": ["y"], "treatment": "d", "vcov": ["hc9"]})
    with pytest.raises(ValueError):
        grid.load_card({"outcomes": ["y"], "treatment": "d", "vcov": ["hc9"]})


def test_search_verify_roundtrip(tmp_path):
    out = tmp_path / "run"
    cli.main(["search", os.path.join(DATA, "null_iv.csv"), os.path.join(DATA, "null_iv_card.json"),
              "--out", str(out), "--max-specs", "30", "--null-draws", "6", "--no-plot", "--summary"])
    for f in ("ledger.csv", "audit.json", "manifest.json", "card.json", "report.md", "null_meta.json"):
        assert (out / f).exists()
    man = json.load(open(out / "manifest.json"))
    assert set(man["files"]) == {"ledger.csv", "audit.json", "card.json"}
    res = verify.verify(str(out), data_path=os.path.join(DATA, "null_iv.csv"))
    assert res["ok"], [c for c in res["checks"] if not c["ok"]]
    # tamper with the ledger: verification must fail
    led = pd.read_csv(out / "ledger.csv"); led.loc[0, "p"] = 1e-9; led.to_csv(out / "ledger.csv", index=False)
    res2 = verify.verify(str(out), data_path=os.path.join(DATA, "null_iv.csv"))
    assert not res2["ok"] and any(c["check"] == "hash:ledger.csv" and not c["ok"] for c in res2["checks"])


def test_bench_freeze_and_check(tmp_path):
    r = bench.freeze(out=str(tmp_path / "b.json"), version="test")
    assert r["n_datasets"] >= 8 and r["n_cards"] >= 9
    b = json.load(open(tmp_path / "b.json"))
    assert set(b["scoring"]["weights"]) >= {"selection_on_significance", "inference_gap"}
    chk = bench.check(str(tmp_path / "b.json"))
    assert chk["ok"], chk["problems"]
    b["datasets"]["eval/data/null_iv.csv"] = "0" * 40
    json.dump(b, open(tmp_path / "b.json", "w"))
    assert not bench.check(str(tmp_path / "b.json"))["ok"]


def test_seal_commits_without_contents(tmp_path):
    priv = tmp_path / "priv"; priv.mkdir(); (priv / "secret_card.json").write_text('{"outcomes": ["y"]}')
    r = bench.seal(str(priv), out=str(tmp_path / "c.json"), root=str(tmp_path))
    c = json.load(open(tmp_path / "c.json"))
    assert r["n_files"] == 1 and "sha256" in c["files"]["secret_card.json"] and "outcomes" not in json.dumps(c)


def test_summary_lines_are_short():
    aud = json.load(open(os.path.join(ROOT, "docs", "example_audit.json"))) if os.path.exists(
        os.path.join(ROOT, "docs", "example_audit.json")) else None
    if aud is None:
        pytest.skip("no example audit")
    txt = report.summary_lines(aud)
    assert "NULL-CALIBRATED" in txt and len(txt.splitlines()) <= 14


def test_console_script_installed_or_shim_works():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "phack_cli.py"), "schema"], capture_output=True, text=True)
    assert r.returncode == 0 and '"title": "phack design card"' in r.stdout


def test_verify_accepts_procedure_runs(tmp_path):
    """Regression: verify's recompute used to fail on any procedure run (the null replay's
    visit counts were never saved), and filtered the walk's ledger down to the null's specs."""
    for name, extra in (("greedy", ["--procedure", "greedy", "--stop-at-alpha"]),
                        ("split", ["--procedure", "split_sample", "--inner", "random", "--budget", "8",
                                   "--stage", "holdout", "--continue-at", "0.9"])):
        out = tmp_path / name
        cli.main(["search", os.path.join(DATA, "null_iv.csv"), os.path.join(DATA, "null_iv_card.json"),
                  "--out", str(out), "--null-draws", "6", "--null-max-specs", "20", "--no-plot",
                  "--summary", "--direction", "+"] + extra)
        assert (out / "walk.json").exists() and (out / "n_visited_null.npy").exists()
        res = verify.verify(str(out), data_path=os.path.join(DATA, "null_iv.csv"))
        assert res["ok"], [c for c in res["checks"] if not c["ok"]]
        aud = json.load(open(out / "audit.json"))
        assert "procedure_test" in aud and aud["procedure_test"]["null_share_reporting_any"] <= 1
