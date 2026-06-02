# Changelog

This is the project's narrative changelog. `README.md` keeps only a short
"Recent highlights" list and links here for the full history.

## Unreleased

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

- **[chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/)** — CoPaper.AI's
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
