# Data Manipulation Packages in Stata

## Overview

Essential user-written packages for data manipulation, especially with large datasets.

**Packages covered:**
- **gtools** - Fast replacements for collapse, egen, reshape, etc. (C plugin, 5-20x speedup)
- **rangestat** - Moving window / rolling statistics over arbitrary intervals
- **egenmore** - Extended egen functions (strings, outliers, etc.)
- **distinct** - Count distinct values
- **unique** - Identify unique value combinations, tag duplicates
- **missings** - Missing data analysis and management
- **carryforward** - Forward/backward fill of missing values

---

## Installation

```stata
ssc install gtools
ssc install ftools       // recommended dependency for gtools
ssc install rangestat
ssc install egenmore
ssc install distinct
ssc install unique
ssc install missings
ssc install carryforward

* Verify
gtools, check
adoupdate, update
```

---

## gtools: Fast Data Manipulation

Drop-in replacements for built-in commands using C plugins. Same syntax, 5-20x faster on large data.

| Built-in | gtools replacement | Typical speedup |
|----------|-------------------|-----------------|
| `collapse` | `gcollapse` | 8x |
| `egen` | `gegen` | 20x |
| `reshape` | `greshape` | 8x |
| `isid` | `gisid` | 7x |
| `levelsof` | `glevelsof` | 9x |
| `xtile`/`pctile` | `gquantiles` | -- |
| `sort` | `hashsort` | 3x |

### gcollapse: Fast Aggregation

```stata
* Identical syntax to collapse
gcollapse (mean) mean_price=price ///
          (median) med_price=price ///
          (sd) sd_price=price ///
          (p25) p25_price=price ///
          (p75) p75_price=price ///
          (count) n=price, by(foreign)

* Weighted
gcollapse (mean) price [aw=weight], by(foreign)
```

### gegen: Fast egen

```stata
* Group statistics
gegen mean_price = mean(price), by(foreign)
gegen sd_price = sd(price), by(foreign)
gegen n_obs = count(price), by(foreign rep78)

* Percentiles within groups
gegen p25_price = pctile(price), p(25) by(foreign)
gegen p50_price = pctile(price), p(50) by(foreign)

* Standardize, rank, IQR, MAD
gegen z_price = std(price), by(foreign)
gegen rank_price = rank(price), by(foreign)
gegen iqr_price = iqr(price), by(foreign)
gegen mad_price = mad(price), by(foreign)

* Tag and group
gegen tag = tag(foreign rep78)       // Tag first obs in group
gegen group_id = group(foreign rep78) // Numeric group ID
gegen group_n = count(1), by(foreign rep78)
```

### greshape: Fast Reshape

```stata
* Wide to long (same syntax as reshape)
greshape long score, i(id) j(test)

* Long to wide
greshape wide income expenses, i(id) j(year)
```

### Other gtools Commands

```stata
* Fast ID check
gisid make              // errors if not unique
gisid id, missok        // allow missing

* Unique levels
glevelsof foreign, local(levels)

* Quantile groups
gquantiles price_quartile = price, nquantiles(4)
gquantiles price_decile = price, nquantiles(10)
gquantiles price_cut = price, cutpoints(5000 10000 15000)

* Top levels by frequency
gtoplevelsof rep78, ntop(5)
```

### Real-World Example: Panel Data Prep

```stata
webuse nlswork, clear

gegen mean_wage = mean(ln_wage), by(idcode)
gegen sd_wage = sd(ln_wage), by(idcode)
gegen first_obs = tag(idcode)
gegen n_obs = count(1), by(idcode)

* Within-group standardization
gegen mean_exp = mean(ttl_exp), by(idcode)
gegen sd_exp = sd(ttl_exp), by(idcode)
generate exp_std = (ttl_exp - mean_exp) / sd_exp

keep if n_obs >= 5

gcollapse (mean) avg_wage=ln_wage ///
          (sd) sd_wage=ln_wage ///
          (first) first_year=year ///
          (last) last_year=year ///
          (count) n_years=year, by(idcode)
```

### When to Use gtools

- **Use gtools**: datasets >100K obs, repeated aggregations, panel data group operations
- **Stick with built-in**: datasets <10K obs, one-time ops, need egen functions not in gegen

---

## rangestat: Moving Window Statistics

Computes statistics on observations within a specified range -- ideal for rolling calculations, event windows, and irregular time intervals.

### Syntax

```stata
rangestat (statistic) newvar=varname, interval(varname min max) [by(varlist)]
```

### Moving Averages and Rolling Statistics

```stata
tsset date

* 7-day and 30-day backward-looking moving averages
rangestat (mean) ma7=value, interval(date -6 0)
rangestat (mean) ma30=value, interval(date -29 0)

* Multiple rolling stats
rangestat (mean) roll_mean=value ///
          (sd) roll_sd=value ///
          (min) roll_min=value ///
          (max) roll_max=value ///
          (count) roll_n=value, ///
          interval(date -9 0)

* Rolling correlation and regression
rangestat (corr) roll_corr=value value2, interval(date -19 0)
rangestat (reg) roll_beta=value value2, interval(date -29 0)

* Forward-looking, centered, or exact lag/lead
rangestat (mean) forward_ma5=value, interval(date 0 5)
rangestat (mean) centered_ma7=value, interval(date -3 3)
rangestat (mean) lag10=value, interval(date -10 -10)
```

### Event Study Windows

```stata
* Pre- and post-event averages by group
rangestat (mean) pre_avg=outcome, interval(date -5 -1) by(firm_id)
rangestat (mean) post_avg=outcome, interval(date 0 5) by(firm_id)
```

### Panel Data Applications

```stata
webuse nlswork, clear
xtset idcode year

rangestat (mean) wage_trend=ln_wage, interval(year -2 2) by(idcode)
rangestat (mean) lag3_wage=ln_wage, interval(year -3 -1) by(idcode)
```

### Performance Tips

```stata
* rangestat can be slow with wide windows on large data
* For simple MA on regular time series, tssmooth or lag operators are faster:
tssmooth ma value_ma5 = value, window(5)
generate ma5_manual = (value + L1.value + L2.value + L3.value + L4.value)/5
```

---

## egenmore: Extended egen Functions

Adds specialized `egen` functions. **Note:** many have been incorporated into modern Stata -- check built-in egen first.

### Key Functions

```stata
ssc install egenmore

* String functions
egen first_word = nss(make), find(1)
egen n_words = nwords(make)
egen combined = concat(var1 var2), punct(" ")
egen clean_text = sieve(text), omit(":$,.")

* Outlier detection (1.5*IQR rule)
egen price_outlier = outside(price)
egen price_out_grp = outside(price), by(foreign)

* Rounding
egen price_rounded = roundi(price), nearest(100)
```

---

## distinct: Count Distinct Values

More flexible than `codebook` for counting unique values.

```stata
ssc install distinct

distinct rep78                    // One variable
distinct foreign rep78, joint     // Joint combinations
distinct mpg, by(foreign)         // By groups

* Stored results
distinct foreign
local n = r(ndistinct)

* Find low-variation variables
foreach var of varlist _all {
    quietly distinct `var'
    if r(ndistinct) < 5 {
        display "`var' has only " r(ndistinct) " distinct values"
    }
}
```

---

## unique: Unique Value Combinations

Like `distinct` but can tag observations and identify duplicates.

```stata
ssc install unique

* Check uniqueness
unique make
* If r(unique) == r(N), variable is a unique ID

* Tag first occurrence
unique foreign rep78, gen(tag)
list foreign rep78 if tag == 1

* Find duplicates in panel
unique idcode year, gen(unique_obs)
list idcode year if unique_obs == 0   // These are duplicates

* Programmatic duplicate check
unique idcode year
if r(unique) != r(N) {
    display "WARNING: Duplicate observations found!"
}
```

**distinct vs unique:** Use `distinct` for quick counts. Use `unique` when you need to tag/identify specific observations.

---

## missings: Missing Data Utilities

```stata
ssc install missings
```

### Commands

```stata
* Report missing counts
missings report
missings report price mpg rep78
missings report price mpg, by(foreign)

* Cross-tabulation of missing patterns
missings table price mpg rep78

* Tag observations with missing
missings tag price mpg rep78, generate(any_miss)
missings tag price mpg rep78, generate(n_miss) count

* List observations with missing
missings list price mpg rep78

* Drop observations with any missing in specified vars
missings dropobs price mpg rep78
* Drop only if ALL specified vars are missing
missings dropobs price mpg rep78, all

* Drop variables with >50% missing
missings dropvars, min(50)
```

### Real-World Example

```stata
webuse nlswork, clear
missings report ln_wage ttl_exp tenure union, by(year)
missings tag ln_wage ttl_exp tenure, generate(n_miss) count

* Compare complete vs incomplete cases
summarize ln_wage if n_miss == 0
summarize ln_wage if n_miss > 0
```

---

## carryforward: Fill Missing Values

Fills missing values by carrying forward (or backward) the last non-missing value within groups.

```stata
ssc install carryforward
```

### Usage

```stata
* Forward fill within groups
bysort id (year): carryforward value, gen(value_filled)

* Replace in place (destructive -- prefer gen())
carryforward value, replace

* Backward fill: reverse sort, carry forward, re-sort
gsort id -year
by id: carryforward value, gen(value_back)
sort id year

* Forward then backward for max coverage
bysort id (year): carryforward value, gen(value_fwd)
gsort id -year
by id: carryforward value_fwd, replace
sort id year
```

### Panel Data Example

```stata
* Fill time-invariant variables with occasional gaps
bysort id (year): carryforward city, gen(city_filled)
bysort id (year): carryforward race, gen(race_filled)
```

**Caution:** Only appropriate for time-invariant or slowly-changing variables. Don't use for truly missing data (introduces bias). Always use `gen()` over `replace` to preserve originals.

---

## Choosing the Right Tool

| Task | Small data | Large data |
|------|-----------|------------|
| Aggregation/collapse | `collapse` | `gcollapse` |
| Group statistics | `egen` | `gegen` |
| Reshape | `reshape` | `greshape` |
| Rolling/moving stats | `tssmooth` / lag ops | `rangestat` |
| Irregular-interval windows | `rangestat` | `rangestat` |
| Missing data analysis | `summarize`/`codebook` | `missings` |
| Forward fill | `carryforward` | `carryforward` |
| Uniqueness check | `isid` / `distinct` | `gisid` / `distinct` |
| Duplicate detection | `unique` | `unique` |

---

## Related Packages

```stata
ssc install ftools        // Fast fixed effects (works with gtools)
ssc install reghdfe       // Fast fixed effects regression
ssc install fastxtile     // Fast quantile groups
```
