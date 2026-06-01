#!/usr/bin/env python3
"""Grade candidate results against AERS benchmark tasks.

A "candidate" is a results.json produced by any pipeline (the reference pipeline,
the repo's demo outputs, or a real agent run). For each task the checker
recomputes the data-derived golds from the dataset itself, so a candidate cannot
pass by reporting fabricated numbers. Literature constants (the LaLonde
experimental benchmark, the Card canonical values) come from the task specs.

Usage:
    python3 benchmark/reference_pipeline.py            # produce reference candidates
    python3 benchmark/check_benchmark.py               # grade all tasks
    python3 benchmark/check_benchmark.py --task card-iv-recovery
    python3 benchmark/check_benchmark.py --strict      # nonzero exit on required fail
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import lalonde  # noqa: E402
import card  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = Path(__file__).resolve().parent / "tasks"
CANDIDATES_DIR = Path(__file__).resolve().parent / "candidates"
RESULTS_DIR = Path(__file__).resolve().parent / "results"


def compute_truth(task: dict) -> dict:
    """Recompute data-derived golds from the dataset for the given task."""
    data = ROOT / task["data"]
    if task["id"] == "lalonde-recovery":
        rows = lalonde.load(data)
        return {
            "n": len(rows),
            "naive_att": lalonde.naive_att(rows, task["treatment"], task["outcome"]),
            "smd": lalonde.smd_table(rows, task["treatment"]),
        }
    if task["id"] == "card-iv-recovery":
        rows = card.load(data)
        coef, f = card.first_stage(rows)
        return {
            "n": len(rows),
            "ols_return": card.ols_return(rows),
            "iv_return": card.iv_return(rows),
            "first_stage_F": f,
            "first_stage_coef": coef,
        }
    raise ValueError(f"unknown task {task['id']}")


def grade(task: dict, candidate: dict, truth: dict) -> list[dict]:
    out = []
    for g in task["gold"]:
        gid, check = g["id"], g["check"]
        passed, detail = False, ""

        # --- shared / lalonde checks ---
        if check == "imbalance_count":
            thr = g["smd_threshold"]
            n_big = sum(1 for v in candidate.get("balance", {}).values() if abs(v) > thr)
            passed = n_big >= g["min_covariates"]
            detail = f"{n_big} covariates with |SMD|>{thr} (need >= {g['min_covariates']})"

        elif check == "naive_sign":
            v = candidate.get("naive_att")
            want = g["expected_sign"]
            passed = v is not None and ((v < 0) if want == "negative" else (v > 0))
            detail = f"naive_att = {v} (want {want})"

        elif check == "adjusted_recovery":
            naive, adj = candidate.get("naive_att"), candidate.get("adjusted_att")
            if naive is not None and adj is not None:
                swing = adj - naive
                passed = adj > 0 and swing >= g["min_swing"]
                detail = f"adjusted {adj} vs naive {naive} (swing {swing:+.0f}, need +{g['min_swing']:.0f} & positive)"
            else:
                detail = "missing naive_att or adjusted_att"

        elif check == "near_benchmark":
            adj = candidate.get("adjusted_att")
            bench, tol = task["experimental_att"], task["experimental_tol"]
            if adj is not None:
                passed = abs(adj - bench) <= tol
                detail = f"adjusted {adj} vs benchmark {bench} (tol {tol}; |diff|={abs(adj-bench):.0f})"
            else:
                detail = "missing adjusted_att"

        # --- card checks ---
        elif check == "value_near":
            v, exp, tol = candidate.get(g["field"]), g["expected"], g["tol"]
            if v is not None:
                passed = abs(v - exp) <= tol
                detail = f"{g['field']} {v} vs {exp} (tol {tol}; |diff|={abs(v-exp):.4f})"
            else:
                detail = f"missing {g['field']}"

        elif check == "iv_gt_ols":
            ols, iv = candidate.get("ols_return"), candidate.get("iv_return")
            if ols is not None and iv is not None:
                passed = iv > 0 and iv > ols
                detail = f"iv {iv:.4f} {'>' if iv > ols else '<='} ols {ols:.4f}"
            else:
                detail = "missing ols_return or iv_return"

        elif check == "first_stage_min":
            f = candidate.get("first_stage_F")
            if f is not None:
                passed = f >= g["min_f"]
                detail = f"first-stage F {f} (need >= {g['min_f']})"
            else:
                detail = "missing first_stage_F"

        # --- shared anti-fabrication cross-check ---
        elif check == "cross_check":
            problems = []
            if task["id"] == "lalonde-recovery":
                rn = candidate.get("naive_att")
                if rn is None or abs(rn - truth["naive_att"]) > g["naive_tol"]:
                    problems.append(f"naive_att {rn} vs true {truth['naive_att']:.1f}")
                rbal = candidate.get("balance", {})
                for k, tv in truth["smd"].items():
                    rv = rbal.get(k)
                    if rv is None or abs(rv - tv) > g["smd_tol"]:
                        problems.append(f"SMD[{k}] {rv} vs true {tv:.3f}")
            else:  # card
                for field in ("ols_return", "iv_return"):
                    rv = candidate.get(field)
                    if rv is None or abs(rv - truth[field]) > g["tol"]:
                        problems.append(f"{field} {rv} vs true {truth[field]:.4f}")
                rf = candidate.get("first_stage_F")
                if rf is None or abs(rf - truth["first_stage_F"]) > g["f_tol"]:
                    problems.append(f"first_stage_F {rf} vs true {truth['first_stage_F']:.2f}")
            passed = not problems
            detail = "reported numbers match data" if passed else "; ".join(problems[:3])

        else:
            detail = f"unknown check {check}"

        out.append({"id": gid, "required": g.get("required", False),
                    "weight": g.get("weight", 1), "passed": passed, "detail": detail})
    return out


def grade_task(task_path: Path, candidate_override: str | None, strict: bool) -> tuple[int, list[str]]:
    with task_path.open("rb") as fh:
        task = tomllib.load(fh)
    cand_dir = candidate_override or task.get("reference_candidate", "")
    results_json = (CANDIDATES_DIR / cand_dir / "results.json") if cand_dir else None
    if not results_json or not results_json.exists():
        print(f"[{task['id']}] no candidate results.json at {results_json}", file=sys.stderr)
        print("  Run: python3 benchmark/reference_pipeline.py", file=sys.stderr)
        return 1, [task["id"]]
    candidate = json.loads(results_json.read_text(encoding="utf-8"))
    truth = compute_truth(task)
    graded = grade(task, candidate, truth)
    earned = sum(g["weight"] for g in graded if g["passed"])
    possible = sum(g["weight"] for g in graded)
    req_fail = [g["id"] for g in graded if g["required"] and not g["passed"]]

    print(f"Benchmark: {task['id']}  (candidate: {results_json.parent.name}, N={truth['n']})")
    print("-" * 72)
    for g in graded:
        mark = "PASS" if g["passed"] else "FAIL"
        req = "*" if g["required"] else " "
        print(f"  [{mark}]{req} {g['id']:32s} {g['detail']}")
    print(f"Score: {earned}/{possible}  |  required failures: {req_fail or 'none'}")
    print()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / f"{task['id']}.json").write_text(
        json.dumps({"task": task["id"], "candidate": results_json.parent.name,
                    "earned": earned, "possible": possible,
                    "required_failures": req_fail, "items": graded}, indent=2) + "\n",
        encoding="utf-8")
    return (1 if (req_fail and strict) else 0), req_fail


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Grade AERS benchmark candidates")
    ap.add_argument("--task", help="grade only this task id (default: all)")
    ap.add_argument("--candidate", help="override candidate dir name under benchmark/candidates/")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)

    tasks = sorted(TASKS_DIR.glob("*.toml"))
    if args.task:
        tasks = [t for t in tasks if t.stem == args.task]
        if not tasks:
            print(f"No task '{args.task}'", file=sys.stderr)
            return 1

    rc = 0
    for t in tasks:
        code, _ = grade_task(t, args.candidate, args.strict)
        rc = rc or code
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
