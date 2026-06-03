#!/usr/bin/env python3
"""Enrich the generated catalog with a method/stage taxonomy, an effective
description (body-derived when frontmatter is absent), and a per-skill hygiene
score.

This is an additive layer: it reads the authoritative ``catalog/skills.json`` and
``catalog/provenance.json`` (it never mutates them or any vendored skill) and
writes ``catalog/skills-enriched.json`` plus human-readable
``docs/SKILL_QUALITY.md`` and ``docs/TAXONOMY.md``. The upgraded
``docs/search.html`` consumes the enriched JSON.

Stdlib only (no PyYAML / third-party), consistent with the rest of scripts/.

    python3 scripts/build-catalog-enrich.py            # write outputs
    python3 scripts/build-catalog-enrich.py --check    # CI freshness gate
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_JSON = ROOT / "catalog" / "skills.json"
PROVENANCE_JSON = ROOT / "catalog" / "provenance.json"
ENRICHED_JSON = ROOT / "catalog" / "skills-enriched.json"
QUALITY_MD = ROOT / "docs" / "SKILL_QUALITY.md"
TAXONOMY_MD = ROOT / "docs" / "TAXONOMY.md"

SCHEMA_VERSION = 1

# Tag taxonomy. Each tag maps to regex patterns matched against a lowercased
# haystack of name + description + path. Patterns are deliberately conservative
# to avoid false positives on a 977-skill corpus.
TAXONOMY: dict[str, dict[str, list[str]]] = {
    "language": {
        "python": [r"\bpython\b", r"\bpandas\b", r"statsmodels", r"pyfixest", r"matplotlib", r"scikit", r"\.py\b"],
        "r": [r"ggplot", r"\bfixest\b", r"tidyverse", r"rmarkdown", r"data\.table", r"modelsummary", r"\br\b econometric", r"\bin r\b", r"\.r\b"],
        "stata": [r"\bstata\b", r"esttab", r"outreg2", r"reghdfe", r"\.do\b", r"ivreghdfe"],
        "latex": [r"\blatex\b", r"beamer", r"booktabs", r"overleaf", r"documentclass", r"\.tex\b"],
    },
    "method": {
        "did": [r"difference-in-differences", r"diff-in-diff", r"two-way fixed effects", r"\btwfe\b"],
        "event-study": [r"event[- ]study"],
        "staggered-did": [r"staggered", r"callaway", r"sant'?anna", r"sun[- ]abraham", r"de ?chaisemartin", r"borusyak", r"goodman[- ]bacon", r"bacon decomp"],
        "iv": [r"instrumental variable", r"\biv\b", r"2sls", r"two-stage least squares", r"first-stage f", r"weak instrument"],
        "rdd": [r"regression discontinuity", r"\brdd?\b", r"mccrary", r"rdrobust"],
        "synthetic-control": [r"synthetic control", r"\bscm\b", r"\bsynth\b"],
        "matching": [r"propensity score", r"\bpsm\b", r"\bmatching\b", r"\bipw\b", r"inverse probability", r"coarsened exact"],
        "dml": [r"double machine learning", r"\bdml\b", r"double/debiased", r"causal forest", r"meta-learner", r"\bcate\b"],
        "panel-fe": [r"panel data", r"fixed effects", r"reghdfe", r"within estimator"],
        "bayesian": [r"bayesian", r"\bmcmc\b", r"posterior", r"\bpymc\b"],
        "survival": [r"survival analysis", r"kaplan[- ]meier", r"cox proportional", r"hazard model"],
    },
    "stage": {
        "ideation": [r"topic selection", r"research question", r"ideation", r"brainstorm", r"hypothesis generation"],
        "literature": [r"literature review", r"lit[- ]review", r"related work", r"\barxiv\b", r"semantic scholar"],
        "data": [r"data cleaning", r"data wrangling", r"data collection", r"web scraping", r"panel construction"],
        "analysis": [r"\bestimation\b", r"\bregression\b", r"causal infer", r"econometric", r"identification"],
        "robustness": [r"robustness", r"placebo", r"sensitivity analysis", r"falsification", r"specification curve"],
        "writing": [r"paper writing", r"academic writing", r"manuscript", r"\bintroduction\b", r"\babstract\b"],
        "tables-figures": [r"regression table", r"booktabs", r"visualization", r"coefficient plot", r"esttab", r"modelsummary"],
        "presentation": [r"\bslides\b", r"beamer", r"presentation", r"\bposter\b"],
        "citation": [r"bibtex", r"citation management", r"zotero", r"reference manager", r"\.bib\b"],
        "submission": [r"submission", r"cover letter", r"desk reject", r"replication package", r"\breferee\b"],
        "peer-review": [r"peer review", r"rebuttal", r"response to reviewers", r"\br&r\b", r"reviewer report"],
        "reproduction": [r"replicat", r"reproducib"],
        "de-aigc": [r"de-aigc", r"降.{0,3}aigc", r"humaniz", r"ai writing", r"\baigc\b", r"deslop", r"\bslop\b", r"去ai"],
    },
    "topic": {
        "causal-inference": [r"causal infer", r"treatment effect", r"counterfactual"],
        "econometrics": [r"econometric", r"applied micro", r"panel data"],
        "scientific-writing": [r"scientific writing", r"academic writing", r"manuscript"],
        "proofreading": [r"proofread", r"copy-edit", r"\bediting\b"],
        "reproducibility": [r"reproducib", r"replication package", r"replicat"],
    },
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def skip_leading_comment(lines: list[str]) -> list[str]:
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith("<!--"):
        while i < len(lines) and "-->" not in lines[i]:
            i += 1
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
    return lines[i:]


def derive_description(text: str, limit: int = 240) -> str:
    """First prose sentence after the banner/frontmatter, for skills whose
    frontmatter description is missing."""
    lines = skip_leading_comment(text.splitlines())
    # Drop a frontmatter block if present.
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                lines = lines[j + 1:]
                break
    in_fence = False
    first_heading = ""
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not s:
            continue
        if s.startswith("#") and not first_heading:
            first_heading = s.lstrip("# ").strip()
        if s.startswith(("#", ">", "-", "*", "|", "<!--")):
            continue
        s = re.sub(r"\s+", " ", s).strip()
        if len(s) < 12:
            continue
        m = re.match(r"(.+?[.!?。！？])(\s|$)", s)
        out = (m.group(1) if m else s).strip()
        return out if len(out) <= limit else out[: limit - 1].rstrip() + "…"
    # Fallback: a skill that is only a heading + code fence still gets a label.
    if first_heading:
        return first_heading if len(first_heading) <= limit else first_heading[: limit - 1] + "…"
    return ""


def assign_tags(haystack: str) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for facet, rules in TAXONOMY.items():
        hits = [tag for tag, pats in rules.items()
                if any(re.search(p, haystack) for p in pats)]
        if hits:
            tags[facet] = sorted(hits)
    return tags


def has_references(skill_path: Path) -> bool:
    refs = (ROOT / skill_path).parent / "references"
    return refs.is_dir() and any(refs.iterdir())


def score_skill(skill: dict, eff_desc: str, desc_source: str, refs: bool) -> tuple[int, list[str]]:
    score, flags = 100, []
    if not skill.get("has_frontmatter"):
        score -= 30
        flags.append("no-frontmatter")
    if not eff_desc:
        score -= 25
        flags.append("no-description")
    elif desc_source == "derived":
        score -= 8
        flags.append("description-derived-from-body")
    if not skill.get("has_name"):
        score -= 5
        flags.append("no-name")
    lc = skill.get("line_count", 0)
    if lc > 800 and not refs:
        score -= 15
        flags.append("very-long-no-references")
    elif lc > 500 and not refs:
        score -= 8
        flags.append("long-no-references")
    if eff_desc and len(eff_desc) < 40:
        score -= 5
        flags.append("short-description")
    return max(0, min(100, score)), flags


def build() -> dict:
    catalog = load_json(SKILLS_JSON)
    provenance = load_json(PROVENANCE_JSON)
    prov_by_id = {c["id"]: c for c in provenance.get("collections", [])}

    enriched = []
    facet_counts: dict[str, dict[str, int]] = {f: {} for f in TAXONOMY}
    for skill in catalog.get("skills", []):
        path = Path(skill["path"])
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")

        desc = (skill.get("description") or "").strip()
        if desc:
            eff_desc, desc_source = desc, "frontmatter"
        else:
            eff_desc = derive_description(text)
            desc_source = "derived" if eff_desc else "none"

        haystack = " ".join([skill.get("name", ""), eff_desc, skill["path"]]).lower()
        tags = assign_tags(haystack)
        for facet, hits in tags.items():
            for tag in hits:
                facet_counts[facet][tag] = facet_counts[facet].get(tag, 0) + 1

        refs = has_references(path)
        score, flags = score_skill(skill, eff_desc, desc_source, refs)
        prov = prov_by_id.get(skill["collection"], {})
        enriched.append({
            "name": skill.get("name"),
            "path": skill["path"],
            "collection": skill["collection"],
            "line_count": skill.get("line_count", 0),
            "description_effective": eff_desc,
            "description_source": desc_source,
            "has_references": refs,
            "tags": tags,
            "quality_score": score,
            "quality_flags": flags,
            "license": prov.get("license"),
            "commercial_use": prov.get("commercial_use"),
            "source_url": prov.get("source_url"),
            "sync": prov.get("sync"),
        })

    enriched.sort(key=lambda s: s["path"])
    scores = [s["quality_score"] for s in enriched]
    summary = {
        "skills": len(enriched),
        "mean_quality_score": round(sum(scores) / len(scores), 1) if scores else 0,
        "with_frontmatter_description": sum(1 for s in enriched if s["description_source"] == "frontmatter"),
        "body_derived_description": sum(1 for s in enriched if s["description_source"] == "derived"),
        "no_description": sum(1 for s in enriched if s["description_source"] == "none"),
        "tagged": sum(1 for s in enriched if s["tags"]),
    }
    taxonomy = {f: dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))) for f, c in facet_counts.items()}
    return {
        "generated_by": "scripts/build-catalog-enrich.py",
        "schema_version": SCHEMA_VERSION,
        "summary": summary,
        "taxonomy": taxonomy,
        "skills": enriched,
    }


def render_quality_md(payload: dict) -> str:
    s = payload["summary"]
    skills = payload["skills"]
    by_collection: dict[str, list[dict]] = {}
    for sk in skills:
        by_collection.setdefault(sk["collection"], []).append(sk)

    lines = [
        "# Skill Quality Scorecard",
        "",
        "Generated by `scripts/build-catalog-enrich.py`. The hygiene score is a "
        "**structural** signal (frontmatter, description, length vs. progressive "
        "disclosure) — not a correctness judgement. For correctness see "
        "[`eval-harness/`](../eval-harness/) and [`benchmark/`](../benchmark/).",
        "",
        "## Summary",
        "",
        f"- Skills scored: {s['skills']}",
        f"- Mean hygiene score: **{s['mean_quality_score']}/100**",
        f"- Descriptions: {s['with_frontmatter_description']} from frontmatter, "
        f"{s['body_derived_description']} body-derived, {s['no_description']} none",
        f"- Tagged with at least one taxonomy facet: {s['tagged']}",
        "",
        "## Per-collection hygiene",
        "",
        "| Collection | Skills | Mean score | Lowest |",
        "|---|---:|---:|---:|",
    ]
    for coll in sorted(by_collection):
        group = by_collection[coll]
        mean = round(sum(g["quality_score"] for g in group) / len(group), 1)
        low = min(g["quality_score"] for g in group)
        lines.append(f"| `{coll}` | {len(group)} | {mean} | {low} |")

    lowest = sorted(skills, key=lambda x: x["quality_score"])[:25]
    lines += ["", "## 25 lowest-hygiene skills (improvement targets)", "",
              "| Score | Skill | Flags |", "|---:|---|---|"]
    for sk in lowest:
        flags = ", ".join(sk["quality_flags"]) or "-"
        lines.append(f"| {sk['quality_score']} | [`{sk['path']}`]({_doc_rel(sk['path'])}) | {flags} |")
    return "\n".join(lines) + "\n"


def render_taxonomy_md(payload: dict) -> str:
    tax = payload["taxonomy"]
    skills = payload["skills"]
    lines = [
        "# Skill Taxonomy",
        "",
        "Generated by `scripts/build-catalog-enrich.py`. Tags are inferred from "
        "each skill's name, description, and path with conservative keyword rules, "
        "so coverage is a floor, not a census. Use [`search.html`](search.html) to "
        "filter interactively.",
        "",
    ]
    facet_titles = {"language": "Languages", "method": "Methods",
                    "stage": "Workflow stages", "topic": "Topics"}
    for facet in ("stage", "method", "language", "topic"):
        lines += [f"## {facet_titles[facet]}", "", "| Tag | Skills |", "|---|---:|"]
        for tag, count in tax.get(facet, {}).items():
            lines.append(f"| `{tag}` | {count} |")
        lines.append("")
    # Method index: list skills per method tag (selective, bounded).
    lines += ["## Skills by method", ""]
    for tag in tax.get("method", {}):
        members = [sk for sk in skills if tag in sk["tags"].get("method", [])]
        lines.append(f"<details><summary><b>{tag}</b> ({len(members)})</summary>")
        lines.append("")
        for sk in members[:40]:
            lines.append(f"- [`{sk['path']}`]({_doc_rel(sk['path'])})")
        if len(members) > 40:
            lines.append(f"- …and {len(members) - 40} more")
        lines += ["", "</details>", ""]
    return "\n".join(lines) + "\n"


def _doc_rel(repo_path: str) -> str:
    # Links in docs/*.md are relative to docs/.
    return "../" + repo_path


def write_outputs(payload: dict) -> None:
    ENRICHED_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    QUALITY_MD.write_text(render_quality_md(payload), encoding="utf-8")
    TAXONOMY_MD.write_text(render_taxonomy_md(payload), encoding="utf-8")
    print(f"Wrote {ENRICHED_JSON.relative_to(ROOT)}")
    print(f"Wrote {QUALITY_MD.relative_to(ROOT)}")
    print(f"Wrote {TAXONOMY_MD.relative_to(ROOT)}")


def check_outputs(payload: dict) -> int:
    problems = []
    if not ENRICHED_JSON.exists() or ENRICHED_JSON.read_text(encoding="utf-8") != \
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n":
        problems.append("catalog/skills-enriched.json is stale")
    if not QUALITY_MD.exists() or QUALITY_MD.read_text(encoding="utf-8") != render_quality_md(payload):
        problems.append("docs/SKILL_QUALITY.md is stale")
    if not TAXONOMY_MD.exists() or TAXONOMY_MD.read_text(encoding="utf-8") != render_taxonomy_md(payload):
        problems.append("docs/TAXONOMY.md is stale")
    if problems:
        for p in problems:
            print(f"  - {p}")
        print("Run: python3 scripts/build-catalog-enrich.py")
        return 1
    print("Enriched catalog outputs are current.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify outputs are current")
    args = ap.parse_args(argv)
    payload = build()
    if args.check:
        return check_outputs(payload)
    write_outputs(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
