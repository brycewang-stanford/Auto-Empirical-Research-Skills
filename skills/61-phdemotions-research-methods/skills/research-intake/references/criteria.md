# Gap Analysis Rubric — Outward Review

> For each criterion: check existence, completeness, and quality.
> Apply severity from _shared/severity-scale.md.
> Map each gap to the skill that closes it.

---

## 1. Documentation Completeness

### 1.1 Codebook / Data Dictionary
**Gold standard:** Every variable has: full name, description, type (continuous/categorical/ordinal/binary), measurement scale (e.g., "7-point Likert, 1=Strongly Disagree to 7=Strongly Agree"), source (survey item number, database field), missing data coding, and for composites: component items + reliability (alpha/omega).
**Check:** Does it exist? Does it cover ALL variables, not just key ones? Are scale anchors documented? Is reliability reported for multi-item scales?
**Severity if missing:** BLOCKER — reviewers require this; reproducibility impossible without it.
**Skill to close gap:** `/data-validate` (auto-generates codebook)

### 1.2 Decision Log
**Gold standard:** Every subjective analytical choice documented with: what was decided, alternatives considered, rationale, impact on results, pre-registration alignment.
**Check:** Does it exist? Are exclusion criteria documented? Outlier handling? Variable transformation choices? Model specification decisions?
**Severity if missing:** MAJOR — reviewers increasingly expect transparency about analytical decisions.
**Skill to close gap:** `/data-clean` (creates entries for cleaning decisions), `/analyze` (creates entries for analysis decisions)

### 1.3 Pre-Registration
**Gold standard:** Hypotheses, planned analyses, exclusion criteria, sample size justification — registered before data analysis.
**Check:** Does it exist? Is it linked (AsPredicted, OSF)? Does current analysis match? Are deviations documented?
**Severity if missing:** MAJOR for confirmatory studies (increasingly required by top journals). MINOR for purely exploratory work (but should be labeled as such).
**Skill to close gap:** `/research-init` (creates skeleton), `/analyze` (checks alignment)

### 1.4 README
**Gold standard:** Cornell template for research data: project description, data sources, file inventory, variable definitions, methodological information, access conditions, licensing.
**Check:** Does it exist? Does it follow a recognized template? Is the file inventory complete? Could a stranger understand the project from the README alone?
**Severity if missing:** MAJOR — required for OSF/Dataverse deposit and basic discoverability.
**Skill to close gap:** `/research-init` (creates from template), `/reproduce` (finalizes)

### 1.5 IRB / Ethics Documentation
**Gold standard:** Ethics approval number, approving body, approval date, study protocol reference.
**Check:** Is there any ethics documentation? Is the approval number noted somewhere accessible?
**Severity if missing:** BLOCKER for human subjects research. N/A for secondary data with no identifiable information.
**Skill to close gap:** `/research-init` (creates `docs/irb/` with template)

### 1.6 Data Provenance
**Gold standard:** Where did this data come from? When was it collected? By whom? Under what conditions? What is the population? What was the sampling strategy?
**Check:** Is this documented anywhere? In the README? In a separate provenance file?
**Severity if missing:** MAJOR — reviewers need to evaluate generalizability and potential biases.
**Skill to close gap:** `/research-init` (README template includes provenance section)

---

## 2. Data Quality Baseline

### 2.1 Raw / Processed Separation
**Gold standard:** `data/raw/` contains untouched original files (read-only). `data/processed/` contains cleaned versions. Raw is never modified.
**Check:** Is there a clear separation? Or is there one file that's been modified in place? Is raw data in a read-only location?
**Severity if missing:** BLOCKER — raw data modification breaks reproducibility fundamentally.
**Skill to close gap:** `/research-init` (creates directory structure), raw-data-guard hook (enforces)

### 2.2 Data Format
**Gold standard:** Open, non-proprietary formats (CSV, Parquet) for sharing. Proprietary formats (.sav, .dta, .xlsx) acceptable as originals in `data/raw/` but should have open-format copies.
**Check:** What formats are the data files in? Are there open-format versions?
**Severity if missing:** MINOR — proprietary formats are readable but not ideal for FAIR compliance.
**Skill to close gap:** `/data-validate` (can convert and create open-format copies)

### 2.3 Validation Checks
**Gold standard:** Systematic checks for completeness, impossible values, duplicates, range violations, type consistency. Results documented in a validation report.
**Check:** Has any validation been done? Is there a report? Or was the data assumed to be clean?
**Severity if missing:** MAJOR — unvalidated data may contain errors that propagate through all analyses.
**Skill to close gap:** `/data-validate`

### 2.4 Missingness Documentation
**Gold standard:** Missingness patterns visualized and documented. Missing data mechanism assessed (MCAR/MAR/MNAR). Handling strategy chosen and justified in decision log.
**Check:** Is missingness documented? What percentage? Is the mechanism discussed? Is the handling strategy justified?
**Severity if missing:** MAJOR — missing data handling affects all downstream results.
**Skill to close gap:** `/data-validate` (diagnoses missingness), `/data-clean` (implements handling)

### 2.5 Attention / Manipulation Checks
**Gold standard:** For survey/experimental data: attention check items identified, failure rate reported, exclusion criteria pre-specified.
**Check:** Are there attention checks in the data? Have they been evaluated? What's the failure rate?
**Severity if missing:** MAJOR for survey data — reviewers expect this. N/A for secondary/archival data.
**Skill to close gap:** `/data-validate` (identifies checks), `/data-clean` (applies exclusions)

---

## 3. Code Quality Baseline

### 3.1 Pipeline / Workflow
**Gold standard:** One-command reproduction via `targets` (R) or Snakemake/Makefile (Python). All steps from raw data to final output are automated.
**Check:** Is there a pipeline definition? Or are scripts run manually in an ad-hoc order? Are there numbered scripts (01_, 02_) suggesting intended order?
**Severity if missing:** MAJOR — without a pipeline, reproduction requires guesswork about execution order.
**Skill to close gap:** `/research-init` (creates pipeline stub)

### 3.2 Environment Reproducibility
**Gold standard:** `renv.lock` (R) or `uv.lock` (Python) capturing exact package versions. Anyone can recreate the environment.
**Check:** Is there a lockfile? A requirements.txt? A DESCRIPTION file? Or are packages just loaded without version tracking?
**Severity if missing:** MAJOR — "it works on my machine" is not reproducibility.
**Skill to close gap:** `/research-init` (initializes renv/uv)

### 3.3 Variable Naming
**Gold standard:** Domain-appropriate construct names (`brand_authenticity`, `purchase_intention`), not generic (`x1`, `var_a`, `DV`).
**Check:** What naming convention is used? Are names meaningful to someone reading without context?
**Severity if missing:** MINOR — functional but hurts readability and publishability.
**Skill to close gap:** `/data-clean` (renames during cleaning with codebook mapping)

### 3.4 Session Info
**Gold standard:** R `sessionInfo()` or Python `watermark` output capturing package versions, OS, platform, date.
**Check:** Is session info captured anywhere? In the output? In a file?
**Severity if missing:** MINOR — easy to add, but reviewers may request it.
**Skill to close gap:** `/reproduce` (captures at packaging time)

---

## 4. Methodology Baseline

### 4.1 Effect Sizes
**Gold standard:** Effect sizes (Cohen's d, eta-squared, R-squared, etc.) reported alongside every significance test, with confidence intervals.
**Check:** Are effect sizes present in any existing analysis output? Or just p-values?
**Severity if missing:** BLOCKER — APA requires it, top journals reject without it.
**Skill to close gap:** `/analyze` (always includes effect sizes via easystats)

### 4.2 Assumption Testing
**Gold standard:** Every parametric test preceded by appropriate assumption checks (normality, homoscedasticity, linearity, multicollinearity, independence).
**Check:** Is there any evidence of assumption testing? Diagnostic plots? Test statistics?
**Severity if missing:** MAJOR — reviewers will question whether results are valid.
**Skill to close gap:** `/analyze` (runs assumption tests before every model)

### 4.3 Robustness Checks
**Gold standard:** At least one alternative specification for primary findings. Ideally: specification curve or multiverse analysis.
**Check:** Are there any robustness checks? Alternative models? Subsample analyses?
**Severity if missing:** MAJOR for primary findings at top journals. MINOR for exploratory work.
**Skill to close gap:** `/robustness`

### 4.4 Statistical Appropriateness
**Gold standard:** The analytical method matches the research design, data structure, and variable types.
**Check:** Is the method appropriate? (e.g., OLS with a binary outcome should be logistic; nested data without multilevel modeling is misspecified)
**Severity if missing:** BLOCKER — wrong test invalidates results entirely.
**Skill to close gap:** `/method-advisor` (recommends appropriate methods), `/analyze` (implements correctly)
