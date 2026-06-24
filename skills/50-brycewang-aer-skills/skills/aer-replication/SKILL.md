---
name: aer-replication
description: Use when assembling the AEA Data and Code Availability deposit for an AER, AER:Insights, or AEJ acceptance, writing the README, or auditing a replication package before the AEA Data Editor review. Implements the current AEA policy, including the February 2026 Data and Code Availability Policy.
---

# AER Replication

## Overview

Prior to acceptance, every empirical, simulation, or experimental paper submitted to an AEA journal must provide data, code, and a complete README sufficient for an independent researcher to reproduce every reported result. The AEA Data Editor's Office now performs a **computational reproducibility check** before final acceptance, and a failed check delays publication by weeks or months.

This skill produces an AEA-compliant deposit on the first try.

## When to Use

- A conditional acceptance arrived and the deposit deadline is set
- Drafting the README at any point in the project (recommended: from day one)
- An AEA Data Editor report flagged the deposit
- Preparing a deposit for openICPSR

## Current AEA Data and Code Availability Policy (February 2026)

Three pillars:

1. **Data deposit** — all data the paper uses, or full provenance documentation for data that cannot be public
2. **Code deposit** — all code that produces every reported number, table, and figure
3. **README** — a single document instructing a replicator on how to run everything

Materials must be deposited in an **openly accessible trusted repository**. The strongly encouraged repository is the **AEA Data and Code Repository at openICPSR**, which gives the Data Editor automatic access to draft deposits.

### Forms and Statements

The current policy centers on the **Data and Code Availability Statement** embedded in the README, plus any forms the editorial office sends during the revision stage (for example, confirming whether a private copy of restricted data can be shared with the Data Editor for verification). Exact form titles change between policy revisions, so:

- Build the README Data Availability Statement to the AEA template (see below).
- Complete whatever forms the editorial office provides at the revision stage — do not invent substitute forms or assume titles carried over from an older policy cycle.

## Repository Structure

```text
replication-package/
├── README.pdf                       (required for final AEA deposit)
├── README.md                        (optional editable source)
├── LICENSE                         (commonly MIT or CC-BY for code; data per source license)
├── data/
│   ├── raw/                        (original files as obtained, never modified)
│   ├── intermediate/               (cleaned analytic datasets)
│   └── codebook/
│       └── source-register.md      (source inventory, crosswalk, derived files)
├── code/
│   ├── 00_setup.do                 (or .R, .py)
│   ├── 01_clean.do
│   ├── 02_analysis.do
│   ├── 03_tables.do
│   └── 04_figures.do
├── output/
│   ├── tables/
│   └── figures/
└── docs/
    ├── exhibit-register.md
    ├── data_appendix.pdf
    └── computing_environment.txt
```

## README Required Sections

The AEA Data Editor's office publishes a template and requires a README
document in PDF format in the uppermost directory of the replication package.
Keep `README.md` as editable source if useful, but render `README.pdf` for the
final deposit. Required sections:

### 1. Overview

One paragraph: what the package does, what paper it accompanies, what software is required.

### 2. Data Availability and Provenance Statement

For **every** dataset used, state:

- Source (with URL or institution)
- Citation
- License or terms of access
- Date accessed
- Whether the data is included in the deposit, and if not, why not

If data cannot be deposited (proprietary, restricted, IRB), the author must:

1. Commit to preserving data and code for ≥ 5 years
2. Commit to assisting reasonable replication requests
3. Make the **code** publicly available
4. Document the data source thoroughly enough for an independent researcher to obtain it

### 3. Dataset List

A table of every file in `data/`, with columns: Filename | Description | Source | Notes.
Keep `data/codebook/source-register.md` synchronized with this section so every
raw source, derived file, access restriction, and analytic variable has one
auditable home.

### 4. Computational Requirements

Operating system, software version, packages, estimated runtime, peak memory. Example:

```
Software: Stata 18.0 MP, R 4.4.1
Stata packages: reghdfe (6.12), ftools (2.49), did (1.3.1), rdrobust (9.2)
R packages: fixest (0.12.1), did (2.1.2), modelsummary (2.1.1)
Hardware: standard laptop (8 GB RAM); full run completes in ~25 minutes.
```

### 5. Description of Programs / Code

What each script does and the order to run them. State the master script (e.g., `run_all.do`).

### 6. Instructions to Replicators

A literal step-by-step:

```
1. Download this archive and unzip to a working directory.
2. Open Stata 18; install dependencies via `setup/install_packages.do`.
3. Edit line 12 of `00_setup.do` to point to the working directory.
4. Run `do run_all.do`. Total runtime: ~25 minutes.
5. All tables and figures are written to `output/`.
```

### 7. List of Tables and Programs

A second table mapping each exhibit in the published paper to the script that produces it:

| Table/Figure | Script              | Line in Script | Output File             |
|--------------|---------------------|----------------|--------------------------|
| Table 1      | 03_tables.do        | 12             | output/tables/tab1.tex   |
| Table 2      | 03_tables.do        | 67             | output/tables/tab2.tex   |
| Figure 1     | 04_figures.do       | 8              | output/figures/fig1.pdf  |

For a fuller audit, keep `docs/exhibit-register.md` synchronized with this
README table. The register should also record the supported claim, exact sample
size, estimator or statistic, table/figure note, and accessibility evidence.

## Coding Discipline for Reproducibility

Adopt from day one. Retrofitting is expensive.

### General

- **One master script** that runs the entire pipeline end-to-end
- **Relative paths only** — `data/raw/foo.csv`, never `/Users/yourname/...`
- **Set the random seed** explicitly in any stochastic procedure
- **Document package versions**: in Stata, install from a setup script and
  record `which` / `ado describe` output; vendor an `ado/` snapshot if exact
  SSC versions are required. In R, use `renv` or `groundhog`; in Python, use
  `requirements.txt` with exact versions
- **Log files** for every run, saved to `logs/`

### Stata

- `version 18.0` at the top of every do-file
- `set seed` before any randomization
- Keep display tweaks such as `set more off` in the master script, not hidden inside analysis scripts
- Use `reghdfe` over `xtreg, fe` for performance and clarity
- Comment heavily — Julian Reif's Stata Coding Guide is a reasonable standard

### R

- `set.seed()` at the top of every analysis script
- `renv::snapshot()` to lock the package environment
- Avoid loading data with `read.csv` and writing with `write.csv` — explicit `data.table::fread` / `fwrite` with column types

### Python

- `requirements.txt` with `==` pins
- `numpy.random.default_rng(seed=...)` for new-style RNG
- Jupyter notebooks acceptable only if accompanied by an equivalent `.py` script

## AEA Data Editor — What They Actually Check

1. **Does the README exist and follow the template?**
2. **Does the master script run end-to-end without errors?**
3. **Do the produced numbers match the published paper?**
4. **Are all data sources documented with provenance?**
5. **Is the data deposit complete, or properly justified if restricted?**

If yes to all: **Approved**, paper proceeds to publication.
If no: **Revisions required**, with a public report.

Common failure modes flagged in published Data Editor reports:

- Hardcoded absolute paths
- Missing package versions
- Master script that errors on a clean machine
- Tables in the deposit that differ from the published version
- Restricted-data papers with no provenance documentation
- README that says "see paper" instead of explaining the steps

## openICPSR Workflow

1. Create deposit on https://www.openicpsr.org/openicpsr/aea
2. Upload files so the data and code are unzipped inside the repository; avoid one opaque top-level ZIP except for rare repository-approved exceptions
3. Fill metadata: citation, abstract, keywords, geographic coverage, time period
4. Submit; the AEA Data Editor's office reviews
5. Address feedback in the deposit and resubmit
6. Approval triggers DOI assignment and publication

## Restricted Data Special Cases

If data is restricted:

- Provide **access instructions** in the README — exact dataset name, agency, application process, approximate cost, expected turnaround
- Provide **code that would run** if the data were available
- Provide **sample synthetic data** with the same schema if possible, so the code can be smoke-tested
- Consider depositing intermediate aggregates (cell-suppressed counts) that allow partial replication

## Repository Resources

When working from the AER-skills repository or plugin bundle, load only the relevant resource:

- Deposit skeleton: `examples/replication-package-skeleton/`
- Data source register template: `examples/replication-package-skeleton/data/codebook/source-register.md`
- Exhibit register template: `examples/replication-package-skeleton/docs/exhibit-register.md`
- Language template: `templates/stata/`, `templates/r/`, or `templates/python/`
- Classic replication examples and repository links: `examples/aer-exemplars.md`

## Pre-Deposit Checklist

- [ ] Master script runs from clean state on a different machine
- [ ] All paths are relative
- [ ] Random seeds set
- [ ] All software and package versions documented
- [ ] README follows AEA template
- [ ] Every published table and figure mapped to its producing script
- [ ] Data Availability statement covers every dataset
- [ ] Data/code files are visible in the repository, not hidden behind one opaque ZIP
- [ ] Required AEA data/code forms are complete or ready for the editorial office
- [ ] Repository structure matches standard layout
- [ ] License files present

## Handoff

```text
DEPOSIT TYPE: <public-data | restricted-data | hybrid>
README STATUS: <complete | incomplete>
REPRODUCIBILITY CHECK: <self-tested clean / not yet>
RESTRICTED DATA HANDLING: <n/a | provenance documented>
NEXT SKILL: aer-submission
```

## Anti-Patterns

- Waiting until acceptance to start the deposit
- Treating the README as documentation for collaborators, not for an unknown replicator
- Depositing the JEL appendix tables but not the regressions that produced them
- "All code available from the authors upon request" — does not satisfy the policy
- Uploading one giant ZIP whose contents the repository cannot display
- A deposit that runs only with packages from 2018 — pin versions but use current stable releases
