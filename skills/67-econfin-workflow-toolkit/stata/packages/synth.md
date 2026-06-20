# Synthetic Control Methods with synth

## Contents

- [Installation](#installation)
- [The synth Command Syntax](#the-synth-command-syntax)
- [Specifying Treated Unit and Predictors](#specifying-treated-unit-and-predictors)
- [Training and Treatment Periods](#training-and-treatment-periods)
- [Optimization Options](#optimization-options)
- [Obtaining Synthetic Weights](#obtaining-synthetic-weights)
- [Post-Estimation and Gaps](#post-estimation-and-gaps)
- [synth_runner for Multiple Treated Units](#synth_runner-for-multiple-treated-units)
- [In-Space Placebos](#in-space-placebos)
- [In-Time Placebos](#in-time-placebos)
- [Inference using RMSPE Ratios](#inference-using-rmspe-ratios)
- [Visualization of Results](#visualization-of-results)
- [Augmented Synthetic Control](#augmented-synthetic-control)
- [Complete Workflow Examples](#complete-workflow-examples)

---

## Installation

```stata
* Install synth and synth_runner
ssc install synth
ssc install synth_runner

* Update
adoupdate synth, update

* Check
which synth
which synth_runner
```

**Note:** Requires Stata 11+. For best performance, Stata 14+.

---

## The synth Command Syntax

### Basic Syntax

```stata
synth outcome_var predictor_vars(time_periods) ///
    outcome_var(pre_treatment_periods) ///
    , trunit(#) trperiod(#) ///
    [options]
```

### Required Arguments

- **outcome_var**: The dependent variable (e.g., cigarette sales, GDP)
- **trunit(#)**: Numeric identifier of the treated unit
- **trperiod(#)**: Time period when treatment begins

### Common Options Example

```stata
synth cigsale ///
    cigsale(1980) cigsale(1988) ///    // Outcome in specific years
    retprice beer age15to24 ///          // Time-varying predictors
    , trunit(3) trperiod(1989) ///       // California, treatment in 1989
    xperiod(1980(1)1988) ///             // Period for predictors
    mspeperiod(1970(1)1988) ///          // Period for MSPE calculation
    resultsperiod(1970(1)2000) ///       // Period for results
    keep(synth_results.dta) replace ///  // Save results
    fig                                   // Generate figure
```

### Predictor Specification Formats

```stata
* Format 1: Time-varying predictors averaged over period
retprice(1980(1)1988)  // Average retail price 1980-1988

* Format 2: Outcome variable in specific years
cigsale(1975 1980 1988)  // Sales in these specific years

* Format 3: Time-invariant predictors (still need a year)
population(1980)  // Population in 1980
```

### Complete Syntax Reference

```stata
synth depvar [predvar1 predvar2 ...] ///
    , trunit(#) trperiod(#) ///
    [counit(numlist) ///           // Specify donor pool
    xperiod(numlist) ///            // Period for predictor averaging
    mspeperiod(numlist) ///         // Period for fit calculation
    resultsperiod(numlist) ///      // Period to display
    customV(matname) ///            // Custom V matrix
    margin(#) ///                   // Optimization margin
    maxiter(#) ///                  // Maximum iterations
    sigf(#) ///                     // Significance level
    bound(#) ///                    // Bound on weights
    keep(filename) ///              // Save results
    replace ///                     // Overwrite existing file
    fig ///                         // Generate figure
    nested ///                      // Nested optimization
    allopt]                         // Show all optimization output
```

---

## Specifying Treated Unit and Predictors

### Identifying the Treated Unit

Unit identifiers must be numeric. Use `encode` for string identifiers:

```stata
encode state_name, generate(state_id)
tab state_name state_id
```

### Predictor Categories

```stata
* 1. Pre-treatment outcome values (lagged outcomes)
cigsale(1975 1980 1988)

* 2. Time-varying covariates (averaged over period)
retprice(1980(1)1988)
income(1980(1)1988)

* 3. Time-invariant covariates (need a year anyway)
population(1985)
region(1980)
```

### Example: California Proposition 99

```stata
use smoking.dta, clear
xtset state year

synth cigsale ///
    cigsale(1988) cigsale(1980) cigsale(1975) ///  // Pre-treatment sales
    retprice(1980(1)1988) ///                       // Average price
    beer(1980(1)1988) ///                           // Beer consumption
    age15to24(1980(1)1988) ///                      // Youth population
    , trunit(3) trperiod(1989) ///
    keep(synth_ca.dta) replace
```

### Choosing Predictors

- Use theory-driven variables known to affect the outcome
- Include lagged outcomes to match trends
- Predictors must not be affected by treatment anticipation
- Must be available for all units (missing data excludes controls)
- Number of predictors should be less than donor pool size (typical: 3-10)

---

## Training and Treatment Periods

### Three Key Periods

- **xperiod**: When to average time-varying predictors
- **mspeperiod**: When to calculate fit (training period)
- **resultsperiod**: When to display results

### Period Specification Syntax

```stata
1970(1)1988        // 1970, 1971, ..., 1988 (increment of 1)
1970(2)1988        // 1970, 1972, ..., 1988 (increment of 2)
1975 1980 1988     // Specific years only
```

### Predictor vs MSPE Period Can Differ

```stata
* Strategy: MSPE over longer period than predictor averaging
xperiod(1985(1)1988)      // Recent predictors only
mspeperiod(1970(1)1988)   // Fit over full history

* Useful when early predictors not available
* but you want to match long-run trends
```

### Guidelines

- Minimum: 5-10 pre-treatment periods; recommended 15-20+
- Avoid structural breaks in pre-period (financial crisis, wars)
- Longer pre-treatment better for volatile outcomes

---

## Optimization Options

### Nested vs Regression Optimization

```stata
* Regression method (default, faster) - good for most applications
synth cigsale ..., trunit(3) trperiod(1989)

* Nested method (slower, more accurate) - use when default fit is poor
synth cigsale ..., trunit(3) trperiod(1989) nested

* Show all optimization output
synth cigsale ..., trunit(3) trperiod(1989) allopt
```

### Custom V Matrix

```stata
* Assign your own predictor importance weights
matrix V = (1, 2, 1, 3, 5, 5, 5)

synth cigsale ///
    retprice(1980(1)1988) beer(1980(1)1988) age15to24(1980(1)1988) ///
    cigsale(1988) cigsale(1980) cigsale(1975) ///
    , trunit(3) trperiod(1989) ///
    customV(V)
```

### Iteration and Convergence

```stata
synth cigsale ..., maxiter(10000)  // Default 1000
synth cigsale ..., sigf(6)         // Less strict (default 7)
synth cigsale ..., sigf(8)         // More strict
synth cigsale ..., margin(0.001)   // Higher precision (default 0.005)
```

### Weight Bounds

```stata
* Prevent any single control from dominating
synth cigsale ..., bound(0.3)  // No unit > 30% weight
* Warning: Too restrictive bounds can worsen fit
```

### Troubleshooting

```stata
* Poor convergence: try nested, more iterations, or relax convergence
synth cigsale ..., nested maxiter(10000) sigf(5)

* Poor pre-treatment fit: add more lagged outcomes
synth cigsale cigsale(1988) cigsale(1980) cigsale(1975) cigsale(1970) ...

* Too slow: use default regression method, avoid nested
```

---

## Obtaining Synthetic Weights

### Extracting Weights

```stata
synth cigsale ///
    cigsale(1988) cigsale(1980) cigsale(1975) ///
    retprice(1980(1)1988) beer(1980(1)1988) ///
    , trunit(3) trperiod(1989) ///
    keep(synth_weights.dta) replace

* Unit weights (W) and predictor weights (V) in return matrices
matrix list e(W_weights)
matrix list e(V_weights)
```

### Interpreting Weights

- **W (unit weights)**: all between 0 and 1, sum to 1, many exactly 0 (sparse)
- **V (predictor weights)**: higher = more important for matching

### Creating a Weights Table

```stata
matrix W = e(W_weights)

preserve
clear
svmat W, names(weight)
generate state_id = _n
generate weight = weight1

merge 1:1 state_id using state_names.dta
keep if _merge == 3
keep state_name weight
keep if weight > 0.001
gsort -weight
list state_name weight, clean noobs
restore
```

### Constructing Synthetic Control Manually from Weights

```stata
use smoking.dta, clear
keep if inlist(state, 2, 6, 8)  // States with non-zero weights

generate weight = .
replace weight = 0.234 if state == 2
replace weight = 0.421 if state == 6
replace weight = 0.345 if state == 8

collapse (mean) synth_cigsale=cigsale [pw=weight], by(year)
```

### Assessing Weight Quality

```stata
* Count states in synthetic control
matrix W = e(W_weights)
mata: sum(st_matrix("W") :> 0.001)

* Good: 3-5 states with weights 0.1-0.4
* Warning: one state > 0.7 (too concentrated) or many tiny weights (overfitting)
```

### Exporting for Publication

```stata
use results.dta, clear
keep if _Co_Number != .
keep _Co_Number _W_Weight
rename _Co_Number state_id
rename _W_Weight weight

merge 1:1 state_id using statenames.dta
keep if _merge == 3
format weight %9.3f
keep if weight > 0.001
gsort -weight

texsave state_name weight using "table_weights.tex", ///
    replace title("Synthetic Control Weights") ///
    marker(tab:weights) hlines(0) frag
```

---

## Post-Estimation and Gaps

### Accessing Results

```stata
synth cigsale ..., trunit(3) trperiod(1989) ///
    keep(synth_results.dta) replace

use synth_results.dta, clear
* Key variables: _time, _Y_treated, _Y_synthetic, _Co_Number, _W_Weight
```

### Calculating Treatment Effects

```stata
use synth_results.dta, clear
keep _time _Y_treated _Y_synthetic

generate gap = _Y_treated - _Y_synthetic
generate post = (_time >= 1989)

summarize gap if post == 0  // Pre-treatment fit (should be small)
summarize gap if post == 1  // Post-treatment effects
```

### Pre-Treatment Fit: RMSPE

```stata
generate gap_sq = gap^2

summarize gap_sq if _time < 1989
scalar pre_RMSPE = sqrt(r(mean))

summarize gap_sq if _time >= 1989
scalar post_RMSPE = sqrt(r(mean))

scalar RMSPE_ratio = post_RMSPE / pre_RMSPE
display "RMSPE ratio: " RMSPE_ratio
```

### Visualizing the Gap

```stata
twoway (line gap _time) ///
    (function y=0, range(_time) lcolor(black) lpattern(dash)), ///
    xline(1989, lcolor(red) lpattern(dash)) ///
    xlabel(1970(5)2000) ylabel(, angle(0)) ///
    ytitle("Gap in Cigarette Sales (Packs per Capita)") ///
    xtitle("Year") legend(off) ///
    title("Treatment Effect: California vs Synthetic California")
```

### Assessing Match Quality

```stata
* Good fit: pre-treatment RMSPE < 10% of outcome mean
* Check predictor balance table and visual inspection
use synth_results.dta, clear
keep _time _Y_treated _Y_synthetic
generate pct_gap = 100 * abs(_Y_treated - _Y_synthetic) / _Y_treated
summarize pct_gap if _time < 1989
* If > 5%, try more predictors, nested optimization, or different donor pool
```

---

## synth_runner for Multiple Treated Units

### Installation and Syntax

```stata
ssc install synth_runner

synth_runner depvar predvars(period) depvar(years), ///
    trunit(numlist|varname) trperiod(#|varname) [options]
```

### Multiple Treatment Units

```stata
synth_runner cigsale ///
    cigsale(1988) cigsale(1980) ///
    retprice(1980(1)1988) beer(1980(1)1988), ///
    trunit(3 5 8) ///           // Multiple treated units
    trperiod(1989 1991 1993) /// // Corresponding treatment years
    gen_vars                     // Generate synthetic variables
```

### gen_vars Creates These Variables

- `synth_cigsale` : Synthetic control outcome
- `effect` : Treatment effect (gap)
- `pre_rmspe` : Pre-treatment RMSPE
- `post_rmspe` : Post-treatment RMSPE

### Using Variable Names for Units/Periods

```stata
synth_runner cigsale ///
    cigsale(1988) cigsale(1980) retprice(1980(1)1988), ///
    trunit(tr_unit) trperiod(tr_period) gen_vars
```

### Parallel Processing

```stata
ssc install parallel
parallel initialize 4  // Use 4 cores

synth_runner cigsale ///
    cigsale(1988) cigsale(1980) retprice(1980(1)1988), ///
    trunit(3 5 8 10 12 15) trperiod(1989) ///
    gen_vars parallel
```

### Automating Placebo Tests

```stata
use smoking.dta, clear
levelsof state, local(all_states)

synth_runner cigsale ///
    cigsale(1988) cigsale(1980) retprice(1980(1)1988), ///
    trunit(`all_states') trperiod(1989) ///
    gen_vars keep(placebo_results.dta) replace
```

---

## In-Space Placebos

Apply synthetic control to each untreated unit as if it were treated. If many untreated units show similar "effects," the treatment effect may not be real.

### Using synth_runner

```stata
use smoking.dta, clear
levelsof state, local(all_states)

synth_runner cigsale ///
    cigsale(1988) cigsale(1980) cigsale(1975) ///
    retprice(1980(1)1988) beer(1980(1)1988), ///
    trunit(`all_states') trperiod(1989) ///
    mspeperiod(1970(1)1988) resultsperiod(1970(1)2000) ///
    gen_vars
```

### Manual Loop Approach

```stata
levelsof state if state != 3, local(control_states)

foreach s in `control_states' {
    capture noisily synth cigsale ///
        cigsale(1988) cigsale(1980) cigsale(1975) ///
        retprice(1980(1)1988) beer(1980(1)1988), ///
        trunit(`s') trperiod(1989) ///
        counit(3) ///  // Exclude California from donor pool
        keep(placebo_`s'.dta) replace
}
```

### Filtering by Pre-Treatment Fit

```stata
* Keep only placebos with pre-treatment RMSPE < 2x treated unit's
summarize pre_rmspe if state == 3
local ca_rmspe = r(mean)
keep if pre_rmspe < 2 * `ca_rmspe' | state == 3
```

### Visualizing Placebo Effects

```stata
keep state year effect
reshape wide effect, i(year) j(state)

twoway (line effect3 year, lwidth(thick) lcolor(red)) ///
       (line effect* year, lcolor(gs12) lwidth(thin)), ///
       legend(off) xline(1989, lpattern(dash)) ///
       title("California vs Placebo Effects")
```

### Standardized Effects

```stata
* Divide by pre-treatment RMSPE to account for different fit quality
generate std_effect = effect / pre_rmspe
```

---

## In-Time Placebos

Assign a fake treatment date in the pre-treatment period. Should see no effect -- if one appears, suggests pre-existing differential trends.

### Basic In-Time Placebo

```stata
use smoking.dta, clear
keep if year <= 1988  // Before actual treatment

synth cigsale ///
    cigsale(1975) cigsale(1978) ///
    retprice(1975(1)1982) beer(1975(1)1982), ///
    trunit(3) trperiod(1983) ///  // Fake treatment in 1983
    mspeperiod(1970(1)1982) ///
    resultsperiod(1970(1)1988) ///
    keep(placebo_time_1983.dta) replace

use placebo_time_1983.dta, clear
keep _time _Y_treated _Y_synthetic
generate gap = _Y_treated - _Y_synthetic
summarize gap if _time >= 1983  // Should be small
```

### Multiple In-Time Placebos

```stata
local fake_years 1980 1983 1986

foreach fy in `fake_years' {
    preserve
    keep if year <= 1988
    local pre_end = `fy' - 1

    synth cigsale ///
        cigsale(1975) cigsale(`pre_end') ///
        retprice(1975(1)`pre_end') beer(1975(1)`pre_end'), ///
        trunit(3) trperiod(`fy') ///
        mspeperiod(1970(1)`pre_end') ///
        keep(placebo_time_`fy'.dta) replace
    restore
}
```

---

## Inference using RMSPE Ratios

**RMSPE Ratio** = Post-treatment RMSPE / Pre-treatment RMSPE. Large ratio suggests treatment caused divergence. Compare treated unit's ratio to placebo distribution.

### Permutation-Based P-Values

```stata
use smoking.dta, clear
levelsof state, local(all_states)

synth_runner cigsale ///
    cigsale(1988) cigsale(1980) cigsale(1975) ///
    retprice(1980(1)1988) beer(1980(1)1988), ///
    trunit(`all_states') trperiod(1989) ///
    mspeperiod(1970(1)1988) gen_vars

generate rmspe_ratio = post_rmspe / pre_rmspe

* Filter by pre-treatment fit
summarize pre_rmspe if state == 3
keep if pre_rmspe < 2 * r(mean)

* Calculate p-value
preserve
collapse (mean) rmspe_ratio, by(state)
gsort -rmspe_ratio
generate rank = _n
count
local total = r(N)
summarize rank if state == 3
local ca_rank = r(mean)
display "P-value: " `ca_rank' / `total'
restore
```

### RMSPE Ratio Bar Chart

```stata
collapse (mean) rmspe_ratio pre_rmspe, by(state)
summarize pre_rmspe if state == 3
keep if pre_rmspe < 2 * r(mean)

gsort -rmspe_ratio
generate rank = _n
generate is_ca = (state == 3)

twoway (bar rmspe_ratio rank if is_ca == 0, barwidth(0.8) color(gs12)) ///
       (bar rmspe_ratio rank if is_ca == 1, barwidth(0.8) color(red)), ///
       yline(1, lpattern(dash)) xlabel(none) ///
       legend(label(1 "Placebos") label(2 "California")) ///
       ytitle("Post/Pre RMSPE Ratio") title("RMSPE Ratios")
```

### Confidence Intervals from Placebo Distribution

```stata
generate std_effect = effect / pre_rmspe

* Percentiles from placebo distribution
preserve
keep if state != 3
collapse (p2.5) ci_lower=std_effect (p97.5) ci_upper=std_effect, by(year)
save ci_bounds.dta, replace
restore

keep if state == 3
merge 1:1 year using ci_bounds.dta

twoway (rarea ci_lower ci_upper year, color(gs14)) ///
       (line std_effect year, lcolor(red) lwidth(thick)) ///
       (function y=0, range(year) lpattern(dash)), ///
       xline(1989, lpattern(dash)) ///
       legend(label(1 "95% CI from placebos") label(2 "California")) ///
       title("Standardized Treatment Effect with Placebo-Based CI")
```

---

## Visualization of Results

### Basic Synth Plot

```stata
synth cigsale ..., trunit(3) trperiod(1989) fig
```

### Custom Trends Plot

```stata
use results.dta, clear
keep _time _Y_treated _Y_synthetic

twoway (line _Y_treated _time, lwidth(medthick) lcolor(black)) ///
       (line _Y_synthetic _time, lwidth(medthick) lpattern(dash) lcolor(gs8)), ///
       xline(1989, lpattern(shortdash) lcolor(red)) ///
       xlabel(1970(5)2000, angle(0)) ylabel(40(20)140, angle(0)) ///
       xtitle("Year") ytitle("Per-Capita Cigarette Sales (in packs)") ///
       legend(label(1 "California") label(2 "Synthetic California") ///
              ring(0) position(11))
graph export "synth_trends.png", replace width(2000)
```

### Gap Plot

```stata
generate gap = _Y_treated - _Y_synthetic

twoway (line gap _time, lwidth(medthick) lcolor(navy)) ///
       (function y=0, range(_time) lcolor(black) lpattern(dash)), ///
       xline(1989, lpattern(shortdash) lcolor(red)) ///
       xlabel(1970(5)2000) ylabel(, angle(0)) ///
       xtitle("Year") ytitle("Gap in Cigarette Sales") legend(off)
graph export "synth_gap.png", replace width(2000)
```

### Multi-Panel Figure

```stata
* Panel A: Trends
twoway (line _Y_treated _time) (line _Y_synthetic _time, lpattern(dash)), ///
       xline(1989, lpattern(dash)) title("(A) Trends") name(trends, replace)

* Panel B: Gap
twoway (line gap _time) (function y=0, range(_time) lpattern(dash)), ///
       xline(1989, lpattern(dash)) title("(B) Treatment Effect") name(gap, replace)

* Panel C: Placebos
twoway (line effect* year, lcolor(gs13 ...) lwidth(thin ...)) ///
       (line effect3 year, lcolor(red) lwidth(thick)), ///
       xline(1989, lpattern(dash)) title("(C) Placebo Tests") name(placebos, replace)

graph combine trends gap placebos, rows(3)
graph export "synth_combined.png", replace width(2000)
```

---

## Augmented Synthetic Control

Combines synthetic control with regression adjustment. Allows for imperfect pre-treatment fit by using regression to adjust for remaining imbalance.

### Installation

```stata
* From GitHub (requires Stata 16+)
net install augsynth, from("https://raw.githubusercontent.com/ebenmichael/augsynth-stata/master/")
```

### Basic Syntax

```stata
use smoking.dta, clear
generate treated = (state == 3 & year >= 1989)

augsynth cigsale retprice beer age15to24, ///
    unit(state) time(year) ///
    treated(treated) ///
    method(ridge)
```

### Augmentation Methods

```stata
method(ridge)   // Ridge regression (default)
method(en)      // Elastic net
method(lasso)   // LASSO
method(ols)     // Simple regression
```

### Sensitivity Analysis

```stata
local methods "ridge en lasso ols"

foreach m in `methods' {
    augsynth cigsale retprice beer, ///
        unit(state) time(year) treated(treated) method(`m')
    estimates store augsynth_`m'
}

estimates table augsynth_*, stats(N) star
```

### When to Use Augsynth vs Standard Synth

- **Standard synth**: good pre-treatment fit achievable, want transparent weights, small sample, non-technical audience
- **Augsynth**: poor pre-treatment fit with standard synth, many covariates with small donor pool, staggered adoption, need standard errors

---

## Complete Workflow Examples

### Example 1: California Proposition 99

```stata
* Load data
use "http://web.stanford.edu/~jhain/synthdata/smoking.dta", clear
xtset state year

* Step 1: Run Synthetic Control
synth cigsale ///
    cigsale(1988) cigsale(1980) cigsale(1975) ///
    retprice(1980(1)1988) beer(1980(1)1988) age15to24(1980(1)1988), ///
    trunit(3) trperiod(1989) ///
    mspeperiod(1970(1)1988) resultsperiod(1970(1)2000) ///
    keep(results_ca.dta) replace nested

matrix list e(W_weights)
matrix list e(V_weights)

* Step 2: Pre-Treatment Fit
use results_ca.dta, clear
keep _time _Y_treated _Y_synthetic
generate gap = _Y_treated - _Y_synthetic
generate gap_sq = gap^2
summarize gap_sq if _time < 1989
scalar pre_rmspe = sqrt(r(mean))
display "Pre-treatment RMSPE: " pre_rmspe

* Step 3: Treatment Effects
summarize gap if _time >= 1989
display "Average treatment effect: " r(mean) " packs per capita"

* Step 4: Placebo Tests
use smoking.dta, clear
levelsof state, local(all_states)

synth_runner cigsale ///
    cigsale(1988) cigsale(1980) cigsale(1975) ///
    retprice(1980(1)1988) beer(1980(1)1988) age15to24(1980(1)1988), ///
    trunit(`all_states') trperiod(1989) ///
    mspeperiod(1970(1)1988) resultsperiod(1970(1)2000) gen_vars

summarize pre_rmspe if state == 3
keep if pre_rmspe < 2 * r(mean)
generate rmspe_ratio = post_rmspe / pre_rmspe

* Step 5: P-value
preserve
collapse (mean) rmspe_ratio, by(state)
gsort -rmspe_ratio
generate rank = _n
count
local total = r(N)
summarize rank if state == 3
display "P-value: " r(mean) / `total'
restore

* Step 6: Robustness - different predictors
use smoking.dta, clear
synth cigsale ///
    cigsale(1988) cigsale(1985) cigsale(1980) ///
    retprice(1985(1)1988) beer(1985(1)1988), ///
    trunit(3) trperiod(1989) keep(robust1.dta) replace

* Robustness - exclude specific donors
synth cigsale ///
    cigsale(1988) cigsale(1980) retprice(1980(1)1988), ///
    trunit(3) trperiod(1989) ///
    counit(1/2 4/39) keep(robust3.dta) replace
```

### Example 2: Staggered Adoption

```stata
use staggered_minwage.dta, clear

generate treated = !missing(treatment_year)
levelsof state if treated, local(treated_units)

foreach s in `treated_units' {
    summarize treatment_year if state == `s'
    local tr_year = r(mean)
    local pre_end = `tr_year' - 1

    synth employment ///
        employment(`pre_end') employment(`=`pre_end'-5') ///
        gdp(1990(1)`pre_end') minwage(1990(1)`pre_end'), ///
        trunit(`s') trperiod(`tr_year') ///
        mspeperiod(1990(1)`pre_end') ///
        keep(results_state`s'.dta) replace
}

* Combine and aggregate
clear
foreach s in `treated_units' {
    append using results_state`s'.dta
}
collapse (mean) avg_effect=gap, by(year_relative_to_treatment)
```
