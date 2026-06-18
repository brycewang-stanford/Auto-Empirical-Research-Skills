# Machine Learning in Stata

## Overview

Stata provides built-in lasso, elastic net, and cross-validation, plus user-written packages for trees and random forests.

---

## Lasso Regression

### Basic Lasso Commands

```stata
// Linear lasso
lasso linear price mpg weight length headroom trunk gear_ratio ///
    turn displacement

// Logistic lasso for binary outcomes
lasso logit foreign mpg weight length headroom trunk gear_ratio ///
    turn displacement

// Poisson lasso for count data
lasso poisson count_var predictor1 predictor2 predictor3
```

### Lambda Selection Methods

```stata
// Cross-validation (default, usually best)
lasso linear price mpg weight length headroom, selection(cv)

// Adaptive lasso (data-dependent penalties)
lasso linear price mpg weight length headroom, selection(adaptive)

// Plugin method (theory-based, faster)
lasso linear price mpg weight length headroom, selection(plugin)

// Custom number of folds
lasso linear price mpg weight length headroom, selection(cv, folds(10))

// Manually specify lambda grid
lasso linear price mpg weight length, lambda(0.1 0.5 1 5 10 50 100)
```

### Viewing Lasso Results

```stata
lasso linear price mpg weight length headroom trunk gear_ratio

lassocoef                        // Coefficients at selected lambda
lassocoef, display(nonzero)      // Only nonzero coefficients
lassocoef, display(all)          // All lambdas tried
lassocoef, standardized          // Standardized coefficients
lassoknots, display(nonzero)     // Coefficient path (which vars enter when)
cvplot                           // CV error vs lambda plot
predict price_pred               // Predictions at selected lambda
predict price_pred_alt, lambda(0.5)  // At specific lambda
```

### Practical Example

```stata
webuse lbw, clear

// Lasso logistic with factor variables and CV
lasso logit low age lwt i.race smoke ptl ht ui, selection(cv)
lassocoef
cvplot
predict prob_low
estat classification
```

---

## Elastic Net Regression

Elastic net combines lasso (L1) and ridge (L2) penalties. The alpha parameter controls the mix: alpha=1 is pure lasso, alpha=0 is pure ridge.

```stata
// Default alpha grid
elasticnet linear price mpg weight length headroom trunk

// Logistic elastic net
elasticnet logit foreign mpg weight length headroom trunk

// Custom alpha values
elasticnet linear price mpg weight length, alpha(0.1 0.3 0.5 0.7 0.9)

// With CV over all lambdas
elasticnet linear price mpg weight length, selection(cv, alllambdas)
```

**Use elastic net over lasso when:** predictors are highly correlated (lasso arbitrarily picks one from correlated group; elastic net keeps groups together).

---

## Cross-Validation

### With Lasso (Built-in)

```stata
// K-fold CV (default k=10)
lasso linear price mpg weight length headroom, selection(cv)
lasso linear price mpg weight length headroom, selection(cv, folds(5))

lassoknots              // CV results
cvplot                  // CV error curve
lassoknots, display(nonzero)  // Lambda that minimized CV error
```

### Manual Cross-Validation

```stata
set seed 12345
generate fold = mod(_n, 5) + 1

forvalues k = 1/5 {
    quietly regress price mpg weight if fold != `k'
    predict temp if fold == `k'
    // Calculate and accumulate MSE for this fold
    drop temp
}
```

### Lasso Goodness-of-Fit

```stata
lasso linear price mpg weight length headroom trunk
lassogof                    // In-sample fit
lassogof, postselection     // Post-selection OLS fit
lassogof, over(sample) postselection  // By train/test indicator
```

---

## Model Selection Criteria

### AIC and BIC in Stata

```stata
sysuse auto, clear

regress price mpg weight
estimates store model1
estat ic

regress price mpg weight length
estimates store model2
estat ic

regress price mpg weight length headroom trunk
estimates store model3
estat ic

// Compare all models (lower = better)
estimates stats model1 model2 model3
```

---

## Variable Selection with Lasso

### Double Selection for Inference

When you want lasso-based variable selection AND valid inference on a treatment variable, put the treatment variable outside parentheses and controls inside:

```stata
// Interested in effect of foreign on price; uncertain about controls
lasso linear price foreign (mpg weight length headroom trunk ///
    gear_ratio turn displacement)
lassocoef
```

### Post-Selection Inference

```stata
// After lasso, refit with OLS for valid standard errors
lasso linear price mpg weight length headroom trunk
lassocoef, display(nonzero)
// Refit with only selected variables
regress price mpg weight length

// Or use post-selection option
lassogof, postselection
```

### Variable Selection with Interactions

```stata
webuse lbw, clear
lasso logit low age lwt i.race smoke ptl ht ui ///
    c.age#c.lwt c.age#i.race c.lwt#i.race, selection(cv)
lassocoef, display(nonzero)
```

---

## Classification and Regression Trees (CART)

Stata does not have built-in CART. User-written packages are available:

```stata
// Install (check current availability)
ssc install tree

// Classification tree
tree classify foreign mpg weight length, prune

// Regression tree
tree regress price mpg weight length

tree display    // Structure
tree graph      // Plot

// Pruning with CV
tree regress price mpg weight length, maxdepth(10)
tree prune, cv
tree select optimal
```

---

## Random Forests

Requires user-written packages:

```stata
ssc install rforest

// Classification
rforest foreign mpg weight length headroom trunk, type(class) iter(500)

// Regression
rforest price mpg weight length headroom trunk, type(reg) iter(500)

// Key options:
// iter()     - number of trees
// mtry()     - predictors randomly sampled per split
// maxdepth() - maximum tree depth
```

### Variable Importance and OOB Error

```stata
rforest price mpg weight length headroom trunk, type(reg) iter(500)

// Variable importance
rforest, importance

// Out-of-bag error (built-in validation: ~37% of data unused per tree)
display "OOB MSE: " e(oob_mse)
display "OOB R-squared: " e(oob_r2)
```

---

## Train/Test Splits

### Creating Splits

```stata
sysuse auto, clear

// Random 80/20 split
set seed 12345
generate train = runiform() <= 0.8

// Stratified split (maintains outcome proportions)
bysort foreign: generate random2 = runiform()
by foreign: egen threshold = pctile(random2), p(80)
generate train_strat = (random2 <= threshold)

// Three-way split: 60/20/20
set seed 123
generate random = runiform()
generate sample = 1 if random <= 0.6
replace sample = 2 if random > 0.6 & random <= 0.8
replace sample = 3 if random > 0.8
label define samplelbl 1 "Train" 2 "Validation" 3 "Test"
label values sample samplelbl
```

---

## Prediction and Evaluation

### Making Predictions

```stata
// After lasso
lasso linear price mpg weight length headroom
predict price_lasso

// For classification
lasso logit foreign mpg weight length
predict prob_foreign          // Probability
predict class_foreign, pr     // Classification
```

### Evaluation Metrics

**Regression:**
```stata
generate squared_error = (price - price_pred)^2
summarize squared_error
scalar mse = r(mean)
scalar rmse = sqrt(mse)

generate abs_error = abs(price - price_pred)
summarize abs_error
scalar mae = r(mean)

correlate price price_pred
scalar r2_oos = r(rho)^2
```

**Classification:**
```stata
tab actual predicted                    // Confusion matrix
estat classification                    // Sensitivity, specificity, accuracy
roctab actual predicted_prob, graph     // ROC curve and AUC

// Brier score
generate brier = (actual - predicted_prob)^2
summarize brier
```

---

## Complete Workflow Examples

### Workflow 1: Basic Lasso Prediction

```stata
sysuse auto, clear
set seed 42
generate train = runiform() <= 0.8

// Fit on training data
lasso linear price mpg-gear_ratio if train, selection(cv)
lassocoef, display(nonzero)
cvplot

// Evaluate on test set
predict price_pred if !train
generate mse = (price - price_pred)^2 if !train
summarize mse
correlate price price_pred if !train
```

### Workflow 2: Classification Model Comparison

```stata
webuse lbw, clear
set seed 2024
generate random = runiform()
generate sample = cond(random <= 0.6, 1, cond(random <= 0.8, 2, 3))

// Fit candidates on training set
quietly logit low age lwt i.race smoke ptl ht ui if sample == 1
estimates store logit_full

quietly lasso logit low age lwt i.race smoke ptl ht ui ///
    if sample == 1, selection(cv)
estimates store lasso_cv

// Evaluate on validation set
foreach model in logit_full lasso_cv {
    estimates restore `model'
    predict p_`model' if sample == 2
    roctab low p_`model' if sample == 2
}

// Final evaluation on test set with best model
estimates restore lasso_cv
predict prob_test if sample == 3
roctab low prob_test if sample == 3, graph
estat classification if sample == 3
```

### Workflow 3: High-Dimensional Variable Selection

```stata
// Simulate: 50 predictors, only 5 truly relevant
clear all
set seed 1234
set obs 200
generate y = rnormal()
forvalues i = 1/5 {
    generate x`i' = rnormal()
    replace y = y + `i' * x`i' / 10
}
forvalues i = 6/50 {
    generate x`i' = rnormal()
}

generate train = (_n <= 150)
lasso linear y x1-x50 if train, selection(cv)
lassocoef, display(nonzero)   // Should select x1-x5

// Compare to OLS on test set
predict y_lasso if !train
generate mse_lasso = (y - y_lasso)^2 if !train

quietly regress y x1-x50 if train
predict y_ols if !train
generate mse_ols = (y - y_ols)^2 if !train

summarize mse_lasso mse_ols   // Lasso should win
```

### Workflow 4: Elastic Net Alpha Tuning

```stata
sysuse auto, clear
set seed 555
generate train = runiform() <= 0.75

local best_mse = 999999999
foreach a in 0.1 0.3 0.5 0.7 0.9 {
    quietly elasticnet linear price mpg weight length headroom ///
        if train, alpha(`a') selection(cv)
    predict p if !train
    quietly generate mse = (price - p)^2 if !train
    quietly summarize mse
    display "Alpha = `a', Test MSE = " r(mean)
    if r(mean) < `best_mse' {
        local best_mse = r(mean)
        local best_alpha = `a'
    }
    drop p mse
}

display "Best alpha: `best_alpha'"
elasticnet linear price mpg weight length headroom ///
    if train, alpha(`best_alpha') selection(cv)
```

### Workflow 5: K-Fold Model Comparison

```stata
sysuse auto, clear
set seed 100
local K = 5
generate fold = mod(_n - 1, `K') + 1
matrix results = J(3, `K', .)
matrix rownames results = OLS Lasso ElasticNet

forvalues k = 1/`K' {
    // OLS
    quietly regress price mpg weight length if fold != `k'
    predict p_ols if fold == `k'
    quietly generate mse = (price - p_ols)^2 if fold == `k'
    quietly summarize mse
    matrix results[1, `k'] = r(mean)
    drop p_ols mse

    // Lasso
    quietly lasso linear price mpg weight length headroom trunk ///
        if fold != `k', selection(cv)
    predict p_lasso if fold == `k'
    quietly generate mse = (price - p_lasso)^2 if fold == `k'
    quietly summarize mse
    matrix results[2, `k'] = r(mean)
    drop p_lasso mse

    // Elastic Net
    quietly elasticnet linear price mpg weight length headroom trunk ///
        if fold != `k', selection(cv)
    predict p_enet if fold == `k'
    quietly generate mse = (price - p_enet)^2 if fold == `k'
    quietly summarize mse
    matrix results[3, `k'] = r(mean)
    drop p_enet mse
}

matrix list results
mata: st_matrix("cv_means", mean(st_matrix("results")'))
matrix list cv_means
```

---

## Best Practices and Pitfalls

**General Guidelines:**
1. Always split data before any analysis; test set must never influence model building
2. Stata handles standardization automatically for lasso/elastic net
3. Start with lasso + default CV before elastic net or custom tuning
4. Check variable selection stability across different seeds
5. Don't over-tune on validation set

**Common Pitfalls:**
1. **Data leakage**: Don't standardize or select features using full dataset (including test)
2. **Training error underestimates true error**: Always report test/CV error
3. **Post-selection inference**: Lasso SEs are not valid for inference; use double-selection or refit with OLS on selected variables
4. ML needs adequate sample size; use simpler models when n is small

**Key Commands Summary:**

| Command | Purpose |
|---|---|
| `lasso linear/logit/poisson` | L1-regularized regression |
| `elasticnet linear/logit` | L1+L2 regularized regression |
| `lassocoef` | View selected coefficients |
| `lassoknots` | View lambda path |
| `cvplot` | Plot CV error curve |
| `lassogof` | Goodness-of-fit measures |
| `predict` | Generate predictions |
| `estimates store/stats` | Compare models via AIC/BIC |
| `rforest` (user-written) | Random forests |
