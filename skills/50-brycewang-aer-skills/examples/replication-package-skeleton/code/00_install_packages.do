/*------------------------------------------------------------------
  00_install_packages.do
  Install user-written Stata packages if missing and report locations.

  Record exact versions in README.md after a clean setup run. For strict
  replication, preserve an ado/plus snapshot alongside this package.
-------------------------------------------------------------------*/

version 18.0

local packages reghdfe ftools csdid estout coefplot rdrobust rddensity

foreach pkg of local packages {
    capture which `pkg'
    if _rc {
        display as text "Installing `pkg' from SSC..."
        ssc install `pkg'
    }
    which `pkg'
}
