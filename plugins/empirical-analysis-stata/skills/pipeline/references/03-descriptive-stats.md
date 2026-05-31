# Step 3 — Descriptive Statistics & Table 1 in Stata (Deep Reference)

Goal: before any regression, produce the full set of descriptives a referee expects — size, central tendency, dispersion, comparison across treatment groups, balance (with SMDs), correlations with stars, and the distribution / time-trend plots that motivate the identification strategy.

## Contents

1. Full-sample summary (`tabstat`, `summarize, detail`, `asdoc sum`)
2. Stratified Table 1 (`balancetable`, manual `ttest` loop)
3. Weighted descriptives
4. Correlation matrix (`pwcorr` with stars, `corrtex`, `estpost correlate` + `esttab`)
5. Distribution plots (`histogram`, `kdensity`, `twoway`, `qnorm`)
6. Box / violin / strip plots
7. Time-series trends (the DID motivation plot)
8. Panel balance diagnostics (`xtdescribe`, heatmap via `twoway`)
9. Binned means / `binscatter`
10. Export recipes (LaTeX, Word, Excel, PDF)

---

## 1. Full-sample summary

```stata
local vars "log_wage age edu tenure training"

* One-line tabstat
tabstat `vars', statistics(n mean sd min p25 p50 p75 max) columns(statistics)

* Or detailed per-variable
foreach v of local vars {
    summarize `v', detail
}

* Export to Word with one command (community package)
asdoc sum `vars', ///
    stat(N mean sd min median max) ///
    save("tables/table1_full.docx") replace ///
    title("Table 1: Summary statistics")

* Export to LaTeX via estpost + esttab
estpost tabstat `vars', ///
    statistics(count mean sd min p25 p50 p75 max) columns(statistics)
esttab using "tables/table1_full.tex", ///
    cells("count mean sd min p25 p50 p75 max") ///
    nomtitle nonumber replace booktabs
```

For categorical / binary variables, report frequencies, not means:

```stata
foreach v of varlist female union industry region {
    tab `v', missing
}

* Or dense table:
tab1 female union, missing
```

---

## 2. Stratified Table 1 (treated vs. control + SMDs)

The single most-read table in an empirical paper.

### Fast route — `balancetable`

```stata
ssc install balancetable

balancetable training age edu tenure female ///
    using "tables/table1_balance.tex", ///
    vce(cluster firm_id) ///
    pval ///
    replace ///
    varlabels
```

Produces a LaTeX table with treated mean, control mean, t-test p-value. Add `stdev` for SDs and `nodiff` / `nototal` for formatting tweaks.

### Manual route (gives you SMD column too)

```stata
tempname T
postfile `T' str32 var float(mT sdT mC sdC diff smd p) using "tables/t1_manual.dta", replace
foreach v of varlist age edu tenure {
    quietly sum `v' if training == 1
    local mT = r(mean); local sdT = r(sd)
    quietly sum `v' if training == 0
    local mC = r(mean); local sdC = r(sd)
    local diff = `mT' - `mC'
    local smd  = `diff' / sqrt((`sdT'^2 + `sdC'^2)/2)
    quietly ttest `v', by(training)
    post `T' ("`v'") (`mT') (`sdT') (`mC') (`sdC') (`diff') (`smd') (r(p))
}
postclose `T'
use "tables/t1_manual.dta", clear
list, clean
```

**Interpretation** (from the PSM literature):

| |SMD| | Balance quality |
|------|-----------------|
| < 0.10 | well-balanced |
| 0.10 – 0.25 | modest imbalance; control in regression |
| > 0.25 | severe imbalance; consider matching / reweighting |

### Categorical version — chi-squared

```stata
foreach v of varlist female union region {
    tab `v' training, chi2 col
}
```

---

## 3. Weighted descriptives

When the sample uses survey or inverse-probability weights:

```stata
svyset psu [pweight=svywt], strata(stratum)
svy: mean wage age edu

* Post-stratification calibration
svyset psu [pweight=svywt], strata(stratum) poststrata(region) ///
    postweight(pop_region)
svy: proportion industry

* Weighted tabstat (no svyset needed)
tabstat wage [aweight=svywt], stat(mean sd) by(training)
```

---

## 4. Correlation matrix

```stata
local vars "log_wage age edu tenure training"

* Pearson
pwcorr `vars', sig star(.05)

* Spearman (rank)
spearman `vars', stats(rho p) star(.05)

* Matrix form (symmetric, with N per cell)
pwcorr `vars', obs

* Heatmap via -heatplot-
ssc install heatplot, replace
ssc install palettes, replace
ssc install colrspace, replace

heatplot `vars', values(format(%4.2f)) ///
    color(hcl diverging, intensity(.6)) ///
    aspectratio(1) ///
    title("Correlation matrix")
graph export "figures/corr_heatmap.pdf", replace

* Export correlations to LaTeX via estpost
estpost correlate `vars', matrix listwise
esttab using "tables/corr.tex", ///
    replace booktabs unstack compress ///
    not noobs nonumber nomtitle label
```

---

## 5. Distribution plots

```stata
* 5a. Histogram
histogram wage, bin(50) frequency ///
    title("Histogram of wage") saving(figures/hist_wage, replace)
graph export "figures/hist_wage.pdf", replace

* 5b. KDE by group
twoway (kdensity log_wage if training==1, lcolor(navy)) ///
       (kdensity log_wage if training==0, lcolor(maroon)), ///
    legend(order(1 "Treated" 2 "Control")) ///
    xtitle("Log wage") ytitle("Density") ///
    title("Log-wage density by treatment")
graph export "figures/kde_wage.pdf", replace

* 5c. Empirical CDF (cumulative density)
cumul log_wage if training==1, gen(cdf_T)
cumul log_wage if training==0, gen(cdf_C)
twoway (line cdf_T log_wage if training==1, sort lcolor(navy)) ///
       (line cdf_C log_wage if training==0, sort lcolor(maroon)), ///
    legend(order(1 "Treated" 2 "Control")) ///
    ytitle("Cumulative share")
graph export "figures/ecdf_wage.pdf", replace

* 5d. Q–Q vs. Normal
qnorm log_wage, title("Normal Q-Q plot, log wage")
graph export "figures/qq_wage.pdf", replace

* 5e. Kolmogorov–Smirnov two-sample test
ksmirnov log_wage, by(training)
```

---

## 6. Box / violin / strip

```stata
graph box log_wage, over(training) ///
    title("Box plot: log wage by treatment")
graph export "figures/box_wage.pdf", replace

* Violin via -violinplot- (community)
ssc install violinplot, replace
ssc install dstat,      replace          // dependency

violinplot log_wage, over(training) ///
    title("Violin plot: log wage by treatment")
graph export "figures/violin_wage.pdf", replace

* Strip / jitter (simple alternative)
twoway scatter log_wage training, jitter(5) msize(tiny) mcolor(%30)
graph export "figures/strip_wage.pdf", replace
```

---

## 7. Time-series trends (the DID motivation plot)

```stata
preserve
    collapse (mean) log_wage, by(year training)
    twoway (line log_wage year if training==1, lcolor(navy) lpattern(solid)) ///
           (line log_wage year if training==0, lcolor(maroon) lpattern(dash)), ///
        xline(`policy_year', lpattern(dash_dot) lcolor(gs8)) ///
        legend(order(1 "Treated" 2 "Control")) ///
        xtitle("Year") ytitle("Mean log wage") ///
        title("Pre/post trends by treatment status")
    graph export "figures/trend_did.pdf", replace
restore

* Also plot the DIFFERENCE (treated - control) — pre-period should hug zero
preserve
    collapse (mean) log_wage, by(year training)
    reshape wide log_wage, i(year) j(training)
    gen diff = log_wage1 - log_wage0
    twoway (line diff year, lcolor(navy)) ///
           (scatteri 0 `=year[1]' 0 `=year[_N]', recast(line) lcolor(gs10)), ///
        xline(`policy_year', lpattern(dash)) ///
        ytitle("Δ log wage (treated − control)") ///
        legend(off)
    graph export "figures/did_diff.pdf", replace
restore
```

---

## 8. Panel balance diagnostics

```stata
xtdescribe                                            // classic Stata balance summary
xtsum log_wage training                               // overall / between / within SD

* Units-per-year bar chart
preserve
    contract year
    twoway bar _freq year, xtitle("Year") ytitle("# unique observations") ///
        title("Panel coverage by year")
    graph export "figures/panel_coverage.pdf", replace
restore

* Years-per-unit histogram
preserve
    bysort worker_id: gen n_obs = _N
    contract worker_id n_obs
    histogram n_obs, bin(30) frequency ///
        xtitle("Years observed per worker")
    graph export "figures/years_per_unit.pdf", replace
restore

* Cohort sizes (staggered DID)
preserve
    keep if !missing(first_treat)
    contract first_treat
    twoway bar _freq first_treat, xtitle("First treatment year") ///
        ytitle("# units")
    graph export "figures/cohort_sizes.pdf", replace
restore

* Observation-matrix heatmap (unit × year) via -heatplot-
preserve
    keep worker_id year
    gen obs = 1
    reshape wide obs, i(worker_id) j(year)
    * → each row is one unit; columns are years; cell = 1 if observed
    * then heatplot on the matrix
restore
```

---

## 9. `binscatter` — residualized pre-regression eyeball

```stata
binscatter log_wage tenure, nquantiles(20) ///
    xtitle("Tenure (years)") ytitle("Mean log wage")
graph export "figures/binscatter_tenure_raw.pdf", replace

* Residualized on covariates
binscatter log_wage tenure, controls(age edu female) ///
    nquantiles(20) ///
    xtitle("Tenure") ytitle("Residualized mean log wage")
graph export "figures/binscatter_tenure_resid.pdf", replace

* By group
binscatter log_wage tenure, by(training) nquantiles(20)
graph export "figures/binscatter_tenure_bytreat.pdf", replace
```

---

## 10. Export recipes

```stata
* ---- LaTeX ----
estpost tabstat log_wage age edu tenure training, ///
    statistics(count mean sd min p25 p50 p75 max) columns(statistics)
esttab using "tables/summary.tex", replace ///
    cells("count mean(fmt(3)) sd(fmt(3)) min(fmt(3)) p50(fmt(3)) max(fmt(3))") ///
    nomtitle nonumber label booktabs

* ---- Word ----
asdoc sum log_wage age edu tenure training, ///
    stat(N mean sd min median max) ///
    save("tables/summary.docx") replace

* ---- Excel ----
putexcel set "tables/summary.xlsx", sheet("Table1") replace
putexcel A1 = "Variable"  B1 = "N"  C1 = "Mean"  D1 = "SD"
local row = 2
foreach v of varlist log_wage age edu tenure {
    quietly summarize `v'
    putexcel A`row' = "`v'" B`row' = `r(N)' ///
             C`row' = `r(mean)' D`row' = `r(sd)'
    local ++row
}

* ---- PDF figures ----
* All twoway / histogram / kdensity commands above use:
graph export "figures/name.pdf", replace
* Also recommend:
graph export "figures/name.png", width(1600) replace
```

---

## Standard Step 3 deliverable

For every paper, Step 3 produces at minimum these 6 artifacts:

1. `tables/table1_full.tex` — full-sample summary
2. `tables/table1_balance.tex` — treated vs. control with t-tests + SMDs
3. `figures/corr_heatmap.pdf`
4. `figures/kde_wage.pdf` (+ `ecdf_wage.pdf`, `qq_wage.pdf`, `hist_wage.pdf` in appendix)
5. `figures/trend_did.pdf` (the DID motivation plot)
6. `figures/panel_coverage.pdf` (or `cohort_sizes.pdf` for staggered designs)

If all 6 exist and look right, Step 4 is ready to start.
