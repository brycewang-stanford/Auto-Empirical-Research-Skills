"""
Polyglot: the grid is the contract.

A design card enumerates a specification universe once, in Python. This
module writes that universe out as a flat `specs.csv` and generates a runner
in the user's own statistical language -- Stata, R, Python (statsmodels /
linearmodels) or StatsPAI -- that estimates every row with that language's
own commands and writes back a ledger in the schema `phack audit`, `plot`,
`theatre` and `score` already read. Null draws are exported the same way
(the permuted columns, one set per draw) so the runner can replay the search
under the null and the honest p-value can be computed from what *that
language* reports.

Why this matters for an evaluation instrument: an agent that p-hacks in
Stata reports Stata's p-values, with Stata's small-sample conventions, and
the honest counterpart has to be computed on the same footing. The keys
(sha1 of the specification label) are identical across languages, so a
Stata ledger, an R ledger and the Python ledger of the same card line up
row for row.

    phack export DATA CARD --lang stata --out run_stata/ --null-draws 100
    cd run_stata && stata -b do run_specs.do        # or Rscript run_specs.R, python run_specs.py
    phack ingest run_stata/ --out run_stata/         # -> ledger.csv, audit.json, report.md

Coverage differs by language and is recorded per row as `status =
unsupported: ...` rather than silently skipped. See references/language-map.md.
"""
from __future__ import annotations

import json, os, re, textwrap

import numpy as np
import pandas as pd

from . import core, grid, search

__all__ = ["LANGUAGES", "write_specs", "write_null_columns", "write_runner", "export",
           "ingest_ledger", "ingest_null", "ingest"]

LANGUAGES = ("stata", "r", "python", "statspai")

SPEC_COLS = ["key", "label", "outcome", "treatment", "controls", "fe", "vcov", "cluster1", "cluster2",
             "y_transform", "d_transform", "outlier_rule", "outlier_basis", "imputation",
             "subsample", "weight", "lag", "did_estimator", "comparison_group",
             "ev_pre", "ev_post", "ev_ref", "ev_estimand",
             "bw_abs", "kernel", "poly", "donut", "rdd_inference",
             "instruments", "iv_estimator", "running", "cutoff", "design"]


# --------------------------------------------------------------------------
# specs.csv
# --------------------------------------------------------------------------

def _query_generic(q):
    """pandas query -> the subset of syntax Stata and R both accept."""
    if not q:
        return ""
    s = q.strip()
    s = re.sub(r"\band\b", "&", s); s = re.sub(r"\bor\b", "|", s); s = re.sub(r"\bnot\b", "!", s)
    return s


def spec_rows(specs, card, df=None) -> pd.DataFrame:
    """Flatten Spec objects into the language-neutral table. RDD bandwidths
    are resolved to absolute values here (pilot x multiplier, IK computed
    on the data) so every language uses exactly the same h."""
    rows = []
    design = card.get("design", "ols")
    subs = card.get("subsamples") or {}
    pilot_cache = {}
    for s in specs:
        cl1 = cl2 = ""
        if isinstance(s.cluster, tuple):
            cl1, cl2 = s.cluster
        elif s.cluster:
            cl1 = s.cluster
        bw_abs = ""
        if design == "rdd" and s.bandwidth is not None:
            if isinstance(s.bandwidth, tuple):
                bw_abs = float(s.bandwidth[1])
            elif df is not None:
                k = (s.outcome, s.bw_selector, s.subsample, s.imputation)
                if k not in pilot_cache:
                    d = df.query(subs[s.subsample]) if s.subsample != "full" else df
                    d = d[[s.outcome, card["running"]]].dropna()
                    x = d[card["running"]].to_numpy(float); y = d[s.outcome].to_numpy(float)
                    pilot_cache[k] = (core.ik_bandwidth(y, x, card["cutoff"]) if s.bw_selector == "ik"
                                      else core.rot_bandwidth(x - card["cutoff"]))
                bw_abs = float(s.bandwidth) * pilot_cache[k]
        rows.append({
            "key": s.key(), "label": s.label(), "outcome": s.outcome, "treatment": s.treatment,
            "controls": " ".join(s.controls), "fe": " ".join(s.fe), "vcov": s.vcov,
            "cluster1": cl1, "cluster2": cl2, "y_transform": s.y_transform, "d_transform": s.d_transform,
            "outlier_rule": s.outlier_rule, "outlier_basis": card.get("outlier_basis", "outcome"),
            "imputation": s.imputation,
            "subsample": _query_generic(subs.get(s.subsample)) if s.subsample != "full" else "",
            "weight": s.weight or "", "lag": int(s.lag or 0),
            "did_estimator": s.did_estimator, "comparison_group": s.comparison_group,
            "ev_pre": s.ev_window[0] if s.ev_window else "", "ev_post": s.ev_window[1] if s.ev_window else "",
            "ev_ref": s.ev_ref if s.ev_window else "", "ev_estimand": s.ev_estimand or "",
            "bw_abs": bw_abs, "kernel": s.kernel if design == "rdd" else "",
            "poly": s.poly if design == "rdd" else "", "donut": s.donut if design == "rdd" else "",
            "rdd_inference": s.rdd_inference if design == "rdd" else "",
            "instruments": " ".join(s.instruments), "iv_estimator": s.iv_estimator if design == "iv" else "",
            "running": card.get("running") or "", "cutoff": card.get("cutoff", 0.0) if design == "rdd" else "",
            "design": design,
        })
    return pd.DataFrame(rows, columns=SPEC_COLS)


def write_specs(specs, card, path, df=None):
    tab = spec_rows(specs, card, df)
    tab.to_csv(path, index=False)
    return tab


# --------------------------------------------------------------------------
# null columns: one set of permuted columns per draw
# --------------------------------------------------------------------------

def null_vars(card):
    design = card.get("design", "ols")
    if design == "rdd":
        return list(card["outcomes"])
    if design == "iv":
        return list(card["instruments_pool"])
    return [card["treatment"]]


def write_null_columns(df, card, path, B=100, scheme="permute", seed=0):
    """`<var>__<b>` for b = 1..B, plus `__row` to merge on. Exactly the draws
    `search._draw_null` would make, so a foreign runner and the Python engine
    are calibrated against the same nulls."""
    rng = np.random.default_rng(seed)
    out = pd.DataFrame({"__row": np.arange(len(df))})
    vs = null_vars(card)
    for b in range(1, B + 1):
        d = search._draw_null(df, card, rng, scheme)
        for v in vs:
            out[f"{v}__{b}"] = d[v].to_numpy()
    out.to_csv(path, index=False)
    return vs


# --------------------------------------------------------------------------
# runners
# --------------------------------------------------------------------------

def _fill(template, **kw):
    for k, v in kw.items():
        template = template.replace("@@" + k + "@@", str(v))
    return template


def write_runner(lang, out_dir, card, *, null_B=0, null_vars_list=(), data_file="data.csv"):
    lang = lang.lower()
    if lang not in LANGUAGES:
        raise KeyError(f"unknown language {lang!r}; known: {LANGUAGES}")
    tmpl = {"stata": STATA, "r": R, "python": PYTHON, "statspai": STATSPAI}[lang]
    fname = {"stata": "run_specs.do", "r": "run_specs.R", "python": "run_specs.py",
             "statspai": "run_specs_statspai.py"}[lang]
    unit = card.get("panel_unit") or ""; time = card.get("panel_time") or ""
    code = _fill(tmpl, NULL_B=null_B, NULL_VARS=" ".join(null_vars_list),
                 NULL_VARS_R='c(' + ", ".join(f'"{v}"' for v in null_vars_list) + ')',
                 NULL_VARS_PY=json.dumps(list(null_vars_list)),
                 UNIT=unit, TIME=time, DATA=data_file, DESIGN=card.get("design", "ols"),
                 STACK_PRE=(card.get("stack_window") or [3, 3])[0],
                 STACK_POST=(card.get("stack_window") or [3, 3])[1])
    path = os.path.join(out_dir, fname)
    with open(path, "w") as fh:
        fh.write(code)
    return path


def export(df, card, specs, out_dir, *, lang="stata", data_path=None, null_B=0,
           null_scheme="permute", seed=0):
    os.makedirs(out_dir, exist_ok=True)
    tab = write_specs(specs, card, os.path.join(out_dir, "specs.csv"), df)
    df.to_csv(os.path.join(out_dir, "data.csv"), index=False)
    nv = []
    if null_B:
        nv = write_null_columns(df, card, os.path.join(out_dir, "null_columns.csv"),
                                B=null_B, scheme=null_scheme, seed=seed)
    runner = write_runner(lang, out_dir, card, null_B=null_B, null_vars_list=nv)
    meta = {"lang": lang, "n_specs": int(len(tab)), "null_draws": int(null_B), "null_scheme": null_scheme,
            "null_vars": nv, "seed": seed, "design": card.get("design", "ols"), "card": card,
            "data_path": data_path, "runner": os.path.basename(runner),
            "how_to_run": {"stata": "stata-mp -b do run_specs.do   (or: do run_specs.do inside Stata)",
                           "r": "Rscript run_specs.R", "python": "python run_specs.py",
                           "statspai": "python run_specs_statspai.py"}[lang],
            "then": "phack ingest <this directory>"}
    meta["requirements"] = REQUIREMENTS[lang]
    with open(os.path.join(out_dir, "export.json"), "w") as fh:
        json.dump(meta, fh, indent=2, default=str)
    with open(os.path.join(out_dir, "README.txt"), "w") as fh:
        fh.write(EXPORT_README.format(lang=lang, n=len(tab), B=null_B, runner=os.path.basename(runner),
                                      how=meta["how_to_run"], req=REQUIREMENTS[lang], design=card.get("design")))
    return {"dir": out_dir, "runner": runner, "n_specs": int(len(tab)), "null_draws": null_B,
            "how_to_run": meta["how_to_run"], "requirements": REQUIREMENTS[lang]}


REQUIREMENTS = {
    "stata": "Stata 16+; ssc install reghdfe ftools ivreghdfe ivreg2 ranktest rdrobust did2s",
    "r": "R >= 4.1; install.packages(c('fixest', 'data.table', 'rdrobust', 'did2s'))",
    "python": "pip install pandas numpy scipy statsmodels linearmodels",
    "statspai": "pip install statspai   (pip install 'statspai[fixest]' for IV with fixed effects)",
}

EXPORT_README = """phack export -- {lang} runner for a {design} design card
=================================================================

Files
  specs.csv          {n} specifications, one per row: every analytical choice, plus key and label
  data.csv           the data, exactly as the engine saw it
  null_columns.csv   {B} null draws: the permuted columns (<var>__<b>) the null replay swaps in
  {runner}    the generated runner -- read it; edit only if the grid semantics are kept
  export.json        what was exported, by whom, with which card

Requirements
  {req}

Run
  {how}

It writes
  ledger_raw.csv     key, label, coef, se, t, p, n, status, first_stage_F, bandwidth, n_left, n_right
  null_stats.csv     draw, key, coef, t, p   (only when null draws were exported)

Then, back in Python
  phack ingest <this directory> --parity
which writes ledger.csv, audit.json, manifest.json, report.md, spec_curve.png and parity.json.

Rows the runner cannot estimate in this language are written with
status = "unsupported: ..." and counted, never skipped. See references/language-map.md.
"""


# --------------------------------------------------------------------------
# ingest: foreign ledger -> phack ledger; foreign null stats -> NullDraws
# --------------------------------------------------------------------------

_COLMAP = {
    "coef": ["coef", "coefficient", "estimate", "b", "beta", "_b", "est"],
    "se": ["se", "std_err", "std.error", "stderr", "std_error", "_se", "std"],
    "t": ["t", "tstat", "t_stat", "statistic", "z", "tvalue"],
    "p": ["p", "pvalue", "p_value", "p.value", "pval", "prob"],
    "n": ["n", "nobs", "N", "n_obs", "obs"],
    "key": ["key", "spec_key", "spec", "id"],
    "label": ["label", "spec_label", "specification"],
}


def _normalise_columns(df):
    cols = {c.lower(): c for c in df.columns}
    out = pd.DataFrame(index=df.index)
    for want, alts in _COLMAP.items():
        for a in alts:
            if a.lower() in cols:
                v = df[cols[a.lower()]]
                out[want] = v if want in ("key", "label") else pd.to_numeric(v, errors="coerce")
                break
    for extra in ("status", "first_stage_F", "bandwidth", "n_left", "n_right", "ar_p", "kappa",
                  "n_clusters", "df", "psd_ok"):
        c = next((cc for cc in df.columns if cc.lower() == extra.lower()), None)
        if c is not None:
            out[extra] = df[c] if extra in ("status",) else pd.to_numeric(df[c], errors="coerce")
    return out


def ingest_ledger(raw: pd.DataFrame, specs_tab: pd.DataFrame, card: dict, direction=None) -> pd.DataFrame:
    """Join a runner's raw ledger (key, coef, se, t, p, n, status, ...) onto
    the spec table and rebuild the full phack ledger: axis columns,
    spec_json, one-sided p, flags."""
    raw = _normalise_columns(raw)
    if "key" not in raw:
        raise ValueError("foreign ledger needs a 'key' column (or spec/id) matching specs.csv")
    raw["key"] = raw["key"].astype(str).str.strip()
    specs = grid.enumerate_specs(card)
    by_key = {s.key(): s for s in specs}
    rows = []
    for i, r in raw.iterrows():
        s = by_key.get(r["key"])
        if s is None:
            continue
        rec = search._spec_record(s, int(i))
        for c in ("coef", "se", "t", "p"):
            rec[c] = float(r[c]) if c in r and pd.notna(r[c]) else np.nan
        rec["n"] = int(r["n"]) if "n" in r and pd.notna(r["n"]) else 0
        if not np.isfinite(rec["t"]) and np.isfinite(rec["coef"]) and rec["se"] and np.isfinite(rec["se"]):
            rec["t"] = rec["coef"] / rec["se"]
        if not np.isfinite(rec["p"]) and np.isfinite(rec["t"]):
            from scipy import stats
            rec["p"] = float(2 * stats.norm.sf(abs(rec["t"])))
        for c in ("first_stage_F", "bandwidth", "n_left", "n_right", "ar_p", "df", "n_clusters"):
            if c in r and pd.notna(r[c]):
                rec[c] = float(r[c])
        st = str(r["status"]) if "status" in r and pd.notna(r["status"]) else ("ok" if np.isfinite(rec["p"]) else "error")
        rec["status"] = "ok" if st.lower() in ("ok", "0", "success", "true") else st
        rec["psd_ok"] = bool(r["psd_ok"]) if "psd_ok" in r and pd.notna(r["psd_ok"]) else bool(np.isfinite(rec["se"]) and rec["se"] > 0)
        rec["df"] = int(rec.get("df", max(rec["n"] - 2, 1)))
        rec["ci_low"] = rec["coef"] - 1.96 * rec["se"]; rec["ci_high"] = rec["coef"] + 1.96 * rec["se"]
        rows.append(rec)
    led = pd.DataFrame(rows)
    if led.empty:
        raise ValueError("no row of the foreign ledger matched a key in the card's grid")
    led["abs_t"] = led["t"].abs()
    from . import inference
    led["p_dir"] = inference.one_sided_p(led["t"], led["p"], direction)
    led["sign_ok"] = True if direction is None else (np.sign(led["coef"]) == direction)
    return search.flag_pathologies(led, card)


def ingest_null(null_stats: pd.DataFrame, ledger: pd.DataFrame, card: dict, scheme="foreign", seed=0):
    """`null_stats` is long: draw, key, coef, t, p. Returns a NullDraws over the
    ledger's keys (columns in ledger order), so audit() lines up."""
    ns = _normalise_columns(null_stats.rename(columns={"draw": "draw"}))
    ns["draw"] = null_stats["draw"].to_numpy()
    ns["key"] = ns["key"].astype(str).str.strip()
    keys = ledger["key"].tolist()
    draws = sorted(ns["draw"].unique())
    idx = {k: j for j, k in enumerate(keys)}
    B, S = len(draws), len(keys)
    T = np.full((B, S), np.nan); C = T.copy(); P = T.copy()
    for b, dnum in enumerate(draws):
        sub = ns[ns["draw"] == dnum]
        for _, r in sub.iterrows():
            j = idx.get(r["key"])
            if j is None:
                continue
            T[b, j] = r.get("t", np.nan); C[b, j] = r.get("coef", np.nan); P[b, j] = r.get("p", np.nan)
    direction = grid.direction_sign(card)
    min_p = np.where(np.isfinite(P).any(axis=1),
                     np.nanmin(np.where(np.isfinite(P), P, np.nan), axis=1, initial=np.inf), np.nan)
    specs = {s.key(): s for s in grid.enumerate_specs(card)}
    nd = search.NullDraws(min_p=min_p, t=T, coef=C, p=P, specs=[specs[k] for k in keys],
                          scheme=scheme, seed=seed, direction=direction,
                          min_p_dir=search._min_p_dir(T, P, direction))
    return nd


def parity(run_dir, engine_ledger=None) -> dict:
    """Compare a foreign runner's ledger with the Python engine on the same
    specifications: max |delta coef|, max relative SE gap and max |delta p|
    by design axis, plus the share of keys that agree on significance."""
    meta = json.load(open(os.path.join(run_dir, "export.json")))
    card = grid.load_card(meta["card"])
    raw = _normalise_columns(pd.read_csv(os.path.join(run_dir, "ledger_raw.csv")))
    raw["key"] = raw["key"].astype(str).str.strip()
    ok = raw[raw.get("status", pd.Series("ok", index=raw.index)).astype(str).str.lower().eq("ok") & raw["coef"].notna()]
    by_key = {s.key(): s for s in grid.enumerate_specs(card)}
    specs = [by_key[k] for k in ok["key"] if k in by_key]
    eng = engine_ledger if engine_ledger is not None else search.run(
        pd.read_csv(os.path.join(run_dir, "data.csv")), card, specs=specs)
    m = ok.merge(eng[["key", "coef", "se", "p", "n", "vcov", "fe", "did_estimator", "rdd_inference",
                      "iv_estimator", "ev_estimand"]], on="key", suffixes=("_x", "_py"))
    if m.empty:
        return {"language": meta["lang"], "n_compared": 0}
    m["d_coef"] = (m["coef_x"] - m["coef_py"]).abs()
    m["rel_se"] = (m["se_x"] / m["se_py"] - 1).abs()
    m["d_p"] = (m["p_x"] - m["p_py"]).abs()
    m["same_sig"] = (m["p_x"] < 0.05) == (m["p_py"] < 0.05)
    grp = [c for c in ("vcov", "did_estimator", "rdd_inference", "iv_estimator") if c in m and m[c].astype(str).nunique() > 1]
    tab = (m.groupby(grp)[["d_coef", "rel_se", "d_p"]].max().round(5) if grp
           else m[["d_coef", "rel_se", "d_p"]].max().to_frame().T.round(5))
    return {"language": meta["lang"], "n_compared": int(len(m)),
            "n_unsupported": int((raw["status"].astype(str).str.startswith("unsupported")).sum()) if "status" in raw else 0,
            "n_error": int((raw["status"].astype(str).str.startswith("error")).sum()) if "status" in raw else 0,
            "max_abs_coef_gap": float(m["d_coef"].max()), "median_rel_se_gap": float(m["rel_se"].median()),
            "max_rel_se_gap": float(m["rel_se"].max()), "max_abs_p_gap": float(m["d_p"].max()),
            "share_same_significance": float(m["same_sig"].mean()),
            "by_axis": json.loads(tab.to_json(orient="index")),
            "worst_rows": m.sort_values("rel_se", ascending=False).head(5)[
                ["key", "coef_x", "coef_py", "se_x", "se_py", "p_x", "p_py"]].round(5).to_dict(orient="records")}


def ingest(run_dir, out_dir=None, alpha=0.05, with_parity=False):
    """Read export.json, ledger_raw.csv and null_stats.csv from a runner's
    directory; write ledger.csv, audit.json, report.md."""
    from . import report as _report
    meta = json.load(open(os.path.join(run_dir, "export.json")))
    card = grid.load_card(meta["card"])
    direction = grid.direction_sign(card)
    raw = pd.read_csv(os.path.join(run_dir, "ledger_raw.csv"))
    specs_tab = pd.read_csv(os.path.join(run_dir, "specs.csv"))
    led = ingest_ledger(raw, specs_tab, card, direction=direction)
    nd = None
    ns_path = os.path.join(run_dir, "null_stats.csv")
    if os.path.exists(ns_path):
        nd = ingest_null(pd.read_csv(ns_path), led, card, scheme=f"{meta['lang']}:{meta['null_scheme']}",
                         seed=meta.get("seed", 0))
    pre = grid.resolve_prereg(card)
    out_dir = out_dir or run_dir
    os.makedirs(out_dir, exist_ok=True)
    led.to_csv(os.path.join(out_dir, "ledger.csv"), index=False)
    if nd is not None:
        nd.save(out_dir)
    aud = search.audit(led, null=nd, preregistered_key=pre, alpha=alpha, direction=direction)
    aud["language"] = meta["lang"]
    aud["n_unsupported"] = int(led["status"].astype(str).str.startswith("unsupported").sum())
    man = search.manifest(card, pd.read_csv(os.path.join(run_dir, "data.csv")),
                          [s for s in grid.enumerate_specs(card) if s.key() in set(led["key"])],
                          data_path=meta.get("data_path"), null=nd, seed=meta.get("seed", 0),
                          extra={"language": meta["lang"], "runner": meta["runner"], "preregistered_key": pre})
    with open(os.path.join(out_dir, "audit.json"), "w") as fh:
        json.dump(aud, fh, indent=2, default=str)
    with open(os.path.join(out_dir, "manifest.json"), "w") as fh:
        json.dump(man, fh, indent=2, default=str)
    with open(os.path.join(out_dir, "report.md"), "w") as fh:
        fh.write(_report.honest_report(aud, man, card, title=f"Specification search ({meta['lang']}): honest report"))
    if with_parity:
        aud["parity"] = parity(run_dir)
        with open(os.path.join(out_dir, "parity.json"), "w") as fh:
            json.dump(aud["parity"], fh, indent=2, default=str)
    return aud


# ==========================================================================
# Templates. @@TOKENS@@ are filled by write_runner. Each runner:
#   reads specs.csv and data.csv, fits every row, writes ledger_raw.csv
#   (key,label,coef,se,t,p,n,status,first_stage_F,bandwidth,n_left,n_right);
#   with NULL_B > 0 reads null_columns.csv and writes null_stats.csv
#   (draw,key,coef,t,p).
# ==========================================================================

STATA = r'''* ---------------------------------------------------------------------------
* Generated by `phack export --lang stata`. Do not edit the grid here: edit
* the design card and re-export. Every row of specs.csv is one specification;
* this script estimates each with Stata's own commands and writes
* ledger_raw.csv in the schema `phack ingest` reads.
* Requires: reghdfe, ivreghdfe/ivreg2, rdrobust, did2s (ssc install ...).
* ---------------------------------------------------------------------------
clear all
set more off
set varabbrev off
capture set maxvar 32767
local NULL_B = @@NULL_B@@
local NULL_VARS "@@NULL_VARS@@"
local UNIT "@@UNIT@@"
local TIME "@@TIME@@"

* ---- helpers ---------------------------------------------------------------
capture program drop _phack_transform
program define _phack_transform
    * _phack_transform newvar sourcevar kind
    args new src kind
    quietly {
        if "`kind'" == "level"   gen double `new' = `src'
        else if "`kind'" == "log" {
            summarize `src', meanonly
            local shift = cond(r(min) <= 0, 1 - r(min), 0)
            gen double `new' = log(`src' + `shift')
        }
        else if "`kind'" == "log1p" gen double `new' = log(1 + max(`src', -0.999999))
        else if "`kind'" == "asinh" gen double `new' = asinh(`src')
        else if "`kind'" == "sqrt" {
            summarize `src', meanonly
            gen double `new' = sqrt(max(`src' - r(min), 0))
        }
        else if "`kind'" == "std" {
            summarize `src'
            gen double `new' = (`src' - r(mean)) / r(sd)
        }
        else if "`kind'" == "rank" {
            egen double `new' = rank(`src')
            count if !missing(`src')
            replace `new' = `new' / r(N)
        }
        else if "`kind'" == "inv"    gen double `new' = cond(abs(`src') < 1e-9, ., 1 / `src')
        else if "`kind'" == "square" gen double `new' = `src'^2
        else if inlist("`kind'", "winsor1", "winsor5") {
            local q = cond("`kind'" == "winsor1", 1, 5)
            _pctile `src', percentiles(`q' `=100-`q'')
            gen double `new' = max(min(`src', r(r2)), r(r1))
        }
        else if "`kind'" == "median_split" {
            _pctile `src', percentiles(50)
            gen double `new' = (`src' > r(r1)) if !missing(`src')
        }
        else if "`kind'" == "above_mean" {
            summarize `src', meanonly
            gen double `new' = (`src' > r(mean)) if !missing(`src')
        }
        else if "`kind'" == "quartile_top" {
            _pctile `src', percentiles(75)
            gen double `new' = (`src' >= r(r1)) if !missing(`src')
        }
        else if "`kind'" == "tercile_extremes" {
            _pctile `src', percentiles(33.3333333 66.6666667)
            gen double `new' = .
            replace `new' = 0 if `src' <= r(r1)
            replace `new' = 1 if `src' >= r(r2)
        }
        else {
            display as error "unknown transform `kind'"
            exit 198
        }
    }
end

capture program drop _phack_outlier
program define _phack_outlier
    * _phack_outlier flagvar basisvar rule   (flag = 1 -> drop)
    args flag src rule
    quietly {
        gen byte `flag' = 0
        if "`rule'" == "none" exit
        if substr("`rule'", 1, 2) == "sd" {
            local k = real(substr("`rule'", 3, .))
            summarize `src'
            replace `flag' = abs(`src' - r(mean)) > `k' * r(sd) & !missing(`src')
        }
        else if substr("`rule'", 1, 3) == "iqr" {
            local k = real(substr("`rule'", 4, .))
            _pctile `src', percentiles(25 75)
            local iqr = r(r2) - r(r1)
            replace `flag' = (`src' < r(r1) - `k' * `iqr' | `src' > r(r2) + `k' * `iqr') & !missing(`src')
        }
        else if "`rule'" == "mad3" {
            _pctile `src', percentiles(50)
            local med = r(r1)
            tempvar ad
            gen double `ad' = abs(`src' - `med')
            _pctile `ad', percentiles(50)
            local mad = r(r1) * 1.4826
            if `mad' == 0 local mad = 1
            replace `flag' = abs(`src' - `med') > 3 * `mad' & !missing(`src')
        }
        else if inlist("`rule'", "pct1", "pct5") {
            local q = cond("`rule'" == "pct1", 1, 5)
            _pctile `src', percentiles(`q' `=100-`q'')
            replace `flag' = (`src' < r(r1) | `src' > r(r2)) & !missing(`src')
        }
        else {
            display as error "unknown outlier rule `rule'"
            exit 198
        }
    }
end

capture program drop _phack_impute
program define _phack_impute
    args var method
    quietly {
        if "`method'" == "listwise" exit
        count if missing(`var')
        if r(N) == 0 exit
        if "`method'" == "mean" {
            summarize `var', meanonly
            replace `var' = r(mean) if missing(`var')
        }
        else if "`method'" == "median" {
            _pctile `var', percentiles(50)
            replace `var' = r(r1) if missing(`var')
        }
        else if "`method'" == "zero" replace `var' = 0 if missing(`var')
        else if "`method'" == "ffill" {
            if "$phack_unit" != "" {
                bysort $phack_unit ($phack_time): replace `var' = `var'[_n-1] if missing(`var')
                gsort $phack_unit -$phack_time
                by $phack_unit: replace `var' = `var'[_n-1] if missing(`var')
                sort $phack_unit $phack_time
            }
            else {
                replace `var' = `var'[_n-1] if missing(`var')
            }
        }
        else {
            display as error "imputation `method' not supported in the Stata runner"
            exit 198
        }
    }
end

* Fit one specification; everything about it is in globals s_*; results in r()
capture program drop _phack_fit
program define _phack_fit, rclass
    quietly {
        * ---- sample
        if `"$s_subsample"' != "" keep if $s_subsample
        if "$s_comparison_group" == "drop_never_treated" {
            egen double _ever = max($s_treatment), by($phack_unit)
            keep if _ever > 0
        }
        if "$s_comparison_group" == "drop_always_treated" {
            egen double _always = min($s_treatment), by($phack_unit)
            keep if _always < 1
        }
        * ---- imputation
        foreach v in $s_outcome $s_treatment $s_controls $s_instruments {
            _phack_impute `v' $s_imputation
        }
        * ---- lag
        if $s_lag > 0 {
            xtset $phack_unit $phack_time
            gen double _dlag = L$s_lag.$s_treatment
            replace $s_treatment = _dlag
        }
        * ---- transforms
        if "$s_design" == "rdd" {
            gen double _D = ($s_running >= $s_cutoff)
            _phack_transform _y $s_outcome $s_y_transform
            gen double _d = _D
        }
        else {
            _phack_transform _y $s_outcome $s_y_transform
            _phack_transform _d $s_treatment $s_d_transform
        }
        local need "_y _d $s_controls $s_instruments $s_cluster1 $s_cluster2 $s_weight $s_fe"
        if "$s_design" == "rdd" local need "`need' $s_running"
        foreach v of local need {
            drop if missing(`v')
        }
        * ---- outliers
        if "$s_outlier_rule" != "none" {
            if "$s_outlier_basis" == "residual" {
                regress _y _d $s_controls
                predict double _rst, rstudent
                _phack_outlier _flag _rst $s_outlier_rule
            }
            else if "$s_outlier_basis" == "treatment" _phack_outlier _flag _d $s_outlier_rule
            else _phack_outlier _flag _y $s_outlier_rule
            drop if _flag
        }
        * ---- weights and vce
        local wt ""
        if "$s_weight" != "" local wt "[aw=$s_weight]"
        local vce ""
        if "$s_vcov" == "hc1" local vce "vce(robust)"
        else if inlist("$s_vcov", "hc0", "hc2", "hc3") local vce "vce($s_vcov)"
        else if "$s_vcov" == "cluster" local vce "vce(cluster $s_cluster1)"
        else if "$s_vcov" == "twoway" local vce "vce(cluster $s_cluster1 $s_cluster2)"
        local target "_d"
        return local status "ok"
        * ---- estimation by design
        if "$s_design" == "rdd" {
            local vcer "vce(hc1)"
            if "$s_vcov" == "cluster" local vcer "vce(cluster $s_cluster1)"
            local covs ""
            if "$s_controls" != "" local covs "covs($s_controls)"
            rdrobust _y $s_running if abs($s_running - $s_cutoff) > $s_donut, c($s_cutoff) ///
                h($s_bw_abs) kernel($s_kernel) p($s_poly) `covs' `vcer'
            if "$s_rdd_inference" == "conventional" {
                return scalar coef = e(tau_cl)
                return scalar se = e(se_tau_cl)
                return scalar p = e(pv_cl)
            }
            else if "$s_rdd_inference" == "robust" {
                return scalar coef = e(tau_bc)
                return scalar se = e(se_tau_rb)
                return scalar p = e(pv_rb)
            }
            else {
                return scalar coef = e(tau_bc)
                return scalar se = e(se_tau_cl)
                return scalar p = 2 * normal(-abs(e(tau_bc) / e(se_tau_cl)))
            }
            return scalar t = return(coef) / return(se)
            return scalar n = e(N_h_l) + e(N_h_r)
            return scalar n_left = e(N_h_l)
            return scalar n_right = e(N_h_r)
            return scalar bandwidth = e(h_l)
            exit
        }
        if "$s_design" == "iv" {
            local vcei "robust"
            if "$s_vcov" == "cluster" local vcei "cluster($s_cluster1)"
            if "$s_vcov" == "iid" local vcei ""
            local liml ""
            if "$s_iv_estimator" == "liml" local liml "liml"
            if "$s_fe" != "" {
                ivreghdfe _y $s_controls (_d = $s_instruments) `wt', absorb($s_fe) `vcei' `liml'
            }
            else {
                ivreg2 _y $s_controls (_d = $s_instruments) `wt', `vcei' `liml'
            }
            return scalar first_stage_F = cond(missing(e(widstat)), e(rkf), e(widstat))
        }
        else if "$s_did_estimator" == "did2s" {
            did2s _y `wt', first_stage(i.$phack_unit i.$phack_time $s_controls) ///
                second_stage(_d) treatment(_d) cluster($s_cluster1)
        }
        else if "$s_did_estimator" == "stacked" {
            return local status "unsupported: stacked DiD (use the Python engine or StatsPAI runner)"
            exit
        }
        else if "$s_ev_estimand" != "" {
            * event study: relative time, binned endpoints, omitted reference period
            egen double _first = min(cond($s_treatment > 0, $phack_time, .)), by($phack_unit)
            gen double _rel = $phack_time - _first
            replace _rel = -$s_ev_pre if _rel < -$s_ev_pre & !missing(_rel)
            replace _rel = $s_ev_post if _rel > $s_ev_post & !missing(_rel)
            local dums ""
            local post ""
            local pre ""
            forvalues r = -$s_ev_pre / $s_ev_post {
                if `r' == $s_ev_ref continue
                local nm = cond(`r' < 0, "_rm" + string(-`r'), "_rp" + string(`r'))
                gen byte `nm' = (_rel == `r') if !missing(_rel)
                replace `nm' = 0 if missing(_rel)
                local dums "`dums' `nm'"
                if `r' >= 0 local post "`post' `nm'"
                else local pre "`pre' `nm'"
            }
            if "$s_fe" != "" reghdfe _y `dums' $s_controls `wt', absorb($s_fe) `vce'
            else regress _y `dums' $s_controls `wt', `vce'
            local expr ""
            if "$s_ev_estimand" == "avg_post" local set "`post'"
            else if "$s_ev_estimand" == "avg_pre" local set "`pre'"
            else local set = "_rp" + substr("$s_ev_estimand", 4, .)
            local k : word count `set'
            foreach v of local set {
                if "`expr'" == "" local expr "`v'"
                else local expr "`expr' + `v'"
            }
            lincom (`expr') / `k'
            return scalar coef = r(estimate)
            return scalar se = r(se)
            return scalar t = r(estimate) / r(se)
            return scalar p = r(p)
            return scalar n = e(N)
            exit
        }
        else {
            if "$s_fe" != "" reghdfe _y _d $s_controls `wt', absorb($s_fe) `vce'
            else regress _y _d $s_controls `wt', `vce'
        }
        matrix _T = r(table)
        return scalar coef = _b[_d]
        return scalar se = _se[_d]
        return scalar t = _b[_d] / _se[_d]
        return scalar p = _T[rownumb(_T, "pvalue"), colnumb(_T, "_d")]
        return scalar n = e(N)
    }
end

* ---- main -------------------------------------------------------------------
import delimited using "data.csv", clear case(preserve)
gen long __row = _n - 1
tempfile data
save `data'

import delimited using "specs.csv", clear case(preserve) stringcols(_all)
local S = _N
frame put *, into(specs)

global phack_unit "`UNIT'"
global phack_time "`TIME'"

capture file close led
file open led using "ledger_raw.csv", write replace
file write led "key,label,coef,se,t,p,n,status,first_stage_F,bandwidth,n_left,n_right" _n

capture program drop _phack_load_spec
program define _phack_load_spec
    args i
    foreach v in key label outcome treatment controls fe vcov cluster1 cluster2 y_transform d_transform ///
        outlier_rule outlier_basis imputation subsample weight lag did_estimator comparison_group ///
        ev_pre ev_post ev_ref ev_estimand bw_abs kernel poly donut rdd_inference instruments ///
        iv_estimator running cutoff design {
        frame specs: local x = `v'[`i']
        global s_`v' `"`x'"'
    }
    if "$s_lag" == "" global s_lag 0
end

forvalues i = 1/`S' {
    _phack_load_spec `i'
    use `data', clear
    capture noisily _phack_fit
    local rc = _rc
    if `rc' == 0 & "`r(status)'" == "ok" {
        file write led `"$s_key,"$s_label",`r(coef)',`r(se)',`r(t)',`r(p)',`r(n)',ok,`r(first_stage_F)',`r(bandwidth)',`r(n_left)',`r(n_right)'"' _n
    }
    else if `rc' == 0 {
        file write led `"$s_key,"$s_label",.,.,.,.,0,"`r(status)'",.,.,.,."' _n
    }
    else {
        file write led `"$s_key,"$s_label",.,.,.,.,0,"error: r(`rc')",.,.,.,."' _n
    }
    if mod(`i', 50) == 0 display "  `i' / `S' specifications"
}
file close led
display "ledger_raw.csv written (`S' specifications)"

* ---- null replay ------------------------------------------------------------
if `NULL_B' > 0 {
    import delimited using "null_columns.csv", clear case(preserve)
    tempfile nulls
    save `nulls'
    capture file close nul
    file open nul using "null_stats.csv", write replace
    file write nul "draw,key,coef,t,p" _n
    forvalues b = 1/`NULL_B' {
        forvalues i = 1/`S' {
            _phack_load_spec `i'
            use `data', clear
            merge 1:1 __row using `nulls', nogenerate keepusing(*__`b')
            foreach v of local NULL_VARS {
                replace `v' = `v'__`b'
            }
            capture noisily _phack_fit
            if _rc == 0 & "`r(status)'" == "ok" {
                file write nul `"`b',$s_key,`r(coef)',`r(t)',`r(p)'"' _n
            }
        }
        display "  null draw `b' / `NULL_B'"
    }
    file close nul
    display "null_stats.csv written"
}
'''

R = r'''# ---------------------------------------------------------------------------
# Generated by `phack export --lang r`. Do not edit the grid here: edit the
# design card and re-export. Every row of specs.csv is one specification;
# this script estimates each with fixest / rdrobust / did2s and writes
# ledger_raw.csv in the schema `phack ingest` reads.
# ---------------------------------------------------------------------------
suppressPackageStartupMessages({
  library(fixest); library(data.table)
  has_rd <- requireNamespace("rdrobust", quietly = TRUE)
  has_did2s <- requireNamespace("did2s", quietly = TRUE)
})
NULL_B <- @@NULL_B@@
NULL_VARS <- @@NULL_VARS_R@@
UNIT <- "@@UNIT@@"; TIME <- "@@TIME@@"

data0 <- fread("data.csv"); data0[, `__row` := .I - 1L]
specs <- fread("specs.csv", colClasses = "character")
S <- nrow(specs)

num <- function(x, default = NA_real_) { v <- suppressWarnings(as.numeric(x)); ifelse(is.na(v), default, v) }
sp_words <- function(x) { x <- trimws(x); if (is.na(x) || x == "") character(0) else strsplit(x, " +")[[1]] }

transform_var <- function(x, kind) {
  switch(kind,
    level = x,
    log = { m <- min(x, na.rm = TRUE); log(x + ifelse(m <= 0, 1 - m, 0)) },
    log1p = log1p(pmax(x, -0.999999)),
    asinh = asinh(x),
    sqrt = sqrt(pmax(x - min(x, na.rm = TRUE), 0)),
    std = (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE),
    rank = rank(x, na.last = "keep") / sum(!is.na(x)),
    inv = ifelse(abs(x) < 1e-9, NA_real_, 1 / x),
    square = x^2,
    winsor1 = { q <- quantile(x, c(.01, .99), na.rm = TRUE); pmin(pmax(x, q[1]), q[2]) },
    winsor5 = { q <- quantile(x, c(.05, .95), na.rm = TRUE); pmin(pmax(x, q[1]), q[2]) },
    median_split = as.numeric(x > median(x, na.rm = TRUE)),
    above_mean = as.numeric(x > mean(x, na.rm = TRUE)),
    quartile_top = as.numeric(x >= quantile(x, .75, na.rm = TRUE)),
    tercile_extremes = { q <- quantile(x, c(1/3, 2/3), na.rm = TRUE)
      ifelse(x <= q[1], 0, ifelse(x >= q[2], 1, NA_real_)) },
    stop("unknown transform ", kind))
}

outlier_flag <- function(x, rule) {
  if (rule == "none") return(rep(FALSE, length(x)))
  if (startsWith(rule, "sd")) { k <- as.numeric(substring(rule, 3)); return(abs(x - mean(x, na.rm = TRUE)) > k * sd(x, na.rm = TRUE)) }
  if (startsWith(rule, "iqr")) { k <- as.numeric(substring(rule, 4)); q <- quantile(x, c(.25, .75), na.rm = TRUE); i <- q[2] - q[1]
    return(x < q[1] - k * i | x > q[2] + k * i) }
  if (rule == "mad3") { m <- median(x, na.rm = TRUE); md <- median(abs(x - m), na.rm = TRUE) * 1.4826; if (md == 0) md <- 1
    return(abs(x - m) > 3 * md) }
  if (rule %in% c("pct1", "pct5")) { q <- if (rule == "pct1") c(.01, .99) else c(.05, .95); qq <- quantile(x, q, na.rm = TRUE)
    return(x < qq[1] | x > qq[2]) }
  stop("unknown outlier rule ", rule)
}

impute <- function(v, method, d) {
  if (method == "listwise" || !anyNA(v)) return(v)
  if (method == "mean") { v[is.na(v)] <- mean(v, na.rm = TRUE); return(v) }
  if (method == "median") { v[is.na(v)] <- median(v, na.rm = TRUE); return(v) }
  if (method == "zero") { v[is.na(v)] <- 0; return(v) }
  if (method == "ffill") { return(data.table::nafill(data.table::nafill(v, "locf"), "nocb")) }
  stop("imputation ", method, " not supported in the R runner")
}

fit_one <- function(s, d) {
  res <- list(coef = NA, se = NA, t = NA, p = NA, n = 0, status = "ok",
              first_stage_F = NA, bandwidth = NA, n_left = NA, n_right = NA)
  d <- copy(d)
  if (s$subsample != "") d <- d[eval(parse(text = s$subsample))]
  if (s$comparison_group == "drop_never_treated") { d[, phk_ever := max(get(s$treatment)), by = c(UNIT)]; kr <- d$phk_ever > 0; d <- d[kr] }
  if (s$comparison_group == "drop_always_treated") { d[, phk_alw := min(get(s$treatment)), by = c(UNIT)]; kr <- d$phk_alw < 1; d <- d[kr] }
  ctl <- sp_words(s$controls); fe <- sp_words(s$fe); z <- sp_words(s$instruments)
  for (v in unique(c(s$outcome, s$treatment, ctl, z))) if (v %in% names(d)) set(d, j = v, value = impute(d[[v]], s$imputation, d))
  lag <- as.integer(num(s$lag, 0))
  if (lag > 0) { setorderv(d, c(UNIT, TIME)); d[, (s$treatment) := shift(get(s$treatment), lag), by = c(UNIT)] }
  if (s$design == "rdd") {
    d[, phk_d := as.numeric(get(s$running) >= num(s$cutoff, 0))]
  } else d[, phk_d := transform_var(get(s$treatment), s$d_transform)]
  d[, phk_y := transform_var(get(s$outcome), s$y_transform)]
  need <- unique(c("phk_y", "phk_d", ctl, z, fe, s$cluster1, s$cluster2, s$weight, if (s$design == "rdd") s$running))
  need <- need[need != ""]
  cc <- complete.cases(d[, need, with = FALSE])   # computed outside `[`: a column named `d` would shadow the table
  d <- d[cc]
  if (s$outlier_rule != "none") {
    basis <- if (s$outlier_basis == "residual") {
      f <- as.formula(paste("phk_y ~ phk_d", if (length(ctl)) paste("+", paste(ctl, collapse = "+")) else ""))
      m <- lm(f, d); rstudent(m)
    } else if (s$outlier_basis == "treatment") d$phk_d else d$phk_y
    keep_rows <- !outlier_flag(basis, s$outlier_rule)
    d <- d[keep_rows]
  }
  wts <- if (s$weight != "") as.formula(paste0("~", s$weight)) else NULL
  vc <- switch(s$vcov, iid = "iid", hc0 = "hetero", hc1 = "hetero", hc2 = "hetero", hc3 = "hetero",
               cluster = as.formula(paste0("~", s$cluster1)),
               twoway = as.formula(paste0("~", s$cluster1, "+", s$cluster2)))
  ctl_txt <- if (length(ctl)) paste("+", paste(ctl, collapse = " + ")) else ""
  fe_txt <- if (length(fe)) paste("|", paste(fe, collapse = " + ")) else ""
  if (s$design == "rdd") {
    if (!has_rd) { res$status <- "unsupported: rdrobust not installed"; return(res) }
    kr <- abs(d[[s$running]] - num(s$cutoff, 0)) > num(s$donut, 0); dd <- d[kr]
    covs <- if (length(ctl)) as.matrix(dd[, ctl, with = FALSE]) else NULL
    cl <- if (s$vcov == "cluster") dd[[s$cluster1]] else NULL
    m <- rdrobust::rdrobust(dd$phk_y, dd[[s$running]], c = num(s$cutoff, 0), h = num(s$bw_abs),
                            kernel = s$kernel, p = as.integer(num(s$poly, 1)), covs = covs,
                            vce = if (is.null(cl)) "hc1" else "hc1", cluster = cl)
    row <- switch(s$rdd_inference, conventional = 1, bias_corrected = 2, robust = 3)
    res$coef <- m$coef[row]; res$se <- if (row == 2) m$se[1] else m$se[row]
    res$t <- res$coef / res$se
    res$p <- if (row == 2) 2 * pnorm(-abs(res$t)) else m$pv[row]
    res$n <- sum(m$N_h); res$n_left <- m$N_h[1]; res$n_right <- m$N_h[2]; res$bandwidth <- m$bws[1, 1]
    return(res)
  }
  if (s$design == "iv") {
    if (s$iv_estimator == "liml") { res$status <- "unsupported: LIML (fixest has no LIML; use ivmodel or the Python engine)"; return(res) }
    f <- as.formula(paste("phk_y ~ 1", ctl_txt, if (length(fe)) fe_txt else "| 0", "| phk_d ~", paste(z, collapse = " + ")))
    m <- feols(f, d, vcov = vc, weights = wts)
    res$first_stage_F <- tryCatch(fitstat(m, "ivf")[[1]]$stat, error = function(e) NA)
    cf <- coef(m)["fit_phk_d"]; se <- se(m)["fit_phk_d"]; pv <- pvalue(m)["fit_phk_d"]
    res$coef <- cf; res$se <- se; res$t <- cf / se; res$p <- pv; res$n <- nobs(m)
    return(res)
  }
  if (s$did_estimator == "did2s") {
    if (!has_did2s) { res$status <- "unsupported: did2s not installed"; return(res) }
    ff <- as.formula(paste("~ 0", ctl_txt, "|", UNIT, "+", TIME))
    m <- did2s::did2s(as.data.frame(d), yname = "phk_y", first_stage = ff, second_stage = ~ phk_d,
                      treatment = "phk_d", cluster_var = if (s$cluster1 != "") s$cluster1 else UNIT, verbose = FALSE)
    cf <- coef(m)[1]; se <- se(m)[1]
    res$coef <- cf; res$se <- se; res$t <- cf / se; res$p <- 2 * pnorm(-abs(cf / se)); res$n <- nobs(m)
    return(res)
  }
  if (s$did_estimator == "stacked") { res$status <- "unsupported: stacked DiD (use the Python engine or StatsPAI runner)"; return(res) }
  if (s$ev_estimand != "") {
    pre <- as.integer(num(s$ev_pre)); post <- as.integer(num(s$ev_post)); ref <- as.integer(num(s$ev_ref))
    d[, phk_first := { tt <- get(TIME)[get(s$treatment) > 0]; if (length(tt)) min(tt) else NA_real_ }, by = c(UNIT)]
    d[, phk_rel := pmin(pmax(get(TIME) - phk_first, -pre), post)]
    d[is.na(phk_rel), phk_rel := -1000]
    f <- as.formula(paste("phk_y ~ i(phk_rel, ref = c(", ref, ", -1000))", ctl_txt, fe_txt))
    m <- feols(f, d, vcov = vc, weights = wts)
    nm <- names(coef(m)); rel <- as.numeric(sub("phk_rel::", "", nm[startsWith(nm, "phk_rel::")]))
    sel <- switch(substr(s$ev_estimand, 1, 3), avg = if (s$ev_estimand == "avg_post") rel >= 0 else rel < 0,
                  lag = rel == as.numeric(substring(s$ev_estimand, 4)))
    a <- rep(0, length(nm)); a[startsWith(nm, "phk_rel::")][sel] <- 1 / sum(sel)
    cf <- sum(a * coef(m)); se <- sqrt(as.numeric(t(a) %*% vcov(m) %*% a))
    res$coef <- cf; res$se <- se; res$t <- cf / se; res$p <- 2 * pt(-abs(cf / se), df = degrees_freedom(m, "t")); res$n <- nobs(m)
    return(res)
  }
  f <- as.formula(paste("phk_y ~ phk_d", ctl_txt, fe_txt))
  m <- feols(f, d, vcov = vc, weights = wts)
  cf <- coef(m)["phk_d"]; se <- se(m)["phk_d"]; pv <- pvalue(m)["phk_d"]
  res$coef <- cf; res$se <- se; res$t <- cf / se; res$p <- pv; res$n <- nobs(m)
  res
}

safe_fit <- function(s, d) tryCatch(fit_one(s, d), error = function(e) list(coef = NA, se = NA, t = NA, p = NA, n = 0,
  status = paste0("error: ", conditionMessage(e), " [in ", paste(deparse(conditionCall(e))[1], collapse = ""), "]"),
  first_stage_F = NA, bandwidth = NA, n_left = NA, n_right = NA))

rows <- vector("list", S)
for (i in seq_len(S)) {
  s <- as.list(specs[i]); r <- safe_fit(s, data0)
  rows[[i]] <- data.table(k = s$key, label = s$label, coef = as.numeric(r$coef), se = as.numeric(r$se),
                          t = as.numeric(r$t), p = as.numeric(r$p), n = as.numeric(r$n),
                          status = r$status, first_stage_F = as.numeric(r$first_stage_F), bandwidth = as.numeric(r$bandwidth),
                          n_left = as.numeric(r$n_left), n_right = as.numeric(r$n_right))
  setnames(rows[[i]], "k", "key")
  if (i %% 50 == 0) cat("  ", i, "/", S, "specifications\n")
}
fwrite(rbindlist(rows), "ledger_raw.csv")
cat("ledger_raw.csv written (", S, "specifications )\n")

if (NULL_B > 0) {
  nulls <- fread("null_columns.csv")
  out <- list()
  for (b in seq_len(NULL_B)) {
    d <- copy(data0)
    for (v in NULL_VARS) set(d, j = v, value = nulls[[paste0(v, "__", b)]])
    for (i in seq_len(S)) {
      s <- as.list(specs[i]); r <- safe_fit(s, d)
      if (r$status == "ok") { o <- data.table(draw = b, k = s$key, coef = as.numeric(r$coef), t = as.numeric(r$t), p = as.numeric(r$p)); setnames(o, "k", "key"); out[[length(out) + 1]] <- o }
    }
    cat("  null draw", b, "/", NULL_B, "\n")
  }
  fwrite(rbindlist(out), "null_stats.csv")
  cat("null_stats.csv written\n")
}
'''

PYTHON = r'''#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Generated by `phack export --lang python`. Estimates every row of specs.csv
# with statsmodels / linearmodels -- the stack a Python analyst would reach
# for -- and writes ledger_raw.csv in the schema `phack ingest` reads.
# Requires: pandas, numpy, scipy, statsmodels; linearmodels for IV.
# ---------------------------------------------------------------------------
import json, sys, warnings
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
warnings.filterwarnings("ignore")          # non-PSD corners produce sqrt warnings; the ledger records them as NaN SEs

NULL_B = @@NULL_B@@
NULL_VARS = @@NULL_VARS_PY@@
UNIT, TIME = "@@UNIT@@", "@@TIME@@"

data0 = pd.read_csv("data.csv"); data0["__row"] = np.arange(len(data0))
specs = pd.read_csv("specs.csv", dtype=str).fillna("")

def words(x): return [w for w in str(x).split() if w]
def num(x, default=np.nan):
    try: return float(x)
    except (TypeError, ValueError): return default

def transform(x, kind):
    x = np.asarray(x, float)
    if kind == "level": return x
    if kind == "log":
        m = np.nanmin(x); return np.log(x + (1 - m if m <= 0 else 0.0))
    if kind == "log1p": return np.log1p(np.clip(x, -0.999999, None))
    if kind == "asinh": return np.arcsinh(x)
    if kind == "sqrt": return np.sqrt(np.clip(x - np.nanmin(x), 0, None))
    if kind == "std": return (x - np.nanmean(x)) / np.nanstd(x, ddof=1)
    if kind == "rank": return stats.rankdata(x, nan_policy="omit") / np.sum(np.isfinite(x))
    if kind == "inv": return 1.0 / np.where(np.abs(x) < 1e-9, np.nan, x)
    if kind == "square": return x ** 2
    if kind in ("winsor1", "winsor5"):
        q = 1 if kind == "winsor1" else 5; return np.clip(x, np.nanpercentile(x, q), np.nanpercentile(x, 100 - q))
    if kind == "median_split": return (x > np.nanmedian(x)).astype(float)
    if kind == "above_mean": return (x > np.nanmean(x)).astype(float)
    if kind == "quartile_top": return (x >= np.nanpercentile(x, 75)).astype(float)
    if kind == "tercile_extremes":
        lo, hi = np.nanpercentile(x, [100 / 3, 200 / 3]); out = np.full(x.shape, np.nan)
        out[x <= lo] = 0; out[x >= hi] = 1; return out
    raise KeyError(kind)

def outlier_flag(x, rule):
    x = np.asarray(x, float)
    if rule == "none": return np.zeros(x.size, bool)
    if rule.startswith("sd"): k = float(rule[2:]); return np.abs(x - np.nanmean(x)) > k * np.nanstd(x, ddof=1)
    if rule.startswith("iqr"):
        k = float(rule[3:]); q1, q3 = np.nanpercentile(x, [25, 75]); i = q3 - q1
        return (x < q1 - k * i) | (x > q3 + k * i)
    if rule == "mad3":
        m = np.nanmedian(x); md = np.nanmedian(np.abs(x - m)) * 1.4826 or 1.0; return np.abs(x - m) > 3 * md
    if rule in ("pct1", "pct5"):
        q = 1 if rule == "pct1" else 5; return (x < np.nanpercentile(x, q)) | (x > np.nanpercentile(x, 100 - q))
    raise KeyError(rule)

def impute(s, method):
    if method == "listwise" or not s.isna().any(): return s
    if method == "mean": return s.fillna(s.mean())
    if method == "median": return s.fillna(s.median())
    if method == "zero": return s.fillna(0.0)
    if method == "ffill": return s.ffill().bfill()
    raise KeyError(method)

def _cov_kw(s, d):
    if s["vcov"] == "iid": return {}
    if s["vcov"] in ("hc0", "hc1", "hc2", "hc3"): return {"cov_type": s["vcov"].upper()}
    if s["vcov"] == "cluster": return {"cov_type": "cluster", "cov_kwds": {"groups": pd.factorize(d[s["cluster1"]])[0]}}
    if s["vcov"] == "twoway":
        g = np.column_stack([pd.factorize(d[s["cluster1"]])[0], pd.factorize(d[s["cluster2"]])[0]])
        return {"cov_type": "cluster", "cov_kwds": {"groups": g}}
    raise KeyError(s["vcov"])

def _design(d, s, ctl):
    X = pd.DataFrame({"_d": d["_d"].to_numpy(float)}, index=d.index)
    for c in ctl: X[c] = d[c].to_numpy(float)
    fe = words(s["fe"])
    if fe:
        for f in fe: X = pd.concat([X, pd.get_dummies(d[f].astype(str), prefix=f, drop_first=True, dtype=float)], axis=1)
    X = sm.add_constant(X, has_constant="add")
    return X

def fit_one(s, d):
    res = dict(coef=np.nan, se=np.nan, t=np.nan, p=np.nan, n=0, status="ok", first_stage_F=np.nan,
               bandwidth=np.nan, n_left=np.nan, n_right=np.nan)
    d = d.copy()
    if s["subsample"]: d = d.query(s["subsample"].replace("&", " and ").replace("|", " or "))
    if s["comparison_group"] == "drop_never_treated": d = d[d.groupby(UNIT)[s["treatment"]].transform("max") > 0]
    if s["comparison_group"] == "drop_always_treated": d = d[d.groupby(UNIT)[s["treatment"]].transform("min") < 1]
    ctl, z = words(s["controls"]), words(s["instruments"])
    for v in dict.fromkeys([s["outcome"], s["treatment"], *ctl, *z]):
        if v in d: d[v] = impute(d[v], s["imputation"])
    lag = int(num(s["lag"], 0))
    if lag: d = d.sort_values([UNIT, TIME]); d[s["treatment"]] = d.groupby(UNIT)[s["treatment"]].shift(lag)
    if s["design"] == "rdd": d["_d"] = (d[s["running"]] >= num(s["cutoff"], 0)).astype(float)
    else: d["_d"] = transform(d[s["treatment"]], s["d_transform"])
    d["_y"] = transform(d[s["outcome"]], s["y_transform"])
    need = [c for c in dict.fromkeys(["_y", "_d", *ctl, *z, *words(s["fe"]), s["cluster1"], s["cluster2"], s["weight"],
                                      s["running"] if s["design"] == "rdd" else ""]) if c]
    d = d.dropna(subset=need)
    if s["outlier_rule"] != "none":
        if s["outlier_basis"] == "residual":
            m = sm.OLS(d["_y"], sm.add_constant(d[["_d", *ctl]])).fit(); basis = m.get_influence().resid_studentized_internal
        else: basis = d["_d"] if s["outlier_basis"] == "treatment" else d["_y"]
        d = d[~outlier_flag(basis, s["outlier_rule"])]
    w = d[s["weight"]].to_numpy(float) if s["weight"] else None
    if s["design"] == "rdd":
        x = d[s["running"]].to_numpy(float) - num(s["cutoff"], 0); h = num(s["bw_abs"]); donut = num(s["donut"], 0)
        keep = (np.abs(x) <= h) & (np.abs(x) > donut); x = x[keep]; y = d["_y"].to_numpy(float)[keep]
        D = (x >= 0).astype(float)
        def lp(p):
            cols = [np.ones(x.size), D] + [c for k in range(1, p + 1) for c in (x ** k, D * x ** k)]
            cols += [d[c].to_numpy(float)[keep] for c in ctl]
            X = np.column_stack(cols)
            kern = {"triangular": lambda u: np.clip(1 - np.abs(u), 0, None), "uniform": lambda u: (np.abs(u) <= 1) * 1.0,
                    "epanechnikov": lambda u: np.clip(.75 * (1 - u ** 2), 0, None)}[s["kernel"]](x / h)
            kw = {"cov_type": "HC1"} if s["vcov"] != "cluster" else {"cov_type": "cluster", "cov_kwds": {"groups": pd.factorize(d[s["cluster1"]][keep])[0]}}
            return sm.WLS(y, X, weights=kern).fit(**kw)
        p = int(num(s["poly"], 1)); m0 = lp(p)
        if s["rdd_inference"] == "conventional": cf, se = m0.params[1], m0.bse[1]
        else:
            m1 = lp(p + 1); cf = m1.params[1]; se = m1.bse[1] if s["rdd_inference"] == "robust" else m0.bse[1]
        res.update(coef=cf, se=se, t=cf / se, p=2 * stats.t.sf(abs(cf / se), m0.df_resid), n=int(x.size),
                   n_left=int((D == 0).sum()), n_right=int(D.sum()), bandwidth=h)
        return res
    if s["design"] == "iv":
        from linearmodels.iv import IV2SLS, IVLIML
        fe = words(s["fe"])
        exog = sm.add_constant(pd.DataFrame({c: d[c].to_numpy(float) for c in ctl}, index=d.index), has_constant="add")
        for f in fe: exog = pd.concat([exog, pd.get_dummies(d[f].astype(str), prefix=f, drop_first=True, dtype=float)], axis=1)
        cls_ = IVLIML if s["iv_estimator"] == "liml" else IV2SLS
        mod = cls_(d["_y"], exog, d[["_d"]], d[z], weights=w)
        kw = {"cov_type": "robust"} if s["vcov"] in ("hc0", "hc1") else ({"cov_type": "unadjusted"} if s["vcov"] == "iid"
              else {"cov_type": "clustered", "clusters": d[s["cluster1"]]})
        m = mod.fit(**kw)
        res.update(coef=float(m.params["_d"]), se=float(m.std_errors["_d"]), t=float(m.tstats["_d"]),
                   p=float(m.pvalues["_d"]), n=int(m.nobs))
        try: res["first_stage_F"] = float(m.first_stage.diagnostics.loc["_d", "f.stat"])
        except Exception: pass
        return res
    if s["did_estimator"] in ("did2s", "stacked") or s["ev_estimand"]:
        res["status"] = "unsupported: %s (use the phack engine or the StatsPAI runner)" % (s["did_estimator"] if s["did_estimator"] != "twfe" else "event study")
        return res
    X = _design(d, s, ctl)
    m = (sm.WLS(d["_y"], X, weights=w) if w is not None else sm.OLS(d["_y"], X)).fit(**_cov_kw(s, d))
    res.update(coef=float(m.params["_d"]), se=float(m.bse["_d"]), t=float(m.tvalues["_d"]), p=float(m.pvalues["_d"]), n=int(m.nobs))
    return res

def safe(s, d):
    try: return fit_one(s, d)
    except Exception as e:
        return dict(coef=np.nan, se=np.nan, t=np.nan, p=np.nan, n=0, status=f"error: {type(e).__name__}: {e}",
                    first_stage_F=np.nan, bandwidth=np.nan, n_left=np.nan, n_right=np.nan)

rows = []
for i, s in specs.iterrows():
    r = safe(s, data0); rows.append({"key": s["key"], "label": s["label"], **r})
    if (i + 1) % 50 == 0: print(f"  {i + 1} / {len(specs)} specifications", flush=True)
pd.DataFrame(rows).to_csv("ledger_raw.csv", index=False)
print(f"ledger_raw.csv written ({len(specs)} specifications)")

if NULL_B > 0:
    nulls = pd.read_csv("null_columns.csv"); out = []
    for b in range(1, NULL_B + 1):
        d = data0.copy()
        for v in NULL_VARS: d[v] = nulls[f"{v}__{b}"].to_numpy()
        for _, s in specs.iterrows():
            r = safe(s, d)
            if r["status"] == "ok": out.append({"draw": b, "key": s["key"], "coef": r["coef"], "t": r["t"], "p": r["p"]})
        print(f"  null draw {b} / {NULL_B}", flush=True)
    pd.DataFrame(out).to_csv("null_stats.csv", index=False)
    print("null_stats.csv written")
'''

STATSPAI = r'''#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Generated by `phack export --lang statspai`. Estimates every row of
# specs.csv with StatsPAI's agent-native estimators (hdfe_ols, regress,
# rdrobust, ivreg / liml, did_2stage, stacked_did, event_study) and writes
# ledger_raw.csv in the schema `phack ingest` reads.
# Requires: statspai >= 1.20 (pip install statspai).
# ---------------------------------------------------------------------------
import warnings
import numpy as np, pandas as pd
from scipy import stats
warnings.filterwarnings("ignore")
import statspai as sp

NULL_B = @@NULL_B@@
NULL_VARS = @@NULL_VARS_PY@@
UNIT, TIME = "@@UNIT@@", "@@TIME@@"
STACK_WINDOW = (-@@STACK_PRE@@, @@STACK_POST@@)

data0 = pd.read_csv("data.csv"); data0["__row"] = np.arange(len(data0))
specs = pd.read_csv("specs.csv", dtype=str).fillna("")

def words(x): return [w for w in str(x).split() if w]
def num(x, default=np.nan):
    try: return float(x)
    except (TypeError, ValueError): return default

def transform(x, kind):
    x = np.asarray(x, float)
    if kind == "level": return x
    if kind == "log":
        m = np.nanmin(x); return np.log(x + (1 - m if m <= 0 else 0.0))
    if kind == "log1p": return np.log1p(np.clip(x, -0.999999, None))
    if kind == "asinh": return np.arcsinh(x)
    if kind == "sqrt": return np.sqrt(np.clip(x - np.nanmin(x), 0, None))
    if kind == "std": return (x - np.nanmean(x)) / np.nanstd(x, ddof=1)
    if kind == "rank": return stats.rankdata(x, nan_policy="omit") / np.sum(np.isfinite(x))
    if kind == "inv": return 1.0 / np.where(np.abs(x) < 1e-9, np.nan, x)
    if kind == "square": return x ** 2
    if kind in ("winsor1", "winsor5"):
        q = 1 if kind == "winsor1" else 5; return np.clip(x, np.nanpercentile(x, q), np.nanpercentile(x, 100 - q))
    if kind == "median_split": return (x > np.nanmedian(x)).astype(float)
    if kind == "above_mean": return (x > np.nanmean(x)).astype(float)
    if kind == "quartile_top": return (x >= np.nanpercentile(x, 75)).astype(float)
    if kind == "tercile_extremes":
        lo, hi = np.nanpercentile(x, [100 / 3, 200 / 3]); out = np.full(x.shape, np.nan)
        out[x <= lo] = 0; out[x >= hi] = 1; return out
    raise KeyError(kind)

def outlier_flag(x, rule):
    x = np.asarray(x, float)
    if rule == "none": return np.zeros(x.size, bool)
    if rule.startswith("sd"): k = float(rule[2:]); return np.abs(x - np.nanmean(x)) > k * np.nanstd(x, ddof=1)
    if rule.startswith("iqr"):
        k = float(rule[3:]); q1, q3 = np.nanpercentile(x, [25, 75]); i = q3 - q1
        return (x < q1 - k * i) | (x > q3 + k * i)
    if rule == "mad3":
        m = np.nanmedian(x); md = np.nanmedian(np.abs(x - m)) * 1.4826 or 1.0; return np.abs(x - m) > 3 * md
    if rule in ("pct1", "pct5"):
        q = 1 if rule == "pct1" else 5; return (x < np.nanpercentile(x, q)) | (x > np.nanpercentile(x, 100 - q))
    raise KeyError(rule)

def impute(s, method):
    if method == "listwise" or not s.isna().any(): return s
    if method == "mean": return s.fillna(s.mean())
    if method == "median": return s.fillna(s.median())
    if method == "zero": return s.fillna(0.0)
    if method == "ffill": return s.ffill().bfill()
    raise KeyError(method)

def _get(obj, *names):
    for n in names:
        if hasattr(obj, n):
            v = getattr(obj, n)
            return v() if callable(v) else v
    raise AttributeError(names)

def _scalar(v, name=None):
    if isinstance(v, pd.Series):
        if name is not None and name in v.index: return float(v[name])
        return float(v.iloc[0])
    if hasattr(v, "estimate"): return float(v.estimate)
    return float(v)

def _read(res, name):
    """coef / se / p / t / n from any StatsPAI result object."""
    cf = _scalar(_get(res, "params", "coef", "estimate"), name)
    se = _scalar(_get(res, "std_errors", "se", "bse"), name)
    try: p = _scalar(_get(res, "pvalues", "pvalue", "pv"), name)
    except Exception: p = float(2 * stats.norm.sf(abs(cf / se)))
    try: n = int(_get(res, "n_obs", "nobs", "N"))
    except Exception: n = 0
    return cf, se, cf / se, p, n

def fit_one(s, d):
    res = dict(coef=np.nan, se=np.nan, t=np.nan, p=np.nan, n=0, status="ok", first_stage_F=np.nan,
               bandwidth=np.nan, n_left=np.nan, n_right=np.nan)
    d = d.copy()
    if s["subsample"]: d = d.query(s["subsample"].replace("&", " and ").replace("|", " or "))
    if s["comparison_group"] == "drop_never_treated": d = d[d.groupby(UNIT)[s["treatment"]].transform("max") > 0]
    if s["comparison_group"] == "drop_always_treated": d = d[d.groupby(UNIT)[s["treatment"]].transform("min") < 1]
    ctl, z = words(s["controls"]), words(s["instruments"])
    for v in dict.fromkeys([s["outcome"], s["treatment"], *ctl, *z]):
        if v in d: d[v] = impute(d[v], s["imputation"])
    lag = int(num(s["lag"], 0))
    if lag: d = d.sort_values([UNIT, TIME]); d[s["treatment"]] = d.groupby(UNIT)[s["treatment"]].shift(lag)
    if s["design"] == "rdd": d["_d"] = (d[s["running"]] >= num(s["cutoff"], 0)).astype(float)
    else: d["_d"] = transform(d[s["treatment"]], s["d_transform"])
    d["_y"] = transform(d[s["outcome"]], s["y_transform"])
    need = [c for c in dict.fromkeys(["_y", "_d", *ctl, *z, *words(s["fe"]), s["cluster1"], s["cluster2"], s["weight"],
                                      s["running"] if s["design"] == "rdd" else ""]) if c]
    d = d.dropna(subset=need).reset_index(drop=True)
    if s["outlier_rule"] != "none":
        if s["outlier_basis"] == "residual":
            m = sp.regress("_y ~ _d" + "".join(" + " + c for c in ctl), d)
            u = np.asarray(_get(m, "resid", "residuals"), float); basis = u / np.std(u, ddof=1)
        else: basis = d["_d"] if s["outlier_basis"] == "treatment" else d["_y"]
        d = d[~outlier_flag(basis, s["outlier_rule"])].reset_index(drop=True)
    fe = words(s["fe"]); ctl_txt = "".join(" + " + c for c in ctl)
    cl = s["cluster1"] if s["vcov"] in ("cluster", "twoway") else None
    if s["design"] == "rdd":
        dd = d[np.abs(d[s["running"]] - num(s["cutoff"], 0)) > num(s["donut"], 0)].reset_index(drop=True)
        m = sp.rdrobust(dd, "_y", s["running"], c=num(s["cutoff"], 0), h=num(s["bw_abs"]), kernel=s["kernel"],
                        p=int(num(s["poly"], 1)), covs=ctl or None, cluster=cl)
        # StatsPAI reports the conventional and the robust bias-corrected rows in
        # its diagnostics; the under-covering "bias-corrected point estimate with
        # the conventional SE" combination (strategy 23) is assembled here from
        # those two rows, exactly as a user would do by hand.
        diag = getattr(m, "diagnostics", None) or {}
        conv, rob = diag.get("conventional"), diag.get("robust")
        n_eff = int((diag.get("n_effective_left") or 0) + (diag.get("n_effective_right") or 0)) or len(dd)
        if not conv or not rob:
            cf, se, tt, p, n = _read(m, None); res.update(coef=cf, se=se, t=tt, p=p, n=n or len(dd)); return res
        if s["rdd_inference"] == "conventional": cf, se, p = conv["estimate"], conv["se"], conv["pvalue"]
        elif s["rdd_inference"] == "robust": cf, se, p = rob["estimate"], rob["se"], rob["pvalue"]
        else: cf, se = rob["estimate"], conv["se"]; p = 2 * stats.norm.sf(abs(cf / se))
        res.update(coef=float(cf), se=float(se), t=float(cf / se), p=float(p), n=n_eff, bandwidth=num(s["bw_abs"]),
                   n_left=diag.get("n_effective_left", np.nan), n_right=diag.get("n_effective_right", np.nan))
        return res
    if s["design"] == "iv":
        rob = "hc1" if s["vcov"] in ("hc0", "hc1") else "nonrobust"
        if fe:
            # fixed effects in IV need pyfixest (sp.feols); fall back to FWL absorption otherwise
            try:
                fml = "_y ~ " + (" + ".join(ctl) if ctl else "1") + " | " + " + ".join(fe) + " | _d ~ " + " + ".join(z)
                if s["iv_estimator"] == "liml": raise ImportError("LIML with fixed effects is not available in StatsPAI")
                m = sp.feols(fml, d, vcov=({"CRV1": s["cluster1"]} if cl else ("HC1" if rob == "hc1" else "iid")))
                cf, se, tt, p, n = _read(m, "_d"); res.update(coef=cf, se=se, t=tt, p=p, n=n or len(d)); return res
            except ImportError as exc:
                res["status"] = "unsupported: " + str(exc).splitlines()[0][:80]; return res
        fml = "_y ~ " + "".join(c + " + " for c in ctl) + "(_d ~ " + " + ".join(z) + ")"
        if s["iv_estimator"] == "liml":
            if hasattr(sp, "liml"): m = sp.liml(fml, d, robust=rob, cluster=cl)
            else: m = sp.iv(fml, d, method="liml", robust=rob, cluster=cl)
        else:
            m = sp.ivreg(fml, d, robust=rob, cluster=cl)
        cf, se, tt, p, n = _read(m, "_d"); res.update(coef=cf, se=se, t=tt, p=p, n=n or len(d))
        for a in ("first_stage_f", "first_stage_F", "weak_iv_f", "f_first_stage"):
            if hasattr(m, a):
                try: res["first_stage_F"] = float(getattr(m, a)); break
                except Exception: pass
        if np.isnan(res["first_stage_F"]):
            diag = getattr(m, "diagnostics", None)
            if isinstance(diag, dict):
                for k, v in diag.items():
                    if "first" in str(k).lower() and "f" in str(k).lower():
                        try: res["first_stage_F"] = float(v); break
                        except Exception: pass
        return res
    if s["did_estimator"] in ("did2s", "stacked") or s["ev_estimand"]:
        first = d[d[s["treatment"]] > 0].groupby(UNIT)[TIME].min()
        d["_first"] = d[UNIT].map(first)
        if s["did_estimator"] in ("did2s", "stacked") and s["weight"]:
            res["status"] = "unsupported: StatsPAI did_2stage / stacked_did take no weights"; return res
        if s["did_estimator"] == "did2s":
            d["_first_treat"] = d["_first"].fillna(0)
            m = sp.did_2stage(d, y="_y", group=UNIT, time=TIME, first_treat="_first_treat", controls=ctl or None,
                              cluster=cl or UNIT)
            cf, se, tt, p, n = _read(m, None); res.update(coef=cf, se=se, t=tt, p=p, n=n or len(d)); return res
        if s["did_estimator"] == "stacked":
            d["_first_treat"] = d["_first"].fillna(np.inf)
            m = sp.stacked_did(d, y="_y", group=UNIT, time=TIME, first_treat="_first_treat", window=STACK_WINDOW,
                               controls=ctl or None, cluster=cl or UNIT, never_treated_only=False)
            cf, se, tt, p, n = _read(m, None); res.update(coef=cf, se=se, t=tt, p=p, n=n or len(d)); return res
        pre, post, ref = int(num(s["ev_pre"])), int(num(s["ev_post"])), int(num(s["ev_ref"]))
        m = sp.event_study(d, y="_y", treat_time="_first", time=TIME, unit=UNIT, window=(-pre, post),
                           ref_period=ref, covariates=ctl or None, cluster=cl, weights=s["weight"] or None)
        n = int(_get(m, "n_obs", "nobs") or len(d))
        if s["ev_estimand"] == "avg_post":
            # StatsPAI's ATT is the average of the post-period event coefficients with its proper SE
            cf, se, tt, p, _ = _read(m, "ATT"); res.update(coef=cf, se=se, t=tt, p=p, n=n); return res
        t = m.tidy(); t = t[t["type"].astype(str) == "event_study"].drop_duplicates("term")
        import re as _re
        t["rel"] = t["term"].astype(str).map(lambda x: int(_re.search(r"([+-]?\d+)", x.replace("event_", "")).group(1)))
        if s["ev_estimand"] == "avg_pre": sel = t[(t["rel"] < 0) & (t["rel"] != ref)]
        else: sel = t[t["rel"] == int(s["ev_estimand"][3:])]
        if sel.empty: res["status"] = "error: event-time coefficients not found"; return res
        cf = float(sel["estimate"].mean())
        # the pre-period average ignores covariances between event coefficients (StatsPAI does not expose
        # the full vcov); a single lag is exact
        se = float(np.sqrt((sel["std_error"] ** 2).sum()) / len(sel))
        res.update(coef=cf, se=se, t=cf / se, p=2 * stats.norm.sf(abs(cf / se)), n=n)
        if len(sel) > 1: res["status"] = "ok"
        return res
    fml = "_y ~ _d" + ctl_txt
    if fe:
        m = sp.hdfe_ols(fml + " | " + " + ".join(fe), d, cluster=([s["cluster1"], s["cluster2"]] if s["vcov"] == "twoway" else cl),
                        se_type=None if s["vcov"] in ("cluster", "twoway", "iid") else s["vcov"],
                        weights=s["weight"] or None)
    else:
        m = sp.regress(fml, d, robust=("nonrobust" if s["vcov"] in ("iid", "cluster", "twoway") else s["vcov"]),
                       cluster=cl, weights=(d[s["weight"]] if s["weight"] else None))
    cf, se, tt, p, n = _read(m, "_d"); res.update(coef=cf, se=se, t=tt, p=p, n=n or len(d))
    return res

def safe(s, d):
    try: return fit_one(s, d)
    except Exception as e:
        return dict(coef=np.nan, se=np.nan, t=np.nan, p=np.nan, n=0, status=f"error: {type(e).__name__}: {e}",
                    first_stage_F=np.nan, bandwidth=np.nan, n_left=np.nan, n_right=np.nan)

rows = []
for i, s in specs.iterrows():
    r = safe(s, data0); rows.append({"key": s["key"], "label": s["label"], **r})
    if (i + 1) % 50 == 0: print(f"  {i + 1} / {len(specs)} specifications", flush=True)
pd.DataFrame(rows).to_csv("ledger_raw.csv", index=False)
print(f"ledger_raw.csv written ({len(specs)} specifications)")

if NULL_B > 0:
    nulls = pd.read_csv("null_columns.csv"); out = []
    for b in range(1, NULL_B + 1):
        d = data0.copy()
        for v in NULL_VARS: d[v] = nulls[f"{v}__{b}"].to_numpy()
        for _, s in specs.iterrows():
            r = safe(s, d)
            if r["status"] == "ok": out.append({"draw": b, "key": s["key"], "coef": r["coef"], "t": r["t"], "p": r["p"]})
        print(f"  null draw {b} / {NULL_B}", flush=True)
    pd.DataFrame(out).to_csv("null_stats.csv", index=False)
    print("null_stats.csv written")
'''
