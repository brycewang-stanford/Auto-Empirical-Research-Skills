---
name: did-analysis
description: |
  Econometrics skill for Difference-in-Differences (DID) analysis. Activates when the user asks about:
  "difference in differences", "DID", "DiD", "diff-in-diff", "parallel trends",
  "treatment group", "control group", "pre-treatment", "post-treatment",
  "policy evaluation", "natural experiment", "staggered DID", "event study regression",
  "two-way fixed effects DID", "callaway santanna", "sun and abraham",
  "双重差分", "倍差法", "平行趋势", "处理组", "对照组", "政策评估",
  "事件研究", "交错DID", "渐进处理"
---

# Difference-in-Differences (DID) Skill

This skill guides complete DID analysis: from assumption validation and model specification to staggered treatment designs and event study regressions. Designed for policy evaluation and natural experiment settings.

## Core DID Logic

DID compares the change in outcomes for a treatment group before and after treatment to the change for a control group over the same period.

**DID Estimator** = (Ȳ_treat,post − Ȳ_treat,pre) − (Ȳ_ctrl,post − Ȳ_ctrl,pre)

**Key Assumption (Parallel Trends)**: In the absence of treatment, the treatment group's outcome would have evolved in parallel with the control group.

## DID Workflow

1. **Design check**: Confirm treatment/control assignment and timing
2. **Parallel trends**: Test with pre-treatment event study regression
3. **Baseline regression**: 2×2 DID or TWFE regression
4. **Staggered design check**: If adoption dates vary, use robust estimators
5. **Robustness**: Placebo treatment, alternative control groups, callaway-santanna

## Basic 2×2 DID Model

```
Y_it = β₀ + β₁·Treat_i + β₂·Post_t + β₃·(Treat_i × Post_t) + ε_it

β₃ = DID estimate (ATT)
```

### Code Templates

```python
# Python — 2×2 DID with TWFE
import statsmodels.formula.api as smf

# Simple 2x2
model = smf.ols('y ~ treat + post + treat_post', data=df).fit(cov_type='HC3')

# TWFE with entity and time FE (preferred)
from linearmodels.panel import PanelOLS
df_panel = df.set_index(['entity_id', 'year'])
twfe = PanelOLS(df_panel['y'], df_panel[['treat_post']],
                entity_effects=True, time_effects=True)
result = twfe.fit(cov_type='clustered', cluster_entity=True)
print(result.summary)
```

```r
# R — TWFE
library(plm); library(lmtest); library(sandwich)
panel_df <- pdata.frame(df, index = c("entity_id", "year"))
twfe <- plm(y ~ treat_post, data = panel_df, model = "within", effect = "twoways")
coeftest(twfe, vcov = vcovHC(twfe, cluster = "group"))
```

```stata
* Stata — TWFE with clustered SE
xtset entity_id year
xtreg y treat_post i.year, fe cluster(entity_id)
* Or equivalently:
reghdfe y treat_post, absorb(entity_id year) cluster(entity_id)
```

## Parallel Trends: Event Study Regression

Replace the single `treat_post` dummy with relative-time dummies to visualize pre-trends:

```stata
* Stata — event study
reghdfe y ib(-1).rel_time, absorb(entity_id year) cluster(entity_id)
coefplot, vertical yline(0) xline(0) ///
    title("Event Study: Pre/Post Treatment Effects") ///
    xlabel(, angle(45))
```

```r
# R — event study
library(fixest)
es_model <- feols(y ~ i(rel_time, treat, ref = -1) | entity_id + year,
                  data = df, cluster = ~entity_id)
iplot(es_model, xlab = "Periods relative to treatment")
```

**Interpreting the event study plot:**
- Pre-treatment coefficients ≈ 0 → parallel trends assumption holds
- Pre-trend test: joint F-test for all pre-treatment coefficients = 0
- Post-treatment coefficients show dynamic treatment effects

## Staggered DID

When units adopt treatment at different times, standard TWFE can be biased (Callaway-Sant'Anna, Sun-Abraham).

```r
# R — Callaway-Sant'Anna estimator (csdid)
library(did)
cs_result <- att_gt(yname = "y",
                    gname = "cohort_year",   # year of first treatment (0 if never treated)
                    idname = "entity_id",
                    tname  = "year",
                    xformla = ~x1 + x2,
                    data = df)

# Aggregate to average ATT
aggte(cs_result, type = "simple")   # Overall ATT
aggte(cs_result, type = "dynamic")  # Dynamic effects
ggdid(cs_result)
```

```r
# R — Sun-Abraham (fixest)
library(fixest)
sa_model <- feols(y ~ sunab(cohort_year, year) | entity_id + year,
                  data = df, cluster = ~entity_id)
iplot(sa_model)
```

```stata
* Stata — Callaway-Sant'Anna (csdid from SSC)
csdid y x1 x2, ivar(entity_id) time(year) gvar(cohort_year)
csdid_plot
```

## Robustness Checks for DID

1. **Placebo treatment dates**: assign fake treatment 1–2 periods before actual treatment
2. **Placebo treatment groups**: run DID using only control units with a fake treatment
3. **Alternative control groups**: restrict to more comparable controls
4. **Continuous treatment intensity**: use dose-response DID

## Reporting Standards

- Report event study plot as Figure (essential for credibility)
- State the parallel trends assumption and supporting evidence
- Report DID coefficient with clustered SE (cluster at entity level)
- Discuss potential violations: anticipation effects, Ashenfelter's dip, spillovers
- For staggered designs, always use CS or SA estimators and explain why

See `references/did-reference.md` for heterogeneous treatment effects, triple-difference models, synthetic control comparison, Borusyak-Jaravel-Spiess imputation estimator, de Chaisemartin-D'Haultfoeuille estimator, and Roth (2022) pre-trends power analysis.

## Common Pitfalls

- **Using TWFE with staggered treatment and heterogeneous effects**: Standard TWFE is biased — use Callaway-Sant'Anna, Sun-Abraham, or Borusyak-Jaravel-Spiess
- **Clustering at the treatment level**: Don't cluster at the individual level if treatment varies at the state level — cluster at the state level
- **Failing to reject pre-trends ≠ parallel trends hold**: Low power is common; use Roth (2022) power analysis to assess
- **Ignoring anticipation effects**: If agents anticipate treatment, pre-treatment coefficients may be non-zero even with parallel trends
- **Not showing the event study plot**: Reviewers expect to see pre-trends visually — always include the event study figure

## Related Skills & Commands

- **synthetic-control**: When you have few treated units, SCM may be more appropriate
- **rdd-analysis**: If treatment is assigned by a threshold rule, use RDD instead
- **ml-causal**: Causal forests can identify heterogeneous treatment effects within DID
- **/diagnose**: Run DID-specific diagnostics (pre-trends, Bacon decomposition)
- **/robustness**: Placebo tests, alternative estimators, wild cluster bootstrap
- **/method**: Generate the methodology section for your DID paper
