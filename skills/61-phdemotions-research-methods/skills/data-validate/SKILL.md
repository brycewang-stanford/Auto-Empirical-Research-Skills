---
name: data-validate
description: >
  Run declarative data quality checks and generate a codebook. Checks completeness, distributions,
  impossible values, duplicates, outliers, encoding issues, attention check failures, and manipulation
  check results. Produces a pointblank/pandera validation report and an auto-generated codebook.
  Use when the user says "validate data," "check data quality," "generate codebook," "what's wrong
  with my data," "data audit," "check my dataset," or when /research-intake identifies missing
  validation. Triggers on "validate," "data quality," "codebook," "check my data."
argument-hint: "<path to data file or data/raw/ directory — defaults to data/raw/>"
---

# /data-validate — Data Quality Assessment

You are the first line of defense against bad data. Your job is to systematically examine every aspect of a dataset before any analysis happens, and to generate the documentation that makes the data understandable to anyone.

You never assume data is clean. You check everything. And you produce two things: a validation report (what's wrong) and a codebook (what this data IS).

## How to run validation

### Step 1 — Locate and read the data

Follow [_shared/project-discovery.md](../_shared/project-discovery.md) to find the project root. Look for data in `data/raw/`. If the researcher points to a specific file, use that.

Read the data. Identify:
- File format (CSV, Excel, SPSS .sav, Stata .dta, Parquet)
- Number of rows and columns
- Variable names and types
- Whether there are existing labels (SPSS/Stata files often have embedded labels)

### Step 2 — Load rubric and run checks

Read [references/principles.md](references/principles.md) and [references/criteria.md](references/criteria.md).

For each criterion in the rubric, check the data and record findings.

### Step 3 — Generate codebook

For each variable, document:
- **Name:** variable name in the data
- **Label:** human-readable description (from SPSS labels, or inferred, or ask researcher)
- **Type:** continuous, categorical, ordinal, binary, text, date
- **Measurement:** scale details (e.g., "7-point Likert, 1=Strongly Disagree to 7=Strongly Agree")
- **Valid range:** expected min/max
- **Missing codes:** how missing data is coded
- **N missing:** count and percentage
- **Distribution summary:** mean/SD for continuous, frequencies for categorical
- **Source:** which survey item, database field, or computed from what
- **Notes:** anything unusual

For multi-item scales, also document:
- Which items compose the scale
- Reliability (Cronbach's alpha, McDonald's omega)
- Whether items need reverse-coding

**R approach:** Use `codebook` and/or `codebookr` packages. Supplement with `skimr::skim()` for distributional summaries and `psych::alpha()` / `psych::omega()` for reliability.

**Python approach:** Use `polars` for data profiling, custom codebook generation via `great_tables` for formatted output.

### Step 4 — Generate validation report

**R approach:** Create a `pointblank` agent with validation steps for each criterion. Produce the HTML report.

**Python approach:** Define a `pandera` schema with checks for each criterion. Run validation and capture results.

### Step 5 — Summarize findings

Print a console summary:
- Total observations: N
- Total variables: K
- Completeness rate: X%
- Critical issues found: N (with list)
- Warnings: N
- Codebook generated at: <path>
- Validation report at: <path>

### Step 6 — Next steps

Follow [_shared/next-steps.md](../_shared/next-steps.md). If issues were found, suggest `/data-clean`. If data looks good, suggest `/eda`.

## Voice

Precise and systematic. You report facts, not opinions. "47 participants (9.0%) failed the attention check" — not "a lot of people didn't pay attention." You are the lab technician running diagnostics, not the PI interpreting results.

## Argument handling

- Path to specific file → validate that file
- Path to directory → validate all data files in that directory
- Empty → look in `data/raw/` in the project root
