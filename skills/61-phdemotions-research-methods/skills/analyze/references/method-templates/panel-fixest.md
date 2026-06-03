# Panel Regression with Fixed Effects (fixest)

> For panel/longitudinal data with entity and/or time fixed effects.

---

## R Pattern

```r
library(fixest)
library(modelsummary)

# Two-way fixed effects
model_fe <- feols(
  dv ~ iv + covariate | entity_id + time_period,
  data = panel_df,
  cluster = ~entity_id  # clustered SEs at entity level
)

# Summary with clustered SEs
summary(model_fe)

# Multiple specifications in one call
models <- feols(
  dv ~ csw(iv, iv + covariate1, iv + covariate1 + covariate2) | entity_id + time_period,
  data = panel_df,
  cluster = ~entity_id
)

# Publication table
modelsummary(
  models,
  stars = c("*" = .05, "**" = .01, "***" = .001),
  output = "output/tables/panel-results.docx"
)

# Diagnostics
# Within-variation check
fixest::demean(panel_df$iv, panel_df[, c("entity_id", "time_period")])

# Hausman test (FE vs RE)
model_re <- feols(dv ~ iv + covariate | entity_id, data = panel_df)
# Compare via Mundlak approach or Hausman test
```

## Python Pattern

```python
import linearmodels.panel as lp
import pandas as pd

# Set panel index
panel_df = panel_df.set_index(["entity_id", "time_period"])

# Fixed effects
model_fe = lp.PanelOLS.from_formula(
    "dv ~ iv + covariate + EntityEffects + TimeEffects",
    data=panel_df
).fit(cov_type="clustered", cluster_entity=True)

# Random effects
model_re = lp.RandomEffects.from_formula(
    "dv ~ 1 + iv + covariate",
    data=panel_df
).fit()
```

## Key Considerations

- fixest is dramatically faster than plm for large panels
- Always cluster SEs at the level of treatment assignment
- Report within-R² (not overall R²) for FE models
- Check for sufficient within-variation in key IVs
- Consider Conley SEs for spatial correlation
