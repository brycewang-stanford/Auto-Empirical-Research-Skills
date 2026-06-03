# Scaffolding Principles

## 1. Structure enables reproducibility

The directory structure IS the reproducibility strategy. When `data/raw/` exists, people know not to modify it. When `docs/decisions/` exists, people know to document choices. When `_targets.R` exists, people know there's a pipeline. The structure teaches the conventions by its shape.

## 2. Sensible defaults, easy overrides

Every template should work out of the box. A researcher who scaffolds a project and immediately runs `tar_make()` should get no errors (just nothing to do yet). Defaults are APA 7th, seed 42, tidyverse style — all overridable but chosen because they're the most common in business research.

## 3. Both languages from day one

Unless the researcher explicitly says R-only or Python-only, scaffold both. Many research projects benefit from R's statistical ecosystem and Python's data processing power. The cost of including both stubs is nearly zero; the cost of adding one later is real.

## 4. Git from the start

Every research project should be version-controlled from the first file. This is non-negotiable for reproducibility and collaboration. The `.gitignore` must be correct from the start — no data in git, no secrets, no IDE files.

## 5. Data never in git

Raw data files go in `data/raw/` but are gitignored. They're shared via OSF, Dataverse, or institutional storage. Code in git, data in a repository with DOI. This separation is fundamental to research data management.

## 6. Templates over empty files

An empty `docs/decisions/TEMPLATE.md` is infinitely more useful than an empty `docs/decisions/` directory. The template shows the researcher exactly what information to capture. Same for the codebook template, pre-registration skeleton, and README.

## 7. Pipeline from minute zero

Even if the researcher won't use the full pipeline immediately, having `_targets.R` or `Snakefile` present normalizes its existence. When they're ready to automate, the infrastructure is already there. The stub should be commented and educational.

## 8. Existing work is preserved, not replaced

When wrapping existing data, the original files are copied (not moved) to `data/raw/`. Original paths are documented. Existing analysis scripts are noted and referenced. Nothing the researcher already has is discarded.
