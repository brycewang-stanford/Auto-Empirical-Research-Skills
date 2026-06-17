# Event Study Packages in Stata

## Contents

- [Core Packages Overview](#core-packages-overview)
- [Installation and Setup](#installation-and-setup)
- [eventdd: Dynamic Difference-in-Differences](#eventdd-dynamic-difference-in-differences)
- [eventstudyinteract: Sun & Abraham Estimator](#eventstudyinteract-sun--abraham-estimator)
- [Creating Event Study Plots](#creating-event-study-plots)
- [Pre-Trend Testing](#pre-trend-testing)
- [Binning Endpoints](#binning-endpoints)
- [Heterogeneous Treatment Effects](#heterogeneous-treatment-effects)
- [Standard Errors and Clustering](#standard-errors-and-clustering)
- [Integration with did_multiplegt](#integration-with-did_multiplegt)
- [Integration with csdid](#integration-with-csdid)
- [Comparison of Event Study Approaches](#comparison-of-event-study-approaches)
- [Publication-Quality Plots](#publication-quality-plots)
- [Complete Workflow Example](#complete-workflow-example)
- [Best Practices and Pitfalls](#best-practices-and-pitfalls)
- [References](#references)

---

## Core Packages Overview

| Package | Developer | Purpose |
|---------|-----------|---------|
| **eventdd** | Borusyak, Jaravel | Automated event study plots + dynamic treatment effects. Integrates with reghdfe. |
| **eventstudyinteract** | Sun, Abraham | Interaction-weighted estimator robust to heterogeneous effects with staggered adoption. Addresses TWFE bias. |
| **event_plot** | (supporting) | Flexible event study plotting from stored estimates |
| **did_multiplegt** | de Chaisemartin, D'Haultfoeuille | Heterogeneity-robust dynamic effects estimator |
| **csdid** | Callaway, Sant'Anna | Group-time ATTs with doubly-robust estimation |
| **did_imputation** | Borusyak, Jaravel, Spiess | Imputation-based event study |

---

## Installation and Setup

```stata
// Core packages
ssc install eventdd
ssc install eventstudyinteract
ssc install reghdfe
ssc install ftools
ssc install did_multiplegt
ssc install csdid
ssc install drdid
ssc install avar

// Plotting tools
ssc install coefplot
ssc install event_plot
ssc install grstyle
ssc install palettes

// Verify
which eventdd
which eventstudyinteract
which reghdfe
which event_plot
```

### Testing Installation

```stata
webuse nlswork, clear
xtset idcode year

set seed 12345
by idcode: gen treated = (runiform() < 0.3) if _n == 1
by idcode: replace treated = treated[1]
gen treat_year = 79 if treated == 1
by idcode: replace treat_year = treat_year[1]
gen post = (year >= treat_year) if !missing(treat_year)
replace post = 0 if missing(treat_year)

gen rel_time = year - treat_year
eventdd ln_wage tenure, timevar(rel_time) ci(rcap) ///
    baseline(-1) leads(3) lags(5) ///
    graph_op(title("Test Event Study"))
```

### Dependency Check

```stata
foreach pkg in reghdfe ftools coefplot event_plot {
    capture which `pkg'
    if _rc {
        display "Missing package: `pkg'"
        display "Install with: ssc install `pkg'"
    }
    else {
        display "`pkg' is installed"
    }
}
```

---

## eventdd: Dynamic Difference-in-Differences

### Syntax

```stata
eventdd depvar [indepvars], timevar(varname) [options]

// Key options:
// - baseline(#)     : Reference period (default: -1)
// - leads(#)        : Number of pre-treatment periods
// - lags(#)         : Number of post-treatment periods
// - ci(style)       : CI style (rcap, rarea, rline) or noci
// - method(method)  : Estimation method (ols, hdfe, fe)
// - cluster(varname): Cluster standard errors
// - keepbal(event)  : Keep balanced panel around event
// - inrange(# #)    : Limit event time range (implicitly bins outside)
```

### Basic Usage

```stata
// Create relative time variable: 0 at treatment, negative before, positive after
gen rel_time = year - treatment_year
replace rel_time = -999 if missing(treatment_year)  // Never treated

// Basic event study
eventdd outcome, timevar(rel_time) ///
    baseline(-1) leads(5) lags(5) ///
    ci(rcap) ///
    graph_op(title("Event Study: Policy Impact") ///
             xtitle("Years Since Policy") ytitle("Effect on Outcome"))
graph export "event_study_simple.png", replace
```

### With Controls and Fixed Effects

```stata
// Controls are partialled out
eventdd outcome control1 control2 control3, ///
    timevar(rel_time) baseline(-1) leads(5) lags(5) ci(rcap)

// Using reghdfe for high-dimensional fixed effects
eventdd outcome, timevar(rel_time) ///
    baseline(-1) leads(5) lags(5) ///
    method(hdfe, absorb(unit_id year)) ///
    cluster(unit_id) ci(rcap)
```

### Accessing Results

```stata
eventdd outcome control1 control2, timevar(rel_time) ///
    baseline(-1) leads(5) lags(5) ///
    method(hdfe, absorb(unit_id year)) cluster(unit_id)

// Coefficient naming convention
display "Effect at t=0: " _b[_eq2_lead_0]
display "Effect at t=1: " _b[_eq2_lag1]

// Test joint significance of post-treatment
test _eq2_lag1 _eq2_lag2 _eq2_lag3

// Test pre-trends (leads should be zero)
test _eq2_lead_5 _eq2_lead_4 _eq2_lead_3 _eq2_lead_2
```

### Bootstrap and Balanced Panels

```stata
// Bootstrap standard errors
eventdd outcome, timevar(rel_time) baseline(-1) leads(5) lags(5) ///
    method(hdfe, absorb(unit_id year)) ///
    vce(bootstrap, reps(500) cluster(unit_id))

// Wild cluster bootstrap (requires boottest)
eventdd outcome, timevar(rel_time) baseline(-1) leads(5) lags(5) ///
    method(hdfe, absorb(unit_id year)) cluster(unit_id)
boottest _eq2_lead_5, cluster(unit_id) boottype(wild) reps(999)

// Balanced panel: drops units without all periods [-5, 5]
eventdd outcome, timevar(rel_time) baseline(-1) leads(5) lags(5) ///
    keepbal(event) method(hdfe, absorb(unit_id year)) ci(rcap)
```

---

## eventstudyinteract: Sun & Abraham Estimator

**Why Sun & Abraham?** Standard TWFE event studies with staggered adoption use already-treated units as controls ("forbidden comparisons"), producing bias when treatment effects are heterogeneous. Sun & Abraham (2021) uses cohort-specific event time indicators and only clean comparison groups.

### Syntax

```stata
eventstudyinteract depvar treatment_dummies [controls], ///
    cohort(varname) control_cohort(varname) ///
    absorb(absvars) vce(vcetype)

// - treatment_dummies: Cohort x relative time interactions
// - cohort(): Treatment cohort variable
// - control_cohort(): Never-treated or last-treated cohort indicator
```

### Creating Treatment Dummies and Running

```stata
gen rel_time = year - treatment_year
replace rel_time = -999 if missing(treatment_year)

// Create cohort x relative time dummies
quietly: levelsof treatment_year if !missing(treatment_year), local(cohorts)
foreach g of local cohorts {
    forvalues k = -5/10 {
        if `k' != -1 {  // Skip baseline
            gen treat_`g'_`k' = (treatment_year == `g' & rel_time == `k')
        }
    }
}
gen never_treated = missing(treatment_year)

// Estimate
eventstudyinteract outcome treat_*, ///
    cohort(treatment_year) control_cohort(never_treated) ///
    absorb(unit_id year) vce(cluster unit_id)
estimates store sa_baseline
```

### Plotting Results

```stata
event_plot sa_baseline, ///
    default_look ///
    stub_lag(treat_#_) stub_lead(treat_#_) ///
    together ///
    graph_opt(xtitle("Periods to Treatment") ///
              ytitle("Average Treatment Effect") ///
              xlabel(-5(1)10) ///
              title("Event Study: Sun & Abraham (2021)"))
graph export "sun_abraham_event_study.png", replace
```

### Using Not-Yet-Treated as Control

```stata
quietly: summarize treatment_year
local last_cohort = r(max)
gen last_treated = (treatment_year == `last_cohort')

eventstudyinteract outcome treat_*, ///
    cohort(treatment_year) control_cohort(last_treated) ///
    absorb(unit_id year) vce(cluster unit_id)
estimates store sa_notyet
```

### Automating Dummy Creation for Many Cohorts

```stata
capture program drop create_sa_dummies
program define create_sa_dummies
    syntax, cohort_var(varname) time_var(varname) ///
            rel_time_var(varname) ///
            [min_lead(integer -5) max_lag(integer 10) baseline(integer -1)]

    quietly: levelsof `cohort_var' if !missing(`cohort_var'), local(cohorts)
    foreach g of local cohorts {
        forvalues k = `min_lead'/`max_lag' {
            if `k' != `baseline' {
                quietly: gen treat_`g'_`k' = ///
                    (`cohort_var' == `g' & `rel_time_var' == `k')
            }
        }
    }
    display "Created treatment dummies for cohorts: `cohorts'"
end

create_sa_dummies, cohort_var(treatment_year) ///
    time_var(year) rel_time_var(rel_time) ///
    min_lead(-5) max_lag(10) baseline(-1)
```

---

## Creating Event Study Plots

### Manual Event Study with coefplot

```stata
// Create event time dummies
forvalues k = 5(-1)2 {
    gen lead`k' = (rel_time == -`k')
}
gen lead1 = 0  // Baseline period
forvalues k = 0/10 {
    gen lag`k' = (rel_time == `k')
}

reghdfe outcome lead5-lead2 lag0-lag10 controls, ///
    absorb(unit_id year) vce(cluster unit_id)

coefplot, keep(lead* lag*) vertical ///
    yline(0, lcolor(black)) ///
    xline(5.5, lcolor(red) lpattern(dash)) ///
    coeflabels(lead5="-5" lead4="-4" lead3="-3" lead2="-2" ///
               lead1="-1" lag0="0" lag1="1" lag2="2" lag3="3" ///
               lag4="4" lag5="5" lag6="6" lag7="7" lag8="8" ///
               lag9="9" lag10="10") ///
    xtitle("Periods Relative to Treatment") ytitle("Treatment Effect") ///
    graphregion(color(white)) bgcolor(white)
```

### Using event_plot

```stata
reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster unit_id)
estimates store es_results

// Basic
event_plot es_results, ///
    stub_lag(lag#) stub_lead(lead#) ///
    plottype(scatter) ciplottype(rcap) together ///
    graph_opt(xtitle("Periods to Treatment") ytitle("Effect") xlabel(-5(1)10))

// Advanced customization
event_plot es_results, ///
    stub_lag(lag#) stub_lead(lead#) ///
    plottype(scatter) ciplottype(rarea) together ///
    graph_opt(xtitle("Years Since Policy", size(medium)) ///
              ytitle("Effect (pp)", size(medium)) ///
              xlabel(-5(1)10, labsize(small)) ///
              ylabel(, labsize(small) format(%4.2f)) ///
              graphregion(color(white)) legend(off)) ///
    ciopt(color(navy%30)) scatter_opt(mcolor(navy) msize(medium))
```

### Multiple Specifications on One Plot

```stata
reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster unit_id)
estimates store spec1

reghdfe outcome lead5-lead2 lag0-lag10 control1 control2, ///
    absorb(unit_id year) vce(cluster unit_id)
estimates store spec2

reghdfe outcome lead5-lead2 lag0-lag10 control1 control2, ///
    absorb(unit_id year unit_id#c.year) vce(cluster unit_id)
estimates store spec3

event_plot spec1 spec2 spec3, ///
    stub_lag(lag#) stub_lead(lead#) ///
    plottype(scatter) ciplottype(rcap) ///
    together perturb(-0.2(0.2)0.2) ///
    graph_opt(xtitle("Periods to Treatment") ytitle("Treatment Effect") ///
              legend(order(1 "No Controls" 3 "Controls" 5 "Controls + Trends") rows(1)))
```

---

## Pre-Trend Testing

### Formal Tests

```stata
reghdfe outcome lead10-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster unit_id)

// Joint F-test of all pre-treatment coefficients
test lead10 lead9 lead8 lead7 lead6 lead5 lead4 lead3 lead2
// p > 0.10: Cannot reject zero pre-trends (good)
// p < 0.05: Evidence of pre-trends (concern)

// Individual t-tests
foreach k of numlist 10(-1)2 {
    test lead`k' = 0
    display "Period -`k': p-value = " %5.4f r(p)
}
```

### Placebo Event Studies

```stata
preserve
keep if year < treatment_year | missing(treatment_year)

gen placebo_year = treatment_year - 3 if !missing(treatment_year)
gen placebo_rel_time = year - placebo_year
replace placebo_rel_time = -999 if missing(placebo_year)

forvalues k = 5(-1)2 {
    gen placebo_lead`k' = (placebo_rel_time == -`k')
}
forvalues k = 0/5 {
    gen placebo_lag`k' = (placebo_rel_time == `k')
}

reghdfe outcome placebo_lead5-placebo_lead2 placebo_lag0-placebo_lag5, ///
    absorb(unit_id year) vce(cluster unit_id)
test placebo_lag0 placebo_lag1 placebo_lag2 placebo_lag3 placebo_lag4 placebo_lag5
// Should find no significant effects if parallel trends holds
restore
```

### Pre-Trend-Robust Inference

```stata
// Rambachan & Roth (2023): honest confidence intervals
// accounting for potential pre-trend violations
// Check for packages: honestdid, pretrends
```

---

## Binning Endpoints

Binning groups distant event-time periods (where observations are sparse) into a single indicator. Standard practice in applied work -- reduces noise and improves precision near treatment.

### Basic Endpoint Binning

```stata
gen rel_time_binned = rel_time
replace rel_time_binned = -5 if rel_time < -5 & rel_time != -999
replace rel_time_binned = 10 if rel_time > 10

forvalues k = 5(-1)2 {
    gen lead`k' = (rel_time_binned == -`k')
}
forvalues k = 0/10 {
    gen lag`k' = (rel_time_binned == `k')
}

reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster unit_id)

// lead5 captures all periods <= -5; lag10 captures all periods >= 10
```

### With eventdd

```stata
eventdd outcome, timevar(rel_time) ///
    baseline(-1) leads(5) lags(10) ///
    method(hdfe, absorb(unit_id year)) cluster(unit_id) ///
    inrange(-5 10)  // Implicitly bins outside this range
```

### Choosing Bin Cutoffs

```stata
// Rule of thumb: Bin when sample size drops below threshold
preserve
keep if !missing(treatment_year)
collapse (count) n=outcome, by(rel_time)
list rel_time n, sep(0)
restore
// Bin where n drops substantially
```

### Labeling Binned Endpoints in Plots

```stata
event_plot binned_es, stub_lag(lag#) stub_lead(lead#) together ///
    graph_opt(xlabel(-5 "<==-5" -4 "-4" -3 "-3" -2 "-2" -1 "-1(ref)" ///
                     0 "0" 1 "1" 2 "2" 3 "3" 4 "4" 5 "5" ///
                     6 "6" 7 "7" 8 "8" 9 "9" 10 ">=10", labsize(small)) ///
              note("Endpoints binned at t<=-5 and t>=10"))
```

---

## Heterogeneous Treatment Effects

With staggered treatment adoption, TWFE can place negative weights on some treatment effects because already-treated units serve as controls. The bias direction is unpredictable.

### Diagnosing with Bacon Decomposition

```stata
bacondecomp outcome, ddetail

// Plot decomposition
bacondecomp outcome, stub(bd_)
scatter bd_estimate bd_weight, ///
    xlabel(0(0.1)0.5) ///
    title("Bacon Decomposition") ///
    xtitle("Weight") ytitle("2x2 DiD Estimate")
// If substantial weight on "treated vs. already-treated", use robust estimators
```

### Solution 1: Callaway & Sant'Anna (csdid)

```stata
csdid outcome controls, ///
    ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet

estat event, window(-5 10) estore(cs_event)
estat pretrend

event_plot cs_event, default_look ///
    stub_lag(Tp#) stub_lead(Tm#) together ///
    graph_opt(title("Callaway-Sant'Anna Event Study"))
```

### Solution 2: did_multiplegt

```stata
did_multiplegt outcome unit_id year treatment, ///
    robust_dynamic dynamic(10) placebo(5) ///
    breps(100) cluster(unit_id)
```

### Solution 3: Imputation (Borusyak, Jaravel, Spiess)

```stata
ssc install did_imputation

did_imputation outcome unit_id year treatment_year, ///
    horizons(0/10) pretrend(5) autosample minn(0)

event_plot, default_look ///
    graph_opt(title("Imputation-Based Event Study"))
```

### Stacked Regression Approach

```stata
// Stack separate datasets for each cohort to avoid forbidden comparisons
local cohorts "2010 2012 2015"
tempfile stacked
local first = 1

foreach cohort of local cohorts {
    use original_data, clear
    keep if treatment_year == `cohort' | missing(treatment_year)
    gen cohort = `cohort'
    gen cohort_unit_id = unit_id * 10000 + `cohort'
    gen rel_time_cohort = year - `cohort'

    if `first' {
        save `stacked', replace
        local first = 0
    }
    else {
        append using `stacked'
        save `stacked', replace
    }
}

use `stacked', clear
forvalues k = 5(-1)2 {
    gen lead`k' = (rel_time_cohort == -`k')
}
forvalues k = 0/10 {
    gen lag`k' = (rel_time_cohort == `k')
}

// Cohort-specific fixed effects avoid forbidden comparisons
reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(cohort_unit_id cohort#year) vce(cluster unit_id)
```

---

## Standard Errors and Clustering

**Rule: Cluster at the level of treatment assignment.** Failure to cluster leads to understated SEs and over-rejection.

### Single and Multi-Way Clustering

```stata
// Cluster by unit (most common)
reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster unit_id)

// Cluster at treatment assignment level (e.g., state policy)
reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster state_id)

// Two-way clustering (unit AND time)
reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster state_id year)

// Three-way clustering
reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) vce(cluster unit_id year industry_id)
```

### Wild Cluster Bootstrap (for Few Clusters)

```stata
ssc install boottest

reghdfe outcome lead5-lead2 lag0-lag10, ///
    absorb(unit_id year) cluster(state_id)

// Use when number of clusters < 30
boottest lag0, cluster(state_id) boottype(wild) reps(999)
boottest lag1, cluster(state_id) boottype(wild) reps(999)
```

### Spatial Correlation

```stata
ssc install ols_spatial_HAC

ols_spatial_HAC outcome lead5-lead2 lag0-lag10 i.unit_id i.year, ///
    lat(latitude) lon(longitude) time(year) ///
    distcutoff(500) lagcutoff(5)
```

### Exporting Results

```stata
ssc install estout

esttab main_spec using "event_study_results.tex", ///
    keep(lead5 lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4 lag5) ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label replace booktabs ///
    title("Event Study Results") ///
    addnote("Standard errors clustered at state level in parentheses.")
```

---

## Integration with did_multiplegt

### Basic Usage

```stata
// Treatment must be binary (0/1)
gen treated_binary = (year >= treatment_year) if !missing(treatment_year)
replace treated_binary = 0 if missing(treatment_year)

did_multiplegt outcome unit_id year treated_binary, ///
    robust_dynamic dynamic(10) placebo(5) ///
    breps(100) cluster(unit_id)

// Results: Placebo_5..Placebo_1 (pre), Effect (t=0), Dynamic_1..Dynamic_10 (post)
```

### Extracting and Plotting Results

```stata
preserve
clear
matrix effects = e(effect)
matrix se = e(se)
matrix lb = e(lower_bound)
matrix ub = e(upper_bound)

svmat effects
svmat lb
svmat ub
gen period = _n - 6  // Adjust for 5 placebos + 1 baseline
rename effects1 estimate
rename lb1 ci_lower
rename ub1 ci_upper

twoway (scatter estimate period, mcolor(navy)) ///
       (rcap ci_lower ci_upper period, lcolor(navy)), ///
       xline(-0.5, lcolor(red) lpattern(dash)) yline(0) ///
       xlabel(-5(1)10) xtitle("Periods Since Treatment") ///
       ytitle("Treatment Effect") legend(off)
restore
```

### Pre-Trend Test

```stata
did_multiplegt outcome unit_id year treated_binary, ///
    robust_dynamic dynamic(5) placebo(5) ///
    breps(100) cluster(unit_id) jointtestplacebo

display "Joint placebo test p-value: " e(p_jointplacebo)
// p > 0.10: Cannot reject parallel trends
```

---

## Integration with csdid

### Basic Usage

```stata
// gvar = year when first treated; missing for never-treated
csdid outcome, ///
    ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet

// Options:
// - method(): dripw (doubly-robust, recommended), drimp, reg, ipw
// - notyet: not-yet-treated as control; long2: never-treated only
// - anticipation(#): allow effects # periods before gvar
// - balanced: require units observed in all periods
```

### Aggregations

```stata
// Event study
estat event, window(-5 10) estore(cs_event)

// Overall ATT
estat simple

// By treatment cohort
estat group

// By calendar time
estat calendar

// Pre-trend test
estat pretrend
// Reports chi-squared stat and p-value
```

### Plotting

```stata
event_plot cs_event, default_look ///
    stub_lag(Tp#) stub_lead(Tm#) together ///
    graph_opt(xtitle("Periods to Treatment") ///
              ytitle("Average Treatment Effect") ///
              xlabel(-5(1)10) title("Callaway & Sant'Anna"))
```

### Comparing Control Groups

```stata
// Never-treated
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) long2
estat event, window(-5 10) estore(cs_never)

// Not-yet-treated
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet
estat event, window(-5 10) estore(cs_notyet)

event_plot cs_never cs_notyet, ///
    stub_lag(Tp#) stub_lead(Tm#) ///
    together perturb(-0.15 0.15) ///
    graph_opt(legend(order(1 "Never-Treated" 3 "Not-Yet-Treated") rows(1)))
```

---

## Comparison of Event Study Approaches

| Method | Package | Best For | Limitations |
|--------|---------|----------|-------------|
| **TWFE** | reghdfe | Single treatment timing, homogeneous effects | Biased with staggered + heterogeneity |
| **Sun & Abraham** | eventstudyinteract | Staggered, cohort heterogeneity | Manual dummy creation |
| **Callaway & Sant'Anna** | csdid | Staggered, flexible aggregation | Computational intensity |
| **did_multiplegt** | did_multiplegt | Staggered, simple syntax | Binary treatment required |
| **Imputation** | did_imputation | Staggered, many periods | Newer, less tested |

### Plotting All Methods Together

```stata
event_plot twfe sun_abraham callaway_santanna imputation, ///
    stub_lag(lag# treat_#_# Tp# tau#) ///
    stub_lead(lead# treat_#_# Tm# pre#) ///
    plottype(scatter) ciplottype(rcap) ///
    together perturb(-0.35(0.175)0.35) ///
    graph_opt(xtitle("Periods to Treatment") ytitle("Treatment Effect") ///
              legend(order(1 "TWFE" 3 "Sun-Abraham" ///
                          5 "Callaway-Sant'Anna" 7 "Imputation") rows(2)))
```

### When to Use Each Method

- **Not staggered**: Standard TWFE (simplest)
- **Staggered**: Check Bacon decomposition for negative weights. If problematic, use CS, SA, or did_multiplegt and compare results across methods
- **Few clusters (<30)**: Add wild cluster bootstrap

---

## Publication-Quality Plots

### Setup

```stata
ssc install grstyle
ssc install palettes
ssc install colrspace

grstyle init
grstyle set plain, horizontal grid dotted
grstyle set color economist
grstyle set legend 6, nobox
```

### Publication-Quality Event Study

```stata
event_plot pub_es, stub_lag(lag#) stub_lead(lead#) ///
    plottype(scatter) ciplottype(rcap) together ///
    graph_opt(xtitle("Years Relative to Policy", size(medlarge)) ///
              ytitle("Effect (Percentage Points)", size(medlarge)) ///
              xlabel(-5(1)10, labsize(medsmall)) ///
              ylabel(, labsize(medsmall) format(%4.2f) angle(0)) ///
              xline(-0.5, lcolor(cranberry) lpattern(dash) lwidth(medium)) ///
              yline(0, lcolor(black) lwidth(thin)) ///
              graphregion(color(white) margin(medium)) ///
              plotregion(margin(small)) bgcolor(white) ///
              title("") legend(off)) ///
    scatter_opt(mcolor(navy) msize(large) msymbol(circle)) ///
    rcap_opt(lcolor(navy) lwidth(medthick))

graph export "event_study_publication.png", replace width(3000)
graph export "event_study_publication.eps", replace
```

### CI Style Options

```stata
// Range caps (traditional)
ciplottype(rcap)

// Shaded area (modern)
ciplottype(rarea) ... ciopt(color(navy%20))

// Connected line with area
plottype(line) ciplottype(rarea) ... line_opt(lcolor(navy) lwidth(medthick)) ciopt(color(navy%15))

// Spike plot
plottype(spike) ciplottype(rcap) ... spike_opt(lcolor(navy) lwidth(thick))
```

### Exporting Formats

```stata
graph export "fig.png", replace width(3000)   // Web/Word
graph export "fig.eps", replace                // LaTeX
graph export "fig.pdf", replace                // LaTeX alt
graph export "fig.tif", replace width(3000)    // Print journals
graph save "fig.gph", replace                  // Stata editable

// Export underlying data
parmest, saving("event_study_data.dta", replace)
```

---

## Complete Workflow Example

```stata
/*==============================================================================
Event Study: State Minimum Wage -> Teen Employment
==============================================================================*/
clear all
set more off

// Step 1: Data prep
use "state_employment.dta", clear
gen treatment_year = .
replace treatment_year = 2010 if inlist(state, "CA", "NY")
replace treatment_year = 2012 if inlist(state, "MA", "WA")
replace treatment_year = 2015 if inlist(state, "OR", "VT")

gen rel_time = year - treatment_year
replace rel_time = -999 if missing(treatment_year)
encode state, gen(state_id)
xtset state_id year

// Step 2: Check sample sizes
preserve
keep if !missing(treatment_year)
collapse (count) n=teen_employment, by(rel_time)
list if inrange(rel_time, -10, 10), sep(0)
restore

// Step 3: TWFE event study (bin at -8/+8)
gen rel_time_binned = rel_time
replace rel_time_binned = -8 if rel_time < -8 & rel_time != -999
replace rel_time_binned = 8 if rel_time > 8

forvalues k = 8(-1)2 {
    gen lead`k' = (rel_time_binned == -`k')
}
forvalues k = 0/8 {
    gen lag`k' = (rel_time_binned == `k')
}

reghdfe teen_employment lead8-lead2 lag0-lag8 ///
    gdp_growth population_growth, ///
    absorb(state_id year) vce(cluster state_id)
estimates store twfe

test lead8 lead7 lead6 lead5 lead4 lead3 lead2
local p_pretrend_twfe = r(p)

// Step 4: Bacon decomposition
bacondecomp teen_employment, ddetail

// Step 5: Callaway & Sant'Anna
csdid teen_employment gdp_growth population_growth, ///
    ivar(state_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet
estat simple
estat event, window(-8 8) estore(cs_event)
estat pretrend

// Step 6: Sun & Abraham
quietly: levelsof treatment_year if !missing(treatment_year), local(cohorts)
foreach g of local cohorts {
    forvalues k = -8/8 {
        if `k' != -1 {
            gen treat_`g'_`k' = (treatment_year == `g' & rel_time_binned == `k')
        }
    }
}
gen never_treated = missing(treatment_year)

eventstudyinteract teen_employment treat_* gdp_growth population_growth, ///
    cohort(treatment_year) control_cohort(never_treated) ///
    absorb(state_id year) vce(cluster state_id)
estimates store sa

// Step 7: Compare methods
event_plot twfe cs_event sa, ///
    stub_lag(lag# Tp# treat_#_) stub_lead(lead# Tm# treat_#_) ///
    plottype(scatter) ciplottype(rcap) ///
    together perturb(-0.25(0.25)0.25) ///
    graph_opt(xtitle("Years to Minimum Wage Increase") ///
              ytitle("Effect on Teen Employment (pp)") xlabel(-8(2)8) ///
              legend(order(1 "TWFE" 3 "CS" 5 "Sun-Abraham") rows(1)))
graph export "minwage_method_comparison.png", replace width(3500)

// Step 8: Robustness - placebo outcome
reghdfe adult_employment lead8-lead2 lag0-lag8 ///
    gdp_growth population_growth, ///
    absorb(state_id year) vce(cluster state_id)

// Step 9: Export
esttab twfe cs_event sa using "minwage_results.tex", ///
    keep(lag0 lag1 lag2 lag3 lag4 lag5) ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label replace booktabs ///
    mtitles("TWFE" "CS" "Sun-Abraham")
```

---

## Best Practices and Pitfalls

### Common Pitfalls

```stata
// WRONG: Skip pre-trend testing
reghdfe outcome lag0-lag10, absorb(unit_id year)
// RIGHT: Always include leads and test
reghdfe outcome lead5-lead2 lag0-lag10, absorb(unit_id year)
test lead5 lead4 lead3 lead2

// WRONG: TWFE with staggered adoption (potentially biased)
gen post = (year >= treatment_year)
reghdfe outcome post, absorb(unit_id year)
// RIGHT: Use heterogeneity-robust estimators
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year)

// WRONG: No clustering
reghdfe outcome lead5-lead2 lag0-lag10, absorb(unit_id year)
// RIGHT: Cluster at treatment assignment level
reghdfe outcome lead5-lead2 lag0-lag10, absorb(unit_id year) vce(cluster state_id)

// WRONG: Include all periods including baseline (collinearity)
forvalues k = 5(-1)1 {
    gen lead`k' = (rel_time == -`k')
}
// RIGHT: Omit one period as baseline (usually -1)
forvalues k = 5(-1)2 {
    gen lead`k' = (rel_time == -`k')
}

// WRONG: Pure event-time dummies with uniform treatment timing
// When all treated units share the same treatment_year, these are
// perfectly collinear with year FEs — coefficients are dropped or wrong.
gen lead5 = (rel_time == -5)   // collinear with year FE
gen lead4 = (rel_time == -4)   // collinear with year FE
reghdfe outcome lead5 lead4 lead3 lead2 lag0 lag1, absorb(unit_id year)
// RIGHT: Interact event-time with treatment group indicator
gen treated = !missing(treatment_year)
reghdfe outcome ib(-1).rel_time#1.treated, ///
    absorb(unit_id year) vce(cluster unit_id)
// This only matters for uniform timing; staggered designs break the
// collinearity because rel_time maps to different calendar years per cohort.
```

### Quick Reference: Package Syntax

```stata
// eventdd
eventdd outcome [controls], timevar(rel_time) ///
    baseline(-1) leads(#) lags(#) ///
    method(hdfe, absorb(fe1 fe2)) cluster(clustervar)

// eventstudyinteract
eventstudyinteract outcome treat_* [controls], ///
    cohort(treatment_year) control_cohort(never_treated) ///
    absorb(fe1 fe2) vce(cluster clustervar)

// csdid
csdid outcome [controls], ///
    ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet
estat event, window(-5 10) estore(results)

// did_multiplegt
did_multiplegt outcome unit_id year treatment, ///
    robust_dynamic dynamic(#) placebo(#) ///
    breps(100) cluster(clustervar)

// event_plot
event_plot results, ///
    stub_lag(lag#) stub_lead(lead#) ///
    plottype(scatter) ciplottype(rcap) together ///
    graph_opt(options)
```

---

## References

- Borusyak, Jaravel, & Spiess (2021). "Revisiting Event Study Designs"
- Callaway & Sant'Anna (2021). "DiD with Multiple Time Periods"
- de Chaisemartin & D'Haultfoeuille (2020). "TWFE with Heterogeneous Treatment Effects"
- Goodman-Bacon (2021). "DiD with Variation in Treatment Timing"
- Rambachan & Roth (2023). "A More Credible Approach to Parallel Trends"
- Sun & Abraham (2021). "Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects"
- DiD resources: https://asjadnaqvi.github.io/DiD/
