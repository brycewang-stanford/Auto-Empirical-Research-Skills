# Data Cleaning Principles

## 1. Raw data is sacred

This is non-negotiable principle #1 of the entire suite. Cleaning code reads from `data/raw/` and writes to `data/processed/`. The raw data is never modified, overwritten, or deleted. If someone deletes `data/processed/` and re-runs the pipeline, they get identical cleaned data from the untouched originals.

## 2. Every transformation is logged

Not just the final result — every step along the way. "Started with N=523. Applied attention check filter: removed 47. N=476. Applied age filter (>18): removed 3. N=473." This is the CONSORT flow principle applied to all data cleaning, not just clinical trials.

## 3. Every subjective choice is documented

What counts as an outlier? What do you do with missing data? How do you handle participants who failed one attention check but not others? These are analytical decisions, not technical operations. Each gets a decision log entry with: what was decided, alternatives considered, rationale, and pre-registration alignment.

## 4. Pre-registration drives exclusions (when available)

If the researcher pre-registered exclusion criteria, those are the default. Deviations are documented and justified. If there's no pre-registration, exclusion criteria should be established before looking at results — and documented in the decision log as if they were pre-registered.

## 5. Cleaning is separate from analysis

Cleaning makes the data ready for analysis. It does NOT make analytical decisions like which model to fit, which covariates to include, or which subgroups to focus on. Those are for `/analyze`. If a cleaning decision seems to depend on the results (e.g., "remove outliers that weaken the effect"), that's a red flag — document it carefully and note it as a researcher degree of freedom.

## 6. Report reliability BEFORE composites

Before averaging items into a composite score, report internal consistency. If alpha < .60, the composite may not be defensible. This information belongs in the codebook and in the manuscript's measures section. Use omega (McDonald's) in addition to alpha — it's more robust to violations of tau-equivalence.

## 7. Name things meaningfully

The cleaned dataset should use construct names, not survey item numbers. `brand_authenticity` not `Q14_1`. `purchase_intention` not `DV`. Prefix transformed variables: `z_brand_auth` (standardized), `log_income` (log-transformed), `c_age` (centered). This mapping is documented in the codebook.

## 8. Verify the cleaned data

After cleaning, run a quick validation: does the cleaned data pass all expected checks? Are there no remaining impossible values? Are all composites within their theoretical range? Is the final N what was expected? A cleaning script that produces bad data defeats the purpose.
