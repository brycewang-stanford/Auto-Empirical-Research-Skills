# Linear Regression in Stata

## The `regress` Command

```stata
regress depvar indepvars [if] [in] [weight] [, options]
```

```stata
sysuse auto, clear
regress price mpg weight foreign
regress price mpg weight, beta           // Standardized coefficients
regress price mpg weight, noconstant     // Suppress constant
regress price mpg weight, level(90)      // 90% confidence level
```

### Understanding Output

**ANOVA Table:** Model SS, Residual SS, F-statistic (tests overall model significance)

**Model Fit:** R-squared, Adjusted R-squared, Root MSE

**Coefficient Table:** Coef, Std.Err, t-stat, P>|t|, 95% CI

Each coefficient = change in Y per one-unit increase in X, holding other variables constant.

### Collinearity Detection
Stata automatically drops perfectly collinear variables (shown as "omitted").
```stata
estat vif            // VIF > 10 indicates problematic multicollinearity
```

---

## Post-Estimation Commands

### predict - Fitted Values and Diagnostics
```stata
regress price mpg weight foreign

predict price_hat                // Fitted values
predict residuals, residuals     // Residuals (y - yhat)
predict std_res, rstandard       // Standardized residuals
predict stud_res, rstudent       // Studentized (jackknifed) residuals
predict se_pred, stdp            // SE of prediction
predict se_fcst, stdf            // SE of forecast (includes residual variance)
predict cooksd, cooksd           // Cook's distance
predict leverage, leverage       // Hat values (leverage)
```

### margins - Marginal Effects
```stata
regress wage c.education##c.experience i.gender

margins, dydx(education)                              // Average marginal effect
margins, at(education=(12 16 20))                     // Predictions at values
margins gender                                         // Predictive margins by category
margins, dydx(education) at(experience=(5 10 15))     // Effect varies with experience
marginsplot                                            // Visualize
```

### estat - Diagnostic Tests
```stata
estat vif                 // Variance Inflation Factors
estat hettest             // Breusch-Pagan test (H0: homoskedasticity)
estat imtest, white       // White's test for heteroskedasticity
estat ovtest              // Ramsey RESET test (H0: no omitted variables)
```

### Storing and Comparing Models
```stata
estimates store model1
regress price mpg weight
estimates store model2
estimates table model1 model2, se stats(N r2 r2_a)
```

**`estimates table` valid options:** `b()` (format coefficients), `se()` (format SEs),
`star()` (significance stars, e.g. `star(.05 .01 .001)`), `stats()` (scalar statistics),
`modelwidth()` (column width). That is the complete set — `title()` is NOT a valid option
for `estimates table`. Use `esttab` from the `estout` package for richer formatting:

```stata
// esttab equivalent with title and more (requires: ssc install estout)
esttab model1 model2, se stats(N r2 r2_a) title("Price Models") star(* 0.05 ** 0.01 *** 0.001)
```
See `packages/estout.md` for full `esttab`/`estout` reference.

### Accessing Stored Results
```stata
ereturn list              // List all stored results
display e(r2)             // R-squared
matrix list e(b)          // Coefficient vector
```

---

## Robust Standard Errors

Corrects for heteroskedasticity. Coefficients unchanged; only SEs, t-stats, p-values change.

```stata
regress wage education experience, vce(robust)
// Also called Huber-White or sandwich estimators
```

**HC2/HC3 variants** (better for small samples):
```stata
regress y x, vce(hc2)
regress y x, vce(hc3)
```

---

## Clustered Standard Errors

For grouped/panel data where errors may be correlated within clusters.

```stata
regress test_score hours_studied class_size, vce(cluster school_id)
```

**Important considerations:**
- Need ~50+ clusters for reliable inference
- Clustered SEs are automatically robust to heteroskedasticity
- Assume independence BETWEEN clusters
- Can be larger or smaller than robust SEs depending on intra-cluster correlation sign

**Two-way clustering:**
```stata
ssc install reghdfe
reghdfe wage education experience, absorb(i.firm_id i.year) vce(cluster firm_id year)
```

---

## Weighted Regression

| Weight Type | Syntax | When to Use |
|-------------|--------|-------------|
| Frequency (`fweight`) | `[fweight=n]` | Aggregated data; each row = n identical obs |
| Analytic (`aweight`) | `[aweight=w]` | Variance proportional to 1/w; cell means, meta-analysis |
| Probability (`pweight`) | `[pweight=w]` | Survey data; w = 1/selection probability; auto-applies robust SEs |
| Importance (`iweight`) | `[iweight=w]` | Programming/intermediate calculations |

```stata
regress outcome predictor [aweight=n]
regress outcome predictor [pweight=survey_weight]
svyset [pweight=survey_weight]
svy: regress outcome predictor
```

---

## Instrumental Variables Regression

For endogenous regressors (correlated with error term). Instruments must be: (1) relevant (correlated with endogenous var) and (2) exogenous (uncorrelated with error).

```stata
ivregress estimator depvar [exog_vars] (endog_vars = instruments) [, options]
```

### 2SLS (most common)
```stata
ivregress 2sls wage experience (education = parent_education), first
// first: Shows first-stage regression

// Multiple instruments
ivregress 2sls wage experience (education = parent_ed sibling_ed)

// Multiple endogenous variables
ivregress 2sls y x1 (x2 x3 = z1 z2 z3)
```

**Critical:** All exogenous variables are automatically instruments. Don't omit them:
```stata
// WRONG: ivregress 2sls y (x1 = z)          -- missing exogenous x2
// RIGHT: ivregress 2sls y x2 (x1 = z)
```

### Other Estimators
```stata
ivregress liml wage experience (education = parent_ed), first   // Better with weak instruments
ivregress gmm wage experience (education = parent_ed), wmatrix(robust)  // Efficient under heteroskedasticity
```

### IV Diagnostics
```stata
ivregress 2sls wage experience (education = parent_ed sibling_ed), first

estat firststage       // First-stage F-stat (F > 10 = strong instruments)
estat endogenous       // Durbin-Wu-Hausman test (H0: variable is exogenous)
estat overid           // Sargan/Hansen test (H0: all instruments valid; requires overidentification)
```

**Don't manually do 2SLS** (first-stage predict then second-stage regress) -- standard errors will be wrong.

---

## Testing Coefficients

### test - Linear Restrictions (F-test)
```stata
regress wage education experience age

test education                        // H0: beta_education = 0
test education = 0.5                  // H0: beta = specific value
test education experience             // Joint test: both = 0
test education = experience           // H0: equal coefficients
test (education = experience) (age = 0)  // Multiple restrictions
```

### lincom - Linear Combinations (estimate + SE + CI)
```stata
lincom education + experience         // Sum of coefficients
lincom education - experience         // Difference
lincom 2*education + 3*experience     // Weighted combination
lincom _cons + 10*education           // Predicted value at education=10
```

### nlcom - Nonlinear Functions (delta method)
```stata
nlcom _b[x1]/_b[x2]                  // Ratio of coefficients
nlcom exp(_b[x1])                     // Exponentiated coefficient
nlcom (ratio: _b[x1]/_b[x2]) (product: _b[x1]*_b[x2])  // Multiple
```

### testnl - Nonlinear Restrictions
```stata
testnl _b[x1]/_b[x2] = 1            // H0: ratio = 1
```

| Need | Linear | Nonlinear |
|------|--------|-----------|
| p-value only | `test` | `testnl` |
| Estimate + SE + CI | `lincom` | `nlcom` |

---

## Interaction Terms

### Factor Variable Operators
```stata
i.varname       // Categorical indicators
c.varname       // Continuous (explicit)
var1#var2       // Interaction only
var1##var2      // Main effects AND interaction
```

### Continuous x Continuous
```stata
regress wage c.education##c.experience
// Effect of education: beta1 + beta3*experience

margins, dydx(education) at(experience=(5 10 15 20))
marginsplot
```

### Categorical x Continuous
```stata
regress wage i.gender##c.education
// Allows different slopes per gender
// beta3 = difference in returns to education between groups

margins gender, at(education=(8(2)20))
marginsplot    // Separate slopes per gender
```

### Categorical x Categorical
```stata
regress wage i.gender##i.region
margins gender#region
```

### Reference Categories
```stata
regress wage ib3.education_cat          // Category 3 as reference
regress wage ib(first).region
regress wage ib(last).region
```

**GOTCHA: `ib()` prefixes the variable being factored, not its interaction partner.**
```stata
* WRONG — ib() on the wrong side of the interaction
regress y treated#ib(-1).time

* RIGHT — ib() directly prefixes its own variable
regress y ib(-1).time#1.treated          // base = time period -1
```

### Testing Interactions
```stata
regress wage i.gender##c.education
test 1.gender#c.education               // Is interaction significant?

regress wage i.region##c.education
testparm i.region#c.education            // Joint test of all interaction terms
```

**GOTCHA: `test` vs `testparm` for factor variables.** `test` requires you to spell out each
level explicitly and **cannot parse negative factor levels** (the `-` is read as subtraction).
Use `testparm` with wildcards or level lists instead:
```stata
* WRONG — test cannot handle negative levels or wildcards
test 1.treated#-5.time   // syntax error: "-" parsed as subtraction

* RIGHT — testparm handles wildcards and level lists
testparm 1.treated#(-5 -4 -3 -2).time   // specific levels
testparm lead*                            // wildcard on manual dummies
```

### Centering for Interpretation
```stata
sum education
gen education_c = education - r(mean)
regress wage i.gender##c.education_c
// Now: gender main effect = difference at MEAN education
```

---

## Regression Diagnostics

### Visual Diagnostics
```stata
rvfplot                    // Residual vs fitted (check linearity + homoskedasticity)
rvpplot mpg                // Residual vs predictor
avplot mpg                 // Added-variable plot (partial regression)
avplots                    // All added-variable plots
cprplot mpg                // Component-plus-residual (check linearity)
lvr2plot                   // Leverage vs residual-squared
qnorm residuals            // Q-Q plot for normality
histogram residuals, normal
```

### Statistical Tests
```stata
estat hettest              // Breusch-Pagan (H0: homoskedasticity)
estat imtest, white        // White's test
estat ovtest               // Ramsey RESET (H0: no omitted vars)
estat vif                  // VIF > 10 = serious multicollinearity
swilk residuals            // Shapiro-Wilk normality test (n < 2000)
```

### Influential Observations
```stata
predict cooksd, cooksd
gen influential = cooksd > 4/e(N)           // Rule of thumb

predict leverage, leverage
gen high_lev = leverage > 2*e(rank)/e(N)    // Rule of thumb

predict rstud, rstudent
gen outlier = abs(rstud) > 2                // ~5% expected
list make price mpg if abs(rstud) > 3       // Serious outliers

dfbeta                                       // Influence on individual coefficients
```

### Addressing Issues

**Heteroskedasticity:** `vce(robust)`, log-transform Y, or WLS

**Non-linearity:** Polynomial terms (`c.x##c.x`), log transform, splines

**Outliers:** Robust regression (`rreg y x`), report with and without

**Multicollinearity:** Drop redundant vars, create composites, or accept if theoretically important (coefficients still unbiased, just imprecise)

---

## Quick Reference

| Task | Command |
|------|---------|
| Basic regression | `regress y x1 x2` |
| Robust SEs | `regress y x, vce(robust)` |
| Clustered SEs | `regress y x, vce(cluster id)` |
| Weighted | `regress y x [aweight=w]` |
| Interaction | `regress y i.cat##c.cont` |
| IV regression | `ivregress 2sls y x2 (x1 = z)` |
| Predictions | `predict yhat` |
| Marginal effects | `margins, dydx(x)` |
| Test coefficients | `test x1 = x2` |
| Linear combination | `lincom x1 + x2` |
| Nonlinear function | `nlcom _b[x1]/_b[x2]` |
| Diagnostics | `estat hettest` / `estat vif` |
| Influence | `predict cooksd, cooksd` |

## Common Mistakes

- Ignoring heteroskedasticity (invalid inference)
- Not clustering with grouped data (understated SEs)
- Interpreting interaction coefficients directly (use `margins`)
- Manually doing 2SLS (wrong standard errors)
- Excluding exogenous variables in IV specification
- Over-interpreting R-squared (fit does not equal good model)
- Assuming causality without identification strategy
