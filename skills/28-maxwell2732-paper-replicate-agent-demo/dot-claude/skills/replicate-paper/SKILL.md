---
name: replicate-paper
description: "Run a full 6-phase autonomous replication of a biomedical/epidemiology paper against UK Biobank or similar cohort data, producing Python and R scripts plus a validated replication report. Use when asked to replicate a paper end-to-end, or when invoked as /replicate-paper [paper.pdf] [data.csv|dta]."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
---

# Skill: /replicate-paper

**Trigger:** `/replicate-paper [paper.pdf] [data.csv|dta]` or "replicate this paper"

**Purpose:** Full 6-phase autonomous replication of a biomedical/epidemiology paper using UK Biobank or similar data. Produces Python and R scripts plus a polished validation report.

---

## Invocation

```
/replicate-paper papers/AuthorYear.pdf data/ukb_extract.csv
```

Or with just: "replicate this paper" (Claude will ask for paths if not provided).

---

## The 6-Phase Pipeline

### Phase 1: Intake

**Goal:** Understand exactly what needs to be replicated.

1. Read the paper PDF (all sections: Abstract, Methods, Results, Supplementary)
2. Identify **every table and figure** that presents empirical results
3. For each: record the gold standard values, SEs/CIs, sample sizes, and source location
4. Save targets to `quality_reports/[paper_name]_replication_targets.md`
5. Summarize: original software, data source, sample N, key methods, any replication package available

**Output:** `quality_reports/[paper_name]_replication_targets.md`

---

### Phase 2: Data Audit

**Goal:** Confirm what we can and cannot replicate given the available data.

1. Load the provided dataset (`data/[filename]`)
2. Compare to paper's described sample:
   - Total N, exposed N, event counts
   - Key variable distributions
   - Missing data patterns
3. Apply inclusion/exclusion criteria as stated in Methods; document each step's effect on N
4. If variables are missing or differently named: document the gap; flag as a known discrepancy
5. Save audit summary to `quality_reports/[paper_name]_data_audit.md`

**Output:** `quality_reports/[paper_name]_data_audit.md`

---

### Phase 3: Code Analysis

**Goal:** Map the paper's methods to our dataset before writing a single line of code.

1. Read original Stata/R code (if provided in replication package)
2. Map each variable name in original code → corresponding variable in our dataset
3. Identify methodological steps: sample construction, covariate coding, model fitting, SE clustering
4. Flag any steps where original code differs from Methods text (use the paper, not the code, as ground truth)
5. Document the mapping in `quality_reports/[paper_name]_variable_map.md`

**Output:** `quality_reports/[paper_name]_variable_map.md`

---

### Phase 4: Translation

**Goal:** Produce clean, reproducible Python and R scripts that implement the paper's analysis.

**Rules:**
- Line-by-line translation first — **no improvements during replication**
- Follow `python-code-conventions.md` and `r-code-conventions.md` exactly
- Set seed: `random.seed(YYYYMMDD)` + `numpy.random.seed(YYYYMMDD)` (Python); `set.seed(YYYYMMDD)` (R)
- Use `pathlib.Path` for all Python paths; `here::here()` for all R paths
- Comment every non-obvious Stata→Python or Stata→R translation decision
- Refer to `replication-protocol.md` translation pitfall tables

**Python script:** `replications/[paper_name]/python/replicate.py`

Structure:
```python
# Replication: [Paper Author (Year)]
# Date: YYYY-MM-DD
# Original: Stata / R
# Python version: X.Y.Z
# Key packages: pandas X.X, statsmodels X.X, lifelines X.X

from pathlib import Path
import random
import numpy as np
import pandas as pd
# ... other imports

random.seed(YYYYMMDD)
np.random.seed(YYYYMMDD)

DATA_DIR = Path(__file__).parents[3] / "data"
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# --- 1. Load Data ---
# --- 2. Sample Construction ---
# --- 3. Model Fitting ---
# --- 4. Save Results ---
```

**R script:** `replications/[paper_name]/R/replicate.R`

Structure:
```r
# Replication: [Paper Author (Year)]
# Date: YYYY-MM-DD
# Original: Stata / Python
# R version: X.Y.Z
# Key packages: survival X.X, fixest X.X

library(here)
library(tidyverse)
library(survival)
# ... other packages

set.seed(YYYYMMDD)

data_dir <- here("data")
results_dir <- here("replications", "[paper_name]", "R", "results")
dir.create(results_dir, recursive = TRUE, showWarnings = FALSE)

# --- 1. Load Data ---
# --- 2. Sample Construction ---
# --- 3. Model Fitting ---
# --- 4. Save Results ---
```

**Outputs:**
- `replications/[paper_name]/python/replicate.py`
- `replications/[paper_name]/R/replicate.R`
- `replications/[paper_name]/python/results/` (parquet/pkl files)
- `replications/[paper_name]/R/results/` (rds files)

---

### Phase 5: Validation

**Goal:** Run both scripts and compare results to gold standard targets.

1. Execute Python script: `python replications/[paper_name]/python/replicate.py`
2. Execute R script: `Rscript replications/[paper_name]/R/replicate.R`
3. Load results; compare to targets using tolerance thresholds from `replication-protocol.md`:
   - Integers: exact
   - Point estimates: ±0.01
   - SEs: ±0.05
   - P-values: same significance bracket
   - Percentages: ±0.1pp
4. For each mismatch: investigate root cause before proceeding
5. Save `replications/[paper_name]/validation_report.md`

**Output:** `replications/[paper_name]/validation_report.md`

---

### Phase 6: Report

**Goal:** Produce a polished, self-contained replication report.

Report structure:
```markdown
# Replication Report: [Paper Author (Year)]
**Date:** [YYYY-MM-DD]
**Replicator:** Claude (domain-reviewer verified)

## Paper Summary
[1 paragraph: research question, population, exposure, outcome, key finding]

## Methods Summary
[Bullet list: sample, exclusions, covariates, model, SEs, software]

## Data
[Bullet list: our dataset, N after exclusions, any discrepancies vs. paper sample]

## Results Comparison

| Target | Table/Fig | Paper Value | Our Value (Python) | Our Value (R) | Diff | Status |
|--------|-----------|-------------|-------------------|---------------|------|--------|

## Discrepancies
[Each discrepancy: what, investigated how, resolved or not]

## Corrective Steps Taken
[Any adjustments made during validation and why]

## Verdict
**[REPLICATED / PARTIAL / FAILED]**
- Targets matched: N / Total
- Remaining discrepancies: [list or "none"]

## Reproducibility
- Python: X.Y.Z | pandas X.X | statsmodels X.X | lifelines X.X
- R: X.Y.Z | survival X.X | fixest X.X
- Data: [filename, UKB application ID if applicable]
- Seed: YYYYMMDD
```

Save to: `reports/[paper_name]_replication_report.md`

After saving: run domain-reviewer agent on the report.

---

## Quality Gate

After Phase 6, score the output. Minimum 80/100 to commit.

**Auto-commit if score >= 80:**
```
git add replications/[paper_name]/ reports/[paper_name]_replication_report.md quality_reports/[paper_name]_*.md
git commit -m "Replicate [Paper Author (Year)] -- [VERDICT]: N/Total targets matched"
```

---

## Failure Modes & Recovery

| Failure | Recovery |
|---------|---------|
| Script syntax error | Fix before proceeding |
| N mismatch > 5% | Stop, audit inclusion/exclusion criteria |
| All point estimates off by same factor | Check unit conversion (HR vs. log-HR, OR vs. log-OR) |
| SEs systematically too large | Check clustering level |
| Cannot install package | Document, note in report, use closest alternative |
| Data variable missing | Document gap; attempt proxy; flag as ASSUMED in report |
