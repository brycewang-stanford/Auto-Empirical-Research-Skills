# Synthetic Control — Detailed Reference

## Multi-Unit SCM Extensions

When multiple units receive treatment at the same time, extend SCM by:

### Pooled SCM

Estimate SCM separately for each treated unit, then average effects.

```r
# Average effect across multiple treated units
effects <- list()
for (treated_id in treated_units) {
  dp <- dataprep(foo = df, ...,
                 treatment.identifier = treated_id,
                 controls.identifier = setdiff(all_units, treated_units))
  so <- synth(dp)
  effects[[as.character(treated_id)]] <- dp$Y1plot - dp$Y0plot %*% so$solution.w
}
avg_effect <- Reduce("+", effects) / length(effects)
```

### Penalized SCM (Abadie & L'Hour 2021)

Adds a penalty to prevent extreme weights and allows for multiple treated units.

```r
# R — penalized SCM via augsynth
library(augsynth)
pscm <- augsynth(outcome ~ treatment,
                 unit = unit_id, time = year,
                 data = df,
                 progfunc = "None",
                 scm = TRUE,
                 lambda = 1e-6)   # regularization parameter
summary(pscm)
```

## Staggered Adoption SCM

When units adopt treatment at different times:

```r
# R — staggered SCM with augsynth
library(augsynth)

# multisynth handles staggered treatment timing
msyn <- multisynth(outcome ~ treatment,
                   unit = unit_id, time = year,
                   data = df,
                   n_leads = 10)    # post-treatment periods
summary(msyn)
plot(msyn)

# Individual and average treatment effects
print(msyn)
```

## Conformal Inference for SCM (Chernozhukov et al. 2021)

Provides valid p-values and confidence intervals without permutation.

```r
# R — conformal inference
library(augsynth)

asyn <- augsynth(outcome ~ treatment,
                 unit = unit_id, time = year,
                 data = df)
# Conformal p-values
conformal_test <- inference(asyn, type = "conformal")
print(conformal_test)
```

## Sensitivity Analysis

### Pre-Treatment Fit Diagnostics

```r
# Root Mean Squared Prediction Error (pre-treatment)
pre_mspe <- sqrt(synth_out$loss.w)
cat("Pre-treatment RMSPE:", pre_mspe, "\n")

# Visual: compare predictor values
synth.tab <- synth.tab(synth_out, dataprep_out)
print(synth.tab$tab.pred)  # Treated vs Synthetic vs Sample Mean
```

### Leave-One-Out Donor Test

```r
# Drop each donor with positive weight and re-estimate
donors_with_weight <- which(synth_out$solution.w > 0.01)
loo_effects <- list()

for (d in donors_with_weight) {
  controls_loo <- setdiff(controls, d)
  dp_loo <- dataprep(foo = df, ...,
                     controls.identifier = controls_loo)
  so_loo <- synth(dp_loo)
  loo_effects[[as.character(d)]] <- dp_loo$Y1plot - dp_loo$Y0plot %*% so_loo$solution.w
}
# Plot LOO results alongside main estimate
```

### Alternative Predictor Sets

```r
# Test robustness to predictor choice
predictor_sets <- list(
  base = c("gdp_pc", "trade_share"),
  extended = c("gdp_pc", "trade_share", "inflation", "population"),
  minimal = c("gdp_pc")
)

for (name in names(predictor_sets)) {
  dp <- dataprep(foo = df, predictors = predictor_sets[[name]], ...)
  so <- synth(dp)
  cat(name, ": avg post-treatment effect =",
      mean(dp$Y1plot[(T0+1):T] - (dp$Y0plot %*% so$solution.w)[(T0+1):T]), "\n")
}
```

## Matrix Completion Methods (Athey et al. 2021)

Alternative to SCM that uses nuclear norm minimization.

```r
# R — matrix completion via augsynth
library(augsynth)
mc <- augsynth(outcome ~ treatment,
               unit = unit_id, time = year,
               data = df,
               progfunc = "MCPanel",
               scm = FALSE)
summary(mc)
```

## Comparison: SCM vs DID vs SDID

| Feature | SCM | DID | SDID |
|---------|-----|-----|------|
| Number of treated units | 1 (typically) | Many | Many |
| Parallel trends required | No | Yes | Relaxed |
| Unit weights | Data-driven | Equal | Data-driven |
| Time weights | None | Equal | Data-driven |
| Covariates | Via predictors | As controls | As controls |
| Inference | Permutation | Standard/cluster | Placebo/jackknife |

## Key Citations

- **Original SCM**: Abadie & Gardeazabal (2003), *American Economic Review*
- **Formal framework**: Abadie, Diamond & Hainmueller (2010), *JASA*
- **Inference**: Abadie, Diamond & Hainmueller (2015), *American Journal of Political Science*
- **Augmented SCM**: Ben-Michael, Feller & Rothstein (2021), *JASA*
- **Synthetic DID**: Arkhangelsky, Athey, Hirshberg, Imbens & Wager (2021), *AER*
- **Penalized SCM**: Abadie & L'Hour (2021), *JASA*
- **Matrix completion**: Athey, Bayati, Doudchenko, Imbens & Khosravi (2021), *JASA*
- **Conformal inference**: Chernozhukov, Wüthrich & Zhu (2021), *Annals of Statistics*
- **Practical guide**: Abadie (2021), *Journal of Economic Literature*

## Package Installation

```r
# R
install.packages(c("Synth", "augsynth", "synthdid"))
# For augsynth:
# remotes::install_github("ebenmichael/augsynth")
```

```python
# Python
# pip install SparseSC
# pip install synthdid
```

```stata
* Stata
ssc install synth
ssc install synth_runner
```
