# RDD — Detailed Reference

## Polynomial Order Selection

Local linear (p=1) is the default and preferred for most applications.
Higher-order polynomials (p=2,3) can overfit away from cutoff.

```r
# Compare polynomial orders
for (p in 1:4) {
  res <- rdrobust(df$y, df$running_var, c = cutoff, p = p)
  cat("p =", p, ": coef =", round(res$coef[1],3),
      ", CI: [", round(res$ci[1,1],3), ",", round(res$ci[1,2],3), "]\n")
}
```

**Recommendation**: Report p=1 as main result; p=2 as robustness.

## Kernel Options

| Kernel | Description | Use |
|--------|-------------|-----|
| Triangular | Linearly declining weights | Default; optimal MSE |
| Uniform | Equal weights within BW | Robustness check |
| Epanechnikov | Parabolic weights | Alternative |

## Regression Kink Design (RKD)

When the slope (not level) of the running variable-outcome relationship changes at the cutoff.

```r
# RKD: test for kink using p=2
rkd <- rdrobust(df$y, df$running_var, c = cutoff, deriv = 1)
summary(rkd)
```

**Example**: Unemployment benefit amount = f(previous wage), kink at wage threshold.

## Geographic / Spatial RDD

Uses geographic boundaries as the discontinuity.

```r
library(rdrobust)
# Distance to boundary as running variable; negative = control side
geo_rdd <- rdrobust(y = df$y, x = df$dist_to_boundary, c = 0)
```

**Key concern**: ensure no other policies also change at the boundary (boundary discontinuity design validity).

## Donut-Hole Robustness

Exclude observations very close to the cutoff (potential manipulation zone).

```r
for (donut in c(0, 1, 2, 3)) {
  df_donut <- df[abs(df$running_var - cutoff) > donut, ]
  res <- rdrobust(df_donut$y, df_donut$running_var, c = cutoff)
  cat("Donut =", donut, ": coef =", round(res$coef[1],3), "\n")
}
```

## CER-Optimal Bandwidth (Coverage Error Rate)

For confidence interval coverage, use CER-optimal bandwidth (slightly wider than MSE-optimal).

```r
bw <- rdbwselect(df$y, df$running_var, c = cutoff, bwselect = "cerrd")
```

## Multiple Testing Correction in RDD Validity Checks

When running many placebo tests, apply Bonferroni or BH correction.

```r
p_values <- c(0.12, 0.08, 0.45, 0.02, 0.67)  # from covariate balance tests
p.adjust(p_values, method = "BH")  # Benjamini-Hochberg
```

## Visualization: Publication-Quality RDD Plot

```r
library(ggplot2)
library(rdrobust)

# Get fitted values from rdrobust for both sides
plot_data <- rdplot(df$y, df$running_var, c = cutoff,
                    nbins = c(20, 20), hide = TRUE)$vars_bins

ggplot(plot_data, aes(x = rdplot_mean_x, y = rdplot_mean_y)) +
  geom_point(color = "steelblue", alpha = 0.7, size = 2) +
  geom_smooth(data = subset(plot_data, rdplot_mean_x < cutoff),
              method = "lm", formula = y ~ poly(x, 1), se = TRUE,
              color = "navy", fill = "lightblue") +
  geom_smooth(data = subset(plot_data, rdplot_mean_x >= cutoff),
              method = "lm", formula = y ~ poly(x, 1), se = TRUE,
              color = "navy", fill = "lightblue") +
  geom_vline(xintercept = cutoff, linetype = "dashed", color = "red") +
  theme_minimal() +
  labs(x = "Running Variable", y = "Outcome",
       title = "Regression Discontinuity Design")
```

## RDD with Discrete Running Variable

When the running variable takes only integer values (e.g., test scores, age in years):

```r
# Cattaneo, Frandsen & Titiunik (2015)
# Use local randomization approach instead of local polynomial
library(rdlocrand)

# Randomization-based RDD
rd_rand <- rdrandinf(df$y, df$running_var, cutoff = cutoff,
                      wl = cutoff - 2, wr = cutoff + 2)  # window around cutoff
summary(rd_rand)

# Window selection
rd_win <- rdwinselect(df$running_var, df[, c("x1", "x2")],
                       cutoff = cutoff, nwindows = 10)
```

**Key difference**: With a discrete running variable, there are mass points at each value, so standard density-based methods (rdrobust) may not work well near the cutoff. The local randomization framework treats units within a small window as if they were randomly assigned.

## Multi-Cutoff / Multi-Score RDD

### Multi-Cutoff RDD

Different groups face different cutoffs on the same running variable.

```r
# Cattaneo, Keele, Titiunik & Vazquez-Bare (2016, 2021)
library(rdmulti)

# Normalize running variable: center each group at its own cutoff
df$rv_normalized <- df$running_var - df$group_cutoff

# Pool all groups with normalized running variable
rdmc_result <- rdmc(
  Y = df$y,
  X = df$rv_normalized,
  C = rep(0, nrow(df)),      # all normalized to 0
  fuzzy = NULL
)
summary(rdmc_result)
```

### Multi-Score RDD (Multiple Running Variables)

Treatment determined by multiple scores (e.g., math AND reading scores must exceed thresholds).

```r
# Cattaneo, Keele, Titiunik & Vazquez-Bare (2024)
library(rdmulti)

# Two running variables, two cutoffs
rdms_result <- rdms(
  Y = df$y,
  X = df$score1,
  X2 = df$score2,
  zvar = df$treatment,
  C = cutoff1,
  C2 = cutoff2
)
summary(rdms_result)
```

## Geographic / Boundary RDD (Extended)

Uses administrative or geographic boundaries as the discontinuity.

```r
# Step 1: Compute distance to boundary
library(sf)
boundary <- st_read("boundary.shp")
df_sf <- st_as_sf(df, coords = c("lon", "lat"), crs = 4326)
df$dist_to_boundary <- as.numeric(st_distance(df_sf, boundary))

# Step 2: Assign sign (negative for control side)
df$dist_signed <- ifelse(df$treated_side, df$dist_to_boundary,
                          -df$dist_to_boundary)

# Step 3: Run RDD with distance as running variable
library(rdrobust)
geo_rdd <- rdrobust(y = df$y, x = df$dist_signed, c = 0)
summary(geo_rdd)

# Step 4: Validate — no other policies change at boundary
for (cov in c("population_density", "income_pre", "school_quality")) {
  res <- rdrobust(df[[cov]], df$dist_signed, c = 0)
  cat(cov, ": p =", res$pv[3], "\n")
}
```

**Key concerns for geographic RDD**:
- Sorting: Can people move across the boundary? (check migration data)
- Compound treatment: Other policies may also change at the same boundary
- Distance measurement: Euclidean vs road distance

## Key Citations

- **Foundational**: Hahn, Todd & Van der Klaauw (2001), *Econometrica*
- **IK bandwidth**: Imbens & Kalyanaraman (2012), *Review of Economic Studies*
- **CCT bandwidth**: Calonico, Cattaneo & Titiunik (2014), *Econometrica*
- **rdrobust package**: Calonico, Cattaneo, Farrell & Titiunik (2017), *Stata Journal*
- **Density test**: Cattaneo, Jansson & Ma (2020), *Journal of Econometrics*
- **Practical guide**: Cattaneo, Idrobo & Titiunik (2020), *A Practical Introduction to RDD*
- **Discrete running variable**: Cattaneo, Frandsen & Titiunik (2015), *Journal of Causal Inference*
- **Multi-cutoff RDD**: Cattaneo, Keele, Titiunik & Vazquez-Bare (2016), *Journal of Politics*
- **Multi-score RDD**: Cattaneo, Keele, Titiunik & Vazquez-Bare (2024), *American Economic Review*
- **Geographic RDD**: Keele & Titiunik (2015), *Political Analysis*

## Stata Package Installation

```stata
* Install rdrobust suite
ssc install rdrobust
ssc install rddensity
ssc install lpdensity
```

## R Package Installation

```r
install.packages(c("rdrobust", "rddensity", "rdlocrand"))
```
