# Step 5 — Empirical Modeling in Stata (Deep Reference)

Goal: estimate the causal / predictive relationship of interest with the right command for the identification strategy. This file is the deep catalog — every classical estimator with its canonical Stata syntax, kwargs, standard-error family, and post-estimation diagnostics.

## Contents

1. OLS, WLS, robust / cluster SEs, multi-way clustering
2. Panel data — `xtreg`, `areg`, `reghdfe`
3. Binary / ordinal / count outcomes — `logit`, `probit`, `ologit`, `mlogit`, `poisson`, `nbreg`, `ppmlhdfe`
4. Instrumental variables — `ivreg2`, `ivregress`, `ivreghdfe`
5. Difference-in-differences — 2×2, TWFE, event study, `csdid`, `eventstudyinteract`, `did_imputation`, `sdid`, `did_multiplegt_dyn`
6. Regression discontinuity — `rdrobust`, `rddensity`, `rdmc`, `rdplot`, `rdbwselect`
7. Synthetic control — `synth`, `synth_runner`
8. Matching & reweighting — `psmatch2`, `teffects psmatch / ipw / ipwra / aipw`, `ebalance`, `cem`
9. Heckman selection
10. Quantile regression — `qreg`, `sqreg`, `bsqreg`, `iqreg`
11. Survival / duration
12. SEM / GSEM (when needed for mediation)

---

## 1. OLS

```stata
* Default
reg log_wage training age edu tenure

* Robust (HC1; for HC3 use -robreg- or -bcse-)
reg log_wage training age edu tenure, vce(robust)

* Cluster
reg log_wage training age edu tenure, vce(cluster firm_id)

* Multi-way clustering — built-in via -ivreg2- or -reghdfe-
reghdfe log_wage training age edu tenure, ///
    noabsorb vce(cluster worker_id firm_id)

* Bootstrap
reg log_wage training age edu tenure, vce(bootstrap, reps(1000) seed(42))

* HAC / Newey-West (time series; tsset first)
newey log_wage training age edu, lag(4)

* WLS — pass weights as analytic
reg log_wage training age edu [aweight=svywt]

* Constrained OLS (test joint hypotheses post-fit)
reg log_wage training age edu tenure, vce(cluster firm_id)
test training = 0.05
test training age                              // joint
test training - female = 0
lincom training + 0.5*age                     // linear combination
```

### Margins (always after non-linear or interaction models)

```stata
margins, dydx(training) atmeans
margins, dydx(*) at(age=(20(10)60))
marginsplot, recast(connected)
```

---

## 2. Panel data

**Default tool**: `reghdfe` (fastest, handles multiple HD FE, multi-way clustering). **Alternatives**: `xtreg`, `areg`.

```stata
xtset worker_id year

* 2a. xtreg, fe — classical within transform
xtreg log_wage training age edu tenure, fe vce(cluster worker_id)

* 2b. xtreg, re — random effects
xtreg log_wage training age edu tenure, re vce(cluster worker_id)

* 2c. xtreg, be — between
xtreg log_wage training age edu tenure, be

* 2d. First differences (xtreg has no fd; use D. operator + reg)
xtset worker_id year
reg D.log_wage D.training D.age D.edu, vce(cluster worker_id)

* 2e. areg — single-dim FE absorb (predates reghdfe)
areg log_wage training age edu tenure, absorb(worker_id) vce(cluster worker_id)

* 2f. reghdfe — multi-dim FE, multi-way cluster, fastest for big panels
reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster worker_id)

* High-dim interaction FE
reghdfe log_wage training, absorb(worker_id i.industry#i.year) ///
    vce(cluster firm_id)

* Multi-way clustering
reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster worker_id firm_id)

* Weighted
reghdfe log_wage training [aweight=svywt], absorb(worker_id year)

* Save residuals
reghdfe log_wage training, absorb(worker_id year) residuals(resid_fe)
```

**Hausman & friends** — see references/04 §10 for FE vs. RE testing.

---

## 3. Binary / ordinal / count outcomes

```stata
* Logit — never interpret coefficients directly; use margins
logit employed training age edu, vce(cluster firm_id)
margins, dydx(*)                                       // average marginal effects
margins, dydx(training) atmeans                        // ME at means
estat classification                                   // sensitivity/specificity
estat gof                                              // Hosmer-Lemeshow (use sparingly)

* Probit
probit employed training age edu, vce(cluster firm_id)
margins, dydx(*)

* Ordered logit (3+ ordered outcome)
ologit rating training age edu, vce(cluster firm_id)
margins, dydx(*) predict(outcome(2))                   // ME for category 2

* Multinomial logit
mlogit job_choice training age edu, baseoutcome(0) vce(cluster firm_id)
margins, dydx(*) predict(outcome(1))                   // ME for outcome 1

* Poisson with HD FE — use ppmlhdfe (handles separation, clustering)
ppmlhdfe citations training age, absorb(firm_id year) ///
    cluster(firm_id)

* Negative binomial (count w/ overdispersion)
nbreg citations training age, vce(cluster firm_id)
estat ic                                               // AIC / BIC vs. poisson

* Zero-inflated counts
zinb citations training age, inflate(_cons) vce(cluster firm_id)

* Beta regression (proportions in (0,1))
betareg mkt_share training age edu                    // requires -betareg- (older) or
zoib   mkt_share training age edu, fixed(0 1)         // ssc install zoib
```

---

## 4. Instrumental variables

`ivreg2` is the de-facto standard in applied work — full diagnostic suite by default. Built-in `ivregress` works, but you'll pair it with `estat firststage` and `estat overid`.

```stata
* 4a. ivreg2 — full output: first stage, weak-IV stats, overid, endogeneity
ivreg2 log_wage age edu (training = draft_lottery z2 z3), ///
    cluster(firm_id) ///
    first ///                                          // print first-stage
    endog(training) ///                                // Wu-Hausman
    savefirst savefprefix(fs_)                         // save first-stage estimates

* Outputs to read:
* - First-stage F-statistic — target ≥ 104 (Lee et al. 2022) or ≥ 10 rule of thumb
* - Cragg-Donald F          — minimum eigenvalue, weak IV homoskedastic
* - Kleibergen-Paap rk Wald — weak IV under cluster / hetero
* - Hansen J / Sargan       — overid (need overid to be informative)
* - Anderson-Rubin           — weak-IV-robust test of β = 0

* 4b. ivreghdfe — HD FE + IV (combines reghdfe + ivreg2)
ivreghdfe log_wage age (training = draft_lottery z2), ///
    absorb(worker_id year) cluster(worker_id) first

* 4c. ivregress — built-in
ivregress 2sls log_wage age edu (training = draft_lottery z2), ///
    vce(cluster firm_id)
estat firststage                                       // F per endog
estat overid                                           // Sargan / Basmann
estat endogenous                                       // Wu-Hausman + Durbin

* LIML (less biased w/ weak IV)
ivregress liml log_wage age edu (training = draft_lottery z2), ///
    vce(cluster firm_id)

* GMM (efficient with heteroskedasticity)
ivregress gmm log_wage age (training = draft_lottery z2), ///
    wmatrix(cluster firm_id) vce(cluster firm_id)

* 4d. Anderson-Rubin confidence set (weak-IV robust)
ssc install weakiv, replace
weakiv log_wage age edu (training = draft_lottery), strong

* 4e. Conley spatial HAC SEs (geographic Z)
ivreg2 log_wage age (training = z), bw(5) kernel(uniform)

* 4f. Bartik / shift-share
* Construct: bartik_z = sum_k(share_ik * national_growth_k)
* Then plug bartik_z as the instrument in ivreg2.
```

---

## 5. Difference-in-differences

### 5.1 2×2 DID

```stata
* Cleanest: factor-variable interaction
reg log_wage i.treated##i.post age edu, vce(cluster worker_id)
* Coefficient on 1.treated#1.post is the ATT.
* Or:
reghdfe log_wage c.treated#c.post, absorb(worker_id year) vce(cluster worker_id)
```

### 5.2 TWFE — only with simultaneous treatment, not staggered

```stata
gen treat_post = treated * post
reghdfe log_wage treat_post, absorb(worker_id year) vce(cluster worker_id)
```

### 5.3 Event study (dynamic DID)

```stata
* Build relative-event-time dummies (base period = -1)
gen rel = year - first_treat
* Bin tails to avoid sparse leads/lags
replace rel = -5 if rel < -5 & !missing(rel)
replace rel =  5 if rel >  5 & !missing(rel)

* Reference period = -1, so omit ib(-1).rel — Stata expects non-negative levels.
* Workaround: shift +5 so -5..5 → 0..10, base at 4 (originally -1).
gen rel_p = rel + 5
replace rel_p = . if missing(first_treat)               // never-treated → out

reghdfe log_wage ib4.rel_p age edu, ///
    absorb(worker_id year) vce(cluster worker_id)

coefplot, keep(*.rel_p) omitted vertical ///
    yline(0) xline(4.5, lpattern(dash)) ///
    rename(0.rel_p="-5" 1.rel_p="-4" 2.rel_p="-3" 3.rel_p="-2" ///
           4.rel_p="-1" 5.rel_p="0"  6.rel_p="1"  7.rel_p="2"  ///
           8.rel_p="3"  9.rel_p="4"  10.rel_p="5+") ///
    xtitle("Years relative to treatment") ytitle("Coefficient (ATT)")
graph export "figures/event_study.pdf", replace
```

### 5.4 Staggered DID — the modern estimators

For staggered adoption (units treated at different times), TWFE is biased (Goodman-Bacon 2021). Use one of:

```stata
* --- Callaway–Sant'Anna (CS 2021) ---
* gvar = first treatment year (0 = never-treated)
gen gvar = first_treat
replace gvar = 0 if missing(first_treat)

csdid log_wage age edu, ///
    ivar(worker_id) time(year) gvar(gvar) ///
    method(dripw)                                       // doubly-robust IPW
* Aggregations:
estat group                                             // ATT(g)
estat calendar                                          // ATT(t)
estat event                                             // event-study aggregation
estat simple                                            // overall ATT

csdid_plot, ytitle("ATT")
graph export "figures/csdid_event.pdf", replace

* --- Sun & Abraham (2021) — interaction-weighted event study ---
* Build cohort-relative-time interactions
gen rel = year - first_treat
gen rel_p = rel + 5
replace rel_p = . if missing(first_treat)

eventstudyinteract log_wage ib4.rel_p, ///
    cohort(first_treat) control_cohort(never_treated) ///
    absorb(i.worker_id i.year) vce(cluster worker_id)

* --- Borusyak–Jaravel–Spiess (2024) — imputation ---
did_imputation log_wage worker_id year first_treat, ///
    allhorizons pretrend(5) autosample

event_plot, default_look ///
    graph_opt(xtitle("Years since treatment") ytitle("ATT"))
graph export "figures/did_imputation.pdf", replace

* --- Synthetic DID (Arkhangelsky et al. 2021) ---
sdid log_wage worker_id year training, ///
    vce(bootstrap) reps(500) seed(42) ///
    graph g1on g1_opt(ytitle("Log wage"))

* --- de Chaisemartin & D'Haultfœuille (2023) ---
did_multiplegt_dyn log_wage worker_id year training, ///
    effects(5) placebo(3) cluster(worker_id)
```

### 5.5 Goodman-Bacon decomposition (TWFE bias diagnostic)

```stata
xtset worker_id year
bacondecomp log_wage training, ddetail
* Plots the decomposition of the TWFE coefficient into 2×2 comparisons,
* with weights — negative weights indicate the "forbidden comparisons".
graph export "figures/bacon.pdf", replace
```

### 5.6 HonestDiD — Rambachan–Roth (2023) sensitivity

```stata
* After event study (eventstudyinteract / reghdfe with relative-time dummies)
honestdid, pre(1/4) post(5/9) mvec(0(0.1)0.5)
* Returns identified set under relaxed parallel trends.
* Plot:
honestdid, pre(1/4) post(5/9) mvec(0(0.1)0.5) coefplot
```

### 5.7 Continuous treatment DID

```stata
* See -did_continuous- (community) or hand-roll with i.treat_intensity_decile.
xtile dose = training_hours, nq(10)
reghdfe log_wage i.dose, absorb(worker_id year) vce(cluster worker_id)
```

---

## 6. Regression discontinuity

```stata
* 6a. Sharp RD
rdrobust outcome running_var, c(0) ///
    kernel(triangular) bwselect(mserd) vce(hc1)
ereturn list

* Visualize
rdplot outcome running_var, c(0) ///
    binselect(esmv) p(1) ///
    graph_options(title("RD plot") ///
                  ytitle("Outcome") xtitle("Running variable"))
graph export "figures/rd.pdf", replace

* Bandwidth selection alone
rdbwselect outcome running_var, c(0) bwselect(mserd)

* 6b. Fuzzy RD (treatment is imperfectly assigned by cutoff)
rdrobust outcome running_var, c(0) fuzzy(treatment)

* 6c. Kink RD (slope discontinuity)
rdrobust outcome running_var, c(0) deriv(1)

* 6d. Multi-cutoff RD
rdmc outcome running_var, c(cutoffs_var) genvars

* 6e. Density (manipulation) test — McCrary / Cattaneo et al.
rddensity running_var, c(0)

* 6f. Covariate smoothness (placebo on pre-determined covariates)
foreach v of varlist age edu female {
    rdrobust `v' running_var, c(0)
    display "`v': coef=" e(tau_cl) "  p=" e(pv_rb)
}

* 6g. Bandwidth sensitivity
foreach h of numlist 0.5 0.75 1.0 1.25 1.5 {
    rdrobust outcome running_var, c(0) h(`=`h'*e(h_l)')
}

* 6h. Donut hole
preserve
    drop if abs(running_var) < 0.1                      // exclude obs near cutoff
    rdrobust outcome running_var, c(0)
restore

* 6i. Local randomization (Cattaneo–Frandsen–Titiunik 2015)
rdrandinf outcome running_var, c(0) wl(-0.5) wr(0.5) seed(42)
```

---

## 7. Synthetic control

```stata
* 7a. Single treated unit, ADH 2003 / 2010
xtset country year
synth gdp_pc gdp_pc(1990(1)2000) trade(1990 1995 2000) ///
                                   invest(1990 1995 2000), ///
    trunit(7) trperiod(2001) fig keep(synth_out, replace)

* 7b. With placebo inference (synth_runner)
synth_runner gdp_pc gdp_pc(1990(1)2000) trade(1990 1995 2000), ///
    trunit(7) trperiod(2001) ///
    gen_vars                                             // creates effect_*, lead_*

* Plot effect with placebo distribution
single_treatment_graphs, ///
    effects_ylabels(-1000(500)1000) ///
    raw_options(ylabel(0(2000)10000))
graph export "figures/synth_effect.pdf", replace

* RMSPE-ratio test for inference
effect_graphs                                            // distribution of effects
pval_graphs                                              // p-value at each post period

* 7c. Multiple treated units
synth_runner gdp_pc gdp_pc(1990(1)2000), ///
    trunit() trperiod(2001) gen_vars                     // accept treated as variable
```

---

## 8. Matching & reweighting

### Propensity score matching

```stata
* psmatch2 — community standard, very flexible
psmatch2 training, outcome(log_wage) pscore(pscore) ///
    common neighbor(1) caliper(0.05) noreplacement ate

* Balance check before / after
pstest age edu tenure, both graph

* teffects psmatch — built-in, supports multiple-NN matching
teffects psmatch (log_wage) (training age edu tenure, logit), ///
    nneighbor(3) ate

* Diagnostics
tebalance summarize age edu tenure
tebalance density age, by(training) treated(1)
graph export "figures/balance_age.pdf", replace
```

### IPW / IPWRA / AIPW

```stata
* IPW
teffects ipw (log_wage) (training age edu tenure, logit), ///
    ate

* IPW with regression adjustment (doubly-robust)
teffects ipwra (log_wage age edu tenure) ///
                (training age edu tenure, logit), ate

* AIPW
teffects aipw (log_wage age edu tenure) ///
              (training age edu tenure, logit), ate

* Overlap / common-support diagnostics
teoverlap                                                // density of pscore by treatment
graph export "figures/overlap.pdf", replace
```

### Coarsened Exact Matching

```stata
ssc install cem, replace
cem age (#5) edu (#3) tenure (#4), treatment(training)
* L1 imbalance score is reported; use generated weights:
reg log_wage training age edu tenure [iweight=cem_weights], ///
    vce(cluster firm_id)
```

### Entropy balancing

```stata
ebalance training age edu tenure                         // first-moment exact match
* Generates _webal weights
reg log_wage training [aweight=_webal], vce(cluster firm_id)

* Higher moments
ebalance training age edu tenure, targets(2)             // means + variances
ebalance training age edu tenure, targets(3)             // + skewness
```

### Balance diagnostics

```stata
* SMDs before / after
foreach v of varlist age edu tenure {
    quietly sum `v' if training==1
    local m1 = r(mean); local sd1 = r(sd)
    quietly sum `v' if training==0
    local m0 = r(mean); local sd0 = r(sd)
    quietly sum `v' if training==1 [aweight=_webal]
    local m1w = r(mean); local sd1w = r(sd)
    quietly sum `v' if training==0 [aweight=_webal]
    local m0w = r(mean); local sd0w = r(sd)
    display "`v': SMD before=" %5.3f (`m1'-`m0')/sqrt((`sd1'^2+`sd0'^2)/2) ///
            "  after=" %5.3f (`m1w'-`m0w')/sqrt((`sd1w'^2+`sd0w'^2)/2)
}
```

---

## 9. Heckman selection

```stata
* Two-step (Heckman) — outcome equation conditional on selection
heckman log_wage age edu training, ///
    select(in_labor_force = age edu marital kids) twostep
* Coefficient on Mills's lambda > 0 & significant ⇒ selection bias matters.

* Maximum likelihood (more efficient)
heckman log_wage age edu training, ///
    select(in_labor_force = age edu marital kids)

* Heckman probit (binary outcome with selection)
heckprob employed age edu training, ///
    select(in_labor_force = age edu marital kids)
```

---

## 10. Quantile regression

```stata
* Single quantile
qreg log_wage training age edu, quantile(0.5)
qreg log_wage training age edu, quantile(0.5) vce(cluster firm_id)

* Multiple quantiles simultaneously (with bootstrap SEs)
sqreg log_wage training age edu, quantile(0.1 0.25 0.5 0.75 0.9) reps(500)

* Bootstrap SE quantile reg
bsqreg log_wage training age edu, quantile(0.5) reps(500)

* Plot coefficient across quantiles
ssc install grqreg, replace
grqreg training, ci ols olsci ///
    title("Coefficient of training across quantiles")
graph export "figures/qreg.pdf", replace

* Counterfactual decomposition (Machado-Mata) — see -rqdeco-
```

---

## 11. Survival / duration

```stata
stset duration, failure(event) id(worker_id)
sts graph, by(training)                                  // KM survival curves
sts test training, logrank                               // log-rank test

stcox training age edu                                   // Cox PH
estat phtest, detail                                     // PH assumption test
estat concordance                                        // C-index

streg training age edu, distribution(weibull)            // parametric
streg training age edu, distribution(gompertz)
```

---

## 12. SEM / GSEM

```stata
* Linear SEM (for mediation, factor analysis, etc.)
sem (log_wage <- training age edu hours_worked) ///
    (hours_worked <- training age edu)
estat teffects                                           // direct, indirect, total

* Generalized SEM (logit, poisson outcomes; latent variables)
gsem (employed <- training age, logit) ///
     (log_wage <- training age employed), ///
     vce(cluster firm_id)
```

---

## Quick command → estimator cheat sheet

| Estimator | Canonical command |
|-----------|-------------------|
| OLS robust | `reg y x, vce(robust)` |
| OLS cluster | `reg y x, vce(cluster id)` |
| Panel FE | `reghdfe y x, absorb(unit time) vce(cluster id)` |
| Panel FE + IV | `ivreghdfe y x (endog = z), absorb(...) cluster(...)` |
| Logit + ME | `logit y x; margins, dydx(*)` |
| Poisson + HD FE | `ppmlhdfe y x, absorb(...) cluster(...)` |
| 2SLS | `ivreg2 y x (endog = z), cluster(...)` |
| 2×2 DID | `reg y i.treat##i.post, vce(cluster id)` |
| Event study | `reghdfe y ib(ref).rel, absorb(...) vce(...)` |
| CS 2021 | `csdid y x, ivar() time() gvar() method(dripw)` |
| SA 2021 | `eventstudyinteract y rel_dummies, cohort() control_cohort()` |
| BJS 2024 | `did_imputation y unit time first_treat` |
| SDID | `sdid y unit time treat, vce(bootstrap)` |
| Sharp RD | `rdrobust y x, c(0)` |
| Fuzzy RD | `rdrobust y x, c(0) fuzzy(treat)` |
| RD density | `rddensity x, c(0)` |
| SCM | `synth y predictors, trunit() trperiod()` |
| SCM + inference | `synth_runner y predictors, trunit() trperiod() gen_vars` |
| PSM | `psmatch2 treat, outcome(y) ate` or `teffects psmatch (y)(treat x)` |
| IPWRA | `teffects ipwra (y x) (treat x), ate` |
| AIPW | `teffects aipw (y x) (treat x), ate` |
| Entropy balance | `ebalance treat x` then weighted reg |
| Heckman | `heckman y x, select(s = z)` |
| Quantile | `qreg y x, q(0.5)` / `sqreg` for multi |
