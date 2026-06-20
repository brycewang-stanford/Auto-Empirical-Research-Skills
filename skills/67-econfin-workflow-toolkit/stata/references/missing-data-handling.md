# Missing Data Handling in Stata

## Table of Contents
1. [Missing Value Representation](#missing-value-representation)
2. [Types of Missingness](#types-of-missingness)
3. [Missing Data Patterns and Diagnostics](#missing-data-patterns-and-diagnostics)
4. [Multiple Imputation Framework](#multiple-imputation-framework)
5. [Imputation Methods](#imputation-methods)
6. [Analyzing Imputed Data](#analyzing-imputed-data)
7. [Combining Results Across Imputations](#combining-results-across-imputations)
8. [Maximum Likelihood Approaches](#maximum-likelihood-approaches)
9. [Complete Case Analysis](#complete-case-analysis)
10. [Sensitivity Analysis](#sensitivity-analysis)
11. [Practical Workflows](#practical-workflows)
12. [Best Practices and Recommendations](#best-practices-and-recommendations)

---

## Missing Value Representation

```stata
.      // Generic missing (numeric)
.a-.z  // Extended missing values (27 types for different reasons)
""     // Missing string value
```

**Critical gotcha: missing values sort as larger than any non-missing value:**
```stata
* WRONG -- missing age will be flagged as true!
generate flag = (age > 50)

* Correct approaches:
generate flag = (age > 50) if !missing(age)
generate flag = (age > 50 & age < .)
```

### Extended Missing Value Codes

```stata
replace wage = .r if refused_wage == 1        // .r = refused
replace wage = .d if dont_know_wage == 1      // .d = don't know
replace wage = .n if not_applicable == 1      // .n = not applicable

* Tabulate reasons
count if wage == .r
summarize age if wage < .  // All non-missing (any missing > any non-missing)
```

---

## Types of Missingness

| Mechanism | Depends on Observed? | Depends on Missing? | Standard MI Valid? | Complete Case Bias? |
|-----------|---------------------|---------------------|-------------------|---------------------|
| MCAR | No | No | Yes | No (but inefficient) |
| MAR | Yes | No | Yes | Generally yes |
| MNAR | Maybe | Yes | No | Yes |

**Testing for MCAR:**
```stata
* ssc install mcartest
* mcartest wage age grade hours
```

**Checking MAR (association between missingness and observed variables):**
```stata
generate wage_missing = missing(wage)
logit wage_missing age grade, nolog
```

---

## Missing Data Patterns and Diagnostics

### Summarizing Missing Data

```stata
misstable summarize
misstable summarize wage age grade hours

misstable patterns
misstable patterns wage age grade hours, frequency

misstable nested wage age grade hours
```

### Missing Data by Variable

```stata
egen nmiss = rowmiss(wage age grade hours)
tabulate nmiss

generate wage_miss = missing(wage)
```

### Analyzing Missing Data Patterns

```stata
generate wage_miss = missing(wage)

* Compare means by missing status
tabstat age grade hours, by(wage_miss) statistics(mean sd n)
ttest age, by(wage_miss)

* Logistic regression of missingness
logit wage_miss age grade i.race married, nolog
```

### Missing Data Correlations

```stata
foreach var of varlist wage age grade hours {
    generate miss_`var' = missing(`var')
}
pwcorr miss_*, star(0.05)
tabulate miss_wage miss_age, chi2 expected
```

---

## Multiple Imputation Framework

### Setting Up MI Data

```stata
* Register data as MI data
mi set mlong  // mlong is most flexible format

* Register variables
mi register imputed wage age grade  // Variables to be imputed
mi register regular hours married   // Complete variables (no missing)

* Check MI setup
mi describe
mi varying
mi query
```

### MI Data Formats

```stata
mi set wide     // Separate variables for each imputation
mi set mlong    // Most flexible, recommended
mi set flong    // One observation per imputation
mi set flongsep // Separate files for each imputation

* Convert between formats
mi convert mlong, clear
```

### MI Data Management

```stata
mi update                // Run after modifying variables
mi describe
mi extract 0, clear      // m=0 is original data with missing
mi extract 1, clear      // m=1 is first imputation
mi unset                 // Drop MI settings
```

---

## Imputation Methods

### Univariate Imputation Methods

#### Regression Imputation (continuous, normal)
```stata
mi impute regress wage age grade hours i.race i.married, ///
    add(20) rseed(12345) noisily
```

#### Predictive Mean Matching (robust general-purpose)
```stata
mi impute pmm wage age grade hours i.race i.married, ///
    add(20) rseed(12345) knn(5)

* knn(#) = number of nearest neighbors to draw from
* knn(3) more variable; knn(10) less variable; default knn(1)
```
PMM imputes actual observed values -- no normality assumption needed, preserves distribution, handles non-linearity.

#### Truncated Regression (bounded variables)
```stata
mi impute truncreg wage age grade hours, ll(0) add(20) rseed(12345)
mi impute truncreg score age, ll(0) ul(100) add(20) rseed(12345)
```

#### Logistic Imputation (binary)
```stata
mi impute logit married age grade wage i.race, add(20) rseed(12345) augment
* augment adds observation to prevent perfect prediction
```

#### Ordered Logistic (ordinal)
```stata
mi impute ologit educ_level age wage hours i.race, add(20) rseed(12345) augment
```

#### Multinomial Logistic (nominal)
```stata
mi impute mlogit race age grade wage i.married, add(20) rseed(12345) augment
```

#### Poisson (count)
```stata
mi impute poisson nchildren age married wage, add(20) rseed(12345)
```

### Multivariate Imputation: Chained Equations (MICE)

```stata
* Different models for different variable types
mi impute chained ///
    (pmm, knn(5)) wage hours ///
    (truncreg, ll(0)) tenure ///
    (logit) married ///
    = age i.race, ///
    add(25) rseed(12345) burnin(10) ///
    savetrace(trace, replace)

* Key options:
* burnin(#)     - iterations before first imputation (default 10)
* savetrace()   - save iteration history for convergence checks
* dryrun        - check model specification without imputing
* chaindots     - show iteration dots
* noisily       - show each iteration's results
* augment       - prevent perfect prediction
```

**General syntax:**
```stata
mi impute chained ///
    (method1) var1 var2 ///           // Variables using method1
    (method2, options) var3 ///       // Variable with options
    = predictor1 predictor2, ///      // Common predictors
    add(M) burnin(B)                  // Global options
```

### Checking Convergence

```stata
mi impute chained (...) ..., savetrace(trace, replace)

use trace, clear
tsset iter
tsline wage1 wage2 wage3, title("Trace plot: Wage")
* Should look like random noise around mean
```

### Passive Imputation (derived variables)

```stata
mi register passive wage_hrs  // Derived variable

mi impute chained ///
    (regress) wage hours ///
    (passive: wage * hours) wage_hrs ///
    = age grade i.race, add(20) rseed(12345)

* Other passive examples:
* (passive: exp(log_wage)) wage
* (passive: wage > 20) high_wage
* (passive: age^2) age_squared
```

---

## Analyzing Imputed Data

### Basic MI Estimation

```stata
mi estimate: regress wage age grade hours i.race

* Automatically runs on each imputed dataset and pools via Rubin's rules
```

### Supported Estimation Commands

```stata
mi estimate: regress wage age grade hours i.race
mi estimate: logit married age wage i.race
mi estimate: mlogit occupation age grade wage
mi estimate: ologit job_satisfaction wage hours married
mi estimate: poisson num_jobs age grade
mi estimate: nbreg num_children age married wage
mi estimate: stcox age grade wage, basehc(race)
mi estimate: xtreg wage age grade hours, fe
mi estimate: xtlogit employed age wage, re
mi estimate: ivregress 2sls wage age (educ = parent_educ)
```

### MI Estimate Options

```stata
mi estimate, mcerror: regress wage age grade      // Monte Carlo error
mi estimate, vartable: regress wage age grade     // Show variance components
mi estimate, post: regress wage age grade         // Enable post-estimation
margins, dydx(*)                                  // Works after post
mi estimate, saving(miresults): regress wage age grade
```

### Examining Individual Imputations

```stata
mi estimate, noisily: regress wage age grade hours   // Show each imputation
mi xeq 1: regress wage age grade      // Run on imputation 1
mi xeq 0: regress wage age grade      // Run on original data (m=0)
mi xeq 1/5: regress wage age grade    // Run on imputations 1-5
mi xeq: summarize wage age grade      // Run on all
```

### Post-Estimation After MI

```stata
* Most post-estimation doesn't work directly after mi estimate
* Solution: Use post option
mi estimate, post: regress wage age grade hours i.race
margins, dydx(age)
margins race
margins, at(age=(20(5)60))

* mi predictnl for predictions
mi estimate: regress wage age grade
mi predictnl wage_pred = predict(), label(Predicted wage)

mi estimate: logit employed age wage
mi predictnl p_emp = predict(pr), label(Pr(Employed))
```

### Testing After MI Estimation

```stata
mi estimate: regress wage age grade hours tenure
mi test age
mi test age grade
mi testnl _b[age] = _b[grade]

mi estimate: regress wage age grade i.race
mi test 2.race 3.race
```

---

## Combining Results Across Imputations

### Understanding MI Output

```stata
mi estimate: regress wage age grade
/*
Key output statistics:
- RVI: Relative Variance Increase -- how much variance increased due to missing data
       RVI = (1 + 1/M) * B/W
- FMI: Fraction of Missing Information -- proportion of variance due to missing data
       FMI close to 1 = lots of missing information
       FMI close to 0 = little missing information
- RE:  Relative Efficiency = (1 + FMI/M)^(-1)
       RE = 0.95 means 95% as efficient as infinite imputations
*/
```

### Choosing Number of Imputations

```stata
* Modern rule: M = % missing information
* M >= 20 for estimation, M >= 100 for hypothesis testing

* Check adequacy:
mi estimate, mcerror: regress wage age grade
* Monte Carlo SE should be < 10% of SE
```

### Manual Pooling

For commands `mi estimate` doesn't support:
```stata
forvalues m = 1/20 {
    mi xeq `m': {
        regress wage age grade
        matrix b`m' = e(b)
        matrix V`m' = e(V)
    }
}
* Pool manually using Rubin's rules
```

---

## Maximum Likelihood Approaches

### Full Information Maximum Likelihood (FIML)

```stata
* SEM with FIML (uses all available info, assumes MAR)
sem (wage <- age grade hours), method(ml) missing
* 'missing' option activates FIML
```

### Panel Data with Missing Waves

```stata
webuse nlswork, clear
xtset idcode year

xtreg ln_wage age grade, re   // ML handles unbalanced panels
xtreg ln_wage age grade, fe   // FE automatically handles missing waves
```

### MI vs. FIML

- **FIML**: Simpler workflow, theoretically efficient, no convergence issues; but limited to models that support it (mainly SEM), typically only handles missing Y
- **MI**: Works with any estimation command, easier diagnostics, can impute predictors

---

## Complete Case Analysis

```stata
* Default in Stata -- automatically drops observations with missing
regress wage age grade hours

* Acceptable when: truly MCAR, < 5% missing, or exploratory only
* Check whether complete cases differ:
generate complete = !missing(wage, age, grade, hours)
tabstat age grade hours, by(complete) statistics(mean sd) nototal
```

### Pairwise Deletion

```stata
pwcorr wage age grade hours, obs
* Caution: different N per pair, can produce non-positive-definite matrices
```

---

## Sensitivity Analysis

### Pattern-Mixture Models

```stata
* Compare complete-case vs MI estimates
regress wage age grade hours if !missing(wage)
estimates store complete_case

mi estimate: regress wage age grade hours
estimates store mi_est

estimates table complete_case mi_est, b se
```

### Tipping Point Analysis

```stata
* Adjust imputed values by different amounts to test MNAR sensitivity
forvalues delta = 0(0.5)5 {
    mi extract 1, clear
    replace wage = wage + `delta' if mi_miss == 1
    mi estimate: regress wage age grade
    estimates store delta`delta'
}
```

### Varying Imputation Models

```stata
* Compare: PMM few predictors, PMM many predictors, regression imputation
mi impute pmm wage age grade, add(20) rseed(1) replace
mi estimate: regress wage age grade
estimates store model1

mi impute pmm wage age grade hours tenure i.race i.married, ///
    add(20) rseed(1) replace
mi estimate: regress wage age grade
estimates store model2

estimates table model1 model2, b se star
```

### MI Diagnostics

```stata
* Compare distributions
mi xeq 0: summarize wage, detail          // Original
mi xeq 1/5: summarize wage, detail        // Imputations

* Check imputation model fit
mi impute pmm wage age grade hours, add(20) rseed(123) noisily replace
```

---

## Practical Workflows

### Workflow 1: Simple MI

```stata
* 1. Examine missing data
misstable summarize
misstable patterns wage age grade hours

* 2. Set up MI
mi set mlong
mi register imputed wage
mi register regular age grade hours race married
mi describe

* 3. Impute
mi impute pmm wage age grade hours i.race married, ///
    add(10) rseed(54321) noisily

* 4. Check quality
mi xeq 0: summarize wage, detail
mi xeq 1/5: summarize wage, detail

* 5. Analyze
mi estimate: regress wage age grade hours
mi estimate, vartable: regress wage age grade hours

* 6. Post-estimation
mi estimate, post: regress wage age grade hours
margins, dydx(*)

* 7. Sensitivity: compare to complete case
regress wage age grade hours
estimates store complete_case
estimates table mi_results complete_case, b(%9.3f) se star stats(N)
```

### Workflow 2: Chained Equations (Multiple Incomplete Variables)

```stata
* 1. Diagnose
misstable summarize wage hours tenure grade
misstable patterns wage hours tenure grade, frequency

* 2. Setup
mi set mlong
mi register imputed wage hours tenure grade
mi register regular age race married

* 3. Dry run
mi impute chained ///
    (pmm, knn(5)) wage hours ///
    (truncreg, ll(0)) tenure ///
    (regress) grade ///
    = age i.race married, dryrun

* 4. Impute
mi impute chained ///
    (pmm, knn(5)) wage hours ///
    (truncreg, ll(0)) tenure ///
    (regress) grade ///
    = age i.race married, ///
    add(25) burnin(15) rseed(98765) ///
    savetrace(convergence, replace) chaindots

* 5. Check convergence
use convergence, clear
tsset iter
tsline wage1 wage2 wage3, title("Convergence: wage")

* 6. Analyze
mi estimate: regress wage grade hours tenure i.race married
```

### Workflow 3: Complex Survey Data with MI

```stata
* Include survey design variables in imputation model
mi set mlong
mi register imputed bpsystol bpdiast hdresult
mi register regular age sex race diabetes i.psu i.strata finalwgt

mi impute chained ///
    (pmm, knn(3)) bpsystol bpdiast ///
    (logit) hdresult ///
    = age sex i.race diabetes i.psu i.strata, add(20) rseed(123)

* Declare survey design after imputation
mi svyset psu [pweight=finalwgt], strata(strata)

mi estimate: svy: regress bpsystol age sex i.race diabetes
mi estimate: svy, subpop(if sex==1): mean bpsystol
```

### Workflow 4: Panel Data with MI

```stata
webuse nlswork, clear
xtset idcode year

* Include person-level means to capture panel structure
by idcode: egen mean_wage = mean(ln_wage)

mi set mlong
mi register imputed ln_wage hours
mi register regular age grade tenure mean_wage

mi impute chained ///
    (pmm) ln_wage hours ///
    = age grade tenure mean_wage i.year, ///
    add(20) rseed(123) by(idcode)
* by(idcode) imputes within person

mi estimate: xtreg ln_wage age grade hours, fe
mi estimate: xtreg ln_wage age grade hours, re
```

---

## Best Practices and Recommendations

### Imputation Model Building

```stata
* Include in imputation model:
* 1. All variables in analysis model
* 2. Auxiliary variables correlated with missing variables
* 3. Auxiliary variables predicting missingness
* 4. Interactions/transformations if in analysis model

* DON'T impute: identifiers, already-complete time-invariant vars,
* variables with > 50% missing (unless special circumstances)
```

### Method Selection Guide

| Variable Type | Recommended Method | Alternative |
|---------------|-------------------|-------------|
| Continuous, normal | `regress` | `pmm` |
| Continuous, non-normal | `pmm` | `truncreg` if bounded |
| Continuous, non-negative | `truncreg, ll(0)` | `pmm` |
| Binary | `logit` | `pmm` |
| Ordinal categorical | `ologit` | `mlogit` |
| Nominal categorical | `mlogit` | N/A |
| Count | `poisson` | `pmm` or `nbreg` |
| **General robust choice** | **`pmm`** | Works for almost everything |

### Common Mistakes to Avoid

```stata
* MISTAKE 1: Not imputing all incomplete analysis variables
mi impute pmm wage = age grade, add(20)
mi estimate: regress wage age grade hours  // hours not imputed!
* Fix: impute all incomplete vars with chained equations

* MISTAKE 2: Not including interactions in imputation model
mi impute pmm wage = age grade, add(20)
mi estimate: regress wage c.age##c.grade   // interaction not modeled!
* Fix: include interaction terms or use passive imputation

* MISTAKE 3: Imputing derived variables directly
mi impute chained (regress) wage log_wage = ..., add(20)  // Wrong!
* Fix: impute base variable, use passive for derived
mi impute pmm wage = ..., add(20)
mi passive: generate log_wage = log(wage)

* MISTAKE 4: Forgetting mi update after creating new variables
generate new_var = age^2
mi update   // Required!

* MISTAKE 5: Registering incomplete variable as regular
mi register regular wage  // Wrong if wage has missing!
mi varying                // Check with this
```

### Advanced Tips

```stata
* TIP 1: "Impute and delete" -- impute more variables than needed
* to help the imputation model, then analyze a subset
mi impute chained (pmm) wage hours income occupation = ..., add(20)
mi estimate: regress wage age grade  // Use only subset

* TIP 2: Wide format for large datasets (faster but less flexible)
mi convert wide, clear

* TIP 3: Save imputation results for post-estimation
mi estimate, post saving(miest): regress wage age grade
estimates use miest
margins, at(age=(20(5)60))
```

---

## Summary

**Recommended Workflow:**
```stata
* 1. Examine missingness: misstable summarize/patterns
* 2. Set up MI: mi set mlong, mi register
* 3. Choose method(s): PMM as robust default
* 4. Impute with diagnostics: savetrace, noisily
* 5. Check quality: compare observed vs imputed distributions
* 6. Analyze: mi estimate: [command]
* 7. Sensitivity analysis: vary models, tipping point
* 8. Report: FMI, RVI, method details
```

**Further Reading:**
- `help mi`
- Rubin (1987). Multiple Imputation for Nonresponse in Surveys
- van Buuren (2018). Flexible Imputation of Missing Data
