# Data Management in Stata

## Generate and Replace

### `generate` - Create New Variables
Errors if variable already exists.
```stata
generate len_ft = length / 12
generate log_price = log(price)
generate high_price = 1 if price > 10000
generate luxury = 1 if price > 15000 & foreign == 1
```

### `replace` - Modify Existing Variables
Errors if variable doesn't exist.
```stata
replace price = price * 1.1
replace mpg = . if mpg < 0
replace category = "high" if price > 15000
replace category = "medium" if price >= 5000 & price <= 15000
replace category = "low" if price < 5000
```

---

## Recode and Egen

### `recode`
```stata
recode mpg (min/18=1) (19/23=2) (24/max=3)
recode age (0/17=1 "Child") (18/64=2 "Adult") (65/max=3 "Senior"), gen(age_group)
recode education (1 2 3 = 1 "Low") (4 5 = 2 "Medium") (6 7 8 = 3 "High"), gen(educ_level)
recode income (. = 0 "No income") (nonmissing = 1 "Has income"), gen(has_income)
recode var1 var2 var3 (1=0) (2=1)   // Multiple variables at once
```

### `egen` - Extended Generate

#### Row-wise Operations
```stata
egen avg_score = rowmean(test1 test2 test3)
egen total_score = rowtotal(test1 test2 test3)
egen total_score = rowtotal(test1 test2 test3), missing  // Propagate missing
egen max_score = rowmax(test1 test2 test3)
egen min_score = rowmin(test1 test2 test3)
egen num_missing = rowmiss(test1 test2 test3)
egen num_nonmiss = rownonmiss(test1 test2 test3)
```

#### Group-wise Operations
```stata
bysort country: egen avg_income = mean(income)
bysort region: egen total_sales = total(sales)
bysort firm: egen num_employees = count(employee_id)
bysort category: egen min_price = min(price)
bysort industry: egen sd_wage = sd(wage)
```

#### Creating Group IDs
```stata
egen region_id = group(region)
egen state_year_id = group(state year)
egen city_id = group(city), missing    // Missing as separate group
```

#### Other Useful Functions
```stata
egen income_rank = rank(income)
egen p25 = pctile(income), p(25)
bysort id (year): egen first_wage = first(wage)
bysort id (year): egen last_wage = last(wage)
egen tag = tag(country)                // Tag first observation in group
egen income_std = std(income)          // Z-score standardization
```

---

## Sort and By/Bysort

```stata
sort price
sort state county city
gsort -price                           // Descending
gsort country -year                    // Mixed

// by requires data to be sorted first
sort country
by country: summarize income

// bysort combines sort + by
bysort country: summarize gdp
bysort country (year): gen observation_num = _n
bysort firm_id (date): gen cumulative_sales = sum(sales)
bysort household_id: gen first = (_n == 1)
bysort household_id: gen last = (_n == _N)
bysort company (year): gen revenue_growth = revenue - revenue[_n-1]
bysort region: gen region_count = _N
```

**Special Variables in by-groups:**
- `_n`: Current observation number within group
- `_N`: Total observations within group
- `_n-1`, `_n+1`: Previous/next observation

```stata
// Forward fill missing values
bysort id (date): replace value = value[_n-1] if missing(value)

// Identify gaps in sequence
bysort patient_id (visit_date): gen days_since_last = visit_date - visit_date[_n-1]
```

---

## Merge and Append

### `merge` - Add Variables (Columns)

**Merge Types:**
- `1:1` - Identifier unique in both datasets
- `m:1` - Identifier unique in using dataset only
- `1:m` - Identifier unique in master dataset only
- `m:m` - Not recommended

**The `_merge` Variable:**
- `_merge == 1`: Only in master
- `_merge == 2`: Only in using
- `_merge == 3`: Successfully merged

```stata
// One-to-one
merge 1:1 person_id using income_data
tab _merge
drop if _merge != 3
drop _merge

// Many-to-one
merge m:1 school_id using school_characteristics

// Keep only matched
merge 1:1 id using dataset2, keep(3) nogenerate

// Assert merge results
merge 1:1 id using dataset2, assert(match master) nogenerate

// Keep specific variables from using
merge 1:1 person_id using dataset2, keep(3) keepusing(income age)

// Update master data
merge 1:1 id using updates, update replace
```

**Gotcha: Always `tab _merge` before `assert` or `drop`:**
```stata
merge m:1 state using state_data
tab _merge              // inspect: how many matched vs unmatched?
assert _merge == 3      // now assert — if it fails, tab output shows why
drop _merge
```
Skipping `tab _merge` and jumping straight to `assert _merge == 3` gives no diagnostic output when the assert fails. The `tab` costs nothing and makes debugging merge mismatches trivial.

**Always check uniqueness before merging:**
```stata
isid id              // Verify id uniquely identifies observations
duplicates report id
```

### `append` - Add Observations (Rows)

```stata
use survey_2020, clear
append using survey_2021 survey_2022

// Track source
use dataset1, clear
gen source = 1
append using dataset2
replace source = 2 if missing(source)

// Force when variables differ
append using dataset2, force
```

---

## Reshape (Wide/Long)

### Wide vs Long Format
```
Wide: id  income2020  income2021  income2022
Long: id  year  income
```

### `reshape long`
```stata
reshape long faminc, i(famid) j(year)
reshape long ht wt, i(famid birth) j(age)          // Multiple variables
reshape long income, i(famid) j(parent) string       // Character suffixes
```

### `reshape wide`
```stata
reshape wide income, i(person_id) j(year)
reshape wide revenue profit employees, i(firm_id) j(year)
```

### Troubleshooting
```stata
duplicates report id year     // Check before reshaping
fillin id year                // Handle missing combinations
reshape error                 // Shows current configuration
```

---

## Collapse

**Warning:** Replaces your dataset. Use `preserve` first.

### Available Statistics
`mean` (default), `sum`, `count`, `median`, `min`, `max`, `sd`, `p1`-`p99`

```stata
// Simple mean by group
collapse (mean) avg_income=income, by(state)

// Multiple statistics
collapse (mean) avg_wage=wage (median) med_wage=wage ///
         (sd) sd_wage=wage (count) n=wage, by(industry)

// Different statistics for different variables
collapse (sum) total_pop=population (mean) avg_income=income ///
         (median) med_age=age, by(county year)

// Weighted collapse
collapse (mean) avg_test_score=test_score [aweight=enrollment], by(district)

// Aggregating daily to monthly
gen month = mofd(date)
format month %tm
collapse (mean) avg_price=price (firstnm) open_price=price ///
         (lastnm) close_price=price, by(stock_id month)
```

### Collapse and Merge Back (preserve/tempfile Pattern)

This is the standard pattern for computing group statistics via `collapse` and attaching them back to the original data. The `egen` approach (below) is simpler for basic stats, but collapse supports statistics `egen` cannot (e.g., `sd`, percentiles, weighted stats, multiple stats at once).

```stata
sysuse auto, clear
tempfile groupstats
preserve

collapse (mean) mean_price=price mean_mpg=mpg, by(foreign)
save `groupstats'

restore

merge m:1 foreign using `groupstats'
tab _merge              // always inspect before asserting
assert _merge == 3      // all obs must match (groups came from same data)
drop _merge

gen price_demeaned = price - mean_price
```

**Key points:**
- `preserve` before `collapse` (collapse destroys the dataset)
- `save` the collapsed data to a `tempfile` (auto-deleted when Stata exits)
- `restore` brings back the original data, then `merge m:1` attaches group stats
- Always `tab _merge` before `assert _merge == 3` — if the assert fails, `tab` output in the log tells you why

**When `egen` is simpler:** For basic group means, `egen` avoids the entire preserve/collapse/merge round-trip:
```stata
bysort foreign: egen mean_price = mean(price)
bysort foreign: egen mean_mpg = mean(mpg)
gen price_demeaned = price - mean_price
```
Use collapse-merge-back when you need statistics `egen` doesn't support, or when computing many stats at once.

### Preserving Labels
```stata
local income_label : variable label income
collapse (mean) income, by(region)
label variable income "`income_label'"
```

---

## Drop and Keep

```stata
// Drop/keep variables
drop temp_var var1 var2 test* *_temp
keep id name age income*

// Drop/keep observations
drop if age < 18
drop if missing(income)
drop in 1/10
keep if age >= 18 & age <= 65
keep in 1/100

// Duplicates
duplicates drop
duplicates drop id year, force
bysort id year (revenue): keep if _n == _N   // Keep highest revenue

// Temporary subset without modifying data
preserve
keep if year == 2020
restore
```

---

## Rename and Label

### `rename`
```stata
rename rep78 repair_record
rename (v1 v2 v3) (score1 score2 score3)
rename *, lower                        // All to lowercase
rename * old_*                         // Add prefix
rename (*_final) (*_revised)           // Replace pattern
```

### Variable Labels
```stata
label variable income "Annual household income"
label variable income ""               // Remove label
```

### Value Labels
```stata
label define yesno 0 "No" 1 "Yes"
label values married yesno
label values employed retired yesno    // Same label for multiple vars

// Modify existing
label define gender 3 "Non-binary", modify
label define gender 4 "Prefer not to say", add

label list                             // Show all label definitions
label list yesno                       // Show specific
label save using labels.do             // Export labels to do-file
```

---

## Encode and Decode

### `encode` - String to Labeled Numeric
```stata
encode gender_str, gen(gender)         // Alphabetical codes by default
tab gender, nolabel                    // Show numeric codes

// Control coding order
label define race_lbl 1 "White" 2 "Black" 3 "Asian" 4 "Other"
encode race_str, gen(race) label(race_lbl)

// Batch encode
foreach var of varlist city state country {
    encode `var', gen(`var'_num)
}
```

**Gotcha:** `encode` assigns numeric codes alphabetically. If you need specific codes, pre-define the value label.

### `decode` - Labeled Numeric to String
```stata
decode gender, gen(gender_str)
```

### Clean Before Encoding
```stata
replace country = proper(country)
replace country = trim(country)
replace country = "USA" if inlist(country, "United States", "U.S.A.", "US")
encode country, gen(country_code)
```

---

## Common Data Manipulation Patterns

### Lagged Variables
```stata
bysort firm_id (year): gen revenue_lag = revenue[_n-1]
bysort firm_id (year): gen growth = (revenue - revenue[_n-1]) / revenue[_n-1] * 100
```

### Standardized Variables
```stata
egen income_std = std(income)
bysort country: egen income_z = std(income)   // Within groups
```

### Combining Survey Waves with Tempfiles
```stata
use wave1, clear
gen wave = 1
tempfile w1
save `w1'

use wave2, clear
gen wave = 2
append using `w1'
sort id wave
```

### Identifying and Handling Duplicates
```stata
duplicates report id year
duplicates tag id year, gen(dup_tag)
list if dup_tag > 0
bysort id year: keep if _n == 1              // Keep first
bysort id year (revenue): keep if _n == _N   // Keep highest
```

### Dummy Variables
```stata
tab region, gen(region_)       // Creates region_1, region_2, ...
gen high_income = (income > 50000)
gen female = (gender == 2)
```
