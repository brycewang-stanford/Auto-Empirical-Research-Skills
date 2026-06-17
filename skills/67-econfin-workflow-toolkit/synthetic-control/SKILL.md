---
name: synthetic-control
description: |
  Econometrics skill for Synthetic Control Method (SCM). Activates when the user asks about:
  "synthetic control", "SCM", "synthetic counterfactual", "donor pool",
  "placebo test", "in-space placebo", "in-time placebo", "MSPE ratio",
  "Abadie Diamond Hainmueller", "augmented synthetic control", "penalized SCM",
  "synthetic DID", "合成控制", "合成控制法", "捐助池", "安慰剂检验",
  "合成反事实", "合成DID", "政策评估"
---

# Synthetic Control Method (SCM) Skill

This skill guides complete synthetic control analyses: donor pool construction, weight optimization, gap estimation, placebo-based inference, and extensions including augmented SCM and synthetic DID. Designed for policy evaluation with few treated units.

## When to Use Synthetic Control

| Situation | Method |
|-----------|--------|
| Single treated unit, many potential controls | Classic SCM |
| Few treated units | Multi-unit SCM or Synthetic DID |
| Treatment at aggregate level (state, country) | Classic SCM |
| Want DID-like inference with SCM weighting | Synthetic DID (Arkhangelsky et al. 2021) |

**Key advantage over DID**: SCM constructs a data-driven counterfactual rather than assuming parallel trends for all control units equally.

## Core Logic

SCM constructs a weighted combination of untreated ("donor") units that best approximates the treated unit's pre-treatment characteristics and outcome trajectory.

**Estimand**: τ_t = Y₁ₜ − Ŷ₁ₜ^(SC) for post-treatment periods t > T₀

**Key Assumptions**:
1. No interference between units (SUTVA)
2. No anticipation of treatment
3. Treated unit can be well-approximated by donor pool in pre-treatment period
4. The data-generating process is stable across pre/post periods

## SCM Workflow

1. **Define units and treatment**: Identify treated unit, donor pool, treatment date
2. **Select predictors**: Choose pre-treatment covariates and outcome lags
3. **Optimize weights**: Minimize pre-treatment MSPE between treated and synthetic control
4. **Estimate effects**: Gap = treated outcome − synthetic control outcome
5. **Inference**: Run placebo tests (in-space and in-time)
6. **Report**: Gap plot, placebo plot, MSPE ratios

## Code Templates

### R — Classic SCM (Synth package)

```r
# R — Abadie-Diamond-Hainmueller SCM
library(Synth)

dataprep_out <- dataprep(
  foo = df,
  predictors = c("gdp_pc", "trade_share", "inflation"),
  predictors.op = "mean",
  time.predictors.prior = 1980:1999,
  special.predictors = list(
    list("outcome", 1995:1999, "mean"),   # pre-treatment outcome lags
    list("outcome", 1990, "mean"),
    list("outcome", 1985, "mean")
  ),
  dependent = "outcome",
  unit.variable = "unit_id",
  unit.names.variable = "unit_name",
  time.variable = "year",
  treatment.identifier = 1,              # treated unit ID
  controls.identifier = 2:20,            # donor pool IDs
  time.optimize.ssr = 1980:1999,         # pre-treatment period
  time.plot = 1980:2010                  # full plot range
)

synth_out <- synth(dataprep_out)

# View donor weights (non-zero weights = selected donors)
synth.tab <- synth.tab(synth_out, dataprep_out)
print(synth.tab$tab.w)   # unit weights
print(synth.tab$tab.v)   # predictor weights

# Gap plot: treated vs synthetic control
path.plot(synth_out, dataprep_out,
          Ylab = "Outcome", Xlab = "Year",
          Main = "Treated vs Synthetic Control")
abline(v = 2000, lty = 2, col = "red")

# Gap (treatment effect) plot
gaps.plot(synth_out, dataprep_out,
          Ylab = "Gap (Treated − Synthetic)", Xlab = "Year",
          Main = "Treatment Effect Over Time")
abline(v = 2000, lty = 2, col = "red")
abline(h = 0, lty = 3)
```

### R — Augmented SCM (augsynth)

```r
# R — Augmented SCM (Ridge-augmented, Ben-Michael et al. 2021)
library(augsynth)

asyn <- augsynth(outcome ~ treatment,
                 unit = unit_id, time = year,
                 data = df,
                 progfunc = "Ridge",    # augmentation method
                 scm = TRUE)            # include SCM weights
summary(asyn)
plot(asyn)
```

**Ridge Augmentation** (`progfunc = "Ridge"`): When the pre-treatment fit of standard SCM is imperfect, Ridge augmentation adds a bias-correction term estimated by a penalized (ridge) regression of the residuals on donor outcomes. This reduces sensitivity to poor pre-treatment balance by shrinking the bias correction toward zero when donor pool fit is already good. The result is an estimator that converges to the standard SCM when pre-treatment fit is excellent, but provides robustness when it is not. Other options include `"gsyn"` (matrix completion) and `"None"` (standard SCM only).

### Python — SparseSC

```python
# Python — SparseSC (penalized synthetic control)
import SparseSC
import numpy as np

# Reshape data to (N_units × T_periods) matrix
Y = df.pivot(index='unit_id', columns='year', values='outcome').values
T0 = 20  # number of pre-treatment periods

# Fit sparse synthetic control
sc = SparseSC.fit(
    features=Y[:, :T0],       # pre-treatment outcomes
    targets=Y[:, T0:],        # post-treatment outcomes
    treated_units=[0]          # index of treated unit
)

# Treatment effect estimate
treated_actual = Y[0, T0:]
synthetic_control = sc.predict(Y[0:1, :T0])[0]
effect = treated_actual - synthetic_control
print(f"Average post-treatment effect: {np.mean(effect):.4f}")
```

### Stata — synth and synth_runner

```stata
* Stata — Classic SCM
ssc install synth
ssc install synth_runner

tsset unit_id year

synth outcome gdp_pc trade_share inflation ///
    outcome(1995) outcome(1990) outcome(1985), ///
    trunit(1) trperiod(2000) ///
    fig keep(synth_results) replace

* Plot results
twoway (line outcome year if unit_id == 1, lcolor(black) lwidth(medium)) ///
       (line _Y_synthetic year if unit_id == 1, lcolor(red) lpattern(dash)), ///
       xline(2000, lpattern(dash)) ///
       legend(label(1 "Treated") label(2 "Synthetic Control")) ///
       title("Synthetic Control Estimate")
```

## Inference: Placebo Tests

SCM does not have standard errors in the traditional sense. Inference is based on placebo (permutation) tests.

### In-Space Placebo Test

Iteratively apply SCM to every control unit as if it were treated. If the treated unit's effect is unusually large relative to placebos, the effect is credible.

```r
# R — in-space placebo (Synth)
library(Synth)
placebo_gaps <- list()
all_units <- unique(df$unit_id)

for (u in all_units) {
  controls <- setdiff(all_units, u)
  dp <- dataprep(foo = df, predictors = c("gdp_pc", "trade_share"),
                 predictors.op = "mean", time.predictors.prior = 1980:1999,
                 special.predictors = list(list("outcome", 1995:1999, "mean")),
                 dependent = "outcome", unit.variable = "unit_id",
                 time.variable = "year", treatment.identifier = u,
                 controls.identifier = controls,
                 time.optimize.ssr = 1980:1999, time.plot = 1980:2010)
  so <- synth(dp, Sigf.ipop = 3)
  placebo_gaps[[as.character(u)]] <- dp$Y1plot - (dp$Y0plot %*% so$solution.w)
}

# Plot all gaps; treated unit should stand out
plot(1980:2010, placebo_gaps[["1"]], type = "l", lwd = 2, col = "black",
     ylim = range(unlist(placebo_gaps)), ylab = "Gap", xlab = "Year")
for (u in names(placebo_gaps)[-1]) {
  lines(1980:2010, placebo_gaps[[u]], col = "grey70")
}
abline(v = 2000, lty = 2); abline(h = 0, lty = 3)
legend("topleft", c("Treated", "Placebos"), col = c("black","grey70"), lwd = c(2,1))
```

```stata
* Stata — in-space placebo with synth_runner
synth_runner outcome gdp_pc trade_share inflation ///
    outcome(1995) outcome(1990) outcome(1985), ///
    trunit(1) trperiod(2000) gen_vars
effect_graphs
single_treatment_graphs
```

### MSPE Ratios

Calculate post/pre MSPE ratio for each unit. The treated unit's ratio should rank highest.

```r
# Rank by post/pre MSPE ratio
mspe_ratios <- sapply(names(placebo_gaps), function(u) {
  gap <- placebo_gaps[[u]]
  pre  <- gap[1:20]   # pre-treatment periods
  post <- gap[21:31]  # post-treatment periods
  sum(post^2) / sum(pre^2)
})

# p-value: fraction of placebos with ratio ≥ treated
p_value <- mean(mspe_ratios >= mspe_ratios["1"])
cat("MSPE ratio rank p-value:", p_value, "\n")
# p < 0.05 → significant effect
```

### In-Time Placebo

Apply SCM with a fake treatment date in the pre-treatment period. Effect should be near zero.

```r
# Use earlier fake treatment date
dp_placebo <- dataprep(foo = df, ...,
                       time.optimize.ssr = 1980:1989,  # shorter pre-period
                       time.plot = 1980:1999)           # only pre-treatment
so_placebo <- synth(dp_placebo)
# Gap should be ≈ 0 if model is well-specified
```

## Donor Pool Construction

| Guideline | Rationale |
|-----------|-----------|
| Exclude units affected by similar treatment | Avoids contamination |
| Include only structurally similar units | Improves fit quality |
| Use pre-treatment outcome lags as predictors | Most powerful predictors |
| Drop donors with zero weight and large pre-MSPE | Focus on contributing donors |
| Leave-one-out: iteratively drop each donor | Check weight sensitivity |

### Covariate Balance Check

After constructing the synthetic control, verify that predictors are balanced between the treated unit and its synthetic counterpart:

```r
# R — predictor balance check after synth()
synth_tab <- synth.tab(synth_out, dataprep_out)

# tab.pred: treated, synthetic control, and sample average for each predictor
print(synth_tab$tab.pred)
# Look for rows where treated and synthetic values are close (small gap)
# Large gaps in key predictors signal poor donor pool or predictor choice

# Compute RMSPE on predictor balance:
pred_balance <- synth_tab$tab.pred[, 1:2]  # treated vs synthetic
pred_gaps <- pred_balance[, 1] - pred_balance[, 2]
cat("Predictor balance (treated - synthetic):\n")
print(round(pred_gaps, 4))
```

```python
# Python — predictor balance after SparseSC or manual SCM
import numpy as np
import pandas as pd

# Treated unit predictor values (pre-treatment means)
treated_pred  = X_treated.mean(axis=0)
synthetic_pred = (weights @ X_donors).flatten()  # weights × donor covariates

balance_df = pd.DataFrame({
    'Predictor':  predictor_names,
    'Treated':    treated_pred,
    'Synthetic':  synthetic_pred,
    'Gap':        treated_pred - synthetic_pred,
    'Pct_Gap':    100 * (treated_pred - synthetic_pred) / np.abs(treated_pred)
})
print(balance_df.to_string(index=False))
# Flag predictors where |Pct_Gap| > 5% — consider adjusting donor pool
```

```stata
* Stata — predictor balance displayed automatically after synth
synth outcome gdp_pc trade_share inflation ///
    outcome(1995) outcome(1990) outcome(1985), ///
    trunit(1) trperiod(2000)
* The output table "Predictor Balance" compares treated vs synthetic vs sample avg
* Verify that treated and synthetic columns are close for key predictors
```

## Synthetic DID (Arkhangelsky et al. 2021)

Combines SCM weighting with DID estimation; works with multiple treated units.

```r
# R — Synthetic DID
library(synthdid)

# Data must be a balanced panel in matrix form
setup <- panel.matrices(df, unit = "unit_id", time = "year",
                        outcome = "outcome", treatment = "treated")
sdid <- synthdid_estimate(setup$Y, setup$N0, setup$T0)
se <- sqrt(vcov(sdid, method = "placebo"))
cat("SDID estimate:", sdid, "SE:", se, "\n")
plot(sdid)
```

```python
# Python — synthdid
# pip install synthdid
from synthdid.model import SynthDID
model = SynthDID(df, unit='unit_id', time='year',
                 outcome='outcome', treatment='treated')
model.fit()
print(f"SDID ATT: {model.att():.4f}")
model.plot()
```

## Pre-Treatment Fit Diagnostics

Good pre-treatment fit is the foundation of SCM credibility. A poorly fitting synthetic control cannot be trusted as a counterfactual.

**RMSPE benchmark**: Pre-treatment RMSPE should generally be **< 5% of the treated unit's pre-treatment outcome mean**. Higher values suggest the synthetic control is unreliable; reconsider predictor selection or donor pool composition.

```r
# R — compute and assess pre-treatment RMSPE
# After synth() and dataprep():
gaps <- dataprep_out$Y1plot - (dataprep_out$Y0plot %*% synth_out$solution.w)

pre_periods  <- which(as.numeric(rownames(gaps)) < treatment_year)
post_periods <- which(as.numeric(rownames(gaps)) >= treatment_year)

pre_rmspe  <- sqrt(mean(gaps[pre_periods]^2))
post_rmspe <- sqrt(mean(gaps[post_periods]^2))
outcome_mean <- mean(dataprep_out$Y1plot[pre_periods])

cat(sprintf("Pre-treatment RMSPE: %.4f (%.1f%% of outcome mean)\n",
            pre_rmspe, 100 * pre_rmspe / outcome_mean))
cat(sprintf("Post-treatment RMSPE: %.4f\n", post_rmspe))
cat(sprintf("Post/Pre MSPE ratio: %.2f\n", (post_rmspe/pre_rmspe)^2))

# Rule of thumb: if pre-RMSPE > 5% of outcome mean, reconsider the design
if (pre_rmspe / outcome_mean > 0.05) {
  warning("Pre-treatment RMSPE exceeds 5% of outcome mean — fit may be poor.")
}
```

```python
# Python — pre-treatment fit visualization
import matplotlib.pyplot as plt
import numpy as np

years = np.array(all_years)
treated  = Y_actual          # actual treated unit outcomes
synthetic = Y_synthetic      # synthetic control outcomes
treatment_year = 2000

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Panel A: level plot
axes[0].plot(years, treated,   'k-',  linewidth=2,   label='Treated')
axes[0].plot(years, synthetic, 'r--', linewidth=1.5, label='Synthetic Control')
axes[0].axvline(treatment_year, color='gray', linestyle=':', linewidth=1)
axes[0].set_title('Treated vs Synthetic Control'); axes[0].legend()

# Panel B: gap plot with pre-period RMSPE annotation
gap = treated - synthetic
axes[1].plot(years, gap, 'b-', linewidth=2, label='Gap (τ̂)')
axes[1].axvline(treatment_year, color='gray', linestyle=':', linewidth=1)
axes[1].axhline(0, color='black', linestyle='-', linewidth=0.5)

pre_mask = years < treatment_year
pre_rmspe = np.sqrt(np.mean(gap[pre_mask]**2))
axes[1].set_title(f'Treatment Effect (Pre-RMSPE = {pre_rmspe:.3f})')
axes[1].legend()

plt.tight_layout()
plt.savefig('synthetic_control_fit.pdf', bbox_inches='tight')
```

```stata
* Stata — pre-treatment fit assessment
* After synth estimation, compute RMSPE manually:
* (synth stores results; use stored matrices)
matrix gaps = e(Y_treated) - e(Y_synthetic)

* Pre-treatment RMSPE:
* (Stata code depends on synth version; synth_runner automates this)
synth_runner outcome gdp_pc trade_share outcome(1995) outcome(1990), ///
    trunit(1) trperiod(2000) gen_vars
* Outputs pre_rmspe and post_rmspe in stored results
pval2 using synth_results   // rank-based p-value from synth_runner
```

## Reporting Standards

1. **Pre-treatment fit**: Show treated vs synthetic control plot with clear pre-treatment match
2. **Gap plot**: Show treatment effect over time with vertical treatment line
3. **Donor weights table**: Report which units contribute to synthetic control and their weights
4. **Predictor balance table**: Compare treated, synthetic, and sample average
5. **Placebo plot**: In-space placebos with treated unit highlighted
6. **MSPE ratio**: Report rank-based p-value (e.g., "treated unit ranks 1st of 20 units")
7. **Robustness**: Leave-one-out donor test, in-time placebo, alternative predictor sets

**Key sentence template**:
> "We construct a synthetic [unit] using a weighted combination of [N] donor [units] from the [donor pool description]. The synthetic [unit] closely tracks the treated [unit] in the pre-treatment period ([year range], pre-treatment MSPE = [value]). The estimated effect is [magnitude] ([% change]), with the treated unit ranking [1st/2nd] out of [N] units in post/pre-MSPE ratio (p = [value])."

## Common Pitfalls

- **Poor pre-treatment fit**: If pre-MSPE is large, the synthetic control is unreliable — reconsider predictor set or donor pool
- **Overfitting to noise**: Using too many outcome lags can overfit; use 3–5 evenly spaced lags
- **Interpolation bias**: SCM requires the treated unit to be within the convex hull of donors
- **Cherry-picking donors**: Always report full donor pool; justify exclusions

See `references/synthetic-control-reference.md` for multi-unit SCM extensions, staggered adoption SCM, and sensitivity analysis.

## Related Skills & Commands

- **did-analysis**: DID is the most common alternative; consider SCM when few treated units exist
- **matching**: Matching methods as complementary approach for causal inference
- **/robustness**: Generate additional robustness checks for SCM results
- **/method**: Write up the synthetic control methodology section
- **/plot**: Create publication-quality SCM plots
