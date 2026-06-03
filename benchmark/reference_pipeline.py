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


def reference_candidates(write_missing_data: bool = True) -> list[tuple[Path, dict]]:
    return [
        (CAND / "reference-ols" / "results.json", lalonde_candidate()),
        (CAND / "reference-iv" / "results.json", card_candidate()),
        (CAND / "reference-did" / "results.json", did_candidate(write_missing_data)),
        (CAND / "reference-rd" / "results.json", rdd_candidate(write_missing_data)),
        (CAND / "reference-badcontrol" / "results.json", badcontrol_candidate(write_missing_data)),
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
