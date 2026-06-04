#!/usr/bin/env python3
"""Validate the AERS tools catalog and (re)generate its derived browse files.

`tools/tools.json` is the hand-curated source of truth — a list of automated
empirical-research / causal-inference *tools* (libraries, MCP servers, causal
discovery packages, benchmark datasets) as distinct from agent *skills* (which
live under `skills/` and are catalogued by `build-catalog.py`).

This script:
  * validates every record against a small, explicit schema;
  * regenerates `tools/CATALOG.md` (a deterministic, grouped browse table);
  * fills the generated summary block inside `tools/README.md`.

Run `python3 scripts/build-tools-catalog.py` to rebuild, or pass `--check` to
fail (exit 1) on any schema error or stale generated output — the `--check`
form is wired into `make validate` / CI so the catalog cannot silently drift
from its generated views.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"
TOOLS_JSON = TOOLS_DIR / "tools.json"
CATALOG_MD = TOOLS_DIR / "CATALOG.md"
README_MD = TOOLS_DIR / "README.md"

SUMMARY_BEGIN = "<!-- BEGIN GENERATED: summary (scripts/build-tools-catalog.py) -->"
SUMMARY_END = "<!-- END GENERATED: summary -->"

# --- schema -----------------------------------------------------------------

CATEGORIES = {
    "causal-inference-library": "Causal-inference & treatment-effect libraries",
    "econometrics-library": "Econometrics & quasi-experimental libraries",
    "causal-discovery": "Causal discovery / structure learning",
    "research-agent": "Autonomous research & data-science agents",
    "benchmark-dataset": "Benchmarks & datasets",
    "mcp-server": "MCP servers (data & stats execution)",
}
# Stable display order for the catalog (largest / most-foundational first).
CATEGORY_ORDER = [
    "causal-inference-library",
    "econometrics-library",
    "causal-discovery",
    "research-agent",
    "mcp-server",
    "benchmark-dataset",
]
MAINTAINED = {"active", "maintained", "dormant", None}
AUTOMATION = {"library", "framework", "application", "mcp-server", "dataset", None}
REQUIRED_KEYS = {
    "id",
    "name",
    "category",
    "subcategory",
    "languages",
    "license",
    "owner_repo",
    "url",
    "homepage",
    "stars_approx",
    "last_activity",
    "maintained",
    "automation_level",
    "description",
    "verified",
}

LANG_LABEL = {
    "python": "Python",
    "r": "R",
    "stata": "Stata",
    "julia": "Julia",
    "java": "Java",
    "cpp": "C++",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
}
STATUS_BADGE = {"active": "🟢 active", "maintained": "🟡 maintained", "dormant": "🔴 dormant"}


def load_tools() -> list[dict]:
    payload = json.loads(TOOLS_JSON.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("tools"), list):
        raise SystemExit("error: tools/tools.json must be an object with a `tools` array")
    return payload["tools"]


def validate(tools: list[dict]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()

    for i, t in enumerate(tools):
        where = t.get("id") or t.get("name") or f"index {i}"
        missing = REQUIRED_KEYS - set(t)
        if missing:
            errors.append(f"{where}: missing keys {sorted(missing)}")
            continue

        if t["category"] not in CATEGORIES:
            errors.append(f"{where}: unknown category {t['category']!r}")
        if not isinstance(t["subcategory"], list):
            errors.append(f"{where}: subcategory must be a list")
        if not isinstance(t["languages"], list):
            errors.append(f"{where}: languages must be a list")
        if not (isinstance(t["url"], str) and t["url"].startswith("http")):
            errors.append(f"{where}: url must be an http(s) string")
        if t["maintained"] not in MAINTAINED:
            errors.append(f"{where}: invalid maintained {t['maintained']!r}")
        if t["automation_level"] not in AUTOMATION:
            errors.append(f"{where}: invalid automation_level {t['automation_level']!r}")
        if not str(t.get("license") or "").strip():
            errors.append(f"{where}: empty license (use 'unverified' if unknown)")
        if not str(t.get("description") or "").strip():
            errors.append(f"{where}: empty description")
        if not isinstance(t["verified"], bool):
            errors.append(f"{where}: verified must be boolean")
        if t["category"] == "mcp-server" and "data_source" not in t:
            errors.append(f"{where}: mcp-server entries need a data_source field (may be null)")

        tid = t.get("id")
        if tid in seen_ids:
            errors.append(f"{where}: duplicate id {tid!r}")
        seen_ids.add(tid)

        url_key = (t.get("url") or "").rstrip("/").lower()
        if url_key in seen_urls:
            errors.append(f"{where}: duplicate url {t.get('url')!r}")
        seen_urls.add(url_key)

    # Source-of-truth ordering: (category, name lower) — keeps diffs minimal.
    expected = sorted(tools, key=lambda x: (x.get("category", ""), x.get("name", "").lower()))
    if [t.get("id") for t in tools] != [t.get("id") for t in expected]:
        errors.append("tools.json is not sorted by (category, name); re-run the builder to fix ordering")

    return errors


# --- rendering --------------------------------------------------------------


def lang_str(langs: list[str]) -> str:
    return " · ".join(LANG_LABEL.get(x, x) for x in langs) or "—"


def status_str(t: dict) -> str:
    badge = STATUS_BADGE.get(t.get("maintained"), "—")
    act = t.get("last_activity")
    return f"{badge}" + (f" · {act}" if act else "")


def tool_link(t: dict) -> str:
    name = t["name"].replace("|", "\\|")
    return f"[{name}]({t['url']})"


def summary_tables(tools: list[dict]) -> str:
    by_cat = Counter(t["category"] for t in tools)
    by_lang: Counter[str] = Counter()
    for t in tools:
        for lang in t["languages"]:
            by_lang[lang] += 1
    by_status = Counter(str(t.get("maintained")) for t in tools)
    by_license_class: Counter[str] = Counter()
    for t in tools:
        lic = t["license"]
        if lic in {"unverified", "NOASSERTION"}:
            by_license_class["unverified / unmapped"] += 1
        elif any(tag in lic for tag in ("Commons Clause", "Responsible-AI", "Scientist Source", "custom")):
            by_license_class["non-OSI / custom"] += 1
        elif lic.startswith(("GPL", "AGPL", "LGPL")):
            by_license_class["copyleft (GPL/AGPL/LGPL)"] += 1
        else:
            by_license_class["permissive (MIT/BSD/Apache/…)"] += 1

    lines: list[str] = []
    lines.append(f"**{len(tools)} tools** across {len(by_cat)} categories.")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    for cat in CATEGORY_ORDER:
        if by_cat.get(cat):
            lines.append(f"| {CATEGORIES[cat]} | {by_cat[cat]} |")
    lines.append("")
    lines.append("| By language | Tools | | By maintenance | Tools | | By license | Tools |")
    lines.append("|---|---:|:-:|---|---:|:-:|---|---:|")
    lang_rows = [(LANG_LABEL.get(k, k), v) for k, v in by_lang.most_common()]
    status_rows = [
        (STATUS_BADGE.get(k, k), v)
        for k, v in sorted(by_status.items(), key=lambda kv: {"active": 0, "maintained": 1, "dormant": 2}.get(kv[0], 9))
    ]
    lic_rows = list(by_license_class.most_common())
    for idx in range(max(len(lang_rows), len(status_rows), len(lic_rows))):
        la, lv = lang_rows[idx] if idx < len(lang_rows) else ("", "")
        sa, sv = status_rows[idx] if idx < len(status_rows) else ("", "")
        ca, cv = lic_rows[idx] if idx < len(lic_rows) else ("", "")
        lines.append(f"| {la} | {lv} |  | {sa} | {sv} |  | {ca} | {cv} |")
    return "\n".join(lines)


def render_catalog(tools: list[dict]) -> str:
    out: list[str] = []
    out.append("# Tools Catalog — Automated Empirical Research & Causal Inference")
    out.append("")
    out.append(
        "<!-- GENERATED by scripts/build-tools-catalog.py from tools/tools.json — do not edit by hand. -->"
    )
    out.append("")
    out.append(
        "Curated, license- and maintenance-aware index of **software tools** for automated "
        "empirical research and causal inference — distinct from the agent **skills** under "
        "[`../skills/`](../skills/). Source of truth: [`tools.json`](tools.json). "
        "Rebuild with `python3 scripts/build-tools-catalog.py`."
    )
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(summary_tables(tools))
    out.append("")
    out.append(
        "> `last_activity` and `stars_approx` are point-in-time snapshots from the curation pass "
        "(see [`README.md`](README.md) for caveats). Status: 🟢 active ≈ commit within ~6 months · "
        "🟡 maintained ≈ within ~2 years · 🔴 dormant ≈ older."
    )
    out.append("")

    by_cat: dict[str, list[dict]] = defaultdict(list)
    for t in tools:
        by_cat[t["category"]].append(t)

    for cat in CATEGORY_ORDER:
        rows = sorted(by_cat.get(cat, []), key=lambda x: x["name"].lower())
        if not rows:
            continue
        out.append(f"## {CATEGORIES[cat]} ({len(rows)})")
        out.append("")
        if cat == "mcp-server":
            out.append("| Tool | Lang | License | Status | Data source / what it serves |")
            out.append("|---|---|---|---|---|")
            for t in rows:
                desc = (t.get("data_source") or t["description"]).replace("|", "\\|")
                out.append(
                    f"| {tool_link(t)} | {lang_str(t['languages'])} | {t['license']} "
                    f"| {status_str(t)} | {desc} |"
                )
        else:
            out.append("| Tool | Lang | License | Status | What it does |")
            out.append("|---|---|---|---|---|")
            for t in rows:
                desc = t["description"].replace("|", "\\|")
                out.append(
                    f"| {tool_link(t)} | {lang_str(t['languages'])} | {t['license']} "
                    f"| {status_str(t)} | {desc} |"
                )
        out.append("")

    out.append("---")
    out.append("")
    out.append(
        "*Inclusion ≠ endorsement. Licenses/activity were verified during curation but change over "
        "time; confirm upstream before relying on a tool in a high-trust context. To propose a tool, "
        "see [`README.md`](README.md#contributing).*")
    out.append("")
    return "\n".join(out)


def fill_summary_block(readme_text: str, tools: list[dict]) -> str:
    block = f"{SUMMARY_BEGIN}\n\n{summary_tables(tools)}\n\n{SUMMARY_END}"
    start = readme_text.find(SUMMARY_BEGIN)
    end = readme_text.find(SUMMARY_END)
    if start == -1 or end == -1:
        raise SystemExit(
            "error: tools/README.md is missing the generated summary markers "
            f"({SUMMARY_BEGIN} … {SUMMARY_END})"
        )
    return readme_text[:start] + block + readme_text[end + len(SUMMARY_END):]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on schema error or stale generated output")
    args = parser.parse_args()

    if not TOOLS_JSON.exists():
        print(f"error: {TOOLS_JSON} not found", file=sys.stderr)
        return 1

    tools = load_tools()
    errors = validate(tools)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    catalog = render_catalog(tools)
    readme_exists = README_MD.exists()
    new_readme = fill_summary_block(README_MD.read_text(encoding="utf-8"), tools) if readme_exists else None

    if args.check:
        stale: list[str] = []
        if not CATALOG_MD.exists() or CATALOG_MD.read_text(encoding="utf-8") != catalog:
            stale.append("tools/CATALOG.md")
        if readme_exists and README_MD.read_text(encoding="utf-8") != new_readme:
            stale.append("tools/README.md (summary block)")
        if stale:
            print(
                "error: stale generated tools files: "
                + ", ".join(stale)
                + " — run `python3 scripts/build-tools-catalog.py`",
                file=sys.stderr,
            )
            return 1
        print(f"tools catalog OK: {len(tools)} tools, generated views fresh.", file=sys.stderr)
        return 0

    CATALOG_MD.write_text(catalog, encoding="utf-8")
    if readme_exists:
        README_MD.write_text(new_readme, encoding="utf-8")
    print(f"Wrote {CATALOG_MD.relative_to(ROOT)} ({len(tools)} tools).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
