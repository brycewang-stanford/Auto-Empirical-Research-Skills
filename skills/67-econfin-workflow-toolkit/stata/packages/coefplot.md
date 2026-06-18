# Coefplot: Visualizing Regression Coefficients

`coefplot` creates publication-quality coefficient plots with confidence intervals from stored estimation results.

## Installation

```stata
ssc install coefplot, replace

// Recommended companions
ssc install estout
ssc install grstyle
ssc install palettes
ssc install colrspace

// Verify
sysuse auto, clear
regress price mpg weight foreign
coefplot
```

## Basic Coefficient Plots

```stata
// Basic plot from last estimation
regress price mpg weight foreign length
coefplot

// Specify confidence levels
coefplot, levels(90)
coefplot, levels(90 95 99)

// From stored estimates
regress price mpg weight foreign
estimates store model1
coefplot model1, keep(mpg weight)

// With labels and title
coefplot, ///
    title("Determinants of Automobile Price") ///
    xtitle("Coefficient Estimate") ///
    xlabel(, format(%9.0fc))
```

## Plotting Multiple Models

```stata
quietly regress price mpg
estimates store m1
quietly regress price mpg weight
estimates store m2
quietly regress price mpg weight foreign
estimates store m3

// Side-by-side comparison
coefplot m1 m2 m3, drop(_cons)

// With reference line and legend
coefplot (m1) (m2) (m3), drop(_cons) ///
    xline(0, lcolor(red) lpattern(dash)) ///
    legend(order(1 "Model 1" 2 "Model 2" 3 "Model 3"))

// Stacked panels
coefplot (m1, label(Model 1)) ///
         (m2, label(Model 2)) ///
         (m3, label(Model 3)), ///
    drop(_cons) xline(0) byopts(yrescale)
```

## Customization

### Markers and Confidence Intervals

```stata
// Custom markers
coefplot, ///
    msymbol(square) msize(large) mcolor(navy) mfcolor(navy%50)

// Different markers per model
coefplot m1 m2, drop(_cons) ///
    msymbol(O D) mcolor(navy maroon)

// CI appearance
coefplot, ciopts(lwidth(2) lcolor(navy)) levels(95)

// Capped intervals
coefplot, ciopts(recast(rcap) lwidth(medium))

// Multiple CI levels with different styles
coefplot, levels(90 95) ///
    ciopts1(lwidth(thin) lcolor(gs10)) ///
    ciopts2(lwidth(thick) lcolor(navy))
```

### Colors

```stata
// Named colors
coefplot m1 m2 m3, drop(_cons) mcolor(navy maroon forest_green)

// Semi-transparent
coefplot m1 m2 m3, drop(_cons) mcolor(navy%60 maroon%60 forest_green%60)

// Grayscale for print
coefplot m1 m2 m3, drop(_cons) ///
    mcolor(gs2 gs8 gs14) ciopts(lcolor(gs2 gs8 gs14))
```

### Labels

```stata
// Use variable labels
label variable mpg "Fuel Efficiency (MPG)"
coefplot, label

// Rename coefficients inline
coefplot, coeflabels(mpg = "Miles per Gallon" ///
                     weight = "Vehicle Weight" ///
                     foreign = "Foreign Indicator")
```

## Horizontal vs Vertical Plots

```stata
// Horizontal (default) - better for many variables
coefplot, drop(_cons) xline(0)

// Vertical - better for comparing many models
coefplot m1 m2 m3, drop(_cons) vertical yline(0, lcolor(red) lpattern(dash))
```

## Reordering and Grouping

```stata
// Custom order
coefplot, order(foreign mpg weight length) drop(_cons)

// Group headings
coefplot, ///
    headings(mpg = "{bf:Vehicle Characteristics}" ///
             foreign = "{bf:Origin}") ///
    drop(_cons)

// Combined ordering and grouping
coefplot, ///
    headings(mpg = "{bf:Performance}" ///
             foreign = "{bf:Origin & Quality}") ///
    order(mpg weight displacement foreign rep78) ///
    drop(_cons turn)
```

## Omitting and Keeping Variables

```stata
// Drop constant (almost always do this)
coefplot, drop(_cons)

// Drop multiple
coefplot, drop(_cons foreign)

// Drop factor variables with wildcards
regress price i.rep78 mpg weight foreign
coefplot, drop(_cons *.rep78)

// Keep only specific variables
coefplot, keep(mpg weight foreign)

// Keep only interactions
coefplot, keep(*#*)

// Drop factor and interaction terms
coefplot, drop(*.foreign *#*)
```

## Interaction Terms

```stata
// Basic interaction plot
regress price c.mpg##i.foreign weight
coefplot, drop(_cons weight) xline(0)

// Organized with headings
regress price c.mpg##i.foreign c.weight##i.foreign
coefplot, drop(_cons) ///
    headings(mpg = "{bf:Main Effects}" ///
             1.foreign#c.mpg = "{bf:Interactions}") ///
    xline(0)

// Continuous-by-continuous
regress price c.mpg##c.weight foreign
coefplot, ///
    keep(mpg weight *#*) ///
    coeflabels(mpg#c.weight = "MPG x Weight") ///
    xline(0)
```

## Integration with Margins

```stata
// Marginal effects plot
regress price c.mpg##i.foreign weight
margins, dydx(mpg) over(foreign)
coefplot, xline(0) ///
    coeflabels(0.foreign = "Domestic" 1.foreign = "Foreign")

// Average marginal effects from logit
logit foreign price mpg weight
margins, dydx(*)
coefplot, drop(_cons) xline(0) xlabel(, format(%9.3f))

// Marginal effects at representative values
regress price c.mpg##c.weight foreign
margins, dydx(mpg) at(weight=(2000(500)4500))
coefplot, vertical yline(0) ///
    xtitle("Weight (pounds)") ///
    xlabel(1 "2000" 2 "2500" 3 "3000" 4 "3500" 5 "4000" 6 "4500")

// Contrasts
regress price i.rep78 mpg weight
contrast rep78, nowald
estimates store contrasts
coefplot contrasts, xline(0) ///
    coeflabels(2.rep78 = "Fair vs Poor" ///
               3.rep78 = "Average vs Poor" ///
               4.rep78 = "Good vs Poor" ///
               5.rep78 = "Excellent vs Poor")
```

## Publication-Quality Examples

### Single Model, Journal Style

```stata
set scheme plotplain

regress price mpg weight foreign length, robust

coefplot, ///
    drop(_cons) ///
    xline(0, lcolor(black) lpattern(dash)) ///
    msymbol(D) msize(medium) mcolor(black) ///
    ciopts(lwidth(medthick) lcolor(black)) ///
    levels(95) ///
    title("Figure 1. Determinants of Automobile Prices", ///
          size(medium) position(11) justification(left)) ///
    xtitle("Coefficient Estimate (USD)", size(small)) ///
    xlabel(, format(%9.0fc) labsize(small)) ///
    ylabel(, labsize(small) angle(0)) ///
    graphregion(color(white)) ///
    plotregion(margin(medium) lcolor(black) lwidth(thin)) ///
    note("Note: 95% confidence intervals shown. Robust standard errors.", ///
         size(vsmall) span)

graph export "figure1_coefficients.pdf", replace
```

### Model Comparison with eststo

```stata
set scheme plotplain
eststo clear
eststo: quietly regress price mpg, robust
eststo: quietly regress price mpg weight, robust
eststo: quietly regress price mpg weight foreign, robust

coefplot est1 est2 est3, ///
    drop(_cons) ///
    xline(0, lcolor(black) lpattern(dash)) ///
    msymbol(O S D) msize(medium medium medium) ///
    mcolor(gs2 gs6 gs10) ///
    ciopts(lwidth(medium) lcolor(gs2 gs6 gs10)) ///
    legend(order(1 "Model 1" 2 "Model 2" 3 "Model 3") ///
           rows(1) size(small) region(lwidth(none))) ///
    graphregion(color(white))

graph export "figure2_model_comparison.pdf", replace
```

### Vertical with Multiple CI Levels

```stata
set scheme plotplain
regress price mpg weight foreign, robust

coefplot, ///
    drop(_cons) vertical ///
    yline(0, lcolor(black) lpattern(dash)) ///
    levels(90 95 99) ///
    msymbol(D) msize(medium) mcolor(black) ///
    ciopts1(lwidth(thin) lcolor(gs12)) ///
    ciopts2(lwidth(medium) lcolor(gs6)) ///
    ciopts3(lwidth(thick) lcolor(black)) ///
    legend(order(2 "90% CI" 4 "95% CI" 6 "99% CI") ///
           rows(1) position(12) size(vsmall))
```

## Advanced Techniques

### Using graph combine

```stata
// Create named sub-plots with nodraw, then combine
quietly regress price mpg weight foreign
coefplot, drop(_cons) xline(0) title("Full Sample") name(g1, replace)

quietly regress price mpg weight if foreign==0
coefplot, drop(_cons) xline(0) title("Domestic") name(g2, replace)

graph combine g1 g2, rows(1) graphregion(color(white))
```

### Suppress Display During Multi-Plot Construction

```stata
coefplot m1, name(g1, replace) nodraw
coefplot m2, name(g2, replace) nodraw
graph combine g1 g2  // display once
```

### Coefficient Plot + esttab Table

```stata
eststo clear
eststo: quietly regress price mpg weight
eststo: quietly regress price mpg weight foreign

coefplot est1 est2, drop(_cons) xline(0) bylabel

esttab est1 est2 using "table.tex", ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs replace
```

## Quick Reference

| Option | Description |
|--------|-------------|
| `drop(varlist)` | Omit variables from plot |
| `keep(varlist)` | Keep only specified variables |
| `xline(#)` | Add vertical reference line |
| `vertical` | Vertical orientation |
| `levels(#)` | Confidence level (default 95) |
| `msymbol()` | Marker symbol |
| `mcolor()` | Marker color |
| `ciopts()` | Confidence interval options |
| `label` | Use variable labels |
| `coeflabels()` | Custom coefficient labels |
| `order()` | Specify coefficient order |
| `headings()` | Add group headings |
| `bylabel` | Use estimate labels |
| `nodraw` | Suppress display (for `graph combine`) |

### Common Pitfalls

- **Always** `drop(_cons)` -- the constant clutters the plot
- **Always** add `xline(0)` (or `yline(0)` if vertical) for interpretability
- Use `label` or `coeflabels()` -- raw variable names are unclear
- Use grayscale (`gs2`, `gs8`, etc.) for print publications
- Use `keep()` to focus on key variables when there are many coefficients
- Wildcard `*.varname` drops all factor levels; `*#*` drops all interactions

## Resources

- `help coefplot`
- Ben Jann's coefplot page: https://repec.sowi.unibe.ch/stata/coefplot/
- Related: `marginsplot`, `esttab`/`estout`, `grstyle`
