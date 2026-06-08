/*------------------------------------------------------------------
  06_tables.do
  AER-style booktabs regression tables via esttab.
-------------------------------------------------------------------*/

version 18.0

* ==================================================================
* Main results — 5 columns, progressively richer
* ==================================================================
use "$intermediate/analytic.dta", clear

eststo clear

eststo col1: reghdfe outcome treat, noabsorb cluster(unit_id)
estadd local ctrl  "No"
estadd local fe    "None"
estadd local samp  "Full"

eststo col2: reghdfe outcome treat $controls, noabsorb cluster(unit_id)
estadd local ctrl  "Yes"
estadd local fe    "None"
estadd local samp  "Full"

eststo col3: reghdfe outcome treat $controls, ///
    absorb(unit_id year) cluster(unit_id)
estadd local ctrl  "Yes"
estadd local fe    "Unit + Year"
estadd local samp  "Full"

eststo col4: ivreg2 outcome (endog = iv) $controls i.unit_id i.year, ///
    cluster(unit_id) first
estadd local ctrl  "Yes"
estadd local fe    "Unit + Year"
estadd local samp  "Full"
estadd scalar fs_F = e(widstat)

eststo col5: ivreg2 outcome (endog = iv) $controls i.unit_id i.year ///
    if balanced == 1, cluster(unit_id)
estadd local ctrl  "Yes"
estadd local fe    "Unit + Year"
estadd local samp  "Balanced"
estadd scalar fs_F = e(widstat)

esttab col1 col2 col3 col4 col5 ///
    using "$tables/tab_main.tex", ///
    replace booktabs ///
    b(3) se(3) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    keep(treat endog) ///
    order(treat endog) ///
    mtitles("OLS" "OLS" "OLS" "IV" "IV") ///
    coeflabels(treat "Treatment" endog "Endogenous regressor") ///
    stats(ctrl fe samp N r2 fs_F, ///
          labels("Controls" "Fixed effects" "Sample" ///
                 "Observations" "R-squared" "First-stage F") ///
          fmt(%s %s %s %12.0fc %5.3f %5.1f)) ///
    label nonotes ///
    addnotes("Standard errors in parentheses, clustered at the unit level." ///
             "*** \(p<0.01\), ** \(p<0.05\), * \(p<0.1\).")

display as result "Main results table written to $tables/tab_main.tex"
