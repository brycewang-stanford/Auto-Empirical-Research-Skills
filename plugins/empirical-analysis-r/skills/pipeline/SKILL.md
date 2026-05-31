---
name: Full-empirical-analysis-skill-R
description: Classical end-to-end empirical analysis workflow in the modern tidyverse + econometrics R ecosystem — dplyr + tidyr + haven + fixest + sandwich + lmtest + clubSandwich + AER + ivreg + did + bacondecomp + HonestDiD + eventstudyr + rdrobust + rddensity + Synth + gsynth + synthdid + MatchIt + WeightIt + cobalt + ebal + grf + DoubleML + mediation + marginaleffects + modelsummary + kableExtra + gt + ggplot2 + ggpubr + cowplot + binsreg. **Defaults to economics empirical-paper style** (AER / QJE / AEJ) — every run produces a publication-ready output set with a multi-column regression table (M1→M6 progressive controls/FE) as the centerpiece, plus Table 1 (descriptives), mechanism / heterogeneity / robustness tables, and event-study + coefficient + trend figures. Covers the full 8-step R pipeline an applied economist runs on every paper — (1) data import & cleaning (read_dta/read_csv, naniar, janitor, validate-merges), (2) variable construction (mutate/across/winsorize/group_by + lag/lead with dplyr), (3) descriptive statistics & Table 1 (gtsummary, modelsummary::datasummary, tableone), (4) classical diagnostic tests (shapiro/jarque.bera.test/bptest/dwtest/bgtest/vif/adf.test/kpss.test/Hausman), (5) baseline modeling (fixest::feols, ivreg, did::att_gt, eventstudyr, sun_ab, did_imputation, synthdid, rdrobust, MatchIt, WeightIt, grf::causal_forest, DoubleML, mediation), (6) robustness battery (modelsummary stack, clubSandwich CRSE, fwildclusterboot, ri2, robomit Oster, bacondecomp, HonestDiD), (7) further analysis (interactions + marginaleffects, mediation::mediate, gsem via lavaan, dose-response splines, grf CATE), (8) publication-ready tables & figures (modelsummary, kableExtra, gt, stargazer, texreg, flextable to LaTeX/Word/HTML; ggplot2 + ggpubr + cowplot + binsreg + iplot for figures). **Also covers two parallel domain modes that share the same 8-step scaffolding** — **Mode A — Epidemiology / public health** (target-trial emulation, IPTW + g-formula + TMLE doubly-robust triplet via `WeightIt` / `gfoRmula` / `tmle` / `ltmle`, Mendelian randomization via `MendelianRandomization` / `TwoSampleMR` / `MRPRESSO`, KM / Cox / AFT / RMST survival via `survival` / `survminer` / `flexsurv`, E-value sensitivity via `EValue`, principal stratification — STROBE / TRIPOD reporting), and **Mode B — ML causal inference** (DML via `DoubleML`, S/T/X/R/DR meta-learners via `causalweight` / `grf`, causal forest via `grf::causal_forest`, BART/BCF via `bartCause` / `bcf`, matrix completion via `MCPanel`, CATE distribution + policy tree via `policytree`, off-policy evaluation, conformal causal via `conformalInference` / `cfcausal`, fairness audit via `fairmodels`, DAG learning via `pcalg` / `bnlearn` / LLM-assisted). Use when the user asks for a complete R empirical analysis, wants a tidyverse-style reproducible R script / Quarto workflow, prefers fixest over reghdfe, needs the R counterpart to StatsPAI / 00.1 / 00.2, or names a specific R step in isolation ("feols with cluster", "MatchIt nearest neighbor", "bacondecomp in R", "gtsummary table 1", "modelsummary to Word"). Mode A triggers on "target trial emulation R", "tmle ltmle", "MendelianRandomization", "TwoSampleMR", "MRPRESSO", "survival cox AFT", "STROBE R", "EValue R", "公共健康 R", "流行病学 R". Mode B triggers on "DoubleML R", "grf causal forest", "policytree", "bartCause bcf", "conformal causal R", "fairmodels", "pcalg NOTEARS", "因果机器学习 R".
triggers:
  - R empirical analysis
  - tidyverse econometrics workflow
  - reproducible R script
  - Quarto empirical pipeline
  - fixest feols feglm fepois
  - high-dimensional fixed effects R
  - clubSandwich cluster-robust
  - fwildclusterboot wild cluster bootstrap
  - ivreg AER 2SLS R
  - did att_gt Callaway SantAnna R
  - eventstudyr event study R
  - did_imputation Borusyak R
  - synthdid R package
  - bacondecomp R Goodman Bacon
  - HonestDiD R Rambachan Roth
  - rdrobust R
  - rddensity R
  - Synth gsynth R
  - MatchIt nearest neighbor R
  - WeightIt IPW propensity R
  - cobalt balance check R
  - ebal entropy balancing R
  - grf causal forest R
  - DoubleML R
  - mediation R Imai
  - marginaleffects R
  - gtsummary table 1
  - modelsummary publication table
  - kableExtra LaTeX
  - texreg stargazer
  - flextable Word
  - ggplot2 coefplot
  - iplot fixest
  - binsreg R
  - haven read_dta sav
  - janitor clean_names
  - naniar missing
  # Mode A — Epidemiology / public health
  - epidemiology pipeline R
  - public health causal inference R
  - target trial emulation R
  - g-formula R gfoRmula
  - IPTW marginal structural model R
  - WeightIt PSweight
  - tmle ltmle doubly robust
  - HAL-TMLE R
  - Mendelian randomization R
  - MendelianRandomization package
  - TwoSampleMR
  - MRPRESSO
  - MR-Egger weighted median R
  - STROBE TRIPOD reporting R
  - EValue sensitivity R
  - Kaplan-Meier AFT survival R
  - survival survminer flexsurv
  - 流行病学 R
  - 公共健康 R
  # Mode B — ML causal inference
  - ML causal inference R
  - DoubleML R
  - grf causal forest R
  - meta-learner S T X R DR R
  - causalweight R
  - bartCause bcf
  - Bayesian causal forest BCF R
  - CATE distribution R
  - policytree R
  - off-policy evaluation R
  - conformalInference cfcausal
  - conformal causal prediction R
  - fairmodels fairness audit
  - causal discovery PC NOTEARS R
  - pcalg bnlearn
  - 因果机器学习 R
---

# Full Empirical Analysis — Classical R Workflow

This skill is the *canonical* 8-step pipeline an applied economist runs on every empirical paper, written in the **modern tidyverse + econometrics R ecosystem** — `dplyr`/`tidyr`/`haven` for data, `fixest` as the panel/IV/DID workhorse, `did`/`bacondecomp`/`HonestDiD` for modern DID, `rdrobust`/`rddensity` for RD, `Synth`/`gsynth`/`synthdid` for synthetic control, `MatchIt`/`WeightIt`/`cobalt`/`ebal` for matching, `grf`/`DoubleML` for ML causal, `mediation` for causal mediation, `marginaleffects` for post-estimation, `modelsummary`/`kableExtra`/`gt` for publication tables, `ggplot2`/`iplot`/`binsreg` for figures.

**Companion skills**: this is the R sibling of `00-StatsPAI_skill` (Python DSL), `00.1-Full-empirical-analysis-skill` (explicit Python), and `00.2-Full-empirical-analysis-skill_Stata` (Stata `.do`). All four implement the same 8 steps, in their respective ecosystems.

## Philosophy

1. **Tidyverse + fixest, the modern R idioms.** `feols(... | unit + year, cluster = ~unit)`, not Frankenstein-y `lm(y ~ x + factor(unit) + factor(year))`.
2. **Reproducible scripts / Quarto.** Every example below is paste-runnable. `renv` for package locking; `Quarto` (`.qmd`) for combined narrative + code + tables/figures.
3. **8 steps, first-class.** R users historically over-invest in Step 5; this skill treats Steps 1–4 and 6–8 as core.
4. **Rich outputs.** Every step yields at least one table or figure — tex/docx/png/pdf.
5. **Progressive disclosure.** `SKILL.md` gives the canonical call per step; [`references/`](references/) holds variant-specific depth.

---

## Three domain modes (default = AER econ; alternates = epi & ML-causal)

The default playbook above is **AER-style applied econometrics** — the AEA convention: written-out estimating equation, identifying assumption, design horse-race, full robustness gauntlet. The skill **also** ships two parallel sub-pipelines for the other two big causal-inference traditions, each reusing the same Steps 1–4 (cleaning / construction / Table 1 / diagnostics) and Step 8 (tables/figures) — only Step 5 (estimator) and Step 6/7 swap packages:

| Mode | Reader convention | Step-5 estimator stack | Reporting stack | Jump to |
|---|---|---|---|---|
| **Default — Applied Econ (AER / QJE / AEJ)** | "Show the equation + identifying assumption + design horse-race; controls visible; clustered SE" | DID / IV / RD / SCM / matching / `fixest::feols` HDFE | AER house-style multi-column `modelsummary` + `kableExtra` / `gt` / `flextable` + 8-section paper layout | Steps 1 → 8 (entire playbook below) |
| **Mode A — Epidemiology / Public Health** | "STROBE / TRIPOD-AI; target trial protocol; doubly-robust estimand; absolute & relative risk; KM survival" | Target-trial emulation · IPTW (`WeightIt` / `PSweight`) · g-formula (`gfoRmula`) · TMLE (`tmle` / `ltmle`) · Mendelian randomization (`MendelianRandomization` / `TwoSampleMR` / `MRPRESSO`) · KM / Cox / AFT (`survival` / `survminer` / `flexsurv`) | Same `modelsummary` + risk-difference / hazard-ratio / E-value rows | §A. Epidemiology pipeline |
| **Mode B — ML Causal Inference** | "DML / meta-learners / causal forest / DR-learner; CATE distribution; policy value" | DML (`DoubleML`) · S/T/X/R/DR-Learner (`causalweight` / `grf`) · GRF causal forest (`grf::causal_forest`) · BART/BCF (`bartCause` / `bcf`) · matrix completion (`MCPanel`) | `modelsummary` ML horse-race + `grf` CATE plot + policy-value table + `conformalInference` PI | §B. ML causal pipeline |

**How to invoke a non-default mode** (Claude / agent picks this up from the user's wording):

| User says... | Mode the skill switches to |
|---|---|
| "Run a DID / IV / RD / event study", "AER table", "applied micro" | Default (AER econ) — Steps 1 → 8 |
| "Target trial emulation", "g-formula", "IPTW", "TMLE", "Mendelian randomization", "STROBE / TRIPOD", "公共健康 / 流行病学", "epi pipeline", "RWE study", "cohort study", "case-control" | Mode A (Epi) — §A |
| "DML", "double machine learning", "causal forest", "meta-learner", "CATE", "BCF", "policytree", "policy learning", "conformal causal", "fairness audit", "ML causal", "uplift modeling", "因果机器学习" | Mode B (ML causal) — §B |
| "Mix" (e.g. "estimate DID + then ML CATE on the heterogeneity") | Default + Mode B in sequence — every estimator yields a coefficient + SE pair, drop them all into one `modelsummary(...)` for the horse-race column |

The three modes share **the same Step 1–4 cleaning / Table 1 / diagnostics scaffolding, the same Step 8 export stack, and the same DAG-first identification logic** — switching modes only changes which Step-5 estimator family you reach for, not the surrounding paper structure. If you only want descriptive stats / Table 1 / a balance check, the AER `gtsummary::tbl_summary` / `modelsummary::datasummary_balance` calls in Step 3 work identically across all three modes.

---

## Default Output Spec — Economics Empirical Paper

This skill defaults to the **applied-economics paper convention**. Unless the user explicitly asks for a single point estimate, every run produces the full publication-ready output set below. Treat it as the contract of Step 8 — **mandatory**, not opt-in.

### Required tables (always produced)

| # | Table | R source | Saves to |
|---|---|---|---|
| **T1** | Summary statistics & balance (treated vs control, with SMD / p-values) | `gtsummary::tbl_summary` + `add_p` + `add_difference` (Step 3) | `tables/table1_balance.xlsx` + `.docx` + `.tex` |
| **T2** ★ | **Main results — multi-column regression M1→M6** (progressive controls + FE) | `fixest::feols` × 6 specs → `modelsummary` (Step 5–6) | `tables/table2_main.xlsx` + `.docx` + `.tex` |
| **T3** | Mechanism / outcome ladder — same treatment, 3+ outcomes side-by-side | loop `feols` over `y ∈ {Y1, Y2, Y3, Y_main}` → `modelsummary` (Step 7) | `tables/table3_mechanism.xlsx` + `.docx` + `.tex` |
| **T4** | Heterogeneity — subgroup × main coef (gender, age, region, …) | subgroup `feols` × `linearHypothesis` → `modelsummary` (Step 7) | `tables/table4_heterogeneity.xlsx` + `.docx` + `.tex` |
| **T5** | Robustness battery — alt SE / cluster / sample / placebo, in **one** table | `feols` × variants → `modelsummary` (Step 6) | `tables/table5_robustness.xlsx` + `.docx` + `.tex` |

> **★ Table 2 is the centerpiece of every economics paper.** It is the multi-column regression table that walks the reader from raw correlation (M1) to the fully-specified design (M6: 2-way FE + interacted FE + cluster-robust SE). Do **not** collapse it into a single column. Do **not** report only the headline coefficient. The progression *is* the credibility argument: if M1→M6 is monotone and stable, the design is plausibly identifying; if it collapses on adding FE, that *is* the result.
>
> **Canonical 6 columns, in order:**
> 1. **M1** raw bivariate (`feols(y ~ treat, data)`)
> 2. **M2** + demographics (`+ age + edu`)
> 3. **M3** + sector controls (`+ tenure / firm_size`)
> 4. **M4** + unit FE (`| worker_id`)
> 5. **M5** + 2-way FE (`| worker_id + year`)
> 6. **M6** + interacted FE (`| worker_id + year + industry^year`) with `cluster = ~ worker_id`

### Required figures (always produced)

| # | Figure | R source | Saves to |
|---|---|---|---|
| **F1** | Trend / motivation — treated vs control over time, with policy line | `dplyr` group means → `ggplot + geom_line` (Step 3) | `figures/fig1_trend.png` (300 dpi, **必须导出 PNG**) + `.pdf` |
| **F2** | Event-study coefficients with 95% CI, base period at –1 | `fixest::sunab()` / `did::ggdid` / `iplot` (Step 5) | `figures/fig2_event_study.png` (300 dpi, **必须导出 PNG**) + `.pdf` |
| **F3** | Coefficient plot across specs M1→M6 | `modelsummary::modelplot()` (Step 8) | `figures/fig3_coefplot.png` (300 dpi, **必须导出 PNG**) + `.pdf` |
| **F4** | Robustness / sensitivity — `bacondecomp::bacon` plot, `HonestDiD::createSensitivityPlot`, or spec curve | scenario-specific (Step 6) | `figures/fig4_sensitivity.png` (300 dpi, **必须导出 PNG**) + `.pdf` |

### Output file layout (default)

```
project/
├── tables/    table1_balance.xlsx/.docx/.tex  table2_main.xlsx/.docx/.tex
│              table3_mechanism.xlsx/.docx/.tex table4_heterogeneity.xlsx/.docx/.tex
│              table5_robustness.xlsx/.docx/.tex
└── figures/   fig1_trend.png(300dpi)+.pdf      fig2_event_study.png(300dpi)+.pdf
               fig3_coefplot.png(300dpi)+.pdf   fig4_sensitivity.png(300dpi)+.pdf
```

**关键输出规则（必须遵守）：**
- **图片格式**：所有图片必须同时导出 **PNG 格式（≥300 dpi）** 和 PDF 格式（用于 LaTeX 排版）
- **表格格式**：所有回归表格必须同时导出 **Excel（.xlsx）**、**Word（.docx）** 和 **LaTeX（.tex）** 三种格式
- PNG 用于幻灯片、Markdown 文档、邮件等场景；PDF 用于学术论文排版

### When to deviate

- **Single quick estimate** — produce only the relevant cell, but warn that the standard deliverable is the full set above and offer to run it.
- **Design does not support a figure** (cross-section → no event study) — skip with a printed `message()` explaining why; do **not** silently drop.
- **N=1 treated unit (`Synth` / `synthdid`)** — replace F1/F2 with the SCM trajectory + placebo distribution; T1–T5 still apply.

---

## Required packages

```r
# Run once on a fresh R install:
install.packages(c(
  # Data
  "tidyverse", "haven", "readxl", "data.table", "janitor",
  "naniar", "VIM", "mice", "validate",
  # Description / tables
  "gtsummary", "tableone", "modelsummary", "kableExtra", "gt",
  "stargazer", "texreg", "flextable", "psych", "summarytools",
  # Tests
  "lmtest", "sandwich", "car", "tseries", "urca", "plm",
  "clubSandwich", "fwildclusterboot",
  # Modeling — workhorses
  "fixest",                                        # panel/IV/DID with HD FE — primary
  "AER",                                           # ivreg
  "ivreg",                                         # alternative IV
  # Modern DID
  "did",                                           # Callaway–Sant'Anna
  "didimputation",                                 # Borusyak–Jaravel–Spiess
  "fixest",                                        # sunab() for Sun–Abraham
  "synthdid",                                      # Synthetic DID
  "bacondecomp", "HonestDiD",
  "DIDmultiplegtDYN",                              # de Chaisemartin–D'Haultfœuille
  # RD
  "rdrobust", "rddensity", "rdmulti",
  # Synthetic control
  "Synth", "gsynth", "tidysynth",
  # Matching / weighting
  "MatchIt", "WeightIt", "cobalt", "ebal",
  # ML causal
  "grf", "DoubleML",
  # Mediation / SEM
  "mediation", "lavaan",
  # Robustness / inference
  "robomit",                                       # Oster delta
  "ri2", "ritools",                                # randomization inference
  "multcomp",
  # Margins / post-estimation
  "marginaleffects",
  # Plotting
  "ggplot2", "ggpubr", "cowplot", "patchwork",
  "binsreg",
  "ggdist", "ggrepel"
))
# fixest's iplot, esttex, etable are bundled.
```

---

## The 8 Steps — Canonical Pipeline (mapped to AER paper sections)

```
┌──────────────────────────────────────────────────────────────────────┐
│ Step −1 Pre-Analysis Plan (PAP)  pwr / WebPower / DeclareDesign      │
│ Step 0  Sample log + data contract sample_log/stopifnot/jsonlite     │
│ Step 1  Data import & cleaning   read_csv/read_dta/janitor/naniar/mice│
│ Step 2  Variable construction    mutate/across/winsorize/lag/group_by │
│ Step 2.5 Empirical strategy      equation × ID assumption + pre-reg  │
│ Step 3  Descriptive statistics   gtsummary/datasummary_balance/cor_pmat│
│ Step 3.5 Identification graphics iplot/binsreg/rdplot/cobalt/Synth   │
│ Step 4  Diagnostic tests         shapiro/bptest/dwtest/vif/adf/kpss   │
│ Step 5  Baseline modeling        feols/ivreg/att_gt/synthdid/MatchIt  │
│ Step 6  Robustness battery       bacondecomp/HonestDiD/fwildclusterboot│
│ Step 7  Further analysis         marginaleffects/mediation/grf        │
│ Step 8  Tables & figures         modelsummary/iplot/ggplot2/cowplot   │
└──────────────────────────────────────────────────────────────────────┘
```

The 8 steps mirror the canonical sections of an applied AER / QJE / AEJ paper. Each step is one paper section and emits a paper-ready artifact on disk:

```
Paper section               Step  R moves
─────────────────────────── ───── ────────────────────────────────────────────────
Pre-Analysis Plan           −1    pwr / WebPower / DeclareDesign + freeze pap.json
§1. Data                     0    sample_log + 5-check stopifnot → JSON via jsonlite
§1. Data                     1    haven::read_dta · janitor::clean_names · naniar/mice
§1. Data                     2    mutate/across/Winsorize/lag/lead/diff · CPI deflate
§1.1 Descriptives (Table 1)  3    gtsummary::tbl_summary · datasummary_balance
§2. Empirical Strategy       2.5  write equation + ID assumption → strategy.md
§3. Identification graphics  3.5  fixest::iplot · binsreg · rdplot · cobalt::love.plot · Synth
§3.5 Diagnostics             4    bptest · dwtest · car::vif · urca::ur.df · phtest
§4. Main Results (Table 2)   5    fixest::feols progressive (m1...m6) · modelsummary
§5. Heterogeneity (Table 3)  7    feols(... + i(.):X) · marginaleffects::avg_slopes
§6. Mechanisms / Channels    7    mediation::mediate · lavaan · outcome ladder
§7. Robustness gauntlet      6    bacondecomp · HonestDiD · robomit · fwildclusterboot · ri2
§8. Replication package      8    modelsummary("...tex") · gt → docx · result.json
```

Below is the canonical call at each step. **All examples share one running narrative** — labor-econ panel where `training` (treatment) affects `log_wage` (outcome), with covariates `age`, `edu`, `tenure`, panel keys `worker_id`/`firm_id`/`year`. Variable names and parameter values are **illustrative**.

> **When a step has many variants** (5 staggered-DID estimators; 4 hetero tests), SKILL.md shows the one you reach for first; deeper variants live in `references/NN-<topic>.md`.

---

## Paper-ready figure & table inventory (what to produce by section)

A modern AER paper has **5–7 figures** and **3–5 main tables** + an appendix robustness table. Every step below leaves at least one numbered artifact on disk. Default file names assume parallel `.tex` / `.docx` / `.xlsx` exports (the agent should produce all three so co-authors can edit in Word, the build system can use LaTeX, and editors can edit raw numbers in Excel). **所有图片必须同时保存 PNG（≥300 dpi）和 PDF 两种格式。**

| § | Artifact | R primitive | Filenames |
|---|---|---|---|
| §1 | **Figure 1**: raw trends / treatment rollout | `df %>% group_by(year, treat) %>% summarise(mean(y)) %>% ggplot()` | `figures/fig1_trend.png`(300dpi)+`.pdf` |
| §1 | **Table 1**: summary stats (full / treated / control + Δ + SMD) | `gtsummary::tbl_summary` · `modelsummary::datasummary_balance` | `tables/table1_balance.xlsx/.docx/.tex` |
| §3 | **Figure 2**: identification graphic (event-study / first-stage / McCrary / RD scatter / SCM trajectory) | `fixest::iplot(es)` · `binsreg` · `rdrobust::rdplot` · `rddensity` · `Synth::path.plot` | `figures/fig2_event_study.png`(300dpi)+`.pdf` |
| §4 | **Table 2**: main results — progressive controls M1→M6 | `modelsummary(list("(1)"=m1,...,"(6)"=m6))` · `fixest::etable` | `tables/table2_main.xlsx/.docx/.tex` |
| §4 | **Table 2-bis**: design horse-race (OLS / IV / DID / DML) | `modelsummary(list("OLS"=ols, "2SLS"=iv, "CS-DID"=cs, "DML"=dml))` | `tables/table2b_designs.xlsx/.docx/.tex` |
| §4 | **Figure 3**: coefficient plot across specs | `modelplot(list(m1,...,m6), coef_map="training")` | `figures/fig3_coefplot.png`(300dpi)+`.pdf` |
| §5 | **Table 3**: heterogeneity by subgroup | `modelsummary(g_full, g_male, g_fem, g_q1, ..., g_q4)` | `tables/table3_heterogeneity.xlsx/.docx/.tex` |
| §5 | **Figure 4**: dose-response / CATE | `marginaleffects::plot_predictions` · `grf::plot.causal_forest` | `figures/fig4_cate.png`(300dpi)+`.pdf` |
| §6 | **Table 4**: mechanism / outcome ladder | loop `feols` over outcomes → `modelsummary` | `tables/table4_mechanism.xlsx/.docx/.tex` |
| §7 | **Table A1**: robustness master (one column per check) | `modelsummary(list(base, no99, balpan, dropearly, wfe, cl2way, logy, ihsy, psm, ebal))` | `tables/tableA1_robustness.xlsx/.docx/.tex` |
| §7 | **Figure 5**: spec curve | `specr::specr()` + `plot_specs` (or hand-rolled `purrr::pmap`) | `figures/fig5_spec_curve.png`(300dpi)+`.pdf` |
| §7 | **Figure 6**: sensitivity (HonestDiD / Oster / E-value) | `HonestDiD::createSensitivityPlot` · `robomit::o_test` · `EValue` | `figures/fig6_sensitivity.png`(300dpi)+`.pdf` |
| §8 | **Replication bundle**: all tables in one document | `modelsummary(..., output="docx")` · `gt::gtsave()` · Quarto / Rmd | `replication/paper_tables.xlsx/.docx/.tex` |

> Every R estimator above (`fixest::feols` / `AER::ivreg` / `did::att_gt` / `grf::causal_forest` / `synthdid_estimate`) returns a result object that can be passed straight into `modelsummary(...)` / `modelplot(...)` / `etable(...)`. Don't hand-roll LaTeX from `kable()`, and don't render Word via `flextable` directly — `modelsummary`, `etable`, and `gtsummary` apply book-tab borders, AER stars, and the right SE label automatically. For deeper export recipes, see [`references/08-tables-plots.md`](references/08-tables-plots.md).

---

## Export cookbook — LaTeX / Word / Excel in one block

**关键规则（必须遵守）：每个表格必须同时导出三种格式——Excel(.xlsx)、Word(.docx)、LaTeX(.tex)。每个图片必须同时保存PNG(≥300dpi)和PDF两种格式。**

R has the **best** publication-table ecosystem of the three languages. Three tiers, picked by **scope**:

| Tier | Use when | API | Hot args |
|---|---|---|---|
| **1. Single multi-column table** | Exporting *one* Table 2 / Table 3 / Table A1 with progressive columns | `modelsummary(list("(1)"=m1,...,"(N)"=mN), output="tables/tab.tex", stars=c("*"=.1,"**"=.05,"***"=.01), gof_omit="BIC|AIC|F|Log", coef_map=c(...))` — or `fixest::etable(m1,...,mN, file="tab.tex")` for `feols`-only | `coef_map=`, `gof_omit=`, `stars=`, `notes=`, `output= "latex"/"docx"/"xlsx"/"markdown"`, `add_rows=` |
| **2. Multi-panel paper format** (Tables 2 + 3 + A1 + A2 in one file) | Producing the *paper-tables block* — main + heterogeneity + robustness + placebo as a single document | `modelsummary` chained with `gt::gt_group()` for one document with section headers, OR Quarto `.qmd` rendering multiple `modelsummary` calls between prose | `gt_group(modelsummary(...), modelsummary(...))` · `quarto render paper.qmd` |
| **3. Full session bundle** (the Stata `collect` / Python `Stargazer + pylatex` equivalent) | Replication appendix that mixes summary stats + balance + multiple regression tables + headings + prose in **one** file | **Quarto** is the modern R-native answer. `master.qmd` interleaves prose + chunks that emit `modelsummary` / `gtsummary` / `ggplot2` outputs; one `quarto render` produces .pdf / .docx / .html | YAML front matter sets `format: [pdf, docx, html]` for triple-target output |

**Journal styling — pick the right `stars` and SE label.** The AEA convention is `c("*"=.1, "**"=.05, "***"=.01)` and `notes = "Cluster-robust standard errors in parentheses..."`. Define a wrapper once at the top of `master.R`:

```r
# Top of master.R — journal house-style wrapper
# 输出三格式：.xlsx（编辑）、.docx（Word）、.tex（LaTeX）
aer_table <- function(models, output, headers = NULL, coef_map = NULL) {
  base <- tools::file_path_sans_ext(output)
  for (ext in c(".xlsx", ".docx", ".tex")) {
    output_file <- paste0(base, ext)
    fmt <- if (ext == ".xlsx") "html" else if (ext == ".docx") "docx" else "latex"
    modelsummary(
      models,
      output    = output_file,
      stars     = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
      gof_omit  = "BIC|AIC|F|Log|Adj",
      coef_map  = coef_map,
      notes     = paste("Cluster-robust standard errors in parentheses.",
                        "* p<0.10, ** p<0.05, *** p<0.01."),
      output_format = fmt
    )
  }
}
```

For the multi-panel `.docx` / `.xlsx` and Quarto cookbook (single-file paper-tables bundle), see [`references/08-tables-plots.md`](references/08-tables-plots.md).

---

## Step −1 — Pre-Analysis Plan (pre-data; AEA RCT Registry style)

Before touching the data, write down (a) the population, (b) the design, (c) the **minimum detectable effect (MDE)** under the planned sample size and α=0.05, β=0.20. Persist the result as `pap.json` so a referee can verify the design was powered before, not after, the data were seen.

```r
library(pwr)         # classical power calculations
library(WebPower)    # cluster RCT, longitudinal, mixed designs
library(jsonlite)

# Two-sample MDE for a continuous outcome (Cohen's d framing)
pwr.t.test(d = 0.20, power = 0.80, sig.level = 0.05,
           type = "two.sample", alternative = "two.sided")
# → required n per arm

# Solve for MDE given fixed n
pwr.t.test(n = 2000, power = 0.80, sig.level = 0.05,
           type = "two.sample")$d
# → minimum detectable Cohen's d

# Cluster-randomized RCT — design effect
# Solve via WebPower::wp.crt2arm(...) for clusters / per-cluster size / power triangle
WebPower::wp.crt2arm(f = 0.20, J = NULL, n = 50, icc = 0.05, power = 0.80,
                     alpha = 0.05, alternative = "two.sided")
# → required clusters per arm

# DID power (Frison-Pocock / Bloom 1995): use WebPower::wp.kanova() or simulate
# RD power: simulate via DeclareDesign — see references/05-modeling.md §5.5

# Persist the protocol — referee will ask whether design was powered ex ante
pap <- list(
  population        = "manufacturing workers, 2010–2020",
  treatment         = "training (binary, staggered adoption)",
  outcome           = "log_wage",
  estimand          = "ATT",
  design            = "staggered DID, Callaway-Sant'Anna",
  alpha             = 0.05,
  power_target      = 0.80,
  mde_d             = 0.20,
  n_planned         = 12000,
  frozen_at         = "2026-01-15T09:00:00Z",
  git_sha           = "<paste>"
)
write_json(pap, "artifacts/pap.json", pretty = TRUE, auto_unbox = TRUE)
```

For richer DAG-aware power analysis (write down the DAG, declare estimands, simulate the design), use **`DeclareDesign`** — it is the R-native equivalent of EGAP's pre-analysis flow.

Commit `artifacts/pap.json` in the repo **before** Step 1. AEA RCT Registry / OSF preregistration tools accept it as the analysis-plan exhibit.

---

## Step 0 — Sample-construction log & 5-check data contract

An AER §1 *Data* section has three jobs: (a) describe sources, (b) document **every** sample restriction (the "footnote 4" sample log), (c) lock the panel structure.

### 0.1 Sample-construction log (footnote 4)

```r
library(tidyverse); library(jsonlite)

sample_log <- tibble::tibble(step = character(), n = integer())

df_raw <- read_dta("raw/panel.dta") %>% janitor::clean_names()
sample_log <- sample_log %>% add_row(step = "0. raw",                    n = nrow(df_raw))

df1 <- df_raw %>% drop_na(wage)
sample_log <- sample_log %>% add_row(step = "1. drop missing wage",       n = nrow(df1))

df2 <- df1 %>% filter(between(age, 18, 65))
sample_log <- sample_log %>% add_row(step = "2. drop age outside 18-65",  n = nrow(df2))

df3 <- df2 %>% filter(industry %in% c("manuf", "construction", "transport"))
sample_log <- sample_log %>% add_row(step = "3. keep target industries",  n = nrow(df3))

df <- df3
print(sample_log)
write_json(sample_log, "artifacts/sample_construction.json", pretty = TRUE)
```

Paste the printed tibble verbatim as footnote 4 of the paper.

### 0.2 Five-check data contract (go / no-go gate)

```r
library(validate); library(assertr)

data_contract <- function(df, y, treatment, id = NULL, time = NULL, covariates = c()) {
  keys <- c(y, treatment, id, time, covariates)
  contract <- list(
    n_obs            = nrow(df),                                            # 1. shape
    dtypes           = sapply(df[keys], function(x) class(x)[1]),           # 2. dtypes
    n_missing        = sapply(df[keys], function(x) sum(is.na(x))),         # 3. missingness
    n_dupes_on_keys  = if (!is.null(id) && !is.null(time))
                         sum(duplicated(df[, c(id, time)])) else 0,          # 4. duplicates
    panel_balanced   = NULL,
    cohort_sizes     = NULL
  )

  if (!is.null(id) && !is.null(time)) {
    bal <- df %>% count(.data[[id]])
    contract$panel_balanced <- all(bal$n == max(bal$n))                      # 5. balance
    contract$n_dropped_by_balance <- sum(bal$n != max(bal$n))

    if ("first_treat" %in% names(df)) {
      contract$cohort_sizes <- df %>% distinct(.data[[id]], .keep_all = TRUE) %>%
                                count(first_treat) %>% deframe()
    }
  }

  contract$y_range         <- range(df[[y]],         na.rm = TRUE)
  contract$treatment_share <- mean(df[[treatment]],  na.rm = TRUE)

  # MCAR sniff test (Rubin) — if missing(y) is associated with covariates,
  # listwise deletion biases the estimate. Use mice / IPW instead.
  miss_y <- is.na(df[[y]])
  contract$mcar_hint <- "likely MCAR (listwise OK)"
  if (any(miss_y) && any(!miss_y)) {
    for (cov in covariates) {
      if (is.numeric(df[[cov]])) {
        p <- t.test(df[[cov]][miss_y], df[[cov]][!miss_y])$p.value
        if (p < 0.05) {
          contract$mcar_hint <- sprintf("NOT MCAR (y-miss differs on %s, p=%.3f) → use mice / IPW",
                                         cov, p)
          break
        }
      }
    }
  }
  contract
}

contract <- data_contract(df, y = "wage", treatment = "training",
                          id = "worker_id", time = "year",
                          covariates = c("age", "edu", "tenure"))

stopifnot(contract$n_dupes_on_keys == 0)
stopifnot(all(contract$n_missing == 0))

write_json(contract, "artifacts/data_contract.json",
           pretty = TRUE, auto_unbox = TRUE)
```

If any `stopifnot` fires, **stop** and fix it in `dplyr` first. R estimators silently drop NA rows downstream — this contract is the cheapest insurance against "why did N drop from 12,000 to 9,800 between Table 1 and Table 2?" referee questions.

---

### Step 1 — Data import & cleaning

Deeper patterns: [references/01-data-cleaning.md](references/01-data-cleaning.md) — every format (`haven`/`readxl`/`data.table::fread`/`arrow::read_parquet`/`DBI`), `janitor::clean_names`, `naniar` missingness viz, MCAR/MAR/MNAR triage with `mice`, validation with `validate`/`assertr`, panel structure checks.

```r
library(tidyverse)
library(haven)        # .dta / .sav / .sas7bdat
library(janitor)      # clean_names()
library(naniar)       # missing-data viz
library(skimr)        # one-line dataset summary

# 1a. Load + first look
df <- read_dta("raw/panel.dta") %>%
  clean_names()                       # standardize to snake_case

skim(df)                              # rich one-line-per-var summary
naniar::miss_var_summary(df)
naniar::vis_miss(df)                  # missingness heatmap

# 1b. Dtypes
df <- df %>%
  mutate(
    year   = as.integer(year),
    wage   = as.numeric(wage),
    gender = as.factor(gender),
    date   = as.Date(date)
  )

# 1c. Missing values — decide PER VARIABLE
key_vars <- c("wage", "training", "worker_id", "year")
df <- df %>%
  drop_na(all_of(key_vars))
cat("After dropping NA on keys:", nrow(df), "rows\n")

df <- df %>%
  mutate(
    tenure_missing = is.na(tenure),
    tenure         = if_else(is.na(tenure), median(tenure, na.rm = TRUE), tenure),
    union          = fct_explicit_na(as.factor(union), na_level = "unknown")
  )

# 1d. Outliers — flag, don't drop yet
df <- df %>%
  mutate(wage_z = scale(wage)[,1],
         outlier_z4 = abs(wage_z) > 4)
cat("|z|>4 on wage:", sum(df$outlier_z4, na.rm = TRUE), "\n")

# 1e. Deduplicate panel key
stopifnot(nrow(df %>% distinct(worker_id, year)) == nrow(df))

# 1f. Merge with assertion
firm_chars <- read_dta("raw/firm_chars.dta")
n_before <- nrow(df)
df <- df %>%
  left_join(firm_chars, by = "firm_id", relationship = "many-to-one")
stopifnot(nrow(df) == n_before)       # no row inflation

# 1g. Panel structure
df %>% count(year)                    # per-year
df %>% count(worker_id) %>% summary() # per-unit
```

**Key principle**: `dplyr` + explicit `stopifnot()` assertions. No silent row drops downstream.

---

### Step 2 — Variable construction & transformation

Deeper patterns: [references/02-data-transformation.md](references/02-data-transformation.md) — log/IHS/Box–Cox via `MASS::boxcox`, group winsorization with `dplyr`, `scale()` and `bestNormalize`, factor handling, lag/lead with `dplyr::lag`, panel timing.

```r
library(DescTools)        # Winsorize()

df <- df %>%
  mutate(
    # 2a. Log / IHS
    log_wage   = log(pmax(wage, 1)),
    ihs_assets = asinh(assets),

    # 2b. Winsorize 1/99
    wage_w1 = DescTools::Winsorize(wage, probs = c(0.01, 0.99), na.rm = TRUE),

    # 2c. Standardize
    age_std = as.numeric(scale(age)),

    # 2d. Polynomial / interaction (or use formula syntax in fixest)
    age_sq        = age^2,
    trt_x_edu     = training * edu
  ) %>%

  # 2e. Within-group winsorize
  group_by(industry, year) %>%
  mutate(wage_w1_iy = DescTools::Winsorize(wage, probs = c(0.01, 0.99),
                                           na.rm = TRUE)) %>%
  ungroup() %>%

  # 2f. Panel operators (always arrange first to make lag deterministic)
  arrange(worker_id, year) %>%
  group_by(worker_id) %>%
  mutate(
    log_wage_l1 = lag(log_wage, 1),
    log_wage_f1 = lead(log_wage, 1),
    d_log_wage  = log_wage - lag(log_wage, 1),
    wage_mean_i = mean(log_wage, na.rm = TRUE),
    log_wage_dm = log_wage - wage_mean_i
  ) %>%
  ungroup() %>%

  # 2g. Staggered-DID timing
  group_by(worker_id) %>%
  mutate(first_treat = ifelse(any(training == 1),
                              min(year[training == 1]), NA_real_)) %>%
  ungroup() %>%
  mutate(rel_time      = year - first_treat,
         never_treated = is.na(first_treat))

# 2h. CPI deflation
cpi <- read_csv("raw/cpi.csv")
df <- df %>%
  left_join(cpi, by = "year") %>%
  mutate(cpi_base = cpi[year == 2010][1],
         wage_real     = wage * cpi_base / cpi,
         log_wage_real = log(pmax(wage_real, 1)))
```

---

### Step 2.5 — Empirical strategy (write the equation + identifying assumption)

This is the heart of an AER paper. **Before any code**, write down the equation explicitly and state the identifying assumption. Vague identification language is the single most common reason a referee rejects an applied paper. Persist the strategy as `strategy.md` so it is a dated, version-controlled artifact — *not* a post-hoc rationalization written after seeing the coefficient.

#### Equation × identifying assumption × R estimator (decision table)

| Design | Estimating equation | Identifying assumption | R estimator |
|---|---|---|---|
| 2×2 DID | `Y_it = α_i + λ_t + β·D_it + X'γ + ε_it` | parallel trends conditional on X | `feols(y ~ i(treated, post, ref=0) | i + t, data, cluster = ~i)` |
| Event-study (CS / SA) | `Y_it = α_i + λ_t + Σ_{e≠-1} β_e · 1{t-G_i = e} + ε_it` | no anticipation + group-time PT | `feols(y ~ sunab(G, t) | i + t)` · `did::att_gt` · `didimputation::did_imputation` |
| 2SLS | `Y_i = α + β·D_i + X'γ + ε_i;  D_i = π·Z_i + X'δ + u_i` | exclusion + relevance + monotonicity | `feols(y ~ X | D ~ Z, data)` · `AER::ivreg` · `ivreg::ivreg` |
| Sharp RD | `Y_i = α + β·1{X_i ≥ c} + f(X_i) + ε_i` (local poly) | continuity of E[Y(0)\|X] at c, no manipulation | `rdrobust::rdrobust(y, x, c=0)` (+ `rddensity`) |
| SCM | `Ŷ_1t(0) = Σ_j ŵ_j Y_jt`, τ_t = `Y_1t − Ŷ_1t(0)` for t≥T_0 | pre-period fit + interpolation validity | `Synth::synth` · `gsynth::gsynth` · `synthdid::synthdid_estimate` · `tidysynth` |
| Selection-on-observables (matching/IPW/DML) | `Y_i = m(X_i) + β·D_i + ε_i` (Robinson partialling-out) | unconfoundedness + overlap | `MatchIt::matchit` + `lm` · `WeightIt` · `DoubleML::DoubleMLPLR` · `grf::causal_forest` |

#### Design picker (when the user is unsure)

```
                 ┌─ running var + cutoff ───────────────── RDD       (rdrobust)
                 │
                 ├─ exogenous instrument Z ─────────────── IV/2SLS   (feols  / AER::ivreg)
data + question ─┤
                 ├─ pre/post × treat/control ─┬ 2 periods  ── 2×2 DID (feols + i())
                 │                            └ staggered  ── CS / SA / BJS  (att_gt / sunab / did_imputation)
                 │
                 ├─ 1 treated unit + donor pool + long pre ── SCM    (Synth / gsynth / synthdid)
                 │
                 ├─ high-dim X, selection-on-observables ── ML causal (DoubleML / grf — see §B)
                 │
                 └─ none of the above ──────────────────── matching + sensitivity (MatchIt + EValue)
```

#### Pre-registration `strategy.md` template

```r
strategy <- "\\
# Empirical Strategy (pre-registration)

**Frozen**: 2026-01-15  (Git SHA: <paste>)
**Population**: manufacturing workers, 2010–2020, balanced panel
**Treatment**: training (binary, staggered adoption)
**Outcome**:   log_wage (CPI-deflated 2010 USD)
**Estimand**:  ATT on the treated, dynamic horizon -4..+4

## Estimating equation (paste from §2.5 row that matches the design)

  log_wage_it = α_i + λ_t + Σ_{e≠-1} β_e · 1{t - G_i = e} + ε_it

## Identifying assumption

1. No anticipation:   E[Y_it(0) | t < G_i] = E[Y_it(0) | never-treated]
2. Group-time PT:     Δ E[Y_it(0)] is the same across treatment cohorts

## Auto-flagged threats (must defend in §2)

- Selection of G_i on Y_i(0)              → bacondecomp + HonestDiD sensitivity
- Spillover within firm                    → cluster at firm_id, also try firm_id × year
- Anticipation in pre-period               → include lead in event study

## Fallback estimators (Step 6 robustness)

- Sun–Abraham via `feols(y ~ sunab(G, t) | i + t, data)`
- Borusyak-Jaravel-Spiess via `didimputation::did_imputation`
- Synthetic DID via `synthdid::synthdid_estimate`
"
writeLines(strategy, "artifacts/strategy.md")
```

Commit `artifacts/strategy.md` in the repo **before** running Step 5 / Step 6. The `git log` of this file *is* the analysis plan.

---

### Step 3 — Descriptive statistics & Table 1

Deeper patterns: [references/03-descriptive-stats.md](references/03-descriptive-stats.md) — `gtsummary::tbl_summary` (the modern Table 1 standard), `modelsummary::datasummary_balance` with SMDs, `tableone::CreateTableOne`, correlation matrices with significance via `corrplot` / `psych::corr.test`, distribution plots via `ggplot2`.

```r
library(gtsummary)
library(modelsummary)

# 3a. Full-sample summary — one line, publication ready
df %>%
  select(log_wage, age, edu, tenure, training) %>%
  datasummary_skim()

# Or
df %>%
  select(log_wage, age, edu, tenure, training) %>%
  tbl_summary(
    type  = list(all_continuous() ~ "continuous2"),
    statistic = all_continuous() ~ c("{N_nonmiss}", "{mean} ({sd})",
                                      "{min} – {median} – {max}")
  ) %>%
  bold_labels() %>%
  as_kable_extra() %>%
  kableExtra::save_kable("tables/table1_full.tex")

# 3b. Stratified Table 1 (treated vs control, with SMDs + p-values)
df %>%
  select(log_wage, age, edu, tenure, female, training) %>%
  tbl_summary(by = training, missing = "ifany") %>%
  add_p() %>%
  add_difference() %>%
  add_n() %>%
  modify_header(label = "**Variable**") %>%
  bold_labels() %>%
  as_gt() %>%
  gt::gtsave("tables/table1_balance.html")

# Or via modelsummary (writes LaTeX/Word/HTML)
datasummary_balance(~ training,
                    data = df %>% select(training, age, edu, tenure, female),
                    output = "tables/table1_balance.tex")

# 3c. Correlation matrix with stars
library(corrplot); library(psych)
corr_obj <- corr.test(df %>% select(log_wage, age, edu, tenure, training),
                       method = "pearson")
corrplot(corr_obj$r, method = "color", type = "upper",
         p.mat = corr_obj$p, sig.level = 0.05, insig = "blank",
         addCoef.col = "black", number.cex = 0.7,
         tl.col = "black", tl.srt = 45,
         col = colorRampPalette(c("#B2182B","white","#2166AC"))(200))

# 3d. Distribution plots
library(ggplot2)
p1 <- ggplot(df, aes(log_wage, fill = factor(training))) +
  geom_density(alpha = 0.5) +
  scale_fill_manual(values = c("0" = "darkred", "1" = "navy"),
                    labels = c("Control", "Treated"), name = "") +
  labs(x = "Log wage", y = "Density",
       title = "Log-wage density by treatment") +
  theme_classic()

p2 <- ggplot(df, aes(sample = log_wage)) +
  stat_qq() + stat_qq_line() +
  labs(title = "Normal Q-Q") + theme_classic()

cowplot::plot_grid(p1, p2, labels = "auto") %>%
  ggsave("figures/distributions.pdf", plot = ., width = 10, height = 4)

# 3e. Time-trend (DID motivation)
df %>%
  group_by(year, training) %>%
  summarise(mean_log_wage = mean(log_wage, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(year, mean_log_wage, color = factor(training))) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  geom_vline(xintercept = policy_year, linetype = "dashed") +
  scale_color_manual(values = c("0" = "darkred", "1" = "navy"),
                     labels = c("Control","Treated"), name = "") +
  labs(x = "Year", y = "Mean log wage") + theme_classic()
ggsave("figures/trend_did.pdf", width = 7, height = 4)
```

---

### Step 3.5 — Identification graphics (Section "Identification, graphical evidence")

**AER convention: the identification figure precedes the regression table.** The reader should see graphical evidence that PT holds / first stage is strong / RD jumps cleanly *before* you ask them to trust your point estimate.

#### 3.5.1 Event-study figure + numerical pre-trends test (DID identification)

Pre-period coefficients ≈ 0 (with the −1 reference period normalized to zero) is the visual evidence for parallel trends. Pair the **figure** with a **numerical** pre-trends test so reviewers don't have to eyeball it.

```r
library(fixest); library(ggplot2)

# (a) Sun-Abraham via fixest::sunab — the modern primary for staggered DID
es <- feols(log_wage ~ sunab(first_treat, year) | worker_id + year,
            data = df, cluster = ~ worker_id)

# (b) Coefficient figure
iplot(es,
      xlab = "Years relative to treatment",
      ylab = "Coefficient (ATT, 95% CI)",
      main = "Figure 2a. Event-study coefficients (95% CI; ref. e = -1)")
ggsave("figures/fig2a_event_study.pdf", width = 7, height = 4)
ggsave("figures/fig2a_event_study.png", width = 7, height = 4, dpi = 300)

# (c) Numerical pre-trends Wald test (joint zero on the leads)
pre_idx <- grep("year::-", names(coef(es)))[!grepl("ref", names(coef(es)))]
W <- wald(es, names(coef(es))[pre_idx])
cat(sprintf("Pre-trends Wald χ² = %.2f, p = %.3f\n", W$stat, W$p))

# (d) Bacon decomposition (Goodman-Bacon 2021) — TWFE diagnostic
library(bacondecomp)
bd <- bacon(log_wage ~ training, data = df,
            id_var = "worker_id", time_var = "year")
ggplot(bd, aes(weight, estimate, color = type, shape = type)) +
  geom_point(size = 2) +
  labs(title = "Figure 2a-bis. Goodman-Bacon decomposition",
       x = "Weight", y = "Estimate")
ggsave("figures/fig2a_bacon.pdf", width = 7, height = 4)

# (e) Callaway-Sant'Anna dynamic ATT (when att_gt is the main estimator)
library(did)
cs <- att_gt(yname = "log_wage", tname = "year", idname = "worker_id",
             gname = "first_treat", data = df,
             control_group = "nevertreated", est_method = "dr",
             clustervars = "firm_id")
ggdid(aggte(cs, type = "dynamic")) +
  labs(title = "Figure 2a-ter. Dynamic ATT (Callaway-Sant'Anna)")
ggsave("figures/fig2a_csdid.pdf", width = 7, height = 4)
```

#### 3.5.2 First-stage F-statistic + scatter (IV identification)

Rule of thumb: first-stage F ≥ 10 for OLS-style inference; F ≥ 23 for AR-equivalent inference (Stock–Yogo / Lee 2022). `fixest::feols` reports F automatically; `AER::ivreg` requires `summary(..., diagnostics = TRUE)`.

```r
iv <- feols(log_wage ~ age + edu | training ~ Z1 + Z2,
            data = df, cluster = ~ firm_id)
summary(iv, stage = 1)
fitstat(iv, ~ ivf + ivwald + sargan + cd)        # CD / KP / Sargan / first-stage F

# Binscatter for the first-stage scatter (residualized on age + edu)
library(binsreg)
binsreg(y = df$training, x = df$Z1, w = df[, c("age","edu")],
        nbins = 20, polyreg = 2, ci = c(3, 3))
ggsave("figures/fig2b_first_stage.pdf", width = 7, height = 4)
```

#### 3.5.3 RD: McCrary density + canonical RD plot

The signature RD figure is `rdplot` (CCT-style binned scatter with local-polynomial fit on each side), paired with the McCrary manipulation test.

```r
library(rdrobust); library(rddensity)

# (a) Canonical RD plot — binned means + local poly on each side
rdplot(y = df$outcome, x = df$running_var, c = 0,
       p = 4, kernel = "triangular", binselect = "esmv",
       title = "Figure 2c. RD plot")
ggsave("figures/fig2c_rdplot.pdf", width = 7, height = 4)

# (b) McCrary density (Cattaneo-Jansson-Ma 2018)
rdd <- rddensity(X = df$running_var, c = 0)
print(summary(rdd))
rdplotdensity(rdd, X = df$running_var,
              title = "Figure 2c-bis. McCrary density (manipulation test)")
ggsave("figures/fig2c_mccrary.pdf", width = 7, height = 4)
```

#### 3.5.4 Matching: love plot (standardized differences pre vs post)

```r
library(MatchIt); library(cobalt)

m.out <- matchit(training ~ age + edu + tenure + firm_size,
                 data = df, method = "nearest", ratio = 1)
love.plot(m.out, threshold = 0.10,
          var.order = "unadjusted", abs = TRUE,
          title = "Figure 2d. Love plot — |SMD| pre vs post matching")
ggsave("figures/fig2d_loveplot.pdf", width = 7, height = 4)
```

#### 3.5.5 SCM: synthetic-control trajectory + gap plot

For synthetic-control designs the canonical Figure 2 is the treated-vs-synthetic time series with treatment time annotated.

```r
library(tidysynth)
sc <- df %>%
  synthetic_control(outcome = log_wage, unit = unit_id, time = year,
                    i_unit = "treated_unit_name", i_time = 2015) %>%
  generate_predictor(time_window = 2010:2014,
                     mean_age = mean(age, na.rm = TRUE),
                     mean_edu = mean(edu, na.rm = TRUE)) %>%
  generate_weights() %>% generate_control()
plot_trends(sc); ggsave("figures/fig2e_synth_trajectory.pdf", width = 7, height = 4)
plot_differences(sc); ggsave("figures/fig2e_synth_gap.pdf", width = 7, height = 4)

# Synthetic DID
library(synthdid)
sdid_setup <- panel.matrices(df, unit = "worker_id", time = "year",
                              outcome = "log_wage", treatment = "training")
sdid_fit <- synthdid_estimate(sdid_setup$Y, sdid_setup$N0, sdid_setup$T0)
plot(sdid_fit, control.name = "Synthetic DiD")
ggsave("figures/fig2e_sdid.pdf", width = 7, height = 4)
```

> Identification-specific checks (PT for DID, weak-IV F, density for RD, common support for matching) **are also auto-run inside the Step-5 estimators** — don't duplicate the numerics here, but DO produce the figures: a referee scans the figures first.

---

### Step 4 — Diagnostic statistical tests

Deeper patterns: [references/04-statistical-tests.md](references/04-statistical-tests.md) — every classical test. `lmtest`/`sandwich`/`car`/`tseries`/`urca`/`plm`.

```r
library(lmtest)
library(sandwich)
library(car)
library(tseries)
library(urca)

# Fit baseline OLS for diagnostics
ols <- lm(log_wage ~ training + age + edu + tenure, data = df)

# 4a. Normality of residuals
shapiro.test(sample(residuals(ols), min(5000, length(residuals(ols)))))
tseries::jarque.bera.test(residuals(ols))

# 4b. Heteroskedasticity
bptest(ols)                                  # Breusch-Pagan
bptest(ols, ~ I(fitted(ols)^2) + ., data = df)  # White-style

# 4c. Autocorrelation (time series / panel)
dwtest(ols)                                   # Durbin-Watson
bgtest(ols, order = 4)                        # Breusch-Godfrey
Box.test(residuals(ols), lag = 8, type = "Ljung-Box")

# Panel-specific
library(plm)
pdata <- pdata.frame(df, index = c("worker_id", "year"))
plm_fe  <- plm(log_wage ~ training + age + edu, data = pdata, model = "within")
pbgtest(plm_fe)                               # Wooldridge serial correlation
pcdtest(plm_fe, test = "cd")                  # Pesaran cross-sectional dependence

# 4d. Multicollinearity
vif(ols)                                       # VIFs
kappa(model.matrix(ols), exact = TRUE)         # condition number

# 4e. Stationarity (time series — assumes a single y over time)
adf.test(df$log_wage, k = 4)                   # ADF
kpss.test(df$log_wage, null = "Level")         # KPSS

# 4f. Hausman (FE vs RE)
plm_re <- plm(log_wage ~ training + age + edu, data = pdata, model = "random")
phtest(plm_fe, plm_re)

# 4g. Specification — RESET
resettest(ols, power = 2:3, type = "fitted")
```

**Decision table**:

| Test | Null | Action if rejected |
|------|------|--------------------|
| `shapiro.test` / `jarque.bera.test` | residuals Normal | bootstrap CIs if N small |
| `bptest` | homoskedastic | use HC3 via `coeftest(ols, vcov = vcovHC(ols, "HC3"))` or cluster |
| `dwtest` / `bgtest` | no autocorr | HAC SEs (`vcovHAC`) or cluster by unit |
| `pbgtest` (panel) | no panel autocorr | cluster by entity |
| `pcdtest` | no CSD | Driscoll–Kraay (`vcovDC`) |
| `vif` > 10 | — | drop / combine |
| ADF rejects + KPSS doesn't | stationary | levels |
| ADF doesn't reject | unit root | first-difference |
| `phtest` | RE consistent | use FE |

---

### Step 5 — Baseline empirical modeling (Section 4: Main Results)

Deeper patterns: [references/05-modeling.md](references/05-modeling.md) — every estimator. `fixest` is the workhorse.

This is the densest section of an applied paper. A modern AER §4 typically contains **2–3 multi-regression tables and one coefficient plot**:

- **Table 2** (main): progressive controls, 4–6 columns — **Pattern A** below
- **Table 2-bis** (design horse race): same coefficient under OLS / IV / DID / DML — **Pattern B**
- **Table 2-ter** (multi-outcome): same treatment, several outcomes side-by-side — **Pattern C**
- **Figure 3** (coefplot): visual summary of β̂ and 95% CI across specs

> **Estimator routing** (memorize this — getting it wrong silently produces nonsense):
> - **No FE / single low-card FE** → `feols(y ~ X, data, cluster = ~i)`
> - **High-dim FE** → `feols(y ~ X | fe1 + fe2, data, cluster = ~i)`
> - **Two-way cluster** → `feols(..., cluster = ~ firm_id + year)`
> - **2SLS / IV** → `feols(y ~ X | D ~ Z, data, cluster = ~ firm_id)` (or `AER::ivreg` for diagnostics)
> - **DID / event-study** → `feols(y ~ sunab(G, t) | i + t, data)` (SA) · `did::att_gt` (CS) · `didimputation::did_imputation` (BJS)

**Pick by identification strategy**:

```
Cross-section, selection on observables  →  feols  |  MatchIt + lm  |  WeightIt
Panel + policy shock + parallel trends   →  feols / did::att_gt / sunab / didimputation / synthdid
Exogenous instrument                     →  feols(... | endog ~ z)  |  AER::ivreg
Discontinuity                            →  rdrobust + rddensity + rdmc
N=1 treated, long panel                  →  Synth / gsynth / synthdid
Selection on observables + heterogeneity →  WeightIt + cobalt; grf::causal_forest
Binary outcome                           →  feglm or glm(family=binomial)
Count outcome                            →  fepois
```

Canonical calls (the eight patterns A–H below are the AER table cookbook — `modelsummary(...)` and `fixest::etable(...)` are the two workhorses, equivalent to Stata `outreg2`/`esttab` and Python `pf.etable`/`Stargazer`).

#### 5.A Pattern A — Progressive controls (the canonical Table 2)
Stable β̂ across columns ⇒ less concern that selection on observables is driving the estimate (Oster 2019 selection-stability logic; quantified in Step 6).

```r
library(fixest); library(modelsummary)

m1 <- feols(log_wage ~ training,                                                 data = df, cluster = ~ firm_id)
m2 <- feols(log_wage ~ training + age + edu,                                     data = df, cluster = ~ firm_id)
m3 <- feols(log_wage ~ training + age + edu + tenure + firm_size,                data = df, cluster = ~ firm_id)
m4 <- feols(log_wage ~ training + age + edu + tenure + firm_size | industry + year,
            data = df, cluster = ~ firm_id)
m5 <- feols(log_wage ~ training + age + edu + tenure + firm_size | worker_id + year,
            data = df, cluster = ~ firm_id)
m6 <- feols(log_wage ~ training + age + edu + tenure + firm_size | worker_id + year + industry^year,
            data = df, cluster = ~ firm_id)

modelsummary(
  list("(1) Baseline"    = m1,
       "(2) +Demog"      = m2,
       "(3) +Labor-mkt"  = m3,
       "(4) Ind×Yr FE"   = m4,
       "(5) Worker FE"   = m5,
       "(6) Worker FE+Ind×Yr" = m6),
  output    = "tables/table2_main.tex",
  stars     = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  gof_omit  = "BIC|AIC|F|Log|Adj",
  coef_map  = c("training" = "Job training",
                "age" = "Age", "edu" = "Education",
                "tenure" = "Tenure", "firm_size" = "Firm size"),
  notes     = c("Cluster-robust SE in parentheses, clustered at firm_id.",
                "* p<0.10, ** p<0.05, *** p<0.01.")
)
modelsummary(list("(1)"=m1,"(2)"=m2,"(3)"=m3,"(4)"=m4,"(5)"=m5,"(6)"=m6),
             output = "tables/table2_main.docx")
```

> **AER convention: show ALL controls (and the intercept).** Pass NEITHER `keep =` NOR `coef_omit =` so every parameter is visible. Use `coef_map = c("training" = "Training")` (single mapping) only when a focal-coefficient-only table is intentional (interaction-form heterogeneity, IV first-stage triplet); use `coef_omit = "Intercept"` only when you want to suppress the constant for paper aesthetics.

#### 5.B Pattern B — Design horse race (Table 2-bis)
Show the same coefficient of interest under multiple identification strategies. This is *the* AER credibility move: convergent evidence across designs each making different identifying assumptions.

```r
library(fixest); library(AER); library(did); library(MatchIt); library(WeightIt)

ols  <- feols(log_wage ~ training + age + edu + tenure | industry + year,
              data = df, cluster = ~ firm_id)
iv   <- feols(log_wage ~ age + edu + tenure | training ~ Z1 + Z2,
              data = df, cluster = ~ firm_id)
cs   <- att_gt(yname = "log_wage", tname = "year", idname = "worker_id",
                gname = "first_treat", data = df,
                control_group = "nevertreated", est_method = "dr",
                clustervars = "firm_id")
psm  <- matchit(training ~ age + edu + tenure, data = df,
                method = "nearest", ratio = 1)
psm_lm <- lm(log_wage ~ training + age + edu + tenure,
             data = match.data(psm), weights = weights)
ebal <- weightit(training ~ age + edu + tenure, data = df, method = "ebal")
ebal_lm <- lm(log_wage ~ training + age + edu + tenure,
              data = df, weights = ebal$weights)

modelsummary(
  list("(1) OLS+FE"     = ols,
       "(2) 2SLS"       = iv,
       "(3) CS-DID"     = aggte(cs, type = "simple"),
       "(4) PSM"        = psm_lm,
       "(5) Entropy bal." = ebal_lm),
  output    = "tables/table2b_designs.tex",
  stars     = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map  = c("training" = "Job training (β̂)"),
  gof_omit  = "BIC|AIC|F|Log|Adj",
  notes     = "Convergent evidence: same β̂ under five identification strategies."
)
```

#### 5.C Pattern C — Multi-outcome table (same X, several Y's)

```r
ys <- c("log_wage", "weeks_employed", "left_firm", "promoted")
multi_y <- lapply(ys, function(y)
  feols(as.formula(paste(y, "~ training + age + edu + tenure | industry + year")),
        data = df, cluster = ~ firm_id))
names(multi_y) <- ys

modelsummary(multi_y,
             output = "tables/table2c_multi_outcome.tex",
             stars  = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
             coef_map = c("training" = "Training"),
             notes  = "Each column is a separate regression on the labelled outcome.")
```

#### 5.D Pattern D — Stacked Panel A / Panel B table
Same model family, two horizons (short-run / long-run) or two samples. Use `gt::gt_group()` to stack two `modelsummary` blocks with panel headers.

```r
library(gt)

panelA <- list(
  "(1) Industry FE" = feols(wage_t1 ~ training + X | industry + year,  data = df, cluster = ~ firm_id),
  "(2) Worker FE"   = feols(wage_t1 ~ training + X | worker_id + year, data = df, cluster = ~ firm_id))
panelB <- list(
  "(1) Industry FE" = feols(wage_t5 ~ training + X | industry + year,  data = df, cluster = ~ firm_id),
  "(2) Worker FE"   = feols(wage_t5 ~ training + X | worker_id + year, data = df, cluster = ~ firm_id))

ms_A <- modelsummary(panelA, output = "gt") %>%
  tab_header(title = "Panel A. Short-run (1 year)")
ms_B <- modelsummary(panelB, output = "gt") %>%
  tab_header(title = "Panel B. Long-run (5 years)")

gt_group(ms_A, ms_B) %>%
  gtsave("tables/table2d_horizons.tex")
gt_group(ms_A, ms_B) %>%
  gtsave("tables/table2d_horizons.docx")
```

#### 5.E Pattern E — IV reporting triplet (first-stage / reduced-form / 2SLS)
The textbook AER IV table presents the **first stage**, the **reduced form**, and the **2SLS** in three columns so the reader can verify Wald-ratio = RF / FS.

```r
fs  <- feols(training ~ Z + age + edu | industry + year, data = df, cluster = ~ firm_id)
rf  <- feols(log_wage ~ Z + age + edu | industry + year, data = df, cluster = ~ firm_id)
iv2 <- feols(log_wage ~ age + edu | training ~ Z, data = df, cluster = ~ firm_id)

modelsummary(
  list("(1) First stage"   = fs,
       "(2) Reduced form"  = rf,
       "(3) 2SLS"          = iv2),
  output     = "tables/table2e_iv_triplet.tex",
  stars      = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map   = c("Z" = "Instrument Z", "training" = "Training (endog.)"),
  gof_map    = list(list(raw = "ivf", clean = "First-stage F", fmt = 2)),
  notes      = "Wald ratio: $\\hat\\beta_{2SLS} = \\hat\\beta_{RF} / \\hat\\pi_{FS}$."
)
```

> **IV triplet is intentionally focal:** show only Z + endogenous regressor so the reader can eyeball the Wald ratio. Drop `coef_map=` only if a referee asks for the full coefficient list.

#### 5.F Pattern F — Causal-orchestrator main via `did::att_gt` / `synthdid` / `grf::causal_forest`
For DID / SCM / matching / forest mains, the modern R estimator returns a self-contained estimate + automatic placebos / pre-trends / overlap diagnostics. Pipe into `modelsummary` via the auto-tidiers.

```r
# CS-DID with full diagnostics
cs <- att_gt(yname = "log_wage", tname = "year", idname = "worker_id",
             gname = "first_treat", data = df,
             control_group = "nevertreated", est_method = "dr",
             clustervars = "firm_id")
print(aggte(cs, type = "group"))                           # ATT(g) summary
print(aggte(cs, type = "dynamic", min_e = -4, max_e = 4))  # event-study aggregation

# Synthetic DID
library(synthdid)
sdid_setup <- panel.matrices(df, unit="worker_id", time="year",
                              outcome="log_wage", treatment="training")
sdid_fit <- synthdid_estimate(sdid_setup$Y, sdid_setup$N0, sdid_setup$T0)
print(summary(sdid_fit))

# Causal forest with overlap + variable importance
library(grf)
cf <- causal_forest(X = as.matrix(df[, c("age","edu","tenure","firm_size")]),
                    Y = df$log_wage, W = df$training, num.trees = 4000)
average_treatment_effect(cf, target.sample = "treated")
test_calibration(cf)
variable_importance(cf)
```

#### 5.G Pattern G — Subgroup `modelsummary` (Table 3, see Step 7)
One column per subgroup. Detailed code in §Step 7 — Heterogeneity.

#### 5.H Pattern H — Robustness master (Table A1, see Step 6)
Stack every robustness specification next to the baseline. Detailed code in §Step 6.

---

#### Canonical estimator commands (the underlying primitives)

```r
library(fixest)

# 5a. OLS with cluster-robust SEs — feols is the modern primary
ols <- feols(log_wage ~ training + age + edu + tenure,
             data = df, cluster = ~ firm_id)
summary(ols)

# 5b. Two-way FE — single line
fe <- feols(log_wage ~ training + age + edu + tenure | worker_id + year,
            data = df, cluster = ~ worker_id)

# Multi-way clustering
fe_mw <- feols(log_wage ~ training | worker_id + year,
               data = df, cluster = ~ worker_id + firm_id)

# High-dim interaction FE
fe_hd <- feols(log_wage ~ training | worker_id + industry^year,
               data = df, cluster = ~ firm_id)

# 5c. 2×2 DID
did22 <- feols(log_wage ~ i(treated, post, ref = 0) + age + edu,
               data = df, cluster = ~ worker_id)

# Or with absorbed FE:
did22 <- feols(log_wage ~ i(treated, post, ref = 0) | worker_id + year,
               data = df, cluster = ~ worker_id)

# 5d. Event study — base period at -1
es <- feols(log_wage ~ i(rel_time, ref = -1) | worker_id + year,
            data = df %>% filter(!is.na(first_treat)),
            cluster = ~ worker_id)
iplot(es,
      xlab = "Years relative to treatment",
      main = "Event study")

# 5e. Staggered DID — modern estimators (see references/05-modeling.md §5.4)
library(did)
cs <- att_gt(yname = "log_wage", tname = "year", idname = "worker_id",
             gname = "first_treat", data = df,
             control_group = "nevertreated",
             est_method = "dr",
             clustervars = "firm_id")
ggdid(cs)                                     # event-study plot

# Sun & Abraham via fixest::sunab
sa <- feols(log_wage ~ sunab(first_treat, year) | worker_id + year,
            data = df, cluster = ~ worker_id)
iplot(sa, sub.title = "Sun-Abraham (2021)")

# Borusyak–Jaravel–Spiess (didimputation)
library(didimputation)
bjs <- did_imputation(data = df, yname = "log_wage", gname = "first_treat",
                      tname = "year", idname = "worker_id",
                      horizon = 0:5, pretrends = -5:-1,
                      cluster_var = "worker_id")

# Synthetic DID
library(synthdid)
sdid_setup <- synthdid::panel.matrices(df, unit = "worker_id", time = "year",
                                        outcome = "log_wage", treatment = "training")
sdid_fit <- synthdid_estimate(sdid_setup$Y, sdid_setup$N0, sdid_setup$T0)

# 5f. IV / 2SLS
iv <- feols(log_wage ~ age + edu | training ~ draft_lottery + z2,
            data = df, cluster = ~ firm_id)
summary(iv, stage = 1)
fitstat(iv, ~ ivf + ivwald + sargan)         # first-stage F + Wald + overid

# Or via AER:
library(AER)
iv_aer <- ivreg(log_wage ~ training + age + edu |
                 draft_lottery + z2 + age + edu, data = df)
summary(iv_aer, vcov. = sandwich, diagnostics = TRUE)

# 5g. Sharp RD
library(rdrobust); library(rddensity)
rd <- rdrobust(y = df$outcome, x = df$running_var, c = 0,
               kernel = "triangular", bwselect = "mserd")
summary(rd)
rdplot(y = df$outcome, x = df$running_var, c = 0)
rddensity(X = df$running_var, c = 0)         # manipulation test

# 5h. Binary outcome
logit <- feglm(employed ~ training + age + edu | firm_id + year,
               data = df, family = binomial(link = "logit"),
               cluster = ~ firm_id)
library(marginaleffects)
avg_slopes(logit, variables = "training")    # AME

# 5i. Count w/ HD FE
pois <- fepois(citations ~ training + age | firm_id + year,
               data = df, cluster = ~ firm_id)
```

---

### Step 6 — Robustness battery

Deeper patterns: [references/06-robustness.md](references/06-robustness.md) — `modelsummary` for M1–M6; `clubSandwich`/`fwildclusterboot`; `bacondecomp`/`HonestDiD`/`robomit`; `ri2` randomization inference.

```r
library(modelsummary)
library(fixest)

# 6a. Progressive specs (M1 → M6)
m1 <- feols(log_wage ~ training, data = df, cluster = ~ firm_id)
m2 <- feols(log_wage ~ training + age + edu, data = df, cluster = ~ firm_id)
m3 <- feols(log_wage ~ training + age + edu + tenure | worker_id,
            data = df, cluster = ~ worker_id)
m4 <- feols(log_wage ~ training + age + edu + tenure | worker_id + year,
            data = df, cluster = ~ worker_id)
m5 <- feols(log_wage ~ training + age + edu + tenure | worker_id + year + region,
            data = df, cluster = ~ worker_id)
m6 <- feols(log_wage ~ training + age + edu + tenure | worker_id + year + industry^year,
            data = df, cluster = ~ worker_id)

modelsummary(list("(1)" = m1, "(2)" = m2, "(3)" = m3,
                  "(4)" = m4, "(5)" = m5, "(6)" = m6),
             stars = c('*' = .1, '**' = .05, '***' = .01),
             gof_omit = "BIC|AIC|F|Log",
             coef_map  = c("training" = "Training",
                           "age" = "Age", "edu" = "Education", "tenure" = "Tenure"),
             output = "tables/table_main.tex")

# 6b. Alternative cluster levels
for (cl in c("worker_id", "firm_id", "industry", "state")) {
  fit <- feols(log_wage ~ training | worker_id + year, data = df,
               cluster = as.formula(paste0("~", cl)))
  cat(cl, ":  b=", coef(fit)["training"], "  se=", se(fit)["training"], "\n")
}

# 6c. Wild cluster bootstrap (when few clusters)
library(fwildclusterboot)
boot <- boottest(m4, param = "training", clustid = "state",
                 B = 9999, seed = 42)
summary(boot)

# 6d. Subsample splits
splits <- list(
  "Female=0"     = df %>% filter(female == 0),
  "Female=1"     = df %>% filter(female == 1),
  "Young (<40)"  = df %>% filter(age < 40),
  "Old (>=40)"   = df %>% filter(age >= 40)
)
sub_fits <- imap(splits, ~ feols(log_wage ~ training | worker_id + year,
                                  data = .x, cluster = ~ worker_id))
modelsummary(sub_fits, stars = TRUE)

# 6e. Placebo — fake timing
df_placebo <- df %>%
  mutate(fake_first = first_treat - 3,
         fake_post  = year >= fake_first) %>%
  filter(year < first_treat)
feols(log_wage ~ fake_post | worker_id + year,
      data = df_placebo, cluster = ~ worker_id)

# 6f. Randomization inference
library(ri2)
ri_out <- conduct_ri(formula = log_wage ~ training + age + edu,
                     declaration = randomizr::declare_ra(N = nrow(df),
                                                          prob = mean(df$training)),
                     assignment = "training",
                     sharp_hypothesis = 0,
                     data = df,
                     sims = 1000)
summary(ri_out); plot(ri_out)

# 6g. TWFE bias diagnosis
library(bacondecomp)
bacon_out <- bacon(log_wage ~ training,
                   data = df, id_var = "worker_id", time_var = "year")
ggplot(bacon_out, aes(weight, estimate, color = type)) + geom_point()
ggsave("figures/bacon.pdf")

# 6h. Parallel-trends sensitivity
library(HonestDiD)
honest_out <- createSensitivityResults(betahat = es$coefficients,
                                       sigma = vcov(es),
                                       numPrePeriods = 5, numPostPeriods = 5,
                                       Mbarvec = seq(0, 0.5, by = 0.05))
createSensitivityPlot(honest_out, originalResults = honest_out$mainResult)
ggsave("figures/honestdid.pdf")

# 6i. Oster (2019) δ*
library(robomit)
o_test(y = "log_wage", x = "training",
       con = "age + edu + tenure | worker_id + year",
       id = "worker_id", time = "year",
       data = df, R2max = 1.3 * fitstat(m6, "r2"), beta = 0)

# ============================================================
# 6j. Pattern H — Robustness master table (Table A1, one column per check)
# ============================================================
library(modelsummary); library(MatchIt); library(WeightIt)

base       <- feols(log_wage ~ training + age + edu + tenure | industry + year,
                    data = df, cluster = ~ firm_id)
no99       <- feols(log_wage ~ training + age + edu + tenure | industry + year,
                    data = df %>% filter(wage < quantile(wage, 0.99, na.rm = TRUE)),
                    cluster = ~ firm_id)
balpan     <- feols(log_wage ~ training + age + edu + tenure | industry + year,
                    data = df %>% group_by(worker_id) %>%
                            filter(n_distinct(year) == max(n_distinct(year))) %>% ungroup(),
                    cluster = ~ firm_id)
dropearly  <- feols(log_wage ~ training + age + edu + tenure | industry + year,
                    data = df %>% filter(first_treat > 2008), cluster = ~ firm_id)
wfe        <- feols(log_wage ~ training + age + edu + tenure | worker_id + year,
                    data = df, cluster = ~ firm_id)
cl2way     <- feols(log_wage ~ training + age + edu + tenure | industry + year,
                    data = df, cluster = ~ firm_id + year)
logy       <- feols(log(wage + 1) ~ training + age + edu + tenure | industry + year,
                    data = df, cluster = ~ firm_id)
ihsy       <- feols(asinh(wage) ~ training + age + edu + tenure | industry + year,
                    data = df, cluster = ~ firm_id)
m_psm      <- matchit(training ~ age + edu + tenure + firm_size, data = df, method = "nearest")
psm_lm     <- lm(log_wage ~ training + age + edu + tenure, data = match.data(m_psm), weights = weights)
ebal_w     <- weightit(training ~ age + edu + tenure + firm_size, data = df, method = "ebal")
ebal_lm    <- lm(log_wage ~ training + age + edu + tenure, data = df, weights = ebal_w$weights)

modelsummary(
  list("(1) Baseline"        = base,
       "(2) Drop top 1%"     = no99,
       "(3) Balanced"        = balpan,
       "(4) Drop early"      = dropearly,
       "(5) Worker FE"       = wfe,
       "(6) 2-way cluster"   = cl2way,
       "(7) log Y"           = logy,
       "(8) IHS Y"           = ihsy,
       "(9) PSM"             = psm_lm,
       "(10) Entropy bal."   = ebal_lm),
  output    = "tables/tableA1_robustness.tex",
  stars     = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  coef_map  = c("training" = "Training (β̂)"),
  gof_omit  = "BIC|AIC|F|Log|Adj",
  notes     = "Each column is one robustness check. β̂ on training is the focal coefficient."
)

# ============================================================
# 6k. Specification curve (Simonsohn-Simmons-Nelson 2020) via `specr`
# ============================================================
library(specr); library(ggplot2)

specs <- setup(data = df,
               y = c("log_wage", "ihs_wage"),
               x = "training",
               model = c("feols"),
               controls = c("age", "edu", "tenure", "firm_size"),
               subsets = list(industry = c("manuf", "construction", "transport")))

results <- specr(specs)
plot(results, choices = c("x", "y", "controls", "subsets"))
ggsave("figures/fig5_spec_curve.pdf", width = 10, height = 6)
ggsave("figures/fig5_spec_curve.png", width = 10, height = 6, dpi = 300)

# Hand-rolled alternative when `specr` doesn't fit (with custom FE / SE):
# spec_grid <- expand.grid(controls = list(c("age"), c("age","edu"), c("age","edu","tenure")),
#                           ytrans   = c("log_wage", "ihs_wage"),
#                           sample   = c("all", "manuf", "no99"),
#                           cluster  = c("firm_id", "firm_id+year"))
# Loop, run feols, collect b/se, ggplot::geom_pointrange.

# ============================================================
# 6l. Sensitivity dashboard — HonestDiD + Oster + E-value
# ============================================================
# (a) HonestDiD — Rambachan-Roth (2023): bound on β̂ under bounded PT violation
library(HonestDiD)
es_pre  <- coef(es)[grep("year::-", names(coef(es)))]
es_post <- coef(es)[grep("year::[0-9]", names(coef(es)))]
honest_out <- createSensitivityResults(betahat = c(es_pre, es_post),
                                       sigma   = vcov(es)[c(names(es_pre), names(es_post)),
                                                          c(names(es_pre), names(es_post))],
                                       numPrePeriods  = length(es_pre),
                                       numPostPeriods = length(es_post),
                                       Mbarvec = seq(0, 0.5, by = 0.05))
createSensitivityPlot(honest_out, originalResults = honest_out$mainResult)
ggsave("figures/fig6_honestdid.pdf", width = 7, height = 4)

# (b) Oster δ — `robomit::o_test` (already shown in 6i)

# (c) E-value (VanderWeele-Ding 2017) — for risk-ratio outcomes
library(EValue)
evalue(RR(1.45), lo = 1.10, hi = 1.91)
# → reports the minimum strength of unmeasured confounding to nullify the result.
```

---

### Step 7 — Further analysis

Deeper patterns: [references/07-further-analysis.md](references/07-further-analysis.md) — `marginaleffects` is the post-estimation workhorse; `mediation::mediate` for Imai mediation; `lavaan` for SEM; `grf::causal_forest` for CATE.

```r
library(marginaleffects)
library(fixest)

# 7a. Heterogeneity via interaction
het <- feols(log_wage ~ i(female, training, ref = 0) + age + edu | worker_id + year,
             data = df, cluster = ~ worker_id)
summary(het)
iplot(het)                                          # visualize interaction

# Continuous moderator + marginsplot
het_c <- feols(log_wage ~ training * tenure + age + edu | worker_id + year,
               data = df, cluster = ~ worker_id)
plot_slopes(het_c, variables = "training",
            condition = list(tenure = seq(0, 20, by = 2))) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(x = "Tenure", y = "Marginal effect of training")
ggsave("figures/het_tenure.pdf", width = 6, height = 4)

# 7b. Triple difference
ddd <- feols(log_wage ~ treated * post * high_exposure | worker_id + year,
             data = df, cluster = ~ firm_id)

# 7c. Outcome ladder
out_ladder <- list()
for (y in c("hours_worked", "productivity", "log_wage")) {
  out_ladder[[y]] <- feols(as.formula(paste(y, "~ training | worker_id + year")),
                           data = df, cluster = ~ worker_id)
}
modelsummary(out_ladder, stars = TRUE,
             coef_map = c("training" = "Training"),
             output = "tables/outcome_ladder.tex")

# 7d. Mediation — Imai et al. (2010)
library(mediation)
med_M <- lm(hours_worked ~ training + age + edu, data = df)
med_Y <- lm(log_wage     ~ training + hours_worked + age + edu, data = df)
med   <- mediate(med_M, med_Y, treat = "training", mediator = "hours_worked",
                 boot = TRUE, sims = 1000)
summary(med); plot(med)

# Sensitivity to unobserved M-Y confounding
medsens <- medsens(med, rho.by = 0.05, effect.type = "indirect")
plot(medsens)

# 7e. CATE via causal forest
library(grf)
cf <- causal_forest(X = as.matrix(df %>% select(age, edu, tenure, firm_size)),
                    Y = df$log_wage, W = df$training,
                    num.trees = 2000, min.node.size = 5)
df$tau_hat <- predict(cf)$predictions
variable_importance(cf)
average_treatment_effect(cf, target.sample = "all")

# Plot CATE by a moderator
ggplot(df, aes(tenure, tau_hat)) +
  geom_smooth(method = "loess", se = TRUE) +
  labs(x = "Tenure", y = "Estimated CATE")
ggsave("figures/cate_tenure.pdf")

# 7f. Dose-response — splines
library(splines)
dr <- feols(log_wage ~ ns(training_hours, df = 4) + age + edu | worker_id + year,
            data = df, cluster = ~ worker_id)
plot_predictions(dr, condition = "training_hours")
```

---

### Step 8 — Publication tables & figures

> **This step is mandatory** — every analysis run produces all 5 required tables (T1–T5) and all 4 required figures (F1–F4) defined in the *Default Output Spec* at the top of this skill. Do not skip Step 8 because "the regression already ran". A coefficient without a table and a figure is not how applied economics communicates a result.

Deeper patterns: [references/08-tables-plots.md](references/08-tables-plots.md) — `modelsummary` is the modern default (LaTeX/Word/HTML/Excel from one call); `kableExtra` for further LaTeX styling; `gt` for HTML/Word; `ggplot2` + `iplot` + `ggpubr` + `cowplot` + `binsreg` for figures.

```r
library(modelsummary)
library(kableExtra)
library(gt)
library(fixest)
library(ggplot2)

# ============================================================
# 8a. ★ TABLE 2 — Main results, multi-column regression M1→M6
#     (the centerpiece of every economics paper)
# ============================================================
modelsummary(
  list("(1) Raw"        = m1,
       "(2) +Demog"     = m2,
       "(3) +Tenure"    = m3,
       "(4) +Unit FE"   = m4,
       "(5) +2-way FE"  = m5,
       "(6) +Ind×Yr FE" = m6),
  stars    = c('*' = .1, '**' = .05, '***' = .01),
  coef_map = c("training" = "Training",
               "age" = "Age", "edu" = "Education", "tenure" = "Tenure"),
  gof_map  = list(
    list("raw" = "nobs",         "clean" = "N",         "fmt" = 0),
    list("raw" = "r.squared",    "clean" = "R²",        "fmt" = 3),
    list("raw" = "adj.r.squared","clean" = "Adj. R²",   "fmt" = 3)
  ),
  notes  = "Cluster-robust SE at worker_id in parentheses. * p<0.10, ** p<0.05, *** p<0.01.",
  output = "tables/table2_main.tex"
)
modelsummary(list("(1)"=m1, "(2)"=m2, "(3)"=m3, "(4)"=m4, "(5)"=m5, "(6)"=m6),
             stars = TRUE, output = "tables/table2_main.docx")

# ============================================================
# 8b. TABLE 1 — Summary statistics & balance
# ============================================================
library(gtsummary)
tbl1 <- df %>%
  select(log_wage, age, edu, tenure, female, training) %>%
  tbl_summary(by = training, missing = "ifany",
              statistic = all_continuous() ~ "{mean} ({sd})") %>%
  add_p() %>% add_difference() %>% add_n() %>% bold_labels()
tbl1 %>% as_kable_extra(format = "latex", booktabs = TRUE) %>%
  kableExtra::save_kable("tables/table1_balance.tex")
tbl1 %>% as_flex_table() %>%
  flextable::save_as_docx(path = "tables/table1_balance.docx")

# ============================================================
# 8c. TABLE 3 — Mechanism / outcome ladder (3+ outcomes)
# ============================================================
ladder <- list()
for (y in c("hours_worked", "productivity", "log_wage")) {
  ladder[[y]] <- feols(as.formula(paste(y, "~ training + age + edu + tenure | worker_id + year")),
                       data = df, cluster = ~ worker_id)
}
modelsummary(ladder,
             stars    = c('*' = .1, '**' = .05, '***' = .01),
             coef_map = c("training" = "Training"),
             notes    = "Each column is a separate regression on the labelled outcome. Cluster-robust SE at worker_id.",
             output   = "tables/table3_mechanism.tex")

# ============================================================
# 8d. TABLE 4 — Heterogeneity (subgroup × main coef)
# ============================================================
het_specs <- list(
  "All"         = df,
  "Female=0"    = df %>% filter(female == 0),
  "Female=1"    = df %>% filter(female == 1),
  "Age<40"      = df %>% filter(age < 40),
  "Age≥40"      = df %>% filter(age >= 40),
  "Manuf."      = df %>% filter(industry == "manufacturing")
)
het_models <- imap(het_specs,
                   ~ feols(log_wage ~ training + age + edu + tenure | worker_id + year,
                           data = .x, cluster = ~ worker_id))
modelsummary(het_models,
             stars    = c('*' = .1, '**' = .05, '***' = .01),
             coef_map = c("training" = "Training"),
             notes    = "Cluster-robust SE at worker_id. Wald p-values for cross-subgroup equality should accompany this table — see references/07.",
             output   = "tables/table4_heterogeneity.tex")

# ============================================================
# 8e. TABLE 5 — Robustness battery (alt SE / cluster / sample / placebo)
# ============================================================
rob <- list(
  "Baseline"      = feols(log_wage ~ training | worker_id + year, data = df,
                          cluster = ~ worker_id),
  "Cluster=Firm"  = feols(log_wage ~ training | worker_id + year, data = df,
                          cluster = ~ firm_id),
  "2-way Cluster" = feols(log_wage ~ training | worker_id + year, data = df,
                          cluster = ~ worker_id + firm_id),
  "Winsor 1/99"   = feols(log_wage ~ training | worker_id + year,
                          data = df %>% mutate(log_wage = DescTools::Winsorize(log_wage,
                                                                               probs = c(.01,.99),
                                                                               na.rm = TRUE)),
                          cluster = ~ worker_id),
  "Drop Manuf."   = feols(log_wage ~ training | worker_id + year,
                          data = df %>% filter(industry != "manufacturing"),
                          cluster = ~ worker_id),
  "Placebo (-3)"  = feols(log_wage ~ fake_post | worker_id + year,
                          data = df %>% filter(year < first_treat),
                          cluster = ~ worker_id)
)
modelsummary(rob,
             stars  = c('*' = .1, '**' = .05, '***' = .01),
             output = "tables/table5_robustness.tex")

# ============================================================
# 8f. ★ FIGURE 3 — Coefficient plot across M1→M6
# ============================================================
modelplot(list("(1)"=m1, "(2)"=m2, "(3)"=m3, "(4)"=m4, "(5)"=m5, "(6)"=m6),
          coef_map = c("training" = "Training"),
          conf_level = 0.95) +
  geom_vline(xintercept = 0, linetype = "dashed", alpha = 0.5) +
  labs(x = "Coefficient on training (95% CI)", y = "Specification",
       title = "Effect of training across specifications") +
  theme_classic(base_size = 11)
ggsave("figures/fig3_coefplot.pdf", width = 6, height = 4)
ggsave("figures/fig3_coefplot.png", width = 6, height = 4, dpi = 300)

# ============================================================
# 8g. FIGURE 2 — Event-study plot (dynamic DID, base period = -1)
# ============================================================
pdf("figures/fig2_event_study.pdf", width = 7, height = 4)
iplot(es,
      xlab = "Years relative to treatment",
      ylab = "Coefficient (ATT, 95% CI)",
      main = "Event study: dynamic effect of training",
      ref.line = -0.5)
dev.off()
png("figures/fig2_event_study.png", width = 2100, height = 1200, res = 300)
iplot(es,
      xlab = "Years relative to treatment",
      ylab = "Coefficient (ATT, 95% CI)",
      main = "Event study: dynamic effect of training",
      ref.line = -0.5)
dev.off()

# ============================================================
# 8h. FIGURE 4 — Sensitivity / robustness curve
#     (HonestDiD / spec curve / forest of robustness battery)
# ============================================================
# HonestDiD example (after the event study with stored b/V):
library(HonestDiD)
honest_out <- createSensitivityResults(betahat       = es$coefficients,
                                       sigma         = vcov(es),
                                       numPrePeriods = 5, numPostPeriods = 5,
                                       Mbarvec       = seq(0, 0.5, by = 0.05))
sens_plot <- createSensitivityPlot(honest_out, originalResults = honest_out$mainResult)
ggsave("figures/fig4_sensitivity.pdf", plot = sens_plot, width = 7, height = 4)
ggsave("figures/fig4_sensitivity.png", plot = sens_plot, width = 7, height = 4, dpi = 300)

# Alternative — robustness forest plot:
# rob_summary <- imap_dfr(rob, ~ tibble(
#   group = .y,
#   est   = coef(.x)[1],
#   se    = se(.x)[1]
# ))
# ggplot(rob_summary, aes(est, fct_rev(factor(group)))) +
#   geom_point(size = 3, color = "navy") +
#   geom_errorbarh(aes(xmin = est - 1.96*se, xmax = est + 1.96*se),
#                  height = 0.2, color = "navy") +
#   geom_vline(xintercept = 0, linetype = "dashed") +
#   labs(x = "Coefficient on training (95% CI)", y = NULL,
#        title = "Robustness forest plot")
# ggsave("figures/fig4_sensitivity.pdf", width = 7, height = 4)

# ============================================================
# 8i. FIGURE 1 — Trend / motivation (treated vs control over time)
# ============================================================
df %>%
  group_by(year, training) %>%
  summarise(mean_log_wage = mean(log_wage, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(year, mean_log_wage, color = factor(training))) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  geom_vline(xintercept = policy_year, linetype = "dashed", color = "gray40") +
  scale_color_manual(values = c("0" = "darkred", "1" = "navy"),
                     labels = c("Control", "Treated"), name = "") +
  labs(x = "Year", y = "Mean log wage",
       title = "Treated vs control trend") +
  theme_classic(base_size = 11) +
  theme(legend.position = "bottom")
ggsave("figures/fig1_trend.pdf", width = 7, height = 4)
ggsave("figures/fig1_trend.png", width = 7, height = 4, dpi = 300)

# ============================================================
# 8j. Auxiliary plots (optional — produce when relevant)
# ============================================================
library(binsreg)
binsreg(y = df$log_wage, x = df$tenure, w = df %>% select(age, edu, female))
ggsave("figures/figA_binscatter.pdf", width = 6, height = 4)

# RD plot (only when running_var exists)
# rdplot(y = df$outcome, x = df$running_var, c = 0,
#        title = "RD plot", x.label = "Running variable", y.label = "Outcome")

# ============================================================
# 8k. Multi-panel combined (optional, for slides / appendix)
# ============================================================
library(cowplot)
# plot_grid(p_trend, p_event, p_coef, p_sens, ncol = 2, labels = "AUTO") %>%
#   ggsave("figures/combined.pdf", plot = ., width = 10, height = 8)

# ============================================================
# 8l. Theme — set once at top of script for consistency
# ============================================================
theme_set(theme_classic(base_size = 11) +
          theme(legend.position = "bottom",
                plot.title      = element_text(face = "bold")))
```

**Deliverables checklist** (verify before declaring the run complete):

```
[ ] tables/table1_balance.tex     [ ] figures/fig1_trend.pdf
[ ] tables/table2_main.tex   ★    [ ] figures/fig2_event_study.pdf
[ ] tables/table3_mechanism.tex   [ ] figures/fig3_coefplot.pdf
[ ] tables/table4_heterogeneity.tex
[ ] tables/table5_robustness.tex  [ ] figures/fig4_sensitivity.pdf
[ ] tables/tableA1_robustness.tex [ ] figures/fig5_spec_curve.pdf
[ ] artifacts/sample_construction.json (footnote 4)
[ ] artifacts/data_contract.json
[ ] artifacts/result.json (reproducibility stamp — see 8m)
```

#### 8m. Reproducibility stamp

The single artifact a journal's replication office (or a future co-author) needs to reproduce the headline number. Persist R version, seed, dataset hash, baseline coefficient + CI, and pointers to the protocol/contract:

```r
library(jsonlite); library(digest)

# Get baseline result (assumes `base` is the headline feols object)
b_hat <- coef(base)["training"]
se_b  <- se(base)["training"]
ci    <- c(b_hat - 1.96 * se_b, b_hat + 1.96 * se_b)

stamp <- list(
  R_version          = R.version.string,
  fixest_version     = as.character(packageVersion("fixest")),
  modelsummary_version = as.character(packageVersion("modelsummary")),
  seed               = 42,
  dataset_sha256     = substr(digest::digest(df, algo = "sha256"), 1, 16),
  n_obs              = base$nobs,
  estimand           = "ATT",
  estimator          = "fixest::feols",
  estimate           = unname(b_hat),
  se_cluster         = unname(se_b),
  ci95               = unname(ci),
  pre_registration   = "artifacts/strategy.md",
  data_contract      = "artifacts/data_contract.json",
  sample_log         = "artifacts/sample_construction.json",
  paper_bundle       = "tables/table2_main.tex"
)
write_json(stamp, "artifacts/result.json", pretty = TRUE, auto_unbox = TRUE)
```

Commit `artifacts/result.json` alongside the paper PDF. A referee should be able to run `Rscript master.R` and bit-identically reproduce this JSON.

---

## §A — Epidemiology / Public Health Mode

When the user's wording flags Mode A (target-trial emulation / IPTW / TMLE / MR / STROBE / 流行病学 / 公共健康 / RWE / cohort), the 8 steps still apply — but Step 5 swaps the OLS-and-FE stack for the doubly-robust + survival + MR triplet, and the deliverables follow STROBE / TRIPOD-AI conventions. **Steps 1–4 (cleaning, construction, Table 1, diagnostics) and Step 8 (tables/figures export) are identical to the Default mode.**

**Package footprint** (install on top of the Default stack):

```r
install.packages(c(
  "WeightIt", "PSweight", "cobalt",         # IPTW / propensity weighting + balance
  "gfoRmula",                               # parametric g-formula (time-varying)
  "tmle", "ltmle",                          # TMLE / longitudinal TMLE
  "survival", "survminer", "flexsurv",      # KM / Cox / AFT / RMST
  "MendelianRandomization", "TwoSampleMR",  # IVW, Egger, weighted-median MR
  "MRPRESSO",                               # outlier-robust MR
  "EValue"                                  # E-value sensitivity (VanderWeele)
))
```

### A.0 Cohort construction + target-trial protocol

Write the protocol **before** touching the data. Save it as `protocol.yml` and quote it in the paper.

```r
# protocol.yml — target-trial emulation skeleton
# eligibility:    age 40-75, no_prior_event, ascertained_at t0
# treatment:      A=1 statin initiation; A=0 no initiation
# assignment:     emulated random at t0 via IPTW on baseline covariates
# outcome:        incident MI within 5 years
# estimand:       ITT ATE on risk difference + hazard ratio

library(dplyr)
cohort <- df |>
  filter(age >= 40, age <= 75, prior_MI == 0) |>
  mutate(
    t0           = coalesce(statin_initiation_date, enrollment_date),
    event_5y     = as.integer((MI_date - t0) <= 365 * 5 & !is.na(MI_date)),
    time_at_risk = pmin(as.numeric(censor_date - t0), 365 * 5)
  )
```

### A.1 Table 1 by exposure (identical to Default Step 3)

Use the same `gtsummary::tbl_summary` from Step 3, just `by = A`. E-values for unmeasured confounding go in the footer.

```r
library(gtsummary)
cohort |>
  select(A, age, edu, smoke, bmi, ldl, sbp) |>
  tbl_summary(by = A, missing = "ifany") |>
  add_difference() |>
  add_p() |>
  bold_labels()
```

### A.2 DAG + propensity-score overlap (positivity check)

```r
library(WeightIt); library(cobalt)

# Estimate PS + IPTW weights
w_out <- weightit(A ~ age + edu + smoke + bmi + ldl + sbp,
                  data = cohort, method = "glm", estimand = "ATE")

# Overlap density (positivity)
bal.plot(w_out, var.name = "prop.score", which = "both")
ggsave("figures/figA2_ps_overlap.pdf")

# Love plot (SMDs before vs after IPTW)
love.plot(w_out, threshold = 0.1, abs = TRUE)
ggsave("figures/figA2_love.pdf")
```

### A.3 IPTW + g-formula + TMLE doubly-robust triplet (Step 5 swap)

The "AER Table 2" of epi: a 3-column table where each column is one of {IPTW-MSM, g-formula, TMLE}, so the reader can confirm doubly-robust agreement.

```r
# IPTW marginal structural model
library(survey)
des  <- svydesign(ids = ~1, data = cohort, weights = w_out$weights)
msm  <- svyglm(event_5y ~ A, design = des, family = quasibinomial())
RD_iptw <- coef(msm)["A"]; CI_iptw <- confint(msm)["A", ]

# g-formula (parametric, time-fixed)
library(gfoRmula)
gf <- gformula_binary_eof(
  obs_data = cohort,
  id = "subject_id", time_name = "t", outcome_name = "event_5y",
  covnames = c("age","edu","smoke","bmi","ldl","sbp"),
  intvars = list("A"), interventions = list(list(c(static, 1)), list(c(static, 0))),
  ref_int = 1, time_points = 1, basecovs = c("age","edu","smoke","bmi","ldl","sbp")
)

# TMLE (doubly robust)
library(tmle)
fit_tmle <- tmle(
  Y = cohort$event_5y, A = cohort$A,
  W = cohort[, c("age","edu","smoke","bmi","ldl","sbp")],
  family = "binomial",
  Q.SL.library = c("SL.glm","SL.glmnet","SL.ranger"),
  g.SL.library = c("SL.glm","SL.glmnet","SL.ranger")
)
RD_tmle <- fit_tmle$estimates$ATE$psi
CI_tmle <- fit_tmle$estimates$ATE$CI

# Stack the triplet into one paper table
library(modelsummary)
tableA3 <- tibble::tribble(
  ~Estimator,    ~RD,        ~`95% CI`,
  "IPTW-MSM",    RD_iptw,    sprintf("[%.3f, %.3f]", CI_iptw[1], CI_iptw[2]),
  "g-formula",   gf$result[2,"mean"] - gf$result[1,"mean"], "—",
  "TMLE",        RD_tmle,    sprintf("[%.3f, %.3f]", CI_tmle[1], CI_tmle[2])
)
modelsummary::datasummary_df(tableA3, output = "tables/tableA3_dr_triplet.tex")
```

### A.4 Survival outcomes — KM / Cox / AFT / RMST

```r
library(survival); library(survminer); library(flexsurv)

# KM by treatment
fit_km <- survfit(Surv(time_at_risk, event_5y) ~ A, data = cohort)
ggsurvplot(fit_km, conf.int = TRUE, pval = TRUE, risk.table = TRUE)
ggsave("figures/figA4_km.pdf")

# Cox HR (covariate-adjusted)
fit_cox <- coxph(Surv(time_at_risk, event_5y) ~ A + age + edu + smoke + bmi + ldl + sbp,
                 data = cohort, weights = w_out$weights)
HR <- exp(coef(fit_cox)["A"]); HR_CI <- exp(confint(fit_cox)["A", ])

# AFT (Weibull) for time-ratio interpretation
fit_aft <- flexsurvreg(Surv(time_at_risk, event_5y) ~ A + age + edu + smoke + bmi + ldl + sbp,
                       data = cohort, dist = "weibull")

# RMST contrast at t = 5 years
library(survRM2)
rmst <- rmst2(cohort$time_at_risk, cohort$event_5y, cohort$A, tau = 365 * 5)
```

### A.5 Mendelian randomization (IVW / Egger / weighted-median triplet)

```r
library(MendelianRandomization)

mri <- mr_input(bx = BX, bxse = BXSE, by = BY, byse = BYSE,
                exposure = "Statin use", outcome = "MI")
ivw    <- mr_ivw(mri)
egger  <- mr_egger(mri)         # pleiotropy intercept test
wmedian<- mr_median(mri, weighting = "weighted")

# Or harmonized two-sample workflow
# library(TwoSampleMR); harmonised <- harmonise_data(exposure_dat, outcome_dat)
# res <- mr(harmonised, method_list = c("mr_ivw", "mr_egger_regression", "mr_weighted_median"))

# Sensitivity to outliers
library(MRPRESSO)
mr_presso(BetaOutcome = "by", BetaExposure = "bx", SdOutcome = "byse", SdExposure = "bxse",
          OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = data.frame(bx, by, bxse, byse), NbDistribution = 1000)
```

### A.6 Robustness — E-value / bounds / principal stratification

```r
library(EValue)
ev <- evalue(RR(1.45), lo = 1.10, hi = 1.91)   # required strength of unmeasured confounding
print(ev)
```

### A.7 STROBE / TRIPOD-AI reporting checklist

Save as `replication/strobe_checklist.md` and tick before submission:

```
[ ] Eligibility criteria + dates                           (target-trial protocol)
[ ] Adjustment set with DAG justification                  (A.2)
[ ] Positivity / overlap diagnostic                        (A.2)
[ ] Doubly-robust triplet (IPTW + g-formula + TMLE)        (A.3)
[ ] Risk difference + hazard ratio + RMST                  (A.3, A.4)
[ ] E-value for unmeasured confounding                     (A.6)
[ ] Loss-to-follow-up rate + censoring assumption          (A.0)
[ ] Pre-registered protocol or analysis plan               (A.0)
```

---

## §B — ML Causal Inference Mode

When the user's wording flags Mode B (DML / meta-learner / causal forest / BCF / CATE / policy learning / conformal causal / fairness / 因果机器学习), the pipeline keeps Steps 1–4 and Step 8 from the Default mode, swaps Step 5 for the ML estimator stack, and adds a CATE-distribution + policy-value layer between Step 7 and Step 8.

**Package footprint** (install on top of the Default stack):

```r
install.packages(c(
  "DoubleML", "mlr3", "mlr3learners",       # DML + ML nuisance learners
  "grf",                                    # causal forest, GRF, instrumental forest
  "causalweight",                           # IPW / DR / sensitivity for CATE
  "bartCause", "bcf",                       # BART / Bayesian causal forest
  "policytree",                             # honest policy trees
  "conformalInference",                     # conformal prediction (general)
  # cfcausal — install via devtools::install_github("lihualei71/cfcausal")
  "fairmodels",                             # fairness audit
  "pcalg", "bnlearn"                        # causal discovery (PC / GES / Bayesian net)
))
```

### B.0 Train/holdout split + nuisance learner stack

```r
library(mlr3); library(mlr3learners); library(DoubleML)

set.seed(42)
idx <- sample(seq_len(nrow(df)), size = 0.7 * nrow(df))
train <- df[idx, ]; holdout <- df[-idx, ]

# Standard nuisance pair: outcome regression Q(X,A) and propensity g(A|X)
ml_g <- lrn("regr.ranger",  num.trees = 500, mtry = 5)   # outcome
ml_m <- lrn("classif.ranger", num.trees = 500, mtry = 5) # propensity
```

### B.1 DAG / estimand declaration (optionally LLM-assisted)

```r
library(pcalg)
# PC algorithm — constraint-based DAG discovery
suffStat <- list(C = cor(df[, c("A","Y","X1","X2","X3","X4")]), n = nrow(df))
pc.fit <- pc(suffStat, indepTest = gaussCItest,
             alpha = 0.01, labels = c("A","Y","X1","X2","X3","X4"))
plot(pc.fit, main = "PC-recovered DAG")

# OR: bnlearn for hill-climbing GES
# library(bnlearn); hc.fit <- hc(df[, c("A","Y","X1","X2","X3","X4")]); plot(hc.fit)
```

### B.2 Estimator stack — DML · meta-learners · causal forest · BCF (Step 5 swap)

The "AER Table 2" of ML causal: a horse-race table where each column is one estimator family on the same `(Y, A, X)` data — readers want to see DML, T-learner, causal forest, and BCF all agree (or disagree) on the ATE.

```r
# DML — partially linear or interactive regression model
dml_data <- DoubleMLData$new(train, y_col = "Y", d_cols = "A",
                             x_cols = c("X1","X2","X3","X4"))
dml_plr  <- DoubleMLPLR$new(dml_data, ml_g = ml_g, ml_m = ml_m, n_folds = 5)
dml_plr$fit()
ate_dml <- dml_plr$coef; ci_dml <- dml_plr$confint()

# Causal forest (GRF) — non-parametric CATE
library(grf)
cf <- causal_forest(X = as.matrix(train[, c("X1","X2","X3","X4")]),
                    Y = train$Y, W = train$A, num.trees = 2000)
ate_cf <- average_treatment_effect(cf, target.sample = "all")
cate_cf <- predict(cf, newdata = as.matrix(holdout[, c("X1","X2","X3","X4")]))$predictions

# T-learner / DR-learner (use causalweight or hand-rolled with grf::*)
library(causalweight)
dr <- treatDML(y = train$Y, d = train$A, x = as.matrix(train[, c("X1","X2","X3","X4")]),
               MLmethod = "lasso")$effect
ate_DR <- mean(dr)

# Bayesian Causal Forest — separate prognostic + treatment functions
library(bcf)
bcf_fit <- bcf(y = train$Y, z = train$A,
               x_control = as.matrix(train[, c("X1","X2","X3","X4")]),
               x_moderate = as.matrix(train[, c("X1","X2","X3","X4")]),
               pihat = predict(glm(A ~ ., data = train[, c("A","X1","X2","X3","X4")], family = binomial), type = "response"),
               nburn = 1000, nsim = 1000)
ate_bcf <- mean(bcf_fit$tau)

# Stack the horse-race
library(modelsummary)
tableB2 <- tibble::tribble(
  ~Estimator,           ~ATE,
  "DML (PLR)",          ate_dml[1],
  "Causal Forest",      ate_cf[1],
  "DR-learner",         ate_DR,
  "Bayesian Causal Forest", ate_bcf
)
modelsummary::datasummary_df(tableB2, fmt = 4, output = "tables/tableB2_ml_horserace.tex")
```

### B.3 CATE distribution + subgroup CATE plot (Step 7 extension)

```r
library(ggplot2)

# CATE histogram
data.frame(cate = cate_cf) |>
  ggplot(aes(x = cate)) +
  geom_histogram(bins = 30, fill = "grey70", colour = "black") +
  geom_vline(xintercept = 0, lty = 2) +
  labs(x = "CATE", y = "Count")
ggsave("figures/figB3_cate_hist.pdf")

# CATE by quartile of a covariate
holdout |>
  mutate(cate = cate_cf, age_q = ntile(X1, 4)) |>
  group_by(age_q) |>
  summarise(mean_cate = mean(cate)) |>
  ggplot(aes(age_q, mean_cate)) + geom_col() + labs(y = "Mean CATE")
ggsave("figures/figB3_cate_by_age_q.pdf")
```

### B.4 Policy learning + off-policy evaluation

```r
library(policytree)

# Honest discrete policy tree on doubly-robust scores from causal forest
dr_scores <- double_robust_scores(cf)
ptree     <- policy_tree(X = as.matrix(train[, c("X1","X2","X3","X4")]),
                         Gamma = dr_scores, depth = 3)
print(ptree)            # human-readable tree of "treat if X1<a and X2>b"
plot(ptree)
ggsave("figures/figB4_policy_tree.pdf")

# Off-policy evaluation — DR policy value on holdout
holdout_X <- as.matrix(holdout[, c("X1","X2","X3","X4")])
pred_pol  <- predict(ptree, holdout_X)
DR_holdout <- double_robust_scores(cf, newdata = holdout_X)
policy_value_DR <- mean(DR_holdout[cbind(seq_len(nrow(DR_holdout)), pred_pol)])
cat(sprintf("DR policy value (holdout): %.3f\n", policy_value_DR))
```

### B.5 Uncertainty (conformal causal) + fairness + sensitivity

```r
# Conformal prediction interval around CATE (split conformal via cfcausal)
# devtools::install_github("lihualei71/cfcausal")
library(cfcausal)
ci90 <- conformalIte(X = as.matrix(train[, c("X1","X2","X3","X4")]),
                     Y = train$Y, T = train$A,
                     alpha = 0.1,
                     algo = "nest",
                     type = "CQR",
                     X.test = as.matrix(holdout[, c("X1","X2","X3","X4")]))

# Fairness audit — disparate impact / equalised odds
library(fairmodels)
fobject <- fairness_check(model_treated = predict(ptree, holdout_X),
                          data = holdout, protected = holdout$sensitive_attr,
                          privileged = "majority")
plot(fobject)
ggsave("figures/figB5_fairness.pdf")
```

### B.6 ML-causal-specific reporting checklist

Save as `replication/ml_causal_checklist.md`:

```
[ ] Nuisance learners listed (Q model, g model, hyperparameters, CV folds)
[ ] Cross-fitting / sample-splitting documented (DML K-fold)
[ ] Overlap / propensity diagnostics (B.0 + A.2-style overlap plot)
[ ] CATE summary (mean, SD, quartiles) + heterogeneity p-value (grf::test_calibration)
[ ] Policy value with confidence interval (B.4)
[ ] Conformal coverage rate on holdout (B.5)
[ ] Fairness gaps across sensitive attributes (B.5)
[ ] DAG / adjustment set + sensitivity to unmeasured confounding (E-value or Manski bounds)
```

---

## Library cheat-sheet

| Step | Task | Go-to package | Fallback |
|------|------|---------------|----------|
| 1 | Read data | `haven` / `readr` / `readxl` / `data.table::fread` | `arrow` for Parquet |
| 1 | Clean names | `janitor::clean_names` | manual |
| 1 | Missing | `naniar` / `mice` | `Hmisc` |
| 2 | Winsorize | `DescTools::Winsorize` | manual `pmin`/`pmax` |
| 2 | Lag in panel | `dplyr::lag` (with `arrange`+`group_by`) | `data.table::shift` |
| 3 | Table 1 | `gtsummary` / `modelsummary::datasummary_balance` | `tableone` |
| 3 | Correlation | `psych::corr.test` + `corrplot` | `Hmisc::rcorr` |
| 4 | Hetero / autocorr | `lmtest::bptest` / `dwtest` / `bgtest` | `car` |
| 4 | Panel tests | `plm::pbgtest` / `pcdtest` / `phtest` | — |
| 4 | Stationarity | `tseries::adf.test` / `tseries::kpss.test` | `urca` |
| 5 | OLS / panel FE | `fixest::feols` | `lfe::felm` (older) |
| 5 | IV | `fixest::feols(\| ~ )` | `AER::ivreg` / `ivreg::ivreg` |
| 5 | DID — 2×2 | `feols` with `i(treated, post)` | — |
| 5 | DID — CS | `did::att_gt` | — |
| 5 | DID — SA | `fixest::sunab` | — |
| 5 | DID — BJS | `didimputation::did_imputation` | — |
| 5 | DID — SDID | `synthdid` | — |
| 5 | RD | `rdrobust` / `rddensity` / `rdmulti` | — |
| 5 | SC | `Synth` / `gsynth` / `tidysynth` | — |
| 5 | PSM | `MatchIt::matchit` | — |
| 5 | IPW | `WeightIt::weightit` | — |
| 5 | Entropy balance | `ebal` | — |
| 5 | DML | `DoubleML` | — |
| 5 | CATE (causal forest) | `grf::causal_forest` | — |
| 5 | Mediation | `mediation::mediate` | `lavaan` |
| 6 | Wild cluster boot | `fwildclusterboot::boottest` | `clubSandwich` |
| 6 | Random. inference | `ri2::conduct_ri` | manual `boot` |
| 6 | Multiple testing | `multcomp` / hand-roll Romano-Wolf | — |
| 6 | TWFE diagnosis | `bacondecomp::bacon` | — |
| 6 | PT sensitivity | `HonestDiD` | — |
| 6 | Oster δ\* | `robomit::o_test` / `o_beta` | — |
| 7 | Margins / slopes | `marginaleffects::avg_slopes` / `plot_slopes` | — |
| 7 | Mediation w/ sensitivity | `mediation::mediate` + `medsens` | — |
| 7 | SEM | `lavaan::sem` | — |
| 8 | Reg table (any format) | `modelsummary` | `texreg` / `stargazer` |
| 8 | Word table | `flextable` / `gt::gtsave` | `officer` |
| 8 | LaTeX table styling | `kableExtra` | — |
| 8 | Coefplot / event study | `modelplot` / `fixest::iplot` | `ggplot2` manual |
| 8 | Binscatter | `binsreg` | — |
| 8 | Multi-panel | `cowplot::plot_grid` / `patchwork` | `gridExtra` |

---

## Common mistakes (and what to do instead)

| Mistake | Correct approach |
|---------|------------------|
| `lm(y ~ x + factor(unit) + factor(year))` on big panels | `feols(y ~ x | unit + year, data)` |
| Default iid SEs on clustered data | `feols(..., cluster = ~ id)`; `boottest` if clusters < 50 |
| TWFE on staggered adoption | `did::att_gt` / `fixest::sunab` / `didimputation::did_imputation` |
| Using `lag(x)` without `arrange()` + `group_by()` | always `arrange(id, time) %>% group_by(id) %>% mutate(x_l1 = lag(x))` |
| Joining without checking row count | use `relationship` arg in `dplyr::*_join`, then `stopifnot(nrow(df) == n_before)` |
| Interpreting logit coefficients directly | `marginaleffects::avg_slopes(model)` for AME |
| Reporting only point estimates | always plot — `modelplot`, `iplot`, `plot_slopes` |
| Manually formatting reg tables | `modelsummary` writes LaTeX/Word/HTML in one call |
| Reporting only the headline coefficient (no Table 2) | **Always** ship the multi-column M1→M6 main table — that is the centerpiece of an economics paper, not the abstract sentence |
| Coefficient table without any figures | An economics result needs **at least** F1 trend + F2 event study + F3 coefplot + F4 sensitivity — see the Default Output Spec |
| Saving plots as `.png` only | also `.pdf` for LaTeX submissions |
| Hard-coding dataset paths in scripts | use `here::here()` and `renv::init()` |
| Running tests manually each time | wrap into `targets::tar_make()` or Quarto |

---

## Typical project skeleton

```
project/
├── R/
│   ├── 01_clean.R              # produces data/analysis.rds
│   ├── 02_transform.R
│   ├── 03_describe.R
│   ├── 04_diagnose.R
│   ├── 05_model.R              # saves models to estimates/
│   ├── 06_robust.R
│   ├── 07_further.R
│   └── 08_tables_figures.R
├── data/
│   ├── raw/
│   └── analysis.rds
├── tables/
├── figures/
├── estimates/                  # saved fixest objects via saveRDS
├── logs/
├── renv.lock                   # package versions locked
├── _targets.R                  # or main.qmd / main.R
└── README.md
```

`_targets.R` (using `targets` package) or `main.qmd` (Quarto) at the top makes the whole pipeline reproducible:

```r
# main.R — minimal driver
source("R/01_clean.R")
source("R/02_transform.R")
source("R/03_describe.R")
source("R/04_diagnose.R")
source("R/05_model.R")
source("R/06_robust.R")
source("R/07_further.R")
source("R/08_tables_figures.R")
```

For Quarto authoring (combined narrative + code + tables/figures, render to PDF/HTML/Word), see [references/08-tables-plots.md](references/08-tables-plots.md) §12.

---

## Regtable (modelsummary / etable) cookbook (one-page recipe index)

`modelsummary(...)` and `fixest::etable(...)` are the two primitives behind every multi-regression table. The eight patterns above map to:

| Pattern | What varies across columns | Step |
|---|---|---|
| **A. Progressive controls** | covariate set / FE depth | 5.A — Table 2 |
| **B. Design horse race** | identification strategy (OLS / IV / DID / DML / PSM) | 5.B — Table 2-bis |
| **C. Multi-outcome** | dependent variable Y | 5.C — Table 2-ter |
| **D. Stacked Panel A / B** | horizon / sample (panel rows × spec columns) | 5.D — Table 2-quater |
| **E. IV reporting triplet** | first stage / reduced form / 2SLS | 5.E — Table 2-quinto |
| **F. Causal-orchestrator** | 1 column, full diagnostics (`att_gt` / `synthdid` / `causal_forest`) | 5.F |
| **G. Subgroup table** | subsample (full / female / male / Q1…Q4) | 7 — Table 3 |
| **H. Robustness master** | every robustness check stacked | 6.j — Table A1 |

Default `modelsummary` settings for AER house style:

```r
modelsummary(
  list("(1)" = m1, ..., "(N)" = mN),
  output    = "tables/tableN.tex",                                         # or .docx / .html
  stars     = c("*" = 0.1, "**" = 0.05, "***" = 0.01),                     # AER stars
  gof_omit  = "BIC|AIC|F|Log|Adj",
  coef_map  = c("training" = "Training"),                                   # pretty names
  notes     = c("Cluster-robust SE in parentheses.",
                "* p<0.10, ** p<0.05, *** p<0.01.")
)
# For multi-panel paper bundles, use gt::gt_group(modelsummary(...), modelsummary(...))
# or render via Quarto for a single .pdf / .docx / .html target.
```

---

## Figure factory (the 12 standard AER figures in R)

| # | Figure | R commands | Section |
|---|---|---|---|
| 1a | Raw trends (DID Figure 1) | `df %>% group_by(year, treat) %>% summarise(mean(y)) %>% ggplot()` | §1 |
| 1b | Treatment rollout heatmap | `panelView::panelview(...)` · `ggplot + geom_tile` | §1 |
| 2a | Event-study coefficients | `fixest::iplot(feols(y ~ sunab(G, t) | i + t))` | §3 (Step 3.5.1) |
| 2a' | Bacon weights | `bacondecomp::bacon` + ggplot | §3 |
| 2a'' | CS-DID dynamic effects | `did::ggdid(aggte(cs, type="dynamic"))` | §3 |
| 2b | First-stage scatter | `binsreg::binsreg(y=D, x=Z, w=X)` | §3 (Step 3.5.2) |
| 2c | RD canonical plot | `rdrobust::rdplot(y, x, c=0)` | §3 (Step 3.5.3) |
| 2c' | McCrary density | `rddensity::rdplotdensity(rdd, X)` | §3 |
| 2d | Matching love plot | `cobalt::love.plot(MatchIt::matchit(...))` | §3 (Step 3.5.4) |
| 2e | SCM trajectory | `tidysynth::plot_trends` · `synthdid::plot` · `Synth::path.plot` | §3 (Step 3.5.5) |
| 3 | Coefficient plot of main specs | `modelsummary::modelplot(list(m1,...,m6), coefs="training")` | §4 |
| 4a | Dose-response | `marginaleffects::plot_predictions(model, condition="dose")` | §5 |
| 4b | CATE distribution | `grf::causal_forest(...)` + `ggplot::geom_histogram(predict(cf)$predictions)` | §5 |
| 5 | Specification curve | `specr::plot(specr(...))` (see 6.k) | §7 |
| 6 | Sensitivity dashboard | `HonestDiD::createSensitivityPlot` · `EValue::evalue` | §7 (Step 6.l) |
| 7 | Final main figure | estimator-specific (`rdplot`, `iplot`, `Synth::path.plot`) | §8 |

> Every figure is exported via `ggsave()` as **both** `.pdf` (for LaTeX) and `.png ≥ 300 dpi` (for slides / web). Set `theme_set(theme_classic(base_size = 11))` once at the top of `master.R` for consistent styling.

---

## Method Catalog

### Classical OLS / Panel
```r
library(fixest); library(plm); library(sandwich); library(lmtest)
feols(y ~ X,                       data = df, cluster = ~ i)               # OLS (modern primary)
feols(y ~ X | fe1,                 data = df, cluster = ~ i)               # OLS + 1 FE
feols(y ~ X | fe1 + fe2,           data = df, cluster = ~ i)               # HD FE workhorse
feols(y ~ X | fe1 + fe2,           data = df, cluster = ~ fe1 + fe2)       # 2-way cluster
fepois(count ~ X | fe1 + fe2,      data = df, cluster = ~ i)               # Poisson + FE
feglm (y ~ X | fe1, data = df, family = binomial(link = "logit"),
       cluster = ~ i)                                                       # Logit + FE
plm   (y ~ X, data = df, model = "within",  index = c("i","t"))            # panel FE
plm   (y ~ X, data = df, model = "random",  index = c("i","t"))            # RE (Hausman: phtest)
```

### Difference-in-Differences
```r
library(fixest); library(did); library(didimputation); library(synthdid); library(bacondecomp); library(HonestDiD); library(DIDmultiplegtDYN)

feols(y ~ i(treated, post, ref = 0) | i + t, df, cluster = ~ i)            # 2×2
feols(y ~ sunab(first_treat, year) | i + year, df, cluster = ~ i)          # SA event study
att_gt(yname="y", tname="t", idname="i", gname="G", data=df,
       control_group="nevertreated", est_method="dr", clustervars="i")     # CS-DID
did_imputation(data=df, yname="y", gname="G", tname="t", idname="i",
               horizon=0:5, pretrends=-5:-1, cluster_var="i")               # BJS imputation
DIDmultiplegtDYN(df, "y", "i", "t", "training", effects=5, placebo=3)      # de Chaisemartin
synthdid_estimate(panel.matrices(df,"i","t","y","training"), ...)          # synthetic DID
bacon(y ~ training, data=df, id_var="i", time_var="t")                     # TWFE diagnostic
HonestDiD::createSensitivityResults(...)                                    # PT sensitivity
```

### Instrumental Variables / 2SLS
```r
library(fixest); library(AER); library(ivreg)
feols(y ~ X | D ~ Z, df, cluster = ~ firm_id)                              # workhorse w/ HD FE
fitstat(iv, ~ ivf + ivwald + sargan + cd)                                  # CD/KP/Sargan/F
AER::ivreg(y ~ D + X | Z + X, data = df)                                   # classic API
summary(iv, vcov. = sandwich, diagnostics = TRUE)                          # with diagnostics
```

### Regression Discontinuity
```r
library(rdrobust); library(rddensity); library(rdmulti)
rdrobust(y, x, c = 0, kernel = "triangular", bwselect = "mserd")           # Sharp RD
rdrobust(y, x, c = 0, fuzzy = D)                                           # Fuzzy RD
rddensity(X = x, c = 0)                                                    # McCrary density
rdplot(y, x, c = 0)
rdmc(y, x, cutoffs = c(0, 5, 10))                                          # multi-cutoff
```

### Matching / Reweighting
```r
library(MatchIt); library(WeightIt); library(cobalt)
matchit (D ~ X1 + X2, data = df, method = "nearest", ratio = 1)            # PSM
matchit (D ~ X1 + X2, data = df, method = "cem")                           # Coarsened EM
weightit(D ~ X1 + X2, data = df, method = "ebal")                          # entropy balancing
weightit(D ~ X1 + X2, data = df, method = "ps", estimand = "ATE")          # IPW
love.plot(matchit_obj, threshold = 0.10)                                   # SMD diagnostic
```

### Synthetic Control
```r
library(Synth); library(gsynth); library(tidysynth); library(synthdid)
Synth::synth(...)                                                           # ADH SCM
gsynth(y ~ training, data = df, index = c("i","t"), force = "two-way")     # generalized SC
synthdid_estimate(panel.matrices(...))                                      # synthetic DID
tidysynth::synthetic_control(df, ...) %>% generate_predictor(...) %>%
  generate_weights() %>% generate_control()
```

### ML Causal (Mode B — see §B)
```r
library(grf); library(DoubleML); library(mlr3); library(causalDML)
causal_forest(X, Y, W, num.trees = 4000, honesty = TRUE)                   # GRF causal forest
DoubleML::DoubleMLPLR$new(data, ml_l = lrn("regr.ranger"),
                           ml_m = lrn("regr.ranger"))                       # DML PLR
DoubleML::DoubleMLIRM$new(data, ...)                                       # DML interactive
predict(cf)$predictions                                                    # CATE per row
average_treatment_effect(cf, target.sample = "treated")
test_calibration(cf); variable_importance(cf)
policytree::policy_tree(X, gamma, depth = 3)                               # policy tree
```

### Robustness, Sensitivity & Inference
```r
library(fwildclusterboot); library(ri2); library(multcomp); library(robomit); library(EValue)
boottest(model, param = "training", clustid = "state", B = 9999)           # wild cluster bootstrap
ri2::conduct_ri(...)                                                        # randomization inference
robomit::o_test(...)                                                        # Oster δ
EValue::evalue(RR(1.45), lo = 1.10, hi = 1.91)                             # E-value
fwildclusterboot::boottest(..., type = "rademacher")                       # alt bootstrap dist
```

### Survival / Epi (Mode A — see §A)
```r
library(survival); library(survminer); library(survRM2); library(ipw); library(tmle); library(zelig)
survfit(Surv(time, event) ~ A, data = df)                                  # KM
coxph  (Surv(time, event) ~ A + X, data = df)                              # Cox
survreg(Surv(time, event) ~ A + X, data = df, dist = "weibull")            # AFT
rmst2  (time, status, arm, tau = 1825)                                     # RMST contrast
ipw::ipwpoint(...)                                                          # IPTW
tmle  (Y, A, W = X, ...)                                                    # TMLE
gfoRmula::gformula_survival(...)                                            # parametric g-formula
TwoSampleMR::mr(...)                                                        # Mendelian randomization
```

---

## When to hand off to other skills

- **Agent-native single-import Python workflow** (`import statspai as sp`) → `00-StatsPAI_skill`.
- **Explicit Python traditional stack** → `00.1-Full-empirical-analysis-skill`.
- **Stata `.do` pipeline** → `00.2-Full-empirical-analysis-skill_Stata`.
- **Cross-language Mixtape templates** (Python/R/Stata side-by-side) → `10-Jill0099-causal-inference-mixtape`.
- **Bayesian R workflow** (`brms`/`rstan`/`cmdstanr`) → `23-Learning-Bayesian-Statistics-baygent-skills`.
- **Paper drafting** after analysis → the writing skills in this repo.

This skill ends at Step 8 — `.tex` / `.docx` tables and `.pdf` figures. Paper drafting is out of scope.
