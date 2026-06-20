# Diagnostic Packages for Stata

## Overview

**Packages covered:**
- **bacondecomp**: Bacon decomposition for TWFE DiD -- reveals how staggered treatment timing creates weighted averages of 2x2 comparisons, some potentially biased
- **xttest3**: Modified Wald test for groupwise heteroskedasticity in panel FE models
- **xtcsd**: Cross-sectional dependence tests (Pesaran CD, Friedman, Frees) for panel data
- **xtserial**: Wooldridge test for first-order serial correlation in panels
- **vif/collin**: Multicollinearity diagnostics (VIF, condition number, variance decomposition)
- **hettest/imtest**: Breusch-Pagan and White heteroskedasticity tests (built-in)
- **ovtest/linktest**: Ramsey RESET and link specification tests (built-in)

## Installation

```stata
// Panel data diagnostics
ssc install xttest3
ssc install xtcsd
ssc install xtserial
ssc install bacondecomp
ssc install collin

// Built-in (no install needed): vif, hettest, imtest, ovtest, linktest

// Verify
which xttest3
which xtcsd
which xtserial
which bacondecomp
which collin
```

---

## Bacon Decomposition for TWFE DiD

The Bacon decomposition (Goodman-Bacon 2021) shows how a TWFE DiD estimate is a weighted average of all 2x2 comparisons. Critical for detecting negative weights and bias from staggered adoption.

### Usage

```stata
ssc install bacondecomp

bacondecomp outcome treatment_var, ddetail

// With plot options
bacondecomp outcome treatment_var, ///
    ddetail stub(bacon_) ///
    gropt(title("Bacon Decomposition") ///
          xtitle("Weight") ytitle("2x2 DD Estimate"))
```

### Interpreting Results

```
Comparison types:
  "Earlier T vs. Later C": Early treated vs. not-yet-treated (GOOD)
  "Later T vs. Earlier C": Late treated vs. already-treated (PROBLEMATIC)
  "T vs. Never treated": Treated vs. never-treated (GOOD)

Warning signs:
  - Large weight on "Later T vs. Earlier C" (uses already-treated as control)
  - 2x2 estimates with opposite signs across comparison types
  - Any negative weights
```

### Workflow

```stata
// Step 1: TWFE estimate
reghdfe outcome treatment, absorb(unit time) cluster(unit)

// Step 2: Decompose
bacondecomp outcome treatment, ddetail stub(bacon_)

// Step 3: Check problematic weight
preserve
collapse (sum) bacon_weight (mean) bacon_dd_estimate, by(bacon_type)
list bacon_type bacon_weight bacon_dd_estimate
restore

// Step 4: If >20% weight on "Later T vs. Earlier C", use robust estimators:
//   - Sun & Abraham (eventstudyinteract)
//   - Callaway & Sant'Anna (csdid)
//   - De Chaisemartin & D'Haultfoeuille (did_multiplegt)
```

---

## Panel Data Heteroskedasticity: xttest3

Tests whether error variances differ across panel groups (H0: sigma_i^2 = sigma^2 for all i).

### Usage

```stata
// MUST run after xtreg, fe
xtreg depvar indepvars, fe
xttest3

// No options needed -- automatic after xtreg, fe
```

### Remedies

```stata
// If xttest3 rejects (heteroskedasticity detected):

// SOLUTION 1: Robust SE (most common)
xtreg y x1 x2, fe vce(robust)

// SOLUTION 2: Cluster-robust SE (also handles serial correlation)
xtreg y x1 x2, fe vce(cluster id)

// SOLUTION 3: reghdfe (automatically robust)
reghdfe y x1 x2, absorb(id) vce(robust)
// or
reghdfe y x1 x2, absorb(id) vce(cluster id)

// SOLUTION 4: Bootstrap
xtreg y x1 x2, fe vce(bootstrap, reps(1000))

/*
Decision tree:
  Just heteroskedasticity     -> vce(robust)
  + clustering structure      -> vce(cluster id)
  Few clusters (<30)          -> Bootstrap or wild bootstrap
  Need efficiency             -> FGLS (if specification correct)
*/
```

---

## Cross-Sectional Dependence: xtcsd

Tests whether errors are correlated across panel units (common shocks, spatial correlation, network effects).

### Usage

```stata
// Run after xtreg, fe
xtreg depvar indepvars, fe

xtcsd, pesaran          // Pesaran CD test (recommended, large N large T)
xtcsd, pesaran abs      // With absolute correlation
xtcsd, frees            // Frees' Q test (unbalanced panels)
xtcsd, friedman         // Friedman test (small N)
```

### Remedies

```stata
// SOLUTION 1: Driscoll-Kraay SE (recommended for general CSD)
ssc install xtscc
xtscc y x1 x2, fe lag(2)

// SOLUTION 2: Add time fixed effects (absorbs common shocks)
reghdfe y x1 x2, absorb(unit year) vce(cluster unit)

// SOLUTION 3: Common correlated effects (Pesaran 2006)
foreach var of varlist y x1 x2 {
    bysort year: egen `var'_avg = mean(`var')
}
xtreg y x1 x2 y_avg x1_avg x2_avg, fe

// SOLUTION 4: Two-way clustering
reghdfe y x1 x2, absorb(unit) vce(cluster unit year)

/*
Decision tree:
  Large N, large T        -> Driscoll-Kraay SE (xtscc)
  Common shocks           -> Add time fixed effects
  Factor structure        -> CCE or factor models
  Spatial correlation     -> Spatial econometrics
  General case            -> Two-way clustering
*/
```

---

## Serial Correlation: xtserial

Implements Wooldridge's (2002) test for first-order autocorrelation in panel data (H0: no AR(1) serial correlation).

### Usage

```stata
xtserial depvar indepvars [if] [in], [output]
```

### Example

```stata
webuse nlswork, clear
xtset idcode year

xtserial ln_wage tenure ttl_exp age grade
// Reject H0 (p < 0.05): Serial correlation present
```

### Remedies

```stata
// SOLUTION 1: Cluster SE by panel unit (most common)
xtreg y x1 x2, fe vce(cluster id)

// SOLUTION 2: AR(1) model (xtregar)
xtregar y x1 x2, fe

// SOLUTION 3: Driscoll-Kraay SE (handles serial + CSD)
xtscc y x1 x2, fe lag(4)

// SOLUTION 4: Dynamic panel GMM (Arellano-Bond)
ssc install xtabond2
xtabond2 y L.y x1 x2, gmm(L.y) iv(x1 x2) robust small

/*
Decision tree:
  Short T          -> Cluster by id
  Long T           -> HAC (Newey-West) or Driscoll-Kraay
  Dynamic model    -> GMM (xtabond2)
  AR(1) structure  -> xtregar
  CSD + serial     -> Driscoll-Kraay (xtscc)
*/
```

---

## Multicollinearity: VIF and collin

### Built-in VIF

```stata
regress y x1 x2 x3 x4
vif

// Interpretation:
// VIF = 1: No collinearity
// VIF < 5: Acceptable
// 5 <= VIF < 10: Moderate (caution)
// VIF >= 10: Problematic
```

### Enhanced collin

```stata
ssc install collin

collin x1 x2 x3 x4

// Additional output:
// - Condition number (<30 OK, 30-100 moderate, >100 severe)
// - Condition indices (>30 indicates problem)
// - Variance decomposition proportions (>0.5 on high index = problem)
```

### Remedies

```stata
// SOLUTION 1: Drop redundant variables
correlate weight displacement length
// If r > 0.9, drop one
regress y weight length turn foreign
vif

// SOLUTION 2: Combine correlated variables
egen size = rowmean(weight length)
// Or factor analysis
factor weight length displacement
predict size_factor

// SOLUTION 3: Center variables (especially for interactions)
summarize weight
gen weight_c = weight - r(mean)
summarize length
gen length_c = length - r(mean)
gen weight_X_length = weight_c * length_c
regress y weight_c length_c weight_X_length
vif

// SOLUTION 4: Ridge regression
ssc install ridgereg
ridgereg y x1 x2 x3, model(orr) ridge(0.001 0.01 0.1 1 10)

// SOLUTION 5: Principal components regression
pca weight length turn displacement
predict pc1 pc2
regress y pc1 pc2 foreign
vif  // VIF will be low

// SOLUTION 6: Use joint tests instead of individual tests
regress y weight length turn displacement foreign
testparm weight displacement

/*
Decision tree:
  VIF < 5                           -> No action needed
  Perfect collinearity              -> Drop redundant variable
  Variables measure same concept    -> Combine or choose one
  Polynomial terms causing high VIF -> Center variables
  Prediction focus                  -> Ridge or PCA
  Inference focus                   -> Drop or collect more data
*/
```

---

## Heteroskedasticity Tests: hettest and imtest

### Usage

```stata
regress y x1 x2 x3

// Breusch-Pagan / Cook-Weisberg (H0: constant variance)
hettest              // Test against fitted values
hettest x1 x2       // Test against specific variables
hettest, fstat       // F-test version

// White's General Test (more general, no functional form assumption)
imtest, white
```

### Remedies

```stata
// SOLUTION 1: Robust (Huber-White) SE -- most common
regress y x1 x2, robust

// SOLUTION 2: Log transformation (for positive Y)
gen ln_y = ln(y)
regress ln_y x1 x2
hettest

// SOLUTION 3: WLS (if variance structure known)
quietly regress y x1 x2
predict resid, residuals
gen resid2 = resid^2
regress resid2 x1 x2
predict var_hat
gen wt = 1/var_hat
regress y x1 x2 [aweight=wt]

// SOLUTION 4: Bootstrap SE
regress y x1 x2, vce(bootstrap, reps(1000))

// SOLUTION 5: Cluster-robust SE
regress y x1 x2, cluster(group_var)

/*
Decision tree:
  Just need valid inference   -> robust SE
  Positive Y, wide range     -> log transformation
  Variance structure known    -> WLS
  Clustered data              -> cluster-robust SE
  Unknown structure           -> robust SE or bootstrap
*/
```

---

## Specification Tests: ovtest and linktest

### Ramsey RESET Test

Tests for omitted variables/nonlinearity by adding powers of fitted values.

```stata
regress y x1 x2 x3
ovtest           // H0: no omitted variables
ovtest, rhs      // Use powers of RHS variables instead
```

### Link Test

Tests specification by regressing y on y-hat and y-hat-squared.

```stata
regress y x1 x2 x3
linktest
// _hat should be significant (model has explanatory power)
// _hatsq should NOT be significant (no misspecification)
```

### Remedies for Specification Errors

```stata
// SOLUTION 1: Add polynomial terms
gen x1_sq = x1^2
regress y x1 x1_sq x2
ovtest

// SOLUTION 2: Add interactions
gen x1_X_x2 = x1 * x2
regress y x1 x2 x1_X_x2
ovtest

// SOLUTION 3: Fractional polynomials
fracpoly: regress y x1 x2

// SOLUTION 4: Log transformations
gen ln_y = ln(y)
gen ln_x1 = ln(x1)
regress ln_y ln_x1 x2
ovtest

// SOLUTION 5: Splines
mkspline x1_sp = x1, nknots(4) cubic
regress y x1_sp* x2
ovtest

// Compare alternatives with AIC/BIC
estimates stats baseline alt1 alt2 alt3

/*
Decision tree:
  Single variable nonlinear   -> log(Y)/log(X) or fractional polynomial
  Interaction suspected       -> Add interaction terms
  Omitted variables           -> Add controls based on theory
  Very nonlinear, prediction  -> Splines or GAM
  Very nonlinear, inference   -> Fractional polynomial
*/
```

---

## Complete Diagnostic Workflow: Cross-Sectional

```stata
capture program drop diagnostic_suite
program define diagnostic_suite
    syntax varlist(min=2) [if] [in]
    gettoken depvar indepvars : varlist

    display "{hline 70}"
    display "COMPREHENSIVE REGRESSION DIAGNOSTICS"
    display "{hline 70}"

    quietly regress `depvar' `indepvars' `if' `in'

    // 1. Heteroskedasticity
    display ""
    display "1. HETEROSKEDASTICITY"
    hettest
    scalar bp_p = r(p)
    quietly imtest, white
    display "White test: chi2=" %7.2f r(chi2) ", p=" %6.4f r(p)
    scalar white_p = r(p)

    if bp_p < 0.05 | white_p < 0.05 {
        display "-> Heteroskedasticity detected: Use robust SE"
    }

    // 2. Specification
    display ""
    display "2. SPECIFICATION"
    quietly regress `depvar' `indepvars' `if' `in'
    ovtest
    scalar reset_p = r(p)
    quietly linktest
    test _hatsq
    scalar link_p = r(p)

    if reset_p < 0.05 | link_p < 0.05 {
        display "-> Misspecification detected: Check functional form"
    }

    // 3. Normality
    display ""
    display "3. NORMALITY"
    quietly regress `depvar' `indepvars' `if' `in'
    predict resid_temp, residuals
    swilk resid_temp
    scalar norm_p = r(p)
    if norm_p < 0.05 {
        display "-> Non-normality: Consider robust inference"
    }

    // 4. Multicollinearity
    display ""
    display "4. MULTICOLLINEARITY"
    quietly regress `depvar' `indepvars' `if' `in'
    vif

    // Recommendation
    display ""
    display "{hline 70}"
    display "RECOMMENDED SPECIFICATION"
    if bp_p < 0.05 | white_p < 0.05 {
        display "-> Use robust SE"
        regress `depvar' `indepvars' `if' `in', robust
    }
    if reset_p < 0.05 | link_p < 0.05 {
        display "-> Check functional form (quadratic, log, interactions)"
    }

    capture drop resid_temp
end

// Usage:
sysuse auto, clear
diagnostic_suite mpg weight length foreign
```

---

## Complete Diagnostic Workflow: Panel Data

```stata
capture program drop panel_diagnostics
program define panel_diagnostics
    syntax varlist [if] [in], Panel(varname) Time(varname)
    gettoken depvar indepvars : varlist

    display "{hline 70}"
    display "PANEL DATA DIAGNOSTICS"
    display "{hline 70}"

    xtset `panel' `time'
    quietly xtreg `depvar' `indepvars' `if' `in', fe

    // 1. Groupwise heteroskedasticity
    display ""
    display "1. HETEROSKEDASTICITY (xttest3)"
    xttest3
    scalar het_p = r(p)

    // 2. Serial correlation
    display ""
    display "2. SERIAL CORRELATION (xtserial)"
    xtserial `depvar' `indepvars' `if' `in'
    scalar serial_p = r(p)

    // 3. Cross-sectional dependence
    display ""
    display "3. CROSS-SECTIONAL DEPENDENCE (xtcsd)"
    quietly xtreg `depvar' `indepvars' `if' `in', fe
    xtcsd, pesaran abs
    scalar csd_p = r(p)

    // Recommendation
    display ""
    display "{hline 70}"
    display "RECOMMENDED SPECIFICATION"
    display "{hline 70}"

    if het_p < 0.05 & serial_p < 0.05 & csd_p < 0.05 {
        display "All three violations -> Driscoll-Kraay SE"
        xtscc `depvar' `indepvars' `if' `in', fe lag(2)
    }
    else if het_p < 0.05 & serial_p < 0.05 {
        display "Heteroskedasticity + serial correlation -> Clustered SE"
        xtreg `depvar' `indepvars' `if' `in', fe vce(cluster `panel')
    }
    else if het_p < 0.05 {
        display "Heteroskedasticity only -> Robust SE"
        xtreg `depvar' `indepvars' `if' `in', fe vce(robust)
    }
    else if serial_p < 0.05 {
        display "Serial correlation only -> Clustered SE"
        xtreg `depvar' `indepvars' `if' `in', fe vce(cluster `panel')
    }
    else if csd_p < 0.05 {
        display "CSD only -> Time FE or Driscoll-Kraay"
    }
    else {
        display "No violations -> Conventional SE valid"
    }
end

// Usage:
webuse nlswork, clear
panel_diagnostics ln_wage tenure ttl_exp age grade, panel(idcode) time(year)
```

---

## Quick Reference

```stata
// Install all
ssc install bacondecomp xttest3 xtcsd xtserial collin xtscc

// Panel diagnostics
xtreg y x1 x2, fe
xttest3              // Groupwise heteroskedasticity
xtserial y x1 x2    // Serial correlation
xtcsd, pesaran abs   // Cross-sectional dependence

// Cross-sectional diagnostics
regress y x1 x2 x3
hettest              // Breusch-Pagan
imtest, white        // White's test
ovtest               // RESET specification
linktest             // Link specification
vif                  // VIF
collin x1 x2 x3     // Enhanced multicollinearity

// DiD diagnostics
bacondecomp y treatment, ddetail

// Remedies
regress y x1 x2, robust                    // Robust SE
regress y x1 x2, cluster(id)               // Cluster SE
xtscc y x1 x2, fe lag(2)                   // Driscoll-Kraay
xtreg y x1 x2, fe vce(cluster id)          // Panel cluster
```

## References

- Goodman-Bacon (2021). "Difference-in-differences with variation in treatment timing." *Journal of Econometrics*.
- Hoechle (2007). "Robust standard errors for panel regressions with cross-sectional dependence." *Stata Journal*.
- Pesaran (2004). "General diagnostic tests for cross section dependence in panels."
- White (1980). "A heteroskedasticity-consistent covariance matrix estimator." *Econometrica*.
- Wooldridge (2002). *Econometric Analysis of Cross Section and Panel Data*. MIT Press.

---

**Stata version**: 17.0+
**Required packages**: bacondecomp, xttest3, xtcsd, xtserial, collin, xtscc
