# Winsorizing in Stata: winsor and winsor2

## Overview

Winsorizing caps extreme values at specified percentiles rather than removing observations. Two packages are available:
- `winsor` - Basic command by Nicholas Cox (single variable at a time)
- `winsor2` - Enhanced version by Yujun Lian (multiple variables, by-group, replace option)

**Winsorizing vs. trimming:** Winsorizing replaces extremes with percentile values (preserves N). Trimming deletes extremes (reduces N).

---

## Installation

```stata
ssc install winsor
ssc install winsor2
help winsor
help winsor2
```

---

## winsor (Basic Command)

```stata
* Syntax
winsor varname [if] [in], gen(newvar) p(#)

* Options:
*   p(#)   - Fraction for each tail (0.01 = 1%/99%, 0.05 = 5%/95%)
*   gen()  - Name for new variable (required)
*   h(#)   - High-tail fraction (asymmetric)
*   l(#)   - Low-tail fraction (asymmetric)
```

### Examples

```stata
sysuse auto, clear

* Symmetric: 1% each tail
winsor price, gen(price_w1) p(0.01)

* Symmetric: 5% each tail
winsor price, gen(price_w5) p(0.05)

* Asymmetric cutoffs
winsor price, gen(price_asym) l(0.01) h(0.05)

* Only upper tail
winsor price, gen(price_upper) l(0) h(0.05)

* Only lower tail
winsor price, gen(price_lower) l(0.05) h(1)
```

**Limitation:** Only handles one variable at a time. Use a loop for multiple:

```stata
local varlist "price mpg weight length"
foreach var of local varlist {
    winsor `var', gen(`var'_w) p(0.05)
}
```

---

## winsor2 (Enhanced Command)

```stata
* Syntax
winsor2 varlist [if] [in] [, options]

* Key options:
*   cuts(# #)    - Lower and upper percentile cutoffs (e.g., cuts(1 99))
*   suffix(str)  - Suffix for new variables (default: _w)
*   replace      - Overwrite original variables (destructive!)
*   trim         - Trim (delete) instead of winsorize
*   by(varlist)  - Winsorize within groups
*   label        - Add labels to new variables
```

### Basic Usage

```stata
sysuse auto, clear

* Single variable
winsor2 price, cuts(1 99) suffix(_w)

* Multiple variables at once
winsor2 price mpg weight, cuts(1 99) suffix(_wins)

* Variable range
winsor2 price-trunk, cuts(5 95) suffix(_w)

* Replace original (use with caution)
preserve
winsor2 price mpg weight, cuts(1 99) replace
restore
```

### By-Group Winsorizing

When groups have different distributions, winsorize within groups:

```stata
sysuse auto, clear

* By a single grouping variable
winsor2 price, cuts(5 95) suffix(_bygroup) by(foreign)

* Panel data: by firm
webuse grunfeld, clear
winsor2 invest, cuts(1 99) suffix(_w) by(company)

* By industry-year (common in finance research)
* egen industry_year = group(industry year)
* winsor2 roa roe leverage, cuts(1 99) suffix(_w) by(industry_year)
```

### Trimming with winsor2

```stata
* trim option deletes observations instead of capping
winsor2 price, cuts(1 99) trim
* WARNING: This drops observations, reducing N
```

---

## Replace vs. Suffix

```stata
* suffix (safer -- keeps original)
winsor2 price mpg, cuts(1 99) suffix(_w)
* Creates price_w, mpg_w; originals unchanged

* replace (destructive -- overwrites original)
preserve
winsor2 price mpg, cuts(1 99) replace
* Original values are gone
restore
```

**Best practice:** Use `suffix()` and keep originals for robustness checks. If you must use `replace`, wrap in `preserve`/`restore` or back up data first.

---

## Common Percentile Choices

| Context | Percentiles | Notes |
|---------|------------|-------|
| Finance/accounting (large N) | 1%/99% or 0.5%/99.5% | Standard in JF, RFS, JAR |
| Economics (large N) | 1%/99% | Conservative |
| Economics (medium N) | 2.5%/97.5% or 5%/95% | |
| Small samples (N < 100) | Avoid winsorizing | Too few obs; consider robust regression |

```stata
* Common specifications
winsor2 price, cuts(1 99) suffix(_w1)       // Conservative
winsor2 price, cuts(2.5 97.5) suffix(_w2p5) // Moderate
winsor2 price, cuts(5 95) suffix(_w5)       // Aggressive
```

**Rule of thumb:** At 1% with N=100, you are capping ~1 observation per tail. With N < 50, winsorizing removes too much information -- use `rreg` (robust regression) or `qreg` (quantile regression) instead.

---

## Quality Control After Winsorizing

```stata
winsor2 roa, cuts(1 99) suffix(_w)

* Check how many observations changed
gen changed = (roa != roa_w)
tab changed
* Should be ~2% (1% each tail)

* Verify percentile boundaries
_pctile roa, p(1 99)
summarize roa_w
* Min should equal 1st percentile, max should equal 99th

* Visual check
scatter roa_w roa
* Should see diagonal line with horizontal flats at tails
```

---

## Workflow: Order of Operations

```stata
* CORRECT order:
use firm_data, clear

* 1. Construct variables
gen roa = net_income / total_assets

* 2. Apply sample restrictions
drop if total_assets < 10
keep if year >= 2000

* 3. Winsorize within final sample
winsor2 roa leverage, cuts(1 99) suffix(_w)

* 4. Run analysis
regress y roa_w leverage_w
```

**Important:** Winsorize AFTER sample restrictions so percentiles are based on the observations actually used in analysis.

---

## Robustness: Comparing Outlier Treatments

```stata
sysuse auto, clear
estimates clear

* No treatment
regress mpg price weight
estimates store m1

* Winsorize 1%
winsor2 price weight, cuts(1 99) suffix(_w1)
regress mpg price_w1 weight_w1
estimates store m2

* Winsorize 5%
winsor2 price weight, cuts(5 95) suffix(_w5)
regress mpg price_w5 weight_w5
estimates store m3

* Log transformation
gen log_price = log(price)
gen log_weight = log(weight)
regress mpg log_price log_weight
estimates store m4

* Robust regression
rreg mpg price weight
estimates store m5

esttab m1 m2 m3 m4 m5, ///
    mtitles("Original" "Wins1%" "Wins5%" "Log" "Robust") ///
    b(3) se(3) r2 star(* 0.10 ** 0.05 *** 0.01)
```

---

## Quick Reference

```stata
* Install
ssc install winsor
ssc install winsor2

* winsor: single variable, fraction-based
winsor price, gen(price_w) p(0.01)           // 1%/99%
winsor price, gen(price_w) p(0.05)           // 5%/95%
winsor price, gen(price_w) l(0.01) h(0.05)   // Asymmetric

* winsor2: multiple variables, percentile-based
winsor2 price mpg weight, cuts(1 99) suffix(_w)
winsor2 price mpg weight, cuts(5 95) replace
winsor2 roa roe, cuts(1 99) suffix(_w) by(industry)
winsor2 price, cuts(1 99) trim               // Trim instead

* Related commands
help _pctile   // Calculate percentiles manually
help rreg      // Robust regression (alternative to winsorizing)
help qreg      // Quantile regression (alternative)
```

### When NOT to Winsorize

- Extreme values are your research focus (e.g., fraud detection, tail risk)
- Very small samples (N < 50)
- Outliers are clearly data errors (fix or delete instead)
- Theory predicts heavy tails (e.g., income, firm size -- use log transform)
- Distribution is already well-behaved (check with `summarize, detail`)
