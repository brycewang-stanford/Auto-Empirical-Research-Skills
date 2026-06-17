# Stata Workflow Best Practices

## Contents

- [Project Organization and Folder Structure](#project-organization-and-folder-structure)
- [Master Do-Files and Modular Code](#master-do-files-and-modular-code)
- [Version Control with Git](#version-control-with-git)
- [Reproducible Research Practices](#reproducible-research-practices)
- [Code Commenting and Documentation](#code-commenting-and-documentation)
- [Data Management Best Practices](#data-management-best-practices)
- [Testing and Validation](#testing-and-validation)
- [Debugging Strategies](#debugging-strategies)
- [Performance Optimization](#performance-optimization)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)
- [Collaboration](#collaboration)

## Project Organization and Folder Structure

### Recommended Directory Layout

```
MyProject/
├── data/
│   ├── raw/              # Original, untouched data (READ ONLY)
│   ├── intermediate/     # Partially processed data
│   └── final/           # Analysis-ready datasets
├── code/
│   ├── 00_master.do     # Master script that runs everything
│   ├── 01_import.do     # Data import scripts
│   ├── 02_clean.do      # Data cleaning
│   ├── 03_construct.do  # Variable construction
│   ├── 04_analysis.do   # Statistical analysis
│   └── 05_tables.do     # Table and figure generation
├── output/
│   ├── tables/
│   ├── figures/
│   └── logs/
├── documentation/
│   ├── codebook.xlsx
│   └── methods.md
├── .gitignore
└── README.md
```

### Creating the Structure

```stata
local project_root "C:/Projects/MyProject"

foreach dir in data code output documentation {
    mkdir "`project_root'/`dir'"
}
foreach subdir in raw intermediate final {
    mkdir "`project_root'/data/`subdir'"
}
foreach subdir in tables figures logs {
    mkdir "`project_root'/output/`subdir'"
}
```

### Path Management with Global Macros

**00_setup.do**
```stata
clear all
set more off
set maxvar 10000

* Per-user project root
if "`c(username)'" == "johndoe" {
    global project "C:/Users/johndoe/Projects/MyProject"
}
else if "`c(username)'" == "janedoe" {
    global project "/Users/janedoe/Research/MyProject"
}
else {
    display as error "Unknown user: `c(username)'. Add your path to 00_setup.do"
    exit
}

* Define subdirectories
global data       "$project/data"
global raw        "$data/raw"
global intermediate "$data/intermediate"
global final      "$data/final"
global code       "$project/code"
global output     "$project/output"
global tables     "$output/tables"
global figures    "$output/figures"
global logs       "$output/logs"

* Verify directories exist
foreach dir in project data raw intermediate final code output tables figures logs {
    capture confirm file "${`dir'}/."
    if _rc {
        display as error "Directory not found: ${`dir'}"
        exit 601
    }
}
```

### Output Versioning

```stata
local today = string(date(c(current_date), "DMY"), "%tdCCYY-NN-DD")
export excel using "output/tables/table1_`today'.xlsx", replace
```

### Using profile.do

Create a `profile.do` in your Stata installation directory -- it runs automatically when Stata starts:

```stata
set more off, permanently
set maxvar 10000, permanently
set scrollbufsize 500000, permanently

global dropbox "C:/Users/YourName/Dropbox"
global projects "C:/Projects"

* Auto-install common packages
quietly {
    capture which estout
    if _rc ssc install estout, replace
}
```

---

## Master Do-Files and Modular Code

### Master Do-File Template

```stata
/*******************************************************************************
MASTER DO-FILE: Project Title
Author: Your Name | Date: 2025-11-23
Description: Runs the complete analysis pipeline.
Requires: Stata 17+, estout, outreg2, reghdfe
*******************************************************************************/

version 17
clear all
macro drop _all
set more off
set varabbrev off              // Require full variable names
capture log close _all

* Record start time
local start_time = clock(c(current_time), "hms")

* Define project paths
do "code/00_setup.do"

* Install required packages
local packages estout outreg2 reghdfe ftools
foreach pkg of local packages {
    capture which `pkg'
    if _rc ssc install `pkg', replace
}

* Create master log
local today = string(date(c(current_date), "DMY"), "%tdCCYY-NN-DD")
log using "$logs/master_`today'.log", replace text name(master)

* Execute pipeline with verification
foreach step in 01_import 02_clean 03_construct 04_analysis 05_tables {
    display as result _newline "{hline 80}"
    display as result "Running: `step'.do"
    display as result "{hline 80}"
    do "$code/`step'.do"
}

* Optional robustness section
local run_robustness = 1
if `run_robustness' {
    do "$code/06_robustness.do"
}

* Report runtime
local end_time = clock(c(current_time), "hms")
local runtime_min = round((`end_time' - `start_time')/60000, 0.1)
display as result "Total runtime: `runtime_min' minutes"

log close master
beep
```

**Tip**: Verify expected outputs between steps:
```stata
capture confirm file "$intermediate/merged_data.dta"
if _rc {
    display as error "ERROR: 01_import.do did not produce expected output"
    exit 601
}
```

### Modular Specifications with Loops

```stata
local spec1 "age education"
local spec2 "age education experience"
local spec3 "age education experience female"

forvalues i = 1/3 {
    regress income `spec`i''
    estimates store spec`i'

    outreg2 using "$tables/regressions.xlsx", ///
        excel label ctitle("Spec `i'") ///
        `=cond(`i'==1, "replace", "append")'
}

estimates table spec1 spec2 spec3, star stats(N r2 r2_a)
```

### Reusable Programs

```stata
capture program drop make_regtable
program define make_regtable
    syntax varlist, DEPvar(varname) [OUTfile(string) TITle(string)]

    if "`outfile'" == "" local outfile "$tables/regression_table.xlsx"
    if "`title'" == "" local title "Regression Results"

    regress `depvar' `varlist'

    outreg2 using "`outfile'", ///
        excel replace label title("`title'") ctitle("`depvar'") dec(3)
end

make_regtable age education experience, ///
    depvar(income) outfile("$tables/income_regression.xlsx")
```

---

## Version Control with Git

### .gitignore for Stata

```.gitignore
# Stata temporary files
*.tmp
*.smcl
*.stswp
*.gph

# Large data files
data/raw/*.dta
data/raw/*.csv
*.zip

# Regenerable logs
output/logs/*.log
output/logs/*.smcl

# OS files
.DS_Store
Thumbs.db

# Large output
*.pdf
output/figures/*.png

# Keep directory structure
!.gitkeep
```

### .gitattributes

```.gitattributes
# Stata files are binary
*.dta binary
*.gph binary

# Text files with LF line endings
*.do text eol=lf
*.ado text eol=lf
```

### Managing Data with Git

**Challenge**: .dta files are binary and often large.

```stata
* Use datasignature to verify raw data integrity
use "$raw/original_data.dta", clear
datasignature set, saving("$raw/original_data.sig")

* Later, verify data hasn't changed
datasignature confirm using "$data/raw/dataset.sig"
if _rc {
    display as error "WARNING: Data has changed since signature was set"
}
```

For small lookup tables you want to version, whitelist in .gitignore:
```bash
echo "!data/final/lookup_table.dta" >> .gitignore
```

### Do-File Version Headers

```stata
/*******************************************************************************
PROJECT: Analysis of Income Determinants
FILE:    04_analysis.do
AUTHOR:  Your Name
CREATED: 2025-01-15 | UPDATED: 2025-11-23

VERSION HISTORY:
v2.0 (2025-11-23): Major revision using new data
v1.2 (2025-02-15): Fixed standard error clustering
v1.1 (2025-02-01): Added education controls

INPUTS:  $final/analysis.dta
OUTPUTS: $tables/main_results.xlsx
DEPENDS: estout (ssc install estout)
*******************************************************************************/
```

---

## Reproducible Research Practices

### Reproducibility Checklist

- All code runs from master do-file without manual intervention
- All file paths use global macros (no hard-coded paths)
- All random number generators seeded
- `version` specified at top of every do-file
- All user-written packages documented and auto-installed
- All data sources documented with access dates
- All sample restrictions justified and documented

### Recording the Research Environment

```stata
log using "$output/logs/system_info.log", replace text

about
creturn list

* Check key package versions
foreach pkg in estout outreg2 reghdfe ftools {
    capture which `pkg'
    if !_rc {
        which `pkg'
    }
    else {
        display "`pkg': NOT INSTALLED"
    }
}

query memory
log close
```

### Seeding Random Number Generators

```stata
set seed 20251123

* Document seed in bootstrap/simulation code
bootstrap r(mean) = r(mean), reps(1000) seed(20251123): ///
    summarize income

* For multiple random operations, use different seeds
set seed 20251123
generate random1 = runiform()
set seed 20251124
generate random2 = runiform()
```

### Package Installation Script

```stata
local packages estout outreg2 reghdfe ftools winsor2 coefplot

foreach pkg of local packages {
    capture which `pkg'
    if _rc {
        display as result "Installing `pkg'..."
        ssc install `pkg', replace
    }
}
```

### Codebook Export

```stata
* Using codebookout
capture which codebookout
if _rc ssc install codebookout, replace
codebookout using "$documentation/codebook.xlsx", replace

* Manual alternative: export variable metadata
preserve
    describe, replace clear
    export excel using "$documentation/variables.xlsx", firstrow(variables) replace
restore
```

### Dynamic Documents

```stata
* markstat: Stata Markdown
ssc install markstat, replace
ssc install whereis, replace
dyndoc "analysis_report.md", replace
```

---

## Code Commenting and Documentation

### Comment Types

```stata
* Single-line comment (most common)
summarize income  // Inline comment

/*
Multi-line comment block
*/

/// Line continuation (not a comment per se)
regress income age education ///
        experience gender

*! Special comment for ado-file headers (preserved in help)
*! Version 1.0 2025-11-23
```

### Commenting: Explain WHY, Not WHAT

```stata
* GOOD: Explains reasoning
* Use log income because distribution is highly skewed
generate log_income = log(income)

* Winsorize at 1%/99% to reduce influence of outliers
winsor2 income, replace cuts(1 99)

* Include only working-age population for labor market analysis
keep if age >= 18 & age <= 65

* BAD: Just restates the code
* Generate log of income
generate log_income = log(income)
```

### Document Complex Logic and Sample Selection

```stata
/*******************************************************************************
SAMPLE SELECTION LOGIC
We restrict to:
1. Ages 25-65 (prime working age)
2. Non-missing income (dependent variable)
3. At least high school (focus on skilled labor)
4. Worked >= 20 hours/week (exclude part-time)
Following Smith et al. (2023, AER).
Initial N: 50,000 -> After restrictions: 32,456 (65% retention)
*******************************************************************************/

keep if age >= 25 & age <= 65
keep if !missing(income)
keep if education >= 12
keep if hours_worked >= 20
```

### Variable Documentation

```stata
generate log_income = log(income)
label variable log_income "Natural log of annual income (2024 USD)"
note log_income: Created from income variable on 2025-11-23
note log_income: Missing if income <= 0

label define education_lbl ///
    1 "Less than high school" ///
    2 "High school graduate" ///
    3 "Some college" ///
    4 "Bachelor's degree" ///
    5 "Graduate degree"
label values education education_lbl
```

---

## Data Management Best Practices

### Core Principles

1. **Never modify raw data** -- always save to intermediate/final
2. All changes documented in code
3. Validate at every step with assertions
4. Use `datasignature` to verify raw data integrity

### Variable Naming Conventions

```stata
* Consistent prefixes for constructed variables
generate ln_income = log(income_total)       // ln_ for natural log
generate d_employed = (employment_status == 1)  // d_ for dummy
generate z_income = (income - r(mean))/r(sd)  // z_ for standardized

* Time suffix for panel data
rename income income_2024

* Indices
egen ses_index = rowmean(income_z educ_z occupation_z)
```

### Data Validation Program

```stata
capture program drop validate_data
program define validate_data

    * Check for duplicate IDs
    duplicates report id

    * Validate required variables exist
    foreach var in id age income education {
        confirm variable `var'
    }

    * Validate ranges
    quietly count if !inrange(age, 0, 120) & !missing(age)
    if r(N) > 0 {
        display as error "`r(N)' observations with invalid age"
        list id age if !inrange(age, 0, 120) & !missing(age)
        error 459
    }

    * Missing value patterns
    misstable summarize, all
end
```

### Assertions for Quality Control

```stata
assert !missing(id)
assert inrange(age, 0, 120) | missing(age)
assert inlist(gender, 0, 1, .)
assert income >= wage_income if !missing(income, wage_income)
isid id  // ID must uniquely identify observations

* Custom assertion with informative error
capture assert income > 0 if employed == 1
if _rc {
    display as error "Found employed individuals with zero income"
    list id income employed if income <= 0 & employed == 1
    error 459
}
```

### Missing Data Handling

```stata
* Comprehensive missing analysis
misstable summarize
misstable patterns income education employment, frequency

* Create missing indicators
foreach var in income education employment {
    generate byte miss_`var' = missing(`var')
    label variable miss_`var' "Missing indicator for `var'"
}

* Test MCAR by comparing characteristics
foreach var in age gender race {
    ttest `var', by(miss_income)
}

* Multiple imputation
mi set wide
mi register imputed income education
mi impute chained (regress) income (regress) education = age gender, ///
    add(20) rseed(20251123) augment
```

### Standardize Missing Value Codes

```stata
foreach var of varlist _all {
    quietly replace `var' = . if inlist(`var', -99, -98, -97, 999)
}
```

---

## Testing and Validation

### Test Suite Pattern

```stata
capture program drop run_tests
program define run_tests
    local tests 0
    local passed 0
    local failed 0

    * Test 1: Data loads
    local ++tests
    capture use "$final/analysis.dta", clear
    if _rc == 0 {
        local ++passed
    }
    else {
        local ++failed
        display as error "FAILED: Data load"
    }

    * Test 2: No missing IDs
    local ++tests
    quietly count if missing(id)
    if r(N) == 0 {
        local ++passed
    }
    else {
        local ++failed
        display as error "FAILED: `r(N)' missing IDs"
    }

    * Summary
    display "Tests: `tests' | Passed: `passed' | Failed: `failed'"
    if `failed' > 0 error 459
end
```

### Unit Testing Custom Programs

```stata
* Define a program, then test it
sysuse auto, clear

calculate_winsorized_mean price
assert r(mean) > 0
display "Test 1 passed: Returns positive mean"

calculate_winsorized_mean price, percentile(10)
local mean1 = r(mean)
calculate_winsorized_mean price, percentile(5)
local mean2 = r(mean)
assert `mean1' != `mean2'
display "Test 2 passed: Different percentiles give different results"

calculate_winsorized_mean price if foreign == 1
assert r(N) == 22
display "Test 3 passed: If condition works correctly"
```

### Regression Validation

```stata
regress income age education experience

* Multicollinearity
quietly vif
* VIF > 10 indicates concern

* Residual normality
predict resid, residuals
quietly sktest resid

* Heteroskedasticity
quietly estat hettest
* If p < 0.05, use robust SE

* Influential outliers
predict cooksd, cooksd
quietly count if cooksd > 4/_N

drop resid cooksd
```

### K-Fold Cross-Validation

```stata
set seed 20251123
local k = 10

generate fold = mod(_n, `k') + 1
matrix results = J(`k', 2, .)
matrix colnames results = rmse r2

forvalues i = 1/`k' {
    quietly regress income age education experience if fold != `i'
    quietly predict yhat if fold == `i'
    quietly generate error = (income - yhat)^2 if fold == `i'
    quietly summarize error if fold == `i'
    matrix results[`i', 1] = sqrt(r(mean))
    quietly correlate income yhat if fold == `i'
    matrix results[`i', 2] = r(rho)^2
    drop yhat error
}

matrix list results
drop fold
```

### Sensitivity Analysis

```stata
quietly regress income age education experience
estimates store baseline

quietly regress income c.age##c.age education experience
estimates store alt_quadratic

quietly regress income age education experience if age >= 25
estimates store alt_sample

quietly regress income age education experience, robust
estimates store alt_robust

esttab baseline alt_quadratic alt_sample alt_robust ///
    using "$tables/sensitivity.rtf", ///
    label star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2, labels("Observations" "R-squared")) ///
    title("Sensitivity Analysis") replace
```

---

## Debugging Strategies

### Debugging Tools

#### Trace Mode

```stata
set trace on
* Run problematic code
set trace off

* Limit depth for less noise
set trace on, depth(2)
```

#### Pause for Interactive Inspection

```stata
forvalues i = 1/10 {
    summarize income if group == `i'
    if `i' == 5 {
        pause on
        pause  // Execution stops; type 'q' to continue
    }
}
pause off
```

#### Return Code Handling

```stata
capture merge 1:1 id using "$data/other.dta"

if _rc == 0 {
    display as result "Merge successful"
}
else if _rc == 601 {
    display as error "File not found"
}
else if _rc == 459 {
    display as error "Merge variable problems"
}
else {
    display as error "Unexpected error: " _rc
    error _rc
}
```

#### Profiling with set rmsg

```stata
set rmsg on
* Timing info appears after each command
summarize income
regress income age education
set rmsg off
```

### Common Error Patterns and Fixes

| Error | Code | Cause | Fix |
|-------|------|-------|-----|
| `r(111)` | no variables defined | Typo or variable doesn't exist | `lookfor income` or `ds *income*` |
| `r(2000)` | no observations | All obs excluded by `if` | Check conditions with `count if ...` |
| `r(109)` | type mismatch | String vs numeric confusion | `describe var` then `destring var, replace force` |
| `r(5)` | not sorted | `by:` requires sorted data | Use `bysort` instead of `by` |
| `r(110)` | already defined | Variable already exists | `capture drop var` before `generate` |

### Debugging a Merge

```stata
* Before merging, inspect both sides
use "$data/dataset1.dta", clear
describe id
codebook id
duplicates report id

use "$data/dataset2.dta", clear
describe id                        // Check type matches dataset1
codebook id
duplicates report id

* Merge with diagnostic variable
use "$data/dataset1.dta", clear
merge 1:1 id using "$data/dataset2.dta", generate(_merge_debug)
tabulate _merge_debug
list id if _merge_debug == 1       // Only in master
list id if _merge_debug == 2       // Only in using
```

---

## Performance Optimization

### Timing Code

```stata
timer clear
timer on 1
summarize income
timer off 1

timer on 2
regress income age education
timer off 2

timer list
```

### Efficient Data Loading

```stata
* BAD: Load entire dataset then subset
use "$data/huge_dataset.dta", clear
keep if year == 2024
keep id income age education

* GOOD: Load only what you need
use id income age education if year == 2024 ///
    using "$data/huge_dataset.dta", clear
```

### Vectorize Instead of Loop

```stata
* BAD: Row-by-row loop (100x+ slower)
generate income_cat = .
forvalues i = 1/`=_N' {
    if income[`i'] < 25000 replace income_cat = 1 in `i'
    else if income[`i'] < 50000 replace income_cat = 2 in `i'
    else replace income_cat = 3 in `i'
}

* GOOD: Vectorized
generate income_cat = 1
replace income_cat = 2 if income >= 25000
replace income_cat = 3 if income >= 50000

* BEST: Use egen or recode
egen income_cat2 = cut(income), at(0,25000,50000,1000000)
```

### Efficient Loops

```stata
* BAD: Loading data inside loop
forvalues year = 2000/2020 {
    use "$data/panel.dta", clear     // Reloads every iteration!
    keep if survey_year == `year'
    summarize income
}

* GOOD: Load once, use preserve/restore
use "$data/panel.dta", clear
forvalues year = 2000/2020 {
    preserve
    keep if survey_year == `year'
    summarize income
    restore
}

* BEST: Use bysort when possible
use "$data/panel.dta", clear
bysort survey_year: egen mean_income = mean(income)
```

### Data Type Optimization

```stata
* compress auto-optimizes all storage types
compress

* Manual: use appropriate types
generate byte age = person_age      // 1 byte instead of 8
recast byte gender                  // If only 0/1
recast int year                     // Integer year values
recast float income                 // If extreme precision not needed
```

### Memory Management with Frames (Stata 16+)

```stata
frame create demographics
frame demographics: use "$data/demographics.dta"

frame create income
frame income: use "$data/income.dta"

* Switch without loading/unloading
frame change demographics
summarize age

frame change income
summarize income

frame drop demographics income
```

### Efficient Merging

```stata
* Pre-sort for faster merge
sort id
merge 1:1 id using "$data/large2_sorted.dta", sorted

* Load only needed variables from using dataset
merge 1:1 id using "$data/large2.dta", keepusing(income education)
```

### Parallel Processing

```stata
ssc install parallel, replace
parallel setclusters 4

* Parallel bootstrap
parallel bootstrap r(mean), reps(1000): summarize income
```

---

## Common Mistakes to Avoid

### Top Gotchas

**1. Missing values are treated as +infinity in comparisons**
```stata
* WRONG: Missing income becomes 1!
generate high_income = (income > 50000)

* RIGHT:
generate high_income = (income > 50000) if !missing(income)
```

**2. Overwriting raw data**
```stata
* NEVER do this:
use "$raw/original.dta", clear
drop if age < 18
save "$raw/original.dta", replace    // DESTROYED!

* Always save to intermediate/final
save "$intermediate/filtered.dta", replace
```

**3. Not validating merges**
```stata
* WRONG:
merge 1:1 id using "$data/other.dta"
drop _merge

* RIGHT:
merge 1:1 id using "$data/other.dta"
tabulate _merge
assert _merge == 3   // Or handle non-matches
drop _merge
```

**4. Confusing = and ==**
```stata
* WRONG (syntax error):
generate employed = 1 if status = 1

* RIGHT:
generate employed = 1 if status == 1
```

**5. Not checking for duplicates before merge**
```stata
duplicates report id
assert r(unique_value) == r(N)
merge 1:1 id using "$data/other.dta"
```

**6. Using `by:` without sorting**
```stata
* WRONG: Error if not sorted
by id: generate first = _n == 1

* RIGHT: bysort auto-sorts
bysort id: generate first = _n == 1
```

**7. Forgetting preserve/restore**
```stata
* WRONG: Original data lost after collapse
collapse (mean) income, by(state)

* RIGHT:
preserve
collapse (mean) income, by(state)
* ... use collapsed data ...
restore
```

**8. Not setting seed**
```stata
* WRONG: Not reproducible
generate random_sample = runiform()

* RIGHT:
set seed 20251123
generate random_sample = runiform()
```

**9. Ignoring return codes from capture**
```stata
* WRONG:
capture some_command
* Continue regardless

* RIGHT:
capture some_command
if _rc != 0 {
    display as error "Command failed: " _rc
    exit _rc
}
```

**10. Using egen when summarize suffices**
```stata
* Slower:
egen mean_income = mean(income)

* Faster:
summarize income
generate mean_income = r(mean)
```

**11. Not specifying version**
```stata
* At top of every do-file:
version 17
```

**12. Forgetting to close log files**
```stata
* Start with capture log close to handle previously unclosed logs
capture log close
log using "analysis.log", replace
* ... work ...
log close
```

**13. Forgetting quotes around string labels**
```stata
* WRONG:
label variable income Annual income in USD

* RIGHT:
label variable income "Annual income in USD"
```

**14. Not compressing before save**
```stata
compress
save "$final/analysis.dta", replace
```

**15. Using wrong weight type**
```stata
* pweight = probability/sampling weights (most survey data)
regress income age [pweight = survey_weight]

* aweight = analytic/precision weights
regress income age [aweight = cell_size]
```

---

## Collaboration

### Style Guide Essentials

```stata
* Variables: lowercase_with_underscores
* Files: numbered_descriptive_names.do
* Indent: 4 spaces (not tabs)
* Max line length: 80 chars, use /// for continuation
* Blank line between sections
* Space after commas, around operators

* GOOD:
egen age_group = cut(age), ///
    at(18, 25, 35, 45, 55, 65, 100) ///
    label

* BAD:
egen age_group=cut(age),at(18,25,35,45,55,65,100) label
```

### Team Setup File

```stata
* Each team member's path
if "`c(username)'" == "alice" {
    global project "C:/Users/alice/Research/TeamProject"
}
else if "`c(username)'" == "bob" {
    global project "/Users/bob/Projects/TeamProject"
}

* Auto-install required packages
local packages estout outreg2 reghdfe ftools
foreach pkg of local packages {
    capture which `pkg'
    if _rc ssc install `pkg', replace
}

set varabbrev off, permanently
set more off, permanently
```

### Shared Utility Functions

```stata
* lib/team_functions.do -- source this in master do-file

capture program drop winsorize
program define winsorize
    syntax varname [if] [in], Percentile(real 5)
    marksample touse
    quietly {
        summarize `varlist' if `touse', detail
        local p_low = `percentile'
        local p_high = 100 - `percentile'
        replace `varlist' = r(p`p_low') if `varlist' < r(p`p_low') & `touse'
        replace `varlist' = r(p`p_high') if `varlist' > r(p`p_high') & `touse'
    }
end

capture program drop export_regression
program define export_regression
    syntax using/, [TITle(string) replace append]
    outreg2 using "`using'", excel label title("`title'") dec(3) `replace' `append'
end
```

### Data Dictionary Generation

```stata
use "$final/analysis.dta", clear
describe, replace clear
export excel using "$documentation/data_dictionary.xlsx", firstrow(variables) replace
```
