/*------------------------------------------------------------------
  00_globals.do
  Project-wide globals. Run from the project root.
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

* ---- Create expected directories ---------------------------------
foreach d in "$data" "$raw" "$intermediate" "$output" "$tables" "$figures" "$logs" "$docs" {
    capture mkdir "`d'"
}

* ---- Model specification -----------------------------------------
* Controls used across the analysis scripts. Edit to match your data;
* the R and Python templates use the same two example covariates.
global controls "x1 x2"

* ---- Reproducibility ---------------------------------------------
set seed 20260101    // fixed seed for any randomization

* ---- House-style display options (table & graph) -----------------
graph set window fontface "Helvetica"
set scheme s2color
