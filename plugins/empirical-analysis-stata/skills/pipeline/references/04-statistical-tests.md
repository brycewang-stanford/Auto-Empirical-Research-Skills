# Step 4 — Diagnostic Statistical Tests in Stata (Deep Reference)

Goal: before interpreting any coefficient, verify the assumptions that prop up its standard error and identification. The 5 classes below — normality, heteroskedasticity, autocorrelation, multicollinearity, stationarity — plus post-estimation IV, panel, and specification tests, cover 90% of applied work.

Each test is presented with **null → command → output to read → action if rejected**.

## Contents

1. Normality of residuals
2. Heteroskedasticity
3. Autocorrelation (time series & panel)
4. Cross-sectional dependence (panel)
5. Multicollinearity
6. Stationarity & unit roots (time series)
7. Panel unit roots
8. Cointegration
9. Endogeneity / weak instruments / overidentification (IV)
10. Panel-specific (Hausman FE vs. RE, Breusch–Pagan LM)
11. Model specification (`ovtest`, `linktest`)
12. Outlier / leverage / influence

---

## 1. Normality of residuals

```stata
quietly reg log_wage training age edu tenure
predict resid, resid

* Shapiro–Wilk (N ≤ 5000)
swilk resid

* Skewness + kurtosis test
sktest resid

* Skewness / kurtosis individually
summarize resid, detail
display "skew=" r(skewness) "  kurt=" r(kurtosis)

* Jarque–Bera (-jb-)
ssc install jb, replace
jb resid
```

**Action**: with N > 200 and OLS, CLT generally rescues you — usually ignore. With small N or MLE, use bootstrap CIs (`bootstrap, reps(1000): ...`) or robust M-estimation (`rreg`).

---

## 2. Heteroskedasticity

```stata
quietly reg log_wage training age edu tenure

* Breusch-Pagan / Cook-Weisberg
estat hettest                         // tests fitted-value form
estat hettest training age edu        // arbitrary form

* White's general test (squares + cross-products)
estat imtest, white

* Goldfeld–Quandt — for known-direction variance change
* (no built-in; hand-roll by sorting and comparing two sub-regressions)
gsort -firm_size
local n3 = floor(_N/3)
quietly reg log_wage training age edu in 1/`n3'
local rss_lo = e(rss); local df_lo = e(df_r)
quietly reg log_wage training age edu in `=`n3'*2+1'/`=_N'
local rss_hi = e(rss); local df_hi = e(df_r)
local F = (`rss_hi'/`df_hi')/(`rss_lo'/`df_lo')
display "GQ F=" `F' "  p=" Ftail(`df_hi', `df_lo', `F')

* Panel — modified Wald for groupwise heteroskedasticity (after xtreg, fe)
xtreg log_wage training age edu, fe
xttest3
```

**Action when rejected**: switch to `vce(robust)` or `vce(cluster id)`. With clusters < 50, also run `boottest`.

---

## 3. Autocorrelation

### Time series

```stata
quietly reg log_wage training age trend

* Durbin–Watson (after time-series regression with -tsset-)
tsset year
quietly reg log_wage training age trend
estat dwatson

* Breusch–Godfrey (general AR(p))
estat bgodfrey, lags(1 2 3 4)

* Durbin's alternative (allows lagged dep var)
estat durbinalt

* Ljung–Box portmanteau
predict resid, resid
wntestq resid, lags(8)
```

### Panel

```stata
xtset worker_id year

* Wooldridge test for serial correlation in panel data
xtserial log_wage training age edu

* Modified Wald test for groupwise hetero (FE)
xtreg log_wage training age edu, fe
xttest3
```

**Action**: HAC (Newey–West) for time series: `newey log_wage training age, lag(4)`; cluster by unit for panels: `vce(cluster worker_id)`; or Driscoll–Kraay: `xtscc log_wage training age, fe`.

---

## 4. Cross-sectional dependence (panel)

```stata
xtset worker_id year

* Pesaran CD test
xtcsd, pesaran abs

* Friedman's R-bar
xtcsd, friedman abs

* Frees' Q-distribution
xtcsd, frees abs
```

**Action**: Driscoll–Kraay SEs (`xtscc`) or common-correlated-effects panel (`xtcce`).

---

## 5. Multicollinearity

```stata
quietly reg log_wage training age edu tenure

* Variance inflation factors
estat vif

* Condition number
* (no estat command; via Mata)
mata: M = st_data(., "training age edu tenure", 0)
mata: M = (J(rows(M),1,1), M)
mata: M = M :- mean(M)
mata: M = M :/ sqrt(diagonal(M' * M / rows(M)))'
mata: cn = sqrt(max(eigenvalues(M' * M)) / min(eigenvalues(M' * M)))
mata: cn
```

| Threshold | Reading |
|-----------|---------|
| max VIF < 5 | fine |
| 5 ≤ max VIF < 10 | watch |
| max VIF ≥ 10 | severe; drop / combine / regularize |
| condition number > 30 | warning |
| condition number > 100 | severe |

**Action**: drop a collinear regressor; build a composite index (`pca`); or accept it (joint hypotheses still valid; individual coefficients unstable).

---

## 6. Stationarity (time series)

Two tests, complementary directions. Run both.

```stata
tsset year

* ADF — Null: unit root; reject (p<0.05) ⇒ stationary
dfuller log_wage, lags(4) trend

* ADF GLS — more power
dfgls log_wage, maxlag(4)

* KPSS — Null: stationary; FAIL to reject ⇒ stationary
kpss log_wage, maxlag(4) notrend

* Phillips–Perron — robust to serial correlation
pperron log_wage, lags(4)

* Zivot–Andrews — allows one structural break in intercept/trend
ssc install zandrews, replace
zandrews log_wage, lagmethod(AIC) maxlag(4) break(intercept)
```

| ADF | KPSS | Conclusion |
|-----|------|------------|
| reject | fail to reject | **stationary** |
| fail to reject | reject | **non-stationary** — first-difference |
| reject | reject | inconclusive — try Zivot–Andrews |
| both fail to reject | both fail | insufficient data |

---

## 7. Panel unit roots

```stata
xtset id year

* Im–Pesaran–Shin (heterogeneous AR coefficients)
xtunitroot ips log_wage, lags(aic 4)

* Levin–Lin–Chu (homogeneous AR)
xtunitroot llc log_wage, lags(aic 4)

* Fisher-type
xtunitroot fisher log_wage, dfuller lags(4)

* Hadri LM (Null: stationary)
xtunitroot hadri log_wage
```

---

## 8. Cointegration

```stata
* Engle–Granger two-step (single equation)
egranger y x, regress trend

* Johansen — multivariate
ssc install vecrank, replace
vecrank y1 y2 y3, lags(2) trend(constant)

* Pedroni / Westerlund for panel cointegration
xtcointtest pedroni y x, trend
xtcointtest westerlund y x, allpanels
```

---

## 9. Endogeneity / weak instruments / overidentification (IV)

```stata
* Estimate via -ivreg2- (preferred — full diagnostic suite by default)
ivreg2 log_wage age edu (training = draft_lottery z2), ///
    cluster(firm_id) first endog(training) ///
    savefirst savefprefix(fs_)

* Outputs to read:
* - First-stage F (each endog) — target ≥ 104 (Lee et al. 2022) or ≥ 10 (rule of thumb)
* - Cragg–Donald F          — minimum eigenvalue, weak-IV in homoskedasticity
* - Kleibergen–Paap rk Wald — weak-IV under heteroskedasticity / clustering
* - Hansen J / Sargan       — overidentification (need overid → multiple instruments)
* - Anderson–Rubin           — weak-IV-robust test of β

* Equivalent commands (built-in):
ivregress 2sls log_wage age edu (training = draft_lottery z2), ///
    vce(cluster firm_id)
estat firststage
estat overid                                     // Sargan / Basmann
estat endogenous                                 // Wu-Hausman + Durbin

* Limited Information ML (less biased w/ weak IV)
ivregress liml log_wage age edu (training = draft_lottery z2), ///
    vce(cluster firm_id)

* Continuously-updating GMM
ivregress gmm log_wage age edu (training = draft_lottery z2), ///
    wmatrix(cluster firm_id) vce(cluster firm_id)

* Anderson–Rubin confidence set
ssc install weakiv, replace
weakiv log_wage age edu (training = draft_lottery), strong

* Conley spatial HAC SEs (geographic instruments)
ivreg2 log_wage age (training = z), bw(5) kernel(uniform)
```

---

## 10. Panel-specific tests

```stata
xtset worker_id year

quietly xtreg log_wage training age edu, fe
estimates store fe
quietly xtreg log_wage training age edu, re
estimates store re

* Hausman (H0: RE consistent — use RE)
hausman fe re, sigmamore

* Sigmamore is recommended; sigmaless is alternative.
* If p < 0.05, RE is inconsistent — use FE.

* Robust Hausman (when classical Hausman fails / non-positive variance matrix)
ssc install xtoverid, replace
xtoverid

* Breusch–Pagan LM (H0: pooled OLS adequate, no random effects)
quietly xtreg log_wage training age edu, re
xttest0

* F-test of unit FE = 0 (after xtreg, fe)
quietly xtreg log_wage training age edu, fe
* The F-statistic for "all u_i = 0" is reported in the output

* Chow test for structural break
ssc install chowtest, replace
chowtest log_wage training age edu, group(post_2010)
```

---

## 11. Model specification

```stata
quietly reg log_wage training age edu tenure

* Ramsey RESET — H0: no functional-form misspecification
estat ovtest

* Stata's "linktest" — refits with yhat and yhat^2 as regressors
linktest

* Pregibon's link test for non-linear models
quietly logit employed training age edu
linktest

* Heckman selection bias indirect test (via Mills ratio)
* See Step 5 / references/05-modeling.md §11 for the full Heckman recipe.
```

---

## 12. Outlier / leverage / influence

```stata
quietly reg log_wage training age edu tenure

* Leverage
predict lev, leverage
gen high_lev = lev > 2*5/_N                      // p=5; threshold 2p/N

* Studentized residuals
predict stud_r, rstudent
gen high_resid = abs(stud_r) > 3

* Cook's distance
predict cooks_d, cooksd
gen high_cook = cooks_d > 4/_N

* DFFITS
predict dffits_v, dfits
gen high_dff = abs(dffits_v) > 2*sqrt(5/_N)

* DFBETAs (per-coefficient influence)
dfbeta training
gen high_dfb_train = abs(_dfbeta_1) > 2/sqrt(_N)

* Tabular summary
count if high_lev
count if high_resid
count if high_cook
count if high_dff
count if high_dfb_train

* Visualize: leverage vs. studentized residual (sized by Cook's D)
twoway scatter stud_r lev [aweight=cooks_d], msymbol(oh) ///
    yline(3 -3, lpattern(dash)) ///
    title("Leverage-residual plot")
graph export "figures/influence.pdf", replace

* Robustness re-fit dropping influential obs
preserve
    drop if high_cook == 1
    reg log_wage training age edu tenure, vce(cluster firm_id)
restore
```

---

## A standard Step-4 diagnostic log

Before moving to Step 5, generate a one-page diagnostic report:

```text
=== Diagnostics for log_wage ~ training + age + edu + tenure  (N=5,432) ===
[Normality]   swilk p=0.08   sktest p=0.12  → CLT OK at this N
[Hetero]      hettest p=0.003  imtest white p=0.002  → use cluster SEs
[Autocorr]    xtserial p=0.01           → cluster by worker_id
[CSD]         pesaran p=0.40            → no cross-sectional dependence
[Multicoll]   max VIF = 3.4  cond# ≈ 14  → OK
[Stationarity] ADF p=0.04  KPSS p=0.07  → stationary in levels
[Spec]        ovtest p=0.30   linktest yhat^2 p=0.45  → spec OK
[Influence]   2 obs flagged Cook>4/N; main coef stable after drop
```

Save this to `logs/diagnostics.log` so reviewers can see the choice of SE family is principled.
