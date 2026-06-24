/*------------------------------------------------------------------
  00_globals.do
  Project-wide globals. Run from the replication-package root.
  See ../README.md for the full instructions to replicators.
-------------------------------------------------------------------*/

version 18.0

* ---- Project root -------------------------------------------------
global project "`c(pwd)'"

* ---- Derived paths -----------------------------------------------
global data        "$project/data"
global raw         "$data/raw"
global intermediate "$data/intermediate"
global code        "$project/code"
global output      "$project/output"
global tables      "$output/tables"
global figures     "$output/figures"
global logs        "$project/logs"
global docs        "$project/docs"

foreach d in "$data" "$raw" "$intermediate" "$code" "$output" "$tables" "$figures" "$logs" "$docs" {
    capture mkdir "`d'"
}

* ---- Reproducibility ---------------------------------------------
set seed 20260101
