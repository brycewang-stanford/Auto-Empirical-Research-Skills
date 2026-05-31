---
name: Full-empirical-analysis-skill-Stata
description: Classical end-to-end empirical analysis workflow in the traditional Stata ecosystem — native Stata + reghdfe + ivreg2 + csdid + did_imputation + eventstudyinteract + sdid + rdrobust + rddensity + synth + synth_runner + psmatch2 + teffects + ebalance + coefplot + esttab + asdoc + binscatter. **Defaults to economics empirical-paper style** (AER / QJE / AEJ) — every run produces a publication-ready output set with a multi-column regression table (M1→M6 progressive controls/FE) as the centerpiece, plus Table 1 (descriptives), mechanism / heterogeneity / robustness tables, and event-study + coefficient + trend figures. Covers the full 8-step Stata pipeline an applied economist runs on every paper — (1) data import & cleaning (use/import, destring, misstable, duplicates, merge assert), (2) variable construction (gen/egen/winsor2/xtile/xtset with L./F./D.), (3) descriptive statistics & Table 1 (tabstat/balancetable/asdoc), (4) classical diagnostic tests (sktest/swilk/hettest/imtest/xtserial/xttest3/vif/dfuller/kpss/hausman/estat overid), (5) baseline modeling (reg/xtreg/reghdfe/ivreg2/ivregress/csdid/did_imputation/eventstudyinteract/sdid/rdrobust/synth/psmatch2/teffects/heckman/qreg/ppmlhdfe), (6) robustness battery (bacondecomp/honestdid/rwolf/ritest/wildbootstrap/oster), (7) further analysis (subgroup/triple-diff/interactions/medsem/marginsplot/binscatter by group), (8) publication-ready tables & figures (esttab/outreg2/estout/coefplot/marginsplot/rdplot/twoway combined). **Also covers two parallel domain modes that share the same 8-step scaffolding** — **Mode A — Epidemiology / public health** (target-trial emulation, IPTW + g-formula + TMLE doubly-robust triplet via `teffects ipw` / `teffects ipwra` / `teffects aipw` / `eltmle`, Mendelian randomization via `mrrobust` (IVW / Egger / weighted median) and `mregger` / `mrpresso`, KM / Cox / AFT / RMST survival via `sts` / `stcox` / `streg` / `strmst2`, E-value sensitivity via `evalue` (Linden-Mathur), principal stratification — STROBE / TRIPOD reporting), and **Mode B — ML causal inference** (DML via `ddml` / `pdslasso`, S/T/X/R/DR meta-learners via `crforest` and `ddml interactive`, causal forest via `crforest` / `cforest`, BART/BCF via `bart` / `bartCause`-style externals, CATE distribution + policy tree via `crforest`, off-policy evaluation, conformal causal externals, fairness audit, DAG learning via `pcalg` / external Python callouts). Use when the user asks for a complete Stata empirical analysis, wants a reproducible .do-file pipeline, needs a Stata counterpart to the Python StatsPAI / Full-empirical-analysis-skill, or names a specific Stata step in isolation ("run reghdfe with two-way clustering", "csdid event study", "winsor2 at 1%", "esttab to LaTeX", "coefplot with CI", "ivreg2 weak-IV test", "synth_runner placebos", "teffects psmatch balance check"). Mode A triggers on "target trial emulation Stata", "teffects ipw aipw", "eltmle", "mrrobust", "mregger weighted median", "stcox AFT survival", "strmst2", "evalue Stata", "STROBE Stata", "公共健康 Stata", "流行病学 Stata". Mode B triggers on "ddml Stata", "pdslasso", "crforest causal forest Stata", "policy tree Stata", "因果机器学习 Stata".
triggers:
  - Stata empirical analysis
  - full Stata pipeline
  - reproducible do-file
  - Stata do-file workflow
  - reghdfe two-way FE
  - high-dimensional fixed effects Stata
  - ivreg2 weak instruments
  - ivregress 2sls liml gmm
  - csdid Callaway SantAnna
  - did_imputation Borusyak
  - eventstudyinteract Sun Abraham
  - sdid synthetic DID Stata
  - rdrobust Stata
  - rddensity manipulation test
  - synth synthetic control
  - synth_runner placebo
  - psmatch2 propensity score
  - teffects psmatch
  - teffects ipwra AIPW Stata
  - ebalance entropy balancing
  - xtreg fe re hausman
  - ppmlhdfe Poisson
  - quantile regression qreg
  - heckman selection model
  - esttab publication table
  - outreg2 LaTeX
  - estout coefplot
  - marginsplot interaction
  - rdplot binned scatter
  - binscatter Stata
  - bacondecomp Goodman Bacon
  - honestdid Rambachan Roth
  - wild cluster bootstrap boottest
  - ritest randomization inference
  - rwolf Romano-Wolf
  - oster delta
  - winsor2 winsorize Stata
  - tabstat table 1
  - balancetable Stata
  - misstable patterns
  - destring dates
  - xtset panel
  # Mode A — Epidemiology / public health
  - epidemiology pipeline Stata
  - public health causal inference Stata
  - target trial emulation Stata
  - teffects ipw aipw ipwra
  - g-formula Stata
  - eltmle TMLE Stata
  - HAL-TMLE Stata
  - Mendelian randomization Stata
  - mrrobust mregger
  - MR-PRESSO Stata
  - MR-Egger weighted median Stata
  - STROBE TRIPOD reporting Stata
  - evalue sensitivity Stata
  - Kaplan-Meier AFT survival Stata
  - sts stcox streg strmst2
  - 流行病学 Stata
  - 公共健康 Stata
  # Mode B — ML causal inference
  - ML causal inference Stata
  - ddml double machine learning Stata
  - pdslasso ivlasso
  - crforest causal forest Stata
  - cforest Stata
  - meta-learner S T X R DR Stata
  - CATE distribution Stata
  - policy tree Stata
  - off-policy evaluation Stata
  - conformal causal Stata
  - causal discovery PC Stata
  - 因果机器学习 Stata
---

# Full Empirical Analysis — Classical Stata Workflow

This skill is the *canonical* 8-step pipeline an applied economist runs on every empirical paper, written in the **traditional Stata ecosystem** — native Stata + the 20+ community commands that have become de-facto standards (`reghdfe`, `ivreg2`, `csdid`, `did_imputation`, `eventstudyinteract`, `sdid`, `rdrobust`, `rddensity`, `synth`, `synth_runner`, `psmatch2`, `teffects`, `ebalance`, `coefplot`, `esttab`, `outreg2`, `boottest`, `ritest`, `rwolf`, `bacondecomp`, `honestdid`, `binscatter`).

**Companion skills**: if the user wants the same pipeline in Python, route to `00-StatsPAI_skill` (agent-native DSL) or `00.1-Full-empirical-analysis-skill` (explicit Python stack). **This skill is the Stata counterpart** — every step produces a `.do` file you can hand to a journal's replication office or a co-author who refuses to leave Stata.

## Philosophy

1. **Stata idioms, not Python-translated.** `reghdfe`, not "statsmodels analogue of reghdfe". `esttab`, not "Stata's stargazer".
2. **Reproducible .do files.** Every code block below is runnable after `use data.dta, clear`. No Jupyter, no notebooks — just do-files and log files.
3. **Full pipeline, not just regressions.** Stata users historically over-invest in Step 5 (modeling) and under-invest in Steps 1–4 and 6–8. This skill treats them as first-class.
4. **Rich outputs.** Every step yields at least one table (`.tex`/`.rtf`) or figure (`.pdf`/`.png`) — never a coefficient printed to the Results window and forgotten.
5. **Progressive disclosure.** `SKILL.md` gives the canonical command at each step; [`references/`](references/) holds variant-specific depth (dozens of tests, estimator-specific diagnostics, graph recipes).

---

## Three domain modes (default = AER econ; alternates = epi & ML-causal)

The default playbook above is **AER-style applied econometrics** — the AEA convention: written-out estimating equation, identifying assumption, design horse-race, full robustness gauntlet. The skill **also** ships two parallel sub-pipelines for the other two big causal-inference traditions, each reusing the same Steps 1–4 (cleaning / construction / Table 1 / diagnostics) and Step 8 (tables/figures) — only Step 5 (estimator) and Step 6/7 swap commands:

| Mode | Reader convention | Step-5 estimator stack | Reporting stack | Jump to |
|---|---|---|---|---|
| **Default — Applied Econ (AER / QJE / AEJ)** | "Show the equation + identifying assumption + design horse-race; controls visible; clustered SE" | DID / IV / RD / SCM / matching / `reghdfe` HDFE | AER house-style multi-column `esttab` / `outreg2` / `coefplot` + 8-section paper layout | Steps 1 → 8 (entire playbook below) |
| **Mode A — Epidemiology / Public Health** | "STROBE / TRIPOD-AI; target trial protocol; doubly-robust estimand; absolute & relative risk; KM survival" | Target-trial emulation · IPTW (`teffects ipw`) · IPWRA / AIPW (`teffects ipwra` / `teffects aipw`) · g-formula (`gformula`) · TMLE (`eltmle`) · Mendelian randomization (`mrrobust` IVW / `mregger` / `mrpresso`) · KM/Cox/AFT (`sts`/`stcox`/`streg`/`strmst2`) | Same `esttab` + risk-difference / hazard-ratio / E-value rows | §A. Epidemiology pipeline |
| **Mode B — ML Causal Inference** | "DML / meta-learners / causal forest / DR-learner; CATE distribution; policy value" | DML (`ddml` / `pdslasso`) · S/T/X/R/DR-Learner (`ddml interactive`) · GRF causal forest (`crforest` / `cforest`) · BART / BCF (external Python via `python_user`) · matrix completion (external) | `esttab` ML horse-race + `crforest` CATE plot + policy-value table | §B. ML causal pipeline |

**How to invoke a non-default mode** (Claude / agent picks this up from the user's wording):

| User says... | Mode the skill switches to |
|---|---|
| "Run a DID / IV / RD / event study", "AER table", "applied micro" | Default (AER econ) — Steps 1 → 8 |
| "Target trial emulation", "g-formula", "IPTW", "TMLE", "Mendelian randomization", "STROBE / TRIPOD", "公共健康 / 流行病学", "epi pipeline", "RWE study", "cohort study", "case-control" | Mode A (Epi) — §A |
| "DML", "double machine learning", "ddml", "causal forest", "crforest", "meta-learner", "CATE", "policy learning", "ML causal", "因果机器学习" | Mode B (ML causal) — §B |
| "Mix" (e.g. "estimate DID + then ML CATE on the heterogeneity") | Default + Mode B in sequence — every estimator stores results via `eststo`, drop them all into one `esttab` for the horse-race column |

The three modes share **the same Step 1–4 cleaning / Table 1 / diagnostics scaffolding, the same Step 8 export stack, and the same DAG-first identification logic** — switching modes only changes which Step-5 command family you reach for. If you only want descriptive stats / Table 1 / a balance check, the AER `tabstat` / `balancetable` / `asdoc` calls in Step 3 work identically across all three modes.

> **Stata-specific caveat for Mode B**: Stata's first-party ML-causal coverage is thinner than Python/R. For Dragonnet / TARNet / CEVAE / cfcausal / fairness audit, call out to Python via Stata 18's `python:` / `python script` block (or shell out to a sister `.py`) and read the result back via `frame` or `import delimited`. The skill prefers native Stata commands (`ddml`, `pdslasso`, `crforest`) where they exist, and explicitly marks the Python callouts in §B.

---

## Default Output Spec — Economics Empirical Paper

This skill defaults to the **applied-economics paper convention**. Unless the user explicitly asks for a single point estimate, every `.do`-file run produces the full publication-ready output set below. Treat it as the contract of Step 8 — **mandatory**, not opt-in.

### Required tables (always produced)

| # | Table | Stata source | Saves to |
|---|---|---|---|
| **T1** | Summary statistics & balance (treated vs control, with SMD / p-values) | `balancetable` + `asdoc sum` (Step 3) | `tables/table1_balance.{tex,rtf,xlsx,docx}` |
| **T2** ★ | **Main results — multi-column regression M1→M6** (progressive controls + FE) | `eststo` 6 specs → `esttab` (Step 5–6) | `tables/table2_main.{tex,rtf,xlsx,docx}` |
| **T3** | Mechanism / outcome ladder — same treatment, 3+ outcomes side-by-side | loop `eststo: reghdfe` over outcomes → `esttab` (Step 7) | `tables/table3_mechanism.{tex,rtf,xlsx,docx}` |
| **T4** | Heterogeneity — subgroup × main coef (gender, age, region, …) | subgroup `eststo` + `suest` Wald → `esttab` (Step 7) | `tables/table4_heterogeneity.{tex,rtf,xlsx,docx}` |
| **T5** | Robustness battery — alt SE / cluster / sample / placebo, in **one** table | `eststo` × variants → `esttab` (Step 6) | `tables/table5_robustness.{tex,rtf,xlsx,docx}` |

> **★ Table 2 is the centerpiece of every economics paper.** It is the multi-column regression table that walks the reader from raw correlation (M1) to the fully-specified design (M6: 2-way FE + interacted FE + cluster-robust SE). Do **not** collapse it into a single column. Do **not** report only the headline coefficient. The progression *is* the credibility argument: if M1→M6 is monotone and stable, the design is plausibly identifying; if it collapses on adding FE, that *is* the result.
>
> **Canonical 6 columns, in order:**
> 1. **M1** raw bivariate (`reg y treat`)
> 2. **M2** + demographics (`+ age + edu`)
> 3. **M3** + sector controls (`+ tenure / firm_size`)
> 4. **M4** + unit FE (`reghdfe ..., absorb(unit)`)
> 5. **M5** + 2-way FE (`absorb(unit year)`)
> 6. **M6** + interacted FE (`absorb(unit year i.industry#i.year)`) with `vce(cluster unit)`

### Required figures (always produced)

| # | Figure | Stata source | Saves to |
|---|---|---|---|
| **F1** | Trend / motivation — treated vs control over time, with policy line | `collapse (mean) y, by(year treat)` → `twoway line` (Step 3) | `figures/fig1_trend.pdf` (+ `.png`) |
| **F2** | Event-study coefficients with 95% CI, base period at –1 | `eventstudyinteract` / `csdid` / `coefplot, keep(*.rel)` (Step 5) | `figures/fig2_event_study.pdf` |
| **F3** | Coefficient plot across specs M1→M6 | `coefplot m1 m2 m3 m4 m5 m6, keep(treat) vertical` (Step 8) | `figures/fig3_coefplot.pdf` |
| **F4** | Robustness / sensitivity curve — `bacondecomp` plot, `honestdid` plot, or cluster-comparison forest | scenario-specific (Step 6) | `figures/fig4_sensitivity.pdf` |

### Output file layout (default)

```
project/
├── tables/    table1_balance.{tex,rtf,xlsx,docx}  table2_main.{tex,rtf,xlsx,docx}
│              table3_mechanism.{tex,rtf,xlsx,docx}   table4_heterogeneity.{tex,rtf,xlsx,docx}
│              table5_robustness.{tex,rtf,xlsx,docx}
└── figures/   fig1_trend.{pdf,png}        fig2_event_study.{pdf,png}
               fig3_coefplot.{pdf,png}     fig4_sensitivity.{pdf,png}
```

Every table → `.tex` (LaTeX `booktabs`) **and** `.rtf` (Word) **and** `.xlsx` (Excel) **and** `.docx` (Word OOXML). Every figure → `.pdf` (vector for LaTeX) **and** `.png` at ≥300 dpi (slides / web).

### When to deviate

- **Single quick estimate** — produce only the relevant cell, but warn that the standard deliverable is the full set above and offer to run it.
- **Design does not support a figure** (cross-section → no event study) — skip with a printed `display` note explaining why; do **not** silently drop.
- **N=1 treated unit (`synth`)** — replace F1/F2 with the SCM trajectory + placebo distribution from `synth_runner`; T1–T5 still apply.

---

## Required packages

```stata
* Run once on a fresh Stata install:
ssc install reghdfe,         replace
ssc install ftools,          replace       // dependency of reghdfe / ivreg2
ssc install ivreg2,          replace
ssc install ranktest,        replace       // dependency of ivreg2
ssc install ivreghdfe,       replace       // ivreg2 × reghdfe: high-dim FE IV
ssc install ppmlhdfe,        replace       // Poisson with HD FE
ssc install csdid,           replace       // Callaway–Sant'Anna (2021)
ssc install drdid,           replace       // dependency of csdid
ssc install did_imputation,  replace       // Borusyak–Jaravel–Spiess (2024)
ssc install eventstudyinteract, replace    // Sun & Abraham (2021)
ssc install sdid,            replace       // Synthetic DID (Arkhangelsky et al. 2021)
ssc install did_multiplegt_dyn, replace    // de Chaisemartin & D'Haultfœuille
ssc install bacondecomp,     replace       // Goodman-Bacon (2021)
ssc install honestdid,       replace       // Rambachan–Roth (2023) PT sensitivity
ssc install rdrobust,        replace       // Calonico–Cattaneo–Titiunik RD
ssc install rddensity,       replace       // McCrary / Cattaneo et al. density test
ssc install synth,           replace       // Abadie–Diamond–Hainmueller SCM
ssc install synth_runner,    replace       // SCM with placebos + inference
ssc install psmatch2,        replace       // propensity-score matching
ssc install ebalance,        replace       // entropy balancing
ssc install coefplot,        replace
ssc install estout,          replace       // provides estout / esttab / eststo
ssc install outreg2,         replace
ssc install asdoc,           replace       // one-click Word/Excel tables
ssc install binscatter,      replace
ssc install balancetable,    replace
ssc install winsor2,         replace
ssc install xtable,          replace       // better xtreg output tables
ssc install boottest,        replace       // wild cluster bootstrap (Roodman et al.)
ssc install ritest,          replace       // randomization inference
ssc install rwolf,           replace       // Romano–Wolf multiple-testing
ssc install moremata,        replace       // Mata extensions (dep for several)
ssc install mdesc,           replace       // missing data description
ssc install missings,        replace       // missings dropvars, report
ssc install unique,          replace       // unique IDs in panel
ssc install schemepack,      replace       // modern publication themes
```

---

## The 8 Steps — Canonical Pipeline (mapped to AER paper sections)

```
┌──────────────────────────────────────────────────────────────────────┐
│ Step −1 Pre-Analysis Plan (PAP)   power/sampsi/clustersampsi/MDE     │
│ Step 0  Sample log + data contract sample_log/assert/xtdescribe/JSON │
│ Step 1  Data import & cleaning    use/import/destring/misstable/merge│
│ Step 2  Variable construction     gen/egen/winsor2/xtile/xtset/L.F.D.│
│ Step 2.5 Empirical strategy       equation × ID assumption + pre-reg │
│ Step 3  Descriptive statistics    tabstat/balancetable/asdoc/pwcorr  │
│ Step 3.5 Identification graphics  event-study/1st-stage/McCrary/love │
│ Step 4  Diagnostic tests          sktest/hettest/xtserial/vif/dfuller│
│ Step 5  Baseline modeling         reghdfe/ivreg2/csdid/rdrobust/synth│
│ Step 6  Robustness battery        bacondecomp/honestdid/rwolf/boottest│
│ Step 7  Further analysis          triple-diff/subgroup/medsem/margins│
│ Step 8  Tables & figures          esttab/outreg2/coefplot/rdplot     │
└──────────────────────────────────────────────────────────────────────┘
```

The 8 steps mirror the canonical sections of an applied AER / QJE / AEJ paper. Each step is one paper section and emits a paper-ready artifact on disk:

```
Paper section               Step  Stata moves
─────────────────────────── ───── ────────────────────────────────────────────────
Pre-Analysis Plan           −1    power/sampsi + freeze protocol.do to disk
§1. Data                     0    sample_log + 5-check data contract → JSON
§1. Data                     1    use/import/destring/misstable/merge assert/xtset
§1. Data                     2    gen/egen/winsor2/xtile/L./F./D./CPI deflation
§1.1 Descriptives (Table 1)  3    tabstat · balancetable · asdoc · pwcorr · twoway
§2. Empirical Strategy       2.5  write equation + ID assumption → strategy.do
§3. Identification graphics  3.5  event-study · 1st-stage F · McCrary · love · SCM
§3.5 Diagnostics             4    swilk · hettest · xtserial · vif · dfuller · hausman
§4. Main Results (Table 2)   5    M1→M6 progressive controls + FE  (eststo + esttab)
§5. Heterogeneity (Table 3)  7    margins/marginsplot · subgroup · medsem
§6. Mechanisms / Channels    7    medsem/khb · outcome ladder · DDD interactions
§7. Robustness gauntlet      6    bacondecomp · honestdid · psacalc · boottest · ritest · rwolf
§8. Replication package      8    esttab + outreg2 + coefplot + reproducibility stamp
```

Below is the canonical command at each step. **All examples share one running narrative** — a labor-economics panel where `training` (treatment) affects `log_wage` (outcome), with covariates `age`, `edu`, `tenure`, panel keys `worker_id` / `firm_id` / `year`. Variable names and parameter values are **illustrative**; substitute the real ones from the user's dataset. Only command names and option *shapes* are normative.

> **When a step has many variants** (e.g. staggered DID has 5 estimators; heteroskedasticity has 4 classic tests), SKILL.md shows the one you reach for first and links to `references/NN-<topic>.md` for the rest. **Read the reference file when the user's case doesn't fit the default.**

---

## Paper-ready figure & table inventory (what to produce by section)

A modern AER paper has **5–7 figures** and **3–5 main tables** + an appendix robustness table. Every step below leaves at least one numbered artifact on disk. Default file names assume parallel `.tex` / `.rtf` exports (the agent should produce both so co-authors can edit in Word, and the build system can use LaTeX):

| § | Artifact | Stata primitive | Filenames |
|---|---|---|---|
| §1 | **Figure 1**: raw trends / treatment rollout | `collapse` + `twoway line` · `heatplot` for staggered rollout | `figures/fig1_trend.{pdf,png}` |
| §1 | **Table 1**: summary stats (full / treated / control + Δ + SMD) | `balancetable` · `asdoc sum, by()` · `tabstat` | `tables/table1_balance.{tex,rtf,xlsx,docx}` |
| §3 | **Figure 2**: identification graphic (event-study / first-stage / McCrary / RD scatter / SCM trajectory) | `coefplot` after `eventstudyinteract`/`csdid` · `binscatter` · `rdplot` · `rddensity, plot` · `synth` | `figures/fig2_event_study.{pdf,png}` |
| §4 | **Table 2**: main results — progressive controls M1→M6 | `eststo` 6 specs → `esttab` | `tables/table2_main.{tex,rtf,xlsx,docx}` |
| §4 | **Table 2-bis**: design horse-race (OLS / IV / DID / matching) | `eststo` mix + `esttab` | `tables/table2b_designs.{tex,rtf,xlsx,docx}` |
| §4 | **Figure 3**: coefficient plot across specs | `coefplot m1 m2 m3 m4 m5 m6, keep(treat)` | `figures/fig3_coefplot.{pdf,png}` |
| §5 | **Table 3**: heterogeneity by subgroup | `eststo` per slice + `esttab` + `suest` Wald | `tables/table3_heterogeneity.{tex,rtf,xlsx,docx}` |
| §5 | **Figure 4**: dose-response / margins-by-quartile | `xtile` + `margins` + `marginsplot` | `figures/fig4_dose.{pdf,png}` |
| §6 | **Table 4**: mechanism / outcome ladder | loop `eststo: reghdfe` over outcomes → `esttab` | `tables/table4_mechanism.{tex,rtf,xlsx,docx}` |
| §7 | **Table A1**: robustness master (one column per check) | `eststo` × variants → `esttab` | `tables/tableA1_robustness.{tex,rtf,xlsx,docx}` |
| §7 | **Figure 5**: spec curve — coefficient + 95% CI across all specs | hand-rolled spec loop + `twoway rcap` | `figures/fig5_spec_curve.{pdf,png}` |
| §7 | **Figure 6**: sensitivity (HonestDiD / Oster / E-value) | `honestdid, coefplot` · `psacalc plot` · `evalue` table | `figures/fig6_sensitivity.{pdf,png}` |
| §8 | **Replication bundle**: all tables in one document | `esttab ..., append` to one `.tex` / `.rtf` · `texdoc` | `replication/paper_tables.{tex,rtf,xlsx,docx}` |

> Every Stata estimator above stores results via `eststo` and can be passed straight into `esttab` / `coefplot` / `outreg2`. Don't hand-roll LaTeX, and don't render Word from `outsheet`/`putexcel` matrices — `esttab` and `outreg2` apply book-tab borders, AER-style stars, and the right SE label automatically. For deeper export recipes (LaTeX / Word / Markdown variants, `texdoc`, `frmttable`), see [`references/08-tables-plots.md`](references/08-tables-plots.md).

---

## Export cookbook — LaTeX / Word / RTF in one block

Stata's export stack is more fragmented than Python's StatsPAI. Three tiers, picked by **scope**:

| Tier | Use when | API | Hot options |
|---|---|---|---|
| **1. Single multi-column table** | Exporting *one* Table 2 / Table 3 / Table A1 with progressive columns | **`.tex` / `.rtf`**: `esttab` with `booktabs`<br>**`.xlsx` / `.docx`**: `outreg2` (esttab's native Office export is a data dumper, not a publication formatter — outreg2 produces properly formatted Word/Excel with borders, aligned stars, and AER-style layout) | **`esttab`** for tex/rtf: `keep()`, `drop()`, `mtitles()`, `stats(N r2 r2_a, labels(...))`, `star(* 0.10 ** 0.05 *** 0.01)`, `label`, `booktabs`, `addnotes()`.<br>**`outreg2`** for xlsx/docx: `label dec(3)`, `addtext()` for FE indicators, `replace` first / `append` subsequent columns.<br>Always emit all four formats — esttab for tex/rtf in a `foreach ext in tex rtf` loop, outreg2 for xlsx/docx in a separate `foreach ext in xlsx docx` loop. |
| **2. Multi-panel paper format** (Tables 2 + 3 + A1 + A2 in one file) | Producing the paper-tables block — main + heterogeneity + robustness + placebo as a single document | `esttab ... using "paper.tex", replace` for first panel; subsequent `esttab ... using "paper.tex", append` for each next panel; `texdoc init "paper.tex"` for full LaTeX with prose. Repeat for `.rtf`/`.xlsx`/`.docx` bundles. | first panel: `replace`; subsequent: `append`; surround with `texdoc` for headings |
| **3. Full session bundle** (the Stata 17+ `collect` equivalent) | Replication appendix that mixes summary stats + balance + multiple regression tables + headings + prose in **one** file | `collect create paper`<br>`collect get summary, ...`<br>`collect get est ...`<br>`collect layout ...`<br>`collect export "paper.xlsx"` (also `.docx`/`.html`/`.tex`/`.md`) | Stata 17+ only; for older Stata use `texdoc` / `markdoc` |

**Journal styling — pick the right `star` levels and SE label.** The AEA convention is `* 0.10 ** 0.05 *** 0.01` and SE label "Standard errors in parentheses"; QJE / Econometrica / RES variants only differ in stars / notes / fonts. Define an `esttab` wrapper once at the top of the do-file:

```stata
* Top of master.do — journal house-style wrapper
local AER_STAR  "* 0.10 ** 0.05 *** 0.01"
local AER_NOTES "Cluster-robust standard errors in parentheses. * p<0.10, ** p<0.05, *** p<0.01."
local AER_STATS stats(N r2_a, labels("N" "Adj. R²"))

* LaTeX + RTF via esttab (booktabs for tex)
* esttab m1 m2 m3 using "tables/table2.tex", replace ///
*     se star(`AER_STAR') label booktabs `AER_STATS' addnotes(`AER_NOTES')
* esttab m1 m2 m3 using "tables/table2.rtf", replace ///
*     se star(`AER_STAR') label `AER_STATS' addnotes(`AER_NOTES')

* Excel + Word via outreg2 (publication-grade Office formatting)
* First column: replace; subsequent: append
* outreg2 using "tables/table2.xlsx", replace label dec(3) ///
*     keep(training age edu tenure) addtext(Worker FE, Yes, Year FE, Yes)
* outreg2 using "tables/table2.xlsx", append   label dec(3) ///
*     keep(training age edu tenure region) addtext(Worker FE, Yes, Year FE, Yes, Region, Yes)
```

**Multi-format export pattern** — emit `.tex` and `.rtf` via `esttab`, then `.xlsx` and `.docx` via `outreg2`. Never use `esttab ... using "... .xlsx"` or `esttab ... using "... .docx"` — esttab's native Office export is a raw data dumper, not a publication formatter:

```stata
* LaTeX + RTF — use esttab (booktabs for tex, rich text for rtf)
foreach ext in tex rtf {
    esttab m1 m2 m3 using "tables/table2_main.`ext'", ///
        replace se star(* 0.10 ** 0.05 *** 0.01) ///
        label booktabs mtitles("(1)" "(2)" "(3)") ///
        stats(N r2_a, labels("N" "Adj. R²")) ///
        addnotes("Cluster-robust SE in parentheses. * p<0.10, ** p<0.05, *** p<0.01.")
}

* Excel + Word — use outreg2 (proper Office table formatting, aligned stars, borders)
* First model: replace
eststo m1: qui reghdfe log_wage training age edu tenure, absorb(worker_id year) vce(cluster worker_id)
outreg2 using "tables/table2_main.xlsx", replace label dec(3) ///
    keep(training age edu tenure) ///
    addtext(Worker FE, Yes, Year FE, Yes)

* Subsequent models: append
eststo m2: qui reghdfe log_wage training age edu tenure region, absorb(worker_id year) vce(cluster worker_id)
outreg2 using "tables/table2_main.xlsx", append label dec(3) ///
    keep(training age edu tenure region) ///
    addtext(Worker FE, Yes, Year FE, Yes, Region, Yes)

* docx follows the same pattern but with the .doc extension
outreg2 using "tables/table2_main.doc", replace label dec(3) ///
    keep(training age edu tenure) ///
    addtext(Worker FE, Yes, Year FE, Yes)
eststo m2
outreg2 using "tables/table2_main.doc", append label dec(3) ///
    keep(training age edu tenure region) ///
    addtext(Worker FE, Yes, Year FE, Yes, Region, Yes)
```

**Figures always export to both `.pdf` and `.png` at ≥300 dpi** (vector for LaTeX, raster for slides/web/Word embedding):

```stata
graph export "figures/fig1_trend.pdf", replace
graph export "figures/fig1_trend.png", replace width(2400) height(1800)
```

For the `collect` / `texdoc` / `markdoc` cookbook (Stata 17+ multi-panel paper bundle and prose+tables PDF/Word generation), see [`references/08-tables-plots.md`](references/08-tables-plots.md).

---

## Step −1 — Pre-Analysis Plan (pre-data; AEA RCT Registry style)

Before touching the data, write down (a) the population, (b) the design, (c) the **minimum detectable effect (MDE)** under the planned sample size and α=0.05, β=0.20. Persist the result as `protocol.do` so a referee can verify the design was powered before, not after, the data were seen.

```stata
* Two-sample MDE (continuous outcome, Cohen's d framing)
power twomeans 0, diff(0.2) sd(1) power(0.80) alpha(0.05)
* → required n per arm

* Cluster-randomized RCT — solve for n_clusters given ICC
power twomeans 0, diff(0.2) sd(1) power(0.80) k1(50) rho(0.05) cluster
* → required clusters per arm under ICC=0.05, cluster size 50

* DID power (Frison–Pocock / Bloom 1995): use -sampsi- + -clustersampsi-
* (no native `power did`; for staggered DID see references/05-modeling.md §5.4)
sampsi 0 0.15, sd(1.0) alpha(0.05) power(0.80) n1(.) n2(.)

* RD power — McCrary-style: solve via Monte Carlo with -simulate-
* (see references/05-modeling.md §5.5 RD power template)

* Persist the protocol — referee will ask whether design was powered ex ante
file open f using "protocol.do", write replace
file write f "* Pre-analysis plan — frozen `c(current_date)' `c(current_time)'" _n
file write f "* Population:    manufacturing workers 2010-2020" _n
file write f "* Treatment:     training (binary)" _n
file write f "* Outcome:       log_wage" _n
file write f "* Design:        staggered DID, csdid (Callaway-Sant'Anna 2021)" _n
file write f "* MDE:           0.05 log points at 80% power, α=0.05" _n
file write f "* N planned:     ~12,000 worker-years" _n
file close f
```

Save this `.do` file in version control **before** running Step 1. AEA RCT Registry / OSF preregistration tools accept it as the analysis-plan exhibit.

---

## Step 0 — Sample-construction log & 5-check data contract

An AER §1 *Data* section has three jobs: (a) describe sources, (b) document **every** sample restriction (the "footnote 4" sample log), (c) lock the panel structure. Stata users typically chain `keep` / `drop` commands in a single do-file with no count log, then can't reconstruct the analysis sample for the response letter. The data contract is the cure.

### 0.1 Sample-construction log (footnote 4)

```stata
use "raw.dta", clear
matrix sample_log = J(0, 2, .)
local row 0
local n0 = _N
local ++row
matrix sample_log = (nullmat(sample_log) \ `row', `n0')
display "Step 0. raw:                          N = " %12.0fc `n0'

drop if missing(wage)
local n1 = _N
local ++row
matrix sample_log = (nullmat(sample_log) \ `row', `n1')
display "Step 1. drop missing wage:            N = " %12.0fc `n1' "  (Δ " %10.0fc `n0' - `n1' ")"

drop if !inrange(age, 18, 65)
local n2 = _N
local ++row
matrix sample_log = (nullmat(sample_log) \ `row', `n2')
display "Step 2. drop age outside 18-65:       N = " %12.0fc `n2' "  (Δ " %10.0fc `n1' - `n2' ")"

keep if inlist(industry, "manuf", "construction", "transport")
local n3 = _N
local ++row
matrix sample_log = (nullmat(sample_log) \ `row', `n3')
display "Step 3. keep target industries:       N = " %12.0fc `n3' "  (Δ " %10.0fc `n2' - `n3' ")"

* Persist to JSON (for paste into footnote 4)
file open f using "artifacts/sample_construction.json", write replace
file write f "{" _n
file write f `"  "step_0_raw":     `=sample_log[1,2]',"' _n
file write f `"  "step_1_wage":    `=sample_log[2,2]',"' _n
file write f `"  "step_2_age":     `=sample_log[3,2]',"' _n
file write f `"  "step_3_indust":  `=sample_log[4,2]'"' _n
file write f "}" _n
file close f
```

Paste the `display` lines verbatim as footnote 4 of the paper.

### 0.2 Five-check data contract (go / no-go gate)

```stata
* (1) Shape
display "Check 1. n_obs = " _N

* (2) Dtypes on key vars — assert types are numeric where required
foreach v in wage training worker_id year age edu tenure {
    capture confirm numeric variable `v'
    if _rc {
        display as error "Check 2 FAILED: `v' is not numeric — fix before any panel command"
        exit 198
    }
}
display "Check 2. dtypes OK on all key vars"

* (3) Missingness pattern on key vars
mdesc wage training worker_id year age edu tenure                 // ssc install mdesc
foreach v in wage training worker_id year {
    qui count if missing(`v')
    if r(N) > 0 {
        display as error "Check 3 FAILED: `v' has " r(N) " missing — fix before estimation"
        exit 198
    }
}

* (4) Duplicate (id, time) — fatal for panel methods
duplicates report worker_id year
duplicates tag worker_id year, gen(dup)
qui count if dup > 0
if r(N) > 0 {
    display as error "Check 4 FAILED: " r(N) " duplicate (worker_id, year) rows"
    exit 198
}
drop dup

* (5) Panel balance
xtset worker_id year
xtdescribe
qui xtdes
local n_balanced = r(N)
display "Check 5. panel n=" _N " (balanced cells if `n_balanced' equals expected unit×period)"

* MCAR sniff test (Rubin) — if missing(y) is associated with covariates,
* listwise deletion biases the estimate. Use `mi` / IPW instead.
gen byte miss_y = missing(wage)
foreach cov in age edu tenure {
    qui ttest `cov', by(miss_y)
    if r(p) < 0.05 {
        display as error "WARNING: y-missingness associates with `cov' (p=" %5.3f r(p) ")."
        display as error "         -> NOT MCAR, use -mi impute- or IPW, NOT listwise drop."
    }
}
drop miss_y

* Persist contract
file open f using "artifacts/data_contract.json", write replace
file write f "{" _n
file write f `"  "n_obs": `=_N',"' _n
file write f `"  "panel": "worker_id × year","' _n
file write f `"  "treatment": "training","' _n
file write f `"  "outcome":   "log_wage""' _n
file write f "}" _n
file close f
```

If any assertion fires, **stop** and fix it. Stata estimators silently drop NaN rows, the most common source of "mysterious sample-size shrinkage" bugs in the response letter.

---

### Step 1 — Data import & cleaning

Deeper patterns: [references/01-data-cleaning.md](references/01-data-cleaning.md) — reading Excel/CSV/SAS/SPSS, `destring` on numeric-looking strings, `misstable` patterns, `duplicates` tagging, `merge` with `assert(match using)`, `xtset` balance checks, spells / gaps, labels.

```stata
* 1a. Load + first look
use "raw.dta", clear
describe, short
summarize
misstable summarize
mdesc                                   // missing-data report

* 1b. Dtypes — destring strings-that-should-be-numeric
destring year wage, replace force       // force: convert non-numeric to .
gen hire_date = date(hire_date_str, "YMD"); format hire_date %td

* 1c. Missing values — decide PER VARIABLE
local key_vars "wage training worker_id year"
foreach v of local key_vars {
    drop if missing(`v')
}
sum tenure, detail
replace tenure = r(p50) if missing(tenure)      // median-impute
gen byte tenure_miss = missing(tenure)           // keep the flag

* 1d. Outliers — flag first (winsorize in Step 2)
egen wage_z = std(wage)
count if abs(wage_z) > 4
display "Flagged |z|>4 on wage: " r(N)

* 1e. Deduplicate on panel key
duplicates report worker_id year
duplicates tag worker_id year, gen(dup)
assert dup == 0                                  // hard-fail if panel key not unique
drop dup

* 1f. Merge with assert — never silently lose rows
merge m:1 firm_id using "firm_chars.dta", ///
    assert(match using master) keep(master match) nogen

* 1g. Panel structure
xtset worker_id year                              // declares panel
xtdescribe                                        // balance summary
tab year                                          // observations per year
```

**Key principle**: all row exclusions are explicit, counted, logged. No command in Steps 2+ should silently drop rows.

---

### Step 2 — Variable construction & transformation

Deeper patterns: [references/02-data-transformation.md](references/02-data-transformation.md) — log / ihs / Box–Cox, within-group `winsor2`, `xtile` and custom cuts, `egen` recipes, time-series operators (`L.`, `F.`, `D.`, `S.`), CPI deflation, staggered-DID timing construction.

```stata
* 2a. Log / IHS
gen log_wage = log(max(wage, 1))                  // floor at 1
gen ihs_assets = asinh(assets)                    // handles 0 / negative

* 2b. Winsorize 1/99
winsor2 wage, cuts(1 99) suffix(_w1) by(year)     // within-year winsorize

* 2c. Standardize
egen age_std = std(age)

* 2d. Categorical encoding (factor variables — use i. inside regressions)
* Explicit dummies only when needed for export
tab industry, gen(ind_)
drop ind_1                                        // base category

* 2e. Interactions & polynomials — use c. and i. inline in reg commands
gen age_sq = age^2
gen trt_x_edu = training * edu

* 2f. Panel operators (xtset is required for L./F./D. to work)
xtset worker_id year
gen log_wage_l1 = L.log_wage
gen log_wage_f1 = F.log_wage
gen d_log_wage  = D.log_wage

* 2g. Within-unit mean (egen)
egen wage_mean_i = mean(log_wage), by(worker_id)

* 2h. Treatment timing for staggered DID
bysort worker_id (year): egen first_treat = min(cond(training==1, year, .))
gen rel_time = year - first_treat
replace rel_time = . if missing(first_treat)      // never-treated = .
gen never_treated = missing(first_treat)

* 2i. Real values (CPI deflation)
merge m:1 year using "cpi.dta", keep(master match) nogen
sum cpi if year == 2010
gen wage_real = wage * r(mean) / cpi
```

---

### Step 2.5 — Empirical strategy (write the equation + identifying assumption)

This is the heart of an AER paper. **Before any code**, write down the equation explicitly and state the identifying assumption. Vague identification language is the single most common reason a referee rejects an applied paper. Persist the strategy as `strategy.do` (or `.md`) so it is a dated, version-controlled artifact — *not* a post-hoc rationalization written after seeing the coefficient.

#### Equation × identifying assumption × Stata estimator (decision table)

| Design | Estimating equation | Identifying assumption | Stata estimator |
|---|---|---|---|
| 2×2 DID | `Y_it = α_i + λ_t + β·D_it + X'γ + ε_it` | parallel trends conditional on X | `reghdfe Y c.D#c.post X, absorb(i t) vce(cluster i)` |
| Event-study (CS / SA) | `Y_it = α_i + λ_t + Σ_{e≠-1} β_e · 1{t-G_i = e} + ε_it` | no anticipation + group-time PT | `csdid` / `eventstudyinteract` / `did_imputation` |
| 2SLS | `Y_i = α + β·D_i + X'γ + ε_i;  D_i = π·Z_i + X'δ + u_i` | exclusion + relevance + monotonicity | `ivreg2` / `ivreghdfe` |
| Sharp RD | `Y_i = α + β·1{X_i ≥ c} + f(X_i) + ε_i` (local poly) | continuity of E[Y(0)\|X] at c, no manipulation | `rdrobust` (+ `rddensity`) |
| SCM | `Ŷ_1t(0) = Σ_j ŵ_j Y_jt`, τ_t = `Y_1t − Ŷ_1t(0)` for t≥T_0 | pre-period fit + interpolation validity | `synth` / `synth_runner` / `sdid` |
| Selection-on-observables (matching/IPW) | `E[Y_i(d) \| X_i] = E[Y_i \| D=d, X_i]` | unconfoundedness + overlap | `teffects psmatch / ipw / aipw / ipwra`, `ebalance` |

#### Design picker (when the user is unsure)

```
                 ┌─ running var + cutoff ───────────────── RDD       (rdrobust)
                 │
                 ├─ exogenous instrument Z ─────────────── IV/2SLS   (ivreg2 / ivreghdfe)
data + question ─┤
                 ├─ pre/post × treat/control ─┬ 2 periods  ── 2×2 DID (reghdfe / xtreg)
                 │                            └ staggered  ── CS / SA / BJS  (csdid / eventstudyinteract / did_imputation)
                 │
                 ├─ 1 treated unit + donor pool + long pre ── SCM    (synth / synth_runner / sdid)
                 │
                 ├─ high-dim X, selection-on-observables ── ML causal (ddml / crforest — see §B)
                 │
                 └─ none of the above ──────────────────── matching + sensitivity (teffects + evalue)
```

#### Pre-registration `strategy.do` template

```stata
*--- strategy.do — empirical-strategy pre-registration ---
* Frozen `c(current_date)' `c(current_time)'  (Git SHA: <paste>)
* Population:    manufacturing workers, 2010–2020, balanced panel
* Treatment:     training (binary, staggered adoption)
* Outcome:       log_wage (CPI-deflated 2010 USD)
* Estimand:      ATT on the treated, dynamic horizon -4..+4
*
* Estimating equation (paste from the §2.5 row that matches the design):
*   log_wage_it = α_i + λ_t + Σ_{e≠-1} β_e · 1{t - G_i = e} + ε_it
*
* Identifying assumption:
*   1. No anticipation:    E[Y_it(0) | t < G_i] = E[Y_it(0) | never-treated]
*   2. Group-time PT:      Δ E[Y_it(0)] is the same across treatment cohorts
*
* Auto-flagged threats (must defend in §2):
*   - Selection of G_i on Y_i(0)            -> bacondecomp + honestdid sensitivity
*   - Spillover across worker_id within firm -> cluster at firm_id, also try firm_id × year
*   - Anticipation in the year before adoption -> include lead in event study
*
* Fallback estimators (Step 6 robustness):
*   - eventstudyinteract  (Sun-Abraham 2021)
*   - did_imputation      (Borusyak-Jaravel-Spiess 2024)
*   - sdid                (Synthetic DID)
```

Commit `strategy.do` **before** running Step 5 / Step 6. The `git log` of this file *is* the analysis plan.

---

### Step 3 — Descriptive statistics & Table 1

Deeper patterns: [references/03-descriptive-stats.md](references/03-descriptive-stats.md) — stratified Table 1 with SMDs, `asdoc` / `tabstat` / `balancetable`, correlation matrix with significance stars (`pwcorr, sig star(.05)`), histograms / kdensity by group, `xtline` for DID motivation, panel-coverage `xtdescribe`.

```stata
* 3a. Full-sample summary
local vars "log_wage age edu tenure training"
tabstat `vars', statistics(n mean sd min p25 p50 p75 max) columns(statistics)

* One-command Word/Excel output:
asdoc sum `vars', stat(N mean sd min median max) ///
    save(tables/table1_full.docx) replace

* 3b. Stratified Table 1 (treated vs control + t-tests + SMDs)
balancetable training age edu tenure female ///
    using "tables/table1_balance.tex", ///
    vce(cluster firm_id) replace ///
    varlabels pval

* Manual per-variable t-test + SMD:
foreach v of varlist age edu tenure {
    qui sum `v' if training == 1
    local m1 = r(mean); local sd1 = r(sd); local n1 = r(N)
    qui sum `v' if training == 0
    local m0 = r(mean); local sd0 = r(sd); local n0 = r(N)
    local smd = (`m1' - `m0') / sqrt((`sd1'^2 + `sd0'^2)/2)
    ttest `v', by(training)
    display "`v': Δ=" %7.3f (`m1'-`m0') "  SMD=" %7.3f `smd' "  p=" %6.3f r(p)
}

* 3c. Correlation matrix with significance stars
pwcorr `vars', sig star(.05)
estout using "tables/corr.tex", replace ///
    cells("b(star fmt(3))") style(tex)        // alternative: estpost correlate

* 3d. Distribution plots
twoway (kdensity log_wage if training==1) ///
       (kdensity log_wage if training==0), ///
    legend(order(1 "Treated" 2 "Control")) ///
    title("Log wage density by treatment") ///
    saving(figures/kde_wage, replace)
graph export "figures/kde_wage.pdf", replace

* 3e. Time trends — the DID motivation plot
preserve
    collapse (mean) log_wage, by(year training)
    twoway (line log_wage year if training==1) ///
           (line log_wage year if training==0), ///
        xline(`policy_year', lpattern(dash)) ///
        legend(order(1 "Treated" 2 "Control"))
    graph export "figures/trend_did.pdf", replace
restore

* 3f. Panel coverage
xtdescribe
```

---

### Step 3.5 — Identification graphics (Section "Identification, graphical evidence")

**AER convention: the identification figure precedes the regression table.** The reader should see graphical evidence that PT holds / first stage is strong / RD jumps cleanly *before* you ask them to trust your point estimate. This block is one or two figures saved to `figures/` — most of the heavy lifting is one Stata command + one `coefplot`.

#### 3.5.1 Event-study figure + numerical pre-trends test (DID identification)

Pre-period coefficients ≈ 0 (with the −1 reference period normalized to zero) is the visual evidence for parallel trends. Pair the **figure** with a **numerical** pre-trends test so reviewers don't have to eyeball it.

```stata
* Build relative-time factor variable, base at e = -1
gen rel = year - first_treat
replace rel = . if missing(first_treat)        // never-treated dropped from event study
keep if inrange(rel, -4, 4) | missing(first_treat)
gen rel_p = rel + 5                             // shift -4..4 → 1..9; ib4 means "base = -1"

* (a) Sun-Abraham via -eventstudyinteract- (preferred for staggered adoption)
forvalues k = 1/9 {
    gen rel_d`k' = (rel_p == `k')
}
eventstudyinteract log_wage rel_d1 rel_d2 rel_d3 rel_d5 rel_d6 rel_d7 rel_d8 rel_d9, ///
    cohort(first_treat) control_cohort(never_treated) ///
    absorb(worker_id year) vce(cluster worker_id)

* (b) Coefficient figure with shaded CI + reference line at e=-1
coefplot, keep(rel_d*) vertical omitted ///
    yline(0, lpattern(dash) lcolor(gs10)) xline(4.5, lpattern(dash)) ///
    rename(rel_d1="-4" rel_d2="-3" rel_d3="-2" rel_d5="0" ///
           rel_d6="1" rel_d7="2" rel_d8="3" rel_d9="4") ///
    ciopts(recast(rcap)) levels(95) ///
    xtitle("Years relative to treatment") ///
    ytitle("Coefficient (ATT, 95% CI)") ///
    title("Figure 2a. Event-study coefficients (95% CI; ref. e = -1)") ///
    scheme(s2color)
graph export "figures/fig2a_event_study.pdf", replace
graph export "figures/fig2a_event_study.png", replace width(2400)

* (c) Numerical pre-trends F-test (joint zero on the leads e = -4..-2)
test rel_d1 rel_d2 rel_d3
display "Pre-trends F = " %5.2f r(F) "  p = " %5.3f r(p)

* (d) Bacon decomposition figure (Goodman-Bacon 2021) — TWFE diagnostic
bacondecomp log_wage training, ddetail
* The -bacondecomp- output names the contaminated 2×2 weights.
* Save the auto-generated figure as figures/fig2a_bacon.pdf.

* (e) Callaway-Sant'Anna dynamic ATT (when -csdid- is the main estimator)
csdid log_wage age edu, ivar(worker_id) time(year) gvar(first_treat) ///
    method(dripw) agg(event)
estat event, window(-4 4)
csdid_plot, title("Figure 2a-bis. Dynamic ATT (Callaway-Sant'Anna)")
graph export "figures/fig2a_csdid.pdf", replace
```

#### 3.5.2 First-stage F-statistic + scatter (IV identification)

Rule of thumb: first-stage F ≥ 10 for OLS-style inference; F ≥ 23 for AR-equivalent inference (Stock–Yogo / Lee 2022). `ivreg2` reports CD / KP / weak-IV statistics by default — far more useful than `ivregress`'s minimal output.

```stata
ivreg2 log_wage age edu (training = Z1 Z2), cluster(firm_id) first endog(training)
* Look for the line "Cragg-Donald Wald F" and "Kleibergen-Paap rk Wald F" —
* and "Anderson-Rubin Wald test" for weak-IV-robust CIs.

* First-stage scatter (binscatter — residualizes age + edu)
binscatter training Z1, controls(age edu) nquantiles(20) ///
    xtitle("Excluded instrument Z1") ytitle("Pr(training)") ///
    title("Figure 2b. First-stage relationship (residualized)") ///
    savegraph("figures/fig2b_first_stage.pdf") replace
```

#### 3.5.3 RD: McCrary density + canonical RD plot

The signature RD figure is `rdplot` (CCT-style binned scatter with local-polynomial fit on each side), paired with the McCrary manipulation test. Together they answer: (a) is there a visual jump? (b) is the density continuous at the cutoff?

```stata
* (a) Canonical RD plot
rdplot outcome running_var, c(0) p(4) kernel(triangular) binselect(esmv) ///
    graph_options(title("Figure 2c. RD plot") ///
                  ytitle("Outcome") xtitle("Running variable") ///
                  scheme(s2color))
graph export "figures/fig2c_rdplot.pdf", replace

* (b) McCrary density (manipulation test) — Cattaneo–Jansson–Ma 2018
rddensity running_var, c(0) plot ///
    plot_options(title("Figure 2c-bis. McCrary density (manipulation test)"))
graph export "figures/fig2c_mccrary.pdf", replace

* (c) Covariate-adjusted continuity test (continuity of *covariates* at c)
foreach v of varlist age edu tenure {
    rdrobust `v' running_var, c(0)
}
```

#### 3.5.4 Matching: love plot (standardized differences pre vs post)

```stata
teffects psmatch (log_wage) (training age edu tenure), atet
tebalance summarize           // table of pre/post SMDs
tebalance density ps          // density overlap plot — save as figures/fig2d_overlap.pdf
graph export "figures/fig2d_overlap.pdf", replace

* Or use -psmatch2- + -pstest- for the canonical love plot
psmatch2 training age edu tenure, out(log_wage) n(1) common
pstest age edu tenure, both graph                 // pre/post |std diff| with target |Δ|<10%
graph export "figures/fig2d_loveplot.pdf", replace
```

#### 3.5.5 SCM: synthetic-control trajectory + gap plot

For synthetic-control designs the canonical Figure 2 is the treated-vs-synthetic time series with treatment time annotated.

```stata
synth log_wage age edu tenure, ///
    trunit(1) trperiod(2015) fig keep("synth_results.dta", replace)
graph export "figures/fig2e_synth_trajectory.pdf", replace

* Synthetic DID variant
sdid log_wage worker_id year training, vce(bootstrap) graph g1on
graph export "figures/fig2e_sdid.pdf", replace

* Placebo gap distribution
synth_runner log_wage age edu tenure, ///
    trunit(1) trperiod(2015) gen_vars
effect_graphs, trlinediff(0)
graph export "figures/fig2e_placebo_gaps.pdf", replace
```

> Identification-specific checks (PT for DID, weak-IV F, density for RD, common support for matching) **are also auto-run inside the Step-5 estimators** — don't duplicate the numerics here, but DO produce the figures: a referee scans the figures first.

---

### Step 4 — Diagnostic statistical tests

Deeper patterns: [references/04-statistical-tests.md](references/04-statistical-tests.md) — Shapiro–Wilk, Jarque–Bera, Breusch–Pagan, White, Cook–Weisberg, Durbin–Watson, Breusch–Godfrey, Wooldridge `xtserial`, Pesaran CD, `xttest3`, VIF, `estat ovtest` (RESET), Augmented Dickey–Fuller, KPSS, Phillips–Perron, Hausman (FE vs RE), Sargan–Hansen, `estat firststage` (weak IV).

```stata
* Baseline OLS to anchor diagnostics
reg log_wage training age edu tenure

* 4a. Normality of residuals
predict resid, resid
swilk resid                                       // Shapiro–Wilk (N ≤ 5000)
sktest resid                                      // skewness + kurtosis test

* 4b. Heteroskedasticity
estat hettest                                     // Breusch–Pagan / Cook–Weisberg
estat imtest, white                               // White's general test

* 4c. Autocorrelation (panel)
xtset worker_id year
xtreg log_wage training age edu tenure, fe
xtserial log_wage training age edu tenure         // Wooldridge serial-correlation
xttest3                                           // modified Wald groupwise hetero

* 4d. Cross-sectional dependence (panel)
xtcsd, pesaran abs                                // Pesaran CD test

* 4e. Multicollinearity
quietly reg log_wage training age edu tenure
estat vif

* 4f. Model specification
estat ovtest                                      // Ramsey RESET
linktest                                          // Stata "linktest"

* 4g. Stationarity (time series)
dfuller log_wage, lags(4) trend                   // ADF
kpss    log_wage, maxlag(4) notrend               // KPSS
pperron log_wage, lags(4)                         // Phillips–Perron

* 4h. Panel unit root (multiple series)
xtunitroot ips log_wage, lags(aic 4)              // Im–Pesaran–Shin
xtunitroot llc log_wage, lags(aic 4)              // Levin–Lin–Chu

* 4i. Hausman (after running FE and RE)
qui xtreg log_wage training age edu, fe
estimates store fe
qui xtreg log_wage training age edu, re
estimates store re
hausman fe re, sigmamore
```

**Decision table**:

| Test | Null | If rejected |
|------|------|-------------|
| `swilk` / `sktest` | residuals Normal | large N: usually ignore; small N: bootstrap |
| `estat hettest` / `imtest, white` | homoskedastic | use `vce(robust)` or `vce(cluster id)` |
| `xtserial` / `xttest3` | no panel autocorr / no groupwise hetero | cluster by unit |
| `xtcsd, pesaran` | no cross-sectional dependence | Driscoll–Kraay or `xtscc` |
| `estat vif` > 10 | — | drop/combine collinear regressors |
| `estat ovtest` | specification OK | add polynomials / logs |
| `dfuller` reject + `kpss` fail to reject | stationary | keep levels |
| `dfuller` fail to reject | unit root | first-difference or cointegrate |
| `hausman` | RE consistent | use FE |

---

### Step 5 — Baseline empirical modeling (Section 4: Main Results)

Deeper patterns: [references/05-modeling.md](references/05-modeling.md) — every classical estimator with syntax: `reg`, `areg`, `xtreg`, `reghdfe`, `ivreg2` / `ivregress` / `ivreghdfe`, `logit` / `probit` / `ppmlhdfe`, `csdid` / `did_imputation` / `eventstudyinteract` / `sdid` / `did_multiplegt_dyn`, `rdrobust` / `rddensity` / `rdmc`, `synth` / `synth_runner`, `psmatch2` / `teffects psmatch|ipw|ipwra|aipw`, `ebalance`, `heckman`, `qreg`.

This is the densest section of an applied paper. A modern AER §4 typically contains **2–3 multi-regression tables and one coefficient plot**:

- **Table 2** (main): progressive controls, 4–6 columns — **Pattern A** below
- **Table 2-bis** (design horse race): same coefficient under OLS / IV / DID / matching — **Pattern B**
- **Table 2-ter** (multi-outcome): same treatment, several outcomes side-by-side — **Pattern C**
- **Figure 3** (coefplot): visual summary of β̂ and 95% CI across specs

> **Estimator routing** (memorize this — getting it wrong silently produces nonsense):
> - **No FE / single low-card FE** → `reg y x1 x2, vce(cluster id)`
> - **High-dim FE** → `reghdfe y x1 x2, absorb(fe1 fe2) vce(cluster id)`
> - **Two-way cluster** → `reghdfe ..., vce(cluster fe1 fe2)`
> - **2SLS / IV** → `ivreg2 y x (D = Z), cluster(id) first endog(D)` (or `ivreghdfe` for HD FE + IV)
> - **DID / event-study** → `csdid` / `eventstudyinteract` / `did_imputation`

**Pick the estimator by identification strategy**:

```
Observational cross-section, selection on obs  →  reg + controls  |  teffects psmatch|ipwra
Observational panel, policy shock, parallel trends → csdid / did_imputation / eventstudyinteract / sdid
Exogenous instrument                           →  ivreg2 / ivregress / ivreghdfe
Discontinuity in assignment rule               →  rdrobust (+ rddensity)
N=1 treated, long panel                        →  synth / synth_runner
Selection on observables + heterogeneity       →  teffects aipw / ebalance
Binary outcome                                 →  logit / probit + margins
Count outcome                                  →  poisson / nbreg / ppmlhdfe
```

Canonical commands (a Stata equivalent of `outreg2` / `esttab` is the workhorse — `eststo` 5–6 specs, then `esttab` consolidates them into one table). Key options:

```
keep(...)        : list of coefficients to display (e.g. keep(training))
drop(...)        : list of coefficients to suppress (controls / intercept)
mtitles("(1)" "(2)" ...) : column labels for the regression table
stats(N r2 r2_a, labels(...))      : footer rows
star(* 0.10 ** 0.05 *** 0.01)      : AER stars
addnotes("...")  : table footer (cluster level, FE absorbed, sample restrictions)
label  booktabs  : pretty-print + LaTeX booktabs borders
```

#### 5.A Pattern A — Progressive controls (the canonical Table 2)
Stable β̂ across columns ⇒ less concern that selection on observables is driving the estimate (Oster 2019 selection-stability logic; quantified in Step 6.j). **`eststo m1...m6` + `esttab` is the Stata equivalent of `outreg2` and R's `modelsummary`.**

```stata
eststo clear
eststo m1: qui reg     log_wage training,                                                  vce(cluster firm_id)
eststo m2: qui reg     log_wage training age edu,                                          vce(cluster firm_id)
eststo m3: qui reg     log_wage training age edu tenure firm_size,                         vce(cluster firm_id)
eststo m4: qui reghdfe log_wage training age edu tenure firm_size,  absorb(industry year)  vce(cluster firm_id)
eststo m5: qui reghdfe log_wage training age edu tenure firm_size,  absorb(worker_id year) vce(cluster firm_id)
eststo m6: qui reghdfe log_wage training age edu tenure firm_size,  absorb(worker_id year i.industry#i.year) vce(cluster firm_id)

esttab m1 m2 m3 m4 m5 m6 using "tables/table2_main.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    mtitles("(1) Baseline" "(2) +Demog" "(3) +Labor-mkt" "(4) Ind×Yr FE" "(5) Worker FE" "(6) Ind×Yr × Worker FE") ///
    stats(N r2 r2_a, labels("N" "R²" "Adj. R²")) ///
    addnotes("Cluster-robust SE at firm_id in parentheses." ///
             "* p<0.10, ** p<0.05, *** p<0.01.")
* Word version: same call with .rtf extension.
```

> **AER convention: show all controls — pass NEITHER `keep()` NOR `drop()`** so every parameter is visible. Use `keep(training)` only when a focal-coefficient-only table is intentional (e.g. interaction-form heterogeneity, IV first-stage triplet); use `drop(_cons)` only when you want to suppress the constant for paper aesthetics.

#### 5.B Pattern B — Design horse race (Table 2-bis)
Show the same coefficient of interest under multiple identification strategies. This is *the* AER credibility move: convergent evidence across designs each making different identifying assumptions.

```stata
eststo clear
eststo ols:  qui reghdfe log_wage training age edu tenure, absorb(industry year) vce(cluster firm_id)
eststo iv:   qui ivreg2  log_wage age edu tenure (training = Z1 Z2), cluster(firm_id)
eststo did:  qui csdid   log_wage age edu tenure, ivar(worker_id) time(year) gvar(first_treat) method(dripw) agg(group)
eststo psm:  qui teffects psmatch (log_wage) (training age edu tenure), atet
eststo ebal: qui ebalance training age edu tenure
              qui reg     log_wage training age edu tenure [pw=_webal], vce(cluster firm_id)
              eststo ebal_main

esttab ols iv did psm ebal_main using "tables/table2b_designs.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    keep(training) ///
    mtitles("(1) OLS+FE" "(2) 2SLS" "(3) CS-DID" "(4) PSM" "(5) Entropy bal.") ///
    stats(N, labels("N")) ///
    addnotes("Convergent evidence: same β̂ under five identification strategies.")
```

#### 5.C Pattern C — Multi-outcome table (same X, several Y's)
A single treatment, several outcomes. Use `mtitles` so each column carries the Y name.

```stata
eststo clear
foreach y of varlist log_wage weeks_employed left_firm promoted {
    eststo `y': qui reghdfe `y' training age edu tenure, ///
        absorb(industry year) vce(cluster firm_id)
}
esttab log_wage weeks_employed left_firm promoted using "tables/table2c_multi_outcome.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    keep(training) ///
    mtitles("Log wage" "Weeks empl." "Left firm" "Promoted") ///
    stats(N r2, labels("N" "R²")) ///
    addnotes("Each column is a separate regression on the labelled outcome.")
```

#### 5.D Pattern D — Stacked Panel A / Panel B table
Same model family, two horizons (short-run / long-run) or two samples (pre-2015 / post-2015). Stack vertically with two `esttab` calls + `texdoc` glue, OR use `esttab ..., refcat()` to inject panel headers.

```stata
* Panel A — short-run (1 year horizon)
eststo clear
eststo a1: qui reghdfe log_wage_t1 training X, absorb(industry year)  vce(cluster firm_id)
eststo a2: qui reghdfe log_wage_t1 training X, absorb(worker_id year) vce(cluster firm_id)

* Panel B — long-run (5 year horizon)
eststo b1: qui reghdfe log_wage_t5 training X, absorb(industry year)  vce(cluster firm_id)
eststo b2: qui reghdfe log_wage_t5 training X, absorb(worker_id year) vce(cluster firm_id)

* First panel — write
esttab a1 a2 using "tables/table2d_horizons.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    keep(training) mtitles("(1) Industry FE" "(2) Worker FE") ///
    refcat(training "\textbf{Panel A. Short-run (1 year)}", nolabel) ///
    stats(N r2, labels("N" "R²"))
* Second panel — append
esttab b1 b2 using "tables/table2d_horizons.tex", append ///
    se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    keep(training) mtitles("(1) Industry FE" "(2) Worker FE") ///
    refcat(training "\textbf{Panel B. Long-run (5 years)}", nolabel) ///
    stats(N r2, labels("N" "R²"))
```

#### 5.E Pattern E — IV reporting triplet (first-stage / reduced-form / 2SLS)
The textbook AER IV table presents the **first stage**, the **reduced form**, and the **2SLS** in three columns so the reader can verify Wald-ratio = RF / FS.

```stata
eststo clear
eststo fs: qui reghdfe training Z age edu, absorb(industry year) vce(cluster firm_id)  // first stage
eststo rf: qui reghdfe log_wage Z age edu, absorb(industry year) vce(cluster firm_id)  // reduced form
eststo iv: qui ivreghdfe log_wage age edu (training = Z), absorb(industry year) cluster(firm_id) first

esttab fs rf iv using "tables/table2e_iv_triplet.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    keep(Z training) ///
    mtitles("(1) First stage" "(2) Reduced form" "(3) 2SLS") ///
    stats(N r2 widstat, labels("N" "R²" "First-stage F (KP)")) ///
    addnotes("Wald ratio: $\hat\beta_{2SLS} = \hat\beta_{RF} / \hat\pi_{FS}$.")
```

> **IV triplet is intentionally focal:** show only Z + endogenous regressor so the reader can eyeball the Wald ratio. Drop `keep(Z training)` only if a referee asks for the full coefficient list.

#### 5.F Pattern F — Causal-orchestrator main via `csdid` / `synth_runner` / `teffects`
For DID / SCM / matching mains, the modern Stata estimator returns a self-contained estimate + automatic placebos / pre-trends / overlap diagnostics. Use the estimator's own report, then pipe into `eststo` + `esttab`.

```stata
* CS-DID with pre-trends test
csdid log_wage age edu tenure, ivar(worker_id) time(year) gvar(first_treat) ///
    method(dripw) agg(group) saverif(csdid_rif.dta)
estat pretrend                                                       // joint zero on pre-period leads
estat simple                                                          // ATT(g) summary
estat event, window(-4 4)                                            // dynamic ATT
csdid_estat aggte, type(group) saverif(att_g.dta)
eststo m_csdid

* Synth-runner with 50 placebo treated units → exact p-value on β̂_treated
synth_runner log_wage age edu tenure, trunit(1) trperiod(2015) gen_vars
single_treatment_graphs, do_color(red)
effect_graphs, trlinediff(0)
* Reports exact p-value from the placebo distribution.

* Teffects AIPW with overlap + balance check
teffects aipw (log_wage age edu tenure) (training age edu tenure)
tebalance summarize
eststo m_aipw
```

#### 5.G Pattern G — Subgroup `esttab` (Table 3, see Step 7)
One column per subgroup. Detailed code in §Step 7 — Heterogeneity.

#### 5.H Pattern H — Robustness master (Table A1, see Step 6)
Stack every robustness specification next to the baseline. Detailed code in §Step 6 — Robustness master.

---

#### Canonical estimator commands (the underlying primitives)

```stata
* 5a. OLS with cluster-robust SE
reg log_wage training age edu tenure, vce(cluster firm_id)
eststo ols_m1

* 5b. Two-way FE — reach for reghdfe (absorb HD FE; clusters any level)
reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster worker_id)
eststo fe_m1

* Multi-way clustering
reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster worker_id firm_id)

* High-dim FE (industry × year, firm × state)
reghdfe log_wage training, absorb(worker_id i.industry#i.year) ///
    vce(cluster firm_id)

* 5c. 2×2 DID
reg log_wage i.treated##i.post age edu, vce(cluster worker_id)

* Or with absorbed FE:
reghdfe log_wage c.treated#c.post, absorb(worker_id year) ///
    vce(cluster worker_id)

* 5d. Event study (dynamic DID, base period = -1)
* Build relative-time factor var, base at k = -1:
gen rel = rel_time + 10                          // shift so -10..10 → 0..20
replace rel = 0 if missing(rel_time)             // never-treated → bin 0
* (preferable: use -eventstudyinteract- or -did_imputation- — see reference 5.4)
reghdfe log_wage ib9.rel, absorb(worker_id year) vce(cluster worker_id)
coefplot, keep(*.rel) vertical omitted ///
    yline(0) xline(9.5, lpattern(dash)) ///
    xtitle("Years relative to treatment") ytitle("Coefficient (ATT)")
graph export "figures/event_study.pdf", replace

* 5e. Staggered DID — modern estimators (see references/05-modeling.md §5.4)
* Callaway–Sant'Anna (2021):
csdid log_wage, ivar(worker_id) time(year) gvar(first_treat) ///
    method(dripw) agg(group)

* Sun & Abraham (2021):
eventstudyinteract log_wage rel_dummies_*, ///
    cohort(first_treat) control_cohort(never_treated) ///
    absorb(worker_id year) vce(cluster worker_id)

* Borusyak–Jaravel–Spiess (2024) imputation:
did_imputation log_wage worker_id year first_treat, ///
    allhorizons pretrend(5)

* Synthetic DID (Arkhangelsky et al. 2021):
sdid log_wage worker_id year training, vce(bootstrap) ///
    graph g1on g1_opt(ytitle("log wage"))

* 5f. IV / 2SLS — ivreg2 is the de-facto standard (full diagnostics)
ivreg2 log_wage age edu (training = draft_lottery), ///
    cluster(firm_id) first endog(training)

* ivreghdfe for HD FE with IV:
ivreghdfe log_wage age (training = draft_lottery), ///
    absorb(worker_id year) cluster(worker_id) first

* 5g. Sharp RD
rdrobust outcome running_var, c(0) kernel(triangular) bwselect(mserd)
rdplot   outcome running_var, c(0)

* Fuzzy RD
rdrobust outcome running_var, c(0) fuzzy(treatment)

* Density test (McCrary / Cattaneo et al.)
rddensity running_var, c(0)

* 5h. Binary outcome — always follow with margins
logit employed training age edu, vce(cluster firm_id)
margins, dydx(training) atmeans

* 5i. Count outcome with HD FE
ppmlhdfe citations training age, absorb(firm_id year) ///
    cluster(firm_id)

* 5j. Quantile regression
qreg log_wage training age edu, quantile(0.5)
sqreg log_wage training age edu, quantile(0.1 0.25 0.5 0.75 0.9) reps(500)
```

---

### Step 6 — Robustness battery

Deeper patterns: [references/06-robustness.md](references/06-robustness.md) — progressive specs M1–M6 with `eststo` / `esttab`, `bacondecomp` for TWFE bias, `honestdid` (Rambachan–Roth), `boottest` wild-cluster bootstrap, `ritest` randomization inference, `rwolf` Romano–Wolf, alternative cluster levels, Oster δ*, placebo timing, subsample splits, specification curve via loops.

```stata
* 6a. Progressive specifications (M1 → M6)
eststo clear
eststo m1: qui reg    log_wage training, vce(cluster firm_id)
eststo m2: qui reg    log_wage training age edu, vce(cluster firm_id)
eststo m3: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id) vce(cluster worker_id)
eststo m4: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster worker_id)
eststo m5: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year region) vce(cluster worker_id)
eststo m6: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year i.industry#i.year) vce(cluster worker_id)
esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_a, labels("N" "R²" "Adj. R²")) ///
    label booktabs

* 6b. Alternative cluster levels
foreach c in worker_id firm_id industry state {
    qui reghdfe log_wage training, absorb(worker_id year) vce(cluster `c')
    display "cluster=`c'  b=" _b[training] "  se=" _se[training]
}

* 6c. Wild cluster bootstrap (few clusters)
qui reghdfe log_wage training, absorb(worker_id year) vce(cluster state)
boottest training, cluster(state) reps(9999) seed(42)

* 6d. Subsample splits
foreach mask in "female==0" "female==1" "age<40" "age>=40" {
    qui reghdfe log_wage training if `mask', ///
        absorb(worker_id year) vce(cluster worker_id)
    display "`mask': b=" _b[training] "  se=" _se[training] "  N=" e(N)
}

* 6e. Placebo timing
gen fake_first = first_treat - 3
gen fake_post  = (year >= fake_first)
preserve
    keep if year < first_treat                       // drop real post-period
    reghdfe log_wage fake_post, absorb(worker_id year) ///
        vce(cluster worker_id)
restore

* 6f. Randomization inference (permutation)
ritest training _b[training], reps(1000) seed(0) ///
    strata(worker_id): reghdfe log_wage training, ///
    absorb(worker_id year) vce(cluster worker_id)

* 6g. Romano–Wolf multiple testing
rwolf log_wage employed hours_worked, indepvar(training) ///
    controls(age edu) reps(500) seed(42) method(reghdfe) ///
    fe(worker_id year) cluster(worker_id)

* 6h. TWFE bias diagnosis — Goodman-Bacon decomposition
bacondecomp log_wage training, ddetail

* 6i. Parallel trends sensitivity — HonestDiD
* (after running the event study and saving b/V)
honestdid, pre(1/4) post(5/9) mvec(0(0.1)0.5)

* 6j. Oster (2019) δ*
qui reg log_wage training                             // short
scalar bs = _b[training]; scalar r2s = e(r2)
qui reghdfe log_wage training age edu tenure, absorb(worker_id year)
scalar bl = _b[training]; scalar r2l = e(r2)
psacalc delta training, mcontrol(age edu tenure) rmax(1.3*r2l)
```

#### 6.k Pattern H — Robustness master table (Table A1, one column per check)

The canonical AER appendix Table A1 stacks every robustness specification next to the baseline so reviewers see at a glance that β̂ survives. Build the list of `eststo` results dynamically:

```stata
eststo clear

* (1) Baseline
eststo base: qui reghdfe log_wage training age edu tenure, ///
    absorb(industry year) vce(cluster firm_id)

* (2) Drop top 1% of wage
qui sum wage, detail
eststo no99: qui reghdfe log_wage training age edu tenure if wage < r(p99), ///
    absorb(industry year) vce(cluster firm_id)

* (3) Balanced panel only
preserve
    keep if e(sample)                                      // start from baseline sample
    bysort worker_id: egen n_obs = count(year)
    qui sum n_obs, detail
    keep if n_obs == r(max)
    eststo balpan: qui reghdfe log_wage training age edu tenure, ///
        absorb(industry year) vce(cluster firm_id)
restore

* (4) Drop early adopting cohorts
eststo dropearly: qui reghdfe log_wage training age edu tenure if first_treat > 2008, ///
    absorb(industry year) vce(cluster firm_id)

* (5) Worker FE absorbed (selection on FE-removable unobservables)
eststo wfe: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster firm_id)

* (6) Two-way cluster (firm × year)
eststo cl2way: qui reghdfe log_wage training age edu tenure, ///
    absorb(industry year) vce(cluster firm_id year)

* (7) Wild cluster bootstrap (after running the baseline)
qui reghdfe log_wage training age edu tenure, absorb(industry year) vce(cluster firm_id)
boottest training, cluster(firm_id) reps(9999) seed(42) nograph                  // returns CI
* Note bootstrapped p-value in the row footer of the master table.

* (8) Log outcome
eststo logy: qui reghdfe log_log_wage training age edu tenure, ///
    absorb(industry year) vce(cluster firm_id)

* (9) IHS outcome (handles zeros)
gen ihs_wage = asinh(wage)
eststo ihsy: qui reghdfe ihs_wage training age edu tenure, ///
    absorb(industry year) vce(cluster firm_id)

* (10) PSM-weighted outcome
qui psmatch2 training age edu tenure, out(log_wage) n(1) common
eststo psm: qui reg log_wage training age edu tenure if _support == 1, vce(cluster firm_id)

* (11) Entropy balance
ebalance training age edu tenure
eststo ebal: qui reg log_wage training age edu tenure [pw=_webal], vce(cluster firm_id)

esttab base no99 balpan dropearly wfe cl2way logy ihsy psm ebal ///
    using "tables/tableA1_robustness.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    keep(training) ///
    mtitles("(1) Baseline" "(2) Drop top 1%" "(3) Balanced" "(4) Drop early" ///
            "(5) Worker FE" "(6) 2-way cluster" "(7) log Y" "(8) IHS Y" ///
            "(9) PSM" "(10) Entropy bal.") ///
    stats(N r2, labels("N" "R²")) ///
    addnotes("Each column is one robustness check. β̂ on training is the focal coefficient.")
```

#### 6.l Specification curve (Simonsohn–Simmons–Nelson 2020) in Stata

`esttab` doesn't have a native spec-curve; loop over {controls × samples × outcome transforms × SE types}, store each β̂ + 95% CI in a frame, then plot.

```stata
capture frame drop spec
frame create spec spec_id b se lo hi label
local id 0
foreach controls in "age" "age edu" "age edu tenure" "age edu tenure firm_size" {
    foreach trans in "log_wage" "ihs_wage" {                         // outcome transforms
        foreach mask in "1" "industry==\"manuf\"" "wage < r(p99)" {  // subsamples
            foreach cl in "firm_id" "firm_id year" {                  // SE types
                qui reghdfe `trans' training `controls' if `mask', ///
                    absorb(industry year) vce(cluster `cl')
                local ++id
                local b = _b[training]
                local se = _se[training]
                local lo = `b' - 1.96*`se'
                local hi = `b' + 1.96*`se'
                frame post spec (`id') (`b') (`se') (`lo') (`hi') ("c=`controls'/y=`trans'/s=`mask'/cl=`cl'")
            }
        }
    }
}
frame change spec
sort b
gen rank = _n
twoway (rcap lo hi rank) (scatter b rank), ///
    yline(0, lpattern(dash) lcolor(gs10)) ///
    xtitle("Specification (sorted by β̂)") ytitle("Coefficient on training") ///
    title("Figure 5. Specification curve") ///
    legend(off) scheme(s2color)
graph export "figures/fig5_spec_curve.pdf", replace
graph export "figures/fig5_spec_curve.png", replace width(2400)
frame change default
```

A modern AER referee letter often asks "what about specification X?" — the spec curve answers all such asks at once.

#### 6.m Sensitivity dashboard (HonestDiD + Oster + E-value, one block)

For DID main results, produce one figure (`HonestDiD` partial-identification bound) + one row of sensitivity stats (Oster δ + E-value).

```stata
* (a) HonestDiD — Rambachan-Roth (2023) bound on β̂ under bounded PT violation
* Re-run the event study and store b/V:
qui eventstudyinteract log_wage rel_d1-rel_d9, ///
    cohort(first_treat) control_cohort(never_treated) ///
    absorb(worker_id year) vce(cluster worker_id)
honestdid, pre(rel_d1 rel_d2 rel_d3) post(rel_d5 rel_d6 rel_d7 rel_d8 rel_d9) ///
    mvec(0(0.1)0.5) coefplot
graph export "figures/fig6_honestdid.pdf", replace

* (b) Oster δ (Pattern: how big would selection on unobservables have to be?)
qui psacalc delta training, mcontrol(age edu tenure firm_size) rmax(1.3)
display "Oster δ for β=0: " r(delta)

* (c) E-value (Linden-Mathur 2020) — for binary / risk-ratio outcomes
* Convert OLS coefficient to risk-ratio scale first if applicable.
evalue rr, est(1.45) lcl(1.10) ucl(1.91)
* → reports the minimum strength of unmeasured confounding to nullify the result.
```

---

### Step 7 — Further analysis (mechanism / heterogeneity / mediation / moderation)

Deeper patterns: [references/07-further-analysis.md](references/07-further-analysis.md) — factor-variable interactions, `margins` / `marginsplot`, triple-difference (DDD), outcome ladder, `medsem` / Baron–Kenny, `khb` (Karlson–Holm–Breen) for non-linear mediation, dose-response via `xtile` or splines, subgroup event studies.

```stata
* 7a. Heterogeneity via interaction — coefficient IS the heterogeneity test
reghdfe log_wage c.training##i.female age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
margins, dydx(training) at(female=(0 1))
marginsplot, title("Marginal effect of training by gender") ///
    ytitle("dY/d(training)")
graph export "figures/het_female.pdf", replace

* Continuous moderator
reghdfe log_wage c.training##c.tenure age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
margins, dydx(training) at(tenure=(0(2)20))
marginsplot

* 7b. Subgroup estimation + Wald test of equality
eststo clear
eststo m_male:   qui reghdfe log_wage training if female==0, ///
    absorb(worker_id year) vce(cluster worker_id)
eststo m_female: qui reghdfe log_wage training if female==1, ///
    absorb(worker_id year) vce(cluster worker_id)
suest m_male m_female                                  // joint covariance
test [m_male_mean]training = [m_female_mean]training  // Wald test

* 7c. Triple difference (DDD)
reghdfe log_wage c.treated##c.post##c.high_exposure, ///
    absorb(worker_id year) vce(cluster firm_id)
* coefficient on treated#post#high_exposure IS the differential DID

* 7d. Outcome ladder
eststo clear
foreach y of varlist hours_worked productivity log_wage {
    eststo: qui reghdfe `y' training, ///
        absorb(worker_id year) vce(cluster worker_id)
}
esttab using "tables/mechanism_ladder.tex", replace ///
    se label booktabs

* 7e. Mediation — Baron–Kenny (manual)
qui reghdfe log_wage training age edu, absorb(worker_id year)
scalar c = _b[training]
qui reghdfe hours_worked training age edu, absorb(worker_id year)
scalar a = _b[training]
qui reghdfe log_wage training hours_worked age edu, absorb(worker_id year)
scalar b_m   = _b[hours_worked]
scalar cprim = _b[training]
display "Total = " c "  Direct = " cprim "  Indirect a*b = " a*b_m

* Or via -medsem- (for SEM-based mediation with bootstrap CI)
medsem, indep(training) med(hours_worked) dep(log_wage) ///
    mcreps(1000)

* 7f. CATE via Nonparametric (grf) — typically fall back to Python econml
* See references/07-further-analysis.md §7.7 for the rpy2-style bridge.

* 7g. Dose-response (continuous treatment, decile bins)
xtile dose10 = training_hours, nq(10)
reghdfe log_wage i.dose10 age edu, absorb(worker_id year) vce(cluster worker_id)
margins i.dose10
marginsplot, recast(connected) ytitle("Predicted log wage") ///
    xtitle("Training-hours decile")
graph export "figures/dose_response.pdf", replace
```

---

### Step 8 — Publication tables & figures

> **This step is mandatory** — every analysis run produces all 5 required tables (T1–T5) and all 4 required figures (F1–F4) defined in the *Default Output Spec* at the top of this skill. Do not skip Step 8 because "the regression already ran". A coefficient without a table and a figure is not how applied economics communicates a result.

Deeper patterns: [references/08-tables-plots.md](references/08-tables-plots.md) — `esttab` and `outreg2` for regression tables; `coefplot` for coefficient plots, event studies, forest plots; `marginsplot` for interactions; `binscatter` for residualized scatter; `rdplot` for RD; `twoway` + combined graphs; Stata scheme / graph options; LaTeX / Word / Excel export.

```stata
* ============================================================
* 8a. ★ TABLE 2 — Main results, multi-column regression M1→M6
*     (the centerpiece of every economics paper)
* ============================================================
esttab m1 m2 m3 m4 m5 m6 using "tables/table2_main.tex", ///
    replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_a fe_worker fe_year fe_indyr, ///
        labels("N" "R²" "Adj. R²" "Worker FE" "Year FE" "Industry×Year FE")) ///
    keep(training age edu tenure) ///
    order(training age edu tenure) ///
    mtitles("(1) Raw" "(2) +Demog" "(3) +Tenure" "(4) +Unit FE" "(5) +2-way FE" "(6) +Ind×Yr FE") ///
    label booktabs nonumbers noobs ///
    addnotes("Cluster-robust standard errors at worker_id level in parentheses." ///
             "* p<0.10, ** p<0.05, *** p<0.01.")

* Word version
esttab m1 m2 m3 m4 m5 m6 using "tables/table2_main.rtf", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) label ///
    mtitles("(1)" "(2)" "(3)" "(4)" "(5)" "(6)")

* outreg2 — alternative (one-line, broad compatibility)
* reghdfe log_wage training age edu tenure, absorb(worker_id year)
* outreg2 using "tables/table2_main_outreg2.doc", replace label dec(3) ///
*     addtext(Worker FE, YES, Year FE, YES)

* ============================================================
* 8b. TABLE 1 — Summary statistics & balance
* ============================================================
balancetable training age edu tenure female ///
    using "tables/table1_balance.tex", ///
    vce(cluster firm_id) replace ///
    varlabels pval booktabs

asdoc sum log_wage training age edu tenure female, ///
    by(training) stat(N mean sd min median max) ///
    save(tables/table1_balance.rtf) replace

* ============================================================
* 8c. TABLE 3 — Mechanism / outcome ladder (3+ outcomes)
* ============================================================
eststo clear
foreach y of varlist hours_worked productivity log_wage {
    eststo: qui reghdfe `y' training age edu tenure, ///
        absorb(worker_id year) vce(cluster worker_id)
}
esttab using "tables/table3_mechanism.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    mtitles("Hours worked" "Productivity" "Log wage") ///
    keep(training) ///
    addnotes("Each column is a separate regression of the labelled outcome on training," ///
             "with worker and year FE and cluster-robust SE at worker_id.")

* ============================================================
* 8d. TABLE 4 — Heterogeneity (subgroup × main coef + Wald)
* ============================================================
eststo clear
eststo all:    qui reghdfe log_wage training,                                   ///
    absorb(worker_id year) vce(cluster worker_id)
eststo male:   qui reghdfe log_wage training if female==0,                       ///
    absorb(worker_id year) vce(cluster worker_id)
eststo female: qui reghdfe log_wage training if female==1,                       ///
    absorb(worker_id year) vce(cluster worker_id)
eststo young:  qui reghdfe log_wage training if age<40,                          ///
    absorb(worker_id year) vce(cluster worker_id)
eststo old:    qui reghdfe log_wage training if age>=40,                         ///
    absorb(worker_id year) vce(cluster worker_id)
eststo manuf:  qui reghdfe log_wage training if industry=="manufacturing",       ///
    absorb(worker_id year) vce(cluster worker_id)
esttab all male female young old manuf using "tables/table4_heterogeneity.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    mtitles("All" "Female=0" "Female=1" "Age<40" "Age≥40" "Manuf.") ///
    keep(training) ///
    addnotes("Cluster-robust SE at worker_id. Wald p-values for cross-subgroup equality" ///
             "(via -suest-) should accompany this table — see references/07.")

* ============================================================
* 8e. TABLE 5 — Robustness battery (alt SE / cluster / sample / placebo)
* ============================================================
eststo clear
eststo base:    qui reghdfe log_wage training, absorb(worker_id year) vce(cluster worker_id)
eststo cl_firm: qui reghdfe log_wage training, absorb(worker_id year) vce(cluster firm_id)
eststo cl_2way: qui reghdfe log_wage training, absorb(worker_id year) vce(cluster worker_id firm_id)
eststo wins:    qui reghdfe log_wage_w1 training, absorb(worker_id year) vce(cluster worker_id)
eststo dropmf:  qui reghdfe log_wage training if industry!="manufacturing", ///
    absorb(worker_id year) vce(cluster worker_id)
eststo placebo: qui reghdfe log_wage fake_post if year < first_treat, ///
    absorb(worker_id year) vce(cluster worker_id)
esttab base cl_firm cl_2way wins dropmf placebo using "tables/table5_robustness.tex", ///
    replace se star(* 0.10 ** 0.05 *** 0.01) label booktabs ///
    mtitles("Baseline" "Cluster=Firm" "2-way Cluster" "Winsor 1/99" "Drop Manuf." "Placebo (-3 yr)") ///
    keep(training fake_post)

* ============================================================
* 8f. ★ FIGURE 3 — Coefficient plot across M1→M6
* ============================================================
coefplot m1 m2 m3 m4 m5 m6, keep(training) ///
    vertical yline(0, lpattern(dash)) ///
    ciopts(recast(rcap)) ///
    levels(95) ///
    ylabel(, angle(0)) ///
    xtitle("Specification") ytitle("Coefficient on training (95% CI)") ///
    title("Effect of training across specifications") ///
    scheme(s2color)
graph export "figures/fig3_coefplot.pdf", replace
graph export "figures/fig3_coefplot.png", replace width(2400)

* ============================================================
* 8g. FIGURE 2 — Event-study plot (dynamic DID, base period = -1)
* ============================================================
* (after running -eventstudyinteract- or -csdid- or reghdfe with relative-time factor)
coefplot, keep(*.rel) vertical omitted ///
    xline(9.5, lpattern(dash)) yline(0, lpattern(dash)) ///
    xtitle("Years relative to treatment") ///
    ytitle("Coefficient (ATT, 95% CI)") ///
    title("Event study: dynamic effect of training") ///
    ciopts(recast(rcap)) ///
    scheme(s2color)
graph export "figures/fig2_event_study.pdf", replace
graph export "figures/fig2_event_study.png", replace width(2400)

* ============================================================
* 8h. FIGURE 4 — Sensitivity / robustness curve
*     (HonestDiD post-DID; or forest plot of robustness battery)
* ============================================================
* HonestDiD sensitivity (after the event study with stored b/V):
honestdid, pre(1/4) post(5/9) mvec(0(0.1)0.5) coefplot
graph export "figures/fig4_sensitivity.pdf", replace
graph export "figures/fig4_sensitivity.png", replace width(2400)

* Alternative: forest plot of subgroup / robustness coefficients
* coefplot (all, label(All)) (male, label(Male)) (female, label(Female)) ///
*          (young, label(Age<40)) (old, label(Age≥40)) (manuf, label(Manuf.)), ///
*     keep(training) xline(0, lpattern(dash)) ciopts(recast(rcap)) ///
*     title("Heterogeneity forest plot")
* graph export "figures/fig4_forest.pdf", replace

* ============================================================
* 8i. FIGURE 1 — Trend / motivation (treated vs control over time)
* ============================================================
preserve
    collapse (mean) log_wage, by(year training)
    twoway (line log_wage year if training==1, lcolor(navy) lwidth(medthick)) ///
           (line log_wage year if training==0, lcolor(cranberry) lwidth(medthick)), ///
        xline(`policy_year', lpattern(dash) lcolor(gs8)) ///
        legend(order(1 "Treated" 2 "Control") rows(1) position(6)) ///
        xtitle("Year") ytitle("Mean log wage") ///
        title("Treated vs control trend") ///
        scheme(s2color)
    graph export "figures/fig1_trend.pdf", replace
    graph export "figures/fig1_trend.png", replace width(2400)
restore

* ============================================================
* 8j. Auxiliary plots (optional — produce when relevant to design)
* ============================================================
* Binscatter — residualized scatter
binscatter log_wage tenure, controls(age edu female) nquantiles(20) ///
    savegraph("figures/figA_binscatter.pdf") replace

* RD plot (only when running_var exists)
* rdplot outcome running_var, c(0) ///
*     graph_options(title("Effect of eligibility") ///
*                   ytitle("Outcome") xtitle("Running variable"))
* graph export "figures/figA_rdplot.pdf", replace

* Bacon decomposition plot — TWFE diagnostic
* bacondecomp log_wage training, ddetail
* graph export "figures/figA_bacon.pdf", replace

* ============================================================
* 8k. Graph theme (consistent styling across all figures)
* ============================================================
set scheme s2color
* or the modern: set scheme white_tableau  (from -schemepack-)
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

The single artifact a journal's replication office (or a future co-author) needs to reproduce the headline number. Persist Stata version, seed, dataset hash, baseline coefficient + CI, and pointers to the protocol/contract:

```stata
* After the headline regression has run as `eststo base`:
qui estimates restore base
matrix b = e(b); matrix V = e(V)
local b_hat = b[1, "training"]
local se    = sqrt(V["training","training"])
local lo    = `b_hat' - 1.96 * `se'
local hi    = `b_hat' + 1.96 * `se'

file open f using "artifacts/result.json", write replace
file write f "{" _n
file write f `"  "stata_version":   "`c(stata_version)'","' _n
file write f `"  "current_date":    "`c(current_date)' `c(current_time)'","' _n
file write f `"  "seed":            42,"' _n
file write f `"  "n_obs":           `=e(N)',"' _n
file write f `"  "estimand":        "ATT","' _n
file write f `"  "estimator":       "`e(cmd)'","' _n
file write f `"  "estimate":        `b_hat',"' _n
file write f `"  "se_cluster":      `se',"' _n
file write f `"  "ci95_lo":         `lo',"' _n
file write f `"  "ci95_hi":         `hi',"' _n
file write f `"  "pre_registration": "strategy.do","' _n
file write f `"  "data_contract":    "artifacts/data_contract.json","' _n
file write f `"  "sample_log":       "artifacts/sample_construction.json","' _n
file write f `"  "paper_bundle":     "tables/table2_main.tex"' _n
file write f "}" _n
file close f
```

Commit `artifacts/result.json` alongside the paper PDF. A referee should be able to run `make clean && do main.do` and bit-identically reproduce this JSON.

---

## §A — Epidemiology / Public Health Mode

When the user's wording flags Mode A (target-trial emulation / IPTW / TMLE / MR / STROBE / 流行病学 / 公共健康 / RWE / cohort), the 8 steps still apply — but Step 5 swaps the OLS-and-FE stack for the doubly-robust + survival + MR triplet, and the deliverables follow STROBE / TRIPOD-AI conventions. **Steps 1–4 (cleaning, construction, Table 1, diagnostics) and Step 8 (tables/figures export) are identical to the Default mode.**

**Command footprint** (install on top of the Default Stata stack):

```stata
ssc install eltmle           // TMLE for binary outcome
ssc install mrrobust         // Mendelian randomization (IVW / Egger / weighted median)
ssc install mregger          // alternative MR-Egger implementation
ssc install mrpresso         // outlier-robust MR
ssc install evalue           // E-value sensitivity (Linden-Mathur)
ssc install strmst2          // RMST contrast for survival
ssc install gformula         // parametric g-formula (time-varying)
* `teffects ipw / ipwra / aipw` are native to Stata 13+; no install needed.
```

### A.0 Cohort construction + target-trial protocol

Write the protocol **before** touching the data. Save it as `protocol.do` and quote it in the paper.

```stata
*--- protocol.do — target-trial emulation skeleton ---
* eligibility:  age 40-75, no prior MI, ascertained at t0
* treatment:    A=1 statin initiation; A=0 no initiation
* assignment:   emulated random at t0 via IPTW on baseline covariates
* outcome:      incident MI within 5 years
* estimand:     ITT ATE on risk difference + hazard ratio

use raw/cohort.dta, clear
keep if inrange(age, 40, 75) & prior_MI == 0
gen t0           = cond(missing(statin_initiation_date), enrollment_date, statin_initiation_date)
gen event_5y     = (MI_date - t0 <= 365 * 5) & !missing(MI_date)
gen time_at_risk = min(censor_date - t0, 365 * 5)
stset time_at_risk, failure(event_5y)
```

### A.1 Table 1 by exposure (identical to Default Step 3)

Use the same `balancetable` / `asdoc tabstat` from Step 3, just `by(A)`. E-values for unmeasured confounding go in the footer.

```stata
balancetable A age edu smoke bmi ldl sbp using tables/tableA1_strobe.tex, ///
    replace ctitles("Untreated" "Treated" "Diff (SE)") pvalues
```

### A.2 DAG + propensity-score overlap (positivity check)

```stata
* Estimate PS via logit
logit A age edu smoke bmi ldl sbp
predict ps, pr

* Overlap density (positivity)
twoway (kdensity ps if A == 0) (kdensity ps if A == 1), ///
    legend(order(1 "A=0" 2 "A=1")) xtitle("Propensity score")
graph export figures/figA2_ps_overlap.pdf, replace

* Love plot — pre vs post-IPTW SMDs
teffects ipw (event_5y) (A age edu smoke bmi ldl sbp)
tebalance summarize
tebalance density ps
graph export figures/figA2_love.pdf, replace
```

### A.3 IPTW + g-formula + TMLE doubly-robust triplet (Step 5 swap)

The "AER Table 2" of epi: a 3-row table where each row is one of {IPTW-MSM via `teffects ipw`, IPWRA / AIPW via `teffects aipw`, TMLE via `eltmle`}, so the reader can confirm doubly-robust agreement.

```stata
* IPTW-MSM (marginal effect on risk difference)
eststo m_iptw: teffects ipw (event_5y) (A age edu smoke bmi ldl sbp), atet
* AIPW (doubly robust ATE)
eststo m_aipw: teffects aipw (event_5y age edu smoke bmi ldl sbp) ///
                              (A age edu smoke bmi ldl sbp)
* IPWRA — alternative DR estimator
eststo m_ipwra: teffects ipwra (event_5y age edu smoke bmi ldl sbp) ///
                                (A age edu smoke bmi ldl sbp)
* TMLE via eltmle (uses SuperLearner under the hood)
preserve
    eltmle event_5y A age edu smoke bmi ldl sbp, tmle
restore

* Stack the triplet
esttab m_iptw m_aipw m_ipwra using tables/tableA3_dr_triplet.tex, ///
    replace b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("IPTW" "AIPW" "IPWRA") ///
    title("Doubly-robust risk-difference triplet")
```

### A.4 Survival outcomes — KM / Cox / AFT / RMST

```stata
* KM by treatment (already stset above)
sts graph, by(A) ci risktable
graph export figures/figA4_km.pdf, replace

* Cox HR (covariate-adjusted)
stcox A age edu smoke bmi ldl sbp
estimates store m_cox
* HR + 95% CI for A:
matrix b  = e(b);   matrix V = e(V)
local HR    = exp(b[1, "A"])
local lo    = exp(b[1, "A"] - 1.96*sqrt(V["A","A"]))
local hi    = exp(b[1, "A"] + 1.96*sqrt(V["A","A"]))
display "HR = " %5.3f `HR' "  95% CI [" %5.3f `lo' ", " %5.3f `hi' "]"

* AFT (Weibull) for time-ratio interpretation
streg A age edu smoke bmi ldl sbp, distribution(weibull) time

* RMST contrast at t = 5 years
strmst2 A, tau(1825) covariates(age edu smoke bmi ldl sbp)
```

### A.5 Mendelian randomization (IVW / Egger / weighted-median triplet)

```stata
* Two-sample MR with pre-extracted instrument betas/SEs
* (BX, BXSE, BY, BYSE in long format, one row per SNP)
mrrobust, beta_outcome(by) se_outcome(byse) beta_exposure(bx) se_exposure(bxse)
mregger by bx [aw=1/byse^2], gxse(bxse)
mrmedian by bx, weighted gxse(bxse) gyse(byse)

* Outlier-robust + heterogeneity sensitivity
mrpresso by bx, gxse(bxse) gyse(byse) outlier distortion seed(1) niter(1000)

* Stack the triplet
esttab using tables/tableA5_mr_triplet.tex, ///
    replace mtitles("IVW" "MR-Egger" "Weighted median") ///
    title("Mendelian randomization triplet")
```

### A.6 Robustness — E-value / bounds / principal stratification

```stata
* E-value (Linden-Mathur Stata implementation) — required strength of unmeasured confounding
evalue rr, est(1.45) lcl(1.10) ucl(1.91)
```

### A.7 STROBE / TRIPOD-AI reporting checklist

Save as `replication/strobe_checklist.do` (or `.md`) and tick before submission:

```
[ ] Eligibility criteria + dates                           (target-trial protocol)
[ ] Adjustment set with DAG justification                  (A.2)
[ ] Positivity / overlap diagnostic                        (A.2)
[ ] Doubly-robust triplet (IPTW + AIPW + TMLE)             (A.3)
[ ] Risk difference + hazard ratio + RMST                  (A.3, A.4)
[ ] E-value for unmeasured confounding                     (A.6)
[ ] Loss-to-follow-up rate + censoring assumption          (A.0)
[ ] Pre-registered protocol or analysis plan               (A.0)
```

---

## §B — ML Causal Inference Mode

When the user's wording flags Mode B (DML / meta-learner / causal forest / CATE / policy learning / 因果机器学习), the pipeline keeps Steps 1–4 and Step 8 from the Default mode, swaps Step 5 for the ML estimator stack, and adds a CATE-distribution + policy-value layer between Step 7 and Step 8.

> **Native vs Python callout**: Stata 17+ ships first-class ML-causal commands for DML and causal forests. For neural causal (Dragonnet / TARNet / CEVAE), conformal causal, and fairness audit, the skill calls out to Python via Stata 18's `python:` block — clearly marked at each step.

**Command footprint** (install on top of the Default Stata stack):

```stata
ssc install ddml             // double machine learning (Ahrens-Hansen-Schaffer-Wiemann)
ssc install pdslasso         // post-double-selection lasso for high-dim controls
ssc install ivlasso          // IV variant of pdslasso
ssc install crforest         // causal forest (Athey-Tibshirani-Wager) for Stata
ssc install lassopack        // covariate selection helpers
* For BART / BCF / Dragonnet / conformal: shell out to Python via `python:` block
* (Stata 18 ships first-class Python integration)
```

### B.0 Train/holdout split + nuisance super-learner

DML / TMLE / Causal Forest are doubly-robust *if* the nuisance learners (outcome regression `Q(X,A) = E[Y|X,A]` and propensity `g(A|X) = Pr(A=1|X)`) converge faster than `n^(-1/4)`. Use `pystacked` (Stata 18 + Python callout) to stack GBM / RF / Lasso / NN under cross-validation — that is the Stata equivalent of StatsPAI's SuperLearner.

```stata
set seed 42
gen u = runiform()
gen byte holdout = u > 0.7

* pystacked — installed via `python: import pystacked` (requires Stata 18 + Python ≥ 3.8)
ssc install pystacked, replace

* The standard nuisance pair (will be reused inside ddml below):
*   ml_g  = outcome model         pystacked Y X*, type(reg)   methods(ols rf gradboost lassocv)
*   ml_m  = propensity model      pystacked D X*, type(class) methods(logit rf gradboost)

* For TMLE-style binary-outcome workflows, use -eltmle- which already wraps SL.
* Standalone holdout is needed for the OFF-policy evaluation in B.4 — DML / GRF
* handle their own cross-fitting internally and don't need a manual split.
```

### B.1 DAG / estimand declaration (optionally LLM-assisted)

```stata
* Causal discovery is thin in Stata — call out to Python's causal-learn:
python:
import pandas as pd
from causallearn.search.ConstraintBased.PC import pc
from sfi import Data
df = pd.DataFrame({v: Data.get(v) for v in ["A","Y","X1","X2","X3","X4"]})
cg = pc(df.to_numpy())
cg.draw_pydot_graph(labels=list(df.columns)).write_pdf("figures/figB1_dag.pdf")
end
```

### B.2 Estimator stack — DML · meta-learners · causal forest (Step 5 swap)

The "AER Table 2" of ML causal: a horse-race table where each column is one estimator family on the same `(Y, A, X)` data — readers want to see DML (PLR), DML (interactive), and causal forest all agree (or disagree) on the ATE.

```stata
*--- 1. DML — partially linear regression ---
ddml init partial, kfolds(5) reps(5)
ddml E[Y|X]: reg Y X1 X2 X3 X4
ddml E[Y|X]: pystacked Y X1 X2 X3 X4, type(reg) methods(rf gradboost lassocv)
ddml E[D|X]: reg A X1 X2 X3 X4
ddml E[D|X]: pystacked A X1 X2 X3 X4, type(reg) methods(rf gradboost lassocv)
ddml crossfit
ddml estimate, robust
eststo m_dml_plr

*--- 2. DML — interactive (heterogeneous treatment effects) ---
ddml init interactive, kfolds(5) reps(5)
ddml E[Y|X,D]: pystacked Y X1 X2 X3 X4, type(reg) methods(rf gradboost)
ddml E[D|X]:   pystacked A X1 X2 X3 X4, type(class) methods(rf gradboost logit)
ddml crossfit
ddml estimate, atet
eststo m_dml_atet

*--- 3. Causal forest — non-parametric CATE ---
crforest Y A X1 X2 X3 X4, ntrees(2000) honesty
predict cate, te
eststo m_cf

*--- 4. (Optional) Neural causal (Dragonnet / TARNet) — Python callout ---
* Stata has no native neural-causal estimator; shell out to econml / causalml:
python:
import numpy as np, pandas as pd
from sfi import Data
from econml.dr import DRLearner
from econml.metalearners import XLearner
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
df = pd.DataFrame({v: Data.get(v) for v in ["Y","A","X1","X2","X3","X4"]})
X = df[["X1","X2","X3","X4"]].values; T = df["A"].values; Y = df["Y"].values
dr = DRLearner(model_propensity=GradientBoostingClassifier(),
               model_regression=GradientBoostingRegressor(),
               model_final=GradientBoostingRegressor()).fit(Y, T, X=X)
ate, lo, hi = dr.ate(X), *dr.ate_interval(X)
Data.addVarFloat("cate_dr"); Data.store("cate_dr", range(len(df)), dr.effect(X))
end

*--- 5. (Optional) Bayesian Causal Forest (BCF) — R callout ---
* Use the bcf R package via -shell Rscript- to fit the full posterior over CATE.
* The R script writes posterior_summary.csv; we import it back as a frame:
* shell Rscript scripts/bcf.R
* import delimited posterior_summary.csv, clear case(preserve)

*--- 6. Stack the horse-race ---
esttab m_dml_plr m_dml_atet m_cf using tables/tableB2_ml_horserace.tex, ///
    replace b(4) se(4) star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("DML (PLR)" "DML (ATET)" "Causal forest") ///
    stats(N, labels("N")) ///
    title("ML causal horse-race on \$(Y, A, X)\$") ///
    addnotes("DR-Learner / Dragonnet / BCF columns added via Python/R callouts when relevant.")
```

### B.3 CATE distribution + subgroup CATE plot (Step 7 extension)

```stata
* CATE histogram from causal forest
histogram cate, frequency normal xtitle("CATE") xline(0)
graph export figures/figB3_cate_hist.pdf, replace

* CATE by quartile of a covariate
xtile age_q = X1, n(4)
collapse (mean) cate, by(age_q)
graph bar (asis) cate, over(age_q) ytitle("Mean CATE")
graph export figures/figB3_cate_by_age_q.pdf, replace
```

### B.4 Policy learning + off-policy evaluation

```stata
* Stata's native policy-tree support is via crforest; for honest depth-3 trees,
* call out to R's policytree from within Stata:
shell Rscript scripts/policy_tree.R                          // saves policy_pred.csv

import delimited using policy_pred.csv, clear case(preserve)
* DR off-policy evaluation on holdout
keep if holdout
gen DR_match = (policy_pred == A) * Y - (policy_pred != A) * Y
summarize DR_match
display "DR policy value (holdout): " r(mean)
```

### B.5 Uncertainty (conformal causal) + fairness + sensitivity

```stata
python:
# Conformal prediction interval around CATE — distribution-free coverage guarantee
import numpy as np
from sfi import Data
from sklearn.ensemble import GradientBoostingRegressor
from mapie.regression import MapieRegressor
df = ...   # same DataFrame as B.1
mapie = MapieRegressor(estimator=GradientBoostingRegressor(), method="plus", cv=10)
# fit on training CATE, predict 90% PI on holdout
end

* Fairness audit — disparate impact (compute via teffects diff across sensitive groups)
foreach g in 0 1 {
    quietly mean cate if sensitive_attr == `g'
    matrix b = e(b)
    display "Mean CATE in group `g': " b[1, 1]
}
```

### B.6 ML-causal-specific reporting checklist

Save as `replication/ml_causal_checklist.md`:

```
[ ] Nuisance learners listed (Q model, g model, hyperparameters, CV folds)
[ ] Cross-fitting / sample-splitting documented (ddml kfolds(K) reps(R))
[ ] Overlap / propensity diagnostics (B.0 + A.2-style overlap plot)
[ ] CATE summary (mean, SD, quartiles) + heterogeneity p-value (crforest test)
[ ] Policy value with confidence interval (B.4)
[ ] Conformal coverage rate on holdout (B.5)
[ ] Fairness gaps across sensitive attributes (B.5)
[ ] DAG / adjustment set + sensitivity to unmeasured confounding (E-value or Manski bounds)
```

---

## Library / command cheat-sheet

| Step | Task | Go-to command | Fallback |
|------|------|---------------|----------|
| 1 | Import | `use` / `import excel` / `import delimited` / `import sas` / `import spss` | `usespss` / `infile` |
| 1 | Missing | `misstable summarize` / `mdesc` | `missings report` |
| 1 | Merge | `merge m:1 ... assert(match using)` | — |
| 1 | Panel | `xtset` / `xtdescribe` | `tsset` for pure TS |
| 2 | Winsorize | `winsor2` | hand-roll via `summ, detail` + `replace` |
| 2 | Lag / lead / diff | `L.` / `F.` / `D.` (require `xtset`) | `bys id (t): gen lx = x[_n-1]` |
| 3 | Table 1 | `tabstat` + `balancetable` + `asdoc sum` | manual loop |
| 3 | Correlations | `pwcorr, sig star(.05)` | `corr` |
| 4 | Hetero | `estat hettest` / `estat imtest, white` | — |
| 4 | Panel serial | `xtserial` / `xttest3` | — |
| 4 | Stationarity | `dfuller` / `kpss` / `pperron` / `xtunitroot` | — |
| 4 | Hausman | `hausman fe re, sigmamore` | — |
| 5 | OLS / panel FE | `reghdfe` | `areg` / `xtreg, fe` |
| 5 | IV | `ivreg2` / `ivreghdfe` | `ivregress 2sls` |
| 5 | DID — 2×2 | `reg` / `reghdfe` with `c.treated#c.post` | — |
| 5 | DID — CS | `csdid` | — |
| 5 | DID — SA | `eventstudyinteract` | — |
| 5 | DID — imputation | `did_imputation` | `did_multiplegt_dyn` |
| 5 | DID — SDID | `sdid` | — |
| 5 | RD | `rdrobust` / `rddensity` / `rdplot` | `rdmc` for multi-cutoff |
| 5 | Synthetic control | `synth` / `synth_runner` | — |
| 5 | PSM | `psmatch2` / `teffects psmatch` | — |
| 5 | IPW / AIPW | `teffects ipw` / `teffects ipwra` / `teffects aipw` | — |
| 5 | Entropy balancing | `ebalance` | — |
| 5 | Count + FE | `ppmlhdfe` | `poisson` / `nbreg` |
| 5 | Heckman | `heckman` | manual 2-step |
| 5 | Quantile | `qreg` / `sqreg` | `bsqreg` |
| 6 | Wild cluster boot | `boottest` | `bootstrap, cluster()` |
| 6 | Randomization inf | `ritest` | `permute` |
| 6 | Multiple testing | `rwolf` | `wyoung` |
| 6 | TWFE diagnosis | `bacondecomp` | — |
| 6 | PT sensitivity | `honestdid` | — |
| 6 | Oster δ* | `psacalc delta` | manual formula |
| 7 | Interaction margins | `margins` + `marginsplot` | — |
| 7 | Mediation | `medsem` / `khb` | manual Baron–Kenny |
| 7 | SEM / path | `sem` / `gsem` | — |
| 8 | Regression table | `esttab` (from `estout`) | `outreg2` / `xtable` |
| 8 | Coefplot / eventstudy | `coefplot` | `marginsplot` |
| 8 | Binscatter | `binscatter` | `twoway` manual |
| 8 | RD plot | `rdplot` | — |

---

## Common mistakes (and what to do instead)

| Mistake | Correct approach |
|---------|------------------|
| `reg y x1 x2` on panel data with no FE | `reghdfe y x1 x2, absorb(unit time) vce(cluster unit)` |
| Default iid SEs on clustered data | `vce(cluster id)`; `boottest` if clusters < 50 |
| TWFE (`reghdfe` with treatment dummy) on staggered adoption | Use `csdid` / `eventstudyinteract` / `did_imputation` |
| `xtreg, fe` with large panel (>10k units) | Switch to `reghdfe` — faster and allows multi-dim FE + multi-way cluster |
| `merge` without `assert()` | Always specify `assert(match using master)` or similar |
| Generating lag as `L.x` without `xtset` first | Run `xtset id time` before any time-series op |
| `ivregress` without `estat firststage` | For weak-IV diagnostics, prefer `ivreg2` — reports CD, KP, AR automatically |
| RD with a single bandwidth | `rdrobust` default reports MSE-optimal + sensitivity; also show `rdbwselect` and halve/double |
| `psmatch2` without balance check | Use `pstest, both` to report pre/post SMDs; target <10% |
| Interpreting `logit` coefficients directly | Always run `margins, dydx(*)` — that's the interpretable quantity |
| Reporting only `estimates` and manual copy-paste | `esttab` / `outreg2` → LaTeX/Word/RTF automatically |
| Reporting only the headline coefficient (no Table 2) | **Always** ship the multi-column M1→M6 main table — that is the centerpiece of an economics paper, not the abstract sentence |
| Coefficient table without any figures | An economics result needs **at least** F1 trend + F2 event study + F3 coefplot + F4 sensitivity — see the Default Output Spec |
| Saving graphs with `graph save` (`.gph` only) | Also `graph export ..., replace` to `.pdf` / `.png` |
| Not logging the session | `log using main.log, replace` at top of do-file |
| `gen x2 = x^2` instead of `c.x##c.x` inside regressions | Factor-variable notation plays nicely with `margins` |

---

## Typical .do-file skeleton

```stata
* ============================================================
* main.do — reproducible 8-step pipeline
* ============================================================
version 17
clear all
set more off
capture log close
log using "logs/main.log", replace text

cd "/path/to/project"

* 1. Clean -----------------------------------------------------
do "code/01_clean.do"                 // produces data/analysis.dta

* 2. Transform -------------------------------------------------
do "code/02_transform.do"             // adds engineered vars

* 3. Describe --------------------------------------------------
do "code/03_describe.do"              // writes tables/table1_*, figures/*_trend.pdf

* 4. Diagnose --------------------------------------------------
do "code/04_diagnose.do"              // writes logs/diagnostics.log

* 5. Model -----------------------------------------------------
do "code/05_model.do"                 // saves e() for m1–m6 via eststo

* 6. Robustify -------------------------------------------------
do "code/06_robust.do"

* 7. Further ---------------------------------------------------
do "code/07_further.do"

* 8. Export ----------------------------------------------------
do "code/08_tables_figures.do"        // writes tables/*.tex, figures/*.pdf

log close
```

Every `.do` file loads `data/analysis.dta`, writes its outputs to `tables/` or `figures/`, and saves a log. A clean `make clean && do main.do` regenerates the entire paper from raw data.

---

## Regtable (esttab) cookbook (one-page recipe index)

`eststo` + `esttab` is the single primitive behind every multi-regression table in an AER paper. The eight patterns above map to:

| Pattern | What varies across columns | Step |
|---|---|---|
| **A. Progressive controls** | covariate set / FE depth | 5.A — Table 2 |
| **B. Design horse race** | identification strategy (OLS / IV / DID / PSM / EB) | 5.B — Table 2-bis |
| **C. Multi-outcome** | dependent variable Y | 5.C — Table 2-ter |
| **D. Stacked Panel A / B** | horizon / sample (panel rows × spec columns) | 5.D — Table 2-quater |
| **E. IV reporting triplet** | first stage / reduced form / 2SLS | 5.E — Table 2-quinto |
| **F. Causal-orchestrator** | 1 column, full diagnostics (`csdid`/`synth_runner`/`teffects`) | 5.F |
| **G. Subgroup table** | subsample (full / female / male / Q1…Q4) | 7.b — Table 3 |
| **H. Robustness master** | every robustness check stacked | 6.k — Table A1 |

Default `esttab` settings for AER house style:

```stata
esttab m1 ... mN using "tables/tableN.tex", ///
    replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///       AER stars convention
    label booktabs ///
    mtitles("(1)" "(2)" ...) ///                column labels
    stats(N r2 r2_a, labels("N" "R²" "Adj. R²")) ///
    addnotes("Cluster-robust SE in parentheses." ///
             "* p<0.10, ** p<0.05, *** p<0.01.")
* Word version: same call with .rtf extension.
* For multi-panel paper bundles, chain esttab with `, append` (see 5.D / 8.5.4).
```

---

## Figure factory (the 12 standard AER figures in Stata)

| # | Figure | Stata commands | Section |
|---|---|---|---|
| 1a | Raw trends (DID Figure 1) | `collapse (mean) y, by(year treat)` → `twoway line` | §1 (Step 3.e) |
| 1b | Treatment rollout heatmap | `heatplot first_treat unit, color(...)` | §1 |
| 2a | Event-study coefficients | `eventstudyinteract` → `coefplot, keep(rel_d*)` | §3 (Step 3.5.1) |
| 2a' | Bacon weights | `bacondecomp y treat, ddetail` → built-in graph | §3 |
| 2a'' | CS-DID dynamic effects | `csdid` → `csdid_plot` | §3 |
| 2b | First-stage scatter | `binscatter D Z, controls(X)` | §3 (Step 3.5.2) |
| 2c | RD canonical plot | `rdplot Y X, c(0)` | §3 (Step 3.5.3) |
| 2c' | McCrary density | `rddensity X, c(0) plot` | §3 |
| 2d | Matching love plot | `pstest X, both graph` (after `psmatch2`) | §3 (Step 3.5.4) |
| 2e | SCM trajectory | `synth y X, trunit() trperiod() fig` · `sdid` graph | §3 (Step 3.5.5) |
| 3 | Coefficient plot of main specs | `coefplot m1...m6, keep(D)` | §4 (Step 8.f) |
| 4a | Dose-response | `xtile dose10 = D, nq(10)` → `margins i.dose10` → `marginsplot` | §5 (Step 7.g) |
| 4b | Margins-by-subgroup | `margins, dydx(D) at(group=(0 1))` → `marginsplot` | §5 |
| 5 | Specification curve | hand-rolled spec loop → `twoway rcap` (see 6.l) | §7 |
| 6 | Sensitivity dashboard | `honestdid, coefplot` · `psacalc plot` · `evalue` | §7 (Step 6.m) |
| 7 | Final main figure | estimator-specific (`csdid_plot`, `synth` fig, `rdplot`) | §8 |

> Every Stata figure is exported as **both** `.pdf` (for LaTeX) and `.png ≥ 300 dpi` (for slides / web). Use `set scheme s2color` (or `white_tableau` from `schemepack`) once at the top of `master.do` for consistent styling.

---

## Method Catalog

### Classical OLS / Panel
```stata
reg log_wage training age edu,                        vce(cluster firm_id)            // OLS
areg log_wage training age edu, absorb(industry)      vce(cluster firm_id)            // OLS + 1 FE
xtreg log_wage training age edu, fe                                                   // panel FE
xtreg log_wage training age edu, re                                                   // panel RE (Hausman)
reghdfe log_wage training age edu, absorb(worker_id year) vce(cluster firm_id)        // HD FE workhorse
reghdfe log_wage training,        absorb(worker_id year) vce(cluster firm_id year)    // 2-way cluster
ppmlhdfe count training,          absorb(firm_id year) cluster(firm_id)               // Poisson + FE
heckman log_wage training, select(in_lf = age edu marital kids)                       // Heckman selection
qreg    log_wage training age,    quantile(0.5)                                       // quantile reg
sqreg   log_wage training age,    quantile(0.1 0.25 0.5 0.75 0.9) reps(500)
```

### Difference-in-Differences
```stata
* 2×2
reghdfe log_wage c.treat#c.post, absorb(worker_id year) vce(cluster worker_id)
* Staggered — modern stack
csdid                log_wage age edu, ivar(worker_id) time(year) gvar(first_treat) method(dripw) agg(group)
eventstudyinteract   log_wage rel_d*, cohort(first_treat) control_cohort(never_treated) absorb(worker_id year) vce(cluster worker_id)
did_imputation       log_wage worker_id year first_treat, allhorizons pretrend(5)
did_multiplegt_dyn   log_wage worker_id year training, effects(5) placebo(3)
sdid                 log_wage worker_id year training, vce(bootstrap) graph
* Diagnostics + sensitivity
bacondecomp log_wage training, ddetail                                                // TWFE diagnostic
honestdid, pre(rel_d1-rel_d3) post(rel_d5-rel_d9) mvec(0(0.1)0.5)                     // PT sensitivity
```

### Instrumental Variables / 2SLS
```stata
ivregress 2sls   log_wage age edu (training = Z), vce(cluster firm_id)                // baseline
ivreg2           log_wage age edu (training = Z), cluster(firm_id) first endog(training) // workhorse: full diagnostics
ivreghdfe        log_wage age (training = Z), absorb(industry year) cluster(firm_id) first
* Weak-IV diagnostics
estat firststage                                                                      // (after ivregress)
* ivreg2 reports CD / KP / AR automatically.
```

### Regression Discontinuity
```stata
rdrobust  outcome running_var, c(0) kernel(triangular) bwselect(mserd)                // Sharp RD (CCT)
rdrobust  outcome running_var, c(0) fuzzy(treatment)                                  // Fuzzy RD
rddensity running_var, c(0) plot                                                      // McCrary density
rdmc      outcome running_var, cutoffs(0 5 10)                                        // multi-cutoff
rdplot    outcome running_var, c(0)
```

### Matching / Reweighting
```stata
psmatch2  training age edu tenure, out(log_wage) n(1) common                          // PSM (canonical)
teffects  psmatch (log_wage) (training age edu tenure), atet                          // PSM (modern)
teffects  ipw     (log_wage) (training age edu tenure), atet                          // IPW
teffects  ipwra   (log_wage age edu tenure) (training age edu tenure)                 // IPWRA
teffects  aipw    (log_wage age edu tenure) (training age edu tenure)                 // AIPW (DR)
ebalance  training age edu tenure                                                     // entropy balancing
```

### Synthetic Control
```stata
synth         log_wage age edu, trunit(1) trperiod(2015) fig keep(synth.dta, replace)
synth_runner  log_wage age edu, trunit(1) trperiod(2015) gen_vars                      // + 50 placebos
sdid          log_wage worker_id year training, vce(bootstrap) graph
```

### ML Causal (Mode B — see §B for the full pipeline)
```stata
ddml init partial, kfolds(5) reps(5)                                                  // DML setup
ddml E[Y|X]: pystacked Y X*, type(reg) methods(rf gradboost lassocv)
ddml E[D|X]: pystacked D X*, type(reg) methods(rf gradboost lassocv)
ddml crossfit
ddml estimate, robust
crforest log_wage training age edu, ntrees(2000) honesty                              // causal forest
predict cate, te
pdslasso log_wage training (X1-X100), cluster(firm_id) partial                        // post-double-selection
```

### Robustness, Sensitivity & Inference
```stata
boottest         training, cluster(state) reps(9999) seed(42)                         // wild cluster bootstrap
ritest           training _b[training], reps(1000) seed(0): reghdfe ...               // randomization inf.
rwolf            y1 y2 y3, indepvar(training) controls(X) reps(500) ...               // Romano-Wolf MTC
psacalc delta    training, mcontrol(X) rmax(1.3)                                      // Oster δ
honestdid, pre(...) post(...) mvec(0(0.1)0.5)                                         // RR PT sensitivity
evalue rr,       est(1.45) lcl(1.10) ucl(1.91)                                        // E-value
xtcsd, pesaran abs                                                                    // cross-sec dependence
```

### Survival / Epi (Mode A — see §A)
```stata
stset time, failure(event)
sts graph, by(A) ci risktable                                                         // Kaplan-Meier
stcox A age edu                                                                       // Cox
streg A age edu, distribution(weibull) time                                           // AFT
strmst2 A, tau(1825) covariates(age edu)                                              // RMST contrast
gformula ...                                                                          // parametric g-formula
eltmle event A age edu, tmle                                                          // TMLE for binary outcome
mrrobust, beta_outcome(by) se_outcome(byse) beta_exposure(bx) se_exposure(bxse)       // MR-IVW
mregger by bx [aw=1/byse^2], gxse(bxse)                                                // MR-Egger
```

---

## When to hand off to other skills

- **Agent-native single-import Python workflow** (`import statspai as sp`) → `00-StatsPAI_skill`.
- **Explicit Python traditional stack** → `00.1-Full-empirical-analysis-skill`.
- **Mixtape-style cross-language code templates** (Python/R/Stata side-by-side) → `10-Jill0099-causal-inference-mixtape`.
- **Stata syntax reference** (complete command catalog, Mata, etc.) → `32-dylantmoore-stata-skill`.
- **Stata for accounting research** → `18-jusi-aalto-stata-accounting-research`.
- **Paper drafting** after the analysis is done → the writing-oriented skills in this repo (`04-*-scientific-writer`, `08-*-web-latex`, etc.).

This skill's remit **ends at Step 8** — polished `.tex` tables and `.pdf` figures. Paper drafting is out of scope.
