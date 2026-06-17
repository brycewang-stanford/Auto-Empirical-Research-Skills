# Stata Programming Basics

## Do-files and Ado-files

### Do-files

```stata
// Running
do "path/to/analysis.do"
quietly do "path/to/analysis.do"

// Best practice template
version 17
clear all
set more off
log using "analysis_log.log", replace

sysuse auto, clear
// ... analysis ...

log close
```

### Ado-files

Ado-files extend Stata's functionality and are auto-loaded when called.

```stata
* mysumm.ado
program define mysumm
    version 17
    syntax varlist [if] [in]
    marksample touse
    foreach var of local varlist {
        quietly summarize `var' if `touse'
        display as text "`var': " as result %9.2f r(mean) ///
            " (SD: " %9.2f r(sd) ")"
    }
end
```

**Where to save:** `adopath` shows directories. Use PLUS directory for user-installed programs.

---

## Local and Global Macros

### Local Macros

Exist only within the current program or do-file. Referenced with backtick-quote: `` `name' ``.

```stata
local filename "mydata.dta"
use "`filename'", clear

local n = 100
display "Sample size: `n'"

local demog_vars "age gender education income"
summarize `demog_vars'
```

**Extended macro functions:**

```stata
local price_label : variable label price
local foreign_vallabel : value label foreign
local count : word count `mylist'
local third : word 3 of `mylist'
```

### Global Macros

Persist throughout the session. Referenced with `$name`.

```stata
global datadir "/home/user/data"
use "$datadir/myfile.dta", clear

global controls "age gender education income"
regress outcome treatment $controls
```

**Caution:** Globals create conflicts across programs. Prefer locals. Clear when done: `macro drop _all`.

---

## Loops

### foreach Loop

```stata
// Over variable names
foreach var of varlist price mpg weight {
    quietly summarize `var'
    display "`var': mean = " r(mean)
}

// Over strings
foreach country in "USA" "Canada" "Mexico" {
    count if country == "`country'"
}

// Over a local macro
local outcomes "income health education"
foreach outcome of local outcomes {
    regress `outcome' `controls'
    estimates store model_`outcome'
}

// Over all numeric variables
foreach var of varlist _all {
    capture confirm numeric variable `var'
    if !_rc {
        summarize `var'
    }
}

// Nested loops
foreach year of local years {
    foreach region of local regions {
        // ...
    }
}
```

### forvalues Loop

**GOTCHA: No C-style increment operators.** Stata has no `++`, `--`, `+=`, etc.
```stata
* WRONG — Stata is not C
local i = 0
local ++i           // error: ++ does not exist

* RIGHT
local i = `i' + 1
```

```stata
forvalues i = 1/10 {
    display "Iteration `i'"
}

forvalues year = 2000(5)2020 {
    display "Year: `year'"
}

forvalues i = 1/5 {
    generate category`i' = (category == `i')
}
```

---

## Conditional Statements

```stata
// Basic if
if _N > 50 {
    display "Large dataset"
}

// if/else
capture confirm variable price
if !_rc {
    summarize price
}
else {
    display "Variable 'price' not found"
}

// if/else if/else
if `age' < 18 {
    local category "Minor"
}
else if `age' >= 18 & `age' < 65 {
    local category "Adult"
}
else {
    local category "Senior"
}

// capture for error handling
capture drop newvar
generate newvar = oldvar * 2

capture confirm file "mydata.dta"
if _rc == 0 {
    use mydata.dta, clear
}
else {
    display "File not found"
}
```

---

## Programs and Functions

### Basic Structure

```stata
program define programname
    version 17
    syntax [varlist] [if] [in] [, options]
    // Program code
end
```

### Program with syntax

```stata
program define myreg
    version 17
    syntax varlist(min=2) [if] [in] [, Robust CLuster(varname)]

    local depvar : word 1 of `varlist'
    local indepvars : list varlist - depvar

    if "`robust'" != "" {
        regress `depvar' `indepvars' `if' `in', robust
    }
    else if "`cluster'" != "" {
        regress `depvar' `indepvars' `if' `in', cluster(`cluster')
    }
    else {
        regress `depvar' `indepvars' `if' `in'
    }
end

myreg price mpg weight, robust
```

### Ado-file with Return Values

```stata
*! version 1.0.0
program define mystats, rclass
    version 17
    syntax varname [if] [in] [, Detail]
    marksample touse

    quietly summarize `varlist' if `touse', detail

    return scalar N = r(N)
    return scalar mean = r(mean)
    return scalar sd = r(sd)

    if "`detail'" != "" {
        return scalar p50 = r(p50)
    }

    display as text "Variable: " as result "`varlist'"
    display as text "Mean: " as result %9.2f return(mean)
end
```

---

## return and ereturn

### r-class (general results)

```stata
program define compute_stats, rclass
    syntax varname
    quietly summarize `varlist'
    return scalar mean = r(mean)
    return scalar cv = r(sd) / r(mean)
    return local varname "`varlist'"
end

compute_stats price
display "CV: " r(cv)
```

**Gotcha:** r-class results are overwritten by the next r-class command. Save to locals immediately.

### e-class (estimation results)

```stata
program define myregress, eclass
    syntax varlist [if] [in]
    marksample touse
    local depvar : word 1 of `varlist'
    local indepvars : list varlist - depvar
    regress `depvar' `indepvars' if `touse'
    ereturn local cmd "myregress"
    ereturn local depvar "`depvar'"
end
```

**Key difference:** e-class results persist until the next estimation command, even through r-class calls.

### Returning Matrices

```stata
program define return_matrix, rclass
    matrix A = (1, 2, 3 \ 4, 5, 6)
    return matrix mymatrix = A
end
```

---

## preserve and restore

```stata
preserve
collapse (mean) avg_price=price, by(foreign)
list
restore
// Original data unchanged

// In loops
foreach condition of local groups {
    preserve
    keep if `condition'
    summarize price mpg weight
    restore
}

// Nested
preserve
    drop if missing(rep78)
    preserve
        collapse (mean) price, by(foreign)
        list
    restore
    // Back to non-missing rep78 data
restore
// Back to original
```

---

## quietly and noisily

```stata
// Suppress output
quietly summarize price
display "Mean: " r(mean)

// Block suppression
quietly {
    use mydata, clear
    generate newvar = oldvar * 2
    summarize newvar
}

// Force display inside quiet block
quietly {
    noisily summarize newvar
    regress y x
}

// In loops (faster)
foreach var of varlist price mpg weight {
    quietly summarize `var'
    display "`var': mean = " %9.2f r(mean)
}

// Suppress errors
capture quietly {
    use nonexistent_file.dta
}
if _rc {
    display "Error occurred"
}
```

---

## Reusable Code Patterns

### Data Cleaning Program

```stata
program define clean_data, rclass
    version 17
    syntax [, Outliers(real 3)]
    local n_original = _N
    quietly {
        foreach var of varlist _all {
            capture confirm numeric variable `var'
            if !_rc {
                summarize `var', detail
                drop if abs(`var' - r(mean)) > `outliers' * r(sd)
            }
        }
    }
    local n_dropped = `n_original' - _N
    return scalar n_dropped = `n_dropped'
    display as text "Dropped: " as result `n_dropped'
end
```

### Data Validation

```stata
program define validate_data
    version 17
    syntax [, REQuired(varlist) POSitive(varlist) UNIque(varlist)]
    local errors = 0

    if "`required'" != "" {
        foreach var of local required {
            capture confirm variable `var'
            if _rc {
                display as error "Required variable `var' not found"
                local ++errors
            }
            else {
                count if missing(`var')
                if r(N) > 0 {
                    display as error "`var' has " r(N) " missing values"
                    local ++errors
                }
            }
        }
    }

    if `errors' == 0 {
        display as result "All checks passed"
    }
    else {
        display as error "`errors' error(s)"
        exit 198
    }
end
```

### Best Practices

1. **Version control:** `version 17`
2. **Document:** `*! version 1.0.0  Author`
3. **Validate inputs:** `marksample touse` + `count if `touse''`
4. **Return results:** `program define ..., rclass`
5. **Handle errors:** `capture confirm file ...`
6. **Modular design:** Separate programs for load, clean, analyze
