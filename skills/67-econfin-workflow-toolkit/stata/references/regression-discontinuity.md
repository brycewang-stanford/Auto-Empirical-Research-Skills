# Regression Discontinuity Design in Stata

## Key Concepts

**Sharp RD**: Treatment probability jumps from 0 to 1 at the cutoff. Treatment is a deterministic function of the running variable.

**Fuzzy RD**: Treatment probability changes discontinuously but not from 0 to 1 (imperfect compliance). Estimates a LATE for compliers via IV-like estimation: Effect = Discontinuity in outcome / Discontinuity in treatment.

## Installing Required Packages

```stata
// rdrobust suite (Calonico, Cattaneo, Titiunik)
ssc install rdrobust, replace    // Main estimation
ssc install rddensity, replace   // Manipulation testing
ssc install rdlocrand, replace   // Local randomization
ssc install rdmulti, replace     // Multiple cutoffs/scores
ssc install rdpower, replace     // Power calculations
```

## Basic RD Estimation with `rdrobust`

### Sharp RD

```stata
// Basic syntax
rdrobust outcome runvar [if] [in] [, options]

// Example: Effect of scholarship on test scores (cutoff at GPA 3.0)
gen gpa_centered = gpa - 3.0
rdrobust test_score gpa_centered
```

### Understanding Output

Three rows of estimates:
- **Conventional**: Standard local polynomial estimate
- **Bias-Corrected**: Corrected for polynomial approximation bias (preferred point estimate)
- **Robust**: Robust confidence intervals and p-values (preferred for inference)

Also reports: kernel type, bandwidth (h for estimation, b for bias correction), effective N left/right of cutoff.

### Key Options

```stata
// Polynomial order (default p=1 = local linear, recommended)
rdrobust y x, p(1)          // Local linear
rdrobust y x, p(2)          // Local quadratic

// Kernel function
rdrobust y x, kernel(triangular)    // Default
rdrobust y x, kernel(uniform)
rdrobust y x, kernel(epanechnikov)

// Covariates (for precision, not identification)
rdrobust y x, covs(age gender income)

// Cluster standard errors
rdrobust y x, vce(cluster school_id)

// Show all three estimation rows
rdrobust y x, all

// Access stored results
rdrobust y x
scalar rd_effect = e(tau_cl)       // Bias-corrected estimate
scalar rd_se = e(se_tau_cl)        // SE of bias-corrected
scalar bw = e(h_l)                 // Left bandwidth
scalar n_l = e(N_h_l)             // Effective N left
scalar n_r = e(N_h_r)             // Effective N right
matrix list e(b)                   // Coefficient vector
```

## Bandwidth Selection

### Automatic Selection Methods

```stata
// Default: MSE-optimal, one common bandwidth
rdrobust y x, bwselect(mserd)

// MSE-optimal, different bandwidths each side
rdrobust y x, bwselect(msetwo)

// CER-optimal (coverage error rate), one common bandwidth
rdrobust y x, bwselect(cerrd)

// CER-optimal, different bandwidths each side
rdrobust y x, bwselect(certwo)
```

### Manual Bandwidth

```stata
rdrobust y x, h(0.5)              // Single bandwidth
rdrobust y x, h(0.4 0.6)          // Different left/right
rdrobust y x, h(0.5) b(0.7)       // Main and bias bandwidth
```

### Compare Selectors with `rdbwselect`

```stata
rdbwselect y x                     // Shows all bandwidth methods
rdbwselect y x, covs(age gender)   // With covariates
rdbwselect y x, kernel(uniform)    // Different kernel
```

## Polynomial Order and Bias Correction

```stata
// Compare polynomial orders
forvalues p = 1/3 {
    display as text _n "Polynomial order: `p'"
    rdrobust y x, p(`p')
}
// Rule of thumb: p=1 (local linear) for estimation, higher orders for bias correction

// Derivative estimation (kink RD: slope change instead of level change)
rdrobust y x, deriv(1)

// Bias correction order (default q = p+1)
rdrobust y x, p(1) q(2)           // Default
rdrobust y x, p(1) q(1)           // Disable bias correction
```

## Fuzzy RD Design

```stata
// Fuzzy RD estimation (IV-like)
rdrobust outcome score_centered, fuzzy(treatment)

// Examine first stage (should show substantial jump)
rdrobust treatment score_centered

// With covariates and clustering
rdrobust outcome score_centered, fuzzy(treatment) covs(age male)
rdrobust outcome score_centered, fuzzy(treatment) vce(cluster cluster_id)
```

## Manipulation Testing with `rddensity`

Tests for sorting/bunching at the cutoff. H0: density is continuous at cutoff.

```stata
rddensity score_centered
// p > 0.05 → no evidence of manipulation (good)

// With density plot
rddensity score_centered, plot ///
    graph_opt(title("Density Test") ///
    xtitle("Running Variable") ytitle("Density"))

// Options
rddensity score_centered, h(0.5)                  // Manual bandwidth
rddensity score_centered, fitselect(restricted)    // Restricted model
```

## Covariate Balance Tests

Run `rdrobust` with each predetermined covariate as the outcome. Large p-values indicate balance (good).

```stata
// Individual balance tests
foreach var in age female income baseline_score {
    display as text _n "Balance test for: `var'"
    rdrobust `var' running
}

// Build balance table with postfile
preserve
    tempname balance_results
    postfile `balance_results' str30 variable coef se pval using balance_table, replace

    foreach var in age female income baseline_score {
        quietly rdrobust `var' running
        local coef = e(tau_cl)
        local se = e(se_tau_cl)
        local pval = 2*normal(-abs(`coef'/`se'))
        post `balance_results' ("`var'") (`coef') (`se') (`pval')
    }
    postclose `balance_results'
restore

use balance_table, clear
list, clean noobs
```

### Joint Balance Test

```stata
// Using seemingly unrelated estimation within bandwidth
preserve
    keep if abs(running) < 0.5

    reg age treatment running
    estimates store age_eq
    reg female treatment running
    estimates store female_eq
    reg income treatment running
    estimates store income_eq

    suest age_eq female_eq income_eq
    test [age_eq]treatment [female_eq]treatment [income_eq]treatment
restore
// Want to fail to reject (p > 0.05)
```

## Bandwidth Sensitivity Analysis

```stata
// Systematic sweep
matrix results = J(20, 4, .)
local row = 0

forvalues h = 0.2(0.1)2.0 {
    local ++row
    quietly rdrobust y x, h(`h')
    matrix results[`row', 1] = `h'
    matrix results[`row', 2] = e(tau_cl)
    matrix results[`row', 3] = e(tau_cl) - 1.96*e(se_tau_cl)
    matrix results[`row', 4] = e(tau_cl) + 1.96*e(se_tau_cl)
}

// Plot sensitivity
preserve
    clear
    svmat results, names(col)
    rename (c1 c2 c3 c4) (bandwidth estimate ci_lower ci_upper)

    twoway (rarea ci_lower ci_upper bandwidth, color(gs12)) ///
           (line estimate bandwidth, lcolor(navy) lwidth(medium)), ///
        title("RD Estimate Sensitivity to Bandwidth") ///
        xtitle("Bandwidth") ytitle("Treatment Effect") ///
        legend(order(2 "Point Estimate" 1 "95% CI")) ///
        yline(0, lpattern(dash) lcolor(red))
restore
```

### Half/Double Optimal Bandwidth

```stata
rdrobust y x
local h_opt = e(h_l)

rdrobust y x, h(`=`h_opt'*0.5')
estimates store half_bw

rdrobust y x, h(`h_opt')
estimates store opt_bw

rdrobust y x, h(`=`h_opt'*2')
estimates store double_bw

estimates table half_bw opt_bw double_bw, ///
    keep(Conventional) se stats(N_h_l N_h_r)
```

## Graphical Presentation

### RD Plot with `rdplot`

```stata
// Basic (automatic binning and polynomial fit)
rdplot outcome score

// Control bins and polynomial
rdplot outcome score, nbins(20 20) p(1)

// Bin selection methods:
//   es:   IMSE-optimal evenly-spaced
//   espr: IMSE-optimal evenly-spaced using polynomial regression
//   esmv: mimicking variance evenly-spaced (default)
//   qs:   IMSE-optimal quantile-spaced
rdplot outcome score, binselect(esmv)

// Publication-quality
rdplot outcome score, p(1) nbins(20 20) ///
    graph_options(title("RD Effect of Program on Outcomes") ///
                  xtitle("Distance from Cutoff") ///
                  ytitle("Outcome") ///
                  graphregion(color(white)) legend(off) ///
                  name(rdplot1, replace))
```

### Manual RD Plot

```stata
preserve
    xtile bin_temp = score if score < 0, nq(15)
    replace bin = bin_temp if score < 0
    xtile bin_temp2 = score if score >= 0, nq(15)
    replace bin = bin_temp2 + 15 if score >= 0

    collapse (mean) outcome score, by(bin treatment)

    twoway (scatter outcome score if treatment==0, mcolor(navy)) ///
           (scatter outcome score if treatment==1, mcolor(maroon)) ///
           (lfit outcome score if treatment==0, lcolor(navy)) ///
           (lfit outcome score if treatment==1, lcolor(maroon)), ///
        xline(0, lcolor(black) lpattern(dash)) ///
        legend(order(1 "Control" 2 "Treatment") position(6) row(1))
restore
```

## Complete RD Analysis Workflow

### Step 1: Descriptive Statistics

```stata
table () (treatment), ///
    statistic(mean outcome parent_income female) ///
    statistic(sd outcome parent_income female) ///
    statistic(count outcome)

histogram running_centered, width(0.1) fraction ///
    xline(0, lcolor(red) lpattern(dash))
```

### Step 2: Graphical Analysis

```stata
rdplot college_gpa hs_gpa_centered, p(1) nbins(20 20) ///
    graph_options(title("RD Plot") xtitle("Running Variable") ytitle("Outcome"))

// Compare polynomial orders
forvalues p = 1/4 {
    rdplot y x, p(`p') graph_options(title("p=`p'") name(rdplot_p`p', replace) nodraw)
}
graph combine rdplot_p1 rdplot_p2 rdplot_p3 rdplot_p4
```

### Step 3: Manipulation Test

```stata
rddensity hs_gpa_centered
rddensity hs_gpa_centered, plot ///
    graph_opt(title("McCrary Density Test") xtitle("Running Variable"))
```

### Step 4: Covariate Balance Tests

```stata
local covariates "parent_income female age sat_score"
foreach var of local covariates {
    quietly rdrobust `var' hs_gpa_centered
    local coef_`var' = string(e(tau_cl), "%6.3f")
    local se_`var' = string(e(se_tau_cl), "%6.3f")
    local pval_`var' = string(2*normal(-abs(e(tau_cl)/e(se_tau_cl))), "%6.3f")
}
```

### Step 5: Main Estimation

```stata
rdrobust college_gpa hs_gpa_centered, all

scalar te_main = e(tau_cl)
scalar se_main = e(se_tau_cl)
scalar bw_main = e(h_l)
```

### Step 6: Specification Robustness

```stata
// Polynomial orders
forvalues p = 1/3 {
    quietly rdrobust y x, p(`p')
    display "p=`p': Effect=" %6.3f e(tau_cl) " SE=" %6.3f e(se_tau_cl)
}

// Bandwidth selectors
foreach bw in mserd msetwo cerrd certwo {
    quietly rdrobust y x, bwselect(`bw')
    display "`bw': Effect=" %6.3f e(tau_cl) " h=" %6.3f e(h_l)
}

// Kernel functions
foreach kern in triangular epanechnikov uniform {
    quietly rdrobust y x, kernel(`kern')
    display "`kern': Effect=" %6.3f e(tau_cl)
}
```

### Step 7: Covariate-Adjusted Estimation

```stata
rdrobust college_gpa hs_gpa_centered, covs(parent_income female sat_score)
// Compare SE with unadjusted — covariates should improve precision
```

### Step 8: Placebo Tests

```stata
// Placebo cutoffs (test fake cutoffs on each side)
foreach cutoff in -0.5 -0.25 {
    preserve
        keep if hs_gpa_centered < 0
        quietly rdrobust college_gpa hs_gpa_centered, c(`cutoff')
        display "Placebo cutoff `cutoff': p=" ///
            %6.3f 2*normal(-abs(e(tau_cl)/e(se_tau_cl)))
    restore
}

// Placebo outcomes (predetermined variables should show no effect)
foreach var in parent_income sat_score {
    quietly rdrobust `var' hs_gpa_centered
    display "Placebo outcome `var': p=" ///
        %6.3f 2*normal(-abs(e(tau_cl)/e(se_tau_cl)))
}
```

### Step 9: Donut RD

```stata
// Exclude observations near cutoff to address manipulation concerns
foreach donut in 0 0.05 0.10 0.15 {
    preserve
        if `donut' > 0 drop if abs(hs_gpa_centered) < `donut'
        quietly rdrobust college_gpa hs_gpa_centered
        display "Donut=`donut': Effect=" %6.3f e(tau_cl) " SE=" %6.3f e(se_tau_cl)
    restore
}
```

## Advanced Topics

### RD with Discrete Running Variable

```stata
// Standard rdrobust may not work well; consider local randomization
preserve
    keep if inrange(test_score, 65, 75)    // Narrow window
    ttest outcome, by(treatment)            // Simple comparison
    reg outcome treatment                   // Or regression
restore

// rdrobust can still be used but interpret with caution
rdrobust outcome test_score
```

### Geographic/Spatial RD

```stata
// Distance from border as running variable
rdrobust outcome distance_from_border
// May need: vce(cluster geo_id) for spatial correlation
```

### Kink RD Design

```stata
// Estimates change in slope (not level) at cutoff
rdrobust y x, deriv(1)
rdplot y x, p(2)       // Quadratic fit to visualize kink
```

### Power Calculations

```stata
// ssc install rdpower
// rdpower y x, tau(0.3) sampsi    // Required sample size
// rdpower y x, tau(0.3) samph     // Power for given sample
```

## Gotchas and Best Practices

1. **Use p=1 (local linear) as default.** Higher-order polynomials (p > 2) overfit and are unreliable.
2. **Use data-driven bandwidth selection** (rdrobust default). Always report sensitivity.
3. **Report bias-corrected estimates** with robust inference, not conventional.
4. **Always run manipulation tests** (`rddensity`) and covariate balance checks.
5. **RD effects are local** to the cutoff neighborhood -- they may not generalize.
6. **Always include an RD plot** -- visual evidence of the discontinuity is essential for credibility.
7. **Covariates in `rdrobust`** improve precision but are not needed for identification.

### Reporting Checklist

```
Essential elements:
1. RD plot showing discontinuity
2. Density test results (manipulation check)
3. Covariate balance table
4. Main estimates with multiple specifications
5. Bandwidth sensitivity analysis
6. Polynomial order robustness
7. Placebo tests (fake cutoffs + predetermined outcomes)
8. Clear statement that effect is local to cutoff
```
