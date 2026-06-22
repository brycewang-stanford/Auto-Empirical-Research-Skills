/*------------------------------------------------------------------
  02_descriptives.do
  Summary-statistics scaffold.
-------------------------------------------------------------------*/

version 18.0

capture confirm file "$intermediate/analytic.dta"
if _rc {
    display as text "Skipping descriptives; analytic file does not exist yet."
    exit
}

use "$intermediate/analytic.dta", clear
summarize
