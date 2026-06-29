# AER-Skills

<p align="center">
  <img src="assets/aer-cover.jpg" alt="The American Economic Review — cover" width="220">
</p>
<p align="center"><em>An agent skill stack for targeting the <a href="https://www.aeaweb.org/journals/aer">American Economic Review</a>, <em>AER: Insights</em>, and the AEJ family.</em></p>

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Top-5 focused](https://img.shields.io/badge/focus-AER%20%2F%20AER%3AInsights%20%2F%20AEJ-1f6feb)](docs/workflow-map.md)
[![Workflow](https://img.shields.io/badge/workflow-identification--driven-blue)](docs/design-principles.md)
[![Claude Code](https://img.shields.io/badge/agent-Claude%20Code-cc785c)](docs/installation-claude.md)
[![Codex](https://img.shields.io/badge/agent-Codex-0a7ea4)](docs/installation-codex.md)

[简体中文](README.md) | English

Agent skills for **selecting, positioning, writing, identifying, formatting, internally refereeing, submitting, and revising** manuscripts targeted at the *American Economic Review* (AER), *AER: Insights*, and the *AEJ* family.

This repository is opinionated. It is **not** a generic economics writing toolbox. It is a **top-5 economics skill stack** for: identification-first empirics, AEA-policy-compliant replication packages, Keith-Head-style introductions, AER-style booktabs tables, and editor-efficient rebuttals.

## Recent Upgrades

v1.1 expands AER-Skills from ten core skills to fourteen, and turns the fragile late-stage checks after "the draft is done" into explicit quality gates:

- New `aer-literature`: closest-papers mapping and citation verification before literature claims enter the manuscript.
- New `aer-paper-body`: background, data, empirical strategy, results, mechanisms, and conclusion writing, with the body drafted before the introduction.
- New `aer-consistency`: audit numbers, tables, sample funnels, unit conversions, cross-references, and the bibliography; ships a runnable LaTeX audit script.
- New `aer-referee-sim`: pre-submission desk screen plus three adversarial referee reports, scored with a rubric and converted into a revise list.
- New supporting resources: `docs/style-guide.md`, `docs/referee-report-rubric.md`, `examples/results-section-example.md`, and `examples/referee-report-example.md`.

---

## Why a Separate AER Skill Stack?

Top-5 economics journals impose constraints that do not exist in life-science venues:

| Constraint                       | AER                | AER: Insights       | Implication                                          |
|----------------------------------|--------------------|---------------------|------------------------------------------------------|
| Abstract length                  | **100 words**      | 100 words           | 4-5 sentences. Sell results, not motivation.         |
| Main text length                 | ~40 typeset pages  | **≤ 7,000 words minus 200 per exhibit** | Tight prose; five exhibits leave 6,000 words.        |
| Desk rejection                   | High               | **~45%**            | First 3 pages decide the verdict.                    |
| Replication                      | Mandatory          | Mandatory           | AEA Data and Code Availability Policy is enforced.   |
| Identification                   | Causal, design-based| Causal, design-based | TWFE, weak IV, and naive RDD get desk-rejected.     |
| Cover letter                     | Optional           | Optional            | Use only for COI disclosure or data access limits.   |
| Disclosure statements            | Required           | Required            | One separate PDF per coauthor, even with no conflicts. |

Generic "scientific writing" skills (e.g. [Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills), [nature-skills](https://github.com/Yuan1z0825/nature-skills)) miss these constraints.

---

## Quick Start

### Option A — Claude Code Plugin (recommended)

```bash
# Add the marketplace (one-time)
/plugin marketplace add https://github.com/brycewang-stanford/AER-Skills

# Install the plugin
/plugin install aer-skills

# Reload
/reload-plugins
```

All fourteen skills are then available automatically.

### Option B — Scripted Install

```bash
git clone https://github.com/brycewang-stanford/AER-Skills.git
cd AER-Skills

# Claude Code (user-scoped)
python3 scripts/install_skills.py claude

# Or Codex
python3 scripts/install_skills.py codex
```

The installer copies the full skill directories. Use `--replace` when updating
an existing install, and `--dry-run` to inspect planned copies first. Keep the
cloned repository available if you want the `templates/` and `examples/`
resources referenced by the skills.

### First Prompt

After restarting your agent:

```text
Use aer-workflow to tell me which skill I should use next for this manuscript.
```

For longer install instructions see [docs/installation-claude.md](docs/installation-claude.md) and [docs/installation-codex.md](docs/installation-codex.md).

---

## Default Workflow

```text
aer-topic-selection
    -> aer-literature
        -> aer-identification
            -> aer-robustness
                -> aer-paper-body
                    -> aer-introduction
                        -> aer-tables-figures
                            -> aer-consistency
                                -> aer-referee-sim   (loop until ≥ major R&R)
                                    -> aer-replication
                                        -> aer-submission
                                            -> aer-rebuttal
```

The default assumption is:

- **identification before writing** — if your design is fragile, no prose will save it
- **AER vs AER:Insights vs AEJ** is a *routing* decision made before the abstract is written
- **the body is written before the introduction** — the intro summarizes a paper, it does not promise one
- **no citation is written from memory** — every reference is verified against a fetched source
- **the manuscript must survive its own referees** — a consistency audit and an adversarial referee simulation gate the submission
- **replication package quality** is part of the paper, not an afterthought
- **rebuttal letters** are written against the *revised* manuscript, never against the old draft

See [docs/workflow-map.md](docs/workflow-map.md).

---

## Skills

### Core — Lifecycle

| Skill | Purpose |
|---|---|
| [`aer-workflow`](skills/aer-workflow/SKILL.md) | Routing map with quality gates. Tells you which skill to use next. |
| [`aer-topic-selection`](skills/aer-topic-selection/SKILL.md) | Top-5 bar test, novelty audit, AER vs Insights vs AEJ routing. |
| [`aer-literature`](skills/aer-literature/SKILL.md) | Closest-papers map, positioning moves, and the citation-integrity protocol — every reference verified, no hallucinated citations. |
| [`aer-identification`](skills/aer-identification/SKILL.md) | DiD (staggered), IV (weak-IV-robust), RDD, SCM, shift-share/Bartik. |
| [`aer-robustness`](skills/aer-robustness/SKILL.md) | Robustness, heterogeneity, mechanism, placebo. Referee-anticipating. |
| [`aer-paper-body`](skills/aer-paper-body/SKILL.md) | Body sections — background, data, empirical strategy, finding-first results narration, magnitude interpretation, mechanisms, conclusion. |
| [`aer-introduction`](skills/aer-introduction/SKILL.md) | Keith Head five-paragraph formula + 100-word abstract drafting. |
| [`aer-tables-figures`](skills/aer-tables-figures/SKILL.md) | AER booktabs style, `etable`/`estout`/`modelsummary`, figure notes. |
| [`aer-consistency`](skills/aer-consistency/SKILL.md) | Full-manuscript integrity audit — numbers vs tables, sample funnels, log-point conversions, cross-references, citation two-way match. Ships a runnable LaTeX audit script. |
| [`aer-referee-sim`](skills/aer-referee-sim/SKILL.md) | Adversarial internal review — desk screen plus three calibrated referee reports, scored against the editorial rubric; loop until ≥ major R&R. |
| [`aer-replication`](skills/aer-replication/SKILL.md) | AEA Data and Code Availability Policy, README, openICPSR. |
| [`aer-submission`](skills/aer-submission/SKILL.md) | Format preflight, cover letter, length audit, conflict declaration. |
| [`aer-rebuttal`](skills/aer-rebuttal/SKILL.md) | R&R response letter, triage, concede / clarify / push-back rules. |

### Optional — Implementation Engine

A second way to *run* the empirics, alongside the hand-written templates below.

| Skill | Purpose |
|---|---|
| [`aer-statspai`](skills/aer-statspai/SKILL.md) | Run the analysis with [StatsPAI](https://github.com/brycewang-stanford/StatsPAI) — an agent-native unified Python engine + MCP server covering DiD / IV / RDD / SCM / DML, `audit_result` robustness, honest-DiD / Oster sensitivity, and `to_latex` / `to_docx` table export. Executes the design; `aer-identification` still chooses it. |

---

## Code Templates

Drop-in, version-conscious scripts for three common empirical economics stacks. Each
template includes a master script, a Callaway-Sant'Anna DiD example, an
AER-style booktabs regression table, and a README.

| Language | Stack | Path |
|---|---|---|
| Stata | `reghdfe`, `csdid`, `estout`, `bacondecomp`, `honestdid` | [`templates/stata/`](templates/stata/) |
| R | `fixest`, `did`, `HonestDiD`, `modelsummary`, `fwildclusterboot` | [`templates/r/`](templates/r/) |
| Python | `pyfixest`, `differences`, `linearmodels`, `statsmodels`, `rdrobust`, `rddensity` | [`templates/python/`](templates/python/) |

Each template enforces: fixed seed (`20260101`), relative paths, package
version documentation or exact pins where the stack supports them, AER booktabs
table style, and vector-format figures.

Scaffold a project without manually copying files:

```bash
python3 scripts/scaffold_project.py stata /path/to/new-project
python3 scripts/scaffold_project.py r /path/to/new-project
python3 scripts/scaffold_project.py python /path/to/new-project
python3 scripts/scaffold_project.py skeleton /path/to/new-replication-package

# or via Make
make scaffold-stata DEST=/path/to/new-project
```

Use `--dry-run` to inspect planned copies. The scaffolder refuses protected
destinations such as repository-internal paths and bundled template source
trees; create paper projects outside this repository.

## Validation

Run the repository checks before copying skills into an agent profile or opening
a PR:

```bash
make preflight
# equivalent: python3 scripts/validate_repo.py
```

`make preflight` also runs staged and unstaged `git diff --check` for
whitespace and patch hygiene.
The validator checks skill frontmatter, skill directory shape, agent metadata,
plugin manifests, local Markdown links, template layout, exact Python
dependency pins and import coverage, installer and scaffolder behavior,
generated/cache file exclusions, and Python/R/Stata template syntax. R syntax checks are skipped
with a warning when `Rscript` is unavailable. CI installs R, runs
`make preflight`, then runs `make validate-strict`, which fails instead of
skipping optional-tool checks.

Runnable example Monte Carlo assertions are the optional second-layer gate.
After installing the dependencies in `templates/python/requirements.txt` (and
the R packages when needed), run:

```bash
make smoke-examples
# or: python3 scripts/run_example_smoke.py --strict-deps
```

The default mode skips demos whose optional dependencies are missing. Use
`--strict-deps` before release so any missing dependency or failed assertion
returns a non-zero status.

`make preflight` also runs the citation-integrity gate
(`verify_citations.py --selftest`): a hermetic, gold-set check that
`references.bib` still matches the Crossref/OpenAlex metadata it was verified
against — turning *"no citation from memory"* from a principle into a
re-runnable test. Verify against the live indexes with
`make verify-citations-online`, and check a draft's `\cite` ↔ bib
correspondence with `--manuscript`. See the
[citation-integrity protocol](docs/citation-integrity-protocol.md).

---

## Examples

Worked examples grounded in classic AER and adjacent-top-5 papers.
See the full examples index in [examples/README.md](examples/README.md).

| File | What it shows |
|---|---|
| [`examples/aer-exemplars.md`](examples/aer-exemplars.md) | Classic papers (Card-Krueger, AJR, ADH, Dell, Chetty-Hendren, Abadie, BDGK, Karlan-List …) mapped to each skill, with openICPSR / Dataverse links |
| [`examples/modern-aer-exemplars.md`](examples/modern-aer-exemplars.md) | **30+ recent (2018-2025) papers organized by 13 subfields** — Labor, Public, Development, Trade, Macro, IO, Health, Environment, Urban, Education, Finance, Political Economy, Social Networks — plus the modern identification-methods toolkit. Each with deposit link |
| [`examples/intro-example.md`](examples/intro-example.md) | Full Keith Head five-paragraph introduction + 97-word abstract, with a counterexample of what not to write |
| [`examples/results-section-example.md`](examples/results-section-example.md) | Worked body-section narration for the same fictional paper — sample funnel, finding-first results paragraphs, magnitude conversions, back-of-envelope calculation, mechanisms by channel, plus a table-walk-through counterexample |
| [`examples/rebuttal-example.md`](examples/rebuttal-example.md) | Complete R&R response: cover letter + editor + 3 referees, demonstrating concede / clarify / push-back / decline outcomes |
| [`examples/referee-report-example.md`](examples/referee-report-example.md) | Full internal referee simulation — desk screen, three adversarial reports, rubric-scored synthesis, routed revise list — catching before submission the issues that cost the fictional authors an R&R round |
| [`examples/replication-package-skeleton/`](examples/replication-package-skeleton/) | Deposit-ready directory layout with AEA-compliant README template, master script, and globals file — drop-in starting point for an openICPSR submission |
| [`examples/staggered-did-demo/`](examples/staggered-did-demo/) | Runnable Python/R simulation showing why naive TWFE fails under staggered adoption |
| [`examples/iv-weak-instrument-demo/`](examples/iv-weak-instrument-demo/) | Runnable Python simulation contrasting conventional 2SLS inference with Anderson-Rubin inference |
| [`examples/rdd-polynomial-demo/`](examples/rdd-polynomial-demo/) | Runnable Python simulation showing why high-order global-polynomial RDD is unsafe |
| [`examples/synthetic-control-demo/`](examples/synthetic-control-demo/) | Runnable Python simulation showing why synthetic-control inference comes from the placebo-in-space permutation distribution, not visual pre-period fit |
| [`examples/shift-share-demo/`](examples/shift-share-demo/) | Runnable Python simulation showing why shift-share/Bartik inference belongs at the shock (industry) level, not the region level — region-clustered SEs over-reject |
| [`examples/few-clusters-demo/`](examples/few-clusters-demo/) | Runnable Python simulation showing why a cluster-robust t-test over-rejects with few clusters and the wild cluster bootstrap restores nominal size |
| [`examples/multiple-testing-demo/`](examples/multiple-testing-demo/) | Runnable Python simulation showing why testing many outcomes inflates the family-wise error rate and how Bonferroni/Holm control it without killing power |

---

## Design Principles

- **Identification-driven, not narrative-driven.** Decide and stress-test the research design *before* writing prose.
- **One contribution per paper.** AER editors reject competent extensions; rewrite around a single sharpest claim.
- **Cross-subfield interest is a hard filter.** A labor paper must speak to public, macro, and IO economists or it desk-rejects.
- **Modern econometrics, not 1990s defaults.** TWFE → Callaway-Sant'Anna; first-stage F → Anderson-Rubin; naive RDD → covariate-adjusted local linear.
- **No citation from memory.** Every reference is verified against a fetched source; every attributed claim is checked against the paper's text.
- **The manuscript must survive its own referees.** A full consistency audit (`aer-consistency`) and an adversarial referee simulation (`aer-referee-sim`) gate every submission.
- **The replication package is part of the paper.** A README that does not run is grounds for AEA Data Editor delay.
- **Editor time is the scarcest resource.** Cover letter ≤ 200 words. Response letter quotes the comment, states the action, and cites the revised location.

See [docs/design-principles.md](docs/design-principles.md).

Key references:

- [Academic Research Skills reference review](docs/academic-research-skills-review.md) —
  what transferred from the external ARS repository and what stayed out
- [Desk-rejection audit](docs/desk-rejection-audit.md) — pre-submission no-go
  checks from an editor/referee perspective
- [Methods reference](docs/methods-reference.md) — estimator defaults,
  diagnostics, package calls, and BibTeX keys
- [Style guide](docs/style-guide.md) — sentence- and paragraph-level
  economics prose rules, plus the AI-pattern scrub
- [Referee report rubric](docs/referee-report-rubric.md) — anchored 0-5
  scoring dimensions and calibrated verdict mapping for `aer-referee-sim`
- [SkillOpt evaluation protocol](docs/skillopt-evaluation-protocol.md) —
  fixed scenarios and gates for skill optimization patches
- [PNAS Nexus publication plan](docs/pnas-nexus-publication-plan.md) —
  reviewer-style audit and one-week venue-compliance plan
- [PNAS Nexus submission checklist](docs/pnas-nexus-submission-checklist.md) —
  evidence-driven final preflight for manuscript, data, code, and figures
- [Source register](docs/source-register.md) — official AEA policy sources and
  repo surfaces that depend on them
- [Glossary](docs/glossary.md) — shared vocabulary for journal, identification,
  replication, and response-letter terms

---

## Repository Layout

```text
AER-Skills/
├── README.md               (Chinese, primary)
├── README.en.md            (English, full)
├── LICENSE                 (MIT)
├── Makefile                (validation and install shortcuts)
├── CONTRIBUTING.md         (concurrent-agent workflow)
├── .github/
│   └── workflows/ci.yml    (repository validation)
├── .claude-plugin/
│   ├── plugin.json         (plugin manifest)
│   └── marketplace.json    (Claude Code marketplace entry)
├── docs/
│   ├── academic-research-skills-review.md
│   ├── citation-integrity-protocol.md
│   ├── desk-rejection-audit.md
│   ├── design-principles.md
│   ├── glossary.md
│   ├── installation-claude.md
│   ├── installation-codex.md
│   ├── methods-reference.md
│   ├── pnas-nexus-publication-plan.md
│   ├── pnas-nexus-submission-checklist.md
│   ├── referee-report-rubric.md
│   ├── source-register.md
│   ├── style-guide.md
│   └── workflow-map.md
├── skills/                 (14 skill directories — SKILL.md + agents/openai.yaml)
│   ├── aer-workflow/
│   ├── aer-topic-selection/
│   ├── aer-literature/
│   ├── aer-identification/
│   ├── aer-robustness/
│   ├── aer-paper-body/
│   ├── aer-introduction/
│   ├── aer-tables-figures/
│   ├── aer-consistency/    (ships scripts/audit_manuscript.py)
│   ├── aer-referee-sim/
│   ├── aer-replication/
│   ├── aer-submission/
│   ├── aer-rebuttal/
│   └── aer-statspai/       (optional implementation engine)
├── templates/              (drop-in pipelines, all three languages)
│   ├── stata/
│   ├── r/
│   └── python/
├── scripts/
│   ├── install_skills.py
│   ├── run_skillopt_gate.py    (SkillOpt routing gate)
│   ├── scaffold_project.py
│   ├── skill_audit.py          (SkillOpt document-quality audit)
│   ├── validate_repo.py
│   ├── verify_citations.py     (citation-integrity verifier)
│   └── citation_gold/          (hermetic gold set + recorded index responses)
└── examples/
    ├── aer-exemplars.md
    ├── intro-example.md
    ├── rebuttal-example.md
    └── replication-package-skeleton/
        ├── data/codebook/source-register.md
        ├── docs/exhibit-register.md
        └── docs/claim-evidence-ledger.csv
```

---

## Scope

This repository is for:

- *American Economic Review* (full-length papers, ≤ 40 pages)
- *American Economic Review: Insights* (short-form, ≤ 7,000 words minus 200 per exhibit; ≤ 6,000 words with five exhibits)
- *American Economic Journal* family (Applied, Policy, Macro, Micro)
- Empirical and theoretical economics manuscripts
- Field experiments (with AEA RCT Registry workflow)

This repository is **not** trying to be:

- A finance-journal toolbox (JF, JFE, RFS have their own conventions)
- A theory-only stack (no proof-writing helpers)
- A generic "academic writing" library

---

## Acknowledgements

Skill architecture inspired by [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills) and [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills). Methodology distilled from public-domain advice by **Keith Head**, **Marc F. Bellemare**, **Susan Athey**, **Berk-Harvey-Hirshleifer**, the **AEA Data Editor's Office**, and the *Annual Review of Economics*.

---

## License

[MIT](LICENSE).
