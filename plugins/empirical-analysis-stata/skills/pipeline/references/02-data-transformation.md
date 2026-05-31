# Step 2 — Variable Construction & Transformation in Stata (Deep Reference)

Goal: turn a clean `.dta` into one where every engineered variable is named consistently, documented with `label variable`, and ready for regression — logs, IHS, winsorized outcomes, standardized covariates, factor variables for dummies, panel operators, deflated real values, and staggered-DID timing.

## Contents

1. Naming convention
2. Log / IHS / Box–Cox
3. Winsorize & trim (`winsor2`)
4. Standardize (`egen std`, `center`)
5. Factor-variable encoding (`i.`, `c.`) — no more manual dummies
6. Interactions & polynomials (`c.x##c.x`, `i.a##i.b`)
7. Panel / time-series operators (`L.`, `F.`, `D.`, `S.`, `bys` alternatives)
8. Index construction (`pca`, `egen rowmean`, standardized sum)
9. Deflation with CPI / PPP
10. Binning (`xtile`, custom cuts with `recode` or `irecode`)
11. Per-capita / rate / share
12. Staggered-DID timing variables

---

## 1. Naming convention

Suffixes you should see in a well-organized .dta after Step 2:

| Suffix | Meaning |
|--------|---------|
| `_log` | natural log |
| `_ihs` | inverse hyperbolic sine |
| `_w1`  | winsorized at 1%/99% |
| `_std` | z-scored (from `egen std`) |
| `_l1` / `_l2` | lag 1 / lag 2 |
| `_f1`  | lead 1 |
| `_d`   | first difference |
| `_dm`  | within-group demeaned |
| `_pc`  | per-capita |
| `_real`| CPI-deflated to a base year |

A reader who scans `describe, fullnames` should be able to infer everything from these suffixes.

---

## 2. Log / IHS / Box–Cox

```stata
* Log — positive only
gen log_wage = log(max(wage, 1))                       // floor to avoid log(0)

* log(1+x) — safe when x ≥ 0
gen grants_log1p = log(1 + grants)

* Inverse hyperbolic sine (asinh) — handles 0 and negative
gen assets_ihs = asinh(assets)
* equivalently: gen assets_ihs = ln(assets + sqrt(assets^2 + 1))

* Box–Cox (estimate λ)
boxcox wage, model(lhsonly)
* Stata returns λ in r(lambda); transform:
scalar lam = r(lambda)
gen wage_bc = (wage^lam - 1)/lam if lam != 0
replace wage_bc = log(wage) if lam == 0

* Yeo–Johnson (no user-written equivalent in Stata; often done in Python)
```

Interpretation guide: `log` for magnitudes (wages, assets, sales), `ihs` for variables with legitimate zero / negative values, `log1p` for count-like.

---

## 3. Winsorize & trim

Winsorize = clip to the percentile (keep rows). Trim = delete rows. Prefer winsorize.

```stata
* 3a. winsor2 — the community standard
winsor2 wage, cuts(1 99) suffix(_w1)
* 1% and 99% on both tails; creates wage_w1

* Top-only
winsor2 wage, cuts(0 99) suffix(_w99)

* Within-group winsorize (most common in accounting / finance)
winsor2 wage, cuts(1 99) by(year) suffix(_w1_y)
winsor2 wage, cuts(1 99) by(industry year) suffix(_w1_iy)

* Replace in place (no new variable)
winsor2 wage, cuts(1 99) replace

* 3b. Trim (drop rows outside percentiles)
quietly sum wage, detail
drop if wage < r(p1) | wage > r(p99)

* 3c. Hand-roll if you want custom percentiles or logic
foreach v of varlist wage assets sales {
    quietly sum `v', detail
    replace `v' = r(p99) if `v' > r(p99) & !missing(`v')
    replace `v' = r(p1)  if `v' < r(p1)
}
```

---

## 4. Standardize

```stata
* z-score (mean 0, SD 1)
egen age_std = std(age)

* Within-group z-score
bysort industry year: egen roa_std = std(roa)

* Center only (demean)
egen age_mean = mean(age)
gen  age_c = age - age_mean
drop age_mean

* Min-max to [0,1]
sum age
gen age_mm = (age - r(min)) / (r(max) - r(min))

* Robust scaling (median / IQR)
quietly sum age, detail
gen age_rob = (age - r(p50)) / (r(p75) - r(p25))

* Bulk standardize multiple variables
foreach v of varlist age edu tenure {
    egen `v'_std = std(`v')
}
```

---

## 5. Factor-variable encoding

Stata's factor-variable syntax (`i.`, `c.`, `#`, `##`) lets you avoid manual dummies inside regressions. Manual dummies are only needed when you need to *export* them.

```stata
* Inside a regression (preferred)
reg log_wage training age i.industry i.year, vce(cluster firm_id)

* With interactions
reg log_wage c.training##c.age, vce(cluster firm_id)
reg log_wage c.training##i.female, vce(cluster firm_id)

* Absorb many levels as FE (reghdfe — see Step 5)
reghdfe log_wage training age, absorb(industry year) vce(cluster firm_id)

* When you DO need explicit dummies (e.g. export to another tool):
tab industry, gen(ind_)                             // creates ind_1, ind_2, ...
drop ind_1                                           // drop base for dummy trap

* Encode string → numeric + labels (needed before i.industry)
encode industry, gen(industry_n)
label values industry_n _all                         // auto-generated labels
```

---

## 6. Interactions & polynomials

Factor-variable notation is the preferred way, because it plays nicely with `margins`:

```stata
* Polynomial
reg log_wage c.age##c.age, vce(cluster firm_id)      // age + age^2

* Triple interaction (for DDD)
reg log_wage c.treated##c.post##c.high_exposure, vce(cluster firm_id)

* Continuous × categorical
reg log_wage c.training##i.edu_cat, vce(cluster firm_id)

* Margins on any of these
margins, dydx(training) at(edu_cat=(1 2 3 4 5))
marginsplot
```

When you explicitly need named variables (for `esttab` rows, or for exports):

```stata
gen age_sq      = age^2
gen trt_x_edu   = training * edu
gen trt_x_post  = treated * post
```

---

## 7. Panel / time-series operators

`xtset` is mandatory first.

```stata
xtset worker_id year

* Lag / lead
gen wage_l1 = L.log_wage                             // lag 1
gen wage_l2 = L2.log_wage                            // lag 2
gen wage_f1 = F.log_wage                             // lead 1

* First / second difference
gen d_wage  = D.log_wage                             // Δy
gen d2_wage = D2.log_wage                            // Δ²y

* Seasonal difference (when seasonal frequency declared)
gen s_wage = S4.log_wage                             // y_t - y_{t-4}

* Within-unit mean
bysort worker_id: egen wage_mean_i = mean(log_wage)

* Within-unit demean (useful when not using a FE estimator)
gen wage_dm = log_wage - wage_mean_i

* Growth rate
gen wage_growth = (log_wage - L.log_wage)             // already in logs
* or in levels: gen wage_growth = (wage - L.wage)/L.wage

* Rolling / moving average (time-series command; requires tsset or xtset)
bysort worker_id (year): gen wage_ma3 = (log_wage + L.log_wage + L2.log_wage)/3

* Expanding mean (cumulative)
bysort worker_id (year): gen wage_cummean = sum(log_wage)/_n

* Pre-treatment baseline (DID-heterogeneity variable)
bysort worker_id: egen wage_pre = mean(cond(year < first_treat, log_wage, .))

* Count within unit
bysort worker_id: egen n_obs = count(year)
bysort worker_id: gen  nth   = _n
```

**Gotcha**: `L.` on unbalanced panels returns `.` for the first observation of each unit — this is correct. But if you use `gen x_l1 = x[_n-1]` without `bys id (t)`, you'll silently borrow values from the previous *unit*. Always either use `xtset` + `L.` or `bys id (t): gen ...`.

---

## 8. Index construction

```stata
* Simple average of z-scored components
foreach c in leverage cash_ratio current_ratio {
    egen `c'_std = std(`c')
}
egen fin_idx_mean = rowmean(leverage_std cash_ratio_std current_ratio_std)

* PCA first component as the index
pca leverage cash_ratio current_ratio, components(1)
predict fin_idx_pc1, score

* Inverse-covariance weighted (Anderson 2008) — hand-roll in Mata or see -weightmean-
```

Report all versions (mean vs. PCA) in the robustness appendix.

---

## 9. Deflation (CPI / PPP)

```stata
* Assume CPI table in cpi.dta with year + cpi columns
merge m:1 year using "data/cpi.dta", keep(master match) nogen

* Base-year value of CPI (e.g. 2010)
sum cpi if year == 2010
scalar cpi_base = r(mean)

gen wage_real     = wage * cpi_base / cpi
gen log_wage_real = log(max(wage_real, 1))

* Country-specific deflators for cross-country panels (use country-year CPI)
merge m:1 country year using "data/cpi_by_country.dta", ///
    keep(master match) nogen
gen gdp_real_pc = gdp_nom_pc * cpi_base / cpi
```

---

## 10. Binning

```stata
* Equal-count quantiles (quintiles, deciles)
xtile wage_quint = wage, nq(5)
xtile tenure_dec = tenure, nq(10)

* Within-group quantiles
bysort year: egen wage_quint_y = xtile(wage), nq(5)

* Equal-width bins
egen age_bin5 = cut(age), group(5)                   // equal-count (same as xtile)
egen age_cut  = cut(age), at(0 18 30 45 65 200)      // custom cutoffs

* Custom cutoffs with labels
recode age (0/17 = 1 "Minor") (18/29 = 2 "Young") ///
           (30/44 = 3 "Mid") (45/64 = 4 "Senior") ///
           (65/max = 5 "Retired"), gen(age_cat)
label values age_cat agecat_lbl
```

---

## 11. Per-capita / rate / share

```stata
gen gdp_pc      = gdp / population
gen gdp_pc_log  = log(gdp_pc)

gen crime_rate  = crimes / population * 100000       // per 100k

* Within-group share (market share at firm-industry-year level)
bysort industry year: egen ind_yr_rev = sum(firm_rev)
gen mkt_share = firm_rev / ind_yr_rev

* Bounded share → logit transform if it's a regression outcome
gen mkt_share_logit = log(mkt_share / (1 - mkt_share + 1e-9))
```

---

## 12. Staggered-DID timing variables

Essential enough to have its own section.

```stata
* Assume training switches on at some year for each treated unit, never back off.
* 12a. First-treatment year per unit (NaN = never treated)
bysort worker_id (year): egen first_treat = min(cond(training==1, year, .))

* 12b. Treatment-current indicator
gen treated_now = (year >= first_treat) if !missing(first_treat)
replace treated_now = 0 if missing(first_treat)     // never-treated

* 12c. Relative event time
gen rel_time = year - first_treat                   // negative = pre

* 12d. Never-treated flag (cleanest control group)
gen byte never_treated = missing(first_treat)

* 12e. Not-yet-treated (CS/SA style control group)
gen byte not_yet_treated = never_treated | (year < first_treat)

* 12f. Event-time dummies (for event study with binned tails)
gen rt = rel_time
replace rt = -5 if rel_time <= -5 & !missing(rel_time)
replace rt = 5  if rel_time >=  5 & !missing(rel_time)
* Then in the regression: i.rt  (with a reference level, usually -1)

* 12g. Treatment cohort variable (for csdid / eventstudyinteract / did_imputation)
gen gvar = first_treat                              // Callaway–Sant'Anna uses this
replace gvar = 0 if missing(first_treat)            // CS convention: 0 = never
```

Sanity check before moving on:

```stata
* Cross-check construction
tab year first_treat, missing
tab rel_time, missing
tab rt
```

---

## Final checklist before Step 3

- [ ] Every engineered variable has a documented suffix
- [ ] Factor-variable notation used in regressions; no redundant manual dummies
- [ ] `xtset` is in place before any `L.`, `F.`, `D.` use
- [ ] All panel operators use `bys id (t):` pattern when not using `L./F./D.`
- [ ] Nominal variables deflated with an explicit base year
- [ ] Raw variables preserved; transformations live in new columns with new names
- [ ] `label variable` applied to every engineered variable
- [ ] `save "data/analysis.dta", replace` at the bottom of `02_transform.do`
