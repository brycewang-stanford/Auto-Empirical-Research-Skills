# ML for Causal Inference — Detailed Reference

## DML with Instrumental Variables

### Partially Linear IV Model

```
Y = θ·D + g(X) + ε
D = m(X) + π·Z + v
```

```r
# R — DML-IV with DoubleML
library(DoubleML)
library(mlr3learners)

dml_data <- DoubleMLData$new(
  data = df,
  y_col = "outcome",
  d_cols = "treatment",
  z_cols = "instrument",
  x_cols = c("x1", "x2", "x3")
)

ml_g <- lrn("regr.ranger", num.trees = 500)
ml_m <- lrn("regr.ranger", num.trees = 500)
ml_r <- lrn("regr.ranger", num.trees = 500)

dml_pliv <- DoubleMLPLIV$new(dml_data, ml_g, ml_m, ml_r,
                              n_folds = 5, n_rep = 10)
dml_pliv$fit()
print(dml_pliv)
```

```python
# Python — DML-IV
from doubleml import DoubleMLPLIV

dml_data = dml.DoubleMLData(
    df, y_col='outcome', d_cols='treatment',
    z_cols='instrument', x_cols=['x1', 'x2', 'x3']
)
dml_pliv = DoubleMLPLIV(dml_data, ml_g, ml_m, ml_r,
                         n_folds=5, n_rep=10)
dml_pliv.fit()
print(dml_pliv.summary)
```

## Instrumental Forest (GRF)

```r
# R — Instrumental forest
library(grf)

X <- as.matrix(df[, c("x1", "x2", "x3")])
Y <- df$outcome
W <- df$treatment
Z <- df$instrument

# Fit instrumental forest
ivf <- instrumental_forest(X, Y, W, Z,
                            num.trees = 4000,
                            honesty = TRUE)

# Local ATE
late <- average_treatment_effect(ivf, target.sample = "all")
cat("LATE:", late["estimate"], "SE:", late["std.err"], "\n")

# CLATE: conditional LATE
clate <- predict(ivf, estimate.variance = TRUE)
df$clate_hat <- clate$predictions
```

## Multi-Armed Treatment (Multiple Treatments)

```r
# R — Multi-arm causal forest
library(grf)

# W is a factor with multiple treatment levels
W_multi <- as.numeric(df$treatment_group)  # 0, 1, 2, ...
cf_multi <- multi_arm_causal_forest(X, Y, as.factor(W_multi),
                                      num.trees = 4000)

# Contrasts: each treatment vs control
ate_contrasts <- average_treatment_effect(cf_multi)
print(ate_contrasts)
```

## Sensitivity Analysis for DML

### Varying ML Methods

```r
# Compare different ML learners for nuisance estimation
learners <- list(
  "LASSO" = list(lrn("regr.cv_glmnet"), lrn("classif.cv_glmnet")),
  "Random Forest" = list(lrn("regr.ranger"), lrn("classif.ranger")),
  "Gradient Boosting" = list(lrn("regr.xgboost"), lrn("classif.xgboost"))
)

results <- data.frame()
for (name in names(learners)) {
  dml_plr <- DoubleMLPLR$new(dml_data, learners[[name]][[1]],
                              learners[[name]][[2]], n_folds = 5)
  dml_plr$fit()
  results <- rbind(results, data.frame(
    Method = name,
    Estimate = dml_plr$coef,
    SE = dml_plr$se
  ))
}
print(results)
# Estimates should be similar across ML methods if model is well-specified
```

## GATES (Sorted Group Average Treatment Effects)

Formal test from Chernozhukov, Demirer, Duflo & Fernandez-Val (2020).

```r
# Step 1: Split sample in half (auxiliary and main)
set.seed(42)
aux <- sample(1:nrow(df), nrow(df)/2)
main <- setdiff(1:nrow(df), aux)

# Step 2: Estimate CATE on auxiliary sample
cf_aux <- causal_forest(X[aux,], Y[aux], W[aux], num.trees = 4000)

# Step 3: Predict CATE on main sample
cate_main <- predict(cf_aux, X[main,])$predictions

# Step 4: Create CATE quartile groups
groups <- cut(cate_main, breaks = quantile(cate_main, c(0,.25,.5,.75,1)),
              labels = c("Q1","Q2","Q3","Q4"), include.lowest = TRUE)

# Step 5: GATES regression on main sample
df_main <- data.frame(Y = Y[main], W = W[main], group = groups)
gates_model <- lm(Y ~ W * group, data = df_main)
summary(gates_model)
```

## Survival Forests for Duration Data

```r
# R — survival forest (grf)
library(grf)

# For right-censored duration outcomes
sf <- survival_forest(X, Y_duration, censoring_indicator,
                       num.trees = 2000, honesty = TRUE)
survival_pred <- predict(sf)
```

## Simulation: Verifying CATE Recovery

```r
# Simulation to verify causal forest performance
set.seed(42)
n <- 5000
X <- matrix(rnorm(n * 5), n, 5)
tau_true <- X[,1] + 0.5 * X[,2]  # true CATE function
W <- rbinom(n, 1, 0.5)
Y <- 2 + tau_true * W + X[,3] + rnorm(n)

cf <- causal_forest(X, Y, W, num.trees = 4000, honesty = TRUE)
tau_hat <- predict(cf)$predictions

# Correlation between true and estimated CATE
cat("Correlation:", cor(tau_true, tau_hat), "\n")
# MSE
cat("MSE:", mean((tau_true - tau_hat)^2), "\n")
```

## Key Citations

- **DML**: Chernozhukov, Chetverikov, Demirer, Duflo, Hansen, Newey & Robins (2018), *Econometrics Journal*
- **Causal Forest**: Athey, Tibshirani & Wager (2019), *Annals of Statistics*
- **GRF framework**: Athey & Wager (2019), *Annals of Statistics*
- **GATES/CLAN/BLP**: Chernozhukov, Demirer, Duflo & Fernandez-Val (2020), *NBER Working Paper*
- **Post-LASSO**: Belloni, Chernozhukov & Hansen (2014), *Review of Economic Studies*
- **Honest estimation**: Athey & Imbens (2016), *PNAS*
- **DML-IV**: Chernozhukov et al. (2018), *Econometrics Journal*
- **ddml (Stata)**: Ahrens, Hansen, Schaffer & Wiemann (2024)

## Package Installation

```r
# R
install.packages(c("grf", "DoubleML", "mlr3", "mlr3learners", "hdm"))
```

```python
# Python
# pip install doubleml econml scikit-learn
```

```stata
* Stata
ssc install ddml
ssc install pystacked
ssc install lassopack
```
