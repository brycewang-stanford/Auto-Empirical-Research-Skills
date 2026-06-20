# xtabond2: Dynamic Panel GMM Estimation

## Overview

`xtabond2` implements Arellano-Bond (1991) difference GMM and Arellano-Bover/Blundell-Bond (1995, 1998) system GMM for dynamic panel data. Designed for:

- Small T (time periods), large N (panel units)
- A lagged dependent variable as a regressor
- Independent variables that are not strictly exogenous
- Fixed individual effects correlated with regressors

---

## Installation

```stata
ssc install xtabond2, replace
ssc install ranktest          * Required dependency

* Verify installation
webuse abdata, clear
xtabond2 n L.n w k, gmm(L.n) iv(w k) robust
```

---

## The Dynamic Panel Problem

Standard FE estimation with a lagged dependent variable produces **Nickell bias**: the within-transformed lag correlates with the transformed error. Bias is O(1/T), severe when T is small.

**Key insight**: The true parameter on the lagged DV lies between FE (downward biased) and OLS (upward biased). GMM should fall in this range.

```stata
* Demonstrate bias bounds
xtset id t
xtreg y L.y, fe                              * Biased downward
reg y L.y                                     * Biased upward
xtabond2 y L.y, gmm(L.y, lag(2 3)) robust    * Should fall between
```

---

## Difference GMM (Arellano-Bond)

First-differences to remove fixed effects, then instruments with lagged levels:

- y_i,t-2 is uncorrelated with delta-epsilon_it (if epsilon has no serial correlation)

```stata
* Difference GMM
xtabond2 n L.n w k, ///
    gmm(L.n, lag(2 .)) ///
    iv(w k, equation(diff)) ///
    robust
```

**Best for**: Low/moderate persistence (AR parameter < 0.8), small T (3-10 periods).

**Limitations**: Weak instruments when series are highly persistent; loses one time period to differencing.

---

## System GMM (Blundell-Bond)

Combines difference and level equations to address weak instruments in difference GMM:

1. **Difference equation**: instruments = lagged levels
2. **Level equation**: instruments = lagged differences

**Additional assumption**: E[delta-y_i,t-1 * mu_i] = 0 (changes uncorrelated with fixed effect).

```stata
* System GMM (default when no equation(diff) restriction)
xtabond2 n L.n w k, ///
    gmm(L.n, lag(1 .) collapse) ///
    iv(w k) ///
    robust twostep
```

| Feature | Difference GMM | System GMM |
|---------|---------------|------------|
| **Equations** | First differences only | Differences + levels |
| **Instruments for levels** | None | Lagged differences |
| **Efficiency** | Lower for persistent series | Higher |
| **Additional assumption** | None | E[delta-y * mu] = 0 |
| **Number of instruments** | Fewer | More (needs collapse) |

The **Difference-in-Hansen** test (reported automatically for system GMM) evaluates the additional level-equation instruments.

---

## Basic Syntax and Usage

```stata
xtabond2 depvar [indepvars] [if] [in] [weight], ///
    gmm(varlist [, lag(start end) collapse orthogonal equation()]) ///
    [iv(varlist [, equation(diff|level|both)])] ///
    [onestep | twostep] [robust] [small] [orthogonal]
```

### Variable Treatment

**Strictly exogenous** (use `iv()`):
```stata
xtabond2 y L.y x1 x2, gmm(L.y) iv(x1 x2) robust
```

**Predetermined** -- may respond to past shocks but not current (use `gmm()` with `lag(1 .)`):
```stata
xtabond2 y L.y x, gmm(L.y x, lag(1 .)) robust
```

**Endogenous** -- may correlate with current shocks (use `gmm()` with `lag(2 .)`):
```stata
xtabond2 y L.y x, gmm(L.y x, lag(2 .)) robust
```

### Multiple Variables with Different Treatments

```stata
xtabond2 y L.y x1 x2 x3, ///
    gmm(L.y x3, lag(2 .)) ///      /* Endogenous */
    gmm(x2, lag(1 .)) ///           /* Predetermined */
    iv(x1) ///                      /* Strictly exogenous */
    robust twostep
```

---

## Instrument Creation

### The lag() Option

```stata
gmm(L.y, lag(2 .))    * Lags 2 through all available
gmm(L.y, lag(2 3))    * Only lags 2 and 3
gmm(L.y, lag(1 4))    * Lags 1 through 4
```

Without collapse, instrument count grows quadratically with T (one column per variable per time period per lag).

### The equation() Suboption

```stata
gmm(L.y, lag(2 .) equation(diff))    * First-differences equation only
gmm(L.y, lag(2 .) equation(level))   * Levels equation only
gmm(L.y, lag(2 .) equation(both))    * Both (system GMM default)
iv(x, equation(diff))                * Standard IV for diff equation only
iv(x)                                * Default is equation(both)
```

### Mixed Instrument Example

```stata
xtabond2 n L.n L(0/1).w L(0/1).k yr1980-yr1984, ///
    gmm(L.n, lag(2 4)) ///                    /* Lags 2-4 of employment */
    gmm(L.(w k), lag(1 3)) ///                /* Lags 1-3 of wages & capital */
    iv(yr1980-yr1984) ///                     /* Year dummies strictly exogenous */
    robust twostep
```

---

## Lag Limits and the Collapse Option

### The Instrument Proliferation Problem

Without collapse: # instruments = T(T-1)/2 per GMM variable. With T=10 and 3 GMM variables, that is 135 instruments.

**Problems**: Overfitting, weak Hansen test, finite sample bias toward OLS.

**Rule of thumb: Keep instruments <= number of groups.**

```stata
* Check after estimation
display e(j)    // Number of instruments
display e(N_g)  // Number of groups
assert e(j) <= e(N_g)
```

### Limiting Lag Depth

```stata
gmm(L.y, lag(2 3))    * Only lags 2 and 3 (instead of lag(2 .))
```

### The collapse Option

Creates one instrument per variable per lag instead of one per variable per time period per lag.

```stata
gmm(varlist, lag(start end) collapse)
```

```stata
* Without collapse (many instruments, likely > 100)
xtabond2 n L.n w k, ///
    gmm(L.n, lag(2 .)) gmm(L.(w k), lag(1 .)) ///
    iv(yr1980-yr1984) robust

* With collapse (likely 20-40 instruments)
xtabond2 n L.n w k, ///
    gmm(L.n, lag(2 .) collapse) gmm(L.(w k), lag(1 .) collapse) ///
    iv(yr1980-yr1984) robust twostep
```

**Use collapse when**: instruments approach/exceed groups, Hansen p > 0.90.

**Optimal strategy**: Always use collapse for system GMM, limit lags to 2-3, check j < N_g.

---

## Orthogonal Deviations

First differences lose TWO observations per gap in unbalanced panels. Orthogonal deviations (subtract future mean) lose only ONE, preserving more data.

```stata
xtabond2 depvar indepvars, ///
    gmm(...) iv(...) ///
    orthogonal ///
    robust
```

**Standard practice** -- use orthogonal with system GMM:

```stata
xtabond2 y L.y x, ///
    gmm(L.y, lag(1 .) collapse) ///
    iv(x) ///
    robust twostep orthogonal small
```

---

## One-Step vs Two-Step Estimation

**One-step** (default): Fixed weighting matrix. Faster, more robust in finite samples.

**Two-step**: Optimal weighting matrix from first-step residuals. Asymptotically efficient but SEs are downward-biased in small samples -- requires Windmeijer correction via `small`.

**Best practice -- use two-step with Windmeijer correction**:

```stata
xtabond2 y L.y x, ///
    gmm(L.y, lag(2 3) collapse) ///
    iv(x) ///
    robust twostep small
```

Typical pattern: coefficients similar across one-step/two-step; uncorrected two-step SEs are smaller (biased); `small` correction brings them to comparable levels.

---

## Standard Errors

**Always use `robust twostep small`**:

| Type | Syntax | Notes |
|------|--------|-------|
| Conventional | (no options) | Not recommended; assumes homoskedasticity |
| Robust | `robust` | Sandwich estimator; standard in applied work |
| Windmeijer-corrected | `robust twostep small` | Essential for two-step; typically inflates SE by 10-40% |
| Cluster-robust | `robust cluster(group_var)` | Rarely needed; panel structure already handles within-unit correlation |

---

## Diagnostic Tests

### 1. Arellano-Bond AR Tests

Tests serial correlation in **differenced** residuals.

- **AR(1)**: Should be significant (p < 0.05) -- differencing induces MA(1) by construction
- **AR(2)**: Should NOT be significant (p > 0.05) -- validates no serial correlation in level errors

```
Arellano-Bond test for AR(1) in first differences: z = -2.49  Pr > z = 0.013  (expected)
Arellano-Bond test for AR(2) in first differences: z = -0.28  Pr > z = 0.777  (good)
```

**If AR(2) rejects**:
```stata
* Add more lags of DV, start instruments deeper
xtabond2 y L(1/2).y x, gmm(L.y, lag(3 .)) iv(x) robust
```

### 2. Hansen Test (Overidentifying Restrictions)

Tests instrument validity. H0: instruments are exogenous.

- **p > 0.10**: Cannot reject -- instruments appear valid
- **p < 0.10**: Instruments may be invalid
- **p > 0.90**: Test weakened by too many instruments -- reduce them

**Ideal range: 0.10 < p < 0.25**

**Hansen vs Sargan**: Sargan is not robust to heteroskedasticity but not weakened by many instruments. Hansen is robust but weakened. Focus on Hansen when using `robust`.

### 3. Difference-in-Hansen Test

Tests subsets of instruments. Reported automatically for system GMM level instruments.

```stata
* Manual difference-in-Hansen
quietly xtabond2 n L.n w k, gmm(L.(n w)) iv(k) robust twostep small
scalar H_full = e(hansen)
scalar df_full = e(hansendf)

quietly xtabond2 n L.n w k, gmm(L.n) iv(w k) robust twostep small
scalar diff_H = H_full - e(hansen)
scalar diff_df = df_full - e(hansendf)
display "P-value: " chi2tail(diff_df, diff_H)
```

### 4. Coefficient Bounds Check

GMM estimate on lagged DV should fall between FE (lower) and OLS (upper):

```stata
quietly reg n L.n w k
scalar beta_ols = _b[L.n]
quietly xtreg n L.n w k, fe
scalar beta_fe = _b[L.n]
quietly xtabond2 n L.n w k, gmm(L.n, lag(2 3)) iv(w k) robust twostep small
assert beta_fe < _b[L.n] & _b[L.n] < beta_ols
```

### Complete Diagnostic Checklist

```stata
xtabond2 n L.n w k, gmm(L.n, lag(2 3) collapse) iv(w k) robust twostep small

display "AR(2) p > 0.05:     " cond(e(ar2p) > 0.05, "PASS", "FAIL")
display "Hansen p 0.10-0.90: " cond(e(hansenp) > 0.10 & e(hansenp) < 0.90, "PASS", "FAIL")
display "Instruments < Groups: " cond(e(j) < e(N_g), "PASS", "FAIL")
```

---

## Complete Dynamic Panel Workflow

### Steps 1-3: Data Prep and Baselines

```stata
webuse abdata, clear
xtset id year
xtsum n w k

* Pooled OLS (upward biased)
reg n L.n w k
estimates store ols
scalar beta_ols = _b[L.n]

* Fixed effects (downward biased)
xtreg n L.n w k, fe vce(cluster id)
estimates store fe
scalar beta_fe = _b[L.n]
```

### Steps 4-5: GMM Estimation

```stata
* Difference GMM
xtabond2 n L.n w k, ///
    gmm(L.n, lag(2 3)) iv(w k, equation(diff)) ///
    robust twostep small
estimates store diff_gmm

* System GMM (preferred)
xtabond2 n L.n w k yr1980-yr1984, ///
    gmm(L.n, lag(1 2) collapse) iv(w k yr1980-yr1984) ///
    robust twostep orthogonal small
estimates store sys_gmm

* Test time effects
test yr1980 yr1981 yr1982 yr1983 yr1984
```

### Step 6: Robustness

```stata
* Sensitivity to lag structure
forvalues maxlag = 2/4 {
    quietly xtabond2 n L.n w k, ///
        gmm(L.n, lag(2 `maxlag') collapse) iv(w k) ///
        robust twostep small
    display "Max lag = `maxlag': coef=" %6.4f _b[L.n] ///
        " AR2p=" %6.4f e(ar2p) " Hansenp=" %6.4f e(hansenp) " j=" e(j)
}

* Treat wages as predetermined
xtabond2 n L.n w k, ///
    gmm(L.n, lag(2 3) collapse) gmm(w, lag(1 2) collapse) ///
    iv(k) robust twostep small
```

### Step 7: Postestimation

```stata
* Long-run effects
nlcom (lr_wage: _b[w] / (1 - _b[L.n])) ///
      (lr_capital: _b[k] / (1 - _b[L.n]))

* Export results
esttab ols fe diff_gmm sys_gmm using "results.tex", replace ///
    b(%9.4f) se(%9.4f) star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N N_g ar2p hansenp j, ///
        labels("Observations" "Firms" "AR(2) p-value" "Hansen p-value" "Instruments")) ///
    mtitles("OLS" "FE" "Diff-GMM" "Sys-GMM")
```

---

## Best Practices

### Standard Specification (Use as Default)

```stata
xtabond2 depvar L.depvar indepvars, ///
    gmm(L.depvar, lag(1 2) collapse) ///
    iv(exog_vars) ///
    robust twostep orthogonal small
```

Why: System GMM (efficient), limited lags with collapse (avoids proliferation), orthogonal deviations (handles gaps), Windmeijer correction (valid SEs).

### Instrument Selection

- Keep instruments < groups (`assert e(j) < e(N_g)`)
- Use collapse + limit lag depth to 2-3
- Only GMM-instrument truly endogenous variables; use `iv()` for exogenous ones

### Common Mistakes

**DON'T**: Use `lag(2 .)` without collapse; ignore AR(2) test; omit `robust`; use two-step without `small`; trust Hansen p > 0.90.

**DO**: Always `robust twostep small`; keep instruments < groups; use `collapse`; limit lag depth; report all diagnostics.

### Sample Size Requirements

- N (groups): At least 50-100
- T (time periods): At least 3-4
- Very large T (> 20): FE may be better; N ~ T: not suitable for dynamic panel GMM

### When NOT to Use xtabond2

- No lagged dependent variable -> use `xtreg, fe`
- Large T relative to N (T > 20, N < 100) -> use FE with cluster-robust SEs
- Very persistent series (AR near 1) -> consider `xtlsdvc` or cointegration methods

### Reporting Requirements

Report: coefficients with robust SEs, N and groups, AR(1)/AR(2) p-values, Hansen p-value, number of instruments, specification details (one/two-step, lags, collapse).

---

## Troubleshooting

### AR(2) Test Rejects

```stata
* Add more lags of DV, start instruments deeper
xtabond2 y L(1/2).y x, gmm(L.y, lag(3 4)) iv(x) robust
```

### Hansen Test Rejects (p < 0.10)

```stata
* Reduce instruments; move suspect exogenous vars to gmm()
xtabond2 y L.y x, gmm(L.y, lag(2 3) collapse) iv(x) robust
xtabond2 y L.y x z, gmm(L.(y x)) iv(z) robust   * Treat x as endogenous
```

### Hansen Test Too High (p > 0.90)

```stata
* Reduce instruments dramatically
xtabond2 y L.y x, gmm(L.y, lag(2 2) collapse) iv(x) robust twostep small
* Target j < N_g/2
```

### GMM Outside OLS-FE Bounds

- GMM < FE (weak instruments): Switch to system GMM
- GMM > OLS (invalid instruments): Try difference GMM only with `equation(diff)`

### "Could not calculate robust VCE"

```stata
* Check for collinearity; drop units with zero within-variation
bysort id: egen sd_y = sd(y)
drop if sd_y == 0
```

### Very Large Standard Errors

Use system GMM, reduce instruments, check first-stage relevance:
```stata
reg L.y L2.y L3.y x
test L2.y L3.y    * F > 10 suggests reasonable instruments
```

### Insufficient Observations

```stata
* Reduce lags; use orthogonal deviations; drop short panels
xtabond2 y L.y x, gmm(L.y, lag(2 2)) iv(x) robust orthogonal
bysort id: gen T = _N
keep if T >= 4
```

---

## Quick Reference

```stata
* Difference GMM
xtabond2 y L.y x, gmm(L.y, lag(2 3)) iv(x, equation(diff)) robust

* System GMM (recommended)
xtabond2 y L.y x, ///
    gmm(L.y, lag(1 2) collapse) iv(x) ///
    robust twostep orthogonal small

* Diagnostics
display "AR(2): " e(ar2p)
display "Hansen: " e(hansenp)
display "Instruments: " e(j) "/" e(N_g)
```

### Related Commands

- `xtabond`: Official Stata Arellano-Bond (less flexible)
- `xtdpdsys`: Official Stata system GMM (less flexible)
- `xtdpd`: General dynamic panel data estimator

### Key References

- Roodman (2009). "How to Do xtabond2." *Stata Journal*, 9(1), 86-136.
- Windmeijer (2005). Finite sample correction for two-step GMM. *JoE*, 126(1), 25-51.

```stata
help xtabond2
```
