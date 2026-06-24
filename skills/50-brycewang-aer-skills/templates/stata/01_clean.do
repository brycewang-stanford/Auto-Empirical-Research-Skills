/*------------------------------------------------------------------
  01_clean.do
  Raw-to-analytic data construction placeholder.

  Replace this file with project-specific cleaning code. The downstream
  template expects data/intermediate/analytic.dta with at least:
  unit_id, year, treat, treat_year, outcome, x1, x2, endog, iv, balanced.
-------------------------------------------------------------------*/

version 18.0

capture confirm file "$intermediate/analytic.dta"
if _rc {
    display as error "Missing $intermediate/analytic.dta."
    display as error "Replace 01_clean.do with project-specific cleaning code,"
    display as error "or create the analytic file before running run_all.do."
    exit 601
}

display as text "Found existing analytic file: $intermediate/analytic.dta"
