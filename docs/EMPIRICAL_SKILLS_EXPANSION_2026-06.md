# Empirical-Skills Expansion — 2026-06

This pass added **12 vetted, open-source, no-paid-core agent skills** (collections
`51`–`62`, **73 `SKILL.md` files**) to the catalog, chosen to fill concrete gaps in
the existing 54-collection set. Every addition is a curated upstream snapshot with
`SKILL.md` frontmatter, an attributed `README-original.md`, and an upstream `LICENSE`
(or an explicit provenance note where upstream ships none).

Selection bar (per [`SKILL_SUBMISSION_GUIDE.md`](SKILL_SUBMISSION_GUIDE.md)): open
source with a clear license; runnable/inspectable **without** a paid or proprietary
core; safe for an agent to read (no credential exfiltration, reverse shells, hidden
download-and-run, or prompt injection); relevant to empirical research; and not a
duplicate of an already-vendored owner/repo.

## What was added

| # | Collection | License | Skills | Gap it fills |
|---|---|---|---|---|
| 51 | [pymc-labs/CausalPy](../skills/51-pymc-labs-CausalPy/) | Apache-2.0 | 3 | Quasi-experiment **estimation**: DiD, staggered/synthetic DiD, RDD & regression kink, interrupted time series, synthetic control, IV/IPW, panel — with method-choice and placebo skills |
| 52 | [keemanxp/slr-prisma](../skills/52-keemanxp-slr-prisma/) | MIT | 1 | **PRISMA 2020** systematic literature review (all 27 items + flow diagram) |
| 53 | [keemanxp/thematic-analysis-skill](../skills/53-keemanxp-thematic-analysis-skill/) | MIT | 1 | **Qualitative** analysis: Braun & Clarke six-phase thematic analysis |
| 54 | [scdenney/open-science-skills](../skills/54-scdenney-open-science-skills/) | CC-BY-NC-4.0 | 24 | **Experimental & survey social science**: conjoint design/cleaning/diagnostics, cross-national design, list experiments, pre-registration, topic modeling, text classification |
| 55 | [ab604/claude-code-r-skills](../skills/55-ab604-claude-code-r-skills/) | MIT | 8 | **R statistical computing**: `r-bayes` (brms/cmdstanr multilevel + DAG validation + marginal effects), idiomatic tidyverse/perf/TDD |
| 56 | [hanlulong/econ-writing-skill](../skills/56-hanlulong-econ-writing-skill/) | MIT | 1 | **Economics writing** with 13 identification strategies + AEA replication-package standards |
| 57 | [dgunning/edgartools](../skills/57-dgunning-edgartools/) | MIT | 1 | **Corporate-disclosure data**: SEC EDGAR filings / XBRL / 13F / Forms 3-4-5 (free API, no key) |
| 58 | [charlescoverdale/econstack](../skills/58-charlescoverdale-econstack/) | MIT¹ | 7 | **Official-statistics** macro/fiscal briefings & cost-benefit (Green Book), multi-source public data |
| 59 | [shiquda/openalex-skill](../skills/59-shiquda-openalex-skill/) | MIT | 1 | **Bibliometric data**: OpenAlex works/authors/citations retrieval |
| 60 | [regisely/superpapers](../skills/60-regisely-superpapers/) | MIT | 16 | **Reproducible empirical paper pipeline** (replication-driven: every number regenerable from raw data with a fixed seed) |
| 61 | [phdemotions/research-methods](../skills/61-phdemotions-research-methods/) | MIT | 9 | **Data management**: clean / validate / profile / EDA, raw-data immutability, CONSORT exclusion flows, method templates |
| 62 | [PHY041/claude-skill-citation-checker](../skills/62-PHY041-claude-skill-citation-checker/) | MIT¹ | 1 | **Citation hygiene**: verify `.bib` against CrossRef / Semantic Scholar / OpenAlex; catch hallucinated/chimeric refs |

¹ `econstack` and `citation-checker` declare MIT in their README (badge / `## License`
section) but ship no separate `LICENSE` file upstream; recorded with
`source_confidence: medium` in [`provenance.json`](../catalog/provenance.json).

### Curation notes

- **CausalPy** — only the `causalpy/skills/` component is vendored (3 method skills +
  reference cards), not the package source; the dev-workflow skills under
  `.github/skills/` were excluded.
- **scdenney/open-science-skills** — Claude-native skills only. The `-codex` variants
  (which call the OpenAI API) and the `presubmit` setup skill (which `eval`s the user's
  shell rc to locate `ANTHROPIC_API_KEY`) were **excluded** to keep the snapshot
  no-paid-core and read-safe.
- **edgartools** — only `edgar/ai/skills/` (the agent-skill bundle) is vendored, not the
  Python package.
- **econstack** — skill definitions + supporting `facts/` and `templates/` markdown only;
  the upstream `bin/` and `scripts/*.sh` executables and `tests/` were not vendored.

## Security review summary

Executable surface in the new collections is small and was read end-to-end:

- `62/scripts/citation_checker.py` — HTTP **GET** only to `api.crossref.org`,
  `api.semanticscholar.org`, `api.openalex.org` (free scholarly APIs). No shell, no
  exfiltration.
- `60/skills/compile-latex/scripts/compile.sh` — standard multi-pass LaTeX compiler
  (`set -euo pipefail`, engine auto-detect). No network.
- `57/.../content/skill.yaml` — local SVG→PNG via `inkscape subprocess` (chart export).
- `55/.../rlang-patterns/SKILL.md:238` — `eval(parse())` appears only as a labelled
  **anti-pattern example** ("# Dangerous!"), not executed.

No `curl|bash`, reverse shells, base64-piped execution, or credential exfiltration was
found in vendored content. (The upstream `README-original.md` for `56` documents an
upstream `curl … | bash` installer; AERS vendors the skill directly, so that path is
informational only.)

## Ready-to-paste README rows (for the maintainer)

`README.md` / `README-zh.md` were being edited concurrently in the shared worktree
during this pass, so they were intentionally **not** touched here. The rows below can be
dropped into the relevant README tables when convenient.

Rows link to upstream GitHub (matching the README's existing external-link style); the
local vendored path is noted as `skills/NN` in the function column.

**Economics / Causal Inference**

```markdown
| [pymc-labs/CausalPy](https://github.com/pymc-labs/CausalPy) | Apache-2.0 | Quasi-experiment estimation skills: DiD/SDID, RDD/kink, ITS, synthetic control, IV/IPW, panel + method-choice + placebo (`skills/51`) | Observational causal estimation |
| [hanlulong/econ-writing-skill](https://github.com/hanlulong/econ-writing-skill) | MIT | Economics paper writing with 13 identification strategies + AEA replication standards (`skills/56`) | Econ manuscript writing |
| [dgunning/edgartools](https://github.com/dgunning/edgartools) | MIT | SEC EDGAR filings / XBRL / 13F / insider-form data skills, free API (`skills/57`) | Empirical finance / IO data |
| [charlescoverdale/econstack](https://github.com/charlescoverdale/econstack) | MIT | Official-statistics macro/fiscal briefings + Green Book cost-benefit (`skills/58`) | Policy / macro data work |
```

**Reproducibility / Data**

```markdown
| [regisely/superpapers](https://github.com/regisely/superpapers) | MIT | Replication-driven empirical paper pipeline, every number regenerable from raw data (`skills/60`) | Reproducible quant research |
| [phdemotions/research-methods](https://github.com/phdemotions/research-methods) | MIT | Data clean/validate/profile/EDA with raw-data immutability + CONSORT flows (`skills/61`) | Data management |
```

**Social-science methods**

```markdown
| [keemanxp/slr-prisma](https://github.com/keemanxp/slr-prisma) | MIT | PRISMA 2020 systematic literature review (`skills/52`) | Systematic review |
| [keemanxp/thematic-analysis-skill](https://github.com/keemanxp/thematic-analysis-skill) | MIT | Braun & Clarke six-phase thematic analysis (`skills/53`) | Qualitative analysis |
| [scdenney/open-science-skills](https://github.com/scdenney/open-science-skills) | CC-BY-NC-4.0 | Conjoint/survey/list-experiment design, pre-registration, topic modeling (`skills/54`) | Experimental social science |
```

**Statistical computing / bibliometrics / citation hygiene**

```markdown
| [ab604/claude-code-r-skills](https://github.com/ab604/claude-code-r-skills) | MIT | r-bayes (brms/cmdstanr multilevel, DAGs, marginal effects) + idiomatic R (`skills/55`) | R statistical computing |
| [shiquda/openalex-skill](https://github.com/shiquda/openalex-skill) | MIT | OpenAlex works/authors/citations retrieval (`skills/59`) | Bibliometric data |
| [PHY041/claude-skill-citation-checker](https://github.com/PHY041/claude-skill-citation-checker) | MIT | Verify .bib vs CrossRef/Semantic Scholar/OpenAlex; catch hallucinated refs (`skills/62`) | Citation hygiene |
```

## Vetted backlog (not vendored this pass)

**Deferred — strong content, but license-blocked** (re-check if upstream adds an OSI/CC
license):

- `HaipingXu/social-science-claude-scholar` — staggered/Callaway-Sant'Anna/Sun-Abraham/Bartik causal skill; **no LICENSE**.
- `franklee16/academic-research-skills`, `lingzhi227/agent-research-skills`,
  `nimrodfisher/data-analytics-skills`, `johanfourieza/econtools`,
  `lcrawfurd/claude-skills` (Cunningham referee-2 reproducibility audit) — all **no top-level LICENSE**.

**Deferred — acceptable but lower priority / overlap** (candidates for a future wave):

- `beita6969/ScienceClaw` (MIT, ~829★) — `economics-analysis` skill; strip one hardcoded venv path.
- `flonat/claude-research` (MIT) — `causal-design` + `pipeline-manifest`; broad, some overlap with 60/61.
- `tondevrel/scientific-agent-skills` (MIT) — DoWhy identify-estimate-refute.
- `ondata/skills` (CC-BY-SA-4.0 + GPL-3.0) — OpenAlex + open-data quality scoring.
- `smartbiblia-solutions/agent-skills` (MIT) — OpenAlex/HAL/Sudoc bibliometric pipeline.
- `posit-dev/skills` (MIT) — vendor only `quarto-authoring`.

**Gaps with no clean candidate found** (June 2026): a standalone, licensed skill for
local projections / impulse responses, spatial econometrics, MRP / survey weighting, or
`metafor`-style meta-analysis forest plots. These exist only as sub-sections inside
broader skills, not as dedicated licensed repos.

## Coordination & handoff

- **Branch / worktree:** committed on `bench/empirical-benchmark-depth` in the primary
  worktree, which was **shared with a concurrent agent** working on
  benchmark / eval-harness / repo-hygiene tooling. To avoid entangling work, this pass
  staged **only its own paths** with explicit pathspecs and never ran `git add -A`.
- **Files intentionally not touched** (concurrent edits in flight): `README.md`,
  `README-zh.md`, `Makefile`, `scripts/validate-repo.py`, `benchmark/**`,
  `eval-harness/**`, `tests/**`, `.pre-commit-config.yaml`,
  `.github/workflows/quality-evals.yml`, `docs/QUALITY_GATE.md`,
  `docs/agent-worklog-bench.md`, `docs/FAQ.md`.
- **Generated files** were rebuilt with `make catalog` (provenance, skill-audit, catalog,
  enriched catalog, license audit) and committed alongside the source. `make validate`
  is clean.
- **Provenance source of truth:** `scripts/build-provenance.py` `OVERRIDES` gained one
  entry per new collection (source URL, license, snapshot note).
- **Follow-ups for the maintainer:** (1) paste the README rows above; (2) optionally pull
  from the vetted backlog in a future wave.
