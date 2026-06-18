# Nonparametric Methods in Stata

## Table of Contents
- [Kernel Density Estimation](#kernel-density-estimation)
- [Nonparametric Tests for Paired Data](#nonparametric-tests-for-paired-data)
- [Nonparametric Tests for Independent Samples](#nonparametric-tests-for-independent-samples)
- [Nonparametric Correlations](#nonparametric-correlations)
- [Lowess Smoothing](#lowess-smoothing)
- [Nonparametric Regression](#nonparametric-regression)
- [Bootstrap Methods](#bootstrap-methods)
- [Quantile Regression](#quantile-regression)
- [Median Tests](#median-tests)
- [Quick Reference](#quick-reference)

---

## Kernel Density Estimation

### kdensity Command

```stata
kdensity varname [if] [in] [weight] [, options]
```

**Key Options:**
- `kernel(kernel)` - epanechnikov (default), gaussian, biweight, cosine, parzen, rectangle, triangle
- `bwidth(#)` - Bandwidth (smoothing parameter); Stata default is usually good
- `n(#)` - Number of evaluation points (default 300)
- `generate(newvar)` - Save density estimates
- `normal` - Overlay normal density
- `nograph` - Suppress graph

**Examples:**
```stata
sysuse auto, clear
kdensity price                       // Basic density plot
kdensity price, normal               // Compare to normal
kdensity price, kernel(gaussian)     // Gaussian kernel
kdensity price, bwidth(500)          // Narrower bandwidth (less smooth)
kdensity price, bwidth(2000)         // Wider bandwidth (more smooth)
```

**Save and plot density estimates:**
```stata
kdensity price, generate(x_price density_price) nograph
twoway line density_price x_price, title("Price Distribution")
```

**Compare distributions by groups:**
```stata
kdensity price if foreign==0, generate(x_dom d_dom) nograph
kdensity price if foreign==1, generate(x_for d_for) nograph
twoway (line d_dom x_dom, lcolor(blue)) ///
       (line d_for x_for, lcolor(red)), ///
    legend(label(1 "Domestic") label(2 "Foreign"))
```

**Overlay histogram with density and normal curve:**
```stata
histogram price, kdensity normal
```

---

## Nonparametric Tests for Paired Data

### Wilcoxon Signed-Rank Test (signrank)

Nonparametric alternative to the paired t-test. Tests whether median of differences is zero.

```stata
signrank varname = exp [if] [in]
```

```stata
webuse fuel, clear
signrank mpg1 = mpg2            // Test paired difference

// Equivalent: create difference first
generate diff = mpg1 - mpg2
signrank diff = 0

// Test if median equals a specific value
signrank price = 6000
```

### Sign Test (signtest)

Simpler than signrank -- only uses the sign of differences (not magnitudes).

```stata
signtest varname = exp [if] [in]
```

```stata
webuse fuel, clear
signtest mpg1 = mpg2
```

---

## Nonparametric Tests for Independent Samples

### Wilcoxon Rank-Sum / Mann-Whitney U Test (ranksum)

Nonparametric alternative to the two-sample t-test.

```stata
ranksum varname [if] [in], by(groupvar) [porder]
```

- `porder` - Reports P(observation from group 1 > observation from group 2)

```stata
sysuse auto, clear
ranksum price, by(foreign)
ranksum mpg, by(foreign) porder
```

### Kruskal-Wallis Test (kwallis)

Nonparametric alternative to one-way ANOVA (extends rank-sum to 3+ groups).

```stata
kwallis varname [if] [in], by(groupvar)
```

```stata
sysuse auto, clear
kwallis price, by(rep78)

// Post-hoc pairwise comparisons (user-written)
// ssc install dunntest
// dunntest price, by(rep78)
```

---

## Nonparametric Correlations

### Spearman's Rank Correlation

```stata
spearman varlist [if] [in] [, options]
```

**Options:** `stats(rho obs p)`, `star(#)`, `bonferroni`, `sidak`, `pw`, `print(#)`, `matrix`

```stata
sysuse auto, clear
spearman price mpg                           // Bivariate
spearman price mpg weight length, star(0.05) matrix  // Matrix with stars
spearman price mpg weight length, pw star(0.05)      // Pairwise
```

### Kendall's Tau

Often more robust than Spearman's, especially with small samples or many tied ranks.

```stata
ktau varlist [if] [in] [, options]
```

```stata
ktau price mpg
ktau price mpg weight length
```

---

## Lowess Smoothing

```stata
lowess yvar xvar [if] [in] [, options]
```

**Key Options:**
- `bwidth(#)` - Bandwidth 0 to 1 (default 0.8); smaller = less smooth
- `mean` - Running-mean smooth instead of running-line
- `generate(newvar)` - Save smoothed values
- `nograph` - Suppress graph

```stata
sysuse auto, clear
lowess mpg weight                          // Basic
lowess mpg weight, bwidth(0.3)             // Less smooth
lowess mpg weight, bwidth(0.9)             // More smooth
lowess mpg weight, generate(mpg_smooth) nograph  // Save values
```

**Custom plot with lowess overlay:**
```stata
twoway (scatter mpg weight, msize(small) mcolor(gs10)) ///
       (line mpg_smooth weight, lcolor(red)), ///
    legend(label(1 "Observed") label(2 "Lowess smooth"))
```

---

## Nonparametric Regression

### Local Polynomial Regression (lpoly)

```stata
lpoly yvar xvar [if] [in] [weight] [, options]
```

**Key Options:**
- `degree(#)` - Polynomial degree (0, 1, 2, 3; default 0)
- `kernel(kernel)` - Kernel function
- `bwidth(#)` - Bandwidth
- `generate(newvar_y newvar_x)` - Save fitted values
- `ci` - Add confidence interval

```stata
sysuse auto, clear
lpoly mpg weight                              // Basic
lpoly mpg weight, ci                          // With confidence interval
lpoly mpg weight, degree(1) title("Local Linear")   // Local linear
lpoly mpg weight, degree(2) title("Local Quadratic") // Local quadratic

// Save fitted values
lpoly mpg weight, degree(1) generate(mpg_fit weight_fit) nograph
```

### npregress (Formal Nonparametric Regression)

Provides nonparametric regression with formal inference and automatic bandwidth selection.

```stata
npregress kernel depvar indepvars [if] [in] [, options]
```

- `estimator(mean|gradient)` - Local constant or local linear

```stata
sysuse auto, clear
npregress kernel mpg weight
predict mpg_np

// Multivariate
npregress kernel mpg weight length
margins, dydx(weight length)       // Marginal effects
```

---

## Bootstrap Methods

### Bootstrap Estimation

```stata
bootstrap [exp_list] [, options] : command
```

**Key Options:**
- `reps(#)` - Replications (default 50; use 500-1000 for analysis, 5000+ for publication)
- `seed(#)` - Random seed for reproducibility
- `saving(filename)` - Save bootstrap dataset
- `size(#)` - Bootstrap sample size
- `cluster(varlist)` - Cluster bootstrap
- `strata(varlist)` - Stratified bootstrap
- `bca` / `percentile` / `normal` - CI type

```stata
sysuse auto, clear

// Bootstrap mean
bootstrap r(mean), reps(1000) seed(12345): summarize price

// Bootstrap regression
bootstrap, reps(1000) seed(12345): regress mpg weight length

// Percentile CIs
bootstrap r(mean), reps(1000) seed(12345) percentile: summarize price

// Bootstrap correlation
bootstrap r(rho), reps(1000) seed(12345): spearman price mpg
```

**Cluster and stratified bootstrap:**
```stata
// Cluster bootstrap
bootstrap, reps(500) seed(12345) cluster(idcode): regress ln_wage age tenure

// Stratified bootstrap
bootstrap, reps(1000) seed(12345) strata(foreign): regress mpg weight
```

**Bootstrap for custom statistics:**
```stata
program define median_stat, rclass
    summarize price, detail
    return scalar median = r(p50)
end
bootstrap r(median), reps(1000) seed(12345): median_stat
```

**Save and examine bootstrap distribution:**
```stata
bootstrap r(mean), reps(1000) seed(12345) saving(boot_means): summarize price
use boot_means, clear
histogram _bs_1, normal title("Bootstrap Distribution of Mean Price")
```

### Jackknife Estimation

```stata
jackknife [exp_list] [, options] : command
```

```stata
sysuse auto, clear
jackknife: regress mpg weight length
```

---

## Quantile Regression

### Basic Quantile Regression (qreg)

```stata
qreg depvar indepvars [if] [in] [weight] [, quantile(#) vce(vcetype)]
```

- `quantile(#)` - Default 0.5 (median); range 0-1
- `vce(robust)` or `vce(bootstrap)`

```stata
sysuse auto, clear
qreg price mpg weight                        // Median regression
qreg price mpg weight, quantile(0.25)        // 25th percentile
qreg price mpg weight, quantile(0.75)        // 75th percentile
qreg price mpg weight, vce(robust)           // Robust SEs
```

### Bootstrap Quantile Regression (bsqreg)

Automatically uses bootstrap for standard errors.

```stata
bsqreg depvar indepvars [, quantile(#) reps(#)]
```

```stata
bsqreg price mpg weight, quantile(0.25) reps(500)
```

### Simultaneous Quantile Regression (sqreg)

Estimates multiple quantiles simultaneously; enables cross-quantile coefficient tests.

```stata
sqreg depvar indepvars [, quantiles(numlist) reps(#)]
```

```stata
sqreg price mpg weight, quantiles(0.1 0.25 0.5 0.75 0.9) reps(100)

// Test if coefficient is same across quantiles
test [q25]mpg = [q50]mpg
test [q25]mpg = [q50]mpg = [q75]mpg
```

### Visualizing Quantile Regression

**Plot predicted lines at multiple quantiles:**
```stata
sysuse auto, clear

// Estimate at each quantile and store coefficients
foreach q in 10 25 50 75 90 {
    qreg price weight, quantile(`q'/100) vce(robust)
    matrix b`q' = e(b)
    generate pred_`q' = b`q'[1,2] + b`q'[1,1] * weight
}
regress price weight
predict pred_ols

sort weight
twoway (scatter price weight, msize(small) mcolor(gs12)) ///
       (line pred_10 weight, lcolor(blue) lpattern(dash)) ///
       (line pred_25 weight, lcolor(blue)) ///
       (line pred_50 weight, lcolor(red) lwidth(medium)) ///
       (line pred_75 weight, lcolor(blue)) ///
       (line pred_90 weight, lcolor(blue) lpattern(dash)) ///
       (line pred_ols weight, lcolor(green) lpattern(shortdash)), ///
    legend(label(1 "Data") label(2 "Q10") label(3 "Q25") ///
           label(4 "Q50") label(5 "Q75") label(6 "Q90") label(7 "OLS"))
```

---

## Median Tests

```stata
median varname [if] [in], by(groupvar) [continuity] [exact] [medianties(below|above|drop|split)]
```

```stata
sysuse auto, clear
median price, by(foreign)
median mpg, by(foreign) continuity
```

---

## Quick Reference

### Parametric vs Nonparametric Equivalents

| Parametric | Nonparametric | Stata Commands |
|---|---|---|
| Paired t-test | Wilcoxon signed-rank | `ttest x = y` vs `signrank x = y` |
| Two-sample t-test | Mann-Whitney / Rank-sum | `ttest x, by(g)` vs `ranksum x, by(g)` |
| One-way ANOVA | Kruskal-Wallis | `oneway x g` vs `kwallis x, by(g)` |
| Pearson correlation | Spearman / Kendall | `pwcorr` vs `spearman` / `ktau` |
| OLS regression | Quantile regression | `regress y x` vs `qreg y x` |
| Parametric SEs | Bootstrap SEs | `regress y x` vs `bootstrap: regress y x` |

### When to Use Nonparametric Methods

- Normality violated (`swilk varname` to test)
- Small sample size (n < 30)
- Outliers present
- Ordinal data
- Interest in medians or quantiles rather than means
- Heterogeneous effects across the distribution

### Bandwidth Selection (kdensity, lpoly, lowess)

- Stata defaults are usually good starting points
- Smaller bandwidth = less smooth (more local detail, more noise)
- Larger bandwidth = more smooth (loses detail)

### Bootstrap Replications Guide

| Purpose | Reps |
|---|---|
| Initial exploration | 100-200 |
| Standard analysis | 500-1000 |
| Publication | 2000-5000+ |

### Quantile Selection

```stata
sqreg y x, quantiles(0.25 0.50 0.75)              // Standard
sqreg y x, quantiles(0.1 0.25 0.5 0.75 0.9)       // More detailed
sqreg y x, quantiles(0.05(0.05)0.95)               // Very detailed
```

### Complete Analysis Workflow

```stata
sysuse auto, clear

// 1. Descriptive statistics
tabstat price mpg, by(foreign) statistics(n mean sd p50 iqr)

// 2. Normality assessment
swilk price

// 3. Group comparisons (parametric + nonparametric)
ttest price, by(foreign)
ranksum price, by(foreign)

// 4. Correlations
pwcorr price mpg, sig
spearman price mpg

// 5. Regression
regress price mpg weight foreign
qreg price mpg weight foreign

// 6. Bootstrap inference
bootstrap, reps(500): regress price mpg weight
```
