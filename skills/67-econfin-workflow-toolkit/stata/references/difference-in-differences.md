# Difference-in-Differences Analysis in Stata

## Table of Contents
1. [Core Concepts and Assumptions](#core-concepts-and-assumptions)
2. [Basic Two-Period DiD](#basic-two-period-did)
3. [Two-Way Fixed Effects (TWFE) Estimation](#two-way-fixed-effects-twfe-estimation)
4. [Event Study Designs](#event-study-designs)
5. [Testing and Visualizing Parallel Trends](#testing-and-visualizing-parallel-trends)
6. [Staggered Treatment Adoption](#staggered-treatment-adoption)
7. [Heterogeneous Treatment Effects](#heterogeneous-treatment-effects)
8. [Synthetic Control Methods](#synthetic-control-methods)
9. [Triple Differences](#triple-differences)
10. [Standard Errors and Clustering](#standard-errors-and-clustering)
11. [Recent Advances and Pitfalls](#recent-advances-and-pitfalls)
12. [Complete Workflow Examples](#complete-workflow-examples)

---

## Core Concepts and Assumptions

### Key Assumptions

#### 1. Parallel Trends (Critical)
In the absence of treatment, treated and control groups would have followed parallel trends. Cannot be directly tested but can be assessed with pre-treatment data.

```stata
* Visual inspection of pre-treatment trends
preserve
keep if year < treatment_year
collapse (mean) outcome, by(treated year)
twoway (line outcome year if treated == 0) ///
       (line outcome year if treated == 1), ///
       legend(label(1 "Control") label(2 "Treated"))
restore

* Formal test with leads
regress outcome i.treated##ib(last).pre_period_year i.year, cluster(state)
test 1.treated#1.pre_period_year 1.treated#2.pre_period_year
```

#### 2. No Anticipation
Treatment does not affect outcomes before implementation. Violations: firms adjusting in anticipation, migration before implementation.

#### 3. Common Shocks
Time-varying shocks affect treated and control groups similarly.

```stata
* Check for differential time trends
regress outcome i.treated##c.year i.year, cluster(state)
test 1.treated#c.year  // Should be insignificant
```

---

## Basic Two-Period DiD

### Regression-Based DiD

```stata
* Standard DiD regression
regress wage_outcome i.treated##i.post

* With controls
regress wage_outcome i.treated##i.post age education, robust

* Interpretation:
* - treated: baseline difference between groups
* - post: time trend for control group
* - treated#post: DiD estimate (treatment effect)
```

### Manual DiD Calculation

```stata
quietly: summarize wage_outcome if treated == 1 & post == 1
local y11 = r(mean)
quietly: summarize wage_outcome if treated == 1 & post == 0
local y10 = r(mean)
quietly: summarize wage_outcome if treated == 0 & post == 1
local y01 = r(mean)
quietly: summarize wage_outcome if treated == 0 & post == 0
local y00 = r(mean)

display "DiD Estimate: " (`y11' - `y10') - (`y01' - `y00')
```

---

## Two-Way Fixed Effects (TWFE) Estimation

TWFE extends DiD to multiple periods and/or multiple treatment groups.

### Panel Data Setup

```stata
xtset unit_id year

* TWFE regression with xtreg
xtreg outcome post_treatment, fe vce(cluster unit_id)

* Equivalent using reghdfe (faster for large datasets)
ssc install reghdfe
reghdfe outcome post_treatment, absorb(unit_id year) vce(cluster unit_id)

* With time-varying controls
reghdfe outcome post_treatment x1 x2, ///
    absorb(unit_id year) vce(cluster unit_id)
```

### Unit-Specific and Group-Specific Time Trends

```stata
* Linear unit-specific trends
reghdfe outcome post_treatment, ///
    absorb(unit_id year unit_id#c.year) vce(cluster unit_id)

* Group-specific time trends
reghdfe outcome post_treatment, ///
    absorb(unit_id year group#c.year) vce(cluster unit_id)
```

---

## Event Study Designs

### Basic Event Study

```stata
* Create relative time variable
generate rel_time = year - treatment_year
replace rel_time = -999 if missing(treatment_year)  // Never treated

* Create event time dummies (omit -1 as base period)
* GOTCHA: Variable names cannot contain hyphens, so never embed a negative
* `k' directly in a name (e.g., lead_lag_-5 is illegal). Use lead/lag prefixes.
forvalues k = 5(-1)2 {
    generate lead`k' = (rel_time == -`k')
}
forvalues k = 0/5 {
    generate lag`k' = (rel_time == `k')
}

* Event study regression
reghdfe outcome lead* lag*, absorb(unit_id year) vce(cluster unit_id)

* Plot event study coefficients
preserve
parmest, saving(event_study.dta, replace)
use event_study.dta, clear
keep if regexm(parm, "^(lead|lag)")
generate event_time = real(regexr(parm, "lead", "-"))
replace event_time = real(regexr(parm, "lag", "")) if missing(event_time)
sort event_time
twoway (scatter estimate event_time) ///
       (rcap min95 max95 event_time), ///
       xline(-0.5, lcolor(red) lpattern(dash)) ///
       yline(0, lcolor(black)) ///
       xlabel(-5(1)5) ///
       xtitle("Periods Relative to Treatment") ///
       ytitle("Treatment Effect") legend(off)
restore
```

### Event Study with Uniform Treatment Timing

When all treated units receive treatment at the same time (no staggered adoption), pure event-time dummies like `gen lead5 = (rel_time == -5)` are **collinear with year fixed effects** because every treated unit has the same mapping from calendar year to relative time. The regression will either drop coefficients or produce meaningless estimates.

The fix is to interact event-time indicators with a treatment group indicator. This gives variation within each calendar year (treated vs. control) that year FEs do not absorb.

```stata
* ----- WRONG: pure event-time dummies with uniform timing -----
* These are perfectly collinear with year FEs when all treated units
* share the same treatment_year (e.g., treatment_year == 2010 for all).
gen lead5 = (rel_time == -5)
gen lead4 = (rel_time == -4)
* ...
reghdfe outcome lead5 lead4 lead3 lead2 lag0 lag1 lag2, ///
    absorb(unit_id year) vce(cluster unit_id)
* Result: coefficients dropped or estimates are nonsensical

* ----- RIGHT: interact event-time with treatment group -----
* Option A: Manual interaction dummies
gen treated = !missing(treatment_year)
forvalues k = 5(-1)2 {
    gen lead`k' = treated * (rel_time == -`k')
}
forvalues k = 0/5 {
    gen lag`k' = treated * (rel_time == `k')
}
reghdfe outcome lead5-lead2 lag0-lag5, ///
    absorb(unit_id year) vce(cluster unit_id)

* Option B: Factor variable notation (concise)
gen treated = !missing(treatment_year)
reghdfe outcome ib(-1).rel_time#1.treated, ///
    absorb(unit_id year) vce(cluster unit_id)

* Pre-trend test (works with either approach)
testparm lead*           // Option A
testparm *b(-1).rel_time#1.treated, equal  // Option B: test pre-period interactions
```

**Why pure dummies work in staggered designs:** When treatment timing varies across units, `rel_time == -5` maps to *different* calendar years for different cohorts, so the event-time dummies are not collinear with year FEs. Never-treated units typically have `rel_time` set to a sentinel value like -999, further breaking the collinearity.

### Event Study with Binned Endpoints

```stata
* Bin distant periods to reduce noise
generate rel_time_binned = rel_time
replace rel_time_binned = -5 if rel_time < -5 & rel_time != -999
replace rel_time_binned = 5 if rel_time > 5

* Same lead/lag naming to avoid hyphens in variable names
forvalues k = 5(-1)2 {
    generate lead`k' = (rel_time_binned == -`k')
}
forvalues k = 0/5 {
    generate lag`k' = (rel_time_binned == `k')
}
reghdfe outcome lead* lag*, absorb(unit_id year) vce(cluster unit_id)
```

### Automated Event Study (csdid)

```stata
ssc install csdid
ssc install drdid

* Callaway and Sant'Anna (2021)
csdid outcome x1 x2, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet

* Plot event study
estat event, window(-5 5) estore(cs_results)
csdid_plot, name(event_study, replace)

* Pre-trend test
estat pretrend
```

---

## Testing and Visualizing Parallel Trends

### Visual Inspection

```stata
preserve
collapse (mean) outcome, by(treated year)
twoway (connected outcome year if treated == 0, msymbol(circle)) ///
       (connected outcome year if treated == 1, msymbol(square)), ///
       xline(`treatment_year', lcolor(red)) ///
       legend(order(1 "Control" 2 "Treated"))
restore
```

### Formal Tests for Pre-Trends

```stata
reghdfe outcome lead* lag*, absorb(unit_id year) vce(cluster unit_id)

* Joint test of pre-treatment leads
test lead5 lead4 lead3 lead2
```

### Placebo Tests

```stata
* Assign fake treatment earlier, use only pre-treatment data
generate placebo_treatment = (year >= treatment_year - 3) if year < treatment_year
keep if year < treatment_year
reghdfe outcome placebo_treatment, absorb(unit_id year) vce(cluster unit_id)
* Should find no significant effect
```

---

## Staggered Treatment Adoption

### The Problem with TWFE

Standard TWFE with staggered adoption uses already-treated units as controls ("forbidden comparisons"), can have negative weights, and is biased under heterogeneous treatment effects.

### Goodman-Bacon Decomposition

```stata
ssc install bacondecomp

bacondecomp outcome, ddetail
bacondecomp outcome, stub(bacon_)
scatter bacon_estimate bacon_weight, ///
    xlabel(0(0.1)0.5) ylabel(-2(1)2) xline(0) yline(0)
```

### Callaway and Sant'Anna (2021) Estimator

```stata
ssc install csdid

* Group-time average treatment effects
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet

* Aggregations
estat simple     // Overall ATT
estat group      // By cohort
estat calendar   // By time period
estat event, window(-5 5) estore(event_results)  // Event study

* With covariates
csdid outcome x1 x2, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet

* Use never-treated as control instead of not-yet-treated
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year) ///
    method(dripw) long2
```

### Sun and Abraham (2021) Estimator

```stata
ssc install eventstudyinteract

eventstudyinteract outcome treat_*, ///
    cohort(treatment_year) control_cohort(never_treated) ///
    absorb(unit_id year) vce(cluster unit_id)

event_plot, default_look graph_opt(xtitle("Periods to Treatment") ///
    ytitle("Average Effect") xlabel(-5(1)5))
```

### de Chaisemartin and D'Haultfoeuille (2020)

```stata
ssc install did_multiplegt

did_multiplegt outcome unit_id year treatment, ///
    robust_dynamic dynamic(5) placebo(3) breps(100) cluster(unit_id)

* With controls
did_multiplegt outcome unit_id year treatment, ///
    controls(x1 x2) robust_dynamic dynamic(5) breps(100) cluster(unit_id)

* Results: Placebo_X (pre-treatment, should be 0), Effect (at treatment),
*          Dynamic_X (X periods after treatment)
matrix list e(effect)
matrix list e(N_effect)
```

### Imputation Methods

```stata
ssc install did_imputation

* Borusyak, Jaravel, Spiess (2021)
did_imputation outcome unit_id year treatment_year, ///
    autosample minn(0)

* Event study version
did_imputation outcome unit_id year treatment_year, ///
    horizons(0/5) pretrend(5)
event_plot, default_look
```

---

## Heterogeneous Treatment Effects

### Heterogeneity by Subgroup

```stata
did_multiplegt outcome unit_id year treatment if subgroup == 1, ///
    robust_dynamic dynamic(5) breps(100) cluster(unit_id)
estimates store subgroup1

did_multiplegt outcome unit_id year treatment if subgroup == 2, ///
    robust_dynamic dynamic(5) breps(100) cluster(unit_id)
estimates store subgroup2

estimates table subgroup1 subgroup2
```

### Quantile DiD

```stata
ssc install didq

didq outcome, tr(treated) time(post) quantile(0.25 0.50 0.75)
didq outcome, tr(treated) time(post) quantile(0.1(0.1)0.9)
didq_plot
```

---

## Synthetic Control Methods

### Basic Synthetic Control

```stata
ssc install synth

tsset unit_id year
synth outcome outcome(1990) outcome(1995) outcome(2000) ///
    x1 x2 x3, ///
    trunit(treated_unit_id) trperiod(treatment_year) ///
    keep(synth_results, replace) fig

* View weights
matrix list e(W_weights)   // Unit weights
matrix list e(V_matrix)    // Predictor weights
```

### Placebo Tests for Synthetic Control

```stata
* In-space placebo: Apply to each control unit
local control_units "2 3 4 5 6"
foreach unit of local control_units {
    capture synth outcome outcome(1990) outcome(1995) x1 x2, ///
        trunit(`unit') trperiod(treatment_year) ///
        keep(placebo_`unit', replace)
}

* In-time placebo: Fake treatment date
local fake_treatment = treatment_year - 5
synth outcome outcome(1990) outcome(1995) x1 x2, ///
    trunit(treated_unit) trperiod(`fake_treatment') ///
    keep(placebo_time, replace)
```

### Inference via RMSPE Ratios

```stata
use synth_results, clear

* Pre-treatment RMSPE
generate sq_error = (_Y_treated - _Y_synthetic)^2 if _time < treatment_year
quietly: summarize sq_error
local rmspe_pre = sqrt(r(mean))

* Post-treatment RMSPE
replace sq_error = (_Y_treated - _Y_synthetic)^2 if _time >= treatment_year
quietly: summarize sq_error
local rmspe_post = sqrt(r(mean))

local rmspe_ratio = `rmspe_post' / `rmspe_pre'
display "RMSPE Ratio: " `rmspe_ratio'
* Compare to placebo distribution of RMSPE ratios for p-value
```

---

## Triple Differences

Triple differences (DDD) adds a third difference to control for group-specific trends.

```stata
* Three dimensions: Treatment group x Time x Third dimension
generate ddd = treated * post * third_group

reghdfe outcome treated##post##third_group, ///
    absorb(state year demographic) vce(cluster state)
* Coefficient on three-way interaction is DDD estimate
```

### Example: Minimum Wage by Age Group

```stata
generate teen = (age >= 16 & age <= 19)
generate treated_state = inlist(state, "CA", "NY", "WA")
generate post_policy = (year >= 2016)

reghdfe employment treated_state##post_policy##teen ///
    age education, ///
    absorb(state year age_group) vce(cluster state)
* Coefficient on treated_state#post_policy#teen is the DDD estimate
```

---

## Standard Errors and Clustering

### Clustering Considerations

```stata
* Cluster at treatment level (most conservative)
reghdfe outcome post_treatment, absorb(unit_id year) vce(cluster state)

* Two-way clustering
reghdfe outcome post_treatment, absorb(unit_id year) vce(cluster state year)

* Multi-way clustering (requires reghdfe)
reghdfe outcome post_treatment, absorb(unit_id year) vce(cluster state year industry)
```

### Wild Bootstrap for Few Clusters

```stata
ssc install boottest

reghdfe outcome post_treatment, absorb(unit_id year) cluster(state)
boottest post_treatment, cluster(state) boottype(wild) reps(10000)
```

### Randomization Inference

```stata
* Save actual estimate
reghdfe outcome post_treatment, absorb(unit_id year)
local actual_coef = _b[post_treatment]

* Permutation test
set seed 12345
local n_perm = 1000
matrix perm_coefs = J(`n_perm', 1, .)

forvalues i = 1/`n_perm' {
    preserve
    sort unit_id
    generate random = runiform()
    bysort year: egen rank = rank(random)
    generate perm_treat = (rank <= number_treated)
    quietly: reghdfe outcome perm_treat, absorb(unit_id year)
    matrix perm_coefs[`i', 1] = _b[perm_treat]
    restore
}

svmat perm_coefs
count if abs(perm_coefs1) >= abs(`actual_coef')
local p_value = r(N) / `n_perm'
display "Randomization inference p-value: " `p_value'
```

### Spatial HAC Standard Errors

```stata
ssc install ols_spatial_HAC

ols_spatial_HAC outcome post_treatment x1 x2, ///
    lat(latitude) lon(longitude) time(year) ///
    distcutoff(500) lagcutoff(5)
```

---

## Recent Advances and Pitfalls

### Common Pitfalls

**1. Negative Weights in TWFE**
```stata
* Check with Bacon decomposition, then use robust estimators
bacondecomp outcome
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year)
```

**2. Violation of Parallel Trends** -- Consider: adding controls, matching on pre-treatment trends, synthetic control, or unit-specific trends (`absorb(unit_id#c.year)`).

**3. Clustering Too Low** -- Cluster at treatment variation level. Too few clusters? Use wild bootstrap.

**4. Choosing Wrong Comparison Group**
```stata
* Not-yet-treated (time-varying control)
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year) notyet

* Never-treated (time-invariant control)
csdid outcome, ivar(unit_id) time(year) gvar(treatment_year) long2
```

### Stacked DiD

```stata
* Create separate datasets for each treatment cohort, stack them
local cohorts "2010 2012 2015"
tempfile stacked
local first = 1
foreach cohort of local cohorts {
    use original_data, clear
    keep if treatment_year == `cohort' | missing(treatment_year)
    generate cohort = `cohort'
    generate cohort_id = unit_id * 10000 + `cohort'
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
reghdfe outcome post_treatment, ///
    absorb(cohort_id cohort#year) vce(cluster unit_id)
```

---

## Complete Workflow Examples

### Example 1: State Minimum Wage Policy

```stata
use "state_employment.dta", clear

* Define treatment
generate treated = inlist(state_name, "California", "New York", "Massachusetts")
generate treatment_year = 2014 if treated == 1
generate post = (year >= 2014) if treated == 1
replace post = 0 if treated == 0
encode state_name, generate(state_id)
xtset state_id year

* Visual trends
preserve
collapse (mean) teen_employment, by(treated year)
twoway (connected teen_employment year if treated == 0, msymbol(O)) ///
       (connected teen_employment year if treated == 1, msymbol(S)), ///
       xline(2014, lcolor(red) lpattern(dash)) ///
       legend(order(1 "Control States" 2 "Treated States"))
restore

* Basic DiD
reghdfe teen_employment i.treated##i.post, ///
    absorb(state_id year) vce(cluster state_id)
estimates store basic_did

* Event study
generate rel_time = year - treatment_year
replace rel_time = -999 if missing(treatment_year)
forvalues k = 5(-1)2 {
    generate lead`k' = (rel_time == -`k')
}
forvalues k = 0/5 {
    generate lag`k' = (rel_time == `k')
}
reghdfe teen_employment lead5 lead4 lead3 lead2 lag0-lag5, ///
    absorb(state_id year) vce(cluster state_id)

* Pre-trend test
test lead5 lead4 lead3 lead2

* Callaway-Sant'Anna (robust to staggered adoption)
csdid teen_employment gdp_growth population_growth, ///
    ivar(state_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet
estat simple
estat event, window(-5 5) estore(cs_event)
csdid_plot

* Placebo test (fake treatment at t-2)
preserve
keep if year < 2014
generate placebo_post = (year >= 2012)
reghdfe teen_employment i.treated##i.placebo_post, ///
    absorb(state_id year) vce(cluster state_id)
restore
```

### Example 2: Synthetic Control for Single Treatment

```stata
use "smoking.dta", clear
encode state, generate(state_id)
tsset state_id year

local treated_id = 3  // California
local treatment_year = 1989

* Synthetic control estimation
synth cigsale cigsale(1980) cigsale(1988) ///
    lnincome(1980(1)1988) retprice(1980(1)1988) age15to24(1980(1)1988), ///
    trunit(`treated_id') trperiod(`treatment_year') ///
    keep(synth_ca, replace) replace fig

matrix list e(W_weights)

* Gap plot
use synth_ca, clear
generate effect = _Y_treated - _Y_synthetic
twoway (line effect _time, lcolor(black)), ///
    xline(`treatment_year', lcolor(red) lpattern(dash)) ///
    yline(0, lcolor(gray)) ///
    xtitle("Year") ytitle("Gap in Cigarette Sales")

* In-space placebos for inference
* (Run synth for each control unit, compare RMSPE ratios)
```

### Example 3: Staggered DiD with did_multiplegt

```stata
use "paid_leave.dta", clear
bysort state_id (year): egen first_treat = min(year) if paid_leave == 1
bysort state_id: egen treatment_year = min(first_treat)

* Standard TWFE (potentially biased)
reghdfe female_lfp paid_leave gdp_pc unemployment_rate, ///
    absorb(state_id year) vce(cluster state_id)
estimates store twfe

* Bacon decomposition to diagnose
bacondecomp female_lfp, ddetail

* Heterogeneity-robust: did_multiplegt
did_multiplegt female_lfp state_id year paid_leave, ///
    robust_dynamic dynamic(10) placebo(5) breps(100) cluster(state_id)

* Heterogeneity-robust: Callaway-Sant'Anna
csdid female_lfp gdp_pc unemployment_rate, ///
    ivar(state_id) time(year) gvar(treatment_year) ///
    method(dripw) notyet
estat simple
estat event, window(-5 10) estore(cs_event)

* Wild cluster bootstrap for TWFE
reghdfe female_lfp paid_leave gdp_pc unemployment_rate, ///
    absorb(state_id year) cluster(state_id)
boottest paid_leave, cluster(state_id) boottype(wild) reps(999)
```

---

## Summary: When to Use Each Method

| Method | Use Case |
|--------|----------|
| Basic DiD (2x2) | Two periods, two groups, uniform treatment timing |
| TWFE | Multiple periods/groups; cautious with staggered timing |
| Event Study | Visualize dynamic effects, test parallel trends |
| `csdid` / `did_multiplegt` / `did_imputation` | Staggered adoption, heterogeneous effects |
| Synthetic Control | Single or few treated units, rich pre-treatment data |
| Triple Differences | Additional difference controls for group-specific trends |

### Essential Packages

```stata
ssc install reghdfe
ssc install ftools
ssc install csdid
ssc install drdid
ssc install did_multiplegt
ssc install did_imputation
ssc install eventstudyinteract
ssc install bacondecomp
ssc install synth
ssc install boottest
ssc install avar
ssc install coefplot
ssc install event_plot
```
