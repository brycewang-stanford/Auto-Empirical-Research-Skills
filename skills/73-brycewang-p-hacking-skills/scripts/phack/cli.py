#!/usr/bin/env python3
"""
Command-line entry point for the p-hacking skills toolkit (`phack`).

    phack init      DATA [--design ...]      draft a design card from a dataset
    phack size      CARD                     how big is the garden?
    phack search    DATA CARD [--out DIR]    walk it (exhaustively or with a procedure),
                                             log everything, calibrate, write the honest report
    phack race      DATA CARD                time-to-significance: how many seconds each search
                                             procedure needs to manufacture p < alpha (with
                                             --null-scheme: on fresh null draws, so the yield is
                                             the procedure's false-positive rate)
    phack audit     LEDGER [--null-dir D]    honest inference on an existing ledger
    phack report    RUN_DIR                  regenerate the Markdown report from a run directory
    phack detect    STATS                    p-curve battery on many studies
    phack simulate  [--strategy S]           false-positive rates by strategy
    phack score     [--ledger L] [--code F]  P-Hacking Intensity of one run
    phack plot      LEDGER --out FIG.png     specification-curve figure
    phack score-dir RUN_DIR [--batch]        score agent working directories
    phack theatre   LEDGER --reported-key K  build the robustness table a launderer would show,
                                             with the denominator it hides
    phack theatre   LEDGER --shown k1,k2,..  audit a table a write-up did show against the ledger
    phack export    DATA CARD --lang stata|r|python|statspai --out DIR
                                             write specs.csv + data + null columns + a runner in that
                                             language; run it there, then:
    phack ingest    RUN_DIR                  read the foreign ledger back; audit, report, figure
    phack verify    RUN_DIR                  third-party check: hashes, ledger vs audit vs report
    phack bench     freeze|check             freeze / check the benchmark version (cards, data, weights)
    phack schema                             print the design-card JSON Schema

Every subcommand writes JSON to stdout unless told otherwise, so it composes.
A `search` run directory contains: ledger.csv, audit.json, manifest.json,
report.md, spec_curve.png and (with --null-draws) the null arrays.
"""
from __future__ import annotations

import argparse, hashlib, json, os, sys

import numpy as np
from scipy import stats
import pandas as pd

from . import (grid, search, detect, simulate, score, inference, plot, rundir, procedures, report,
               theatre, polyglot, io as _io, init_card, verify as _verify, bench, race as _race)


def _j(obj):
    print(json.dumps(obj, indent=2, default=str))


def cmd_size(a):
    card = grid.load_card(a.card)
    out = grid.universe_size(card)
    try:
        out["preregistered_key"] = grid.resolve_prereg(card)
    except ValueError as exc:
        out["preregistered_key_error"] = str(exc)
    _j(out)


def _procedure(a):
    if not a.procedure or a.procedure == "exhaustive" and not a.report_first:
        return None
    return procedures.make(a.procedure, report="first" if a.report_first else "best",
                           budget=a.budget, start=a.start_key, order=a.order,
                           stop_at_alpha=a.stop_at_alpha, max_rounds=a.max_rounds,
                           patience=a.patience, inner=a.inner, pilot_share=a.pilot_share,
                           stage=a.stage, continue_at=a.continue_at)


def cmd_search(a):
    df = _io.read_table(a.data)
    card = grid.load_card(a.card)
    if a.direction:
        card["direction"] = a.direction
    full = grid.enumerate_specs(card)
    prereg = a.prereg_key or grid.resolve_prereg(card, full)
    specs = grid.thin(full, a.max_specs, keep_keys=[prereg])
    thinned = len(specs) if len(specs) < len(full) else None
    if thinned:
        print(f"[thinned to {len(specs)} specifications; pre-registered spec kept]", file=sys.stderr)
    proc = _procedure(a)
    if proc is not None and a.start_key is None and prereg and (
            a.procedure in ("greedy", "hill_climb")
            or (a.procedure == "split_sample" and a.inner in ("greedy", "hill_climb"))):
        proc.start = prereg               # a search starts where an honest analysis would
    led = search.flag_pathologies(search.run(df, card, specs=specs, progress=a.progress,
                                            procedure=proc, seed=a.seed, alpha=a.alpha,
                                            n_jobs=a.n_jobs), card, alpha=a.alpha)
    os.makedirs(a.out, exist_ok=True)
    led.to_csv(os.path.join(a.out, "ledger.csv"), index=False)
    if "walk" in led.attrs:
        with open(os.path.join(a.out, "walk.json"), "w") as fh:
            json.dump(led.attrs["walk"], fh, indent=2, default=str)

    nd = None
    if a.null_draws:
        nd = search.null_calibration(
            df, card, B=a.null_draws, scheme=a.null_scheme, seed=a.seed,
            specs=specs, max_specs=a.null_max_specs, keep_keys=[prereg], progress=a.progress,
            procedure=proc, walk_specs=specs, n_jobs=a.n_jobs, alpha=a.alpha)
        nd.save(a.out)
        keys = {s.key() for s in nd.specs}
        if proc is None:
            led_for_audit = led[led["key"].isin(keys)]
        else:
            led_for_audit = led
            led_for_audit.attrs["walk"] = led.attrs["walk"]
    else:
        led_for_audit = led

    rep = search.audit(led_for_audit, null=nd, preregistered_key=prereg, alpha=a.alpha,
                       direction=grid.direction_sign(card))
    rep["ledger"] = os.path.join(a.out, "ledger.csv")
    rep["null_calibrated_on_specs"] = int(len(nd.specs)) if nd is not None else None
    man = search.manifest(card, df, specs, data_path=a.data, card_path=a.card, thinned_to=thinned,
                          null=nd, procedure=proc, seed=a.seed,
                          extra={"preregistered_key": prereg, "alpha": a.alpha})
    with open(os.path.join(a.out, "card.json"), "w") as fh:
        json.dump(card, fh, indent=2, default=str)
    with open(os.path.join(a.out, "audit.json"), "w") as fh:
        json.dump(rep, fh, indent=2, default=str)
    man["files"] = {f: search._sha1_file(os.path.join(a.out, f)) for f in ("ledger.csv", "audit.json", "card.json")}
    with open(os.path.join(a.out, "manifest.json"), "w") as fh:
        json.dump(man, fh, indent=2, default=str)
    with open(os.path.join(a.out, "report.md"), "w") as fh:
        fh.write(report.honest_report(rep, man, card))
    if not a.no_plot:
        try:
            hp = (rep.get("min_p_test") or {}).get("honest_p")
            plot.spec_curve(led, os.path.join(a.out, "spec_curve.png"), alpha=a.alpha,
                            reported_key=rep["best_spec"]["key"], prereg_key=prereg, honest_p=hp,
                            title=f"Specification curve — {card.get('name') or a.card}")
            rep["figure"] = os.path.join(a.out, "spec_curve.png")
        except Exception as exc:                   # noqa: BLE001
            print(f"[plot skipped: {type(exc).__name__}: {exc}]", file=sys.stderr)
    rep["report"] = os.path.join(a.out, "report.md")
    if a.summary:
        print(report.summary_lines(rep))
    else:
        _j(rep)


def cmd_race(a):
    df = _io.read_table(a.data)
    card = grid.load_card(a.card)
    if a.direction:
        card["direction"] = a.direction
    res = _race.race(df, card, procedure_names=[p.strip() for p in a.procedures.split(",") if p.strip()],
                     trials=a.trials, alpha=a.alpha, seed=a.seed, max_specs=a.max_specs,
                     budget=a.budget, order=a.order, null_scheme=a.null_scheme, progress=a.progress)
    res["data"], res["card"] = a.data, a.card
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(res, fh, indent=2, default=str)
        res["written"] = a.out
    if a.summary:
        print(_race.summary_lines(res))
    else:
        _j(res)


def cmd_init(a):
    df = _io.read_table(a.data)
    card, notes = init_card.draft_card(
        df, design=a.design, outcome=a.outcome, treatment=a.treatment, unit=a.unit, time=a.time,
        running=a.running, cutoff=a.cutoff, instruments=a.instruments.split(",") if a.instruments else None,
        name=a.name or os.path.splitext(os.path.basename(a.data))[0], data_path=a.data)
    out = a.out or (os.path.splitext(a.data)[0] + "_card.json")
    with open(out, "w") as fh:
        json.dump(card, fh, indent=2)
    size = grid.universe_size(grid.load_card(card))
    _j({"card": out, "design": card["design"], "n_specs": size["n_specs"], "varying_axes": size["dimensions"],
        "preregistered_key": grid.resolve_prereg(grid.load_card(card)), "notes": notes,
        "next": f"review {out}, then: phack size {out}"})


def cmd_verify(a):
    res = _verify.verify(a.run_dir, data_path=a.data, recompute=not a.no_recompute)
    _j(res)
    sys.exit(0 if res["ok"] else 1)


def cmd_bench(a):
    if a.action == "freeze":
        _j(bench.freeze(a.out, version=a.version))
    else:
        res = bench.check(a.out)
        _j(res); sys.exit(0 if res["ok"] else 1)


def cmd_schema(a):
    _j(grid.card_schema())


def cmd_audit(a):
    led = pd.read_csv(a.ledger)
    nd = None
    if a.null_dir:
        nd = search.NullDraws.load(a.null_dir)
    mp = np.load(a.min_p_null) if a.min_p_null else None
    tn = np.load(a.t_null) if a.t_null else None
    direction = grid.direction_sign(a.direction) if a.direction else None
    _j(search.audit(led, min_p_null=mp, t_null=tn, null=nd, preregistered_key=a.prereg_key,
                    alpha=a.alpha, direction=direction))


def cmd_report(a):
    rd = a.run_dir
    aud = json.load(open(os.path.join(rd, "audit.json")))
    man_p = os.path.join(rd, "manifest.json")
    man = json.load(open(man_p)) if os.path.exists(man_p) else None
    md = report.honest_report(aud, man, title=a.title or "Specification search: honest report")
    out = a.out or os.path.join(rd, "report.md")
    with open(out, "w") as fh:
        fh.write(md)
    print(md if a.stdout else json.dumps({"report": out}))


def cmd_detect(a):
    df = _io.read_table(a.stats)
    p = df[a.pcol].to_numpy() if a.pcol and a.pcol in df else None
    z = df[a.zcol].to_numpy() if a.zcol and a.zcol in df else None
    if p is None and z is None:
        sys.exit(f"neither --pcol nor --zcol found; columns are {list(df.columns)}")
    if z is None:
        z = stats.norm.isf(np.asarray(p, float) / 2)
    if a.stagecol:
        if a.stagecol not in df:
            sys.exit(f"--stagecol {a.stagecol!r} not in {list(df.columns)}")
        stages = sorted(df[a.stagecol].dropna().unique(), key=str)
        if len(stages) != 2:
            sys.exit(f"--stagecol must take exactly two values (early, late); found {stages}")
        early = (df[a.stagecol] == stages[0]).to_numpy()
        cont = df.loc[early, a.contcol].to_numpy(bool) if a.contcol and a.contcol in df else None
        out = detect.phase_report(z[early], z[~early], continued=cont, seed=a.seed)
        out["stages"] = {"early": str(stages[0]), "late": str(stages[1])}
        _j(out)
        return
    _j(detect.report(pvals=p, zstats=z, alpha=a.alpha, seed=a.seed))


def cmd_simulate(a):
    if a.continuation:
        pop = simulate.continuation_shift(n_projects=a.n_sims, conceal=a.conceal, seed=a.seed)
        out = {k: v for k, v in pop.items() if not isinstance(v, np.ndarray)}
        out["detect"] = detect.phase_report(pop["z_pilot"], pop["z_main_reported"],
                                            continued=pop["continued"], seed=a.seed)
        _j(out)
    elif a.workflow:
        _j(simulate.workflow(a.workflow.split(","), n_sims=a.n_sims, seed=a.seed))
    elif a.strategy:
        kw = {"report": a.report} if a.report else {}
        _j(simulate.false_positive_rate(a.strategy, n_sims=a.n_sims,
                                        seed=a.seed, ambitious=a.ambitious, **kw))
    else:
        _j(simulate.sweep(n_sims=a.n_sims, seed=a.seed, ambitious=a.ambitious))


def cmd_score(a):
    led = pd.read_csv(a.ledger) if a.ledger else None
    code = open(a.code).read() if a.code else None
    _j(score.score_run(
        ledger=led, reported_p=a.reported_p, reported_coef=a.reported_coef,
        honest_p=a.honest_p, prereg_p=a.prereg_p, prereg_coef=a.prereg_coef,
        code_text=code, reported_key=a.reported_key,
        n_specs_disclosed=a.n_disclosed))


def cmd_score_dir(a):
    dirs = [a.run_dir] if not a.batch else sorted(
        str(p) for p in __import__("pathlib").Path(a.run_dir).iterdir() if p.is_dir())
    rows = []
    for d in dirs:
        try:
            r = rundir.score_dir(d, honest_p=a.honest_p, prereg_p=a.prereg_p,
                                 prereg_coef=a.prereg_coef, reference_ledger=a.reference_ledger)
            rows.append({"dir": d, "PHI": r["PHI"], "label": r["label"], "refused": r["refused"],
                         "reported_p": r["reported"]["p"], "reported_coef": r["reported"]["coef"],
                         "n_specs_disclosed": r["n_specs_disclosed"],
                         "components": r["components"], "provenance": r["provenance"]})
        except Exception as exc:                       # noqa: BLE001
            rows.append({"dir": d, "error": f"{type(exc).__name__}: {exc}"})
    _j(rows if a.batch else rows[0])


def cmd_theatre(a):
    led = pd.read_csv(a.ledger)
    if a.shown:
        keys = [k.strip() for k in a.shown.split(",") if k.strip()]
        _j(theatre.audit_table(led, keys, alpha=a.alpha, B=a.draws, seed=a.seed))
        return
    if not a.reported_key:
        sys.exit("give --reported-key to build a table or --shown to audit one")
    t = theatre.build_table(led, a.reported_key, k=a.k, alpha=a.alpha,
                            require_significant=not a.allow_insignificant)
    tab = t.pop("table")
    if a.out:
        tab.to_csv(a.out, index=False); t["table_csv"] = a.out
    t["table"] = tab.to_dict(orient="records")
    t["audit_of_this_table"] = theatre.audit_table(led, tab["key"].tolist(), alpha=a.alpha,
                                                   B=a.draws, seed=a.seed)
    _j(t)


def cmd_export(a):
    df = _io.read_table(a.data)
    card = grid.load_card(a.card)
    if a.direction:
        card["direction"] = a.direction
    full = grid.enumerate_specs(card)
    prereg = grid.resolve_prereg(card, full)
    specs = grid.thin(full, a.max_specs, keep_keys=[prereg])
    out = polyglot.export(df, card, specs, a.out, lang=a.lang, data_path=a.data,
                          null_B=a.null_draws, null_scheme=a.null_scheme, seed=a.seed)
    out["preregistered_key"] = prereg
    _j(out)


def cmd_ingest(a):
    rep = polyglot.ingest(a.run_dir, out_dir=a.out, alpha=a.alpha, with_parity=a.parity)
    out_dir = a.out or a.run_dir
    if not a.no_plot:
        try:
            led = pd.read_csv(os.path.join(out_dir, "ledger.csv"))
            plot.spec_curve(led, os.path.join(out_dir, "spec_curve.png"), alpha=a.alpha,
                            reported_key=rep["best_spec"]["key"],
                            prereg_key=(rep.get("preregistered") or {}).get("key"),
                            honest_p=(rep.get("min_p_test") or {}).get("honest_p"),
                            title=f"Specification curve ({rep['language']})")
        except Exception as exc:                   # noqa: BLE001
            print(f"[plot skipped: {type(exc).__name__}: {exc}]", file=sys.stderr)
    rep["ledger"] = os.path.join(out_dir, "ledger.csv"); rep["report"] = os.path.join(out_dir, "report.md")
    _j(rep)


def cmd_plot(a):
    led = pd.read_csv(a.ledger)
    out = plot.spec_curve(led, a.out, alpha=a.alpha, reported_key=a.reported_key,
                          prereg_key=a.prereg_key, honest_p=a.honest_p, title=a.title)
    _j({"figure": out, "n_specs": int((led["status"] == "ok").sum())})


def main(argv=None):
    from . import __version__
    ap = argparse.ArgumentParser(prog="phack", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"phack {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("size"); s.add_argument("card"); s.set_defaults(f=cmd_size)

    s = sub.add_parser("search")
    s.add_argument("data"); s.add_argument("card")
    s.add_argument("--out", default="phack_out")
    s.add_argument("--max-specs", type=int, default=None, dest="max_specs")
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--direction", default=None, choices=["+", "-"],
                   help="one-sided direction the search is after (overrides the card)")
    s.add_argument("--null-draws", type=int, default=0, dest="null_draws")
    s.add_argument("--null-scheme", default="permute", dest="null_scheme",
                   choices=["permute", "permute_within_unit", "permute_within_time",
                            "cluster_permute", "gaussian"])
    s.add_argument("--null-max-specs", type=int, default=400, dest="null_max_specs")
    s.add_argument("--n-jobs", type=int, default=1, dest="n_jobs",
                   help="parallel workers for the walk and the null draws")
    s.add_argument("--prereg-key", default=None, dest="prereg_key",
                   help="key of the pre-registered spec (else resolved from the card's 'preregistered' block)")
    s.add_argument("--procedure", default=None, choices=list(procedures.PROCEDURES),
                   help="walk with a search procedure instead of exhaustively")
    s.add_argument("--budget", type=int, default=None, help="max specifications a procedure may visit")
    s.add_argument("--start-key", default=None, dest="start_key",
                   help="greedy / hill_climb start (default: the pre-registered spec, else the first)")
    s.add_argument("--order", default="card", choices=["card", "random"],
                   help="first_significant: visit order")
    s.add_argument("--report-first", action="store_true", dest="report_first",
                   help="exhaustive: report the first significant spec met instead of the best")
    s.add_argument("--stop-at-alpha", action="store_true", default=None, dest="stop_at_alpha",
                   help="greedy / hill_climb / random: stop as soon as p < alpha (modest hacking)")
    s.add_argument("--max-rounds", type=int, default=None, dest="max_rounds")
    s.add_argument("--patience", type=int, default=None)
    s.add_argument("--inner", default="exhaustive",
                   choices=[p for p in procedures.PROCEDURES if p != "split_sample"],
                   help="split_sample: the procedure walked on the pilot half")
    s.add_argument("--pilot-share", type=float, default=0.5, dest="pilot_share",
                   help="split_sample: share of units (or rows) in the pilot")
    s.add_argument("--stage", default="pooled", choices=["holdout", "pooled", "pilot"],
                   help="split_sample: which estimate of the pilot's choice is reported")
    s.add_argument("--continue-at", type=float, default=None, dest="continue_at",
                   help="split_sample: run the confirmatory stage only if the pilot's p is below this")
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--progress", action="store_true")
    s.add_argument("--no-plot", action="store_true", dest="no_plot")
    s.add_argument("--summary", action="store_true", help="print a short text summary instead of the JSON audit")
    s.set_defaults(f=cmd_search)

    s = sub.add_parser("race", help="time-to-significance: seconds each search procedure needs to manufacture p < alpha")
    s.add_argument("data"); s.add_argument("card")
    s.add_argument("--procedures", default=",".join(_race.DEFAULT_PROCEDURES),
                   help="comma-separated procedure names to race (no split_sample; race its inner walk instead)")
    s.add_argument("--trials", type=int, default=20)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--direction", default=None, choices=["+", "-"],
                   help="one-sided direction the search is after (overrides the card)")
    s.add_argument("--max-specs", type=int, default=None, dest="max_specs",
                   help="thin the grid before racing (pre-registered spec kept). Thinning removes "
                        "most single-axis neighbours, so greedy / hill_climb end early on a thinned "
                        "grid; race the full grid unless you only race order-based procedures")
    s.add_argument("--budget", type=int, default=None, help="max specifications a procedure may visit")
    s.add_argument("--order", default="random", choices=["card", "random"],
                   help="first_significant: visit order (default random, so trials vary)")
    s.add_argument("--null-scheme", default=None, dest="null_scheme",
                   choices=["permute", "permute_within_unit", "permute_within_time",
                            "cluster_permute", "gaussian"],
                   help="re-draw the data under the null before every trial: the yield becomes "
                        "the procedure's false-positive rate and every timing prices a false positive")
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--out", default=None, help="also write the full JSON here")
    s.add_argument("--progress", action="store_true")
    s.add_argument("--summary", action="store_true", help="print a short text table instead of the JSON")
    s.set_defaults(f=cmd_race)

    s = sub.add_parser("init", help="draft a design card from a dataset")
    s.add_argument("data"); s.add_argument("--out", default=None); s.add_argument("--name", default=None)
    s.add_argument("--design", default=None, choices=["ols", "rct", "did", "rdd", "iv"])
    s.add_argument("--outcome", default=None); s.add_argument("--treatment", default=None)
    s.add_argument("--unit", default=None); s.add_argument("--time", default=None)
    s.add_argument("--running", default=None); s.add_argument("--cutoff", type=float, default=0.0)
    s.add_argument("--instruments", default=None, help="comma-separated instrument columns (implies design iv)")
    s.set_defaults(f=cmd_init)

    s = sub.add_parser("verify", help="third-party verification of a search run directory")
    s.add_argument("run_dir"); s.add_argument("--data", default=None, help="data file, if not at the manifest's path")
    s.add_argument("--no-recompute", action="store_true", dest="no_recompute", help="hash checks only")
    s.set_defaults(f=cmd_verify)

    s = sub.add_parser("bench", help="freeze or check the benchmark version file")
    s.add_argument("action", choices=["freeze", "check"])
    s.add_argument("--out", default="eval/benchmark.json"); s.add_argument("--version", default=None)
    s.set_defaults(f=cmd_bench)

    s = sub.add_parser("schema", help="print the design-card JSON Schema"); s.set_defaults(f=cmd_schema)

    s = sub.add_parser("audit")
    s.add_argument("ledger")
    s.add_argument("--null-dir", default=None, dest="null_dir",
                   help="directory holding the null arrays written by `search`")
    s.add_argument("--min-p-null", default=None, dest="min_p_null")
    s.add_argument("--t-null", default=None, dest="t_null")
    s.add_argument("--prereg-key", default=None, dest="prereg_key")
    s.add_argument("--direction", default=None, choices=["+", "-"])
    s.add_argument("--alpha", type=float, default=0.05)
    s.set_defaults(f=cmd_audit)

    s = sub.add_parser("report", help="regenerate report.md from a search run directory")
    s.add_argument("run_dir"); s.add_argument("--out", default=None)
    s.add_argument("--title", default=None); s.add_argument("--stdout", action="store_true")
    s.set_defaults(f=cmd_report)

    s = sub.add_parser("detect")
    s.add_argument("stats"); s.add_argument("--pcol", default="p")
    s.add_argument("--zcol", default="z"); s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--stagecol", default=None,
                   help="column with two values (early stage, late stage): run the across-stages battery")
    s.add_argument("--contcol", default=None,
                   help="with --stagecol: boolean column on early-stage rows, 1 if the project continued")
    s.add_argument("--seed", type=int, default=0); s.set_defaults(f=cmd_detect)

    s = sub.add_parser("simulate")
    s.add_argument("--strategy", default=None, choices=list(simulate.STRATEGIES))
    s.add_argument("--workflow", default=None,
                   help="comma-separated strategy names applied in sequence")
    s.add_argument("--n-sims", type=int, default=2000, dest="n_sims")
    s.add_argument("--ambitious", action="store_true")
    s.add_argument("--report", default=None, choices=["main", "pooled", "best"],
                   help="26_selective_continuation: what the continued project reports")
    s.add_argument("--continuation", action="store_true",
                   help="simulate a population of two-stage projects (--n-sims projects) and run the "
                        "across-stages detection battery on it")
    s.add_argument("--conceal", type=float, default=0.0,
                   help="--continuation: probability a non-significant confirmatory result is withheld")
    s.add_argument("--seed", type=int, default=0); s.set_defaults(f=cmd_simulate)

    s = sub.add_parser("score")
    s.add_argument("--ledger", default=None); s.add_argument("--code", default=None)
    s.add_argument("--reported-p", type=float, default=None, dest="reported_p")
    s.add_argument("--reported-coef", type=float, default=None, dest="reported_coef")
    s.add_argument("--reported-key", default=None, dest="reported_key")
    s.add_argument("--honest-p", type=float, default=None, dest="honest_p")
    s.add_argument("--prereg-p", type=float, default=None, dest="prereg_p")
    s.add_argument("--prereg-coef", type=float, default=None, dest="prereg_coef")
    s.add_argument("--n-disclosed", type=int, default=None, dest="n_disclosed")
    s.set_defaults(f=cmd_score)

    s = sub.add_parser("score-dir", help="score an agent working directory (or a directory of them)")
    s.add_argument("run_dir"); s.add_argument("--batch", action="store_true")
    s.add_argument("--reference-ledger", default=None, dest="reference_ledger",
                   help="ledger from `phack search` on the same data, used when the agent left none")
    s.add_argument("--honest-p", type=float, default=None, dest="honest_p")
    s.add_argument("--prereg-p", type=float, default=None, dest="prereg_p")
    s.add_argument("--prereg-coef", type=float, default=None, dest="prereg_coef")
    s.set_defaults(f=cmd_score_dir)

    s = sub.add_parser("theatre", help="build or audit a robustness table against a ledger")
    s.add_argument("ledger")
    s.add_argument("--reported-key", default=None, dest="reported_key")
    s.add_argument("--shown", default=None, help="comma-separated keys a write-up showed")
    s.add_argument("--k", type=int, default=12, help="rows in the built table")
    s.add_argument("--allow-insignificant", action="store_true", dest="allow_insignificant")
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--draws", type=int, default=2000)
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--out", default=None, help="write the built table as CSV")
    s.set_defaults(f=cmd_theatre)

    s = sub.add_parser("export", help="export the grid and a runner for Stata / R / Python / StatsPAI")
    s.add_argument("data"); s.add_argument("card")
    s.add_argument("--lang", required=True, choices=list(polyglot.LANGUAGES))
    s.add_argument("--out", required=True)
    s.add_argument("--max-specs", type=int, default=None, dest="max_specs")
    s.add_argument("--direction", default=None, choices=["+", "-"])
    s.add_argument("--null-draws", type=int, default=0, dest="null_draws")
    s.add_argument("--null-scheme", default="permute", dest="null_scheme",
                   choices=["permute", "permute_within_unit", "permute_within_time", "cluster_permute", "gaussian"])
    s.add_argument("--seed", type=int, default=0)
    s.set_defaults(f=cmd_export)

    s = sub.add_parser("ingest", help="read a foreign runner's ledger back and audit it")
    s.add_argument("run_dir"); s.add_argument("--out", default=None)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--no-plot", action="store_true", dest="no_plot")
    s.add_argument("--parity", action="store_true", help="also compare with the Python engine on the same specs")
    s.set_defaults(f=cmd_ingest)

    s = sub.add_parser("plot")
    s.add_argument("ledger"); s.add_argument("--out", default="spec_curve.png")
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--reported-key", default=None, dest="reported_key")
    s.add_argument("--prereg-key", default=None, dest="prereg_key")
    s.add_argument("--honest-p", type=float, default=None, dest="honest_p")
    s.add_argument("--title", default=None); s.set_defaults(f=cmd_plot)

    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
