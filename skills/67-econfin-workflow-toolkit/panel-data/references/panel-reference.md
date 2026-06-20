# Panel Data — Detailed Reference

## First-Difference Estimator

Differences out time-invariant unobserved heterogeneity like FE, but useful when T=2.

```python
# Python
df_sorted = df.sort_values(['entity_id', 'time_var'])
df_diff = df_sorted.groupby('entity_id').diff().dropna()
model_fd = sm.OLS(df_diff['y'], sm.add_constant(df_diff[['x1', 'x2']])).fit(cov_type='HC3')
```

```r
plm(y ~ x1 + x2, data = panel_df, model = "fd")
```

```stata
xtreg y x1 x2, fd cluster(entity_id)
```

## Dynamic Panel Models (Arellano-Bond GMM)

Use when lagged dependent variable is a regressor (creates endogeneity with FE).

```r
library(plm)
# Arellano-Bond difference GMM
ab_model <- pgmm(y ~ lag(y,1) + x1 | lag(y, 2:4),
                 data = panel_df, effect = "individual",
                 model = "twosteps")
summary(ab_model, robust = TRUE)
```

```stata
* Arellano-Bond (xtabond2 from SSC)
xtabond2 y L.y x1, gmm(L.y, lag(2 4)) iv(x1) twostep robust
```

Key diagnostics for GMM:
- **AR(1)** test: should be significant (first-order autocorrelation expected)
- **AR(2)** test: should be insignificant (no second-order autocorrelation)
- **Hansen/Sargan** test: p > 0.05 → instruments valid (don't over-identify)

## Mundlak / Correlated Random Effects

Allows estimating time-invariant variable effects while controlling for correlation between αᵢ and X.

```r
# Add group means of time-varying variables
panel_df$x1_mean <- ave(panel_df$x1, panel_df$entity_id)
panel_df$x2_mean <- ave(panel_df$x2, panel_df$entity_id)

mundlak <- plm(y ~ x1 + x2 + x1_mean + x2_mean + time_invariant_var,
               data = panel_df, model = "random")
summary(mundlak)
```

## Driscoll-Kraay Standard Errors (spatial/temporal dependence)

```r
library(lmtest); library(sandwich)
coeftest(fe_model, vcov = vcovSCC(fe_model, type = "HC3", maxlag = 3))
```

```stata
xtscc y x1 x2, fe lag(3)
```

## Testing for Poolability

### F-test for Fixed Effects (are unit FEs jointly significant?)

```r
pFtest(fe_model, pooled_model)
# p < 0.05 → FE are jointly significant, pooled OLS is inappropriate
```

```stata
xtreg y x1 x2, fe
testparm i.entity_id
```

### Breusch-Pagan LM Test (random effects vs pooled OLS)

```r
plmtest(re_model, type = "bp")
# p < 0.05 → significant individual effects, RE preferred over pooled OLS
```

## Serial Correlation Tests in Panels

### Wooldridge Test (H₀: no serial correlation in FE residuals)

```r
library(plm)
pbgtest(fe_model)
# or
pwtest(fe_model)
```

```stata
xtserial y x1 x2
```

## Cross-Sectional Dependence Tests

Important for macro panels (N small, T large).

```r
library(plm)
pcdtest(fe_model, test = "cd")  # Pesaran CD test
# p < 0.05 → cross-sectional dependence present → use Driscoll-Kraay SE
```

```stata
xtcsd, pesaran abs
```

## Panel Unit Root Tests

For macro panels with large T, test stationarity at the panel level.

```r
library(plm)
purtest(panel_df[, "y"], test = "ips", exo = "intercept")  # Im-Pesaran-Shin
purtest(panel_df[, "y"], test = "levinlin", exo = "intercept")  # Levin-Lin-Chu
```

```stata
xtunitroot ips y
xtunitroot llc y
```

## Panel Cointegration (Pedroni, Kao)

```stata
xtcointtest pedroni y x1 x2, trend lags(aic 4)
xtcointtest kao y x1 x2
```

## Interpretation Checklist

- [ ] Entity effects significant? (F-test / LM test)
- [ ] Time effects significant? (F-test on time dummies)
- [ ] Hausman test reported?
- [ ] SE clustering level stated?
- [ ] Serial correlation tested?
- [ ] Cross-sectional dependence tested (if macro panel)?
- [ ] N, T, and total observations stated?
