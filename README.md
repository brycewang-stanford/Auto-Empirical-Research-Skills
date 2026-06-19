# Auto-Empirical Research Skills (AERS)

<div align="center">

**🌐 Language: English | [简体中文](README-zh-CN.md) | [繁體中文](README-zh-TW.md) | [日本語](README-ja.md) | [한국어](README-ko.md)**

<br/>

  <img src="images/aers-readme-cover-en.png" alt="Auto-Empirical Research Skills cover" width="100%" />

  <br/>

  <table>
    <tr>
      <td align="center">
        <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="260" /></a>
      </td>
      <td width="60"></td>
      <td align="center">
        <img src="images/stanford-reap-logo.png" alt="Stanford REAP - Center on China's Economy & Institutions" width="380" />
      </td>
    </tr>
  </table>

  <br/>

  <strong>Stanford REAP × CoPaper.AI</strong> · An academic–industrial AI toolkit for empirical research<br/>
  <sub>Built by Stanford's empirical-methodology team — the full pipeline from data cleaning to top-journal submission</sub>

  <br/>
</div>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/brycewang-stanford/Auto-Empirical-Research-Skills?style=social)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Validate catalog](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/brycewang-stanford/Auto-Empirical-Research-Skills/badge)](https://scorecard.dev/viewer/?uri=github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![Security audit: 52/52 CLEAN](https://img.shields.io/badge/security%20audit-52%2F52%20CLEAN-brightgreen)](SECURITY-SCAN-REPORT.md)
[![Powered by StatsPAI](https://img.shields.io/badge/powered%20by-StatsPAI-orange)](https://github.com/brycewang-stanford/StatsPAI)

**The empirical-research specialist's agent-skills distribution.** Not a marketing list — **1,145 skills vendored and cataloged** in this repo, wrapped in a **numeric benchmark, an eval harness, a security audit, and CI**, plus a curated map of **23,000+ skills across 119 repositories** in the wider ecosystem.

AERS is two things at once: (1) a small set of **first-party flagship skills** that run the full empirical pipeline — data cleaning → identification → estimation → robustness → tables/figures → submission-ready draft — and (2) a **curated, security-aware catalog** of the empirical-research skill ecosystem, organized by research-workflow stage. The differentiator is not the count; it is that the flagship behavior is **verified against known answers**, not asserted.

> [!NOTE]
> **Renamed.** This project was formerly *Awesome Agent Skills for Empirical Research*. GitHub redirects the old URL automatically; please update your remote:
> ```bash
> git remote set-url origin https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
> ```

---

## Contents

- [What you actually get (the numbers, precisely)](#what-you-actually-get-the-numbers-precisely)
- [Verify it yourself in 2 minutes](#verify-it-yourself-in-2-minutes)
- [Why trust this — three layers](#why-trust-this--three-layers)
- [The flagship pipeline skills](#the-flagship-pipeline-skills)
- [Start here — pick a skill in 30 seconds](#start-here--pick-a-skill-in-30-seconds)
- [What makes this more than a 23K-skill dump](#what-makes-this-more-than-a-23k-skill-dump)
- [Browse the landscape](#browse-the-landscape)
  - [By research stage](#by-research-stage)
  - [Comprehensive skill suites](#comprehensive-skill-suites)
  - [Anti-AIGC detection & de-AI academic writing](#anti-aigc-detection--de-ai-academic-writing)
  - [Tools catalog (tools/)](#tools-catalog-tools--automated-empirical--causal-inference-tools)
  - [Multi-agent systems · MCP servers · platforms · learning](#multi-agent-systems--mcp-servers--platforms--learning)
- [Security](#security)
- [Changelog](#changelog)
- [Contributing & citation](#contributing--citation)

---

## What you actually get (the numbers, precisely)

Numbers in this README are kept honest and disambiguated. "Vendored" means the files live in this repo and are tracked in a generated catalog; "cataloged ecosystem" means curated links to external repositories.

| What it is | Count | Source of truth |
|---|---:|---|
| Skills **vendored into this repo** and cataloged | **1,145** | [`catalog/skills.json`](catalog/skills.json) |
| Vendored **collections** | **69** | [`catalog/skills.json`](catalog/skills.json) · [all 69 at a glance ↓](#all-69-vendored-skill-collections-at-a-glance) |
| **First-party flagship** full-pipeline skills (StatsPAI DSL + explicit Python/Stata/R) | **4** | [`skills/00*`](skills/) |
| Numeric **benchmark tasks** with gold values recomputed from data each run | **5** | [`benchmark/`](benchmark/) |
| Behavioral **eval scenarios / rubric items** | **17 / 95** | [`eval-harness/`](eval-harness/) |
| Security audit of the **original baseline** (collections / files) | **52 / 2,940+**, 52/52 CLEAN | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| Curated **map of the wider ecosystem** | **23,000+ skills / 119 repos** | this README · [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md) |
| **Tools catalog** (`tools/`): causal/econometrics libraries, autonomous research agents, MCP servers, causal discovery, benchmark datasets | **335 tools / 6 categories** | [`tools/tools.json`](tools/tools.json) · [`tools/CATALOG.md`](tools/CATALOG.md) |

> The security audit covered the original **52-collection / 2,940-file baseline (52/52 CLEAN)**. Skills vendored after that baseline are tracked in [`catalog/provenance.json`](catalog/provenance.json), [`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md), and [`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md); run `make audit` before relying on them in high-trust contexts.

---

## Verify it yourself in 2 minutes

The most persuasive thing here is not a number — it is that the flagship pipeline's behavior is **checkable without an API key or paid model**. Just Python 3:

```bash
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
cd Auto-Empirical-Research-Skills
make check        # repo validation + unit tests + eval lint + numeric benchmark
```

The benchmark is the convincing part: it **recomputes the gold answer from the raw dataset on every run**, so a passing score cannot be faked by hard-coding a number. Out of the box it recovers:

- **LaLonde (1986) / Dehejia–Wahba (1999)** — the naive observational comparison gets the *wrong sign* (−$635); covariate adjustment flips it positive (≈ +$1,548) toward the experimental benchmark (≈ +$1,794).
- **Card (1995)** — IV return to schooling (0.131) *exceeds* OLS (0.075), with the first-stage F (13.3) reported rather than hidden.
- Plus staggered-DID (TWFE bias vs. group-time truth), sharp **RDD**, and a **bad-control / post-treatment-bias** trap.

A pipeline passes only if it **surfaces the trap, refuses to headline the misleading number, and matches the recomputed truth**. See [`benchmark/`](benchmark/) and the full trust overview in [`docs/TRUST.md`](docs/TRUST.md).

> 💡 **Want it hosted and end-to-end?** Skip the assembly — [**copaper.ai**](https://copaper.ai) runs the empirical pipeline for you, built alongside this catalog by the same Stanford methodology team.

---

## Why trust this — three layers

| Layer | Anchor | What it brings |
|---|---|---|
| 🏛️ **Academic lineage** | **[Stanford REAP / SCCEI](https://sccei.fsi.stanford.edu/reap)** — Stanford Center on China's Economy and Institutions | A research center with a sustained publication record in empirical-economics methodology and a deep tradition in applied causal inference. |
| 🔧 **Engineering delivery** | **[CoPaper.AI](https://copaper.ai)** — empirical-research AI assistant | Ships **20 econometric-methodology skills** (DID / IV / RDD / PSM / DML, …) behind a Supervisor + 4-sub-agent architecture, one-sentence triggers, automatic publication-ready output. |
| ⚙️ **Open-source engine** | **[StatsPAI](https://github.com/brycewang-stanford/StatsPAI)** — the causal-inference engine | **900+ functions · one `import statspai as sp` · JOSS in submission · MIT.** Every DID / IV / RD / SCM estimate CoPaper.AI produces is driven by StatsPAI, and this catalog is part of that ecosystem. |

---

## The flagship pipeline skills

Four parallel implementations of the **same 8-step empirical loop** — *data cleaning → variable construction → descriptives → diagnostics → estimation → robustness → mechanism/heterogeneity → publication-ready tables & figures* — plus the submission and de-AIGC stacks. Each uses **progressive disclosure**: a thin canonical-call spine in `SKILL.md`, with deep per-step reference manuals loaded only on demand. They coexist; pick by stack and use case.

| Skill | Stack | Best for |
|---|---|---|
| **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)** 🔥 | Agent-native Python **DSL** — one `sp.causal(...)` runs the loop; 900+ functions, self-describing API, unified `CausalResult` | Whole-pipeline automation in one agent call when you trust the DSL |
| **[Full Empirical Analysis — Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md)** 📘 | **Explicit** stack: `pandas` · `statsmodels` · `linearmodels` · `pyfixest` · `rdrobust` · `econml` · `causalml` | Teaching, referee-level line-by-line audit, strict replication needing full control |
| **[Full Empirical Analysis — Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md)** 📊 | Community standard: `reghdfe` · `ivreg2` · `csdid` · `did_imputation` · `sdid` · `rdrobust` · `synth` · `psmatch2` · `boottest` · `esttab` | When a referee or co-author insists on a Stata replication pack (AER/QJE/JPE/ReStud style) |
| **[Full Empirical Analysis — R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)** 📗 | Modern tidyverse: `fixest` · `did` · `synthdid` · `HonestDiD` · `rdrobust` · `grf` · `DoubleML` · `marginaleffects` · **Quarto** | Single-`.qmd` reproducibility reports rendered to PDF/HTML/Word in one command |
| **[AER-Skills](skills/50-brycewang-aer-skills/)** 📕 | 9 skills: topic routing → identification audit → robustness → intro → tables → replication → submission → R&R → orchestrator | Top-5 economics (AER / AER:Insights / AEJ) submission: *identification-first* — fragile design, no prose saves it |
| **[chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/SKILL.md)** 🇨🇳 | 17-pattern Chinese AI-tell library, 5-step locate→diagnose→rewrite→score→review loop | Lowering AI-writing signal for CNKI / Wanfang / VIP / Turnitin-Chinese submissions |

> **Why a DSL *and* explicit ports?** Reach for StatsPAI when you trust the one-shot DSL; reach for 00.1/00.2/00.3 when you are teaching, auditing, or must swap every diagnostic by hand. AER-skills then takes a correct analysis to acceptance threshold — these solve *different* problems and compose.

---

## Start here — pick a skill in 30 seconds

| Goal | Start with |
|---|---|
| Run a complete empirical pipeline | [`StatsPAI`](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md) (or [Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md) · [Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md) · [R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)) |
| Audit a top-5 identification strategy first | [`aer-identification`](skills/50-brycewang-aer-skills/skills/aer-identification/SKILL.md) |
| Prepare an AER / AEJ submission | [`aer-workflow`](skills/50-brycewang-aer-skills/skills/aer-workflow/SKILL.md) |
| Build an AEA-ready replication package | [`aer-replication`](skills/50-brycewang-aer-skills/skills/aer-replication/SKILL.md) |
| Lower the AI-writing signal of a Chinese draft | [`chinese-de-aigc`](skills/48-copaper-ai-chinese-de-aigc/SKILL.md) |

**More ways in:**

- **Not sure which skill?** → [`docs/CHOOSING_A_SKILL.md`](docs/CHOOSING_A_SKILL.md) · faceted search: [`docs/search.html`](docs/search.html)
- **First 10 minutes, end to end** → [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)
- **Copy-paste a full workflow** → [`docs/GOLDEN_WORKFLOWS.md`](docs/GOLDEN_WORKFLOWS.md)
- **Install into a runtime / use without installing** → [`docs/INSTALL.md`](docs/INSTALL.md)
- **Machine-readable index** → [`catalog/skills.json`](catalog/skills.json) · taxonomy: [`docs/TAXONOMY.md`](docs/TAXONOMY.md) · full catalog: [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md)
- **FAQ** → [`docs/FAQ.md`](docs/FAQ.md)

---

## What makes this more than a 23K-skill dump

Public-skill counts are easy to inflate, and recent studies show large skill indexes are often redundant and occasionally unsafe. AERS competes on **verifiable quality**, not raw count. Every layer below runs locally via `make check` and in CI.

| Layer | What it catches | Where |
|---|---|---|
| **Numeric benchmark** | Reported numbers that don't match truth recomputed from real data — the naive-DID sign trap, weak-IV without first-stage F, TWFE bias under staggered timing, RDD trend confound, post-treatment bad controls | [`benchmark/`](benchmark/) · 5 tasks |
| **Eval harness** | Prose-level failures: weak-IV false reassurance, staggered-DID TWFE misuse, fabricated citations, unsafe `curl \| bash` setup, multiple-testing abuse, AER compliance gaps | [`eval-harness/`](eval-harness/) · 17 scenarios / 95 rubric items |
| **Security audit** | Pipe-to-shell, reverse shells, credential exfiltration, prompt injection across 13 risk categories — 6-phase, 40+ hook scripts reviewed by hand | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| **Provenance & license** | Unvendored sources, license risk, hygiene drift across all 1,145 cataloged skills | [`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md) · [`docs/SKILL_QUALITY.md`](docs/SKILL_QUALITY.md) |
| **CI & compatibility** | Catalog freshness, broken local links, GitHub Actions policy, Python 3.9 **and** 3.12 syntax floor | [`.github/workflows/`](.github/workflows/) · 6 workflows |

```bash
make catalog     # regenerate catalog, provenance, audit, enrichment
make validate    # freshness + link / frontmatter checks
make check       # full gate: validate + Python compile + unit tests + eval lint + benchmark
```

The trust surface is **necessary, not sufficient** — regex rubrics don't certify prose and a small benchmark doesn't cover every design. It is built to *fail fast on known high-cost mistakes*. Read the honest scope in [`docs/TRUST.md`](docs/TRUST.md) and [`docs/QUALITY_GATE.md`](docs/QUALITY_GATE.md).

---

## Browse the landscape

### All 69 vendored skill collections at a glance

> **69 collections · 1,145 skills**, every one vendored into this repo and tracked in [`catalog/skills.json`](catalog/skills.json). Grouped by what they do — click any collection to open its folder. (Source of truth: `make catalog`.)

**🚀 Full-pipeline flagships & orchestrators** — *one call, the whole empirical loop*

| Collection | What it does | Skills |
|---|---|---:|
| [`00` · StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/) 🔥 | Agent-native Python **DSL** — one `sp.causal(...)` runs DID/RD/IV/SCM/DML | 1 |
| [`00.1` · Python](skills/00.1-Full-empirical-analysis-skill_Python/) 📘 | Explicit stack: `pandas` · `statsmodels` · `linearmodels` · `pyfixest` | 1 |
| [`00.2` · Stata](skills/00.2-Full-empirical-analysis-skill_Stata/) 📊 | `reghdfe` · `ivreg2` · `csdid` · `sdid` · `rdrobust` replication pack | 1 |
| [`00.3` · R](skills/00.3-Full-empirical-analysis-skill_R/) 📗 | tidyverse · `fixest` · `did` · `HonestDiD`, rendered via Quarto | 1 |
| [`33` · claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) | Full research lifecycle: ideation → review → experiments → response | 47 |
| [`42` · ARIS](skills/42-wanshuiyin-ARIS/) | Autonomous "research-in-sleep" agent, end-to-end | 104 |
| [`50` · AER-skills](skills/50-brycewang-aer-skills/) 📕 | Top-5 econ submission stack: identification → robustness → R&R | 9 |
| [`67` · econfin-workflow-toolkit](skills/67-econfin-workflow-toolkit/) | China corporate-finance empirical workflow, proposal → paper | 46 |
| [`69` · Paper-WorkFlow](skills/69-Paper-WorkFlow/) | Meta-orchestrator chaining the whole social-science pipeline | 1 |

**🎯 Causal inference & econometrics** — *the methodological core of AERS*

| Collection | What it does | Skills |
|---|---|---:|
| [`09` · awesome-econ-ai](skills/09-meleantonio-awesome-econ-ai-stuff/) | Python panel-data analysis (`linearmodels`) | 17 |
| [`10` · causal-inference-mixtape](skills/10-Jill0099-causal-inference-mixtape/) | DID / IV / RDD / SCM templates (Cunningham) | 1 |
| [`11` · compound-science](skills/11-James-Traina-compound-science/) | Bayesian estimation for quantitative social science | 20 |
| [`13` · MixtapeTools](skills/13-scunning1975-MixtapeTools/) | Cunningham's causal-inference toolkit & decks | 5 |
| [`14` · research-starter](skills/14-luischanci-claude-code-research-starter/) | IV / DiD / RDD in R with proper diagnostics | 16 |
| [`15` · social-science-research](skills/15-Felpix-Studios-social-science-research/) | End-to-end data analysis in R or Python | 12 |
| [`16` · clo-author](skills/16-hsantanna88-clo-author/) | Multi-agent data analysis (R / Stata / Python) | 10 |
| [`18` · stata-accounting](skills/18-jusi-aalto-stata-accounting-research/) | Tested Stata patterns from 126 *JAR* papers | 1 |
| [`20` · python-econ-skill](skills/20-wenddymacro-python-econ-skill/) | DSGE / HANK & quantitative economic computation | 1 |
| [`23` · baygent](skills/23-Learning-Bayesian-Statistics-baygent-skills/) | PyMC / ArviZ Bayesian workflow with guardrails | 2 |
| [`26` · scholar](skills/26-Data-Wise-scholar/) | Statistical-algorithm design & documentation | 17 |
| [`31` · claude-code-skills](skills/31-thalysandratos-claude-code-skills/) | Python panel-data analysis | 13 |
| [`39` · marginaleffects](skills/39-vincentarelbundock-marginaleffects/) | Predictions, slopes & comparisons (R / Python) | 1 |
| [`40` · pyfixest](skills/40-py-econometrics-pyfixest/) | Fast fixed-effects estimation in Python | 1 |
| [`51` · CausalPy](skills/51-pymc-labs-CausalPy/) | Bayesian quasi-experiments (PyMC Labs) | 3 |
| [`55` · r-skills](skills/55-ab604-claude-code-r-skills/) | Bayesian inference in R with `brms` | 8 |
| [`61` · research-methods](skills/61-phdemotions-research-methods/) | Confirmatory testing matched to pre-registration | 9 |
| [`63` · scientific-agent-skills](skills/63-tondevrel-scientific-agent-skills/) | DoWhy identify–estimate–refute framework | 2 |
| [`64` · mcp-stata](skills/64-tmonk-mcp-stata/) | 20 Stata causal-inference & replication skills | 20 |

**📚 Literature, reading & research design** — *from question to evidence base*

| Collection | What it does | Skills |
|---|---|---:|
| [`02` · research-skills](skills/02-luwill-research-skills/) | Medical-imaging reviews, proposals, paper-to-slides | 3 |
| [`03` · scientific-skills](skills/03-K-Dense-AI-claude-scientific-skills/) | Hypothesis generation + 28 scientific databases | 4 |
| [`05` · research-superpower](skills/05-kthorn-research-superpower/) | Systematic search, screening & citation traversal | 10 |
| [`25` · Diverga](skills/25-HosungYou-Diverga/) | Research-question refiner (anti mode-collapse) | 34 |
| [`34` · research-companion](skills/34-andrehuang-research-companion/) | Brainstorm, evaluate & decide research directions | 1 |
| [`35` · academic-writing-skills](skills/35-bahayonghang-academic-writing-skills/) | Venue-aware industrial-AI literature research | 5 |
| [`36` · literature-review-skill](skills/36-taoyunudt-literature-review-skill/) | Full literature-review workflow (Chinese) | 1 |
| [`52` · slr-prisma](skills/52-keemanxp-slr-prisma/) | Systematic literature review, PRISMA 2020 | 1 |
| [`53` · thematic-analysis](skills/53-keemanxp-thematic-analysis-skill/) | Braun & Clarke six-phase qualitative TA | 1 |
| [`59` · openalex-skill](skills/59-shiquda-openalex-skill/) | Query 240M+ scholarly works via OpenAlex | 1 |
| [`60` · superpapers](skills/60-regisely-superpapers/) | Comprehensive empirical-research support suite | 16 |

**✍️ Writing, editing & de-AIGC** — *draft, polish, and pass AI-detection*

| Collection | What it does | Skills |
|---|---|---:|
| [`01` · academic-paper-skills](skills/01-lishix520-academic-paper-skills/) | Outline → manuscript writing + 7-dim reviewer sim | 2 |
| [`04` · scientific-writer](skills/04-K-Dense-AI-claude-scientific-writer/) | Citation management + scientific writing | 8 |
| [`06` · stats-paper-writing](skills/06-fuhaoda-stats-paper-writing/) | End-to-end LaTeX statistical-paper writing | 1 |
| [`22` · christopherkenny-skills](skills/22-christopherkenny-skills/) | APSA style checker for Quarto (`.qmd`) | 11 |
| [`27` · my_claude_skills](skills/27-dariia-m-my_claude_skills/) | Economics-abstract writing guide | 6 |
| [`38` · academic-proofreader](skills/38-peternka-academic-proofreader/) | Academic proofreading | 1 |
| [`44` · humanizer_academic](skills/44-matsuikentaro1-humanizer_academic/) | De-AI medical/academic manuscripts (23 patterns) | 1 |
| [`45` · deslop](skills/45-stephenturner-skill-deslop/) | Remove AI writing patterns (5-dim scoring) | 1 |
| [`46` · stop-slop](skills/46-hardikpandya-stop-slop/) | 3-layer AI-tell detection & rewrite | 1 |
| [`47` · avoid-ai-writing](skills/47-conorbronsdon-avoid-ai-writing/) | Audit → rewrite → re-audit AI-isms (paper trail) | 1 |
| [`48` · chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/) 🇨🇳 | Chinese de-AIGC for CNKI / Wanfang / Turnitin-CN | 1 |
| [`49` · humanize-chinese](skills/49-voidborne-d-humanize-chinese/) | Detect & humanize AI-generated Chinese text | 1 |
| [`56` · econ-writing-skill](skills/56-hanlulong-econ-writing-skill/) | Econ writing synthesizing 50+ top guides | 1 |
| [`58` · econstack](skills/58-charlescoverdale-econstack/) | Policy briefing notes (UK GES / AU Treasury) | 7 |
| [`65` · game-theory-paper-writer](skills/65-game-theory-paper-writer/) | Generate & stress-test game-theory papers | 1 |

**📑 Citation, replication & peer review** — *make it verifiable and reproducible*

| Collection | What it does | Skills |
|---|---|---:|
| [`24` · academic-research-skills](skills/24-Imbad0202-academic-research-skills/) | 5-reviewer multi-perspective paper review | 4 |
| [`28` · paper-replicate-agent](skills/28-maxwell2732-paper-replicate-agent-demo/) | Paper-replication agent demo | 11 |
| [`29` · project20XXy](skills/29-quarcs-lab-project20XXy/) | Reproducible manuscript + notebook project | 24 |
| [`41` · sewage-econometrics-check](skills/41-sticerd-eee-sewage-econometrics-check/) | 10-check replication-package audit | 22 |
| [`54` · open-science-skills](skills/54-scdenney-open-science-skills/) | Citation parity, DOI & claim-support audit | 24 |
| [`62` · citation-checker](skills/62-PHY041-claude-skill-citation-checker/) | Verify citations vs CrossRef / S2 / OpenAlex | 1 |

**🛠️ Data, tooling & infrastructure** — *the plumbing under the pipeline*

| Collection | What it does | Skills |
|---|---|---:|
| [`07` · AI-Research-SKILLs](skills/07-Orchestra-Research-AI-Research-SKILLs/) | Publication ML figures, LaTeX, citation verify | 3 |
| [`08` · latex-document-skill](skills/08-ndpvt-web-latex-document-skill/) | Create / compile any LaTeX doc to PDF | 1 |
| [`12` · claude-code-my-workflow](skills/12-pedrohcgs-claude-code-my-workflow/) | Commit → PR → merge research workflow (Emory) | 22 |
| [`17` · DAAF](skills/17-DAAF-Contribution-Community-daaf/) | Security-conscious agent framework (32 deny rules) | 35 |
| [`32` · stata-skill](skills/32-dylantmoore-stata-skill/) | High-performance Stata C/C++ plugins | 3 |
| [`43` · research-plugins](skills/43-wentorai-research-plugins/) | 478 research plugins: dataviz, domains, infra | 478 |
| [`57` · edgartools](skills/57-dgunning-edgartools/) | Query & analyze SEC filings | 1 |
| [`66` · empirical-research-skills](skills/66-zheng-siyao-empirical-research-skills/) | R performance optimization for large panels | 7 |
| [`68` · research-productivity-skills](skills/68-research-productivity-skills/) | Paper search, SSRN, DOI lookup, downloads | 18 |

### By research stage

```
Topic Ideation → Lit Search → Deep Reading → Research Design → Data Collection
      │              │             │              │                │
      ▼              ▼             ▼              ▼                ▼
     01             02            03             01               04

Data Cleaning → Statistical Analysis → First Draft → Revision → Typesetting
      │              │                    │            │            │
      ▼              ▼                    ▼            ▼            ▼
     04             05                   06           07           08

Replication → Submission → Peer Review Response → Defense
      │           │              │                   │
      ▼           ▼              ▼                   ▼
     09          10             10                  10
```

Per-stage skill notes (bilingual): [01 Topic & design](docs/01-选题与研究设计.md) · [02 Lit review](docs/02-文献检索与综述.md) · [03 Paper reading](docs/03-论文阅读与拆解.md) · [04 Data & cleaning](docs/04-数据获取与清洗.md) · [05 Causal inference](docs/05-统计分析与因果推断.md) · [06 Writing](docs/06-论文写作.md) · [07 Revision](docs/07-论文修改与润色.md) · [08 Citation & typesetting](docs/08-引用管理与排版.md) · [09 Replication](docs/09-论文复现与可复现研究.md) · [10 Review response](docs/10-审稿回复与学术答辩.md)

### Comprehensive skill suites

> The pain point AERS exists to fix: ask an AI to "run a DID" and it gives the baseline regression and stops. "Parallel trends?" — it adds one. "Placebo?" — another. *Every time, like squeezing toothpaste.* A skill is a **methodology playbook for the agent**: it already knows a complete DID means parallel-trends → baseline → robustness battery → heterogeneity → mechanism, with a defined output at each step.

<details>
<summary><b>Academic research</b> — general-purpose research suites (K-Dense, AI-Research-SKILLs, claude-scholar, …)</summary>

| Suite | Stars | # Skills | Key features |
|-------|-------|----------|-------------|
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 8,799 | 140+ | 28+ scientific databases (OpenAlex, PubMed); scientific-writing + literature-review + statistical-analysis |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 3,637 | 87 | 22 categories, ML paper writing, LaTeX templates, citation verification |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | ~1,790 | Multiple | Full paper pipeline (research → write → review → revise → finalize), style calibration, hallucination detection |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | - | 25+ | Full research lifecycle: ideation → review → experiments → writing → review response; Zotero MCP |
| [luwill/research-skills](https://github.com/luwill/research-skills) | 209 | 3 | Research-proposal generation, medical review writing, paper-to-slides, bilingual |
| [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | 22 | 2 | Strategist (7-dimension reviewer simulation) + Composer (systematic writing) |
| [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) | - | 17 | Statistical research: arXiv search, DOI lookup, BibTeX, methodology writing, referee response |

</details>

<details>
<summary><b>Economics / causal inference</b> — the first-party flagships plus community Stata/IV/feedback suites</summary>

The first-party flagships ([StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/), [Python](skills/00.1-Full-empirical-analysis-skill_Python/), [Stata](skills/00.2-Full-empirical-analysis-skill_Stata/), [R](skills/00.3-Full-empirical-analysis-skill_R/), [AER-skills](skills/50-brycewang-aer-skills/)) are described [above](#the-flagship-pipeline-skills). Community complements:

| Suite | Key features | Use case |
|-------|-------------|----------|
| **[CoPaper.AI](https://copaper.ai)** | 20 methodology skills, Supervisor + 4 sub-agents, smart routing, automatic output | Full empirical-economics workflow, hosted |
| [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) | 2-agent pre-review: causal-overclaiming detection, identification assessment (AER/QJE/JPE/Econometrica/REStud); 6-agent grant review | Pre-submission self-review, grants |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | LaTeX statistical-paper writing, front-end draft generation | Statistics & econometrics papers |
| [dylantmoore/stata-skill](https://github.com/dylantmoore/stata-skill) | Full Stata coverage: syntax, data management, econometrics, causal inference, Mata, 20+ packages | Stata users |
| [SepineTam/stata-mcp](https://github.com/SepineTam/stata-mcp) | LLM drives Stata regressions directly via MCP | Stata econometrics |
| [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp) | Stata-MCP editor extension (VS Code/Cursor/Antigravity): run `.do` directly, live output, data/graph viewer; MIT · 414★ (same name as SepineTam above, different project) | In-editor AI pairing with Stata |
| [tmonk/mcp-stata](https://github.com/tmonk/mcp-stata) · vendored at [`skills/64`](skills/64-tmonk-mcp-stata/) | **20 SKILL.md skills** from the Stata MCP server: replication / data audit / publication QA / legacy modernization / referee response / power / causal inference; **AGPL-3.0** (kept as a separately-licensed aggregate; server code not vendored) | Stata replication & robustness audits |
| [PovertyAction/ipa-stata-template](https://github.com/PovertyAction/ipa-stata-template) | IPA reproducible Stata research template + `.claude/skills`: numbered pipeline, assertion-based defensive programming, LaTeX tables; MIT | Development economics / field-RCT replication |
| [lcrawfurd/claude-skills](https://github.com/lcrawfurd/claude-skills) | Academic skills: paper / code review, referee, pre-submission; code-review encodes Stata/R/Python coding standards (DIME / Reif / AEA Data Editor) | Pre-submission review & code audit |
| [AEADataEditor/replication-template](https://github.com/AEADataEditor/replication-template) | AEA Data Editor's official replication-package template (Stata-centric, `REPLICATION.md`) — the reproducibility "gold standard" | AEA / top-journal replication packaging |

</details>

<details>
<summary><b>Finance · education & public health · law · marketing · product · general agents</b></summary>

**Finance & investment** — [financial-services-plugins](https://github.com/anthropics/financial-services-plugins) (Anthropic official) · [OctagonAI/skills](https://github.com/OctagonAI/skills) · [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) · [himself65/finance-skills](https://github.com/himself65/finance-skills) · [quant-sentiment-ai/claude-equity-research](https://github.com/quant-sentiment-ai/claude-equity-research)

**Education & public health** — [GarethManning/claude-education-skills](https://github.com/GarethManning/claude-education-skills) · [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) (**869** medical skills: epidemiology, surveillance, clinical research, drug safety, biostatistics)

**Governance, compliance & law** — [Claude-Skills-Governance-Risk-and-Compliance](https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance) (ISO 27001 / SOC 2 / GDPR / HIPAA) · [zubair-trabzada/ai-legal-claude](https://github.com/zubair-trabzada/ai-legal-claude) · [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)

**Marketing & consumer behavior** — [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) · [zubair-trabzada/ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude) · [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills)

**Product & organizational behavior** — [phuryn/pm-skills](https://github.com/phuryn/pm-skills) (100+ skills) · [mastepanoski/claude-skills](https://github.com/mastepanoski/claude-skills) (Nielsen heuristics, NIST AI RMF, ISO 42001)

**General agent capabilities** — [lyndonkl/claude](https://github.com/lyndonkl/claude) (85 skills + 6 orchestrators) · [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (220+ skills, ~5,200★) · [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) · [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) (1,367 skills) · [posit-dev/skills](https://github.com/posit-dev/skills) (Posit official)

</details>

### Anti-AIGC detection & de-AI academic writing

> One of 2026's sharpest pain points: papers failing AIGC detection (Turnitin, GPTZero, CNKI) can be rejected outright. The skills below are the most complete open-source solutions — all MIT, all locally archived (`skills/44-48`).

| Suite | Key features | Best for | Local |
|-------|-------------|----------|-------|
| **chinese-de-aigc** 🇨🇳 | **Original** Chinese academic de-AIGC by CoPaper.AI; 17-pattern Chinese-tell library, 5-step loop, per-section strategy, 5-dim scoring. The only GitHub skill dedicated to Chinese academic de-AIGC | CNKI / Wanfang / VIP / Turnitin-Chinese | [`48`](skills/48-copaper-ai-chinese-de-aigc/) |
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | Academic-specific; 23 AI-writing patterns; preserves legitimate academic transitions | Medical, life-science, natural-science papers | [`44`](skills/44-matsuikentaro1-humanizer_academic/) |
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) | Distinguishes legitimate discipline conventions from AI tells; 5-dimension scoring | Scientific papers, technical blogs | [`45`](skills/45-stephenturner-skill-deslop/) |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 3-layer detection + 5-dim scoring; banned phrases, structural clichés, sentence rules | General prose, blogs, reports | [`46`](skills/46-hardikpandya-stop-slop/) |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | Structured audit + rewrite + second-pass audit; auditable, traceable | Workflows needing a paper trail | [`47`](skills/47-conorbronsdon-avoid-ai-writing/) |

> **Combos:** 🇨🇳 Chinese (CNKI/Wanfang/VIP) → chinese-de-aigc · 🇬🇧 English → humanizer_academic · need an audit trail → avoid-ai-writing · general prose → stop-slop.

### Tools catalog (`tools/`) — automated empirical & causal-inference tools

> Unlike the skills above, [`tools/`](tools/) catalogs the **software and services an agent (or researcher) actually invokes** — structured, license- and maintenance-aware, and wired into `make validate`. Source of truth: [`tools/tools.json`](tools/tools.json); browsable list: [`tools/CATALOG.md`](tools/CATALOG.md).

**335 tools across 6 categories** (curated 2026-06):

- **Causal-inference / treatment-effect libraries (32)** — DoWhy · EconML · CausalML · DoubleML · CausalPy · causallib · grf · CATENets · TMLE family · Mendelian randomization …
- **Econometrics / quasi-experimental libraries (170)** — panel FE · DiD (incl. modern/staggered) · event study · RDD · IV · synthetic control/SDID · matching & weighting · sensitivity (fixest · did · HonestDiD · rdrobust · synthdid · reghdfe · csdid · sdid · pyfixest · linearmodels …); **plus** spatial econometrics (spdep · PySAL/spreg · GeoDa), local projections/IRF & (S)VAR (lpirfs · vars · svars), survey weighting/MRP/raking (survey · samplics · balance), and meta-analysis (metafor · meta · netmeta · metan) — across R/Python/Stata/Julia.
- **Autonomous research / data-science agents (51)** — end-to-end research & data analysis: AI-Scientist · data-to-paper · Agent Laboratory · RD-Agent · AI-Researcher · STORM · PaperQA2 · gpt-researcher · DeepAnalyze · MetaGPT (DI) · Biomni …  (⚠️ includes non-OSI / no-LICENSE repos — confirm terms before use).
- **MCP servers (48)** — stats execution (StatsPAI · stata-mcp · R/Jupyter MCP) + data access (FRED · World Bank · IMF · OECD · Eurostat · Census · BEA · BLS · SEC EDGAR · OpenAlex · Semantic Scholar · PubMed · Zotero · arXiv …).
- **Causal discovery / structure learning (25)** — causal-learn · Tetrad/py-tetrad · gCastle · CDT · tigramite (PCMCI) · LiNGAM · NOTEARS/DAGMA · pcalg · bnlearn · pgmpy …
- **Benchmarks & datasets (9)** — causaldata · IHDP/Twins · ACIC competition data · RealCause · JustCause · Tübingen cause-effect pairs · bnlearn network repository …

Full write-up: [`tools/README.md`](tools/README.md).

### Multi-agent systems · MCP servers · platforms · learning

<details>
<summary><b>Multi-agent collaboration systems</b> — paper revision, autonomous research, data-science teams</summary>

Role separation beats a single agent because the reviewer is independent of the drafter — the same logic as peer review.

**Paper revision & writing:** copy-edit-master (3 sub-agents, Strunk & White / McCloskey rules) · introduction-writer (strategist → drafter → reviewer → reviser) · CoPaper.AI PaperAgent (Supervisor + 4 sub-agents).

**Autonomous research & data science:** [ruc-datalab/DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze) · [business-science/ai-data-science-team](https://github.com/business-science/ai-data-science-team) · [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) (NeurIPS 2025 Spotlight) · [wanshuiyin/ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) · [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) (84% cost reduction) · [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) · [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) · [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) (Emory).

</details>

<details>
<summary><b>Academic data MCP servers</b> — OpenAlex, Semantic Scholar, FRED, World Bank, Zotero, …</summary>

[xingyulu23/Academix](https://github.com/xingyulu23/Academix) · [Eclipse-Cj/paper-distill-mcp](https://github.com/Eclipse-Cj/paper-distill-mcp) · [oksure/openalex-research-mcp](https://github.com/oksure/openalex-research-mcp) (240M+ works) · [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) (20+ sources) · [lzinga/us-gov-open-data-mcp](https://github.com/lzinga/us-gov-open-data-mcp) (40+ US gov APIs) · [stefanoamorelli/fred-mcp-server](https://github.com/stefanoamorelli/fred-mcp-server) (FRED 800K+ series) · [llnOrmll/world-bank-data-mcp](https://github.com/llnormll/world-bank-data-mcp) · [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)

</details>

<details>
<summary><b>Skill aggregation platforms & learning resources</b></summary>

**Platforms:** [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) (1,000+) · [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) (1,340+) · [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) (5,400+) · [skills.sh](https://skills.sh/) · [ClawHub](https://clawhub.com) (13,729) · [Anthropic official skills](https://github.com/anthropics/skills).

**Learning:** [Claude Code Skills guide (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) · [Agent Skills Standard](https://agentskills.io/) · [Causal Inference for the Brave and True](https://github.com/xieliaing/CausalInferenceIntro) · [Awesome AI for Economists](https://github.com/hanlulong/awesome-ai-for-economists) · [Awesome Econ AI Stuff](https://github.com/meleantonio/awesome-econ-ai-stuff).

</details>

---

## Security

The **original 52 skill collections / 2,940+ files** passed a systematic audit — **52/52 CLEAN, zero FLAGGED**: no malicious prompts, viruses, reverse shells, or prompt injection. Every "sensitive" hit verified as one of three legitimate categories: **defensive security rules**, **legitimate academic API calls** (arXiv / CrossRef / PubMed / FRED / World Bank / OECD / BLS), or **standard Claude Code workflow hooks** (all local file ops, zero network IO).

![Skills Security Scan Overview](images/security-scan/security-scan-01-overview.png)

Six-phase, defense-in-depth: automated grep across **13 risk categories** → 100% manual review of all **6 hook-bearing skills and their 40+ hook scripts** (no `Bash(*)` wildcards anywhere) → three parallel agent content audits → supplemental integrity checks (hidden Unicode, encoding anomalies, HTML injection, network imports).

> **Key insight:** largest ≠ riskiest. The biggest skills all passed; [17-DAAF](skills/17-DAAF-Contribution-Community-daaf/) actually sets the bar for security-conscious design (14 defensive hooks + 32 deny rules + active credential scanning).

Newer vendored additions are tracked in [`catalog/provenance.json`](catalog/provenance.json) and [`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md) — run `make audit`. Full report: [**SECURITY-SCAN-REPORT.md**](SECURITY-SCAN-REPORT.md).

---

## Changelog

The narrative changelog has moved to [**CHANGELOG.md**](CHANGELOG.md). Recent highlights:

- **2026-05** — Vendored **AER-skills** (top-5 economics submission stack, 9 skills) with weekly upstream sync; expanded the numeric benchmark to **5 causal-recovery tasks** and the eval harness to **17 scenarios / 95 rubric items**.
- **2026-04** — Completed the **52/52 security baseline**; shipped the four full-pipeline flagships (**StatsPAI** + explicit **Python / Stata / R**); launched the original **chinese-de-aigc** skill.
- **Earlier** — Grew from 43 collections to a curated map of **119 repos / 23,000+ skills**; added bilingual README, academic data MCP servers, and multi-agent systems.

---

## Contributing & citation

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the [`docs/SKILL_SUBMISSION_GUIDE.md`](docs/SKILL_SUBMISSION_GUIDE.md). We especially welcome social-science skills (economics, political science, sociology, psychology, education, public health), new causal-inference implementations, MCP servers for academic/government data, Chinese-friendly skills, and multi-agent case studies. New submissions must declare **source, license, and category** for the provenance audit.

If AERS helps your work, please **cite it** ([CITATION.cff](CITATION.cff)) and **star the repo** so more researchers can find it.

<a href="https://www.star-history.com/#brycewang-stanford/Auto-Empirical-Research-Skills&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" width="600" />
 </picture>
</a>

---

<div align="center">

**AI is an amplifier, not a replacement. It handles the heavy lifting; you keep the core judgment.**

<br/>

<table>
  <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="220" /></a>
    </td>
    <td width="40"></td>
    <td align="center">
      <img src="images/stanford-reap-logo.png" alt="Stanford REAP" width="320" />
    </td>
  </tr>
</table>

<sub><strong>Stanford REAP × CoPaper.AI</strong> · An academic–industrial AI toolkit for empirical research</sub>

<br/>

<table>
  <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-qrcode.png" alt="Visit copaper.ai" width="180" /></a><br/>
      <strong>Visit <a href="https://copaper.ai">copaper.ai</a></strong>
    </td>
    <td align="center">
      <img src="images/copaper-wechat.jpg" alt="CoPaper.AI WeChat" width="180" /><br/>
      <strong>WeChat: CoPaper.AI</strong>
    </td>
  </tr>
</table>

20 built-in methodology skills · 20-minute empirical paper · powered by <a href="https://github.com/brycewang-stanford/StatsPAI">StatsPAI</a> (900+ functions, MIT)

<br/>

Maintained by <a href="https://copaper.ai"><strong>CoPaper.AI</strong></a>, incubated at <a href="https://sccei.fsi.stanford.edu/reap"><strong>Stanford REAP / SCCEI</strong></a> · AI Assistant for Empirical Research

</div>
