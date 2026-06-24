#!/usr/bin/env python3
"""Produce reference candidate results for the AERS benchmark tasks.

Deliberately simple, transparent, dependency-free reference pipelines so the
benchmark is runnable end to end out of the box. A real agent run would drop its
own results.json into a sibling candidate directory and grade against it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import lalonde  # noqa: E402
import card  # noqa: E402
import simdid  # noqa: E402
import rdd  # noqa: E402
import badcontrol  # noqa: E402
import panelfe  # noqa: E402
import eventstudy  # noqa: E402
import dml  # noqa: E402
import survival  # noqa: E402
import bayesian  # noqa: E402
import synth  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CAND = Path(__file__).resolve().parent / "candidates"


def serialize(payload: dict) -> str:
    return json.dumps(payload, indent=2) + "\n"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(serialize(payload), encoding="utf-8")
    print(f"Wrote {rel(path)}")


def lalonde_candidate() -> dict:
    rows = lalonde.load(ROOT / "demo-notebooks" / "_lalonde_data.csv")
    t, c = lalonde.split(rows, "treat")
    return {
        "task": "lalonde-recovery",
        "method": "OLS regression adjustment (full controls incl. re74, re75)",
        "n_treated": len(t), "n_control": len(c),
        "naive_att": round(lalonde.naive_att(rows, "treat", "re78"), 1),
        "adjusted_att": round(lalonde.adjusted_att(rows, "treat", "re78"), 1),
        "balance": {k: round(v, 3) for k, v in lalonde.smd_table(rows, "treat").items()},
    }


def card_candidate() -> dict:
    rows = card.load(ROOT / "demo-StatsPAI-skill" / "data" / "card.csv")
    coef, f = card.first_stage(rows)
    return {
        "task": "card-iv-recovery",
        "method": "OLS vs 2SLS (nearc4 instrument), manual two-stage",
        "n": len(rows),
        "ols_return": round(card.ols_return(rows), 4),
        "iv_return": round(card.iv_return(rows), 4),
        "first_stage_coef": round(coef, 4),
        "first_stage_F": round(f, 2),
    }


def did_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-staggered-did.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        simdid.write_csv(data_path)
    rows = simdid.load(data_path)
    return {
        "task": "did-staggered-recovery",
        "method": "Group-time DID with not-yet-treated controls; TWFE diagnostic reported",
        "n": len(rows),
        "true_att": round(simdid.true_att(rows), 4),
        "twfe_att": round(simdid.twfe_att(rows), 4),
        "cs_att": round(simdid.cs_att(rows), 4),
    }


def rdd_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-rdd.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        rdd.write_csv(data_path)
    rows = rdd.load(data_path)
    return {
        "task": "rdd-recovery",
        "method": "Sharp RD: local-linear at the cutoff vs global common-slope OLS vs naive across-cutoff mean difference",
        "n": len(rows),
        "bandwidth": rdd.BANDWIDTH,
        "true_tau": round(rdd.true_tau(rows), 4),
        "naive_jump": round(rdd.naive_jump(rows), 4),
        "global_att": round(rdd.global_att(rows), 4),
        "local_att": round(rdd.local_att(rows), 4),
    }


def badcontrol_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-badcontrol.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        badcontrol.write_csv(data_path)
    rows = badcontrol.load(data_path)
    return {
        "task": "bad-control-recovery",
        "method": "y~d (naive) vs y~d+x (good pre-treatment control) vs y~d+x+m (bad post-treatment mediator control)",
        "n": len(rows),
        "true_total": round(badcontrol.true_total(rows), 4),
        "naive_effect": round(badcontrol.naive_effect(rows), 4),
        "good_control_effect": round(badcontrol.good_control_effect(rows), 4),
        "bad_control_effect": round(badcontrol.bad_control_effect(rows), 4),
    }


def panelfe_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-panel-fe.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        panelfe.write_csv(data_path)
    rows = panelfe.load(data_path)
    return {
        "task": "panel-fe-recovery",
        "method": "Two-way (unit+time) fixed effects vs pooled OLS that ignores unit heterogeneity",
        "n": len(rows),
        "true_att": round(panelfe.true_att(rows), 4),
        "twoway_fe_att": round(panelfe.twoway_fe_att(rows), 4),
        "pooled_att": round(panelfe.pooled_att(rows), 4),
    }


def eventstudy_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-event-study.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        eventstudy.write_csv(data_path)
    rows = eventstudy.load(data_path)
    return {
        "task": "event-study-recovery",
        "method": "Event-study with unit+time FE and treated x relative-time dummies vs naive treated-only before/after",
        "n": len(rows),
        "true_att": round(eventstudy.true_att(rows), 4),
        "es_att": round(eventstudy.es_att(rows), 4),
        "es_pre_max": round(eventstudy.es_pre_max(rows), 4),
        "naive_before_after": round(eventstudy.naive_before_after(rows), 4),
    }


def dml_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-dml.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        dml.write_csv(data_path)
    rows = dml.load(data_path)
    return {
        "task": "dml-recovery",
        "method": "Cross-fitted partialling-out (DML) vs naive OLS of outcome on treatment only",
        "n": len(rows),
        "true_theta": round(dml.true_theta(rows), 4),
        "dml_theta": round(dml.dml_theta(rows), 4),
        "naive_theta": round(dml.naive_theta(rows), 4),
    }


def survival_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-survival.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        survival.write_csv(data_path)
    rows = survival.load(data_path)
    return {
        "task": "survival-recovery",
        "method": "Kaplan-Meier survival (handles censoring) vs naive proportion that treats censored as failures",
        "n": len(rows),
        "true_surv_treat": round(survival.true_survival(rows, 1), 4),
        "true_surv_control": round(survival.true_survival(rows, 0), 4),
        "km_surv_treat": round(survival.km_survival(rows, 1), 4),
        "km_surv_control": round(survival.km_survival(rows, 0), 4),
        "naive_surv_treat": round(survival.naive_survival(rows, 1), 4),
        "naive_surv_control": round(survival.naive_survival(rows, 0), 4),
    }


def bayesian_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-bayesian.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        bayesian.write_csv(data_path)
    rows = bayesian.load(data_path)
    return {
        "task": "bayesian-recovery",
        "method": "Conjugate Normal-Normal posterior mean: weakly-informative vs overconfident miscalibrated prior",
        "n": len(rows),
        "data_mean": round(bayesian.data_mean(rows), 4),
        "posterior_weak": round(bayesian.posterior_weak(rows), 4),
        "posterior_strong": round(bayesian.posterior_strong(rows), 4),
    }


def synth_candidate(write_missing_data: bool = True) -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-synth.csv"
    if not data_path.exists():
        if not write_missing_data:
            raise FileNotFoundError(data_path)
        synth.write_csv(data_path)
    rows = synth.load(data_path)
    return {
        "task": "synthetic-control-recovery",
        "method": "Synthetic control (simplex-fit donor weights on the pre-period) vs equal-weight donor average",
        "n": len(rows),
        "true_effect": round(synth.true_effect(rows), 4),
        "sc_effect": round(synth.sc_effect(rows), 4),
        "naive_effect": round(synth.naive_effect(rows), 4),
    }


def reference_candidates(write_missing_data: bool = True) -> list[tuple[Path, dict]]:
    return [
        (CAND / "reference-ols" / "results.json", lalonde_candidate()),
        (CAND / "reference-iv" / "results.json", card_candidate()),
        (CAND / "reference-did" / "results.json", did_candidate(write_missing_data)),
        (CAND / "reference-rd" / "results.json", rdd_candidate(write_missing_data)),
        (CAND / "reference-badcontrol" / "results.json", badcontrol_candidate(write_missing_data)),
        (CAND / "reference-panelfe" / "results.json", panelfe_candidate(write_missing_data)),
        (CAND / "reference-eventstudy" / "results.json", eventstudy_candidate(write_missing_data)),
        (CAND / "reference-dml" / "results.json", dml_candidate(write_missing_data)),
        (CAND / "reference-survival" / "results.json", survival_candidate(write_missing_data)),
        (CAND / "reference-bayesian" / "results.json", bayesian_candidate(write_missing_data)),
        (CAND / "reference-synth" / "results.json", synth_candidate(write_missing_data)),
    ]


def print_summary(payloads: list[tuple[Path, dict]]) -> None:
    by_task = {payload["task"]: payload for _, payload in payloads}
    lc = by_task["lalonde-recovery"]
    print(f"  lalonde: naive {lc['naive_att']:,.0f} -> adjusted {lc['adjusted_att']:,.0f}")
    cc = by_task["card-iv-recovery"]
    print(
        f"  card:    OLS {cc['ols_return']} -> IV {cc['iv_return']} "
        f"(first-stage F {cc['first_stage_F']})"
    )
    dc = by_task["did-staggered-recovery"]
    print(
        f"  staggered DID: TWFE {dc['twfe_att']} -> group-time {dc['cs_att']} "
        f"(true {dc['true_att']})"
    )
    rc = by_task["rdd-recovery"]
    print(
        f"  sharp RD: naive jump {rc['naive_jump']} -> local-linear {rc['local_att']} "
        f"(true {rc['true_tau']})"
    )
    bc = by_task["bad-control-recovery"]
    print(
        f"  bad control: good {bc['good_control_effect']} -> bad/mediator {bc['bad_control_effect']} "
        f"(true total {bc['true_total']})"
    )
    pf = by_task["panel-fe-recovery"]
    print(
        f"  panel FE: pooled {pf['pooled_att']} -> two-way FE {pf['twoway_fe_att']} "
        f"(true {pf['true_att']})"
    )
    es = by_task["event-study-recovery"]
    print(
        f"  event study: naive {es['naive_before_after']} -> dynamic ATT {es['es_att']} "
        f"(true {es['true_att']}, max |pre| {es['es_pre_max']})"
    )
    dm = by_task["dml-recovery"]
    print(
        f"  DML: naive {dm['naive_theta']} -> cross-fit {dm['dml_theta']} "
        f"(true {dm['true_theta']})"
    )
    sv = by_task["survival-recovery"]
    print(
        f"  survival: naive treated {sv['naive_surv_treat']} -> KM {sv['km_surv_treat']} "
        f"(true {sv['true_surv_treat']})"
    )
    bayes = by_task["bayesian-recovery"]
    print(
        f"  bayesian: strong-wrong-prior {bayes['posterior_strong']} -> weak-prior "
        f"{bayes['posterior_weak']} (true {bayes['data_mean']})"
    )
    sc = by_task["synthetic-control-recovery"]
    print(
        f"  synthetic control: naive {sc['naive_effect']} -> SC {sc['sc_effect']} "
        f"(true {sc['true_effect']})"
    )


def check_outputs(payloads: list[tuple[Path, dict]]) -> int:
    stale: list[str] = []
    for path, payload in payloads:
        expected = serialize(payload)
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            stale.append(rel(path))
    if stale:
        print("Reference benchmark candidates are stale. Regenerate with:", file=sys.stderr)
        print("  python3 benchmark/reference_pipeline.py", file=sys.stderr)
        for path in stale:
            print(f"stale: {path}", file=sys.stderr)
        return 1
    print("Reference benchmark candidates are current.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed reference candidates without rewriting them",
    )
    args = parser.parse_args(argv)

    payloads = reference_candidates(write_missing_data=not args.check)
    if args.check:
        return check_outputs(payloads)
    for path, payload in payloads:
        write(path, payload)
    print_summary(payloads)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
