# Time Series — Detailed Reference

## Cointegration Analysis

### Engle-Granger Two-Step Method (bivariate)

```python
# Python
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

# Step 1: Regress y on x
model = sm.OLS(y, sm.add_constant(x)).fit()
residuals = model.resid

# Step 2: Test residuals for stationarity
adf_resid = adfuller(residuals, maxlag=4, regression='nc')
print(f"EG test stat: {adf_resid[0]:.4f}, p-value: {adf_resid[1]:.4f}")
# p < 0.05 → cointegrated
```

```r
library(tseries)
# Step 1: OLS
ols_resid <- residuals(lm(y ~ x))
# Step 2: ADF on residuals
adf.test(ols_resid)
```

### Johansen Trace / Max-Eigenvalue Test (multivariate)

```python
from statsmodels.tsa.vector_ar.vecm import coint_johansen

result = coint_johansen(data_matrix, det_order=0, k_ar_diff=2)
print("Trace statistics:\n", result.lr1)
print("Critical values (90%, 95%, 99%):\n", result.cvt)
print("Max-eigenvalue statistics:\n", result.lr2)
print("Critical values:\n", result.cvm)
```

```r
library(urca)
jo_test <- ca.jo(data_matrix, type = "trace", ecdet = "const", K = 2)
summary(jo_test)
```

```stata
vecrank series1 series2 series3, lags(2) trend(constant)
```

## VECM Estimation

```python
from statsmodels.tsa.vector_ar.vecm import VECM

vecm = VECM(data_matrix, k_ar_diff=2, coint_rank=1, deterministic='ci')
vecm_fit = vecm.fit()
print(vecm_fit.summary())

# Impulse response from VECM
irf = vecm_fit.irf(periods=12)
irf.plot()
```

```r
library(vars)
# Convert Johansen result to VECM
vec_model <- vec2var(jo_test, r = 1)
irf(vec_model, impulse = "y2", response = "y1", n.ahead = 12)
```

## ARCH/GARCH Models (Volatility)

```python
from arch import arch_model

# GARCH(1,1)
gm = arch_model(returns, vol='Garch', p=1, q=1, dist='normal')
gm_fit = gm.fit()
print(gm_fit.summary())

# EGARCH for asymmetric effects
em = arch_model(returns, vol='EGARCH', p=1, q=1)
em_fit = em.fit()
```

```r
library(rugarch)
spec <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
                   mean.model = list(armaOrder = c(1, 0)))
fit <- ugarchfit(spec, returns)
show(fit)
```

```stata
arch returns, arch(1) garch(1)
```

## Structural Break Tests

### Chow Test (known break date)

```python
# Manual: split sample and F-test
n1, n2 = len(pre_break), len(post_break)
model_full = sm.OLS(y, X).fit()
model_pre  = sm.OLS(y_pre, X_pre).fit()
model_post = sm.OLS(y_post, X_post).fit()

k = X.shape[1]
F = ((model_full.ssr - model_pre.ssr - model_post.ssr) / k) / \
    ((model_pre.ssr + model_post.ssr) / (n1 + n2 - 2*k))
```

### Zivot-Andrews (unknown break date)

```python
from statsmodels.tsa.stattools import zivot_andrews
za = zivot_andrews(series, maxlag=4, regression='ct')
print(f"ZA stat: {za[0]:.4f}, break at: {za[4]}")
```

```r
library(strucchange)
breakpoints(y ~ x)
```

## Seasonal Decomposition

```python
from statsmodels.tsa.seasonal import seasonal_decompose

decomp = seasonal_decompose(series, model='additive', period=12)
decomp.plot()

# STL decomposition (robust)
from statsmodels.tsa.seasonal import STL
stl = STL(series, period=12, robust=True).fit()
stl.plot()
```

```r
decompose(ts_object, type = "additive")
# or
stl(ts_object, s.window = "periodic")
```

## Model Diagnostics

### Ljung-Box Test (residual autocorrelation)

```python
from statsmodels.stats.diagnostic import acorr_ljungbox
lb = acorr_ljungbox(model.resid, lags=[10, 20], return_df=True)
print(lb)
# p > 0.05 → residuals are white noise (good)
```

```r
Box.test(residuals(model), lag = 10, type = "Ljung-Box")
```

### Information Criteria for Lag Selection

```python
# VAR lag selection
from statsmodels.tsa.api import VAR
var_model = VAR(data)
lag_results = var_model.select_order(maxlags=12)
print(lag_results.summary())
# Compare AIC (forecasting), BIC (parsimony), HQIC
```

## Reporting Guidelines for Academic Papers

1. **Unit root tests**: Always report ADF and KPSS together with lag lengths
2. **Cointegration**: Report trace and max-eigenvalue statistics with critical values
3. **VAR**: State lag order selection criterion and number of lags chosen
4. **Granger causality**: Report F-statistic and p-value; clarify direction tested
5. **IRF**: Show orthogonalized IRF with 95% confidence bands; state ordering assumption
6. **Forecast evaluation**: Report RMSE, MAE on out-of-sample period
