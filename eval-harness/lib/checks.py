#!/usr/bin/env python3
"""Machine-checkable rubric primitives for the AERS eval harness.

Skills in this repo are *prompts*, not code, so the unit of evaluation is a
rubric: a list of checkable properties an agent's output should (or must not)
have. Some rubric items can be verified deterministically (a forbidden phrase
is absent, an abstract is <= 100 words, a recovered estimate is within
tolerance of a known value). Those live here. Items that need judgement are
marked ``manual`` and routed to a human or LLM judge instead.

This module is intentionally stdlib-only (no PyYAML, no third-party deps),
mirroring ``scripts/build-catalog.py``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# Check types that the runner can verify without a judge.
AUTO_CHECKS = {
    "regex_any",       # PASS if at least one pattern matches
    "regex_all",       # PASS if every pattern matches
    "regex_none",      # PASS if no pattern matches (forbidden content absent)
    "regex_count_max",  # PASS if total match count <= target (optionally per N chars)
    "word_count_max",  # PASS if word/char count of (section or doc) <= target
    "word_count_min",  # PASS if word/char count of (section or doc) >= target
    "numeric_tolerance",  # PASS if extracted number within tol of expected
    "numeric_sign",    # PASS if extracted number has the expected sign
}
MANUAL_CHECK = "manual"  # always routed to a judge
ALL_CHECKS = AUTO_CHECKS | {MANUAL_CHECK}


@dataclass
class CheckResult:
    item_id: str
    status: str            # "pass" | "fail" | "manual" | "error"
    weight: float
    required: bool
    detail: str = ""
    evidence: list[str] = field(default_factory=list)


def _slice_section(text: str, section: str | None) -> str:
    """Return the substring captured by ``section`` (a regex with group 1), or
    the whole text if ``section`` is empty/None or does not match.
    """
    if not section:
        return text
    m = re.search(section, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if not m:
        return text
    return m.group(1) if m.groups() else m.group(0)


def _count_units(text: str, unit: str) -> int:
    if unit == "chars":
        # Count non-whitespace characters (works for CJK and Latin alike).
        return len(re.sub(r"\s+", "", text))
    if unit == "cjk":
        # Count CJK ideographs only.
        return len(re.findall(r"[一-鿿]", text))
    # Default: whitespace-delimited words, plus each CJK char as one word so
    # mixed-language abstracts are counted sensibly.
    latin = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", text)
    cjk = re.findall(r"[一-鿿]", text)
    return len(latin) + len(cjk)


def _find_number(text: str, pattern: str) -> float | None:
    m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not m or not m.groups():
        return None
    raw = m.group(1).replace(",", "").replace("$", "").strip()
    try:
        return float(raw)
    except ValueError:
        return None


def run_check(item: dict[str, Any], candidate: str) -> CheckResult:
    """Evaluate one rubric item against candidate output text."""
    item_id = str(item.get("id", "<unnamed>"))
    weight = float(item.get("weight", 1))
    required = bool(item.get("required", False))
    check = item.get("check", MANUAL_CHECK)

    def ok(detail: str = "", evidence: list[str] | None = None) -> CheckResult:
        return CheckResult(item_id, "pass", weight, required, detail, evidence or [])

    def bad(detail: str, evidence: list[str] | None = None) -> CheckResult:
        return CheckResult(item_id, "fail", weight, required, detail, evidence or [])

    if check == MANUAL_CHECK:
        return CheckResult(item_id, "manual", weight, required,
                           item.get("guidance", "Requires human/LLM judgement."))

    if check not in AUTO_CHECKS:
        return CheckResult(item_id, "error", weight, required,
                           f"Unknown check type: {check!r}")

    section = item.get("section")
    text = _slice_section(candidate, section)

    try:
        if check in {"regex_any", "regex_all", "regex_none"}:
            patterns = item.get("patterns") or ([item["pattern"]] if "pattern" in item else [])
            if not patterns:
                return CheckResult(item_id, "error", weight, required, "No patterns given.")
            hits = [p for p in patterns
                    if re.search(p, text, re.IGNORECASE | re.DOTALL | re.MULTILINE)]
            if check == "regex_any":
                return ok(f"matched {len(hits)}/{len(patterns)}", hits[:3]) if hits \
                    else bad("no required pattern matched", patterns[:3])
            if check == "regex_all":
                missing = [p for p in patterns if p not in hits]
                return ok("all patterns matched") if not missing \
                    else bad(f"missing {len(missing)} pattern(s)", missing[:3])
            # regex_none
            return bad("forbidden pattern present", hits[:3]) if hits \
                else ok("no forbidden pattern present")

        if check == "regex_count_max":
            pattern = item.get("pattern") or (item.get("patterns") or [None])[0]
            count = len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE))
            target = float(item["target"])
            per_chars = item.get("per_chars")
            if per_chars:
                n = max(_count_units(text, "chars"), 1)
                target = target * n / float(per_chars)
            return ok(f"{count} matches <= {target:.2f}") if count <= target \
                else bad(f"{count} matches > {target:.2f}")

        if check in {"word_count_max", "word_count_min"}:
            unit = item.get("unit", "words")
            n = _count_units(text, unit)
            target = float(item["target"])
            if check == "word_count_max":
                return ok(f"{n} {unit} <= {target:.0f}") if n <= target \
                    else bad(f"{n} {unit} > {target:.0f} limit")
            return ok(f"{n} {unit} >= {target:.0f}") if n >= target \
                else bad(f"{n} {unit} < {target:.0f} minimum")

        if check == "numeric_tolerance":
            val = _find_number(text, item["extract"])
            if val is None:
                return bad("could not extract a number with the given pattern")
            expected = float(item["expected"])
            tol = float(item.get("tol", 0))
            return ok(f"{val} within {tol} of {expected}") if abs(val - expected) <= tol \
                else bad(f"{val} not within {tol} of {expected}")

        if check == "numeric_sign":
            val = _find_number(text, item["extract"])
            if val is None:
                return bad("could not extract a number with the given pattern")
            want = item.get("sign", "positive")
            good = (val > 0) if want == "positive" else (val < 0) if want == "negative" else (val == 0)
            return ok(f"{val} is {want}") if good else bad(f"{val} is not {want}")

    except KeyError as exc:
        return CheckResult(item_id, "error", weight, required, f"missing field {exc}")
    except re.error as exc:
        return CheckResult(item_id, "error", weight, required, f"bad regex: {exc}")

    return CheckResult(item_id, "error", weight, required, "unreachable")
