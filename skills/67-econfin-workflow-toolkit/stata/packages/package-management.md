# Stata Package Management Guide

## Distribution Channels

1. **SSC** (Boston College Archive) - Primary repo, ~3500 packages. Install: `ssc install pkg`
2. **Stata Journal** - Peer-reviewed. Install: `net install pkgname, from(http://www.stata-journal.com/software/sjX-Y)`
3. **GitHub** - Cutting-edge/dev versions. Requires `github` package.
4. **Official Stata** - `update all` for StataCorp updates.

---

## Searching for Packages

```stata
findit "difference in differences"    // Most comprehensive -- searches SSC, SJ, help, FAQs
search matching, all                  // Search local help + remote
net search "instrumental variables"   // Downloadable packages only
ssc describe reghdfe                  // SSC package info
ssc describe estout, all              // Detailed SSC info
```

---

## Installing Packages

### SSC (most common)

```stata
ssc install reghdfe, replace
```

### Net Install

```stata
net from http://www.stata-journal.com/software/sj16-3
net install st0448
```

### GitHub

```stata
* Install github package manager first
net install github, from("https://haghish.github.io/github/")

* Then install packages
github install mcaceresb/stata-gtools
github install mcaceresb/stata-gtools@v1.11.0   // Specific version
github update gtools
```

### Manual

```stata
sysdir             // Find PLUS directory (usually ~/ado/plus/)
* Copy .ado/.sthlp files to ~/ado/plus/[first-letter]/
discard            // Reload after copying
```

### Custom Install Location

```stata
net set ado "~/my_custom_ado"
ssc install estout
net set ado PLUS                     // Reset to default
```

---

## Updating Packages

```stata
ado update                           // Check for updates (dry run)
ado update, update                   // Install all updates
ssc install reghdfe, replace         // Reinstall specific package
update query                         // Check official Stata updates
update all                           // Install official updates
github update _all                   // Update all GitHub packages
```

---

## Package Info and Diagnostics

```stata
which reghdfe                        // Show version and location
ado dir                              // List all installed user packages
adopath                              // Show ado search paths
sysdir                               // Show system directories
ado uninstall packagename            // Remove a package
discard                              // Clear programs from memory
```

---

## Reproducibility: Installation Scripts

```stata
* Auto-install missing packages
local packages reghdfe ftools estout coefplot ivreg2 ranktest

foreach pkg of local packages {
    capture which `pkg'
    if _rc {
        ssc install `pkg', replace
    }
}
```

### Project-Specific Ado Directory (full isolation)

```stata
local projdir "~/projects/my_project"
mkdir "`projdir'/ado/plus"
adopath ++ "`projdir'/ado/plus"
net set ado "`projdir'/ado/plus"

ssc install reghdfe          // Goes to project directory
* net set ado PLUS           // Reset when done
```

### Version Documentation

```stata
log using package_versions.log, replace text
about
which reghdfe
which estout
which ivreg2
ado dir
log close
```

---

## Essential Packages by Category

### Regression and Estimation

| Package | Install | Purpose | Dependencies |
|---------|---------|---------|--------------|
| `reghdfe` | `ssc install reghdfe` | High-dimensional FE regression | `ftools` |
| `ivreg2` | `ssc install ivreg2` | IV/2SLS/GMM | `ranktest` |
| `ivreghdfe` | `ssc install ivreghdfe` | IV + multiple FE | `reghdfe`, `ivreg2` |
| `xtabond2` | `ssc install xtabond2` | Arellano-Bond/Blundell-Bond GMM | -- |
| `ppmlhdfe` | `ssc install ppmlhdfe` | Poisson PML with FE | `ftools` |

### Causal Inference: Difference-in-Differences

| Package | Install | Method |
|---------|---------|--------|
| `did_multiplegt` | `ssc install did_multiplegt` | Multiple groups/periods, Bacon decomp |
| `csdid` | `net install csdid, from("https://friosavila.github.io/playingwithstata/drdid")` | Callaway-Sant'Anna doubly robust DID |
| `drdid` | `ssc install drdid` | Doubly robust DID |
| `did_imputation` | `ssc install did_imputation` | Borusyak et al. imputation |
| `eventstudyinteract` | `ssc install eventstudyinteract` | Sun-Abraham event studies |
| `bacondecomp` | `ssc install bacondecomp` | Bacon decomposition |

### Causal Inference: RD, Matching, SC

| Package | Install | Method |
|---------|---------|--------|
| `rdrobust` | `net install rdrobust, from("https://raw.githubusercontent.com/rdpackages/rdrobust/master/stata")` | Robust RD estimation |
| `rddensity` | `net install rddensity, from("https://raw.githubusercontent.com/rdpackages/rddensity/master/stata")` | Manipulation testing |
| `rdmulti` | `net install rdmulti, from("https://raw.githubusercontent.com/rdpackages/rdmulti/master/stata")` | Multi-cutoff RD |
| `binsreg` | `net install binsreg, from("https://raw.githubusercontent.com/nppackages/binsreg/master/stata")` | Optimal binscatter |
| `psmatch2` | `ssc install psmatch2` | Propensity score matching |
| `cem` | `ssc install cem` | Coarsened exact matching |
| `kmatch` | `ssc install kmatch` | Kernel matching / IPW |
| `ebalance` | `ssc install ebalance` | Entropy balancing |
| `synth` | `ssc install synth` | Synthetic control |
| `synth_runner` | `ssc install synth_runner` | Parallel synth |

### Tables and Output

| Package | Install | Purpose |
|---------|---------|---------|
| `estout` | `ssc install estout` | LaTeX/HTML/Word tables (includes esttab, eststo, estadd) |
| `outreg2` | `ssc install outreg2` | Quick regression tables |
| `asdoc` | `ssc install asdoc` | Auto Word tables |
| `regsave` | `ssc install regsave` | Save estimates as dataset |
| `table1_mc` | `ssc install table1_mc` | Summary "Table 1" |

### Graphics

| Package | Install | Purpose |
|---------|---------|---------|
| `coefplot` | `ssc install coefplot` | Coefficient plots |
| `binscatter` | `ssc install binscatter` | Binned scatterplots |
| `grc1leg` | `ssc install grc1leg` | Combine graphs, shared legend |
| `schemepack` | `ssc install schemepack` | Modern color schemes |
| `blindschemes` | `ssc install blindschemes` | Colorblind-friendly schemes |
| `palettes` | `ssc install palettes` | Color palettes (dep: `colrspace`) |
| `spmap` / `maptile` | `ssc install spmap` | Choropleth maps |
| `heatplot` | `ssc install heatplot` | Heatmaps |

### Panel Data and Time Series

| Package | Install | Purpose |
|---------|---------|---------|
| `xtivreg2` | `ssc install xtivreg2` | Panel IV |
| `xtoverid` | `ssc install xtoverid` | Panel overidentification tests |
| `xtserial` | `ssc install xtserial` | Serial correlation test for FE/RE |
| `xttest3` | `ssc install xttest3` | Heteroskedasticity test for FE |
| `xtcsd` | `ssc install xtcsd` | Cross-sectional dependence test |
| `pvar` | `ssc install pvar` | Panel VAR |

### Machine Learning

| Package | Install | Purpose |
|---------|---------|---------|
| `lassopack` | `ssc install lassopack` | LASSO, ridge, elastic net + CV |
| `rforest` | `ssc install rforest` | Random forest |
| `boost` | `ssc install boost` | Gradient boosting |
| `crossfold` | `ssc install crossfold` | K-fold cross-validation |

### Inference and Testing

| Package | Install | Purpose |
|---------|---------|---------|
| `wyoung` | `ssc install wyoung` | Westfall-Young multiple testing |
| `rwolf` | `ssc install rwolf` | Romano-Wolf step-down |
| `ritest` | `ssc install ritest` | Randomization inference |
| `boottest` | `ssc install boottest` | Wild cluster bootstrap |
| `weakiv` | `ssc install weakiv` | Weak instrument diagnostics |

### Data Manipulation

| Package | Install | Purpose |
|---------|---------|---------|
| `gtools` | `ssc install gtools` | Fast collapse/egen/reshape (dep: `ftools`) |
| `rangestat` | `ssc install rangestat` | Rolling/moving window stats |
| `carryforward` | `ssc install carryforward` | Forward/backward fill |
| `missings` | `ssc install missings` | Missing data utilities |
| `unique` / `distinct` | `ssc install unique` | Uniqueness checks |

---

## Package Families (install dependencies first)

```stata
* reghdfe family
ssc install ftools, replace
ssc install reghdfe, replace
ssc install ivreghdfe, replace
ssc install ppmlhdfe, replace

* IV family
ssc install ranktest, replace
ssc install ivreg2, replace
ssc install xtivreg2, replace
ssc install ivreghdfe, replace
ssc install weakiv, replace

* RD family (all Cattaneo et al.)
net install rdrobust, from("https://raw.githubusercontent.com/rdpackages/rdrobust/master/stata") replace
net install rddensity, from("https://raw.githubusercontent.com/rdpackages/rddensity/master/stata") replace
net install rdmulti, from("https://raw.githubusercontent.com/rdpackages/rdmulti/master/stata") replace
net install rdpower, from("https://raw.githubusercontent.com/rdpackages/rdpower/master/stata") replace

* estout family (single install gets esttab, eststo, estpost, estadd)
ssc install estout, replace

* DID family
ssc install drdid, replace
ssc install csdid, replace
ssc install did_multiplegt, replace
ssc install did_imputation, replace
ssc install eventstudyinteract, replace
ssc install bacondecomp, replace
```

### Common Dependencies

| Dependency | Required by |
|------------|-------------|
| `ftools` | reghdfe, ivreghdfe, ppmlhdfe |
| `ranktest` | ivreg2, xtivreg2 |
| `moremata` | Many packages for Mata operations |
| `colrspace` | palettes |

---

## Troubleshooting

**Command not found after install:**
```stata
discard                              // Clear program memory
which packagename                    // Check location
```

**Download/file errors:**
```stata
ssc install pkg, replace all         // Force full reinstall
net search packagename               // Try alternative source
update all                           // Update Stata itself
```

**Version conflicts:**
```stata
ado uninstall packagename            // Remove old version
ssc install packagename, replace     // Fresh install
```

**Dependency errors -- install deps first:**
```stata
ssc install ftools, replace
ssc install reghdfe, replace         // Now works
```

**GitHub install fails:**
```stata
net install github, from("https://haghish.github.io/github/") replace
* Or manually: download .ado/.sthlp from GitHub, copy to PLUS dir
```

**Permission denied:**
```stata
sysdir set PLUS "~/my_ado_folder"    // Use writable directory
```
