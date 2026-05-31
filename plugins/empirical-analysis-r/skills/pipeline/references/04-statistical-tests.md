# Step 4 — Diagnostic Statistical Tests in R (Deep Reference)

Goal: before interpreting any coefficient, validate the assumptions behind its standard error and identification. The 5 classes — normality, heteroskedasticity, autocorrelation, multicollinearity, stationarity — plus IV / panel / specification tests, cover 90% of applied work.

Each test: **null → R command → output → action if rejected**.

## Contents

1. Normality of residuals
2. Heteroskedasticity
3. Autocorrelation (time series & panel)
4. Cross-sectional dependence (panel)
5. Multicollinearity
6. Stationarity & unit roots (`tseries`, `urca`)
7. Panel unit roots
8. Cointegration
9. Endogeneity / weak IV / overid
10. Panel-specific tests (Hausman, Breusch-Pagan LM)
11. Model specification (RESET, link test)
12. Outlier / leverage / influence

---

## 1. Normality of residuals

```r
library(tseries)

ols <- lm(log_wage ~ training + age + edu + tenure, data = df)
resid_v <- residuals(ols)

# Shapiro-Wilk (N ≤ 5000)
shapiro.test(sample(resid_v, min(5000, length(resid_v))))

# Jarque-Bera (asymptotic)
tseries::jarque.bera.test(resid_v)

# D'Agostino skew & kurtosis
library(moments)
agostino.test(resid_v)
anscombe.test(resid_v)

# Anderson-Darling
nortest::ad.test(resid_v)

# Visual
qqnorm(resid_v); qqline(resid_v, col = "red")
hist(resid_v, breaks = 50)
```

**Action**: with N > 200 OLS is generally fine; small-N or MLE → bootstrap CIs (`car::Boot`).

---

## 2. Heteroskedasticity

```r
library(lmtest); library(sandwich)

# Breusch-Pagan
bptest(ols)

# White's general (squares + cross-products via studentized residuals)
bptest(ols, ~ . + I(fitted(ols)^2), data = df)
# Or use whitestrap or skedastic:
library(skedastic)
white(ols)
goldfeld_quandt(ols)
breusch_pagan(ols, koenker = TRUE)

# Action when rejected — use HC3 (Davidson–MacKinnon recommendation)
coeftest(ols, vcov. = vcovHC(ols, type = "HC3"))

# Cluster-robust (clubSandwich gives small-sample corrections too)
library(clubSandwich)
coef_test(ols, vcov = "CR2", cluster = df$firm_id)
```

---

## 3. Autocorrelation

### Time series

```r
# Durbin-Watson
dwtest(ols)

# Breusch-Godfrey (general AR(p))
bgtest(ols, order = 4)

# Ljung-Box portmanteau
Box.test(resid_v, lag = 8, type = "Ljung-Box")
Box.test(resid_v, lag = 12, type = "Box-Pierce")
```

### Panel

```r
library(plm)
pdata <- pdata.frame(df, index = c("worker_id","year"))
plm_fe <- plm(log_wage ~ training + age + edu + tenure,
              data = pdata, model = "within")

# Wooldridge serial correlation in FE panel
pbgtest(plm_fe)

# Wooldridge for first-differences
pwfdtest(log_wage ~ training + age + edu + tenure,
         data = pdata, h0 = "fd")

# Pesaran cross-sectional dependence
pcdtest(plm_fe, test = "cd")

# Modified Wald for groupwise heteroskedasticity (FE panel)
# Hand-rolled — see plm vignette §6
```

**Action**: HAC (Newey-West) for time-series → `coeftest(ols, vcov. = vcovHAC(ols))`; cluster by entity for panels → `vcov = vcovCR(ols, cluster = df$worker_id, type = "CR2")`.

---

## 4. Cross-sectional dependence (panel)

```r
library(plm)
pcdtest(plm_fe, test = "cd")            # Pesaran CD
pcdtest(plm_fe, test = "lm")            # Breusch-Pagan LM
pcdtest(plm_fe, test = "sclm")          # scaled LM
```

**Action**: Driscoll-Kraay SEs via `vcovSCC()` from `plm`, or `clubSandwich::vcovCR(..., type = "CR2", cluster = df$year)`.

---

## 5. Multicollinearity

```r
library(car)

vif(ols)                                 # generalized VIF for factors
sqrt(vif(ols))                           # sqrt VIF — interpret as coefficient SE inflation

# Condition number
kappa(model.matrix(ols), exact = TRUE)

# Tolerance = 1/VIF
1 / vif(ols)
```

| Threshold | Reading |
|-----------|---------|
| max VIF < 5 | fine |
| 5 ≤ max VIF < 10 | watch |
| max VIF ≥ 10 | severe |
| condition number > 30 | warning |
| condition number > 100 | severe |

---

## 6. Stationarity (time series)

Two complementary directions; run both.

```r
library(tseries); library(urca)

# ADF — Null: unit root; reject ⇒ stationary
adf.test(df$log_wage)
ur.df(df$log_wage, type = "drift", lags = 4)
summary(ur.df(df$log_wage, type = "trend", lags = 4))

# ADF-GLS — more power
ur.ers(df$log_wage, type = "DF-GLS", model = "constant", lag.max = 4)

# KPSS — Null: stationary; FAIL to reject ⇒ stationary
kpss.test(df$log_wage, null = "Level")
kpss.test(df$log_wage, null = "Trend")
ur.kpss(df$log_wage, type = "tau", lags = "short")

# Phillips-Perron
pp.test(df$log_wage)
ur.pp(df$log_wage, type = "Z-tau", model = "trend")

# Zivot-Andrews — allows ONE structural break
ur.za(df$log_wage, model = "intercept", lag = 4)
ur.za(df$log_wage, model = "both",      lag = 4)
```

**Decision** (intersection of ADF + KPSS):

| ADF | KPSS | Conclusion |
|-----|------|------------|
| reject | fail to reject | **stationary** |
| fail to reject | reject | **non-stationary** — first-difference |
| reject | reject | inconclusive (try ZA / structural break) |
| both fail | both fail | insufficient data |

---

## 7. Panel unit roots

```r
library(plm)

# Im-Pesaran-Shin (heterogeneous AR)
purtest(log_wage ~ 1, data = pdata, test = "ips", lags = "AIC")

# Levin-Lin-Chu (homogeneous AR)
purtest(log_wage ~ 1, data = pdata, test = "levinlin", lags = "AIC")

# Maddala-Wu / Choi (Fisher-type)
purtest(log_wage ~ 1, data = pdata, test = "madwu")

# Hadri (Null: stationary)
purtest(log_wage ~ 1, data = pdata, test = "hadri")
```

---

## 8. Cointegration

```r
# Engle-Granger two-step
library(urca)
eg <- ur.df(residuals(lm(y ~ x, data = ts_df)), type = "none", lags = 4)

# Johansen (multivariate)
johansen <- ca.jo(ts_df %>% select(y1, y2, y3),
                  type = "trace", ecdet = "const", K = 2)
summary(johansen)

# Pedroni (panel cointegration — via plm)
pcdtest                        # see plm vignette
# Or via -panelvar- / -tsDyn-
```

---

## 9. Endogeneity / weak IV / overid

`fixest::feols` provides one-stop diagnostics:

```r
library(fixest)
iv <- feols(log_wage ~ age + edu | worker_id + year |
            training ~ draft_lottery + z2,
            data = df, cluster = ~ firm_id)

summary(iv, stage = 1:2)         # both stages
fitstat(iv, ~ ivf + ivf1 + ivwald + sargan + endo)
# - ivf      = first-stage F per endogenous (Olea-Pflueger preferred)
# - ivwald   = Kleibergen-Paap rk Wald (weak-IV under cluster)
# - sargan   = overid test (need overid for it to be informative)
# - endo     = Wu-Hausman endogeneity test
```

`AER::ivreg` is the alternative:

```r
library(AER)
iv_aer <- ivreg(log_wage ~ training + age + edu |
                 draft_lottery + z2 + age + edu, data = df)
summary(iv_aer, vcov. = sandwich, diagnostics = TRUE)
# Reports: weak instruments F, Wu-Hausman, Sargan
```

Anderson-Rubin / weak-IV-robust CI:

```r
library(ivmodel)
ivm <- ivmodel(Y = df$log_wage, D = df$training,
               Z = df %>% select(draft_lottery, z2) %>% as.matrix(),
               X = df %>% select(age, edu)        %>% as.matrix())
AR.test(ivm)            # Anderson-Rubin (weak-IV robust)
CLR(ivm)                # Conditional Likelihood Ratio
```

---

## 10. Panel-specific tests

```r
library(plm)

# Hausman: H0 RE consistent
pdata <- pdata.frame(df, index = c("worker_id","year"))
plm_fe <- plm(log_wage ~ training + age + edu, data = pdata, model = "within")
plm_re <- plm(log_wage ~ training + age + edu, data = pdata, model = "random")
phtest(plm_fe, plm_re)
# p < 0.05 → use FE

# Robust Hausman (when classical fails)
phtest(plm_fe, plm_re, vcov = function(x) vcovHC(x, method = "white2"))

# Breusch-Pagan LM (H0: pooled OLS adequate)
plmtest(plm_re, type = "bp")           # one-way
plmtest(plm_re, type = "kw")           # Honda for unbalanced
plmtest(plm_re, effect = "twoways", type = "ghm")

# F-test of unit FE = 0 (after FE estimation)
pFtest(plm_fe, lm(log_wage ~ training + age + edu, data = df))

# Chow test (structural break)
pooltest(log_wage ~ training + age + edu, data = pdata)
```

---

## 11. Model specification

```r
# Ramsey RESET
resettest(ols, power = 2:3, type = "fitted")
resettest(ols, power = 2:3, type = "regressor")

# Pregibon link test (manual)
yhat <- fitted(ols)
linktest <- lm(df$log_wage ~ yhat + I(yhat^2))
summary(linktest)$coefficients["I(yhat^2)", ]   # if significant → spec wrong

# For GLM (logit/probit)
logit <- glm(employed ~ training + age + edu, data = df, family = binomial)
yhat <- predict(logit, type = "link")
summary(glm(df$employed ~ yhat + I(yhat^2), family = binomial))
```

---

## 12. Outlier / leverage / influence

```r
library(broom)

# All influence measures in one tidy frame
inf_df <- augment(ols) %>%
  mutate(
    high_leverage = .hat       > 2*length(coef(ols))/nrow(df),
    high_resid    = abs(.std.resid) > 3,
    high_cook     = .cooksd    > 4/nrow(df)
  )

# Plot
library(ggplot2)
ggplot(inf_df, aes(.hat, .std.resid, size = .cooksd, color = high_cook)) +
  geom_point(alpha = 0.4) +
  scale_color_manual(values = c("FALSE" = "gray60", "TRUE" = "red")) +
  geom_hline(yintercept = c(-3, 3), linetype = "dashed") +
  labs(x = "Leverage", y = "Studentized residual",
       size = "Cook's D", color = "Cook > 4/n")
ggsave("figures/influence.pdf", width = 7, height = 4.5)

# DFBETAs (per-coefficient influence)
library(car)
dfbetas_v <- dfbetas(ols)
high_dfb_train <- abs(dfbetas_v[, "training"]) > 2/sqrt(nrow(df))
sum(high_dfb_train)

# Re-fit dropping top 1% Cook's D
cook_threshold <- quantile(inf_df$.cooksd, 0.99, na.rm = TRUE)
ols_clean <- update(ols, data = df %>% slice(which(inf_df$.cooksd <= cook_threshold)))
modelsummary::modelsummary(list("All" = ols, "Drop top 1% Cook" = ols_clean))
```

---

## A standard Step-4 diagnostic report

Save to `logs/04_diagnostics.txt`:

```text
=== Diagnostics: log_wage ~ training + age + edu + tenure  (N=5,432) ===
[Normality]   shapiro p=0.08   JB p=0.12              → CLT OK at this N
[Hetero]      bptest p=0.003   white p=0.002           → use HC3 / cluster
[Autocorr]    pbgtest p=0.01                            → cluster by worker_id
[CSD]         pcdtest p=0.40                            → no panel CSD
[Multicoll]   max VIF=3.4   condition number ≈ 14       → OK
[Stationarity] ADF p=0.04   KPSS p=0.07                 → stationary in levels
[Spec]        RESET p=0.30   linktest yhat^2 p=0.45     → spec OK
[Influence]   2 obs flagged Cook>4/N; main coef stable after drop
```

A `purrr::walk` wrapper that emits this report from a fitted model is a useful internal helper for any project — see [`05-modeling.md`](05-modeling.md) for the modelsummary-based version.
