# nprobust: Nonparametric Kernel-Based Estimation and Robust Bias-Corrected Inference

## Overview

**nprobust** provides kernel density estimation and local polynomial regression with robust bias-corrected confidence intervals and automatic bandwidth selection.

"Robust bias-corrected" means the package addresses coverage distortions that arise when standard bias-correction is used -- conventional bias-corrected CIs can have incorrect coverage; nprobust fixes this.

### Main Commands

1. **kdrobust** - Kernel density estimation with robust inference
2. **kdbwselect** - Bandwidth selection for kernel density estimation
3. **lprobust** - Local polynomial regression with robust inference
4. **lpbwselect** - Bandwidth selection for local polynomial regression

## Installation

```stata
net install nprobust, from(https://raw.githubusercontent.com/nppackages/nprobust/master/stata) replace
```

---

## kdrobust: Kernel Density Estimation

### Syntax

```stata
kdrobust varname [if] [in] [, options]
```

### Key Options

| Option | Description | Default |
|--------|-------------|---------|
| `eval(varname)` | Custom evaluation points | 30 quantile-spaced |
| `neval(#)` | Number of evaluation points | 30 |
| `h(varname\|#)` | Main bandwidth | Data-driven |
| `b(varname\|#)` | Bias correction bandwidth | Data-driven |
| `kernel(type)` | `epanechnikov`, `triangular`, `uniform` | epanechnikov |
| `bwselect(method)` | Bandwidth selection method | mse-dpi (single), imse-dpi (multiple) |
| `level(#)` | Confidence level | 95 |
| `genvars` | Generate result variables (prefix: `kdrobust_`) | -- |
| `plot` | Produce density plot with CIs | -- |
| `graph_options(string)` | Pass options to twoway graph | -- |

### Generated Variables (with genvars)

- `kdrobust_eval` - Evaluation points
- `kdrobust_h`, `kdrobust_b` - Main and bias bandwidths
- `kdrobust_f_us` - Conventional density estimate
- `kdrobust_f_bc` - Bias-corrected density estimate
- `kdrobust_se_us`, `kdrobust_se_rb` - Conventional and robust SEs
- `kdrobust_CI_l_rb`, `kdrobust_CI_r_rb` - Robust CI bounds

### Examples

```stata
sysuse auto, clear

// Basic estimation
kdrobust price

// With plot
kdrobust price, plot graph_options(title("Price Distribution") ///
    xtitle("Price") ytitle("Density"))

// Custom evaluation grid with saved results
summarize price
range price_grid `r(min)' `r(max)' 50
kdrobust price, eval(price_grid) genvars

// Custom visualization from saved results
twoway (line kdrobust_f_bc kdrobust_eval, lcolor(navy)) ///
       (rarea kdrobust_CI_l_rb kdrobust_CI_r_rb kdrobust_eval, ///
        fcolor(navy%20) lcolor(none)), ///
       legend(order(1 "Density" 2 "95% CI"))

// Compare kernels
kdrobust price, kernel(epanechnikov) genvars
rename kdrobust_f_bc f_epa
kdrobust price, kernel(triangular) genvars
rename kdrobust_f_bc f_tri

// Compare all bandwidth methods
kdrobust price, bwselect(all)
```

---

## kdbwselect: Bandwidth Selection for Density

### Syntax

```stata
kdbwselect varname [if] [in] [, eval() neval() kernel() bwselect()]
```

### Example

```stata
sysuse auto, clear

kdbwselect price
matrix list e(bws)   // h and b for each evaluation point

// Compare all methods
kdbwselect price, bwselect(all)

// Use selected bandwidth in kdrobust
kdbwselect price, bwselect(mse-dpi)
matrix bw_result = e(bws)
local h_opt = bw_result[1,1]
kdrobust price, h(`h_opt')
```

---

## lprobust: Local Polynomial Regression

### Syntax

```stata
lprobust depvar indepvar [if] [in] [, options]
```

### Key Options

| Option | Description | Default |
|--------|-------------|---------|
| `p(#)` | Polynomial order | 1 (local linear) |
| `q(#)` | Bias correction polynomial order | p+1 |
| `deriv(#)` | Derivative order to estimate | 0 (the function) |
| `eval(varname)` | Custom evaluation points | 30 quantile-spaced |
| `neval(#)` | Number of evaluation points | 30 |
| `h(varname\|#)` | Main bandwidth | Data-driven |
| `b(varname\|#)` | Bias correction bandwidth | Data-driven |
| `kernel(type)` | `epanechnikov`, `triangular`, `uniform` | epanechnikov |
| `bwselect(method)` | Bandwidth selection method | mse-dpi / imse-dpi |
| `vce(type)` | Variance estimator | nn |
| `level(#)` | Confidence level | 95 |
| `interior` | Interior points only | -- |
| `genvars` | Generate result variables (prefix: `lprobust_`) | -- |
| `plot` | Create visualization | -- |

### VCE Options

| VCE Type | Description |
|----------|-------------|
| `nn` | Nearest neighbor heteroskedasticity-robust (default) |
| `hc0`-`hc3` | HC variance estimators (`hc3` most conservative) |
| `cluster clustvar` | Cluster-robust |
| `nncluster clustvar` | Nearest neighbor cluster-robust |

### Generated Variables (with genvars)

- `lprobust_eval` - Evaluation points
- `lprobust_h`, `lprobust_b` - Bandwidths
- `lprobust_N` - Effective sample size
- `lprobust_tau_us`, `lprobust_tau_bc` - Conventional and bias-corrected estimates
- `lprobust_se_us`, `lprobust_se_rb` - Conventional and robust SEs
- `lprobust_CI_l_rb`, `lprobust_CI_r_rb` - Robust CI bounds

### Examples

```stata
sysuse auto, clear

// Basic local linear regression
lprobust mpg weight
lprobust mpg weight, genvars plot

// Custom evaluation grid
summarize weight
range weight_grid `r(min)' `r(max)' 50
lprobust mpg weight, eval(weight_grid) plot ///
    graph_options(title("MPG vs Weight") xtitle("Weight") ytitle("MPG"))

// Higher-order polynomials
lprobust mpg weight, p(1) genvars    // local linear
rename lprobust_tau_bc fit_p1
lprobust mpg weight, p(2) genvars    // local quadratic
rename lprobust_tau_bc fit_p2

// Estimating derivatives
lprobust mpg weight, deriv(0) genvars   // function
lprobust mpg weight, deriv(1) genvars   // first derivative (slope)

// Cluster-robust inference
lprobust y x, vce(cluster cluster_id)

// Coverage error optimal bandwidth (better for inference)
lprobust mpg weight, bwselect(ce-dpi)
```

### Custom Visualization

```stata
sysuse auto, clear
lprobust mpg weight, genvars

twoway (scatter mpg weight, mcolor(gs12) msize(vsmall)) ///
       (line lprobust_tau_bc lprobust_eval, lcolor(navy) lwidth(medium)) ///
       (rarea lprobust_CI_l_rb lprobust_CI_r_rb lprobust_eval, ///
        fcolor(navy%15) lwidth(none)), ///
       legend(order(1 "Data" 2 "Fit" 3 "95% CI"))
```

### Comparing Subgroup Fits

```stata
sysuse auto, clear

lprobust mpg weight if foreign==0, genvars
rename lprobust_tau_bc fit_domestic
rename lprobust_eval eval_domestic

lprobust mpg weight if foreign==1, genvars
rename lprobust_tau_bc fit_foreign
rename lprobust_eval eval_foreign

twoway (line fit_domestic eval_domestic, lcolor(navy)) ///
       (line fit_foreign eval_foreign, lcolor(maroon)), ///
       legend(order(1 "Domestic" 2 "Foreign"))
```

---

## lpbwselect: Bandwidth Selection for Local Polynomial

### Syntax

```stata
lpbwselect depvar indepvar [if] [in] [, p() deriv() eval() neval() kernel() bwselect() vce()]
```

### Example

```stata
sysuse auto, clear

lpbwselect mpg weight
matrix list e(Result)

// All methods
lpbwselect mpg weight, bwselect(all)

// Derivative estimation needs different bandwidth
lpbwselect mpg weight, deriv(0)
lpbwselect mpg weight, deriv(1)   // typically larger bandwidth

// Use in lprobust
lpbwselect mpg weight, bwselect(ce-dpi)
matrix bw_result = e(Result)
local h_opt = bw_result[1,2]
local b_opt = bw_result[1,3]
lprobust mpg weight, h(`h_opt') b(`b_opt')
```

---

## Bandwidth Selection Methods

| Method | Full Name | Use Case |
|--------|-----------|----------|
| `mse-dpi` | MSE-optimal, direct plug-in | Point estimation accuracy (default single-point) |
| `imse-dpi` | Integrated MSE-optimal, DPI | Curve estimation (default multi-point) |
| `mse-rot` | MSE-optimal, rule-of-thumb | Faster approximation |
| `imse-rot` | Integrated MSE-optimal, ROT | Faster approximation |
| `ce-dpi` | Coverage error optimal, DPI | When inference/CIs are primary goal |
| `ce-rot` | Coverage error optimal, ROT | Inference, faster |

**Rule of thumb**: Use `ce-dpi` when you care about CI coverage; use `mse-dpi`/`imse-dpi` when you care about point estimate accuracy. CE bandwidths are typically larger.

```stata
// Compare methods
lpbwselect mpg weight, bwselect(all)
// Generally: h_mse <= h_imse <= h_ce
```

---

## Common Use Cases

### Non-Linear Relationships (vs Parametric)

```stata
webuse nlswork, clear

// Non-parametric age-wage profile
lprobust ln_wage age, genvars

// Compare to quadratic
gen age2 = age^2
reg ln_wage age age2
predict wage_quad

twoway (line lprobust_tau_bc lprobust_eval, lcolor(navy)) ///
       (line wage_quad age, sort lcolor(maroon) lpattern(dash)), ///
       legend(order(1 "Non-parametric" 2 "Quadratic"))
```

### Regression Discontinuity Visualization

```stata
// Non-parametric fit on each side of cutoff
lprobust y x if x < 0, genvars
rename lprobust_tau_bc fit_left
rename lprobust_eval eval_left

lprobust y x if x >= 0, genvars
rename lprobust_tau_bc fit_right
rename lprobust_eval eval_right

twoway (scatter y x, msize(tiny) mcolor(gs12)) ///
       (line fit_left eval_left, lcolor(navy)) ///
       (line fit_right eval_right, lcolor(navy)), ///
       xline(0, lpattern(dash)) legend(off)
```

### Heterogeneous Treatment Effects

```stata
// Estimate conditional means for treated and control
lprobust y x if treatment==1, genvars
rename lprobust_tau_bc y1_fit
rename lprobust_eval x_grid

lprobust y x if treatment==0, genvars
rename lprobust_tau_bc y0_fit

// Treatment effect function
gen te_estimate = y1_fit - y0_fit
line te_estimate x_grid
```

### Distribution Comparison

```stata
sysuse auto, clear

kdrobust price if foreign==0, eval(grid) genvars
rename kdrobust_f_bc density_domestic
rename kdrobust_se_rb se_domestic

kdrobust price if foreign==1, eval(grid) genvars
rename kdrobust_f_bc density_foreign
rename kdrobust_se_rb se_foreign

gen density_diff = density_foreign - density_domestic
gen se_diff = sqrt(se_domestic^2 + se_foreign^2)
gen ci_lower = density_diff - 1.96*se_diff
gen ci_upper = density_diff + 1.96*se_diff

twoway (rarea ci_lower ci_upper kdrobust_eval, fcolor(gs14) lwidth(none)) ///
       (line density_diff kdrobust_eval, lcolor(navy)) ///
       (function y = 0, range(kdrobust_eval) lpattern(dash)), ///
       legend(order(2 "Difference" 1 "95% CI"))
```

### Covariate-Adjusted (Partial Linear Model)

```stata
sysuse auto, clear

// Partial out covariates from both Y and X
reg mpg foreign rep78
predict mpg_resid, residuals
reg weight foreign rep78
predict weight_resid, residuals

// Non-parametric regression on residuals
lprobust mpg_resid weight_resid, plot
```

---

## Troubleshooting

**Insufficient observations near evaluation point:**
```stata
lprobust y x, neval(20)         // fewer eval points
lprobust y x, interior          // interior points only
// Or manually increase bandwidth
lpbwselect y x
local h_opt = e(Result)[1,2]
lprobust y x, h(`=1.5*`h_opt'')
```

**Erratic estimates near boundaries:**
```stata
lprobust y x, kernel(triangular)   // better boundary properties
lprobust y x, interior             // drop boundary points
// Or trim to interior
summarize x
lprobust y x if x >= `r(p5)' & x <= `r(p95)'
```

**Slow with large N:**
```stata
lprobust y x, neval(20)            // fewer evaluation points
lprobust y x, bwselect(imse-rot)   // ROT faster than DPI
```

**MSE vs CE bandwidth choice:**
- Use `ce-dpi` for inference (hypothesis tests, CIs)
- Use `mse-dpi` for prediction accuracy

---

## Stored Results

After `kdrobust` or `lprobust`:

| Result | Description |
|--------|-------------|
| `e(N)` | Number of observations |
| `e(h)` | Main bandwidth |
| `e(b)` | Bias bandwidth |
| `e(level)` | Confidence level |
| `e(Result)` | Complete results matrix |
| `e(bws)` | Bandwidth information |
| `e(bwselect)` | BW selection method used |
| `e(vce)` | Variance estimator used |

## Quick Reference

```stata
// Kernel density
kdrobust varname [if] [in] [, eval() h() b() kernel() bwselect() level() plot genvars]

// Density bandwidth selection
kdbwselect varname [if] [in] [, eval() kernel() bwselect()]

// Local polynomial regression
lprobust depvar indepvar [if] [in] [, eval() p() deriv() h() b() kernel() ///
    bwselect() vce() level() plot genvars]

// LP bandwidth selection
lpbwselect depvar indepvar [if] [in] [, eval() p() deriv() kernel() bwselect() vce()]
```

## References

- Calonico, Cattaneo, & Farrell (2019). "nprobust: Nonparametric Kernel-Based Estimation and Robust Bias-Corrected Inference." *Journal of Statistical Software*, 91(8).
- Package website: https://nppackages.github.io/nprobust/
- Related: `rdrobust` (RD designs), `lpdensity` (local polynomial density)
