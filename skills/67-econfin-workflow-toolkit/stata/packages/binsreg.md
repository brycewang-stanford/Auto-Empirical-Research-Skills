# BINSREG: Binscatter Estimation and Inference

## Overview

The `binsreg` package (Cattaneo, Crump, Farrell, Feng) implements modern binscatter methods with rigorous statistical foundations: data-driven bin selection, pointwise and uniform inference, hypothesis testing, and support for OLS, logit, probit, and quantile regression.

**Key advantage over traditional `binscatter` (Stepner):** Proper covariate adjustment (no residualization), formal inference (CI/CB), optimal bin selection, and hypothesis testing.

### Package Commands

| Command | Purpose |
|---------|---------|
| `binsreg` | Binscatter for continuous outcomes (OLS) |
| `binslogit` | Binscatter for binary outcomes (logit) |
| `binsprobit` | Binscatter for binary outcomes (probit) |
| `binsqreg` | Binscatter for quantile regression |
| `binstest` | Hypothesis testing (linearity, monotonicity, shape) |
| `binspwc` | Pairwise group comparison |
| `binsregselect` | Optimal bin count selection |

---

## Installation

```stata
net install binsreg, from(https://raw.githubusercontent.com/nppackages/binsreg/master/stata) replace
which binsreg
help binsreg
```

Also available in R (`install.packages('binsreg')`) and Python (`pip install binsreg`).

---

## Core Syntax and Options

### binsreg (Main Command)

```stata
binsreg depvar xvar [controls] [if] [in] [weight] [, options]
```

**Binning Options:**
- `nbins(#)` - Number of bins (default: data-driven)
- `binspos(es|qs)` - Evenly-spaced or quantile-spaced bins
- `binsmethod(dpi|rot)` - Bin selection method (direct plug-in or rule-of-thumb)

**Polynomial Options (all take `(p v)` = polynomial degree, derivative order):**
- `dots(p v)` - Dots (use `dots(0,0)` for canonical binscatter)
- `line(p v)` - Smooth line connecting bins
- `ci(p v)` - Pointwise confidence intervals
- `cb(p v)` - Uniform confidence bands
- `polyreg(#)` - Global polynomial overlay of specified degree
- `deriv(#)` - Plot derivative of specified order

**Inference Options:**
- `level(#)` - Confidence level (default: 95)
- `vce(robust)` - Heteroskedasticity-robust
- `vce(cluster clustervar)` - Cluster-robust
- `vce(bootstrap, reps(#))` - Bootstrap (recommended for quantile regression)

**Covariate Options:**
- `at(mean|median|#)` - Evaluation point for control variables
- `absorb(varlist)` - Fixed effects to absorb

**Grouping Options:**
- `by(groupvar)` - Separate binscatter by group
- `bycolors(colorlist)` - Colors per group
- `bysymbols(symbollist)` - Symbols per group

**Output Options:**
- `saveplot(filename)` - Save graph (.png, .pdf, .gph)
- `savedata(filename)` - Save bin data for custom plotting
- `name(graphname, replace)` - Named graph for `graph combine`

Standard Stata graph options (`title()`, `xtitle()`, `ytitle()`, `legend()`, `scheme()`, etc.) all work.

---

## Covariate Adjustment (Critical Difference)

**WRONG -- traditional residualization approach (biased):**
```stata
* DON'T DO THIS
reg wage controls
predict wage_resid, resid
reg education controls
predict educ_resid, resid
binscatter wage_resid educ_resid
```

**CORRECT -- binsreg handles adjustment internally:**
```stata
* DO THIS -- estimates E[wage | education=x, controls=w0]
binsreg wage education controls
```

---

## Binary Outcomes: binslogit / binsprobit

```stata
binslogit depvar xvar [controls] [, nolink options]
binsprobit depvar xvar [controls] [, nolink options]
```

- `nolink` - Plot fitted probabilities instead of logit/probit index
- All other options same as `binsreg`

```stata
* Employment probability by age
binslogit employed age education, nolink ci(3,3)
binsprobit employed age education, nolink cb(3,3)
```

---

## Quantile Regression: binsqreg

```stata
binsqreg depvar xvar [controls] [, quantile(#) options]
```

- `quantile(#)` - Quantile to estimate (default: 0.5)
- Bootstrap recommended for inference: `vce(bootstrap, reps(100))`

```stata
binsqreg wage education, quantile(0.5) ci(3,3)
binsqreg wage education experience, quantile(0.75) ci(3,3) vce(bootstrap, reps(100))
```

---

## Hypothesis Testing: binstest

```stata
binstest depvar xvar [controls] [, test_options]
```

**Test Options:**
- `testmodelpoly(#)` - Test polynomial specification (1=linear, 2=quadratic, ...)
- `testshaper(#)` - Shape restriction: 0 for >= (increasing), 1 for <= (decreasing)
- `testshapel(#)` - Lower bound on derivative
- `deriv(#)` - Derivative order to test
- `lp(#|inf)` - Test metric (inf=supremum default, 2=L2, 1=L1)
- `estmethod(reg|logit|probit|qreg #)` - Estimation method

```stata
* Test linearity
binstest wage education, testmodelpoly(1)

* Test quadratic
binstest wage education, testmodelpoly(2)

* Test monotonicity (increasing)
binstest wage education, testshaper(0) deriv(1)

* Test concavity (decreasing returns)
binstest wage education, testshaper(1) deriv(2)

* Test with logit model
binstest employed age, estmethod(logit) testshaper(0) deriv(1)

* Test at specific quantile
binstest wage education, estmethod(qreg 0.5) testmodelpoly(1)
```

---

## Pairwise Comparison: binspwc

```stata
binspwc depvar xvar [controls], by(groupvar) [options]
```

- `by(groupvar)` - Required grouping variable
- `estmethod(method)` - Estimation method
- `pwc(#)` - Comparison type

```stata
binspwc wage education, by(gender)
binspwc wage education experience, by(union_status) vce(robust)
binspwc wage education, by(gender) estmethod(qreg 0.4)
```

---

## Bin Selection: binsregselect

```stata
binsregselect depvar xvar [controls] [, options]
```

- `binsmethod(dpi|rot)` - Selection method
- `binspos(es|qs)` - Bin positioning
- `pselect(# #)` - Range of polynomial degrees to search
- `sselect(# #)` - Range of smoothness degrees

```stata
binsregselect wage education
binsregselect wage education, binspos(es) pselect(1/4)
```

---

## Practical Examples

### Wage-Education Relationship

```stata
sysuse nlsw88, clear
rename grade education
rename ttl_exp experience

* Basic binscatter
binsreg wage education

* With controls, CI, and polynomial overlay
binsreg wage education experience age, ///
    dots(0,0) line(3,3) ci(3,3) polyreg(2) ///
    title("Wage-Education Relationship") ///
    xtitle("Years of Education") ytitle("Hourly Wage ($)")

* Test linearity
binstest wage education experience age, testmodelpoly(1)

* Test monotonicity
binstest wage education experience age, testshaper(0) deriv(1)
```

### Group Comparison

```stata
* Visual comparison by union status
binsreg wage education experience, ///
    by(union) dots(0,0) line(3,3) ci(3,3) ///
    legend(order(1 "Non-Union" 2 "Union"))

* Formal pairwise test
binspwc wage education experience, by(union) vce(robust)
```

### Binary Outcome

```stata
* Logit binscatter (probability scale)
binslogit employed age education, nolink ci(3,3) ///
    title("Employment Probability by Age") ytitle("Pr(Employed)")

* Test monotonicity
binstest employed age education, estmethod(logit) testshaper(1) deriv(1)
```

### Quantile Comparison

```stata
binsqreg wage education experience, quantile(0.25) name(q25, replace)
binsqreg wage education experience, quantile(0.75) name(q75, replace)
graph combine q25 q75, title("Wage Distribution by Education")

* Test linearity at multiple quantiles
foreach q in 0.25 0.5 0.75 {
    display "Testing linearity at quantile `q'"
    binstest wage education experience, estmethod(qreg `q') testmodelpoly(1)
}
```

### Specification Testing Workflow

```stata
* Step 1: Visualize with linear overlay
binsreg wage education experience age, ///
    line(3,3) cb(3,3) polyreg(1)

* Step 2: Test linearity
binstest wage education experience age, testmodelpoly(1)
local pval_linear = r(p_val)

* Step 3: If rejected, test quadratic
if `pval_linear' < 0.05 {
    binstest wage education experience age, testmodelpoly(2)
}

* Step 4: Test economic shape restrictions
binstest wage education experience age, testshaper(0) deriv(1)  // Increasing
binstest wage education experience age, testshaper(1) deriv(2)  // Concave
```

### Derivative Plot

```stata
* Marginal return to education
binsreg wage education, deriv(1) line(2,2) cb(2,2) ///
    title("Marginal Return to Education")
```

### Saved Data for Custom Plotting

```stata
binsreg wage education, savedata(bindata) replace
use bindata, clear
* Variables: bins_x, bins_fit, bins_ci_l, bins_ci_r, bins_cb_l, bins_cb_r
twoway (scatter bins_fit bins_x) ///
       (rcap bins_ci_l bins_ci_r bins_x), ///
       title("Custom Binscatter")
```

### Publication-Ready Plot

```stata
binsreg wage education experience age, ///
    nbins(20) dots(0,0) line(3,3) ///
    ci(3,3) cb(3,3) polyreg(2) ///
    title("Returns to Education", size(medium)) ///
    xtitle("Years of Education", size(small)) ///
    ytitle("Hourly Wage ($)", size(small)) ///
    note("95% CI and CB shown. Quadratic overlay.", size(vsmall)) ///
    graphregion(color(white)) scheme(s1color) ///
    saveplot("figure1_wage_education.pdf") replace
```

---

## Migration from Traditional binscatter

```stata
* OLD (binscatter):
binscatter wage education, nquantiles(20) ///
    controls(experience age) absorb(state)

* NEW (binsreg) -- with proper covariate adjustment and inference:
binsreg wage education experience age, ///
    nbins(20) binspos(qs) absorb(state) ci(3,3) cb(3,3)

* Or with automatic bin selection:
binsreg wage education experience age, absorb(state) ci(3,3)
```

| Feature | binscatter | binsreg |
|---------|------------|---------|
| Bin selection | Manual (`nquantiles`) | Automatic or manual (`nbins`) |
| Covariates | Residualization (`controls`) | Direct adjustment (listed after xvar) |
| Inference | None | CI/CB |
| Testing | Visual only | Formal tests (`binstest`) |
| Estimators | OLS only | OLS, logit, probit, quantile |

---

## References

**Cattaneo, M. D., Crump, R. K., Farrell, M. H., and Feng, Y. (2024).** "On Binscatter." *American Economic Review*, 114(5): 1488-1514.

**Cattaneo, M. D., Crump, R. K., Farrell, M. H., and Feng, Y. (2025).** "Binscatter Regressions." *The Stata Journal* (forthcoming). arXiv:2407.15276.

- Website: [https://nppackages.github.io/binsreg/](https://nppackages.github.io/binsreg/)
- GitHub: [https://github.com/nppackages/binsreg](https://github.com/nppackages/binsreg)
