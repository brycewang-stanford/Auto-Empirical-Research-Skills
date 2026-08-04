# Changelog

This is the project's narrative changelog. `README.md` keeps only a short
"Recent highlights" list and links here for the full history.

## Unreleased

- Renamed and rewrote collection 48: **`48-copaper-ai-chinese-de-aigc` →
  [`48-de-AIGC-skills`](skills/48-de-AIGC-skills/)**, extending the
  Chinese-only academic de-AIGC skill to **bilingual EN+ZH coverage** for
  empirical papers in economics, management, and the social sciences. The v2
  skill adds a 22-pattern English library (`references/patterns-en.md`, with a
  preserve-list against over-correction), renumbers the Chinese library to
  ZH01–ZH17, upgrades the five-step loop to a six-step loop with an explicit
  **claim–evidence audit** (verb strength must match identification strength),
  makes the section strategies and five-dimension rubric bilingual, and ships
  8 new English before/after cases alongside the 12 Chinese ones. Design
  references: the humanizer_academic / academic-humanizer / deslop / stop-slop
  lineages. All six locale READMEs, the router, and the demo
  ([`docs/demos/de-aigc.md`](docs/demos/de-aigc.md), renamed from
  `chinese-de-aigc.md`) were updated to the new path.
- Hardened the whole-repo skill encapsulation. The root router
  [`SKILL.md`](SKILL.md) now declares its `license` in frontmatter, warns
  that the two catalog JSON files are ~1 MB each and shows a copy-paste
  query one-liner instead of inviting a full read, and adds ten
  previously-unrouted method rows to the routing table (matching/propensity
  scores, structural estimation, time series, text-as-data/NLP, spatial/GIS,
  RCT design, survey design, open science, grant proposals, and conference
  posters — each verified against `catalog/skills.json`). A new
  `validate_root_skill_stats` check in `scripts/validate-repo.py` (wired
  into `make validate`) keeps the router's hardcoded numbers honest: the
  "N skills across M vendored collections" line, the duplicate bare-name
  count, and the legacy-collections list are now all cross-checked against
  the committed catalog, so a catalog refresh can no longer strand the
  router with stale stats.
- Added a generated **rigor coverage badge** (shields.io endpoint JSON at
  [`docs/badges/rigor-coverage.json`](docs/badges/rigor-coverage.json), built
  by `scripts/build-release-notes.py` and freshness-checked in `make
  validate`) and wired it into all six locale READMEs. The badge and the
  release snapshot now source the method-family roster from
  `build-coverage-map.py`'s METHOD_ORDER, so they can never disagree with
  [`docs/RIGOR_COVERAGE.md`](docs/RIGOR_COVERAGE.md).
- Documented the **candidate grading protocol** in
  [`docs/INTEROP.md`](docs/INTEROP.md) (Recipe C): step-by-step instructions
  for grading any external agent against the numeric benchmark by dropping a
  `results.json` into `benchmark/candidates/`, with the honesty checks
  explained — groundwork for the AERS-vs-Econometrics-Agent comparison.
- Expanded the methodological rigor coverage map from 13 to **15 method
  families**, adding end-to-end closure (taxonomy tag + eval scenario +
  numeric benchmark task) for **shift-share / Bartik IV**
  (`aer-shiftshare-identification` + `bartik-recovery`: a 12-region design
  where OLS through the local demand shock is biased 1.157 vs true 0.5 and
  only the share-times-shock instrument recovers it — the exclusion
  restriction holds exactly in-sample by construction) and **causal
  mediation** (`statspai-mediation-assumptions` + `mediation-recovery`: the
  folk "control for the mediator" move flips the sign of the true +1 direct
  effect to -2.76 under mediator-outcome confounding, while the
  confounder-adjusted NDE/NIE decomposition recovers 1 + 3 = 4 exactly).
  Eval/CI ratchet floors raised to lock in the coverage (28 scenarios /
  132 auto-checks, 15 benchmark tasks), with construction-invariant unit
  tests for both simulations and README stats synced across all six locales
  (enforced by the rigor-stats gate).

## 2026-07-02 — v2026.07 (first tagged release)

Everything below this line up to the 2026-06-04 section shipped in
[`v2026.07`](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/releases/tag/v2026.07),
the project's first tagged release. Additional v2026.07 changes not itemized
below: CI installs the scientific stack for the Paper-WorkFlow demo gate
(validate-catalog had been red on `main` since 2026-06-26); both weekly
upstream sync PRs were unblocked and merged (the StatsPAI sync restores the
SkillOpt execution-gate card that upstream had condensed away); the
Paper-WorkFlow submodule's competitive-rigor layer (29/29 executable gates)
merged to its `main` with a drift-gated README rigor badge; headline counts
were reconciled to **1,150 skills / 69 collections**; and debugging scratch
files were removed from `demo-notebooks/`.

- Expanded the methodological rigor coverage map from 11 to **13 method
  families**, adding end-to-end closure (taxonomy tag + eval scenario +
  numeric benchmark task) for **heterogeneous treatment effects (CATE)**
  (`statspai-heterogeneous-effects` + `cate-recovery`: opposite-signed
  subgroup effects with a composition-biased pooled contrast) and
  **quantile / distributional effects** (`statspai-quantile-effects` +
  `qte-recovery`: a tail-only shift where the median QTE is 0 and the q90
  QTE is 5x the mean effect). Eval-harness and CI ratchet floors were raised
  to lock in the new coverage (26 scenarios / 122 auto-checks, 13 benchmark
  tasks), with construction-invariant unit tests for both simulations.
- Added a machine-generated release snapshot
  ([`docs/RELEASE_NOTES.md`](docs/RELEASE_NOTES.md), built by
  `scripts/build-release-notes.py` via `make catalog`, freshness-checked in
  `make validate`), replacing the hand-filled stats template in
  [`docs/RELEASE.md`](docs/RELEASE.md).
- Added a six-locale README rigor-stats consistency gate
  (`scripts/check-readme-stats.py`, wired into `make validate` with unit
  tests): the benchmark-task and eval-scenario counts in every README's
  numbers table and trust-surface table must now match the committed TOMLs,
  so rigor expansions can no longer ship with stale marketing numbers. The
  gate immediately caught drift in all six locales (trust-surface rows still
  said 5/11 tasks and 17/95 scenarios) — now fixed.
- Added a feature-request issue template scoped to rigor coverage, catalog
  tooling, docs, and CI (skill collections keep their own submission
  template).
- Published the July 2026 execution plan
  ([`docs/PLAN-2026-07.md`](docs/PLAN-2026-07.md)) with week-by-week
  milestones, linked from the roadmap.
- Added two community-contributed collections (PRs #21/#22), bringing the repo to
  **1,144 vendored & cataloged skills / 68 collections**:
  [`67-econfin-workflow-toolkit`](skills/67-econfin-workflow-toolkit/) — an
  end-to-end econ/finance research workflow (ideation → estimation → writing →
  submission), and
  [`68-research-productivity-skills`](skills/68-research-productivity-skills/) —
  a compact productivity layer (paper discovery, literature synthesis, file
  conversion, slides, authoring). Both were rebased onto current `main` to drop a
  duplicate `zheng-siyao` collection, and the proprietary Anthropic office skills
  (`docx`/`pdf`/`pptx`/`xlsx`) and general-purpose UI skills (`frontend-design`,
  `ui-ux-pro-max`) were removed before vendoring per repo licensing policy.
- Restructured `README.md` / `README-zh.md` to lead with verifiable rigor
  (numbers, the 2-minute `make check` proof, and the trust surface), removed
  duplicated flagship-skill descriptions, consolidated badges, and moved this
  narrative changelog out of the README.
- Disambiguated the headline numbers: **1,052 vendored & cataloged skills /
  63 collections** in-repo, versus a curated map of **23,000+ skills / 119
  repos** in the wider ecosystem.
- Added generated machine-readable skill catalog and GitHub-readable catalog.
- Added generated provenance and license audit.
- Added local validation, catalog freshness checks, and CI workflow.
- Added external-link checker workflow for maintained documentation.
- Added Dependabot for GitHub Actions, OpenSSF Scorecard, and workflow policy validation.
- Added static search page over the generated catalog.
- Added flagship eval prompt registry and generated eval documentation.
- Added installation guide, skill submission guide, quality gate, roadmap, competitive landscape, and flagship demo pages.
- Normalized lowercase `skill.md` files to exact-case `SKILL.md` for Linux CI/runtime compatibility.

## 2026-06-04 — Tools catalog module (automated empirical & causal-inference tools)

- Added a new first-party module [`tools/`](tools/) cataloging **335 software
  tools** (across three same-day waves) for automated empirical research and causal
  inference — a layer distinct from the agent *skills* under `skills/` (a skill is
  read by an agent; a tool is invoked by one). Categories: `causal-inference-library`
  (32), `econometrics-library` (170), `research-agent` (51), `mcp-server` (48),
  `causal-discovery` (25), `benchmark-dataset` (9).
- **Second wave:** added the **`research-agent`** category — 51 autonomous research &
  data-science agents (AI-Scientist, data-to-paper, Agent Laboratory, RD-Agent,
  AI-Researcher, STORM, PaperQA2, gpt-researcher, DeepAnalyze, MetaGPT, Biomni, …), from
  two verified sweeps, de-duplicated. License caveats recorded verbatim (SakanaAI's custom
  Responsible-AI license, Coscientist's Commons Clause, 7 no-LICENSE repos); closed/hosted
  systems excluded.
- **Third wave:** niche-econometrics expansion (`econometrics-library` 86 → 170, +84) —
  **spatial econometrics** (spdep, spatialreg, PySAL/spreg, GeoDa, Stata `sp`), **local
  projections / IRF & (S)VAR** (lpirfs, vars, svars, localprojections, Stata `lpirf`),
  **survey weighting / MRP / raking** (survey, srvyr, samplics, balance, anesrake; brms /
  rstanarm as MRP engines), and **meta-analysis** (metafor, meta, netmeta, metaSEM, metan,
  PyMARE). Stata built-ins recorded `proprietary`, SSC modules `community-command`.
- Source of truth is the hand-curated [`tools/tools.json`](tools/tools.json);
  [`tools/CATALOG.md`](tools/CATALOG.md) and the README summary block are generated by
  [`scripts/build-tools-catalog.py`](scripts/build-tools-catalog.py), wired into
  `make catalog` and `make validate` (`--check`), with
  [`tests/test_tools_catalog.py`](tests/test_tools_catalog.py) in the suite.
- Added a scheduled **link/license re-check** for the catalog
  ([`scripts/check-tools-links.py`](scripts/check-tools-links.py) +
  [`.github/workflows/check-tools-links.yml`](.github/workflows/check-tools-links.yml))
  and integrated `tools.json` into the static search page
  ([`docs/tools-search.html`](docs/tools-search.html)).
- Every entry was verified against its upstream repo/CRAN/SSC page (license + activity
  snapshot). No third-party executable code is vendored — `tools/` is a metadata index.
- Curation notes, method, and backlog: [`docs/archive/EMPIRICAL_TOOLS_2026-06.md`](docs/archive/EMPIRICAL_TOOLS_2026-06.md).
- Linked the module from both READMEs (numbers table + a dedicated "Browse the
  landscape" subsection).

## 2026-05-31 — Rename and bilingual positioning

- Repository renamed to **Auto-Empirical Research Skills (AERS)**. GitHub
  redirects the old URL; update remotes to
  `https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git`.
- Expanded README and bilingual (EN/ZH) project positioning.

## 2026-05-25 — AER-skills vendored (top-5 economics submission stack)

- Vendored the sister project [brycewang-stanford/AER-skills](https://github.com/brycewang-stanford/AER-skills)
  in full at [`skills/50-brycewang-aer-skills/`](skills/50-brycewang-aer-skills/),
  with a StatsPAI-style weekly sync loop
  ([`scripts/sync-aer-skills.sh`](scripts/sync-aer-skills.sh) +
  [`.github/workflows/sync-aer-skills.yml`](.github/workflows/sync-aer-skills.yml),
  Monday 06:00 UTC diff, PR on drift; manual `workflow_dispatch` supported).
- **Nine skills covering the full submission pipeline:** `aer-topic-selection`
  (AER vs Insights vs AEJ routing) → `aer-identification` (modern DiD / weak IV /
  boundary RDD audit) → `aer-robustness` (referee-anticipating matrix) →
  `aer-introduction` (Keith Head five-paragraph intro) → `aer-tables-figures`
  (AER booktabs typesetting) → `aer-replication` (AEA Data and Code Availability
  Policy package, openICPSR-ready) → `aer-submission` (preflight: 100-word
  abstract, disclosure, cover letter) → `aer-rebuttal` (R&R letters against the
  *revised* manuscript) → `aer-workflow` (orchestrator).
- **Positioning:** StatsPAI / 00.x solve "run the analysis correctly"; AER-skills
  solves "write the paper to top-5 acceptance threshold" — covering AER's
  100-word abstract, AER:Insights' 7000-word limit, the ~45% desk-rejection
  rate, and AEA mandatory replication. Identification-first. License: MIT.

## 2026-04-28 — Security scan baseline complete (52/52 CLEAN)

- Ran a six-phase, defense-in-depth security audit over the **original 52 skill
  directories / 2,940+ files** — **52/52 CLEAN, zero FLAGGED**: no malicious
  prompts, viruses, trojans, reverse shells, or prompt injection.
- Method: automated grep across 13 risk categories → 100% manual review of all
  6 hook-bearing skills and their 40+ hook scripts → three parallel agent
  content audits → supplemental integrity checks (hidden Unicode, encoding
  anomalies, ultra-long lines, HTML injection, network imports).
- Every "sensitive" hit verified as a defensive security rule, a legitimate
  academic API call (arXiv / CrossRef / PubMed / FRED / World Bank / OECD / BLS),
  or a standard Claude Code workflow hook (all local file ops, zero network IO).
  Key insight: largest size ≠ highest risk. Full report:
  [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md).

## 2026-04-24 — Four full-pipeline flagship skills shipped

The same 8-step empirical loop, implemented four ways. All use progressive
disclosure (a canonical-call spine in `SKILL.md` plus deep per-step reference
manuals loaded on demand).

- **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)** (slot #0, flagship) —
  agent-native Python **DSL**: one `sp.causal(...)` runs the whole loop. 900+
  functions, self-describing API (`list_functions()` / `describe_function()` /
  `function_schema()`), unified `CausalResult`. Covers OLS, IV, panel, DID
  (Callaway–Sant'Anna / Sun–Abraham / Bacon / HonestDID / continuous), RDD, PSM,
  SCM, SDID, DML, Causal Forest, Meta-Learners, TMLE, AIPW, neural causal models,
  text causal, Heckman, and BLP. JOSS in submission, MIT. Weekly upstream sync
  from the StatsPAI main repo.
- **[00.1 Python](skills/00.1-Full-empirical-analysis-skill_Python/)** — the
  explicit, auditable counterpart: drives `pandas` / `statsmodels` /
  `linearmodels` / `pyfixest` / `rdrobust` / `econml` / `causalml` directly, every
  line swappable. For teaching, referee-level audit, and strict replication.
- **[00.2 Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)** — the
  community-standard `.do` chain (`reghdfe`, `ivreg2`, `csdid`, `did_imputation`,
  `sdid`, `rdrobust`, `synth`, `psmatch2`, `boottest`, `esttab`, …); one
  `ssc install` block installs 30+ packages. The choice when a referee or
  co-author insists on Stata.
- **[00.3 R](skills/00.3-Full-empirical-analysis-skill_R/)** — modern tidyverse +
  `fixest` + `Quarto`: the full pipeline in a single `.qmd` rendered to
  PDF/HTML/Word in one command. The Quarto reproducibility report is unique to
  this edition.

## 2026-04-13 — Original Chinese de-AIGC skill

- **[chinese-de-aigc](skills/48-de-AIGC-skills/)** — CoPaper.AI's
  original Chinese academic de-AIGC skill, targeting CNKI AMLC / Wanfang / VIP /
  Turnitin-Chinese detectors. 17-pattern Chinese-tell library, 5-step
  locate→diagnose→rewrite→self-score→review loop, per-section strategy, 5-dim
  scoring rubric. Currently the only GitHub skill dedicated to Chinese academic
  de-AIGC.

## 2026-04-12 — StatsPAI package + anti-AIGC detection skills

- **[StatsPAI](https://github.com/brycewang-stanford/StatsPAI)** introduced as
  the agent-native causal-inference & econometrics Python package (390+ functions
  at the time, since grown to 900+). MIT, JOSS.
- Added the English anti-AIGC skill set: `humanizer_academic` (44),
  `skill-deslop` (45), `stop-slop` (46), `avoid-ai-writing` (47), plus the
  community `ai-revision-guard` contribution.

## 2026-04-11 — Expanded to 119 repos / 23,000+ skills

- Grew from 43 curated collections to a map of **119 GitHub repositories /
  23,000+ skills** across eight social-science disciplines.
- Added finance, law, marketing, product-management, education, and public-health
  skill suites; 13 academic-data MCP servers; 11 multi-agent collaboration
  systems; and the bilingual Chinese/English README.
