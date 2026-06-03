# Mixed / Multilevel Models (lme4)

> For nested/hierarchical data: students in classrooms, employees in firms, repeated measures.

---

## R Pattern

```r
library(lme4)
library(lmerTest)  # provides p-values via Satterthwaite
library(easystats)
library(modelsummary)

# Check ICC first — does multilevel structure matter?
library(performance)
null_model <- lmer(dv ~ 1 + (1 | group_id), data = df)
icc(null_model)  # ICC > .05 justifies multilevel

# Random intercepts
model_ri <- lmer(
  dv ~ iv + covariate + (1 | group_id),
  data = df
)

# Random intercepts and slopes
model_rs <- lmer(
  dv ~ iv + covariate + (1 + iv | group_id),
  data = df
)

# Compare models
anova(model_ri, model_rs)  # likelihood ratio test
compare_performance(model_ri, model_rs)

# Assumption checks
check_model(model_rs)
check_normality(model_rs)       # residual normality
check_heteroscedasticity(model_rs)

# Results
model_parameters(model_rs, effects = "fixed")
model_parameters(model_rs, effects = "random")
r2(model_rs)  # marginal and conditional R²

# Publication table
modelsummary(
  list("Random Intercept" = model_ri, "Random Slope" = model_rs),
  stars = c("*" = .05, "**" = .01, "***" = .001),
  output = "output/tables/mixed-model-results.docx"
)


# --- Generalized Linear Mixed Models ---
# Binary DV with nesting
model_glmm <- glmer(
  binary_dv ~ iv + covariate + (1 | group_id),
  data = df,
  family = binomial
)
```

## Python Pattern

```python
import statsmodels.formula.api as smf

# Random intercepts
model_ri = smf.mixedlm(
    "dv ~ iv + covariate",
    data=df,
    groups=df["group_id"]
).fit()

# Random intercepts and slopes
model_rs = smf.mixedlm(
    "dv ~ iv + covariate",
    data=df,
    groups=df["group_id"],
    re_formula="~iv"
).fit()
```

## Key Considerations

- Report ICC to justify the multilevel approach
- Report both marginal R² (fixed effects only) and conditional R² (fixed + random)
- With < 20 groups, random effects variance estimates are unreliable
- Convergence warnings are common — try different optimizers (`bobyqa`, `nloptwrap`) before simplifying the random effects structure
- Centering predictors (group-mean centering for Level 1, grand-mean for Level 2) aids interpretation
- Use `lmerTest` for Satterthwaite degrees of freedom (conservative, recommended)
