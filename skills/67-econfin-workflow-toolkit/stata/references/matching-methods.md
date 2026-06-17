# Matching Methods in Stata

## Table of Contents
1. [Propensity Score Estimation](#propensity-score-estimation)
2. [Nearest Neighbor Matching](#nearest-neighbor-matching)
3. [Caliper Matching](#caliper-matching)
4. [Kernel and Local Linear Matching](#kernel-and-local-linear-matching)
5. [The teffects psmatch Command](#the-teffects-psmatch-command)
6. [The psmatch2 User-Written Command](#the-psmatch2-user-written-command)
7. [Balance Assessment](#balance-assessment)
8. [Common Support and Trimming](#common-support-and-trimming)
9. [Matching Quality Diagnostics](#matching-quality-diagnostics)
10. [Combining Matching with Regression](#combining-matching-with-regression)
11. [Complete Matching Workflow](#complete-matching-workflow)
12. [Advanced Matching Topics](#advanced-matching-topics)

---

## Propensity Score Estimation

### Estimating Propensity Scores

```stata
* Logit (standard)
logit treatment age education income married urban
predict pscore, pr

* Probit alternative
probit treatment age education income married urban i.region
predict pscore_probit, pr

* Check distribution
histogram pscore, by(treatment)
tabstat pscore, by(treatment) statistics(mean sd min max p25 p50 p75)
```

### Choosing Covariates

```stata
* Include confounders (affect both treatment and outcome)
* Include variables that predict treatment or outcome
* DO NOT include post-treatment variables
* DO NOT include instrumental variables

logit training ///
    age c.age#c.age ///          // Age and age squared
    education ///                  // Years of education
    married children ///           // Demographics
    prior_earnings ///             // Pre-treatment outcome
    unemployment_duration ///      // Duration unemployed
    i.industry i.region            // Indicators
predict pscore_full, pr
```

### Trimming Propensity Scores

```stata
* Min-max common support
egen pscore_min_treat = min(pscore) if treatment==1
egen pscore_max_treat = max(pscore) if treatment==1
egen pscore_min_control = min(pscore) if treatment==0
egen pscore_max_control = max(pscore) if treatment==0
egen min_all = max(pscore_min_treat)
egen max_all = min(pscore_max_treat)
gen common_support = (pscore >= min_all & pscore <= max_all)
tab treatment common_support
keep if common_support==1

* Or simply drop extreme scores
drop if pscore < 0.1 | pscore > 0.9
```

---

## Nearest Neighbor Matching

### One-to-One Matching

```stata
* Using teffects
teffects psmatch (outcome) (treatment age education income), ///
    nn(1) ate caliper(0.05)

* Using psmatch2 (user-written)
ssc install psmatch2
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common

* View matches
list treatment earnings pscore _pscore _weight if _support==1 in 1/20
```

### Matching With vs Without Replacement

```stata
* With replacement (default in psmatch2) - lower bias, higher variance
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common

* Check how often controls are used
tab _weight if treatment==0

* Without replacement
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    neighbor(1) common noreplacement
```

### K-Nearest Neighbor Matching

```stata
teffects psmatch (earnings) (treatment age education income), nn(3) att caliper(0.05)
teffects psmatch (earnings) (treatment age education income), nn(5) att
tebalance summarize
```

### Mahalanobis Distance Matching

```stata
* Mahalanobis distance on covariates
psmatch2 treatment age education income, ///
    outcome(earnings) mahal(age education income) common

* Combine propensity score and Mahalanobis
psmatch2 treatment, pscore(pscore) outcome(earnings) ///
    mahal(age education) neighbor(1) common
```

---

## Caliper Matching

### Rule of Thumb: 0.25 * SD of Propensity Score

```stata
quietly summarize pscore
local caliper = 0.25 * r(sd)
display "Caliper: `caliper'"

teffects psmatch (earnings) (treatment age education income), ///
    nn(1) att caliper(`caliper')
```

### Sensitivity to Caliper Width

```stata
foreach c of numlist 0.01 0.025 0.05 0.1 {
    quietly teffects psmatch (earnings) (treatment age education income), ///
        nn(1) att caliper(`c')
    matrix results = r(table)
    local ate = results[1,1]
    local se = results[2,1]
    display "Caliper: `c', ATE: `ate', SE: `se'"
}
```

---

## Kernel and Local Linear Matching

### Kernel Matching

Each treated unit matched to weighted average of all controls; weights based on distance. Kernel types: Epanechnikov (default), Gaussian, biweight, tricube.

```stata
* Epanechnikov kernel
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    kernel kerneltype(epan) common bwidth(0.06)

* Gaussian kernel
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    kernel kerneltype(normal) common bwidth(0.06)

* Balance check
pstest age education income, both graph
```

### Bandwidth Selection

```stata
* Test different bandwidths (narrower = less bias, more variance)
foreach bw of numlist 0.02 0.04 0.06 0.08 0.10 {
    display _newline "Bandwidth: `bw'"
    quietly psmatch2 treatment, outcome(earnings) pscore(pscore) ///
        kernel kerneltype(epan) bwidth(`bw') att common
}

* Optimal bandwidth (rule of thumb)
quietly summarize pscore
local bw_opt = 1.06 * r(sd) * r(N)^(-1/5)
display "Optimal bandwidth: `bw_opt'"
```

### Local Linear Matching

Better boundary properties and more robust to bandwidth choice than kernel matching.

```stata
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    llr kerneltype(epan) bwidth(0.06) common att
```

---

## The teffects psmatch Command

Stata's built-in command with integrated variance estimation and post-estimation tools.

### Syntax

```stata
teffects psmatch (outcome_equation) (treatment_equation) [if] [in], ///
    [stat] [nneighbor(#)] [caliper(#)] [options]
```

### Examples

```stata
webuse cattaneo2, clear

* ATT with nearest neighbor
teffects psmatch (bweight) ///
    (mbsmoke mmarried c.mage##c.mage fbaby medu), ///
    att nn(1) caliper(0.1)

* Post-estimation
teffects overlap          // Overlap plot
tebalance summarize       // Balance check
tebalance density mage    // Density plot
```

### Generate Variables After Estimation

```stata
teffects psmatch (earnings) (training age education income), att
predict te, te          // Individual treatment effects
predict po0, po         // Potential outcome control
predict po1, po tlevel  // Potential outcome treated
predict ps, ps          // Propensity score
```

### Weights

```stata
* Sampling weights
teffects psmatch (earnings) (training age education income) ///
    [pweight=sampweight], att nn(1)

* Frequency weights
teffects psmatch (earnings) (training age education income) ///
    [fweight=freq], att nn(1)
```

---

## The psmatch2 User-Written Command

### Installation and Basic Workflow

```stata
ssc install psmatch2

* Step 1: Estimate propensity score
logit treatment age education income married
predict pscore, pr

* Step 2: Perform matching
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1) common

* Step 3: Check balance
pstest age education income, both graph

* Step 4: Assess common support
psgraph
```

### Matching Algorithms

```stata
* Nearest neighbor (default)
psmatch2 treatment, outcome(earnings) pscore(pscore) neighbor(1)

* Radius matching
psmatch2 treatment, outcome(earnings) pscore(pscore) radius caliper(0.05)

* Kernel matching
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    kernel kerneltype(epan) bwidth(0.06)

* Local linear regression
psmatch2 treatment, outcome(earnings) pscore(pscore) ///
    llr kerneltype(epan) bwidth(0.06)

* Stratification matching
psmatch2 treatment, outcome(earnings) pscore(pscore) nblocks(5)
```

### Variables Created by psmatch2

```stata
* _treated    : 1 if treated, 0 if control
* _support    : 1 if in common support
* _pscore     : Propensity score of matched control
* _weight     : Matching weight (# times used as match)
* _n1         : ID of 1st nearest neighbor
* _pdif       : |pscore - _pscore|
* _id         : Observation ID

* Check match quality
summarize _pdif
histogram _pdif, title("Propensity Score Differences")
```

### Multiple Outcomes

```stata
psmatch2 treatment, pscore(pscore) ///
    outcome(earnings wage_growth employment) ///
    neighbor(1) common
return list
```

---

## Balance Assessment

### Standardized Bias

Rule of thumb: |standardized bias| < 5% is acceptable after matching.

### pstest (after psmatch2)

```stata
pstest age education income married, both graph
* Shows: %bias before/after, %reduction, t-test p-values
```

### tebalance (after teffects)

```stata
teffects psmatch (earnings) (treatment age education income), att

tebalance summarize                  // Summary balance table
tebalance summarize, standardized    // Standardized differences
tebalance summarize, variances       // Variance ratios (good: 0.5 to 2)

* Visual balance
tebalance density age
tebalance box age education income

* Multiple covariates
foreach var of varlist age education income {
    tebalance density `var', name(g_`var', replace)
}
graph combine g_age g_education g_income
```

---

## Common Support and Trimming

### Visual Assessment

```stata
twoway (histogram pscore if treatment==0, color(blue%30) frequency) ///
       (histogram pscore if treatment==1, color(red%30) frequency), ///
    legend(label(1 "Control") label(2 "Treated")) ///
    title("Propensity Score Common Support")

* After psmatch2
psgraph

* After teffects
teffects overlap
teffects overlap, ptlevel(1) bin(20)
```

### Trimming Strategies

```stata
* Strategy 1: Min-max trimming
summarize pscore if treatment==1
local min_t = r(min)
local max_t = r(max)
summarize pscore if treatment==0
local min_c = r(min)
local max_c = r(max)
local lower = max(`min_t', `min_c')
local upper = min(`max_t', `max_c')
gen common_support = (pscore >= `lower' & pscore <= `upper')

* Strategy 2: Percentile trimming
_pctile pscore, p(5 95)
keep if pscore >= r(r1) & pscore <= r(r2)

* Strategy 3: psmatch2 common option (automatic)
psmatch2 treatment, pscore(pscore) outcome(earnings) neighbor(1) common
tab _support treatment
```

---

## Matching Quality Diagnostics

### Match Rate and Quality

```stata
* After psmatch2
tab _support treatment, row

* Propensity score distances
summarize _pdif if _support==1, detail
gen poor_match = (_pdif > 0.05) if _support==1
tab poor_match
```

### Pseudo R-squared Reduction

```stata
* Before matching
logit treatment age education income married
local r2_before = e(r2_p)

* After matching (should be much lower)
logit treatment age education income married if _support==1
local r2_after = e(r2_p)

display "Pseudo R² before: " `r2_before'
display "Pseudo R² after: " `r2_after'
display "Reduction: " (`r2_before' - `r2_after')/`r2_before'
```

### Sensitivity Analysis: Vary Parameters

```stata
* Vary number of neighbors
forvalues k = 1/5 {
    quietly teffects psmatch (earnings) (treatment age education income), ///
        att nn(`k') caliper(0.05)
    estimates store nn`k'
}
estimates table nn1 nn2 nn3 nn4 nn5, stats(N) b se

* Vary caliper width
foreach c of numlist 0.01 0.025 0.05 0.1 {
    quietly teffects psmatch (earnings) (treatment age education income), ///
        att nn(1) caliper(`c')
    estimates store cal`c'
}
estimates table cal*, stats(N) b se
```

### Compare with Other Methods

```stata
teffects psmatch (earnings) (treatment age education income), att
estimates store matching
teffects ra (earnings age education income) (treatment), att
estimates store regression
teffects ipw (earnings) (treatment age education income), att
estimates store ipw
teffects ipwra (earnings age education income) (treatment age education income), att
estimates store dr

estimates table matching regression ipw dr, ///
    stats(N) b(%9.2f) se(%9.2f) t p
```

---

## Combining Matching with Regression

### Regression Adjustment After Matching (Bias Correction)

```stata
* Match then regress on matched sample
psmatch2 treatment, pscore(pscore) outcome(earnings) neighbor(1) common

regress earnings treatment age education income ///
    if _support==1 [aweight=_weight], vce(robust)
* treatment coefficient is bias-corrected ATT
```

### Doubly Robust Alternative

```stata
teffects aipw (earnings age education income) ///
    (treatment age education income), att
```

### Matching + Difference-in-Differences

```stata
* Step 1: Estimate pscore from pre-period data
preserve
    keep if period==0
    logit treatment age education income baseline_outcome
    predict pscore, pr
    keep id pscore
    save temp_pscore, replace
restore
merge m:1 id using temp_pscore

* Step 2: Match on pre-period
psmatch2 treatment if period==0, pscore(pscore) neighbor(1) common

* Step 3: DiD on matched sample
gen treat_post = treatment * post
regress outcome treatment post treat_post ///
    if _support==1 [aweight=_weight], vce(cluster id)
* treat_post coefficient is DiD-matched estimator
```

### Entropy Balancing

```stata
ssc install ebalance

ebalance treatment age education income married, generate(eb_weight)
regress earnings treatment age education income [aweight=eb_weight], vce(robust)
```

### IPW with Regression

```stata
gen ipw = treatment/pscore + (1-treatment)/(1-pscore)
summarize ipw, detail
replace ipw = . if ipw > 10  // Trim extreme weights
regress earnings treatment age education income [pweight=ipw], vce(robust)
```

---

## Complete Matching Workflow

### Workflow 1: Basic PSM Analysis

```stata
use "program_evaluation.dta", clear

* Check for missing data
misstable summarize treatment earnings age education income married
drop if missing(treatment) | missing(earnings)

* STEP 1: Propensity score estimation
logit treatment age c.age##c.age education income married i.region
predict pscore, pr
summarize pscore, detail
by treatment, sort: summarize pscore, detail

* STEP 2: Common support
summarize pscore if treatment==1
local min_treat = r(min)
local max_treat = r(max)
summarize pscore if treatment==0
local min_control = r(min)
local max_control = r(max)
gen common_support = (pscore >= max(`min_treat', `min_control') & ///
                      pscore <= min(`max_treat', `max_control'))
tab treatment common_support, row
keep if common_support==1

* STEP 3: Matching
psmatch2 treatment, pscore(pscore) outcome(earnings) ///
    neighbor(1) caliper(0.05) common

* STEP 4: Balance assessment
pstest age education income married, both graph
psgraph

* STEP 5: Match quality
summarize _pdif if _support==1, detail
tab _support treatment, row

* STEP 6: Sensitivity - multiple algorithms
estimates store nn1
psmatch2 treatment, pscore(pscore) outcome(earnings) neighbor(3) caliper(0.05) common
estimates store nn3
psmatch2 treatment, pscore(pscore) outcome(earnings) ///
    kernel kerneltype(epan) bwidth(0.06) common
estimates store kernel
psmatch2 treatment, pscore(pscore) outcome(earnings) ///
    llr kerneltype(epan) bwidth(0.06) common
estimates store llr

* STEP 7: Bias-corrected regression
regress earnings treatment age education income ///
    if _support==1 [aweight=_weight], vce(robust)
estimates store matched_reg

* STEP 8: Report
esttab nn1 nn3 kernel llr matched_reg, ///
    title("Treatment Effect Estimates") ///
    mtitles("NN(1)" "NN(3)" "Kernel" "LLR" "Reg Adj") ///
    stats(N, labels("Observations")) ///
    b(%9.2f) se(%9.2f) star(* 0.10 ** 0.05 *** 0.01)
```

### Workflow 2: Subgroup and Quantile Analysis

```stata
use "program_evaluation.dta", clear
logit treatment age education income married urban
predict pscore, pr

* Overall ATT
teffects psmatch (earnings) (treatment age education income married urban), ///
    att nn(1) caliper(0.05)
estimates store att_overall

* Subgroup by education
foreach level in "low" "high" {
    preserve
    if "`level'" == "low" keep if education < 12
    if "`level'" == "high" keep if education >= 12
    teffects psmatch (earnings) (treatment age income married urban), ///
        att nn(1) caliper(0.05)
    estimates store att_`level'_ed
    restore
}

* Quantile treatment effects on matched sample
psmatch2 treatment, pscore(pscore) outcome(earnings) neighbor(1) caliper(0.05) common
foreach q of numlist 0.25 0.50 0.75 {
    qreg earnings treatment age education income ///
        if _support==1 [aweight=_weight], quantile(`q')
    estimates store qte_`q'
}
estimates table qte_0.25 qte_0.50 qte_0.75, stats(N) b(%9.2f) se(%9.2f)
```

### Workflow 3: Multiple Outcomes

```stata
* Single propensity score for all outcomes
logit treatment age education income married children urban i.region
predict pscore, pr

* Match once with psmatch2
psmatch2 treatment, pscore(pscore) ///
    outcome(earnings employment wage) neighbor(1) caliper(0.05) common

* Or outcome-specific with teffects
teffects psmatch (earnings) (treatment age education income married), att nn(1) caliper(0.05)
estimates store earnings_te
teffects psmatch (employment) (treatment age education income married), att nn(1) caliper(0.05)
estimates store employment_te
teffects psmatch (wage) (treatment age education income married) ///
    if employment==1, att nn(1) caliper(0.05)
estimates store wage_te

estimates table earnings_te employment_te wage_te, stats(N) b(%9.2f) se(%9.2f) star
```

---

## Advanced Matching Topics

### Coarsened Exact Matching (CEM)

```stata
ssc install cem

cem age education income, treatment(treatment) showbreaks

* Custom breakpoints
cem age (#10) education (#5) income (#10), treatment(treatment)

* Estimate with CEM weights
regress earnings treatment age education income [iweight=cem_weights]
imbalance age education income, treatment(treatment)
```

### Matching with Time-Varying Treatments

```stata
xtset id time
forvalues t = 1/10 {
    preserve
        keep if time == `t'
        logit treatment_`t' lag_x1 lag_x2 lag_x3
        predict pscore_`t', pr
        psmatch2 treatment_`t', pscore(pscore_`t') outcome(y_`t') neighbor(1) common
        matrix att_`t' = r(att)
    restore
}
```

### Matching + IV

```stata
psmatch2 treatment, pscore(pscore) outcome(earnings) neighbor(1) common
ivregress 2sls earnings (treatment = instrument) ///
    age education income ///
    if _support==1 [aweight=_weight], vce(robust)
```

### Machine Learning Propensity Scores

```stata
lasso logit treatment age education income married children ///
    urban i.region i.industry, selection(cv)
predict pscore_lasso, pr
psmatch2 treatment, pscore(pscore_lasso) outcome(earnings) ///
    neighbor(1) caliper(0.05) common
```

### Rosenbaum Bounds (Sensitivity to Unobservables)

```stata
ssc install rbounds

psmatch2 treatment, pscore(pscore) outcome(earnings) neighbor(1) common
rbounds earnings treatment if _support==1

* Gamma = 1: No hidden bias
* Shows critical Gamma where results become insignificant
```

### Multilevel Propensity Scores

```stata
* Mixed effects logit for clustered data
melogit treatment age ability parent_education || school_id:, or
predict pscore_ml, pr
```

---

## Best Practices Summary

### Common Pitfalls
1. Including post-treatment variables in propensity score
2. Ignoring common support violations
3. Not checking balance after matching
4. Over-fitting propensity score model
5. Not reporting sensitivity analyses

### Recommended Workflow
1. Always check balance: `pstest` or `tebalance summarize`
2. Visualize common support: `psgraph` or `teffects overlap`
3. Try multiple matching methods (NN, kernel, local linear)
4. Report sensitivity to caliper, neighbors, covariates
5. Use regression adjustment for bias correction
6. Compare with IPW and doubly robust estimators
