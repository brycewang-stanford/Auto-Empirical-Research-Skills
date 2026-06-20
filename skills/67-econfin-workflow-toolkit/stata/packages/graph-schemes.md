# Graph Schemes: Professional Visualization Design

## Table of Contents
- [Installation and Setup](#installation-and-setup)
- [grstyle: Dynamic Graph Styling](#grstyle-dynamic-graph-styling)
- [schemepack: Professional Scheme Collection](#schemepack-professional-scheme-collection)
- [blindschemes: Colorblind-Friendly Palettes](#blindschemes-colorblind-friendly-palettes)
- [Activating Schemes](#activating-schemes)
- [Color Palette Selection](#color-palette-selection)
- [Font and Size Customization](#font-and-size-customization)
- [Creating Custom Schemes](#creating-custom-schemes)
- [Publication Requirements](#publication-requirements)
- [Quick Reference](#quick-reference)

---

## Installation and Setup

### Install All Major Packages

```stata
ssc install grstyle, replace
ssc install palettes, replace
ssc install colrspace, replace
ssc install schemepack, replace
ssc install blindschemes, replace
```

### Built-in Stata Schemes

```stata
graph query, schemes       // View all available schemes

set scheme s2color         // Default colored scheme
set scheme s1mono          // Monochrome scheme
set scheme s1color         // Alternative color scheme
```

### Setting Default Scheme

```stata
set scheme plotplain              // Current session only
set scheme plotplain, permanently // Persists across sessions

query graphics                    // Check current scheme
```

### Profile Setup

Create a `profile.do` to set preferences automatically:
- Windows: `C:\Users\[username]\ado\profile.do`
- Mac: `~/Library/Application Support/Stata/ado/profile.do`
- Linux: `~/.stata/ado/profile.do`

```stata
// Contents of profile.do:
set scheme plotplain, permanently
```

### Workspace Setup (Top of Do-File)

```stata
clear all
set more off
set scheme plotplain

grstyle clear
grstyle init
grstyle set plain, box
grstyle set color tableau
```

---

## grstyle: Dynamic Graph Styling

On-the-fly customization without creating permanent scheme files. Requires `palettes` and `colrspace` as dependencies.

### Basic Usage

```stata
grstyle init          // Must run first
grstyle set plain     // Clean graph style

scatter price mpg     // Uses new style
```

### Color Palettes

```stata
grstyle set color tableau             // Tableau palette
grstyle set color viridis             // Colorblind-friendly
grstyle set color Set1                // ColorBrewer
grstyle set color tol bright          // Paul Tol palettes
grstyle set color tol muted
grstyle set color okabe               // Okabe & Ito

// RGB values
grstyle set color "0 114 178" "213 94 0" "0 158 115"

// Named colors
grstyle set color navy maroon forest_green
```

### Symbols, Lines, Grids

```stata
grstyle set symbol O D T S            // Marker symbols
grstyle set lpattern solid dash dot   // Line patterns
grstyle set linewidth thin medium thick

grstyle set plain, box                // White bg with box
grstyle set grid, horizontal          // Horizontal gridlines
grstyle set nogrid                    // Remove grids
```

### Font Sizes

```stata
grstyle set size 11pt                 // Overall
grstyle set size axis_title: 12pt     // Specific elements
grstyle set size tick_label: 10pt
grstyle set size title: 14pt
```

### Comprehensive Setup

```stata
grstyle clear
grstyle init
grstyle set plain, box horizontal
grstyle set color tableau
grstyle set symbol
grstyle set lpattern
grstyle set linewidth thin medium thick
grstyle set size 11pt
```

### Resetting

```stata
grstyle clear           // Clear all grstyle settings
set scheme s2color      // Return to default
```

---

## schemepack: Professional Scheme Collection

### Available Schemes

| Scheme | Style |
|--------|-------|
| `538` | FiveThirtyEight (gray bg, bold, vibrant colors) |
| `economist` | The Economist (light blue bg, serif fonts) |
| `tableau` | Tableau Software (white bg, blue/orange/red/teal) |
| `gg_s2color` | ggplot2-inspired (gray panel bg, white gridlines) |
| `gg_hue` | ggplot2 hue-based |
| `gg_gray` | ggplot2 grayscale |
| `tufte` | Edward Tufte (extreme minimalism, high data-ink ratio) |
| `burd` | Minimalist |
| `cblind1` | Colorblind-friendly (8 colors) |
| `virdis` | Viridis color scheme |

### Usage

```stata
set scheme 538
scatter price mpg, title("FiveThirtyEight Style")

set scheme economist
scatter price mpg, title("Economist Style")

set scheme tableau
scatter price mpg, title("Tableau Style")

set scheme tufte
scatter price mpg, title("Tufte Minimalist")
```

---

## blindschemes: Colorblind-Friendly Palettes

Installed via `ssc install blindschemes`. Includes:

| Scheme | Description |
|--------|-------------|
| `plotplain` | Minimalist (white bg, black lines, no gridlines) |
| `plotplainblind` | plotplain + Okabe & Ito colorblind-safe colors |
| `plottig` | Tufte-inspired + colorblind colors |
| `plottigblind` | Enhanced colorblind version |
| `tab1`, `tab2`, `tab3` | Tableau-inspired colorblind variants |

### plotplain for Publications

```stata
set scheme plotplain

scatter price mpg, ///
    title("Automobile Prices and Fuel Efficiency") ///
    ytitle("Price (USD)") xtitle("Miles per Gallon")
```

### Colorblind-Safe Multi-Series

```stata
set scheme plotplainblind

twoway (scatter price mpg if rep78<=2, msymbol(O)) ///
       (scatter price mpg if rep78==3, msymbol(D)) ///
       (scatter price mpg if rep78>=4, msymbol(T)), ///
    legend(order(1 "Poor" 2 "Average" 3 "Good"))
```

### Extra Accessibility: Color + Patterns

```stata
set scheme plotplainblind

graph bar (mean) price, over(rep78) ///
    asyvars showyvars legend(off) blabel(group)
```

---

## Activating Schemes

### Three Levels of Scope

```stata
// 1. Permanent (persists across sessions)
set scheme plotplain, permanently

// 2. Session-level (all graphs in session)
set scheme plotplain

// 3. Graph-specific (single graph only)
scatter price mpg, scheme(economist)
histogram mpg  // Uses session default, not economist
```

### grstyle Scope

```stata
// grstyle is global within session until cleared
grstyle init
grstyle set color tableau    // Affects all graphs

grstyle clear                // Returns to base scheme
```

### Comparing Schemes Side-by-Side

```stata
local schemes "plotplain 538 economist tableau"
local i = 1
foreach scheme of local schemes {
    set scheme `scheme'
    scatter price mpg, title("`scheme'") name(g`i', replace)
    local i = `i' + 1
}
graph combine g1 g2 g3 g4, cols(2)
```

---

## Color Palette Selection

### colorpalette Command

```stata
colorpalette tableau           // Display palette visually
colorpalette tableau, nograph  // Get colors programmatically
local colors `r(p)'
```

### Palette Types

```stata
// Sequential (continuous data): Blues, Reds, viridis
// Diverging (data with midpoint): RdBu, PiYG
// Qualitative (categories): Set1, Paired, tableau, okabe
```

### Colorblind-Safe Palettes

```stata
colorpalette tol bright     // Paul Tol
colorpalette okabe          // Okabe & Ito
colorpalette Set2           // ColorBrewer (many are safe)
colorpalette Dark2
```

### Manual Color Specification

```stata
// RGB values in Stata
twoway (scatter price mpg if foreign==0, mcolor("0 114 178")) ///
       (scatter price mpg if foreign==1, mcolor("213 94 0"))

// Named locals for readability
local blue "0 114 178"
local orange "213 94 0"
scatter price mpg, mcolor("`blue'")
```

### Grayscale

```stata
grstyle set color gs2 gs6 gs10 gs14

// Or manually
twoway (scatter price mpg if rep78<=2, mcolor(gs2) msymbol(O)) ///
       (scatter price mpg if rep78==3, mcolor(gs8) msymbol(D)) ///
       (scatter price mpg if rep78>=4, mcolor(gs14) msymbol(T))
```

### Dynamic Palette from Data

```stata
levelsof rep78, local(levels)
local n : word count `levels'
colorpalette viridis, n(`n') nograph
local colors `r(p)'

local i = 1
local plots ""
foreach lev of local levels {
    local color : word `i' of `colors'
    local plots `plots' (scatter price mpg if rep78==`lev', mcolor("`color'"))
    local i = `i' + 1
}
twoway `plots', legend(order(1 "Poor" 2 "Fair" 3 "Average" 4 "Good" 5 "Excellent"))
```

---

## Font and Size Customization

### Presentation vs Publication Sizes

```stata
// Publication (journal article)
grstyle clear
grstyle init
grstyle set size 9pt
grstyle set size title: 11pt
grstyle set size axis_title: 10pt

// Presentation (slides)
grstyle clear
grstyle init
grstyle set size 14pt
grstyle set size title: 18pt
grstyle set size axis_title: 16pt
```

### Size Hierarchy in a Single Graph

```stata
scatter price mpg, ///
    title("Main Title", size(large) color(black)) ///
    subtitle("Context", size(medium) color(gs4)) ///
    ytitle("Y-Axis", size(medsmall)) ///
    xtitle("X-Axis", size(medsmall)) ///
    ylabel(, labsize(small)) ///
    xlabel(, labsize(small)) ///
    note("Source info", size(vsmall) color(gs8))
```

### Legend Customization

```stata
twoway (scatter price mpg if foreign==0) ///
       (scatter price mpg if foreign==1), ///
    legend(order(1 "Domestic" 2 "Foreign") ///
           size(small) region(lwidth(thin)) ///
           position(6) rows(1))
```

---

## Creating Custom Schemes

### Method 1: Scheme File

Scheme files are `.scheme` text files in `~/ado/plus/s/`. They inherit from existing schemes:

```
#include s2color

// Background
color background white
color plotregion white

// Lines
color p1line "0 82 155"
color p2line "232 119 34"
color p3line "0 150 136"
linewidth p medthick

// Markers
symbol p1 O
symbol p2 D
symbol p3 T
color p1markfill "0 82 155"
color p2markfill "232 119 34"

// Text sizes
gsize heading medlarge
gsize axis_title medsmall
gsize tick_label small

// Grid
color grid gs12
linestyle grid dot
linewidth grid thin
```

```stata
// Install: place myscheme.scheme in ado/plus/s/
graph query, schemes   // Verify it appears
set scheme myscheme
```

### Method 2: grstyle-Generated Scheme

```stata
grstyle clear
grstyle init myscheme, replace
grstyle set plain, box
grstyle set color navy maroon forest_green
grstyle set symbol O D T
grstyle set lpattern solid dash dot

// Creates myscheme.scheme file
set scheme myscheme
```

### Project Template (Reusable Do-File)

```stata
// graph_setup.do
program define setup_project_graphs
    grstyle clear
    set scheme plotplain
    grstyle init
    grstyle set color "0 75 135" "242 101 34" "0 128 128"
    grstyle set plain, box horizontal
    grstyle set symbol O D T S
    grstyle set size 10pt
    grstyle set size axis_title: 11pt
    grstyle set size title: 12pt
end

// In analysis do-files:
do graph_setup.do
setup_project_graphs
```

---

## Publication Requirements

### Journal-Style Figure

```stata
set scheme plotplain

scatter price mpg, ///
    title("Figure 1. Price and Fuel Efficiency", ///
          position(11) justification(left) size(medium)) ///
    ytitle("Price (USD)", size(small)) ///
    xtitle("Miles per Gallon", size(small)) ///
    ylabel(, labsize(vsmall) angle(0)) ///
    xlabel(, labsize(vsmall)) ///
    graphregion(color(white) margin(medium)) ///
    plotregion(lcolor(black) margin(zero)) ///
    note("Notes: Sample of 74 automobiles from 1978.", ///
         size(vsmall) span)

graph export "figure1.pdf", replace
```

### Multi-Panel Figure

```stata
set scheme plotplain

scatter price mpg, title("Panel A.", position(11) size(medsmall)) ///
    name(panelA, replace) nodraw

histogram price, title("Panel B.", position(11) size(medsmall)) ///
    name(panelB, replace) nodraw

graph combine panelA panelB, cols(2) ///
    title("Figure 2.", position(11) size(medium)) ///
    graphregion(color(white)) ///
    note("Notes: 1978 automobile data (N=74).", size(vsmall) span)

graph export "figure2.pdf", replace
```

### Export Formats

```stata
graph export "figure.pdf", replace                // PDF vector (best for LaTeX)
graph export "figure.eps", replace fontface(Times) // EPS vector
graph export "figure.png", width(3000) replace     // PNG at ~300 DPI
```

### Size Specifications

```stata
// Full page width (6.5 inches typical)
scatter price mpg, xsize(6.5) ysize(4) graphregion(color(white))

// Two-column format (3.25 inches typical)
scatter price mpg, xsize(3.25) ysize(3) graphregion(color(white))
```

### Common Journal Styles

```stata
// NBER Working Paper
set scheme plotplain
grstyle init
grstyle set color navy maroon forest_green
grstyle set size 10pt

// Econometrica (very minimal)
set scheme plotplain
grstyle init
grstyle set plain
grstyle set size 9pt

// PLOS (colorblind-safe required)
set scheme plotplain
grstyle init
grstyle set color "0 114 178" "213 94 0" "0 158 115"
```

### Grayscale for Print

```stata
set scheme plotplain
grstyle init
grstyle set color gs2 gs6 gs10 gs14
grstyle set lpattern solid dash dot dash_dot
```

---

## Quick Reference

### Common Schemes

| Scheme | Best For |
|--------|----------|
| `plotplain` | Academic publications |
| `plotplainblind` | Accessible publications |
| `538` | Presentations, blogs |
| `economist` | Professional reports |
| `tableau` | Business presentations |
| `gg_s2color` | R users, modern look |
| `tufte` | Extreme minimalism |
| `s1mono` | Grayscale printing |
| `tab1`/`tab2`/`tab3` | Accessible charts |

### Quick Setup Templates

```stata
// Academic Paper
set scheme plotplain
grstyle init
grstyle set plain, box
grstyle set color navy maroon forest_green
grstyle set size 10pt

// Presentation
set scheme 538
grstyle init
grstyle set size 14pt

// Colorblind-Safe
set scheme plotplainblind
grstyle init
grstyle set plain, box horizontal

// Grayscale
set scheme s1mono
grstyle init
grstyle set color gs2 gs6 gs10 gs14
```

### Troubleshooting

```stata
// Scheme not found
graph query, schemes       // List available
ssc install schemepack     // Install package
findfile xyz.scheme        // Check file exists

// grstyle not taking effect
grstyle clear              // Clear first
grstyle init               // Then reinitialize
grstyle set color tableau

// Export looks different
graph export "fig.pdf", replace           // Use vector format
graph export "fig.png", width(3000) replace // Or high-res raster

// Scheme reverts on restart
set scheme plotplain, permanently
```

### Preserving and Restoring

```stata
local savedscheme "`c(scheme)'"
set scheme economist
scatter price mpg
set scheme `savedscheme'
```

### Cleanup at End of Do-File

```stata
grstyle clear
graph drop _all
set scheme s2color  // Return to default
```
