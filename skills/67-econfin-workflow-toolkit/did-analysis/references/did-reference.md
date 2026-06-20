# DID Analysis — Detailed Reference

## Triple Difference (DDD)

Adds a third source of variation to strengthen identification.

```
Y_igt = β₀ + β₁·T_g + β₂·P_t + β₃·D_i + β₄·T_g×P_t + β₅·T_g×D_i
        + β₆·P_t×D_i + β₇·(T_g×P_t×D_i) + ε_igt

β₇ = DDD estimate
```

```stata
reg y treat##post##subgroup, cluster(entity_id)
```

```r
lm(y ~ treat * post * subgroup, data = df)
```

**Use DDD when**: there's a sub-group within treatment and control groups that should be differentially affected; strengthens exclusion restriction.

## Heterogeneous Treatment Effects

### By subgroup

```r
# Interaction with moderator
feols(y ~ i(post_treat, moderate_var) | entity_id + year,
      data = df, cluster = ~entity_id)
```

### Quantile Treatment Effects

```r
library(quantreg)
rq(y ~ treat_post + factor(entity_id) + factor(year),
   tau = c(0.25, 0.5, 0.75), data = df)
```

## Synthetic Control Method

Use when a single treated unit and many control units exist (e.g., country-level policy).

```r
library(Synth)
dataprep_out <- dataprep(
  foo = df,
  predictors = c("x1", "x2"),
  predictors.op = "mean",
  time.predictors.prior = 1990:1999,
  special.predictors = list(
    list("y", 1998:1999, "mean")
  ),
  dependent = "y",
  unit.variable = "country_id",
  unit.names.variable = "country",
  time.variable = "year",
  treatment.identifier = 1,
  controls.identifier = 2:20,
  time.optimize.ssr = 1990:1999,
  time.plot = 1990:2010
)
synth_out <- synth(dataprep_out)
path.plot(synth_out, dataprep_out)
gaps.plot(synth_out, dataprep_out)
```

## Bacon Decomposition (Diagnosing TWFE Bias in Staggered Design)

```r
library(bacondecomp)
bacon_decomp <- bacon(y ~ treat_post, data = df,
                      id_var = "entity_id", time_var = "year")
ggplot(bacon_decomp) +
  aes(x = weight, y = estimate, color = type) +
  geom_point() +
  labs(title = "Bacon Decomposition")
```

If the "Treated vs Already Treated" weight is substantial and estimates differ widely, TWFE is unreliable → switch to Callaway-Sant'Anna.

## Anticipation Effects

If agents anticipate treatment and adjust behavior before it occurs:

```r
# Extend pre-period window to check for anticipation
feols(y ~ i(rel_time, treat, ref = c(-1, -2)) | entity_id + year,
      data = df)
# If t-2 or earlier coefficients are significant → anticipation present
```

**Remedies**:
- Extend "clean" pre-period by excluding anticipation window
- Use Callaway-Sant'Anna with `anticipation = 1` argument

## Parallel Trends Formal Tests

```r
# Pre-trend test: joint test that all pre-treatment coefficients = 0
library(fixest)
es <- feols(y ~ i(rel_time, treat, ref = -1) | entity_id + year,
            data = df, cluster = ~entity_id)

# Extract pre-period coefficients
pre_coefs <- which(grepl("rel_time::-[2-9]|rel_time::-1[0-9]", names(coef(es))))
wald(es, keep = names(coef(es))[pre_coefs])
```

## Spillover / SUTVA Testing

SUTVA (Stable Unit Treatment Value Assumption) requires no spillovers between units.

1. **Geographic buffer**: drop units near treated units from control group
2. **Check**: do control units near treatment show pre/post changes?

```r
# Compare DID estimates with and without near-neighbor controls
df_no_spillover <- df %>% filter(distance_to_treatment > threshold)
```

## Borusyak-Jaravel-Spiess Imputation Estimator

An alternative to Callaway-Sant'Anna that uses imputation for staggered DID.

```r
# R — Borusyak, Jaravel & Spiess (2024) imputation estimator
library(didimputation)

did_imp <- did_imputation(
  data = df,
  yname = "outcome",
  gname = "cohort_year",    # first treatment year (0 or Inf if never treated)
  tname = "year",
  idname = "entity_id",
  first_stage = ~ 0 | entity_id + year  # FE specification
)
summary(did_imp)

# Event study
did_imp_es <- did_imputation(
  data = df,
  yname = "outcome",
  gname = "cohort_year",
  tname = "year",
  idname = "entity_id",
  horizon = TRUE,             # event study
  pretrends = -5:-1           # pre-treatment horizons
)
plot(did_imp_es)
```

```stata
* Stata — did_imputation (Borusyak et al.)
ssc install did_imputation

did_imputation outcome entity_id year cohort_year, ///
    horizons(0/5) pretrends(5) minn(0)
event_plot, default_look
```

**Advantages over CS/SA**: More efficient (uses all clean controls), directly handles covariates, natural event study output.

## de Chaisemartin & D'Haultfoeuille Estimator

Robust to heterogeneous treatment effects with staggered adoption.

```r
# R — de Chaisemartin & D'Haultfoeuille (2020)
# install.packages("DIDmultiplegt")
library(DIDmultiplegt)

result <- did_multiplegt(
  df = df,
  Y = "outcome",
  G = "entity_id",
  T = "year",
  D = "treatment",
  placebo = 3,          # number of placebo tests
  dynamic = 5,          # number of dynamic effects
  brep = 100,           # bootstrap replications for SE
  cluster = "entity_id"
)
```

```stata
* Stata — did_multiplegt
ssc install did_multiplegt

did_multiplegt outcome entity_id year treatment, ///
    placebo(3) dynamic(5) brep(100) cluster(entity_id)
```

## Roth (2022) Pre-Trends Power Analysis

Tests whether pre-trend tests have sufficient power to detect violations.

```r
# R — Pre-trends power analysis (Roth 2022)
# remotes::install_github("jonathandroth/pretrends")
library(pretrends)

# After estimating event study:
es <- feols(y ~ i(rel_time, treat, ref = -1) | entity_id + year,
            data = df, cluster = ~entity_id)

# Extract coefficients and variance-covariance matrix for pre-period
pre_coefs <- coef(es)[grep("rel_time::-", names(coef(es)))]
pre_vcov <- vcov(es)[grep("rel_time::-", names(coef(es))),
                      grep("rel_time::-", names(coef(es)))]

# Power analysis: could we detect a linear pre-trend of slope delta?
power_result <- pretrends(
  betahat = pre_coefs,
  sigma = pre_vcov,
  tVec = -5:-2,             # relative time periods
  referencePeriod = -1,
  deltagrid = seq(0, 0.1, by = 0.01)  # slopes to test
)
plot(power_result)
# If power is low for plausible slopes → pre-trends test is not very informative
```

**Key insight**: Failing to reject parallel trends ≠ parallel trends hold. Roth (2022) shows many DID studies have low power to detect violations.

## Honest DID (Rambachan & Roth 2023)

Sensitivity analysis for DID that relaxes parallel trends.

```r
# R — HonestDiD
# remotes::install_github("asheshrambachan/HonestDiD")
library(HonestDiD)

# After event study estimation:
honest_result <- HonestDiD::createSensitivityResults(
  betahat = coef(es),
  sigma = vcov(es),
  numPrePeriods = 5,
  numPostPeriods = 5,
  Mbarvec = seq(0, 0.05, by = 0.01)  # max deviation from linear trend
)
HonestDiD::createSensitivityPlot(honest_result)
```

## Key Citations for Methods

- **Classic DID**: Card & Krueger (1994) minimum wage paper
- **Parallel trends testing**: Angrist & Pischke (2009), *Mostly Harmless Econometrics*
- **Staggered DID bias**: Goodman-Bacon (2021), *Journal of Econometrics*
- **Callaway-Sant'Anna**: Callaway & Sant'Anna (2021), *Journal of Econometrics*
- **Sun-Abraham**: Sun & Abraham (2021), *Journal of Econometrics*
- **Imputation estimator**: Borusyak, Jaravel & Spiess (2024), *Review of Economic Studies*
- **de Chaisemartin-D'Haultfoeuille**: de Chaisemartin & D'Haultfoeuille (2020), *American Economic Review*
- **Pre-trends power**: Roth (2022), *American Economic Review: Insights*
- **Honest DID**: Rambachan & Roth (2023), *Review of Economic Studies*
- **Synthetic control**: Abadie, Diamond & Hainmueller (2010), *JASA*
