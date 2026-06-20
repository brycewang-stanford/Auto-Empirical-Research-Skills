# EDA Checklist

> Run every section. Report every finding. Organize output by section.

---

## 1. Sample Overview

### 1.1 Sample size
- Total N after cleaning
- N per condition/group (if experimental)
- Compare to expected N from pre-registration or power analysis

### 1.2 Demographics
- For each demographic variable: frequencies or M/SD
- Compare sample composition to target population (if known)

### 1.3 Data completeness
- Overall completeness rate of the analysis dataset
- Per-variable completeness for key variables
- Flag if any key variable has >5% missing in the cleaned data

---

## 2. Table 1 — Descriptive Statistics

### 2.1 Continuous variables
- Mean, SD, median, min, max
- Skewness and kurtosis
- Reported by group if applicable

### 2.2 Categorical variables
- n and percentage per level
- Reported by group if applicable

### 2.3 Formatting
- APA-compliant table format (see `_shared/apa-formatting.md`)
- Condition/group comparisons side by side
- Overall column included
- Export as HTML and .docx

---

## 3. Correlation Matrix

### 3.1 Variables included
- All key continuous variables (IVs, DVs, mediators, moderators)
- Control variables if they will enter models
- Composite scores, not individual items

### 3.2 Matrix format
- Lower triangle with correlations
- Diagonal with reliability (alpha or omega) for multi-item scales
- Means and SDs in margin rows
- Significance stars (*p < .05, **p < .01, ***p < .001)
- N noted if pairwise deletion used

### 3.3 Flags
- |r| > .80 between distinct constructs → multicollinearity risk
- r ≈ 0 between theoretically related constructs → measurement concern
- Correlation direction opposite to hypothesis → note for analyst

---

## 4. Distributions

### 4.1 Visual inspection
- Histogram with density overlay for each key variable
- Q-Q plot for primary outcome variables
- Note: ceiling effects, floor effects, bimodality, gaps, outlier clusters

### 4.2 Formal tests
- Skewness statistic with benchmark: |skew| > 2 → concern
- Kurtosis statistic with benchmark: |kurtosis| > 7 → concern
- Shapiro-Wilk (N < 5000) or Anderson-Darling (N ≥ 5000) p-value
- Caveat: with large N, formal tests are almost always significant — visual inspection is primary

### 4.3 Implications
- Strongly non-normal DVs → consider robust methods or transformations
- Likert-scale ceiling/floor effects → note limited variance
- Outliers → report count and distance, do not remove without analyst decision

---

## 5. Assumption Pre-Checks

### 5.1 Normality
- Per variable: visual (histogram, Q-Q) + formal test
- Residual normality checked after preliminary model fitting if feasible

### 5.2 Homoscedasticity
- Levene's test for between-group designs
- Breusch-Pagan or visual residual plot for regression designs
- Report results, note if heteroscedasticity-robust SEs may be needed

### 5.3 Multicollinearity
- VIF for all planned predictors in a single model
- VIF > 5 → flag concern
- VIF > 10 → flag serious concern
- If interaction terms planned, check VIF with centered predictors

### 5.4 Linearity
- Scatterplots of key IV-DV pairs with loess/lowess smoother
- If nonlinear pattern visible, note it — may need polynomial terms or transformation

### 5.5 Independence
- If repeated measures or nested data: note clustering structure
- If time-series component: check autocorrelation

---

## 6. Bivariate Relationships

### 6.1 Continuous × continuous
- Scatterplots with loess smoother for key theoretical pairs
- Note: nonlinearity, heteroscedasticity, influential points

### 6.2 Categorical × continuous
- Box plots or violin plots
- Group means with error bars (95% CI)
- Note: unequal variances, outliers within groups

### 6.3 Categorical × categorical
- Cross-tabulations with counts and percentages
- Note: sparse cells, zero cells

---

## 7. EDA Report

### 7.1 Contents
- All sections above compiled into a single Quarto HTML document
- Each section as a headed chapter
- Figures inline with captions
- Tables properly formatted

### 7.2 Output paths
- Report: `reports/eda-report.html`
- Table 1: `output/tables/table1-descriptives.html` + `.docx`
- Correlation matrix: `output/tables/correlations.html`
- Correlation figure: `output/figures/correlations.png`
- Distribution figures: `output/figures/distributions/`
- Summary data: `output/results/eda-summary.rds` (R) or `.parquet` (Python)
