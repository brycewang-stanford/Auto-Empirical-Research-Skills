#!/usr/bin/env python3
"""Produce reference candidate results for the AERS benchmark tasks.

Deliberately simple, transparent, dependency-free reference pipelines so the
benchmark is runnable end to end out of the box. A real agent run would drop its
own results.json into a sibling candidate directory and grade against it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import lalonde  # noqa: E402
import card  # noqa: E402
import simdid  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CAND = Path(__file__).resolve().parent / "candidates"


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


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


def did_candidate() -> dict:
    data_path = ROOT / "benchmark" / "data" / "sim-staggered-did.csv"
    if not data_path.exists():
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


def main() -> int:
    lc = lalonde_candidate()
    write(CAND / "reference-ols" / "results.json", lc)
    print(f"  lalonde: naive {lc['naive_att']:,.0f} -> adjusted {lc['adjusted_att']:,.0f}")
    cc = card_candidate()
    write(CAND / "reference-iv" / "results.json", cc)
    print(
        f"  card:    OLS {cc['ols_return']} -> IV {cc['iv_return']} "
        f"(first-stage F {cc['first_stage_F']})"
    )
    dc = did_candidate()
    write(CAND / "reference-did" / "results.json", dc)
    print(
        f"  staggered DID: TWFE {dc['twfe_att']} -> group-time {dc['cs_att']} "
        f"(true {dc['true_att']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
