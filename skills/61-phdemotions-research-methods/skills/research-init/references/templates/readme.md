# {{PROJECT_NAME}}

> Adapted from the [Cornell README template for research data](https://data.research.cornell.edu/data-management/sharing/readme/) (CC0 1.0)

## General Information

**Title of project:**

**Principal investigator:** <name, institution, email>

**Co-investigators:** <names, institutions>

**Date of data collection:** <YYYY-MM to YYYY-MM>

**Geographic location of data collection:** <if applicable>

**Funding sources:** <grant numbers if applicable>

---

## Data & File Overview

**File inventory:**

| File | Location | Description | Format |
|------|----------|-------------|--------|
| <filename> | `data/raw/` | <brief description> | CSV |

**Relationship between files:** <how the files relate, e.g., "survey_data.csv contains responses; codebook.html describes all variables">

---

## Methodological Information

**Description of methods used for data collection:**

**Instruments used:** <surveys, scales, equipment>

**Sampling strategy:**

**Sample size:** N =

**Quality assurance procedures:**

---

## Data-Specific Information

**Variable documentation:** See `data/codebook/codebook.html`

**Missing data codes:** <e.g., NA = not applicable, -99 = missing, blank = not collected>

**Specialized formats or abbreviations:**

---

## Sharing & Access Information

**Licenses:**
- Code: MIT License
- Data: CC-BY 4.0

**Links to publications using this data:**

**Recommended citation:** See `CITATION.cff`

**Links to other publicly accessible locations of the data:**

---

## Reproducibility

**Pipeline:** Run `tar_make()` (R) or `snakemake` (Python) to reproduce all results from raw data.

**Environment:**
- R: `renv::restore()` to install exact package versions from `renv.lock`
- Python: `uv sync` to install exact package versions from `uv.lock`

**Pre-registration:** <link to AsPredicted/OSF registration>

**Decision log:** See `docs/decisions/` for documentation of all analytical choices.

---

*Last updated: {{DATE}}*
