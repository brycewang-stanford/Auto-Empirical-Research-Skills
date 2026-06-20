# Instrumental Variables Packages: ivreg2 and ivreghdfe

## Overview

- **ivreg2**: Extended IV/2SLS with comprehensive diagnostics (Baum, Schaffer, Stillman) -- first-stage F-stats, weak instrument tests, Hansen J, endogeneity tests, LIML/GMM/CUE estimation
- **ivreghdfe**: IV regression absorbing high-dimensional fixed effects efficiently (Correia) -- multi-way clustering, integrates with reghdfe ecosystem

### When to Use Each

```stata
// ivreg2: comprehensive diagnostics, no high-dimensional FE, LIML/CUE/GMM
// ivreghdfe: many fixed effects (firm, year, industry), large datasets, multi-way clustering
```

## Installation

```stata
ssc install ivreg2
ssc install ranktest       // Required for rank tests
ssc install xtivreg2       // Panel IV

ssc install ivreghdfe
ssc install reghdfe        // Main FE package
ssc install ftools         // Fast tools dependency
```

### GitHub (Latest Versions)

```stata
net install ftools, from("https://raw.githubusercontent.com/sergiocorreia/ftools/master/src/")
net install reghdfe, from("https://raw.githubusercontent.com/sergiocorreia/reghdfe/master/src/")
net install ivreghdfe, from("https://raw.githubusercontent.com/sergiocorreia/ivreghdfe/master/src/")
```

## Basic Syntax

### ivreg2

```stata
ivreg2 depvar [exog_vars] (endog_vars = instruments) [if] [in] [weight], [options]
```

### ivreghdfe

```stata
ivreghdfe depvar [exog_vars] (endog_vars = instruments), ///
    absorb(fixed_effects) [options]
```

### Examples

```stata
// Basic IV
ivreg2 mpg foreign (price = weight length turn), first robust

// Multiple endogenous variables
ivreg2 mpg foreign (price price2 = weight length turn headroom), first robust

// ivreghdfe with fixed effects
ivreghdfe mpg (price = weight length), absorb(firm year) cluster(firm)
```

---

## First-Stage Diagnostics

### Key Statistics

```stata
ivreg2 mpg foreign (price = weight length turn), first ffirst robust
```

**First-stage F-statistic**: Rule of thumb F > 10; better to compare against Stock-Yogo critical values.

**Kleibergen-Paap F**: Robust version of Cragg-Donald; use when specifying `robust` or `cluster()`.

**Partial R-squared**: How much variation in endogenous variable is explained by excluded instruments after partialing out included instruments.

**Shea's Partial R-squared**: For multiple endogenous variables; accounts for correlation among endogenous regressors.

### Stock-Yogo Critical Values

Reported in output. Depend on number of endogenous variables and excluded instruments. Example (1 endogenous, 3 instruments): 10% maximal IV size ~ 16.38, 15% ~ 8.96, 20% ~ 6.66.

### Accessing Stored Results

```stata
ivreg2 mpg foreign (price = weight length), cluster(firm) first

scalar f_stat = e(widstat)       // Kleibergen-Paap F (with cluster)
scalar cd_stat = e(cdf)          // Cragg-Donald F
scalar partial_r2 = e(pr2)      // Partial R-squared
```

---

## Weak Instruments Testing

### Anderson-Rubin Test

Valid inference even with weak instruments (conservative but correct size):

```stata
ivreg2 mpg foreign (price = weight length turn), robust
scalar ar_p = e(archi2p)    // p < 0.05: endogenous var has significant effect
```

### Weak Instrument Detection Strategy

```stata
// Step 1: Check first-stage F
ivreg2 wage experience (education = parent_edu sibling_edu), first robust
scalar f_stat = e(widstat)

// Step 2: If weak, use LIML and Anderson-Rubin test
if f_stat < 10 {
    ivreg2 wage experience (education = parent_edu sibling_edu), robust liml
    display "AR test p-value = " e(archi2p)
}
```

### Addressing Weak Instruments

**LIML** (less biased than 2SLS with weak instruments):
```stata
ivreg2 wage experience (education = parent_edu sibling_edu), liml robust
```

**Fuller's modified LIML** (reduces median bias further):
```stata
ivreg2 wage experience (education = parent_edu sibling_edu), fuller(1) robust
```

**Jackknife IV**:
```stata
ssc install jive
jive wage experience (education = parent_edu sibling_edu), robust
```

---

## Overidentification Tests

Require more instruments than endogenous variables.

### Hansen J Test (Robust)

```stata
ivreg2 mpg foreign (price = weight length turn), robust

scalar j_stat = e(j)
scalar j_p = e(jp)     // p > 0.05: cannot reject instrument validity
```

**Hansen vs Sargan**: Use Hansen J (with `robust`) in practice. Sargan (without `robust`) assumes i.i.d. errors.

### C-Statistic (Difference-in-Hansen)

Test validity of a specific instrument subset:

```stata
// Built-in orthog() option
ivreg2 mpg foreign (price = weight length turn), robust orthog(turn)
// C-statistic for 'turn' reported; p > 0.05 means cannot reject exogeneity
```

Manual approach:
```stata
quietly ivreg2 mpg foreign (price = weight length turn), robust
scalar j_full = e(j)

quietly ivreg2 mpg foreign turn (price = weight length), robust
scalar c_stat = j_full - e(j)
scalar c_p = chi2tail(1, c_stat)
```

---

## Endogeneity Tests

### Durbin-Wu-Hausman via endog() Option

```stata
ivreg2 wage experience (education = parent_edu sibling_edu), robust endog(education)

scalar endog_p = e(endogp)
// p > 0.05: cannot reject exogeneity (OLS may be preferred)
// p < 0.05: reject exogeneity (use IV)
```

### Manual Augmented Regression Approach

```stata
// First-stage residuals
quietly reg education parent_edu sibling_edu experience, robust
predict education_resid, residuals

// Include residuals in OLS; test significance
regress wage education experience education_resid, robust
test education_resid    // p < 0.05: reject exogeneity
```

**Caveat**: Endogeneity test unreliable with weak instruments (low power).

---

## Standard Errors

### Options

```stata
ivreg2 y x1 (x2 = z1 z2), robust               // Heteroskedasticity-robust (default choice)
ivreg2 y x1 (x2 = z1 z2), cluster(firm)         // Cluster-robust (need 30-50+ clusters)
ivreghdfe y x1 (x2 = z1), absorb(firm year) cluster(firm year)  // Two-way clustering
```

### HAC (Kernel-Robust) Standard Errors

```stata
ivreg2 y x1 (x2 = z1), bw(4) kernel(bartlett)
// Bandwidth rule of thumb: T^(1/4) or floor(4(T/100)^(2/9))
```

Coefficients are identical across SE specifications; only standard errors and test statistics differ.

---

## LIML, GMM, and Alternative Estimators

### Estimator Options in ivreg2

```stata
ivreg2 y x1 (x2 = z1 z2), robust first           // 2SLS (default)
ivreg2 y x1 (x2 = z1 z2), liml robust first       // LIML
ivreg2 y x1 (x2 = z1 z2), fuller(1) robust first  // Fuller's modified LIML
ivreg2 y x1 (x2 = z1 z2), gmm2s robust first      // Two-step efficient GMM
ivreg2 y x1 (x2 = z1 z2), cue robust first        // Continuously Updated Estimator
ivreg2 y x1 (x2 = z1 z2), kclass(1.1) robust      // General k-class
```

### Which Estimator to Use

| Instrument Strength | Recommended Estimator |
|---------------------|----------------------|
| Strong (F > 20) | 2SLS (simplest, well-known) |
| Moderate (10 < F < 20) | LIML or Fuller(1) |
| Weak (F < 10) | Fuller(1); report Anderson-Rubin CIs |
| Heteroskedasticity matters | GMM or CUE (more efficient) |
| Just-identified (# instr = # endog) | All equivalent; use 2SLS |

---

## Partial Out Options and ivreghdfe

### ivreg2 partial() Option

```stata
// Partial out controls (faster, identical coefficients)
ivreg2 wage (education = parent_edu), ///
    partial(gender race age age2 region1-region50) robust
```

### ivreghdfe Usage

```stata
// Absorb high-dimensional FE (much faster than dummy variables)
ivreghdfe wage experience (education = parent_edu), ///
    absorb(firm_id year) cluster(firm_id)

// Multiple FE with interactions
ivreghdfe sales advertising (price = cost), ///
    absorb(firm_id year firm_id#year) cluster(firm_id)

// Save absorbed fixed effects
ivreghdfe wage experience (education = parent_edu), ///
    absorb(firm_fe=firm_id year_fe=year) cluster(firm_id)
// firm_fe and year_fe now contain estimated FE

// Diagnostics
ivreghdfe wage experience (education = parent_edu sibling_edu), ///
    absorb(firm_id year) cluster(firm_id) first
scalar f_stat = e(widstat)
scalar j_p = e(jp)
```

### Enhanced Diagnostics with savefirst

```stata
ivreghdfe wage experience (education = parent_edu sibling_edu), ///
    absorb(firm_id year) cluster(firm_id) first savefirst saverf

estimates restore _ivreg2_education    // First-stage for education
estimates restore _ivreg2_wage         // Reduced-form
```

---

## Best Practices

### DO's

1. **Always check first-stage F** -- Kleibergen-Paap F with robust/cluster; compare to Stock-Yogo critical values
2. **Use `robust` by default** -- required for valid Hansen J; ensures correct KP statistics
3. **Test overidentifying restrictions** when possible -- report Hansen J; investigate with C-statistic via `orthog()`
4. **Justify instruments theoretically** -- statistical tests cannot prove the exclusion restriction
5. **Use appropriate estimator** -- 2SLS for strong instruments, LIML/Fuller for moderate/weak
6. **Cluster when appropriate** -- panel: cluster by unit; need 30-50+ clusters
7. **Report full diagnostics** -- first-stage F, Hansen J, endogeneity test, number of instruments

### DON'Ts

1. **Don't use too many instruments** -- overfits first stage, weakens Hansen J; rule of thumb: instruments < clusters / 5
2. **Don't ignore weak instruments** -- 2SLS severely biased when F < 10
3. **Don't treat endogeneity test as definitive** -- low power with weak instruments
4. **Don't include 1000s of dummies manually** -- use ivreghdfe `absorb()`
5. **Don't report only IV** -- show OLS for comparison plus all diagnostics

---

## Quick Diagnostic Program

```stata
capture program drop iv_diagnostics
program define iv_diagnostics
    syntax, [title(string)]
    if "`title'" != "" display "`title'"

    scalar kp_f = e(widstat)
    scalar hansen_p = e(jp)
    scalar endog_p = e(endogp)

    display "KP F: " %6.2f kp_f ///
        cond(kp_f > 20, " (strong)", cond(kp_f > 10, " (moderate)", " (WEAK)"))
    display "Hansen J p: " %5.3f hansen_p ///
        cond(hansen_p > 0.05, " (valid)", " (INVALID)")
    display "Endogeneity p: " %5.3f endog_p ///
        cond(endog_p < 0.05, " (endogenous, IV needed)", " (exogenous?)")
end

// Usage:
ivreg2 ln_wage age tenure (grade = parent_edu sibling_edu), robust first endog(grade)
iv_diagnostics, title("Education IV Diagnostics")
```

---

## Quick Reference

```stata
// Basic IV with diagnostics
ivreg2 y x1 (x2 = z1 z2), robust first

// With clustering
ivreg2 y x1 (x2 = z1 z2), cluster(id) first

// Test endogeneity
ivreg2 y x1 (x2 = z1 z2), robust endog(x2)

// Test individual instruments
ivreg2 y x1 (x2 = z1 z2), robust orthog(z2)

// LIML for weak instruments
ivreg2 y x1 (x2 = z1), liml robust first

// Fuller (recommended for moderate/weak instruments)
ivreg2 y x1 (x2 = z1), fuller(1) robust first

// Fixed effects IV
ivreghdfe y x1 (x2 = z1 z2), absorb(firm year) cluster(firm)

// Access diagnostics
scalar f = e(widstat)    // Kleibergen-Paap F
scalar j = e(j)          // Hansen J
scalar p = e(jp)         // Hansen J p-value
```

### Key References

- Baum, Schaffer, Stillman (2007). "Enhanced routines for instrumental variables/GMM estimation and testing"
- Stock & Yogo (2005). "Testing for Weak Instruments in Linear IV Regression"
- Correia (2017). "Linear Models with High-Dimensional Fixed Effects" (reghdfe)

```stata
help ivreg2
help ivreghdfe
help reghdfe
```
