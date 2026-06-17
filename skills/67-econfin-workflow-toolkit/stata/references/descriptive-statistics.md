# Descriptive Statistics in Stata

## summarize

```stata
summarize [varlist] [if] [in] [weight] [, options]
```

- Default output: N, mean, SD, min, max
- `detail`: Adds percentiles (1-99), skewness, kurtosis, smallest/largest values
- `meanonly`: Suppress display; only store r(mean)
- `format`: Use variable's display format

```stata
summarize price mpg weight
summarize price, detail
summarize price if foreign == 1
summarize price [aweight=weight]
```

### Stored Results
```stata
r(N)  r(mean)  r(Var)  r(sd)  r(min)  r(max)  r(sum)  r(sum_w)
// With detail:
r(p1)-r(p99)  r(skewness)  r(kurtosis)
```

---

## tabstat

Flexible tables of summary statistics.

```stata
tabstat varlist [if] [in] [weight] [, statistics(...) by(varname) columns(...) format(...)]
```

### Available Statistics
```
mean  count/n  sum  max  min  range  sd  variance  cv  semean
skewness  kurtosis  p1 p5 p10 p25 p50 p75 p90 p95 p99  iqr  q
```

### Examples
```stata
tabstat price mpg weight, statistics(mean sd min max) columns(statistics)
tabstat price mpg, by(foreign) statistics(mean sd median)

tabstat price mpg weight length, ///
    statistics(n mean sd min p25 p50 p75 max) ///
    columns(statistics) format(%9.2f)

tabstat income education age, by(region) statistics(mean median sd) nototal

// Save results to matrices
tabstat price mpg, by(foreign) statistics(mean sd) save
matrix list r(Stat1)
```

---

## tabulate

### One-Way Tables
```stata
tabulate varname [, options]
```
Options: `missing`, `nolabel`, `sort`, `generate(newvar)`, `matcell(matname)`

```stata
tabulate foreign              // Frequency, percent, cumulative
tabulate occupation, sort     // Sorted by frequency
tabulate region, generate(reg)  // Creates dummy variables reg1, reg2, ...
```

### Two-Way Tables (Cross-tabulation)
```stata
tabulate rowvar colvar [, options]
```
Options: `chi2`, `exact`, `V`, `gamma`, `lrchi2`, `row`, `col`, `cell`, `nofreq`, `expected`, `all`

```stata
tabulate foreign rep78, row col          // Row and column percentages
tabulate foreign rep78, chi2             // Chi-squared test
tabulate foreign rep78, all              // All association measures
tabulate foreign rep78, expected         // Expected frequencies
```

---

## table

More flexible multi-dimensional tables.

```stata
table rowvar [colvar [supercolvar]] [, contents(clist) by(var) format(%fmt)]
```

### Contents Options
```
freq  mean var  sd var  sum var  count var  min var  max var
median var  p25 var  p50 var  p75 var  iqr var
```

```stata
table foreign rep78, contents(mean price)
table foreign, contents(freq mean price sd price)
table region, contents(n income mean income sd income median income) format(%9.2f)
table foreign, contents(p25 price p50 price p75 price)
table education income, contents(freq) row col
```

---

## correlate / pwcorr

### correlate
```stata
correlate price mpg weight length
correlate price mpg weight, covariance    // Covariance matrix
correlate price mpg weight, means         // Include means and SDs
```

### pwcorr (pairwise, with significance tests)
```stata
pwcorr price mpg weight length, sig             // With p-values
pwcorr price mpg weight length, star(0.05)      // Star significant
pwcorr price mpg weight length, obs             // Show N per pair
pwcorr price mpg weight length, print(0.5)      // Only |r| > 0.5
pwcorr price mpg weight, sig star(0.05) bonferroni  // Multiple testing adjustment
```

Key difference: `correlate` uses casewise deletion; `pwcorr` uses pairwise deletion by default.

---

## codebook

```stata
codebook [varlist] [, options]
```

Options: `compact`, `problems`, `mv`, `tabulate(#)`

```stata
codebook, compact      // Quick overview: type, unique values, missing count
codebook, problems     // Flag constants, all-missing vars, duplicates
codebook income, mv    // Missing value codes
```

---

## inspect

Compact summary with distribution info, integer vs non-integer counts, negative/zero/positive breakdown.

```stata
inspect price
inspect price if foreign == 1
```

---

## count

```stata
count                                      // All observations
count if foreign == 1
count if missing(price)
count if !missing(price)

// Use stored result
count if mpg > 30
if r(N) > 0 {
    summarize price if mpg > 30
}
```

---

## Calculating Specific Statistics

### Means
```stata
summarize price, meanonly
display r(mean)
scalar price_mean = r(mean)

// By groups
tabstat price, by(foreign) statistics(mean)

// Weighted
summarize price [aweight=weight]
```

### Median and Percentiles
```stata
summarize price, detail
display r(p50)               // Median
display r(p75) - r(p25)     // IQR

tabstat price, statistics(p10 p25 p50 p75 p90)

// Custom percentiles
_pctile price, percentiles(10 25 50 75 90 95 99)
display r(r1)                // 10th percentile

centile price, centile(10 25 50 75 90)

// Create percentile variables
egen pct25 = pctile(price), p(25)
```

### Other Statistics
```stata
summarize price
display r(sd)      // Standard deviation
display r(Var)     // Variance
display r(sum)     // Sum
display r(max) - r(min)  // Range

tabstat price, statistics(cv)            // Coefficient of variation
summarize price, detail
display r(skewness)                      // Skewness
display r(kurtosis)                      // Kurtosis
```

---

## Practical Summary Table Examples

```stata
// Comprehensive summary
tabstat price mpg weight length, ///
    statistics(n mean sd min max) columns(statistics) format(%9.2f)

// By groups
tabstat price mpg weight, by(foreign) statistics(n mean sd median) format(%9.2f)

// Cross-tabulation with statistics
table foreign rep78, contents(n price mean price sd price) format(%9.2f)

// Save to matrix for export
tabstat price mpg weight, statistics(mean sd min max) columns(statistics) save
matrix summary = r(StatTotal)
matrix list summary
```

## Weight Types

```stata
[fweight=var]   // Frequency weights (integers, duplicated observations)
[aweight=var]   // Analytic weights (inverse variance, survey data)
[pweight=var]   // Probability weights (sampling, auto-applies robust SEs)
[iweight=var]   // Importance weights (programming use)
```

## Choosing the Right Command

| Need | Command |
|------|---------|
| Quick basic stats | `summarize` |
| Flexible tables with custom stats | `tabstat` |
| Frequency distributions, cross-tabs | `tabulate` |
| Multi-dimensional tables | `table` |
| Data structure overview | `codebook, compact` |
| Data quality check | `inspect` or `codebook, problems` |
| Correlations with tests | `pwcorr` |
