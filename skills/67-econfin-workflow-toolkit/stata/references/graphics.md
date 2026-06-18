# Graphics in Stata

## Twoway Graphs

### Scatter Plots

```stata
twoway scatter mpg weight

// Marker customization
twoway scatter mpg weight, ///
    msymbol(square) msize(medium) mcolor(blue)
// Symbols: circle, square, triangle, diamond, plus, x, oh, dh, etc.

// Marker labels
twoway scatter mpg weight, ///
    mlabel(make) mlabposition(3) mlabsize(vsmall)
// Position uses clock notation: 12=top, 3=right, 6=bottom, 9=left

// Jitter to reduce overplotting
twoway scatter mpg weight, jitter(5)
```

### Line and Connected Plots

```stata
twoway line mpg weight, sort
twoway connected mpg weight, sort     // Lines + markers
```

### Overlaying Multiple Plot Types

```stata
// Scatter with linear fit and CI
twoway (scatter mpg weight) (lfitci mpg weight)

// Groups with different markers
twoway (scatter mpg weight if foreign==0, msymbol(circle) mcolor(blue)) ///
       (scatter mpg weight if foreign==1, msymbol(triangle) mcolor(red)), ///
       legend(label(1 "Domestic") label(2 "Foreign"))

// Scatter + linear + quadratic fit
twoway (scatter mpg weight) (lfit mpg weight) (qfit mpg weight)
```

### Area and Range Plots

```stata
twoway area mpg weight, sort fcolor(blue%30)

// Shaded confidence interval
twoway (rarea upper lower x, fcolor(gray%20)) (line yhat x)

// Range plots
twoway rcap lower upper x              // With caps
twoway rspike lower upper x            // Spikes
twoway rbar lower upper x              // Bars
```

### Function Plots

```stata
twoway function y=normalden(x), range(-4 4)

twoway (function y=x, range(-5 5)) ///
       (function y=x^2, range(-5 5))
```

---

## Bar and Box Plots

### Graph Bar

```stata
graph bar mpg, over(foreign)
graph hbar mpg, over(foreign)           // Horizontal
graph bar (count) mpg, over(foreign)    // Frequencies
graph bar, over(foreign) percent        // Percentages

// Bar labels and multiple grouping
graph hbar mpg, over(foreign) over(rep78) ///
    blabel(bar, format(%4.1f))

// Custom colors, stacking
graph bar (mean) mpg (mean) price, over(foreign) ///
    stack bar(1, color(navy)) bar(2, color(maroon))

// Sorted bars
graph hbar (mean) mpg, over(make, sort(1) descending)
```

### Graph Box

```stata
graph box mpg, over(foreign)
graph box mpg, over(foreign) noout      // Remove outliers
graph box mpg, over(foreign) over(rep78)

// Customization
graph box mpg, over(foreign) ///
    box(1, fcolor(navy%50)) box(2, fcolor(maroon%50)) ///
    medtype(line) medline(lwidth(thick) lcolor(red))
```

---

## Histograms

```stata
histogram mpg                           // Density (default)
histogram mpg, frequency                // Counts
histogram mpg, fraction                 // Proportions
histogram mpg, percent                  // Percentages
histogram mpg, bin(10) start(10)        // Bin control

// With normal overlay and labels
histogram mpg, frequency bin(15) normal ///
    addlabel fcolor(navy%60) lcolor(navy)

// Discrete variable
histogram rep78, discrete percent addlabel xlabel(1(1)5)

// By group
histogram mpg, by(foreign) frequency bin(10)
```

---

## Graph Options

### Titles and Labels

```stata
twoway scatter mpg weight, ///
    title("Main Title", size(medium)) ///
    subtitle("Subtitle") ///
    note("Note at bottom") ///
    xtitle("Weight (pounds)") ///
    ytitle("Mileage (mpg)")
```

### Axis Options

```stata
twoway scatter mpg weight, ///
    xscale(range(1500 5000)) yscale(range(10 40)) ///
    xlabel(2000(1000)5000, format(%9.0fc)) ///
    ylabel(10(5)40, angle(0))

// Log scale, reverse axis
twoway scatter mpg weight, xscale(log) yscale(reverse)

// Multiple y-axes
twoway (scatter mpg weight, yaxis(1)) ///
       (scatter price weight, yaxis(2))
```

### Legend Options

```stata
// Position: clock notation (0=center inside, 6=bottom outside)
legend(position(6) rows(1))
legend(ring(0) position(5))            // Inside plot at 5 o'clock
legend(label(1 "Domestic") label(2 "Foreign"))
legend(order(2 "Foreign" 1 "Domestic")) // Reorder
legend(off)                             // Remove
legend(title("Origin"))
```

### Graph Region

```stata
graphregion(color(white))               // White background
plotregion(color(gs15) margin(medium))
aspectratio(1)                          // Square plot
xsize(8) ysize(6)                       // Size in inches

// Grid lines
ylabel(, grid gstyle(dot))
xlabel(, grid)
```

---

## Schemes and Styles

```stata
set scheme s2color                      // Default color
set scheme s1mono                       // Black and white
set scheme economist                    // Economist style
set scheme sj                           // Stata Journal
twoway scatter mpg weight, scheme(plotplain)  // Per-graph

// Community schemes
ssc install blindschemes, replace       // plotplain
ssc install schemepack, replace         // white_tableau, gg_hue, etc.
set scheme white_cividis                // Colorblind-friendly
```

### grstyle for Quick Customization

```stata
ssc install grstyle, replace
ssc install palettes, replace
grstyle init
grstyle set plain
grstyle set color hue
grstyle clear                           // Reset
```

### Publication Recommendations

- B&W journals: `s1mono` or `plotplain`
- Color online: `sj` or `plotplain`
- Presentations: `economist` or `white_tableau`
- Colorblind: `white_cividis`

---

## Combining Graphs

```stata
// Create named graphs
twoway scatter mpg weight, name(g1, replace) nodraw
twoway scatter mpg length, name(g2, replace) nodraw

// Combine
graph combine g1 g2, rows(1)           // Side by side
graph combine g1 g2, cols(1)           // Stacked

// Options
graph combine g1 g2, ///
    ycommon xcommon ///                 // Shared axes
    iscale(0.8) ///                     // Scale internal elements
    imargin(medium) ///                 // Margin around each
    title("Combined Figure")

// From saved files
graph save graph1.gph, replace
graph combine graph1.gph graph2.gph

// Different panel sizes
twoway scatter mpg weight, fxsize(66.67) name(left, replace)
graph bar mpg, over(foreign) fxsize(33.33) name(right, replace)
graph combine left right, cols(2)
```

---

## Exporting Graphs

```stata
// Vector formats (scalable, best for publications)
graph export figure.pdf, replace
graph export figure.eps, replace
graph export figure.svg, replace

// Raster formats
graph export figure.png, width(3000) replace   // High-res
graph export figure.png, width(800) replace     // Web

// Save Stata format for editing
graph save figure.gph, replace
```

**Best practices by use case:**
- Word: `.emf` (Windows) or `.png` width(1200)
- LaTeX: `.pdf` or `.eps`
- PowerPoint: `.png` width(1920)
- Web: `.png` width(800) or `.svg`
- Journal: `.eps`, `.tif` width(3000), or `.pdf`

```stata
// Batch export
foreach g in g1 g2 g3 {
    graph export `g'.png, name(`g') width(1200) replace
}
```

---

## Marginsplot

```stata
regress mpg i.foreign weight
margins foreign
marginsplot

// Continuous variable
margins, at(weight=(2000(500)4500))
marginsplot

// Interaction: continuous x categorical
regress mpg c.weight##i.foreign
margins foreign, at(weight=(2000(250)4500))
marginsplot, xdimension(weight) recast(line) recastci(rarea)

// Marginal effects
margins, dydx(weight) at(weight=(2000(500)4500))
marginsplot, yline(0, lpattern(dash))

// Customization
marginsplot, ///
    recast(bar)                         // Bar plot
    recast(line) recastci(rarea)        // Line + shaded CI
    plot1opts(lcolor(navy) lwidth(medthick))
    ci1opts(fcolor(navy%15) lwidth(none))
```

### Combining Marginsplots

```stata
quietly regress mpg weight
margins, at(weight=(2000(500)4500))
marginsplot, name(m1, replace) nodraw

quietly regress mpg c.weight##i.foreign
margins foreign, at(weight=(2000(500)4500))
marginsplot, xdimension(weight) name(m2, replace) nodraw

graph combine m1 m2, ycommon
```

---

## Quick Reference

| Graph Type | Command |
|---|---|
| Scatter | `twoway scatter` |
| Line | `twoway line` |
| Bar chart | `graph bar` / `graph hbar` |
| Box plot | `graph box` / `graph hbox` |
| Histogram | `histogram` |
| Margins | `marginsplot` |

**Key options:** `title()`, `xtitle()`, `ytitle()`, `xlabel()`, `ylabel()`, `legend()`, `scheme()`, `graphregion()`, `plotregion()`

**Combining:** `graph combine g1 g2`, `rows()`, `cols()`, `ycommon`, `xcommon`

**Export:** `graph export file.pdf`, `graph export file.png, width(3000)`, `graph save file.gph`
