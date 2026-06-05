---
name: data-analysis
description: >-
  End-to-end data analysis workflow in R or Python — from exploration through regression to publication-ready tables and figures. Make sure to use this skill whenever the user wants to run any empirical analysis, write analysis code, or produce output from data. Triggers include: "analyze this data", "run a regression", "write R code for this", "write Python code for this", "I have a dataset", "help me with this regression", "run a DiD", "run an RDD", "event study", "IV regression", "fit a model", "produce a table", "make a figure", "explore my data", or any request involving a dataset path or empirical estimation.
argument-hint: "[dataset path or description of analysis goal]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task", "AskUserQuestion"]
---

# Data Analysis Workflow

Run an end-to-end data analysis in R or Python: load, explore, analyze, and produce publication-ready output.

**Input:** `$ARGUMENTS` — a dataset path (e.g., `data/county_panel.csv`) or a description of the analysis goal (e.g., "regress wages on education with state fixed effects using CPS data").

---

## Phase 0: Choose Language

Determine language from `$ARGUMENTS` or ask the user:
- User mentions `tidyverse`, `fixest`, `lm`, `.R` context → **R track**
- User mentions `pandas`, `statsmodels`, `sklearn`, `.py` or `.ipynb` context → **Python track**
- Dataset is `.csv`/`.parquet` with no language cue → use AskUserQuestion with a single-select menu:
  - header: "Language"
  - question: "Which language should I use for this analysis?"
  - options:
    - label: "R (Recommended)", description: "tidyverse, fixest, ggplot2 — full plugin support with coding conventions and R reviewer"
    - label: "Python", description: "pandas, statsmodels — supported for analysis scripts and figures"
    - label: "Both", description: "R for figures and tables, Python for data processing"

---

## R Track

### Constraints
- Follow `rules/r-code-conventions.md` for all standards
- Save scripts to `scripts/R/` with descriptive names
- Save all outputs (figures, tables, RDS) to `output/`
- Use `saveRDS()` for every computed object
- Run `r-reviewer` on the generated script before presenting results

### Phase 1: Setup and Data Loading
1. Create R script with proper header (title, author, purpose, inputs, outputs)
2. Load required packages at top (`library()`, never `require()`)
3. Set seed once at top: `set.seed(42)`
4. Create output directories: `dir.create("output/analysis", recursive = TRUE, showWarnings = FALSE)`
5. Load and inspect the dataset

### Phase 2: Exploratory Data Analysis
- `summary()`, missingness rates, variable types
- Histograms for key continuous variables
- Scatter plots, correlation matrices
- Panel trends, pre-treatment comparisons if applicable
- Save all diagnostic figures to `output/diagnostics/`

### Phase 3: Main Analysis
- Panel data: use `fixest`; cross-section: use `lm`/`glm`
- Cluster SEs at the appropriate level (document why)
- Multiple specifications: start simple, progressively add controls
- Report standardized effects alongside raw coefficients

### Phase 4: Publication-Ready Output
**Tables:** `modelsummary` (preferred) or `stargazer` — export `.tex` and `.html`
**Figures:** `ggplot2` with project theme; explicit `ggsave(width = X, height = Y)`; save as `.pdf` and `.png`; add `bg = "transparent"` only if output is for Beamer slides

### Phase 5: Save and Review
1. `saveRDS()` for all key objects
2. Run the `r-reviewer` agent: *"Review the script at scripts/R/[script_name].R"*
3. Address Critical and High issues before presenting results

### R Script Template
```r
# ============================================================
# [Descriptive Title]
# Author: [from project context]
# Purpose: [What this script does]
# Inputs:  [Data files]
# Outputs: [Figures, tables, RDS files]
# ============================================================

# 0. Setup ----
library(tidyverse)
library(fixest)
library(modelsummary)

set.seed(42)
dir.create("output/analysis", recursive = TRUE, showWarnings = FALSE)

# 1. Data Loading ----
# 2. Exploratory Analysis ----
# 3. Main Analysis ----
# 4. Tables and Figures ----
# 5. Export ----
```

---

## Python Track

### Constraints
- Save scripts to `scripts/python/` with descriptive names
- Save all outputs (figures, tables, pickles) to `output/`
- Use `joblib.dump()` for model objects; `.to_parquet()` for DataFrames
- Use `pathlib.Path` for all file paths — never hardcode absolute paths
- Set random seeds at the top of the script

### Phase 1: Setup and Data Loading
1. Create Python script with header (title, author, purpose, inputs, outputs)
2. Import all packages at the top of the file
3. Set seeds: `np.random.seed(42)` and `random.seed(42)`
4. Create output directories: `Path("output/analysis").mkdir(parents=True, exist_ok=True)`
5. Load and inspect the dataset with `pandas`

### Phase 2: Exploratory Data Analysis
- `df.describe()`, `df.isnull().sum()`, `df.dtypes`
- Histograms and distributions with `matplotlib`/`seaborn`
- Scatter plots and correlation matrices
- Save diagnostic figures to `output/diagnostics/`
- Save summary stats: `df.describe().to_csv("output/diagnostics/summary_stats.csv")`

### Phase 3: Main Analysis
- Cross-section OLS: `smf.ols("y ~ x", data=df).fit(cov_type="HC3")`
- Panel data: `PanelOLS` from `linearmodels` with cluster-robust SEs
- Multiple specifications: build incrementally
- Document SE choice with a comment

### Phase 4: Publication-Ready Output
**Tables:** Format with `pandas` and export via `.to_latex()` or `stargazer` (Python port)
**Figures:** `matplotlib`/`seaborn`; explicit `fig.savefig(path, dpi=300, bbox_inches="tight")`; save as `.pdf` and `.png`

### Phase 5: Save and Review
1. `joblib.dump(model, "output/model.pkl")` for fitted models
2. `df_results.to_parquet("output/results.parquet")` for DataFrames
3. Review the script manually against the Python checklist below before presenting

### Python Script Template
```python
# ============================================================
# [Descriptive Title]
# Author: [from project context]
# Purpose: [What this script does]
# Inputs:  [Data files]
# Outputs: [Figures, tables, pickle/parquet files]
# ============================================================

import random
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

# Seeds
np.random.seed(42)
random.seed(42)

# Output directories
Path("output/analysis").mkdir(parents=True, exist_ok=True)
Path("output/figures").mkdir(parents=True, exist_ok=True)

# 1. Data Loading
# 2. Exploratory Analysis
# 3. Main Analysis
# 4. Tables and Figures
# 5. Export
```

### Python Quality Checklist
```
[ ] All imports at top
[ ] Random seeds set (numpy + stdlib)
[ ] All paths use pathlib.Path — no hardcoded strings
[ ] Output directories created with mkdir(exist_ok=True)
[ ] Figures saved with explicit dpi=300, bbox_inches="tight"
[ ] Model objects saved with joblib.dump()
[ ] DataFrames saved as parquet
[ ] Comments explain WHY, not WHAT
```

---

## Shared Principles

- **Reproduce, don't guess.** If the user specifies a regression, run exactly that.
- **Show your work.** Compute summary statistics before jumping to regression.
- **Check for issues.** Look for multicollinearity, outliers, perfect prediction, missing data.
- **Use relative paths.** All paths relative to repository root.
- **No hardcoded values.** Use variables for sample restrictions, date ranges, thresholds.
