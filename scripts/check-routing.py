#!/usr/bin/env python3
"""Routing eval: does catalog search put an acceptable skill near the top?

Scores ``scripts/find-skill.py`` against the hand-written cases in
``evals/routing-cases.json`` and prints hit@1 / hit@3 / hit@5 for three
rankers, so any change to the catalog, the tiers in ``catalog/curation.json``
or the ranker is measured against the same tasks:

- ``keyword``: count of query words found in name + description, catalog order
  on ties — roughly what grepping ``catalog/skills.json`` gives an agent;
- ``bm25``: find-skill.py ranking with tiers switched off;
- ``tiered``: find-skill.py as shipped (BM25 + curation tiers + duplicate folding).

Stdlib only; writes nothing.

    python3 scripts/check-routing.py                    # report
    python3 scripts/check-routing.py --min-hit3 0.85    # CI gate on the tiered ranker
    python3 scripts/check-routing.py -v                 # show every miss
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_JSON = ROOT / "evals" / "routing-cases.json"
KS = (1, 3, 5)


def _load_finder():
    spec = importlib.util.spec_from_file_location("aers_find_skill", ROOT / "scripts" / "find-skill.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def keyword_rank(skills: list[dict], query: str, tokenize) -> list[dict]:
    words = set(tokenize(query))
    scored = []
    for order, s in enumerate(skills):
        hay = ((s.get("name") or "") + " " + (s.get("description_effective") or "")).lower()
        n = sum(1 for w in words if w in hay)
        if n:
            scored.append((-n, order, s))
    scored.sort(key=lambda x: (x[0], x[1]))
    return [s for _, _, s in scored]


def validate_cases(cases: list[dict], paths: list[str]) -> list[str]:
    problems, seen = [], set()
    for c in cases:
        if c["id"] in seen:
            problems.append(f"duplicate case id {c['id']!r}")
        seen.add(c["id"])
        if not c.get("accept"):
            problems.append(f"{c['id']}: empty accept list")
        for prefix in c.get("accept", []):
            if not any(p.startswith(prefix) for p in paths):
                problems.append(f"{c['id']}: accept prefix matches no cataloged skill: {prefix}")
    return problems


def evaluate(cases: list[dict], rankers: dict) -> dict[str, dict]:
    out = {}
    for name, rank in rankers.items():
        hits = {k: 0 for k in KS}
        misses = []
        for c in cases:
            top = [s["path"] for s in rank(c["query"])[: max(KS)]]
            first = next((i for i, p in enumerate(top) if p.startswith(tuple(c["accept"]))), None)
            for k in KS:
                if first is not None and first < k:
                    hits[k] += 1
            if first is None or first >= 3:
                misses.append((c["id"], c["query"], top[:3]))
        out[name] = {"hit": {k: hits[k] / len(cases) for k in KS}, "misses": misses}
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--min-hit3", type=float, default=None, help="fail if tiered hit@3 is below this")
    ap.add_argument("-v", "--verbose", action="store_true", help="list tiered-ranker misses at k=3")
    args = ap.parse_args(argv)

    finder = _load_finder()
    index = finder.load_index()
    cases = json.loads(CASES_JSON.read_text(encoding="utf-8"))["cases"]
    problems = validate_cases(cases, [s["path"] for s in index.skills])
    if problems:
        print("evals/routing-cases.json is inconsistent with the catalog:")
        for p in problems:
            print(f"  - {p}")
        return 1

    results = evaluate(cases, {
        "keyword": lambda q: keyword_rank(index.skills, q, finder.tokenize),
        "bm25": lambda q: [s for _, s in index.search(q, k=max(KS), use_tiers=False)],
        "tiered": lambda q: [s for _, s in index.search(q, k=max(KS), use_tiers=True)],
    })
    print(f"Routing eval — {len(cases)} cases (evals/routing-cases.json)")
    print(f"  {'ranker':<8} " + "  ".join(f"hit@{k}" for k in KS))
    for name, r in results.items():
        print(f"  {name:<8} " + "  ".join(f"{r['hit'][k]:>5.0%}" for k in KS))
    if args.verbose:
        for cid, q, top in results["tiered"]["misses"]:
            print(f"  miss@3 {cid}: {q!r}\n         got {top}")

    if args.min_hit3 is not None:
        got = results["tiered"]["hit"][3]
        if got < args.min_hit3:
            print(f"FAIL: tiered hit@3 {got:.0%} < required {args.min_hit3:.0%}")
            return 1
        print(f"OK: tiered hit@3 {got:.0%} >= {args.min_hit3:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
