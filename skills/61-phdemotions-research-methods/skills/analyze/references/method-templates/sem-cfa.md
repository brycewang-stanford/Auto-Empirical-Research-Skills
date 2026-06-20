# SEM / CFA (lavaan)

> Structural equation modeling, confirmatory factor analysis, path analysis.

---

## R Pattern

```r
library(lavaan)
library(easystats)
library(semPlot)

# --- CFA: Measurement Model ---
cfa_model <- '
  # Latent factors
  brand_auth =~ ba1 + ba2 + ba3 + ba4
  purch_int  =~ pi1 + pi2 + pi3
  perc_value =~ pv1 + pv2 + pv3 + pv4
'

cfa_fit <- cfa(
  cfa_model,
  data = df,
  estimator = "MLR",  # robust to non-normality
  std.lv = TRUE       # standardize latent variances
)

# Fit indices
fitMeasures(cfa_fit, c("chisq", "df", "pvalue", "cfi", "tli", "rmsea",
                         "rmsea.ci.lower", "rmsea.ci.upper", "srmr"))

# Benchmarks: CFI ≥ .95, TLI ≥ .95, RMSEA ≤ .06, SRMR ≤ .08

# Factor loadings
standardizedSolution(cfa_fit) |>
  dplyr::filter(op == "=~")

# Modification indices (review, don't blindly apply)
modindices(cfa_fit, sort = TRUE, minimum.value = 10)

# Reliability
library(semTools)
reliability(cfa_fit)  # omega, alpha from CFA

# Discriminant validity: AVE vs squared correlations
# AVE for each factor should exceed squared inter-factor correlations


# --- SEM: Full Structural Model ---
sem_model <- '
  # Measurement model
  brand_auth =~ ba1 + ba2 + ba3 + ba4
  purch_int  =~ pi1 + pi2 + pi3
  perc_value =~ pv1 + pv2 + pv3 + pv4

  # Structural paths
  perc_value ~ a*brand_auth           # a path
  purch_int  ~ b*perc_value + c*brand_auth  # b and c (direct) paths

  # Indirect effect
  indirect := a*b
  total    := c + a*b
'

sem_fit <- sem(
  sem_model,
  data = df,
  estimator = "MLR",
  se = "bootstrap",
  bootstrap = 5000
)

# Results
summary(sem_fit, fit.measures = TRUE, standardized = TRUE, ci = TRUE)
parameterEstimates(sem_fit, boot.ci.type = "bca.simple", standardized = TRUE)

# Path diagram
semPaths(sem_fit, what = "std", layout = "tree2",
         edge.label.cex = 1.2, sizeMan = 8, sizeLat = 12)


# --- Multi-Group SEM (Measurement Invariance) ---
# Configural invariance
config <- cfa(cfa_model, data = df, group = "condition", estimator = "MLR")

# Metric invariance (equal loadings)
metric <- cfa(cfa_model, data = df, group = "condition", estimator = "MLR",
              group.equal = "loadings")

# Scalar invariance (equal loadings + intercepts)
scalar <- cfa(cfa_model, data = df, group = "condition", estimator = "MLR",
              group.equal = c("loadings", "intercepts"))

# Compare
anova(config, metric, scalar)
# ΔCFI < .010 suggests invariance holds (Cheung & Rensvold, 2002)
```

## Python Pattern

```python
import semopy

# Define model
model_desc = """
brand_auth =~ ba1 + ba2 + ba3 + ba4
purch_int  =~ pi1 + pi2 + pi3
perc_value =~ pv1 + pv2 + pv3 + pv4

perc_value ~ brand_auth
purch_int  ~ perc_value + brand_auth
"""

model = semopy.Model(model_desc)
model.fit(df)
model.inspect()

# Note: semopy is less mature than lavaan. For complex SEM,
# R/lavaan is strongly preferred.
```

## Key Considerations

- Always start with CFA before SEM — confirm measurement model first
- Use MLR estimator if Mardia's test suggests multivariate non-normality
- Bootstrap CIs (5000 draws, BCa) for indirect effects
- Report standardized AND unstandardized estimates
- Modification indices > 10 warrant inspection but require theoretical justification to apply
- Heywood cases (negative variances, loadings > 1.0) indicate model misspecification
- With ordinal indicators (e.g., 5-point Likert), consider WLSMV estimator
