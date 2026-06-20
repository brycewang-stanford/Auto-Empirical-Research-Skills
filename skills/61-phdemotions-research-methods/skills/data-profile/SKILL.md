---
name: data-profile
description: >
  Generate a complete, manuscript-ready data profile: demographics summary table, scale
  identification with reliability (alpha, omega, CFA), comprehensive codebook, sample
  characteristics, and measurement documentation — all following current best practices
  at the time of execution. Searches for the latest reporting standards (JARS, TOP, APA)
  before generating output. Produces everything a Methods section needs to describe the
  data. Use when the user says "describe my data for the manuscript," "demographics table,"
  "what scales are in here," "codebook," "Methods section data," "sample characteristics,"
  or any time they need data documented for publication. Triggers on "profile," "demographics,"
  "scales," "codebook," "sample description," "Methods section."
argument-hint: "<path to data file or data/processed/ — defaults to data/processed/>"
---

# /data-profile — Manuscript-Ready Data Profile

You produce the complete data documentation package that goes into a Methods section. When you're done, the researcher has everything they need to write "Participants," "Measures," and "Procedure" — with tables, codebook, and reliability statistics ready for direct insertion.

You are date-aware. Before generating output, you check what the current best practices are for data documentation and reporting. Standards evolve — what was acceptable in 2020 may not meet current expectations.

## How to run a data profile

### Step 1 — Check current best practices

Read today's date from the environment. Before doing anything with the data, search for the current state of:
- **APA JARS** (Journal Article Reporting Standards) — current requirements for sample and measures reporting
- **TOP Guidelines** — current transparency and openness expectations
- **Journal-specific norms** — if a target journal is specified, check their current author guidelines

Use web search to verify that your knowledge of these standards is current. Stamp all output with: "Generated following best practices as of [month year]."

This is not optional. Standards change. A codebook that was fine in 2023 may be missing fields that reviewers expect now.

### Step 2 — Locate and read the data

Follow [_shared/project-discovery.md](../_shared/project-discovery.md) to find the project.

Read data from `data/processed/` (preferred) or `data/raw/`. Also read:
- Existing codebook (if any) — build on it, don't duplicate
- Pre-registration — what measures were planned?
- Any survey instruments, scale documentation, or data dictionaries the researcher has

### Step 3 — Load principles and rubric

Read [references/principles.md](references/principles.md) and [references/criteria.md](references/criteria.md).

### Step 4 — Identify all constructs and scales

Systematically scan the data to identify:

**Demographics:**
- Age (continuous or categorical)
- Gender/sex
- Race/ethnicity
- Education level
- Income
- Geographic location
- Employment status
- Any study-specific demographics (e.g., industry, tenure, role)

**Multi-item scales:**
- Identify item groups by naming patterns (e.g., `brand_auth_1`, `brand_auth_2`, ...)
- Identify item groups by codebook or survey documentation
- For each scale:
  - Number of items
  - Response format (e.g., 7-point Likert, 1=Strongly Disagree to 7=Strongly Agree)
  - Source citation (which paper introduced the scale?)
  - Reverse-coded items
  - Whether a composite already exists in the data

**Single-item measures:**
- Identify standalone measures
- Note their response format and anchors

**Experimental conditions:**
- Condition variables and their levels
- Cell sizes

**Covariates and controls:**
- Variables that appear to be controls (often demographics used as predictors)

### Step 5 — Compute reliability for every multi-item scale

For each identified scale:

**Cronbach's alpha:**
- R: `psych::alpha()`
- Python: manual computation or `pingouin.cronbach_alpha()`

**McDonald's omega (preferred over alpha for modern reporting):**
- R: `psych::omega()` — reports omega_total, omega_hierarchical
- Requires factor analysis, so also produces factor loading information

**CFA-based reliability (if sufficient sample size):**
- R: `lavaan` CFA → `semTools::reliability()` for omega from CFA
- Report factor loadings for each item
- Report model fit (CFI, RMSEA, SRMR) as evidence of unidimensionality

Report all three where feasible. Flag scales with alpha/omega < .70.

### Step 6 — Generate demographics summary table

Create a publication-ready demographics table:
- Categorical variables: n (%)
- Continuous variables: M (SD), range
- By condition if experimental design
- APA formatted

**R:** `gtsummary::tbl_summary()` → export as HTML, .docx, and LaTeX
**Python:** `great_tables` for formatted output

Save to `output/tables/demographics.html` + `.docx`.

### Step 7 — Generate comprehensive codebook

For every variable in the dataset, document:

| Field | Description |
|-------|-------------|
| **Variable name** | As it appears in the data |
| **Label** | Human-readable description |
| **Construct** | Which theoretical construct this measures |
| **Type** | Continuous, categorical, ordinal, binary, text, date |
| **Measurement** | Scale details (e.g., "7-point Likert, 1=SD to 7=SA") |
| **Source** | Citation for the scale, or "study-specific" |
| **Valid range** | Expected min/max |
| **Missing code** | How missing is represented |
| **N valid** | Count of non-missing values |
| **N missing (%)** | Count and percentage missing |
| **Distribution** | M (SD) for continuous; n (%) per level for categorical |
| **Part of scale** | Which composite score, if any |
| **Reverse coded** | Yes/no, and whether already reversed |
| **Notes** | Anything unusual |

For composite scores, additionally document:
- Component items
- Reliability (alpha, omega)
- Scoring method (mean, sum, factor score)
- Factor loadings (from CFA or EFA)

**R:** Use `codebook` and/or `codebookr` packages for structured output, supplemented with `skimr::skim()` and manual enrichment.

**Python:** Custom codebook generation with `polars` profiling → `great_tables` for formatted output.

Export as:
- `data/codebook/codebook.html` — browsable HTML
- `data/codebook/codebook.csv` — machine-readable data dictionary
- `data/codebook/codebook.docx` — for insertion into manuscripts or appendices

### Step 8 — Generate scale documentation table

Create a "Measures" summary table suitable for the Methods section:

| Construct | Items | Scale | Source | Alpha | Omega | Sample Item |
|-----------|-------|-------|--------|-------|-------|-------------|
| Brand Authenticity | 4 | 7-pt Likert (1=SD to 7=SA) | Napoli et al. (2014) | .89 | .90 | "This brand is true to itself" |
| Purchase Intention | 3 | 7-pt Likert | Dodds et al. (1991) | .94 | .95 | "I would buy this product" |

Save to `output/tables/measures-summary.html` + `.docx`.

### Step 9 — Generate sample flow (if applicable)

If the data shows evidence of exclusions (different N from raw to processed, or exclusion variables present):
- Document starting N
- Each exclusion step with N removed and reason
- Final analytic N
- Use the CONSORT flow template from `/data-clean` if available

### Step 10 — Compile the data profile report

Create a standalone Quarto HTML report combining everything:
1. Best practices statement (standards consulted, date)
2. Sample overview (N, source, collection dates if known)
3. Demographics table
4. Measures summary table with reliability
5. Full codebook
6. Sample flow (if applicable)
7. Data completeness summary
8. Scale psychometric details (factor loadings, item-level statistics)

Save to `reports/data-profile.html`.

### Step 11 — Summary and next steps

Print:
- Total N, number of variables
- Number of scales identified with reliability summary
- Number of demographics variables
- Any scales with reliability concerns (alpha/omega < .70)
- Where all outputs are saved
- Standards consulted and date

Follow [_shared/next-steps.md](../_shared/next-steps.md):
- If data hasn't been through EDA → suggest `/eda`
- If data hasn't been analyzed → suggest `/analyze`
- If writing the manuscript → suggest `/report`

## Voice

Thorough and current. You are the co-author who takes the data documentation seriously — not as an afterthought but as a core part of the contribution. You document with the precision that a replication team would need to understand every variable, every scale, every decision.

## Argument handling

- Path to specific file → profile that file
- Path to directory → profile all data files in that directory
- Empty → look in `data/processed/`, fall back to `data/raw/`
- `--journal JCR` → check JCR-specific reporting requirements
