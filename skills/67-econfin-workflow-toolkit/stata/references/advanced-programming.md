# Advanced Stata Programming

## Syntax Parsing

### Complete Syntax Specification

```stata
program define advanced_syntax_demo
    version 17
    #delimit ;
    syntax [varlist(min=1 max=5 numeric default=none)]
           [if] [in] [using/]
           [fweight aweight pweight iweight]
           [,
           Required(varname numeric)
           OPTional(varname)
           STRing(string)
           INTeger(integer 10)
           REAL(real 0.5)
           NUMlist(numlist min=1 max=10 >0 <=100)
           VARList(varlist numeric min=2)
           GENerate(name)
           REPlace
           BY(varlist)
           Level(cilevel)
           *                        // Catch additional options
           ];
    #delimit cr
    marksample touse
end
```

### Varlist Specifications

```stata
syntax varlist(numeric)              // Numeric only
syntax varlist(string)               // String only
syntax varlist(min=2 max=10)         // Count constraints
syntax [varlist(default=none)]       // Optional, empty default
syntax varlist(ts)                   // Time-series operators allowed
syntax varlist(fv)                   // Factor variables allowed
syntax varlist(ts fv numeric)        // Combined
```

### Option Types

```stata
// Flags
syntax [, Replace NOIsily Detail]
if "`replace'" != "" { ... }

// Typed arguments
syntax [, SAVing(string) Level(cilevel) GENerate(name) BY(varlist)]

// Integer/real with defaults and validation
syntax [, Reps(integer 1000) Alpha(real 0.05)]
if `reps' < 100 {
    display as error "reps() must be at least 100"
    exit 198
}

// Numlist
syntax [, NUMlist(numlist min=1 >=0 <=1)]

// String preserving quotes
syntax [, TItle(string asis)]
```

### Passthru Options

Pass options directly to sub-commands:

```stata
program define regression_wrapper
    version 17
    syntax varlist [if] [in] [, VCE(passthru) Level(passthru) *]
    gettoken depvar indepvars : varlist
    regress `depvar' `indepvars' `if' `in', `vce' `level' `options'
end
```

### Mutually Exclusive Options

```stata
local optcount = 0
foreach opt in mean median sum count {
    if "``opt''" != "" local ++optcount
}
if `optcount' > 1 {
    display as error "mean, median, sum, count are mutually exclusive"
    exit 184
}
```

---

## gettoken and tokenize

### gettoken: Extract Tokens One at a Time

```stata
gettoken token rest : string [, parse(chars) quotes]

// Separate dependent from independent variables
gettoken depvar indepvars : varlist

// Custom delimiter
local mystring "one,two,three"
gettoken first rest : mystring, parse(",")
// first = "one", rest = ",two,three"

// Parsing parenthetical expressions
gettoken first rest : string, parse("()")
```

### tokenize: Split into Numbered Macros

```stata
tokenize `mystring'
display "`1'"  "`2'"  "`3'"

// Count tokens
local i = 1
while "``i''" != "" {
    local ++i
}
local ntokens = `i' - 1

// Processing variable pairs
tokenize `pairlist'
local i = 1
while "``i''" != "" {
    local var1 "``i''"
    local i = `i' + 1
    local var2 "``i''"
    local i = `i' + 1
    correlate `var1' `var2'
}
```

---

## Matrix Programming

### Matrix Basics

```stata
matrix A = (1, 2, 3 \ 4, 5, 6 \ 7, 8, 9)
matrix accum R = price mpg weight       // From variables
matrix I = I(3)                         // Identity
matrix Z = J(3, 4, 0)                  // Zeros

// Operations
matrix D = B + C
matrix E = B * C'                       // Multiply
matrix F = 2 * B                        // Scalar multiply

// Functions
matrix B = A'                           // Transpose
matrix Ainv = syminv(A)                 // Symmetric inverse
matrix d = vecdiag(A)                   // Diagonal
matrix symeigen X L = A                 // Eigendecomposition
```

### Custom OLS via Matrices

```stata
program define matrix_ols, rclass
    version 17
    syntax varlist
    gettoken depvar indepvars : varlist
    tempname X y XX Xy b V

    mkmat `indepvars', matrix(`X')
    mkmat `depvar', matrix(`y')
    local n = rowsof(`X')
    matrix ones = J(`n', 1, 1)
    matrix `X' = ones, `X'

    matrix `XX' = `X'' * `X'
    matrix `Xy' = `X'' * `y'
    matrix `b' = syminv(`XX') * `Xy'

    matrix yhat = `X' * `b'
    matrix e = `y' - yhat
    matrix e2 = e' * e
    local s2 = e2[1,1] / (`n' - colsof(`X'))
    matrix `V' = `s2' * syminv(`XX')

    return matrix b = `b'
    return matrix V = `V'
    return scalar N = `n'
end
```

### Accessing Estimation Results

```stata
regress price mpg weight foreign
matrix b = e(b)
matrix V = e(V)

// Custom Wald test
matrix R = (0, 1, 0, 0)
matrix RVR = R * V * R'
matrix wald = (R * b' - 0)' * syminv(RVR) * (R * b' - 0)
```

---

## Program Properties and Byable Programs

### rclass, eclass, sclass

```stata
program define rclass_example, rclass        // General results
program define eclass_example, eclass        // Estimation results
program define sclass_example, sclass        // System info (rare)
```

### Byable Programs

```stata
program define simple_byable, byable(recall)
    version 17
    syntax varlist [if] [in]
    marksample touse
    summarize `varlist' if `touse'
end

sysuse auto, clear
by foreign: simple_byable price mpg
```

**`byable(recall)`** re-runs the program for each by-group. **`byable(onecall)`** runs once with access to `_by()`, `_byindex()`, `_bylastcall()`.

```stata
program define advanced_byable, byable(onecall) sortpreserve
    version 17
    syntax varlist [if] [in]
    marksample touse
    if _by() {
        local byvar "`_byvars'"
        // Process per group...
    }
    else {
        summarize `varlist' if `touse'
    }
end
```

---

## Class Programming

### Basic Class

```stata
* point.class
version 17
class point {
    double x
    double y

    program .new
        args x_val y_val
        .x = `x_val'
        .y = `y_val'
    end

    program .distance
        args other
        local dist = sqrt((.x - `other'.x)^2 + (.y - `other'.y)^2)
        return scalar distance = `dist'
    end
}

// Usage
.point_a = .point.new, 0 0
.point_b = .point.new, 3 4
.point_a.distance .point_b           // r(distance) = 5
```

### Inheritance

```stata
class mean_stat {
    inherit statistic
    double mean_value

    program .compute
        quietly summarize `.varname'
        .mean_value = r(mean)
    end
}
```

---

## Dialog Programming

### Basic Dialog (.dlg file)

```stata
VERSION 17.0
POSITION . . 400 250

DIALOG main, label("My Command") tabtitle("Main")
BEGIN
    TEXT     tx_vars    10  10  380  ., label("Variables:")
    VARLIST  vl_vars    10  +20 380  ., label("Select variables")
    CHECKBOX ck_detail  10  +30 380  ., label("Detailed output")
END

PROGRAM command
BEGIN
    put "mycommand "
    require main.vl_vars
    put main.vl_vars
    beginoptions
        if main.ck_detail { put " detail" }
    endoptions
END
```

### Dialog Controls

- `TEXT`, `EDIT`, `CHECKBOX`, `RADIO`, `COMBOBOX`, `LISTBOX`
- `VARNAME` (single), `VARLIST` (multiple), `FILE`, `SPINNER`, `BUTTON`

---

## Debugging

### assert and confirm

```stata
assert price > 0
assert !missing(price, mpg, weight)
isid make                               // Assert unique ID

capture confirm variable `varname'
if _rc { display "`varname' not found" }

capture confirm numeric variable `varname'
capture confirm file "`filename'"
capture confirm new variable newvar
```

### trace

```stata
set trace on
set tracedepth 2                        // Limit depth
myprogram price mpg weight
set trace off
```

### Debug Levels Pattern

```stata
program define myprogram, rclass
    syntax varlist [, Debug Level(integer 0)]
    marksample touse

    if "`debug'" != "" | `level' > 0 {
        display "Debug: Variables = `varlist'"
        quietly count if `touse'
        display "Debug: N = " r(N)
    }
    // ... computation ...
end
```

---

## Error Handling

### Common Error Codes

| Code | Meaning |
|------|---------|
| 7 | Type mismatch |
| 111 | Variable not found |
| 198 | Invalid syntax |
| 416 | Missing values |
| 601 | File not found |
| 602 | File already exists |
| 2000 | No observations |

### Custom Error Messages

```stata
if !inrange(`threshold', 0, 1) {
    display as error "threshold() must be between 0 and 1"
    exit 198
}
```

### try-catch Pattern

```stata
capture noisily {
    assert !missing(`varlist')
    summarize `varlist', detail
}
if _rc {
    if _rc == 9 {
        display as error "Missing values found"
    }
    else {
        display as error "Error code: " _rc
    }
}
```

---

## Version Control

```stata
program define myprogram
    version 17                          // Ensures consistent behavior

    if `c(stata_version)' >= 17 {
        table (), statistic(mean `varlist')
    }
    else {
        tabstat `varlist', statistics(mean sd)
    }
end
```

### Version History Convention

```stata
*! version 2.1.0  23Nov2024
*! version 2.0.0  15Oct2024 - Added matrix support
*! version 1.0.0  10Aug2024 - Initial release
```

---

## Professional Program Template

```stata
*! version 1.0.0
*! Description: Comprehensive descriptive statistics
program define profstats, rclass byable(recall) sortpreserve
    version 17

    #delimit ;
    syntax varlist(numeric) [if] [in] [fweight aweight]
        [, STats(string) Format(string) TItle(string)
        SAVing(string) REPlace EXport(string) NODisplay ];
    #delimit cr

    marksample touse
    quietly count if `touse'
    if r(N) == 0 error 2000

    // Validate stats option
    if "`stats'" == "" local stats "mean sd min max"
    // ... computation ...

    // Return results
    return scalar N = `n'
    return local stats "`stats'"
    return matrix results = `results'
    return local cmd "profstats"
end
```

### Help File (SMCL)

```stata
{smcl}
{title:Title}
{p2colset 5 19 21 2}{...}
{p2col :{cmd:profstats} {hline 2}}Professional descriptive statistics{p_end}

{title:Syntax}
{p 8 17 2}
{cmd:profstats} {varlist} {ifin} {weight} [{cmd:,} {it:options}]

{synoptset 20 tabbed}{...}
{synopt:{opt stat:s(statlist)}}statistics to compute{p_end}
{synopt:{opt format(format)}}display format{p_end}
{synopt:{opt saving(filename)}}save results{p_end}
```

### Package Distribution

```stata
// profstats.pkg
v 3
d profstats - Professional descriptive statistics
d Author: Your Name
f profstats.ado
f profstats.sthlp

// stata.toc
v 3
d Materials by Your Name
p profstats Professional descriptive statistics
```
