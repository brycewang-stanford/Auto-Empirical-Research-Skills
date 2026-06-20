# rdrobust Suite: Regression Discontinuity Design Analysis

## Overview

The **rdrobust** suite (Calonico, Cattaneo, Titiunik) provides tools for RD estimation, bandwidth selection, visualization, and manipulation testing using local polynomial methods with robust bias-corrected inference.

### Suite Components

- **rdrobust**: RD treatment effect estimation with robust bias-corrected inference
- **rdbwselect**: MSE-optimal and CER-optimal bandwidth selection
- **rdplot**: RD plots with binned scatter plots and polynomial fits
- **rddensity**: Manipulation testing (McCrary-style) using local polynomial density estimation
- **rdlocrand**: Randomization inference for RD designs
- **rdmulti**: Multi-cutoff and multi-score RD designs
- **rdpower**: Power and sample size calculations for RD designs

---

## Installation

```stata
* Install all packages from SSC
ssc install rdrobust
ssc install rddensity
ssc install rdlocrand
ssc install rdmulti
ssc install rdpower

* Or from GitHub (development version)
net install rdrobust, from("https://raw.githubusercontent.com/rdpackages/rdrobust/master/stata") replace
net install rddensity, from("https://raw.githubusercontent.com/rdpackages/rddensity/master/stata") replace

* Verify
which rdrobust
```

---

## 1. rdrobust: RD Estimation with Robust Inference

### Syntax

```stata
rdrobust depvar runvar [if] [in] [, options]
```

### Main Options

| Option | Description |
|--------|-------------|
| `h(# [#])` | Main bandwidth (left [right]) |
| `b(# [#])` | Bias bandwidth |
| `rho(#)` | Ratio of bias to main bandwidth |
| `p(#)` | Polynomial order for estimation (default: 1) |
| `q(#)` | Polynomial order for bias estimation (default: p+1) |
| `deriv(#)` | Order of derivative to estimate (default: 0) |
| `bwselect(method)` | `mserd` (default, MSE-optimal), `msetwo`, `cerrd` (CER-optimal), `certwo`, plus `msesum`, `msecomb1/2`, `cersum`, `cercomb1/2` |
| `kernel(fn)` | `triangular` (default), `epanechnikov`, `uniform` |
| `covs(varlist)` | Covariates for adjustment |
| `covs_drop(on\|off)` | Drop collinear covariates |
| `fuzzy(treatvar)` | Treatment variable for fuzzy RD |
| `cluster(varname)` | Cluster variable for robust inference |
| `vce(type)` | `nn` (default), `hc0`, `hc1`, `hc2`, `hc3` |
| `nnmatch(#)` | Nearest neighbors for variance estimation |
| `level(#)` | Confidence level (default: 95) |
| `masspoints(check\|adjust\|off)` | Mass points handling |
| `all` | Report all bandwidth selectors |

### Basic Usage

```stata
* Simple sharp RD with automatic bandwidth
rdrobust outcome running_var

* Specify bandwidth manually
rdrobust outcome running_var, h(10)

* MSE-optimal (best for point estimation) vs CER-optimal (best for inference)
rdrobust outcome running_var, bwselect(mserd)
rdrobust outcome running_var, bwselect(cerrd)

* Two different bandwidths on each side
rdrobust outcome running_var, bwselect(msetwo)

* Different polynomial orders / kernels
rdrobust outcome running_var, p(2) q(3)
rdrobust outcome running_var, kernel(epanechnikov)
```

### Fuzzy RD Designs

```stata
* Fuzzy RD: treatment is discontinuous but not deterministic
rdrobust outcome running_var, fuzzy(treatment_var)

* First stage, reduced form, and IV estimate
rdrobust treatment_var running_var                     // First stage
rdrobust outcome running_var                           // Reduced form
rdrobust outcome running_var, fuzzy(treatment_var)     // IV/Fuzzy RD
```

### Covariate-Adjusted Estimation

```stata
rdrobust outcome running_var, covs(age income education)

* Check covariate balance at cutoff
foreach var of varlist age income education {
    rdrobust `var' running_var
}
```

### Cluster-Robust Inference

```stata
rdrobust outcome running_var, cluster(cluster_id)
rdrobust outcome running_var, covs(x1 x2) cluster(cluster_id)
```

### Extracting Results

```stata
rdrobust outcome running_var
ereturn list

local tau_bc = e(tau_bc)     // Bias-corrected estimate
local se_rb = e(se_tau_rb)   // Robust SE
local pval = e(pv_rb)        // Robust p-value
local ci_l = e(ci_l_rb)      // Robust CI lower
local ci_u = e(ci_r_rb)      // Robust CI upper
local bw = e(h_l)            // Bandwidth (left)
local N = e(N_h_l)           // N within bandwidth (left)
```

---

## 2. rdbwselect: Bandwidth Selection

### Syntax

```stata
rdbwselect depvar runvar [if] [in] [, options]
```

Options are the same as rdrobust bandwidth-related options. Use `all` to show all selectors.

### Usage

```stata
rdbwselect outcome running_var, all
matrix list r(bws)

* Extract specific bandwidths
local h_mse = r(h_mserd)
local h_cer = r(h_cerrd)

* Feed into rdrobust
rdrobust outcome running_var, h(`h_mse')
```

---

## 3. rdplot: RD Visualization

### Syntax

```stata
rdplot depvar runvar [if] [in] [, options]
```

### Main Options

| Option | Description |
|--------|-------------|
| `nbins(# [#])` | Number of bins (left [right]) |
| `binselect(method)` | `esmv` (default), `espr`, `esmvpr`, `qsmv`, `qspr`, `qsmvpr` |
| `p(#)` | Polynomial order (default: 4) |
| `h(# [#])` | Bandwidth for local polynomial fit |
| `ci(#)` | Confidence level for plot |
| `shade` | Shade confidence region |
| `covs(varlist)` | Covariates for residualized plot |
| `hide` | Hide scatter points (show only fit) |
| `support(# [#])` | Lower/upper bounds for support |
| `graph_options(string)` | Pass-through Stata graph options |

### Examples

```stata
* Basic RD plot with CI
rdplot outcome running_var, ci(95) shade

* Custom bins and polynomial
rdplot outcome running_var, nbins(15 25) binselect(qsmv) p(2)

* Publication-quality
rdplot outcome running_var, ci(95) shade nbins(20) p(4) ///
    graph_options( ///
        title("Regression Discontinuity Plot") ///
        xtitle("Running Variable") ytitle("Outcome") ///
        graphregion(color(white)) bgcolor(white) legend(off) ///
    )

* Use bandwidth from rdrobust
rdrobust outcome running_var
local h = e(h_l)
rdplot outcome running_var, h(`h') kernel(triangular)

* Export
graph export "rd_plot.png", replace width(2400) height(1800)
```

---

## 4. rddensity: Manipulation Testing

Tests whether the density of the running variable is continuous at the cutoff (McCrary-style test). Rejection suggests agents may be manipulating the running variable to sort around the threshold.

### Syntax

```stata
rddensity runvar [if] [in] [, options]
```

### Options

| Option | Description |
|--------|-------------|
| `c(#)` | RD cutoff (default: 0) |
| `p(#)` | Polynomial order (default: 2) |
| `q(#)` | Bias correction order (default: p+1) |
| `fitselect(method)` | `unrestricted` (default) or `restricted` |
| `h(# [#])` | Bandwidth (left [right]) |
| `bwselect(method)` | `each`, `diff`, `sum`, `comb` |

### Usage

```stata
rddensity running_var
* p-value < 0.05 => evidence of manipulation

* Store results
local T_stat = r(T)
local pvalue = r(pv)

* Plot density discontinuity
rdplotdensity rddensity running_var, ///
    graph_options( ///
        title("Density Test for Manipulation") ///
        xtitle("Running Variable") ytitle("Density") ///
        graphregion(color(white)) ///
    )
```

---

## 5. rdlocrand: Randomization Inference

Implements randomization inference for RD designs under local randomization assumptions (useful when bandwidth is very small and observations near the cutoff can be treated as near-random).

### Syntax

```stata
rdlocrand depvar runvar [if] [in] [, options]
```

### Key Options

- `wl(#)` / `wr(#)`: Left/right window length
- `cutoff(#)`: RD cutoff (default: 0)
- `reps(#)`: Randomization replications (default: 1000)
- `seed(#)`: Random seed
- `stat(statistic)`: `diffmeans` (default), `ksmirnov`, `ranksum`

### Usage

```stata
* Window selection
rdwinselect running_var, wmin(0.5) wstep(0.5) nwindows(20)
local wl_opt = r(wl_opt)
local wr_opt = r(wr_opt)

* Randomization inference
rdlocrand outcome running_var, wl(`wl_opt') wr(`wr_opt') reps(5000) seed(12345)

* Binomial test for discrete outcomes
rdbinomial outcome running_var, wl(5) wr(5)
```

---

## 6. rdmulti: Multi-Cutoff and Multi-Score RD

### Multi-Cutoff RD

```stata
rdmc depvar runvar [if] [in], c(numlist) [options]

* Example: three cutoffs
rdmc outcome running_var, c(0 50 100)
rdmc outcome running_var, c(0 50 100) covs(x1 x2 x3)
rdmc outcome running_var, c(0 50 100) pooled_opt(p(1) kernel(triangular))

* Plot
rdmcplot outcome running_var, c(0 50 100) ci(95) shade
```

### Multi-Score RD

```stata
rdms depvar runvar1 runvar2 [if] [in], c1(#) c2(#) [options]

* Two-dimensional RD
rdms outcome score1 score2, c1(50) c2(60)
rdms outcome score1 score2, c1(50) c2(60) range1(30 70) range2(40 80)
```

---

## 7. Complete RD Workflow

### Step 1: Data Preparation

```stata
use "rd_data.dta", clear
gen running_var = test_score - 50  // Center at cutoff
gen treatment = (running_var >= 0)
bysort treatment: summarize outcome running_var
```

### Step 2: Visual Inspection

```stata
rdplot outcome running_var, c(0) ci(95) shade nbins(20) p(4) ///
    graph_options(title("RD Plot") graphregion(color(white)) legend(off))
```

### Step 3: Manipulation Testing

```stata
rddensity running_var, c(0)
local mccrary_pval = r(pv)

rdplotdensity rddensity running_var, ///
    graph_options(title("Density Test") subtitle("p = `: display %5.3f `mccrary_pval''"))
```

### Step 4: Covariate Balance

```stata
local covariates "age female education income"
foreach var of local covariates {
    quietly rdrobust `var' running_var, c(0)
    display "`var'" _col(20) %8.4f e(tau_bc) _col(35) %8.4f e(se_tau_rb) _col(50) %6.4f e(pv_rb)
}
* p-values should be > 0.05 for balanced covariates
```

### Step 5: Bandwidth Selection

```stata
rdbwselect outcome running_var, c(0) all
local h_mse = r(h_mserd)
local h_cer = r(h_cerrd)
matrix list r(bws)
```

### Step 6: Main Estimation

```stata
* MSE-optimal (point estimation)
rdrobust outcome running_var, c(0) p(1) bwselect(mserd)
estimates store rd_mse

* CER-optimal (preferred for inference)
rdrobust outcome running_var, c(0) p(1) bwselect(cerrd)
estimates store rd_cer

* With covariates
rdrobust outcome running_var, c(0) p(1) covs(age female education income)
estimates store rd_cov

estimates table rd_mse rd_cer rd_cov, ///
    b(%9.3f) se(%9.3f) stats(N N_h_l N_h_r h_l h_r)
```

### Step 7: Sensitivity Analysis

```stata
* Bandwidth sensitivity
local bw_multipliers "0.5 0.75 1 1.25 1.5"
foreach mult of local bw_multipliers {
    local h_test = `h_mse' * `mult'
    quietly rdrobust outcome running_var, h(`h_test')
    display "BW x " %4.2f `mult' _col(20) "Est: " %8.4f e(tau_bc) _col(40) "SE: " %8.4f e(se_tau_rb)
}

* Polynomial order sensitivity
forvalues p = 1/4 {
    quietly rdrobust outcome running_var, p(`p')
    display "p = `p'" _col(20) "Est: " %8.4f e(tau_bc) _col(40) "SE: " %8.4f e(se_tau_rb)
}

* Donut hole (exclude obs very close to cutoff)
foreach hole in 0 0.5 1 2 {
    quietly rdrobust outcome running_var if abs(running_var) >= `hole'
    display "Hole = `hole'" _col(20) "Est: " %8.4f e(tau_bc) _col(40) "SE: " %8.4f e(se_tau_rb)
}
```

### Step 8: Placebo Tests

```stata
* Placebo cutoffs (should show no effect)
foreach c in -10 -5 5 10 {
    quietly rdrobust outcome running_var if running_var < 0, c(`c')
    display "Cutoff = `c'" _col(20) "Est: " %8.4f e(tau_bc) _col(40) "p: " %6.4f e(pv_rb)
}

* Placebo outcomes (pre-treatment vars should show no effect)
foreach var in age education {
    quietly rdrobust `var' running_var
    display "`var'" _col(20) "Est: " %8.4f e(tau_bc) _col(40) "p: " %6.4f e(pv_rb)
}
```

### Step 9: Fuzzy RD (if applicable)

```stata
* First stage
rdrobust treatment_received running_var
local first_stage = e(tau_bc)
local first_stage_F = (e(tau_bc)/e(se_tau_rb))^2

* Reduced form (ITT)
rdrobust outcome running_var

* Fuzzy RD (LATE)
rdrobust outcome running_var, fuzzy(treatment_received)
```

---

## Common Issues and Solutions

**Insufficient observations within bandwidth:**
```stata
histogram running_var, width(1) freq   // Check data density
rdrobust outcome running_var, h(20)    // Try larger bandwidth
```

**Mass points warning:**
```stata
rdrobust outcome running_var, masspoints(adjust)
```

**Different left/right bandwidths:**
```stata
rdrobust outcome running_var, h(10 15)  // h_left=10, h_right=15
```

**Clustering with few clusters:**
```stata
rdrobust outcome running_var, cluster(cluster_id)
* Rule of thumb: need at least 20-30 clusters
```

---

## Quick Reference

```stata
rdrobust outcome running_var                          // Basic sharp RD
rdrobust outcome running_var, h(10)                   // Manual bandwidth
rdrobust outcome running_var, covs(x1 x2 x3)         // With covariates
rdrobust outcome running_var, fuzzy(treatment_var)    // Fuzzy RD
rdbwselect outcome running_var                        // Select bandwidth
rdplot outcome running_var, ci(95) shade              // RD plot
rddensity running_var                                 // Manipulation test
rdlocrand outcome running_var, wl(5) wr(5)            // Randomization inference
rdmc outcome running_var, c(0 50 100)                 // Multi-cutoff
```

### Key Options

- `p(#)`: Polynomial order (default: 1)
- `bwselect()`: `mserd` (MSE-optimal) or `cerrd` (CER-optimal)
- `kernel()`: `triangular`, `epanechnikov`, `uniform`
- `cluster()`: Cluster-robust SE
- `covs()`: Covariate adjustment
- `fuzzy()`: Fuzzy RD treatment variable

---

### References

- Calonico, Cattaneo, & Titiunik (2014). "Robust Nonparametric Confidence Intervals for RD Designs." *Econometrica*.
- Cattaneo, Jansson, & Ma (2020). "Simple Local Polynomial Density Estimators." *JASA*.
- **rdpackages website**: [https://rdpackages.github.io](https://rdpackages.github.io)
