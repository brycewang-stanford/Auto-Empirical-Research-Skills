#!/usr/bin/env python3
"""Deterministic SkillOpt-style gate for the AER-Skills router."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "examples" / "skillopt-routing-scenarios.json"
WORKFLOW_PATH = ROOT / "skills" / "aer-workflow" / "SKILL.md"
PROTOCOL_PATH = ROOT / "docs" / "skillopt-evaluation-protocol.md"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{2,79}$")
VALID_SPLITS = {"selection", "test"}
REQUIRED_SCENARIO_FIELDS = {
    "id",
    "split",
    "prompt",
    "expected_skill",
    "gate_status",
    "success_criteria",
}
HANDOFF_LABELS = ("NEXT SKILL:", "REASON:", "INPUTS NEEDED:", "GATE STATUS:")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        fail(errors, f"{rel(path)}: missing")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{rel(path)}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}")
        return {}
    if not isinstance(data, dict):
        fail(errors, f"{rel(path)}: top-level JSON value must be an object")
        return {}
    return data


def skill_names() -> set[str]:
    return {
        path.parent.name
        for path in (ROOT / "skills").glob("aer-*/SKILL.md")
        if path.is_file()
    }


def validate_workflow(errors: list[str]) -> str:
    if not WORKFLOW_PATH.is_file():
        fail(errors, f"{rel(WORKFLOW_PATH)}: missing")
        return ""
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    for label in HANDOFF_LABELS:
        if label not in text:
            fail(errors, f"{rel(WORKFLOW_PATH)}: missing handoff label {label!r}")
    for resource in (rel(PROTOCOL_PATH), rel(SCENARIO_PATH)):
        if resource not in text:
            fail(errors, f"{rel(WORKFLOW_PATH)}: missing SkillOpt resource {resource}")
    return text


def validate_scenarios(data: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    if data.get("schema") != 1:
        fail(errors, f"{rel(SCENARIO_PATH)}: schema must be 1")
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        fail(errors, f"{rel(SCENARIO_PATH)}: scenarios must be a non-empty list")
        return []

    names = skill_names()
    routed_names = names - {"aer-workflow"}
    seen_ids: set[str] = set()
    seen_prompts: set[str] = set()
    covered_skills: set[str] = set()
    split_counts = {split: 0 for split in VALID_SPLITS}
    valid_scenarios: list[dict[str, Any]] = []

    for index, item in enumerate(scenarios, 1):
        label = f"{rel(SCENARIO_PATH)}: scenario {index}"
        if not isinstance(item, dict):
            fail(errors, f"{label}: must be an object")
            continue

        missing = REQUIRED_SCENARIO_FIELDS - set(item)
        extra = set(item) - REQUIRED_SCENARIO_FIELDS
        if missing:
            fail(errors, f"{label}: missing fields {', '.join(sorted(missing))}")
        if extra:
            fail(errors, f"{label}: unknown fields {', '.join(sorted(extra))}")

        scenario_id = item.get("id")
        if not isinstance(scenario_id, str) or not ID_RE.match(scenario_id):
            fail(errors, f"{label}: invalid id")
        elif scenario_id in seen_ids:
            fail(errors, f"{label}: duplicate id {scenario_id!r}")
        else:
            seen_ids.add(scenario_id)

        split = item.get("split")
        if split not in VALID_SPLITS:
            fail(errors, f"{label}: split must be one of {', '.join(sorted(VALID_SPLITS))}")
        else:
            split_counts[split] += 1

        prompt = item.get("prompt")
        if not isinstance(prompt, str) or len(prompt.strip()) < 40:
            fail(errors, f"{label}: prompt must be a user-like string of at least 40 characters")
        elif prompt in seen_prompts:
            fail(errors, f"{label}: duplicate prompt")
        else:
            seen_prompts.add(prompt)

        expected_skill = item.get("expected_skill")
        if expected_skill not in names:
            fail(errors, f"{label}: expected_skill {expected_skill!r} has no skill folder")
        elif expected_skill == "aer-workflow":
            fail(errors, f"{label}: router scenarios must route to a non-router skill")
        else:
            covered_skills.add(expected_skill)

        gate_status = item.get("gate_status")
        if not isinstance(gate_status, str) or len(gate_status.strip()) < 6:
            fail(errors, f"{label}: gate_status must be descriptive")

        criteria = item.get("success_criteria")
        if not isinstance(criteria, list) or not all(isinstance(value, str) for value in criteria):
            fail(errors, f"{label}: success_criteria must be a list of strings")
        else:
            expected_next = f"NEXT SKILL: {expected_skill}"
            if expected_next not in criteria:
                fail(errors, f"{label}: success_criteria missing {expected_next!r}")
            for handoff_label in HANDOFF_LABELS[1:]:
                if handoff_label not in criteria:
                    fail(errors, f"{label}: success_criteria missing {handoff_label!r}")

        valid_scenarios.append(item)

    missing_skills = routed_names - covered_skills
    if missing_skills:
        fail(errors, f"{rel(SCENARIO_PATH)}: missing scenarios for {', '.join(sorted(missing_skills))}")
    for split, count in sorted(split_counts.items()):
        if count == 0:
            fail(errors, f"{rel(SCENARIO_PATH)}: split {split!r} has no scenarios")

    return valid_scenarios


def validate_router_coverage(workflow_text: str, scenarios: list[dict[str, Any]], errors: list[str]) -> None:
    for item in scenarios:
        expected_skill = item.get("expected_skill")
        if isinstance(expected_skill, str) and expected_skill not in workflow_text:
            fail(errors, f"{rel(WORKFLOW_PATH)}: missing route mention for {expected_skill}")


def emit_prompts(scenarios: list[dict[str, Any]]) -> None:
    for item in scenarios:
        print(f"[{item['split']}] {item['id']}")
        print(item["prompt"])
        print(f"Expected: {item['expected_skill']}")
        print()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--emit-prompts",
        action="store_true",
        help="print the scenario prompts for manual forward-testing",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    errors: list[str] = []
    workflow_text = validate_workflow(errors)
    data = load_json(SCENARIO_PATH, errors)
    scenarios = validate_scenarios(data, errors)
    validate_router_coverage(workflow_text, scenarios, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.emit_prompts:
        emit_prompts(scenarios)
    else:
        splits = sorted({item["split"] for item in scenarios})
        routed = sorted({item["expected_skill"] for item in scenarios})
        print(
            "SkillOpt gate passed: "
            f"{len(scenarios)} scenarios, {len(routed)} routed skills, "
            f"splits={','.join(splits)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
