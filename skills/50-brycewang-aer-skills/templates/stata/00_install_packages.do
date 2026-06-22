/*------------------------------------------------------------------
  00_install_packages.do
  Install user-written packages if missing, then record their locations.

  SSC packages are not exactly version-pinned by `ssc install`. For final
  replication, record package versions in the README and preserve an ado/plus
  snapshot if exact package reproduction is required.
-------------------------------------------------------------------*/

version 18.0

local ssc_packages ///
    reghdfe ftools ivreg2 ranktest weakivtest ///
    csdid drdid did_imputation did_multiplegt eventstudyinteract ///
    bacondecomp honestdid rdrobust rddensity synth synth2 ///
    estout coefplot binscatter asdoc boottest

foreach pkg of local ssc_packages {
    capture which `pkg'
    if _rc {
        display as text "Installing `pkg' from SSC..."
        ssc install `pkg'
    }
    which `pkg'
}

capture which scul
if _rc {
    net install scul, from("https://raw.githubusercontent.com/hollina/scul/master/")
}
which scul

display as result "All required user-written Stata packages are available."
