#!/usr/bin/env python3
"""Rank cataloged skills for a free-text task — the router's search step.

The root ``SKILL.md`` router sends an agent here when its method table has no
row for the task. Instead of grepping ``catalog/skills.json`` (which returns
dozens of equal-looking hits for "latex" or "literature review"), this ranks
``catalog/skills-enriched.json`` with a small BM25 over name / tags /
description / path, then applies the routing tier from
``catalog/curation.json``: core > extended > duplicate > out-of-domain. Tiers
only reorder; no skill is ever hidden (out-of-domain skills still surface when
the query is about them).

Stdlib only; reads committed catalog files, writes nothing.

    python3 scripts/find-skill.py "staggered difference-in-differences"
    python3 scripts/find-skill.py "降低论文 AIGC 率" -k 5
    python3 scripts/find-skill.py "synthetic control" --json
    python3 scripts/find-skill.py "proofread" --no-tiers      # raw relevance only
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENRICHED_JSON = ROOT / "catalog" / "skills-enriched.json"

# Field weights: a hit in the skill's own name says more than one in its path.
FIELD_WEIGHTS = {"name": 3.0, "tags": 2.0, "description": 1.0, "path": 0.5}
TIER_WEIGHTS = {"core": 1.5, "extended": 1.0, "duplicate": 0.6, "out-of-domain": 0.35}
# A query word this rare that appears in a skill's own name means the user asked
# for that skill by name ("PubChem", "EDGAR"), so its tier penalty is waived.
EXPLICIT_NAME_MAX_DF = 10
BM25_K1, BM25_B = 1.2, 0.75

# Common abbreviations researchers type, expanded to the words skill
# descriptions actually use. Keep this short and generic — it is a query
# normaliser, not a hand-tuned answer key.
ALIASES = {
    "did": "difference-in-differences did",
    "diff-in-diff": "difference-in-differences did",
    "rdd": "regression discontinuity rdd",
    "rd": "regression discontinuity",
    "iv": "instrumental variables iv",
    "2sls": "instrumental variables 2sls",
    "scm": "synthetic control scm",
    "psm": "propensity score matching psm",
    "dml": "double machine learning dml",
    "rct": "randomized experiment rct",
    "r&r": "revise resubmit referee response",
    "aigc": "aigc ai writing humanize",
    "lit": "literature",
    "docx": "docx word",
    "fred": "fred federal reserve economic data",
}
# CJK task words → English catalog vocabulary (descriptions are mostly English).
CJK_ALIASES = {
    "双重差分": "difference-in-differences did",
    "多期": "staggered",
    "事件研究": "event study",
    "断点回归": "regression discontinuity rdd",
    "工具变量": "instrumental variables iv",
    "合成控制": "synthetic control",
    "倾向得分": "propensity score matching",
    "匹配": "matching",
    "文献综述": "literature review",
    "文献": "literature",
    "降": "reduce",
    "aigc": "aigc ai writing humanize",
    "去ai": "humanize ai writing",
    "润色": "polish proofread",
    "审稿": "referee review",
    "回复": "response",
    "复现": "replication",
    "学位论文": "thesis dissertation",
    "模板": "template",
    "论文": "paper",
    "写作": "writing",
    "中文": "chinese",
    "数据清洗": "data cleaning",
    "稳健性": "robustness",
    "规格": "specification",
    "设定曲线": "specification curve",
    "岔路": "forking paths",
    "多重宇宙": "multiverse",
    "p曲线": "p-curve",
    "p 曲线": "p-curve",
    "p值操纵": "p-hacking",
    "发表偏倚": "publication bias",
    "预注册": "pre-registration preregistration",
    "机制": "mechanism mediation",
    "异质性": "heterogeneity",
    "引用": "citation",
    "参考文献": "references bibtex citation",
    "幻灯片": "slides presentation",
    "选题": "research ideation topic",
    "投稿": "submission",
    "表格": "tables",
    "图": "figures",
}
STOPWORDS = frozenset(
    "a an and are as at be by for from how i in into is it me my of on or our so "
    "that the this to use using want we with".split()
)
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+&'.-]*[a-z0-9+]|[a-z0-9]")


def tokenize(text: str) -> list[str]:
    toks = []
    for tok in TOKEN_RE.findall(text.lower()):
        if tok in STOPWORDS:
            continue
        toks.append(tok)
        if "-" in tok:  # "difference-in-differences" also matches "differences"
            toks.extend(p for p in tok.split("-") if p and p not in STOPWORDS)
    return toks


def expand_query(query: str) -> list[str]:
    q = query.lower()
    extra = [en for zh, en in CJK_ALIASES.items() if zh in q]
    toks = tokenize(q + " " + " ".join(extra))
    out = []
    for t in toks:
        out.extend(tokenize(ALIASES[t]) if t in ALIASES else [t])
    # Adjacent pairs joined, so "marginal effects" also matches `marginaleffects`.
    out.extend(a + b for a, b in zip(toks, toks[1:]) if a.isalpha() and b.isalpha())
    return list(dict.fromkeys(out))  # de-dup, keep order


def skill_fields(skill: dict) -> dict[str, list[str]]:
    tags = " ".join(t for vals in (skill.get("tags") or {}).values() for t in vals)
    return {
        "name": tokenize((skill.get("name") or "").replace("_", " ")),
        "tags": tokenize(tags),
        "description": tokenize(skill.get("description_effective") or ""),
        "path": tokenize(skill["path"].replace("/", " ").replace("_", " ")),
    }


class Index:
    def __init__(self, skills: list[dict]):
        self.skills = skills
        self.fields = [skill_fields(s) for s in skills]
        self.tf = [{f: Counter(toks) for f, toks in fl.items()} for fl in self.fields]
        self.avg_len = {
            f: (sum(len(fl[f]) for fl in self.fields) / len(self.fields)) or 1.0 for f in FIELD_WEIGHTS
        }
        df: Counter = Counter()
        for fl in self.fields:
            df.update(set(t for toks in fl.values() for t in toks))
        n = len(skills)
        self.df = df
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def score(self, i: int, q: list[str]) -> float:
        total = 0.0
        for f, w in FIELD_WEIGHTS.items():
            tf, length = self.tf[i][f], len(self.fields[i][f])
            for t in q:
                c = tf.get(t, 0)
                if not c:
                    continue
                norm = c * (BM25_K1 + 1) / (c + BM25_K1 * (1 - BM25_B + BM25_B * length / self.avg_len[f]))
                total += w * self.idf.get(t, 0.0) * norm
        return total

    def search(self, query: str, k: int = 10, use_tiers: bool = True) -> list[tuple[float, dict]]:
        q = expand_query(query)
        if not q:
            return []
        scored = []
        for i, s in enumerate(self.skills):
            raw = self.score(i, q)
            if raw <= 0:
                continue
            mult = TIER_WEIGHTS.get(s.get("tier", "extended"), 1.0) if use_tiers else 1.0
            if mult < 1.0 and any(self.df.get(t, 0) <= EXPLICIT_NAME_MAX_DF and t in self.tf[i]["name"] for t in q):
                mult = 1.0
            scored.append((raw * mult, s))
        scored.sort(key=lambda x: (-x[0], x[1]["path"]))
        if use_tiers:
            # Fold duplicate copies into their preferred copy: one slot per skill,
            # not five near-identical `proofread` rows.
            seen = {s["path"] for _, s in scored if s.get("tier") != "duplicate"}
            scored = [(sc, s) for sc, s in scored
                      if s.get("tier") != "duplicate" or s.get("duplicate_of") not in seen]
        return scored[:k]


def load_index(path: Path = ENRICHED_JSON) -> Index:
    return Index(json.loads(path.read_text(encoding="utf-8"))["skills"])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Rank AERS skills for a task description.")
    ap.add_argument("query", nargs="+", help="free-text task, e.g. 'staggered DiD event study'")
    ap.add_argument("-k", type=int, default=8, help="number of results (default 8)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-tiers", action="store_true", help="ignore catalog/curation.json tiers")
    args = ap.parse_args(argv)

    hits = load_index().search(" ".join(args.query), k=args.k, use_tiers=not args.no_tiers)
    if args.json:
        print(json.dumps([
            {"score": round(sc, 3), "name": s["name"], "path": s["path"], "tier": s.get("tier"),
             "description": s.get("description_effective", "")[:200]}
            for sc, s in hits
        ], indent=2, ensure_ascii=False))
        return 0
    if not hits:
        print("No match. Try English method words (e.g. 'synthetic control'), or browse docs/SKILL_CATALOG.md.")
        return 1
    for rank, (sc, s) in enumerate(hits, 1):
        tier = s.get("tier", "extended")
        note = f"  [{tier}" + (f" of {s['duplicate_of']}" if s.get("duplicate_of") else "") + "]" \
            if tier != "extended" else ""
        desc = (s.get("description_effective") or "").replace("\n", " ")
        print(f"{rank:2d}. {s['name']}  ({sc:.1f}){note}\n    {s['path']}\n    {desc[:160]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
