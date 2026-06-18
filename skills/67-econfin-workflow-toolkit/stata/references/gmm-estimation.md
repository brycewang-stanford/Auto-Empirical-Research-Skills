# GMM Estimation in Stata

## The `gmm` Command

### Basic Syntax

```stata
gmm (moment_expression), instruments(varlist) [options]
```

Two syntaxes: interactive (substitutable expression) and moment-evaluator program.

### Parameter Notation

```stata
{b0}              // Named parameter
{b1}              // Named parameter
{xb: varlist}     // Linear combination shorthand

// These are equivalent:
gmm (y - {b0} - {b1}*x1 - {b2}*x2)
gmm (y - {xb: x1 x2})
```

### Common Options

```stata
onestep          // One-step GMM (default weights)
twostep          // Two-step GMM (optimal weights from first-step residuals)
igmm             // Iterated GMM (iterate until convergence)

winitial(type)   // Initial weight: identity, unadjusted, xt
wmatrix(type)    // Final weight: robust, cluster, hac

vce(robust)
vce(cluster var)
vce(hac kernel #)  // kernel: bartlett, parzen, quadraticspectral, truncated

from(matrix)     // Starting values
hascons          // Model has constant term
```

---

## Linear IV via GMM

```stata
// GMM with endogenous faminc, instrument rent
gmm (hsngval - {b0} - {b1}*faminc - {b2}*price), ///
    instruments(faminc price rent) ///
    winitial(identity) onestep

// Equivalent shorthand via ivregress
ivregress gmm hsngval (faminc = rent) price
```

```stata
// GMM replicating OLS (just-identified)
gmm (price - {xb: mpg weight foreign}), ///
    instruments(mpg weight foreign) onestep
```

## Nonlinear GMM

```stata
gmm (price - {b0}*mpg^{alpha}*weight^{beta}), ///
    instruments(mpg weight length) ///
    winitial(identity) twostep

// Provide starting values for nonlinear models
gmm (...), from(lnA=1.5 alpha=0.5 rho=0.5)
```

## Multiple Equations

```stata
gmm (equation1: hsngval - {xb1: rent faminc}) ///
    (equation2: pcturban - {xb2: rent faminc region}), ///
    instruments(equation1: rent faminc) ///
    instruments(equation2: rent faminc region) ///
    twostep vce(robust)
```

---

## Weighting Matrices

### Initial (`winitial`)

```stata
winitial(identity)     // All moments weighted equally
winitial(unadjusted)   // Inverse of moment covariance, no robust adjustment
winitial(xt varname)   // For panel data
```

### Final (`wmatrix`, for two-step)

```stata
wmatrix(robust)
wmatrix(cluster panelvar)
wmatrix(hac bartlett 4)   // HAC with Bartlett kernel, 4 lags
```

---

## One-Step vs Two-Step vs Iterated

| Method | Pros | Cons |
|--------|------|------|
| **One-step** | Fast; avoids finite-sample bias of two-step; good for just-identified | Less efficient |
| **Two-step** | Asymptotically efficient; optimal weighting | SEs can be downward-biased in small samples |
| **Iterated** | Better finite-sample properties; more robust to starting values | Slow; may not converge |

```stata
// Compare all three
gmm (...), instruments(...) onestep winitial(identity)
gmm (...), instruments(...) twostep wmatrix(robust)
gmm (...), instruments(...) igmm wmatrix(robust)
```

---

## Standard Errors

```stata
vce(robust)              // Heteroskedasticity-robust
vce(cluster company)     // Cluster-robust
vce(hac bartlett 4)      // HAC (Newey-West), 4 lags
vce(bootstrap, reps(500))  // Bootstrap
```

**HAC lag length rule of thumb**: floor(4*(T/100)^(2/9))

---

## Specification Tests

### Hansen's J Test (Overidentification)

Automatically reported after `gmm` estimation. Tests H0: instruments are valid.

```stata
// J stat reported in output; also:
estat overid
display "J = " e(J) ", p = " e(J_p)
```

- p > 0.05: Cannot reject; instruments appear valid
- p < 0.05: Reject; model misspecified or instruments invalid
- Just-identified models: J = 0 (untestable)

### Difference-in-Hansen Test

Test subsets of instruments by comparing J stats from nested models:

```stata
// Full model
quietly gmm (...), instruments(z1 z2 z3 z4) twostep wmatrix(robust)
scalar j_full = e(J)

// Drop suspect instrument
quietly gmm (...), instruments(z1 z2 z3) twostep wmatrix(robust)
scalar j_restricted = e(J)

scalar diff_j = j_full - j_restricted
scalar p_diff = chi2tail(1, diff_j)
```

### Instrument Relevance (First-Stage F-Test)

```stata
ivregress 2sls mpg (price = length turn headroom) weight foreign
estat firststage
// F > 10: instruments likely strong
```

For `gmm`, check manually:
```stata
regress price length turn headroom weight foreign
test length turn headroom
```

---

## Dynamic Panel GMM (xtabond2)

### Installation and Syntax

```stata
ssc install xtabond2

xtabond2 depvar [indepvars], gmm(varlist, lag(#1 #2)) ///
    iv(varlist) [robust small twostep orthogonal]
```

Key options:
- `gmm()`: Variables instrumented with their own lags
- `iv()`: Strictly exogenous instruments
- `lag(#1 #2)`: Lag range for GMM instruments
- `orthogonal`: Forward orthogonal deviations (instead of first differences)
- `small`: Finite-sample correction
- `collapse`: Reduce instrument count

### Difference GMM vs System GMM

```stata
// Difference GMM (Arellano-Bond)
xtabond2 n L.n w k, gmm(L.n, lag(2 3)) ///
    iv(w k, equation(diff)) robust small

// System GMM (Blundell-Bond) - adds level equation, more efficient
xtabond2 n L.n w k, gmm(L.n, lag(2 3)) ///
    iv(w k) robust small twostep orthogonal
```

### Diagnostics

Reported automatically in `xtabond2` output:

- **AR(1)**: Expected to reject (first differences induce serial correlation)
- **AR(2)**: Should NOT reject (p > 0.05 required; otherwise instruments invalid)
- **Hansen J**: p between 0.1-0.25 is ideal; very high p (> 0.9) suggests instrument proliferation

### Instrument Proliferation

Too many instruments overfit and weaken Hansen test.

```stata
// Use collapse to reduce instruments
gmm(L.n, lag(2 3) collapse)

// Limit lag depth
gmm(L.n, lag(2 4))  // Instead of lag(2 99)
```

### Complete Example

```stata
webuse abdata, clear
xtset id year

// Step 1: Difference GMM
xtabond2 n L.n L(0/1).(w k) yr1980-yr1984, ///
    gmm(L.n, lag(2 99)) ///
    gmm(L.(w k), lag(1 99)) ///
    iv(yr1980-yr1984, equation(diff)) ///
    robust small
estimates store diff_gmm

// Step 2: System GMM with collapse
xtabond2 n L.n L(0/1).(w k) yr1980-yr1984, ///
    gmm(L.n, lag(2 99) collapse) ///
    gmm(L.(w k), lag(1 99) collapse) ///
    iv(yr1980-yr1984) ///
    robust twostep orthogonal small
estimates store sys_gmm

// Compare
estimates table diff_gmm sys_gmm, ///
    b(%9.4f) se stats(N N_g ar1p ar2p hansenp)
```

---

## GMM vs 2SLS/IV

```stata
// 2SLS
ivregress 2sls mpg (price = length turn headroom) weight foreign, robust
estimates store tsls

// GMM (efficient under heteroskedasticity)
ivregress gmm mpg (price = length turn headroom) weight foreign, wmatrix(robust)
estimates store gmm_iv

estimates table tsls gmm_iv, b(%9.4f) se stats(N J)
```

- Linear models: coefficients identical; SEs may differ
- 2SLS assumes homoskedasticity for efficiency; GMM does not
- Only overidentified GMM provides J test

---

## Advanced Topics

### Poisson via GMM

```stata
// Moment: E[X'(y - exp(Xb))] = 0
gmm (y - exp({xb: x1 x2})), ///
    instruments(x1 x2) ///
    onestep vce(robust) hascons
```

### Conditional Moment Restrictions

```stata
// E[e|Z]=0 implies E[h(Z)*e]=0 for any h()
gen length2 = length^2
gmm (mpg - {xb: price weight}), ///
    instruments(weight length length2) twostep wmatrix(robust)
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "convergence not achieved" | Better starting values via `from()`; simplify model; reduce instruments |
| "could not calculate numerical derivatives" | Check collinearity; ensure identification; provide starting values |
| Negative weighting matrix | Use `winitial(identity)`; check for outliers; may indicate misspecification |

```stata
// Provide starting values
matrix b0 = (1, 0.5, 0.3)
gmm (...), instruments(...) from(b0) twostep

// Increase iterations
gmm (...), instruments(...) conv_maxiter(1000) technique(nr)
```

### Checking Results

```stata
predict resid, residuals
summarize resid                         // Should be near zero mean
correlate resid instrument1 instrument2 // Should be near zero
```

---

## Best Practices

1. Start simple, add complexity gradually
2. Always report Hansen J test for overidentified models
3. Use `vce(robust)` as default
4. For time series: HAC standard errors
5. For panel data: cluster by panel unit
6. For dynamic panels: check AR(2), avoid instrument proliferation, use `collapse`
7. Hansen p-value of 0.1-0.25 is ideal (too high suggests overfitting)

## Quick Reference

```stata
// Basic GMM
gmm (y - {xb: x1 x2}), instruments(z1 z2 z3) twostep vce(robust)

// Nonlinear GMM
gmm (y - {b0}*exp({b1}*x)), instruments(x z) onestep from(b0=1 b1=0.5)

// Dynamic panel (xtabond2)
xtabond2 y L.y x, gmm(L.y, lag(2 3)) iv(x) robust small

// Overidentification
display "J = " e(J) ", p-value = " e(J_p)

// HAC standard errors
gmm (y - {xb: x}), instruments(x z) twostep vce(hac bartlett 4)
```

## References

- `help gmm`, `help ivregress`, `help xtabond2`
- Roodman (2009): "How to do xtabond2"
- Baum et al. (2003): "Instrumental variables and GMM"
