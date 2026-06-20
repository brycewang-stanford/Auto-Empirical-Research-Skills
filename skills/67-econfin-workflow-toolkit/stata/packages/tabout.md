# tabout: Publication-Quality Cross-Tabulations and Summary Tables

## Overview

`tabout` extends Stata's built-in `tabulate` with extensive formatting and export capabilities for publication-quality tables.

**Key features:**
- One-way and two-way frequency tables with summary statistics
- Export to LaTeX, HTML, plain text, CSV, and Excel
- Multiple panel tables (append mode)
- Support for survey data and weights (`svy`)
- Cell contents: freq, row/col/cell percentages, mean, sd, median, quartiles, se, min, max, confidence intervals

---

## Installation

```stata
ssc install tabout
help tabout
which tabout
```

---

## Quick Start

```stata
sysuse auto, clear

* Basic one-way frequency table
tabout foreign using table1.txt, replace

* One-way with percentages
tabout foreign using table1.txt, c(freq col) f(0 1) replace

* Basic two-way table with row and column percentages
tabout foreign rep78 using table2.txt, ///
    c(freq row col) f(0 1 1) replace

* Export to LaTeX
tabout foreign rep78 using table2.tex, ///
    c(freq row col) f(0 1 1) style(tex) replace
```

---

## One-Way Tables

```stata
* Frequencies with percentages and cumulative
tabout foreign using oneway1.txt, ///
    c(freq col cum) f(0 1 1) replace

* With custom column labels and totals
tabout foreign using oneway2.txt, ///
    c(freq col) f(0 1) ///
    clab(N %) ///
    ptotal(both) ///
    replace

* Stack multiple one-way tables
tabout foreign rep78 using oneway3.txt, ///
    oneway ///
    c(freq col) f(0 1) ///
    clab(N %) ///
    replace

* One-way summary statistics
tabout foreign rep78 using oneway3.txt, ///
    oneway ///
    sum ///
    c(mean price sd price) ///
    f(0 1) ///
    clab(Mean SD) ///
    replace
```

---

## Two-Way Tables

### Cell Contents Options

The `c()` option controls what appears in cells. Each statistic needs a corresponding decimal format in `f()`.

```stata
* Frequencies, row and column percentages
tabout foreign rep78 using twoway.txt, ///
    c(freq row col) f(0 1 1) ///
    clab(N Row% Col%) ///
    replace

* Cell percentages (of total)
tabout foreign rep78 using twoway.txt, ///
    c(cell) f(1) replace

* All four in one table
tabout foreign rep78 using twoway.txt, ///
    c(freq row col cell) f(0 1 1 1) ///
    clab(N Row% Col% Cell%) ///
    replace
```

### Totals and Tests

```stata
* Row and column totals with chi-square test
tabout foreign rep78 using twoway.txt, ///
    c(freq row) f(0 1) ///
    clab(N Row%) ///
    ptotal(both) ///
    stats(chi2) ///
    replace
```

**`ptotal()` values:** `single` (column total), `both` (row + column), `none`

---

## Summary Statistics by Groups

```stata
sysuse auto, clear

* Mean, SD, Min, Max by group
tabout foreign using summary.txt, ///
    sum ///
    c(mean price sd price min price max price) ///
    f(2 2 2 2) ///
    clab(Mean SD Min Max) ///
    replace

* Median and quartiles
tabout foreign using summary.txt, ///
    sum ///
    c(median price q1 price q3 price) ///
    f(2 2 2) ///
    clab(Median Q1 Q3) ///
    replace

* Mean with SE and confidence intervals
tabout foreign using summary.txt, ///
    sum ///
    c(mean price se price lb price ub price) f(2 2 2 2) ///
    clab(Mean SE Lower Upper) ///
    replace

* Two-way summary: Mean and SD
tabout foreign rep78 using summary2.txt, ///
    sum ///
    c(mean price sd price) f(2 2) ///
    clab(Mean SD) ///
    replace

* Multiple variables summary (stacked)
tabout foreign using summary3.txt, ///
    sum ///
    c(mean price sd price) ///
    c(mean mpg sd mpg) ///
    c(mean weight sd weight) ///
    f(2 2) ///
    clab(Mean SD) ///
    replace
```

---

## Multiple Panel Tables

Build panels using `replace` for the first, then `append` for subsequent panels. Use `h1()` / `h2()` for panel headings.

```stata
* Panel A
tabout foreign using panel.txt, ///
    c(freq col) f(0 1) ///
    h1(Panel A: Origin) ///
    ptotal(single) ///
    replace

* Panel B (appended)
tabout rep78 using panel.txt, ///
    c(freq col) f(0 1) ///
    h1(Panel B: Repair Record) ///
    ptotal(single) ///
    append

* Panel C: Summary stats panel (appended)
tabout foreign using panel.txt, ///
    sum ///
    c(mean price sd price) f(2 2) ///
    clab(Mean SD) ///
    h1(Panel C: Price by Origin) ///
    append
```

### Vertical Panels (Layout 2)

```stata
tabout foreign using panel2.txt, ///
    c(freq col) f(0 1) ///
    h2(Domestic vs Foreign) ///
    layout(2) ///
    replace
```

---

## Output Formats

### Plain Text / CSV

```stata
* Tab-delimited (Excel-compatible)
tabout foreign rep78 using table.txt, ///
    c(freq row) f(0 1) ///
    delimit(tab) replace

* CSV
tabout foreign rep78 using table.csv, ///
    c(freq row) f(0 1) ///
    delimit(",") replace
```

### LaTeX

```stata
* LaTeX with booktabs, caption, and label
tabout foreign rep78 using table.tex, ///
    c(freq row col) f(0 1 1) ///
    clab(N Row\% Col\%) ///
    style(tex) bt ///
    caption(Cross-tabulation of car origin and repair record) ///
    lab(tab:cross) ///
    ptotal(both) ///
    replace
```

**Gotcha:** Escape special characters in LaTeX: `\%`, `\$`, `\_`, `\&`, `\#`

### HTML

```stata
tabout foreign rep78 using table.html, ///
    c(freq row) f(0 1) ///
    style(html) ///
    title(Table 1: Car Origin by Repair Record) ///
    fn(Source: 1978 Automobile Data) ///
    replace
```

---

## Survey Data and Weights

```stata
* Setup survey design first
webuse nhanes2, clear
svyset psuid [pweight=finalwgt], strata(stratid)

* Survey-weighted frequency table
tabout sex race using survey.txt, ///
    c(freq row) f(0 1) ///
    svy ///
    replace

* Survey-weighted summary statistics
tabout sex race using survey.txt, ///
    sum ///
    c(mean bpsystol se bpsystol) f(2 2) ///
    clab(Mean SE) ///
    svy ///
    replace

* Subpopulation analysis (proper survey subpop)
tabout sex race using survey.txt, ///
    sum ///
    c(mean bpsystol) f(2) ///
    svy ///
    subpop(if age >= 40) ///
    replace
```

**Gotcha:** Use `subpop()` for proper survey subpopulation estimation rather than `if` conditions, which can produce incorrect standard errors.

---

## Customization Options

### Decimal Places

`f()` takes one value per statistic in `c()`:
```stata
* 0 decimals for freq, 1 for row%, 1 for col%
tabout foreign rep78 using t.txt, c(freq row col) f(0 1 1) replace
```

### Column Labels

```stata
* Underscores become spaces in clab()
tabout foreign using t.txt, ///
    sum c(mean price sd price) f(2 2) ///
    clab(Mean_Price SD_Price) replace
```

### Headings

```stata
tabout foreign rep78 using t.txt, ///
    c(freq row) f(0 1) ///
    h1(Table 1: Descriptive Statistics) ///
    h2(Panel A: Cross-tabulation) ///
    h3(By Origin and Repair Record) ///
    replace
```

### Layout Options

| Layout | Description |
|--------|-------------|
| `layout(1)` | Compact (default) |
| `layout(2)` | Column layout |
| `layout(3)` | Wide layout |

### Missing Values

```stata
* Include missing values as a category
tabout foreign rep78 using t.txt, ///
    c(freq row) f(0 1) mi replace

* Or explicitly exclude
tabout foreign rep78 if !missing(foreign, rep78) using t.txt, ///
    c(freq row) f(0 1) replace
```

---

## Template: Baseline Characteristics Table (Table 1)

```stata
sysuse auto, clear
generate treatment = foreign
label define trt 0 "Control" 1 "Treatment"
label values treatment trt

* Panel A: Categorical variables
tabout treatment using table1.tex, ///
    c(freq col) f(0 1) ///
    clab(N \%) ///
    h1(Panel A: Categorical Variables) ///
    ptotal(single) ///
    style(tex) bt replace

tabout rep78 treatment using table1.tex, ///
    c(freq col) f(0 1) ///
    clab(N \%) ///
    ptotal(both) stats(chi2) ///
    style(tex) bt append

* Panel B: Continuous variables (loop)
local vars "price mpg weight"
local labels `" "Price (\$)" "MPG" "Weight (lbs)" "'
local i = 1
foreach var of local vars {
    local lab : word `i' of `labels'
    tabout treatment using table1.tex, ///
        sum ///
        c(N `var' mean `var' sd `var') f(0 2 2) ///
        clab(N Mean SD) ///
        h2(\textit{`lab'}) ///
        style(tex) bt append
    local ++i
}
```

---

## Template: Multi-Format Output Program

```stata
capture program drop mytable
program define mytable
    syntax using/, [format(string)]
    if "`format'" == "tex" {
        local style "style(tex) bt"
        local pct "\%"
    }
    else if "`format'" == "html" {
        local style "style(html)"
        local pct "%"
    }
    else {
        local style ""
        local pct "%"
    }
    tabout foreign rep78 `using', ///
        c(freq row) f(0 1) ///
        clab(N Row`pct') ///
        `style' ptotal(both) replace
end

mytable using table.txt
mytable using table.tex, format(tex)
mytable using table.html, format(html)
```

---

## Template: Batch Stratified Tables

```stata
sysuse auto, clear
egen price_strata = cut(price), group(3)
replace price_strata = price_strata + 1
label define stratalab 1 "Low Price" 2 "Medium Price" 3 "High Price"
label values price_strata stratalab

* Combined file: overall + each stratum
tabout foreign rep78 using combined.tex, ///
    c(freq row col) f(0 1 1) ///
    h1(Table 1: All Strata Combined) ///
    ptotal(both) style(tex) bt replace

foreach s in 1 2 3 {
    local slab : label stratalab `s'
    tabout foreign rep78 if price_strata == `s' using combined.tex, ///
        c(freq row col) f(0 1 1) ///
        h1(Table `=`s'+1': `slab' Stratum) ///
        ptotal(both) style(tex) bt append
}
```

---

## Advanced Tips

### Conditional Table Generation

```stata
count if foreign == 1
if r(N) >= 20 {
    tabout foreign rep78 using conditional.tex, ///
        c(freq row) f(0 1) style(tex) bt replace
}
else {
    display as error "Insufficient sample size"
}
```

### Dynamic Column Labels

```stata
local today : display %tdCY-N-D date(c(current_date), "DMY")
local clab "N_as_of_`today' Percent"
tabout foreign using dynamic.txt, ///
    c(freq col) f(0 1) clab(`clab') replace
```

### Locals for Consistent Formatting

```stata
local fmt_freq "0"
local fmt_pct "1"
local fmt_mean "2"

tabout foreign using t.txt, ///
    sum c(mean price sd price) ///
    f(`fmt_mean' `fmt_mean') replace
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| LaTeX special chars (`%`, `$`, `_`, `&`, `#`) | Escape with backslash: `\%`, `\$`, etc. |
| Missing values in table | Use `mi` option, or filter with `if !missing()` |
| Long variable labels in headers | Shorten labels or use `h2()` / `h3()` to override |
| Alignment problems | Use `style(txt)` for text; `style(tex) bt` for LaTeX booktabs |
| Survey weights not applied | Run `svyset` first, then use `svy` option |

---

## Quick Reference

### Key Options

| Option | Description |
|--------|-------------|
| `c()` | Cell contents: `freq`, `row`, `col`, `cell`, `cum`, `mean`, `sd`, `median`, `q1`, `q3`, `min`, `max`, `se`, `lb`, `ub`, `N` |
| `f()` | Decimal places for each statistic in `c()` |
| `clab()` | Column labels (underscores become spaces) |
| `h1()`, `h2()`, `h3()` | Hierarchical headings |
| `style()` | Output: `tex`, `html`, `tab`, `csv` |
| `bt` | LaTeX booktabs formatting |
| `ptotal()` | Totals: `single`, `both`, `none` |
| `sum` | Summary statistics mode |
| `svy` | Use survey weights (requires prior `svyset`) |
| `mi` | Include missing values |
| `oneway` | Stack multiple variables as one-way tables |
| `layout()` | Layout: `1` (compact), `2` (column), `3` (wide) |
| `replace` / `append` | File write mode |
| `stats()` | Statistical tests: `chi2` |
| `delimit()` | Delimiter: `tab`, `","` |
| `caption()` | LaTeX table caption |
| `lab()` | LaTeX table label |
| `title()` | HTML title |
| `fn()` | Footnote text |
| `subpop()` | Survey subpopulation |

### Common Patterns

```stata
* Basic frequency:         c(freq) f(0)
* Freq + row%:             c(freq row) f(0 1)
* Freq + row% + col%:      c(freq row col) f(0 1 1)
* Summary stats:           sum c(mean var sd var) f(2 2)
* Full summary:            sum c(N var mean var sd var median var) f(0 2 2 2)
* LaTeX with booktabs:     style(tex) bt
* Survey-weighted:         svy (after svyset)
* Multi-panel:             replace on first, append on rest
```

### Related Packages

```stata
ssc install estout    // Regression tables
ssc install fre       // Enhanced frequency tables
ssc install table1    // Medical-style baseline tables
```
