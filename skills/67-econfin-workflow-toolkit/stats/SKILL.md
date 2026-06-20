---
name: stats
description: |
  Econometrics skill for descriptive statistics and summary tables. Activates when the user asks about:
  "descriptive statistics", "summary statistics", "summary table", "Table 1",
  "balance table", "means and standard deviations", "correlation matrix",
  "data summary", "sample characteristics", "variable distributions",
  "描述性统计", "描述统计", "汇总统计", "统计表", "均值标准差",
  "平衡性检验", "相关矩阵", "样本特征", "变量分布"
---

# Descriptive Statistics & Summary Tables Skill

This skill generates publication-quality summary statistics tables, balance tables, and correlation matrices — the essential "Table 1" found in every empirical economics paper.

## When to Use

- **Before any regression**: Summarize your sample to understand distributions and detect issues
- **For "Data" section of papers**: Standard Table 1 with means, SDs, and sample sizes
- **Treatment/control comparison**: Balance tables with t-tests or normalized differences
- **Variable relationships**: Correlation matrices for initial exploration

## Summary Statistics Table (Table 1)

### Python

```python
# Python — publication-quality summary stats
import pandas as pd

# Basic summary stats
desc = df[['income', 'age', 'education', 'hours_worked']].describe().T
desc = desc[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
desc.columns = ['N', 'Mean', 'SD', 'Min', 'P25', 'Median', 'P75', 'Max']
print(desc.round(3).to_string())

# Using tableone for clinical/econ style Table 1
# pip install tableone
from tableone import TableOne
table1 = TableOne(df, columns=['income', 'age', 'education', 'hours_worked'],
                  categorical=['female', 'race'],
                  groupby='treatment', pval=True)
print(table1.tabulate(tablefmt="github"))
table1.to_excel("table1.xlsx")
```

### R

```r
# R — modelsummary::datasummary
library(modelsummary)

# Full descriptive table
datasummary(income + age + education + hours_worked ~
            N + Mean + SD + Min + Median + Max,
            data = df,
            output = "table1.tex")   # or .docx, .html

# By group (treatment/control)
datasummary(income + age + education ~
            treatment * (N + Mean + SD),
            data = df,
            output = "balance.tex")

# Alternative: stargazer
library(stargazer)
stargazer(df[, c("income", "age", "education", "hours_worked")],
          type = "latex",
          summary.stat = c("n", "mean", "sd", "min", "median", "max"),
          title = "Summary Statistics",
          out = "table1.tex")
```

### Stata

```stata
* Stata — estpost/esttab for summary stats
estpost summarize income age education hours_worked, detail
esttab using "table1.tex", cells("count mean(fmt(3)) sd(fmt(3)) min max") ///
    nomtitle nonumber label replace title("Summary Statistics")

* By group
estpost ttest income age education hours_worked, by(treatment)
esttab using "balance.tex", cells("mu_1(fmt(3)) mu_2(fmt(3)) b(fmt(3) star)") ///
    star(* 0.10 ** 0.05 *** 0.01) replace ///
    collabels("Control" "Treatment" "Diff") ///
    title("Balance Table")

* Alternative: asdoc (simpler)
asdoc summarize income age education hours_worked, stat(N mean sd min max) ///
    save(table1.doc) replace
```

## Balance Tables (Treatment vs Control)

### Normalized Differences

Preferred over t-tests for balance assessment (Imbens & Rubin 2015): Δ = (X̄₁ − X̄₀) / √(S₁² + S₀²). Rule: |Δ| < 0.25 is acceptable.

```python
# Python — normalized differences
import numpy as np

def normalized_diff(treated, control):
    return (treated.mean() - control.mean()) / \
           np.sqrt(treated.var() + control.var())

for col in ['income', 'age', 'education']:
    nd = normalized_diff(df.loc[df.treatment==1, col],
                         df.loc[df.treatment==0, col])
    print(f"{col}: Norm. Diff. = {nd:.3f} {'✓' if abs(nd) < 0.25 else '✗'}")
```

```r
# R — cobalt for comprehensive balance
library(cobalt)
bal.tab(treatment ~ income + age + education + female,
        data = df, thresholds = c(m = 0.25),
        stats = c("mean.diffs", "variance.ratios"))
love.plot(treatment ~ income + age + education + female,
          data = df, binary = "std", threshold = 0.25)
```

```stata
* Stata — balance table with normalized differences
* After matching or for raw comparison:
iebaltab income age education female, grpvar(treatment) ///
    save("balance.xlsx") replace rowvarlabel ///
    pttest starsnoadd normdiff
```

## Correlation Matrix

```python
# Python — correlation matrix with significance
import scipy.stats as stats

vars = ['income', 'age', 'education', 'hours_worked']
corr = df[vars].corr()

# With p-values
def corr_with_pval(df, vars):
    n = len(vars)
    corr_mat = pd.DataFrame(index=vars, columns=vars)
    pval_mat = pd.DataFrame(index=vars, columns=vars)
    for i in range(n):
        for j in range(n):
            r, p = stats.pearsonr(df[vars[i]].dropna(), df[vars[j]].dropna())
            corr_mat.iloc[i,j] = f"{r:.3f}{'***' if p<.01 else '**' if p<.05 else '*' if p<.1 else ''}"
    return corr_mat

print(corr_with_pval(df, vars))
```

```r
# R — correlation matrix
library(modelsummary)
datasummary_correlation(df[, c("income", "age", "education", "hours_worked")],
                        output = "correlation.tex")

# With significance stars
library(Hmisc)
rcorr(as.matrix(df[, c("income", "age", "education")]))
```

```stata
* Stata — correlation matrix with significance
pwcorr income age education hours_worked, star(0.05) sig
* Export to LaTeX:
estpost correlate income age education hours_worked, matrix
esttab using "corr.tex", unstack not noobs replace
```

## Missing Data Summary

```python
# Python — missing data report
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_report = pd.DataFrame({'N_Missing': missing, 'Pct_Missing': missing_pct})
missing_report = missing_report[missing_report.N_Missing > 0].sort_values('Pct_Missing', ascending=False)
print(missing_report)
```

```r
# R — missing data summary
library(naniar)
miss_var_summary(df)
vis_miss(df)    # missingness heatmap
```

```stata
* Stata — missing data
misstable summarize
misstable patterns
```

## Reporting Standards

### For the "Data" Section of Papers

1. **Table 1**: N, Mean, SD (and optionally Min, Max, Median) for all variables used in analysis
2. **Panel structure**: If panel data, report N units, T periods, and total N×T
3. **Balance table**: If treatment/control design, show balance with t-tests or normalized differences
4. **Sample construction**: Note any sample restrictions (e.g., "dropped observations with missing income")
5. **Winsorization**: If applied, note percentiles (e.g., "winsorized at 1st and 99th percentiles")

### Formatting Conventions

| Convention | Details |
|------------|---------|
| Decimal places | 2–3 for continuous variables; 3 for proportions |
| Standard errors | In parentheses below means (if reporting SE of mean) |
| Stars on differences | * p<0.10, ** p<0.05, *** p<0.01 |
| Sample size | Report N per column and per variable if different |
| Notes | State data source, sample period, variable definitions |

## Common Pitfalls

- **Reporting means for skewed variables**: Use median or log-transform for income, firm size, etc.
- **Ignoring missingness**: Always report % missing for each variable
- **Balance test p-hacking**: Use normalized differences instead of t-tests; many variables will be "significant" by chance with large N
- **Wrong clustering for SE**: Summary stats use individual-level data but main analysis may cluster at group level

## Related Skills & Commands

- **/analyze**: Full analysis workflow that starts with descriptive statistics
- **ols-regression**: Proceed to regression after describing your data
- **matching**: Balance tables are critical for matching-based designs
- **table**: Advanced formatting for publication-quality tables
- **/plot**: Visualize distributions and correlations
