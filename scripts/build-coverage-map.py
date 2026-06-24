#!/usr/bin/env python3
"""Generate docs/RIGOR_COVERAGE.md — a methodological rigor coverage map.

AERS already tests methodological correctness in two places: the eval-harness
scenarios (does a skill flag the known pitfall?) and the benchmark tasks (does a
pipeline recover the right number?). This generator joins those with the method
taxonomy in catalog/skills-enriched.json to answer one question per method
family: *how many skills claim this method, and what rigor do we actually test
for it?*

It deliberately surfaces gaps (method families with skills but no eval/benchmark)
and lists any scenario/task it could not classify, so coverage drift stays
visible instead of silently dropping out of the table.

Zero third-party dependencies (TOML via scripts/toml_compat.py). Mirrors the
build-*/--check pattern of the other generators.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import toml_compat

ROOT = Path(__file__).resolve().parents[1]
ENRICHED = ROOT / "catalog" / "skills-enriched.json"
SCENARIO_DIR = ROOT / "eval-harness" / "scenarios"
TASK_DIR = ROOT / "benchmark" / "tasks"
OUT = ROOT / "docs" / "RIGOR_COVERAGE.md"

# Method families presented as rows, in this order. Keys match taxonomy.method.
METHOD_ORDER = [
    "iv",
    "rdd",
    "did",
    "staggered-did",
    "event-study",
    "panel-fe",
    "synthetic-control",
    "matching",
    "dml",
    "bayesian",
    "survival",
]
METHOD_LABEL = {
    "iv": "Instrumental variables (IV / 2SLS)",
    "rdd": "Regression discontinuity (RDD)",
    "did": "Difference-in-differences (2x2)",
    "staggered-did": "Staggered DiD / TWFE",
    "event-study": "Event study / pre-trends",
    "panel-fe": "Panel fixed effects",
    "synthetic-control": "Synthetic control",
    "matching": "Matching / propensity scores",
    "dml": "Double/debiased ML",
    "bayesian": "Bayesian methods",
    "survival": "Survival / duration",
}

# Authoritative classification of each eval scenario. A method-family key credits
# that family; "*" marks a method-agnostic (cross-cutting) check.
SCENARIO_METHOD = {
    "statspai-weak-iv": "iv",
    "statspai-rdd-diagnostics": "rdd",
    "statspai-staggered-did": "staggered-did",
    "causal-inference-twfe-trap": "staggered-did",
    "aer-identification-staggered": "staggered-did",
    "statspai-pretrends-eventstudy": "event-study",
    "statspai-matching-overlap": "matching",
    "statspai-synthetic-control": "synthetic-control",
    "pyfixest-panel-clustering": "panel-fe",
    "statspai-dml-crossfit": "dml",
    "baygent-bayesian-diagnostics": "bayesian",
    "statspai-survival-assumptions": "survival",
    "statspai-bad-controls": "*",
    "statspai-clustered-inference": "*",
    "aer-robustness-multiple-testing": "*",
}
# Scenario categories that are process/integrity checks, not method coverage.
PROCESS_CATEGORIES = {
    "writing-compliance",
    "writing-style",
    "citation-hygiene",
    "reproducibility",
    "runtime-safety",
}

# Authoritative classification of each benchmark task.
TASK_METHOD = {
    "card-iv-recovery": "iv",
    "rdd-recovery": "rdd",
    "did-staggered-recovery": "staggered-did",
    "lalonde-recovery": "matching",
    "panel-fe-recovery": "panel-fe",
    "event-study-recovery": "event-study",
    "dml-recovery": "dml",
    "survival-recovery": "survival",
    "bayesian-recovery": "bayesian",
    "synthetic-control-recovery": "synthetic-control",
    "bad-control-recovery": "*",
}

# Short notes where a family is defended indirectly by a sibling family.
RELATED_NOTE = {
    "did": "2x2 base case; the parallel-trends/pre-trends check lives under Event study, and staggered identification under Staggered DiD.",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_scenarios() -> list[dict]:
    out = []
    for path in sorted(SCENARIO_DIR.glob("*.toml")):
        data = toml_compat.load_path(path)
        out.append(
            {
                "id": data.get("id", path.stem),
                "category": data.get("category", ""),
                "severity": data.get("severity", ""),
                "title": data.get("title", ""),
            }
        )
    return out


def load_tasks() -> list[dict]:
    out = []
    for path in sorted(TASK_DIR.glob("*.toml")):
        data = toml_compat.load_path(path)
        out.append({"id": data.get("id", path.stem), "title": data.get("title", "")})
    return out


def method_counts() -> dict[str, int]:
    data = json.loads(ENRICHED.read_text(encoding="utf-8"))
    return data.get("taxonomy", {}).get("method", {})


def render() -> str:
    scenarios = load_scenarios()
    tasks = load_tasks()
    counts = method_counts()

    # Bucket scenarios.
    by_method_scen: dict[str, list[dict]] = {m: [] for m in METHOD_ORDER}
    cross_scen: list[dict] = []
    process_scen: list[dict] = []
    unclassified_scen: list[dict] = []
    for s in scenarios:
        sid = s["id"]
        if sid in SCENARIO_METHOD:
            tag = SCENARIO_METHOD[sid]
            if tag == "*":
                cross_scen.append(s)
            elif tag in by_method_scen:
                by_method_scen[tag].append(s)
            else:
                unclassified_scen.append(s)
        elif s["category"] in PROCESS_CATEGORIES:
            process_scen.append(s)
        else:
            unclassified_scen.append(s)

    # Bucket tasks.
    by_method_task: dict[str, list[dict]] = {m: [] for m in METHOD_ORDER}
    cross_task: list[dict] = []
    unclassified_task: list[dict] = []
    for t in tasks:
        tid = t["id"]
        if tid in TASK_METHOD:
            tag = TASK_METHOD[tid]
            if tag == "*":
                cross_task.append(t)
            elif tag in by_method_task:
                by_method_task[tag].append(t)
            else:
                unclassified_task.append(t)
        else:
            unclassified_task.append(t)

    def status(method: str) -> str:
        has_e = bool(by_method_scen[method])
        has_b = bool(by_method_task[method])
        if has_e and has_b:
            return "covered"
        if has_e:
            return "eval only"
        if has_b:
            return "benchmark only"
        if method in RELATED_NOTE:
            return "indirect"
        return "gap"

    lines: list[str] = []
    lines.append("<!-- GENERATED by scripts/build-coverage-map.py. Do not edit by hand;")
    lines.append("     run `make catalog` (or `python3 scripts/build-coverage-map.py`) to refresh. -->")
    lines.append("")
    lines.append("# Methodological Rigor Coverage")
    lines.append("")
    lines.append(
        "What rigor does AERS actually test, per method family? This map joins three "
        "layers so coverage — and its gaps — are legible:"
    )
    lines.append("")
    lines.append(
        "- **Skills tagged** — how many catalog skills the taxonomy assigns to the method "
        "(`catalog/skills-enriched.json`)."
    )
    lines.append(
        "- **Eval scenarios** — methodological-pitfall checks in "
        "[`eval-harness/`](../eval-harness/README.md): does a skill flag the known trap?"
    )
    lines.append(
        "- **Benchmark tasks** — numeric recovery checks in "
        "[`benchmark/`](../benchmark/README.md): does a pipeline get the right number?"
    )
    lines.append("")
    lines.append(
        "A family is **covered** when it has both an eval scenario and a benchmark task, "
        "**partial** when it has one, **indirect** when a sibling family's checks defend it "
        "(see notes), and a **gap** when skills claim the method but no rigor check targets "
        "it. Gaps are listed explicitly below — they are the to-do list, not an omission."
    )
    lines.append("")

    # Main table.
    lines.append("## Coverage by method family")
    lines.append("")
    lines.append("| Method family | Skills tagged | Eval scenarios (severity) | Benchmark tasks | Status |")
    lines.append("|---|---:|---|---|---|")
    for m in METHOD_ORDER:
        evs = by_method_scen[m]
        tks = by_method_task[m]
        ev_cell = (
            "<br>".join(f"`{s['id']}` ({s['severity']})" for s in evs) if evs else "—"
        )
        tk_cell = "<br>".join(f"`{t['id']}`" for t in tks) if tks else "—"
        lines.append(
            f"| {METHOD_LABEL[m]} | {counts.get(m, 0)} | {ev_cell} | {tk_cell} | {status(m)} |"
        )
    lines.append("")

    # Notes for indirectly-covered families.
    noted = [m for m in METHOD_ORDER if m in RELATED_NOTE]
    if noted:
        lines.append("Notes:")
        lines.append("")
        for m in noted:
            lines.append(f"- **{METHOD_LABEL[m]}** — {RELATED_NOTE[m]}")
        lines.append("")

    # Gaps section.
    gaps = [m for m in METHOD_ORDER if status(m) == "gap" and counts.get(m, 0) > 0]
    partials = [m for m in METHOD_ORDER if status(m) in {"eval only", "benchmark only"}]
    lines.append("## Open gaps (skills exist, rigor check missing)")
    lines.append("")
    if gaps:
        for m in gaps:
            lines.append(
                f"- **{METHOD_LABEL[m]}** — {counts.get(m, 0)} skills tagged, no eval "
                f"scenario or benchmark task yet."
            )
    else:
        lines.append("- None — every method family with tagged skills has at least one rigor check.")
    lines.append("")
    if partials:
        lines.append("Partially covered (one of two layers):")
        lines.append("")
        for m in partials:
            lines.append(f"- **{METHOD_LABEL[m]}** — {status(m)}.")
        lines.append("")

    # Cross-cutting checks.
    lines.append("## Cross-cutting checks (method-agnostic)")
    lines.append("")
    lines.append(
        "These defend correctness across method families (controls, inference, multiple testing):"
    )
    lines.append("")
    for s in cross_scen:
        lines.append(f"- eval `{s['id']}` ({s['severity']}) — {s['title']}")
    for t in cross_task:
        lines.append(f"- benchmark `{t['id']}` — {t['title']}")
    lines.append("")

    # Process & integrity checks.
    lines.append("## Process & integrity checks")
    lines.append("")
    lines.append(
        "Non-method checks that gate the rest of the workflow (writing, citations, "
        "reproducibility, runtime safety):"
    )
    lines.append("")
    for s in process_scen:
        lines.append(f"- eval `{s['id']}` ({s['category']}, {s['severity']}) — {s['title']}")
    lines.append("")

    # Unclassified (drift guard).
    if unclassified_scen or unclassified_task:
        lines.append("## Unclassified (please classify in build-coverage-map.py)")
        lines.append("")
        for s in unclassified_scen:
            lines.append(f"- eval `{s['id']}` (category: {s['category'] or 'none'})")
        for t in unclassified_task:
            lines.append(f"- benchmark `{t['id']}`")
        lines.append("")

    # Footer counts.
    n_cov = sum(1 for m in METHOD_ORDER if status(m) == "covered")
    lines.append("---")
    lines.append("")
    lines.append(
        f"_{len(scenarios)} eval scenarios and {len(tasks)} benchmark tasks across "
        f"{len(METHOD_ORDER)} method families; {n_cov} families fully covered, "
        f"{len(gaps)} open gaps. Regenerate with `make catalog`._"
    )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if docs/RIGOR_COVERAGE.md is stale instead of writing it",
    )
    args = parser.parse_args(argv)

    content = render()

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != content:
            print(
                f"{rel(OUT)} is stale; run `python3 scripts/build-coverage-map.py` "
                f"(or `make catalog`) and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"{rel(OUT)} is current.")
        return 0

    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {rel(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
