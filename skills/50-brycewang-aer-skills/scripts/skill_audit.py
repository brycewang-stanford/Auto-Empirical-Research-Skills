#!/usr/bin/env python3
"""SkillOpt-style document-quality audit for AER-skills SKILL.md files.

This is the "Reflect/score" half of the SkillOpt loop documented in
docs/skillopt-evaluation-protocol.md. That protocol's behavioral gate
(scripts/run_skillopt_gate.py) checks that the right skill still fires and
routes; this auditor scores the *document quality* of each skill so an edit
can be checked for regression the same way SkillOpt
(https://github.com/microsoft/SkillOpt) gates an edit against a held-out
score: edit a SKILL.md, re-run this audit, keep the edit only if the score
does not regress.

The auditor scores each skill on the dimensions SkillOpt's optimizer rewards
-- a compact token budget, a sharp activation trigger, and concrete
directives in place of prose -- and adds two repository-specific dimensions:
the house section structure and this repo's own style-guide discipline
(docs/style-guide.md). Every dimension is a heuristic; the goal is a fast,
deterministic signal that points editing effort at the weakest skill, not a
ground-truth grade.

No third-party dependencies, so it runs in the same fresh environments as
scripts/validate_repo.py.

Usage:
    python3 scripts/skill_audit.py                # ranked table, advisory
    python3 scripts/skill_audit.py --skill aer-paper-body --verbose
    python3 scripts/skill_audit.py --json
    python3 scripts/skill_audit.py --gate 60      # exit 1 if any skill < 60
    python3 scripts/skill_audit.py --selftest     # run scorer self-tests

    # SkillOpt "do not regress" gate around an edit:
    python3 scripts/skill_audit.py --baseline before.json   # snapshot, then edit
    python3 scripts/skill_audit.py --against before.json     # exit 1 if any score dropped
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+\S")
TABLE_ROW_RE = re.compile(r"^\s*\|")
FENCE_RE = re.compile(r"^\s*```")
DIRECTIVE_VERBS = {
    "use", "apply", "report", "run", "check", "avoid", "state", "keep",
    "show", "cite", "verify", "drop", "include", "write", "confirm",
    "ensure", "prefer", "never", "do", "compute", "flag", "push", "load",
    "round", "cluster", "test", "name", "label", "treat", "pick", "start",
    "stop", "read", "set", "list", "map", "trace", "scan", "trim", "cut",
    "frame", "anchor", "route", "gate", "open", "close", "hand", "return",
    "delete", "replace", "add", "place", "present", "pre-empt", "rerun",
}

# SkillOpt reports optimized skill artifacts in the 300-2,000 token band.
TOKEN_BUDGET_LOW = 300
TOKEN_BUDGET_HIGH = 2000
TOKEN_OVER_SLACK = 3000  # tokens above HIGH at which the budget score hits 0

HOUSE_SECTIONS = ("Overview", "When to Use", "Handoff", "Anti-Patterns")

# Dimension weights (sum to 100).
WEIGHTS = {
    "budget": 20,
    "trigger": 15,
    "structure": 15,
    "directive": 25,
    "hygiene": 15,
    "handoff": 10,
}

# Style-guide tells (docs/style-guide.md). Kept high-precision: phrases and
# vocabulary that almost never appear in legitimate directive prose, so the
# hygiene score stays meaningful instead of noisy.
FILLER_WORDS = (
    "novel", "importantly", "notably", "interestingly", "crucially",
)
FILLER_PHRASES = (
    "plays a crucial role", "plays a pivotal role", "plays a vital role",
    "sheds light on", "underscores the importance of",
    "highlights the need for", "has important implications for policymakers",
    "a growing body of literature", "to the best of our knowledge",
    "delve into", "navigate the landscape of", "in the realm of",
    "it is worth noting that", "in today's rapidly evolving world",
    "nuanced interplay", "paradigm shift",
)
FILLER_VOCAB = ("delve", "tapestry", "multifaceted", "holistic")
DOUBLE_HEDGES = (
    "may potentially", "could possibly", "seems to suggest",
    "might be able to", "could potentially",
)
# "leverage" as a verb-for-"use"; excludes the econometric noun (leverage
# diagnostics, high-leverage points).
LEVERAGE_VERB_RE = re.compile(
    r"\bleverage\s+(?:the|our|a|these|this|its|their)\b", re.IGNORECASE
)
# Filler wrapped in double quotes is being quoted as a bad example, not used.
QUOTED_SPAN_RE = re.compile(r"\"[^\"]*\"|“[^”]*”")
# Lines that discuss what to *avoid* should not be penalized for naming it.
NEGATION_CONTEXT = (
    "never", "avoid", "don't", "do not", "delete", "without", "instead",
    "blacklist", "anti-pattern", "not allowed", "scrub", "reads as",
    "rewrite candidate", "filler", "cut the", "rather than", "no \"",
)
# A heading whose title carries any of these cues turns its whole section into
# negation context: filler named there is being prohibited, not committed.
NEGATION_SECTION = (
    "avoid", "anti-pattern", "not include", "what not", "never", "mistake",
    "pitfall", "blacklist", "scrub", "wrong", "ban", "do not", "don't",
)
HYGIENE_HITS_PER_K_ZERO = 8.0  # hits per 1000 words at which hygiene hits 0


def estimate_tokens(text: str) -> int:
    """Rough English token estimate (~4 chars/token), good enough to rank."""
    return math.ceil(len(text) / 4)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields, text[match.end():]


def iter_body_lines(body: str):
    """Yield (line, in_fence) for body lines, tracking fenced code blocks."""
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            yield line, True  # the fence marker line counts as structure
            continue
        yield line, in_fence


def is_directive_line(line: str) -> bool:
    if LIST_ITEM_RE.match(line) or TABLE_ROW_RE.match(line):
        return True
    stripped = re.sub(r"^[\s>*_#-]+", "", line).lstrip()
    word = re.match(r"[A-Za-z][\w-]*", stripped)
    if not word:
        return False
    return word.group(0).lower() in DIRECTIVE_VERBS


def score_budget(tokens: int) -> float:
    if tokens < TOKEN_BUDGET_LOW:
        return round(tokens / TOKEN_BUDGET_LOW, 3)
    if tokens <= TOKEN_BUDGET_HIGH:
        return 1.0
    over = tokens - TOKEN_BUDGET_HIGH
    return round(max(0.0, 1.0 - over / TOKEN_OVER_SLACK), 3)


def score_trigger(description: str) -> tuple[float, list[str]]:
    """Score the frontmatter description on activation quality.

    Returns (score, issues) where issues name the specific shortfall so the
    recommendation can be precise instead of generic.
    """
    if not description:
        return 0.0, ["no-description"]
    lowered = description.lower()
    issues: list[str] = []
    score = 0.0
    if "use when" in lowered:
        score += 0.5
    else:
        issues.append("no-use-when")
    if len(description) < 25:
        issues.append("too-short")
    elif len(description) > 400:
        issues.append("too-long")
    else:
        score += 0.25
    routing = ("after", "before", "so that", "once", "when the", "if the")
    if any(token in lowered for token in routing):
        score += 0.25
    else:
        issues.append("no-routing")
    return round(min(score, 1.0), 3), issues


def score_structure(headings: list[str]) -> tuple[float, list[str]]:
    present = []
    missing = []
    lowered = [h.lower() for h in headings]
    for section in HOUSE_SECTIONS:
        if any(section.lower() in h for h in lowered):
            present.append(section)
        else:
            missing.append(section)
    return round(len(present) / len(HOUSE_SECTIONS), 3), missing


def score_directive(body: str) -> tuple[float, int, int]:
    actionable = 0
    denom = 0
    for line, in_fence in iter_body_lines(body):
        if not line.strip():
            continue
        if in_fence:
            actionable += 1
            denom += 1
            continue
        if HEADING_RE.match(line):
            continue
        denom += 1
        if is_directive_line(line):
            actionable += 1
    if denom == 0:
        return 0.0, 0, 0
    density = actionable / denom
    return round(min(density / 0.45, 1.0), 3), actionable, denom


def score_hygiene(body: str, word_count: int) -> tuple[float, list[str]]:
    hits: list[str] = []
    in_negation_section = False
    for raw_line in body.splitlines():
        heading = HEADING_RE.match(raw_line)
        if heading:
            title = heading.group(2).lower()
            in_negation_section = any(cue in title for cue in NEGATION_SECTION)
            continue
        if in_negation_section:
            continue
        scan_line = QUOTED_SPAN_RE.sub(" ", raw_line)
        lowered = scan_line.lower()
        if any(neg in lowered for neg in NEGATION_CONTEXT):
            continue
        for phrase in FILLER_PHRASES + DOUBLE_HEDGES:
            if phrase in lowered:
                hits.append(phrase)
        for vocab in FILLER_VOCAB:
            if re.search(rf"\b{re.escape(vocab)}\b", lowered):
                hits.append(vocab)
        for word in FILLER_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", lowered):
                hits.append(word)
        if LEVERAGE_VERB_RE.search(scan_line):
            hits.append("leverage (verb)")
    per_k = 1000.0 * len(hits) / max(word_count, 1)
    score = max(0.0, 1.0 - per_k / HYGIENE_HITS_PER_K_ZERO)
    return round(score, 3), hits


def score_handoff(headings: list[str], body: str) -> float:
    has_section = any("handoff" in h.lower() for h in headings)
    has_routing = bool(re.search(r"NEXT SKILL|NEXT STEP|→", body))
    return round(0.6 * has_section + 0.4 * has_routing, 3)


def grade(score: float) -> str:
    for cutoff, letter in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
        if score >= cutoff:
            return letter
    return "F"


def recommend(dims: dict[str, float], detail: dict) -> list[str]:
    tips: list[str] = []
    if dims["budget"] < 1.0:
        tokens = detail["tokens"]
        if tokens > TOKEN_BUDGET_HIGH:
            tips.append(
                f"DELETE/REPLACE: ~{tokens} tokens, ~{tokens - TOKEN_BUDGET_HIGH} "
                "over the 2,000-token band -- trim redundant prose or move deep "
                "reference into docs/."
            )
        else:
            tips.append(f"ADD: only ~{tokens} tokens -- the skill may be too thin to act on.")
    if dims["trigger"] < 1.0:
        issues = detail["trigger_issues"]
        if "no-use-when" in issues or "no-description" in issues:
            tips.append("REPLACE description: open with 'Use when ...' so activation is unambiguous.")
        if "no-routing" in issues:
            tips.append("REPLACE description: add a concrete before/after routing condition.")
        if "too-long" in issues:
            tips.append("REPLACE description: tighten to <= 400 chars -- the activation summary should be scannable.")
        if "too-short" in issues:
            tips.append("ADD to description: name the manuscript stage it fires on.")
    if dims["structure"] < 1.0 and detail["missing_sections"]:
        tips.append("ADD sections: " + ", ".join(detail["missing_sections"]) + ".")
    if dims["directive"] < 0.8:
        tips.append(
            f"REPLACE prose with directives: {detail['actionable']}/{detail['body_lines']} "
            "body lines are actionable -- convert explanation into numbered steps "
            "or tables."
        )
    if dims["hygiene"] < 1.0 and detail["hygiene_hits"]:
        sample = ", ".join(sorted(set(detail["hygiene_hits"]))[:4])
        tips.append(f"DELETE filler ({len(detail['hygiene_hits'])} hits): {sample}.")
    if dims["handoff"] < 1.0:
        tips.append("ADD a Handoff block with explicit NEXT SKILL routing.")
    return tips


def audit_skill(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    fields, body = split_frontmatter(text)
    headings = [m.group(2) for m in (HEADING_RE.match(l) for l in body.splitlines()) if m]
    words = len(body.split())
    tokens = estimate_tokens(text)

    s_budget = score_budget(tokens)
    s_trigger, trigger_issues = score_trigger(fields.get("description", ""))
    s_structure, missing = score_structure(headings)
    s_directive, actionable, body_lines = score_directive(body)
    s_hygiene, hygiene_hits = score_hygiene(body, words)
    s_handoff = score_handoff(headings, body)

    dims = {
        "budget": s_budget,
        "trigger": s_trigger,
        "structure": s_structure,
        "directive": s_directive,
        "hygiene": s_hygiene,
        "handoff": s_handoff,
    }
    total = round(sum(dims[k] * WEIGHTS[k] for k in WEIGHTS), 1)
    detail = {
        "tokens": tokens,
        "lines": len(text.splitlines()),
        "words": words,
        "missing_sections": missing,
        "actionable": actionable,
        "body_lines": body_lines,
        "hygiene_hits": hygiene_hits,
        "trigger_issues": trigger_issues,
    }
    return {
        "name": skill_md.parent.name,
        "score": total,
        "grade": grade(total),
        "dimensions": dims,
        "detail": detail,
        "recommendations": recommend(dims, detail),
    }


def collect(skill_filter: str | None) -> list[dict]:
    results = []
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        if skill_filter and skill_dir.name != skill_filter:
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.is_file():
            results.append(audit_skill(skill_md))
    return results


def weakest(dims: dict[str, float], n: int = 2) -> str:
    ranked = sorted(dims.items(), key=lambda kv: kv[1])
    return ", ".join(f"{k} {v:.2f}" for k, v in ranked[:n])


def print_table(results: list[dict]) -> None:
    results = sorted(results, key=lambda r: r["score"])
    print(f"{'skill':<22}{'tok':>6}{'grade':>7}{'score':>8}  weakest dimensions")
    print("-" * 78)
    for r in results:
        print(
            f"{r['name']:<22}{r['detail']['tokens']:>6}{r['grade']:>7}"
            f"{r['score']:>8}  {weakest(r['dimensions'])}"
        )
    scores = [r["score"] for r in results]
    if scores:
        print("-" * 78)
        print(
            f"{len(scores)} skills  mean {sum(scores) / len(scores):.1f}  "
            f"min {min(scores):.1f}  max {max(scores):.1f}"
        )


def print_detail(results: list[dict]) -> None:
    for r in sorted(results, key=lambda r: r["score"]):
        d = r["detail"]
        print(f"\n### {r['name']}  ({r['grade']}, {r['score']}/100)")
        print(
            f"    {d['tokens']} tokens | {d['lines']} lines | {d['words']} words | "
            f"{d['actionable']}/{d['body_lines']} actionable lines"
        )
        print("    " + " ".join(f"{k}={v:.2f}" for k, v in r["dimensions"].items()))
        for tip in r["recommendations"]:
            print(f"      - {tip}")


def compare_baseline(results: list[dict], baseline_path: Path, tolerance: float) -> list[str]:
    """Report skills whose score dropped vs a saved baseline (the SkillOpt gate).

    Returns the list of regression messages; empty means no regression.
    """
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    prior = {r["name"]: r["score"] for r in baseline}
    regressions: list[str] = []
    print(f"\n{'skill':<22}{'base':>8}{'now':>8}{'delta':>8}")
    print("-" * 46)
    for r in sorted(results, key=lambda r: r["name"]):
        before = prior.get(r["name"])
        if before is None:
            print(f"{r['name']:<22}{'--':>8}{r['score']:>8}{'new':>8}")
            continue
        delta = round(r["score"] - before, 1)
        mark = "  <-- REGRESSED" if delta < -tolerance else ""
        print(f"{r['name']:<22}{before:>8}{r['score']:>8}{delta:>+8}{mark}")
        if delta < -tolerance:
            regressions.append(f"{r['name']}: {before} -> {r['score']} ({delta:+})")
    return regressions


def run_selftest() -> int:
    """Assert each scorer behaves as designed on synthetic inputs."""
    failures: list[str] = []

    def check(label: str, condition: bool) -> None:
        if not condition:
            failures.append(label)

    check("tokens monotonic", estimate_tokens("x" * 400) > estimate_tokens("x" * 40))
    check("budget in-band", score_budget(1500) == 1.0)
    check("budget over decays to 0", score_budget(TOKEN_BUDGET_HIGH + TOKEN_OVER_SLACK) == 0.0)
    check("budget thin penalized", score_budget(150) < 1.0)

    full, _ = score_trigger("Use when drafting after the data exist, before submission.")
    miss, miss_issues = score_trigger("Draft the results once the tables exist.")
    check("trigger full beats missing use-when", full > miss)
    check("missing use-when flagged", "no-use-when" in miss_issues)
    _, long_issues = score_trigger("Use when " + "x " * 250)
    check("over-long description flagged", "too-long" in long_issues)

    s_struct, missing = score_structure(["Overview", "When to Use", "Handoff", "Anti-Patterns"])
    check("all house sections score 1.0", s_struct == 1.0 and not missing)
    check("missing section detected", score_structure(["Overview"])[0] < 1.0)

    bullets = "\n".join(f"- step {i}" for i in range(10))
    prose = "\n".join("This sentence explains a concept at length." for _ in range(10))
    check("bullet body is directive-dense", score_directive(bullets)[0] > score_directive(prose)[0])

    used = "The model delve into the data and plays a crucial role here.\n"
    quoted = 'Avoid writing "this plays a crucial role" in the body.\n'
    check("unquoted filler scores a hit", score_hygiene(used, 12)[1])
    check("quoted/negated filler is skipped", not score_hygiene(quoted, 12)[1])
    negated_section = "## Anti-Patterns\n- delve into the literature without naming papers\n"
    check("filler under anti-pattern heading skipped", not score_hygiene(negated_section, 12)[1])
    check("econometric leverage not flagged", not score_hygiene("Report leverage and Cook's distance.\n", 8)[1])

    check("handoff full", score_handoff(["Handoff"], "NEXT SKILL: aer-submission") == 1.0)
    check("handoff absent", score_handoff(["Overview"], "no routing here") == 0.0)

    if failures:
        for label in failures:
            print(f"SELFTEST FAILED: {label}", file=sys.stderr)
        return 1
    print("self-tests passed")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--skill", help="audit a single skill by directory name")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--verbose", action="store_true", help="print per-skill detail")
    parser.add_argument(
        "--gate", type=float, default=None,
        help="exit 1 if any audited skill scores below this threshold",
    )
    parser.add_argument(
        "--baseline", metavar="PATH",
        help="write current scores to PATH (a snapshot to compare later edits against)",
    )
    parser.add_argument(
        "--against", metavar="PATH",
        help="compare current scores to a saved baseline; exit 1 on any regression",
    )
    parser.add_argument(
        "--tolerance", type=float, default=0.1,
        help="allowed score drop before --against flags a regression (default 0.1)",
    )
    parser.add_argument(
        "--selftest", action="store_true",
        help="run internal scorer self-tests and exit",
    )
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest()

    if not SKILLS_DIR.is_dir():
        print("skills/ directory not found", file=sys.stderr)
        return 2

    results = collect(args.skill)
    if not results:
        print("no SKILL.md files matched", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_table(results)
        if args.verbose or args.skill:
            print_detail(results)

    if args.baseline:
        baseline_path = Path(args.baseline)
        baseline_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print(f"\nbaseline written: {args.baseline} ({len(results)} skills)")

    exit_code = 0

    if args.against:
        against_path = Path(args.against)
        if not against_path.is_file():
            print(f"baseline not found: {args.against}", file=sys.stderr)
            return 2
        regressions = compare_baseline(results, against_path, args.tolerance)
        if regressions:
            print(f"\nREGRESSION ({len(regressions)}): " + "; ".join(regressions), file=sys.stderr)
            exit_code = 1
        else:
            print(f"\nNO REGRESSION vs {args.against} (tolerance {args.tolerance})")

    if args.gate is not None:
        failing = [r for r in results if r["score"] < args.gate]
        if failing:
            names = ", ".join(f"{r['name']} ({r['score']})" for r in failing)
            print(f"\nGATE FAILED (< {args.gate}): {names}", file=sys.stderr)
            exit_code = 1
        else:
            print(f"\nGATE PASSED: all skills >= {args.gate}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
