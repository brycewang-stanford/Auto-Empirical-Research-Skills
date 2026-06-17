# outreg2: Quick Regression Tables in Stata

## Overview

`outreg2` is a user-written command for creating regression tables. It exports results directly to Word, Excel, LaTeX, and text -- no separate storage step needed (unlike `esttab`). Ideal for quick analyses and Office-format output.

---

## Installation

```stata
ssc install outreg2
help outreg2
adoupdate outreg2, update
```

---

## Core Workflow

```stata
sysuse auto, clear

* First regression - create new table with replace
regress price mpg
outreg2 using myresults.doc, replace

* Subsequent regressions - append to same table
regress price mpg weight
outreg2 using myresults.doc, append

regress price mpg weight foreign
outreg2 using myresults.doc, append
```

**Key difference from esttab:** outreg2 outputs immediately after each regression -- no `eststo` step needed.

```stata
* outreg2: run regression, export immediately
regress price mpg
outreg2 using results.doc, replace

* esttab: store first, export later
eststo clear
eststo: regress price mpg
eststo: regress price mpg weight
esttab using results.tex, replace
```

Works with all Stata estimation commands (regress, logit, probit, ivregress, xtreg, etc.).

---

## Output Formats

| Format | Extension | Option | Notes |
|--------|-----------|--------|-------|
| Word | .doc | `word` (default) | RTF format, not .docx |
| Excel | .xls | `excel` | |
| LaTeX | .tex | `tex` | Auto-handles special chars |
| Text | .txt | `text` | |
| CSV | .csv | (automatic) | |

```stata
outreg2 using table.doc, replace           // Word (default)
outreg2 using table.xls, replace excel     // Excel
outreg2 using table.tex, replace tex       // LaTeX
outreg2 using table.txt, replace text      // Plain text
outreg2 using table.csv, replace           // CSV
```

---

## Essential Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `replace` | Create new file | `outreg2 using t.doc, replace` |
| `append` | Add column to existing file | `outreg2 using t.doc, append` |
| `label` | Use variable labels instead of names | `outreg2 using t.doc, label` |
| `dec(#)` | Decimal places (default 3) | `outreg2 using t.doc, dec(2)` |
| `ctitle()` | Column title | `ctitle(Model 1)` |
| `title()` | Table title | `title(Table 1: Results)` |
| `keep()` | Show only these variables | `keep(mpg weight)` |
| `drop()` | Hide these variables | `drop(length trunk)` |
| `sortvar()` | Reorder rows | `sortvar(foreign weight mpg)` |
| `nocons` | Suppress constant row | |
| `addstat()` | Add scalar statistics | `addstat(Adj R-sq, e(r2_a))` |
| `addtext()` | Add text indicator rows | `addtext(FE, Yes)` |
| `addnote()` | Add footnotes | `addnote(Note: ...)` |
| `bracket` | Brackets instead of parentheses | |
| `wide` | Wider columns (text output) | |
| `noaster` | Suppress significance stars | |

### Statistical Display Options

| Option | Description |
|--------|-------------|
| `se` | Standard errors in parentheses (default) |
| `tstat` | t-statistics instead of SE |
| `pvalue` | p-values |
| `ci` | Confidence intervals |
| `beta` | Standardized coefficients |

### Custom Significance Levels

```stata
* Default: * p<0.05, ** p<0.01, *** p<0.001
* Custom levels:
outreg2 using t.doc, replace pvalue alpha(0.01, 0.05, 0.10)
```

---

## Adding Statistics and Indicators

### Scalar Statistics with addstat()

```stata
regress price mpg weight foreign
outreg2 using t.doc, replace ///
    addstat(Adj R-sq, e(r2_a), F-stat, e(F), Root MSE, e(rmse))

* Custom pre-computed statistics
summarize price
local mean_price = r(mean)
regress price mpg weight
outreg2 using t.doc, replace addstat(Mean Price, `mean_price')
```

### Text Indicators with addtext()

```stata
* Fixed effects indicators (very common pattern)
xtreg ln_wage age ttl_exp tenure, fe
outreg2 using fe.doc, replace ///
    addtext(Individual FE, Yes, Year FE, No)

* Controls/SE type indicators
regress price mpg weight foreign length headroom, robust
outreg2 using t.doc, replace ///
    addtext(Controls, Yes, Robust SE, Yes)
```

### Footnotes with addnote()

```stata
outreg2 using t.doc, replace ///
    addnote(Source: 1978 Automobile Data, ///
            * p<0.05 ** p<0.01 *** p<0.001)
```

---

## Complete Workflow Examples

### Progressive Model Building (Research Paper)

```stata
sysuse auto, clear
label variable price "Price ($)"
label variable mpg "Mileage (MPG)"
label variable weight "Weight (lbs)"
label variable foreign "Foreign Car"

regress price mpg
outreg2 using paper_table1.doc, replace ///
    label ctitle(Model 1) ///
    title(Table 1: Determinants of Automobile Prices) ///
    addtext(Controls, No) dec(2)

regress price mpg weight
outreg2 using paper_table1.doc, append ///
    label ctitle(Model 2) addtext(Controls, No) dec(2)

regress price mpg weight foreign
outreg2 using paper_table1.doc, append ///
    label ctitle(Model 3) addtext(Controls, No) dec(2)

regress price mpg weight foreign length
outreg2 using paper_table1.doc, append ///
    label ctitle(Model 4) addtext(Controls, Yes) dec(2) ///
    addnote(Standard errors in parentheses., ///
            * p<0.05 ** p<0.01 *** p<0.001)
```

### Panel Data with Fixed Effects

```stata
webuse nlswork, clear
xtset idcode year

regress ln_wage age ttl_exp tenure
outreg2 using panel.xls, replace excel label dec(4) ///
    ctitle(Pooled OLS) addtext(Individual FE, No, Year FE, No)

xtreg ln_wage age ttl_exp tenure, fe
outreg2 using panel.xls, append excel label dec(4) ///
    ctitle(FE) addtext(Individual FE, Yes, Year FE, No)

xtreg ln_wage age ttl_exp tenure i.year, fe
outreg2 using panel.xls, append excel label dec(4) ///
    ctitle(Two-way FE) drop(i.year) ///
    addtext(Individual FE, Yes, Year FE, Yes)

xtreg ln_wage age ttl_exp tenure, re
outreg2 using panel.xls, append excel label dec(4) ///
    ctitle(RE) addtext(Individual FE, Random, Year FE, No)
```

### Binary Outcome Models (LPM / Logit / Probit)

```stata
sysuse auto, clear
generate expensive = (price > 6000)

regress expensive mpg weight foreign
outreg2 using binary.tex, replace tex label dec(4) ctitle(LPM)

logit expensive mpg weight foreign
outreg2 using binary.tex, append tex label dec(4) ctitle(Logit)

probit expensive mpg weight foreign
outreg2 using binary.tex, append tex label dec(4) ctitle(Probit)

* Marginal effects from logit
quietly logit expensive mpg weight foreign
margins, dydx(*) post
outreg2 using binary.tex, append tex label dec(4) ctitle(Marg. Effects)
```

### IV/2SLS Table

```stata
sysuse auto, clear

regress price mpg weight
outreg2 using iv.doc, replace label dec(3) ctitle(OLS) ///
    addtext(Estimation, OLS)

regress mpg gear_ratio turn weight
outreg2 using iv.doc, append label dec(3) ctitle(First Stage)

ivregress 2sls price weight (mpg = gear_ratio turn)
outreg2 using iv.doc, append label dec(3) ctitle(2SLS) ///
    addnote(MPG instrumented with gear ratio and turn circle.)
```

### Robustness Checks

```stata
sysuse auto, clear

regress price mpg weight foreign
outreg2 using robust.doc, replace label dec(3) ctitle(Baseline) ///
    addtext(SE, Standard, Sample, Full)

regress price mpg weight foreign, robust
outreg2 using robust.doc, append label dec(3) ctitle(Robust SE) ///
    addtext(SE, Robust, Sample, Full)

bootstrap, reps(500): regress price mpg weight foreign
outreg2 using robust.doc, append label dec(3) ctitle(Bootstrap) ///
    addtext(SE, Bootstrap, Sample, Full)

regress price mpg weight foreign if price > 5000
outreg2 using robust.doc, append label dec(3) ctitle(High Price) ///
    addtext(SE, Standard, Sample, Price>5000)
```

### Loops for Multiple Tables

```stata
sysuse auto, clear
foreach depvar in price mpg weight {
    regress `depvar' foreign length
    outreg2 using table_`depvar'.doc, replace label ///
        title(Table: Determinants of `depvar')
}
```

### Stored Estimates

```stata
regress price mpg weight
estimates store model1
regress price mpg weight foreign
estimates store model2

estimates restore model1
outreg2 using from_stored.doc, replace
estimates restore model2
outreg2 using from_stored.doc, append
```

---

## Publication-Ready LaTeX

```stata
sysuse auto, clear

regress price mpg
outreg2 using pub.tex, replace tex label dec(3) ctitle((1)) ///
    addtext(Controls, No)

regress price mpg weight foreign length, robust
summarize price
local mean_price = r(mean)
outreg2 using pub.tex, append tex label dec(3) ctitle((2)) ///
    addtext(Controls, Yes, SE, Robust) ///
    addstat(Mean of Dep. Var., `mean_price') ///
    addnote(Standard errors in parentheses., ///
            * p<0.05; ** p<0.01; *** p<0.001)
```

LaTeX preamble needs: `\usepackage{booktabs}`. Include with `\input{pub.tex}`.

---

## outreg2 vs esttab

| Feature | outreg2 | esttab |
|---------|---------|--------|
| Workflow | Immediate (no storage) | Store then export |
| Word output | Native .doc | RTF only |
| Excel output | Native .xls | CSV |
| LaTeX | Good | Excellent (more control) |
| Customization | Moderate | Extensive |
| Summary stats | Via `addstat` | Via `estpost` |
| Learning curve | Gentle | Steeper |

**Use outreg2 when:** quick reporting, Word/Excel output, simple multi-model tables.
**Use esttab when:** publication LaTeX with heavy customization, summary statistics tables, need to store/reuse estimates.

---

## Tips and Common Mistakes

### Best Practices

```stata
* Label variables before creating tables
label variable y "Outcome Variable"

* Use descriptive filenames
outreg2 using results/table1_main.doc, replace

* Organize output in a folder
mkdir results
```

### Common Mistakes

```stata
* WRONG: forgetting replace/append
outreg2 using table.doc              // Error!

* WRONG: append on first model (creates weird output)
outreg2 using table.doc, append      // Should be replace

* WRONG: label option without labels set
outreg2 using t.doc, replace label   // Shows var names if no labels

* WRONG: too many decimal places
outreg2 using t.doc, replace dec(8)  // Cluttered; use 2-4

* FIX: drop unneeded variables
outreg2 using t.doc, replace keep(x1 x2 x3) nocons
```

### Troubleshooting

```stata
* "File already open" error: close Word/Excel, or use different filename
erase table.doc
outreg2 using table.doc, replace

* LaTeX special characters in labels
label variable pct_change "\% Change"

* Large/small numbers: rescale before regression
generate price_1000 = price / 1000
label variable price_1000 "Price (thousands)"

* Word uses .doc (not .docx)
outreg2 using table.doc, replace

* Update if broken after Stata upgrade
ssc install outreg2, replace
```

### Journal-Specific Formatting

```stata
* AER style
outreg2 using aer.tex, replace tex label dec(3) nocons ///
    addnote(Robust standard errors in parentheses., ///
            Significance: * 10\%, ** 5\%, *** 1\%.)

* Econometrica style (t-stats)
outreg2 using ecma.tex, replace tex label dec(3) tstat ///
    addnote(t-statistics in parentheses.)
```

### Option Combos for Common Tasks

```stata
* Clean academic table
outreg2 using paper.tex, replace tex label dec(3) ///
    addnote(Standard errors in parentheses., ///
            * p<0.05 ** p<0.01 *** p<0.001)

* Quick presentation
outreg2 using slides.doc, replace label dec(2) title(Main Results)

* Detailed diagnostics
outreg2 using diag.xls, replace excel label ///
    addstat(Adj R-sq, e(r2_a), F-stat, e(F), RMSE, e(rmse))

* Panel with indicators
outreg2 using panel.doc, replace label ///
    addtext(Individual FE, Yes, Year FE, Yes, Clustered SE, Yes)
```
