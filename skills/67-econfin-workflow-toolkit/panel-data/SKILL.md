---
name: panel-data
description: |
  Econometrics skill for panel data models. Activates when the user asks about:
  "panel data", "fixed effects", "random effects", "Hausman test", "within estimator",
  "between estimator", "two-way fixed effects", "clustered standard errors panel",
  "FE model", "RE model", "pooled OLS", "unobserved heterogeneity", "panel regression",
  "first difference estimator", "entity fixed effects", "time fixed effects",
  "面板数据", "固定效应", "随机效应", "豪斯曼检验", "双向固定效应",
  "面板回归", "个体效应", "时间效应", "一阶差分"
---

# Panel Data Models Skill

This skill covers panel data econometrics: pooled OLS, fixed effects (FE), random effects (RE), and two-way FE models. It guides model selection, assumption testing, and interpretation for longitudinal/panel datasets.

## Key Terminology

- **Panel dataset**: observations on N units (individuals, firms, countries) over T time periods
- **Balanced panel**: every unit observed in every period
- **Unbalanced panel**: some unit-period observations missing
- **Unobserved heterogeneity (αᵢ)**: time-invariant unit-specific factors (e.g., firm culture, individual ability)

## Model Selection Framework

```
Start
 ├─ Is unobserved heterogeneity correlated with regressors?
 │    ├─ YES → Fixed Effects (FE)
 │    └─ NO  → Random Effects (RE) — test with Hausman
 │
 ├─ Are time effects important?
 │    ├─ YES → Two-Way FE (entity + time dummies)
 │    └─ NO  → One-Way FE
 │
 └─ Need to estimate effect of time-invariant variables?
      ├─ YES → Random Effects or Mundlak/Correlated RE
      └─ NO  → Fixed Effects preferred
```

### Hausman Test Decision Rule
- H₀: RE is consistent (αᵢ uncorrelated with X)
- H₁: FE is consistent but RE is not (αᵢ correlated with X)
- **p < 0.05**: Use Fixed Effects
- **p ≥ 0.05**: Random Effects is efficient

### Mundlak / Correlated Random Effects (CRE)

Use when you need RE to estimate time-invariant variable effects, but want to relax the strict exogeneity assumption of RE. CRE includes group means of time-varying regressors in the RE equation, making it equivalent to FE for those variables while still estimating time-invariant effects.

```r
# R — Mundlak CRE approach
library(plm); library(dplyr)

# Compute entity means of time-varying regressors
panel_df_cre <- df %>%
  group_by(entity_id) %>%
  mutate(x1_mean = mean(x1),
         x2_mean = mean(x2)) %>%
  ungroup()

panel_cre <- pdata.frame(panel_df_cre, index = c("entity_id", "time_var"))

# RE model augmented with group means (Mundlak approach):
cre_model <- plm(y ~ x1 + x2 + time_invariant_var + x1_mean + x2_mean,
                 data   = panel_cre,
                 model  = "random")
summary(cre_model)
# Coefficients on x1_mean, x2_mean test the correlation between αᵢ and X
# (equivalent to Hausman test; joint significance = prefer FE)
# Coefficient on time_invariant_var is identified via between variation
```

```stata
* Stata — Mundlak CRE
* Step 1: compute entity means
bysort entity_id: egen x1_mean = mean(x1)
bysort entity_id: egen x2_mean = mean(x2)

* Step 2: RE model with group means added
xtreg y x1 x2 time_invariant_var x1_mean x2_mean, re

* Test joint significance of group means (Mundlak test):
testparm x1_mean x2_mean
* p < 0.05 → group means matter → prefer FE for time-varying regressors
```

## Quick Code Templates

### Fixed Effects

```python
# Python (linearmodels)
from linearmodels.panel import PanelOLS
import pandas as pd

# Set multi-index: entity and time
df = df.set_index(['entity_id', 'time_var'])

model = PanelOLS(df['y'], df[['x1', 'x2']], entity_effects=True,
                 time_effects=True)  # Two-way FE
result = model.fit(cov_type='clustered', cluster_entity=True)
print(result.summary)
```

```r
# R (plm)
library(plm)
panel_df <- pdata.frame(df, index = c("entity_id", "time_var"))

# One-way FE
fe_model <- plm(y ~ x1 + x2, data = panel_df, model = "within")

# Two-way FE
twfe_model <- plm(y ~ x1 + x2, data = panel_df, model = "within",
                  effect = "twoways")

# Clustered SE
library(lmtest); library(sandwich)
coeftest(fe_model, vcov = vcovHC(fe_model, cluster = "group"))
```

```stata
* Stata — Two-way FE with clustered SE
xtset entity_id time_var
xtreg y x1 x2 i.time_var, fe cluster(entity_id)
```

### Random Effects

```python
from linearmodels.panel import RandomEffects

re_model = RandomEffects(df['y'], df[['x1', 'x2']])
re_result = re_model.fit()
print(re_result.summary)
```

```r
re_model <- plm(y ~ x1 + x2, data = panel_df, model = "random")
summary(re_model)
```

```stata
xtreg y x1 x2, re
```

### Hausman Test

```python
from linearmodels.panel import compare
# Compare FE vs RE
print(compare({'FE': fe_result, 'RE': re_result}))
# Or use statsmodels hausman
```

```r
phtest(fe_model, re_model)
# p < 0.05 → prefer Fixed Effects
```

```stata
hausman fe_estimates re_estimates
```

## Dynamic Panels and Arellano-Bond GMM

Use when the model includes a lagged dependent variable (Yᵢₜ₋₁) in short-T panels. The within (FE) estimator is biased in this case (Nickell 1981 bias). Arellano-Bond uses lagged levels as instruments for the differenced equation.

**When to use**: Short T (T < 10), panel includes lagged DV, suspicion of endogenous regressors.

```r
# R — Arellano-Bond GMM (plm package)
library(plm)

# Difference GMM (Arellano-Bond 1991)
ab <- pgmm(
  y ~ lag(y, 1) + x1 + x2 | lag(y, 2:4),   # instruments: lags 2-4 of y
  data  = panel_df,
  effect = "individual",
  model  = "twosteps"   # two-step is asymptotically efficient
)
summary(ab, robust = TRUE)

# Key diagnostics:
# AR(1): should be significant (differencing induces MA(1))
# AR(2): should be insignificant (no serial correlation in levels)
# Hansen J test: p > 0.05 → instruments are valid
```

```python
# Python — Arellano-Bond GMM (linearmodels)
# Note: linearmodels does not directly implement Arellano-Bond;
# use the dedicated BetterArellano approach or wrap via R
# Alternatively, use system GMM via a custom estimator:
# pip install pydynpd
import pydynpd

# pydynpd syntax
command_str = "y L1.y x1 x2 | gmm(y, 2 4) iv(x1 x2)"
results = pydynpd.regression.abond(command_str, df, ["entity_id", "time_var"])
print(results.summary)
```

```stata
* Stata — Arellano-Bond with xtabond2 (preferred)
ssc install xtabond2

xtset entity_id time_var

* Difference GMM:
xtabond2 y L.y x1 x2, gmm(L.y, lag(2 4)) iv(x1 x2) ///
    twostep robust noleveleq

* System GMM (adds level equation with lagged differences as instruments):
xtabond2 y L.y x1 x2, gmm(L.y, lag(2 4)) iv(x1 x2) twostep robust

* Diagnostics reported automatically:
* - AR(1), AR(2) tests
* - Hansen J test of overidentifying restrictions
```

**Interpretation rules**:
- AR(1) significant, AR(2) insignificant → no second-order serial correlation in levels ✓
- Hansen J p > 0.05 → instruments jointly valid ✓
- Too many instruments (> N) weakens the Hansen test — restrict lag range

## Standard Errors for Panel Data

| Situation | Recommended SE |
|-----------|---------------|
| Serial correlation within entities | Cluster by entity |
| Cross-sectional dependence | Driscoll-Kraay SE |
| Both serial + cross-sectional | Two-way clustering |
| Heteroskedasticity only | HC robust SE |

### Driscoll-Kraay and Two-Way Clustering Code

**Driscoll-Kraay SE**: Robust to cross-sectional dependence and serial correlation. Preferred for macro panels (small N, large T).

```r
# R — Driscoll-Kraay SE (sandwich package)
library(plm); library(sandwich); library(lmtest)

fe_model <- plm(y ~ x1 + x2, data = panel_df, model = "within")

# Driscoll-Kraay SE (robust to cross-sectional and serial dependence):
coeftest(fe_model, vcov = vcovSCC(fe_model, type = "HC1", maxlag = 4))
# maxlag: number of lags for serial correlation (typically T^0.25)
```

```stata
* Stata — Driscoll-Kraay SE
xtscc y x1 x2, fe lag(4)
* lag(4) = bandwidth parameter; use T^0.25 as a rule of thumb
```

**Two-way clustering**: Clusters at both entity and time level. Use when treatment varies at both levels.

```r
# R — Two-way clustering (sandwich)
library(sandwich); library(lmtest)

# Manually compute two-way clustered SE:
# V_twoway = V_entity + V_time - V_entity×time
vcov_entity <- vcovCL(fe_model, cluster = ~entity_id)
vcov_time   <- vcovCL(fe_model, cluster = ~time_var)
vcov_both   <- vcovCL(fe_model, cluster = ~entity_id + time_var)
coeftest(fe_model, vcov = vcov_both)
```

```stata
* Stata — Two-way clustering
xtreg y x1 x2 i.time_var, fe vce(cluster entity_id)  // cluster by entity only
* For two-way clustering (entity AND time):
reghdfe y x1 x2, absorb(entity_id time_var) vce(cluster entity_id time_var)
```

## Interpreting Fixed Effects Results

- FE coefficients identify **within-unit** variation only
- Cannot estimate effect of time-invariant variables (absorbed by unit FEs)
- Two-way FE removes both unit trends and aggregate time trends
- Always report whether entity FE, time FE, or both are included

## Reporting Standards

- State panel dimensions: N = [units], T = [periods], total obs
- Report whether SE are clustered (at entity level is standard)
- Specify which effects are included (entity, time, or both)
- Report F-test for joint significance of fixed effects
- Include Hausman test result when choosing FE over RE

For first-difference estimators, dynamic panels (Arellano-Bond), Mundlak/Correlated RE, and survival/probit panel models, see `references/panel-reference.md`.

## Common Pitfalls

- **Using RE when FE is appropriate**: If Hausman test rejects, RE is inconsistent — always test
- **Clustering at the wrong level**: Cluster SE at the level of treatment variation, not the individual level
- **Nickell bias**: Including lagged DV in short-T panels with FE is biased — use Arellano-Bond GMM
- **Ignoring cross-sectional dependence**: In macro panels (small N, large T), standard FE SE are invalid — use Driscoll-Kraay
- **Interpreting FE coefficients as between-unit effects**: FE estimates are purely within-unit; they cannot speak to cross-unit differences

## Related Skills & Commands

- **did-analysis**: If your panel data involves a policy intervention with treatment/control groups
- **ols-regression**: For cross-sectional data without panel structure
- **time-series**: For single-unit time series (macro data)
- **/diagnose**: Run panel-specific diagnostics (Hausman, serial correlation, cross-sectional dependence)
- **/robustness**: Generate robustness checks for panel specifications
- **stats**: Summarize panel dimensions and variable distributions
