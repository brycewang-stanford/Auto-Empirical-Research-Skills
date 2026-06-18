# Bootstrap and Simulation Methods in Stata

## Bootstrap Command

```stata
bootstrap exp_list [, options]: command
```

### Basic Usage

```stata
bootstrap meanMPG=r(mean): summarize mpg
bootstrap r(p50), reps(1000): summarize mpg, detail
bootstrap: regress mpg weight foreign       // All coefficients from e(b)
bootstrap f=e(F): regress mpg weight foreign

// ALWAYS name statistics explicitly -- do NOT rely on auto-names like _bs_1
bootstrap weight_coef=_b[weight], reps(500) seed(42): regress price weight mpg
// Now access _b[weight_coef], _se[weight_coef] -- not _b[_bs_1]

// Quantile regression (bootstrap SEs recommended)
bootstrap, reps(200): qreg price weight length foreign
```

### Common Options

- `reps(#)` -- replications (default 50; use 1000+ for CIs)
- `seed(#)` -- random number seed
- `saving(filename)` -- save bootstrap results to dataset
- `cluster(varname)` -- block bootstrap for panel data
- `idcluster(newvar)` -- unique ID for selected clusters
- `nodots`, `nowarn`

### Custom Bootstrap Programs

```stata
program define topQuartileMean, rclass
    xtile quartile = mpg, nq(4)
    summarize weight if quartile == 4
    return scalar tqm = r(mean)
    drop quartile
end

bootstrap tqm=r(tqm), reps(500): topQuartileMean
```

**Requirements:** Program must be `rclass` or `eclass`, return results via `return scalar`, and preserve data structure.

### Panel Data Bootstrap

```stata
bootstrap, cluster(idcode) idcluster(newid) reps(200): xtreg y x1 x2, fe
```

---

## Simulate Command

```stata
simulate exp_list, reps(#) [options]: command
```

**GOTCHA -- comma placement:** The comma separates the expression list from options. It goes AFTER the last `name=expr` and BEFORE `reps()`. Getting this wrong is a fatal syntax error:

```stata
// WRONG: comma after last expression then options without comma
simulate b=r(b) se=r(se) cover=r(cover) reps(1000): myprog     // ERROR
simulate b=r(b) se=r(se) cover=r(cover), reps(1000),: myprog   // ERROR

// RIGHT: single comma separating expressions from options
simulate b=r(b) se=r(se) cover=r(cover), reps(1000) seed(123): myprog
```

```stata
program define simreg, rclass
    drop _all
    set obs 200
    generate x = rnormal(0, 1)
    generate y = 2 + 3*x + rnormal(0, 2)   // SD=2, so errors ~ N(0, 4)
    regress y x
    return scalar b1 = _b[x]
    return scalar se1 = _se[x]
end

simulate b1=r(b1) se1=r(se1), reps(1000) seed(98765): simreg
summarize b1 se1
```

### Using postfile for Complex Simulations

```stata
postfile buffer beta se reject using simresults, replace

forvalues i = 1/2000 {
    quietly {
        drop _all
        set obs 100
        generate x = rnormal(0, 1)
        generate y = 2 + 3*x + rnormal(0, 1.5)
        regress y x
        test x = 3
        post buffer (_b[x]) (_se[x]) ((r(p) < 0.05))
    }
}

postclose buffer
use simresults, clear
summarize
mean reject                     // Should be ~0.05 under true null
```

---

## Permute Command

```stata
permute permvar exp_list, reps(#) [options]: command
```

Randomly shuffles `permvar` to build a null distribution for the test statistic.

```stata
set seed 1234
permute treatment diff=r(mu_2)-r(mu_1), reps(1000): ///
    ttest outcome, by(treatment)

permute female x2=e(chi2), reps(10000) nodots: ///
    logit goodread female i.income
```

**Options:** `left`/`right` for one-sided p-values, `strata(varname)` for within-strata permutation.

---

## Monte Carlo: Heteroskedasticity Example

```stata
program define sim_hetero, rclass
    syntax, n(integer) [beta1(real 3)]
    drop _all
    set obs `n'
    generate x = runiform(0, 10)
    generate y = 2 + `beta1'*x + rnormal(0, x)
    quietly regress y x
    return scalar b1 = _b[x]
    return scalar se1 = _se[x]
    quietly test x = `beta1'
    return scalar reject = (r(p) < 0.05)
    local ci_lower = _b[x] - 1.96*_se[x]
    local ci_upper = _b[x] + 1.96*_se[x]
    return scalar cover = (`ci_lower' <= `beta1' & `beta1' <= `ci_upper')
end

simulate b1=r(b1) se1=r(se1) reject=r(reject) cover=r(cover), ///
    reps(2000) seed(54321): sim_hetero, n(100)

summarize
mean reject                     // Rejection rate under true null (~5%?)
mean cover                      // Coverage rate (~95%?)
egen sd_b1 = sd(b1)
egen mean_se1 = mean(se1)
list sd_b1 mean_se1 in 1       // Compare actual SD to mean SE
```

### Power Analysis via Simulation

```stata
program define sim_power, rclass
    syntax, n(integer) delta(real)
    drop _all
    set obs `n'
    generate group = (_n > `n'/2)
    generate y = group*`delta' + rnormal(0, 1)
    quietly ttest y, by(group)
    return scalar reject = (r(p) < 0.05)
end

postfile power delta power using powerresults, replace
foreach d of numlist 0(0.2)1.0 {
    quietly simulate reject=r(reject), reps(1000) seed(999): ///
        sim_power, n(100) delta(`d')
    quietly mean reject
    matrix b = e(b)
    post power (`d') (b[1,1])
}
postclose power

use powerresults, clear
twoway line power delta, yline(0.8, lpattern(dash)) ///
    title("Power vs Effect Size") ytitle("Power")
```

---

## Random Number Seeds

**DO:** Set seed once at the start; record it in your code.
**DON'T:** Reset seed inside loops or multiple times within a simulation.

```stata
set seed 98765
simulate ..., reps(10000): simprogram

// Save/restore RNG state for exact reproducibility
local rngstate = c(rngstate)
set rngstate `rngstate'

// Multiple streams for parallel work
set rngstream 1
simulate ..., reps(1000): sim1
set rngstream 2
simulate ..., reps(1000): sim2
```

---

## Replication Count Guidelines

| Purpose | Replications |
|---|---|
| Quick exploratory | 50-200 |
| Standard SEs | 200+ |
| Percentile/BC confidence intervals | 1,000+ |
| BCa confidence intervals | 2,000+ |
| Monte Carlo simulation studies | 1,000-10,000 |
| High-precision/publication | 10,000+ |

---

## Bootstrap Confidence Intervals

```stata
bootstrap, reps(2000) seed(54321): regress price mpg weight
estat bootstrap, all
```

| Method | When to Use |
|---|---|
| **Normal (N)** | Large samples, approximately normal distribution |
| **Percentile (P)** | Non-normal distributions, 1000+ reps |
| **Bias-Corrected (BC)** | When bootstrap median != observed estimate |
| **BCa** | Best coverage; needs 2000+ reps |

### Saving and Analyzing Bootstrap Distribution

```stata
bootstrap median=r(p50), reps(2000) saving(bootdist, replace): ///
    summarize price, detail

use bootdist, clear
histogram median, normal
centile median, centile(2.5 97.5)   // Manual percentile CI
```

---

## Bootstrap SEs for Complex Statistics

```stata
// Median
bootstrap median=r(p50), reps(2000): summarize price, detail

// IQR
program define iqr, rclass
    summarize price, detail
    return scalar iqr = r(p75) - r(p25)
end
bootstrap iqr=r(iqr), reps(1000): iqr

// Ratio of means
program define ratio_means, rclass
    summarize price
    local mp = r(mean)
    summarize mpg
    return scalar ratio = `mp' / r(mean)
end
bootstrap ratio=r(ratio), reps(2000): ratio_means

// Cluster-robust bootstrap
bootstrap, cluster(idcode) idcluster(newid) reps(400): ///
    regress ln_wage age ttl_exp tenure
```

---

## Common Pitfalls

1. Too few replications for percentile/BC intervals
2. Resetting seed inside simulation loops
3. Not clustering bootstrap for panel data
4. Assuming normality without checking bootstrap distribution
5. Forgetting to `preserve`/`restore` data in custom programs
6. Using variance instead of SD in `rnormal()` -- N(0, sigma^2) requires `rnormal(0, sqrt(sigma^2))`, not `rnormal(0, sigma^2)`
7. **`r()` results overwritten by each command** -- each `summarize` call overwrites `r(mean)`, `r(sd)`, etc. Store to locals before the next call:

```stata
// WRONG: r(mean) from first summarize is gone after second
quietly summarize b_x
di r(mean)                  // OK here
quietly summarize se_x      // overwrites r(mean)!
di r(mean)                  // this is now mean of se_x, not b_x

// RIGHT: store to locals immediately
quietly summarize b_x
local mean_b = r(mean)
local sd_b = r(sd)
quietly summarize se_x
local mean_se = r(mean)
di `mean_b'                 // safe
```

8. **`di` with format + arithmetic needs parentheses:**

```stata
// WRONG: Stata cannot parse subtraction after format specifier
di %8.4f r(mean) - 3

// RIGHT: wrap the expression in parentheses
di %8.4f (r(mean) - 3)
```

### Related Commands

- `estat bootstrap` -- display bootstrap CI types
- `bstat` -- report bootstrap results from saved dataset
- `jackknife` -- alternative resampling method
- `vce(bootstrap)` -- bootstrap variance for many built-in commands
