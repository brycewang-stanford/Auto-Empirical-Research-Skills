# Modern Difference-in-Differences Packages in Stata

## Introduction

Traditional two-way fixed effects (TWFE) regression can produce biased estimates under staggered treatment adoption with heterogeneous effects. TWFE uses already-treated units as controls for newly-treated units ("forbidden comparisons"), creating negative weights.

**Modern packages solve this by:**
- Using only valid comparisons (never-treated or not-yet-treated as controls)
- Explicitly modeling treatment effect heterogeneity
- Providing transparent aggregation schemes

**Packages covered:**
- **csdid**: Callaway-Sant'Anna group-time ATTs with flexible aggregation
- **did_multiplegt**: de Chaisemartin-D'Haultfoeuille with built-in placebos and dynamics
- **did_imputation**: Borusyak-Jaravel-Spiess imputation-based estimator (most efficient)
- **didregress**: Stata 18 built-in (AIPW, IPW, RA, TWFE)
- **eventstudyinteract**: Sun-Abraham interaction-weighted estimator
- **stackedev**: Stacked event study approach

### Installation

```stata
* Core packages
ssc install csdid
ssc install drdid
ssc install did_multiplegt
ssc install did_imputation
ssc install eventstudyinteract
ssc install bacondecomp

* Supporting packages
ssc install reghdfe
ssc install ftools
ssc install avar
ssc install boottest
ssc install coefplot
ssc install event_plot
```

## Diagnosing the Problem: Goodman-Bacon Decomposition

```stata
ssc install bacondecomp

* Decompose TWFE into component 2x2 DiD comparisons
bacondecomp outcome, ddetail stub(bacon_)

* Visualize: look for negative weights and heterogeneous estimates
scatter bacon_estimate bacon_weight, ///
    yline(`twfe_coef', lcolor(red) lpattern(dash)) yline(0)
```

**When is TWFE valid?** Only when treatment effects are homogeneous across units and time, and there are no dynamic effects.

## Data Structure Requirements

All modern DiD packages need:

```stata
* Key variables:
* - unit_id: Panel identifier
* - year: Time period
* - treatment_year: Year unit FIRST receives treatment
*   (0 or missing for never-treated units)
* - outcome: Outcome variable

* Create binary treatment indicator
generate treated = (year >= treatment_year & treatment_year > 0)
```

---

## csdid: Callaway and Sant'Anna (2021)

Estimates group-time ATTs (ATT(g,t)) and aggregates them flexibly.

### Syntax

```stata
csdid outcome [covariates], ///
    ivar(unit_id) ///           // Panel identifier
    time(time_var) ///          // Time variable
    gvar(first_treat_var) ///   // First treatment period (0 or . for never-treated)
    [method(dripw|reg|ipw)] /// // Estimation method
    [notyet | long2]            // Control group choice
```

**Key options:**
- `method(dripw)`: Doubly-robust (default, most robust)
- `method(reg)`: Regression-based (faster)
- `method(ipw)`: Inverse probability weighting
- `notyet`: Use not-yet-treated as controls (default)
- `long2`: Use only never-treated as controls
- `wboot rseed(#)`: Wild bootstrap SEs
- `wboot_reps(#)`: Number of bootstrap reps

### Basic Usage

```stata
csdid wage_outcome age grade, ///
    ivar(idcode) time(year) gvar(treatment_year) ///
    method(dripw) notyet
```

### Aggregation (estat commands)

```stata
* Overall ATT
estat simple
matrix simple_att = r(table)
local att = simple_att[1,1]
local se = simple_att[2,1]

* By treatment cohort
estat group
csdid_plot, group

* By calendar time
estat calendar
csdid_plot, calendar

* Event study
estat event, window(-5 10) estore(cs_event)
csdid_plot, name(event_study, replace)

* Pre-trend test
estat pretrend, pre(5)
```

### Sensitivity to Control Group

```stata
* Compare not-yet-treated vs never-treated
csdid outcome, ivar(id) time(year) gvar(treat_year) method(dripw) notyet
estat simple
local att_notyet = r(table)[1,1]

csdid outcome, ivar(id) time(year) gvar(treat_year) method(dripw) long2
estat simple
local att_never = r(table)[1,1]

display "Not-yet: " `att_notyet' "  Never: " `att_never'
```

---

## did_multiplegt: de Chaisemartin and D'Haultfoeuille (2020)

Heterogeneity-robust estimator with built-in placebo tests and dynamic effects. Can handle treatment switchers.

### Syntax

```stata
did_multiplegt outcome unit_id time_var treatment_var, ///
    [robust_dynamic] ///        // Robust SEs with dynamic effects
    [dynamic(#)] ///            // Number of post-treatment periods
    [placebo(#)] ///            // Number of pre-treatment placebo periods
    [breps(#)] ///              // Bootstrap replications for SEs
    [cluster(varname)] ///      // Cluster variable
    [controls(varlist)] ///     // Time-varying controls
    [trends_nonparam(varname)] ///  // Unit-specific nonparametric trends
    [jointtestplacebo] ///      // Joint test of all placebos
    [only_never_switchers]      // Restrict to absorbing treatment
```

### Basic Usage

```stata
did_multiplegt price hospital_id year merged, ///
    robust_dynamic dynamic(5) placebo(3) breps(100) cluster(hospital_id)

* Results stored in e()
display "Instantaneous: " e(effect) " (" e(se_effect) ")"
forvalues k = 1/5 {
    display "Dynamic +`k': " e(dynamic_`k') " (" e(se_dynamic_`k') ")"
}
forvalues k = 1/3 {
    display "Placebo -`k': " e(placebo_`k') " (" e(se_placebo_`k') ")"
}
```

### Joint Placebo Test

```stata
did_multiplegt price hospital_id year merged, ///
    robust_dynamic dynamic(5) placebo(3) breps(200) ///
    cluster(hospital_id) jointtestplacebo

display "Joint placebo p-value: " e(p_jointplacebo)
```

### Plotting Dynamic Effects

```stata
* Extract results and build dataset manually
preserve
clear
local n_placebo = 3
local n_dynamic = 5
set obs `= `n_placebo' + 1 + `n_dynamic''
generate period = _n - `n_placebo' - 1
generate estimate = .
generate se = .

forvalues k = 1/`n_placebo' {
    local row = `n_placebo' - `k' + 1
    replace estimate = e(placebo_`k') in `row'
    replace se = e(se_placebo_`k') in `row'
}
local row = `n_placebo' + 1
replace estimate = e(effect) in `row'
replace se = e(se_effect) in `row'
forvalues k = 1/`n_dynamic' {
    local row = `n_placebo' + 1 + `k'
    replace estimate = e(dynamic_`k') in `row'
    replace se = e(se_dynamic_`k') in `row'
}

generate ci_lower = estimate - 1.96 * se
generate ci_upper = estimate + 1.96 * se

twoway (scatter estimate period) (rcap ci_lower ci_upper period), ///
    xline(-0.5, lcolor(red) lpattern(dash)) yline(0) ///
    xtitle("Periods Relative to Treatment") ytitle("Effect") legend(off)
restore
```

### Saving Results

```stata
did_multiplegt price hospital_id year merged, ///
    robust_dynamic dynamic(5) placebo(3) breps(100) ///
    cluster(hospital_id) save_results("did_multiplegt_output")
* Creates did_multiplegt_output.dta
```

---

## did_imputation: Borusyak, Jaravel, and Spiess (2021)

Imputation-based approach: imputes counterfactual outcomes for treated units using untreated observations. Most efficient estimator under homoskedasticity.

### Syntax

```stata
did_imputation outcome unit_id time_var first_treat_var, ///
    [horizons(numlist)] ///     // Event times (e.g., 0/10)
    [pretrend(#)] ///           // Pre-treatment periods to test
    [autosample] ///            // Automatically balance sample
    [minn(#)] ///               // Min obs per group-time
    [controls(varlist)] ///     // Control variables (partialled out)
    [cluster(varname)] ///      // Cluster SEs
    [agg(simple|event|cohort|time)] // Aggregation type
```

### Basic Usage

```stata
did_imputation employed idcode year first_treatment, autosample minn(0)
```

### Event Study

```stata
did_imputation employed idcode year first_treatment, ///
    horizons(0/10) pretrend(5) autosample cluster(idcode)

* Plot
event_plot, ///
    default_look stub_lag(tau#) stub_lead(pre#) together ///
    graph_opt(xtitle("Periods Since Treatment") ytitle("Effect") xlabel(-5(1)10))
```

### Pre-trend Testing

```stata
did_imputation employed idcode year first_treatment, ///
    horizons(0/10) pretrend(5) autosample cluster(idcode)

* Joint test of pre-treatment coefficients
test pre1 pre2 pre3 pre4 pre5
```

### Aggregation Types

```stata
* Cohort-specific effects
did_imputation employed idcode year first_treatment, horizons(0/5) agg(cohort) autosample

* Calendar-time effects
did_imputation employed idcode year first_treatment, horizons(0/5) agg(time) autosample
```

---

## didregress: Stata 18 Built-in Command

Requires Stata 18+. Multiple estimators in one command.

### Syntax

```stata
didregress (outcome [covariates]) (treatment_var [covariates]), ///
    group(unit_id) time(time_var) ///
    [aipw | ipw | ra | twfe] ///
    [vce(cluster varname)]
```

- Covariates in outcome equation: for RA and AIPW
- Covariates in treatment equation: for IPW and AIPW

### Usage

```stata
* AIPW (default, doubly robust)
didregress (outcome gdp_growth) (treated gdp_growth), ///
    group(state) time(year) aipw vce(cluster state)

* Post-estimation aggregations
estat aggregation, event window(-5 10)
estat aggregation, cohort
estat aggregation, time
estat grlevelsof
```

**Advantages:** Official support, multiple estimators, clean post-estimation.
**Limitations:** Stata 18 only, fewer diagnostics than specialized packages, no built-in event study plots.

---

## eventstudyinteract: Sun and Abraham (2021)

Interaction-weighted estimator avoiding negative weights.

```stata
ssc install eventstudyinteract

* Create interaction terms for each cohort x relative-time
levelsof treatment_year if treatment_year > 0, local(cohorts)
foreach g of local cohorts {
    forvalues k = -5/10 {
        if `k' != -1 {
            generate treat_`g'_`k' = (treatment_year == `g' & rel_time == `k')
        }
    }
}

eventstudyinteract outcome treat_*, ///
    absorb(unit_id year) ///
    cohort(treatment_year) ///
    control_cohort(never_treated) ///
    vce(cluster unit_id)

event_plot, default_look ///
    graph_opt(xtitle("Event Time") ytitle("Effect"))
```

---

## Stacked Event Study (Manual)

Stack separate datasets per cohort, each with its own never-treated control group.

```stata
levelsof treatment_year if !missing(treatment_year), local(cohorts)
tempfile stacked
local first = 1

foreach cohort of local cohorts {
    preserve
    keep if treatment_year == `cohort' | missing(treatment_year)
    generate stack_cohort = `cohort'
    generate stack_id = unit_id * 10000 + `cohort'
    generate stack_reltime = year - `cohort'

    if `first' {
        save `stacked', replace
        local first = 0
    }
    else {
        append using `stacked'
        save `stacked', replace
    }
    restore
}

use `stacked', clear

* Create event time dummies (omit -1)
forvalues k = 5(-1)1 {
    generate lead`k' = (stack_reltime == -`k')
}
forvalues k = 0/10 {
    generate lag`k' = (stack_reltime == `k')
}

reghdfe outcome lead* lag*, absorb(stack_id stack_cohort#year) cluster(unit_id)
```

---

## When to Use Each Package

| Scenario | Package | Why |
|----------|---------|-----|
| Single treatment period | Any / TWFE | All equivalent |
| Flexible aggregation needed | `csdid` | Group, calendar, event study aggregations |
| Built-in placebos + dynamics | `did_multiplegt` | Comprehensive diagnostics |
| Maximum efficiency | `did_imputation` | Lowest SEs under homoskedasticity |
| Official Stata 18 | `didregress` | Integrated post-estimation |
| Cohort-specific event studies | `eventstudyinteract` | Transparent weights |
| Teaching / transparency | Stacked event study | Easy to explain |

**Decision rule:** If staggered adoption, always use at least one robust method. Report TWFE alongside for comparison. If estimates diverge, heterogeneity is present and TWFE is biased.

---

## Event Study Setup

```stata
* Relative time variable
generate event_time = year - treatment_year
replace event_time = -1000 if missing(treatment_year) | treatment_year == 0

* Event time dummies (omit -1 as reference)
forvalues k = 10(-1)2 {
    generate lead`k' = (event_time == -`k')
}
forvalues k = 0/10 {
    generate lag`k' = (event_time == `k')
}
```

### Binning Distant Endpoints

```stata
generate event_time_binned = event_time
replace event_time_binned = -10 if event_time < -10 & event_time != -1000
replace event_time_binned = 10 if event_time > 10
```

### Testing Pre-Trends

```stata
* Joint test of all pre-treatment coefficients
test lead10 lead9 lead8 lead7 lead6 lead5 lead4 lead3 lead2

* Or after csdid:
estat pretrend, pre(5)
```

---

## Standard Errors and Clustering

**General rule:** Cluster at the level of treatment assignment or higher.

### By Package

```stata
* csdid: auto-clusters at ivar() level; wild bootstrap available
csdid outcome, ivar(id) time(year) gvar(g) wboot rseed(12345)

* did_multiplegt: explicit cluster + bootstrap reps
did_multiplegt outcome id year treat, breps(200) cluster(state_id)

* did_imputation: cluster option
did_imputation outcome id year g, autosample cluster(id)

* didregress: standard vce()
didregress (outcome) (treat), group(id) time(year) vce(cluster state_id)
```

### Few Clusters (< 30)

```stata
* Wild cluster bootstrap (install boottest)
ssc install boottest
reghdfe outcome treatment, absorb(unit_id year) cluster(state_id)
boottest treatment, cluster(state_id) boottype(wild) reps(9999) seed(12345)
```

### Two-Way Clustering

```stata
reghdfe outcome treatment, absorb(unit_id year) vce(cluster state_id year)
```

---

## Side-by-Side Comparison of All Estimators

```stata
* 1. TWFE
reghdfe outcome treated x1 x2, absorb(unit_id year) cluster(unit_id)
local est1 = _b[treated]

* 2. Callaway-Sant'Anna
csdid outcome x1 x2, ivar(unit_id) time(year) gvar(treatment_year) method(dripw) notyet
estat simple
local est2 = r(table)[1,1]

* 3. did_multiplegt
did_multiplegt outcome unit_id year treated, robust_dynamic breps(100) cluster(unit_id)
local est3 = e(effect)

* 4. did_imputation
did_imputation outcome unit_id year treatment_year, autosample cluster(unit_id)
local est4 = _b[tau]

* 5. didregress (Stata 18)
capture didregress (outcome x1 x2) (treated x1 x2), group(unit_id) time(year) aipw
capture local est5 = _b[ATET:r1vs0.treated]

* Compare
display "TWFE: " `est1'
display "CS:   " `est2'
display "DM:   " `est3'
display "DI:   " `est4'
```

---

## Complete Workflow Template (csdid)

```stata
clear all
set seed 98765

use "your_data.dta", clear

* 1. TWFE baseline
reghdfe outcome treated covars, absorb(unit_id year) vce(cluster unit_id)
local twfe = _b[treated]

* 2. Bacon decomposition
bacondecomp outcome, ddetail

* 3. Main estimation
csdid outcome covars, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet

* 4. Aggregations
estat simple                              // Overall ATT
estat group                               // By cohort
estat event, window(-5 10) estore(es)     // Event study
estat pretrend, pre(5)                    // Pre-trend test

* 5. Plots
csdid_plot, name(event_study, replace)

* 6. Robustness: never-treated controls
csdid outcome covars, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) long2
estat simple

* 7. Robustness: alternative methods
csdid outcome covars, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(reg) notyet
estat simple

csdid outcome covars, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(ipw) notyet
estat simple
```

## Pre-Publication Checklist

- [ ] Test parallel trends (visual + formal `estat pretrend`)
- [ ] Show event study plot
- [ ] Report Goodman-Bacon decomposition (if staggered)
- [ ] Use at least one heterogeneity-robust estimator
- [ ] Report treatment effect dynamics
- [ ] Cluster standard errors at treatment level
- [ ] Check robustness to control group choice (not-yet vs never)
- [ ] Report number of treated/control units and cohort sizes
