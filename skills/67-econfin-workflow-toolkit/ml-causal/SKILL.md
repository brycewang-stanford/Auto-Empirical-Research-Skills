---
name: ml-causal
description: |
  Econometrics skill for machine learning methods in causal inference. Activates when the user asks about:
  "causal forest", "generalized random forest", "GRF", "double machine learning", "DML",
  "debiased machine learning", "LASSO for variable selection", "post-LASSO",
  "heterogeneous treatment effects", "CATE", "conditional average treatment effect",
  "BLP analysis", "CLAN analysis", "causal tree", "honest estimation",
  "因果森林", "双重机器学习", "异质性处理效应", "条件平均处理效应",
  "LASSO变量选择", "机器学习因果推断", "去偏机器学习"
---

# Machine Learning for Causal Inference Skill

This skill covers modern ML-based causal inference methods: Causal Forests (GRF) for heterogeneous treatment effects, Double/Debiased Machine Learning (DML) for partially linear models, and LASSO-based variable selection. These methods combine the flexibility of ML with the rigor of econometric identification.

## When to Use ML Causal Methods

| Goal | Method |
|------|--------|
| Estimate average treatment effect with many controls | Double ML (DML) |
| Discover treatment effect heterogeneity | Causal Forest (GRF) |
| Variable selection for high-dimensional controls | Post-LASSO |
| Best linear predictor of CATE | BLP analysis |
| Subgroup with largest/smallest effects | CLAN analysis |

**Key principle**: ML is used for **nuisance parameter estimation** (predicting Y and D), not for identifying causal effects directly. Identification still requires valid research design (RCT, IV, DID, etc.).

## Double/Debiased Machine Learning (DML)

Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey & Robins (2018)

### Partially Linear Model

```
Y = θ·D + g(X) + ε     (structural equation)
D = m(X) + v           (treatment equation)

θ = causal parameter of interest
g(X), m(X) = unknown nuisance functions estimated by ML
```

### DML Procedure

1. **Cross-fitting**: Split sample into K folds (typically K=5)
2. **Nuisance estimation**: On each fold k, use remaining folds to estimate ĝ(X) and m̂(X) using ML
3. **Residualize**: Compute Ỹ = Y − ĝ(X) and D̃ = D − m̂(X)
4. **Final estimation**: Regress Ỹ on D̃ to obtain θ̂

### R — DoubleML

```r
# R — DoubleML package
library(DoubleML)
library(mlr3)
library(mlr3learners)

# Define data
dml_data <- DoubleMLData$new(
  data = df,
  y_col = "outcome",
  d_cols = "treatment",
  x_cols = c("x1", "x2", "x3", "x4", "x5")
)

# Choose ML methods for nuisance estimation
ml_g <- lrn("regr.ranger", num.trees = 500)   # for E[Y|X]
ml_m <- lrn("classif.ranger", num.trees = 500) # for E[D|X]

# Fit DML (partially linear model)
dml_plr <- DoubleMLPLR$new(dml_data, ml_g, ml_m,
                            n_folds = 5, n_rep = 10)
dml_plr$fit()
print(dml_plr)
# Reports: coefficient, SE, t-stat, p-value, CI

# Interactive model (for CATE via DML)
dml_irm <- DoubleMLIRM$new(dml_data, ml_g, ml_m,
                            n_folds = 5, score = "ATE")
dml_irm$fit()
print(dml_irm)
```

### Python — DoubleML

```python
# Python — DoubleML
import doubleml as dml
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# Define data
dml_data = dml.DoubleMLData(
    df, y_col='outcome', d_cols='treatment',
    x_cols=['x1', 'x2', 'x3', 'x4', 'x5']
)

# Nuisance learners
ml_g = RandomForestRegressor(n_estimators=500, max_depth=5)
ml_m = RandomForestClassifier(n_estimators=500, max_depth=5)

# Partially Linear Regression
dml_plr = dml.DoubleMLPLR(dml_data, ml_g, ml_m,
                            n_folds=5, n_rep=10)
dml_plr.fit()
print(dml_plr.summary)

# Confidence interval
print(dml_plr.confint())
```

### Stata — ddml

```stata
* Stata — ddml (Ahrens et al. 2024)
ssc install ddml
ssc install pystacked

* Partially linear model with cross-fitting
ddml init partial, kfolds(5) reps(10)
ddml E[outcome]: pystacked outcome x1 x2 x3 x4 x5, ///
    type(reg) methods(rf gradboost lassocv)
ddml E[treatment]: pystacked treatment x1 x2 x3 x4 x5, ///
    type(class) methods(rf gradboost lassocv)
ddml crossfit
ddml estimate, robust
```

## Causal Forest (Generalized Random Forest)

Athey, Tibshirani & Wager (2019)

Estimates Conditional Average Treatment Effects (CATE): τ(x) = E[Y(1) − Y(0) | X = x]

### R — grf

```r
# R — Generalized Random Forest
library(grf)

# Prepare data
X <- as.matrix(df[, c("x1", "x2", "x3", "x4", "x5")])
Y <- df$outcome
W <- df$treatment

# Fit causal forest
cf <- causal_forest(X, Y, W,
                    num.trees = 4000,
                    honesty = TRUE,          # honest estimation
                    tune.parameters = "all") # auto-tune

# Average treatment effect (ATE)
ate <- average_treatment_effect(cf, target.sample = "all")
cat("ATE:", ate["estimate"], "SE:", ate["std.err"], "\n")

# ATT
att <- average_treatment_effect(cf, target.sample = "treated")
cat("ATT:", att["estimate"], "SE:", att["std.err"], "\n")

# Individual-level CATE predictions
cate <- predict(cf, estimate.variance = TRUE)
df$cate_hat <- cate$predictions
df$cate_se  <- sqrt(cate$variance.estimates)

# Variable importance
varimp <- variable_importance(cf)
names(varimp) <- colnames(X)
sort(varimp, decreasing = TRUE)
```

### Python — econml / grf

```python
# Python — EconML (Microsoft)
from econml.dml import CausalForestDML

# Fit causal forest via DML
cf = CausalForestDML(
    model_y=RandomForestRegressor(n_estimators=500),
    model_t=RandomForestClassifier(n_estimators=500),
    n_estimators=4000,
    cv=5,
    random_state=42
)
cf.fit(Y=df['outcome'].values,
       T=df['treatment'].values,
       X=df[['x1', 'x2', 'x3', 'x4', 'x5']].values)

# ATE
ate = cf.ate_inference()
print(f"ATE: {ate.mean_point:.4f} (SE: {ate.stderr_mean:.4f})")

# CATE predictions
cate = cf.effect(df[['x1', 'x2', 'x3', 'x4', 'x5']].values)
df['cate_hat'] = cate
```

## BLP Analysis (Best Linear Predictor)

Tests whether CATE varies with observables. From Chernozhukov, Demirer, Duflo & Fernandez-Val (2020).

```r
# R — BLP of CATE
library(grf)

# After fitting causal_forest cf:
blp <- best_linear_projection(cf, A = X)
print(blp)

# Interpretation:
# - Intercept: average effect
# - Coefficients: how CATE varies with each covariate
# - If all coefficients ≈ 0 → homogeneous treatment effect
```

## CLAN Analysis (Classification Analysis)

Identifies subgroups with highest/lowest treatment effects.

```r
# Sorted Group Average Treatment Effects (GATES)
# Split sample by predicted CATE quartiles
df$cate_quartile <- cut(df$cate_hat,
                         breaks = quantile(df$cate_hat, c(0, 0.25, 0.5, 0.75, 1)),
                         labels = c("Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"),
                         include.lowest = TRUE)

# GATES regression
library(fixest)
gates <- feols(outcome ~ i(cate_quartile, treatment),
               data = df, vcov = "HC1")
summary(gates)
# Significant difference between Q4 and Q1 → heterogeneity exists

# CLAN: compare characteristics across CATE quartiles
clan_table <- df %>%
  group_by(cate_quartile) %>%
  summarise(across(c(x1, x2, x3, age, income), mean))
print(clan_table)
```

## AIPW / Augmented IPW (Doubly Robust Estimator)

Combines outcome regression and propensity score weighting. **Doubly robust**: consistent if *either* the outcome model or the propensity score model is correctly specified (but not necessarily both). Particularly natural for binary treatment and binary/continuous outcomes.

**Estimator**:
```
τ_AIPW = E[ μ₁(X) − μ₀(X) + D(Y − μ₁(X))/e(X) − (1−D)(Y − μ₀(X))/(1−e(X)) ]
```
where μ_d(X) = E[Y|D=d, X] and e(X) = P(D=1|X) are estimated by ML.

**Difference from DML**: AIPW is more natural for binary treatment/outcome; DML is better suited for continuous treatment or partially linear structural models. Both use cross-fitting.

```python
# Python — AIPW / DR Learner (EconML)
from econml.dr import DRLearner
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegressionCV
import numpy as np

# Data preparation
Y = df['outcome'].values
T = df['treatment'].values          # binary: 0/1
X = df[['x1', 'x2', 'x3']].values

# DRLearner implements AIPW with cross-fitting for CATE estimation
dr_learner = DRLearner(
    model_propensity=LogisticRegressionCV(cv=5),   # propensity score e(X)
    model_regression=RandomForestRegressor(n_estimators=200),  # outcome μ_d(X)
    model_final=RandomForestRegressor(n_estimators=200),       # CATE model
    cv=5,
    random_state=42
)
dr_learner.fit(Y, T, X=X)

# ATE via AIPW
ate = dr_learner.ate_inference(X=X)
print(f"AIPW ATE: {ate.mean_point:.4f} (SE: {ate.stderr_mean:.4f})")
print(f"95% CI: {ate.conf_int_mean()}")

# CATE predictions
cate = dr_learner.effect(X)
```

```r
# R — AIPW using AIPW package
# install.packages("AIPW")
library(AIPW)
library(SuperLearner)

aipw_obj <- AIPW$new(
  Y = df$outcome,
  A = df$treatment,
  W = df[, c("x1", "x2", "x3")],
  Q.SL.library = c("SL.ranger", "SL.glm"),   # outcome model
  g.SL.library = c("SL.ranger", "SL.glm"),   # propensity model
  k_split = 5,       # cross-fitting folds
  verbose = FALSE
)
aipw_obj$fit()
aipw_obj$summary()
# Reports: ATE, RR, OR with 95% CI
```

## Meta-Learners for CATE Estimation

Meta-learners are general frameworks for estimating CATE that wrap any base ML model. They differ in how they use the treatment variable.

| Learner | Approach | Best When |
|---------|----------|-----------|
| **S-Learner** | Single model: fit μ(X, D), then CATE = μ(X,1) − μ(X,0) | Simple baseline; may shrink CATE to zero if D is weak signal |
| **T-Learner** | Two separate models: μ₁(X) and μ₀(X) | Unequal sample sizes; less regularization shrinkage on treatment |
| **X-Learner** | Imputes counterfactuals, then fits CATE on imputed residuals | Unbalanced treatment (very few treated or controls) |
| **R-Learner** | Residualizes Y and D, then fits CATE on residuals | High confounding; closely related to DML |

```python
# Python — Meta-Learners via EconML
from econml.metalearners import TLearner, SLearner, XLearner
from econml.dml import LinearDML
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import numpy as np

Y = df['outcome'].values
T = df['treatment'].values
X = df[['x1', 'x2', 'x3']].values

# --- T-Learner ---
t_learner = TLearner(models=RandomForestRegressor(n_estimators=500))
t_learner.fit(Y, T, X=X)
cate_t = t_learner.effect(X)
print(f"T-Learner ATE: {np.mean(cate_t):.4f}")

# --- S-Learner ---
s_learner = SLearner(overall_model=RandomForestRegressor(n_estimators=500))
s_learner.fit(Y, T, X=X)
cate_s = s_learner.effect(X)

# --- X-Learner ---
x_learner = XLearner(
    models=RandomForestRegressor(n_estimators=500),
    propensity_model=RandomForestClassifier(n_estimators=500)
)
x_learner.fit(Y, T, X=X)
cate_x = x_learner.effect(X)

# --- R-Learner (via LinearDML with non-parametric final stage) ---
r_learner = LinearDML(
    model_y=RandomForestRegressor(n_estimators=500),
    model_t=RandomForestClassifier(n_estimators=500),
    cv=5, random_state=42
)
r_learner.fit(Y, T, X=X, W=None)
cate_r = r_learner.effect(X)

# Compare ATE across meta-learners
print(f"S: {np.mean(cate_s):.4f} | T: {np.mean(cate_t):.4f} | "
      f"X: {np.mean(cate_x):.4f} | R: {np.mean(cate_r):.4f}")
```

```r
# R — X-Learner using grf building blocks
library(grf)

# Step 1: T-Learner stage
X_mat <- as.matrix(df[, c("x1", "x2", "x3")])
Y <- df$outcome; W <- df$treatment

rf1 <- regression_forest(X_mat[W==1, ], Y[W==1])  # treated
rf0 <- regression_forest(X_mat[W==0, ], Y[W==0])  # control

# Step 2: Impute counterfactuals
mu1 <- predict(rf1, X_mat)$predictions
mu0 <- predict(rf0, X_mat)$predictions

# Step 3: X-Learner imputed effects
D1 <- Y[W==1] - predict(rf0, X_mat[W==1,])$predictions  # treated: Y(1) - mu0
D0 <- predict(rf1, X_mat[W==0,])$predictions - Y[W==0]  # control: mu1 - Y(0)

# Step 4: Fit CATE models on imputed effects
tau1 <- regression_forest(X_mat[W==1,], D1)
tau0 <- regression_forest(X_mat[W==0,], D0)

# Step 5: Combine using propensity score
e_hat <- regression_forest(X_mat, W)$predictions  # propensity
cate_x <- e_hat * predict(tau0, X_mat)$predictions +
          (1 - e_hat) * predict(tau1, X_mat)$predictions
cat("X-Learner ATE:", mean(cate_x), "\n")
```

## LASSO for Variable Selection

### Post-LASSO (Belloni, Chernozhukov & Hansen 2014)

Use LASSO to select controls, then run OLS with selected variables.

```r
# R — Post-LASSO
library(hdm)

# Post-double-selection LASSO for ATE
pds <- rlassoEffect(x = X, y = Y, d = W, method = "double selection")
summary(pds)
# Reports: coefficient, SE, t-stat, CI
```

```python
# Python — Post-LASSO
from sklearn.linear_model import LassoCV
import statsmodels.api as sm

# Step 1: LASSO on Y ~ X to select controls
lasso_y = LassoCV(cv=5).fit(X, Y)
selected_y = np.where(lasso_y.coef_ != 0)[0]

# Step 2: LASSO on D ~ X to select controls
lasso_d = LassoCV(cv=5).fit(X, W)
selected_d = np.where(lasso_d.coef_ != 0)[0]

# Step 3: Union of selected variables
selected = np.union1d(selected_y, selected_d)

# Step 4: OLS with selected controls
X_selected = sm.add_constant(np.column_stack([W, X[:, selected]]))
ols_result = sm.OLS(Y, X_selected).fit(cov_type='HC1')
print(f"Post-LASSO ATE: {ols_result.params[1]:.4f} (SE: {ols_result.bse[1]:.4f})")
```

```stata
* Stata — Post-double-selection LASSO
ssc install lassopack

* pdslasso: post-double-selection
pdslasso outcome treatment (x1-x50), robust
```

## Diagnostics and Validation

### Calibration Test for Causal Forest

```r
# Test forest calibration: does the forest detect heterogeneity?
calibration <- test_calibration(cf)
print(calibration)
# Row 1 (mean forest prediction): should be significant → forest detects an effect
# Row 2 (differential forest prediction): significant → heterogeneity exists
```

### Cross-Validated Performance

```r
# Out-of-bag predictions (built into grf)
oob_predictions <- predict(cf)$predictions  # uses OOB by default
cor(oob_predictions, df$true_cate)  # if true CATE known (simulation)
```

## Reporting Standards

1. **Method description**: State the ML method used for nuisance estimation (RF, LASSO, boosting)
2. **Cross-fitting**: Report number of folds (K) and repetitions
3. **ATE with CI**: Report point estimate, SE, 95% CI
4. **Heterogeneity evidence**: BLP table, GATES plot, variable importance
5. **Robustness**: Compare DML with different ML methods; compare GRF with traditional subgroup analysis

**Key sentence template (DML)**:
> "We estimate the treatment effect using Double Machine Learning (Chernozhukov et al. 2018) with random forests for nuisance estimation, 5-fold cross-fitting, and 10 repetitions. The estimated ATE is [β] (SE = [se], 95% CI: [lb, ub])."

**Key sentence template (Causal Forest)**:
> "We estimate heterogeneous treatment effects using a causal forest (Athey et al. 2019) with [N] trees and honest splitting. The calibration test confirms significant heterogeneity (p = [p]). Units in the top quartile of predicted CATE have an estimated effect of [β_Q4] compared to [β_Q1] in the bottom quartile."

## Common Pitfalls

- **Using ML for identification**: ML estimates nuisance parameters, not causal effects. You still need exogenous variation (RCT, IV, etc.)
- **Overfitting CATE**: Always use honest estimation (separate splitting and estimation samples)
- **Interpreting variable importance causally**: Variable importance in GRF shows predictive power for heterogeneity, not causal mediation
- **Ignoring cross-fitting**: Without cross-fitting, DML estimates are biased

See `references/ml-causal-reference.md` for IV-based causal forests, DML with IV, and simulation studies.

## Related Skills & Commands

- **iv-estimation**: DML can be combined with IV for endogenous treatment
- **did-analysis**: ML methods can complement DID for heterogeneity analysis
- **matching**: AIPW is closely related to DML
- **/robustness**: Compare ML-based and traditional estimates
- **/diagnose**: Check model diagnostics after estimation
