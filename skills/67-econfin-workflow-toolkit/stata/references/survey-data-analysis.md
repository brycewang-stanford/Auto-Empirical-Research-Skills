# Survey Data Analysis in Stata

## Table of Contents
1. [Survey Design Declaration (svyset)](#survey-design-declaration-svyset)
2. [Survey Weights](#survey-weights)
3. [Stratification and Clustering](#stratification-and-clustering)
4. [Finite Population Corrections](#finite-population-corrections)
5. [Survey Estimation Commands](#survey-estimation-commands)
6. [Subpopulation Analysis](#subpopulation-analysis)
7. [Survey Postestimation](#survey-postestimation)
8. [Linearization vs Replicate Weights](#linearization-vs-replicate-weights)
9. [Design Effects and Effective Sample Size](#design-effects-and-effective-sample-size)
10. [Complex Survey Design Examples](#complex-survey-design-examples)
11. [Best Practices and Common Pitfalls](#best-practices-and-common-pitfalls)

---

## Survey Design Declaration (svyset)

### Basic Syntax

```stata
svyset [psu] [weight], strata(varname) fpc(varname) vce(method) options
```

### Common Design Patterns

```stata
* Simple random sample with weights
svyset [pweight = sampwgt]

* Single-stage cluster sample
svyset psu [pweight = sampwgt], strata(stratum)

* Two-stage design
svyset psu [pweight = sampwgt], strata(stratum) || ssu

* Three-stage design
svyset psu [pweight = sampwgt], strata(stratum) || ssu || tsu
```

### Example: NHANES

```stata
webuse nhanes2f, clear
svyset psuid [pweight = finalwgt], strata(stratid)

svyset          // Display current settings
svydescribe     // Detailed description of design
svydescribe, single  // Check for singleton PSUs
```

---

## Survey Weights

### Weight Types

```stata
* Sampling weight = inverse of selection probability
generate sampwgt = 1 / prob_selection

* Final weight = base weight x non-response adj x post-stratification adj
generate finalwgt = basewgt * nonresp_adj * poststrat_adj

* Always use pweight with svyset
svyset [pweight = finalwgt]
```

### Weight Diagnostics

```stata
summarize sampwgt, detail
histogram sampwgt
tabstat sampwgt, by(stratum) statistics(mean sd min max cv)

* Check for problems
count if sampwgt <= 0
count if missing(sampwgt)
```

### Weight Trimming

```stata
summarize sampwgt, detail
scalar p99 = r(p99)

generate wgt_trimmed = sampwgt
replace wgt_trimmed = `=p99' if sampwgt > `=p99'
```

---

## Stratification and Clustering

### Stratification

```stata
* Simple stratified design
svyset [pweight = sampwgt], strata(region)

* With clustering
svyset psu [pweight = sampwgt], strata(region)

* Multiple stratification variables -- create combined variable
generate stratum_id = region*100 + urbanicity
svyset psu [pweight = sampwgt], strata(stratum_id)
```

### Clustering

```stata
* Single-stage clustering
svyset school_id [pweight = student_wgt]

* Multi-stage: Regions -> Households
svyset region [pweight = hhwgt] || household

* Three-stage: Districts -> Villages -> Households
svyset district [pweight = hhwgt], strata(province) ///
       || village || household
```

### Singleton and Certainty PSUs

```stata
* Check for singleton PSUs
svydescribe, single

* Options for handling singletons:
svyset psuid [pweight = finalwgt], strata(stratid) singleunit(centered)
* Options: missing, certainty, scaled, centered (default)
```

---

## Finite Population Corrections

Use FPC when sampling fraction > 5% (n/N > 0.05).

### FPC with Population Totals

```stata
generate fpc1 = pop_size_stratum
svyset psu [pweight = weight], strata(stratum) fpc(fpc1)
```

### FPC with Sampling Rates

```stata
generate sampling_rate = 0.10
generate fpc = _N / sampling_rate
svyset [pweight = weight], fpc(fpc)
```

### Multi-Stage FPC

```stata
svyset district [pweight = hhwgt], strata(province) fpc(fpc_district) ///
       || village, fpc(fpc_village) ///
       || household
```

---

## Survey Estimation Commands

The `svy:` prefix adapts standard commands for survey data.

### Descriptive Statistics

```stata
svy: mean income                        // Overall mean
svy: mean income, over(region)          // Means by group
svy, level(90): mean income             // 90% CI

svy: proportion race                    // Proportions
svy: proportion race, over(region)

svy: ratio (income/assets)              // Ratios
svy: total income                       // Population totals
svy: total income, over(region)
```

### Tabulation

```stata
svy: tabulate race                      // One-way
svy: tabulate race region               // Two-way
svy: tabulate race region, row col cell // With proportions
svy: tabulate race region, pearson      // Chi-squared test
svy: tabulate race, ci deff             // CI and design effects
```

### Regression

```stata
svy: regress income education experience age
svy: regress income i.race i.region education
svy: regress income c.education##i.gender

svy: logistic employed education experience
svy: logit employed education experience, or   // Odds ratios
svy: probit employed education experience
svy: mlogit occupation education experience
svy: ologit health_status income education age
svy: poisson num_visits age chronic_conditions
svy: nbreg num_visits age chronic_conditions
```

---

## Subpopulation Analysis

### Critical: Use subpop(), Not if

```stata
* WRONG -- drops observations from variance estimation
svy: mean income if gender == 1

* RIGHT -- keeps full design information
svy, subpop(if gender == 1): mean income
```

The `if` qualifier drops observations before variance calculation, which biases standard errors. `subpop()` retains the full design.

### Usage Patterns

```stata
* With indicator variable
generate female = (gender == 2)
svy, subpop(female): mean income

* Complex conditions
svy, subpop(if age >= 18 & age <= 30): mean income

* Subpopulation regression
svy, subpop(if employed == 1): regress income education experience

* Comparing subpopulations
svy, subpop(if gender == 1): regress income education
estimates store male
svy, subpop(if gender == 2): regress income education
estimates store female
suest male female
test [male_mean]education = [female_mean]education
```

### over() vs subpop()

```stata
* over() -- estimates for each group simultaneously
svy: mean income, over(region)

* subpop() -- restricts to one subgroup
svy, subpop(if region == 1): mean income

* Combine both
svy, subpop(if age >= 65): mean income, over(gender)
```

---

## Survey Postestimation

### Available Commands After svy

```stata
margins           // Marginal effects and predictive margins
marginsplot       // Plot margins
contrast          // Contrasts
pwcompare         // Pairwise comparisons
test              // Hypothesis tests
lincom            // Linear combinations
nlcom             // Nonlinear combinations
estat effects     // Design effects
```

### Margins

```stata
svy: regress bpsystol age i.race i.sex
margins race
margins, at(age=(30 40 50 60 70))
margins, dydx(age race)
margins race, atmeans
marginsplot, noci
```

### Contrasts and Pairwise

```stata
svy: regress income i.education i.region
contrast education
contrast ar.education              // Adjacent categories
contrast r.education               // Reference category
pwcompare education, mcompare(bonferroni)
```

### Tests and Linear Combinations

```stata
svy: regress income education experience age i.race
test 2.race 3.race 4.race
test education = experience
lincom education + 2*experience
lincom 2.race - 3.race
```

### Predictions

```stata
svy: regress income education experience age
predict yhat
predict resid, residuals
predict se_pred, stdp

svy: logistic employed education experience
predict pr_employed
```

---

## Linearization vs Replicate Weights

### Linearization (Default)

```stata
svyset psu [pweight = sampwgt], strata(stratum) vce(linearized)
* Or simply:
svyset psu [pweight = sampwgt], strata(stratum)
```

### Replicate Weight Methods

#### BRR (Balanced Repeated Replication)
For designs with exactly 2 PSUs per stratum:
```stata
svyset psu [pweight = sampwgt], strata(stratum) vce(brr)
svyset psu [pweight = sampwgt], strata(stratum) vce(brr) fay(0.5)  // Fay's adjustment
```

#### Jackknife
```stata
svyset psu [pweight = sampwgt], strata(stratum) vce(jackknife)
```

#### Bootstrap
```stata
svyset psu [pweight = sampwgt], strata(stratum) vce(bootstrap) bsn(500)
```

### Using Pre-Computed Replicate Weights

Many surveys provide replicate weights:
```stata
* BRR replicate weights
svyset [pweight = finalwgt], vce(brr) brrweight(rep_wgt1-rep_wgt80)

* Jackknife replicate weights
svyset [pweight = finalwgt], vce(jackknife) jkrweight(rep_wgt1-rep_wgt80)

* Bootstrap replicate weights
svyset [pweight = finalwgt], vce(bootstrap) bsrweight(rep_wgt1-rep_wgt200)
```

### When to Use Each

| Method | Use When |
|--------|----------|
| Linearization | Standard design, PSU/stratum info available |
| BRR | Exactly 2 PSUs per stratum, or pre-computed BRR weights |
| Jackknife | Complex statistics, unequal PSUs per stratum |
| Bootstrap | No PSU info, very complex statistics |

---

## Design Effects and Effective Sample Size

### Computing Design Effects

```stata
svy: mean income
estat effects

* Output:
*   Deff = Var_complex / Var_SRS  (>1 means less efficient than SRS)
*   Deft = SE_complex / SE_SRS = sqrt(Deff)
*   Meft = misspecification effect
```

### Effective Sample Size

```stata
* n_eff = n / Deff
* Example: if Deff=1.5 and n=1000, n_eff = 667

svy: mean bpsystol
estat effects
count
display "Effective N = " r(N) / 1.503   // Using Deff from estat effects
```

### Design Effects by Subgroup

```stata
forvalues r = 1/4 {
    svy, subpop(if race == `r'): mean bpsystol
    estat effects
}
```

### Adjusting Sample Size Calculations

```stata
* SRS sample size
power onemean 120, sd(15) diff(5)

* Adjust for complex design
scalar n_needed = 141 * 1.5   // n_srs * expected_deff
display "Sample size needed: " n_needed
```

---

## Complex Survey Design Examples

### DHS-Style Multi-Stage Survey

```stata
* Stratified by region/urban, two-stage (EAs then households)
svyset ea [pweight = finalwgt], strata(stratum) fpc(fpc_ea) ///
       || household || person, singleunit(scaled)

svydescribe

* Analysis
svy, subpop(child_u5): proportion vaccinated
svy, subpop(if age >= 18 & female): mean bmi, over(region)
svy, subpop(if age >= 15 & female): logistic anemia age i.region i.urban
margins region
marginsplot
estat effects
```

### Panel Survey with BRR Weights

```stata
svyset [pweight = finalwgt], vce(brr) brrweight(brr_1-brr_80)

svy, subpop(if wave == 3): mean income
svy: mean income, over(wave)
```

### Dual-Frame Survey (Landline + Cell)

```stata
* Composite weight adjusts for frame overlap
generate composite_wgt = base_wgt
replace composite_wgt = base_wgt * 0.5 if dual_user

svyset psu [pweight = finalwgt], strata(stratum)
svy: proportion internet_use, over(frame)
```

---

## Best Practices and Common Pitfalls

### Critical Pitfalls

**1. Using `if` instead of `subpop()`:**
```stata
* WRONG -- biased variance
svy: mean income if gender == 1
keep if age >= 65
svy: mean income

* RIGHT
svy, subpop(if gender == 1): mean income
svy, subpop(if age >= 65): mean income
```

**2. Ignoring clustering:**
```stata
* WRONG -- treats as SRS, underestimates SE
regress income education [pweight = sampwgt]

* RIGHT
svy: regress income education
```

**3. Forgetting to declare PSUs:**
```stata
* WRONG -- ignores clustering
svyset [pweight = sampwgt], strata(stratum)

* RIGHT
svyset psu [pweight = sampwgt], strata(stratum)
```

**4. Wrong weight type:**
```stata
* WRONG -- fweights duplicate observations
summarize income [fweight = sampwgt]

* RIGHT
svy: mean income
```

**5. Missing values silently alter the subpopulation:**
Listwise deletion in `svy` commands can silently shrink the realized subpopulation when covariates have missing values. You may think you are estimating on the full sample, but missingness in any variable drops those observations without warning.
```stata
* Check missingness before estimation
misstable summarize income education experience age

* Compare N in output to expected subpopulation size
svy: regress income education experience age
```

**6. `svy` commands set their own VCE — you cannot override it:**
The variance estimation method is locked at `svyset` time. Specifying `vce()` on a `svy:` command is an error.
```stata
* WRONG -- vce() is not allowed on svy: commands
svy: regress y x, vce(robust)

* RIGHT -- set VCE at svyset time
svyset psu [pweight = sampwgt], strata(stratum) vce(linearized)
svy: regress y x
```

**7. Misusing replicate weights:**
```stata
* WRONG -- treating replicate weights as separate analyses
foreach var of varlist brr_* {
    svyset [pweight = `var']
    svy: mean income
}

* RIGHT
svyset [pweight = finalwgt], vce(brr) brrweight(brr_*)
svy: mean income
```

### Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| "stratum with only one PSU" | Singleton PSU | `svyset ..., singleunit(certainty)` |
| "sum of weights equals zero" | Missing/zero weights | Check `count if sampwgt <= 0` |
| "missing standard error" | Singleton PSU or tiny subgroup | Check `svydescribe, single` |

### Validation Checklist

```stata
svyset                                    // Design is correct
codebook psu stratum sampwgt              // All variables present
assert sampwgt > 0 if !missing(sampwgt)   // Weights positive
svydescribe, single                       // No singleton PSUs
svy: mean outcome
estat effects                             // Design effects reasonable
```

---

## Quick Reference

```stata
* Core workflow
svyset psu [pweight = sampwgt], strata(stratum)
svydescribe
svy: mean outcome
svy: regress y x1 x2
estat effects

* Key help files
help svy
help svyset
help svy_estimation
help svy_postestimation
```

### Example Datasets

```stata
webuse nhanes2       // NHANES
webuse nhanes2f      // NHANES with design vars
webuse nhanes2brr    // NHANES with BRR weights
```

### References

- Heeringa, West, & Berglund (2017). *Applied Survey Data Analysis*
- Lohr (2019). *Sampling: Design and Analysis*
- Stata Survey Data Reference Manual
