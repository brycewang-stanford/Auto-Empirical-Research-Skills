# asdoc: Automatic Document Creation in Stata

## Overview

`asdoc` creates formatted tables in Word, LaTeX, HTML, and text by adding a simple prefix to Stata commands. No need to store estimation results -- just prefix your command with `asdoc`.

**Key features:**
- Simple prefix syntax for most Stata commands
- Automatic formatting for Word documents (.doc/.docx)
- Supports: `summarize`, `tabstat`, `correlate`, `pwcorr`, `regress`, `xtreg`, `logit`, `probit`, `tabulate`, `ttest`, `anova`, and more
- Append multiple tables to one document
- Output to Word (default), LaTeX, HTML, or plain text

---

## Installation

```stata
ssc install asdoc
help asdoc
which asdoc
```

**Important:** Output files are created in your current working directory. Check with `pwd`.

---

## Quick Start

```stata
sysuse auto, clear

* Just prefix your command with asdoc
asdoc summarize price mpg weight, replace

* Append additional tables to the same document
asdoc correlate price mpg weight, append
asdoc regress price mpg weight foreign, append

* Default output file is "MyFile.doc" in current directory
```

---

## File Management

```stata
* Specify custom filename
asdoc summarize price mpg weight, save(mystats.doc) replace

* Full path
asdoc summarize price mpg, save("C:/Tables/summary.doc") replace

* Pattern: replace for first table, append for the rest
asdoc summarize price mpg, replace
asdoc correlate price mpg, append
asdoc regress price mpg weight, append
```

**Output format is determined by file extension:**
```stata
asdoc summarize price, save(file.doc) replace   // Word (default)
asdoc summarize price, save(file.tex) replace   // LaTeX
asdoc summarize price, save(file.html) replace  // HTML
asdoc summarize price, save(file.txt) replace   // Plain text
```

---

## Summary Statistics

```stata
sysuse auto, clear

* Basic summary
asdoc summarize price mpg weight, replace

* Detailed summary (adds percentiles, skewness, kurtosis)
asdoc summarize price mpg weight, detail replace

* With title and decimal control
asdoc summarize price mpg weight, ///
    title(Table 1: Summary Statistics) dec(2) replace

* tabstat for specific statistics
asdoc tabstat price mpg weight, ///
    statistics(n mean sd min max) replace

* tabstat by groups
asdoc tabstat price mpg weight, ///
    by(foreign) statistics(mean sd) replace
```

### Summary by Groups (Manual Panels)

```stata
asdoc, row(Domestic Cars) replace
asdoc summarize price mpg weight if foreign == 0, append

asdoc, row(Foreign Cars) append
asdoc summarize price mpg weight if foreign == 1, append
```

---

## Regression Tables

```stata
sysuse auto, clear

* Basic regression
asdoc regress price mpg weight, replace

* With robust standard errors
asdoc regress price mpg weight foreign, robust replace

* Clustered standard errors
asdoc regress price mpg weight, vce(cluster rep78) replace

* Control which statistics to display
asdoc regress price mpg weight foreign, ///
    stat(coef se tstat pvalue) dec(3) replace
```

### Progressive Model Building

```stata
asdoc, text(Model 1: Baseline) replace
asdoc regress price mpg, append

asdoc, text(Model 2: Adding Weight) append
asdoc regress price mpg weight, append

asdoc, text(Model 3: Full Model) append
asdoc regress price mpg weight foreign, append
```

**Gotcha:** `asdoc` shows models sequentially (not side-by-side in columns). For side-by-side model comparison, use `estout/esttab` instead.

---

## Panel Data

```stata
webuse nlswork, clear
xtset idcode year

* Fixed effects
asdoc xtreg ln_wage age ttl_exp tenure, fe replace

* Random effects
asdoc xtreg ln_wage age ttl_exp tenure, re append

* With robust SE
asdoc xtreg ln_wage age ttl_exp tenure, fe robust append
```

---

## Correlation Matrices

```stata
sysuse auto, clear

* Simple correlation
asdoc correlate price mpg weight, replace

* Pairwise with significance stars
asdoc pwcorr price mpg weight foreign, star(all) replace

* With p-values and observation counts
asdoc pwcorr price mpg weight, star(0.05) obs replace

* Custom title and formatting
asdoc pwcorr price mpg weight foreign, ///
    star(0.05) title(Correlation Matrix) dec(3) replace
```

---

## Other Statistical Commands

```stata
* Cross-tabulation with chi-square
asdoc tabulate foreign rep78, chi2 replace

* Two-sample t-test
asdoc ttest price, by(foreign) replace

* ANOVA
asdoc anova price foreign rep78, replace

* Logit with odds ratios
asdoc logit foreign mpg weight price, or replace

* Probit
asdoc probit foreign mpg weight price, replace
```

---

## Document Structure: Text, Rows, and Titles

```stata
* Section headers with text()
asdoc, text(SECTION 1: DESCRIPTIVE ANALYSIS) replace
asdoc summarize price mpg weight, append

asdoc, text() append   // Blank line for spacing

asdoc, text(SECTION 2: REGRESSION ANALYSIS) append
asdoc regress price mpg weight, append

* Row labels for subsections
asdoc, row(Panel A: Full Sample) replace
asdoc summarize price mpg, append

asdoc, row(Panel B: Domestic Only) append
asdoc summarize price mpg if foreign == 0, append

* Table titles
asdoc summarize price mpg, ///
    title(Table 1: Descriptive Statistics) replace
```

---

## Formatting Options

| Option | Description |
|--------|-------------|
| `replace` | Create new file (overwrite existing) |
| `append` | Add to existing file |
| `save(filename)` | Specify output filename and format |
| `title(text)` | Add table title |
| `dec(#)` | Set decimal places (default ~3) |
| `stat(list)` | Select regression statistics: `coef`, `se`, `tstat`, `pvalue` |
| `font(name)` | Set font (e.g., `Times New Roman`, `Arial`) |
| `fs(#)` | Set font size |

### Helper Commands

```stata
asdoc, text(your text here) append   // Add text line
asdoc, row(label text) append        // Add row label
asdoc, text() append                 // Blank line
asdoc, version                       // Check version
```

---

## Loops and Automation

```stata
* Loop through variables
asdoc, text(Variable Summaries) replace
foreach var of varlist price mpg weight {
    asdoc, row(`var' Statistics) append
    asdoc summarize `var', append
}

* Loop through groups
levelsof foreign, local(levels)
foreach lev of local levels {
    asdoc, row(Foreign = `lev') append
    asdoc summarize price mpg if foreign == `lev', append
}

* Reusable report program
capture program drop make_report
program make_report
    syntax varlist using/
    asdoc, text(AUTOMATED REPORT) save(`using') replace
    asdoc, text(Generated: `c(current_date)') append
    asdoc summarize `varlist', append
    asdoc correlate `varlist', append
end

make_report price mpg weight using "report.doc"
```

### Dated Filenames

```stata
local date: display %tdCYND daily("$S_DATE", "DMY")
asdoc summarize price, save(summary_`date'.doc) replace
```

---

## When to Use asdoc vs. Alternatives

| Need | Package |
|------|---------|
| Quick reports, exploratory analysis, Word output | **asdoc** |
| Publication-quality tables, side-by-side models, LaTeX | **estout/esttab** |
| Complete document control, mixed content | **putdocx** (Stata 15+) |
| Regression-specific tables | **outreg2** |

**Key asdoc limitations:**
- Models displayed sequentially, not in columns
- Limited layout customization compared to estout
- Less LaTeX control than estout

**Key asdoc advantages:**
- No need to store estimates (`eststo` not required)
- Works with many command types beyond regression
- Minimal learning curve

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Can't find output file | Check `pwd`; use `save()` with full path |
| Accidentally overwrote file | Use `append` after first `replace`; or use different filenames |
| Inconsistent decimals | Set `dec(#)` on every call |
| Variables show names not labels | `label variable` before calling asdoc |
| Regression output too detailed | Use `stat(coef se)` to select statistics |

---

## Quick Reference

```stata
* Summary statistics
asdoc summarize varlist, replace
asdoc tabstat varlist, statistics(mean sd min max) replace

* Correlation
asdoc correlate varlist, replace
asdoc pwcorr varlist, star(all) replace

* Regression
asdoc regress depvar indepvars, replace
asdoc regress depvar indepvars, robust stat(coef se tstat) dec(3) replace

* Panel data
asdoc xtreg depvar indepvars, fe replace
asdoc xtreg depvar indepvars, re append

* Binary outcome
asdoc logit depvar indepvars, or replace
asdoc probit depvar indepvars, replace

* Cross-tabulation
asdoc tabulate var1 var2, chi2 replace

* T-test
asdoc ttest var, by(group) replace

* Text and structure
asdoc, text(Section Header) replace
asdoc, row(Subsection Label) append
asdoc, text() append   // blank line
```
