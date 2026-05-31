# Step 3 — Descriptive Statistics & Table 1 in R (Deep Reference)

Goal: before any regression, produce the full descriptive set a referee expects — sample size, central tendency, dispersion, comparison across treatment, balance with SMDs, correlation matrix with significance stars, and the distribution / time-trend plots that motivate identification.

R's modern table ecosystem (`gtsummary`, `modelsummary::datasummary*`, `tableone`) makes this almost a one-liner.

## Contents

1. Full-sample summary (`gtsummary::tbl_summary`, `datasummary_skim`, `psych::describe`)
2. Stratified Table 1 (treated vs control) with SMDs
3. Weighted descriptives (`survey`, `gtsummary` weights)
4. Correlation matrix with significance + heatmap
5. Distribution plots (`ggplot2`, `ggdist`, density / ECDF / Q-Q)
6. Group comparisons (box / violin / strip / sina via `ggdist`)
7. Time-trend (DID motivation) plot
8. Panel coverage diagnostics
9. Binscatter via `binsreg`
10. Export recipes (LaTeX, Word, HTML, Excel, PNG/PDF)

---

## 1. Full-sample summary

### `gtsummary` — modern Table 1 standard

```r
library(gtsummary)
library(dplyr)

df %>%
  select(log_wage, age, edu, tenure, training, female) %>%
  tbl_summary(
    type  = list(all_continuous() ~ "continuous2"),
    statistic = list(
      all_continuous()  ~ c("{N_nonmiss}", "{mean} ({sd})",
                            "{min} – {median} – {max}"),
      all_categorical() ~ "{n} ({p}%)"
    ),
    digits = list(all_continuous() ~ 3),
    label  = list(log_wage ~ "Log monthly wage",
                  age      ~ "Age (years)",
                  edu      ~ "Years of education",
                  tenure   ~ "Tenure (years)",
                  training ~ "Received training",
                  female   ~ "Female")
  ) %>%
  bold_labels() %>%
  add_n()
```

### `modelsummary::datasummary*` — fast & format-flexible

```r
library(modelsummary)

# One-shot summary
df %>%
  select(log_wage, age, edu, tenure, training) %>%
  datasummary_skim(output = "tables/table1_full.tex")

# Custom layout
datasummary(
  log_wage + age + edu + tenure ~ N + Mean + SD + Min + Median + Max,
  data = df,
  output = "tables/table1_full.html"
)
```

### `psych::describe` — quick numeric summary

```r
library(psych)
df %>% select(log_wage, age, edu, tenure) %>% describe()
# Outputs: vars, n, mean, sd, median, trimmed, mad, min, max, range, skew, kurtosis, se
```

For categoricals, frequencies:

```r
df %>%
  count(industry, sort = TRUE) %>%
  mutate(pct = n / sum(n) * 100)
```

---

## 2. Stratified Table 1 (treated vs control + SMDs)

The single most-read table in any empirical paper.

### `gtsummary` route — most polished

```r
df %>%
  select(log_wage, age, edu, tenure, female, training) %>%
  tbl_summary(by = training, missing = "ifany",
              statistic = all_continuous() ~ "{mean} ({sd})") %>%
  add_p() %>%                              # Wilcoxon / chi-sq automatically
  add_difference() %>%                     # group difference
  add_overall() %>%
  modify_header(label = "**Variable**") %>%
  modify_caption("**Table 1.** Sample characteristics by treatment status") %>%
  bold_labels() %>%
  as_kable_extra(format = "latex", booktabs = TRUE) %>%
  kableExtra::save_kable("tables/table1_balance.tex")
```

### `modelsummary::datasummary_balance` — fastest LaTeX path

```r
datasummary_balance(
  ~ training,
  data = df %>% select(training, age, edu, tenure, female),
  output = "tables/table1_balance.tex",
  fmt = 3,
  dinm = TRUE,                            # difference-in-means column
  dinm_statistic = "p.value"              # add p-value
)
```

### `tableone` route — gives clean SMD column

```r
library(tableone)
vars <- c("log_wage", "age", "edu", "tenure", "female")
t1 <- CreateTableOne(vars = vars, strata = "training", data = df,
                     factorVars = "female", test = TRUE)
print(t1, smd = TRUE, showAllLevels = TRUE,
      catDigits = 1, contDigits = 3, missing = TRUE,
      printToggle = FALSE) %>%
  kableExtra::kable("latex", booktabs = TRUE) %>%
  kableExtra::save_kable("tables/table1_tableone.tex")
```

**Interpretation rules**:

| |SMD| | Reading |
|------|---------|
| < 0.10 | well-balanced |
| 0.10 – 0.25 | modest imbalance — control in regression |
| > 0.25 | severe — consider matching / weighting |

---

## 3. Weighted descriptives

```r
library(survey)
library(gtsummary)

# Declare survey design
svy_design <- svydesign(ids = ~psu, strata = ~stratum, weights = ~svy_wt, data = df)

# Weighted Table 1
svy_design %>%
  tbl_svysummary(
    by = training,
    include = c(log_wage, age, edu, tenure, female)
  ) %>%
  add_p() %>%
  add_overall()

# Weighted summary stat (one-off)
weighted.mean(df$wage, df$svy_wt, na.rm = TRUE)
Hmisc::wtd.mean(df$wage, df$svy_wt)
Hmisc::wtd.var(df$wage, df$svy_wt)
Hmisc::wtd.quantile(df$wage, weights = df$svy_wt, probs = c(0.25, 0.5, 0.75))
```

---

## 4. Correlation matrix with significance

```r
library(psych)
library(corrplot)

cols <- c("log_wage","age","edu","tenure","training")

# corr.test gives r, p, n with adjustment for multiple testing
ct <- corr.test(df %>% select(all_of(cols)), method = "pearson", adjust = "BH")
ct$r        # correlation matrix
ct$p        # p-values (upper tri = adjusted, lower = unadjusted)

# Heatmap with significance markers (insig = "blank" hides non-sig)
corrplot(ct$r, method = "color", type = "upper",
         p.mat = ct$p, sig.level = 0.05, insig = "blank",
         addCoef.col = "black", number.cex = 0.7,
         tl.col = "black", tl.srt = 45,
         col = colorRampPalette(c("#B2182B","white","#2166AC"))(200),
         title = "", mar = c(0,0,1,0))
# Save:
pdf("figures/corr_heatmap.pdf", width = 6, height = 5)
corrplot(...)
dev.off()

# Or via ggcorrplot (ggplot-native)
library(ggcorrplot)
ggcorrplot(ct$r, p.mat = ct$p, type = "upper",
           hc.order = TRUE, lab = TRUE, lab_size = 3,
           outline.color = "white",
           colors = c("#B2182B", "white", "#2166AC"),
           insig = "blank", sig.level = 0.05) +
  labs(title = "Correlation matrix (asterisks = p < 0.05)")
ggsave("figures/corr_ggcorr.pdf", width = 6, height = 5)

# Spearman (rank-based)
ct_sp <- corr.test(df %>% select(all_of(cols)), method = "spearman")
```

For LaTeX export of correlations:

```r
library(modelsummary)
datasummary_correlation(df %>% select(all_of(cols)),
                        output = "tables/corr.tex")
```

---

## 5. Distribution plots

```r
library(ggplot2)

# Histogram + density
p_hist <- ggplot(df, aes(wage)) +
  geom_histogram(bins = 50, fill = "navy", alpha = 0.7) +
  labs(title = "(a) Histogram", x = "Wage", y = "Count") +
  theme_classic()

# KDE by group
p_kde <- ggplot(df, aes(log_wage, fill = factor(training))) +
  geom_density(alpha = 0.5) +
  scale_fill_manual(values = c("0" = "darkred", "1" = "navy"),
                    labels = c("Control","Treated"), name = "") +
  labs(title = "(b) KDE by treatment", x = "Log wage", y = "Density") +
  theme_classic() + theme(legend.position = "bottom")

# ECDF
p_ecdf <- ggplot(df, aes(log_wage, color = factor(training))) +
  stat_ecdf(geom = "step", linewidth = 0.7) +
  scale_color_manual(values = c("0" = "darkred", "1" = "navy"),
                     labels = c("Control","Treated"), name = "") +
  labs(title = "(c) ECDF", x = "Log wage", y = "Cumulative share") +
  theme_classic() + theme(legend.position = "bottom")

# Q-Q vs Normal
p_qq <- ggplot(df, aes(sample = log_wage)) +
  stat_qq(alpha = 0.3) + stat_qq_line(color = "red") +
  labs(title = "(d) Q-Q vs Normal", x = "Theoretical", y = "Sample") +
  theme_classic()

library(cowplot)
cowplot::plot_grid(p_hist, p_kde, p_ecdf, p_qq, ncol = 2) +
  ggsave("figures/distributions.pdf", width = 10, height = 7)

# Two-sample KS
ks.test(df$log_wage[df$training == 1],
        df$log_wage[df$training == 0])
```

---

## 6. Group comparisons

```r
library(ggplot2)
library(ggdist)        # half-eye / sina / dotplot — modern alternative to box+violin

ggplot(df, aes(factor(training), log_wage)) +
  ggdist::stat_halfeye(adjust = 0.5, width = 0.5,
                       .width = 0, justification = -0.2) +
  geom_boxplot(width = 0.15, outlier.shape = NA, alpha = 0.5) +
  ggdist::stat_dots(side = "left", justification = 1.2,
                    binwidth = 0.025, alpha = 0.3) +
  scale_x_discrete(labels = c("0" = "Control", "1" = "Treated")) +
  labs(x = "", y = "Log wage", title = "Distribution comparison")
ggsave("figures/group_compare.pdf", width = 6, height = 4)
```

---

## 7. Time-trend (DID motivation) plot

```r
trend <- df %>%
  group_by(year, training) %>%
  summarise(mean_log_wage = mean(log_wage, na.rm = TRUE),
            n             = n(), .groups = "drop")

ggplot(trend, aes(year, mean_log_wage, color = factor(training))) +
  geom_line(linewidth = 1) +
  geom_point(size = 2.5) +
  geom_vline(xintercept = policy_year, linetype = "dashed", color = "gray40") +
  annotate("text", x = policy_year, y = max(trend$mean_log_wage),
           label = "Policy", hjust = -0.1, color = "gray40") +
  scale_color_manual(values = c("0" = "darkred", "1" = "navy"),
                     labels = c("Control","Treated"), name = "") +
  labs(x = "Year", y = "Mean log wage",
       title = "Pre/post trends by treatment status") +
  theme_classic() + theme(legend.position = "bottom")
ggsave("figures/trend_did.pdf", width = 7, height = 4)

# Difference (treated − control) — pre-period should hug zero
trend_diff <- trend %>%
  pivot_wider(id_cols = year, names_from = training, values_from = mean_log_wage,
              names_prefix = "g") %>%
  mutate(diff = g1 - g0)

ggplot(trend_diff, aes(year, diff)) +
  geom_line(linewidth = 1, color = "navy") +
  geom_point(size = 2.5, color = "navy") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = policy_year, linetype = "dashed", color = "gray40") +
  labs(y = "Δ log wage (treated − control)", x = "Year")
ggsave("figures/did_diff.pdf", width = 7, height = 4)
```

---

## 8. Panel coverage diagnostics

```r
# Units per year
df %>%
  count(year, name = "n_units") %>%
  ggplot(aes(year, n_units)) +
  geom_col(fill = "navy", alpha = 0.8) +
  labs(x = "Year", y = "# unique observations") +
  theme_classic()
ggsave("figures/panel_coverage.pdf", width = 7, height = 4)

# Years per unit
df %>%
  count(worker_id) %>%
  ggplot(aes(n)) + geom_histogram(bins = 30, fill = "navy", alpha = 0.8) +
  labs(x = "# years observed per worker", y = "Count") +
  theme_classic()
ggsave("figures/years_per_unit.pdf", width = 6, height = 4)

# Cohort sizes (staggered DID)
df %>%
  filter(!is.na(first_treat)) %>%
  distinct(worker_id, first_treat) %>%
  count(first_treat) %>%
  ggplot(aes(first_treat, n)) + geom_col(fill = "navy", alpha = 0.8) +
  labs(x = "First treatment year", y = "# units") + theme_classic()
ggsave("figures/cohort_sizes.pdf", width = 6, height = 4)

# Observation-matrix heatmap
df %>%
  mutate(obs = 1) %>%
  ggplot(aes(year, factor(worker_id), fill = obs)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "black", guide = "none") +
  labs(x = "Year", y = "Worker", title = "Observed (black) vs missing (white)") +
  theme_classic() + theme(axis.text.y = element_blank())
ggsave("figures/obs_heatmap.pdf", width = 8, height = 5)
```

---

## 9. Binscatter

```r
library(binsreg)

# Default — residualized + CI band
bs <- binsreg(y = df$log_wage, x = df$tenure,
              w = df %>% select(age, edu, female),
              nbins = 20, polyreg = 1, ci = c(2,2))
# bs$bins_plot is a ggplot object — save it:
bs$bins_plot + labs(x = "Tenure", y = "Residualized log wage")
ggsave("figures/binscatter_resid.pdf", width = 7, height = 4)

# By group
binsreg(y = df$log_wage, x = df$tenure, by = df$training,
        w = df %>% select(age, edu),
        nbins = 20)$bins_plot
```

---

## 10. Export recipes

```r
# LaTeX
datasummary_skim(df %>% select(...), output = "tables/x.tex")
gtsummary_obj %>%
  as_kable_extra(format = "latex", booktabs = TRUE) %>%
  kableExtra::save_kable("tables/x.tex")

# Word
gtsummary_obj %>%
  as_flex_table() %>%
  flextable::save_as_docx(path = "tables/x.docx")
modelsummary(..., output = "tables/x.docx")

# HTML
gtsummary_obj %>% as_gt() %>% gt::gtsave("tables/x.html")

# Excel
df %>% writexl::write_xlsx("tables/x.xlsx")

# Figures (always both PDF for LaTeX + PNG for Word/web)
ggsave("figures/x.pdf", width = 7, height = 4)
ggsave("figures/x.png", width = 7, height = 4, dpi = 300)
```

---

## Standard Step 3 deliverable

For every paper, produce these 6 artifacts in Step 3:

1. `tables/table1_full.tex` — full-sample summary
2. `tables/table1_balance.tex` — treated vs. control + SMDs
3. `figures/corr_heatmap.pdf` — correlation heatmap with stars
4. `figures/distributions.pdf` — 2×2 panel (hist + KDE + ECDF + Q-Q)
5. `figures/trend_did.pdf` — DID motivation plot
6. `figures/panel_coverage.pdf` (or `cohort_sizes.pdf` for staggered designs)

Once all 6 exist and look right, you can move to Step 4 with full confidence about the sample.
