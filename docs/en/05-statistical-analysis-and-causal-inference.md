# 05 - Statistical Analysis and Causal Inference

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  This is where CoPaper.AI's core capability sits. The 20 built-in methodology
  skills cover the full spectrum, from OLS basics to cutting-edge Double
  Machine Learning. Each skill is a structured step-by-step operating procedure
  — not a vague prompt, but a complete plan of "first run this check, then this
  model, output this table." One sentence triggers the workflow. Try it:
  https://copaper.ai
-->

> **There is only one core question in empirical research: when an RCT is impossible, how do we approximate its effect as closely as possible?** All non-experimental methods, at their core, do the same thing — search for a credible control group. The value of skills is this: they encode "what should a complete DID analysis include" so that you don't have to coax the AI each time.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> This stage is the main battlefield for AERS. The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). The CoPaper.AI methodology notes below serve as a "method map," and the table below is what you can run locally right now. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [⭐ `00` StatsPAI](../../skills/00-Full-empirical-analysis-skill_StatsPAI/) | Agent-native Python DSL; one `sp.causal(...)` runs DID/RD/IV/SCM/DML | One-stop causal analysis + automated robustness gating |
| [⭐ `00.2` Stata](../../skills/00.2-Full-empirical-analysis-skill_Stata/) · [⭐ `00.3` R](../../skills/00.3-Full-empirical-analysis-skill_R/) | `reghdfe` / `ivreg2` / `csdid` / `sdid` · `fixest` / `did` / `HonestDiD` | Replicate the same estimates and figures in Stata / R |
| [`10` causal-inference-mixtape](../../skills/10-Jill0099-causal-inference-mixtape/) | DID/IV/RDD/SCM templates (Cunningham) | Standardised templates for classical identification strategies |
| [`40` pyfixest](../../skills/40-py-econometrics-pyfixest/) | Python high-dimensional fixed-effects estimation at speed | Large-panel `reghdfe`-equivalent with clustered SEs |
| [`39` marginaleffects](../../skills/39-vincentarelbundock-marginaleffects/) | Predictions, slopes, and contrasts (R / Python) | Post-estimation marginal effects and heterogeneity interpretation |
| [`51` CausalPy](../../skills/51-pymc-labs-CausalPy/) | Bayesian quasi-experimental methods (PyMC Labs) | Bayesian DID/RD/SCM and uncertainty quantification |
| [`64` mcp-stata](../../skills/64-tmonk-mcp-stata/) | 20 Stata causal-inference and replication skills | Full causal-analysis workflow for Stata users |
| [⭐ `50` AER-skills](../../skills/50-brycewang-aer-skills/) | Top-5 submission stack: identification → robustness → R&R | Polish results to top-journal robustness standards |

---

## CoPaper.AI's 20 Built-In Methodology Skills

This is currently the most complete skill suite for empirical economic research, divided into four major categories:

### Foundational Regression Methods (6)

| Skill | Best for | Core workflow |
|-------|---------|---------|
| **OLS Regression** | The most basic linear regression | Progressive multi-specification comparison → heteroskedasticity test → robust standard errors |
| **Logit / Probit** | Binary dependent variable (yes/no, success/failure) | Model selection → marginal effects → goodness of fit |
| **Tobit Censored Regression** | Dependent variable with many zeros (R&D expenditure, donations) | Set the censoring point → estimate → marginal effects |
| **Panel Data Analysis** | Fixed effects / random effects | Hausman test → model selection → clustered standard errors |
| **GMM Dynamic Panel** | Dependent variable with a lagged term | Arellano-Bond / Blundell-Bond → AR test → Sargan test |
| **Descriptive Statistics** | Table 1 + correlation matrix | Variable description → mean-difference test → VIF for collinearity |

### Causal-Inference Methods (6)

| Skill | Best for | Core workflow |
|-------|---------|---------|
| **DID (Difference-in-Differences)** | The classic method for policy evaluation | Parallel-trends test → baseline regression → 4 robustness checks → heterogeneity analysis → mechanism analysis |
| **Staggered DID** | Different units treated at different times | Callaway-Sant'Anna / Sun-Abraham / de Chaisemartin newer methods |
| **IV Instrumental Variables** | Endogeneity | First-stage regression → weak-instrument test → 2SLS → overidentification test |
| **RDD Regression Discontinuity** | Exploiting discontinuity at a threshold | Bandwidth selection → local-polynomial estimation → density test → covariate balance |
| **PSM Propensity-Score Matching** | Building a comparable control group | Logit estimation → matching → balance test → ATT estimation |
| **Synthetic Control** | Policy evaluation with a single treated unit | Weight optimisation → fit test → placebo test |

### Frontier Methods + Mechanism Analysis (6)

| Skill | Best for | Core workflow |
|-------|---------|---------|
| **Double Machine Learning (DML)** | ML flexibly controls confounders | Cross-fitting → residualise → ATE/CATE estimation → heterogeneity analysis |
| **ML Predictive Modelling** | Classification / regression prediction | Multi-model comparison → hyperparameter tuning → cross-validation → feature importance |
| **Mediation Analysis** | Causal-mechanism test (X → M → Y) | Baron-Kenny → Sobel test → bootstrap confidence interval |
| **Heterogeneity Analysis** | Subgroup regression + interactions | Subsample analysis → interaction regression → between-group coefficient-difference test |
| **Heckman Selection Model** | Sample-selection-bias correction | Selection equation → corrected regression → Lambda significance |
| **Time Series / GARCH** | Volatility modelling | Stationarity test → ARIMA → GARCH → conditional volatility |

### Specialised Analysis Pipelines (2)

| Skill | Best for | Core workflow |
|-------|---------|---------|
| **Event Study** | Financial events + policy events | Event window → abnormal returns (CAR) / dynamic effects → significance test |
| **General Robustness-Check Template** | Applicable to all regression methods | A 6-category, 17-item robustness-check checklist |

### Internal Structure of Each Skill

A skill is not a vague prompt — it is a **structured step-by-step operating procedure**:

```yaml
---
name: did-analysis
description: Complete difference-in-differences causal-inference pipeline
category: methodology
target_agent: modeling
tags: [causal-inference, DID, panel-data]
---

## Preconditions
- Panel data, including unit ID, time, treatment-group indicator, treatment timing
- Outcome variable already defined

## Step 1: Parallel-Trends Test
- Plot the outcome variable's time trends for treatment and control groups
- Regress: are the interaction-term coefficients in the pre-treatment periods jointly zero?

## Step 2: Baseline Regression
- Progressive multi-specification: (1) no controls (2) with controls (3) with fixed effects
- Use save_table() to output the regression table

## Step 3: Robustness Checks (at least 4)
- Placebo test
- Replace the dependent variable
- Winsorisation / trimming
- Drop specific subsamples

## Step 4: Heterogeneity Analysis
...

## Step 5: Mechanism Analysis
...
```

---

## Other Statistical-Analysis Skills

### statistical-analysis

| Attribute | Description |
|------|------|
| **Source** | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) |
| **Function** | General statistical analysis; an essential data-analysis skill |
| **Install** | `npx skills add https://github.com/K-Dense-AI/claude-scientific-skills --skill statistical-analysis` |

### results-analysis (Experiment Result Analysis)

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | Rigorous statistical analysis + scientific visualisation + ablation studies |

### Data Scientist Agent

| Attribute | Description |
|------|------|
| **Source** | [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) |
| **Function** | Dedicated data-scientist agent; includes EDA, hypothesis testing, causal-inference methods (DID, RDD) |

### analysis-plan-generation (Analysis-Plan Generation)

| Attribute | Description |
|------|------|
| **Source** | [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) |
| **Function** | Auto-generate a statistical-analysis plan from a research question, with method-choice suggestions |

### simulation-study-design (Simulation Study Design)

| Attribute | Description |
|------|------|
| **Source** | [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) |
| **Function** | Monte-Carlo simulation design to evaluate finite-sample properties of estimators |

### stata-skill (Stata Expert)

| Attribute | Description |
|------|------|
| **Source** | [dylantmoore/stata-skill](https://github.com/dylantmoore/stata-skill) |
| **Function** | Write idiomatic Stata code: syntax, data management, econometrics, causal inference, graphics, Mata, 20+ community packages |
| **Coverage** | Panel data, time series, linear regression, limited-dependent-variable models, causal inference |

### stata-mcp (Stata MCP Server)

| Attribute | Description |
|------|------|
| **Source** | [SepineTam/stata-mcp](https://github.com/SepineTam/stata-mcp) |
| **Function** | Lets an LLM operate Stata directly through MCP for regression analysis, "from regression monkey to causal thinker" |
| **Highlight** | Paper replication, quick hypothesis testing, step-by-step econometrics teaching, code organisation, result interpretation |
| **Install** | `pip install stata-mcp` |

### stata-mcp (IDE Extension · OpenEcon)

| Attribute | Description |
|------|------|
| **Source** | [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp) |
| **License** | MIT · 414★ |
| **Function** | Stata-MCP extension for VS Code / Cursor / Antigravity: run `.do` files inside the editor, real-time output, data viewer, figure rendering |
| **Distinction** | Different project from `SepineTam/stata-mcp` (one is an IDE extension, the other a pip MCP server) |

### mcp-stata (MCP server + skills directory) ✅ Vendored

| Attribute | Description |
|------|------|
| **Source** | [tmonk/mcp-stata](https://github.com/tmonk/mcp-stata) → this repo [`skills/64-tmonk-mcp-stata`](../../skills/64-tmonk-mcp-stata/) |
| **License** | AGPL-3.0 (copyleft; preserves the original LICENSE as "aggregation"; no vendored Python/Rust server-side code) |
| **Function** | 20 SKILL.md files: `stata`, `stata-replication`, `stata-data-audit`, `stata-publication-qa`, `stata-modernize`, `stata-referee-response`, `stata-power-analysis`, `stata-causal-inference`, `stata-table-builder`, and more |
| **Highlight** | Replication-and-robustness audit closed loop aimed at empirical researchers; running the original server requires Stata 17+ and the official `pystata` (this repo only vendors the skill docs) |

### ipa-stata-template (IPA Reproducible-Research Template)

| Attribute | Description |
|------|------|
| **Source** | [PovertyAction/ipa-stata-template](https://github.com/PovertyAction/ipa-stata-template) |
| **License** | MIT |
| **Function** | Innovations for Poverty Action's reproducible Stata research template, including `.claude/skills/`: numbered pipeline, assertional defensive programming, LaTeX tables, `just`/`scons` automation |
| **Best for** | Development-economics / field-RCT reproducible project scaffolding |

### AEA replication-template (Top-Journal Replication-Package Template)

| Attribute | Description |
|------|------|
| **Source** | [AEADataEditor/replication-template](https://github.com/AEADataEditor/replication-template) |
| **Function** | AEA Data Editor's official replication-package template (Stata-based, `REPLICATION.md`) — the "gold standard" for economics replication |
| **Best for** | Packaging and self-checking AEA / top-journal replication packages |

### Posit Skills for R (R Language Official Skills)

| Attribute | Description |
|------|------|
| **Source** | [posit-dev/skills](https://github.com/posit-dev/skills) |
| **Function** | Posit's official Claude Skills: modern-r-tidyverse, predictive-modeling (tidymodels), quarto-authoring, shiny-bslib |
| **Install** | `/plugin install posit-dev@posit-dev-skills` |

### claude-code-r-skills (R Development Config)

| Attribute | Description |
|------|------|
| **Source** | [ab604/claude-code-r-skills](https://github.com/ab604/claude-code-r-skills) |
| **Function** | Claude Code configuration for R development, including statistical analysis and data-processing workflows |

### geospatial-analysis

| Attribute | Description |
|------|------|
| **Source** | K-Dense-AI / FastMCP |
| **Function** | GeoPandas geospatial analysis, PostGIS spatial queries, SRID transforms, spatial indexing |
| **Best for** | Urban economics, environmental economics, spatial econometrics |

### Economist Analyst

| Attribute | Description |
|------|------|
| **Source** | MCPMarket |
| **Function** | Apply classical / Keynesian / Austrian / behavioural economics principles for economic evaluation: supply-and-demand analysis, game theory, incentive structures |
| **Best for** | Policy analysis, behavioural-economics research |

---

## Causal-Inference Tool Ecosystem

### Python (PyWhy Ecosystem)

| Package | Function | Use case |
|---|------|---|
| [DoWhy](https://github.com/py-why/dowhy) | End-to-end causal-inference framework | Causal graph + potential-outcomes framework |
| [EconML](https://github.com/Microsoft/EconML) | Heterogeneous treatment-effect estimation | DML, causal forest, Meta-Learners |
| [CausalML](https://github.com/uber/causalml) | Uplift modelling + causal inference | A/B test optimisation, CATE |
| [causal-learn](https://github.com/py-why/causal-learn) | Causal-discovery algorithms | PC, FCI, GES |

### R Packages

| Package | Function |
|---|------|
| `fixest` | Fast fixed-effects estimation with multi-way FE and clustered SEs |
| `did` | Callaway & Sant'Anna staggered DID |
| `fect` | Factor-augmented counterfactual estimator |
| `grf` | Generalised random forests (causal forest) |
| `rdrobust` | Robust RDD estimation and inference |
| `MatchIt` | Propensity-score matching |
| `DoubleML` | Double Machine Learning |

### Stata 19 Highlights

| Feature | Command | Description |
|------|------|------|
| CATE | `cate` | Conditional average treatment effect |
| Weak-IV-robust inference | Anderson-Rubin | Reliable inference under weak instruments |
| HDFE | `absorb()` | High-dimensional fixed effects |
| Panel VAR | New | Panel vector autoregression |

---

## Practical Advice

1. **Don't skip descriptive statistics**: Table 1 is the first thing a reviewer sees. Use the descriptive-statistics skill to make sure your variable distributions are reasonable and your sample sizes are adequate.
2. **Robustness is not box-ticking**: there is a 6-category, 17-item robustness-check checklist — run at least 4 items. If the core conclusion holds across many tests, the reviewer has little to attack.
3. **Use the new tools for new methods**: if your data is staggered-treatment, by all means use Callaway-Sant'Anna or other new methods — don't use traditional TWFE; it has serious biases.
4. **DML is not a silver bullet**: DML's advantage is flexibility, but it requires enough sample size. For small samples, traditional parametric methods may be more reliable.

---

[← Previous chapter](04-data-acquisition-and-cleaning.md) | [Next chapter: 06 - Paper Writing →](06-paper-writing.md)