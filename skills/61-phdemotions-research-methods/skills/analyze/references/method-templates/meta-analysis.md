# Meta-Analysis (metafor)

> Quantitative synthesis of effect sizes across studies.

---

## R Pattern

```r
library(metafor)
library(modelsummary)

# --- Effect Size Computation ---
# From means and SDs (two groups)
es <- escalc(measure = "SMD",  # standardized mean difference (Hedges' g)
             m1i = mean_treatment, sd1i = sd_treatment, n1i = n_treatment,
             m2i = mean_control,   sd2i = sd_control,   n2i = n_control,
             data = studies_df)

# From correlations
es_r <- escalc(measure = "ZCOR",  # Fisher's z-transformed r
               ri = correlation, ni = sample_size,
               data = studies_df)


# --- Random-Effects Model ---
model_re <- rma(yi, vi, data = es, method = "REML")
summary(model_re)

# Key output: overall effect, CI, Q-test (heterogeneity), I², tau²

# Prediction interval (where future effects might fall)
predict(model_re)


# --- Forest Plot ---
forest(model_re,
       slab = studies_df$study_label,
       xlab = "Standardized Mean Difference",
       header = TRUE)


# --- Heterogeneity Assessment ---
# Q-test: significant → substantial heterogeneity
# I²: percentage of variability due to true heterogeneity (not sampling error)
#   25% = low, 50% = moderate, 75% = high (Higgins et al., 2003)
# tau²: absolute amount of true heterogeneity


# --- Moderator Analysis (Meta-Regression) ---
model_mod <- rma(yi, vi,
                 mods = ~ study_design + sample_type + publication_year,
                 data = es,
                 method = "REML")
summary(model_mod)


# --- Publication Bias ---
# Funnel plot
funnel(model_re)

# Egger's regression test
regtest(model_re)

# Trim-and-fill
trimfill(model_re)

# P-curve (if applicable)
# Selection models
selmodel(model_re, type = "stepfun")


# --- Subgroup Analysis ---
model_subgroup <- rma(yi, vi, data = es, subset = (study_design == "experimental"))


# --- Sensitivity: Leave-One-Out ---
leave1out(model_re)

# Influence diagnostics
influence(model_re)
```

## Python Pattern

```python
# Python meta-analysis ecosystem is less mature.
# For serious meta-analysis, R/metafor is strongly preferred.

# Basic approach with statsmodels:
import numpy as np
# Manual random-effects via DerSimonian-Laird
# Or use the PyMARE package if available
```

## Key Considerations

- Always specify the effect size metric and ensure consistency across studies
- REML is preferred for random-effects estimation (less biased than DL)
- Report: overall effect with CI, Q-test, I², tau², prediction interval
- Funnel plot + Egger's test are minimum publication bias checks
- Moderator analyses should be pre-registered when possible
- With < 10 studies, heterogeneity estimates are unreliable — interpret cautiously
- Report both random-effects (generalizable) and fixed-effects (conditional) if reviewers expect it
- Use Hedges' g (not Cohen's d) for small-sample bias correction
