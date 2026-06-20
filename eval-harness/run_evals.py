#!/usr/bin/env python3
"""AERS skill evaluation harness.

Skills in this repo are prompt-context, not executable code, so we evaluate them
with *rubrics*: per-skill scenarios that pin down what an agent following the
skill must (and must not) produce. Each rubric item is either machine-checkable
(deterministic regex / word-count / numeric assertions, see ``lib/checks.py``)
or ``manual`` (routed to a human or LLM judge).

Three things this harness does, none of which need an API key:

1. ``lint`` (default) -- validate every scenario, confirm the skill-under-test
   and any fixture data exist on disk, confirm every machine-checkable rubric
   item is well-formed, and emit a coverage report. This is what CI runs.
2. ``--grade DIR`` -- score candidate agent outputs (``DIR/<scenario_id>.md``)
   against the machine-checkable rubric items and write a scorecard. Items that
   need judgement are reported as ``manual`` rather than silently passed.
3. ``--judge-prompts DIR`` -- emit a ready-to-paste judge prompt per scenario
   (scenario + rubric + candidate) so an external LLM or human can grade the
   manual items.

Usage:
    python3 eval-harness/run_evals.py                 # lint + coverage
    python3 eval-harness/run_evals.py --min-scenarios 17 --min-auto-checks 80 \
        --expect-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity
    python3 eval-harness/run_evals.py --list
    python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example
    python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example \
        --expect-graded 8 --expect-fail-required statspai-weak-iv \
        --expect-graded-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity \
        --fail-on-orphans --fail-on-partial --no-write
    python3 eval-harness/run_evals.py --judge-prompts /tmp/judge \
        --grade eval-harness/candidates/_example
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import toml_compat as tomllib  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from checks import ALL_CHECKS, AUTO_CHECKS, MANUAL_CHECK, run_check  # noqa: E402

EVALS_DIR = ROOT / "eval-harness"
SCENARIO_DIR = EVALS_DIR / "scenarios"
RESULTS_DIR = EVALS_DIR / "results"


def rel(path: Path) -> str:
    """Repo-relative posix path when possible, else absolute."""
    p = path.resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)

REQUIRED_SCENARIO_FIELDS = ("id", "skill", "title", "category", "severity", "prompt", "rubric")
SEVERITIES = {"critical", "high", "medium", "low"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SIGNS = {"positive", "negative", "zero"}
UNITS = {"words", "chars", "cjk"}


class ScenarioError(Exception):
    pass


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_regex(sid: str, rid: str, field: str, pattern: Any) -> list[str]:
    if not isinstance(pattern, str):
        return [f"{sid}/{rid}: {field} must be a string"]
    try:
        re.compile(pattern)
    except re.error as exc:
        return [f"{sid}/{rid}: invalid regex in {field}: {exc}"]
    return []


def validate_repo_relative_path(
    value: Any,
    label: str,
    *,
    must_be_dir: bool = False,
    must_be_file: bool = False,
) -> list[str]:
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
    if must_be_dir and not resolved.is_dir():
        return [f"{label} path must be a directory: {value}"]
    if must_be_file and not resolved.is_file():
        return [f"{label} path must be a file: {value}"]
    return []


def load_scenarios() -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for path in sorted(SCENARIO_DIR.glob("*.toml")):
        with path.open("rb") as fh:
            data = tomllib.load(fh)
        data["_path"] = path.relative_to(ROOT).as_posix()
        scenarios.append(data)
    return scenarios


def validate_scenario(s: dict[str, Any]) -> list[str]:
    """Return a list of problems; empty list means valid."""
    problems: list[str] = []
    sid = s.get("id", s.get("_path", "<unknown>"))

    for field_name in REQUIRED_SCENARIO_FIELDS:
        if not s.get(field_name):
            problems.append(f"{sid}: missing required field '{field_name}'")

    if s.get("id") and not ID_RE.fullmatch(str(s["id"])):
        problems.append(f"{sid}: id must match {ID_RE.pattern}")

    if s.get("severity") and s["severity"] not in SEVERITIES:
        problems.append(f"{sid}: severity '{s['severity']}' not in {sorted(SEVERITIES)}")

    # Filename should match id for predictable candidate lookup.
    if s.get("id") and s.get("_path"):
        stem = Path(s["_path"]).stem
        if stem != s["id"]:
            problems.append(f"{sid}: file stem '{stem}' != id '{s['id']}'")

    # Skill-under-test must exist.
    skill = s.get("skill")
    if "skill" in s:
        problems.extend(validate_repo_relative_path(skill, f"{sid}: skill", must_be_dir=True))

    # Optional fixture data must exist if referenced.
    context_data = s.get("context_data", [])
    if not isinstance(context_data, list):
        problems.append(f"{sid}: context_data must be a list")
        context_data = []
    for i, data_path in enumerate(context_data):
        problems.extend(validate_repo_relative_path(data_path, f"{sid}: context_data[{i}]"))

    rubric: list[Any] = []
    raw_rubric = s.get("rubric")
    if "rubric" not in s:
        problems.append(f"{sid}: rubric has no items")
    elif not isinstance(raw_rubric, list):
        problems.append(f"{sid}: rubric must be a list")
    elif not raw_rubric:
        problems.append(f"{sid}: rubric has no items")
    else:
        rubric = raw_rubric
    seen_ids: set[str] = set()
    for i, item in enumerate(rubric):
        if not isinstance(item, dict):
            problems.append(f"{sid}: rubric[{i}] must be a table/object")
            continue
        rid = item.get("id")
        rubric_label = rid or f"rubric[{i}]"
        if not rid:
            problems.append(f"{sid}: rubric[{i}] missing 'id'")
        elif rid in seen_ids:
            problems.append(f"{sid}: duplicate rubric id '{rid}'")
        else:
            seen_ids.add(rid)
            if not ID_RE.fullmatch(str(rid)):
                problems.append(f"{sid}/{rid}: rubric id must match {ID_RE.pattern}")
        check = item.get("check", MANUAL_CHECK)
        if check not in ALL_CHECKS:
            problems.append(f"{sid}/{rid}: invalid check '{check}'")
        if not item.get("description"):
            problems.append(f"{sid}/{rid}: missing 'description'")
        if "required" in item and not isinstance(item["required"], bool):
            problems.append(f"{sid}/{rid}: required must be boolean")
        if "weight" in item and (not is_number(item["weight"]) or item["weight"] < 0):
            problems.append(f"{sid}/{rid}: weight must be a non-negative number")
        if "section" in item:
            problems.extend(validate_regex(sid, rubric_label, "section", item["section"]))
        # Field-shape checks for auto checks so authoring errors fail fast.
        if check in {"regex_any", "regex_all", "regex_none", "regex_count_max"}:
            if not (item.get("pattern") or item.get("patterns")):
                problems.append(f"{sid}/{rid}: {check} needs 'pattern' or 'patterns'")
            if "pattern" in item:
                problems.extend(validate_regex(sid, rubric_label, "pattern", item["pattern"]))
            if "patterns" in item:
                patterns = item["patterns"]
                if not isinstance(patterns, list):
                    problems.append(f"{sid}/{rid}: patterns must be a list")
                else:
                    for j, pattern in enumerate(patterns):
                        problems.extend(
                            validate_regex(sid, rubric_label, f"patterns[{j}]", pattern)
                        )
        if check == "regex_count_max" and "target" not in item:
            problems.append(f"{sid}/{rid}: regex_count_max needs 'target'")
        elif check == "regex_count_max" and not is_number(item.get("target")):
            problems.append(f"{sid}/{rid}: regex_count_max target must be numeric")
        if check == "regex_count_max" and "per_chars" in item and not is_number(item["per_chars"]):
            problems.append(f"{sid}/{rid}: per_chars must be numeric")
        if check in {"word_count_max", "word_count_min"} and "target" not in item:
            problems.append(f"{sid}/{rid}: {check} needs 'target'")
        elif check in {"word_count_max", "word_count_min"} and not is_number(item.get("target")):
            problems.append(f"{sid}/{rid}: {check} target must be numeric")
        if check in {"word_count_max", "word_count_min"} and item.get("unit", "words") not in UNITS:
            problems.append(f"{sid}/{rid}: unit must be one of {sorted(UNITS)}")
        if check == "numeric_tolerance" and not ({"extract", "expected"} <= item.keys()):
            problems.append(f"{sid}/{rid}: numeric_tolerance needs 'extract' and 'expected'")
        if check == "numeric_tolerance":
            if "extract" in item:
                problems.extend(validate_regex(sid, rubric_label, "extract", item["extract"]))
            if "expected" in item and not is_number(item["expected"]):
                problems.append(f"{sid}/{rid}: expected must be numeric")
            if "tol" in item and not is_number(item["tol"]):
                problems.append(f"{sid}/{rid}: tol must be numeric")
        if check == "numeric_sign" and "extract" not in item:
            problems.append(f"{sid}/{rid}: numeric_sign needs 'extract'")
        if check == "numeric_sign":
            if "extract" in item:
                problems.extend(validate_regex(sid, rubric_label, "extract", item["extract"]))
            if "sign" in item and item["sign"] not in SIGNS:
                problems.append(f"{sid}/{rid}: sign must be one of {sorted(SIGNS)}")

    return problems


def rubric_stats(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    auto = manual = total = 0
    per_skill: dict[str, int] = {}
    per_severity: dict[str, int] = {}
    per_category: dict[str, int] = {}
    for s in scenarios:
        per_skill[s["skill"]] = per_skill.get(s["skill"], 0) + 1
        per_severity[s.get("severity", "?")] = per_severity.get(s.get("severity", "?"), 0) + 1
        per_category[s.get("category", "?")] = per_category.get(s.get("category", "?"), 0) + 1
        for item in s.get("rubric", []):
            total += 1
            if item.get("check", MANUAL_CHECK) in AUTO_CHECKS:
                auto += 1
            else:
                manual += 1
    return {
        "scenarios": len(scenarios),
        "rubric_items": total,
        "auto_checkable": auto,
        "manual": manual,
        "skills_covered": len(per_skill),
        "per_skill": per_skill,
        "per_severity": per_severity,
        "per_category": per_category,
    }


def grade_candidate(s: dict[str, Any], candidate_dir: Path, judge=None) -> dict[str, Any]:
    sid = s["id"]
    cand_path = None
    for ext in (".md", ".txt"):
        p = candidate_dir / f"{sid}{ext}"
        if p.exists():
            cand_path = p
            break
    if cand_path is None:
        return {"id": sid, "skill": s["skill"], "category": s.get("category"),
                "status": "no-candidate",
                "items": [], "auto_score": None}

    text = cand_path.read_text(encoding="utf-8", errors="replace")

    # Optional LLM judge verdicts for manual (and any other) items.
    verdicts: dict[str, dict] = {}
    judge_note = ""
    if judge is not None and any(i.get("check", MANUAL_CHECK) == MANUAL_CHECK for i in s["rubric"]):
        try:
            verdicts = judge(emit_judge_prompt(s, candidate_dir))
        except Exception as exc:  # network/parse failure must not crash the run
            judge_note = f"judge unavailable: {exc}"

    items_out = []
    earned = possible = 0.0
    required_failed = []
    manual_items = []
    for item in s["rubric"]:
        res = run_check(item, text)
        status, detail, evidence = res.status, res.detail, res.evidence
        # A judge can resolve a manual item into pass/fail.
        if status == "manual" and res.item_id in verdicts:
            v = verdicts[res.item_id]
            verdict = str(v.get("verdict", "")).lower()
            if verdict in {"pass", "fail"}:
                status = verdict
                detail = "judge: " + str(v.get("why", "")).strip()
        items_out.append({
            "id": res.item_id, "status": status, "weight": res.weight,
            "required": res.required, "detail": detail, "evidence": evidence,
        })
        if status in {"pass", "fail"}:
            possible += res.weight
            if status == "pass":
                earned += res.weight
            elif res.required:
                required_failed.append(res.item_id)
        elif status == "manual":
            manual_items.append(res.item_id)
    auto_score = (earned / possible) if possible else None
    status = "pass"
    if required_failed:
        status = "fail-required"
    elif auto_score is not None and auto_score < 1.0:
        status = "partial"
    elif manual_items:
        status = "needs-manual"
    out = {
        "id": sid, "skill": s["skill"], "category": s.get("category"),
        "candidate": rel(cand_path),
        "status": status, "auto_score": auto_score, "earned": earned, "possible": possible,
        "required_failed": required_failed, "manual_items": manual_items, "items": items_out,
    }
    if judge_note:
        out["judge_note"] = judge_note
    return out


def orphan_candidate_files(candidate_dir: Path, scenarios: list[dict[str, Any]]) -> list[Path]:
    """Candidate .md/.txt files whose stem does not match any scenario id."""
    scenario_ids = {s["id"] for s in scenarios}
    orphans = []
    for pattern in ("*.md", "*.txt"):
        for path in candidate_dir.glob(pattern):
            if path.stem not in scenario_ids:
                orphans.append(path)
    return sorted(orphans)


def parse_judge_response(text: str) -> dict[str, Any]:
    """Extract the JSON verdict object from a (possibly fenced) LLM reply.

    Returns a dict keyed by rubric item id -> {verdict, why}. Tolerant of
    ```json fences and surrounding prose; raises ValueError if no JSON found.
    """
    cleaned = text.strip()
    # Strip a leading/trailing code fence if present.
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", cleaned, re.DOTALL)
    blob = fence.group(1) if fence else None
    if blob is None:
        start, depth = cleaned.find("{"), 0
        if start == -1:
            raise ValueError("no JSON object in judge response")
        for i in range(start, len(cleaned)):
            depth += (cleaned[i] == "{") - (cleaned[i] == "}")
            if depth == 0:
                blob = cleaned[start:i + 1]
                break
    data = json.loads(blob)
    return {str(it.get("id")): it for it in (data.get("items") or []) if it.get("id")}


def make_anthropic_judge(model: str):
    """Return a callable(prompt)->verdict-map backed by the Anthropic SDK, or
    None if the SDK or ANTHROPIC_API_KEY is unavailable (graceful degrade)."""
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic  # type: ignore
    except ImportError:
        return None
    client = anthropic.Anthropic()

    def judge(prompt: str) -> dict[str, Any]:
        msg = client.messages.create(
            model=model, max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(getattr(b, "text", "") for b in msg.content)
        return parse_judge_response(text)

    return judge


def emit_judge_prompt(s: dict[str, Any], candidate_dir: Path | None) -> str:
    lines = [
        f"# Judge prompt: {s['id']}",
        "",
        f"You are grading an agent's output against the skill "
        f"`{s['skill']}`. Be a strict, fair econometrics referee.",
        "",
        "## Task given to the agent",
        "",
        s["prompt"].strip(),
        "",
        "## Rubric (score each item PASS/FAIL with one sentence of justification)",
        "",
    ]
    for item in s["rubric"]:
        flag = " (REQUIRED)" if item.get("required") else ""
        lines.append(f"- [{item['id']}]{flag} {item['description']}")
    lines.append("")
    if candidate_dir:
        for ext in (".md", ".txt"):
            p = candidate_dir / f"{s['id']}{ext}"
            if p.exists():
                candidate_text = p.read_text(encoding="utf-8", errors="replace").strip()
                lines += ["## Candidate output", "", "```", candidate_text, "```", ""]
                break
    lines += ["## Output format", "",
              "Return a JSON object: {\"items\": [{\"id\": ..., \"verdict\": \"pass|fail\", "
              "\"why\": ...}], \"overall\": \"pass|partial|fail\"}."]
    return "\n".join(lines)


def cmd_lint(scenarios: list[dict[str, Any]], strict: bool) -> int:
    problems: list[str] = []
    for s in scenarios:
        problems.extend(validate_scenario(s))
    stats = rubric_stats(scenarios) if scenarios else {}
    print(f"Loaded {len(scenarios)} scenario(s) from {SCENARIO_DIR.relative_to(ROOT)}/")
    if scenarios:
        print(f"  rubric items: {stats['rubric_items']} "
              f"({stats['auto_checkable']} auto-checkable, {stats['manual']} manual)")
        print(f"  skills covered: {stats['skills_covered']}")
        print(f"  by severity: {stats['per_severity']}")
        print(f"  by category: {stats['per_category']}")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nAll scenarios valid.")
    return 0


def write_results(graded: list[dict[str, Any]], stats: dict[str, Any]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"summary": stats, "scenarios": graded}
    (RESULTS_DIR / "results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = ["# Eval results", "",
          "Generated by `eval-harness/run_evals.py --grade`. Machine-checkable rubric items "
          "only; `manual` items still need a human or LLM judge.", "",
          "| Scenario | Category | Skill | Status | Auto-score | Required-fails | Manual |",
          "|---|---|---|---|---:|---|---:|"]
    for g in graded:
        score = "-" if g.get("auto_score") is None else f"{g['auto_score']*100:.0f}%"
        rf = ", ".join(g.get("required_failed", [])) or "-"
        manual = len(g.get("manual_items", []))
        md.append(f"| `{g['id']}` | {g.get('category') or '-'} | "
                  f"{g['skill'].split('/')[-1] or g['skill']} | "
                  f"{g['status']} | {score} | {rf} | {manual} |")
    (RESULTS_DIR / "RESULTS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {RESULTS_DIR.relative_to(ROOT)}/results.json and RESULTS.md")


def parse_expected_failures(raw: str | None) -> set[str]:
    if not raw:
        return set()
    return {part.strip() for part in raw.split(",") if part.strip()}


def parse_expected_categories(raw: str | None) -> set[str]:
    if not raw:
        return set()
    return {part.strip() for part in raw.split(",") if part.strip()}


def coverage_gate_problems(
    scenarios: list[dict[str, Any]],
    *,
    min_scenarios: int | None = None,
    min_auto_checks: int | None = None,
    expect_categories: str | None = None,
) -> list[str]:
    problems: list[str] = []
    stats = rubric_stats(scenarios) if scenarios else {
        "auto_checkable": 0,
        "per_category": {},
    }
    if min_scenarios is not None:
        if min_scenarios < 0:
            problems.append("--min-scenarios must be non-negative")
        elif len(scenarios) < min_scenarios:
            problems.append(f"expected at least {min_scenarios} scenario(s), got {len(scenarios)}")
    if min_auto_checks is not None:
        auto = int(stats["auto_checkable"])
        if min_auto_checks < 0:
            problems.append("--min-auto-checks must be non-negative")
        elif auto < min_auto_checks:
            problems.append(f"expected at least {min_auto_checks} auto-check(s), got {auto}")
    if expect_categories is not None:
        expected = parse_expected_categories(expect_categories)
        categories = set(stats["per_category"])
        missing = sorted(expected - categories)
        if missing:
            problems.append(f"missing scenario categories: {', '.join(missing)}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="AERS skill evaluation harness")
    ap.add_argument("--list", action="store_true", help="list scenarios and exit")
    ap.add_argument("--grade", metavar="DIR", help="score candidate outputs in DIR")
    ap.add_argument("--judge-prompts", metavar="DIR", help="write judge prompts to DIR")
    ap.add_argument(
        "--judge",
        action="store_true",
        help="auto-grade manual items with an LLM judge (needs ANTHROPIC_API_KEY + SDK)",
    )
    ap.add_argument("--judge-model", default="claude-sonnet-4-6", help="model id for --judge")
    ap.add_argument("--expect-fail-required",
                    help="comma-separated scenario ids expected to fail required items")
    ap.add_argument("--expect-graded", type=int, help="expected number of candidate files graded")
    ap.add_argument(
        "--expect-graded-categories",
        help="comma-separated scenario categories that must have at least one graded candidate",
    )
    ap.add_argument(
        "--fail-on-orphans",
        action="store_true",
        help="fail if DIR contains .md/.txt files that do not match a scenario id",
    )
    ap.add_argument(
        "--fail-on-partial",
        action="store_true",
        help="fail if any graded candidate has non-required machine-check failures",
    )
    ap.add_argument(
        "--no-write",
        action="store_true",
        help="grade candidates without writing eval-harness/results scorecards",
    )
    ap.add_argument(
        "--min-scenarios",
        type=int,
        help="coverage gate: require at least this many scenario files",
    )
    ap.add_argument(
        "--min-auto-checks",
        type=int,
        help="coverage gate: require at least this many auto-checkable rubric items",
    )
    ap.add_argument(
        "--expect-categories",
        help="coverage gate: comma-separated scenario categories that must exist",
    )
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    if not SCENARIO_DIR.exists():
        print(f"No scenario directory at {SCENARIO_DIR}", file=sys.stderr)
        return 1

    scenarios = load_scenarios()

    # Always lint first; a malformed scenario should never be graded.
    lint_problems = [p for s in scenarios for p in validate_scenario(s)]
    if lint_problems and (args.grade or args.judge_prompts):
        print("Refusing to grade: scenarios have validation problems:", file=sys.stderr)
        for p in lint_problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    coverage_problems = coverage_gate_problems(
        scenarios,
        min_scenarios=args.min_scenarios,
        min_auto_checks=args.min_auto_checks,
        expect_categories=args.expect_categories,
    )
    if coverage_problems:
        print("Coverage expectation mismatch:", file=sys.stderr)
        for problem in coverage_problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    if args.list:
        for s in scenarios:
            print(f"{s['id']:36s} {s.get('severity',''):8s} {s['skill']}")
        return 0

    candidate_dir = None
    if args.grade:
        candidate_dir = Path(args.grade)
        if not candidate_dir.exists():
            print(f"Candidate dir not found: {candidate_dir}", file=sys.stderr)
            return 1
        if not candidate_dir.is_dir():
            print(f"Candidate path is not a directory: {candidate_dir}", file=sys.stderr)
            return 1

    if args.judge_prompts:
        out = Path(args.judge_prompts)
        if out.exists() and not out.is_dir():
            print(f"Judge prompt output path is not a directory: {out}", file=sys.stderr)
            return 1
        out.mkdir(parents=True, exist_ok=True)
        for s in scenarios:
            (out / f"{s['id']}.md").write_text(
                emit_judge_prompt(s, candidate_dir),
                encoding="utf-8",
            )
        print(f"Wrote {len(scenarios)} judge prompt(s) to {out}")

    if args.grade:
        cand = candidate_dir
        assert cand is not None
        orphans = orphan_candidate_files(cand, scenarios)
        if orphans:
            print(
                f"Found {len(orphans)} candidate file(s) with no matching scenario:",
                file=sys.stderr,
            )
            for path in orphans:
                print(f"  - {rel(path)}", file=sys.stderr)
            if args.fail_on_orphans:
                return 1
        judge = None
        if args.judge:
            judge = make_anthropic_judge(args.judge_model)
            if judge is None:
                print("--judge requested but no judge available "
                      "(set ANTHROPIC_API_KEY and `pip install anthropic`); "
                      "grading machine-checkable items only.", file=sys.stderr)
            else:
                print(f"Judging manual items with {args.judge_model}…")
        graded = [grade_candidate(s, cand, judge=judge) for s in scenarios]
        stats = rubric_stats(scenarios)
        n_graded = sum(1 for g in graded if g["status"] != "no-candidate")
        failed_ids = {g["id"] for g in graded if g["status"] == "fail-required"}
        partial_ids = {g["id"] for g in graded if g["status"] == "partial"}
        graded_categories = {
            str(g.get("category"))
            for g in graded
            if g["status"] != "no-candidate" and g.get("category")
        }
        if args.no_write:
            print("Scorecard write skipped (--no-write).")
        else:
            write_results(graded, stats)
        print(f"\nGraded {n_graded}/{len(graded)} scenario(s); "
              f"{len(failed_ids)} with required-item failures.")
        if args.expect_graded is not None and n_graded != args.expect_graded:
            print(
                f"Expected to grade {args.expect_graded} scenario(s), got {n_graded}.",
                file=sys.stderr,
            )
            return 1
        if args.expect_graded_categories is not None:
            expected_categories = parse_expected_categories(args.expect_graded_categories)
            missing_categories = sorted(expected_categories - graded_categories)
            if missing_categories:
                print("Graded-category expectation mismatch:", file=sys.stderr)
                print(f"  missing categories: {', '.join(missing_categories)}", file=sys.stderr)
                print(
                    f"  graded categories: {', '.join(sorted(graded_categories)) or 'none'}",
                    file=sys.stderr,
                )
                return 1
        if args.fail_on_partial and partial_ids:
            print("Partial-score candidate(s) found:", file=sys.stderr)
            print(f"  {', '.join(sorted(partial_ids))}", file=sys.stderr)
            return 1
        if args.expect_fail_required is not None:
            expected = parse_expected_failures(args.expect_fail_required)
            unexpected = sorted(failed_ids - expected)
            missing = sorted(expected - failed_ids)
            if unexpected or missing:
                print("Required-failure expectation mismatch:", file=sys.stderr)
                if unexpected:
                    print(f"  unexpected failures: {', '.join(unexpected)}", file=sys.stderr)
                if missing:
                    print(f"  expected failures missing: {', '.join(missing)}", file=sys.stderr)
                return 1
        return 1 if (failed_ids and args.strict) else 0

    return cmd_lint(scenarios, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
