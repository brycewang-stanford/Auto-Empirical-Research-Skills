# reghdfe: High-Dimensional Fixed Effects Regression

## Overview

`reghdfe` estimates linear regressions with multiple levels of fixed effects. It absorbs FEs using iterative algorithms (conjugate gradient, alternating projections) without creating dummy variables.

**Key advantages:**
- Handles multiple high-dimensional fixed effects efficiently
- Dramatically faster than `xtreg`, `areg`, and `reg` with factor variables
- Supports multi-way clustering of standard errors
- Integrates with `ivreghdfe` for IV estimation
- Can save fixed effects estimates

## Installation

```stata
ssc install reghdfe
ssc install ftools

// Optional companions
ssc install ivreghdfe
ssc install ivreg2

// Verify
webuse nlswork, clear
reghdfe ln_wage tenure ttl_exp, absorb(idcode year)
```

## Basic Syntax and Usage

```stata
reghdfe depvar indepvars [if] [in] [weight], absorb(absvars) [options]
```

```stata
// Single fixed effect
reghdfe ln_wage tenure ttl_exp, absorb(idcode)

// Two fixed effects
reghdfe ln_wage tenure ttl_exp, absorb(idcode year)

// With clustered standard errors
reghdfe ln_wage tenure ttl_exp, absorb(idcode year) vce(cluster idcode)
```

### Output Key Statistics
- **Within R-squared**: Variation explained after absorbing FEs (the one to report)
- **Singletons dropped**: Observations uniquely identifying an FE category (automatically dropped)

## Multiple Fixed Effects

### Two-Way, Three-Way, and Beyond

```stata
// Two-way (most common panel specification)
reghdfe log_sales marketing R_and_D, absorb(firm_id year)

// Three-way (AKM-style matched employer-employee)
reghdfe log_wage experience, absorb(worker_id firm_id year)

// Four-way
reghdfe log_exports tariff, absorb(industry country year product)
```

### Interacted Fixed Effects

```stata
// Region-specific year effects (region x year)
reghdfe employment policy, absorb(region_id region_id#year)

// Firm-specific linear trends
reghdfe sales marketing, absorb(firm_id firm_id#c.year)

// Industry x year fixed effects
reghdfe log_wage education, absorb(worker_id industry#year)
```

### Diagnostics

```stata
reghdfe log_wage experience, absorb(worker_id firm_id year) verbose(3)
// Shows: levels per FE, singletons, connected components, convergence
```

## Clustered Standard Errors

### Single and Multi-Way Clustering

```stata
// Single-way
reghdfe log_wage experience, absorb(firm_id year) vce(cluster firm_id)

// Two-way
reghdfe log_wage experience, absorb(worker_id) vce(cluster firm_id year)

// Three-way
reghdfe log_wage experience, absorb(occupation) ///
    vce(cluster worker_id firm_id year)
```

### Other VCE Options

```stata
reghdfe log_wage experience, absorb(firm_id) vce(robust)
reghdfe log_wage experience, absorb(firm_id) vce(bootstrap, reps(1000))
reghdfe log_wage experience, absorb(firm_id) vce(jackknife)
reghdfe log_wage experience, absorb(firm_id) vce(ols)
```

**Gotcha**: With few clusters (<30), inference may be unreliable. Consider wild cluster bootstrap (`boottest`).

## IV/2SLS with ivreghdfe

```stata
ivreghdfe depvar (endogvar = instruments) controls, absorb(absvars) [options]
```

```stata
// Basic IV
ivreghdfe log_wage (education = distance_college) experience, ///
    absorb(state_id year) cluster(state_id)

// Multiple endogenous variables
ivreghdfe log_wage (education experience = distance parent_educ sibling_educ) ///
    age married, absorb(state year) cluster(state)

// First stage diagnostics
ivreghdfe log_wage (education = distance) experience, ///
    absorb(state year) cluster(state) first savefirst
est restore _ivreg2_education
est replay

// Endogeneity test
ivreghdfe log_wage (education = distance) experience, ///
    absorb(state year) cluster(state) endog(education)

// LIML and GMM alternatives
ivreghdfe log_wage (education = distance) experience, ///
    absorb(state year) cluster(state) liml
ivreghdfe log_wage (education = distance) experience, ///
    absorb(state year) cluster(state) gmm2s
```

## Comparison with Other Commands

```stata
// DON'T: create dummies manually
tab firm_id, gen(firm_dummy)
reg wage experience firm_dummy1-firm_dummy10000

// DO: use reghdfe
reghdfe wage experience, absorb(firm_id)
```

| Feature | reg | areg | xtreg, fe | reghdfe |
|---------|-----|------|-----------|---------|
| Multiple high-dim FEs | No | No | No | Yes |
| Speed (large data) | Slow | Moderate | Moderate | Fast |
| Multi-way clustering | No | No | No | Yes |
| Save fixed effects | No | Partial | No | Yes |
| IV estimation | No | No | No | Yes (ivreghdfe) |
| Interacted FEs | Limited | Limited | No | Yes |

**Key differences from `areg`**: `areg` absorbs only ONE high-dim FE; others must be factor variables. No multi-way clustering.

**Key differences from `xtreg, fe`**: Only one panel dimension. Use `xtreg` when you need panel-specific diagnostics (`xttest2`, `xtserial`) or random effects.

### Approximate Runtime Benchmarks

| N | Workers | Firms | Years | reg (factor) | areg | reghdfe |
|---|---------|-------|-------|--------------|------|---------|
| 100K | 10K | 1K | 10 | 45 sec | 15 sec | 3 sec |
| 1M | 50K | 10K | 20 | Infeasible | 5 min | 30 sec |
| 10M | 100K | 50K | 20 | Infeasible | Infeasible | 3 min |

## Post-Estimation

```stata
reghdfe log_wage experience education, absorb(firm_id year) cluster(firm_id)

// Predictions
predict resid, residuals
predict xb, xb              // excluding FEs
predict xbd, xbd            // including FEs

// Tests
test experience = education
testparm experience education age   // joint significance
lincom experience + education

// Stored results
ereturn list
// e(r2_within), e(r2_a), e(rmse), e(N), e(df_a), e(df_r)

// Model comparison
reghdfe log_wage experience, absorb(firm_id year)
est store model1
reghdfe log_wage experience education age, absorb(firm_id year)
est store model2
est table model1 model2, star stats(N r2 r2_a)
```

## Saving Fixed Effects and Residuals

```stata
// Save FEs using name=variable syntax in absorb()
reghdfe log_wage experience education, absorb(fe_firm=firm_id fe_year=year)
// Creates fe_firm and fe_year variables

// Save residuals
reghdfe log_wage experience education, absorb(firm_id year) residuals(wage_resid)

// Connected components (for multi-way FEs)
reghdfe log_wage experience, absorb(worker_id firm_id) groupvar(component)
tab component
// Most data should be in one large component
```

### Analyzing Saved FEs

```stata
reghdfe log_wage experience, ///
    absorb(fe_worker=worker_id fe_firm=firm_id fe_year=year) cluster(worker_id)

// Variance decomposition
tabstat fe_worker fe_firm fe_year, stat(mean sd p10 p50 p90) col(stat)

// Collapse to firm level and analyze
preserve
collapse (mean) fe_firm firm_size, by(firm_id)
scatter fe_firm firm_size, msize(tiny)
restore
```

### Exporting FEs

```stata
reghdfe log_wage experience education, absorb(fe_firm=firm_id fe_year=year)

preserve
collapse (mean) fe_firm, by(firm_id)
export delimited using "firm_fixed_effects.csv", replace
restore
```

## Integration with Other Packages

### esttab (estout)

```stata
ssc install estout

reghdfe log_wage experience, absorb(firm_id) cluster(firm_id)
est store m1
reghdfe log_wage experience education, absorb(firm_id year) cluster(firm_id)
est store m2

esttab m1 m2 using "table1.tex", ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label replace booktabs ///
    keep(experience education) ///
    stats(N r2_within, labels("Observations" "Within R-sq")) ///
    indicate("Firm FE = firm_id" "Year FE = year")
```

### outreg2

```stata
reghdfe log_wage experience, absorb(firm_id) cluster(firm_id)
outreg2 using results.doc, replace ctitle("Model 1") ///
    addtext(Firm FE, YES, Year FE, NO)
```

### coefplot

```stata
reghdfe log_wage experience education age married, ///
    absorb(firm_id year) cluster(firm_id)
coefplot, drop(_cons) xline(0) title("Wage Determinants")
```

### boottest (Wild Bootstrap)

```stata
ssc install boottest
reghdfe outcome treatment controls, absorb(firm_id year) cluster(state)
boottest treatment, cluster(state) boottype(wild) reps(10000)
// Better inference with <30 clusters
```

### ppmlhdfe (Poisson with FEs)

```stata
ssc install ppmlhdfe
ppmlhdfe trade_volume tariff, absorb(exporter importer year)
// Handles zeros in dependent variable (no log(0) issue)
```

## Performance Tips

```stata
// 1. Compress data types
compress

// 2. Sort by fixed effects (improves cache locality)
sort firm_id worker_id year

// 3. Acceleration options
reghdfe log_wage experience, absorb(firm_id year) accel(cg)
// accel(cg): conjugate gradient (faster)
// accel(a): alternating (2 FEs only, fastest)

// 4. Relax tolerance for speed
reghdfe log_wage experience, absorb(firm_id year) tol(1e-6)
// Default 1e-8; 1e-6 still accurate for most applications

// 5. Suppress output for batch jobs
reghdfe log_wage experience, absorb(firm_id year) verbose(0)

// 6. Memory management
set max_memory 32g
```

## Common Pitfalls

```stata
// PITFALL: Time-invariant variables absorbed by unit FE
reghdfe log_wage female, absorb(worker_id)  // female is absorbed!
// FIX: Interact with time-varying variables instead
reghdfe log_wage c.experience##i.female, absorb(worker_id firm_id year)

// PITFALL: Forgetting to cluster
reghdfe log_wage treatment, absorb(state year)  // Wrong SEs!
// FIX: Cluster at treatment-assignment level
reghdfe log_wage treatment, absorb(state year) cluster(state)

// PITFALL: Reporting overall R-squared
// FIX: Report within R-squared with FEs

// PITFALL: Interpreting as between-group effects
// FIX: Coefficients are within-group estimates
```

## Best Practices Checklist

1. **Data prep**: `compress`, check for singletons, create numeric IDs with `egen group()`
2. **Build incrementally**: Start with one FE, add more, compare with `est table`
3. **Cluster appropriately**: At treatment-assignment level; use `boottest` if <30 clusters
4. **Always report**: N, number of FE levels, within R-squared, clustering structure
5. **Check diagnostics**: `verbose(3)` for singletons, `groupvar()` for connected components
6. **Reproducibility**: Document `which reghdfe`, set `version`, save `.ster` files

## Quick Reference

```stata
// Installation
ssc install reghdfe ftools

// Basic usage
reghdfe depvar indepvars, absorb(fe1 fe2 ...) cluster(clustervar)

// Save fixed effects
reghdfe depvar indepvars, absorb(fe_saved=fe1 fe2)

// IV estimation
ivreghdfe depvar (endog = instruments) exog, absorb(fe1 fe2) cluster(clustervar)
```

## References

- Correia, S. (2016). "Linear Models with High-Dimensional Fixed Effects: An Efficient and Feasible Estimator."
- http://scorreia.com/software/reghdfe/
