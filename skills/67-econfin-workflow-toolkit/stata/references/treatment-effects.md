# Treatment Effects and Causal Inference

## Table of Contents
1. [Treatment Effect Parameters](#treatment-effect-parameters)
2. [The teffects Command Overview](#the-teffects-command-overview)
3. [Regression Adjustment](#regression-adjustment)
4. [Propensity Score Methods](#propensity-score-methods)
5. [Inverse Probability Weighting](#inverse-probability-weighting)
6. [Doubly Robust Estimation](#doubly-robust-estimation)
7. [Diagnostics and Validation](#diagnostics-and-validation)
8. [Balance Checking](#balance-checking)
9. [Sensitivity Analysis](#sensitivity-analysis)
10. [Interpretation and Reporting](#interpretation-and-reporting)
11. [Complete Workflow Examples](#complete-workflow-examples)

---

## Treatment Effect Parameters

### Choosing the Right Parameter

- **ATE** (Average Treatment Effect): Effect across entire population. Use for policy questions about population-wide interventions.
- **ATET/ATT** (on the Treated): Effect among those who received treatment. Use for evaluating existing programs.
- **POM** (Potential Outcomes Mean): Expected outcome under treatment or control. ATE = POM1 - POM0.

```stata
* Policy questions → ATE
teffects ra (wage age education) (training), ate

* Program evaluation → ATET
teffects ra (wage age education) (training), atet

* Compare both
teffects ra (wage age education) (training), ate
estimates store ate_model
teffects ra (wage age education) (training), atet
estimates store atet_model
estimates table ate_model atet_model
```

---

## The teffects Command Overview

### Syntax Structure

```stata
teffects estimator (outcome_model) (treatment_model) [if] [in] [weight], statistic [options]
```

### Available Estimators

| Estimator | Method | Requires |
|-----------|--------|----------|
| `ra` | Regression adjustment | Outcome model |
| `ipw` | Inverse probability weighting | Treatment model |
| `ipwra` | IPW with regression adjustment | Both models |
| `aipw` | Augmented IPW (doubly robust) | Both models |
| `psmatch` | Propensity score matching | Treatment model |
| `nnmatch` | Nearest-neighbor matching | Covariates |

### General Options

```stata
* Display potential outcomes means
teffects ra (wage education age) (training), ate pomeans

* Variance estimation
teffects ra (wage education age) (training), ate vce(robust)
teffects ra (wage education age) (training), ate vce(cluster id)
teffects ra (wage education age) (training), ate vce(bootstrap, reps(1000))

* Nonlinear models for outcome and treatment
teffects ra (wage education age, poisson) (training, probit), ate
```

---

## Regression Adjustment

RA estimates treatment effects by fitting separate outcome regressions per treatment group, predicting potential outcomes for all observations, then averaging differences.

### Implementation

```stata
webuse cattaneo2, clear

* Simple regression adjustment
teffects ra (mbsmoke mmarried mage fbaby) (prenatal), ate

* Display potential outcomes means
teffects ra (mbsmoke mmarried mage fbaby) (prenatal), ate pomeans
```

### Specifying Outcome Models

```stata
* Linear model (default)
teffects ra (outcome c.age##c.age education) (treatment), ate

* Logit for binary outcomes
teffects ra (binary_outcome age education, logit) (treatment), ate

* Probit for binary outcomes
teffects ra (binary_outcome age education, probit) (treatment), ate

* Poisson for count outcomes
teffects ra (count_outcome age education, poisson) (treatment), ate

* Heteroskedastic Probit
teffects ra (binary_outcome age education, hetprobit) (treatment), ate
```

### Interactions and Nonlinearities

```stata
* Polynomial terms
teffects ra (wage c.age##c.age c.education##c.education) (training), ate

* Categorical variables
teffects ra (wage i.education i.region age) (training), ate

* Interactions between covariates
teffects ra (wage c.age##i.education) (training), ate
```

### Practical Example

```stata
sysuse nlsw88, clear
generate training = (industry >= 4 & industry <= 7)

* Estimate ATE with regression adjustment
teffects ra (wage age grade hours tenure south) (training), ate

* Robust standard errors
teffects ra (wage age grade hours tenure south) (training), ate vce(robust)

* Store and compare ATE vs ATET
estimates store ra_ate
teffects ra (wage age grade hours tenure south) (training), atet
estimates store ra_atet
estimates table ra_ate ra_atet, star stats(N)
```

**Key tradeoff:** Efficient when outcome model is correctly specified, but biased if misspecified. Extrapolation problems when treatment groups differ substantially.

---

## Propensity Score Methods

### Propensity Score Matching

```stata
* Default: Nearest-neighbor matching with one match
teffects psmatch (wage) (training age education experience), ate

* Number of neighbors
teffects psmatch (wage) (training age education), ate nn(3)

* Caliper (maximum distance)
teffects psmatch (wage) (training age education), ate caliper(0.1)

* Combined
teffects psmatch (wage) (training age education), ate nn(3) caliper(0.05)

* Specify logit or probit for propensity score
teffects psmatch (wage) (training age education, logit), ate
teffects psmatch (wage) (training age education, probit), ate
```

**Note:** `psmatch` uses matching with replacement by default.

### Complete Matching Example

```stata
webuse cattaneo2, clear

* ATET with flexible propensity score model
teffects psmatch (bweight) ///
    (mbsmoke mmarried c.mage##c.mage fbaby i.medu prenatal1), ///
    atet

* With caliper to ensure close matches
teffects psmatch (bweight) ///
    (mbsmoke mmarried mage fbaby medu prenatal1), ///
    ate caliper(0.1)
```

### Visualizing Propensity Scores

```stata
* Generate propensity scores
teffects psmatch (wage) (training age education), ate generate(ps)

* Plot distribution
twoway (histogram ps if training==0, color(blue%30)) ///
       (histogram ps if training==1, color(red%30)), ///
       legend(label(1 "Control") label(2 "Treatment")) ///
       title("Propensity Score Distribution")

* Density plots
twoway (kdensity ps if training==0, lcolor(blue)) ///
       (kdensity ps if training==1, lcolor(red)), ///
       legend(label(1 "Control") label(2 "Treatment"))
```

### Nearest-Neighbor Matching

Matches on covariates directly, not propensity scores.

```stata
* Basic nearest-neighbor matching
teffects nnmatch (wage age education) (training), ate

* Mahalanobis distance (accounts for correlations)
teffects nnmatch (wage age education) (training), ate metric(maha)

* Bias correction
teffects nnmatch (wage age education) (training), ate biasadj(education)

* Exact matching on categorical variable
teffects nnmatch (wage age education) (training), ate ematch(region)
```

---

## Inverse Probability Weighting

IPW weights observations by the inverse of the probability of treatment received, creating a pseudo-population where treatment is independent of covariates.

### Basic IPW

```stata
teffects ipw (wage) (training age education), ate
teffects ipw (wage) (training age education), atet
```

### Treatment Model Specification

```stata
* Logit (default), probit, or heteroskedastic probit
teffects ipw (wage) (training age education, logit), ate
teffects ipw (wage) (training age education, probit), ate
teffects ipw (wage) (training age education, hetprobit(medu)), ate

* Interactions in treatment model
teffects ipw (wage) (training c.age##c.age c.education##i.region), ate
```

### Weight Diagnostics

```stata
* After IPW estimation, check for extreme weights
teffects ipw (wage) (training age education), ate
predict pscore, ps
summarize pscore, detail

* Create and examine weights
generate weight_ate = training/pscore + (1-training)/(1-pscore)
tabstat weight_ate, statistics(min p1 p5 p25 p50 p75 p95 p99 max)

* Identify problematic observations
list id training pscore weight_ate if weight_ate > 20

* Trimmed analysis for extreme propensity scores
teffects ipw (wage) (training age education) if inrange(pscore, 0.1, 0.9), ate
```

---

## Doubly Robust Estimation

Consistent if either the outcome model OR the treatment model is correctly specified (not necessarily both).

### AIPW (Augmented IPW)

```stata
* Basic AIPW
teffects aipw (wage age education) (training age education), ate

* Different variables in each model
teffects aipw (wage age education) ///
    (training age education i.region), ate

* Nonlinear specifications
teffects aipw (wage c.age##c.age education, linear) ///
    (training age education i.region, logit), ate

* Binary outcome
teffects aipw (employed age education, logit) ///
    (training age education, probit), ate
```

### IPWRA (IPW with Regression Adjustment)

```stata
teffects ipwra (wage age education) (training age education), ate
teffects ipwra (wage c.age##c.age c.education##c.education) ///
    (training age education), ate
```

### AIPW vs. IPWRA

- **AIPW**: Uses weighted regression, generally more efficient, standard choice
- **IPWRA**: Separate regressions per treatment group, allows different functional forms by group

### Model Specification Strategy

```stata
* Same covariates in both models
teffects aipw (wage age education experience) ///
    (training age education experience), ate

* Richer outcome model
teffects aipw (wage c.age##c.age c.education##c.education experience) ///
    (training age education experience), ate

* Richer treatment model
teffects aipw (wage age education) ///
    (training c.age##c.age c.education##c.education i.region), ate

* Include different predictors if theoretically justified
* (outcome predictors in outcome model, treatment predictors in treatment model)
teffects aipw (wage age education outcome_predictor) ///
    (training age education treatment_predictor), ate
```

---

## Diagnostics and Validation

### Overlap Plots and Common Support

```stata
* Built-in overlap plot (after any teffects estimation)
teffects overlap
teffects overlap, ptlevel(1)

* Manual overlap plot
teffects psmatch (wage) (training age education), ate generate(ps)
twoway (histogram ps if training==0, width(0.05) color(blue%30)) ///
       (histogram ps if training==1, width(0.05) color(red%30)), ///
       xlabel(0(0.1)1) ///
       legend(order(1 "Control" 2 "Treated")) ///
       title("Propensity Score Overlap")
```

### Identifying Overlap Problems

```stata
predict ps_estimated, ps
bysort training: summarize ps_estimated, detail
tabstat ps_estimated, by(training) stats(min max)

* Restrict to common support
teffects psmatch (wage) (training age education) ///
    if inrange(ps_estimated, 0.1, 0.9), ate
```

### tebalance Command

```stata
* After any teffects estimation
tebalance summarize            // Summary of covariate balance
tebalance density age          // Density plots
tebalance box age              // Box plots
teffects overlap               // Propensity score overlap
```

### Common Support Restrictions

```stata
* Trimming by propensity score
teffects ipw (wage) (training age education) ///
    if inrange(ps, 0.1, 0.9), ate

* Trimming by percentiles
_pctile ps, percentiles(5 95)
teffects ipw (wage) (training age education) ///
    if ps >= r(r1) & ps <= r(r2), ate
```

---

## Balance Checking

### Standardized Differences

```stata
* After teffects estimation
tebalance summarize

* Interpret standardized differences:
* |std diff| < 0.1: Good balance
* |std diff| < 0.25: Acceptable
* |std diff| > 0.25: Poor balance

* Variance ratios:
* Between 0.5 and 2: Good
* Outside this range: Concerning
```

### Manual Balance Tables

```stata
* Calculate standardized differences manually
foreach var of varlist age education income {
    quietly summarize `var' if training == 1
    local m1 = r(mean)
    local sd1 = r(sd)
    quietly summarize `var' if training == 0
    local m0 = r(mean)
    local sd0 = r(sd)
    local std_diff = (`m1' - `m0') / sqrt((`sd1'^2 + `sd0'^2) / 2)
    display "Standardized difference for `var': " `std_diff'
}
```

### Weighted Balance After IPW

```stata
teffects ipw (wage) (training age education), ate
predict ps, ps
generate ipw = training/ps + (1-training)/(1-ps)

foreach var of varlist age education {
    quietly summarize `var' [aw=ipw] if training == 1
    local m1 = r(mean)
    quietly summarize `var' [aw=ipw] if training == 0
    local m0 = r(mean)
    display "`var' weighted mean difference: " `m1' - `m0'
}
```

### Love Plots

```stata
* Create data for Love plot (not built-in)
preserve
clear
input str20 variable before_match after_match
"Age"           0.45    0.08
"Education"     0.38    0.12
"Income"        0.52    0.15
"Experience"    0.41    0.09
end
generate order = _n

twoway (scatter order before_match, msymbol(circle) mcolor(red)) ///
       (scatter order after_match, msymbol(diamond) mcolor(blue)), ///
       ylabel(1 "Age" 2 "Education" 3 "Income" 4 "Experience", ///
              angle(0) noticks) ///
       ytitle("") xtitle("Standardized Difference") ///
       xline(0.1, lcolor(black) lpattern(dash)) ///
       xline(-0.1, lcolor(black) lpattern(dash)) ///
       xline(0, lcolor(black)) ///
       legend(order(1 "Before Matching" 2 "After Matching")) ///
       title("Covariate Balance: Love Plot")
restore
```

---

## Sensitivity Analysis

### Varying Model Specifications

```stata
teffects ra (wage age education) (training), ate
estimates store spec1
teffects ra (wage age education experience) (training), ate
estimates store spec2
teffects ra (wage c.age##c.age education experience) (training), ate
estimates store spec3
teffects ra (wage age education experience i.region) (training), ate
estimates store spec4

estimates table spec1 spec2 spec3 spec4, ///
    star stats(N) b(%7.2f) se(%7.2f)

coefplot spec1 spec2 spec3 spec4, ///
    drop(_cons) xline(0) ///
    title("Sensitivity to Model Specification")
```

### Placebo Tests

```stata
* Effect on outcome that should NOT be affected
teffects ra (earnings_before_training age education) ///
    (training), ate
* Should be close to zero if no selection bias

* Placebo treatment test on non-participants
generate placebo_treatment = uniform() < 0.5 if training == 0
teffects ra (wage age education) (placebo_treatment), ate
```

### Comparing Methods

```stata
teffects ra (wage age education) (training), ate
estimates store ra
teffects ipw (wage) (training age education), ate
estimates store ipw
teffects aipw (wage age education) (training age education), ate
estimates store aipw
teffects psmatch (wage) (training age education), ate
estimates store psm

estimates table ra ipw aipw psm, star stats(N) ///
    title("Sensitivity Across Methods")
* Similar estimates → robust finding; different → investigate
```

---

## Interpretation and Reporting

### Understanding Output

```stata
teffects aipw (wage age education) (training age education), ate
* Output: (1) Iteration log, (2) ATE row, (3) POmean rows, (4) Model parameters

* Formal test and linear combination
test _b[ATE:r1vs0.training] = 0
lincom _b[ATE:r1vs0.training]
```

### Effect Sizes

```stata
* ATE as percentage of control mean
teffects ra (wage age education) (training), ate pomeans
nlcom (pct_effect: _b[ATE:r1vs0.training] / _b[POmean:0.training] * 100)

* Cohen's d
quietly summarize wage
local sd = r(sd)
nlcom (cohens_d: _b[ATE:r1vs0.training] / `sd')
```

### Publication Tables

```stata
teffects ra (wage age education) (training), ate
estimates store m1
teffects ipw (wage) (training age education), ate
estimates store m2
teffects aipw (wage age education) (training age education), ate
estimates store m3

esttab m1 m2 m3 using "results.rtf", ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Treatment Effects Estimates") ///
    mtitles("RA" "IPW" "AIPW") ///
    scalars("N Observations") replace

* Forest plot
coefplot m1 m2 m3, ///
    keep(ATE:*) xline(0, lcolor(red)) ///
    title("Treatment Effect Estimates Across Methods") ///
    xtitle("Effect on Wage")
```

---

## Complete Workflow Examples

### Example 1: Program Evaluation (ATET)

```stata
* 1. Load and prepare data
sysuse nlsw88, clear
generate training = (industry >= 4 & industry <= 7)

* 2. Descriptive statistics
tabstat wage age grade hours tenure, by(training) ///
    statistics(mean sd n) columns(statistics) format(%8.2f)
tab training

* 3. Check overlap
logit training age grade hours tenure south
predict ps_check, pr
histogram ps_check, by(training) bin(20)

* 4. Balance before adjustment
foreach var of varlist age grade hours tenure {
    quietly summarize `var' if training == 1
    local m1 = r(mean)
    local sd1 = r(sd)
    quietly summarize `var' if training == 0
    local m0 = r(mean)
    local sd0 = r(sd)
    local std_diff = (`m1' - `m0') / sqrt((`sd1'^2 + `sd0'^2) / 2)
    display "`var': " %5.3f `std_diff'
}

* 5. AIPW estimation (doubly robust)
teffects aipw (wage age grade hours tenure i.south) ///
    (training age grade hours tenure i.south), ///
    atet vce(robust)
estimates store atet_aipw

* 6. Diagnostics
tebalance summarize
teffects overlap

* 7. Sensitivity: Compare methods
teffects ra (wage age grade hours tenure i.south) (training), atet
estimates store atet_ra
teffects ipw (wage) (training age grade hours tenure i.south), atet
estimates store atet_ipw
estimates table atet_ra atet_ipw atet_aipw, ///
    star stats(N) b(%7.2f) se(%7.2f)

* 8. Effect size as percentage of control mean
teffects aipw (wage age grade hours tenure i.south) ///
    (training age grade hours tenure i.south), atet pomeans
nlcom (pct: _b[ATET:r1vs0.training] / _b[POmean:0.training] * 100)

* 9. Visualization
coefplot atet_ra atet_ipw atet_aipw, ///
    keep(ATET:*) xline(0) ///
    title("Effect of Job Training on Wages (ATET)")
graph export "training_effect.png", replace
```

### Example 2: Policy Analysis (ATE)

```stata
webuse cattaneo2, clear

* Estimate ATE using multiple methods
teffects aipw (bweight mbsmoke mmarried c.mage##c.mage fbaby i.medu) ///
    (prenatal1 mbsmoke mmarried c.mage##c.mage fbaby i.medu, probit), ///
    ate vce(robust)
estimates store ate_aipw

teffects ra (bweight mbsmoke mmarried c.mage##c.mage fbaby i.medu) ///
    (prenatal1), ate
estimates store ate_ra

teffects ipw (bweight) ///
    (prenatal1 mbsmoke mmarried c.mage##c.mage fbaby i.medu, probit), ate
estimates store ate_ipw

teffects psmatch (bweight) ///
    (prenatal1 mbsmoke mmarried mage fbaby i.medu), ate nn(3)
estimates store ate_psm

* Compare
estimates table ate_ra ate_ipw ate_aipw ate_psm, ///
    star stats(N) b(%7.1f) se(%7.1f)

* Diagnostics and balance
tebalance summarize
tebalance density mage

* Effect as percentage
teffects aipw (bweight mbsmoke mmarried c.mage##c.mage fbaby i.medu) ///
    (prenatal1 mbsmoke mmarried c.mage##c.mage fbaby i.medu, probit), ///
    ate pomeans
nlcom (pct: _b[ATE:r1vs0.prenatal1] / _b[POmean:0.prenatal1] * 100)

* Publication table
esttab ate_ra ate_ipw ate_aipw ate_psm using "prenatal_effects.rtf", ///
    se star(* 0.10 ** 0.05 *** 0.01) label replace ///
    title("Effect of Prenatal Care on Birthweight (grams)") ///
    mtitles("RA" "IPW" "AIPW" "PSM")
```

### Example 3: Multiple Treatments (Pairwise)

```stata
sysuse nlsw88, clear
generate training_type = 0 if industry < 4
replace training_type = 1 if industry >= 4 & industry <= 7
replace training_type = 2 if industry > 7 & !missing(industry)
label define ttype 0 "No training" 1 "Technical" 2 "Professional"
label values training_type ttype

* Pairwise comparisons (create binary treatment for each pair)
generate tech_vs_none = (training_type == 1) if inlist(training_type, 0, 1)
teffects aipw (wage age grade hours tenure) ///
    (tech_vs_none age grade hours tenure) ///
    if inlist(training_type, 0, 1), ate
estimates store tech_vs_none

generate prof_vs_none = (training_type == 2) if inlist(training_type, 0, 2)
teffects aipw (wage age grade hours tenure) ///
    (prof_vs_none age grade hours tenure) ///
    if inlist(training_type, 0, 2), ate
estimates store prof_vs_none

estimates table tech_vs_none prof_vs_none, star stats(N)
```

### Example 4: Continuous Treatment (Discretize)

```stata
* teffects does not handle continuous treatments natively
* Discretize into bins and estimate for each dose level
generate hours_cat = 0 if training_hours == 0
replace hours_cat = 1 if training_hours > 0 & training_hours <= 10
replace hours_cat = 2 if training_hours > 10 & training_hours <= 20
replace hours_cat = 3 if training_hours > 20 & !missing(training_hours)

forvalues i = 1/3 {
    generate treat_`i' = (hours_cat == `i') if inlist(hours_cat, 0, `i')
    quietly teffects aipw (wage age education) ///
        (treat_`i' age education) ///
        if inlist(hours_cat, 0, `i'), ate
    matrix b = e(b)
    matrix V = e(V)
    local ate`i' = b[1,1]
    local se`i' = sqrt(V[1,1])
    display "Effect of `i'×10 hours: " `ate`i'' " (SE: " `se`i'' ")"
}
```

---

## Quick Reference Tables

### When to Use Each Estimator

| Situation | Recommended | Reason |
|-----------|-------------|--------|
| Confident in outcome model | `ra` | Efficient, straightforward |
| Confident in treatment model | `ipw` or `psmatch` | Uses only treatment model |
| Uncertain about specifications | `aipw` or `ipwra` | Doubly robust |
| Limited overlap | `psmatch` with caliper | Restricts to comparable units |
| Small sample | `psmatch` or `nnmatch` | Non-parametric |
| Large sample with good overlap | `aipw` | Most efficient |

### Balance Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Standardized difference | < 0.1 | < 0.25 | > 0.25 |
| Variance ratio | 0.8 - 1.25 | 0.5 - 2.0 | < 0.5 or > 2.0 |

### Key Commands Summary

```stata
* Estimation
teffects ra (outcome covars) (treatment), ate
teffects ipw (outcome) (treatment covars), ate
teffects aipw (outcome covars) (treatment covars), ate
teffects psmatch (outcome) (treatment covars), ate nn(#)

* Diagnostics
tebalance summarize              // Covariate balance
tebalance density varname        // Density plots
tebalance box varname           // Box plots
teffects overlap                // Propensity score overlap

* Post-estimation
predict pscore, ps              // Propensity scores
predict te, te                  // Individual treatment effects
estat summarize                 // Summary of estimation sample
```

### Common Options

| Option | Purpose |
|--------|---------|
| `ate` | Estimate average treatment effect |
| `atet` | Estimate average treatment effect on treated |
| `pomeans` | Display potential outcome means |
| `vce(robust)` | Robust standard errors |
| `vce(cluster id)` | Clustered standard errors |
| `vce(bootstrap)` | Bootstrap standard errors |
| `nn(#)` | Number of neighbors for matching |
| `caliper(#)` | Maximum distance for matches |
| `generate(newvar)` | Save propensity scores |

---

## Best Practices

1. **Start with AIPW** for double robustness
2. **Compare with RA and IPW** to check sensitivity
3. **Examine balance** with `tebalance` commands
4. **Check overlap** with `teffects overlap`
5. **Consider matching** if overlap is poor
6. **Report multiple methods** to show robustness

### Covariate Selection

**Include:** covariates that predict treatment assignment, predict the outcome, and are pre-treatment.

**Do NOT include:** post-treatment variables (mediators, colliders), instrumental variables, or perfect predictors of treatment.

### Common Pitfalls

1. **Extrapolation** - Poor overlap leads to model dependence
2. **Wrong functional form** - Check non-linearities
3. **Ignoring balance** - Always check post-estimation balance
4. **Confusing ATE and ATET** - Choose based on research question
5. **Over-controlling** - Don't include post-treatment variables
