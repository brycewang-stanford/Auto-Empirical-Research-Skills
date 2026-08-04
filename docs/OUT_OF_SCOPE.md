<!-- Catalog-side companion to SKILL_HYGIENE.md / SCOREBOARD.md / RIGOR_COVERAGE.md.
Source of truth: this file is hand-curated. Do NOT add out-of-scope text to any
vendored SKILL.md — those are mirrors (auto-synced or manual vendor snapshots)
and must remain faithful to upstream. -->

# Out-of-scope: when *not* to use each AERS collection

Every skill collection has a **right place**. Knowing the wrong place is
often more useful for newcomers than a feature list. This page collects
**per-collection "do not use me for…"** notes.

Format: each entry names the collection, when it is *not* the right tool,
and a positive pointer to what *is* the right tool.

> **Maintenance rule.** This file is catalog-side metadata, not vendored
> skill content. It will not be overwritten by `make catalog` because it
> is hand-curated. When adding a new collection to `skills/`, please append
> a one-paragraph "Don't use for" entry here in the same PR.

---

## 00-StatsPAI (`00-Full-empirical-analysis-skill_StatsPAI`)

**Don't use for:** non-empirical prompts (creative writing, code review,
"explain X in plain English"). StatsPAI's value is the rigor layer;
outside empirical analysis the rigor layer is overhead, not signal.
**Don't use for:** batch ops on huge files (it's an LLM-facing
estimator driver, not a SQL engine).
**Use instead:** a plain chat model for non-empirical tasks; or
`00.1` / `00.2` / `00.3` if you want a classical-stack 8-step pipeline.

## 00.1 / 00.2 / 00.3 (Full Empirical · Python / Stata / R)

**Don't use for:** single-shot estimator calls ("is this IV first-stage F
above 10?"). These skills load an entire 8-step pipeline; using them for
one question is heavy and slow.
**Don't use for:** non-statsmodels / non-Stata / non-base-R ecosystems.
If the user is on `pymc-bart`, `bcf-py`, `causalml`, `dowhy`, `DoubleML`,
or `tidyverse` workflows, prefer `00-StatsPAI` (it wraps those) or the
domain-specific skill below.
**Use instead:** `00-StatsPAI` for fast 1-shot calls; the 00.x family
for classical-stack replications where you want to see each estimator
chosen by hand.

## 01-lishix520-academic-paper-skills

**Don't use for:** economics / AER-style empirical work. The collection
is organised around a different house style; using it on a top-5
economics submission will give you the wrong checklist.
**Don't use for:** primary-data work without its own identification
strategy (this collection assumes a narrative paper, not a design-driven
paper).
**Use instead:** `50-brycewang-aer-skills` for economics, or
`00-StatsPAI` / `67-econfin-workflow-toolkit` for end-to-end pipelines.

## 02-luwill-research-skills

**Don't use for:** anything other than the three areas the collection
organises around (medical-imaging review, paper-slide-deck generation,
research-proposal drafting). It is not a generic research copilot.
**Don't use for:** data-driven empirical estimation; the sub-skills are
narrative- and proposal-oriented.
**Use instead:** `00-StatsPAI` for causal/empirical work;
`65-game-theory-paper-writer` for theory slides; `50-aer-skills` for
AER-style proposals.

## 03 / 04 (K-Dense-AI scientific skills / writer)

**Don't use for:** top-5 economics submissions. The collection's house
style is the Nature / general-science register (hypothesis-generation,
literature review, scientific-writing), not the AER / QJE register.
**Don't use for:** design-driven empirical work that needs an
identification strategy — these are writing/research-design skills, not
estimators.
**Use instead:** `50-brycewang-aer-skills` for economics; `00-StatsPAI`
for empirical estimation.

## 05-kthorn-research-superpower

**Don't use for:** short factual queries or single-estimator checks —
this is a "research superpower" / multi-day project kit, not a chat
shortcut.
**Don't use for:** top-5 economics compliance (no AER-specific reviewer
loop).
**Use instead:** `00-StatsPAI` for ad-hoc empirics; `50-aer-skills` for
top-5 journal workflow.

## 06-fuhaoda-stats-paper-writing

**Don't use for:** ML causal inference (BCF, causal forest, meta-learners).
The collection is built around classical stats paper writing.
**Don't use for:** Chinese-language academic writing (it is English-only
by default).
**Use instead:** `00-StatsPAI` for ML causal; `48` / `49` for Chinese
de-AIGC rewrites.

## 07-Orchestra-Research-AI-Research-SKILLs

**Don't use for:** single-call analysis. This is an "orchestra" of
plotting + ML-paper-writing sub-skills, useful when you want a coordinated
multi-stage plot/draft routine.
**Don't use for:** econometric identification / AER / QJE workflow.
**Use instead:** `00-StatsPAI` for ad-hoc calls; `50-aer-skills` for
journal workflow.

## 08-ndpvt-web-latex-document-skill

**Don't use for:** empirical content generation. This is a
LaTeX/Document-style skill (web LaTeX rendering, document layout).
**Don't use for:** prose review or AER-style compliance.
**Use instead:** `38-peternka-academic-proofreader` for prose; keep
empirics in `00-StatsPAI` / `50-aer-skills`.

## 09-meleantonio-awesome-econ-ai-stuff

**Don't use for:** ad-hoc empirical estimation. This is a curated
index/collection of economic-AI tools and references, not a runnable
estimator.
**Use instead:** `00-StatsPAI` for estimation; this collection for
browsing what's out there.

## 10-Jill0099-causal-inference-mixtape

**Don't use for:** publication-ready reporting tables or AER-style
robustness gauntlets — it provides code templates only, not Table-1 / M1-M6
progression.
**Don't use for:** ML causal inference (no DML, BCF, causal forest).
**Use instead:** `00-StatsPAI` for ML causal and full reporting;
`40-py-econometrics-pyfixest` for high-D FE estimation.

## 11-James-Traina-compound-science

**Don't use for:** any single empirical task. This is a meta-orchestration
collection that composes agents and skills — useful for *building* a
workflow, not for running one.
**Don't use for:** causal inference without a design plan.
**Use instead:** `00-StatsPAI` for running empirical work.

## 12-pedrohcgs-claude-code-my-workflow

**Don't use for:** empirical work. This collection is the author's
personal Claude Code configuration (dot-claude, agents, hooks); use it
to learn how they wire a coding assistant, not to do statistics.
**Use instead:** `00-StatsPAI` for empirical work.

## 13-scunning1975-MixtapeTools

**Don't use for:** anything other than Cunningham's Mixtape codebase
recipes. It mirrors `10-Jill0099-causal-inference-mixtape` with different
layout; pick one, not both.
**Don't use for:** ML causal inference or AER compliance.
**Use instead:** `10` if you want a curated skill front-end;
`00-StatsPAI` for ML or full reporting.

## 14-luischanci-claude-code-research-starter

**Don't use for:** substantive empirical analysis. This is a
research-starter scaffold for new Claude Code projects (commands,
agents, project layout).
**Use instead:** `00-StatsPAI` for analysis; this skill for project
setup.

## 15-Felpix-Studios-social-science-research

**Don't use for:** econometrics / AER workflow. Social-science-research
house style differs from AER / QJE.
**Don't use for:** ML causal inference.
**Use instead:** `50-brycewang-aer-skills` for economics; `00-StatsPAI`
for ML causal.

## 16-hsantanna88-clo-author

**Don't use for:** econometrics. The collection is organised around a
specific author's writing style / opinion-piece cadence.
**Use instead:** `00-StatsPAI` for empirics; `50-aer-skills` for
AER-grade writing.

## 17-DAAF-Contribution-Community-daaf

**Don't use for:** anything that needs to *do* economic work. DAAF is a
guardrail / agent-safety framework; it has no empirical methods of its
own.
**Use instead:** DAAF as a *meta-layer* on top of `00-StatsPAI` /
`50-aer-skills`, not instead of them.

## 18-jusi-aalto-stata-accounting-research

**Don't use for:** non-Stata work. The collection is Stata-specific
accounting research templates.
**Don't use for:** ML causal inference or non-accounting applications.
**Use instead:** `32-dylantmoore-stata-skill` for general Stata;
`64-tmonk-mcp-stata` for Stata MCP; `00-StatsPAI` for cross-stack.

## 19-CuellarC05-vera-economic-intelligence

**Don't use for:** causal inference / identification-driven empirical work.
Vera is an economic-intelligence / forecasting-style assistant; the
collection is more about macro/market intelligence than identification.
**Don't use for:** top-5 economics submissions.
**Use instead:** `00-StatsPAI` for causal inference; `50-aer-skills`
for journal work.

## 20-wenddymacro-python-econ-skill

**Don't use for:** causal inference. The collection is focused on
macroeconomic Python workflows (time series, DSGE-style scripting), not
micro/identification.
**Don't use for:** STATA / R work.
**Use instead:** `00-StatsPAI` for micro causal; `00.1` for general
empirical Python; `00.3` for R macro.

## 21-claesbackman-AI-research-feedback

**Don't use for:** empirical estimation. This is feedback-quality /
review-quality tooling, not a causal toolkit.
**Use instead:** `00-StatsPAI` for estimation; `38-peternka-academic-proofreader`
for prose; `50-aer-skills` for AER referee simulation.

## 22-christopherkenny-skills

**Don't use for:** new empirical analysis — the collection is a
snapshot of a personal skill set, not a generalisable pipeline.
**Use instead:** `00-StatsPAI` for fresh empirical work; this collection
for reference patterns only.

## 23-Learning-Bayesian-Statistics-baygent-skills

**Don't use for:** frequentist causal identification (DiD / IV / RD).
The collection is Bayesian workflow oriented.
**Don't use for:** AER-style reporting.
**Use instead:** `00-StatsPAI` for frequentist causal; `00-StatsPAI`
Bayesian modes for posterior-based workflows.

## 24-Imbad0202-academic-research-skills

**Don't use for:** data-driven empirical estimation. The collection is
academic-paper drafting / review oriented.
**Don't use for:** econometric identification.
**Use instead:** `00-StatsPAI` for empirics; `50-aer-skills` for
AER-style papers.

## 25-HosungYou-Diverga

**Don't use for:** empirical causal estimation. The collection appears
to be a workflow / agent-orchestration harness.
**Use instead:** `00-StatsPAI` for estimation; `50-aer-skills` for
paper-writing orchestration.

## 26-Data-Wise-scholar

**Don't use for:** end-to-end empirical analysis. Scholar-style
collection, oriented toward literature navigation and study synthesis
rather than primary-data identification.
**Use instead:** `00-StatsPAI` for primary-data work; `36-taoyunudt-literature-review-skill`
or `52-keemanxp-slr-prisma` for systematic reviews.

## 27-dariia-m-my_claude_skills

**Don't use for:** causal inference with full AER-style robustness.
The collection is a personal skill bundle covering abstract /
event-studies / verification / etc.; pick sub-skills, don't treat it as
one monolithic skill.
**Don't use for:** ML causal inference.
**Use instead:** `00-StatsPAI` for the empirical bits; `38` for
proofreading.

## 28-maxwell2732-paper-replicate-agent-demo

**Don't use for:** new analysis. This is a *demo* of a replication
agent, not a generalisable workflow.
**Use instead:** `50-brycewang-aer-skills` for actual paper replication
support.

## 29-quarcs-lab-project20XXy

**Don't use for:** anything other than its own project conventions.
`20XXy` is a year-of-degree placeholder; the collection is a project
scaffold.
**Use instead:** `50-aer-skills` or `00-StatsPAI`.

## 30-zirui-song-claude-skills

**Don't use for:** empirical estimation. This is a meta-collection of
project-level Claude skill scaffolds (literature review, robustness,
referee response). Use individual sub-skills if useful.
**Use instead:** `00-StatsPAI` for estimation; `50-aer-skills` for
AER referee response.

## 31-thalysandratos-claude-code-skills

**Don't use for:** empirical work. The collection is general Claude
Code workflow utilities, not statistics.
**Use instead:** `00-StatsPAI`.

## 32-dylantmoore-stata-skill

**Don't use for:** non-Stata work. Single-stack Stata workflow only.
**Don't use for:** ML causal inference.
**Use instead:** `64-tmonk-mcp-stata` for an MCP-style Stata experience;
`00-StatsPAI` for ML causal; `18-jusi-aalto-stata-accounting-research`
for accounting-specific Stata.

## 33-Galaxy-Dawn-claude-scholar

**Don't use for:** empirical analysis. Scholar-style collection,
literature / reading oriented.
**Use instead:** `00-StatsPAI` for primary-data work; `26` or `36`
for literature synthesis.

## 34-andrehuang-research-companion

**Don't use for:** causal inference / estimation. The collection is a
research-companion workflow (planning, reading), not an estimator.
**Use instead:** `00-StatsPAI` for estimation.

## 35-bahayonghang-academic-writing-skills

**Don't use for:** data-driven empirical work. Academic-writing /
prose-oriented.
**Use instead:** `00-StatsPAI` for empirics; `50-aer-skills` for
AER-style writing; `38` for proofreading.

## 36-taoyunudt-literature-review-skill

**Don't use for:** primary-data empirical work (no data, no
identification). Literature-review only.
**Don't use for:** systematic-review reporting — see `52-keemanxp-slr-prisma`
for PRISMA-compliant workflow.
**Use instead:** pair with a data source + an identification-design skill
(e.g. `00-StatsPAI`'s card-style IV writeup).

## 37-IlanStrauss-ai-skills

**Don't use for:** empirical causal inference. The collection is
general AI workflow / agent scaffolding, not empirical.
**Use instead:** `00-StatsPAI`.

## 38-peternka-academic-proofreader

**Don't use for:** empirical estimation. Proofreader only — language,
clarity, structure.
**Don't use for:** Chinese prose (English-tuned).
**Use instead:** `00-StatsPAI` for empirics; `48` / `49` for Chinese
de-AIGC.

## 39-vincentarelbundock-marginaleffects

**Don't use for:** non-R work. R-only package skill for marginal-effects
computation.
**Don't use for:** identification strategy choice.
**Use instead:** `00.3` for general R; `00-StatsPAI` for cross-stack;
use this when you already have an R model and want `marginaleffects`-style
contrasts / marginal-effects.

## 40-py-econometrics-pyfixest

**Don't use for:** non-pyfixest estimators. This is the pyfixest
package reference — two-way FE, IV with FE, Poisson with FE.
**Don't use for:** ML causal inference (no DML / BCF / causal forest).
**Use instead:** `00-StatsPAI` for ML causal or other stacks;
`00.1` for classical Python; this for pyfixest specifically.

## 41-sticerd-eee-sewage-econometrics-check

**Don't use for:** anything other than STICERD EEE / sewage-economics
type applications. The collection is narrow by design.
**Don't use for:** general DiD/IV/RD on other topics.
**Use instead:** `00-StatsPAI` for general causal work.

## 42-wanshuiyin-ARIS

**Don't use for:** general empirical analysis. ARIS is a specific
agent-pipeline framework; use individual sub-skills if relevant.
**Use instead:** `00-StatsPAI` for ad-hoc estimation; this collection
for the ARIS pipeline shape specifically.

## 43-wentorai-research-plugins

**Don't use for:** production paper pipelines (it's a meta-collection
of ad-hoc community plugins). Use `00-StatsPAI` or `50-aer-skills`
for any result that goes into a submission.
**Use instead:** browse individual plugins from 43 as inspiration, not
as end-to-end tools. The collection's value is breadth, not depth.

## 44-matsuikentaro1-humanizer_academic

**Don't use for:** empirical work or causal inference. This is a
"humanize" rewrite skill.
**Don't use for:** Chinese prose (English-tuned detectors / rewrites).
**Use instead:** `48` / `49` for Chinese; `45` / `46` / `47` for English.

## 45-stephenturner-skill-deslop

**Don't use for:** empirical estimation. English de-AIGC / de-slop
rewrite.
**Don't use for:** Chinese prose.
**Use instead:** `44` / `46` / `47` for English humanization;
`48` / `49` for Chinese.

## 46-hardikpandya-stop-slop

**Don't use for:** empirical estimation. English de-AIGC rewrite.
**Don't use for:** Chinese prose.
**Use instead:** `44` / `45` / `47` for English; `48` / `49` for Chinese.

## 47-conorbronsdon-avoid-ai-writing

**Don't use for:** empirical estimation. English de-AIGC rewrite.
**Don't use for:** Chinese prose.
**Use instead:** `44` / `45` / `46` for English; `48` / `49` for Chinese.

## 48-de-AIGC-skills

**Don't use for:** non-academic prose (blogs, marketing copy, fiction) —
the pattern libraries and section strategies assume an empirical-paper
skeleton, in English or Chinese.
**Don't use for:** empirical estimation.
**Don't use for:** laundering fully AI-generated papers past detectors;
the skill flags unsupported claims instead of hiding them.
**Use instead:** `46-hardikpandya-stop-slop` / `45-stephenturner-skill-deslop`
for general English prose; `49-voidborne-d-humanize-chinese` for general
Chinese prose outside the academic register.

## 49-voidborne-d-humanize-chinese

**Don't use for:** English prose. Chinese-only humanizer; running
English through it is a waste.
**Don't use for:** empirical estimation.
**Use instead:** `47` / `46` / `45` for English; `48-de-AIGC-skills`
for a different Chinese humanizer.

## 50-brycewang-aer-skills (AER pipeline)

**Don't use for:** non-economics empirical work. The pipeline's house
style is AER / QJE / JPE / AEJ; using it for an epidemiology paper will
give you the wrong review checklist.
**Don't use for:** tasks that don't have a real dataset. AER pipeline
assumes a Table 1 / Table 2 / event-study / robustness gauntlet exists;
if you don't have results, you don't have a paper.
**Don't use for:** fast ad-hoc estimator checks (use `00-StatsPAI`
1-shot).
**Use instead:** `00-StatsPAI`'s epidemiology mode for public-health
(STROBE / TRIPOD reporting, TMLE triplet, KM/AFT survival);
`00-StatsPAI` for ad-hoc empirics.

## 51-pymc-labs-CausalPy

**Don't use for:** non-Bayesian analysis. CausalPy is the Python
`CausalImpact`-style Bayesian structural time-series library.
**Don't use for:** staggered-adoption DiD, panel FE, or AER-style
robustness gauntlets.
**Use instead:** `00-StatsPAI` Bayesian modes for non-time-series
causal inference; `00-StatsPAI` `causal_impact` for BSTS-style time
series.

## 52-keemanxp-slr-prisma

**Don't use for:** primary-data empirical work (no data, no
identification). PRISMA systematic review workflow.
**Don't use for:** narrative / scoping reviews — PRISMA imposes a
specific protocol.
**Use instead:** `36-taoyunudt-literature-review-skill` for narrative
reviews; pair with a data source + identification-design skill for
empirical follow-up.

## 53-keemanxp-thematic-analysis-skill

**Don't use for:** quantitative empirical work. Thematic / qualitative
analysis only.
**Don't use for:** AER / QJE submissions (different genre).
**Use instead:** `52` for systematic-review reporting;
`00-StatsPAI` for quantitative analysis.

## 54-scdenney-open-science-skills

**Don't use for:** empirical causal estimation. Open-science practices
(pre-registration, data sharing, reproducibility checklists) only.
**Don't use for:** primary-data analysis itself.
**Use instead:** `00-StatsPAI` for analysis; pair `54` with that for
proper pre-reg / sharing artefacts.

## 55-ab604-claude-code-r-skills

**Don't use for:** non-R work. R workflow scaffolding only.
**Don't use for:** causal inference design choice.
**Use instead:** `00.3` for full empirical R; `39` for marginal-effects;
`00-StatsPAI` for cross-stack.

## 56-hanlulong-econ-writing-skill

**Don't use for:** non-economics academic writing or causal inference.
This is a Chinese-language economics writing helper.
**Don't use for:** English-only top-5 journals (use `50-aer-skills`
which is English-first and AER-tuned).
**Use instead:** `50-aer-skills` for English AER; `48` / `49` for
Chinese humanization.

## 57-dgunning-edgartools

**Don't use for:** empirical causal inference. EDGAR is a US public-company
filings toolkit; useful for data acquisition, not estimation.
**Use instead:** `00-StatsPAI` for estimation; `57` for EDGAR
data pulls (regime: financial / regulatory text data).

## 58-charlescoverdale-econstack

**Don't use for:** empirical causal inference. Econstack is a structured
econ-memo / briefing pipeline (longlist, cost-benefit, fiscal-briefing),
not an estimator.
**Don't use for:** academic paper writing.
**Use instead:** `00-StatsPAI` for causal inference; `50-aer-skills`
for academic; `58` for policy-briefing memo outputs.

## 59-shiquda-openalex-skill

**Don't use for:** causal estimation. OpenAlex is a literature
metadata API wrapper; useful for citation / corpus pulls, not for
running regressions.
**Use instead:** `00-StatsPAI` for estimation; `59` for literature
search / citation-context mining.

## 60-regisely-superpapers

**Don't use for:** end-to-end empirical work that requires identification.
Superpapers appears to be a writing/formatting/wrapper layer over other
skills.
**Don't use for:** causal inference design choice.
**Use instead:** `00-StatsPAI` for estimation; `50-aer-skills` for
AER-style writing.

## 61-phdemotions-research-methods

**Don't use for:** primary-data empirical analysis. Research-methods
guidance (e.g. exam prep, dissertation-method training), not an
estimator.
**Use instead:** `00-StatsPAI` for primary-data work;
`50-aer-skills` for the applied paper.

## 62-PHY041-claude-skill-citation-checker

**Don't use for:** causal estimation or empirical analysis. Citation /
reference-quality checker only.
**Don't use for:** Chinese-only papers (English-tuned? verify).
**Use instead:** `00-StatsPAI` for estimation; `62` for reference
validation in a paper-writing pipeline.

## 63-tondevrel-scientific-agent-skills

**Don't use for:** micro-econometric identification. The collection
appears oriented toward data-science / ML / survival tooling
(`dowhy`, `lifelines`).
**Don't use for:** AER-style staggered DiD / IV.
**Use instead:** `00-StatsPAI` for micro causal; use `63` for the
dowhy / lifelines parts if those are what you need.

## 64-tmonk-mcp-stata

**Don't use for:** non-Stata work. Single-stack Stata MCP integration.
**Don't use for:** ML causal inference.
**Use instead:** `00-StatsPAI` for ML causal; `32` / `18` for other
Stata workflows.

## 65-game-theory-paper-writer

**Don't use for:** empirical causal inference (no data, no
identification). Theory-paper writing only.
**Use instead:** `50-aer-skills` for applied empirical; `00-StatsPAI`
for empirics; this collection for game-theory / mechanism-design writeup.

## 66-zheng-siyao-empirical-research-skills

**Don't use for:** non-R econometric work (R-focused collection of
sub-skills: did-reviewer, econ-reviewer, latex-table, codebook-pass, etc.).
**Don't use for:** ML causal inference.
**Use instead:** `00-StatsPAI` for ML causal; `00.3` for general
R; this collection for codebook / LaTeX-table polish within R.

## 67-econfin-workflow-toolkit

**Don't use for:** AER / QJE-specific compliance (no AER house style,
no 100-word abstract constraint, no referee simulator tuned to AER).
**Don't use for:** ML causal inference (no BCF / causal forest / DML
in the toolkit's core).
**Use instead:** `50-brycewang-aer-skills` for top-5 economics;
`00-StatsPAI` for ML causal.

## 68-research-productivity-skills

**Don't use for:** empirical causal inference. Productivity-style
collection (literature-survey, slides, docx export, etc.); no
estimator layer.
**Don't use for:** AER compliance.
**Use instead:** `00-StatsPAI` for estimation; `50-aer-skills` for
AER workflow; `68` for slide / docx / literature-survey utilities.

## 69-Paper-WorkFlow

**Don't use for:** empirical causal estimation. Paper-WorkFlow is the
defensive-workflow + paper-build pipeline for this repo (CLAUDE.md +
README + CITATION + scripts); it is repository maintenance, not
estimation.
**Use instead:** `50-aer-skills` for the actual paper workflow;
`69` for the repo's own build-notebook / build-PPTX utilities.

---

## General rule of thumb

- **StatsPAI (00)** when in doubt. It is the *single* entry point that
  picks the right tool and is honest about its limits. It also wraps
  `pymc-bart`, `bcf-py`, `causalml`, `dowhy`, `DoubleML`, `tidyverse`,
  etc.
- **AER-skills (50)** when the user is targeting a top-5 economics
  journal specifically (AER / QJE / JPE / AEJ).
- **Anything with "DAAF" / "humanize" / "de-AIGC" / "stop-slop" /
  "deslop" in the name** is a *quality* / *safety* layer; it does not
  produce empirical results on its own.
- **00.x family** when the user wants the classical statsmodels /
  Stata / base-R stack by hand, and is willing to see each estimator
  chosen step-by-step.
- **For Chinese humanization**: use `48` or `49`. For English: use
  `44`, `45`, `46`, or `47`.
- **For literature review / PRISMA / thematic analysis**: pair a
  review skill with `00-StatsPAI` if you also need empirical
  follow-up.

---

## How this file is maintained

This file is **catalog-side** metadata, not vendored skill content. It
will not be overwritten by `make catalog` because it is hand-curated.
If a new collection is added, please append a one-paragraph "Don't use"
entry here in the same PR. Vendored `SKILL.md` / `README-original.md`
inside `skills/<NN>-<name>/` must remain faithful to upstream; do not
add out-of-scope text to those files.

Cross-references:
- Right-place routing: [`CHOOSING_A_SKILL.md`](CHOOSING_A_SKILL.md)
- Quality / trust signals: [`SCOREBOARD.md`](SCOREBOARD.md)
- Method-coverage: [`RIGOR_COVERAGE.md`](RIGOR_COVERAGE.md)
- Hygiene rules: [`SKILL_HYGIENE.md`](SKILL_HYGIENE.md)