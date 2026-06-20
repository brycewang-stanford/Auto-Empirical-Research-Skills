#!/usr/bin/env python3
"""Grade candidate results against AERS benchmark tasks.

A "candidate" is a results.json produced by any pipeline (the reference pipeline,
the repo's demo outputs, or a real agent run). For each task the checker
recomputes the data-derived golds from the dataset itself, so a candidate cannot
pass by reporting fabricated numbers. Literature constants (the LaLonde
experimental benchmark, the Card canonical values) come from the task specs.

Usage:
    python3 benchmark/reference_pipeline.py            # produce reference candidates
    python3 benchmark/check_benchmark.py --lint        # validate task + candidate metadata only
    python3 benchmark/check_benchmark.py               # grade all tasks
    python3 benchmark/check_benchmark.py --task card-iv-recovery
    python3 benchmark/check_benchmark.py --strict      # nonzero exit on required fail
    python3 benchmark/check_benchmark.py --strict --fail-on-partial --fail-on-orphan-results
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from numbers import Real
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import toml_compat as tomllib  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import lalonde  # noqa: E402
import card  # noqa: E402
import simdid  # noqa: E402
import rdd  # noqa: E402
import badcontrol  # noqa: E402

TASKS_DIR = Path(__file__).resolve().parent / "tasks"
CANDIDATES_DIR = Path(__file__).resolve().parent / "candidates"
RESULTS_DIR = Path(__file__).resolve().parent / "results"

SUPPORTED_TASK_IDS = {
    "bad-control-recovery",
    "card-iv-recovery",
    "did-staggered-recovery",
    "lalonde-recovery",
    "rdd-recovery",
}
CANDIDATE_DIR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
KNOWN_CHECKS = {
    "adjusted_recovery",
    "biased_away",
    "closer_to_truth",
    "cross_check",
    "first_stage_min",
    "imbalance_count",
    "iv_gt_ols",
    "naive_sign",
    "near_benchmark",
    "recovers_truth",
    "value_near",
}

REQUIRED_TASK_FIELDS = ("id", "title", "data", "reference_candidate", "gold")
REQUIRED_GOLD_FIELDS = ("id", "description", "check", "required", "weight")
TASK_STRING_FIELDS = {
    "lalonde-recovery": ("treatment", "outcome"),
}
TASK_NUMERIC_FIELDS = {
    "lalonde-recovery": ("experimental_att", "experimental_tol"),
}
CHECK_REQUIRED_FIELDS = {
    "adjusted_recovery": ("min_swing",),
    "biased_away": ("field", "truth_key", "min_gap"),
    "closer_to_truth": ("near_field", "far_field", "truth_key"),
    "cross_check": (),
    "first_stage_min": ("min_f",),
    "imbalance_count": ("min_covariates", "smd_threshold"),
    "iv_gt_ols": (),
    "naive_sign": ("expected_sign",),
    "near_benchmark": (),
    "recovers_truth": ("field", "truth_key", "tol"),
    "value_near": ("field", "expected", "tol"),
}
CHECK_STRING_FIELDS = {
    "biased_away": ("field", "truth_key"),
    "closer_to_truth": ("near_field", "far_field", "truth_key"),
    "naive_sign": ("expected_sign",),
    "recovers_truth": ("field", "truth_key"),
    "value_near": ("field",),
}
CHECK_NUMERIC_FIELDS = {
    "adjusted_recovery": ("min_swing",),
    "biased_away": ("min_gap",),
    "first_stage_min": ("min_f",),
    "imbalance_count": ("smd_threshold",),
    "recovers_truth": ("tol",),
    "value_near": ("expected", "tol"),
}
CROSS_CHECK_NUMERIC_FIELDS = {
    "bad-control-recovery": ("tol",),
    "card-iv-recovery": ("tol", "f_tol"),
    "did-staggered-recovery": ("tol",),
    "lalonde-recovery": ("naive_tol", "smd_tol"),
    "rdd-recovery": ("tol",),
}
CANDIDATE_NUMERIC_FIELDS = {
    "bad-control-recovery": ("true_total", "naive_effect", "good_control_effect", "bad_control_effect"),
    "card-iv-recovery": ("ols_return", "iv_return", "first_stage_F", "first_stage_coef"),
    "did-staggered-recovery": ("true_att", "twfe_att", "cs_att"),
    "lalonde-recovery": ("naive_att", "adjusted_att"),
    "rdd-recovery": ("true_tau", "naive_jump", "global_att", "local_att"),
}
CANDIDATE_NUMERIC_MAP_FIELDS = {
    "lalonde-recovery": ("balance",),
}


def _is_number(value: object) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)


def validate_candidate_dir_name(value: object, label: str = "candidate") -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{label} must be a non-empty string"]
    if not CANDIDATE_DIR_RE.fullmatch(value):
        return [
            f"{label} '{value}' must be a single directory name matching {CANDIDATE_DIR_RE.pattern}"
        ]
    return []


def validate_repo_relative_file(value: object, label: str) -> list[str]:
    if not isinstance(value, str) or not value:
        return [f"{label} must be a non-empty string"]
    raw_path = Path(value)
    if raw_path.is_absolute():
        return [f"{label} '{value}' must be repo-relative, not absolute"]
    root = ROOT.resolve()
    resolved = (ROOT / raw_path).resolve(strict=False)
    try:
        resolved.relative_to(root)
    except ValueError:
        return [f"{label} '{value}' must stay inside the repository"]
    if not resolved.exists():
        return [f"{label} path does not exist: {value}"]
    if not resolved.is_file():
        return [f"{label} path must be a file: {value}"]
    return []


def orphan_result_files(results_dir: Path, task_ids: set[str]) -> list[Path]:
    """Generated result JSON files whose stem no longer matches a benchmark task."""
    if not results_dir.exists():
        return []
    return sorted(path for path in results_dir.glob("*.json") if path.stem not in task_ids)


def validate_task(task: dict, task_path: Path) -> list[str]:
    """Validate a benchmark task spec before scoring candidates."""
    problems = []
    if not isinstance(task, dict):
        return [f"{task_path} must contain a TOML table"]

    for field in REQUIRED_TASK_FIELDS:
        if field not in task:
            problems.append(f"missing top-level field '{field}'")

    task_id = task.get("id")
    if not isinstance(task_id, str) or not task_id:
        problems.append("field 'id' must be a non-empty string")
    elif task_id != task_path.stem:
        problems.append(f"field 'id' must match file stem '{task_path.stem}'")
    elif task_id not in SUPPORTED_TASK_IDS:
        problems.append(f"unsupported task id '{task_id}'")

    for field in ("title", "data", "reference_candidate"):
        value = task.get(field)
        if field in task and (not isinstance(value, str) or not value.strip()):
            problems.append(f"field '{field}' must be a non-empty string")

    if "reference_candidate" in task:
        problems.extend(validate_candidate_dir_name(task.get("reference_candidate"), "reference_candidate"))

    if isinstance(task_id, str):
        for field in TASK_STRING_FIELDS.get(task_id, ()):
            value = task.get(field)
            if not isinstance(value, str) or not value.strip():
                problems.append(f"field '{field}' must be a non-empty string")
        for field in TASK_NUMERIC_FIELDS.get(task_id, ()):
            value = task.get(field)
            if not _is_number(value):
                problems.append(f"field '{field}' must be numeric")

    if "data" in task:
        problems.extend(validate_repo_relative_file(task.get("data"), "data"))

    gold = task.get("gold")
    if not isinstance(gold, list) or not gold:
        problems.append("field 'gold' must be a non-empty list")
        return problems

    seen_gold_ids = set()
    for idx, item in enumerate(gold):
        prefix = f"gold[{idx}]"
        if not isinstance(item, dict):
            problems.append(f"{prefix} must be a table")
            continue

        for field in REQUIRED_GOLD_FIELDS:
            if field not in item:
                problems.append(f"{prefix} missing field '{field}'")

        gid = item.get("id")
        if not isinstance(gid, str) or not gid:
            problems.append(f"{prefix} field 'id' must be a non-empty string")
        elif gid in seen_gold_ids:
            problems.append(f"{prefix} duplicate id '{gid}'")
        else:
            seen_gold_ids.add(gid)

        description = item.get("description")
        if "description" in item and (not isinstance(description, str) or not description.strip()):
            problems.append(f"{prefix} field 'description' must be a non-empty string")

        required = item.get("required")
        if "required" in item and not isinstance(required, bool):
            problems.append(f"{prefix} field 'required' must be a boolean")

        weight = item.get("weight")
        if "weight" in item and (not _is_number(weight) or weight <= 0):
            problems.append(f"{prefix} field 'weight' must be a positive number")

        check = item.get("check")
        if not isinstance(check, str) or not check:
            problems.append(f"{prefix} field 'check' must be a non-empty string")
            continue
        if check not in KNOWN_CHECKS:
            problems.append(f"{prefix} unknown check '{check}'")
            continue

        for field in CHECK_REQUIRED_FIELDS[check]:
            if field not in item:
                problems.append(f"{prefix} check '{check}' missing field '{field}'")

        if check == "naive_sign" and item.get("expected_sign") not in {"negative", "positive"}:
            problems.append(f"{prefix} expected_sign must be 'negative' or 'positive'")
        if check == "imbalance_count" and not isinstance(item.get("min_covariates"), int):
            problems.append(f"{prefix} min_covariates must be an integer")

        for field in CHECK_STRING_FIELDS.get(check, ()):
            value = item.get(field)
            if field in item and (not isinstance(value, str) or not value.strip()):
                problems.append(f"{prefix} field '{field}' must be a non-empty string")
        for field in CHECK_NUMERIC_FIELDS.get(check, ()):
            value = item.get(field)
            if field in item and not _is_number(value):
                problems.append(f"{prefix} field '{field}' must be numeric")

        if check == "cross_check" and isinstance(task_id, str):
            for field in CROSS_CHECK_NUMERIC_FIELDS.get(task_id, ()):
                value = item.get(field)
                if field not in item:
                    problems.append(f"{prefix} check 'cross_check' missing field '{field}'")
                elif not _is_number(value):
                    problems.append(f"{prefix} field '{field}' must be numeric")

    return problems


def validate_candidate(task: dict, candidate: dict, candidate_path: Path) -> list[str]:
    """Validate candidate result metadata before comparing reported numbers."""
    problems = []
    if not isinstance(candidate, dict):
        return [f"{candidate_path} must contain a JSON object"]

    candidate_task = candidate.get("task")
    if not isinstance(candidate_task, str) or not candidate_task:
        problems.append("candidate field 'task' must be a non-empty string")
    elif candidate_task != task["id"]:
        problems.append(f"candidate task '{candidate_task}' does not match benchmark task '{task['id']}'")

    task_id = task.get("id")
    for field in CANDIDATE_NUMERIC_FIELDS.get(task_id, ()):
        if field in candidate and not _is_number(candidate[field]):
            problems.append(f"candidate field '{field}' must be numeric")

    for field in CANDIDATE_NUMERIC_MAP_FIELDS.get(task_id, ()):
        if field not in candidate:
            continue
        value = candidate[field]
        if not isinstance(value, dict):
            problems.append(f"candidate field '{field}' must be an object of numeric values")
            continue
        for key, item in value.items():
            if not isinstance(key, str) or not key:
                problems.append(f"candidate field '{field}' has a non-string or empty key")
            if not _is_number(item):
                problems.append(f"candidate field '{field}.{key}' must be numeric")

    return problems


def compute_truth(task: dict) -> dict:
    """Recompute data-derived golds from the dataset for the given task."""
    if task["id"] == "lalonde-recovery":
        data = ROOT / task["data"]
        rows = lalonde.load(data)
        return {
            "n": len(rows),
            "naive_att": lalonde.naive_att(rows, task["treatment"], task["outcome"]),
            "smd": lalonde.smd_table(rows, task["treatment"]),
        }
    if task["id"] == "card-iv-recovery":
        data = ROOT / task["data"]
        rows = card.load(data)
        coef, f = card.first_stage(rows)
        return {
            "n": len(rows),
            "ols_return": card.ols_return(rows),
            "iv_return": card.iv_return(rows),
            "first_stage_F": f,
            "first_stage_coef": coef,
        }
    if task["id"] == "did-staggered-recovery":
        data = ROOT / task["data"]
        rows = simdid.load(data)
        return {
            "n": len(rows),
            "true_att": simdid.true_att(rows),
            "twfe_att": simdid.twfe_att(rows),
            "cs_att": simdid.cs_att(rows),
        }
    if task["id"] == "rdd-recovery":
        data = ROOT / task["data"]
        rows = rdd.load(data)
        return {
            "n": len(rows),
            "true_tau": rdd.true_tau(rows),
            "naive_jump": rdd.naive_jump(rows),
            "global_att": rdd.global_att(rows),
            "local_att": rdd.local_att(rows),
        }
    if task["id"] == "bad-control-recovery":
        data = ROOT / task["data"]
        rows = badcontrol.load(data)
        return {
            "n": len(rows),
            "true_total": badcontrol.true_total(rows),
            "naive_effect": badcontrol.naive_effect(rows),
            "good_control_effect": badcontrol.good_control_effect(rows),
            "bad_control_effect": badcontrol.bad_control_effect(rows),
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

        # --- staggered-DID checks ---
        elif check == "recovers_truth":
            field, truth_key, tol = g["field"], g["truth_key"], g["tol"]
            v, exp = candidate.get(field), truth[truth_key]
            if v is not None:
                passed = abs(v - exp) <= tol
                detail = f"{field} {v} vs true {exp:.4f} (tol {tol}; |diff|={abs(v-exp):.4f})"
            else:
                detail = f"missing {field}"

        elif check == "biased_away":
            field, truth_key = g["field"], g["truth_key"]
            v, exp = candidate.get(field), truth[truth_key]
            if v is not None:
                gap = abs(v - exp)
                passed = gap >= g["min_gap"]
                detail = f"{field} {v} vs true {exp:.4f} (gap {gap:.4f})"
            else:
                detail = f"missing {field}"

        elif check == "closer_to_truth":
            near, far = candidate.get(g["near_field"]), candidate.get(g["far_field"])
            exp = truth[g["truth_key"]]
            if near is not None and far is not None:
                near_gap, far_gap = abs(near - exp), abs(far - exp)
                passed = near_gap < far_gap
                detail = f"{g['near_field']} gap {near_gap:.4f} vs {g['far_field']} gap {far_gap:.4f}"
            else:
                detail = f"missing {g['near_field']} or {g['far_field']}"

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
            elif task["id"] == "card-iv-recovery":
                for field in ("ols_return", "iv_return"):
                    rv = candidate.get(field)
                    if rv is None or abs(rv - truth[field]) > g["tol"]:
                        problems.append(f"{field} {rv} vs true {truth[field]:.4f}")
                rf = candidate.get("first_stage_F")
                if rf is None or abs(rf - truth["first_stage_F"]) > g["f_tol"]:
                    problems.append(f"first_stage_F {rf} vs true {truth['first_stage_F']:.2f}")
            elif task["id"] == "did-staggered-recovery":
                for field in ("twfe_att", "cs_att"):
                    rv = candidate.get(field)
                    if rv is None or abs(rv - truth[field]) > g["tol"]:
                        problems.append(f"{field} {rv} vs true {truth[field]:.4f}")
                rt = candidate.get("true_att")
                if rt is not None and abs(rt - truth["true_att"]) > g["tol"]:
                    problems.append(f"true_att {rt} vs true {truth['true_att']:.4f}")
            elif task["id"] == "rdd-recovery":
                for field in ("naive_jump", "global_att", "local_att"):
                    rv = candidate.get(field)
                    if rv is None or abs(rv - truth[field]) > g["tol"]:
                        problems.append(f"{field} {rv} vs true {truth[field]:.4f}")
                rt = candidate.get("true_tau")
                if rt is not None and abs(rt - truth["true_tau"]) > g["tol"]:
                    problems.append(f"true_tau {rt} vs true {truth['true_tau']:.4f}")
            elif task["id"] == "bad-control-recovery":
                for field in ("naive_effect", "good_control_effect", "bad_control_effect"):
                    rv = candidate.get(field)
                    if rv is None or abs(rv - truth[field]) > g["tol"]:
                        problems.append(f"{field} {rv} vs true {truth[field]:.4f}")
                rt = candidate.get("true_total")
                if rt is not None and abs(rt - truth["true_total"]) > g["tol"]:
                    problems.append(f"true_total {rt} vs true {truth['true_total']:.4f}")
            passed = not problems
            detail = "reported numbers match data" if passed else "; ".join(problems[:3])

        else:
            detail = f"unknown check {check}"

        out.append({"id": gid, "required": g.get("required", False),
                    "weight": g.get("weight", 1), "passed": passed, "detail": detail})
    return out


def exit_code_for_failures(
    required_failures: list[str],
    optional_failures: list[str],
    strict: bool,
    fail_on_partial: bool,
) -> int:
    if required_failures and strict:
        return 1
    if optional_failures and fail_on_partial:
        return 1
    return 0


def grade_task(
    task_path: Path,
    candidate_override: str | None,
    strict: bool,
    fail_on_partial: bool,
) -> tuple[int, list[str]]:
    with task_path.open("rb") as fh:
        task = tomllib.load(fh)
    task_id = task.get("id", task_path.stem) if isinstance(task, dict) else task_path.stem
    task_problems = validate_task(task, task_path)
    if task_problems:
        print(f"[{task_id}] invalid benchmark task {task_path}", file=sys.stderr)
        for problem in task_problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1, [task_id]

    cand_dir = candidate_override or task.get("reference_candidate", "")
    candidate_dir_problems = validate_candidate_dir_name(cand_dir, "candidate")
    if candidate_dir_problems:
        print(f"[{task['id']}] invalid candidate directory name", file=sys.stderr)
        for problem in candidate_dir_problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1, [task["id"]]

    results_json = (CANDIDATES_DIR / cand_dir / "results.json") if cand_dir else None
    if not results_json or not results_json.exists():
        print(f"[{task['id']}] no candidate results.json at {results_json}", file=sys.stderr)
        print("  Run: python3 benchmark/reference_pipeline.py", file=sys.stderr)
        return 1, [task["id"]]
    try:
        candidate = json.loads(results_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[{task['id']}] invalid candidate JSON {results_json}", file=sys.stderr)
        print(f"  - {exc.msg} at line {exc.lineno}, column {exc.colno}", file=sys.stderr)
        return 1, [task["id"]]

    candidate_problems = validate_candidate(task, candidate, results_json)
    if candidate_problems:
        print(f"[{task['id']}] invalid candidate {results_json}", file=sys.stderr)
        for problem in candidate_problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1, [task["id"]]

    truth = compute_truth(task)
    graded = grade(task, candidate, truth)
    earned = sum(g["weight"] for g in graded if g["passed"])
    possible = sum(g["weight"] for g in graded)
    req_fail = [g["id"] for g in graded if g["required"] and not g["passed"]]
    opt_fail = [g["id"] for g in graded if not g["required"] and not g["passed"]]

    print(f"Benchmark: {task['id']}  (candidate: {results_json.parent.name}, N={truth['n']})")
    print("-" * 72)
    for g in graded:
        mark = "PASS" if g["passed"] else "FAIL"
        req = "*" if g["required"] else " "
        print(f"  [{mark}]{req} {g['id']:32s} {g['detail']}")
    print(f"Score: {earned}/{possible}  |  required failures: {req_fail or 'none'}")
    if opt_fail:
        print(f"Optional failures: {opt_fail}")
    print()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / f"{task['id']}.json").write_text(
        json.dumps({"task": task["id"], "candidate": results_json.parent.name,
                    "earned": earned, "possible": possible,
                    "required_failures": req_fail,
                    "optional_failures": opt_fail,
                    "items": graded}, indent=2) + "\n",
        encoding="utf-8")
    return exit_code_for_failures(req_fail, opt_fail, strict, fail_on_partial), req_fail


def lint_task(task_path: Path, candidate_override: str | None = None) -> list[str]:
    with task_path.open("rb") as fh:
        task = tomllib.load(fh)
    task_id = task.get("id", task_path.stem) if isinstance(task, dict) else task_path.stem
    problems = [f"{task_id}: {problem}" for problem in validate_task(task, task_path)]
    if problems:
        return problems

    cand_dir = candidate_override or task.get("reference_candidate", "")
    problems.extend(
        f"{task['id']}: {problem}"
        for problem in validate_candidate_dir_name(cand_dir, "candidate")
    )
    if problems:
        return problems

    results_json = CANDIDATES_DIR / cand_dir / "results.json"
    if not results_json.exists():
        return [f"{task['id']}: missing candidate results.json at {results_json.relative_to(ROOT)}"]
    try:
        candidate = json.loads(results_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [
            f"{task['id']}: invalid candidate JSON {results_json.relative_to(ROOT)} "
            f"({exc.msg} at line {exc.lineno}, column {exc.colno})"
        ]
    return [
        f"{task['id']}: {problem}"
        for problem in validate_candidate(task, candidate, results_json)
    ]


def lint_tasks(task_paths: list[Path], candidate_override: str | None = None) -> int:
    problems: list[str] = []
    for task_path in task_paths:
        problems.extend(lint_task(task_path, candidate_override))
    if problems:
        print(f"Benchmark lint found {len(problems)} problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"Benchmark lint passed for {len(task_paths)} task(s).")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Grade AERS benchmark candidates")
    ap.add_argument("--task", help="grade only this task id (default: all)")
    ap.add_argument("--candidate", help="override candidate dir name under benchmark/candidates/")
    ap.add_argument(
        "--lint",
        action="store_true",
        help="validate task specs and reference candidate metadata without scoring",
    )
    ap.add_argument("--strict", action="store_true")
    ap.add_argument(
        "--fail-on-partial",
        action="store_true",
        help="nonzero exit when any non-required gold fails",
    )
    ap.add_argument(
        "--fail-on-orphan-results",
        action="store_true",
        help="nonzero exit when benchmark/results/ contains JSON for no current task",
    )
    args = ap.parse_args(argv)

    all_tasks = sorted(TASKS_DIR.glob("*.toml"))
    task_ids = {path.stem for path in all_tasks}
    orphan_results = orphan_result_files(RESULTS_DIR, task_ids)
    if orphan_results:
        print(
            f"Found {len(orphan_results)} orphan benchmark result file(s):",
            file=sys.stderr,
        )
        for path in orphan_results:
            print(f"  - {path.relative_to(ROOT)}", file=sys.stderr)
        if args.fail_on_orphan_results:
            return 1

    tasks = all_tasks
    if args.task:
        tasks = [t for t in tasks if t.stem == args.task]
        if not tasks:
            print(f"No task '{args.task}'", file=sys.stderr)
            return 1

    if args.lint:
        return lint_tasks(tasks, args.candidate)

    rc = 0
    for t in tasks:
        code, _ = grade_task(t, args.candidate, args.strict, args.fail_on_partial)
        rc = rc or code
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
