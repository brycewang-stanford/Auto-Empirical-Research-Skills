# Stata Basics: Getting Started Guide

## Basic Command Syntax

### Command Structure
```stata
[by varlist:] command [varlist] [=exp] [if exp] [in range] [weight] [, options]
```

### Key Syntax Rules

1. **Commands are case-sensitive for variable names** but not for command names
   ```stata
   summarize age    // Works
   SUMMARIZE age    // Also works
   summarize Age    // Different variable!
   ```

2. **Abbreviations** - Most commands can be abbreviated
   ```stata
   summarize age    // Full command
   sum age          // Abbreviated version
   ```

3. **Variable lists** can use wildcards and ranges
   ```stata
   describe age-income     // Variables from age to income
   describe age*           // All variables starting with "age"
   ```

4. **Comments**
   ```stata
   * This is a comment line
   summarize age  // Inline comment
   /* Multi-line comment */
   ```

5. **Line continuation** using `///`
   ```stata
   regress income age education ///
           experience gender
   ```

### if and in Qualifiers

```stata
summarize income if age > 30
list in 1/10              // First 10 observations
summarize income in 20/50 // Observations 20 through 50
```

---

## Data Types and Structures

### Numeric Storage Types
```stata
byte      // -127 to 100 (1 byte)
int       // -32,767 to 32,740 (2 bytes)
long      // -2,147,483,647 to 2,147,483,620 (4 bytes)
float     // ±10^38 (4 bytes, 6-7 digit precision)
double    // ±10^307 (8 bytes, 15-16 digit precision)
```

### String Variables
```stata
str1-str244  // Fixed-length strings (older format)
strL         // Variable-length strings (up to 2 billion characters)
```

### Variable Labels and Value Labels
```stata
label variable age "Age in years"
label define yesno 0 "No" 1 "Yes"
label values married yesno
```

### Dataset Structure
- **One dataset in memory** at a time (by default)
- **Rectangular format**: All observations have values (or missing) for all variables

---

## Essential Commands

### Data Input/Output
```stata
use "mydata.dta", clear
use age income using "mydata", clear  // Load specific variables
save "mydata.dta", replace
import excel "data.xlsx", firstrow clear
import delimited "data.csv", clear
export excel using "output.xlsx", firstrow(variables) replace
export delimited using "output.csv", replace
```

### Data Exploration
```stata
describe                      // All variables
describe, short               // Brief summary
summarize                     // All numeric variables
summarize age, detail         // Detailed stats (percentiles, etc.)
list in 1/10                  // First 10 observations
browse age income             // Data browser (read-only)
codebook, compact             // Compact variable info
tabulate gender               // One-way frequency table
tab gender married, row col   // Two-way cross-tabulation
```

### Data Modification
```stata
generate age_squared = age^2
generate high_income = (income > 50000)
replace income = income * 1.03
replace age = . if age < 0          // Set invalid ages to missing
rename oldname newname
rename (old1 old2) (new1 new2)      // Multiple renames
drop age                            // Drop a variable
drop if income < 0                  // Drop observations
keep age income education           // Keep only these variables
keep if age >= 18
recode age (0/17=1 "Child") (18/64=2 "Adult") (65/max=3 "Senior"), gen(age_group)
sort age
gsort -age                          // Descending order
```

### Data Management
```stata
clear all
append using "newdata.dta"
merge 1:1 id using "otherdata.dta"
merge m:1 country using "countrydata.dta"
reshape long inc, i(id) j(year)
compress                     // Optimize storage types
```

### Analysis Commands
```stata
correlate age income education
pwcorr age income education, star(0.05)
regress income age education experience
ttest income, by(gender)
```

### System and File Management
```stata
cd "/path/to/project"
pwd
dir *.dta
log using "analysis.log", replace
log close
```

---

## Working Directory Management

```stata
pwd                          // Print working directory
cd "/path/to/project"        // Change directory
cd ..                        // Go up one directory
dir *.dta                    // List Stata datasets
```

**Best Practice**: Use global macros for project paths:
```stata
global projdir "/path/to/project"
cd "$projdir"
use "$projdir/data/mydata.dta"
```

Recommended project structure:
```
MyProject/
├── data/          (raw data)
├── dofiles/       (analysis scripts)
├── results/       (output datasets)
├── logs/          (log files)
└── graphs/        (figures)
```

---

## Getting Help

```stata
help summarize               // Help for specific command
search "panel data"          // Search for topics
findit "robust regression"   // Search including user-written programs
ssc install commandname      // Install user-written commands
adoupdate, update            // Update all packages
```

---

## Common Pitfalls

### Not Using `clear` Before Loading Data
```stata
use "newdata.dta", clear    // Include clear to avoid errors
```

### Confusing = and ==
```stata
generate male = 1 if gender == 1     // Correct (= assigns, == compares)
```

### Ignoring Missing Values
```stata
* Missing values are treated as very large positive numbers
summarize age if !missing(age)  // Exclude missing
```

### Preserving Original Data
```stata
preserve
... do operations ...
restore                     // Returns to original state
```

### Missing Value Codes
| Code | Meaning |
|------|---------|
| `.` | Generic missing |
| `.a` to `.z` | Extended missing (27 types) |
| `""` | String missing |

### Operators Reference
| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` or `~=` | Not equal |
| `>`, `<`, `>=`, `<=` | Comparisons |
| `&` | And |
| `|` | Or |
| `!` | Not |
| `+`, `-`, `*`, `/`, `^` | Arithmetic |
