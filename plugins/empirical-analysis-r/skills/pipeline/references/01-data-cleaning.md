# Step 1 — Data Cleaning in R (Deep Reference)

Goal: from a raw source file to a clean `analysis.rds` (or `analysis.parquet` / `.feather` for big data) with dtypes correct, missing values handled per-variable, duplicates resolved, joins validated, and panel structure declared.

## Contents

1. Reading every common format
2. First-look inspection
3. Type coercion (`as.*`, `parse_*`, lubridate)
4. `janitor::clean_names` and friends
5. Missing values — `naniar`, `mice`, MCAR/MAR/MNAR
6. Outlier detection
7. Duplicates on panel keys
8. Joins with `relationship` argument + assertions
9. Panel structure with `panelr` / `plm::pdata.frame`
10. Validation with `validate` / `assertr`
11. Labels (haven labels, attributes)
12. Reusable `01_clean.R` skeleton

---

## 1. Reading every common format

```r
library(haven)        # Stata / SPSS / SAS
library(readr)        # CSV / TSV
library(readxl)       # Excel
library(data.table)   # fread for big CSVs
library(arrow)        # Parquet / Feather

# Stata
df <- read_dta("raw/panel.dta")            # also returns labels as attributes
# Inspect labels:
attr(df$gender, "labels")                  # value labels
attr(df$wage,   "label")                    # variable label

# SPSS / SAS
df <- read_sav("raw/panel.sav")
df <- read_sas("raw/panel.sas7bdat")

# CSV
df <- read_csv("raw/panel.csv", show_col_types = FALSE)
df <- read_csv("raw/panel.csv",
               col_types = cols(year = col_integer(),
                                wage = col_double(),
                                .default = col_guess()))

# Big CSV — fread is 10–50× faster
library(data.table)
df <- as_tibble(fread("raw/panel.csv"))

# Excel
df <- read_excel("raw/panel.xlsx", sheet = "Sheet1", skip = 0,
                 col_types = c("numeric", "text", "date"))

# Parquet (preferred for > 1 GB)
df <- read_parquet("raw/panel.parquet")

# JSON Lines
library(jsonlite)
df <- stream_in(file("raw/panel.jsonl"), verbose = FALSE) %>% as_tibble()

# Database
library(DBI); library(RPostgres)
con <- dbConnect(Postgres(), dbname = "research", host = "...", user = "...")
df  <- dbGetQuery(con, "SELECT * FROM panel WHERE year >= 2000") %>% as_tibble()
dbDisconnect(con)
```

After reading, **save a snapshot** before mutating:

```r
saveRDS(df, "data/raw_snapshot.rds")
```

---

## 2. First-look inspection

```r
library(skimr); library(naniar)

dim(df)
glimpse(df)                                  # tibble's `str`
head(df); tail(df)
sample_n(df, 10)                             # random rows often more informative

skim(df)                                      # rich one-line-per-var summary
summary(df)                                   # base R

# Missing-data overview
naniar::miss_var_summary(df)                 # % missing per variable
naniar::miss_case_summary(df)                # rows with most missing
naniar::vis_miss(df)                         # heatmap (pairs nicely with grid layout)
naniar::gg_miss_upset(df)                    # which variables co-miss
```

---

## 3. Type coercion

```r
df <- df %>%
  mutate(
    # Numeric
    year   = as.integer(year),
    wage   = as.numeric(wage),

    # Date/time (lubridate)
    date    = lubridate::ymd(date_str),
    quarter = lubridate::quarter(date),
    ym      = format(date, "%Y-%m"),

    # Factor (with explicit levels — ordering matters for output)
    edu_cat = factor(edu_cat,
                     levels = c("<HS", "HS", "Some College", "BA", "BA+"),
                     ordered = TRUE),
    industry = as.factor(industry)
  )

# Bulk via `across`
df <- df %>%
  mutate(across(c(year, age, edu, tenure), as.numeric)) %>%
  mutate(across(where(is.character) & !c(worker_id, firm_id), as.factor))

# parse_number — strip currency / units
df <- df %>%
  mutate(price = readr::parse_number(price_str))   # "$1,234.56" → 1234.56

# String → numeric IDs (preserve leading zeros)
df <- df %>%
  mutate(firm_id = sprintf("%05d", as.integer(firm_id)))
```

---

## 4. `janitor::clean_names` and friends

```r
library(janitor)

df <- df %>% clean_names()                    # snake_case all column names

# Tabulate quickly
df %>% tabyl(industry, training)              # one-line cross-tab
df %>% tabyl(industry) %>% adorn_pct_formatting()

# Find duplicate columns
df %>% get_dupes(worker_id, year)

# Remove constant or all-NA columns
df <- df %>% remove_constant() %>% remove_empty(c("rows","cols"))
```

---

## 5. Missing values

```r
# 5a. Per-variable rule
key_vars <- c("wage", "training", "worker_id", "year")
n0 <- nrow(df)
df <- df %>% drop_na(all_of(key_vars))
cat("dropped", n0 - nrow(df), "rows missing on key vars\n")

# 5b. Median impute + flag (numeric covariates with low missingness)
df <- df %>%
  mutate(across(c(tenure, assets, firm_size), .names = "{.col}_missing", ~ is.na(.))) %>%
  mutate(across(c(tenure, assets, firm_size),
                ~ if_else(is.na(.), median(., na.rm = TRUE), .)))

# 5c. Explicit "unknown" for categoricals
df <- df %>%
  mutate(union  = fct_explicit_na(as.factor(union),  na_level = "unknown"),
         region = fct_explicit_na(as.factor(region), na_level = "unknown"))

# 5d. High-missing columns — decide individually
df %>% miss_var_summary() %>% filter(pct_miss > 30)

# 5e. Multiple imputation (mice) — for MAR with non-trivial missingness
library(mice)
imp <- mice(df %>% select(wage, age, edu, tenure, female),
            m = 5, method = "pmm", seed = 42, printFlag = FALSE)
# Then run the analysis pooled across imputations:
fit <- with(imp, lm(wage ~ training + age + edu + tenure + female))
summary(pool(fit))                            # Rubin's rules

# 5f. Drop columns that are mostly missing
high_miss <- df %>%
  miss_var_summary() %>%
  filter(pct_miss > 50) %>%
  pull(variable)
df <- df %>% select(-all_of(high_miss))
```

---

## 6. Outlier detection

```r
# 6a. z-score
df <- df %>%
  mutate(wage_z = as.numeric(scale(wage)),
         outlier_z4 = abs(wage_z) > 4)

# 6b. IQR rule
iqr_bounds <- quantile(df$wage, c(0.25, 0.75), na.rm = TRUE)
iqr_w <- diff(iqr_bounds)
df <- df %>%
  mutate(outlier_iqr = wage < iqr_bounds[1] - 1.5*iqr_w |
                      wage > iqr_bounds[2] + 1.5*iqr_w)

# 6c. Within-group p99 cap
df <- df %>%
  group_by(industry, year) %>%
  mutate(outlier_iy = wage > quantile(wage, 0.99, na.rm = TRUE) |
                     wage < quantile(wage, 0.01, na.rm = TRUE)) %>%
  ungroup()

# 6d. Multivariate Mahalanobis
X  <- df %>% select(wage, age, tenure) %>% drop_na() %>% as.matrix()
d2 <- mahalanobis(X, colMeans(X), cov(X))
threshold <- qchisq(0.999, df = ncol(X))

# Reporting
sum(df$outlier_z4, na.rm = TRUE)
sum(df$outlier_iqr, na.rm = TRUE)
sum(df$outlier_iy, na.rm = TRUE)
sum(d2 > threshold)
```

**Decision tree**: data-entry error → drop; legitimate extreme → winsorize in Step 2; systematic (clustered in one firm/year) → investigate.

---

## 7. Duplicates on panel keys

```r
# Exact duplicates
df %>% janitor::get_dupes()                    # find duplicates
df <- df %>% distinct()

# Panel-key duplicates (more dangerous)
df %>% janitor::get_dupes(worker_id, year)

# Resolution strategies
# (a) Keep most recent
df <- df %>%
  arrange(worker_id, year, desc(timestamp)) %>%
  distinct(worker_id, year, .keep_all = TRUE)

# (b) Aggregate within key
df <- df %>%
  group_by(worker_id, year) %>%
  summarise(across(c(wage, age, edu), mean, na.rm = TRUE),
            training = max(training, na.rm = TRUE),
            .groups = "drop")

# (c) Genuine multi-record — redefine key
df <- df %>%
  group_by(worker_id, year) %>%
  mutate(spell_id = row_number()) %>%
  ungroup() %>%
  unite("panel_id", worker_id, spell_id, remove = FALSE)

stopifnot(!any(duplicated(df %>% select(panel_id, year))))
```

---

## 8. Joins with `relationship` + assertions

```r
firm_chars <- read_dta("raw/firm_chars.dta")

# Standard m:1 (lookup)
n0 <- nrow(df)
df <- df %>%
  left_join(firm_chars,
            by = "firm_id",
            relationship = "many-to-one")    # dplyr 1.1+ — fails if not m:1
stopifnot(nrow(df) == n0)

# Possible relationships:
#   "one-to-one"  | "one-to-many" | "many-to-one" | "many-to-many"
# Default since dplyr 1.1.0: warns on m:m. Always specify explicitly.

# Anti-joins for diagnostics
missing_in_firms <- df %>% anti_join(firm_chars, by = "firm_id")
nrow(missing_in_firms)                       # rows that won't match

# Fuzzy / nearest joins
library(fuzzyjoin)
df <- df %>%
  fuzzy_left_join(events,
                  by = c("date" = "date"),
                  match_fun = list(`>=`),
                  multiple = "first")        # rolling join

# Asof / range
library(data.table)
setDT(df); setDT(events)
df_asof <- events[df, on = .(date), roll = TRUE]
```

---

## 9. Panel structure declarations

```r
# Tidy approach: just keep tibble + key columns; check structure
df %>% count(year)
df %>% count(worker_id) %>% summary()

# panelr — for plm-style declarations + tools
library(panelr)
panel_df <- panel_data(df, id = worker_id, wave = year)

# plm::pdata.frame
library(plm)
pdf_obj <- pdata.frame(df, index = c("worker_id", "year"))
pdim(pdf_obj)                                # balance summary
make.pbalanced(pdf_obj, balance.type = "shared.individuals")
```

---

## 10. Validation with `validate` / `assertr`

Codify your assumptions; fail fast.

```r
library(validate)

rules <- validator(
  is.numeric(wage),
  wage >= 0,
  training %in% c(0, 1),
  year >= 1990 & year <= 2030,
  !is.na(worker_id),
  !is.na(year)
)
out <- confront(df, rules)
summary(out)                                 # which rules pass / fail
plot(out)

# Or assertr — chains into pipeline
library(assertr)
df <- df %>%
  verify(nrow(.) > 0) %>%
  verify(all(training %in% c(0, 1))) %>%
  assert(within_bounds(0, 1e7), wage) %>%
  assert(not_na, worker_id, year) %>%
  assert_rows(num_row_NAs, within_bounds(0, 5), everything())
```

---

## 11. Labels (haven labels, attributes)

```r
# haven preserves Stata/SPSS labels as attributes:
attr(df$gender, "label")     # "Sex of respondent"
attr(df$gender, "labels")    # named vector: c(Male = 1, Female = 2)

# Convert labelled to factor preserving labels
df <- df %>%
  mutate(gender = as_factor(gender, levels = "labels"))   # haven::as_factor

# Or strip labels entirely (sometimes needed for tidyverse compat)
library(labelled)
df <- df %>% remove_var_label() %>% remove_val_labels()

# Apply your own labels (for tables)
df <- df %>%
  set_variable_labels(
    log_wage  = "Log monthly wage (real, 2010 USD)",
    training  = "= 1 if received training",
    age       = "Age (years)"
  )
```

`gtsummary` and `modelsummary` will pick up `var_label` / haven labels automatically.

---

## 12. Reusable `01_clean.R` skeleton

```r
# R/01_clean.R
library(tidyverse)
library(haven)
library(janitor)
library(naniar)
library(assertr)
library(here)

# --- 1. Load ---
df <- read_dta(here("data", "raw", "panel_raw.dta"))

# --- 2. Names + dtypes ---
df <- df %>%
  clean_names() %>%
  mutate(
    year   = as.integer(year),
    wage   = as.numeric(wage),
    date   = as.Date(date_str),
    edu_cat = factor(edu_cat,
                     levels = c("<HS","HS","Some College","BA","BA+"),
                     ordered = TRUE)
  )

# --- 3. Missing on key vars ---
key_vars <- c("wage","training","worker_id","year")
n0 <- nrow(df); df <- df %>% drop_na(all_of(key_vars))
message("[clean] dropped ", n0 - nrow(df), " rows missing on keys")

# --- 4. Impute numeric covariates ---
df <- df %>%
  mutate(across(c(tenure, assets), .names = "{.col}_missing", ~ is.na(.))) %>%
  mutate(across(c(tenure, assets),
                ~ if_else(is.na(.), median(., na.rm = TRUE), .)))

# --- 5. Outlier flag ---
df <- df %>%
  mutate(wage_z = as.numeric(scale(wage)),
         outlier_z4 = abs(wage_z) > 4)

# --- 6. Dedupe panel key ---
df <- df %>% distinct(worker_id, year, .keep_all = TRUE)

# --- 7. Merges ---
firm_chars <- read_dta(here("data","raw","firm_chars.dta"))
n0 <- nrow(df)
df <- df %>% left_join(firm_chars, by = "firm_id",
                       relationship = "many-to-one")
stopifnot(nrow(df) == n0)

# --- 8. Validate ---
df <- df %>%
  verify(all(training %in% c(0,1))) %>%
  assert(within_bounds(0, 1e7), wage) %>%
  assert(not_na, worker_id, year)

# --- 9. Snapshot ---
saveRDS(df, here("data","analysis.rds"))
message("[clean] wrote ", nrow(df), " rows to data/analysis.rds")
```

Every decision logged via `message()`; every assumption asserted; downstream scripts can `readRDS("data/analysis.rds")` with full confidence.
