---
name: data-cleaning
description: Clean and transform messy data for analysis in Python, R, or Stata
---

# Data Cleaning

## Purpose

This skill helps economists clean, transform, and prepare datasets for analysis in Python, R, or Stata. It emphasizes reproducibility, proper documentation, and handling common data quality issues found in economic research.

## When to Use

- Cleaning raw survey or administrative data
- Merging multiple data sources
- Handling missing values, duplicates, and outliers
- Creating analysis-ready panel datasets
- Documenting data transformations for replication

## Instructions

### Step 1: Understand the Data

Before generating code, ask the user:
1. What is the data source? (survey, administrative, API, etc.)
2. What is the unit of observation?
3. What are the key variables needed for analysis?
4. Are there known data quality issues to address?

### Step 2: Generate Cleaning Pipeline

Create a Stata do-file that:

1. **Has a clear header** with project info and date
2. **Sets up the environment** (clear all, set memory, log)
3. **Loads and inspects raw data**
4. **Documents each transformation** with comments
5. **Creates a codebook** for the final dataset

### Step 3: Follow Best Practices

- Use `assert` statements to verify data integrity
- Create labeled variables with `label variable`
- Use value labels for categorical variables
- Generate a log file for reproducibility
- Save intermediate files when appropriate

## Example Output

```stata
/*==============================================================================
    Project:    Economic Analysis Data Cleaning
    Author:     [Your Name]
    Date:       [Date]
    Purpose:    Clean raw survey data for regression analysis
    Input:      raw_survey_data.dta
    Output:     cleaned_analysis_data.dta
==============================================================================*/

* ============================================
* 1. SETUP
* ============================================

clear all
set more off
cap log close
log using "logs/data_cleaning_`c(current_date)'.log", replace

* Set working directory
cd "/path/to/project"

* Define globals for paths
global raw_data "data/raw"
global clean_data "data/clean"
global output "output"

* ============================================
* 2. LOAD AND INSPECT RAW DATA
* ============================================

use "${raw_data}/raw_survey_data.dta", clear

* Basic inspection
describe
summarize
codebook, compact

* Check for duplicates
duplicates report id_var
duplicates list id_var if _dup > 0

* ============================================
* 3. VARIABLE CLEANING
* ============================================

* --- Rename variables for clarity ---
rename q1 age
rename q2 income_reported
rename q3 education_level

* --- Clean numeric variables ---
* Replace missing value codes with .
mvdecode age income_reported, mv(-99 -88 -77)

* Cap outliers at 99th percentile
qui sum income_reported, detail
replace income_reported = r(p99) if income_reported > r(p99) & !mi(income_reported)

* --- Clean string variables ---
* Standardize state names
replace state = upper(trim(state))
replace state = "NEW YORK" if inlist(state, "NY", "N.Y.", "N Y")

* --- Create categorical variables ---
gen education_cat = .
replace education_cat = 1 if education_level < 12
replace education_cat = 2 if education_level == 12
replace education_cat = 3 if education_level > 12 & education_level <= 16
replace education_cat = 4 if education_level > 16 & !mi(education_level)

label define edu_lbl 1 "Less than HS" 2 "High School" 3 "College" 4 "Graduate"
label values education_cat edu_lbl

* ============================================
* 4. HANDLE MISSING DATA
* ============================================

* Create missing indicator variables
gen mi_income = mi(income_reported)

* Document missingness
tab mi_income

* Count complete cases
egen complete_case = rownonmiss(age income_reported education_cat)
tab complete_case

* ============================================
* 5. CREATE DERIVED VARIABLES
* ============================================

* Age groups
gen age_group = .
replace age_group = 1 if age >= 18 & age < 30
replace age_group = 2 if age >= 30 & age < 50
replace age_group = 3 if age >= 50 & age < 65
replace age_group = 4 if age >= 65 & !mi(age)

label define age_lbl 1 "18-29" 2 "30-49" 3 "50-64" 4 "65+"
label values age_group age_lbl

* Log income
gen log_income = ln(income_reported + 1)

* ============================================
* 6. DATA VALIDATION
* ============================================

* Assert expected ranges
assert age >= 18 & age <= 120 if !mi(age)
assert income_reported >= 0 if !mi(income_reported)

* Check variable types
assert !mi(id_var)
isid id_var  // Verify unique identifier

* ============================================
* 7. LABEL VARIABLES
* ============================================

label variable age "Age in years"
label variable income_reported "Annual income (USD)"
label variable education_cat "Education category"
label variable log_income "Log of annual income"
label variable mi_income "Missing income indicator"

* ============================================
* 8. FINAL CHECKS AND SAVE
* ============================================

* Keep relevant variables
keep id_var age age_group income_reported log_income ///
     education_cat mi_income state year

* Order variables logically
order id_var year state age age_group income_reported ///
      log_income education_cat mi_income

* Compress to minimize file size
compress

* Save cleaned data
save "${clean_data}/cleaned_analysis_data.dta", replace

* Create codebook
codebook, compact

* Close log
log close

* ============================================
* END OF FILE
* ============================================
```

## Requirements

### Software
- Stata 15+ (some commands require newer versions)

### Recommended User-Written Commands
```stata
ssc install unique     // For unique value checking
ssc install mdesc      // For missing data patterns
ssc install labutil    // For label manipulation
```

## Best Practices

1. **Always start with `clear all`** to ensure clean environment
2. **Use log files** to document all transformations
3. **Comment extensively** - explain WHY, not just WHAT
4. **Use `assert` statements** to catch data errors early
5. **Create a data dictionary** alongside your cleaned data
6. **Version your do-files** and datasets

## Common Pitfalls

- ❌ Not checking for duplicates before merging
- ❌ Forgetting to handle missing value codes (-99, -88, etc.)
- ❌ Not labeling variables and values
- ❌ Overwriting raw data files
- ❌ Not documenting data transformations

## Python Data Cleaning Example

```python
"""
Data Cleaning Pipeline (Python / pandas)
=========================================
Input:  data/raw/raw_data.csv
Output: data/clean/clean_data.parquet
"""

import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------
# 1. Load and inspect
# --------------------------------------------------
df = pd.read_csv("data/raw/raw_data.csv")
print(df.dtypes)
print(df.describe())
print(df.isnull().sum())  # missingness report

# Check for duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")
df = df.drop_duplicates()

# --------------------------------------------------
# 2. Rename and standardize column names
# --------------------------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# --------------------------------------------------
# 3. Handle missing value codes
# --------------------------------------------------
MISSING_CODES = [-99, -88, -77, 9999]
df.replace(MISSING_CODES, np.nan, inplace=True)

# --------------------------------------------------
# 4. Fix dtypes
# --------------------------------------------------
df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
df["income"] = pd.to_numeric(df["income"], errors="coerce")

# --------------------------------------------------
# 5. Cap outliers at 1st/99th percentile
# --------------------------------------------------
for col in ["income", "wage"]:
    if col in df.columns:
        lo, hi = df[col].quantile([0.01, 0.99])
        df[col] = df[col].clip(lo, hi)

# --------------------------------------------------
# 6. Create derived variables
# --------------------------------------------------
df["log_income"] = np.log1p(df["income"])
df["mi_income"] = df["income"].isna().astype(int)

# --------------------------------------------------
# 7. Validate
# --------------------------------------------------
assert df["id"].notna().all(), "Missing IDs"
assert df["id"].is_unique, "Duplicate IDs"
assert (df["income"].dropna() >= 0).all(), "Negative income"

# --------------------------------------------------
# 8. Save
# --------------------------------------------------
Path("data/clean").mkdir(parents=True, exist_ok=True)
df.to_parquet("data/clean/clean_data.parquet", index=False)
print(f"Saved {len(df):,} rows × {df.shape[1]} columns")
```

## R Data Cleaning Example

```r
# Data Cleaning Pipeline (R / tidyverse)
# Input:  data/raw/raw_data.csv
# Output: data/clean/clean_data.rds

library(tidyverse)
library(janitor)

# --------------------------------------------------
# 1. Load and inspect
# --------------------------------------------------
df <- read_csv("data/raw/raw_data.csv")
glimpse(df)
summary(df)
colSums(is.na(df))  # missingness

# Check duplicates
cat("Duplicate rows:", sum(duplicated(df)), "\n")
df <- distinct(df)

# --------------------------------------------------
# 2. Standardize column names (snake_case)
# --------------------------------------------------
df <- clean_names(df)  # janitor::clean_names

# --------------------------------------------------
# 3. Replace missing value codes
# --------------------------------------------------
MISSING_CODES <- c(-99, -88, -77, 9999)
df <- df %>%
  mutate(across(where(is.numeric), ~ ifelse(. %in% MISSING_CODES, NA, .)))

# --------------------------------------------------
# 4. Cap outliers at 1st/99th percentile
# --------------------------------------------------
winsorize <- function(x, probs = c(0.01, 0.99)) {
  qs <- quantile(x, probs, na.rm = TRUE)
  pmin(pmax(x, qs[1]), qs[2])
}
df <- df %>%
  mutate(across(c(income, wage), winsorize))

# --------------------------------------------------
# 5. Create derived variables
# --------------------------------------------------
df <- df %>%
  mutate(
    log_income = log1p(income),
    mi_income  = as.integer(is.na(income))
  )

# --------------------------------------------------
# 6. Validate
# --------------------------------------------------
stopifnot("Missing IDs"     = !any(is.na(df$id)),
          "Duplicate IDs"   = !any(duplicated(df$id)),
          "Negative income" = all(df$income >= 0, na.rm = TRUE))

# --------------------------------------------------
# 7. Save
# --------------------------------------------------
dir.create("data/clean", recursive = TRUE, showWarnings = FALSE)
saveRDS(df, "data/clean/clean_data.rds")
cat(sprintf("Saved %d rows × %d columns\n", nrow(df), ncol(df)))
```

## Related Skills & Commands

- **data-fetcher**: Fetch raw data from economic databases before cleaning
- **stats**: Generate summary statistics after cleaning
- **/analyze**: Start analysis workflow with your clean dataset
- **table**: Format summary tables for publication
- **ols-regression**: Proceed to estimation after data preparation
