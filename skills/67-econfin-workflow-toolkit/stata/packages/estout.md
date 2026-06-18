# estout/esttab: Publication-Quality Tables in Stata

## Overview

The `estout` package is the most widely used tool for creating publication-quality regression tables in Stata (by Ben Jann). It stores estimation results and exports formatted side-by-side model comparisons to LaTeX, HTML, RTF (Word), and CSV.

**Main commands:**
- `eststo` - Store estimation results
- `esttab` - User-friendly table creation and export
- `estout` - Low-level flexible table creation
- `estadd` - Add custom statistics to stored results

---

## Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [eststo: Storing Estimation Results](#eststo-storing-estimation-results)
- [esttab: Creating Tables](#esttab-creating-tables)
- [estadd: Adding Custom Statistics](#estadd-adding-custom-statistics)
- [estout: Low-Level Flexible Tables](#estout-low-level-flexible-tables)
- [Output Formats](#output-formats)
- [Multi-Column Model Comparisons](#multi-column-model-comparisons)
- [Summary Statistics Tables](#summary-statistics-tables)
- [Advanced Features](#advanced-features)
- [Publication Template: AER Style](#publication-template-aer-style)
- [Publication Template: Multi-Panel](#publication-template-multi-panel)
- [Tips and Best Practices](#tips-and-best-practices)
- [Common Issues](#common-issues)
- [Quick Reference](#quick-reference)

---

## Installation

```stata
ssc install estout
help esttab
help estout
help eststo
help estadd
```

---

## Quick Start

```stata
sysuse auto, clear

eststo clear
eststo: regress price mpg
eststo: regress price mpg weight
eststo: regress price mpg weight foreign

* Display in Stata
esttab

* Export to LaTeX / CSV / Word
esttab using results.tex, replace
esttab using results.csv, replace csv
esttab using results.rtf, replace
```

---

## eststo: Storing Estimation Results

```stata
eststo clear                                    // Clear all stored estimates

eststo: regress price mpg weight                // Auto-named (est1, est2, ...)
eststo model1: regress price mpg weight foreign // Custom name
quietly eststo: regress price mpg weight        // Store without displaying

* Manage stored estimates
estimates dir                   // List stored estimates
estimates replay model1         // Display a stored estimate
eststo drop model1              // Drop specific estimate
estimates save mymodel, replace // Save to disk
estimates use mymodel           // Load from disk

* Store with title
eststo model1, title("Basic Model"): regress price mpg weight

* Works with prefixed commands
eststo: xi: regress price i.rep78 mpg weight
eststo: ivregress 2sls price (mpg = gear_ratio) weight
```

---

## esttab: Creating Tables

### Basic Options

```stata
eststo clear
eststo: regress price mpg
eststo: regress price mpg weight
eststo: regress price mpg weight foreign

esttab               // Default output
esttab, se           // Standard errors in parentheses
esttab, t            // t-statistics
esttab, p            // p-values
esttab, ci           // Confidence intervals
esttab, not          // Suppress secondary stats
esttab, b(3) se(3)   // 3 decimal places
esttab, compress     // Compact output
esttab, wide         // Wide format
esttab, plain        // No formatting
```

### Titles, Labels, and Stars

```stata
esttab, label                                        // Use variable labels
esttab, mtitles("Model 1" "Model 2" "Model 3")     // Column titles
esttab, nomtitles                                    // No column titles
esttab, title("Table 1: Price Regressions")         // Table title
esttab, star(* 0.10 ** 0.05 *** 0.01)              // Significance stars
esttab, nostar                                       // No stars

* Model groups (for panel headers over columns)
esttab, mgroups("OLS Models" "IV Models", pattern(1 0 0 1 0 0))
```

### Statistics and Scalars

```stata
* Add model statistics below coefficients
esttab, stats(N r2 r2_a F, ///
    labels("Observations" "R-squared" "Adjusted R-squared" "F-statistic") ///
    fmt(%9.0fc %9.3f %9.3f %9.2f))

* Notes
esttab, addnote("Standard errors in parentheses." ///
                "* p<0.10, ** p<0.05, *** p<0.01")

* Replace default note
esttab, nonotes addnote("Custom note here")
```

### Variable Selection and Ordering

```stata
esttab, keep(mpg weight foreign)          // Keep specific variables
esttab, drop(_cons)                        // Drop variables
esttab, order(foreign mpg weight)          // Reorder variables

* Custom variable labels in table (overrides label variable)
esttab, varlabels(mpg "Miles per Gallon" ///
                  weight "Weight (lbs)" ///
                  foreign "Foreign Car" ///
                  _cons "Constant")

* Equivalent alternative
esttab, coeflabels(mpg "Miles per Gallon" ///
                   weight "Vehicle Weight")
```

---

## estadd: Adding Custom Statistics

```stata
eststo clear
eststo: regress price mpg weight foreign

* Add scalar
estadd scalar mystat = 1.234

* Add string (e.g., fixed effects indicators)
estadd local controls "Yes"

* Compute and add
quietly summarize price
estadd scalar mean_y = r(mean)
estadd scalar rmse = e(rmse)

* AIC/BIC
estat ic
matrix ic = r(S)
estadd scalar aic = ic[1,5]
estadd scalar bic = ic[1,6]

* Display with custom stats
esttab, scalars("mean_y Mean of Dep. Var." "rmse RMSE" "aic AIC" "bic BIC")
```

### Fixed Effects Indicators Pattern

```stata
webuse nlswork, clear

eststo clear
eststo: regress ln_wage age ttl_exp tenure
estadd local fe_ind "No"
estadd local fe_year "No"

eststo: areg ln_wage age ttl_exp tenure, absorb(idcode)
estadd local fe_ind "Yes"
estadd local fe_year "No"

eststo: xtreg ln_wage age ttl_exp tenure i.year, fe
estadd local fe_ind "Yes"
estadd local fe_year "Yes"

esttab, scalars("fe_ind Individual FE" "fe_year Year FE")
```

### Adding Test Statistics

```stata
eststo clear
eststo: regress price mpg weight foreign length headroom trunk
test mpg weight foreign
estadd scalar F_joint = r(F)
estadd scalar p_joint = r(p)

esttab, scalars("F_joint F-test (joint)" "p_joint p-value (joint)")
```

---

## estout: Low-Level Flexible Tables

`estout` gives more control over cell formatting than `esttab`.

```stata
eststo clear
eststo: regress price mpg weight
eststo: regress price mpg weight foreign

* Custom cell layout
estout, cells(b(star fmt(3)) se(par fmt(3)))

* Multiple rows per coefficient
estout, cells("b(star fmt(3) label(Coef.))" ///
              "se(par fmt(3) label(Std. Err.))" ///
              "t(fmt(2) label(t-stat))")

* Confidence intervals
estout, cells(b(star) ci(par))

* Standardized (beta) coefficients
estout, cells(b(star fmt(3)) beta(fmt(3)))
```

---

## Output Formats

### LaTeX

```stata
* Basic LaTeX with booktabs
esttab using table.tex, replace ///
    booktabs label ///
    b(%9.3f) se(%9.3f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("Basic" "Full Model") ///
    stats(N r2 r2_a, labels("Observations" "R-squared" "Adj. R-squared")) ///
    title("Determinants of Price\label{tab:price}") ///
    addnote("Standard errors in parentheses." ///
            "* \(p<0.10\), ** \(p<0.05\), *** \(p<0.01\)")

* Longtable (multi-page)
esttab using table.tex, replace booktabs longtable label

* Custom prehead/postfoot for full table environment control
esttab using table.tex, replace ///
    booktabs b(3) se(3) label ///
    prehead("\begin{table}[htbp]\centering" ///
            "\caption{Results}\label{tab:main}" ///
            "\begin{tabular}{l*{@M}{c}}" ///
            "\toprule") ///
    postfoot("\bottomrule" ///
             "\end{tabular}" ///
             "\end{table}")
```

**Gotcha:** In LaTeX, escape special characters: `\%`, `\$`, `\_`, `\&`. In label text use `\(p<0.05\)` to get math mode.

### HTML

```stata
esttab using table.html, replace html label ///
    b(%9.3f) se(%9.3f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("Model 1" "Model 2") ///
    title("Table 1: Regression Results")
```

### RTF (Word)

```stata
esttab using table.rtf, replace label ///
    b(%9.3f) se(%9.3f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("Model 1" "Model 2") ///
    note("Standard errors in parentheses.")
```

### CSV

```stata
esttab using table.csv, replace csv label ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01)

* Plain CSV for Excel
esttab using table.csv, replace csv plain label b(3) se(3)
```

---

## Multi-Column Model Comparisons

### Progressive Specifications

```stata
sysuse auto, clear
eststo clear
eststo m1: regress price mpg
eststo m2: regress price mpg weight
eststo m3: regress price mpg weight foreign
eststo m4: regress price mpg weight foreign length headroom

esttab m1 m2 m3 m4, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) label ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    stats(N r2 r2_a, labels("Observations" "R-squared" "Adj. R-squared"))
```

### Different Estimators

```stata
eststo clear
eststo ols: regress price mpg weight foreign
eststo robust: regress price mpg weight foreign, robust
eststo cluster: regress price mpg weight foreign, vce(cluster rep78)

esttab ols robust cluster, ///
    b(3) se(3) label ///
    mtitles("OLS" "Robust SE" "Clustered SE")
```

### Different Subsamples

```stata
eststo clear
eststo full: regress price mpg weight foreign
eststo domestic: regress price mpg weight if foreign == 0
eststo foreign_only: regress price mpg weight if foreign == 1

esttab full domestic foreign_only, ///
    b(3) se(3) label ///
    mtitles("Full Sample" "Domestic" "Foreign")
```

### Panel Groupings with mgroups

```stata
eststo clear
eststo pa1: regress price mpg weight
eststo pa2: regress price mpg weight foreign
eststo pb1: ivregress 2sls price weight (mpg = gear_ratio)
eststo pb2: ivregress 2sls price weight foreign (mpg = gear_ratio)

esttab pa1 pa2 pb1 pb2 using multipanel.tex, replace booktabs ///
    b(3) se(3) label ///
    mgroups("Panel A: OLS" "Panel B: 2SLS", pattern(1 0 1 0)) ///
    mtitles("(1)" "(2)" "(3)" "(4)")
```

---

## Summary Statistics Tables

```stata
sysuse auto, clear

* Basic summary statistics
estpost summarize price mpg weight length
esttab, cells("count mean(fmt(2)) sd(fmt(2)) min max") ///
    label title("Summary Statistics") nomtitles

* Formatted for LaTeX
estpost summarize price mpg weight length
esttab using summary.tex, replace booktabs ///
    cells("count(fmt(%9.0fc)) mean(fmt(%9.2fc)) sd(fmt(%9.2fc)) min(fmt(%9.2fc)) max(fmt(%9.2fc))") ///
    collabels("N" "Mean" "SD" "Min" "Max") ///
    label nomtitles ///
    title("Table 1: Descriptive Statistics\label{tab:summary}")

* Detailed (with percentiles)
estpost summarize price mpg weight, detail
esttab, cells("count mean sd min p25 p50 p75 max") label nomtitles
```

### Summary by Groups with T-Test

```stata
eststo clear
eststo domestic: estpost summarize price mpg weight if foreign == 0
eststo foreign: estpost summarize price mpg weight if foreign == 1
eststo diff: estpost ttest price mpg weight, by(foreign) unequal

esttab domestic foreign diff, ///
    cells("mean(fmt(2)) sd(fmt(2) par)") ///
    label mtitles("Domestic" "Foreign" "Difference")
```

---

## Advanced Features

### Factor Variables and Interactions

```stata
eststo clear
eststo: regress price i.rep78 c.mpg##c.weight i.foreign#c.mpg

* Hide FE coefficients but indicate their presence
esttab, label ///
    drop(*.rep78) ///
    indicate("Repair Record FE = *.rep78")

* With Yes/No labels
esttab, label ///
    indicate("Repair FE = *.rep78" "Headroom FE = *.headroom", labels("Yes" "No"))
```

### Margins and Marginal Effects

```stata
sysuse auto, clear
eststo clear

* Logit coefficients
quietly logit foreign mpg weight price
estimates store logit_model

* Average marginal effects
margins, dydx(*) post
eststo ame

* Marginal effects at means
quietly logit foreign mpg weight price
margins, dydx(*) atmeans post
eststo mem

esttab logit_model ame mem, ///
    b(3) se(3) label ///
    mtitles("Logit Coef." "AME" "MEM")
```

### Multiple Equation Models

```stata
* Heckman selection model
webuse womenwk, clear
eststo clear
eststo: heckman wage education age, ///
    select(married children education age)

esttab, label b(3) se(3) ///
    eqlabels("Wage Equation" "Selection Equation")
```

### Instrumental Variables

```stata
sysuse auto, clear
eststo clear
eststo ols: regress price mpg weight
eststo iv: ivregress 2sls price weight (mpg = gear_ratio turn)
eststo first: regress mpg gear_ratio turn weight

esttab ols iv first, ///
    b(3) se(3) label ///
    mtitles("OLS" "2SLS" "First Stage") ///
    stats(N r2, labels("Observations" "R-squared"))
```

### Fixed Effects with Indicators

```stata
webuse nlswork, clear
eststo clear

eststo pooled: regress ln_wage age ttl_exp tenure
estadd local fe "No"

eststo fe: xtreg ln_wage age ttl_exp tenure, fe
estadd local fe "Yes"

eststo fe_time: xtreg ln_wage age ttl_exp tenure i.year, fe
estadd local fe "Yes"
estadd local time_fe "Yes"

esttab pooled fe fe_time, ///
    b(3) se(3) label ///
    drop(*.year) ///
    scalars("fe Individual FE" "time_fe Year FE") ///
    mtitles("Pooled" "FE" "FE+Year")
```

---

## Publication Template: AER Style

```stata
sysuse auto, clear
eststo clear
eststo: regress price mpg weight
eststo: regress price mpg weight foreign
eststo: regress price mpg weight foreign length

esttab using "table_aer.tex", replace ///
    booktabs b(%9.3f) se(%9.3f) ///
    star(* 0.10 ** 0.05 *** 0.01) label nomtitles ///
    mgroups("Dependent Variable: Price", pattern(1 0 0) ///
            prefix(\multicolumn{@span}{c}{) suffix(}) ///
            span erepeat(\cmidrule(lr){@span})) ///
    stats(N r2, fmt(%9.0fc %9.3f) labels("Observations" "R-squared")) ///
    prehead("\begin{table}[htbp]\centering" ///
            "\caption{Determinants of Automobile Prices}" ///
            "\label{tab:main}" ///
            "\begin{tabular}{l*{3}{c}}" ///
            "\toprule") ///
    posthead("\midrule") ///
    prefoot("\midrule") ///
    postfoot("\bottomrule" ///
             "\multicolumn{4}{p{0.9\textwidth}}{\footnotesize \textit{Notes:} Standard errors in parentheses. * \(p<0.10\), ** \(p<0.05\), *** \(p<0.01\).}" ///
             "\\" ///
             "\end{tabular}" ///
             "\end{table}")
```

## Publication Template: Multi-Panel

```stata
eststo clear
eststo pa1: regress price mpg weight
eststo pa2: regress price mpg weight foreign
eststo pb1: regress price mpg weight, robust
eststo pb2: regress price mpg weight foreign, robust

esttab pa1 pa2 pb1 pb2 using "table_panels.tex", replace ///
    booktabs b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) label ///
    mgroups("Panel A: Standard SE" "Panel B: Robust SE", ///
            pattern(1 0 1 0) ///
            prefix(\multicolumn{@span}{c}{) suffix(}) ///
            span erepeat(\cmidrule(lr){@span})) ///
    mtitles("(1)" "(2)" "(3)" "(4)") ///
    stats(N r2, fmt(%9.0fc %9.3f) labels("Observations" "R-squared"))
```

---

## Tips and Best Practices

### Workflow Pattern

```stata
* 1. Clear at start
eststo clear

* 2. Store with descriptive names
eststo baseline: regress y x1 x2

* 3. Add custom stats immediately after estimation
estadd local fe "Yes"

* 4. Preview in Stata window first
esttab, label

* 5. Then export
esttab using "table.tex", replace booktabs label ...
```

### Debugging

- **Preview first:** Always `esttab, label` before exporting to file
- **LaTeX errors:** Check for unescaped special characters (`%`, `$`, `&`, `_`, `#`)
- **Missing packages:** LaTeX needs `\usepackage{booktabs}` for `booktabs` option
- **Wide tables:** Use `compress`, smaller font (`\small`), or landscape mode

### Journal-Specific Choices

```stata
* Standard errors vs t-stats vs CI
esttab, se    // Most journals
esttab, t     // Some journals
esttab, ci    // Medical journals

* Star conventions vary
esttab, star(* 0.10 ** 0.05 *** 0.01)   // Economics
esttab, star(+ 0.10 * 0.05 ** 0.01)     // Political science
esttab, star(* 0.05 ** 0.01 *** 0.001)  // Some social sciences
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| No variable labels | Add `label` option; or `label variable` before estimation |
| Too many FE coefficients | `drop(*.year)` and `indicate("Year FE = *.year")` |
| LaTeX special chars | `coeflabels()` or `label variable` to avoid `_`, `%`, `$` |
| Statistic not in `e()` | Add with `estadd scalar mystat = value` |
| Table too wide | `compress`, `\small` in prehead, or landscape mode |
| Wide tables in LaTeX | `prehead("\begin{landscape}")` with `\usepackage{lscape}` |

---

## Quick Reference

### Key Options

| Option | Description |
|--------|-------------|
| `label` | Use variable labels |
| `b(fmt)` / `se(fmt)` | Format coefficients / standard errors |
| `star(...)` | Significance stars |
| `mtitles(...)` | Column titles |
| `mgroups(...)` | Group headers over columns |
| `stats(... , labels(...) fmt(...))` | Bottom-of-table statistics |
| `keep(...)` / `drop(...)` / `order(...)` | Variable selection |
| `indicate(...)` | Show Yes/No for groups of variables |
| `varlabels(...)` / `coeflabels(...)` | Custom coefficient labels |
| `addnote(...)` / `nonotes` | Custom notes |
| `booktabs` | Professional LaTeX lines |
| `replace` | Overwrite output file |
| `compress` / `wide` / `plain` | Layout variants |
| `prehead(...)` / `postfoot(...)` | Custom LaTeX environment |
| `longtable` | Multi-page LaTeX table |
| `csv` / `html` | Output format flags |

### Common Patterns

```stata
* Store + display
eststo clear
eststo: regress y x1 x2
esttab, label se r2

* Export to LaTeX
esttab using "table.tex", replace booktabs label b(3) se(3) ///
    star(* 0.10 ** 0.05 *** 0.01) stats(N r2)

* Export to Word
esttab using "table.rtf", replace label b(3) se(3)

* Summary statistics
estpost summarize var1 var2 var3
esttab, cells("mean sd min max") label

* Clear stored estimates
eststo clear
```

### Help Files

```stata
help esttab       // Main table command
help estout       // Low-level table command
help eststo       // Store estimates
help estadd       // Add custom statistics
```

Official documentation: `http://repec.sowi.unibe.ch/stata/estout/`
