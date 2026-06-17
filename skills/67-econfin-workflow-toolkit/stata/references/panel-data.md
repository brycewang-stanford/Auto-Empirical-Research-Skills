# Panel Data Analysis in Stata

## Setting Up Panel Data: xtset

```stata
xtset panelvar [timevar] [, options]
```

```stata
xtset country year
xtset firm_id year, yearly
xtset person_id              // No time variable
xtset                        // Check current settings
```

- Panel variable must uniquely identify each unit
- Settings persist after save/reload
- Use `xtdescribe` to check if panel is balanced/unbalanced

---

## Time-Series Operators in Panel Data

After `xtset`, these operators work within panels:

```stata
L.variable      // First lag (t-1)
L2.variable     // Second lag
L(1/3).variable // Lags 1 through 3
F.variable      // First lead (t+1)
D.variable      // First difference (y[t] - y[t-1])
D2.variable     // Second difference
LD.variable     // Lag of first difference

// Use directly in regressions
xtreg consumption L.gdp L.income, fe
```

---

## Descriptive Commands

### xtsum - Between/Within Decomposition

```stata
xtsum ln_wage age tenure
```

Output decomposes variation into:
- **Overall**: All observations (ignoring panel structure)
- **Between**: Across panel units (comparing averages across units)
- **Within**: Over time within units

Relationship: sigma_overall^2 approximately equals sigma_between^2 + sigma_within^2

This decomposition is critical for understanding whether your variation is primarily cross-sectional or longitudinal, which informs model choice.

### xttab - Panel Cross-Tabulation

```stata
xttab union
```

Shows overall frequency, between frequency (% of units ever in each state), and within variation.

### xttrans - Transition Probabilities

```stata
xttrans union    // Transition matrix between states over time
```

---

## Fixed Effects (FE)

Eliminates all time-invariant heterogeneity by demeaning (within transformation). Controls for unobserved time-invariant confounders but **cannot estimate effects of time-invariant variables** (gender, race, etc.).

```stata
xtreg ln_wage age tenure, fe
xtreg ln_wage age tenure, fe vce(robust)
xtreg ln_wage age tenure, fe vce(cluster idcode)

// Entity AND time fixed effects
xtreg ln_wage age tenure i.year, fe
testparm i.year                         // Test if time FEs are needed
```

### reghdfe - High-Dimensional Fixed Effects

For multiple sets of fixed effects (faster, more flexible than `xtreg`):
```stata
// ssc install reghdfe
reghdfe ln_wage age tenure, absorb(idcode)
reghdfe ln_wage age tenure, absorb(idcode year)
reghdfe ln_wage age tenure, absorb(idcode year) vce(cluster idcode year)  // Two-way clustering
```

### Key Output Statistics
- **Within R-squared**: Variation explained within entities over time
- **Between R-squared**: Variation explained across entities
- **sigma_u**: SD of entity-specific effects
- **sigma_e**: SD of idiosyncratic error
- **rho**: Fraction of variance due to entity effects = sigma_u^2 / (sigma_u^2 + sigma_e^2)
- **corr(u_i, Xb)**: FE allows this to be nonzero (unlike RE)

---

## Random Effects (RE)

Uses GLS, exploiting both within and between variation. Assumes individual effects u_i are uncorrelated with regressors. More efficient than FE when assumption holds; can include time-invariant variables.

```stata
xtreg ln_wage age tenure, re
xtreg ln_wage age tenure, re vce(robust)
xtreg ln_wage age tenure female, re      // Can include time-invariant vars
```

Key output includes **theta**: the GLS transformation parameter (theta=1 equals FE; theta=0 equals pooled OLS).

### Between Effects and Pooled OLS
```stata
xtreg ln_wage age tenure, be     // Uses group means only
reg ln_wage age tenure           // Pooled OLS (ignores panel structure)
```

---

## First Differences (FD)

Eliminates individual effects by differencing consecutive observations. Preferred over FE when T is small and errors follow a random walk.

```stata
xtreg gdp investment population, fd
xtreg gdp investment population, fd vce(robust)

// Or manually
reg D.gdp D.investment D.population, noconstant vce(cluster country)
```

---

## Hausman Test: FE vs RE

Tests whether individual effects are correlated with regressors.

- **H0**: RE is consistent and efficient (u_i uncorrelated with X)
- **H1**: Only FE is consistent

```stata
quietly xtreg ln_wage age tenure, fe
estimates store fixed

quietly xtreg ln_wage age tenure, re
estimates store random

hausman fixed random
// p < 0.05: Reject H0 -> Use FE
// p >= 0.05: Fail to reject -> RE acceptable
```

### Hausman Gotchas

**"Not positive definite" error:** The Hausman test requires V_fe - V_re to be positive definite. When it fails:
```stata
hausman fe re, sigmamore     // Use RE sigma for both (most common fix)
hausman fe re, sigmaless     // Use FE sigma for both

// Or use the robust overidentification test (works with clustered SEs too)
// ssc install xtoverid
xtreg ln_wage age tenure, re
xtoverid
```

**Hausman requires default SEs:** The classic Hausman test is invalid with robust or clustered standard errors. Estimate both models with default SEs for the test, then re-estimate your chosen model with clustered SEs for inference:
```stata
// Step 1: Hausman test with default SEs
quietly xtreg ln_wage age tenure, fe
estimates store fe_default
quietly xtreg ln_wage age tenure, re
estimates store re_default
hausman fe_default re_default

// Step 2: Re-estimate chosen model with clustered SEs
xtreg ln_wage age tenure, fe vce(cluster idcode)
```

### Mundlak Test (Alternative)
Include group means of time-varying regressors in RE model. If jointly significant, FE is preferred.

```stata
bysort idcode: egen mean_age = mean(age)
bysort idcode: egen mean_tenure = mean(tenure)
xtreg ln_wage age tenure mean_age mean_tenure, re
test mean_age mean_tenure
```

---

## Testing for Panel Effects

```stata
// Breusch-Pagan LM test (after RE estimation)
xtreg ln_wage age tenure, re
xttest0
// H0: sigma_u^2 = 0 (pooled OLS appropriate)
// p < 0.05: Use panel methods
```

---

## Dynamic Panel Data Models

Including lagged dependent variable creates "Nickell bias" in standard FE when T is small. GMM estimators address this.

### xtabond - Arellano-Bond (Difference GMM)

Differences the equation to remove individual effects, uses lagged levels as instruments.

```stata
webuse abdata
xtset id year

xtabond n L(0/2).(w k), vce(robust)
xtabond n w k, lags(2) maxldep(3) vce(robust)
```

### xtdpdsys - Blundell-Bond (System GMM)

Combines difference and level moment conditions. More efficient, especially with persistent series.

```stata
xtdpdsys n L(0/1).(w k), vce(robust)
xtdpdsys n w k, lags(2) maxldep(2) vce(robust)
```

### Dynamic Panel Diagnostics

```stata
// After xtabond or xtdpdsys:
estat abond     // AR test: Expect AR(1) significant, AR(2) NOT significant
estat sargan    // Overidentification: H0 = instruments valid (want p > 0.05)
```

### xtabond2 (User-Written, More Flexible)
```stata
ssc install xtabond2
xtabond2 n L.n w k, gmm(L.(n w k)) iv(yr1980-yr1984) robust
```

---

## When to Use Each Model

| Model | When |
|-------|------|
| **Fixed Effects** | Control for time-invariant unobserved heterogeneity; T >= 3; Hausman rejects RE |
| **Random Effects** | Need time-invariant variables; units are random sample; Hausman doesn't reject |
| **First Differences** | T = 2; errors follow random walk |
| **Dynamic GMM** | Lagged dependent variable as regressor; small T, large N; potential endogeneity |

---

## Summary Table

| Estimator | Command | Key Feature |
|-----------|---------|-------------|
| Pooled OLS | `reg y x` | Ignores panel structure |
| Fixed Effects | `xtreg y x, fe` | Eliminates time-invariant confounders |
| Random Effects | `xtreg y x, re` | More efficient; can estimate time-invariant effects |
| First Difference | `xtreg y x, fd` | Alternative to FE |
| Between Effects | `xtreg y x, be` | Cross-sectional variation only |
| Arellano-Bond | `xtabond y L.y x` | Dynamic panel, difference GMM |
| System GMM | `xtdpdsys y L.y x` | Dynamic panel, more efficient |
| Multi-way FE | `reghdfe y x, absorb(id1 id2)` | High-dimensional fixed effects |

---

## Common Pitfalls

- Including lagged dependent variable with standard FE (use xtabond/xtdpdsys)
- Using RE when individual effects likely correlate with regressors
- Ignoring serial correlation in errors
- Too many instruments in dynamic panel models (overfitting; Sargan test loses power)
- Forgetting to cluster standard errors at the panel level
- Not checking panel balance with `xtdescribe`

## Best Practices

1. Start with `xtdescribe` and `xtsum` to understand your data structure
2. Run Hausman test to choose between FE and RE
3. Use `xttest0` to test whether panel methods are needed at all
4. Always use robust or clustered standard errors
5. For dynamic models, check AR(2) and Sargan/Hansen tests
6. Report: model type, N obs, N groups, R-squared (within/between/overall), SE type, diagnostic tests
