---
name: data-analysis
description: "End-to-end R data analysis for the sewage project. Writes analysis scripts following project conventions (here::here, arrow/parquet, fixest, modelsummary, native pipe), runs code review, and produces publication-ready tables and figures. This skill should be used when asked to run an analysis, estimate the model, add a specification, or write an R script."
argument-hint: "[dataset path, analysis goal, or specification description]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent"]
---

# Data Analysis

Run an end-to-end data analysis following sewage project conventions.

**Input:** `$ARGUMENTS` — a dataset path, analysis goal description, or specification to estimate.

---

## Project-Specific Context

### Analysis Organisation

Scripts in `scripts/R/09_analysis/` by approach:
- `01_descriptive/` — Maps, scatter plots, Google Trends
- `02_hedonic/` — Cross-sectional hedonic regressions
- `03_repeat_sales/` — Repeat-transaction regressions
- `04_long_difference/` — 250m grid-level long differences
- `05_news/` — DiD and event studies with media coverage
- `06_upstream_downstream/` — Directional spillover
- `07_dry_spills/` — Dry spill analysis

### Datasets

- `data/final/` — Analysis-ready datasets
- `data/processed/` — Intermediate pipeline outputs (parquet)
- All data loaded via `arrow::read_parquet()` or `arrow::open_dataset()`

### Output Destinations

- Tables: `output/tables/*.tex` (modelsummary → LaTeX with tabularray)
- Figures: `output/figures/*.pdf` or `*.png`
- Regression objects: `output/regs/*.rds`
- HTML interactive: `output/html_plots/`

### Required R Conventions

- `here::here()` for all paths
- Native pipe `|>`
- `fixest::feols()` for regressions with `vcov = "hetero"`
- `modelsummary` for table output (tabularray format, `[H]` placement)
- `arrow` for parquet I/O
- `snake_case` naming
- `forcats::as_factor()` for factors

---

## Workflow

### Step 1: Context Gathering

1. Understand the analysis goal from `$ARGUMENTS`
2. Read existing analysis scripts in the relevant subdirectory for patterns
3. Read `scripts/R/utils/spill_aggregation_utils.R` if spill metrics are involved
4. Check `data/final/` for available datasets
5. Read the relevant manuscript section in `docs/overleaf/` if the analysis feeds into the paper

### Step 2: Write Analysis Script

Follow the analysis script structure:

```r
# ================================================================
# [Descriptive Title]
# Purpose: [What this script does]
# Inputs: [Data files]
# Outputs: [Figures, tables, RDS files]
# ================================================================

# === 1. Setup ============================================

library(tidyverse)
library(fixest)
library(modelsummary)
library(arrow)
library(here)

# === 2. Data Loading =====================================

df <- read_parquet(here("data", "final", "dataset.parquet"))

# === 3. Main Analysis ====================================

model <- feols(
  log_price ~ spill_count | lsoa + year_quarter,
  data = df,
  vcov = "hetero"
)

# === 4. Tables and Figures ================================

modelsummary(
  list("Main" = model),
  output = here("output", "tables", "table_name.tex"),
  fmt = 3
)

# === 5. Export ============================================

saveRDS(model, here("output", "regs", "model_name.rds"))
```

### Step 3: Code Review

After writing the script, review it against the 9 categories from `/review-r`:
- Script structure, console hygiene, reproducibility
- Function design, figure quality, data persistence
- Comments, error handling, polish

Fix any Critical or Major issues before presenting.

### Step 4: Run the Script

If the user wants execution:
```bash
cd /Users/jacopoolivieri/Library/CloudStorage/Dropbox/01_projects/sewage
Rscript scripts/R/09_analysis/[subdir]/[script_name].R
```

### Step 5: Present Results

1. **Results summary** — Key estimates with SEs and economic interpretation
2. **Script created** — Path and description
3. **Output files** — Tables and figures generated
4. **Code review notes** — Any conventions to flag
5. **TODO items** — Missing data, additional specifications needed

---

## Principles

- **Reproduce, don't guess.** If a specific regression is requested, implement exactly that.
- **Strategy alignment.** If an analysis feeds into a manuscript section, the code must implement what the paper claims.
- **Publication-ready output.** Tables and figures should be directly includable in the paper.
- **Follow existing patterns.** Read neighbouring scripts in the same subdirectory for style consistency.
- **Save everything.** Every regression object saved as RDS, every table as LaTeX, every figure as PDF.
