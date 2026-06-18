# psmatch2: Propensity Score Matching

## Overview

`psmatch2` is a widely-used Stata package for propensity score matching (PSM), developed by Edwin Leuven and Barbara Sianesi. It estimates average treatment effects by matching treated and control units on propensity scores or covariate distances.

**Key advantages over `teffects psmatch`:**
- Multiple matching algorithms (nearest neighbor, kernel, local linear, radius)
- Mahalanobis distance matching option
- Handles multiple outcomes simultaneously
- Detailed matching diagnostics (individual match info via created variables)
- Flexible common support control

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Syntax](#syntax)
- [Variables Created by psmatch2](#variables-created-by-psmatch2)
- [Returned Results](#returned-results)
- [Basic Workflow](#basic-workflow)
- [Matching Algorithms](#matching-algorithms)
- [Common Support](#common-support)
- [ATT, ATE, ATU](#att-ate-atu)
- [Balance Assessment (pstest)](#balance-assessment-pstest)
- [Comparison: psmatch2 vs teffects psmatch](#comparison-psmatch2-vs-teffects-psmatch)
- [Saving Matched Samples](#saving-matched-samples)
- [Bootstrap Standard Errors](#bootstrap-standard-errors)
- [Complete Analysis Template](#complete-analysis-template)
- [DiD-PSM Example](#did-psm-example)
- [Common Pitfalls](#common-pitfalls)
- [Key References](#key-references)

## Installation

```stata
ssc install psmatch2
which psmatch2

// Companion commands
ssc install rbounds   // sensitivity analysis
```

### Testing the Installation

```stata
webuse cattaneo2, clear
logit mbsmoke mmarried c.mage##c.mage fbaby medu
predict pscore, pr
psmatch2 mbsmoke, outcome(bweight) pscore(pscore) neighbor(1)
```

## Syntax

```stata
psmatch2 treatvar [varlist] [if] [in] [weight], ///
    outcome(varlist) ///
    [pscore(varname) | logit probit] ///
    [neighbor(#) caliper(#) radius kernel llr] ///
    [options]
```

**Main options:**
- `outcome(varlist)`: Outcome variable(s) for treatment effect estimation
- `pscore(varname)`: Pre-estimated propensity score variable
- `logit` / `probit`: Estimate propensity score internally (if pscore not provided)
- `neighbor(#)`: Number of nearest neighbors (default: 1)
- `caliper(#)`: Maximum propensity score distance
- `common`: Restrict to common support
- `noreplacement`: Match without replacement
- `kernel`: Use kernel matching
- `kerneltype(epan|normal|biweight|tricube|uniform)`: Kernel function
- `bwidth(#)`: Bandwidth for kernel/LLR matching
- `llr`: Local linear regression matching
- `radius`: Radius matching (match to ALL controls within caliper)
- `mahal(varlist)`: Mahalanobis distance matching on specified variables

## Variables Created by psmatch2

```stata
// After matching, psmatch2 creates:
// _treated  : 1 if treated, 0 if control
// _support  : 1 if in common support region
// _pscore   : Propensity score of matched unit
// _weight   : Number of times control unit is used as match
// _n1       : ID of 1st nearest neighbor
// _nn       : Total number of neighbors
// _pdif     : Absolute propensity score difference
// _id       : Observation identifier

// Examine matched pairs
list treatment earnings pscore _pscore _weight _pdif if treatment==1 in 1/10
```

## Returned Results

```stata
return list
// r(att)    : Average treatment effect on treated
// r(seatt)  : Standard error of ATT
// r(ntr)    : Number of treated units
// r(nco)    : Number of control units

// For multiple outcomes, results in matrix form:
matrix list r(att)    // Row vector of ATTs
matrix list r(seatt)  // Standard errors
local att_earn = r(att)[1,1]
```

## Basic Workflow

```stata
// STEP 1: Estimate Propensity Score
logit treatment age c.age#c.age education income married children i.region
predict pscore, pr

// Check distribution
summarize pscore, detail
by treatment, sort: summarize pscore, detail

// STEP 2: Perform Matching
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common

display "ATT: " r(att)
display "SE: " r(seatt)

// STEP 3: Check Balance
pstest age education income married, both graph
psgraph

// STEP 4: Examine matches
list treatment earnings pscore _pscore _weight if _support==1 in 1/20
```

### Propensity Score Estimation

**Method 1: External estimation (recommended for full control):**

```stata
logit treatment age c.age#c.age education income married children i.region
predict pscore, pr
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1)
```

**Method 2: Internal estimation:**

```stata
// psmatch2 estimates propensity score automatically; saved in _pscore
psmatch2 treatment age education income married, ///
    outcome(earnings) logit neighbor(1)
summarize _pscore
```

**Covariate selection gotchas:**
```stata
// DO include: pre-treatment variables that affect treatment AND outcome
// DON'T include: post-treatment variables, instrumental variables, perfect predictors of treatment
```

**Specification testing:**

```stata
// Compare propensity score models, then match with each and compare balance
foreach i of numlist 1/3 {
    psmatch2 treatment, outcome(earnings) pscore(ps`i') neighbor(1) common
    pstest age education income married, both
}
```

## Matching Algorithms

### Nearest Neighbor Matching

```stata
// With replacement (default) -- controls can be reused
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1)
tab _weight if treatment==0   // check reuse frequency

// Without replacement -- each control used at most once
// NOTE: order-dependent; set seed for reproducibility
set seed 12345
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) noreplacement
```

**K-nearest neighbors (bias-variance tradeoff):**

```stata
foreach k of numlist 1 3 5 10 {
    quietly psmatch2 treatment, outcome(earnings) pscore(pscore) ///
        neighbor(`k') common
    display "K=`k': ATT = " r(att) ", SE = " r(seatt)
}
```

### Mahalanobis Distance Matching

```stata
// Match on covariates directly
psmatch2 treatment age education income, ///
    outcome(earnings) mahal(age education income) neighbor(1)

// Combine propensity score with Mahalanobis on key variables
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    mahal(age education) neighbor(1)

// With caliper: restrict to pscore distance < 0.05,
// then among valid matches choose nearest by Mahalanobis on age
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    mahal(age) neighbor(1) caliper(0.05) common
```

### Caliper Matching

```stata
// Common rule of thumb: caliper = 0.25 * SD(propensity score)
quietly summarize pscore
local caliper = 0.25 * r(sd)

psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    neighbor(1) caliper(`caliper') common

// Check how many treated units lost to caliper
tab _support treatment, row
count if _support==0 & treatment==1
```

### Radius Matching

```stata
// Match each treated to ALL controls within specified distance
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    radius caliper(0.05) common
```

### Kernel Matching

```stata
// Epanechnikov kernel (default, theoretically optimal)
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    kernel kerneltype(epan) bwidth(0.06) common

// Other kernels: normal, biweight, tricube, uniform
// Usually little difference in practice
```

**Bandwidth selection:**

```stata
// Silverman's rule of thumb
quietly summarize pscore
local bw_silverman = 1.06 * r(sd) * r(N)^(-1/5)

// Test range of bandwidths
foreach bw of numlist 0.02 0.04 0.06 0.08 0.10 {
    quietly psmatch2 treatment, outcome(earnings) pscore(pscore) ///
        kernel kerneltype(epan) bwidth(`bw') common
    display "BW=" %5.2f `bw' ": ATT=" %7.2f r(att) ", SE=" %6.2f r(seatt)
}
```

### Local Linear Matching

```stata
// Better boundary properties than kernel; more robust to bandwidth choice
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    llr kerneltype(epan) bwidth(0.06) common
```

## Common Support

```stata
// Always use the common option
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common

// _support variable indicates common support membership
tab _support

// Manual common support calculation
summarize pscore if treatment==1
local min_t = r(min)
local max_t = r(max)
summarize pscore if treatment==0
local min_c = r(min)
local max_c = r(max)
local lower = max(`min_t', `min_c')
local upper = min(`max_t', `max_c')
display "Common support: [" `lower' ", " `upper' "]"
```

**Trimming strategies:**

```stata
// Min-Max: keep overlapping region only
keep if pscore >= max(`min_t', `min_c') & pscore <= min(`max_t', `max_c')

// Percentile trimming
_pctile pscore, p(2.5 97.5)
keep if pscore >= r(r1) & pscore <= r(r2)

// Extreme value trimming
drop if pscore < 0.1 | pscore > 0.9
```

## ATT, ATE, ATU

```stata
// ATT (primary output of psmatch2)
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common
local att = r(att)

// ATU: reverse the treatment indicator
gen treatment_rev = 1 - treatment
psmatch2 treatment_rev, outcome(earnings) pscore(pscore) neighbor(1) common
local atu = r(att)
drop treatment_rev

// ATE = pi * ATT + (1-pi) * ATU
summarize treatment
local ate = r(mean) * `att' + (1-r(mean)) * `atu'
```

### Multiple Outcomes

```stata
// Specify multiple outcomes simultaneously
psmatch2 treatment, pscore(pscore) ///
    outcome(earnings employment wage hours) ///
    neighbor(1) common

// Results stored as matrices
matrix list r(att)    // Row vector of ATTs
matrix list r(seatt)
local att_earn = r(att)[1,1]
local att_employ = r(att)[1,2]
```

### Treatment Effect Heterogeneity

```stata
// Subgroup analysis: re-estimate propensity score within each subgroup
preserve
    keep if education < 12
    logit treatment age income married
    predict ps_low, pr
    psmatch2 treatment, outcome(earnings) pscore(ps_low) neighbor(1) common
    local att_low_ed = r(att)
restore
```

## Balance Assessment (pstest)

```stata
// After matching
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common

// Comprehensive balance test
pstest age education income married children, both graph

// Output columns:
// %bias        : Standardized bias before and after matching
// %reduct      : Percent reduction in bias
// t-test p-val : After-matching p-value for difference in means
// V(T)/V(C)    : Variance ratio (target: between 0.5 and 2.0)
```

**Balance rules of thumb:**
- |standardized bias| < 5%: Good
- |standardized bias| 5-10%: Acceptable
- |standardized bias| > 10%: Poor -- re-specify

**Pseudo R-squared check:**

```stata
// Before matching
logit treatment age education income married children urban
local r2_before = e(r2_p)

// After matching (on matched sample)
logit treatment age education income married children urban ///
    if _support==1 [weight=_weight]
local r2_after = e(r2_p)

// Pseudo R-squared should drop substantially (ideally near 0)
display "Before: " `r2_before' " After: " `r2_after'
```

**Joint balance test:**

```stata
hotelling age education income if _support==1, by(treatment)
```

## Comparison: psmatch2 vs teffects psmatch

| Feature | psmatch2 | teffects psmatch |
|---------|----------|------------------|
| Source | User-written (SSC) | Built-in Stata |
| Propensity score | External or internal | Internal only |
| Matching algorithms | NN, kernel, LLR, radius | NN only |
| Common support | Flexible control | Automatic |
| Balance testing | `pstest` | `tebalance` commands |
| Variables created | _pscore, _weight, _pdif, etc. | Standard `predict` |
| Post-estimation | Limited | Full teffects suite |
| Standard errors | Analytic (no AI correction) | Abadie-Imbens automatic |
| Survey weights | Manual | Built-in (`[pweight=]`) |

**Equivalent analysis with both:**

```stata
// psmatch2
logit treatment age education income married
predict pscore, pr
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) caliper(0.05) common
pstest age education income married, both

// teffects psmatch
teffects psmatch (earnings) (treatment age education income married), ///
    att nn(1) caliper(0.05)
tebalance summarize
teffects overlap
```

**Use psmatch2 when:** need kernel/LLR/radius matching, multiple outcomes, Mahalanobis distance, or detailed match-level diagnostics.

**Use teffects when:** NN matching suffices, want integrated post-estimation (`predict`, `margins`), proper variance estimation, or survey weights.

### Using psmatch2 Weights in Regression

```stata
// After kernel/radius matching, use weights for bias-corrected regression
psmatch2 treatment, outcome(earnings) pscore(pscore) kernel common

gen ipw_weight = .
replace ipw_weight = 1 if treatment==1 & _support==1
replace ipw_weight = _weight if treatment==0 & _support==1

regress earnings treatment age education income ///
    if _support==1 [pweight=ipw_weight], vce(robust)
```

## Saving Matched Samples

```stata
// Save matched sample only
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common
preserve
    keep if _support==1
    save "matched_sample.dta", replace
restore

// Export
keep if _support==1
export delimited using "matched_data.csv", replace
```

## Bootstrap Standard Errors

psmatch2's analytic SEs do not account for propensity score estimation uncertainty. Bootstrap is recommended.

**Using Stata's bootstrap command:**

```stata
capture program drop psmatch_boot
program define psmatch_boot, rclass
    quietly logit treatment age education income married
    quietly predict ps_temp, pr
    quietly psmatch2 treatment, outcome(earnings) pscore(ps_temp) ///
        neighbor(1) common
    return scalar att = r(att)
    drop ps_temp
end

bootstrap r(att), reps(1000) seed(12345): psmatch_boot
```

**Stratified bootstrap (preserves treatment proportions):**

```stata
capture program drop psmatch_boot_strat
program define psmatch_boot_strat, rclass
    preserve
        bsample, strata(treatment)
        quietly logit treatment age education income married
        quietly predict ps_temp, pr
        quietly psmatch2 treatment, outcome(earnings) pscore(ps_temp) ///
            neighbor(1) common
        return scalar att = r(att)
        drop ps_temp
    restore
end

bootstrap r(att), reps(1000) seed(12345): psmatch_boot_strat
```

**Cluster bootstrap:**

```stata
bootstrap r(att), reps(1000) seed(12345) cluster(school_id): psmatch_boot
```

**Bootstrap with multiple outcomes:**

```stata
capture program drop psmatch_boot_multi
program define psmatch_boot_multi, rclass
    quietly logit treatment age education income married
    quietly predict ps_temp, pr
    quietly psmatch2 treatment, pscore(ps_temp) ///
        outcome(earnings employment wage) neighbor(1) common
    matrix att_vec = r(att)
    return scalar att_earnings = att_vec[1,1]
    return scalar att_employment = att_vec[1,2]
    return scalar att_wage = att_vec[1,3]
    drop ps_temp
end

bootstrap r(att_earnings) r(att_employment) r(att_wage), ///
    reps(1000) seed(12345): psmatch_boot_multi
```

## Complete Analysis Template

```stata
clear all
set more off
version 17
set seed 20231123
log using "psm_analysis.log", replace text

// 1. DATA PREPARATION
use "your_data.dta", clear
local treatment "training"
local outcome "earnings"
local covariates "age education income married children urban"
misstable summarize `treatment' `outcome' `covariates'
drop if missing(`treatment') | missing(`outcome')
foreach var of varlist `covariates' {
    drop if missing(`var')
}

// 2. PROPENSITY SCORE ESTIMATION
logit `treatment' `covariates' c.age#c.age c.income#c.income
predict pscore, pr
summarize pscore, detail
count if pscore < 0.01 | pscore > 0.99

// 3. CALIPER
quietly summarize pscore
local caliper = 0.25 * r(sd)

// 4. MATCHING (try multiple methods)

// NN(1:1)
psmatch2 `treatment', outcome(`outcome') pscore(pscore) ///
    neighbor(1) caliper(`caliper') common
local att_nn1 = r(att)
local se_nn1 = r(seatt)

// NN(1:3)
psmatch2 `treatment', outcome(`outcome') pscore(pscore) ///
    neighbor(3) caliper(`caliper') common
local att_nn3 = r(att)

// Kernel
psmatch2 `treatment', outcome(`outcome') pscore(pscore) ///
    kernel kerneltype(epan) bwidth(0.06) common
local att_kernel = r(att)

// LLR
psmatch2 `treatment', outcome(`outcome') pscore(pscore) ///
    llr kerneltype(epan) bwidth(0.06) common
local att_llr = r(att)

// Radius
psmatch2 `treatment', outcome(`outcome') pscore(pscore) ///
    radius caliper(`caliper') common
local att_radius = r(att)

// 5. BALANCE ASSESSMENT (on preferred method)
psmatch2 `treatment', outcome(`outcome') pscore(pscore) ///
    neighbor(1) caliper(`caliper') common
pstest `covariates', both graph
psgraph

// 6. BIAS-CORRECTED REGRESSION ON MATCHED SAMPLE
regress `outcome' `treatment' `covariates' ///
    if _support==1 [aweight=_weight], vce(robust)

// 7. BOOTSTRAP SE
capture program drop psmatch_boot
program define psmatch_boot, rclass
    quietly logit `treatment' `covariates' c.age#c.age c.income#c.income
    quietly predict ps_temp, pr
    quietly psmatch2 `treatment', outcome(`outcome') pscore(ps_temp) ///
        neighbor(1) caliper(`caliper') common
    return scalar att = r(att)
    drop ps_temp
end

bootstrap r(att), reps(1000) seed(12345): psmatch_boot

// 8. SENSITIVITY ANALYSIS
foreach c of numlist 0.01 0.025 0.05 0.075 0.1 {
    quietly psmatch2 `treatment', outcome(`outcome') pscore(pscore) ///
        neighbor(1) caliper(`c') common
    display "Caliper " %5.3f `c' ": ATT=" %7.2f r(att) " SE=" %5.2f r(seatt)
}

// 9. SAVE RESULTS
save "data_with_matches.dta", replace
preserve
    keep if _support==1
    save "matched_sample.dta", replace
restore

log close
```

## DiD-PSM Example

```stata
// Match on pre-treatment characteristics, then run DiD on matched sample
// Step 1: Estimate pscore using pre-period data
preserve
    keep if period==0
    logit treated pop gdp mfg
    predict pscore, pr
    keep state pscore
    save "temp_pscore.dta", replace
restore
merge m:1 state using "temp_pscore.dta", nogen

// Step 2: Match
psmatch2 treated if period==0, pscore(pscore) outcome(employment) ///
    neighbor(1) common
pstest pop gdp mfg, both

// Step 3: DiD on matched sample
gen treat_post = treated * post
regress employment treated post treat_post ///
    if _support==1 [aweight=_weight], vce(cluster state)
```

## Common Pitfalls

1. **Including post-treatment variables** in propensity score
2. **Ignoring common support** -- always use `common` option and check `psgraph`
3. **Not checking balance** -- always run `pstest` after matching
4. **Over-fitting propensity score** -- goal is balance, not prediction
5. **Trusting analytic SEs** -- bootstrap to account for pscore estimation
6. **Not testing sensitivity** to caliper, K, and specification
7. **Order dependency with `noreplacement`** -- always `set seed` before

## Key References

- `help psmatch2` / `help pstest` / `help teffects`
- Caliendo & Kopeinig (2008): practical PSM guidance
- Abadie & Imbens (2006, 2016): matching standard errors
