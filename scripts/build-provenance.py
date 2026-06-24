#!/usr/bin/env python3
"""Build source and license provenance for top-level AERS skill collections."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DEFAULT_JSON = ROOT / "catalog" / "provenance.json"
DEFAULT_MARKDOWN = ROOT / "docs" / "LICENSE_AUDIT.md"
SCAN_DATE = "2026-05-31"


OVERRIDES: dict[str, dict[str, object]] = {
    # --- folder-name-encoded upstreams ---------------------------------------
    # These vendored skills follow the "NN-<github-owner>-<repo>" naming
    # convention, so their upstream URL was previously *derived* from the
    # directory name by infer_source_url(). That heuristic has been removed
    # (it could not tell an "owner-repo" folder from a descriptive one and
    # fabricated 404s such as "github.com/game/theory-paper-writer"), so the
    # mapping is now pinned explicitly. URLs verified reachable on 2026-06-23;
    # confidence stays "low" because folder-name match is not an independently
    # verified content match. Values reproduce the prior inferred output exactly.
    "14-luischanci-claude-code-research-starter": {
        "source_url": "https://github.com/luischanci/claude-code-research-starter",
        "source_confidence": "low",
    },
    "20-wenddymacro-python-econ-skill": {
        "source_url": "https://github.com/wenddymacro/python-econ-skill",
        "source_confidence": "low",
    },
    "22-christopherkenny-skills": {
        "source_url": "https://github.com/christopherkenny/skills",
        "source_confidence": "low",
    },
    "28-maxwell2732-paper-replicate-agent-demo": {
        "source_url": "https://github.com/maxwell2732/paper-replicate-agent-demo",
        "source_confidence": "low",
    },
    "36-taoyunudt-literature-review-skill": {
        "source_url": "https://github.com/taoyunudt/literature-review-skill",
        "source_confidence": "low",
    },
    "46-hardikpandya-stop-slop": {
        "source_url": "https://github.com/hardikpandya/stop-slop",
        "source_confidence": "low",
    },
    "00-Full-empirical-analysis-skill_StatsPAI": {
        "source_url": "https://github.com/brycewang-stanford/StatsPAI",
        "license": "MIT",
        "origin": "first-party upstream mirror",
        "sync": "weekly GitHub Actions sync",
        "source_confidence": "high",
    },
    "00.1-Full-empirical-analysis-skill_Python": {
        "source_url": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills",
        "license": "CC-BY-SA-4.0 (repository default)",
        "origin": "first-party AERS skill",
        "sync": "manual",
        "source_confidence": "high",
    },
    "00.2-Full-empirical-analysis-skill_Stata": {
        "source_url": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills",
        "license": "CC-BY-SA-4.0 (repository default)",
        "origin": "first-party AERS skill",
        "sync": "manual",
        "source_confidence": "high",
    },
    "00.3-Full-empirical-analysis-skill_R": {
        "source_url": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills",
        "license": "CC-BY-SA-4.0 (repository default)",
        "origin": "first-party AERS skill",
        "sync": "manual",
        "source_confidence": "high",
    },
    "48-copaper-ai-chinese-de-aigc": {
        "source_url": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills",
        "license": "CC-BY-SA-4.0 (repository default)",
        "origin": "first-party AERS skill",
        "sync": "manual",
        "source_confidence": "high",
    },
    "50-brycewang-aer-skills": {
        "source_url": "https://github.com/brycewang-stanford/AER-skills",
        "license": "MIT",
        "origin": "first-party upstream mirror",
        "sync": "weekly GitHub Actions sync",
        "source_confidence": "high",
    },
    "12-pedrohcgs-claude-code-my-workflow": {
        "source_url": "https://github.com/pedrohcgs/claude-code-my-workflow",
        "source_confidence": "high",
    },
    "13-scunning1975-MixtapeTools": {
        "source_url": "https://github.com/scunning1975/MixtapeTools",
        "source_confidence": "high",
    },
    "15-Felpix-Studios-social-science-research": {
        "source_url": "https://github.com/Felpix-Studios/social-science-research",
        "source_confidence": "high",
    },
    "16-hsantanna88-clo-author": {
        "source_url": "https://github.com/hsantanna88/clo-author",
        "source_confidence": "high",
    },
    "18-jusi-aalto-stata-accounting-research": {
        "source_url": None,
        "source_confidence": "unresolved",
        "origin": "vendored snapshot; upstream URL unresolved as of 2026-05-31",
    },
    "27-dariia-m-my_claude_skills": {
        "source_url": "https://github.com/dariia-m/my_claude_skills",
        "source_confidence": "high",
    },
    "29-quarcs-lab-project20XXy": {
        "source_url": None,
        "source_confidence": "unresolved",
        "origin": "vendored snapshot; upstream URL unresolved as of 2026-05-31",
    },
    "31-thalysandratos-claude-code-skills": {
        "source_url": "https://github.com/thalysandratos/claude-code-skills",
        "source_confidence": "high",
    },
    "35-bahayonghang-academic-writing-skills": {
        "source_url": "https://github.com/bahayonghang/academic-writing-skills",
        "source_confidence": "high",
    },
    "38-peternka-academic-proofreader": {
        "source_url": None,
        "source_confidence": "unresolved",
        "origin": "vendored snapshot; upstream URL unresolved as of 2026-05-31",
    },
    "44-matsuikentaro1-humanizer_academic": {
        "source_url": "https://github.com/matsuikentaro1/humanizer_academic",
        "source_confidence": "high",
    },
    "49-voidborne-d-humanize-chinese": {
        "source_url": None,
        "source_confidence": "unresolved",
        "origin": "vendored snapshot; upstream URL unresolved as of 2026-05-31",
    },
    # --- 2026-06-01 empirical-skills expansion (51-62) ---
    "51-pymc-labs-CausalPy": {
        "source_url": "https://github.com/pymc-labs/CausalPy",
        "license": "Apache-2.0",
        "origin": "vendored upstream snapshot (causalpy/skills component) 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "52-keemanxp-slr-prisma": {
        "source_url": "https://github.com/keemanxp/slr-prisma",
        "license": "MIT",
        "origin": "vendored upstream snapshot 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "53-keemanxp-thematic-analysis-skill": {
        "source_url": "https://github.com/keemanxp/thematic-analysis-skill",
        "license": "MIT",
        "origin": "vendored upstream snapshot 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "54-scdenney-open-science-skills": {
        "source_url": "https://github.com/scdenney/open-science-skills",
        "license": "CC-BY-NC-4.0 (non-commercial)",
        "origin": "vendored upstream snapshot 2026-06-01 (Claude-native skills only; -codex variants and presubmit excluded)",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "55-ab604-claude-code-r-skills": {
        "source_url": "https://github.com/ab604/claude-code-r-skills",
        "license": "MIT",
        "origin": "vendored upstream snapshot 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "56-hanlulong-econ-writing-skill": {
        "source_url": "https://github.com/hanlulong/econ-writing-skill",
        "license": "MIT",
        "origin": "vendored upstream snapshot 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "57-dgunning-edgartools": {
        "source_url": "https://github.com/dgunning/edgartools",
        "license": "MIT",
        "origin": "vendored upstream snapshot (edgar/ai/skills component) 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "58-charlescoverdale-econstack": {
        "source_url": "https://github.com/charlescoverdale/econstack",
        "license": "MIT",
        "origin": "vendored snapshot 2026-06-01; MIT declared in upstream README (badge + License section), no separate LICENSE file upstream",
        "sync": "manual vendor snapshot",
        "source_confidence": "medium",
    },
    "59-shiquda-openalex-skill": {
        "source_url": "https://github.com/shiquda/openalex-skill",
        "license": "MIT",
        "origin": "vendored upstream snapshot 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "60-regisely-superpapers": {
        "source_url": "https://github.com/regisely/superpapers",
        "license": "MIT",
        "origin": "vendored upstream snapshot 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "61-phdemotions-research-methods": {
        "source_url": "https://github.com/phdemotions/research-methods",
        "license": "MIT",
        "origin": "vendored upstream snapshot 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    "62-PHY041-claude-skill-citation-checker": {
        "source_url": "https://github.com/PHY041/claude-skill-citation-checker",
        "license": "MIT",
        "origin": "vendored snapshot 2026-06-01; MIT declared in upstream README (## License), no separate LICENSE file upstream",
        "sync": "manual vendor snapshot",
        "source_confidence": "medium",
    },
    "63-tondevrel-scientific-agent-skills": {
        "source_url": "https://github.com/tondevrel/scientific-agent-skills",
        "license": "MIT",
        "origin": "vendored upstream snapshot (dowhy + lifelines subset; dowhy SKILL.MD renamed to SKILL.md) 2026-06-01",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    # --- 2026-06-03 Stata expansion ---
    "64-tmonk-mcp-stata": {
        "source_url": "https://github.com/tmonk/mcp-stata",
        "license": "AGPL-3.0",
        "origin": "vendored upstream snapshot (plugin/skills component only — 20 SKILL.md skills + LICENSE; Python/Rust MCP server, installers, tests excluded) 2026-06-03. AGPL-3.0 retained as a separately-licensed aggregate; not relicensed under the repo default.",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    # --- 2026-06-15 game-theory + empirical-research expansion ---
    "65-game-theory-paper-writer": {
        "source_url": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/pull/17",
        "license": "CC-BY-SA-4.0",
        "origin": "original community contribution via PR #17 (game-theory paper-writing skill); no external upstream — repo-default license applies",
        "sync": "manual",
        "source_confidence": "medium",
    },
    "66-zheng-siyao-empirical-research-skills": {
        "source_url": "https://github.com/SiyaoZheng/ai4ss-skills",
        "license": "GPL-3.0",
        "origin": "vendored upstream snapshot (7 SKILL.md skills) from SiyaoZheng/ai4ss-skills (郑思尧 / AI4SS) 2026-06-15; contributed via PR #18",
        "sync": "manual vendor snapshot",
        "source_confidence": "high",
    },
    # --- 2026-06-18 community PR contributions ---
    "67-econfin-workflow-toolkit": {
        "source_url": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/pull/22",
        "license": "Mixed (per-skill; see folder)",
        "origin": "community contribution via PR #22 (econ/finance research workflow toolkit). Proprietary Anthropic office skills (docx/pdf/pptx/xlsx) and general-purpose UI skills (frontend-design, ui-ux-pro-max) removed before vendoring 2026-06-18.",
        "sync": "manual vendor snapshot",
        "source_confidence": "medium",
    },
    "68-research-productivity-skills": {
        "source_url": "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/pull/21",
        "license": "Mixed (per-skill; see folder)",
        "origin": "community contribution via PR #21 (research productivity skills). Proprietary Anthropic office skills (docx/pdf/pptx/xlsx) and general-purpose UI skills (frontend-design, ui-ux-pro-max) removed before vendoring 2026-06-18.",
        "sync": "manual vendor snapshot",
        "source_confidence": "medium",
    },
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_skill_files(collection_path: Path) -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(collection_path):
        dirnames[:] = [name for name in dirnames if name not in {".git", "__pycache__"}]
        for filename in filenames:
            if filename == "SKILL.md":
                paths.append(Path(dirpath) / filename)
    return sorted(paths)


def normalize_github_repo_url(url: str) -> str | None:
    parsed = urlparse(url.strip().rstrip(".,)"))
    if parsed.netloc.lower() != "github.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1].removesuffix(".git")
    if owner in {"user-attachments", "org", "YOUR_USERNAME"}:
        return None
    return f"https://github.com/{owner}/{repo}"


def github_candidates(text: str) -> list[str]:
    urls = re.findall(
        r"(?:https://)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?(?:/[^\s)>\"]*)?",
        text,
    )
    seen: set[str] = set()
    candidates: list[str] = []
    for url in urls:
        normalized = normalize_github_repo_url(url if url.startswith("https://") else f"https://{url}")
        if normalized and normalized not in seen:
            seen.add(normalized)
            candidates.append(normalized)
    return candidates


def infer_source_url(collection: str, text: str) -> tuple[str | None, str]:
    source_line = re.search(r"(?:来源仓库|Source)\s*[:：]\s*(https://github\.com/[^\s)]+)", text, re.I)
    if source_line:
        normalized = normalize_github_repo_url(source_line.group(1))
        if normalized:
            return normalized, "high"

    candidates = github_candidates(text)
    if candidates:
        slug = re.sub(r"^\d+(?:\.\d+)?-", "", collection).lower()
        slug = slug.replace("_", "-")
        for candidate in candidates:
            candidate_slug = candidate.rsplit("/", 1)[-1].lower()
            if candidate_slug in slug or slug.endswith(candidate_slug):
                return candidate, "medium"
        return candidates[0], "medium"

    # No URL is fabricated from the directory name. Splitting "NN-foo-bar" on the
    # first hyphen used to emit "github.com/foo/bar", but the folder name cannot
    # be told apart from a purely descriptive one (e.g. "game-theory-paper-writer"
    # produced the bogus 404 "github.com/game/theory-paper-writer"). Per the
    # repo's "never invent a source" rule, return UNKNOWN and let a maintainer
    # pin the real upstream in OVERRIDES instead.
    return None, "unknown"


def infer_license(collection_path: Path, text: str) -> tuple[str, str | None]:
    license_files = [
        path
        for name in ("LICENSE", "LICENSE.md", "COPYING")
        if (path := collection_path / name).exists()
    ]
    license_text = "\n".join(read_text(path)[:4000] for path in license_files)
    combined = f"{license_text}\n{text[:12000]}"
    lower = combined.lower()

    if "non-commercial" in lower or "noncommercial" in lower or "non commercial" in lower:
        return "MIT Non-Commercial", rel(license_files[0]) if license_files else None
    if "mit license" in lower or "license-mit" in lower or "开源协议: mit" in lower:
        return "MIT", rel(license_files[0]) if license_files else None
    if "apache license" in lower or "apache-2.0" in lower:
        return "Apache-2.0", rel(license_files[0]) if license_files else None
    if "bsd license" in lower:
        return "BSD", rel(license_files[0]) if license_files else None
    if "cc by-sa" in lower or "creative commons attribution-sharealike" in lower:
        return "CC-BY-SA-4.0", rel(license_files[0]) if license_files else None
    return "UNKNOWN - check upstream", rel(license_files[0]) if license_files else None


def commercial_use(license_name: str) -> str:
    lower = license_name.lower()
    if "non-commercial" in lower or "noncommercial" in lower:
        return "restricted"
    if lower.startswith(("mit", "apache", "bsd")):
        return "allowed"
    if lower.startswith("cc-by-sa"):
        return "share-alike"
    if "agpl" in lower or "gpl" in lower:
        # Copyleft: commercial use permitted, but derivative/network use must
        # share source under the same license.
        return "share-alike"
    return "unknown"


def read_collection_text(collection_path: Path) -> str:
    parts: list[str] = []
    for name in ("README-original.md", "README.md", "CLAUDE.md"):
        path = collection_path / name
        if path.exists():
            parts.append(read_text(path))
    for skill_path in iter_skill_files(collection_path)[:5]:
        parts.append(read_text(skill_path)[:5000])
    return "\n\n".join(parts)


def collection_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    if not SKILLS_DIR.exists():
        return records

    for collection_path in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        skills = iter_skill_files(collection_path)
        if not skills:
            continue

        collection = collection_path.name
        text = read_collection_text(collection_path)
        source_url, confidence = infer_source_url(collection, text)
        license_name, license_file = infer_license(collection_path, text)

        record: dict[str, object] = {
            "id": collection,
            "path": rel(collection_path),
            "source_url": source_url,
            "source_confidence": confidence,
            "origin": "vendored upstream",
            "sync": "manual vendor snapshot",
            "vendored_commit": None,
            "license": license_name,
            "license_file": license_file,
            "commercial_use": commercial_use(license_name),
            "skill_count": len(skills),
            "security_review": "SECURITY-SCAN-REPORT.md",
            "last_aers_review": SCAN_DATE,
        }
        if collection in OVERRIDES:
            record.update(OVERRIDES[collection])
            record["commercial_use"] = commercial_use(str(record["license"]))
        records.append(record)

    return records


def build_payload() -> dict[str, object]:
    records = collection_records()
    return {
        "schema_version": "1.0",
        "generated_by": "scripts/build-provenance.py",
        "scan_date": SCAN_DATE,
        "summary": {
            "collections": len(records),
            "licenses": dict(sorted(Counter(str(record["license"]) for record in records).items())),
            "commercial_use": dict(
                sorted(Counter(str(record["commercial_use"]) for record in records).items())
            ),
            "source_confidence": dict(
                sorted(Counter(str(record["source_confidence"]) for record in records).items())
            ),
        },
        "collections": records,
    }


def markdown_escape(text: object) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ").strip()


def render_markdown(payload: dict[str, object]) -> str:
    summary = payload["summary"]
    records = payload["collections"]

    lines = [
        "# License and Provenance Audit",
        "",
        "This file is generated by `scripts/build-provenance.py`. Do not edit it by hand; run `make catalog` after changing vendored skills.",
        "",
        f"Scan date: {payload['scan_date']}.",
        "",
        "## Summary",
        "",
        f"- Collections audited: {summary['collections']}",
        f"- License buckets: {', '.join(f'{key}={value}' for key, value in summary['licenses'].items())}",
        f"- Commercial-use buckets: {', '.join(f'{key}={value}' for key, value in summary['commercial_use'].items())}",
        f"- Source-confidence buckets: {', '.join(f'{key}={value}' for key, value in summary['source_confidence'].items())}",
        "",
        "## Interpretation",
        "",
        "- `allowed`: permissive license detected locally or from upstream README text.",
        "- `restricted`: non-commercial restriction detected; do not use in paid products without separate permission.",
        "- `share-alike`: repository-default CC BY-SA terms may apply; derivative redistribution has share-alike obligations.",
        "- `unknown`: no reliable local license signal was detected; check upstream before reuse.",
        "",
        "## Collection Table",
        "",
        "| Collection | Source | Confidence | License | Commercial use | Sync |",
        "|---|---|---|---|---|---|",
    ]
    for record in records:
        source = record["source_url"]
        source_cell = f"[source]({source})" if source else "UNKNOWN"
        lines.append(
            "| [`{id}`](../{path}/) | {source} | {confidence} | {license} | {commercial} | {sync} |".format(
                id=markdown_escape(record["id"]),
                path=record["path"],
                source=source_cell,
                confidence=markdown_escape(record["source_confidence"]),
                license=markdown_escape(record["license"]),
                commercial=markdown_escape(record["commercial_use"]),
                sync=markdown_escape(record["sync"]),
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(payload: dict[str, object], json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")


def check_outputs(payload: dict[str, object], json_path: Path, markdown_path: Path) -> int:
    expected_json = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    expected_markdown = render_markdown(payload)
    failures: list[str] = []
    if not json_path.exists() or json_path.read_text(encoding="utf-8") != expected_json:
        failures.append(str(json_path.relative_to(ROOT)))
    if not markdown_path.exists() or markdown_path.read_text(encoding="utf-8") != expected_markdown:
        failures.append(str(markdown_path.relative_to(ROOT)))
    if failures:
        print("Provenance outputs are stale. Regenerate with `make catalog`.", file=sys.stderr)
        for failure in failures:
            print(f"stale: {failure}", file=sys.stderr)
        return 1
    print("Provenance outputs are current.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    if args.check:
        return check_outputs(payload, args.json, args.markdown)

    write_outputs(payload, args.json, args.markdown)
    print(f"Wrote {args.json.relative_to(ROOT)}")
    print(f"Wrote {args.markdown.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
