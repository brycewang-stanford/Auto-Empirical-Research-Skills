---
name: rdd-analysis
description: |
  Econometrics skill for Regression Discontinuity Design (RDD). Activates when the user asks about:
  "regression discontinuity", "RDD", "RD design", "sharp RDD", "fuzzy RDD",
  "running variable", "forcing variable", "cutoff", "bandwidth selection",
  "local linear regression", "McCrary test", "density test", "RDROBUST",
  "continuity assumption", "donut hole RDD", "geographic RDD",
  "断点回归", "回归不连续", "运行变量", "截断值", "带宽选择",
  "精确断点", "模糊断点", "密度检验", "局部线性回归"
---

# Regression Discontinuity Design (RDD) Skill

This skill covers sharp and fuzzy RDD: identification assumptions, bandwidth selection, local polynomial estimation, validity tests, and reporting standards for academic papers.

## Core Logic

RDD exploits a known threshold in a continuous "running variable" (X) that determines treatment assignment. Units just above and below the cutoff (c) are comparable on all dimensions except treatment.

**Sharp RDD**: Treatment perfectly determined by crossing cutoff
- T_i = 1 if X_i ≥ c, T_i = 0 if X_i < c
- Estimand: Average treatment effect at the cutoff (τ_SRD)

**Fuzzy RDD**: Crossing cutoff increases probability of treatment (like an instrument)
- Use when there's non-compliance around the cutoff
- Estimand: LATE at the cutoff (τ_FRD = reduced form / first stage)

## RDD Assumptions

1. **Continuity of conditional expectation**: E[Y(0)|X] and E[Y(1)|X] are continuous at X = c
   - Means: units cannot precisely manipulate running variable to select into treatment
2. **No other discontinuities**: Nothing else changes discontinuously at the cutoff
3. **Bandwidth continuity**: Observations near cutoff are locally valid comparisons

## Complete RDD Workflow

### Step 1: Visualize the Discontinuity

Always plot the raw data with binned means before any regression.

```python
# Python
import matplotlib.pyplot as plt
import numpy as np

# Bin the running variable
df['bin'] = pd.cut(df['running_var'], bins=50)
bin_means = df.groupby('bin')[['running_var', 'y']].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.scatter(bin_means['running_var'], bin_means['y'], s=30, color='steelblue')
plt.axvline(x=cutoff, color='red', linestyle='--', label='Cutoff')
plt.xlabel('Running Variable'); plt.ylabel('Outcome')
plt.title('RDD: Binned Scatter Plot')
plt.legend(); plt.show()
```

```r
# R (rdplot from rdrobust)
library(rdrobust)
rdplot(y = df$y, x = df$running_var, c = cutoff,
       title = "RDD Binned Scatter", x.label = "Running Variable",
       y.label = "Outcome")
```

```stata
rdplot y running_var, c(cutoff) graph_options(title("RDD Visualization"))
```

### Step 2: Bandwidth Selection

**Default**: Use Imbens-Kalyanaraman (IK) or Calonico-Cattaneo-Titiunik (CCT) optimal bandwidth.

```python
from rdrobust import rdrobust
result = rdrobust(df['y'], df['running_var'], c=cutoff)
print(result.summary())
```

```r
rdbwselect(y = df$y, x = df$running_var, c = cutoff)
```

```stata
rdbwselect y running_var, c(cutoff) all
```

### Step 3: Main RDD Estimate

```python
# Python (rdrobust) — triangular kernel, local linear
result = rdrobust(y=df['y'], x=df['running_var'], c=cutoff,
                  kernel='triangular', p=1)
print(result.summary())
```

```r
# R
main_rdd <- rdrobust(y = df$y, x = df$running_var, c = cutoff,
                     kernel = "triangular", p = 1)
summary(main_rdd)
```

```stata
rdrobust y running_var, c(cutoff) kernel(triangular) p(1)
```

### Step 4: Validity Tests (All Required)

#### 4a. Density/Manipulation Test (McCrary Test)

H₀: No discontinuity in density of running variable at cutoff

```python
from rdrobust import rddensity
density_test = rddensity(df['running_var'], c=cutoff)
print(density_test.summary())
```

```r
library(rddensity)
rdd_density <- rddensity(df$running_var, c = cutoff)
summary(rdd_density)
rdplotdensity(rdd_density, df$running_var)
```

```stata
rddensity running_var, c(cutoff)
```

**Interpretation**: p > 0.05 → no bunching; manipulation unlikely ✓

#### 4b. Covariate Balance (Placebo Outcome Tests)

Run RDD on pre-determined covariates — should find no discontinuity.

```r
for (cov in c("age", "income_pre", "gender")) {
  res <- rdrobust(y = df[[cov]], x = df$running_var, c = cutoff)
  cat(cov, ": coef =", res$coef[1], ", p =", res$pv[3], "\n")
}
```

#### 4c. Placebo Cutoff Tests

Run RDD at fake cutoffs above and below actual cutoff — should find no effects.

```r
for (fake_c in c(cutoff - 5, cutoff + 5)) {
  df_sub <- df[df$running_var < cutoff, ]  # Use only control side
  res <- rdrobust(df_sub$y, df_sub$running_var, c = fake_c)
  cat("Placebo c =", fake_c, ": coef =", res$coef[1], "\n")
}
```

#### 4d. Bandwidth Sensitivity

Report estimates at 50%, 75%, 125%, 150% of optimal bandwidth.

```r
bw_opt <- rdbwselect(df$y, df$running_var, c = cutoff)$bws[1,1]
for (mult in c(0.5, 0.75, 1, 1.25, 1.5)) {
  res <- rdrobust(df$y, df$running_var, c = cutoff, h = bw_opt * mult)
  cat("BW =", round(bw_opt*mult,2), ": coef =", round(res$coef[1],3),
      ", p =", round(res$pv[3],3), "\n")
}
```

## Fuzzy RDD

```r
# R — fuzzy RDD (uses crossing as instrument for actual treatment)
fuzzy_rdd <- rdrobust(y = df$y, x = df$running_var, c = cutoff,
                      fuzzy = df$actual_treatment)
summary(fuzzy_rdd)
```

```stata
rdrobust y running_var, c(cutoff) fuzzy(actual_treatment)
```

## Reporting Standards

Report in this order:
1. **Binned scatter plot** showing discontinuity visually
2. **Main estimate** with optimal CCT bandwidth, triangular kernel, local linear
3. **Sensitivity table**: estimates across bandwidth multiples and polynomial orders
4. **Validity tests**: density test (McCrary), covariate balance, placebo cutoffs
5. **Sample size**: N total, N within bandwidth (left and right)

**Key sentence template for papers**:
> "We estimate the RDD using a local linear regression with a triangular kernel and the CCT optimal bandwidth (h = [X]). The point estimate at the cutoff is [β] (SE = [se], p = [p])."

See `references/rdd-reference.md` for geographic RDD, kink designs, donut-hole robustness, discrete running variable RDD, and multi-cutoff/multi-score RDD.

## Common Pitfalls

- **Using global polynomial regression**: High-order global polynomials (e.g., 5th degree) overfit and produce misleading results — always use local linear or local quadratic
- **Not showing the binned scatter plot**: The visual discontinuity is crucial for credibility — always include it
- **Ignoring manipulation**: A failed McCrary test means your RDD is fundamentally compromised — address the sorting concern
- **Reporting only one bandwidth**: Show sensitivity across 50%–150% of optimal bandwidth to demonstrate robustness
- **Using RDD far from cutoff**: RDD estimates are valid only at the cutoff — do not extrapolate to units far from the threshold

## Related Skills & Commands

- **did-analysis**: If treatment doesn't have a sharp threshold, consider DID instead
- **iv-estimation**: Fuzzy RDD is essentially an IV design at the cutoff
- **stats**: Summarize data around the cutoff for the "Data" section
- **/diagnose**: Run RDD validity tests (density, covariate balance, placebo cutoffs)
- **/robustness**: Bandwidth sensitivity, polynomial order, kernel type
- **/plot**: Create publication-quality RDD binned scatter plots
