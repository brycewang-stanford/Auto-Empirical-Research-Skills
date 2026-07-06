#!/usr/bin/env python3
"""Regenerate the repository quality scorecard (docs/quality-scorecard.md).

The scorecard is the one-page, machine-generated aggregate of every gate the
repository enforces: skill-audit scores, demo numeric-check counts, citation
verification totals, and the gate inventory itself. It is DERIVED state — the
committed file must always match what this script produces, so the numbers on
the page can never drift from what the tooling actually measures.

Usage:
    python3 scripts/quality_scorecard.py            # print to stdout
    python3 scripts/quality_scorecard.py --write    # rewrite docs/quality-scorecard.md
    python3 scripts/quality_scorecard.py --check    # exit 1 if the committed file drifted

Determinism contract: the output contains no timestamps and depends only on
tracked repository content, so ``--check`` is safe to run in preflight and CI.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import skill_audit
import validate_repo

ROOT = validate_repo.ROOT
SCORECARD = ROOT / "docs" / "quality-scorecard.md"

GATES = (
    ("Repository validator", "make validate",
     "structure, registration, dependency pins, manifest invariants, link integrity"),
    ("Strict optional-tool coverage", "make validate-strict",
     "every optional tool documented and registered"),
    ("SkillOpt routing gate", "make skillopt-gate",
     "routing scenarios select the intended skill"),
    ("Skill document-quality floor", "make audit-skills-gate",
     "score >= 85 and >= 8 substance anchors per skill"),
    ("Citation verification (offline)", "make verify-citations",
     "every bib entry matches its recorded Crossref response"),
    ("Citation groundedness", "make verify-citations-groundedness",
     "every prose citation resolves to a verified bib entry"),
    ("Example smoke + numeric contract", "make smoke-examples",
     "every demo runs and every NUMERIC-CHECK passes"),
    ("Quality-tooling unit tests", "make test",
     "the validators themselves are tested"),
    ("Scorecard drift", "make scorecard",
     "this page always matches what the tooling measures"),
)


def plugin_version() -> str:
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    return manifest["version"]


def count_numeric_checks(script: Path) -> int:
    text = script.read_text(encoding="utf-8")
    calls = 0
    for line in text.splitlines():
        stripped = line.strip()
        if "numeric_check(" not in stripped:
            continue
        if stripped.startswith("#") or "import" in stripped:
            continue
        if re.match(r"numeric_check\s*<-\s*function", stripped):
            continue
        if re.match(r"def\s+numeric_check", stripped):
            continue
        calls += len(re.findall(r"(?<![\w<])numeric_check\(", stripped))
    return calls


def demo_rows() -> list[tuple[str, str, int]]:
    rows = []
    for demo_name, expected in sorted(validate_repo.EXPECTED_EXAMPLE_DEMOS.items()):
        scripts = sorted(name for name in expected if name != "README.md")
        checks = sum(
            count_numeric_checks(ROOT / "examples" / demo_name / name) for name in scripts
        )
        rows.append((demo_name, ", ".join(scripts), checks))
    return rows


def bib_entry_count() -> int:
    text = (ROOT / "references.bib").read_text(encoding="utf-8")
    return len(re.findall(r"^@\w+\{", text, flags=re.MULTILINE))


def recorded_response_count() -> int:
    recorded = json.loads(
        (ROOT / "scripts" / "citation_gold" / "recorded_responses.json").read_text(encoding="utf-8")
    )
    return len(recorded["responses"])


def gold_tuple_counts() -> tuple[int, int]:
    gold = json.loads(
        (ROOT / "scripts" / "citation_gold" / "gold_set.json").read_text(encoding="utf-8")
    )
    return len(gold["tuples"]), len(gold.get("groundedness_cases", []))


def statspai_tool_count() -> int:
    lines = (ROOT / "scripts" / "statspai_tools.txt").read_text(encoding="utf-8").splitlines()
    return sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))


def render() -> str:
    skills = skill_audit.collect(None)
    demos = demo_rows()
    total_checks = sum(row[2] for row in demos)
    tuples, ground_cases = gold_tuple_counts()

    lines: list[str] = []
    out = lines.append
    out("# Quality scorecard")
    out("")
    out("<!-- GENERATED FILE. Edit scripts/quality_scorecard.py, then run: make scorecard -->")
    out("")
    out(f"Machine-generated for **v{plugin_version()}** by `scripts/quality_scorecard.py`; "
        "regenerate with `make scorecard`. Preflight fails if this page drifts from "
        "what the tooling measures.")
    out("")
    out("## Headline numbers")
    out("")
    out("| Metric | Value |")
    out("|---|---|")
    out(f"| Skills in the bundle | {len(skills)} |")
    out(f"| Skills at grade A (score >= 90) | "
        f"{sum(1 for s in skills if s['score'] >= 90)} |")
    out(f"| Lowest skill-audit score (gate: >= 85) | "
        f"{min(s['score'] for s in skills):.1f} |")
    out(f"| Lowest substance-anchor count (gate: >= 8) | "
        f"{min(s['detail']['substance_anchors'] for s in skills)} |")
    out(f"| Runnable demos under the numeric-check contract | {len(demos)} |")
    out(f"| NUMERIC-CHECK assertions across demos | {total_checks} |")
    out(f"| Verified bibliography entries | {bib_entry_count()} |")
    out(f"| Recorded index responses (hermetic offline verification) | "
        f"{recorded_response_count()} |")
    out(f"| Citation gold tuples / groundedness cases | {tuples} / {ground_cases} |")
    out(f"| Validated StatsPAI tool bindings | {statspai_tool_count()} |")
    out(f"| Enforced quality gates | {len(GATES)} |")
    out("")
    out("## Gate inventory")
    out("")
    out("| Gate | Command | What it enforces |")
    out("|---|---|---|")
    for name, command, what in GATES:
        out(f"| {name} | `{command}` | {what} |")
    out("")
    out("## Skill audit")
    out("")
    out("| Skill | Score | Grade | Substance anchors |")
    out("|---|---|---|---|")
    for s in sorted(skills, key=lambda s: (-s["score"], s["name"])):
        out(f"| `{s['name']}` | {s['score']:.1f} | {s['grade']} | "
            f"{s['detail']['substance_anchors']} |")
    out("")
    out("## Demo numeric contracts")
    out("")
    out("| Demo | Script(s) | NUMERIC-CHECK assertions |")
    out("|---|---|---|")
    for demo_name, scripts, checks in demos:
        out(f"| [`{demo_name}/`](../examples/{demo_name}/) | {scripts} | {checks} |")
    out("")
    out("Every assertion pins an estimate to a known truth within a stated tolerance; "
        "`make smoke-examples` fails a demo that emits none or reports a FAIL. See "
        "[`../examples/README.md`](../examples/README.md) for the contract and "
        "[`roadmap.md`](roadmap.md) for the operating definition these numbers serve.")
    out("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="rewrite docs/quality-scorecard.md")
    mode.add_argument("--check", action="store_true",
                      help="exit non-zero if the committed scorecard drifted")
    args = parser.parse_args(argv)

    content = render()
    if args.write:
        SCORECARD.write_text(content, encoding="utf-8")
        print(f"wrote {SCORECARD.relative_to(ROOT)}")
        return 0
    if args.check:
        if not SCORECARD.is_file():
            print("scorecard check FAIL: docs/quality-scorecard.md missing; run: make scorecard",
                  file=sys.stderr)
            return 1
        committed = SCORECARD.read_text(encoding="utf-8")
        if committed != content:
            print("scorecard check FAIL: docs/quality-scorecard.md is stale; run: make scorecard",
                  file=sys.stderr)
            return 1
        print("scorecard check ok: docs/quality-scorecard.md matches the measured state")
        return 0
    print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
