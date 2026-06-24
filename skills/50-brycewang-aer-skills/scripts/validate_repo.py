#!/usr/bin/env python3
"""Repository checks for the AER-skills bundle.

The checks intentionally avoid third-party Python packages so they can run in
fresh CI environments and on a local machine before copying skills into an
agent profile.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_REPOSITORY_URL = "https://github.com/brycewang-stanford/AER-Skills"
LEGACY_REPOSITORY_URL = "https://github.com/brycewang-stanford/" + "AER-skills"
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]{1,63}$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HTML_LOCAL_ATTR_RE = re.compile(r"""\b(?:href|src)=["']([^"']+)["']""")
BACKTICK_RE = re.compile(r"`([^`]+)`")
BIB_ENTRY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
BIB_KEY_CANDIDATE_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*_(?:19|20)\d{2}$")
MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
MD_LINK_TEXT_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
HTML_ANCHOR_RE = re.compile(r"""<[^>]+\s(?:id|name)=["']([^"']+)["']""", re.IGNORECASE)
REQUIRED_AGENT_FIELDS = ("display_name", "short_description", "default_prompt")
AGENT_FIELD_LIMITS = {
    "display_name": (4, 64),
    "short_description": (25, 64),
    "default_prompt": (20, 180),
}
ALLOWED_SKILL_TOP_LEVEL = {"SKILL.md", "agents", "scripts", "references", "assets"}
BANNED_SKILL_FILENAMES = {
    "README.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
    "CHANGELOG.md",
}
MAX_SKILL_MD_LINES = 500
REQUIRED_CLI_SCRIPTS = (
    ROOT / "scripts" / "install_skills.py",
    ROOT / "scripts" / "scaffold_project.py",
    ROOT / "scripts" / "validate_repo.py",
    ROOT / "scripts" / "skill_audit.py",
    ROOT / "scripts" / "run_skillopt_gate.py",
)
PYTHON_IMPORT_PACKAGE_MAP = {
    "dateutil": "python-dateutil",
    "differences": "differences",
    "econtools": "econtools",
    "joblib": "joblib",
    "linearmodels": "linearmodels",
    "matplotlib": "matplotlib",
    "numpy": "numpy",
    "pandas": "pandas",
    "polars": "polars",
    "pyarrow": "pyarrow",
    "pyfixest": "pyfixest",
    "rddensity": "rddensity",
    "rdrobust": "rdrobust",
    "scipy": "scipy",
    "seaborn": "seaborn",
    "statsmodels": "statsmodels",
    "tqdm": "tqdm",
}
PYTHON_STDLIB_FALLBACK = {
    "__future__",
    "argparse",
    "ast",
    "csv",
    "dataclasses",
    "json",
    "logging",
    "math",
    "os",
    "pathlib",
    "random",
    "re",
    "shutil",
    "subprocess",
    "sys",
    "tempfile",
    "time",
    "typing",
    "urllib",
}
EXPECTED_TEMPLATE_FILES = {
    "stata": {
        "00_globals.do",
        "00_install_packages.do",
        "01_clean.do",
        "02_descriptives.do",
        "03_main_did.do",
        "04_robustness.do",
        "05_heterogeneity.do",
        "06_tables.do",
        "07_figures.do",
        "README.md",
        "run_all.do",
    },
    "r": {
        "00_setup.R",
        "01_clean.R",
        "02_descriptives.R",
        "03_main_did.R",
        "04_robustness.R",
        "05_heterogeneity.R",
        "06_tables.R",
        "07_figures.R",
        "README.md",
        "run_all.R",
    },
    "python": {
        "clean.py",
        "descriptives.py",
        "figures.py",
        "heterogeneity.py",
        "main_did.py",
        "README.md",
        "requirements.txt",
        "robustness.py",
        "run_all.py",
        "setup.py",
        "tables.py",
    },
}
REQUIRED_TEMPLATE_README_TEXT = {
    "stata": (
        "python3 scripts/scaffold_project.py stata",
        "do run_all.do",
        "00_install_packages.do",
        "set seed 20260101",
    ),
    "r": (
        "python3 scripts/scaffold_project.py r",
        'source("run_all.R")',
        "00_setup.R",
        "set.seed(20260101)",
    ),
    "python": (
        "scaffold_project.py python",
        "pip install -r requirements.txt",
        "python3 run_all.py",
        "requirements.txt",
        "default_rng(seed=20260101)",
    ),
}
EXPECTED_SKELETON_CODE_FILES = {
    "00_globals.do",
    "00_install_packages.do",
    "01_clean.do",
    "02_descriptives.do",
    "03_main_did.do",
    "04_robustness.do",
    "05_heterogeneity.do",
    "06_tables.do",
    "07_figures.do",
}
REQUIRED_SKELETON_README_TEXT = (
    "Data Availability and Provenance Statement",
    "Package Layout",
    "code/00_install_packages.do",
    "data/raw/",
    "data/intermediate/",
    "data/codebook/",
    "data/codebook/source-register.md",
    "docs/",
    "docs/exhibit-register.md",
    "exact sample size",
    "do run_all.do",
    "output/tables/*.tex",
    "output/tables/",
    "output/figures/*.pdf",
    "output/figures/",
    "logs/run_all.log",
    "logs/",
    "[BRACKETED]",
)
EXPECTED_EXAMPLE_DEMOS = {
    "iv-weak-instrument-demo": {
        "README.md",
        "iv_weak_instrument_demo.py",
    },
    "rdd-polynomial-demo": {
        "README.md",
        "rdd_polynomial_demo.py",
    },
    "staggered-did-demo": {
        "README.md",
        "staggered_did_demo.R",
        "staggered_did_demo.py",
    },
}
TEXT_SUFFIXES = {
    "",
    ".bib",
    ".do",
    ".json",
    ".md",
    ".py",
    ".r",
    ".sh",
    ".txt",
    ".yaml",
    ".yml",
}
GENERATED_OR_CACHE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "logs",
    "node_modules",
    "output",
    "venv",
}
LOCAL_PATH_MARKERS = (
    "/" + "Users" + "/",
    "/" + "home" + "/",
    "C:" + "\\" + "Users" + "\\",
    "/" + "var" + "/" + "folders" + "/",
)
UNFINISHED_MARKERS = (
    "T" + "ODO",
    "FIX" + "ME",
    "T" + "BD",
    "X" + "XX",
    "not " + "implemented",
    "coming " + "soon",
)
ALLOWED_UNFINISHED_MARKER_DIRS = (
    ROOT / "templates",
    ROOT / "examples" / "replication-package-skeleton",
)
ALLOWED_UNFINISHED_MARKER_FILES = {
    ROOT / "examples" / "rebuttal-example.md",
    ROOT / "skills" / "aer-rebuttal" / "SKILL.md",
}
REQUIRED_POLICY_PHRASES = {
    ROOT / "README.md": (
        "7,000",
        "6,000",
        "Disclosure statements",
    ),
    ROOT / "README.en.md": (
        "100 words",
        "7,000 words minus 200 per exhibit",
        "AEA Data and Code Availability Policy",
    ),
    ROOT / "skills" / "aer-submission" / "SKILL.md": (
        "100 words",
        "7,000 words minus 200 per exhibit",
        "Disclosure Statement PDFs",
        "AI usage disclosure",
    ),
    ROOT / "skills" / "aer-replication" / "SKILL.md": (
        "February 2026",
        "Data and Code Availability Statement",
        "README.pdf",
        "openICPSR",
    ),
    ROOT / "docs" / "desk-rejection-audit.md": (
        "100 words",
        "7,000 words",
        "openICPSR-ready",
    ),
    ROOT / "docs" / "pnas-nexus-publication-plan.md": (
        "250 words",
        "50-120 word",
        "public repository",
        "dataset citations",
        "exact sample sizes",
        "software versions",
        "alt text",
        "maximum 12 pages",
    ),
    ROOT / "docs" / "pnas-nexus-submission-checklist.md": (
        "Evidence to record",
        "250 words",
        "50-120 words",
        "public repository",
        "DOI",
        "exact sample size",
        "software source and version",
        "alt text",
        "ORCID",
        "commit hash",
    ),
}
INSTALL_DOC_GUARDRAIL_PHRASES = {
    ROOT / "docs" / "installation-codex.md": (
        "Do not pass a repository source directory",
        "the installer refuses those destinations",
    ),
    ROOT / "docs" / "installation-claude.md": (
        "Do not pass a repository source directory",
        "Project-scoped installs",
        "should use `.claude/skills`",
    ),
}
REQUIRED_REPOSITORY_URL_SURFACES = (
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "docs" / "installation-claude.md",
    ROOT / "docs" / "installation-codex.md",
)
REQUIRED_RESOURCE_LINKS = {
    ROOT / "skills" / "aer-workflow" / "SKILL.md": (
        "docs/workflow-map.md",
        "docs/desk-rejection-audit.md",
        "docs/methods-reference.md",
        "docs/style-guide.md",
        "docs/referee-report-rubric.md",
        "docs/source-register.md",
    ),
    ROOT / "skills" / "aer-literature" / "SKILL.md": (
        "docs/methods-reference.md",
        "examples/modern-aer-exemplars.md",
        "examples/aer-exemplars.md",
        "skills/aer-topic-selection/SKILL.md",
    ),
    ROOT / "skills" / "aer-paper-body" / "SKILL.md": (
        "examples/results-section-example.md",
        "docs/style-guide.md",
        "docs/methods-reference.md",
        "examples/intro-example.md",
    ),
    ROOT / "skills" / "aer-consistency" / "SKILL.md": (
        "examples/replication-package-skeleton/docs/exhibit-register.md",
        "skills/aer-paper-body/SKILL.md",
        "skills/aer-literature/SKILL.md",
        "docs/style-guide.md",
    ),
    ROOT / "skills" / "aer-referee-sim" / "SKILL.md": (
        "docs/referee-report-rubric.md",
        "examples/referee-report-example.md",
        "docs/desk-rejection-audit.md",
        "skills/aer-identification/SKILL.md",
        "skills/aer-robustness/SKILL.md",
        "docs/style-guide.md",
        "skills/aer-rebuttal/SKILL.md",
    ),
    ROOT / "skills" / "aer-topic-selection" / "SKILL.md": (
        "examples/modern-aer-exemplars.md",
        "examples/aer-exemplars.md",
        "docs/desk-rejection-audit.md",
        "docs/workflow-map.md",
    ),
    ROOT / "skills" / "aer-identification" / "SKILL.md": (
        "docs/methods-reference.md",
        "templates/stata/03_main_did.do",
        "templates/r/03_main_did.R",
        "templates/python/main_did.py",
        "examples/aer-exemplars.md",
        "examples/modern-aer-exemplars.md",
    ),
    ROOT / "skills" / "aer-introduction" / "SKILL.md": (
        "examples/intro-example.md",
    ),
    ROOT / "skills" / "aer-rebuttal" / "SKILL.md": (
        "examples/rebuttal-example.md",
    ),
    ROOT / "skills" / "aer-replication" / "SKILL.md": (
        "examples/replication-package-skeleton/",
        "examples/replication-package-skeleton/data/codebook/source-register.md",
        "examples/replication-package-skeleton/docs/exhibit-register.md",
        "templates/stata/",
        "templates/r/",
        "templates/python/",
        "examples/aer-exemplars.md",
    ),
    ROOT / "skills" / "aer-robustness" / "SKILL.md": (
        "docs/methods-reference.md",
        "templates/stata/04_robustness.do",
        "templates/r/04_robustness.R",
        "templates/python/robustness.py",
        "templates/stata/05_heterogeneity.do",
        "templates/r/05_heterogeneity.R",
        "templates/python/heterogeneity.py",
    ),
    ROOT / "skills" / "aer-tables-figures" / "SKILL.md": (
        "templates/stata/06_tables.do",
        "templates/r/06_tables.R",
        "templates/python/tables.py",
    ),
    ROOT / "skills" / "aer-submission" / "SKILL.md": (
        "docs/desk-rejection-audit.md",
        "docs/source-register.md",
        "skills/aer-replication/SKILL.md",
        "examples/replication-package-skeleton/",
    ),
}


class ValidationError(Exception):
    """Raised when one or more repository checks fail."""


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(errors, f"{rel(path)}: missing YAML frontmatter")
        return {}

    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            fail(errors, f"{rel(path)}: invalid frontmatter line: {line!r}")
            continue
        fields[key.strip()] = value.strip().strip('"')
    return fields


def parse_agent_yaml(path: Path, errors: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    in_interface = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line == "interface:":
            in_interface = True
            continue
        if in_interface and raw_line.startswith("  "):
            key, sep, value = raw_line.strip().partition(":")
            if sep:
                fields[key] = value.strip().strip('"')
            continue
        fail(errors, f"{rel(path)}: unsupported YAML shape near {raw_line!r}")

    if not in_interface:
        fail(errors, f"{rel(path)}: missing top-level interface block")
    return fields


def check_skills(errors: list[str]) -> list[str]:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        fail(errors, "skills/: directory missing")
        return []

    skill_names: list[str] = []
    display_names: dict[str, str] = {}
    short_descriptions: dict[str, str] = {}
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        name = skill_dir.name
        skill_names.append(name)
        if not SKILL_NAME_RE.fullmatch(name):
            fail(errors, f"{rel(skill_dir)}: invalid skill directory name")

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            fail(errors, f"{rel(skill_dir)}: missing SKILL.md")
            continue

        for child in sorted(skill_dir.iterdir()):
            if child.name not in ALLOWED_SKILL_TOP_LEVEL:
                fail(errors, f"{rel(child)}: unexpected top-level skill file or directory")
        for banned_file in sorted(
            path for path in skill_dir.rglob("*") if path.name in BANNED_SKILL_FILENAMES
        ):
            fail(errors, f"{rel(banned_file)}: auxiliary docs should not live inside skills/")
        line_count = len(skill_md.read_text(encoding="utf-8").splitlines())
        if line_count > MAX_SKILL_MD_LINES:
            fail(
                errors,
                f"{rel(skill_md)}: {line_count} lines exceeds {MAX_SKILL_MD_LINES}-line limit",
            )

        frontmatter = parse_frontmatter(skill_md, errors)
        if set(frontmatter) != {"name", "description"}:
            fail(
                errors,
                f"{rel(skill_md)}: frontmatter must contain only name and description",
            )
        if frontmatter.get("name") != name:
            fail(errors, f"{rel(skill_md)}: name does not match directory")
        description = frontmatter.get("description", "")
        if "Use when" not in description:
            fail(errors, f"{rel(skill_md)}: description should include trigger context")

        agent_yaml = skill_dir / "agents" / "openai.yaml"
        if not agent_yaml.is_file():
            fail(errors, f"{rel(skill_dir)}: missing agents/openai.yaml")
            continue
        agent_fields = parse_agent_yaml(agent_yaml, errors)
        for field in REQUIRED_AGENT_FIELDS:
            if not agent_fields.get(field):
                fail(errors, f"{rel(agent_yaml)}: missing interface.{field}")
                continue
            value = agent_fields[field]
            minimum, maximum = AGENT_FIELD_LIMITS[field]
            if not minimum <= len(value) <= maximum:
                fail(
                    errors,
                    f"{rel(agent_yaml)}: interface.{field} should be {minimum}-{maximum} characters",
                )
            if "\n" in value or "\r" in value:
                fail(errors, f"{rel(agent_yaml)}: interface.{field} should be one line")
            if "[" in value or "](" in value:
                fail(errors, f"{rel(agent_yaml)}: interface.{field} should be plain text")
        default_prompt = agent_fields.get("default_prompt", "")
        if f"${name}" not in default_prompt:
            fail(errors, f"{rel(agent_yaml)}: default_prompt should invoke ${name}")
        if default_prompt and not default_prompt.startswith(f"Use ${name} "):
            fail(errors, f"{rel(agent_yaml)}: default_prompt should start with Use ${name}")

        display_name = agent_fields.get("display_name", "")
        if display_name:
            if display_name in display_names:
                fail(
                    errors,
                    f"{rel(agent_yaml)}: duplicate display_name also used by {display_names[display_name]}",
                )
            display_names[display_name] = rel(agent_yaml)
        short_description = agent_fields.get("short_description", "")
        if short_description:
            if short_description in short_descriptions:
                fail(
                    errors,
                    f"{rel(agent_yaml)}: duplicate short_description also used by "
                    f"{short_descriptions[short_description]}",
                )
            short_descriptions[short_description] = rel(agent_yaml)

    return skill_names


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{rel(path)}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        fail(errors, f"{rel(path)}: expected top-level JSON object")
        return {}
    return data


def require_json_string(document: dict, path: Path, key: str, errors: list[str]) -> str:
    value = document.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(errors, f"{rel(path)}: missing {key}")
        return ""
    return value


def require_json_object(document: dict, path: Path, key: str, errors: list[str]) -> dict:
    value = document.get(key)
    if not isinstance(value, dict):
        fail(errors, f"{rel(path)}: missing {key} object")
        return {}
    return value


def check_plugin_manifest(skill_names: list[str], errors: list[str]) -> None:
    plugin_json = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_json = ROOT / ".claude-plugin" / "marketplace.json"
    for path in (plugin_json, marketplace_json):
        if not path.is_file():
            fail(errors, f"{rel(path)}: missing")

    plugin = load_json(plugin_json, errors) if plugin_json.is_file() else {}
    marketplace = load_json(marketplace_json, errors) if marketplace_json.is_file() else {}

    expected_paths = [f"skills/{name}" for name in skill_names]
    for key in ("name", "description", "version", "license", "homepage", "repository"):
        require_json_string(plugin, plugin_json, key, errors)
    for key in ("homepage", "repository"):
        if plugin.get(key) != CANONICAL_REPOSITORY_URL:
            fail(errors, f"{rel(plugin_json)}: {key} should be {CANONICAL_REPOSITORY_URL}")
    author = require_json_object(plugin, plugin_json, "author", errors)
    for key in ("name", "email"):
        value = author.get(key)
        if not isinstance(value, str) or not value.strip():
            fail(errors, f"{rel(plugin_json)}: missing author.{key}")

    for key in ("name", "version", "description"):
        require_json_string(marketplace, marketplace_json, key, errors)
    owner = require_json_object(marketplace, marketplace_json, "owner", errors)
    if owner != author:
        fail(errors, f"{rel(marketplace_json)}: owner does not match plugin.json author")

    metadata = marketplace.get("metadata")
    if not isinstance(metadata, dict):
        fail(errors, f"{rel(marketplace_json)}: missing metadata object")
    elif metadata.get("pluginRoot") != "./":
        fail(errors, f"{rel(marketplace_json)}: metadata.pluginRoot should be ./")

    for key in ("name", "version"):
        if plugin.get(key) != marketplace.get(key):
            fail(errors, f"{rel(marketplace_json)}: {key} does not match plugin.json")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail(errors, f"{rel(marketplace_json)}: expected exactly one plugin entry")
        return

    entry = plugins[0]
    if not isinstance(entry, dict):
        fail(errors, f"{rel(marketplace_json)}: plugin entry should be an object")
        return

    for key in ("name", "version", "license", "homepage", "repository"):
        if entry.get(key) != plugin.get(key):
            fail(errors, f"{rel(marketplace_json)}: plugin entry {key} does not match plugin.json")
    for key in ("homepage", "repository"):
        if entry.get(key) != CANONICAL_REPOSITORY_URL:
            fail(errors, f"{rel(marketplace_json)}: plugin entry {key} should be {CANONICAL_REPOSITORY_URL}")
    if entry.get("author") != author:
        fail(errors, f"{rel(marketplace_json)}: plugin entry author does not match plugin.json")
    if entry.get("source") != "./":
        fail(errors, f"{rel(marketplace_json)}: plugin entry source should be ./")

    listed = entry.get("skills")
    if not isinstance(listed, list):
        fail(errors, f"{rel(marketplace_json)}: plugin entry skills should be a list")
        return
    string_paths = [skill_path for skill_path in listed if isinstance(skill_path, str)]
    duplicate_paths = sorted(path for path in set(string_paths) if string_paths.count(path) > 1)
    if duplicate_paths:
        fail(errors, f"{rel(marketplace_json)}: duplicate skill paths: {', '.join(duplicate_paths)}")
    if sorted(string_paths) != sorted(expected_paths) or len(string_paths) != len(listed):
        fail(
            errors,
            f"{rel(marketplace_json)}: skills list does not match skills/ directories",
        )
    for skill_path in listed:
        if not isinstance(skill_path, str):
            fail(errors, f"{rel(marketplace_json)}: skill path should be a string")
            continue
        if not (ROOT / skill_path / "SKILL.md").is_file():
            fail(errors, f"{rel(marketplace_json)}: missing listed skill {skill_path}/SKILL.md")


def check_skill_reference_docs(skill_names: list[str], errors: list[str]) -> None:
    readme_paths = (ROOT / "README.md", ROOT / "README.en.md")
    for path in readme_paths:
        text = path.read_text(encoding="utf-8")
        for name in skill_names:
            link = f"skills/{name}/SKILL.md"
            if link not in text:
                fail(errors, f"{rel(path)}: missing link to {link}")

    workflow_map = ROOT / "docs" / "workflow-map.md"
    text = workflow_map.read_text(encoding="utf-8")
    for name in skill_names:
        if name not in text:
            fail(errors, f"{rel(workflow_map)}: missing {name}")

    primary_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    english_readme = (ROOT / "README.en.md").read_text(encoding="utf-8")
    if "examples/README.md" not in primary_readme:
        fail(errors, "README.md: missing link to examples/README.md")
    if "examples/README.md" not in english_readme:
        fail(errors, "README.en.md: missing link to examples/README.md")

    docs = sorted(path.name for path in (ROOT / "docs").glob("*.md"))
    for doc in docs:
        readme_link = f"docs/{doc}"
        if readme_link not in primary_readme:
            fail(errors, f"README.md: missing link to {readme_link}")
        if readme_link not in english_readme:
            fail(errors, f"README.en.md: missing link to {readme_link}")

    workflow_docs = (
        "desk-rejection-audit.md",
        "methods-reference.md",
        "source-register.md",
    )
    for doc in workflow_docs:
        workflow_link = f"./{doc}"
        if workflow_link not in text:
            fail(errors, f"{rel(workflow_map)}: missing link to {workflow_link}")

    examples_readme = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    for doc in ("../docs/methods-reference.md", "../docs/desk-rejection-audit.md"):
        if doc not in examples_readme:
            fail(errors, f"examples/README.md: missing link to {doc}")


def check_source_register(errors: list[str]) -> None:
    source_register = ROOT / "docs" / "source-register.md"
    if not source_register.is_file():
        fail(errors, f"{rel(source_register)}: missing")
        return

    text = source_register.read_text(encoding="utf-8")
    required_sources = (
        "https://www.aeaweb.org/journals/aer/submissions",
        "https://www.aeaweb.org/journals/aer/accepted-article-guidelines",
        "https://www.aeaweb.org/journals/aeri/submissions",
        "https://www.aeaweb.org/journals/aeri/accepted-article-guidelines",
        "https://www.aeaweb.org/journals/data/data-code-policy",
        "https://www.aeaweb.org/journals/forms/data-code-availability",
        "https://www.icpsr.umich.edu/sites/aea/home",
        "https://academic.oup.com/pnasnexus/pages/general-instructions",
    )
    for source in required_sources:
        if source not in text:
            fail(errors, f"{rel(source_register)}: missing official source {source}")

    for phrase in ("Last reviewed:", "Repo surfaces", "Review trigger"):
        if phrase not in text:
            fail(errors, f"{rel(source_register)}: missing {phrase!r}")

    for path in REQUIRED_POLICY_PHRASES:
        surface = rel(path)
        if f"`{surface}`" not in text:
            fail(errors, f"{rel(source_register)}: missing policy guardrail surface {surface}")

    for match in BACKTICK_RE.finditer(text):
        candidate = match.group(1)
        if " " in candidate or candidate.startswith(("http://", "https://")):
            continue
        if candidate.endswith((".md", ".py", ".bib", "/")):
            resolved = ROOT / candidate.rstrip("/")
            if not resolved.exists():
                fail(errors, f"{rel(source_register)}: listed surface does not exist: {candidate}")


def check_policy_guardrails(errors: list[str]) -> None:
    """Catch accidental deletion of high-risk journal-policy constraints."""

    for path, phrases in REQUIRED_POLICY_PHRASES.items():
        if not path.is_file():
            fail(errors, f"{rel(path)}: missing policy-bearing file")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(errors, f"{rel(path)}: missing policy guardrail phrase {phrase!r}")


def check_installation_guardrails(errors: list[str]) -> None:
    """Keep installer safety behavior documented for manual users."""

    for path, phrases in INSTALL_DOC_GUARDRAIL_PHRASES.items():
        if not path.is_file():
            fail(errors, f"{rel(path)}: missing installation guide")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                fail(errors, f"{rel(path)}: missing installer guardrail phrase {phrase!r}")


def repository_resources_from_skill(text: str) -> list[str]:
    if "## Repository Resources" not in text:
        return []
    resources_section = text.split("## Repository Resources", 1)[1].split("\n## ", 1)[0]
    resources = []
    for match in BACKTICK_RE.finditer(resources_section):
        resource = match.group(1)
        if resource.startswith(("docs/", "examples/", "skills/", "templates/")):
            resources.append(resource)
    return resources


def check_skill_resource_links(errors: list[str]) -> None:
    """Keep core skills tied to runnable templates and citation-backed docs."""

    for skill_path in sorted((ROOT / "skills").glob("aer-*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        if "## Repository Resources" not in text:
            fail(errors, f"{rel(skill_path)}: missing Repository Resources section")
            continue
        section_resources = repository_resources_from_skill(text)
        for resource in section_resources:
            if not (ROOT / resource.rstrip("/")).exists():
                fail(errors, f"{rel(skill_path)}: listed repository resource missing: {resource}")
        if not section_resources:
            fail(errors, f"{rel(skill_path)}: Repository Resources section lists no repo paths")

    for path, resources in REQUIRED_RESOURCE_LINKS.items():
        if not path.is_file():
            fail(errors, f"{rel(path)}: missing skill file")
            continue
        text = path.read_text(encoding="utf-8")
        if "## Repository Resources" not in text:
            fail(errors, f"{rel(path)}: missing Repository Resources section")
        for resource in resources:
            if resource not in text:
                fail(errors, f"{rel(path)}: missing repository resource {resource}")
            if not (ROOT / resource).exists():
                fail(errors, f"{rel(path)}: listed repository resource missing: {resource}")


def check_bibliography_integrity(errors: list[str]) -> None:
    references = ROOT / "references.bib"
    methods_reference = ROOT / "docs" / "methods-reference.md"
    if not references.is_file():
        fail(errors, f"{rel(references)}: missing")
        return
    if not methods_reference.is_file():
        fail(errors, f"{rel(methods_reference)}: missing")
        return

    bib_text = references.read_text(encoding="utf-8")
    keys = BIB_ENTRY_RE.findall(bib_text)
    if not keys:
        fail(errors, f"{rel(references)}: no BibTeX entries found")
        return

    seen: dict[str, int] = {}
    for key in keys:
        if key in seen:
            fail(errors, f"{rel(references)}: duplicate BibTeX key {key!r}")
        seen[key] = seen.get(key, 0) + 1

    for entry in re.split(r"\n(?=@\w+\s*\{)", bib_text):
        match = BIB_ENTRY_RE.search(entry)
        if not match:
            continue
        key = match.group(1)
        if "doi" not in entry.lower() and "No Crossref DOI" not in entry:
            fail(errors, f"{rel(references)}: {key} missing DOI or explicit no-DOI note")

    method_text = methods_reference.read_text(encoding="utf-8")
    bib_keys = set(keys)
    for match in BACKTICK_RE.finditer(method_text):
        candidate = match.group(1)
        if BIB_KEY_CANDIDATE_RE.fullmatch(candidate) and candidate not in bib_keys:
            fail(
                errors,
                f"{rel(methods_reference)}: citation key {candidate!r} missing from references.bib",
            )


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in GENERATED_OR_CACHE_DIRS for part in path.parts)
    )


def text_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(part in GENERATED_OR_CACHE_DIRS for part in path.parts)
        and path.suffix.lower() in TEXT_SUFFIXES
    )


def check_repository_urls(errors: list[str]) -> None:
    for path in text_files():
        text = path.read_text(encoding="utf-8")
        if LEGACY_REPOSITORY_URL in text:
            fail(errors, f"{rel(path)}: replace legacy repository URL with {CANONICAL_REPOSITORY_URL}")

    for path in REQUIRED_REPOSITORY_URL_SURFACES:
        if not path.is_file():
            fail(errors, f"{rel(path)}: missing repository URL surface")
            continue
        if CANONICAL_REPOSITORY_URL not in path.read_text(encoding="utf-8"):
            fail(errors, f"{rel(path)}: missing canonical repository URL")


def normalize_markdown_target(target: str) -> str:
    target = target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith(("./", "../")):
        target = target.split()[0]
    return unquote(target)


def github_heading_slug(heading: str) -> str:
    heading = re.sub(r"`([^`]*)`", r"\1", heading.strip())
    heading = MD_LINK_TEXT_RE.sub(r"\1", heading)
    heading = HTML_TAG_RE.sub("", heading)
    heading = re.sub(r"\s+#*$", "", heading).lower()
    cleaned = "".join(
        character
        for character in heading
        if character.isalnum() or character.isspace() or character in "-_"
    )
    return re.sub(r"\s", "-", cleaned.strip())


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    text = path.read_text(encoding="utf-8")
    for match in HTML_ANCHOR_RE.finditer(text):
        anchors.add(unquote(match.group(1)).strip().lower())

    for line in text.splitlines():
        match = MD_HEADING_RE.match(line)
        if not match:
            continue
        base = github_heading_slug(match.group(2))
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def check_validator_self_tests(errors: list[str]) -> None:
    slug_cases = {
        "1. Difference-in-differences (staggered adoption)": (
            "1-difference-in-differences-staggered-adoption"
        ),
        "3. Shift-share / Bartik": "3-shift-share--bartik",
        "AER: Insights `word-count` PDF": "aer-insights-word-count-pdf",
        "[methods reference](./methods-reference.md)": "methods-reference",
    }
    for heading, expected in slug_cases.items():
        actual = github_heading_slug(heading)
        if actual != expected:
            fail(
                errors,
                f"validator: heading slug for {heading!r} was {actual!r}, expected {expected!r}",
            )

    resource_fixture = "\n".join(
        [
            "# Skill",
            "",
            "## Repository Resources",
            "",
            "- Docs: `docs/methods-reference.md`",
            "- Demo: `examples/rdd-polynomial-demo/`",
            "- Template: `templates/python/`",
            "- Skill: `skills/aer-identification/SKILL.md`",
            "- Non-resource token: `aer-identification`",
            "",
            "## Handoff",
            "",
        ]
    )
    actual_resources = repository_resources_from_skill(resource_fixture)
    expected_resources = [
        "docs/methods-reference.md",
        "examples/rdd-polynomial-demo/",
        "templates/python/",
        "skills/aer-identification/SKILL.md",
    ]
    if actual_resources != expected_resources:
        fail(
            errors,
            "validator: repository resource self-test returned "
            f"{actual_resources!r}, expected {expected_resources!r}",
        )

    unfinished_cases = {
        "finish this " + "T" + "ODO" + " before release": "T" + "ODO",
        "this method is fully documented": None,
        "prefixT" + "ODOsuffix should not match": None,
    }
    for text, expected in unfinished_cases.items():
        actual = unfinished_marker_in_text(text)
        if actual != expected:
            fail(
                errors,
                f"validator: unfinished marker self-test returned {actual!r}, "
                f"expected {expected!r}",
            )

    with tempfile.TemporaryDirectory() as tempdir:
        executable_fixture = Path(tempdir) / "entrypoint.py"
        executable_fixture.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        executable_fixture.chmod(0o644)
        if has_executable_bit(executable_fixture):
            fail(errors, "validator: executable-bit self-test accepted mode 0644")
        executable_fixture.chmod(0o755)
        if not has_executable_bit(executable_fixture):
            fail(errors, "validator: executable-bit self-test rejected mode 0755")

    with tempfile.TemporaryDirectory() as tempdir:
        fixture = Path(tempdir) / "anchors.md"
        fixture.write_text(
            "\n".join(
                [
                    "# Methods Reference",
                    "## Methods Reference",
                    "<a id=\"custom-anchor\"></a>",
                    "<span name=\"legacy-anchor\"></span>",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        actual_anchors = markdown_anchors(fixture)
        expected_anchors = {
            "methods-reference",
            "methods-reference-1",
            "custom-anchor",
            "legacy-anchor",
        }
        missing = sorted(expected_anchors - actual_anchors)
        if missing:
            fail(errors, f"validator: markdown anchor self-test missed {', '.join(missing)}")

    with tempfile.TemporaryDirectory() as tempdir:
        fixture_dir = Path(tempdir)
        python_fixture = fixture_dir / "deps_demo.py"
        python_fixture.write_text(
            "\n".join(
                [
                    '"""Demo.',
                    "Deps: numpy, pandas",
                    '"""',
                    "from __future__ import annotations",
                    "from pathlib import Path",
                    "import numpy as np",
                    "import pandas as pd",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        expected_python_deps = ["numpy", "pandas"]
        actual_python_deps = declared_deps(python_fixture)
        if actual_python_deps != expected_python_deps:
            fail(
                errors,
                "validator: Python Deps self-test returned "
                f"{actual_python_deps!r}, expected {expected_python_deps!r}",
            )
        actual_python_imports = third_party_python_import_packages(python_fixture)
        expected_python_imports = {"numpy", "pandas"}
        if actual_python_imports != expected_python_imports:
            fail(
                errors,
                "validator: Python import self-test returned "
                f"{sorted(actual_python_imports)!r}, expected {sorted(expected_python_imports)!r}",
            )

        r_fixture = fixture_dir / "deps_demo.R"
        r_fixture.write_text(
            "\n".join(
                [
                    "# Deps: fixest, did",
                    "suppressMessages({",
                    "  library(fixest)",
                    "  library(did)",
                    "})",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        expected_r_deps = ["fixest", "did"]
        actual_r_deps = declared_deps(r_fixture)
        if actual_r_deps != expected_r_deps:
            fail(
                errors,
                f"validator: R Deps self-test returned {actual_r_deps!r}, "
                f"expected {expected_r_deps!r}",
            )
        actual_r_libraries = r_library_packages(r_fixture)
        expected_r_libraries = {"fixest", "did"}
        if actual_r_libraries != expected_r_libraries:
            fail(
                errors,
                "validator: R library self-test returned "
                f"{sorted(actual_r_libraries)!r}, expected {sorted(expected_r_libraries)!r}",
            )


def check_markdown_links(errors: list[str]) -> None:
    anchor_cache: dict[Path, set[str]] = {}

    def check_local_target(path: Path, raw_target: str) -> None:
        raw_target = normalize_markdown_target(raw_target)
        if not raw_target or raw_target.startswith(("http://", "https://", "mailto:")):
            return

        local_target, _, anchor = raw_target.partition("#")
        if not local_target:
            resolved = path
        else:
            resolved = (path.parent / local_target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(errors, f"{rel(path)}: link escapes repository: {raw_target}")
            return
        if not resolved.exists():
            fail(errors, f"{rel(path)}: broken local link: {raw_target}")
            return
        if anchor and resolved.suffix.lower() == ".md":
            anchor_id = unquote(anchor).strip().lower()
            if resolved not in anchor_cache:
                anchor_cache[resolved] = markdown_anchors(resolved)
            if anchor_id not in anchor_cache[resolved]:
                fail(errors, f"{rel(path)}: broken markdown anchor: {raw_target}")

    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in MD_LINK_RE.finditer(text):
            check_local_target(path, match.group(1))
        for match in HTML_LOCAL_ATTR_RE.finditer(text):
            check_local_target(path, match.group(1))


def run_command(args: list[str], errors: list[str], label: str) -> None:
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        output = result.stdout.strip()
        fail(errors, f"{label} failed with exit {result.returncode}\n{output}")


def check_expected_file_set(path: Path, expected: set[str], errors: list[str]) -> None:
    if not path.is_dir():
        fail(errors, f"{rel(path)}: directory missing")
        return
    actual = {child.name for child in path.iterdir() if child.is_file()}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        fail(errors, f"{rel(path)}: missing expected files: {', '.join(missing)}")
    if extra:
        fail(errors, f"{rel(path)}: unexpected files: {', '.join(extra)}")


def check_template_layout(errors: list[str]) -> None:
    for template_name, expected in EXPECTED_TEMPLATE_FILES.items():
        check_expected_file_set(ROOT / "templates" / template_name, expected, errors)
        readme = ROOT / "templates" / template_name / "README.md"
        text = readme.read_text(encoding="utf-8")
        for required_text in REQUIRED_TEMPLATE_README_TEXT[template_name]:
            if required_text not in text:
                fail(errors, f"{rel(readme)}: missing {required_text!r}")

    stata_steps = sorted(
        name for name in EXPECTED_TEMPLATE_FILES["stata"] if name.endswith(".do")
    )
    r_steps = sorted(name for name in EXPECTED_TEMPLATE_FILES["r"] if name.endswith(".R"))
    python_modules = sorted(
        path.stem
        for path in (ROOT / "templates" / "python").glob("*.py")
        if path.name != "run_all.py"
    )

    stata_run_all = (ROOT / "templates" / "stata" / "run_all.do").read_text(
        encoding="utf-8"
    )
    for step in stata_steps:
        if step != "run_all.do" and f'"{step}"' not in stata_run_all:
            fail(errors, f"templates/stata/run_all.do: missing do step {step}")

    r_run_all = (ROOT / "templates" / "r" / "run_all.R").read_text(encoding="utf-8")
    for step in r_steps:
        if step != "run_all.R" and f'"{step}"' not in r_run_all:
            fail(errors, f"templates/r/run_all.R: missing source step {step}")

    python_run_all = (ROOT / "templates" / "python" / "run_all.py").read_text(
        encoding="utf-8"
    )
    for module in python_modules:
        if module not in {"setup"} and f"import {module}" not in python_run_all:
            fail(errors, f"templates/python/run_all.py: missing import {module}")

    skeleton = ROOT / "examples" / "replication-package-skeleton"
    check_expected_file_set(skeleton / "code", EXPECTED_SKELETON_CODE_FILES, errors)
    skeleton_source_register = skeleton / "data" / "codebook" / "source-register.md"
    if not skeleton_source_register.is_file():
        fail(errors, f"{rel(skeleton_source_register)}: missing")
    else:
        source_register_text = skeleton_source_register.read_text(encoding="utf-8")
        for phrase in (
            "Source Inventory",
            "Variable Crosswalk",
            "Derived Files",
            "License or access terms",
            "Date accessed",
            "Restrictions / DUA",
            "Unit of observation",
            "Audit Rules",
        ):
            if phrase not in source_register_text:
                fail(errors, f"{rel(skeleton_source_register)}: missing {phrase!r}")
    skeleton_exhibit_register = skeleton / "docs" / "exhibit-register.md"
    if not skeleton_exhibit_register.is_file():
        fail(errors, f"{rel(skeleton_exhibit_register)}: missing")
    else:
        exhibit_register_text = skeleton_exhibit_register.read_text(encoding="utf-8")
        for phrase in (
            "Claim supported",
            "Script and lines",
            "Input data",
            "Estimator or statistic",
            "Exact sample size",
            "Accessibility note",
            "alt text",
        ):
            if phrase not in exhibit_register_text:
                fail(errors, f"{rel(skeleton_exhibit_register)}: missing {phrase!r}")
    skeleton_top_level = {child.name for child in skeleton.iterdir() if child.is_file()}
    expected_top_level = {"LICENSE", "README.md", "run_all.do"}
    missing = sorted(expected_top_level - skeleton_top_level)
    if missing:
        fail(errors, f"{rel(skeleton)}: missing expected files: {', '.join(missing)}")
    skeleton_readme = (skeleton / "README.md").read_text(encoding="utf-8")
    for required_text in REQUIRED_SKELETON_README_TEXT:
        if required_text not in skeleton_readme:
            fail(errors, f"{rel(skeleton / 'README.md')}: missing {required_text!r}")

    skeleton_run_all = (skeleton / "run_all.do").read_text(encoding="utf-8")
    for step in sorted(EXPECTED_SKELETON_CODE_FILES):
        if f'"code/{step}"' not in skeleton_run_all:
            fail(errors, f"{rel(skeleton / 'run_all.do')}: missing do step code/{step}")


def python_requirement_names() -> set[str]:
    requirements = ROOT / "templates" / "python" / "requirements.txt"
    names: set[str] = set()
    for raw_line in requirements.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or "==" not in line:
            continue
        names.add(line.split("==", 1)[0].strip().lower())
    return names


def r_setup_package_names() -> set[str]:
    setup = ROOT / "templates" / "r" / "00_setup.R"
    text = setup.read_text(encoding="utf-8")
    match = re.search(r"required_pkgs\s*<-\s*c\((.*?)\)", text, re.DOTALL)
    if not match:
        return set()
    return {name.lower() for name in re.findall(r'"([^"]+)"', match.group(1))}


def declared_deps(script: Path) -> list[str]:
    for raw_line in script.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().lstrip("#").strip()
        if not line.startswith("Deps:"):
            continue
        deps_text = line.removeprefix("Deps:").split("(", 1)[0]
        return [dep.strip().lower() for dep in deps_text.split(",") if dep.strip()]
    return []


def check_example_demos(errors: list[str]) -> None:
    primary_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    english_readme = (ROOT / "README.en.md").read_text(encoding="utf-8")
    examples_readme = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    python_deps = python_requirement_names()
    r_deps = r_setup_package_names()
    tracked_examples = set(
        subprocess.run(
            ["git", "ls-files", "examples"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        ).stdout.splitlines()
    )
    for artifact in sorted((ROOT / "examples").iterdir()):
        if artifact.name == "README.md" or artifact.name.startswith("."):
            continue
        artifact_rel = rel(artifact)
        if artifact.is_file() and artifact_rel not in tracked_examples:
            continue
        if artifact.is_dir() and not any(
            tracked.startswith(f"{artifact_rel}/") for tracked in tracked_examples
        ):
            continue
        if artifact.is_file() and artifact.suffix != ".md":
            continue
        if artifact.is_dir() and not any(
            child.is_file() and not any(part in GENERATED_OR_CACHE_DIRS for part in child.parts)
            for child in artifact.rglob("*")
        ):
            continue
        if any(part in GENERATED_OR_CACHE_DIRS for part in artifact.parts):
            continue
        link_target = f"{artifact.name}/" if artifact.is_dir() else artifact.name
        if f"]({link_target})" not in examples_readme:
            fail(errors, f"examples/README.md: missing link to {link_target}")

    registered_demos = set(EXPECTED_EXAMPLE_DEMOS)
    for demo_dir in sorted(path for path in (ROOT / "examples").iterdir() if path.is_dir()):
        demo_rel = rel(demo_dir)
        tracked_children = [
            tracked for tracked in tracked_examples if tracked.startswith(f"{demo_rel}/")
        ]
        has_runnable_script = any(
            Path(tracked).suffix in {".py", ".R"} for tracked in tracked_children
        )
        if has_runnable_script and demo_dir.name not in registered_demos:
            fail(errors, f"{demo_rel}: runnable demo should be listed in EXPECTED_EXAMPLE_DEMOS")

    for demo_name, expected_files in EXPECTED_EXAMPLE_DEMOS.items():
        demo_dir = ROOT / "examples" / demo_name
        if not demo_dir.is_dir():
            fail(errors, f"{rel(demo_dir)}: demo directory missing")
            continue
        check_expected_file_set(demo_dir, expected_files, errors)
        if f"{demo_name}/" not in examples_readme:
            fail(errors, f"examples/README.md: missing link to {demo_name}/")
        root_demo_link = f"examples/{demo_name}/"
        if root_demo_link not in primary_readme:
            fail(errors, f"README.md: missing link to {root_demo_link}")
        if root_demo_link not in english_readme:
            fail(errors, f"README.en.md: missing link to {root_demo_link}")

        demo_readme = demo_dir / "README.md"
        if not demo_readme.is_file():
            continue
        demo_text = demo_readme.read_text(encoding="utf-8")
        for script_name in sorted(name for name in expected_files if name != "README.md"):
            if script_name not in demo_text:
                fail(errors, f"{rel(demo_readme)}: missing run/reference text for {script_name}")
        for required_text in (
            "output/",
            "../../docs/methods-reference.md",
            "../../skills/aer-identification/SKILL.md",
        ):
            if required_text not in demo_text:
                fail(errors, f"{rel(demo_readme)}: missing {required_text}")
        if any(name.endswith(".py") for name in expected_files):
            if "../../templates/python/requirements.txt" not in demo_text:
                fail(errors, f"{rel(demo_readme)}: missing Python requirements link")
        if any(name.endswith(".R") for name in expected_files):
            if "../../templates/r/00_setup.R" not in demo_text:
                fail(errors, f"{rel(demo_readme)}: missing R setup link")

        for script_name in sorted(name for name in expected_files if name.endswith(".py")):
            script_path = demo_dir / script_name
            declared = set(declared_deps(script_path))
            imported = third_party_python_import_packages(script_path)
            if not declared:
                fail(errors, f"{rel(script_path)}: missing Deps declaration")
            for dep in sorted(declared):
                if dep not in python_deps:
                    fail(
                        errors,
                        f"{rel(script_path)}: declared dependency {dep} is not pinned",
                    )
                if f"`{dep}`" not in demo_text:
                    fail(errors, f"{rel(demo_readme)}: missing dependency `{dep}`")
            for dep in sorted(imported - declared):
                fail(errors, f"{rel(script_path)}: imported dependency {dep} missing from Deps")
            for dep in sorted(declared - imported):
                fail(errors, f"{rel(script_path)}: declared dependency {dep} is not imported")

        for script_name in sorted(name for name in expected_files if name.endswith(".R")):
            script_path = demo_dir / script_name
            declared = set(declared_deps(script_path))
            imported = r_library_packages(script_path)
            if not declared:
                fail(errors, f"{rel(script_path)}: missing Deps declaration")
            for dep in sorted(declared):
                if dep not in r_deps:
                    fail(
                        errors,
                        f"{rel(script_path)}: declared dependency {dep} is not in R setup",
                    )
                if f"`{dep}`" not in demo_text:
                    fail(errors, f"{rel(demo_readme)}: missing dependency `{dep}`")
            for dep in sorted(imported - declared):
                fail(errors, f"{rel(script_path)}: imported dependency {dep} missing from Deps")
            for dep in sorted(declared - imported):
                fail(errors, f"{rel(script_path)}: declared dependency {dep} is not loaded")


def check_python_templates(errors: list[str]) -> None:
    py_files = sorted((ROOT / "templates" / "python").glob("*.py"))
    py_files.extend(sorted((ROOT / "scripts").glob("*.py")))
    py_files.extend(sorted((ROOT / "examples").rglob("*.py")))
    for path in py_files:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            fail(errors, f"{rel(path)}: Python syntax error: {exc}")


def python_dependency_surface_files() -> list[Path]:
    py_files = sorted((ROOT / "templates" / "python").glob("*.py"))
    py_files.extend(sorted((ROOT / "examples").rglob("*.py")))
    return py_files


def top_level_python_imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return set()

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imports.add(node.module.split(".", 1)[0])
    return imports


def python_stdlib_modules() -> set[str]:
    modules = set(getattr(sys, "stdlib_module_names", ()))
    modules.update(sys.builtin_module_names)
    modules.update(PYTHON_STDLIB_FALLBACK)
    return modules


def local_python_modules() -> set[str]:
    return {path.stem for path in python_dependency_surface_files()}


def third_party_python_import_packages(path: Path) -> set[str]:
    packages: set[str] = set()
    stdlib_modules = python_stdlib_modules()
    local_modules = local_python_modules()
    for import_name in top_level_python_imports(path):
        if import_name in stdlib_modules or import_name in local_modules:
            continue
        package = PYTHON_IMPORT_PACKAGE_MAP.get(import_name)
        if package:
            packages.add(package)
    return packages


def r_library_packages(path: Path) -> set[str]:
    packages: set[str] = set()
    for match in re.finditer(r"\blibrary\(\s*([A-Za-z0-9_.]+)\s*\)", path.read_text(encoding="utf-8")):
        packages.add(match.group(1).lower())
    return packages


def has_executable_bit(path: Path) -> bool:
    return bool(path.stat().st_mode & 0o111)


def check_cli_scripts(errors: list[str]) -> None:
    for path in REQUIRED_CLI_SCRIPTS:
        if not path.is_file():
            fail(errors, f"{rel(path)}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("#!/usr/bin/env python3\n"):
            fail(errors, f"{rel(path)}: missing python3 shebang")
        if not has_executable_bit(path):
            fail(errors, f"{rel(path)}: should be executable")
        if "if __name__ == \"__main__\":" not in text:
            fail(errors, f"{rel(path)}: missing __main__ guard")
        if "argparse.ArgumentParser" not in text:
            fail(errors, f"{rel(path)}: missing argparse CLI")


def check_r_templates(errors: list[str], require_optional_tools: bool) -> None:
    rscript = shutil.which("Rscript")
    if not rscript:
        message = "Rscript not found; skipping R template parse check"
        if require_optional_tools:
            fail(errors, message)
        else:
            print(f"warning: {message}", file=sys.stderr)
        return

    expression = (
        'files <- c(list.files("templates/r", pattern="[.]R$", full.names=TRUE), '
        'list.files("examples", pattern="[.]R$", full.names=TRUE, recursive=TRUE)); '
        'for (f in files) { parse(f); cat("OK", f, "\\n") }'
    )
    run_command([rscript, "-e", expression], errors, "R template parse")


def check_stata_templates(errors: list[str]) -> None:
    do_files = sorted((ROOT / "templates" / "stata").glob("*.do"))
    do_files.extend(
        sorted((ROOT / "examples" / "replication-package-skeleton").rglob("*.do"))
    )
    for path in do_files:
        text = path.read_text(encoding="utf-8")
        if "version 18.0" not in text:
            fail(errors, f"{rel(path)}: missing Stata version declaration")
        if path.name == "00_globals.do" and 'global project "`c(pwd)\'"' not in text:
            fail(errors, f"{rel(path)}: project root should come from c(pwd)")


def check_installer(errors: list[str]) -> None:
    installer = ROOT / "scripts" / "install_skills.py"
    if not installer.is_file():
        fail(errors, f"{rel(installer)}: missing")
        return

    expected = sorted(path.name for path in (ROOT / "skills").glob("aer-*") if path.is_dir())
    with tempfile.TemporaryDirectory() as tempdir:
        destination = Path(tempdir) / "skills"
        result = subprocess.run(
            [
                sys.executable,
                str(installer),
                "codex",
                "--dest",
                str(destination),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if result.returncode != 0:
            fail(errors, f"{rel(installer)} smoke test failed\n{result.stdout.strip()}")
            return
        installed = sorted(path.name for path in destination.glob("aer-*") if path.is_dir())
        if installed != expected:
            fail(errors, f"{rel(installer)} smoke test installed wrong skill set")
            return
        for name in installed:
            if not (destination / name / "SKILL.md").is_file():
                fail(errors, f"{rel(installer)} smoke test missed {name}/SKILL.md")

        second_run = subprocess.run(
            [
                sys.executable,
                str(installer),
                "codex",
                "--dest",
                str(destination),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if second_run.returncode != 0:
            fail(errors, f"{rel(installer)} existing-install smoke test failed")
        if "skip existing" not in second_run.stdout:
            fail(errors, f"{rel(installer)} should skip existing installs by default")

        source_dest = subprocess.run(
            [
                sys.executable,
                str(installer),
                "codex",
                "--dest",
                str(ROOT / "skills"),
                "--replace",
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if source_dest.returncode == 0:
            fail(errors, f"{rel(installer)} should refuse installing into source skills/")

        repo_root_dest = subprocess.run(
            [
                sys.executable,
                str(installer),
                "codex",
                "--dest",
                str(ROOT),
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if repo_root_dest.returncode == 0:
            fail(errors, f"{rel(installer)} should refuse repository root destination")

        repo_child_dest = subprocess.run(
            [
                sys.executable,
                str(installer),
                "codex",
                "--dest",
                str(ROOT / "docs"),
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if repo_child_dest.returncode == 0:
            fail(errors, f"{rel(installer)} should refuse repository-internal destination")

        project_scoped_dest = subprocess.run(
            [
                sys.executable,
                str(installer),
                "claude",
                "--dest",
                str(ROOT / ".claude" / "skills"),
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if project_scoped_dest.returncode != 0:
            fail(errors, f"{rel(installer)} should allow project-scoped .claude/skills dry-run")
        if "install" not in project_scoped_dest.stdout:
            fail(errors, f"{rel(installer)} project-scoped dry-run should preview installs")


def check_scaffolder(errors: list[str]) -> None:
    scaffolder = ROOT / "scripts" / "scaffold_project.py"
    if not scaffolder.is_file():
        fail(errors, f"{rel(scaffolder)}: missing")
        return

    expected_files = {
        "stata": "run_all.do",
        "r": "run_all.R",
        "python": "run_all.py",
        "skeleton": "run_all.do",
    }
    skeleton_dirs = (
        "data/raw",
        "data/intermediate",
        "data/codebook",
        "docs",
        "logs",
        "output/tables",
        "output/figures",
    )
    skeleton_source = ROOT / "examples" / "replication-package-skeleton"
    for directory in skeleton_dirs:
        keep_file = skeleton_source / directory / ".gitkeep"
        if not keep_file.is_file():
            fail(errors, f"{rel(keep_file)}: missing skeleton directory placeholder")

    with tempfile.TemporaryDirectory() as tempdir:
        base = Path(tempdir)
        for kind, expected_file in expected_files.items():
            destination = base / kind
            result = subprocess.run(
                [
                    sys.executable,
                    str(scaffolder),
                    kind,
                    str(destination),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            if result.returncode != 0:
                fail(errors, f"{rel(scaffolder)} {kind} smoke test failed\n{result.stdout.strip()}")
                continue
            if not (destination / expected_file).is_file():
                fail(errors, f"{rel(scaffolder)} {kind} smoke test missed {expected_file}")
            if kind == "skeleton":
                for directory in skeleton_dirs:
                    if not (destination / directory).is_dir():
                        fail(
                            errors,
                            f"{rel(scaffolder)} skeleton smoke test missed {directory}/",
                        )
                if not (destination / "docs" / "exhibit-register.md").is_file():
                    fail(
                        errors,
                        f"{rel(scaffolder)} skeleton smoke test missed docs/exhibit-register.md",
                    )
                if not (destination / "data" / "codebook" / "source-register.md").is_file():
                    fail(
                        errors,
                        f"{rel(scaffolder)} skeleton smoke test missed data/codebook/source-register.md",
                    )

        non_empty = base / "non-empty"
        non_empty.mkdir()
        (non_empty / "README.md").write_text("existing\n", encoding="utf-8")
        refused = subprocess.run(
            [
                sys.executable,
                str(scaffolder),
                "python",
                str(non_empty),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if refused.returncode == 0:
            fail(errors, f"{rel(scaffolder)} should refuse non-empty destination by default")

        source_refused = subprocess.run(
            [
                sys.executable,
                str(scaffolder),
                "stata",
                str(ROOT / "templates" / "stata"),
                "--replace",
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if source_refused.returncode == 0:
            fail(errors, f"{rel(scaffolder)} should refuse template source destination")

        nested_refused = subprocess.run(
            [
                sys.executable,
                str(scaffolder),
                "stata",
                str(ROOT / "templates" / "stata" / "nested-output"),
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if nested_refused.returncode == 0:
            fail(errors, f"{rel(scaffolder)} should refuse destination inside template source")

        protected_refused = subprocess.run(
            [
                sys.executable,
                str(scaffolder),
                "stata",
                str(ROOT),
                "--replace",
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if protected_refused.returncode == 0:
            fail(errors, f"{rel(scaffolder)} should refuse replacing repository root")

        repo_child_refused = subprocess.run(
            [
                sys.executable,
                str(scaffolder),
                "stata",
                str(ROOT / "docs" / "scaffold-output"),
                "--dry-run",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if repo_child_refused.returncode == 0:
            fail(errors, f"{rel(scaffolder)} should refuse repository-internal destinations")


def check_requirements(errors: list[str]) -> dict[str, int]:
    requirements = ROOT / "templates" / "python" / "requirements.txt"
    seen: dict[str, int] = {}
    if not requirements.is_file():
        fail(errors, f"{rel(requirements)}: missing")
        return seen

    for lineno, raw_line in enumerate(requirements.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if "==" not in line:
            fail(errors, f"{rel(requirements)}:{lineno}: dependency is not exactly pinned")
            continue
        package = line.split("==", 1)[0].strip().lower()
        if package in seen:
            fail(errors, f"{rel(requirements)}:{lineno}: duplicate dependency {package}")
        seen[package] = lineno
    return seen


def check_python_dependency_pins(errors: list[str], pinned_packages: dict[str, int]) -> None:
    stdlib_modules = python_stdlib_modules()
    local_modules = local_python_modules()

    for path in python_dependency_surface_files():
        for import_name in sorted(top_level_python_imports(path)):
            if import_name in stdlib_modules or import_name in local_modules:
                continue
            package = PYTHON_IMPORT_PACKAGE_MAP.get(import_name)
            if not package:
                fail(
                    errors,
                    f"{rel(path)}: third-party import {import_name!r} is not mapped "
                    "to a pinned package",
                )
                continue
            if package not in pinned_packages:
                fail(
                    errors,
                    f"{rel(path)}: import {import_name!r} requires {package!r} "
                    "in templates/python/requirements.txt",
                )


def check_makefile(errors: list[str]) -> None:
    makefile = ROOT / "Makefile"
    if not makefile.is_file():
        fail(errors, "Makefile: missing")
        return
    text = makefile.read_text(encoding="utf-8")
    if "preflight:" not in text:
        fail(errors, "Makefile: missing preflight target")
    if "git diff --check" not in text:
        fail(errors, "Makefile: preflight should run git diff --check")
    if "git diff --cached --check" not in text:
        fail(errors, "Makefile: preflight should run git diff --cached --check")
    if "scaffold-skeleton:" not in text:
        fail(errors, "Makefile: missing scaffold-skeleton target")
    if "./aer-" in text:
        fail(errors, "Makefile: scaffold targets should require explicit DEST")
    for target in ("scaffold-stata", "scaffold-r", "scaffold-python", "scaffold-skeleton"):
        pattern = rf"{target}:\n\t@test -n \"\$\(DEST\)\""
        if not re.search(pattern, text):
            fail(errors, f"Makefile: {target} should require DEST")


def check_gitignore(errors: list[str]) -> None:
    gitignore = ROOT / ".gitignore"
    if not gitignore.is_file():
        fail(errors, ".gitignore: missing")
        return

    lines = {
        line.strip()
        for line in gitignore.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    required_patterns = (".claude/", "__pycache__/", ".venv/", "node_modules/")
    for pattern in required_patterns:
        if pattern not in lines:
            fail(errors, f".gitignore: missing {pattern}")


def check_no_tracked_generated_files(errors: list[str]) -> None:
    allowed = {
        "examples/replication-package-skeleton/logs/.gitkeep",
        "examples/replication-package-skeleton/output/figures/.gitkeep",
        "examples/replication-package-skeleton/output/tables/.gitkeep",
    }
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        fail(errors, f"git ls-files failed\n{result.stdout.strip()}")
        return

    for tracked in result.stdout.splitlines():
        if tracked in allowed:
            continue
        if any(part in GENERATED_OR_CACHE_DIRS for part in Path(tracked).parts):
            fail(errors, f"{tracked}: generated/cache path should not be tracked")


def check_ci_workflow(errors: list[str]) -> None:
    workflow = ROOT / ".github" / "workflows" / "ci.yml"
    if not workflow.is_file():
        fail(errors, f"{rel(workflow)}: missing")
        return
    text = workflow.read_text(encoding="utf-8")
    required_snippets = (
        "pull_request:",
        "branches:",
        "- main",
        "actions/checkout@v4",
        "actions/setup-python@v5",
        "python-version: \"3.12\"",
        "sudo apt-get install -y r-base",
        "make preflight",
        "make validate-strict",
    )
    for snippet in required_snippets:
        if snippet not in text:
            fail(errors, f"{rel(workflow)}: missing {snippet!r}")


def check_no_local_paths(errors: list[str]) -> None:
    checked_roots = (
        ROOT / "templates",
        ROOT / "examples",
        ROOT / "scripts",
        ROOT / ".github",
    )
    checked_files = [ROOT / "Makefile"]
    for root in checked_roots:
        if root.exists():
            checked_files.extend(path for path in root.rglob("*") if path.is_file())

    for path in sorted(set(checked_files)):
        if any(part in GENERATED_OR_CACHE_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        for marker in LOCAL_PATH_MARKERS:
            if marker in text:
                fail(errors, f"{rel(path)}: local absolute path marker {marker!r}")


def path_allows_unfinished_markers(path: Path) -> bool:
    if path in ALLOWED_UNFINISHED_MARKER_FILES:
        return True
    return any(path.is_relative_to(directory) for directory in ALLOWED_UNFINISHED_MARKER_DIRS)


def unfinished_marker_in_text(text: str) -> str | None:
    for marker in UNFINISHED_MARKERS:
        if re.search(rf"\b{re.escape(marker)}\b", text, flags=re.IGNORECASE):
            return marker
    return None


def check_unfinished_markers(errors: list[str]) -> None:
    for path in text_files():
        if path_allows_unfinished_markers(path):
            continue
        text = path.read_text(encoding="utf-8")
        marker = unfinished_marker_in_text(text)
        if marker:
            fail(errors, f"{rel(path)}: unfinished-work marker {marker!r} is not allowed here")


def check_text_hygiene(errors: list[str]) -> None:
    for path in text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            fail(errors, f"{rel(path)}: expected UTF-8 text")
            continue

        if text and not text.endswith("\n"):
            fail(errors, f"{rel(path)}: missing final newline")

        for lineno, line in enumerate(text.splitlines(), 1):
            if line.rstrip(" \t") != line:
                fail(errors, f"{rel(path)}:{lineno}: trailing whitespace")
                break


def check_placeholder_links(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        if "journal site" in text.lower():
            fail(errors, f"{rel(path)}: replace 'journal site' placeholder with a DOI or stable URL")


def validate(require_optional_tools: bool = False) -> None:
    errors: list[str] = []
    check_validator_self_tests(errors)
    check_text_hygiene(errors)
    skill_names = check_skills(errors)
    check_plugin_manifest(skill_names, errors)
    check_repository_urls(errors)
    check_skill_reference_docs(skill_names, errors)
    check_source_register(errors)
    check_policy_guardrails(errors)
    check_installation_guardrails(errors)
    check_skill_resource_links(errors)
    check_bibliography_integrity(errors)
    check_markdown_links(errors)
    check_template_layout(errors)
    check_example_demos(errors)
    check_python_templates(errors)
    check_cli_scripts(errors)
    check_r_templates(errors, require_optional_tools=require_optional_tools)
    check_stata_templates(errors)
    check_installer(errors)
    check_scaffolder(errors)
    python_requirements = check_requirements(errors)
    check_python_dependency_pins(errors, python_requirements)
    check_makefile(errors)
    check_gitignore(errors)
    check_no_tracked_generated_files(errors)
    check_ci_workflow(errors)
    check_no_local_paths(errors)
    check_unfinished_markers(errors)
    check_placeholder_links(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise ValidationError(f"{len(errors)} validation error(s)")

    print("Repository validation passed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-optional-tools",
        action="store_true",
        help="fail instead of warning when optional tools such as Rscript are unavailable",
    )
    args = parser.parse_args()

    try:
        validate(require_optional_tools=args.require_optional_tools)
    except ValidationError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
