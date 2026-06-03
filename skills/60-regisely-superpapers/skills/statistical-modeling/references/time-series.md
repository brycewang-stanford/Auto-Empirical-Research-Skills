# Time-Series Methods

Starting-point reference for data ordered in time — single series, multiple series, or series with complex dynamics. **Not exhaustive.**

## Stationarity and Unit Roots

**Why it matters:** Most classical time-series methods (ARIMA, VAR) require stationarity. Nonstationary series produce spurious regressions unless handled explicitly.

**Tests:**
- **Augmented Dickey-Fuller (ADF):** Null is unit root. Underpowered with short series.
- **Phillips-Perron (PP):** Nonparametric correction for serial correlation; alternative to ADF.
- **KPSS:** Null is stationarity (opposite of ADF). Use jointly with ADF for confirmation.
- **Zivot-Andrews:** Unit root test allowing for a single structural break.

**Practical advice:**
- Run ADF and KPSS together. If ADF rejects and KPSS does not reject, the series is stationary.
- If a series has a trend, test with a trend term in the regression.
- If nonstationary, difference the series (and test the differenced version).

**R packages:** `urca`, `tseries`, `forecast::ndiffs`
**Python packages:** `statsmodels.tsa.stattools` (adfuller, kpss)

## ARIMA / SARIMA

**When to use:** Univariate forecasting or modeling a single stationary (after differencing) series.

**Specification:** `ARIMA(p, d, q)` — AR order p, differencing order d, MA order q. Seasonal version adds `(P, D, Q)_s`.

**Box-Jenkins methodology:**
1. Plot the series; look for trend, seasonality, variance changes
2. Transform if variance is non-constant (log, Box-Cox)
3. Difference to achieve stationarity
4. Inspect ACF and PACF of differenced series to guess orders
5. Fit candidate models; compare via AIC/BIC
6. Diagnostic checks on residuals (Ljung-Box, normality)

**Model selection:**
- **AIC:** Trades fit and parsimony; better for out-of-sample forecasting
- **BIC:** Stronger penalty for complexity; better for identifying the "true" model in large samples
- **Auto-ARIMA:** Automated search (use with caution; always inspect final model)

**Diagnostics:**
- **Ljung-Box test:** Joint test for residual autocorrelation
- **Residual ACF:** Should be within confidence bands
- **Normality of residuals:** For prediction intervals

**R packages:** `forecast`, `fable`
**Python packages:** `statsmodels.tsa.arima.model`, `pmdarima`

## VAR and VECM

**When to use:** Multiple time series with potential mutual influence — impulse responses, forecast error variance decomposition, Granger causality.

### VAR (Vector Autoregression)

**Specification:** `y_t = c + A_1 y_{t-1} + ... + A_p y_{t-p} + ε_t`

**Steps:**
1. Test each series for unit roots
2. If all stationary, fit VAR in levels
3. If nonstationary but not cointegrated, difference all series and fit VAR in differences
4. If cointegrated, fit VECM instead

**Lag selection:** AIC, BIC, HQ criteria. BIC tends to select parsimonious models.

**Impulse response functions:**
- **Orthogonalized (Cholesky):** Order matters; impose ordering by economic theory
- **Generalized IRFs (Pesaran-Shin):** Order-invariant; different interpretation
- **Sign-restricted IRFs:** Structural identification via sign restrictions on responses

**Forecast error variance decomposition:** How much of each series' forecast error variance comes from shocks to other series.

### VECM (Vector Error Correction Model)

**When to use:** Multiple nonstationary series that are cointegrated — they share a common long-run equilibrium.

**Cointegration tests:**
- **Engle-Granger:** Single equation; simple but inefficient for more than two variables
- **Johansen trace / max-eigenvalue:** Full system test; identifies number of cointegrating relationships

**Structure:** VECM decomposes dynamics into short-run adjustments and long-run equilibrium corrections.

**R packages:** `vars`, `tsDyn`, `urca` (for Johansen)
**Python packages:** `statsmodels.tsa.vector_ar`, `linearmodels`

## GARCH Family

**When to use:** Volatility clustering in financial returns, risk modeling, value-at-risk.

**Models:**
- **GARCH(1,1):** Baseline model; captures persistence in conditional variance
- **EGARCH:** Exponential GARCH; allows asymmetric response to positive and negative shocks
- **GJR-GARCH:** Alternative asymmetric specification
- **Multivariate GARCH (DCC, BEKK):** Time-varying covariances between multiple series

**Specification:**
- Mean equation: ARMA process for returns
- Variance equation: GARCH process for conditional variance

**Diagnostics:**
- **ARCH-LM test:** For remaining ARCH effects in residuals
- **Ljung-Box on squared residuals:** For conditional variance misspecification
- **Distributional assumptions:** Normal often rejected; try t-distribution or skewed-t for returns

**R packages:** `rugarch`, `rmgarch`
**Python packages:** `arch`

## State-Space Models

**When to use:** Flexible specification with latent components — trends, seasonals, cycles, regression coefficients that evolve over time.

**Common structures:**
- **Local level:** Random walk in the latent mean
- **Local linear trend:** Random walk in level and slope
- **Basic structural model:** Trend, seasonal, cycle, irregular components
- **Time-varying parameters:** Regression coefficients as latent states

**Estimation:** Kalman filter and smoother for Gaussian linear models; particle filters for nonlinear or non-Gaussian.

**Advantages:**
- Natural handling of missing data
- Explicit uncertainty quantification for latent states
- Model structural breaks as time-varying components

**Bayesian alternative:** Bayesian structural time series (BSTS) for causal impact analysis with state-space models.

**R packages:** `dlm`, `KFAS`, `bsts`, `MARSS`
**Python packages:** `statsmodels.tsa.statespace`, `pybsts`

## Structural Breaks

**When to use:** The relationship between variables changes at some point in time.

**Tests:**
- **Chow test:** Break date known a priori
- **Quandt-Andrews / QLR:** Single unknown break; supremum Wald, LM, or LR statistic
- **Bai-Perron:** Multiple unknown breaks, with sequential tests for number of breaks

**Caution:** Structural break tests can have poor size properties in small samples; bootstrap critical values when possible.

**R packages:** `strucchange`, `breakpoint`
**Python packages:** `ruptures`

## High-Frequency and Realized Volatility

**When to use:** Intraday data (tick, minute, hour), realized variance, microstructure noise.

**Key concepts:**
- **Realized variance:** Sum of squared intraday returns; estimator of integrated variance
- **Microstructure noise:** Bid-ask bounce, price discreteness; biases naive realized variance
- **Pre-averaging / two-scale estimators:** Corrections for microstructure noise
- **Jump detection:** Barndorff-Nielsen-Shephard bipower variation

**R packages:** `highfrequency`
**Python packages:** custom implementations; check CRAN/PyPI for current tooling

## Not in This Reference

Wavelet methods, nonlinear time series (SETAR, STAR), long-memory models (ARFIMA), machine-learning forecasting (Prophet, NBEATS, transformer-based models), continuous-time stochastic processes. Use the modeling process from `modeling-process.md`.
