# PyPI packaging draft — AERS first-party skills

> **Status:** proposal, 2026-07. This document is the *plan*, not a
> published package. The actual first-party skills (`brycewang-stanford/*`)
> are vendored into this repo; installing them via `pip` is **optional**
> and not required to use AERS in any agent.

## Why package?

The repo root is a **catalog** (1,150 skills / 69 collections). The
first-party subset (StatsPAI, 00.1 Python, 00.2 Stata, 00.3 R, 50 AER-skills)
is independently useful and has its own test suite / changelog / release
cadence. Researchers and agent builders have asked for a way to `pip
install aers-statspai` without dragging in the 1,150-skill mirror.

Packaging also gives us a unit for **semantic versioning** of empirical
methods — the same `0.1.x → 0.2.0` signal the rest of Python uses, instead
of "whatever the sync gave you this week".

## Scope of the first cut

| Package name | Source path | What it contains | Status |
|---|---|---|---|
| `aers-statspai` | `skills/00-Full-empirical-analysis-skill_StatsPAI/` | `sp.*` DSL, scripts, examples | **proposed** |
| `aers-empirical-py` | `skills/00.1-Full-empirical-analysis-skill_Python/` | Python empirical 8-step pipeline | not yet |
| `aers-empirical-stata` | `skills/00.2-Full-empirical-analysis-skill_Stata/` | Stata .do templates | not yet |
| `aers-empirical-r` | `skills/00.3-Full-empirical-analysis-skill_R/` | R Quarto + scripts | not yet |
| `aers-aer` | `skills/50-brycewang-aer-skills/` | AER pipeline (identification → submission) | not yet |

The first cut should ship **only `aers-statspai`** — the rest depend on
external tool stacks (`statsmodels`, `linearmodels`, `pyfixest`, Stata,
R) that are large and version-sensitive. Mixing them into one metapackage
is a future question.

## Proposed `pyproject.toml` shape (sketch)

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "aers-statspai"
version = "0.1.0"  # starts from the SKILL.md frontmatter in the mirror
description = "StatsPAI skill for Claude Code / Codex — agent-native Python DSL for causal inference and applied econometrics."
readme = "skills/00-Full-empirical-analysis-skill_StatsPAI/README.md"
requires-python = ">=3.9"
license = { text = "MIT" }
authors = [
    { name = "Bryce Wang", email = "brycew@stanford.edu" },
]
keywords = ["causal-inference", "econometrics", "agent-skills", "did", "iv", "rdd", "synthetic-control"]
classifiers = [
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
    "Operating System :: OS Independent",
]

[project.urls]
Homepage = "https://github.com/brycewang-stanford/StatsPAI"
"AERS catalog" = "https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills"

# StatsPAI bundles its own implementation; the SKILL.md file is shipped
# inside the wheel as a "skill manifest" an agent runtime can discover.
[tool.setuptools.package_data]
"aers_statspai" = ["SKILL.md", "references/*.md", "examples/*.py"]
```

The actual implementation is at
[`brycewang-stanford/StatsPAI`](https://github.com/brycewang-stanford/StatsPAI);
this draft is about *how* the vendored mirror would map into a wheel.

## Distribution channels

| Channel | When | How |
|---|---|---|
| **GitHub release tarball** | first | `python3 -m build` → upload to the StatsPAI release page; users `pip install aers-statspai==X.Y.Z` |
| **PyPI** | after a stable API | `twine upload dist/*` from CI; one-time setup |
| **Mirror in this repo** | always | the AERS weekly sync continues to vendor the published release, so the catalog is never stale |

The PyPI channel is the *consumer* path. The vendored mirror in this repo
stays the *catalog* path. They reinforce each other.

## Versioning

- Map the existing SKILL.md frontmatter `version:` field to PyPI semver
  (`0.1.0` → patch / minor / major bumps per the upstream changelog).
- Tag every weekly sync with the upstream PyPI release SHA, so a
  `catalog/skills-enriched.json` entry can show
  "this mirror was taken from aers-statspai 0.1.4 (release-2026-07-03)".
- A new major version of the upstream package triggers a re-audit of
  the mirror in the weekly sync.

## What packaging does *not* change

- The vendored mirror in `skills/00-…/` stays. PyPI is an *additional*
  install path for users who don't want the whole catalog.
- The first-party **routing header** (`SKILL.md` at the repo root) stays
  catalog-only. The PyPI package ships the *implementation* but the
  catalog router still expects an `SKILL.md` next to a vendored folder.
- The RIGOR_COVERAGE, SKILL_HYGIENE, and BENCHMARK_SCOREBOARD numbers
  continue to be computed over the vendored mirror, not over a separate
  PyPI install.

## Decision: which 3 things would have to be true before shipping

1. **`aers-statspai` upstream is at >= 0.1.0 with a frozen public API.**
   Today it is moving fast; packaging an unstable API just to ship a
   package is busy-work.
2. **A CI pipeline in the upstream repo can build wheels and publish
   to TestPyPI on tag.** The catalog sync already runs weekly; the
   PyPI publish should fire from the upstream repo, not the catalog.
3. **The vendored mirror's `SKILL.md` carries the published version
   tag, so `aers-statspai==X.Y.Z` and the vendored mirror at
   `skills/00-…/SKILL.md` describe the same API.** This is what
   `scripts/sync-vendored-commit.py` is meant to enforce.

When those three line up, a `make release-pypi` target on the upstream
side closes the loop.

## What a reviewer should know

- `aers-statspai` is the **first** of potentially five `aers-*` packages;
  the others are sketches in the table above.
- The first cut does **not** include the 50-brycewang-aer-skills pipeline.
  That collection depends on `booktabs` / Quarto / pdflatex and is a
  larger packaging problem; we will tackle it after the StatsPAI cut
  ships cleanly.
- Vendoring stays. PyPI is **additive**.

## Cross-reference

- StatsPAI upstream: https://github.com/brycewang-stanford/StatsPAI
- AERS catalog router: [`SKILL.md`](../SKILL.md)
- Sync tool: [`scripts/sync-vendored-commit.py`](../scripts/sync-vendored-commit.py)
- Roadmap entry: "Package first-party AERS skills as installable bundles
  for agent runtimes that support plugins/marketplaces." —
  [`ROADMAP.md`](ROADMAP.md)
