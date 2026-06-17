---
name: time-series
description: |
  Econometrics skill for time series analysis. Activates when the user asks about:
  "time series", "stationarity", "unit root test", "ADF test", "KPSS test",
  "ARIMA", "ARMA", "autocorrelation", "ACF", "PACF", "VAR model", "VECM",
  "Granger causality", "cointegration", "impulse response function", "forecast",
  "seasonal decomposition", "ARCH", "GARCH", "时间序列", "平稳性检验", "单位根",
  "自回归", "格兰杰因果", "协整", "脉冲响应", "预测", "向量自回归"
---

# Time Series Analysis Skill

This skill provides guidance for univariate and multivariate time series analysis in empirical economics. It covers stationarity testing, ARIMA modeling, VAR/VECM systems, cointegration, and Granger causality.

## Analysis Workflow

### Step 1: Exploratory Inspection
- Plot the series (level, first difference, log)
- Examine ACF and PACF plots to identify dependence structure
- Check for obvious trends, seasonality, structural breaks

### Step 2: Stationarity Testing
Always test for unit roots before modeling. Preferred approach:
1. ADF test (H₀: unit root present)
2. KPSS test (H₀: series is stationary)
3. If ADF rejects AND KPSS fails to reject → stationary (I(0))
4. If both suggest non-stationary → take first difference, retest

**ADF vs KPSS Conflict Resolution**: When ADF fails to reject (suggests unit root) but KPSS also fails to reject (suggests stationary), the tests disagree. Recommended approach: (a) check for structural breaks — a break can make a stationary series look like it has a unit root; (b) use Zivot-Andrews test to allow for one structural break; (c) examine the series visually and consider economic theory. When in doubt, err on the side of differencing to avoid spurious regressions.

### Step 3: Model Selection
- **Univariate**: ARIMA(p,d,q) based on AIC/BIC and ACF/PACF
- **Multivariate, no cointegration**: VAR in differences
- **Multivariate, with cointegration**: VECM (VAR in error-correction form)

### Step 4: Estimation and Diagnostics
- Check residual white noise (Ljung-Box test)
- Test for parameter stability (CUSUM)
- Impulse response functions for structural interpretation

### Step 5: Forecasting (if applicable)
- Report RMSE and MAE on holdout sample
- State forecast horizon and confidence intervals

## Quick Code Templates

### Stationarity Tests

```python
# Python
from statsmodels.tsa.stattools import adfuller, kpss

# ADF test
adf_result = adfuller(series, autolag='AIC')
print(f"ADF stat: {adf_result[0]:.4f}, p-value: {adf_result[1]:.4f}")
print(f"Critical values: {adf_result[4]}")

# KPSS test
kpss_result = kpss(series, regression='c', nlags='auto')
print(f"KPSS stat: {kpss_result[0]:.4f}, p-value: {kpss_result[1]:.4f}")
```

```r
# R
library(tseries); library(urca)
adf.test(series)
kpss.test(series, null = "Level")
```

```stata
* Stata
dfuller series, lags(4) regress
kpss series
```

### ARIMA Model

```python
# Python — auto order selection
from statsmodels.tsa.arima.model import ARIMA
import itertools

# Manual
model = ARIMA(series, order=(1, 1, 1)).fit()
print(model.summary())

# Forecast
forecast = model.forecast(steps=12)
```

```r
# R
library(forecast)
model <- auto.arima(series, ic = "aic")
summary(model)
forecast(model, h = 12)
```

```stata
* Stata
arima series, arima(1,1,1)
predict yhat, xb
```

### VAR Model

```python
# Python
from statsmodels.tsa.api import VAR

model = VAR(data_matrix)
lag_order = model.select_order(maxlags=8)
print(lag_order.summary())

results = model.fit(lag_order.aic)
print(results.summary())

# Granger causality
results.test_causality('y1', ['y2'], kind='f')

# Impulse response
irf = results.irf(periods=10)
irf.plot(orth=True)
```

```r
# R
library(vars)
VARselect(data_matrix, lag.max = 8, type = "const")
var_model <- VAR(data_matrix, p = 2, type = "const")
causality(var_model, cause = "y2")
irf(var_model, impulse = "y2", response = "y1", n.ahead = 10)
```

## Key Decision Rules

| Finding | Implication |
|---------|-------------|
| All series I(0) | Estimate VAR in levels |
| All series I(1), no cointegration | Estimate VAR in first differences |
| All series I(1), cointegration found | Estimate VECM |
| Mixed orders of integration | Cannot use standard VAR/VECM; use ARDL bounds test |

## ARIMA Order Selection Guide

- **AR(p)**: PACF cuts off after lag p, ACF decays
- **MA(q)**: ACF cuts off after lag q, PACF decays
- **ARMA(p,q)**: Both ACF and PACF decay gradually
- Use AIC for forecasting, BIC for parsimony/inference
- Always check residual ACF for remaining autocorrelation

### Residual Diagnostics (Ljung-Box White Noise Test)

```python
# Python — Ljung-Box test for residual autocorrelation
from statsmodels.stats.diagnostic import acorr_ljungbox

# After fitting ARIMA model:
residuals = model.resid
lb_result = acorr_ljungbox(residuals, lags=[10, 20], return_df=True)
print(lb_result)
# If p-value > 0.05 at all lags → residuals are white noise (good)
```

```r
# R — Ljung-Box test
Box.test(residuals(model), lag = 10, type = "Ljung-Box")
# p > 0.05 → no remaining autocorrelation
```

```stata
* Stata — Ljung-Box (portmanteau) test
* After arima estimation:
wntestq residuals, lags(10)
* Q-stat with p > 0.05 → white noise residuals
```

### ARCH/GARCH Models (Volatility Clustering)

Use when residuals exhibit time-varying variance (heteroskedasticity that clusters over time). Common in financial and macroeconomic data.

```python
# Python — GARCH(1,1) using arch library
from arch import arch_model

# First, fit mean model (e.g., AR(1)) and extract residuals
# Then model the conditional variance:
garch_model = arch_model(series, vol='GARCH', p=1, q=1, dist='normal')
garch_result = garch_model.fit(disp='off')
print(garch_result.summary())

# Extract conditional volatility
cond_vol = garch_result.conditional_volatility
# ARCH LM test for remaining ARCH effects:
from arch.unitroot import VarianceRatio
from statsmodels.stats.diagnostic import het_arch
lm_stat, lm_pval, _, _ = het_arch(garch_result.resid)
print(f"ARCH LM test p-value: {lm_pval:.4f}")  # should be > 0.05
```

```r
# R — GARCH(1,1) using rugarch
library(rugarch)

spec <- ugarchspec(
  variance.model = list(model = "sGARCH", garchOrder = c(1, 1)),
  mean.model     = list(armaOrder = c(1, 0), include.mean = TRUE),
  distribution.model = "norm"
)
fit <- ugarchfit(spec = spec, data = series)
show(fit)

# Test for remaining ARCH effects
# ArchTest(residuals(fit), lags = 10)  # from FinTS package
```

```stata
* Stata — ARCH/GARCH
* First run mean model:
arima series, arima(1,0,0)
predict resid_mean, residuals

* ARCH LM test:
estat archlm, lags(1 2 5)

* Fit GARCH(1,1):
arch series, arch(1) garch(1) ar(1)
```

For cointegration tests (Johansen, Engle-Granger), VECM specification, and structural break tests, see `references/time-series-reference.md`.

## Common Pitfalls

- **Regressing non-stationary series on each other**: Produces spurious regression — always test for unit roots first
- **Using VAR in levels when series are I(1) without cointegration**: Leads to invalid inference — difference the data or use VECM
- **Wrong lag length**: Too few lags → autocorrelated residuals; too many → overfitting. Use information criteria
- **Confusing Granger causality with true causality**: Granger causality is about predictive content, not causal mechanisms
- **Ignoring structural breaks**: A break can mimic a unit root — use Zivot-Andrews test, which allows for one endogenous break under the alternative:

```r
# R — Zivot-Andrews test (allows break under stationarity alternative)
library(urca)
za <- ur.za(series, model = "both", lag = 4)
summary(za)
# If test statistic < critical value → reject unit root even with break
# za@teststat gives statistic; za@cval gives 1%, 5%, 10% critical values
```

```python
# Python — Zivot-Andrews test
from statsmodels.tsa.stattools import zivot_andrews

za_stat, pval, cvdict, bpindex, baselag = zivot_andrews(series, maxlag=4, regression='ct')
print(f"ZA stat: {za_stat:.4f}, p-value: {pval:.4f}, break at index: {bpindex}")
# pval < 0.05 → series is stationary with one structural break
```

## Related Skills & Commands

- **panel-data**: For panel data with both cross-sectional and time dimensions
- **ols-regression**: For cross-sectional analysis without time dependence
- **/diagnose**: Run time series diagnostics (stationarity, ARCH effects, stability)
- **/robustness**: Test robustness to lag length, sample period, and model specification
- **/plot**: Create time series plots, ACF/PACF diagrams, and IRF charts
