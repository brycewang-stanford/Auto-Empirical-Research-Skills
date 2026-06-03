# AEA replication deposit structure

Prepare the deposit as an openICPSR-ready `replication-package/` that the AEA
Data Editor can run on a clean machine.

## Required files

- `README.md`: the replicator-facing instructions, not a collaborator memo.
- `run_all.do`: the single master script that reproduces every result, table,
  and figure end to end.
- `LICENSE`: code license and separate notes for any data license.
- `data/raw/`, `data/intermediate/`, and `data/codebook/`: original files,
  constructed analysis files, and variable/source documentation.
- `code/00_setup.do`, `code/01_clean.do`, `code/02_analysis.do`,
  `code/03_tables.do`, and `code/04_figures.do`.
- `output/tables/`, `output/figures/`, `logs/`, and
  `docs/computing_environment.txt`.

## README sections

The README must include a data availability statement for every dataset:
source, citation, URL or agency, date accessed, license or terms of access, and
whether the file is included in the public deposit. For restricted or
proprietary data, document the exact access process, preserve the code, and
explain why the raw data cannot be redistributed.

It also needs a program map that links every published table and figure to the
Stata script and output file that creates it. Include literal instructions:
install dependencies, set the project root, then run `do run_all.do`.

## Reproducibility discipline

Use relative paths only. Put `version 18.0` at the top of every do-file, record
all Stata package versions, and set seed before any random or bootstrap step.
Save logs from the clean run and include the software environment, OS, expected
runtime, and memory requirements.

Before upload, run the package from a fresh checkout. Confirm that `run_all.do`
finishes without errors and that the generated tables and figures match the
accepted manuscript. Upload the visible file tree to openICPSR so the AEA Data
Editor can perform the computational reproducibility check.
