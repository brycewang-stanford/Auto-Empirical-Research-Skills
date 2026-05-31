# Step 8 — Publication Tables & Figures in Stata (Deep Reference)

Goal: turn the saved estimates and graphs into camera-ready outputs — `.tex` for LaTeX submissions, `.rtf` / `.docx` for Word co-authors, `.xlsx` for journal supplements, and clean `.pdf` figures with consistent styling.

## Contents

1. Regression tables — `esttab` (preferred) and `outreg2`
2. Summary-statistics tables — `tabstat`, `estpost summarize`, `asdoc`
3. Coefficient plots — `coefplot`
4. Event-study plots
5. Forest plots (subgroup / heterogeneity)
6. Marginal-effect plots (`marginsplot`)
7. Binscatter
8. RD plots
9. Multi-panel combined graphs (`graph combine`)
10. Themes / scheme / fonts
11. Export to LaTeX / Word / Excel / PNG / PDF
12. Make-style automation: a single `08_tables_figures.do`

---

## 1. Regression tables

### `esttab` (from `estout`) — the de-facto standard

```stata
* Save fits with eststo
eststo clear
eststo m1: qui reg log_wage training, vce(cluster firm_id)
eststo m2: qui reg log_wage training age edu, vce(cluster firm_id)
eststo m3: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id) vce(cluster worker_id)
eststo m4: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster worker_id)
eststo m5: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year region) vce(cluster worker_id)
eststo m6: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year i.industry#i.year) vce(cluster worker_id)

* LaTeX output
esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.tex", ///
    replace booktabs ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_a, ///
          labels("Observations" "R\sup{2}" "Adj. R\sup{2}") ///
          fmt(%9.0fc 3 3)) ///
    keep(training age edu tenure) ///
    order(training age edu tenure) ///
    label ///
    mlabel("(1)" "(2)" "(3)" "(4)" "(5)" "(6)") ///
    mgroups("Outcome: log wage", pattern(1 0 0 0 0 0) span ///
            prefix(\multicolumn{@span}{c}{) suffix(})) ///
    addnotes("Cluster-robust SEs by worker. \sym{*}\(p<0.10\), \sym{**}\(p<0.05\), \sym{***}\(p<0.01\).")

* Word / RTF output
esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.rtf", ///
    replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_a, labels("N" "R²" "Adj. R²")) ///
    label

* HTML
esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.html", ///
    replace label se html

* Markdown
esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.md", ///
    replace label se markdown
```

### Adding custom rows (FE indicators, controls Y/N)

```stata
* Use estadd to attach scalars/locals to each estimation
foreach m in m1 m2 m3 m4 m5 m6 {
    estimates restore `m'
    estadd local fe_worker = cond(e(absvar1)=="" & e(absvars)=="", "No", ///
                                                                 cond(strpos("`e(absvars)'", "worker_id")>0, "Yes", "No"))
    estadd local fe_year   = cond(strpos("`e(absvars)'", "year")>0, "Yes", "No")
    estadd local fe_indyr  = cond(strpos("`e(absvars)'", "industry")>0, "Yes", "No")
    estimates store `m'
}

esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.tex", ///
    replace booktabs ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(fe_worker fe_year fe_indyr N r2, ///
          labels("Worker FE" "Year FE" "Industry × Year FE" "N" "R²") ///
          fmt(%s %s %s %9.0fc 3)) ///
    keep(training age edu tenure) ///
    label
```

### `outreg2` — alternative (one-line, broadly compatible)

```stata
quietly reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster worker_id)
outreg2 using "tables/table_outreg2.doc", replace ///
    label dec(3) ///
    keep(training age edu tenure) ///
    addtext(Worker FE, Yes, Year FE, Yes)

* Subsequent regressions append rather than replace:
quietly reghdfe log_wage training age edu tenure region, ///
    absorb(worker_id year) vce(cluster worker_id)
outreg2 using "tables/table_outreg2.doc", append ///
    label dec(3) addtext(Worker FE, Yes, Year FE, Yes, Region, Yes)
```

---

## 2. Summary-statistics tables

```stata
* Via estpost + esttab
estpost summarize log_wage age edu tenure training, detail
esttab using "tables/table_summary.tex", ///
    cells("count(fmt(%9.0fc)) mean(fmt(3)) sd(fmt(3)) min(fmt(3)) p50(fmt(3)) max(fmt(3))") ///
    nomtitle nonumber label booktabs replace

* tabstat (one-shot)
tabstat log_wage age edu tenure, ///
    statistics(n mean sd min p50 max) columns(statistics) ///
    save                                         // saves r(StatTotal) etc

* asdoc — Word/Excel
asdoc tabstat log_wage age edu tenure, ///
    stat(N mean sd min median max) col(statistics) ///
    save("tables/table_summary.docx") replace
```

---

## 3. Coefficient plots — `coefplot`

```stata
* Single estimate from multiple specs
coefplot m1 m3 m6, keep(training) ///
    vertical ///
    yline(0) ///
    ciopts(recast(rcap)) ///
    levels(95) ///
    ylabel(-0.05(0.025)0.15) ///
    title("Effect of training on log wage") ///
    legend(order(1 "M1" 2 "M3" 3 "M6"))
graph export "figures/coefplot_main.pdf", replace

* Horizontal version (good for long labels)
coefplot m1 m3 m6, keep(training) ///
    xline(0) ///
    ciopts(recast(rcap)) ///
    grid(none)
graph export "figures/coefplot_h.pdf", replace

* Multiple coefficients, multiple specs
coefplot (m1, label("Raw")) ///
         (m3, label("+ unit FE")) ///
         (m6, label("+ unit×year, ind×year FE")), ///
    keep(training age edu tenure) ///
    xline(0) ///
    levels(95)
graph export "figures/coefplot_multi.pdf", replace
```

---

## 4. Event-study plots

```stata
* From eventstudyinteract or reghdfe with relative-time dummies
quietly reghdfe log_wage ib4.rel_p age edu, ///
    absorb(worker_id year) vce(cluster worker_id)

coefplot, keep(*.rel_p) ///
    omitted ///                                  // include the omitted base
    vertical ///
    yline(0) ///
    xline(4.5, lpattern(dash) lcolor(red)) ///
    ciopts(recast(rcap)) ///
    rename(0.rel_p = "-5"   1.rel_p = "-4"   2.rel_p = "-3" ///
           3.rel_p = "-2"   4.rel_p = "-1"   5.rel_p = "0" ///
           6.rel_p = "1"    7.rel_p = "2"    8.rel_p = "3" ///
           9.rel_p = "4"    10.rel_p = "5+") ///
    xtitle("Years relative to treatment") ///
    ytitle("Coefficient (ATT)") ///
    title("Event study")
graph export "figures/event_study.pdf", replace

* csdid_plot (after csdid)
csdid_plot, ytitle("ATT") xtitle("Years relative to treatment")
graph export "figures/csdid_event.pdf", replace

* event_plot (after did_imputation)
event_plot, default_look ///
    graph_opt(xtitle("Years since treatment") ytitle("ATT") ///
              title("Borusyak-Jaravel-Spiess imputation"))
graph export "figures/bjs_event.pdf", replace
```

---

## 5. Forest plot (subgroup / heterogeneity)

```stata
eststo clear
local groups all "female==0" "female==1" "age<40" "age>=40" ///
                  "industry==1" "industry==2"
local labels "All Male Female Young Old Manuf Service"

local i = 0
foreach g of local groups {
    local ++i
    local lab : word `i' of `labels'
    if "`g'" == "all" {
        eststo `lab': qui reghdfe log_wage training, ///
            absorb(worker_id year) vce(cluster worker_id)
    }
    else {
        eststo `lab': qui reghdfe log_wage training if `g', ///
            absorb(worker_id year) vce(cluster worker_id)
    }
}
coefplot All Male Female Young Old Manuf Service, ///
    keep(training) ///
    xline(0, lpattern(dash)) ///
    ciopts(recast(rcap)) levels(95) ///
    title("Heterogeneity forest plot") ///
    grid(none)
graph export "figures/forest.pdf", replace
```

---

## 6. Marginal-effect plots — `marginsplot`

```stata
* Continuous moderator
quietly reghdfe log_wage c.training##c.tenure age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
margins, dydx(training) at(tenure=(0(2)20))
marginsplot, ///
    recast(line) recastci(rarea) ///
    ciopts(fcolor(navy%20) lcolor(none)) ///
    yline(0, lpattern(dash)) ///
    xtitle("Tenure (years)") ///
    ytitle("Marginal effect of training on log wage") ///
    title("How does the effect vary with tenure?")
graph export "figures/marginsplot_tenure.pdf", replace

* Categorical moderator
quietly reghdfe log_wage c.training##i.edu_cat age, ///
    absorb(worker_id year) vce(cluster worker_id)
margins, dydx(training) at(edu_cat=(1(1)5))
marginsplot, recast(connected) ///
    xtitle("Education category") ///
    ytitle("Marginal effect of training")
graph export "figures/marginsplot_edu.pdf", replace
```

---

## 7. Binscatter

```stata
ssc install binscatter, replace
ssc install binsreg,    replace      // newer alternative

* Default
binscatter log_wage tenure, nquantiles(20) ///
    xtitle("Tenure (years)") ytitle("Mean log wage")
graph export "figures/binscatter_tenure.pdf", replace

* Residualized on controls
binscatter log_wage tenure, controls(age edu female) ///
    nquantiles(20) ///
    xtitle("Tenure") ///
    ytitle("Residualized mean log wage")
graph export "figures/binscatter_resid.pdf", replace

* By group
binscatter log_wage tenure, by(training) controls(age edu) ///
    nquantiles(20) ///
    legend(order(1 "Treated" 2 "Control"))
graph export "figures/binscatter_bygroup.pdf", replace

* Newer: binsreg with optimal bins + CI band
binsreg log_wage tenure, controls(age edu female) ///
    polyreg(1) ci(2 2)
graph export "figures/binsreg.pdf", replace
```

---

## 8. RD plots

```stata
rdplot outcome running_var, c(0) ///
    binselect(esmv) ///                         // even-spaced, MSE-optimal, var-matched
    p(1) ///                                    // local linear
    graph_options(title("Effect of eligibility on earnings") ///
                  ytitle("Earnings") ///
                  xtitle("Eligibility score (centered)"))
graph export "figures/rd_main.pdf", replace

* RD density plot
rddensity running_var, c(0) plot
graph export "figures/rd_density.pdf", replace
```

---

## 9. Multi-panel combined graphs

```stata
* Save individual panels
twoway (kdensity log_wage if training==1) ///
       (kdensity log_wage if training==0), ///
    legend(order(1 "Treated" 2 "Control")) ///
    title("(a) Density") ///
    saving(figures/p1, replace)

cumul log_wage if training==1, gen(cdf_T)
cumul log_wage if training==0, gen(cdf_C)
twoway (line cdf_T log_wage if training==1, sort) ///
       (line cdf_C log_wage if training==0, sort), ///
    legend(order(1 "Treated" 2 "Control")) ///
    title("(b) ECDF") ///
    saving(figures/p2, replace)

qnorm log_wage, title("(c) QQ vs. Normal") saving(figures/p3, replace)

twoway scatter log_wage age, title("(d) Wage vs. Age") ///
    saving(figures/p4, replace)

* Combine
graph combine "figures/p1.gph" "figures/p2.gph" ///
              "figures/p3.gph" "figures/p4.gph", ///
    cols(2) iscale(0.7) ///
    title("Distribution of log wage")
graph export "figures/combined.pdf", replace

* Cleanup intermediate .gph
foreach p in p1 p2 p3 p4 {
    capture erase "figures/`p'.gph"
}
```

---

## 10. Themes / scheme / fonts

```stata
* Built-in schemes
set scheme s2color                                   // Stata default (colorful)
set scheme s2mono                                    // monochrome (B&W publications)
set scheme economist                                 // Economist-style
set scheme stcolor                                   // Stata 18+ modern default

* Modern community schemes (-schemepack-)
ssc install schemepack, replace
set scheme white_tableau
set scheme white_w3d
set scheme cleanplots
set scheme lean2
* See: ssc describe schemepack

* Permanent default (saved to your profile)
set scheme white_tableau, permanently

* Font (in graphs)
graph set window fontface "Times New Roman"
graph set ps    fontface "Times New Roman"

* Default options for every twoway
grstyle init
grstyle set color cblind                             // colorblind-safe palette
grstyle set legend 6, nobox                          // legend bottom, no box
```

---

## 11. Export

### LaTeX

```stata
* Tables: esttab using "x.tex" replace booktabs
* Figures:
graph export "figures/x.pdf", replace
* In your .tex:
* \includegraphics[width=\linewidth]{figures/x.pdf}
```

### Word / RTF

```stata
* Tables:
esttab using "tables/x.rtf", replace label
asdoc reghdfe log_wage training, save("tables/x.docx") replace
* Figures:
graph export "figures/x.png", width(1600) replace
* Drag & drop into Word.
```

### Excel

```stata
* Single sheet
esttab using "tables/x.csv", replace label

* Multi-sheet workbook
putexcel set "tables/all.xlsx", replace
foreach sh in summary main robust {
    putexcel sheet("`sh'"), modify
    * ... fill cells with putexcel ...
}

* Export saved estimates with tabular layout
putexcel set "tables/results.xlsx", sheet("Main") replace
matrix B = e(b)
matrix V = e(V)
putexcel A1 = matrix(B)
putexcel A3 = matrix(vecdiag(V))
```

### PNG / PDF figures

```stata
graph export "figures/x.pdf", replace
graph export "figures/x.png", width(1600) replace             // Word / web
graph export "figures/x.eps", replace                          // legacy LaTeX
graph export "figures/x.svg", replace                          // editable vector
```

---

## 12. `08_tables_figures.do` skeleton

```stata
* code/08_tables_figures.do
version 17
clear all
set more off

* Apply consistent styling
set scheme white_tableau
graph set window fontface "Times New Roman"

cd "/path/to/project"

* ---- Replay all saved estimates ----
estimates use "estimates/m1.ster"; eststo m1
estimates use "estimates/m2.ster"; eststo m2
estimates use "estimates/m3.ster"; eststo m3
estimates use "estimates/m4.ster"; eststo m4
estimates use "estimates/m5.ster"; eststo m5
estimates use "estimates/m6.ster"; eststo m6

* ---- Tables ----
esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.tex", ///
    replace booktabs se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_a, labels("N" "R²" "Adj. R²")) ///
    keep(training age edu tenure) label

estpost summarize log_wage age edu tenure training, detail
esttab using "tables/table_summary.tex", replace booktabs ///
    cells("count mean(fmt(3)) sd(fmt(3)) min(fmt(3)) p50(fmt(3)) max(fmt(3))") ///
    nomtitle nonumber label

* ---- Figures ----
coefplot m1 m3 m6, keep(training) vertical yline(0) ///
    title("Effect of training on log wage")
graph export "figures/fig_coefplot.pdf", replace

* ... repeat for forest, marginsplot, binscatter, rd, combined ...

display "All tables → tables/  ;  all figures → figures/"
```

---

## Canonical output directory after Step 8

```
project/
├── tables/
│   ├── table_summary.tex
│   ├── table1_balance.tex
│   ├── table_main.tex
│   ├── table_robust_specs.tex
│   ├── table_robust_cluster.tex
│   ├── table_heterogeneity.tex
│   ├── outcome_ladder.tex
│   ├── table_main.rtf                           // Word version
│   └── all_results.xlsx
├── figures/
│   ├── corr_heatmap.pdf
│   ├── kde_wage.pdf
│   ├── ecdf_wage.pdf
│   ├── trend_did.pdf
│   ├── panel_coverage.pdf
│   ├── coefplot_main.pdf
│   ├── event_study.pdf
│   ├── csdid_event.pdf
│   ├── bjs_event.pdf
│   ├── forest.pdf
│   ├── marginsplot_tenure.pdf
│   ├── marginsplot_edu.pdf
│   ├── binscatter_resid.pdf
│   ├── rd_main.pdf
│   ├── rd_density.pdf
│   ├── bacon.pdf
│   ├── honestdid.pdf
│   ├── ritest_dist.pdf
│   ├── spec_curve.pdf
│   ├── loo.pdf
│   └── combined.pdf
└── logs/
    ├── main.log
    └── diagnostics.log
```

Every file regenerated from `do main.do`. No manual Excel formatting, no ad-hoc PowerPoint screenshots, no LaTeX hand-editing.
