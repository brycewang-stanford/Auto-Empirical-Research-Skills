# Step 2 — Variable Construction & Transformation in R (Deep Reference)

Goal: from a clean tibble to an analysis-ready one — log/IHS, winsorized outcomes, standardized covariates, factors with explicit levels, panel operators (lag/lead/diff/within), CPI deflation, staggered-DID timing variables.

## Contents

1. Naming convention
2. Log / IHS / Box–Cox / Yeo–Johnson
3. Winsorize & trim (`DescTools::Winsorize`, group-wise)
4. Standardize (`scale()`, `bestNormalize`)
5. Factor encoding (forcats)
6. Interactions & polynomials (formula syntax)
7. Panel / time-series operators (`dplyr::lag`/`lead`, `slider` for rolling)
8. Index construction (`psych::principal`, `factoextra`)
9. Deflation (CPI, PPP)
10. Binning (`cut`, `ntile`, `dplyr::quantile`)
11. Per-capita / share / rate
12. Staggered-DID timing

---

## 1. Naming convention

| Suffix | Meaning |
|--------|---------|
| `_log` | natural log |
| `_ihs` | inverse hyperbolic sine |
| `_w1`  | winsorized at 1/99 |
| `_std` | z-scored |
| `_l1` / `_l2` | lag 1 / lag 2 |
| `_f1`  | lead 1 |
| `_d`   | first difference |
| `_dm`  | within-group demeaned |
| `_pc`  | per-capita |
| `_real`| CPI-deflated |

A reader of `glimpse(df)` should be able to infer the transformation from the suffix.

---

## 2. Log / IHS / Box–Cox / Yeo–Johnson

```r
library(dplyr)

df <- df %>%
  mutate(
    # Log — positive only; floor at 1
    log_wage = log(pmax(wage, 1)),

    # log(1+x) — safe when x ≥ 0
    grants_log1p = log1p(grants),

    # Inverse hyperbolic sine — handles 0 / negative
    assets_ihs = asinh(assets),
    # Equivalent: log(assets + sqrt(assets^2 + 1))

    # Box–Cox (estimate λ; positive variable required)
    # Use MASS::boxcox or bestNormalize
  )

# Box–Cox via MASS
library(MASS)
bc <- MASS::boxcox(wage ~ 1, data = df, plotit = FALSE)
lam <- bc$x[which.max(bc$y)]
df <- df %>%
  mutate(wage_bc = if (lam == 0) log(wage) else (wage^lam - 1) / lam)

# Yeo–Johnson (handles 0 / negative)
library(bestNormalize)
yj <- bestNormalize::yeojohnson(df$wage)
df$wage_yj <- yj$x.t                            # transformed values
```

Interpretation guide: `log` for magnitudes (wages, assets, sales), `ihs` for variables with legitimate zero / negative, `log1p` for non-negative count-like.

---

## 3. Winsorize & trim

```r
library(DescTools)

# Winsorize 1/99 (whole sample)
df <- df %>%
  mutate(wage_w1 = DescTools::Winsorize(wage,
                                         probs = c(0.01, 0.99),
                                         na.rm = TRUE))

# Within-group winsorize (most common in accounting / finance)
df <- df %>%
  group_by(industry, year) %>%
  mutate(wage_w1_iy = DescTools::Winsorize(wage,
                                            probs = c(0.01, 0.99),
                                            na.rm = TRUE)) %>%
  ungroup()

# Custom function (more flexible — winsorize only top tail)
winsor_top <- function(x, p = 0.99) {
  q <- quantile(x, p, na.rm = TRUE)
  if_else(x > q, q, x)
}
df <- df %>% mutate(wage_w99 = winsor_top(wage, 0.99))

# Trim (drop rows; rarely preferable to winsorize)
df_trim <- df %>%
  filter(wage >= quantile(wage, 0.01, na.rm = TRUE),
         wage <= quantile(wage, 0.99, na.rm = TRUE))
```

---

## 4. Standardize

```r
# z-score (mean 0, SD 1)
df <- df %>%
  mutate(age_std = as.numeric(scale(age)))

# Bulk standardize via `across`
df <- df %>%
  mutate(across(c(age, edu, tenure),
                ~ as.numeric(scale(.x)),
                .names = "{.col}_std"))

# Within-group z-score
df <- df %>%
  group_by(industry, year) %>%
  mutate(roa_iy_std = as.numeric(scale(roa))) %>%
  ungroup()

# Min-max to [0,1]
df <- df %>%
  mutate(age_mm = (age - min(age, na.rm = TRUE)) /
                  (max(age, na.rm = TRUE) - min(age, na.rm = TRUE)))

# Robust scaling (median / IQR)
df <- df %>%
  mutate(age_rob = (age - median(age, na.rm = TRUE)) /
                   IQR(age, na.rm = TRUE))

# Multiple variables at once with sklearn-like `recipes`
library(recipes)
rec <- recipe(~ age + edu + tenure, data = df) %>%
  step_normalize(all_numeric())
df_std <- bake(prep(rec), df)
```

---

## 5. Factor encoding (forcats)

```r
library(forcats)

# Explicit levels (ordering matters for output)
df <- df %>%
  mutate(edu_cat = factor(edu_cat,
                          levels = c("<HS","HS","Some College","BA","BA+"),
                          ordered = TRUE))

# Reorder by frequency
df <- df %>% mutate(industry = fct_infreq(industry))

# Reorder by another variable
df <- df %>% mutate(industry = fct_reorder(industry, log_wage, .fun = mean))

# Lump rare levels into "Other"
df <- df %>% mutate(industry = fct_lump_n(industry, n = 10, other_level = "Other"))

# Explicit NA level
df <- df %>% mutate(union = fct_explicit_na(as.factor(union),
                                             na_level = "unknown"))

# Recode
df <- df %>% mutate(industry = fct_recode(industry,
                                            "Manufacturing" = "manuf",
                                            "Services"      = "service"))

# Most regression functions handle factors automatically — explicit dummies rarely needed.
# When you do need them (e.g. for export):
library(fastDummies)
df <- df %>% dummy_cols(select_columns = "industry",
                         remove_first_dummy = TRUE,
                         remove_selected_columns = TRUE)
```

---

## 6. Interactions & polynomials

R formula syntax handles these inline; explicit columns rarely needed:

```r
# In any modeling function
fit <- feols(log_wage ~ training * tenure + I(age^2) | worker_id + year, data = df)
# - "training * tenure" expands to training + tenure + training:tenure
# - "I(age^2)" includes age squared
# - "training:tenure" alone = interaction only

# Explicit columns when you need them in the dataset (rare)
df <- df %>%
  mutate(age_sq = age^2,
         trt_x_edu = training * edu)
```

`marginaleffects::avg_slopes` and `plot_slopes` work seamlessly with formula-based interactions.

---

## 7. Panel / time-series operators

The `dplyr::lag` + `arrange()` + `group_by()` pattern is essential.

```r
df <- df %>%
  arrange(worker_id, year) %>%
  group_by(worker_id) %>%
  mutate(
    log_wage_l1 = lag(log_wage, 1),
    log_wage_l2 = lag(log_wage, 2),
    log_wage_f1 = lead(log_wage, 1),

    d_log_wage  = log_wage - lag(log_wage, 1),

    # Within-unit mean
    wage_mean_i = mean(log_wage, na.rm = TRUE),

    # Within-unit demean (when not using FE estimator)
    log_wage_dm = log_wage - wage_mean_i,

    # Growth rate (in logs)
    wage_growth = log_wage - lag(log_wage, 1)
  ) %>%
  ungroup()
```

**Gotcha**: ALWAYS `arrange(id, time) %>% group_by(id)` before `lag()`. Without grouping, `lag()` borrows the previous unit's last value.

### Rolling windows

```r
library(slider)

df <- df %>%
  arrange(worker_id, year) %>%
  group_by(worker_id) %>%
  mutate(
    wage_ma3 = slide_dbl(log_wage, mean, .before = 2, .complete = TRUE),
    wage_max5 = slide_dbl(log_wage, max,  .before = 4, .complete = TRUE)
  ) %>%
  ungroup()

# Or via runner / zoo
library(zoo)
df <- df %>%
  arrange(worker_id, year) %>%
  group_by(worker_id) %>%
  mutate(wage_ma3 = rollmean(log_wage, k = 3, fill = NA, align = "right")) %>%
  ungroup()
```

### Pre-treatment baseline (for DID heterogeneity)

```r
df <- df %>%
  group_by(worker_id) %>%
  mutate(baseline_wage = mean(log_wage[year < first_treat], na.rm = TRUE),
         baseline_wage = if_else(is.nan(baseline_wage), NA_real_, baseline_wage)) %>%
  ungroup()
```

---

## 8. Index construction

```r
# Z-score then average
components <- c("leverage", "cash_ratio", "current_ratio")
df <- df %>%
  mutate(across(all_of(components), ~ as.numeric(scale(.x)), .names = "{.col}_z")) %>%
  mutate(fin_idx_mean = rowMeans(across(ends_with("_z")), na.rm = TRUE))

# Principal component (first PC as index)
library(psych)
pc <- principal(df %>% select(all_of(components)) %>% na.omit(),
                nfactors = 1, rotate = "none")
df$fin_idx_pc1 <- as.numeric(predict(pc, df %>% select(all_of(components))))

# Or via stats::prcomp
pca <- prcomp(df %>% select(all_of(components)) %>% na.omit(),
              center = TRUE, scale. = TRUE)
summary(pca)                                   # variance explained
df$fin_idx_pc1 <- as.numeric(predict(pca, newdata = df %>%
                                       select(all_of(components))))[,1]
```

---

## 9. Deflation (CPI / PPP)

```r
cpi <- read_csv("data/cpi.csv")                # cols: year, cpi
df <- df %>% left_join(cpi, by = "year")

base_cpi <- cpi %>% filter(year == 2010) %>% pull(cpi)
df <- df %>%
  mutate(wage_real     = wage * base_cpi / cpi,
         log_wage_real = log(pmax(wage_real, 1)))

# Country-specific deflators for cross-country panels
cpi_country <- read_csv("data/cpi_country.csv")
df <- df %>%
  left_join(cpi_country, by = c("country","year")) %>%
  mutate(gdp_pc_real = gdp_pc_nom * base_cpi / cpi_country)
```

---

## 10. Binning

```r
# Equal-frequency quantiles (quintiles, deciles)
df <- df %>%
  mutate(wage_quint = ntile(wage, 5),
         tenure_dec = ntile(tenure, 10))

# Within-group quantiles
df <- df %>%
  group_by(year) %>%
  mutate(wage_quint_y = ntile(wage, 5)) %>%
  ungroup()

# Equal-width bins
df <- df %>% mutate(age_bin = cut(age, breaks = 5))

# Custom cutoffs with labels
df <- df %>%
  mutate(age_cat = cut(age,
                       breaks = c(0, 18, 30, 45, 65, Inf),
                       labels = c("Minor", "Young", "Mid", "Senior", "Retired"),
                       right = FALSE))
```

---

## 11. Per-capita / share / rate

```r
df <- df %>%
  mutate(gdp_pc       = gdp / population,
         gdp_pc_log   = log(gdp_pc),
         crime_rate   = crimes / population * 1e5)

# Within-group share
df <- df %>%
  group_by(industry, year) %>%
  mutate(mkt_share = firm_rev / sum(firm_rev, na.rm = TRUE)) %>%
  ungroup() %>%
  mutate(mkt_share_logit = log(mkt_share / (1 - mkt_share + 1e-9)))
```

---

## 12. Staggered-DID timing variables

```r
df <- df %>%
  group_by(worker_id) %>%
  mutate(first_treat = if (any(training == 1)) min(year[training == 1]) else NA_integer_) %>%
  ungroup() %>%
  mutate(
    treated_now      = year >= first_treat & !is.na(first_treat),
    rel_time         = year - first_treat,
    never_treated    = is.na(first_treat),
    not_yet_treated  = never_treated | year < first_treat,
    # Cohort variable (CS / SA / BJS expect this)
    gvar = if_else(is.na(first_treat), 0L, as.integer(first_treat))
  )

# Binned event-time (cap leads/lags)
df <- df %>%
  mutate(rt = case_when(
    is.na(rel_time)   ~ NA_integer_,
    rel_time <= -5    ~ -5L,
    rel_time >=  5    ~  5L,
    TRUE              ~ as.integer(rel_time)
  ))

# Sanity check
df %>% count(year, first_treat) %>% filter(!is.na(first_treat))
df %>% count(rel_time)
```

---

## Final checklist before Step 3

- [ ] Engineered variables follow consistent suffixes
- [ ] No `lag()` / `lead()` without `arrange() %>% group_by()`
- [ ] Factors have explicit `levels = ` with intended ordering
- [ ] Interactions / polynomials live in formulas, not as redundant columns
- [ ] Nominal variables deflated to a clearly-stated base year
- [ ] Raw columns preserved; new ones added with `{var}_*` names
- [ ] `var_label`s applied for `gtsummary` / `modelsummary` to pick up
- [ ] `saveRDS(df, "data/analysis.rds")` at the end of `02_transform.R`
