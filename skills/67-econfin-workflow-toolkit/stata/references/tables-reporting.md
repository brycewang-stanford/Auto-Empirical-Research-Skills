# Stata Tables and Reporting: Publication-Ready Output

## Table of Contents

- [Main Commands Overview](#main-commands-overview)
- [The table Command](#the-table-command)
- [Summary Statistics Tables](#summary-statistics-tables)
- [Regression Tables](#regression-tables)
- [Excel Output with putexcel](#excel-output-with-putexcel)
- [Word Documents with putdocx](#word-documents-with-putdocx)
- [PDF Reports with putpdf](#pdf-reports-with-putpdf)
- [LaTeX Export](#latex-export)
- [User-Written Packages](#user-written-packages)
- [Automated Report Generation](#automated-report-generation)
- [Best Practices](#best-practices)
- [Quick Reference](#quick-reference)

---

## Main Commands Overview

| Task | Command | Output Format | Best For |
|------|---------|---------------|----------|
| Basic tables | `table` | Console, Excel | Quick cross-tabs |
| Summary stats | `tabstat`, `estpost` | Multiple | Descriptive tables |
| Regression tables | `esttab` | LaTeX, RTF, CSV | Publications |
| Excel output | `putexcel` | Excel | Flexible formatting |
| Word documents | `putdocx` | Word | Reports |
| PDF reports | `putpdf` | PDF | Final reports |
| Quick export | `outreg2` | Word, Excel, LaTeX | Fast results |

---

## The table Command

```stata
table rowvar [colvar [supercolvar]], statistic(stat varname) [options]
```

### One-Way Tables

```stata
* Table with multiple statistics and formatting
table foreign, ///
    statistic(mean price) ///
    statistic(sd price) ///
    statistic(count price) ///
    nformat(%9.2f mean sd) ///
    sformat("(%s)" sd)
```

### Two-Way Tables

```stata
* Cross-tabulation with multiple cell statistics
table foreign rep78, ///
    statistic(mean price) ///
    statistic(sd price) ///
    statistic(count price) ///
    nformat(%9.2f mean sd) ///
    sformat("(%s)" sd)
```

### Table Options: Totals, Export, Collect

```stata
* Table with totals
table foreign rep78, ///
    statistic(mean price) ///
    totals(foreign) ///
    totals(rep78) ///
    nformat(%9.2f)

* Export table directly
table foreign rep78, ///
    statistic(mean price) ///
    nformat(%9.2f) ///
    export("table1.xlsx", replace)

* Name and collect for multi-format export
table foreign, ///
    statistic(mean price) ///
    statistic(sd price) ///
    nformat(%9.2f) ///
    name(mytable)

collect export "table1.xlsx", replace
collect export "table1.docx", replace
collect export "table1.pdf", replace
```

### Available Statistics

```stata
* frequency, percent, mean, median, sd, min, max all work:
table foreign rep78, ///
    statistic(frequency) ///
    statistic(percent) ///
    statistic(mean price) ///
    statistic(median price) ///
    statistic(min price) ///
    statistic(max price) ///
    nformat(%9.2f mean median) ///
    nformat(%9.0f min max)
```

---

## Summary Statistics Tables

### estpost + esttab Workflow

```stata
* ssc install estout  (provides estpost, esttab, estout)

* Summary statistics with estpost
estpost summarize price mpg weight length, detail

* Export to LaTeX
esttab using "summary.tex", ///
    cells("mean sd min max count") ///
    nomtitle nonumber ///
    replace

* Export to Word (RTF)
esttab using "summary.rtf", ///
    cells("mean(fmt(2)) sd(fmt(2)) min max count") ///
    nomtitle nonumber ///
    replace
```

### Group Comparison with T-Test

```stata
estpost ttest price mpg weight length, by(foreign)

esttab using "comparison.tex", ///
    cells("mu_1(fmt(2)) mu_2(fmt(2)) b(fmt(2) star)") ///
    label nomtitle nonumber ///
    replace
```

### Multi-Group Summary Table

```stata
eststo clear
eststo domestic: estpost summarize price mpg weight if foreign==0
eststo foreign_cars: estpost summarize price mpg weight if foreign==1

esttab domestic foreign_cars using "by_origin.tex", ///
    cells("mean(fmt(2)) sd(fmt(2)) count") ///
    label nomtitle ///
    replace
```

### Comprehensive Summary with Title/Notes

```stata
eststo clear
eststo all: quietly estpost summarize price mpg weight length
eststo domestic: quietly estpost summarize price mpg weight length if foreign==0
eststo foreign_cars: quietly estpost summarize price mpg weight length if foreign==1

esttab all domestic foreign_cars using "summary_complete.tex", ///
    cells("mean(fmt(2)) sd(fmt(2) par) min max") ///
    mtitle("All Cars" "Domestic" "Foreign") ///
    label booktabs ///
    title("Table 1: Summary Statistics by Car Origin") ///
    note("Standard deviations in parentheses.") ///
    replace
```

### Balance Table for Experiments

```stata
eststo clear
eststo control: estpost summarize price mpg weight if foreign==0
eststo treatment: estpost summarize price mpg weight if foreign==1
eststo diff: estpost ttest price mpg weight, by(foreign)

* pattern() controls which columns show which cells
esttab control treatment diff using "balance.tex", ///
    cells("mean(pattern(1 1 0) fmt(2)) sd(pattern(1 1 0) fmt(2) par) b(pattern(0 0 1) fmt(2) star)") ///
    mtitle("Control" "Treatment" "Difference") ///
    label booktabs ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    note("Standard deviations in parentheses. Stars indicate significance.") ///
    replace
```

---

## Regression Tables

### Basic esttab Regression Table

```stata
regress price mpg weight
estimates store model1
regress price mpg weight foreign
estimates store model2
regress price mpg weight foreign length
estimates store model3

esttab model1 model2 model3 using "regression.tex", ///
    b(%9.2f) se(%9.2f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    replace
```

### Advanced: Auto-Store with eststo

```stata
eststo clear
eststo: quietly regress price mpg
eststo: quietly regress price mpg weight
eststo: quietly regress price mpg weight foreign
eststo: quietly regress price mpg weight foreign length, robust

esttab using "regression_advanced.tex", ///
    b(%9.3f) se(%9.3f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    r2 ar2 ///
    scalars("N Observations" "r2_a Adjusted R-squared" "F F-statistic") ///
    label booktabs ///
    title("Table 2: Determinants of Car Prices") ///
    mtitle("(1)" "(2)" "(3)" "(4)") ///
    note("Robust standard errors in model (4).") ///
    replace
```

### Comparing SE Types (OLS, Robust, Clustered)

```stata
eststo clear
eststo ols: quietly regress price mpg weight foreign
eststo robust: quietly regress price mpg weight foreign, robust
eststo cluster: quietly regress price mpg weight foreign, vce(cluster rep78)

esttab ols robust cluster using "model_comparison.tex", ///
    b(%9.3f) se(%9.3f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    mtitle("OLS" "Robust SE" "Clustered SE") ///
    stats(N r2 r2_a, fmt(%9.0f %9.3f %9.3f) ///
        labels("Observations" "R-squared" "Adjusted R-squared")) ///
    label booktabs ///
    replace
```

### Panel Data Regression Table

```stata
webuse nlswork, clear
eststo clear
eststo pooled: quietly regress ln_wage grade age ttl_exp tenure, robust
eststo fe: quietly xtreg ln_wage grade age ttl_exp tenure, fe robust
eststo re: quietly xtreg ln_wage grade age ttl_exp tenure, re robust

esttab pooled fe re using "panel_regression.tex", ///
    b(%9.4f) se(%9.4f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    mtitle("Pooled OLS" "Fixed Effects" "Random Effects") ///
    stats(N N_g r2 r2_a, fmt(%9.0f %9.0f %9.3f %9.3f) ///
        labels("Observations" "Individuals" "R-squared" "Adjusted R-squared")) ///
    label booktabs ///
    drop(_cons) ///
    replace
```

### Marginal Effects Table

```stata
logit foreign price mpg weight
margins, dydx(*) post
estimates store margins1

esttab margins1 using "margins.tex", ///
    b(%9.4f) se(%9.4f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    title("Table 3: Average Marginal Effects") ///
    replace
```

### Using outreg2 (Alternative)

```stata
* ssc install outreg2

regress price mpg weight
outreg2 using "results.doc", replace ctitle("Model 1") ///
    label dec(3) addstat(Adj. R-squared, e(r2_a))

regress price mpg weight foreign
outreg2 using "results.doc", append ctitle("Model 2") ///
    label dec(3) addstat(Adj. R-squared, e(r2_a))

* LaTeX output
regress price mpg weight foreign
outreg2 using "results.tex", replace tex(frag) ///
    label dec(3) addstat(Adj. R-squared, e(r2_a))
```

---

## Excel Output with putexcel

### Basic Usage

```stata
putexcel set "analysis.xlsx", replace

* Add title with merge and bold
putexcel A1 = "Descriptive Statistics for Auto Dataset"
putexcel A1:E1, merge bold

* Column headers with border
putexcel A3 = "Variable" B3 = "Mean" C3 = "Std. Dev." D3 = "Min" E3 = "Max"
putexcel A3:E3, bold border(bottom)

* Add scalar results after summarize
summarize price
putexcel A4 = "Price"
putexcel B4 = r(mean)
putexcel C4 = r(sd)
putexcel D4 = r(min)
putexcel E4 = r(max)

* Number formatting
putexcel B4:E5, nformat(number_d2)
```

### Loop Through Variables

```stata
putexcel set "summary_stats.xlsx", replace
putexcel A1 = "Variable" B1 = "N" C1 = "Mean" D1 = "SD" E1 = "Min" F1 = "Max"
putexcel A1:F1, bold border(bottom)

local row = 2
foreach var of varlist price mpg weight length {
    quietly summarize `var'
    putexcel A`row' = "`var'"
    putexcel B`row' = r(N)
    putexcel C`row' = r(mean)
    putexcel D`row' = r(sd)
    putexcel E`row' = r(min)
    putexcel F`row' = r(max)
    local row = `row' + 1
}
putexcel B2:F`row', nformat(number_d2)
```

### Export Regression via Matrix

```stata
regress price mpg weight foreign
putexcel set "regression_results.xlsx", replace

* Extract coefficients and SEs from e() matrices
matrix b = e(b)'
matrix se = vecdiag(e(V))'
matrix se = sqrt(se)
matrix pval = 2*ttail(e(df_r), abs(b ./se))

local row = 4
local vars "mpg weight foreign _cons"
local i = 1
foreach var in `vars' {
    putexcel A`row' = "`var'"
    putexcel B`row' = matrix(b[`i',1])
    putexcel C`row' = matrix(se[`i',1])
    putexcel D`row' = matrix(pval[`i',1])
    local row = `row' + 1
    local i = `i' + 1
}
```

### Export Matrix Directly

```stata
correlate price mpg weight
matrix C = r(C)

putexcel set "correlation.xlsx", replace
putexcel A2 = matrix(C, names)
putexcel A2:D4, nformat(number_d3)
```

### Advanced Formatting

```stata
putexcel set "formatted_table.xlsx", replace

* Font, fill pattern, border options
putexcel A1 = "Sales Report Q1 2025"
putexcel A1:D1, merge bold font("Arial", 14) fpattern(solid, "lightblue")
putexcel A2:D2, bold border(all) fpattern(solid, "gray")

* Excel formulas
putexcel D3 = formula(=B3-C3)
putexcel B6 = formula(=SUM(B3:B5))

* Currency format
putexcel B3:D6, nformat("$#,##0")
```

### Multiple Sheets

```stata
putexcel set "multi_sheet.xlsx", replace

* First sheet (created with set)
putexcel A1 = "Summary Statistics", sheet("Summary")

* Additional sheets require modify
putexcel A1 = "Regression Results", sheet("Regression") modify
putexcel A1 = "Correlation Matrix", sheet("Correlations") modify
```

---

## Word Documents with putdocx

### Basic Structure

```stata
putdocx begin

putdocx paragraph, style(Title)
putdocx text ("Analysis of Auto Dataset")

putdocx paragraph, style(Heading1)
putdocx text ("1. Summary Statistics")

putdocx paragraph
putdocx text ("This report presents descriptive statistics.")

putdocx save "report.docx", replace
```

### Adding Tables Manually

```stata
putdocx begin

* Create table: (rows, cols)
putdocx table tbl1 = (5, 5), border(all) layout(autofitcontents)

* Header row
putdocx table tbl1(1,1) = ("Variable"), bold
putdocx table tbl1(1,2) = ("N"), bold
putdocx table tbl1(1,3) = ("Mean"), bold

* Fill with loop
local row = 2
foreach var of varlist price mpg weight {
    quietly summarize `var'
    putdocx table tbl1(`row',1) = ("`var'")
    putdocx table tbl1(`row',2) = (r(N)), nformat(%9.0f)
    putdocx table tbl1(`row',3) = (r(mean)), nformat(%9.2f)
    local row = `row' + 1
}
putdocx save "summary_report.docx", replace
```

### Adding Regression Results via etable

```stata
putdocx begin
regress price mpg weight foreign

* etable auto-generates a formatted regression table
putdocx table regtbl = etable

putdocx save "regression_report.docx", replace
```

### Adding Graphs

```stata
putdocx begin
scatter price mpg
graph export "scatter.png", replace

putdocx paragraph
putdocx image "scatter.png", width(5) height(3.5)

putdocx save "visual_report.docx", replace
```

### Comprehensive Report Features

```stata
putdocx begin, font("Times New Roman", 11)

* Page breaks
putdocx pagebreak

* Data table from dataset variables
putdocx table sumtbl = data("price mpg weight length"), ///
    varnames border(all) ///
    title("Table 1: Descriptive Statistics")

* Inline dynamic values
count
putdocx text ("`r(N)' automobiles"), bold

* Inline formatted return values
putdocx text ("`: display %9.4f e(r2)'")

putdocx save "comprehensive_report.docx", replace
```

---

## PDF Reports with putpdf

Syntax mirrors `putdocx` closely. Key differences noted below.

### Basic Usage

```stata
putpdf begin, font("Helvetica", 11)

putpdf paragraph, style(Title) halign(center)
putpdf text ("PDF Report: Auto Analysis")

putpdf pagebreak
putpdf save "report.pdf", replace
```

### Tables

```stata
putpdf table tbl1 = (5, 5), border(all) headerrow(1)
putpdf table tbl1(1,.), font("", 10, "bold") border(bottom, double)
putpdf table tbl1(1,1) = ("Variable")

* Fill with loop (same pattern as putdocx)
local row = 2
foreach var of varlist price mpg weight length {
    quietly summarize `var'
    putpdf table tbl1(`row',1) = ("`var'")
    putpdf table tbl1(`row',2) = (r(mean)), nformat(%9.2f)
    local row = `row' + 1
}

* Source note
putpdf paragraph
putpdf text ("Source: Auto dataset"), font("", 9, "italic")

putpdf save "analysis.pdf", replace
```

### Images

```stata
* Export graph at high resolution for PDF
graph export "temp_scatter.png", replace width(2000) height(1500)

putpdf paragraph
putpdf image "temp_scatter.png", width(5) height(3.75)
```

---

## LaTeX Export

### Basic Summary to LaTeX

```stata
estpost summarize price mpg weight length
esttab using "summary.tex", ///
    cells("mean sd min max") ///
    nomtitle nonumber noobs ///
    replace
* Include in LaTeX: \input{summary.tex}
```

### Professional Regression Table

```stata
eststo clear
eststo: quietly regress price mpg
eststo: quietly regress price mpg weight
eststo: quietly regress price mpg weight foreign
eststo: quietly regress price mpg weight foreign length

esttab using "regression.tex", ///
    b(3) se(3) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    title("Determinants of Automobile Prices\label{tab:regression}") ///
    mtitle("(1)" "(2)" "(3)" "(4)") ///
    stats(N r2 r2_a, fmt(0 3 3) labels("Observations" "R-squared" "Adjusted R-squared")) ///
    addnote("Standard errors in parentheses." "* \(p<0.10\), ** \(p<0.05\), *** \(p<0.01\)") ///
    replace
```

### Multi-Panel with mgroups

```stata
esttab using "panel_table.tex", ///
    b(3) se(3) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    mtitle("All" "Domestic" "Foreign") ///
    mgroups("Panel A: Full Sample" "Panel B: Domestic" "Panel C: Foreign", ///
        pattern(1 1 1) ///
        prefix(\multicolumn{@span}{c}{) suffix(}) ///
        span erepeat(\cmidrule(lr){@span})) ///
    replace
```

### Fragment vs. Standalone

```stata
* Fragment (to be \input{} in a document) -- default behavior
esttab using "fragment.tex", b(3) se(3) booktabs label replace

* Standalone (complete compilable LaTeX document)
esttab using "standalone.tex", b(3) se(3) booktabs label standalone width(\hsize) replace
```

### Custom LaTeX Preamble (threeparttable example)

```stata
esttab using "custom.tex", ///
    b(3) se(3) booktabs label ///
    prehead("\begin{table}[htbp]\centering" ///
            "\caption{Custom Regression Table}" ///
            "\label{tab:custom}" ///
            "\begin{threeparttable}" ///
            "\begin{tabular}{l*{1}{c}}") ///
    posthead("\hline\hline") ///
    prefoot("\hline") ///
    postfoot("\hline\hline" ///
             "\end{tabular}" ///
             "\begin{tablenotes}[flushleft]" ///
             "\footnotesize" ///
             "\item Notes: Standard errors in parentheses." ///
             "\end{tablenotes}" ///
             "\end{threeparttable}" ///
             "\end{table}") ///
    replace
```

---

## User-Written Packages

### Installing Packages

```stata
ssc install estout    // esttab, estpost, estout
ssc install outreg2
ssc install tabout
ssc install asdoc
ssc install logout
```

### tabout: Flexible Cross-Tabulations

```stata
* Cross-tab to LaTeX
tabout foreign rep78 using "crosstab.tex", ///
    cells(freq col) format(0 1) replace

* With summary statistics
tabout foreign rep78 using "crosstab_stats.tex", ///
    cells(mean price sd price) format(2) sum replace

* To Excel
tabout foreign rep78 using "crosstab.xlsx", ///
    cells(freq row col) format(0 1) replace
```

### asdoc: One-Line Export

```stata
asdoc summarize price mpg weight, stat(mean sd min max) save(asdoc_summary.doc) replace
asdoc correlate price mpg weight, save(asdoc_corr.doc) replace
asdoc regress price mpg weight foreign, save(asdoc_reg.doc) replace
asdoc ttest price, by(foreign) save(asdoc_ttest.doc) replace
```

### logout: Quick Export Wrapper

```stata
logout, save(stats) word replace: ///
    tabstat price mpg weight, statistics(mean sd min max) columns(statistics)

logout, save(correlation) excel replace: ///
    correlate price mpg weight
```

### estout: Advanced Customization

```stata
eststo clear
eststo: quietly regress price mpg weight
eststo: quietly regress price mpg weight foreign

estout using "advanced.tex", ///
    cells(b(star fmt(3)) se(par fmt(3))) ///
    stats(N r2 r2_a F, fmt(0 3 3 2) ///
        labels("Observations" "R-squared" "Adjusted R-squared" "F-statistic")) ///
    legend label ///
    varlabels(_cons Constant) ///
    collabels(none) ///
    mlabels("Model 1" "Model 2") ///
    starlevels(* 0.10 ** 0.05 *** 0.01) ///
    style(tex) ///
    replace

* Use keep/order/indicate for selective display
estout using "multi_panel.tex", ///
    cells(b(star fmt(3)) se(par fmt(3))) ///
    keep(mpg weight) ///
    order(mpg weight) ///
    indicate("Foreign dummy = foreign") ///
    style(tex) replace
```

---

## Automated Report Generation

### Basic Automation Template

```stata
clear all
set more off
global datapath "/path/to/data"
global outpath "/path/to/output"

use "$datapath/monthly_data.dta", clear

putdocx begin

putdocx paragraph, style(Title)
putdocx text ("Monthly Sales Report")

putdocx paragraph
putdocx text ("Report Generated: "), bold
putdocx text ("`c(current_date)'")

putdocx save "$outpath/monthly_report_`c(current_date)'.docx", replace
```

### Parameterized Report Program

```stata
capture program drop generate_report
program define generate_report
    syntax varlist using/

    putdocx begin

    putdocx paragraph, style(Title)
    putdocx text ("Automated Analysis Report")

    putdocx paragraph
    putdocx text ("Generated: `c(current_date)' `c(current_time)'")

    putdocx paragraph, style(Heading1)
    putdocx text ("1. Descriptive Statistics")
    putdocx table tbl1 = data("`varlist'"), varnames border(all)

    putdocx paragraph, style(Heading1)
    putdocx text ("2. Correlation Matrix")
    quietly correlate `varlist'
    matrix C = r(C)
    putdocx table tbl2 = matrix(C), rownames colnames nformat(%9.3f) border(all)

    putdocx save "`using'", replace
    display "Report saved to: `using'"
end

* Usage
sysuse auto, clear
generate_report price mpg weight using "auto_report.docx"
```

### Looping Over Groups

```stata
sysuse auto, clear
levelsof foreign, local(groups)

foreach group in `groups' {
    preserve
    keep if foreign == `group'

    if `group' == 0 local gname "Domestic"
    else local gname "Foreign"

    putdocx begin
    putdocx paragraph, style(Title)
    putdocx text ("`gname' Cars Analysis")

    putdocx table tbl = data("price mpg weight length"), varnames border(all)

    quietly regress price mpg weight
    putdocx table regtbl = etable

    putdocx save "report_`gname'.docx", replace
    restore
}
```

### Complete Multi-Output Workflow

```stata
clear all
set more off
global project "/path/to/project"
global output "$project/output"
global date = subinstr("`c(current_date)'", " ", "_", .)

use "$project/data/analysis_data.dta", clear

* --- 1. Excel Summary ---
putexcel set "$output/summary_tables_$date.xlsx", replace sheet("Summary")
putexcel A1 = "Overall Summary Statistics"
putexcel A1:F1, merge bold

local row = 3
foreach var of varlist price mpg weight length {
    quietly summarize `var'
    putexcel A`row' = "`var'"
    putexcel C`row' = (r(mean)), nformat(number_d2)
    putexcel D`row' = (r(sd)), nformat(number_d2)
    local row = `row' + 1
}

* --- 2. Regression to LaTeX ---
eststo clear
eststo m1: quietly regress price mpg
eststo m2: quietly regress price mpg weight
eststo m3: quietly regress price mpg weight foreign
eststo m4: quietly regress price mpg weight foreign length, robust

esttab m1 m2 m3 m4 using "$output/regression_$date.tex", ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    title("Regression Analysis: Determinants of Price") ///
    stats(N r2 r2_a, fmt(0 3 3) ///
        labels("Observations" "R-squared" "Adjusted R-squared")) ///
    replace

* --- 3. Word Report ---
putdocx begin
putdocx paragraph, style(Title) halign(center)
putdocx text ("Comprehensive Analysis Report")
putdocx paragraph, halign(center)
putdocx text ("Generated: `c(current_date)'")
putdocx pagebreak

putdocx table desc = data("price mpg weight length"), varnames border(all)

graph matrix price mpg weight, half
graph export "$output/matrix_$date.png", replace width(2000)
putdocx paragraph
putdocx image "$output/matrix_$date.png", width(6)

estimates restore m4
putdocx table regtbl = etable
putdocx save "$output/full_report_$date.docx", replace

* --- 4. PDF Summary ---
putpdf begin
putpdf paragraph, style(Title) halign(center)
putpdf text ("Analysis Summary")
putpdf save "$output/summary_$date.pdf", replace
```

---

## Best Practices

### esttab Publication Formatting

```stata
* Consistent decimals, labels, stars, model stats
esttab using "table.tex", ///
    b(%9.3f) se(%9.3f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    stats(N r2 r2_a, fmt(0 3 3) ///
        labels("Observations" "R-squared" "Adjusted R-squared")) ///
    replace

* Use variable labels
label variable price "Price (USD)"
label variable mpg "Fuel Efficiency (MPG)"
esttab using "table.tex", label replace

* Brackets instead of parentheses for SEs
esttab using "table.tex", cells(b(fmt(3)) se(par([ ]) fmt(3))) replace

* Indicate included controls without showing coefficients
esttab using "table.tex", ///
    keep(x1 x2) ///
    indicate("Additional controls = x3 x4 x5") ///
    replace
```

### AER-Style Table

```stata
esttab using "aer_table.tex", ///
    b(3) se(3) booktabs label ///
    alignment(D{.}{.}{-1}) ///
    title("Table 1: Main Results") ///
    nomtitles ///
    mgroups("Dependent Variable: Log(Income)", pattern(1 0 0) ///
        prefix(\multicolumn{@span}{c}{) suffix(}) ///
        span erepeat(\cmidrule(lr){@span})) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2, fmt(%9.0fc %9.3f) labels("Observations" "R-squared")) ///
    addnote("Notes: Robust standard errors in parentheses.") ///
    replace
```

---

## Quick Reference

### esttab Options

```stata
esttab [namelist] using filename [, options]

* Key options:
*   b(fmt)          - coefficient format
*   se(fmt)         - standard error format
*   star(levels)    - significance stars
*   label           - use variable labels
*   booktabs        - professional LaTeX
*   replace/append  - file handling
*   mtitle()        - model titles
*   stats()         - summary statistics row
*   keep()/drop()   - variable selection
*   order()         - variable order
*   indicate()      - indicate control groups
```

### putexcel Options

```stata
putexcel excel_cell = exp [, options]

*   putexcel A1 = "Text"              - text
*   putexcel B2 = (number)            - number
*   putexcel C3 = matrix(matname)     - matrix with names
*   putexcel D4 = formula(=B2*C3)     - Excel formula
*   putexcel A1:D1, merge             - merge cells
*   putexcel A1, bold                 - bold
*   putexcel B2, nformat(#,##0.00)    - number format
```

---

**Common Pitfalls:**

- Forgetting `replace` option or getting file-locked errors
- Inconsistent decimal places across models
- Missing variable labels (always set before `esttab` with `label` option)
- Not testing LaTeX code compilation before submission
- Forgetting to include sample sizes in published tables
