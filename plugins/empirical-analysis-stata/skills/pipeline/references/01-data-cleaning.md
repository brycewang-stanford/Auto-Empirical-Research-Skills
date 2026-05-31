# Step 1 — Data Cleaning in Stata (Deep Reference)

Goal: take a raw source (`.dta`, `.xlsx`, `.csv`, `.sas7bdat`, `.sav`) and arrive at an **analysis-ready `analysis.dta`** with dtypes correct, missing handled explicitly, duplicates resolved, merges validated, and the panel structure declared.

## Contents

1. Reading every common format
2. First-look inspection
3. `destring` / `tostring` / date conversion
4. Missing values — `misstable`, `mdesc`, `missings`
5. Outlier detection
6. `duplicates` on panel keys
7. `merge` with `assert` — catching silent m:m blowups
8. Declaring the panel (`xtset` / `tsset`)
9. Panel balance & gap detection
10. Variable / value labels (internationalization & docs)
11. String cleanup
12. A reusable `01_clean.do` skeleton

---

## 1. Reading every common format

```stata
* Native .dta
use "raw/panel.dta", clear

* CSV / tab-separated
import delimited "raw/panel.csv", clear varnames(1) case(preserve)
import delimited "raw/panel.tsv", clear delimiter("\t")

* Excel
import excel "raw/panel.xlsx", sheet("Sheet1") firstrow clear
* Specific cells:
import excel "raw/panel.xlsx", sheet("Sheet1") cellrange(A2:Z10000) firstrow clear

* SAS / SPSS
import sas "raw/panel.sas7bdat", clear
import spss "raw/panel.sav", clear

* Stat/Transfer-free: user-written -usespss- and -readstat- work too:
* ssc install readstat
* readstat "raw/panel.sav", clear

* Compressed / archived
use "raw/panel.dta.gz", clear     // Stata 17+ supports .gz transparently

* Remote URL
use "https://stats.idre.ucla.edu/stat/stata/examples/chp4/crime", clear
```

After importing, **always** save the raw version before mutating:

```stata
save "data/raw_snapshot.dta", replace
```

---

## 2. First-look inspection

```stata
describe, short                                   // N obs, N vars, memory
describe, fullnames                               // variable names + types + labels
codebook, compact                                 // one-line summary per var
summarize                                         // numeric summary
summarize, detail                                 // + percentiles, skew, kurtosis
inspect wage                                      // quick distribution sketch
tabulate industry, missing                        // value counts incl. missing
unique worker_id                                  // number of unique IDs
unique worker_id year, by(year)                   // panel coverage by time
```

For a fast first-pass report:

```stata
mdesc                                             // % missing per variable
misstable summarize                               // counts of missing by var
misstable patterns, freq                          // joint missing patterns
misstable tree                                    // hierarchical patterns
```

---

## 3. `destring` / `tostring` / date conversion

The most common silent bug: strings that look numeric but aren't.

```stata
* 3a. destring — strings → numeric
destring year wage, replace                       // error if any non-numeric
destring wage, replace force                      // force: set non-numeric to .
destring wage, replace ignore("$,%")              // strip characters first
destring *, replace                               // bulk; careful

* 3b. tostring — numeric → string (e.g. IDs that need leading zeros)
tostring firm_id, replace format(%05.0f)

* 3c. Dates
gen hire_date = date(hire_date_str, "YMD")        // "2020-03-15" → Stata date
format hire_date %td
gen year_hired = year(hire_date)
gen qtr_hired  = quarter(hire_date)

* Datetime (with time of day)
gen login_ts = clock(login_str, "YMDhms")
format login_ts %tc

* 3d. Encode / decode — string categoricals ↔ numeric with labels
encode industry, gen(industry_n)                  // preserves labels
decode  industry_n, gen(industry_str)

* 3e. Recode numeric categorical
recode edu_years (0/11 = 1 "< HS") (12 = 2 "HS") ///
                 (13/15 = 3 "Some College") (16 = 4 "BA") (17/max = 5 "BA+"), ///
    gen(edu_cat)
label var edu_cat "Education category"
```

---

## 4. Missing values

### Mechanism vs. treatment

| Mechanism | Definition | Treatment |
|-----------|-----------|-----------|
| MCAR | missingness independent of everything | listwise drop or any imputation |
| MAR  | missingness depends on observed covariates | multiple imputation (`mi`) |
| MNAR | missingness depends on the unobserved value | Heckman / sensitivity analysis |

```stata
* 4a. Per-variable rule
local key_vars wage training worker_id year
foreach v of local key_vars {
    local before = _N
    drop if missing(`v')
    display "dropped " `before' - _N " missing on `v'"
}

* 4b. Median impute + flag
foreach v of varlist tenure assets firm_size {
    gen byte `v'_miss = missing(`v')
    quietly summarize `v', detail
    replace `v' = r(p50) if missing(`v')
}

* 4c. Explicit "unknown" for categoricals
replace union  = "unknown" if missing(union)
replace region = "unknown" if missing(region)
encode union,  gen(union_n)
encode region, gen(region_n)

* 4d. Multiple imputation (MICE) — for MAR with non-trivial missingness
mi set wide                                         // or mlong
mi register imputed tenure assets firm_size
mi register regular wage training worker_id year

mi impute chained ///
    (regress) tenure assets firm_size ///
    = i.industry age edu, ///
    add(20) rseed(42) force
* then:
mi estimate: reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster worker_id)

* 4e. Drop columns that are mostly missing
missings report                                     // from -missings- package
missings dropvars, force                            // drop any all-missing column
foreach v of varlist _all {
    quietly count if missing(`v')
    if r(N) / _N > 0.5 display "`v': " 100*r(N)/_N "% missing"
}
```

---

## 5. Outlier detection

```stata
* 5a. z-score
egen wage_z = std(wage)
count if abs(wage_z) > 4
generate byte outlier_z4 = abs(wage_z) > 4 if !missing(wage_z)

* 5b. IQR rule
quietly summarize wage, detail
local lo = r(p25) - 1.5*(r(p75) - r(p25))
local hi = r(p75) + 1.5*(r(p75) - r(p25))
generate byte outlier_iqr = (wage < `lo' | wage > `hi') if !missing(wage)

* 5c. Within-group outliers (e.g. within industry-year)
bysort industry year: egen wage_p99 = pctile(wage), p(99)
bysort industry year: egen wage_p01 = pctile(wage), p(1)
generate byte outlier_iy = (wage > wage_p99 | wage < wage_p01)

* 5d. Multivariate — Mahalanobis distance (uses -mahapick- or via Mata)
* See the `-maharapick-` package (ssc) or `mata: mahadist(...)`.

* Decision:
* - data-entry error (wage = 99_999_999)  → drop
* - legitimate extreme (CEO in wage data)  → winsorize in Step 2
* - systematic (all from one firm)         → investigate
```

---

## 6. `duplicates` on panel keys

```stata
* 6a. Exact duplicates
duplicates report
duplicates drop, force                               // identical rows

* 6b. Panel key duplicates (more dangerous)
duplicates report worker_id year
duplicates list   worker_id year, sepby(worker_id)   // inspect

* Fix patterns
duplicates tag worker_id year, gen(dup)
* Keep the most recent record:
bysort worker_id year (timestamp): keep if _n == _N
drop dup

* Or aggregate within key:
collapse (mean) wage age edu (max) training, by(worker_id year)

* Or redefine the panel key (genuine multi-record)
gen spell_id = worker_id * 100 + spell_nr
xtset spell_id year

assert !mi(worker_id) & !mi(year)
isid worker_id year                                  // hard assert
```

---

## 7. `merge` with `assert`

The biggest silent class of Stata bugs is `merge m:m` without knowing it. Always specify `assert()`.

```stata
* 7a. Standard many-to-one (lookup)
merge m:1 firm_id using "firm_chars.dta", ///
    assert(master match using) keep(master match) ///
    nogenerate

* 7b. After merge, inspect _merge BEFORE dropping it
tab _merge                                           // 1=only master, 2=only using, 3=both
* Decide: keep only matched (3), or both master rows (1+3)?
drop if _merge == 2
drop _merge

* 7c. When using data has duplicates (and shouldn't)
preserve
    use "firm_chars.dta", clear
    duplicates report firm_id
    assert r(unique_value) == r(N)                   // one row per firm_id
restore

* 7d. Update values on merge (append / overlay)
merge 1:1 worker_id year using "wage_updates.dta", ///
    update replace nogenerate

* 7e. Fuzzy / nearest merge — use -rangejoin- or -joinby-
rangejoin date -30 30 using "events.dta"             // ±30 days

* 7f. Asof-style: last observation up to t (panel analog of pd.merge_asof)
* See -mmerge- or hand-roll via joinby + keep closest timestamp.
```

**Golden rule**: the row count before and after a lookup merge must match (or differ by a number you predicted). Always:

```stata
count                                                 // before
local n0 = r(N)
merge m:1 ... , assert(master match) nogen
count
assert r(N) == `n0'                                  // verify
```

---

## 8. Declaring the panel

```stata
xtset worker_id year                                  // annual
xtset worker_id year, yearly                          // explicit frequency
xtset worker_id ym,   monthly                         // monthly where ym = ym(year, month)
xtset worker_id dq,   quarterly

* For pure time series (single unit):
tsset year
tsset date, daily
```

After `xtset`, the `L.`, `F.`, `D.`, `S.` operators all work and `xt*` commands become available.

---

## 9. Panel balance & gap detection

```stata
xtdescribe                                            // how balanced is the panel?
xtsum    training log_wage                            // overall / between / within SD

* Units per year
bysort year: egen n_units = count(worker_id)
tab year, sum(n_units)

* Years per unit
by worker_id: egen n_years = count(year)
sum n_years, detail

* Entry / exit patterns
bys worker_id (year): gen first_year = year[1]
bys worker_id (year): gen last_year  = year[_N]
tab first_year

* Gap detection (units with missing years in middle of panel)
by worker_id (year): gen gap = year - year[_n-1] > 1 if _n > 1
bysort worker_id: egen any_gap = max(gap)
tab any_gap

* Balanced-panel subset (drop units with any missing year)
preserve
    contract worker_id year
    drop _freq
    save "data/full_years.dta", replace
restore
* Identify fully-observed units
unique year
local full_T = r(sum)
bys worker_id: egen n_obs = count(year)
keep if n_obs == `full_T'
```

---

## 10. Labels

```stata
* Variable labels (show up in tables, legends)
label variable log_wage "Log monthly wage (real, 2010 USD)"
label variable training "=1 if received training"
label variable age      "Age (years)"

* Value labels
label define female_lbl 0 "Male" 1 "Female"
label values female female_lbl

label define edu_lbl 1 "< HS" 2 "HS" 3 "Some College" 4 "BA" 5 "BA+"
label values edu_cat edu_lbl

* Notes on the dataset (for reproducibility)
note: Cleaned from raw.dta on `c(current_date)' by `c(username)'
note: See code/01_clean.do for details.
notes
```

---

## 11. String cleanup

```stata
replace industry = strtrim(industry)
replace industry = strlower(industry)
replace industry = ustrregexra(industry, "\s+", " ")            // collapse whitespace
replace industry = ustrregexra(industry, "[^a-z0-9 ]", "")       // strip punctuation

* Fuzzy dedupe (user-written)
ssc install matchit,   replace
matchit industry using "canonical.dta", similmethod(bigram)

* Convert UPPERCASE ↔ Title Case
replace firm_name = strproper(firm_name)
```

---

## 12. Reusable `01_clean.do` skeleton

```stata
* code/01_clean.do
version 17
clear all
set more off

* ---- 1. Load ----
use "data/raw/panel_raw.dta", clear

* ---- 2. Dtypes ----
destring year wage, replace force
gen hire_date = date(hire_date_str, "YMD"); format hire_date %td
encode industry, gen(industry_n)

* ---- 3. Missing ----
local key "wage training worker_id year"
foreach v of local key {
    drop if missing(`v')
}
foreach v of varlist tenure assets {
    gen byte `v'_miss = missing(`v')
    quietly sum `v', detail
    replace `v' = r(p50) if missing(`v')
}

* ---- 4. Outlier flags ----
egen wage_z = std(wage)
gen byte outlier_z4 = abs(wage_z) > 4 if !missing(wage_z)

* ---- 5. Dedupe & panel ----
duplicates drop
duplicates tag worker_id year, gen(dup)
assert dup == 0
drop dup

* ---- 6. Merges ----
merge m:1 firm_id using "data/raw/firm_chars.dta", ///
    assert(master match) keep(master match) nogen

* ---- 7. Panel structure ----
xtset worker_id year
xtdescribe

* ---- 8. Labels ----
label variable wage      "Monthly wage (USD)"
label variable training  "=1 if received training"

* ---- 9. Snapshot ----
compress
save "data/analysis.dta", replace
```

Every decision — drop, impute, clip, merge — printed to the log. No silent surprises downstream.
