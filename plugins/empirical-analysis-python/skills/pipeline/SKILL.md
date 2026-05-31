---
name: Full-empirical-analysis-skill
description: Classical end-to-end empirical analysis workflow in the traditional Python econometric stack — pandas + numpy + scipy + statsmodels + linearmodels + pyfixest + rdrobust + econml + causalml + matplotlib/seaborn. **Defaults to economics empirical-paper style** (AER / QJE / AEJ) — every run produces a publication-ready output set with a multi-column regression table (M1→M6 progressive controls/FE) as the centerpiece, plus Table 1 (descriptives), mechanism / heterogeneity / robustness tables, and event-study + coefficient + trend figures. Covers the full 8-step pipeline an applied economist or quantitative social scientist runs on every paper — (1) data cleaning, (2) variable construction & transformation, (3) descriptive statistics & Table 1, (4) statistical diagnostic tests, (5) baseline empirical modeling, (6) robustness battery, (7) further analysis (mechanism, heterogeneity, mediation, moderation), (8) publication-ready tables & figures. **Also covers two parallel domain modes that share the same 8-step scaffolding** — **Mode A — Epidemiology / public health** (target-trial emulation via `zepid` / hand-rolled `pandas`, IPTW + g-formula + TMLE doubly-robust triplet via `zepid` / `econml` / `lifelines`, Mendelian randomization via `pymr` / `mrtool` (or `rpy2` → `MendelianRandomization`/`TwoSampleMR`), KM / AFT / Cox survival via `lifelines`, E-value sensitivity, principal stratification — STROBE / TRIPOD reporting), and **Mode B — ML causal inference** (DML via `econml.dml` / `doubleml`, S/T/X/R/DR meta-learners via `econml.metalearners` / `causalml`, causal forest via `econml.grf` / `causalml`, Dragonnet / TARNet / CEVAE neural causal via `causalml`, BCF via `pymc-bart` / `bcf-py`, matrix completion, CATE distribution + policy tree via `econml.policy` / `policytree-py`, off-policy evaluation, conformal causal via `mapie`, fairness audit via `fairlearn`, DAG learning via `causal-learn` / `cdt` / LLM-assisted). Prescribes which library to reach for at each step, shows the canonical code, and links to deeper `references/` files for variant-specific patterns. Use when the user asks for a **complete empirical analysis** in Python, wants to replicate an applied-economics paper from scratch, needs a reproducible workflow that is NOT opinionated on any single vertical package (contrast with StatsPAI), wants explicit control over every estimator and diagnostic, or asks "how do I write a full empirical pipeline in Python?". Also triggers when the user names a specific classical step in isolation — "winsorize at 1/99%", "run Breusch-Pagan", "build a Table 1 balance table", "do a placebo test", "event study plot", "mediation analysis" — and wants it wired into the broader pipeline. Mode A triggers on "target trial emulation", "IPTW", "TMLE", "Mendelian randomization", "STROBE", "公共健康", "流行病学". Mode B triggers on "DML", "double machine learning", "causal forest", "meta-learner", "Dragonnet", "BCF", "policy tree", "conformal causal", "fairness audit", "因果机器学习".
triggers:
  - full empirical analysis in Python
  - classical econometrics pipeline
  - traditional Python econometrics
  - end-to-end empirical workflow
  - pandas statsmodels linearmodels workflow
  - replicate an applied economics paper
  - data cleaning empirical
  - winsorize and standardize
  - variable construction
  - Table 1 summary statistics
  - balance table
  - correlation matrix
  - normality test
  - heteroskedasticity test
  - autocorrelation test
  - stationarity test
  - multicollinearity VIF
  - endogeneity test
  - baseline regression
  - panel fixed effects
  - DID workflow Python
  - event study
  - instrumental variables regression
  - regression discontinuity
  - propensity score matching
  - synthetic control python
  - double machine learning
  - robustness checks
  - placebo test
  - specification curve
  - alternative clustering
  - heterogeneity analysis
  - mechanism analysis
  - mediation analysis
  - moderation analysis
  - publication-ready regression table
  - coefplot
  - binscatter
  - event study plot
  # Mode A — Epidemiology / public health
  - epidemiology pipeline python
  - public health causal inference python
  - target trial emulation python
  - g-formula python
  - IPTW marginal structural model python
  - TMLE doubly robust python
  - HAL-TMLE python
  - Mendelian randomization python
  - MR-Egger weighted median python
  - STROBE TRIPOD reporting python
  - E-value sensitivity python
  - Kaplan-Meier AFT survival python
  - lifelines survival python
  - zepid epidemiology
  - 流行病学 python
  - 公共健康 python
  # Mode B — ML causal inference
  - ML causal inference python
  - double machine learning DML python
  - econml DoubleML
  - meta-learner S T X R DR python
  - causal forest GRF python
  - causalml meta-learner
  - Dragonnet TARNet CEVAE python
  - Bayesian causal forest BCF python
  - CATE distribution python
  - policy tree python
  - off-policy evaluation python
  - conformal causal prediction python
  - mapie conformal
  - fairness audit python
  - fairlearn audit
  - causal discovery PC NOTEARS python
  - causal-learn cdt
  - 因果机器学习 python
---

# Full Empirical Analysis — Classical Python Workflow

This skill is the *canonical* 8-step pipeline an applied economist runs on every empirical paper, written in the **traditional Python ecosystem** — no opinionated one-stop wrapper. Every step calls libraries directly (`pandas`, `numpy`, `scipy`, `statsmodels`, `linearmodels`, `pyfixest`, `rdrobust`, `econml`, `causalml`, `matplotlib`, `seaborn`), so the agent — or the user reading the agent's code — has full visibility and can swap any component.

**Companion skill**: if the user prefers a single-import agent-native DSL (`import statspai as sp`), route to `00-StatsPAI_skill` instead. **This skill is the opposite philosophy**: everything explicit, everything inspectable, every diagnostic run by hand, every plot shaped by the user.

## Philosophy

1. **Traditional stack, no magic.** Agents should be able to read every line and know exactly which library / estimator / standard error family is at work.
2. **Full pipeline, not just estimation.** 80% of the time on a real paper is steps 1–4 and 6–8. This skill treats them as first-class, not an afterthought.
3. **Rich outputs.** Every step produces at least one table or figure — never a single point estimate in isolation.
4. **Progressive disclosure.** SKILL.md gives the canonical call at each step; `references/` holds variant-specific depth (dozens of tests, estimator-specific diagnostics, plot recipes).
5. **Reproducible.** Every code block is runnable after `pip install -r requirements.txt` and `df = pd.read_csv(...)`.

---

## Three domain modes (default = AER econ; alternates = epi & ML-causal)

The default playbook above is **AER-style applied econometrics** — the AEA convention: written-out estimating equation, identifying assumption, design horse-race, full robustness gauntlet. The skill **also** ships two parallel sub-pipelines for the other two big causal-inference traditions, each reusing the same Steps 1–4 (cleaning / construction / descriptives / diagnostics) and Step 8 (tables & figures) — only Step 5 (estimator) and Step 6/7 (robustness / mechanism) swap libraries:

| Mode | Reader convention | Step-5 estimator stack | Reporting stack | Jump to |
|---|---|---|---|---|
| **Default — Applied Econ (AER / QJE / AEJ)** | "Show the equation + identifying assumption + design horse-race; controls visible; clustered SE" | DID / IV / RD / SCM / matching / `pyfixest.feols` HDFE | AER house-style multi-column `pf.etable` / `Stargazer` + 8-section paper layout | Steps 1 → 8 (entire playbook below) |
| **Mode A — Epidemiology / Public Health** | "STROBE / TRIPOD-AI; target trial protocol; doubly-robust estimand; absolute & relative risk; KM survival" | Target-trial emulation · IPTW (`zepid`) · g-formula (`zepid` / hand-rolled) · TMLE (`zepid.causal.gformula` / `econml`) · Mendelian randomization (`pymr` / `rpy2`+`TwoSampleMR`) · KM/AFT (`lifelines`) | Same `pf.etable` + risk-difference / hazard-ratio / E-value rows | §A. Epidemiology pipeline |
| **Mode B — ML Causal Inference** | "DML / meta-learners / causal forest / DR-learner; CATE distribution; policy value" | DML (`econml.dml` / `doubleml`) · S/T/X/R/DR-Learner (`econml.metalearners` / `causalml`) · GRF causal forest (`econml.grf`) · Dragonnet/TARNet/CEVAE (`causalml`) · BCF (`pymc-bart`/`bcf-py`) · matrix completion | `pf.etable` ML horse-race + CATE plot + policy-value table + conformal PI (`mapie`) | §B. ML causal pipeline |

**How to invoke a non-default mode** (Claude / agent picks this up from the user's wording):

| User says... | Mode the skill switches to |
|---|---|
| "Run a DID / IV / RD / event study", "AER table", "applied micro" | Default (AER econ) — Steps 1 → 8 |
| "Target trial emulation", "g-formula", "IPTW", "TMLE", "Mendelian randomization", "STROBE / TRIPOD", "公共健康 / 流行病学", "epi pipeline", "RWE study", "cohort study", "case-control" | Mode A (Epi) — §A |
| "DML", "double machine learning", "causal forest", "meta-learner", "CATE", "Dragonnet", "BCF", "policy learning", "conformal causal", "fairness audit", "ML causal", "uplift modeling", "因果机器学习" | Mode B (ML causal) — §B |
| "Mix" (e.g. "estimate DID + then ML CATE on the heterogeneity") | Default + Mode B in sequence — every estimator returns a coefficient + SE pair, drop them all into one `pf.etable(...)` for the horse-race column |

The three modes share **the same Step 1–4 cleaning / Table 1 / diagnostics scaffolding, the same Step 8 export stack, and the same DAG-first identification logic** — switching modes only changes which Step-5 estimator family you reach for, not the surrounding paper structure. If you only want descriptive stats / Table 1 / a balance check, the AER `tableone` / `gtsummary`-style calls in Step 3 work identically across all three modes.

---

## Default Output Spec — Economics Empirical Paper

This skill defaults to the **applied-economics paper convention**. Unless the user explicitly asks for a single point estimate, every run produces the full publication-ready output set below. Treat it as the contract of Step 8 — **mandatory**, not opt-in.

### Required tables (always produced)

| # | Table | Source / library | Saves to |
|---|---|---|---|
| **T1** | Summary statistics & balance (treated vs control, with SMD / p-values) | `pandas.describe` + custom `table1()` (Step 3) | `tables/table1_balance.xlsx` + `.docx` + `.tex` |
| **T2** ★ | **Main results — multi-column regression M1→M6** (progressive controls + FE) | `pyfixest.feols` × 6 specs → `pf.etable()` / `Stargazer` (Step 5–6) | `tables/table2_main.xlsx` + `.docx` + `.tex` |
| **T3** | Mechanism / outcome ladder — same treatment, 3+ outcomes side-by-side | `feols` looped over `y ∈ {Y1, Y2, Y3, Y_main}` → `pf.etable` | `tables/table3_mechanism.xlsx` + `.docx` + `.tex` |
| **T4** | Heterogeneity — subgroup × main coef (gender, age, region, …) | subgroup `feols` × Wald → `pf.etable` (Step 7) | `tables/table4_heterogeneity.xlsx` + `.docx` + `.tex` |
| **T5** | Robustness battery — alt SE / alt cluster / alt sample / placebo, in **one** table | `feols` × variants → `pf.etable` (Step 6) | `tables/table5_robustness.xlsx` + `.docx` + `.tex` |

> **★ Table 2 is the centerpiece of every economics paper.** It is the multi-column regression table that walks the reader from raw correlation (M1) to the fully-specified design (M6: 2-way FE + interacted FE + cluster-robust SE). Do **not** collapse it into a single column. Do **not** report only the headline coefficient. The progression *is* the credibility argument: if M1→M6 is monotone and stable, the design is plausibly identifying; if it collapses on adding FE, that *is* the result.
>
> **Canonical 6 columns, in order:**
> 1. **M1** raw bivariate (`y ~ treat`)
> 2. **M2** + demographics (`+ age + edu`)
> 3. **M3** + sector controls (`+ tenure / firm_size / industry`)
> 4. **M4** + unit FE (`| worker_id`)
> 5. **M5** + 2-way FE (`| worker_id + year`)
> 6. **M6** + interacted FE (`| worker_id + year + industry^year`) with cluster-robust SE

### Required figures (always produced)

| # | Figure | Source / library | Saves to |
|---|---|---|---|
| **F1** | Trend / motivation — treated vs control over time, with policy line | `df.groupby([year, treat])[y].mean().unstack().plot()` (Step 3) | `figures/fig1_trend.png` (300 dpi, **必须导出 PNG**) + `.pdf` |
| **F2** | Event-study coefficients with 95% CI, base period at –1 | `pf.feols(... ~ i(rel_time, ref=-1) ...)` → `pf.iplot()` (Step 5) | `figures/fig2_event_study.png` (300 dpi, **必须导出 PNG**) + `.pdf` |
| **F3** | Coefficient plot across specs M1→M6 | `matplotlib.errorbar` over the 6 fitted models (Step 8) | `figures/fig3_coefplot.png` (300 dpi, **必须导出 PNG**) + `.pdf` |
| **F4** | Robustness / sensitivity curve — spec curve, HonestDiD, or cluster-comparison | spec_curve loop or `honest_did` plot (Step 6) | `figures/fig4_sensitivity.png` (300 dpi, **必须导出 PNG**) + `.pdf` |

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
- **Design does not support a figure** (cross-section → no event study) — skip with a printed note explaining why; do **not** silently drop.
- **N=1 treated unit (synthetic control)** — replace F1/F2 with the SCM trajectory + placebo distribution; T1–T5 still apply.

---

## Required Libraries

```bash
pip install pandas numpy scipy matplotlib seaborn \
            statsmodels linearmodels pyfixest \
            rdrobust rddensity \
            econml causalml \
            stargazer  # publication-ready regression tables
# Optional but commonly needed:
pip install missingno   # missing-data visualization
pip install pyreadstat  # Stata .dta / SPSS .sav import
pip install arch        # GARCH, unit-root tests, HAC
pip install pingouin    # clean stats tests wrapper
pip install pysynth     # synthetic control (N=1 treated)
```

---

## The 8 Steps — Canonical Pipeline (mapped to AER paper sections)

```
┌──────────────────────────────────────────────────────────────────────┐
│ Step −1 Pre-Analysis Plan (PAP)   statsmodels.stats.power / mde     │
│ Step 0  Sample log + data contract sample_log/asserts/JSON dump      │
│ Step 1  Data cleaning              missing / outliers / dtype / join │
│ Step 2  Variable construction      log / winsorize / std / encode    │
│ Step 2.5 Empirical strategy        equation × ID assumption + pre-reg│
│ Step 3  Descriptive statistics     Table 1 / corr / distribution     │
│ Step 3.5 Identification graphics   event-study/1st-stage/McCrary/love│
│ Step 4  Diagnostic tests           normality / hetero / autocorr / VIF│
│ Step 5  Baseline modeling          OLS / panel / IV / DID / RD / SC  │
│ Step 6  Robustness battery         placebo / subsample / spec curve  │
│ Step 7  Further analysis           mechanism / heterogeneity / mediation│
│ Step 8  Tables & figures           stargazer / coefplot / event study│
└──────────────────────────────────────────────────────────────────────┘
```

The 8 steps mirror the canonical sections of an applied AER / QJE / AEJ paper. Each step is one paper section and emits a paper-ready artifact on disk:

```
Paper section               Step  Python moves
─────────────────────────── ───── ────────────────────────────────────────────────
Pre-Analysis Plan           −1    statsmodels.stats.power + freeze pap.json
§1. Data                     0    sample_log + 5-check data contract → JSON
§1. Data                     1    pandas read_*/dropna/dtype/merge(validate=)
§1. Data                     2    np.log/np.arcsinh/winsorize/groupby.shift/diff
§1.1 Descriptives (Table 1)  3    df.describe() · table1_with_smd · seaborn
§2. Empirical Strategy       2.5  equation × ID assumption table + pre-reg
§3. Identification graphics  3.5  pf.iplot · binscatter · rdplot · mccrary · love
§3.5 Diagnostics             4    statsmodels.diagnostic + scipy.stats
§4. Main Results (Table 2)   5    pf.feols/IV2SLS/CausalForest · pf.etable / Stargazer
§5. Heterogeneity (Table 3)  7    pf.feols(... + i(.):X) · marginaleffects-py
§6. Mechanisms / Channels    7    Baron-Kenny · econml.dml · outcome ladder
§7. Robustness gauntlet      6    placebo · oster · honestdid · spec_curve · 2-way
§8. Replication package      8    Stargazer.render_latex · pf.etable("docx") · result.json
```

Below is the canonical code at each step. **All examples share one running narrative** — a labor-economics panel where `training` (treatment) affects `log_wage` (outcome), with covariates `age`, `edu`, `tenure`, panel keys `worker_id` / `firm_id` / `year`. Column names and parameter values are **illustrative** — substitute the real ones from the user's DataFrame. Only library names and call shapes are normative.

> **When a step has many variants** (e.g. staggered DID has five different estimators; heteroskedasticity has four classic tests), SKILL.md shows the one you reach for first and links to `references/NN-<topic>.md` for the rest. **Read the reference file when the user's case doesn't fit the default.**

---

## Paper-ready figure & table inventory (what to produce by section)

A modern AER paper has **5–7 figures** and **3–5 main tables** + an appendix robustness table. Every step below leaves at least one numbered artifact on disk. Default file names assume parallel `.tex` / `.docx` / `.xlsx` exports (the agent should produce all three so co-authors can edit in Word, the build system can use LaTeX, and editors can edit raw numbers in Excel). **所有图片必须同时保存 PNG（≥300 dpi）和 PDF 两种格式。**

| § | Artifact | Python primitive | Filenames |
|---|---|---|---|
| §1 | **Figure 1**: raw trends / treatment rollout | `df.groupby([time,treat])[y].mean().unstack().plot()` · `seaborn.heatmap` for staggered rollout | `figures/fig1_trend.png`(300dpi)+`.pdf` |
| §1 | **Table 1**: summary stats (full / treated / control + Δ + SMD) | `table1(df, by=, cols=)` (Step 3.b) → write LaTeX/Word/Excel | `tables/table1_balance.xlsx/.docx/.tex` |
| §3 | **Figure 2**: identification graphic (event-study / first-stage / McCrary / RD scatter / SCM trajectory) | `pf.iplot(es)` · `binscatter` · `rdplot` · `rddensity` · `synthdid` | `figures/fig2_event_study.png`(300dpi)+`.pdf` |
| §4 | **Table 2**: main results — progressive controls M1→M6 | `pf.etable([m1...m6])` · `Stargazer([m1.fit ... m6.fit])` | `tables/table2_main.xlsx/.docx/.tex` |
| §4 | **Table 2-bis**: design horse-race (OLS / IV / DID / DML) | `pf.etable([ols, iv, did, dml])` | `tables/table2b_designs.xlsx/.docx/.tex` |
| §4 | **Figure 3**: coefficient plot across specs | `pf.coefplot([m1...m6], coefs=["training"])` | `figures/fig3_coefplot.png`(300dpi)+`.pdf` |
| §5 | **Table 3**: heterogeneity by subgroup | `pf.etable(g_full, g_male, g_fem, g_q1...q4)` | `tables/table3_heterogeneity.xlsx/.docx/.tex` |
| §5 | **Figure 4**: dose-response / CATE | `econml.CausalForestDML(...).effect()` + matplotlib hist | `figures/fig4_cate.png`(300dpi)+`.pdf` |
| §6 | **Table 4**: mechanism / outcome ladder | loop `pf.feols` over outcomes → `pf.etable` | `tables/table4_mechanism.xlsx/.docx/.tex` |
| §7 | **Table A1**: robustness master (one column per check) | `pf.etable([base, no99, balpan, dropearly, wfe, cl2way, logy, ihsy, psm, ebal])` | `tables/tableA1_robustness.xlsx/.docx/.tex` |
| §7 | **Figure 5**: spec curve | hand-rolled `itertools.product` + matplotlib `errorbar` | `figures/fig5_spec_curve.png`(300dpi)+`.pdf` |
| §7 | **Figure 6**: sensitivity (HonestDiD / Oster / E-value) | `HonestDiD` · `oster_bound` · `evalue` | `figures/fig6_sensitivity.png`(300dpi)+`.pdf` |
| §8 | **Replication bundle**: all tables in one document | `pf.etable([...] + extra=[...], type="docx")` · pylatex / `texdoc`-style multi-panel | `replication/paper_tables.xlsx/.docx/.tex` |

> Every Python estimator above (`pf.feols` / `IV2SLS` / `att_gt` via R-callout / `CausalForestDML`) returns a result object that can be passed straight into `pf.etable(...)` / `pf.coefplot(...)` / `Stargazer(...)`. Don't hand-roll LaTeX from `df.to_latex()`, and don't render Word via `python-docx` directly — `pf.etable` / `Stargazer` apply book-tab borders, AER stars, and the right SE label automatically. For deeper export recipes (LaTeX / Word / Markdown variants, multi-panel `.docx`, full `gtsummary`-style flow), see [`references/08-tables-plots.md`](references/08-tables-plots.md).

---

## Export cookbook — LaTeX / Word / Excel in one block

**关键规则（必须遵守）：每个表格必须同时导出三种格式——Excel(.xlsx)、Word(.docx)、LaTeX(.tex)。每个图片必须同时保存PNG(≥300dpi)和PDF两种格式。**

Three tiers, picked by **scope**:

| Tier | Use when | API | Hot kwargs |
|---|---|---|---|
| **1. Single multi-column table** | Exporting *one* Table 2 / Table 3 / Table A1 with progressive columns | `pf.etable([m1,...,mN], type="tex"/"docx"/"xlsx", file="...", headers=[...], digits=3, signif_code=[0.1,0.05,0.01])` — or `Stargazer([m1.fit,...,mN.fit]).render_latex()` for statsmodels-only | `keep=`, `drop=`, `coef_map=`, `headers=`, `digits=`, `signif_code=`, `fixef_rm=`, `notes=` |
| **2. Multi-panel paper format** (Tables 2 + 3 + A1 + A2 in one file) | Producing the *paper-tables block* — main + heterogeneity + robustness + placebo as a single document | Stack via repeat `pf.etable(..., extralines=...)` calls, or use `gtsummary`-style chained tables; for true single-file multi-panel, write to a `.tex` then concat | first panel: write; subsequent: append; surround with LaTeX `\section{}` headers |
| **3. Full session bundle** (the Stata `collect` / R `gt` equivalent) | Replication appendix that mixes summary stats + balance + multiple regression tables + headings + prose in **one** file | Compose programmatically with `pylatex` / `python-docx` / `quarto` — render once. Or use `statsmodels.iolib.summary2.summary_col` for a quick concat of tables. | journal-style template + per-section heading + footnote macros |

**Journal styling — pick the right `signif_code` and SE label.** AEA convention is `[0.1, 0.05, 0.01]` and SE label "Cluster-robust standard errors in parentheses". Define a wrapper once at the top of `master.py`:

```python
# top of master.py — journal house-style wrapper
AER_SIGNIF = [0.1, 0.05, 0.01]
AER_NOTES  = ("Cluster-robust standard errors in parentheses. "
              "* p<0.10, ** p<0.05, *** p<0.01.")

def aer_table(models, *, file, headers=None, coef_map=None):
    # 同时导出三种格式：.xlsx（用于编辑）、.docx（用于Word）、.tex（用于LaTeX）
    base, ext = os.path.splitext(file)
    for ext, type_ in [(".xlsx", "xlsx"), (".docx", "docx"), (".tex", "tex")]:
        pf.etable(models, type=type_, file=base + ext,
                  headers=headers, coef_map=coef_map,
                  digits=3, signif_code=AER_SIGNIF, notes=AER_NOTES)
```

For the multi-panel `.docx` / `.xlsx` and Markdown / Quarto cookbook (single-file paper-tables bundle), see [`references/08-tables-plots.md`](references/08-tables-plots.md).

---

## Step −1 — Pre-Analysis Plan (pre-data; AEA RCT Registry style)

Before touching the data, write down (a) the population, (b) the design, (c) the **minimum detectable effect (MDE)** under the planned sample size and α=0.05, β=0.20. Persist the result as `pap.json` so a referee can verify the design was powered before, not after, the data were seen.

```python
import json
from statsmodels.stats.power import TTestIndPower, NormalIndPower
from statsmodels.stats.proportion import samplesize_proportions_2indep_onetail

# Two-sample MDE for a continuous outcome (Cohen's d framing)
analysis = TTestIndPower()
n_required = analysis.solve_power(effect_size=0.20, power=0.80, alpha=0.05, ratio=1.0)
print(f"n per arm for d=0.20, 80% power: {n_required:.0f}")

# Solve for MDE given fixed n
mde = analysis.solve_power(nobs1=2000, power=0.80, alpha=0.05, ratio=1.0)
print(f"MDE (Cohen's d) at n=2000 per arm: {mde:.3f}")

# Cluster-randomized RCT — design effect = 1 + (m-1)·ICC
m, icc = 50, 0.05
deff = 1 + (m - 1) * icc
n_eff_required = analysis.solve_power(effect_size=0.20, power=0.80, alpha=0.05) * deff
print(f"n per arm under ICC={icc}, cluster size={m}: {n_eff_required:.0f}")

# DID: use Frison-Pocock / Bloom (1995) — see references/05-modeling.md §5.4
# RD: power via Monte Carlo — see references/05-modeling.md §5.5

# Persist the protocol — the referee will ask whether the design was powered ex ante
pap = {
    "population":        "manufacturing workers, 2010–2020",
    "treatment":         "training (binary, staggered adoption)",
    "outcome":           "log_wage",
    "estimand":          "ATT",
    "design":            "staggered DID, Callaway–Sant'Anna",
    "alpha":             0.05,
    "power_target":      0.80,
    "mde_d":             0.20,
    "n_planned":         12000,
    "frozen_at":         "2026-01-15T09:00:00Z",
    "git_sha":           "<paste>",
}
with open("artifacts/pap.json", "w") as f:
    json.dump(pap, f, indent=2)
```

Commit `artifacts/pap.json` in the repo **before** Step 1. AEA RCT Registry / OSF preregistration tools accept it as the analysis-plan exhibit.

---

## Step 0 — Sample-construction log & 5-check data contract

An AER §1 *Data* section has three jobs: (a) describe sources, (b) document **every** sample restriction (the "footnote 4" sample log), (c) lock the panel structure. The data contract is the cure for "mysterious sample-size shrinkage" bugs in the response letter.

### 0.1 Sample-construction log (footnote 4)

```python
import pandas as pd, json

sample_log = []

df_raw = pd.read_csv("raw.csv")
sample_log.append(("0. raw",                     len(df_raw)))

df1 = df_raw.dropna(subset=["wage"])
sample_log.append(("1. drop missing wage",        len(df1)))

df2 = df1[df1["age"].between(18, 65)]
sample_log.append(("2. drop age outside 18-65",   len(df2)))

df3 = df2[df2["industry"].isin({"manuf","construction","transport"})]
sample_log.append(("3. keep target industries",   len(df3)))

df = df3
for label, n in sample_log:
    print(f"  {label:<30s}  N = {n:>10,d}")

with open("artifacts/sample_construction.json", "w") as f:
    json.dump(sample_log, f, indent=2)
```

Paste the printed lines verbatim as footnote 4 of the paper.

### 0.2 Five-check data contract (go / no-go gate)

```python
import pandas as pd, numpy as np, json
from scipy import stats

def data_contract(df, *, y, treatment, id=None, time=None, covariates=()):
    """Return a go/no-go dict. Stop the pipeline if any required check fails."""
    keys = [y, treatment] + ([id, time] if id and time else []) + list(covariates)
    c = {
        "n_obs":              len(df),                                          # 1. shape
        "dtypes":             df[keys].dtypes.astype(str).to_dict(),            # 2. dtypes
        "n_missing":          df[keys].isna().sum().to_dict(),                  # 3. missingness
        "n_dupes_on_keys":    0,
        "panel_balanced":     None,
        "cohort_sizes":       None,
    }

    if id and time:
        c["n_dupes_on_keys"] = int(df.duplicated([id, time]).sum())             # 4. dups
        bal = df.groupby(id).size()
        c["panel_balanced"]        = bool((bal == bal.max()).all())             # 5. balance
        c["n_dropped_by_balance"]  = int((bal != bal.max()).sum())

        if "first_treat_year" in df.columns:
            c["cohort_sizes"] = (
                df.drop_duplicates(id).groupby("first_treat_year")
                  .size().to_dict()
            )

    c["y_range"]         = (float(df[y].min()), float(df[y].max()))
    c["treatment_share"] = float(df[treatment].mean())

    # MCAR sniff test (Rubin) — if missing(y) is associated with covariates,
    # listwise deletion biases the estimate. Use MI / IPW instead.
    miss_y = df[y].isna()
    c["mcar_hint"] = "likely MCAR (listwise OK)"
    if miss_y.any() and (~miss_y).any():
        for cov in covariates:
            if df[cov].dtype.kind in "fi":
                _, p = stats.ttest_ind(df.loc[miss_y, cov].dropna(),
                                        df.loc[~miss_y, cov].dropna(),
                                        equal_var=False)
                if p < 0.05:
                    c["mcar_hint"] = (f"NOT MCAR (y-miss differs on {cov}, p={p:.3f}) "
                                       f"→ use MI / IPW, NOT listwise drop")
                    break
    return c

contract = data_contract(df, y="wage", treatment="training",
                          id="worker_id", time="year",
                          covariates=["age", "edu", "tenure"])

assert contract["n_dupes_on_keys"] == 0,         f"dup (id, time): {contract['n_dupes_on_keys']}"
assert all(v == 0 for v in contract["n_missing"].values()), \
                                                 f"NaNs on keys: {contract['n_missing']}"

with open("artifacts/data_contract.json", "w") as f:
    json.dump(contract, f, indent=2, default=str)
```

If any assertion fires, **stop** and fix it in pandas. Estimators silently drop NaN rows downstream — this contract is the cheapest insurance against "why did N drop from 12,000 to 9,800 between Table 1 and Table 2?" referee questions.

---

### Step 1 — Data cleaning

Deeper patterns: [references/01-data-cleaning.md](references/01-data-cleaning.md) — missing-value strategies (MCAR/MAR/MNAR), outlier detection (IQR / z-score / Mahalanobis), dtype coercion, merging gotchas, panel-structure validation, deduplication.

```python
import pandas as pd
import numpy as np

df = pd.read_csv("raw.csv")

# 1a. Inspect — always do this first
df.info()                          # dtypes + non-null counts
df.describe(include="all").T       # numeric + categorical
df.isna().mean().sort_values(ascending=False)  # missingness share per column

# 1b. Fix dtypes (strings-that-should-be-numeric are the #1 silent bug)
df["year"]   = pd.to_numeric(df["year"],   errors="coerce")
df["wage"]   = pd.to_numeric(df["wage"],   errors="coerce")
df["gender"] = df["gender"].astype("category")
df["date"]   = pd.to_datetime(df["date"],  errors="coerce")

# 1c. Missing values — decide PER VARIABLE, never blanket-drop
key_vars = ["wage", "training", "worker_id", "year"]
df = df.dropna(subset=key_vars)                       # drop rows missing on keys
df["tenure"] = df["tenure"].fillna(df["tenure"].median())  # median-impute numeric covariate
df["union"]  = df["union"].fillna("unknown")               # explicit "unknown" for categorical

# 1d. Outliers — flag first, winsorize in Step 2
df["wage_z"] = (df["wage"] - df["wage"].mean()) / df["wage"].std()
outlier_mask = df["wage_z"].abs() > 4
print(f"{outlier_mask.sum()} rows flagged as |z|>4 on wage")

# 1e. Deduplicate on the panel key
dupes = df.duplicated(subset=["worker_id", "year"], keep=False)
assert dupes.sum() == 0, f"{dupes.sum()} duplicate (worker_id, year) pairs"

# 1f. Merge auxiliary data — use validate= to catch silent m:m blowups
df = df.merge(firm_chars, on="firm_id", how="left", validate="many_to_one")

# 1g. Panel structure check — balanced vs. unbalanced
panel_summary = df.groupby("worker_id")["year"].agg(["count", "min", "max"])
print(panel_summary.describe())
is_balanced = (panel_summary["count"] == panel_summary["count"].max()).all()
print(f"Balanced: {is_balanced}")
```

**Key principle**: `pandas` + explicit decisions. **Never** silently drop rows inside an estimator — all row exclusions happen in Step 1 with a printed count.

---

### Step 2 — Variable construction & transformation

Deeper patterns: [references/02-data-transformation.md](references/02-data-transformation.md) — log/ihs/Box–Cox, winsorizing vs. trimming, within-group standardization, one-hot vs. ordinal vs. target encoding, interaction terms, lag/lead operators, first differences, deflation with CPI.

```python
# 2a. Log / IHS transform (skewed positive variables)
df["log_wage"] = np.log(df["wage"].clip(lower=1))             # floor at 1 to avoid -inf
df["ihs_assets"] = np.arcsinh(df["assets"])                    # handles zero / negative

# 2b. Winsorize (top/bottom 1%) — reduces outlier influence without dropping rows
from scipy.stats.mstats import winsorize
df["wage_w"] = winsorize(df["wage"], limits=[0.01, 0.01]).data

# 2c. Standardize (z-score) — for interpretability or ML
df["age_std"] = (df["age"] - df["age"].mean()) / df["age"].std()

# 2d. Categorical encoding
df = pd.get_dummies(df, columns=["industry"], prefix="ind", drop_first=True)

# 2e. Interaction & polynomial
df["age_sq"]          = df["age"] ** 2
df["training_x_edu"]  = df["training"] * df["edu"]

# 2f. Panel operators — first difference, lag, lead, within-group mean
df = df.sort_values(["worker_id", "year"])
df["wage_l1"]   = df.groupby("worker_id")["log_wage"].shift(1)      # lag
df["wage_f1"]   = df.groupby("worker_id")["log_wage"].shift(-1)     # lead
df["d_wage"]    = df.groupby("worker_id")["log_wage"].diff()        # Δy_it
df["wage_mean"] = df.groupby("worker_id")["log_wage"].transform("mean")  # within-unit mean

# 2g. Treatment timing variables for staggered DID
df["first_treat_year"] = df.groupby("worker_id")["training"] \
                           .transform(lambda s: s.idxmax() if s.any() else np.nan)
df["rel_time"] = df["year"] - df["first_treat_year"]
```

---

### Step 2.5 — Empirical strategy (write the equation + identifying assumption)

This is the heart of an AER paper. **Before any code**, write down the equation explicitly and state the identifying assumption. Vague identification language is the single most common reason a referee rejects an applied paper. Persist the strategy as `strategy.md` so it is a dated, version-controlled artifact — *not* a post-hoc rationalization written after seeing the coefficient.

#### Equation × identifying assumption × Python estimator (decision table)

| Design | Estimating equation | Identifying assumption | Python estimator |
|---|---|---|---|
| 2×2 DID | `Y_it = α_i + λ_t + β·D_it + X'γ + ε_it` | parallel trends conditional on X | `pf.feols("y ~ i(treated, post, ref=0) | i + t", df, vcov={"CRV1":"i"})` |
| Event-study (CS / SA) | `Y_it = α_i + λ_t + Σ_{e≠-1} β_e · 1{t-G_i = e} + ε_it` | no anticipation + group-time PT | `pf.feols("y ~ i(rel, ref=-1) | i + t", df)` · `att_gt` (R callout) · `did_imputation` |
| 2SLS | `Y_i = α + β·D_i + X'γ + ε_i;  D_i = π·Z_i + X'δ + u_i` | exclusion + relevance + monotonicity | `linearmodels.iv.IV2SLS.from_formula("y ~ X + [D ~ Z]", df)` |
| Sharp RD | `Y_i = α + β·1{X_i ≥ c} + f(X_i) + ε_i` (local poly) | continuity of E[Y(0)\|X] at c, no manipulation | `rdrobust(y, x, c=0)` (+ `rddensity`) |
| SCM | `Ŷ_1t(0) = Σ_j ŵ_j Y_jt`, τ_t = `Y_1t − Ŷ_1t(0)` for t≥T_0 | pre-period fit + interpolation validity | `pysynth` · `synthdid` (R callout) |
| Selection-on-observables (matching/IPW/DML) | `Y_i = m(X_i) + β·D_i + ε_i` (Robinson partialling-out) | unconfoundedness + overlap | `econml.dml.DML` · `econml.dr.DRLearner` · `causalml.matching.PSM` |

#### Design picker (when the user is unsure)

```
                 ┌─ running var + cutoff ───────────────── RDD       (rdrobust)
                 │
                 ├─ exogenous instrument Z ─────────────── IV/2SLS   (linearmodels.IV2SLS)
data + question ─┤
                 ├─ pre/post × treat/control ─┬ 2 periods  ── 2×2 DID (pf.feols + i())
                 │                            └ staggered  ── CS / SA / BJS  (att_gt / sunab / did_imputation)
                 │
                 ├─ 1 treated unit + donor pool + long pre ── SCM    (pysynth / synthdid)
                 │
                 ├─ high-dim X, selection-on-observables ── ML causal (econml.dml / causalml — see §B)
                 │
                 └─ none of the above ──────────────────── matching + sensitivity (causalml + evalue)
```

#### Pre-registration `strategy.md` template

```python
from pathlib import Path
strategy = """\
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

- Selection of G_i on Y_i(0)              → bacondecomp + honestdid sensitivity
- Spillover within firm                    → cluster at firm_id, also try firm_id × year
- Anticipation in pre-period               → include lead in event study

## Fallback estimators (Step 6 robustness)

- Sun–Abraham via `pf.feols("y ~ sunab(G, t) | i + t", df)` (or R callout to `fixest::sunab`)
- Borusyak-Jaravel-Spiess via `did_imputation` (R callout)
- Synthetic DID via `synthdid` (R callout)
"""
Path("artifacts/strategy.md").write_text(strategy)
```

Commit `artifacts/strategy.md` in the repo **before** running Step 5 / Step 6. The `git log` of this file *is* the analysis plan.

---

### Step 3 — Descriptive statistics & Table 1

Deeper patterns: [references/03-descriptive-stats.md](references/03-descriptive-stats.md) — stratified Table 1 with SMDs, weighted descriptives, distributional comparison (ECDF, QQ), correlation heatmaps + clustering, panel balance checks, time-series seasonality plots.

```python
import seaborn as sns
import matplotlib.pyplot as plt

# 3a. Full-sample summary — classic "Table 1, column 1"
stats = df[["log_wage","age","edu","tenure","training"]].describe().T
stats["N"] = df[["log_wage","age","edu","tenure","training"]].notna().sum()
print(stats[["N","mean","std","min","25%","50%","75%","max"]])

# 3b. Stratified Table 1 (treated vs. control + t-test / SMD)
from scipy import stats as sps
def table1(df, by, cols):
    rows = []
    for c in cols:
        t, ctrl = df.loc[df[by]==1, c], df.loc[df[by]==0, c]
        smd = (t.mean() - ctrl.mean()) / np.sqrt((t.var()+ctrl.var())/2)
        p = sps.ttest_ind(t.dropna(), ctrl.dropna(), equal_var=False).pvalue
        rows.append([c, t.mean(), t.std(), ctrl.mean(), ctrl.std(), smd, p])
    return pd.DataFrame(rows, columns=["var","treat_mean","treat_sd",
                                       "ctrl_mean","ctrl_sd","SMD","p"])
t1 = table1(df, by="training", cols=["log_wage","age","edu","tenure"])
print(t1.round(3))

# 3c. Correlation heatmap
corr = df[["log_wage","age","edu","tenure","training"]].corr()
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, vmin=-1, vmax=1)
plt.tight_layout(); plt.savefig("fig_corr.pdf")

# 3d. Distribution plot — density by treatment status
fig, ax = plt.subplots(figsize=(6,4))
for g, sub in df.groupby("training"):
    sub["log_wage"].plot.kde(ax=ax, label=f"training={g}")
ax.set_xlabel("log wage"); ax.legend(); plt.savefig("fig_dist.pdf")

# 3e. Time trends — treated vs. control (the DID motivation plot)
trend = df.groupby(["year","training"])["log_wage"].mean().unstack()
trend.plot(marker="o"); plt.ylabel("mean log wage"); plt.savefig("fig_trend.pdf")

# 3f. Panel balance diagnostic — how many units observed each year?
df.groupby("year")["worker_id"].nunique().plot(kind="bar")
plt.ylabel("# unique workers"); plt.savefig("fig_panel_balance.pdf")
```

---

### Step 3.5 — Identification graphics (Section "Identification, graphical evidence")

**AER convention: the identification figure precedes the regression table.** The reader should see graphical evidence that PT holds / first stage is strong / RD jumps cleanly *before* you ask them to trust your point estimate.

#### 3.5.1 Event-study figure + numerical pre-trends test (DID identification)

Pre-period coefficients ≈ 0 (with the −1 reference period normalized to zero) is the visual evidence for parallel trends. Pair the **figure** with a **numerical** pre-trends test so reviewers don't have to eyeball it.

```python
import pyfixest as pf
import matplotlib.pyplot as plt

# (a) Sun-Abraham via pyfixest::sunab — the modern primary for staggered DID
es = pf.feols("log_wage ~ sunab(first_treat_year, year) | worker_id + year",
              data=df, vcov={"CRV1": "worker_id"})

# (b) Coefficient figure
fig = pf.iplot(es,
               figsize=(7, 4),
               title="Figure 2a. Event-study coefficients (95% CI; ref. e = -1)",
               xlabel="Years relative to treatment",
               ylabel="Coefficient (ATT)")
fig.savefig("figures/fig2a_event_study.pdf", dpi=300)
fig.savefig("figures/fig2a_event_study.png", dpi=300)

# (c) Numerical pre-trends F-test (Wald on the leads jointly = 0)
import numpy as np
pre_idx = [k for k in es.coef().index if "rel_time::-" in k and "ref" not in k]
W = es.wald_test(pre_idx)
print(f"Pre-trends Wald χ² = {W.statistic:.2f}, p = {W.pvalue:.3f}")

# (d) Bacon decomposition (Goodman-Bacon 2021) — TWFE diagnostic
# Pure-Python: callout to R::bacondecomp via rpy2 (Stata/R have first-class support)
# OR use the `bacondecomp` Python port if installed.
try:
    from bacondecomp import bacon
    bd = bacon(df, y="log_wage", D="training", time="year", id_var="worker_id")
    bd.plot(); plt.savefig("figures/fig2a_bacon.pdf", dpi=300)
except ImportError:
    print("bacondecomp not installed; use R callout or Stata's -bacondecomp-.")
```

#### 3.5.2 First-stage F-statistic + scatter (IV identification)

Rule of thumb: first-stage F ≥ 10 for OLS-style inference; F ≥ 23 for AR-equivalent inference (Stock–Yogo / Lee 2022).

```python
from linearmodels.iv import IV2SLS
iv = IV2SLS.from_formula(
    "log_wage ~ 1 + age + edu + [training ~ Z1 + Z2]",
    data=df).fit(cov_type="clustered", clusters=df["firm_id"])
print(iv.first_stage)                            # reports first-stage F
print(iv.summary)

# Binscatter for the first-stage scatter (residualized on age + edu)
from binsreg import binsreg                       # pip install binsreg
res = binsreg(y=df["training"], x=df["Z1"], w=df[["age","edu"]],
              nbins=20, polyreg=2, ci=(3,3))
res.bins_plot.savefig("figures/fig2b_first_stage.pdf", dpi=300)
```

#### 3.5.3 RD: McCrary density + canonical RD plot

The signature RD figure is `rdplot` (CCT-style binned scatter with local-polynomial fit on each side), paired with the McCrary manipulation test.

```python
from rdrobust import rdplot, rdrobust
from rddensity import rddensity, rdplotdensity

# (a) Canonical RD plot — binned means + local poly on each side
rdp = rdplot(y=df["outcome"], x=df["running_var"], c=0,
             p=4, kernel="triangular", binselect="esmv")
plt.savefig("figures/fig2c_rdplot.pdf", dpi=300)

# (b) McCrary density (Cattaneo-Jansson-Ma 2018)
dens = rddensity(X=df["running_var"], c=0)
print(dens)
rdplotdensity(dens, X=df["running_var"])
plt.savefig("figures/fig2c_mccrary.pdf", dpi=300)
```

#### 3.5.4 Matching: love plot (standardized differences pre vs post)

```python
import causalml.matching as cm
from causalml.match import NearestNeighborMatch
import seaborn as sns

# Pre-matching SMDs
pre_smd = ((df.loc[df.training==1, ["age","edu","tenure"]].mean()
            - df.loc[df.training==0, ["age","edu","tenure"]].mean())
           / df[["age","edu","tenure"]].std())

# Match
psm = NearestNeighborMatch(replace=False, ratio=1, random_state=42)
matched = psm.match(data=df, treatment_col="training",
                    score_cols=["age","edu","tenure"])

# Post-matching SMDs
post_smd = ((matched.loc[matched.training==1, ["age","edu","tenure"]].mean()
             - matched.loc[matched.training==0, ["age","edu","tenure"]].mean())
            / matched[["age","edu","tenure"]].std())

love = pd.DataFrame({"pre": pre_smd.abs(), "post": post_smd.abs()})
love.plot.barh(); plt.axvline(0.10, ls="--", c="r")
plt.title("Figure 2d. Love plot — |SMD| pre vs post matching (target < 0.10)")
plt.savefig("figures/fig2d_loveplot.pdf", dpi=300)
```

#### 3.5.5 SCM: synthetic-control trajectory + gap plot

For synthetic-control designs the canonical Figure 2 is the treated-vs-synthetic time series with treatment time annotated.

```python
# Pure Python: pysynth or sparseSC; for SDiD use rpy2 callout to R::synthdid
from SyntheticControlMethods import Synth
sc = Synth(df, "outcome", "unit_id", "time", treatment_period=2015,
           treated_unit=1, n_optim=10)
sc.plot(["original", "pointwise"], treated_label="Treated unit",
        synth_label="Synthetic control")
plt.savefig("figures/fig2e_synth_trajectory.pdf", dpi=300)
```

> Identification-specific checks (PT for DID, weak-IV F, density for RD, common support for matching) **are also auto-run inside the Step-5 estimators** — don't duplicate the numerics here, but DO produce the figures: a referee scans the figures first.

---

### Step 4 — Diagnostic statistical tests

Deeper patterns: [references/04-statistical-tests.md](references/04-statistical-tests.md) — every classical test with its null/alternative/decision rule (Shapiro–Wilk, Kolmogorov–Smirnov, Jarque–Bera, Breusch–Pagan, White, Goldfeld–Quandt, Durbin–Watson, Breusch–Godfrey, Ljung–Box, ADF, KPSS, Phillips–Perron, VIF, condition number, Hausman, Wu–Hausman, Sargan–Hansen).

Run diagnostics **before** taking estimates at face value. The 5 classes below cover 90% of applied work.

```python
import statsmodels.api as sm
from statsmodels.stats.diagnostic import (
    het_breuschpagan, het_white, acorr_breusch_godfrey, acorr_ljungbox,
)
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from scipy import stats as sps

# Fit a baseline OLS to get residuals for diagnostics
X = sm.add_constant(df[["training","age","edu","tenure"]])
y = df["log_wage"]
ols = sm.OLS(y, X, missing="drop").fit()

# 4a. Normality of residuals (informative but NOT required for OLS — CLT handles large N)
jb_stat, jb_p, skew, kurt = jarque_bera(ols.resid)
sw_stat, sw_p = sps.shapiro(ols.resid.sample(min(5000, len(ols.resid))))
print(f"Jarque-Bera p={jb_p:.3f}   Shapiro p={sw_p:.3f}   skew={skew:.2f}  kurt={kurt:.2f}")

# 4b. Heteroskedasticity — Breusch-Pagan + White
bp = het_breuschpagan(ols.resid, ols.model.exog)
wh = het_white        (ols.resid, ols.model.exog)
print(f"Breusch-Pagan p={bp[1]:.3f}   White p={wh[1]:.3f}")
# → if p<0.05, use robust / cluster-robust SEs (you already should)

# 4c. Autocorrelation (time-series / panel) — Durbin-Watson + Breusch-Godfrey + Ljung-Box
dw = durbin_watson(ols.resid)                                # ~2 = no AR(1)
bg = acorr_breusch_godfrey(ols, nlags=4)                     # general AR(p)
lb = acorr_ljungbox(ols.resid, lags=[4,8], return_df=True)
print(f"Durbin-Watson={dw:.2f}   Breusch-Godfrey p={bg[1]:.3f}")
print(lb)

# 4d. Multicollinearity — VIF + condition number
vif = pd.DataFrame({
    "var":  X.columns,
    "VIF":  [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print(vif)                              # VIF > 10 is the classic red flag
cond_number = np.linalg.cond(X.values)  # > 30 = potential collinearity
print(f"Condition number = {cond_number:.1f}")

# 4e. Stationarity (time-series) — ADF + KPSS (dual test: ADF rejects unit root, KPSS accepts stationarity)
from statsmodels.tsa.stattools import adfuller, kpss
adf_stat, adf_p, *_       = adfuller(df["log_wage"].dropna(), autolag="AIC")
kpss_stat, kpss_p, *_     = kpss   (df["log_wage"].dropna(), regression="c", nlags="auto")
print(f"ADF p={adf_p:.3f}   KPSS p={kpss_p:.3f}")
```

**Decision table** (classic rules of thumb):

| Test | Null | Action if rejected |
|------|------|-------------------|
| Jarque–Bera / Shapiro | residuals ~ Normal | usually ignore when N large; bootstrap CIs if small-N inference matters |
| Breusch–Pagan / White | homoskedastic errors | use `cov_type="HC3"` or cluster SEs |
| Durbin–Watson / Breusch–Godfrey | no autocorrelation | use HAC (Newey–West) or cluster by unit |
| VIF > 10 / cond# > 30 | — | drop / combine collinear regressors |
| ADF rejects + KPSS fails to reject | series is stationary | fit levels |
| ADF fails to reject | unit root | first-difference or cointegration test |

---

### Step 5 — Baseline empirical modeling (Section 4: Main Results)

Deeper patterns: [references/05-modeling.md](references/05-modeling.md) — every classical estimator with API: OLS, WLS, GLS, logit/probit, panel FE / RE / PO, clustered SEs, 2SLS / LIML / GMM, DID (2×2, TWFE, event study, CS, SA, BJS, SDiD), RD (sharp, fuzzy, kink, multi-cutoff), Synthetic Control, PSM / IPW / EB, DML / causal forest / DR-Learner.

This is the densest section of an applied paper. A modern AER §4 typically contains **2–3 multi-regression tables and one coefficient plot**:

- **Table 2** (main): progressive controls, 4–6 columns — **Pattern A** below
- **Table 2-bis** (design horse race): same coefficient under OLS / IV / DID / DML — **Pattern B**
- **Table 2-ter** (multi-outcome): same treatment, several outcomes side-by-side — **Pattern C**
- **Figure 3** (coefplot): visual summary of β̂ and 95% CI across specs

> **Estimator routing** (memorize this — getting it wrong silently produces nonsense):
> - **No FE / single low-card FE** → `smf.ols("y ~ X", df).fit(cov_type="cluster", cov_kwds={"groups": df["i"]})`
> - **High-dim FE** → `pf.feols("y ~ X | fe1 + fe2", df, vcov={"CRV1":"i"})`
> - **Two-way cluster** → `pf.feols(..., vcov={"CRV1":"firm_id+year"})`
> - **2SLS / IV** → `IV2SLS.from_formula("y ~ X + [D ~ Z]", df).fit(...)` or `pf.feols("y ~ X | D ~ Z", df)`
> - **DID / event-study** → `pf.feols("y ~ sunab(G, t) | i + t", df)` for SA; R callout to `did::att_gt` for CS

**Pick the estimator by identification strategy** (not by "what's trendy"):

```
Observational cross-section, selection on observables  →  OLS + controls  |  PSM / IPW / DML
Observational panel, policy shock, parallel trends     →  DID (TWFE / CS / SA / BJS / SDiD)
Exogenous instrument for endogenous X                  →  2SLS / LIML / GMM (linearmodels / pyfixest)
Discontinuity in assignment rule                       →  Sharp / Fuzzy / Kink RD (rdrobust)
N=1 treated unit, long panel                           →  Synthetic Control (pysynth / SDiD)
High-dim controls or heterogeneous effects             →  DML / Causal Forest (econml)
Binary outcome                                         →  Logit / Probit (statsmodels)
Count outcome                                          →  Poisson / NegBin (pyfixest / statsmodels)
```

Canonical calls (details in [references/05-modeling.md](references/05-modeling.md)). The eight regression-table patterns A–H below are the AER table cookbook — `pf.etable(*models, ...)` is the workhorse, equivalent to Stata's `outreg2`/`esttab` and R's `modelsummary`.

#### 5.A Pattern A — Progressive controls (the canonical Table 2)
Stable β̂ across columns ⇒ less concern that selection on observables is driving the estimate (Oster 2019 selection-stability logic; quantified in Step 6.f).

```python
import pyfixest as pf

m1 = pf.feols("log_wage ~ training",                                                 data=df, vcov={"CRV1":"firm_id"})
m2 = pf.feols("log_wage ~ training + age + edu",                                     data=df, vcov={"CRV1":"firm_id"})
m3 = pf.feols("log_wage ~ training + age + edu + tenure + firm_size",                data=df, vcov={"CRV1":"firm_id"})
m4 = pf.feols("log_wage ~ training + age + edu + tenure + firm_size | industry + year",
              data=df, vcov={"CRV1":"firm_id"})
m5 = pf.feols("log_wage ~ training + age + edu + tenure + firm_size | worker_id + year",
              data=df, vcov={"CRV1":"firm_id"})
m6 = pf.feols("log_wage ~ training + age + edu + tenure + firm_size | worker_id + year + industry^year",
              data=df, vcov={"CRV1":"firm_id"})

pf.etable([m1, m2, m3, m4, m5, m6],
          type="tex", file="tables/table2_main.tex",
          headers=["(1) Baseline", "(2) +Demog", "(3) +Labor-mkt",
                   "(4) Ind×Yr FE", "(5) Worker FE", "(6) Worker FE+Ind×Yr"],
          digits=3, signif_code=[0.1, 0.05, 0.01],
          notes="Cluster-robust SE in parentheses, clustered at firm_id.")
pf.etable([m1, m2, m3, m4, m5, m6], type="docx", file="tables/table2_main.docx")
```

> **AER convention: show ALL controls (and the intercept).** Pass NEITHER `keep=` NOR `drop=` so every parameter is visible. Use `keep=["training"]` only when a focal-coefficient-only table is intentional (interaction-form heterogeneity, IV first-stage triplet); use `drop=["Intercept"]` only when you want to suppress the constant for paper aesthetics.

#### 5.B Pattern B — Design horse race (Table 2-bis)
Show the same coefficient of interest under multiple identification strategies. This is *the* AER credibility move: convergent evidence across designs each making different identifying assumptions.

```python
from linearmodels.iv import IV2SLS
from econml.dml import LinearDML
from causalml.match import NearestNeighborMatch

ols  = pf.feols("log_wage ~ training + age + edu + tenure | industry + year",
                data=df, vcov={"CRV1":"firm_id"})
iv   = IV2SLS.from_formula("log_wage ~ 1 + age + edu + tenure + [training ~ Z1 + Z2]",
                            data=df).fit(cov_type="clustered", clusters=df["firm_id"])
did  = pf.feols("log_wage ~ sunab(first_treat_year, year) | worker_id + year",
                data=df, vcov={"CRV1":"firm_id"})
dml  = LinearDML().fit(df["log_wage"], df["training"],
                        X=df[["age","edu","tenure","firm_size"]])
psm  = NearestNeighborMatch(replace=False, ratio=1).match(
            df, treatment_col="training", score_cols=["age","edu","tenure"])

# Wrap non-pyfixest models or use Stargazer for a multi-source table:
from stargazer.stargazer import Stargazer
table = Stargazer([ols.fit, iv, dml._final_estimator])
table.title("Table 2-bis. Convergent evidence across designs")
table.custom_columns(["(1) OLS+FE", "(2) 2SLS", "(3) DML"], [1,1,1])
open("tables/table2b_designs.tex", "w").write(table.render_latex())
```

#### 5.C Pattern C — Multi-outcome table (same X, several Y's)

```python
ys = ["log_wage", "weeks_employed", "left_firm", "promoted"]
multi_y = [pf.feols(f"{y} ~ training + age + edu + tenure | industry + year",
                     data=df, vcov={"CRV1":"firm_id"}) for y in ys]
pf.etable(multi_y, type="tex", file="tables/table2c_multi_outcome.tex",
          headers=ys, keep="training",
          notes="Each column is a separate regression on the labelled outcome.")
```

#### 5.D Pattern D — Stacked Panel A / Panel B table
Same model family, two horizons (short-run / long-run) or two samples. Stack vertically with two `pf.etable` calls + LaTeX glue.

```python
panelA = [pf.feols("wage_t1 ~ training + X | industry + year", data=df, vcov={"CRV1":"firm_id"}),
          pf.feols("wage_t1 ~ training + X | worker_id + year", data=df, vcov={"CRV1":"firm_id"})]
panelB = [pf.feols("wage_t5 ~ training + X | industry + year", data=df, vcov={"CRV1":"firm_id"}),
          pf.feols("wage_t5 ~ training + X | worker_id + year", data=df, vcov={"CRV1":"firm_id"})]

# Write Panel A
pf.etable(panelA, type="tex", file="tables/table2d_horizons.tex",
          headers=["(1) Industry FE", "(2) Worker FE"], keep="training",
          custom_row=[("Horizon", "1 year", "1 year")])
# Append Panel B (manually concat via texdoc-style glue, or use a wrapper)
```

#### 5.E Pattern E — IV reporting triplet (first-stage / reduced-form / 2SLS)
The textbook AER IV table presents the **first stage**, the **reduced form**, and the **2SLS** in three columns so the reader can verify Wald-ratio = RF / FS.

```python
fs = pf.feols("training ~ Z + age + edu | industry + year", data=df, vcov={"CRV1":"firm_id"})
rf = pf.feols("log_wage ~ Z + age + edu | industry + year", data=df, vcov={"CRV1":"firm_id"})
iv2 = IV2SLS.from_formula("log_wage ~ 1 + age + edu + [training ~ Z]",
                           data=df).fit(cov_type="clustered", clusters=df["firm_id"])

pf.etable([fs, rf], type="tex", file="tables/table2e_iv_triplet.tex",
          headers=["(1) First stage", "(2) Reduced form"], keep=["Z"],
          notes=("First-stage F = " + f"{fs.fitstat()['F']:.2f}"))
# Append the 2SLS column (linearmodels IV2SLS output) via Stargazer or by hand.
```

> **IV triplet is intentionally focal:** show only Z + endogenous regressor so the reader can eyeball the Wald ratio. Drop `keep=["Z"]` only if a referee asks for the full coefficient list.

#### 5.F Pattern F — Causal-orchestrator main via `did::att_gt` / `synth` / `econml.DML`
For DID / SCM / matching mains, the modern Python estimator returns a self-contained estimate + automatic placebos / pre-trends / overlap diagnostics. Pipe into `pf.etable` via a thin adapter, or use `Stargazer` directly.

```python
# DML with full diagnostics
from econml.dml import CausalForestDML
dml = CausalForestDML(n_estimators=2000, min_samples_leaf=5)
dml.fit(df["log_wage"], df["training"], X=df[["age","edu","tenure","firm_size"]])
ate = dml.ate(df[["age","edu","tenure","firm_size"]])
ci  = dml.ate_interval(df[["age","edu","tenure","firm_size"]])
print(f"DML ATE = {ate:.3f}  (95% CI [{ci[0]:.3f}, {ci[1]:.3f}])")
```

#### 5.G Pattern G — Subgroup `pf.etable` (Table 3, see Step 7)
One column per subgroup. Detailed code in §Step 7 — Heterogeneity.

#### 5.H Pattern H — Robustness master (Table A1, see Step 6)
Stack every robustness specification next to the baseline. Detailed code in §Step 6.f.

---

#### Canonical estimator commands (the underlying primitives)

```python
import statsmodels.formula.api as smf
import pyfixest as pf
from linearmodels.iv import IV2SLS
from rdrobust import rdrobust

# 5a. OLS with cluster-robust SEs (use when no FE or just one FE)
ols = smf.ols("log_wage ~ training + age + edu + tenure", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["firm_id"]})
print(ols.summary())

# 5b. Panel FE (unit + time) — reach for pyfixest first; fastest & mirrors R's fixest
fe = pf.feols("log_wage ~ training + age + edu + tenure | worker_id + year",
              data=df, vcov={"CRV1": "worker_id"})
fe.summary()

# 5c. 2×2 DID
did = smf.ols("log_wage ~ treated * post + age + edu", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["worker_id"]})

# 5d. Event study (dynamic DID, base period = −1)
es = pf.feols("log_wage ~ i(rel_time, ref=-1) | worker_id + year",
              data=df, vcov={"CRV1": "worker_id"})
pf.iplot(es)

# 5e. Staggered DID — Callaway–Sant'Anna (via diff-diff) OR Sun–Abraham (via pyfixest interactions)
#     See references/05-modeling.md §5.4 for the full staggered DID playbook.

# 5f. IV / 2SLS
iv = IV2SLS.from_formula(
    "log_wage ~ 1 + age + edu + [training ~ draft_lottery]", data=df
).fit(cov_type="clustered", clusters=df["firm_id"])
print(iv.first_stage)    # first-stage F > 10 (ideally > 104)
print(iv.summary)

# 5g. Sharp RD
rd = rdrobust(y=df["outcome"], x=df["running_var"], c=0,
              kernel="triangular", bwselect="mserd")
print(rd)

# 5h. Binary outcome
logit = smf.logit("employed ~ training + age + edu", data=df).fit()
print(logit.summary())
print(logit.get_margeff().summary())   # marginal effects — the interpretable quantity
```

---

### Step 6 — Robustness battery

Deeper patterns: [references/06-robustness.md](references/06-robustness.md) — alternative specifications (add/drop controls), subsample splits, alternative clustering levels, alternative outcome definitions, placebo tests (fake treatment / fake timing / permutation), specification curve, Oster δ\*, randomization inference, leave-one-out, winsorization sensitivity.

Every headline result in the paper needs a robustness appendix. The canonical 6:

```python
# 6a. Alternative specifications — progressive controls (M1 → M6)
specs = [
    "log_wage ~ training",                                               # M1 raw
    "log_wage ~ training + age + edu",                                   # M2 +covariates
    "log_wage ~ training + age + edu + tenure",                          # M3 +tenure
    "log_wage ~ training + age + edu + tenure | worker_id",              # M4 +unit FE
    "log_wage ~ training + age + edu + tenure | worker_id + year",       # M5 +time FE
    "log_wage ~ training + age + edu + tenure | worker_id + year + industry^year",  # M6 +industry×year
]
results = [pf.feols(f, data=df, vcov={"CRV1":"worker_id"}) for f in specs]
pf.etable(results)          # side-by-side publication table

# 6b. Alternative cluster levels
for cl in ["worker_id", "firm_id", "industry", "state"]:
    r = pf.feols("log_wage ~ training | worker_id+year", data=df, vcov={"CRV1": cl})
    print(cl, r.coef()["training"], r.se()["training"])

# 6c. Subsample splits
for col in ["male", "has_college", "high_tenure"]:
    for val in [0, 1]:
        sub = df[df[col]==val]
        r = pf.feols("log_wage ~ training | worker_id+year", data=sub)
        print(col, val, r.coef()["training"], r.se()["training"])

# 6d. Placebo — fake timing (treat 3 years before actual policy; should be ~0)
df["fake_post"] = (df["year"] >= df["first_treat_year"] - 3).astype(int)
placebo = pf.feols("log_wage ~ fake_post | worker_id + year", data=df)
placebo.summary()

# 6e. Placebo — permutation / randomization inference (500 draws)
obs_coef = pf.feols("log_wage ~ training | worker_id+year", data=df).coef()["training"]
draws = []
for s in range(500):
    df_s = df.copy()
    df_s["training_perm"] = df_s.groupby("worker_id")["training"].transform(
        lambda x: x.sample(frac=1, random_state=s).values)
    r = pf.feols("log_wage ~ training_perm | worker_id+year", data=df_s)
    draws.append(r.coef()["training_perm"])
p_perm = (np.abs(draws) >= abs(obs_coef)).mean()
print(f"Permutation p = {p_perm:.3f}")

# 6f. Oster (2019) δ* — selection on unobservables
# See references/06-robustness.md §6.6 for the exact formula and its implementation.

# ============================================================
# 6.g Pattern H — Robustness master table (Table A1, one column per check)
# ============================================================
import pyfixest as pf

base    = pf.feols("log_wage ~ training + age + edu + tenure | industry + year",
                    data=df, vcov={"CRV1":"firm_id"})
no99    = pf.feols("log_wage ~ training + age + edu + tenure | industry + year",
                    data=df.query("wage < wage.quantile(0.99)"), vcov={"CRV1":"firm_id"})
balpan  = pf.feols("log_wage ~ training + age + edu + tenure | industry + year",
                    data=df.groupby("worker_id").filter(lambda g: len(g) == g["year"].nunique()),
                    vcov={"CRV1":"firm_id"})
dropearly = pf.feols("log_wage ~ training + age + edu + tenure | industry + year",
                      data=df.query("first_treat_year > 2008"), vcov={"CRV1":"firm_id"})
wfe     = pf.feols("log_wage ~ training + age + edu + tenure | worker_id + year",
                    data=df, vcov={"CRV1":"firm_id"})
cl2way  = pf.feols("log_wage ~ training + age + edu + tenure | industry + year",
                    data=df, vcov={"CRV1":"firm_id+year"})
logy    = pf.feols("np.log1p(wage) ~ training + age + edu + tenure | industry + year",
                    data=df, vcov={"CRV1":"firm_id"})
ihsy    = pf.feols("np.arcsinh(wage) ~ training + age + edu + tenure | industry + year",
                    data=df, vcov={"CRV1":"firm_id"})

pf.etable([base, no99, balpan, dropearly, wfe, cl2way, logy, ihsy],
          type="tex", file="tables/tableA1_robustness.tex",
          headers=["(1) Baseline", "(2) Drop top 1%", "(3) Balanced",
                   "(4) Drop early", "(5) Worker FE", "(6) 2-way cluster",
                   "(7) log Y", "(8) IHS Y"],
          keep="training",
          notes="Each column is one robustness check. β̂ on training is the focal coefficient.")

# ============================================================
# 6.h Specification curve (Simonsohn-Simmons-Nelson 2020)
# ============================================================
import itertools, numpy as np
specs = []
for ctrls in [["age"], ["age","edu"], ["age","edu","tenure"], ["age","edu","tenure","firm_size"]]:
    for trans in ["log_wage", "ihs_wage"]:
        for mask_label, mask in [("all", slice(None)),
                                  ("manuf", df["industry"]=="manuf"),
                                  ("no99", df["wage"] < df["wage"].quantile(0.99))]:
            for cl in ["firm_id", "firm_id+year"]:
                d = df.loc[mask] if not isinstance(mask, slice) else df
                fit = pf.feols(f"{trans} ~ training + {' + '.join(ctrls)} | industry + year",
                                data=d, vcov={"CRV1": cl})
                b  = fit.coef()["training"]
                se = fit.se()["training"]
                specs.append({
                    "label": f"c={'+'.join(ctrls)}/y={trans}/s={mask_label}/cl={cl}",
                    "b": b, "lo": b - 1.96*se, "hi": b + 1.96*se})

specs_df = pd.DataFrame(specs).sort_values("b").reset_index(drop=True)
fig, ax = plt.subplots(figsize=(10, 5))
ax.errorbar(specs_df.index, specs_df["b"],
            yerr=[specs_df["b"]-specs_df["lo"], specs_df["hi"]-specs_df["b"]],
            fmt="o", capsize=2, ms=3)
ax.axhline(0, ls="--", c="gray")
ax.set_xlabel("Specification (sorted by β̂)")
ax.set_ylabel("Coefficient on training")
ax.set_title("Figure 5. Specification curve")
plt.tight_layout()
plt.savefig("figures/fig5_spec_curve.pdf", dpi=300)
plt.savefig("figures/fig5_spec_curve.png", dpi=300)

# ============================================================
# 6.i Sensitivity dashboard — HonestDiD + Oster + E-value
# ============================================================
# (a) HonestDiD — Rambachan-Roth (2023): Python via R callout (rpy2) or HonestDiD-py if installed.
# (b) Oster δ — see references/06-robustness.md §6.6 for the formula implementation.
# (c) E-value (VanderWeele-Ding 2017) — for risk-ratio outcomes; convert OLS to RR scale first.
def evalue(rr_point, rr_lower):
    """Min strength of unmeasured confounding to nullify; (point, ci_lower)."""
    e_point = rr_point + np.sqrt(rr_point * (rr_point - 1))
    e_ci    = rr_lower + np.sqrt(rr_lower * (rr_lower - 1)) if rr_lower > 1 else 1.0
    return e_point, e_ci
print("E-value (point, CI):", evalue(1.45, 1.10))
```

---

### Step 7 — Further analysis (mechanism / heterogeneity / mediation / moderation)

Deeper patterns: [references/07-further-analysis.md](references/07-further-analysis.md) — subgroup + Wald interaction test, triple-difference (DDD) for effect heterogeneity, Baron–Kenny / Imai mediation, causal mediation with sensitivity, moderated mediation, outcome ladder (short → intermediate → final), dose-response curves, CATE via causal forest.

```python
# 7a. Heterogeneity via full interaction (cleanest: lets you test the interaction coefficient)
het = pf.feols("log_wage ~ training + training:female + age + edu | worker_id + year",
               data=df, vcov={"CRV1": "worker_id"})
het.summary()     # the interaction coefficient IS the heterogeneity test

# 7b. Subgroup estimation with Wald test of equality
from scipy.stats import chi2
male_r   = pf.feols("log_wage ~ training | worker_id+year", data=df[df.female==0])
female_r = pf.feols("log_wage ~ training | worker_id+year", data=df[df.female==1])
diff  = male_r.coef()["training"] - female_r.coef()["training"]
se    = np.sqrt(male_r.se()["training"]**2 + female_r.se()["training"]**2)
wald  = (diff/se)**2
print(f"Wald = {wald:.2f},  p = {1-chi2.cdf(wald,1):.3f}")

# 7c. Triple-difference (DDD) — heterogeneity by a THIRD dimension
ddd = pf.feols(
    "log_wage ~ treated*post*high_exposure | worker_id + year",
    data=df, vcov={"CRV1":"firm_id"})

# 7d. Mechanism — "outcome ladder" (same treatment, three sequential outcomes)
for out in ["hours_worked", "productivity", "log_wage"]:
    r = pf.feols(f"{out} ~ training | worker_id + year", data=df)
    print(out, r.coef()["training"], r.se()["training"])

# 7e. Mediation — Baron-Kenny (ok for simple linear setting; use Imai for rigor)
#     Total:     Y = a + c·T + ε
#     Step 1:    M = a1 + b·T + ε      (does T affect M?)
#     Step 2:    Y = a2 + c'·T + d·M + ε   (direct effect of T holding M fixed)
#     Mediated effect = b · d
b_coef = smf.ols("hours_worked ~ training + age+edu", data=df).fit().params["training"]
d_coef = smf.ols("log_wage    ~ training + hours_worked + age+edu", data=df) \
             .fit().params["hours_worked"]
print(f"Indirect effect via hours = {b_coef*d_coef:.3f}")

# 7f. Moderation — add interaction + marginal-effect plot; see references/07 for the full recipe.

# 7g. Heterogeneous treatment effects via causal forest (high-dim moderators)
from econml.dml import CausalForestDML
cf = CausalForestDML(n_estimators=1000, min_samples_leaf=5)
cf.fit(df["log_wage"], df["training"], X=df[["age","edu","tenure","firm_size"]])
tau = cf.effect(df[["age","edu","tenure","firm_size"]])      # per-unit CATE
cf.feature_importances_    # which X drives heterogeneity
```

---

### Step 8 — Publication tables & figures

> **This step is mandatory** — every analysis run produces all 5 required tables (T1–T5) and all 4 required figures (F1–F4) defined in the *Default Output Spec* at the top of this skill. Do not skip Step 8 because "the regression already ran". A coefficient without a table and a figure is not how applied economics communicates a result.

Deeper patterns: [references/08-tables-plots.md](references/08-tables-plots.md) — `stargazer` and `pf.etable()` for regression tables; coefficient plots with CIs; event-study plots (pre/post coefficients with reference line); binscatter; forest plots for subgroup analysis; RD plots; LaTeX / Word / Excel export.

```python
# ============================================================
# 8a. ★ TABLE 2 — Main results, multi-column regression M1→M6
#     (the centerpiece of every economics paper)
# ============================================================
from stargazer.stargazer import Stargazer
table = Stargazer([r.fit for r in [ols_m1, ols_m2, ols_m3, ols_m4, ols_m5, ols_m6]])
table.title("Effect of training on log wage")
table.custom_columns(["(1)","(2)","(3)","(4)","(5)","(6)"], [1]*6)
open("tables/table2_main.tex","w").write(table.render_latex())

# Or pyfixest's etable — handles FE indicators automatically (preferred):
pf.etable([m1, m2, m3, m4, m5, m6],
          type="tex",   file="tables/table2_main.tex",
          headers=["(1) Raw","(2) +Demog","(3) +Tenure",
                   "(4) +Unit FE","(5) +2-way FE","(6) +Ind×Year FE"],
          digits=3, signif_code=[0.1, 0.05, 0.01],
          notes="Cluster-robust SE in parentheses, clustered at worker_id.")
pf.etable([m1, m2, m3, m4, m5, m6], type="docx", file="tables/table2_main.docx")

# ============================================================
# 8b. TABLE 1 — Summary statistics & balance
# ============================================================
# Built in Step 3 as `t1` (DataFrame). Export both formats:
t1.to_latex("tables/table1_balance.tex", float_format="%.3f", index=False)
t1.to_excel("tables/table1_balance.xlsx", index=False)
# .docx version via python-docx or pandas → docx through tabulate

# ============================================================
# 8c. TABLE 3 — Mechanism / outcome ladder (3+ outcomes)
# ============================================================
ladder = [pf.feols(f"{y} ~ training + age + edu + tenure | worker_id + year",
                   data=df, vcov={"CRV1":"worker_id"})
          for y in ["hours_worked", "productivity", "log_wage"]]
pf.etable(ladder, type="tex", file="tables/table3_mechanism.tex",
          headers=["Hours worked", "Productivity", "Log wage"],
          notes="Each column is a separate regression on the labelled outcome.")

# ============================================================
# 8d. TABLE 4 — Heterogeneity (subgroup × main coef)
# ============================================================
het_specs = {
    "All":           df,
    "Female=0":      df[df.female==0],
    "Female=1":      df[df.female==1],
    "Age<40":        df[df.age<40],
    "Age>=40":       df[df.age>=40],
    "Manufacturing": df[df.industry.eq("manufacturing")],
}
het_models = [pf.feols("log_wage ~ training + age + edu + tenure | worker_id + year",
                       data=d, vcov={"CRV1":"worker_id"})
              for d in het_specs.values()]
pf.etable(het_models, type="tex", file="tables/table4_heterogeneity.tex",
          headers=list(het_specs.keys()),
          notes="Cluster-robust SE at worker_id. Wald p-values for cross-subgroup equality "
                "should accompany this table — see references/07.")

# ============================================================
# 8e. TABLE 5 — Robustness battery (alt SE / cluster / sample / placebo)
# ============================================================
rob = {
    "Baseline":      pf.feols("log_wage ~ training | worker_id + year", df,
                              vcov={"CRV1":"worker_id"}),
    "Cluster=firm":  pf.feols("log_wage ~ training | worker_id + year", df,
                              vcov={"CRV1":"firm_id"}),
    "Two-way clust": pf.feols("log_wage ~ training | worker_id + year", df,
                              vcov={"CRV3x1":["worker_id","firm_id"]}),
    "Winsor 1/99":   pf.feols("log_wage ~ training | worker_id + year",
                              df.assign(log_wage=df.log_wage.clip(*df.log_wage.quantile([.01,.99]))),
                              vcov={"CRV1":"worker_id"}),
    "Drop manuf":    pf.feols("log_wage ~ training | worker_id + year",
                              df[df.industry!="manufacturing"], vcov={"CRV1":"worker_id"}),
    "Placebo (-3)":  pf.feols("log_wage ~ fake_post | worker_id + year",
                              df, vcov={"CRV1":"worker_id"}),
}
pf.etable(list(rob.values()), type="tex", file="tables/table5_robustness.tex",
          headers=list(rob.keys()))

# ============================================================
# 8f. ★ FIGURE 3 — Coefficient plot across M1→M6
# ============================================================
fig, ax = plt.subplots(figsize=(6, 3.5))
labels, betas, lows, highs = [], [], [], []
for name, r in [("(1)",m1),("(2)",m2),("(3)",m3),("(4)",m4),("(5)",m5),("(6)",m6)]:
    b  = r.coef()["training"]; se = r.se()["training"]
    labels.append(name); betas.append(b)
    lows.append(b-1.96*se); highs.append(b+1.96*se)
betas = np.array(betas); lows = np.array(lows); highs = np.array(highs)
ax.errorbar(labels, betas, yerr=[betas-lows, highs-betas], fmt="o", capsize=3, color="navy")
ax.axhline(0, ls="--", color="gray", alpha=.6)
ax.set_ylabel("ATT on log wage"); ax.set_xlabel("Specification")
plt.tight_layout()
plt.savefig("figures/fig3_coefplot.pdf"); plt.savefig("figures/fig3_coefplot.png", dpi=300)

# ============================================================
# 8g. FIGURE 2 — Event-study plot (dynamic DID, base period = -1)
# ============================================================
fig, ax = plt.subplots(figsize=(7, 4))
pf.iplot(es, ax=ax)
ax.axhline(0, ls="--", color="gray"); ax.axvline(-0.5, ls=":", color="gray")
ax.set_xlabel("Years relative to treatment"); ax.set_ylabel("Coefficient (ATT)")
plt.tight_layout()
plt.savefig("figures/fig2_event_study.pdf"); plt.savefig("figures/fig2_event_study.png", dpi=300)

# ============================================================
# 8h. FIGURE 4 — Sensitivity / robustness curve (spec curve)
# ============================================================
# Loop over 32 spec combinations and rank by point estimate
specs_curve = []
for fe in ["", "| worker_id", "| worker_id + year", "| worker_id + year + industry^year"]:
    for ctrl in [[], ["age"], ["age","edu"], ["age","edu","tenure"]]:
        f = "log_wage ~ training" + ("+" + "+".join(ctrl) if ctrl else "") + " " + fe
        try:
            r = pf.feols(f, df, vcov={"CRV1":"worker_id"})
            specs_curve.append({"spec": f.strip(), "b": r.coef()["training"],
                                "se": r.se()["training"]})
        except Exception:
            pass
sc = pd.DataFrame(specs_curve).sort_values("b").reset_index(drop=True)
fig, ax = plt.subplots(figsize=(7, 4))
ax.errorbar(range(len(sc)), sc["b"], yerr=1.96*sc["se"], fmt="o", ms=3, color="navy", alpha=.7)
ax.axhline(0, ls="--", color="gray")
ax.set_xlabel("Specification rank (sorted by point estimate)")
ax.set_ylabel("Coefficient on training")
plt.tight_layout()
plt.savefig("figures/fig4_sensitivity.pdf"); plt.savefig("figures/fig4_sensitivity.png", dpi=300)

# ============================================================
# 8i. FIGURE 1 — Trend / motivation (treated vs control over time)
# ============================================================
# Already built in Step 3; re-export with paper-grade styling.
fig, ax = plt.subplots(figsize=(7, 4))
trend = df.groupby(["year","training"])["log_wage"].mean().unstack()
trend.plot(ax=ax, marker="o", color={0:"darkred", 1:"navy"})
ax.axvline(policy_year, ls="--", color="gray", label="Policy")
ax.set_ylabel("Mean log wage"); ax.set_xlabel("Year")
ax.legend(["Control","Treated","Policy"])
plt.tight_layout()
plt.savefig("figures/fig1_trend.pdf"); plt.savefig("figures/fig1_trend.png", dpi=300)

# ============================================================
# 8j. Auxiliary plots (optional — produce when relevant)
# ============================================================
from binsreg import binsreg                                  # binscatter
binsreg(y=df["log_wage"], x=df["tenure"], w=df[["age","edu"]], nbins=20)
plt.savefig("figures/figA_binscatter.pdf")

from rdrobust import rdplot                                  # RD plot (only when running_var exists)
# rdplot(y=df["outcome"], x=df["running_var"], c=0); plt.savefig("figures/figA_rdplot.pdf")

# Forest plot for subgroups → see references/08-tables-plots.md §8.6 for the full recipe.
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
[ ] artifacts/result.json (reproducibility stamp — see 8l)
```

#### 8l. Reproducibility stamp

The single artifact a journal's replication office (or a future co-author) needs to reproduce the headline number. Persist Python version, seed, dataset hash, baseline coefficient + CI, and pointers to the protocol/contract:

```python
import json, sys, hashlib, pyfixest

# Get baseline result (assumes `base` is the headline pf.feols/sm.OLS object)
b_hat = float(base.coef()["training"])
se    = float(base.se()["training"])
lo, hi = b_hat - 1.96*se, b_hat + 1.96*se

dataset_sha = hashlib.sha256(
    pd.util.hash_pandas_object(df, index=True).values.tobytes()
).hexdigest()[:16]

stamp = {
    "python_version":    sys.version,
    "pyfixest_version":   pyfixest.__version__,
    "seed":               42,
    "dataset_sha256_16":  dataset_sha,
    "n_obs":              int(base._N),
    "estimand":           "ATT",
    "estimator":          "pf.feols",
    "estimate":           b_hat,
    "se_cluster":         se,
    "ci95":               [lo, hi],
    "pre_registration":   "artifacts/strategy.md",
    "data_contract":      "artifacts/data_contract.json",
    "sample_log":         "artifacts/sample_construction.json",
    "paper_bundle":       "tables/table2_main.tex",
}
with open("artifacts/result.json", "w") as f:
    json.dump(stamp, f, indent=2)
```

Commit `artifacts/result.json` alongside the paper PDF. A referee should be able to run `python master.py` and bit-identically reproduce this JSON.

---

## §A — Epidemiology / Public Health Mode

When the user's wording flags Mode A (target-trial emulation / IPTW / TMLE / MR / STROBE / 流行病学 / 公共健康 / RWE / cohort), the 8 steps still apply — but Step 5 swaps the OLS-and-FE stack for the doubly-robust + survival + MR triplet, and the deliverables follow STROBE / TRIPOD-AI conventions. **Steps 1–4 (cleaning, construction, Table 1, diagnostics) and Step 8 (tables/figures export) are identical to the Default mode.**

**Library footprint** (install on top of the Default stack):

```bash
pip install zepid                # IPTW, g-formula, TMLE, AIPW, E-value
pip install lifelines            # KM, Cox, AFT, RMST
pip install scikit-survival      # alternative survival stack (scaling-friendly)
# Mendelian randomization — Python coverage is thin; for IVW/Egger/weighted-median:
pip install pymr                 # if available
# Or call R from Python:
pip install rpy2                 # then import TwoSampleMR / MendelianRandomization via rpy2
```

### A.0 Cohort construction + target-trial protocol

Write the protocol **before** touching the data. Save it as `protocol.yml` and quote it in the paper.

```python
# protocol.yml — target-trial emulation skeleton
target_trial = {
    "eligibility":    {"age": "40-75", "no_prior_event": True, "ascertained_at": "t0"},
    "treatment":      {"A=1": "statin initiation", "A=0": "no initiation"},
    "assignment":     "random at t0 (emulated by IPTW on baseline covariates)",
    "follow_up_start":"t0 (treatment initiation date)",
    "outcome":        "incident MI within 5 years",
    "estimand":       "intention-to-treat ATE on risk difference + hazard ratio",
    "censoring":      {"loss_to_FU": True, "competing_risk": "death from non-MI causes"},
}
```

```python
# Cohort construction in pandas — eligibility + index date + censoring date
cohort = (df
    .query("age >= 40 & age <= 75 & prior_MI == 0")            # eligibility
    .assign(t0 = lambda d: d["statin_initiation_date"].fillna(d["enrollment_date"]),
            event_5y = lambda d: ((d["MI_date"] - d["t0"]).dt.days <= 365*5).astype(int),
            time_at_risk = lambda d: ((d["censor_date"] - d["t0"]).dt.days.clip(0, 365*5))))
```

### A.1 Table 1 by exposure (identical to Default Step 3)

Use the same `tableone` / `gtsummary`-style call from Step 3, just `groupby="A"` (treatment indicator). E-values for unmeasured confounding go in the footer.

### A.2 DAG + propensity-score overlap (positivity check)

```python
# Estimate PS, plot overlap (positivity), love-plot SMDs
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

X = df[["age", "edu", "smoke", "bmi", "ldl", "sbp"]]
y = df["A"]
ps = LogisticRegression(max_iter=1000).fit(StandardScaler().fit_transform(X), y).predict_proba(StandardScaler().fit_transform(X))[:, 1]
df["ps"] = ps

# Overlap plot
import matplotlib.pyplot as plt, seaborn as sns
sns.kdeplot(data=df, x="ps", hue="A", common_norm=False)
plt.savefig("figures/figA2_ps_overlap.pdf")

# Love plot (SMDs before vs after IPTW) — see zepid.causal.ipw.diagnostics
```

### A.3 IPTW + g-formula + TMLE doubly-robust triplet (Step 5 swap)

The "AER Table 2" of epi: a 3-column table where each column is one of {IPTW-MSM, g-formula, TMLE} so the reader can confirm doubly-robust agreement.

```python
import zepid as ze
from zepid.causal.ipw import IPTW
from zepid.causal.gformula import TimeFixedGFormula
from zepid.causal.doublyrobust import TMLE

# IPTW (marginal structural model)
iptw = IPTW(df, treatment="A", outcome="event_5y")
iptw.treatment_model("age + edu + smoke + bmi + ldl + sbp", print_results=False)
iptw.outcome_model("A", print_results=False)
iptw.fit()
RD_iptw, CI_iptw = iptw.risk_difference, iptw.risk_difference_ci

# g-formula (parametric)
gf = TimeFixedGFormula(df, exposure="A", outcome="event_5y")
gf.outcome_model("A + age + edu + smoke + bmi + ldl + sbp")
gf.fit(treatment="all")  ; r1 = gf.marginal_outcome
gf.fit(treatment="none") ; r0 = gf.marginal_outcome
RD_gf = r1 - r0

# TMLE (doubly robust)
tmle = TMLE(df, exposure="A", outcome="event_5y")
tmle.exposure_model("age + edu + smoke + bmi + ldl + sbp")
tmle.outcome_model("A + age + edu + smoke + bmi + ldl + sbp")
tmle.fit()
RD_tmle, CI_tmle = tmle.risk_difference, tmle.risk_difference_ci

# Stack the triplet into one paper table
import pandas as pd
tableA3 = pd.DataFrame({
    "Estimator": ["IPTW-MSM", "g-formula", "TMLE"],
    "RD":        [RD_iptw, RD_gf, RD_tmle],
    "95% CI":    [CI_iptw, "—", CI_tmle],
})
tableA3.to_latex("tables/tableA3_dr_triplet.tex", index=False, float_format="%.3f")
```

### A.4 Survival outcomes — KM / Cox / AFT / RMST

```python
from lifelines import KaplanMeierFitter, CoxPHFitter, WeibullAFTFitter
from lifelines.utils import restricted_mean_survival_time

# KM by treatment
fig, ax = plt.subplots()
for a, sub in df.groupby("A"):
    KaplanMeierFitter().fit(sub["time_at_risk"], sub["event_5y"], label=f"A={a}").plot_survival_function(ax=ax)
plt.savefig("figures/figA4_km.pdf")

# Cox HR (covariate-adjusted)
cox = CoxPHFitter().fit(df[["time_at_risk","event_5y","A","age","edu","smoke","bmi","ldl","sbp"]],
                        duration_col="time_at_risk", event_col="event_5y")
HR = cox.hazard_ratios_["A"]; HR_CI = cox.confidence_intervals_.loc["A"].values

# AFT (Weibull) for time-ratio interpretation
aft = WeibullAFTFitter().fit(df[["time_at_risk","event_5y","A","age","edu","smoke","bmi","ldl","sbp"]],
                             duration_col="time_at_risk", event_col="event_5y")

# RMST contrast at t=5y
rmst1 = restricted_mean_survival_time(df.query("A==1")["time_at_risk"], df.query("A==1")["event_5y"], t=5*365)
rmst0 = restricted_mean_survival_time(df.query("A==0")["time_at_risk"], df.query("A==0")["event_5y"], t=5*365)
```

### A.5 Mendelian randomization (IVW / Egger / weighted-median triplet)

Two-sample MR is most ergonomic via R; from Python use `rpy2` or pre-export betas/SEs and call `TwoSampleMR` / `MendelianRandomization` in a sister R script.

```python
# Pure-Python: pymr (or write the IVW/Egger formulas by hand — they're closed-form)
# Cross-language: rpy2 is the de-facto path for IVW/Egger/weighted median.
import rpy2.robjects as ro
ro.r('''
library(MendelianRandomization)
mr_input <- mr_input(bx=BX, bxse=BXSE, by=BY, byse=BYSE)
ivw    <- mr_ivw(mr_input)
egger  <- mr_egger(mr_input)
median <- mr_median(mr_input, weighting="weighted")
''')
# Stack the triplet (IVW, Egger, weighted-median) in one tableA5.
```

### A.6 Robustness — E-value / bounds / principal stratification

```python
# E-value from zepid (Linden & VanderWeele formula)
from zepid.sensitivity_analysis import e_value
ev = e_value(measure="RR", est=1.45, lcl=1.10, ucl=1.91)   # → required strength of unmeasured confounding
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

When the user's wording flags Mode B (DML / meta-learner / causal forest / Dragonnet / BCF / CATE / policy learning / conformal causal / fairness / 因果机器学习), the pipeline keeps Steps 1–4 and Step 8 from the Default mode, swaps Step 5 for the ML estimator stack, and adds a CATE-distribution + policy-value layer between Step 7 and Step 8.

**Library footprint** (install on top of the Default stack):

```bash
pip install econml doubleml causalml dowhy             # core estimators
pip install causal-learn cdt                          # causal discovery (PC / NOTEARS / GES)
pip install mapie                                      # conformal prediction (incl. causal)
pip install fairlearn                                  # fairness audit
pip install policytree-py                              # discrete policy learning (optional; also via econml.policy)
```

### B.0 Train/holdout split + nuisance learner stack

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

train, holdout = train_test_split(df, test_size=0.3, random_state=42, stratify=df["A"])

# Standard nuisance pair: outcome regression Q(X,A) and propensity score g(A|X)
Q_learner = GradientBoostingRegressor(n_estimators=300, max_depth=3)
g_learner = GradientBoostingClassifier(n_estimators=300, max_depth=3)
```

### B.1 DAG / estimand declaration (optionally LLM-assisted)

```python
# Causal discovery on observational data — start with PC algorithm
from causallearn.search.ConstraintBased.PC import pc
cg = pc(df[["A","Y","X1","X2","X3","X4"]].to_numpy())
cg.draw_pydot_graph(labels=["A","Y","X1","X2","X3","X4"])

# OR: NOTEARS for a fully differentiable DAG learner
# from cdt.causality.graph import NOTEARS
# notears = NOTEARS().predict(df[["A","Y","X1","X2","X3","X4"]])

# Always sanity-check the recovered DAG against domain knowledge before reading off the adjustment set.
```

### B.2 Estimator stack — DML · meta-learners · causal forest · neural · BCF (Step 5 swap)

The "AER Table 2" of ML causal: a horse-race table where each column is one estimator family on the same `(Y, A, X)` data — readers want to see DML, T-learner, X-learner, causal forest, and Dragonnet all agree (or disagree) on the ATE.

```python
from econml.dml             import LinearDML, NonParamDML
from econml.metalearners    import SLearner, TLearner, XLearner, DomainAdaptationLearner
from econml.dr              import DRLearner
from econml.grf             import CausalForest
from causalml.inference.tf  import DragonNet
# from bcf_py import BayesianCausalForest  # if BCF needed

X_train, A_train, Y_train = train[["X1","X2","X3","X4"]], train["A"], train["Y"]
X_hold,  A_hold,  Y_hold  = holdout[["X1","X2","X3","X4"]], holdout["A"], holdout["Y"]

# DML — semi-parametric, doubly robust to nuisance ML
dml = LinearDML(model_y=Q_learner, model_t=g_learner, discrete_treatment=True, cv=5).fit(Y_train, A_train, X=X_train, W=X_train)
ate_dml = dml.ate(X_hold); ci_dml = dml.ate_interval(X_hold, alpha=0.05)

# Meta-learners — drop the same Q/g into S/T/X
sl = SLearner(overall_model=Q_learner).fit(Y_train, A_train, X=X_train); ate_S = sl.ate(X_hold)
tl = TLearner(models=Q_learner).fit(Y_train, A_train, X=X_train); ate_T = tl.ate(X_hold)
xl = XLearner(models=Q_learner, propensity_model=g_learner).fit(Y_train, A_train, X=X_train); ate_X = xl.ate(X_hold)

# DR-Learner — orthogonal CATE
dr = DRLearner(model_propensity=g_learner, model_regression=Q_learner, model_final=GradientBoostingRegressor()).fit(Y_train, A_train, X=X_train)
ate_DR = dr.ate(X_hold)

# Causal forest — non-parametric CATE
cf = CausalForest(n_estimators=500).fit(X=X_train, T=A_train, y=Y_train); cate_cf = cf.predict(X_hold)
ate_cf = cate_cf.mean()

# Dragonnet — joint propensity + outcome neural net
dn = DragonNet(); dn.fit(X_train.values, A_train.values, Y_train.values); ate_dn = dn.predict(X_hold.values).mean()

# Stack the horse-race
import pandas as pd
tableB2 = pd.DataFrame({
    "Estimator": ["DML (linear)", "S-learner", "T-learner", "X-learner", "DR-learner", "Causal Forest", "Dragonnet"],
    "ATE":       [ate_dml, ate_S, ate_T, ate_X, ate_DR, ate_cf, ate_dn],
})
tableB2.to_latex("tables/tableB2_ml_horserace.tex", index=False, float_format="%.4f")
```

### B.3 CATE distribution + subgroup CATE plot (Step 7 extension)

```python
# CATE histogram and quantile plot — heterogeneity from causal forest
import numpy as np
cate = cf.predict(X_hold)
plt.figure(); plt.hist(cate, bins=30); plt.axvline(0, ls="--", color="k"); plt.xlabel("CATE")
plt.savefig("figures/figB3_cate_hist.pdf")

# CATE by quartile of a covariate
df_h = X_hold.assign(cate=cate, age_q=pd.qcut(X_hold["X1"], 4, labels=False))
df_h.groupby("age_q")["cate"].mean().plot(kind="bar"); plt.ylabel("Mean CATE")
plt.savefig("figures/figB3_cate_by_age_q.pdf")
```

### B.4 Policy learning + off-policy evaluation

```python
from econml.policy import DRPolicyTree            # honest discrete policy tree

policy = DRPolicyTree(max_depth=3).fit(Y_train, A_train, X=X_train)
policy.plot()   # prose-readable tree of "treat if X1<a and X2>b"
plt.savefig("figures/figB4_policy_tree.pdf")

# Off-policy evaluation (DR-style policy-value)
pred_policy = policy.predict(X_hold)
policy_value_DR = ((Y_hold * (pred_policy == A_hold).astype(int)).mean()
                   - (Y_hold * (pred_policy != A_hold).astype(int)).mean())
print(f"DR policy value (holdout): {policy_value_DR:.3f}")
```

### B.5 Uncertainty (conformal causal) + fairness + sensitivity

```python
from mapie.regression import MapieRegressor

# Conformal prediction interval around CATE — distribution-free coverage guarantee
mapie = MapieRegressor(estimator=GradientBoostingRegressor(), method="plus", cv=10).fit(X_train, cf.predict(X_train))
y_pred, y_pis = mapie.predict(X_hold, alpha=0.1)   # 90% conformal PI

# Fairness audit — disparate-impact / equalized-odds for the learned policy
from fairlearn.metrics import MetricFrame, demographic_parity_difference, equalized_odds_difference
sens = X_hold["sensitive_attr"]              # e.g. female
mf = MetricFrame(metrics={"acc": (lambda y,y_hat: (y == y_hat).mean())},
                 y_true=A_hold, y_pred=policy.predict(X_hold), sensitive_features=sens)
print("Demographic parity diff:", demographic_parity_difference(A_hold, policy.predict(X_hold), sensitive_features=sens))
```

### B.6 ML-causal-specific reporting checklist

Save as `replication/ml_causal_checklist.md`:

```
[ ] Nuisance learners listed (Q model, g model, hyperparameters, CV folds)
[ ] Cross-fitting / sample-splitting documented (DML K-fold)
[ ] Overlap / propensity diagnostics (B.0 + A.2-style overlap plot)
[ ] CATE summary (mean, SD, quartiles) + heterogeneity p-value
[ ] Policy value with confidence interval (B.4)
[ ] Conformal coverage rate on holdout (B.5)
[ ] Fairness gaps across sensitive attributes (B.5)
[ ] DAG / adjustment set + sensitivity to unmeasured confounding (E-value or Manski bounds)
```

---

## Library selection cheat-sheet

| Step | Task | Go-to library | Fallback |
|------|------|---------------|----------|
| 1 | Data cleaning | `pandas` | `polars` for >10M rows |
| 1 | Missing-data viz | `missingno` | manual heatmap |
| 2 | Transformations | `numpy`, `pandas`, `scipy.stats.mstats.winsorize` | `sklearn.preprocessing` |
| 3 | Summary stats + Table 1 | `pandas`, `scipy.stats` | `tableone` |
| 3 | Plots | `matplotlib`, `seaborn` | `plotly` for interactive |
| 4 | Normality / hetero / autocorr | `statsmodels.stats.*`, `scipy.stats` | `pingouin` |
| 4 | Stationarity | `statsmodels.tsa.stattools`, `arch` | — |
| 5 | OLS / panel FE | `pyfixest` | `statsmodels`, `linearmodels` |
| 5 | IV | `linearmodels` | `pyfixest` (panel IV) |
| 5 | DID (2×2, event study, TWFE) | `pyfixest` (+ `diff-diff` for CS/SA/BJS/SDiD) | `statsmodels` with interactions |
| 5 | RD | `rdrobust`, `rddensity` | — |
| 5 | Synthetic Control | `pysynth`, `sdid` | manual `scipy.optimize` |
| 5 | Matching / IPW / EB | `causalml`, `econml`, `ebal` | `pymatch` |
| 5 | DML / Causal Forest | `econml` | `doubleml` |
| 6 | Specification curve | custom loop over formulas | `specurve` |
| 7 | Mediation | `pingouin.mediation_analysis` | manual Baron–Kenny |
| 7 | CATE | `econml` causal forest | — |
| 8 | Regression tables | `stargazer`, `pyfixest.etable` | `summary_col` (statsmodels) |
| 8 | Coefplot / event study | `pyfixest.iplot`, `matplotlib.errorbar` | `forestplot` |
| 8 | Binscatter | `binsreg` | manual quantile cut |

---

## Common mistakes (and what to do instead)

| Mistake | Correct approach |
|---------|------------------|
| Running OLS on panel data without any FE | Use `pyfixest.feols(... \| unit + time, ...)` |
| Default (iid) SEs on clustered / panel / few-cluster data | `vcov={"CRV1":"cluster_var"}`; wild bootstrap if clusters < 50 |
| TWFE with staggered adoption | Use CS / SA / BJS to avoid negative-weight bias |
| Dropping rows silently inside model fit | Do Step 1 cleaning explicitly; print counts |
| Blanket-mean-imputing covariates with high missingness | Consider MICE (`statsmodels.imputation`) or dropping the variable |
| Reporting only the coefficient, not the CI | Always report point + 95% CI + N; plot coefplot |
| One specification, no robustness | Ship progressive specs (M1–M6) + alternative SEs |
| Reporting only the headline coefficient (no Table 2) | **Always** ship the multi-column M1→M6 main table — that is the centerpiece of an economics paper, not the abstract sentence |
| Coefficient table without any figures | An economics result needs **at least** F1 trend + F2 event study + F3 coefplot + F4 sensitivity — see the Default Output Spec |
| RD with a single bandwidth | Show bandwidth sensitivity + `rdbwselect` |
| IV without first-stage F | Always print `.first_stage` (F > 10, ideally > 104) |
| PSM without SMD balance table | Report pre/post SMDs, target \|SMD\| < 0.1 |
| Interpreting mediation without Imai sensitivity | For causal mediation, never stop at Baron–Kenny in a serious paper |
| "Table 1 in Excel after pipeline finishes" | Build Table 1 in Step 3 **before** any regression |
| p-hacking via specification selection | Disclose the **full** specification curve, not the favorite cell |

---

## Typical agent execution pattern

```python
# 1. Clean
df = load_and_clean(raw_path)                    # Step 1

# 2. Transform
df = construct_vars(df)                          # Step 2

# 3. Describe
table1 = build_table1(df, by="training")         # Step 3
save_corr_heatmap(df, cols)                      # Step 3

# 4. Diagnose
run_diagnostics(df, y="log_wage", x=covariates)  # Step 4

# 5. Model
results_main = fit_baseline(df)                  # Step 5

# 6. Robustify
results_robust = robustness_battery(df)          # Step 6

# 7. Extend
results_het   = heterogeneity_analysis(df)       # Step 7
results_mech  = mechanism_analysis(df)           # Step 7

# 8. Export
export_latex_tables(results_main, results_robust, results_het)  # Step 8
save_all_figures()                                              # Step 8
```

The deliverable for every run is the **economics empirical-paper output set** defined in the Default Output Spec:

- **5 tables** — `tables/table1_balance.{tex,docx}`, `tables/table2_main.{tex,docx}` ★, `tables/table3_mechanism.tex`, `tables/table4_heterogeneity.tex`, `tables/table5_robustness.tex`
- **4 figures** — `figures/fig1_trend.{pdf,png}`, `figures/fig2_event_study.{pdf,png}`, `figures/fig3_coefplot.{pdf,png}`, `figures/fig4_sensitivity.{pdf,png}`
- **A diagnostic log** with every Step 4 test result printed and every row exclusion counted
- **A reproducible script / notebook** that regenerates the entire output set from the raw data

If any deliverable is missing or skipped, print **why** (e.g. "F2 event study omitted: design is cross-sectional"). Do not silently drop.

---

## Regtable (pf.etable / Stargazer) cookbook (one-page recipe index)

`pf.etable(*models, ...)` and `Stargazer([...])` are the two primitives behind every multi-regression table. The eight patterns above map to:

| Pattern | What varies across columns | Step |
|---|---|---|
| **A. Progressive controls** | covariate set / FE depth | 5.A — Table 2 |
| **B. Design horse race** | identification strategy (OLS / IV / DID / DML / PSM) | 5.B — Table 2-bis |
| **C. Multi-outcome** | dependent variable Y | 5.C — Table 2-ter |
| **D. Stacked Panel A / B** | horizon / sample (panel rows × spec columns) | 5.D — Table 2-quater |
| **E. IV reporting triplet** | first stage / reduced form / 2SLS | 5.E — Table 2-quinto |
| **F. Causal-orchestrator** | 1 column, full diagnostics (`CausalForestDML` / `att_gt` / `synth`) | 5.F |
| **G. Subgroup table** | subsample (full / female / male / Q1…Q4) | 7 — Table 3 |
| **H. Robustness master** | every robustness check stacked | 6.g — Table A1 |

Default `pf.etable` settings for AER house style:

```python
pf.etable(models,
          type="tex", file="tables/tableN.tex",
          headers=["(1)", "(2)", ...],          # column labels
          digits=3, signif_code=[0.1, 0.05, 0.01],
          notes=("Cluster-robust SE in parentheses. "
                 "* p<0.10, ** p<0.05, *** p<0.01."))
# Word version: same call with type="docx".
# For multi-source tables (mixing pyfixest + statsmodels + linearmodels), use Stargazer.
```

---

## Figure factory (the 12 standard AER figures in Python)

| # | Figure | Python commands | Section |
|---|---|---|---|
| 1a | Raw trends (DID Figure 1) | `df.groupby([time,treat])[y].mean().unstack().plot()` | §1 |
| 1b | Treatment rollout heatmap | `seaborn.heatmap(rollout_pivot)` | §1 |
| 2a | Event-study coefficients | `pf.iplot(pf.feols("y ~ sunab(G,t) | i+t"))` | §3 (Step 3.5.1) |
| 2a' | Bacon weights | `bacondecomp.bacon(...)` (Python port) or rpy2 callout | §3 |
| 2a'' | CS-DID dynamic effects | rpy2 → `did::att_gt`/`ggdid` | §3 |
| 2b | First-stage scatter | `binsreg(y=D, x=Z, w=X)` | §3 (Step 3.5.2) |
| 2c | RD canonical plot | `rdrobust.rdplot(y, x, c=0)` | §3 (Step 3.5.3) |
| 2c' | McCrary density | `rddensity.rdplotdensity(...)` | §3 |
| 2d | Matching love plot | `causalml`/`MatchIt` SMD pre vs post | §3 (Step 3.5.4) |
| 2e | SCM trajectory | `pysynth` · `SyntheticControlMethods.Synth` | §3 (Step 3.5.5) |
| 3 | Coefficient plot of main specs | `pf.coefplot(models, coefs=["training"])` | §4 |
| 4a | Dose-response | `econml.dml.LinearDML(...).effect()` + matplotlib | §5 |
| 4b | CATE distribution | `CausalForestDML(...).effect()` + `plt.hist` | §5 |
| 5 | Specification curve | `itertools.product` + `matplotlib.errorbar` (see 6.h) | §7 |
| 6 | Sensitivity dashboard | `HonestDiD` + Oster δ + E-value table | §7 (Step 6.i) |
| 7 | Final main figure | estimator-specific (`rdplot`, `iplot`, `Synth.plot`) | §8 |

> Every figure is exported as **both** `.pdf` (for LaTeX) and `.png ≥ 300 dpi` (for slides / web). Use `plt.style.use("default")` + `seaborn.set_context("paper")` once at the top of `master.py` for consistent styling.

---

## Method Catalog

### Classical OLS / Panel
```python
import statsmodels.formula.api as smf
import pyfixest as pf
from linearmodels.panel import PanelOLS, RandomEffects, FirstDifferenceOLS

smf.ols   ("y ~ X", df).fit(cov_type="cluster", cov_kwds={"groups": df["i"]})    # OLS
pf.feols  ("y ~ X | fe1", df,                       vcov={"CRV1": "i"})            # OLS + 1 FE
pf.feols  ("y ~ X | fe1 + fe2", df,                 vcov={"CRV1": "i"})            # HD FE workhorse
pf.feols  ("y ~ X | fe1 + fe2", df,                 vcov={"CRV1": "fe1+fe2"})      # 2-way cluster
pf.fepois ("count ~ X | fe1 + fe2", df,             vcov={"CRV1": "i"})            # Poisson + FE
pf.feglm  ("y ~ X | fe1", df, family="logit",       vcov={"CRV1": "i"})            # Logit + FE
PanelOLS.from_formula("y ~ X + EntityEffects + TimeEffects", df).fit(cov_type="clustered")
RandomEffects.from_formula("y ~ X", df).fit()                                     # RE (Hausman)
```

### Difference-in-Differences
```python
# 2×2 DID
pf.feols("y ~ i(treated, post, ref=0) | i + t", df, vcov={"CRV1":"i"})
# Staggered — modern stack (Sun-Abraham via pyfixest::sunab)
pf.feols("y ~ sunab(first_treat, year) | i + year", df, vcov={"CRV1":"i"})
# Callaway-Sant'Anna — R callout via rpy2
import rpy2.robjects as ro; from rpy2.robjects import pandas2ri; pandas2ri.activate()
ro.r('library(did); cs <- att_gt(yname="y", tname="t", idname="i", gname="G", data=df)')
# Borusyak-Jaravel-Spiess — also R callout (didimputation) or Python `did_imputation` if installed
# Synthetic DID — R callout to `synthdid`
```

### Instrumental Variables / 2SLS
```python
from linearmodels.iv import IV2SLS, IVLIML, IVGMM
IV2SLS.from_formula("y ~ 1 + X + [D ~ Z]", df).fit(cov_type="clustered", clusters=df["firm_id"])
# Or via pyfixest:
pf.feols("y ~ X | D ~ Z", df, vcov={"CRV1":"firm_id"})
# Weak-IV diagnostics: ivreg2 has CD/KP, linearmodels reports first_stage().diagnostics
```

### Regression Discontinuity
```python
from rdrobust import rdrobust, rdplot, rdbwselect
from rddensity import rddensity
rdrobust(y=df["y"], x=df["x"], c=0, kernel="triangular", bwselect="mserd")        # Sharp RD
rdrobust(y=df["y"], x=df["x"], c=0, fuzzy=df["D"])                                # Fuzzy RD
rddensity(X=df["x"], c=0)                                                          # McCrary
rdplot   (y=df["y"], x=df["x"], c=0)
```

### Matching / Reweighting
```python
import causalml.match as cm
from causalml.match import NearestNeighborMatch
NearestNeighborMatch(replace=False, ratio=1).match(df, treatment_col="D", score_cols=["X1","X2"])
# Entropy balancing — econml or hand-rolled via scipy.optimize
```

### Synthetic Control
```python
from SyntheticControlMethods import Synth
Synth(df, "y", "unit", "time", treatment_period=2015, treated_unit=1)
# SDiD via rpy2 callout to R::synthdid
```

### ML Causal (Mode B — see §B)
```python
from econml.dml import LinearDML, CausalForestDML, NonParamDML
from econml.dr import DRLearner
from econml.metalearners import SLearner, TLearner, XLearner
from econml.iv.dml import OrthoIV
# Full pipeline in §B.
```

### Robustness, Sensitivity & Inference
```python
# Two-way cluster: vcov={"CRV1":"firm_id+year"} in pyfixest
# Wild cluster bootstrap: rpy2 → R::fwildclusterboot, or pyfixest's wildboottest()
fit.wildboottest(param="training", B=9999, seed=42)
# Randomization inference: rpy2 → R::ri2 or hand-roll via permutation
# Romano-Wolf: rpy2 → R::wyoung; or hand-roll via stepdown
# Oster δ: see references/06-robustness.md §6.6
# HonestDiD: rpy2 → R::HonestDiD
# E-value: hand-rolled VanderWeele-Ding formula (see 6.i)
```

### Survival / Epi (Mode A — see §A)
```python
from lifelines import KaplanMeierFitter, CoxPHFitter, WeibullAFTFitter
KaplanMeierFitter().fit(df["time"], df["event"]).plot()                            # KM
CoxPHFitter().fit(df, duration_col="time", event_col="event")                      # Cox
WeibullAFTFitter().fit(df, duration_col="time", event_col="event")                 # AFT
# RMST: lifelines.utils.restricted_mean_survival_time
import zepid
zepid.causal.gformula.SurvivalGFormula(...)                                        # g-formula
zepid.causal.ipw.IPTW(...)                                                          # IPTW
zepid.sensitivity_analyses.e_value(...)                                            # E-value
```

---

## When to hand off to other skills

- **Agent-native single-import workflow** (`import statspai as sp`) → `00-StatsPAI_skill`.
- **Causal Inference: The Mixtape style code templates** (Python/R/Stata side-by-side) → `10-Jill0099-causal-inference-mixtape`.
- **DSGE / HANK numerical macro** → `20-wenddymacro-python-econ-skill`.
- **Pure pyfixest reference** (every `feols` kwarg) → `40-py-econometrics-pyfixest`.
- **Paper writing / LaTeX drafting** after the analysis is done → the writing-oriented skills in this repo (`04-*-scientific-writer`, `08-*-web-latex`, etc.).

This skill's remit **ends at Step 8** — polished tables and figures. Paper drafting is out of scope.
