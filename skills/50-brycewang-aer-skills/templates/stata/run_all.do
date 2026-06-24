/*------------------------------------------------------------------
  run_all.do
  Master script — AER-compliant Stata pipeline

  Author      : <your name>
  Paper       : <short title>
  Last update : <YYYY-MM-DD>
  Stata       : 18.0 MP

  Reproducibility contract:
    1. Change directory to the project root and run `do run_all.do`.
    2. `00_globals.do` sets $project to the current working directory.
    3. All output is written to `output/`. No file outside the project
       directory is read or written.

  Approximate runtime: 25 minutes on a 2024-class laptop.
-------------------------------------------------------------------*/

version 18.0
clear all
set more off
set varabbrev off
set linesize 100
cap log close

* ---- 1. Globals & package install --------------------------------
do "00_globals.do"
do "00_install_packages.do"

* ---- 2. Pipeline --------------------------------------------------
log using "$logs/run_all.log", replace text

do "01_clean.do"        // raw -> intermediate analytic file
do "02_descriptives.do" // summary stats + balance tables
do "03_main_did.do"     // main regression specifications
do "04_robustness.do"   // referee-anticipating checks
do "05_heterogeneity.do"
do "06_tables.do"       // emit publication-ready .tex tables
do "07_figures.do"      // emit publication-ready .pdf figures

log close

display as result "================================================="
display as result "  Pipeline complete. Outputs in: $output/"
display as result "================================================="
