# Step 8 — Publication Tables & Figures in R (Deep Reference)

Goal: turn estimates and graphs into camera-ready outputs — `.tex` for LaTeX, `.docx` for Word collaborators, `.html` for journal supplements, `.pdf` / `.png` figures with consistent ggplot2 styling. R's modern table ecosystem (`modelsummary`, `gtsummary`, `kableExtra`, `gt`, `flextable`) is unusually flexible; one call → any format.

## Contents

1. Regression tables — `modelsummary` (preferred), `texreg`, `stargazer`, `gtsummary::tbl_regression`
2. Summary-statistics tables — `gtsummary`, `modelsummary::datasummary*`
3. Coefficient plots — `modelplot`, hand-rolled ggplot
4. Event-study plots (`fixest::iplot`, `ggplot2`)
5. Forest plots (subgroup / heterogeneity)
6. Marginal-effect plots (`marginaleffects::plot_slopes` / `plot_predictions`)
7. Binscatter (`binsreg`)
8. RD plots (`rdplot`)
9. CATE heatmap
10. Multi-panel combined (`cowplot`, `patchwork`)
11. Themes, fonts, color palettes
12. Quarto / RMarkdown for narrative + code + outputs

---

## 1. Regression tables

### `modelsummary` — modern default (writes any format)

```r
library(modelsummary)

# LaTeX output
modelsummary(
  list("(1)" = m1, "(2)" = m2, "(3)" = m3,
       "(4)" = m4, "(5)" = m5, "(6)" = m6),
  stars = c('*' = .1, '**' = .05, '***' = .01),
  coef_map = c("training" = "Training",
               "age"      = "Age",
               "edu"      = "Education",
               "tenure"   = "Tenure"),
  gof_map = list(
    list(raw = "nobs",          clean = "N",        fmt = 0),
    list(raw = "r.squared",     clean = "R²",       fmt = 3),
    list(raw = "adj.r.squared", clean = "Adj. R²",  fmt = 3),
    list(raw = "FE: worker_id", clean = "Worker FE",fmt = 0),
    list(raw = "FE: year",      clean = "Year FE",  fmt = 0)
  ),
  notes = list("Cluster-robust SEs in parentheses, clustered by worker_id."),
  output = "tables/table_main.tex"
)

# Word
modelsummary(list("(1)" = m1, "(3)" = m3, "(6)" = m6),
             stars = TRUE, output = "tables/table_main.docx")

# HTML
modelsummary(list("(1)" = m1, "(6)" = m6),
             stars = TRUE, output = "tables/table_main.html")

# Markdown
modelsummary(list(m1, m6), stars = TRUE,
             output = "markdown")              # prints to console
```

### `texreg` — alternative for LaTeX

```r
library(texreg)
texreg(list(m1, m3, m6),
       caption = "Effect of training on log wage",
       label = "tab:main",
       custom.coef.map = list("training" = "Training",
                              "age" = "Age", "edu" = "Education"),
       stars = c(0.01, 0.05, 0.10),
       file = "tables/table_main_texreg.tex")
```

### `stargazer` — the classic (best for LM/GLM, less for fixest)

```r
library(stargazer)
stargazer(m1$lm, m3$lm, m6$lm,        # convert fixest → lm if needed
          out = "tables/table_main_stargazer.tex",
          type = "latex",
          star.cutoffs = c(0.10, 0.05, 0.01))
```

### `gtsummary::tbl_regression` — clinical-style tables

```r
library(gtsummary)
m6 %>%
  tbl_regression(
    label = list(training ~ "Training",
                 age      ~ "Age",
                 edu      ~ "Education")
  ) %>%
  bold_p(t = 0.05) %>%
  add_significance_stars() %>%
  as_kable_extra(format = "latex", booktabs = TRUE) %>%
  kableExtra::save_kable("tables/m6_clinical.tex")
```

---

## 2. Summary-statistics tables

```r
library(modelsummary)

# Quick skim
df %>% select(log_wage, age, edu, tenure, training) %>%
  datasummary_skim(output = "tables/summary_skim.tex")

# Custom layout
datasummary(
  log_wage + age + edu + tenure ~ N + Mean + SD + Min + Median + Max,
  data = df,
  output = "tables/summary_custom.tex"
)

# Stratified balance table (one call)
datasummary_balance(~ training,
                    data = df %>% select(training, age, edu, tenure, female),
                    dinm = TRUE, dinm_statistic = "p.value",
                    output = "tables/balance.tex")
```

---

## 3. Coefficient plots

### `modelplot` — fast ggplot

```r
library(modelsummary)

modelplot(list("M1" = m1, "M3" = m3, "M6" = m6),
          coef_map = c("training" = "Training")) +
  geom_vline(xintercept = 0, linetype = "dashed", alpha = 0.5) +
  labs(x = "Coefficient on training", y = "",
       title = "Effect of training across specifications") +
  theme_classic() + theme(legend.title = element_blank())
ggsave("figures/coefplot_main.pdf", width = 6, height = 3.5)

# Multiple coefficients + multiple models
modelplot(list("Raw" = m1, "+ unit FE" = m3, "+ unit×year + ind×year FE" = m6),
          coef_map = c("training" = "Training",
                       "age" = "Age", "edu" = "Education", "tenure" = "Tenure")) +
  geom_vline(xintercept = 0, linetype = "dashed") +
  facet_wrap(~ term, scales = "free_x")
ggsave("figures/coefplot_multi.pdf", width = 8, height = 4)
```

### Hand-rolled ggplot version (full control)

```r
library(broom)

coef_df <- imap_dfr(list("M1" = m1, "M3" = m3, "M6" = m6),
                    function(fit, name) {
                      tidy(fit, conf.int = TRUE) %>%
                        filter(term == "training") %>%
                        mutate(spec = name)
                    })

ggplot(coef_df, aes(estimate, spec)) +
  geom_point(size = 3, color = "navy") +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high),
                 height = 0.2, color = "navy") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  labs(x = "Coefficient on training", y = "",
       title = "Effect of training") +
  theme_classic()
ggsave("figures/coefplot_handroll.pdf", width = 6, height = 3.5)
```

---

## 4. Event-study plots

```r
library(fixest)

# Cleanest: fixest::iplot
es <- feols(log_wage ~ i(rel_time, ref = -1) | worker_id + year,
            data = df %>% filter(!is.na(first_treat)),
            cluster = ~ worker_id)

# Default plot
iplot(es,
      xlab = "Years relative to treatment",
      ylab = "Coefficient (ATT)",
      main = "Event study")

# Save iplot output (uses base graphics)
pdf("figures/event_study.pdf", width = 7, height = 4)
iplot(es,
      ref.line = -0.5, pt.join = TRUE,
      xlab = "Years relative to treatment",
      ylab = "Coefficient (ATT)")
dev.off()

# ggplot version (more flexibility) — pull coefficients via broom
library(broom); library(ggplot2)

es_df <- broom::tidy(es, conf.int = TRUE) %>%
  filter(stringr::str_detect(term, "rel_time::")) %>%
  mutate(k = as.integer(stringr::str_extract(term, "-?\\d+"))) %>%
  bind_rows(tibble(term = "rel_time::-1",
                   estimate = 0, std.error = 0,
                   conf.low = 0, conf.high = 0, k = -1)) %>%
  arrange(k)

ggplot(es_df, aes(k, estimate)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = -0.5, linetype = "dashed", color = "red") +
  geom_line(color = "navy") +
  geom_point(size = 2, color = "navy") +
  geom_errorbar(aes(ymin = conf.low, ymax = conf.high),
                width = 0.2, color = "navy") +
  labs(x = "Years relative to treatment", y = "Coefficient (ATT)") +
  theme_classic()
ggsave("figures/event_study_gg.pdf", width = 7, height = 4)

# After did::att_gt
ggdid(cs)                                    # comes with did package
ggsave("figures/csdid_event.pdf", width = 7, height = 4)
```

---

## 5. Forest plot for subgroup heterogeneity

```r
library(broom)

groups <- list(
  "All"            = df,
  "Female = 0"     = df %>% filter(female == 0),
  "Female = 1"     = df %>% filter(female == 1),
  "Young (<40)"    = df %>% filter(age < 40),
  "Old (≥40)"      = df %>% filter(age >= 40),
  "Manuf"          = df %>% filter(industry == "manuf"),
  "Service"        = df %>% filter(industry == "service")
)

forest_df <- imap_dfr(groups, function(d, name) {
  fit <- feols(log_wage ~ training | worker_id + year,
               data = d, cluster = ~ worker_id)
  tidy(fit, conf.int = TRUE) %>%
    filter(term == "training") %>%
    mutate(group = name, N = nobs(fit))
})

ggplot(forest_df,
       aes(estimate, fct_rev(factor(group)))) +
  geom_point(size = 3, color = "navy") +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high),
                 height = 0.2, color = "navy") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  geom_text(aes(label = paste0("N=", N)),
            x = max(forest_df$conf.high) * 1.1, hjust = 0, size = 3) +
  labs(x = "Coefficient on training", y = "") +
  theme_classic() + xlim(NA, max(forest_df$conf.high) * 1.3)
ggsave("figures/forest.pdf", width = 7, height = 4)
```

---

## 6. Marginal-effect / prediction plots (`marginaleffects`)

```r
library(marginaleffects)

# Continuous moderator
m_int <- feols(log_wage ~ training * tenure + age + edu | worker_id + year,
               data = df, cluster = ~ worker_id)

plot_slopes(m_int, variables = "training",
            condition = list(tenure = seq(0, 20, by = 1))) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(x = "Tenure (years)", y = "Marginal effect of training",
       title = "How training's effect varies with tenure")
ggsave("figures/marginsplot_tenure.pdf", width = 7, height = 4)

# Categorical moderator
plot_slopes(m_int, variables = "training", condition = "female") +
  labs(x = "Female", y = "Marginal effect of training")

# Predicted Y across levels
plot_predictions(m_int,
                 condition = list(training = c(0,1), tenure = seq(0,20,by=2))) +
  labs(x = "Tenure", y = "Predicted log wage")
```

---

## 7. Binscatter

```r
library(binsreg)

# Default — modern choice (Cattaneo et al.)
bs <- binsreg(y = df$log_wage, x = df$tenure,
              w = df %>% select(age, edu, female),
              nbins = 20, polyreg = 1, ci = c(2, 2))

bs$bins_plot +
  labs(x = "Tenure", y = "Residualized log wage",
       title = "Wage vs. tenure, residualized on age + edu + female") +
  theme_classic()
ggsave("figures/binscatter.pdf", width = 7, height = 4)

# By group
binsreg(y = df$log_wage, x = df$tenure, by = df$training,
        w = df %>% select(age, edu),
        nbins = 20, polyreg = 1)$bins_plot +
  labs(color = "Treatment")
ggsave("figures/binscatter_bygroup.pdf", width = 7, height = 4)
```

---

## 8. RD plots

```r
library(rdrobust)

# Default
rdplot(y = df$outcome, x = df$running_var, c = 0,
       p = 1, binselect = "esmv",
       title = "Effect of eligibility on earnings",
       y.label = "Earnings", x.label = "Eligibility score (centered)")

# Save
pdf("figures/rd_main.pdf", width = 7, height = 4)
rdplot(y = df$outcome, x = df$running_var, c = 0)
dev.off()

# Density (manipulation) plot
library(rddensity)
rdd <- rddensity(X = df$running_var, c = 0)
rdplotdensity(rdd, X = df$running_var)
ggsave("figures/rd_density.pdf", width = 6, height = 4)
```

---

## 9. CATE heatmap

```r
library(grf)

# Build a 2-D grid holding other vars at median
grid <- expand_grid(
  age      = seq(quantile(df$age, .05),    quantile(df$age, .95),    length.out = 30),
  tenure   = seq(quantile(df$tenure, .05), quantile(df$tenure, .95), length.out = 30)
) %>%
  mutate(edu       = median(df$edu),
         firm_size = median(df$firm_size))

X_grid <- grid %>% select(age, edu, tenure, firm_size) %>% as.matrix()
grid$tau <- predict(cf, newdata = X_grid)$predictions

ggplot(grid, aes(age, tenure, fill = tau)) +
  geom_tile() +
  scale_fill_gradient2(low = "darkred", mid = "white", high = "navy",
                       midpoint = 0, name = "CATE") +
  labs(x = "Age", y = "Tenure", title = "Heterogeneous treatment effect") +
  theme_classic()
ggsave("figures/cate_heatmap.pdf", width = 7, height = 5)
```

---

## 10. Multi-panel combined

```r
library(cowplot)
library(patchwork)

# cowplot
p_combo <- plot_grid(p_kde, p_ecdf, p_qq, p_corr,
                     labels = "auto", ncol = 2)
ggsave("figures/combined_distributions.pdf", p_combo, width = 10, height = 8)

# patchwork (more flexible)
(p1 + p2) / (p3 + p4) +
  plot_annotation(title = "Distribution diagnostics",
                  tag_levels = 'A')
ggsave("figures/combined_patchwork.pdf", width = 10, height = 8)
```

---

## 11. Themes, fonts, color palettes

Set once at the top of `08_tables_figures.R`:

```r
library(ggplot2)
library(showtext)                          # font embedding

# Global theme
theme_set(
  theme_classic(base_size = 11, base_family = "sans") +
    theme(
      legend.position = "bottom",
      plot.title    = element_text(face = "bold"),
      plot.subtitle = element_text(color = "gray30"),
      strip.background = element_rect(fill = "gray95", color = NA),
      panel.grid.major.y = element_line(color = "gray90", linetype = "dotted")
    )
)

# Default colors — colorblind-safe palette (viridis)
options(ggplot2.discrete.colour = c("#1f77b4","#d62728","#2ca02c","#9467bd","#ff7f0e"),
        ggplot2.discrete.fill   = c("#1f77b4","#d62728","#2ca02c","#9467bd","#ff7f0e"))

# Font embedding
font_add_google("EB Garamond", "garamond")
showtext_auto()

# Save high-res
ggsave("figures/x.pdf", width = 7, height = 4, device = cairo_pdf)
ggsave("figures/x.png", width = 7, height = 4, dpi = 300)
```

---

## 12. Quarto / RMarkdown — narrative + code + outputs

For collaborators or reproducible research, render the entire empirical pipeline to a single PDF / HTML / Word document:

```yaml
---
title: "Effect of Training on Wages — Replication"
author: "Bryce Wang"
date: today
format:
  pdf:
    documentclass: article
    fontfamily: ebgaramond
    fontsize: 11pt
    geometry:
      - margin=1in
    toc: false
    number-sections: true
    keep-tex: true
  html:
    theme: cosmo
    toc: true
    toc-location: left
execute:
  echo: false
  warning: false
---
```

```{r setup}
#| include: false
library(tidyverse); library(fixest); library(modelsummary)
library(here)
df <- readRDS(here("data","analysis.rds"))
```

```{r main-table}
#| label: tbl-main
#| tbl-cap: "Effect of training on log wage"
modelsummary(list("(1)" = m1, "(3)" = m3, "(6)" = m6),
             stars = TRUE, output = "kableExtra")
```

```{r event-study}
#| label: fig-event
#| fig-cap: "Event study"
#| fig-width: 7
#| fig-height: 4
iplot(es)
```

Render with `quarto render main.qmd` — produces a single self-contained document, tables / figures inline.

---

## Canonical output directory

```
project/
├── tables/
│   ├── summary_full.tex
│   ├── balance.tex
│   ├── table_main.tex
│   ├── table_main.docx
│   ├── subsamples.tex
│   ├── outcome_ladder.tex
│   ├── mediation.tex
│   └── cate_blp.tex
├── figures/
│   ├── corr_heatmap.pdf
│   ├── distributions.pdf
│   ├── trend_did.pdf
│   ├── panel_coverage.pdf
│   ├── coefplot_main.pdf
│   ├── event_study.pdf
│   ├── csdid_event.pdf
│   ├── forest.pdf
│   ├── marginsplot_tenure.pdf
│   ├── binscatter.pdf
│   ├── rd_main.pdf
│   ├── rd_density.pdf
│   ├── bacon.pdf
│   ├── honestdid.pdf
│   ├── ri.pdf
│   ├── spec_curve.pdf
│   ├── loo.pdf
│   ├── cate_tenure.pdf
│   ├── cate_heatmap.pdf
│   └── combined.pdf
├── logs/
│   └── 04_diagnostics.txt
└── main.qmd                     # renders to PDF / HTML / Word
```

Everything regenerated by `Rscript main.R` or `quarto render main.qmd`. No manual Excel formatting, no PowerPoint screenshots, no LaTeX hand-editing.
