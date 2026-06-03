# Publication Figure Checklist

> Every figure must pass every applicable check before export.

---

## 1. Universal Requirements (All Figures)

### 1.1 Theme and style
- [ ] White background, no gridlines (unless data-dense)
- [ ] Black axis lines and tick marks
- [ ] Sans-serif font, 10-12pt minimum for all text elements
- [ ] Consistent theme across all manuscript figures
- [ ] No default ggplot2/matplotlib gray background

### 1.2 Labels
- [ ] Human-readable axis labels (from codebook, not variable names)
- [ ] Axis labels include units where applicable
- [ ] Legend labels are clear and descriptive
- [ ] No overlapping text (use `ggrepel` or manual positioning)

### 1.3 Color
- [ ] Colorblind-safe palette (viridis, cividis, or verified custom)
- [ ] Distinguishable in grayscale (for print)
- [ ] High contrast between elements
- [ ] Color used meaningfully (not decoratively)

### 1.4 Error representation
- [ ] Error bars/bands represent 95% CIs (default) or clearly labeled alternative
- [ ] Error representation stated in figure note
- [ ] Error bars visible and not obscured by data points

### 1.5 Export
- [ ] PDF (vector) for journal submission
- [ ] PNG at 300 DPI for manuscript draft
- [ ] SVG for web/editing
- [ ] TIFF if journal requires it
- [ ] Dimensions match journal requirements (single-column: ~5.5", full-width: ~7.5")
- [ ] 600 DPI for line art (path diagrams, flow charts)

---

## 2. Interaction Plots (Moderation)

### 2.1 Structure
- [ ] Y-axis: DV with clear label
- [ ] X-axis: IV (continuous range or categorical levels)
- [ ] Separate lines/colors for moderator levels (-1 SD, mean, +1 SD for continuous; group labels for categorical)
- [ ] Lines span the meaningful range of the IV

### 2.2 Error representation
- [ ] 95% CI bands around each line (preferred) or error bars at key points
- [ ] Bands semi-transparent to show overlap

### 2.3 Annotations
- [ ] Legend clearly identifies moderator levels
- [ ] Simple slope significance noted if applicable
- [ ] Figure note states: "Error bands represent 95% confidence intervals. Moderator plotted at ±1 SD from the mean."

**R packages:** `interactions::interact_plot()`, `ggplot2` manual

---

## 3. Path Diagrams (Mediation / SEM)

### 3.1 Structure
- [ ] Rectangles for observed variables, ovals/circles for latent variables
- [ ] Single-headed arrows for directional paths
- [ ] Double-headed arrows for correlations/covariances
- [ ] Clear left-to-right or top-to-bottom flow

### 3.2 Annotations
- [ ] Standardized coefficients on each path
- [ ] Significance stars (* p < .05, ** p < .01, *** p < .001)
- [ ] R² inside endogenous variable boxes
- [ ] Indirect effect noted below the diagram
- [ ] Fit indices in figure note (for SEM)

### 3.3 Layout
- [ ] Clean, uncluttered — not the default semPlot output
- [ ] Sufficient spacing between elements
- [ ] Covariates de-emphasized (smaller, to the side) if many

**R packages:** `semPlot`, `tidySEM`, `DiagrammeR`, manual `ggplot2`

---

## 4. Forest Plots (Meta-Analysis)

### 4.1 Structure
- [ ] Study labels on left
- [ ] Effect sizes with 95% CIs as horizontal lines + point estimates
- [ ] Diamond for overall effect at bottom
- [ ] Vertical reference line at null (0 for SMD, 1 for OR)
- [ ] Weight (marker size) proportional to precision

### 4.2 Annotations
- [ ] Effect size and CI values on right margin
- [ ] Heterogeneity statistics (I², Q, tau²) in figure note
- [ ] Subgroup labels if subgroup analysis

**R packages:** `metafor::forest()`, `ggplot2` manual

---

## 5. Marginal Effects / Predicted Values

### 5.1 Structure
- [ ] Y-axis: predicted value of DV
- [ ] X-axis: focal predictor
- [ ] CI bands around predicted values
- [ ] Rug plot or histogram of observed values on x-axis (optional but informative)

### 5.2 For mixed models
- [ ] Population-level (marginal) predictions, not conditional on random effects
- [ ] State whether predictions are at mean of other predictors or marginalized

**R packages:** `ggeffects::ggpredict()`, `marginaleffects::plot_predictions()`

---

## 6. Johnson-Neyman Plots

### 6.1 Structure
- [ ] X-axis: moderator values
- [ ] Y-axis: conditional effect of IV on DV (slope ± CI)
- [ ] Horizontal reference line at zero
- [ ] Shaded region where effect is significant
- [ ] Vertical line(s) at transition point(s)

### 6.2 Annotations
- [ ] Transition point value labeled
- [ ] Percentage of sample in each region
- [ ] Figure note explains interpretation

**R packages:** `interactions::johnson_neyman()`, manual `ggplot2`

---

## 7. Coefficient Plots

### 7.1 Structure
- [ ] Predictor names on y-axis (human-readable)
- [ ] Point estimates with 95% CI whiskers on x-axis
- [ ] Vertical reference line at zero
- [ ] Ordered by effect size or theoretical grouping

### 7.2 Multiple models
- [ ] Different colors/shapes for different model specifications
- [ ] Clear legend identifying each model

**R packages:** `modelsummary::modelplot()`, `ggplot2` manual, `dotwhisker`

---

## 8. Correlation Heatmaps

### 8.1 Structure
- [ ] Lower triangle only (no redundancy)
- [ ] Color intensity maps to correlation magnitude
- [ ] Colorblind-safe diverging palette (blue-white-red or viridis)
- [ ] Diagonal shows variable names or reliability

### 8.2 Annotations
- [ ] Correlation values in cells
- [ ] Significance stars
- [ ] Means and SDs in margin if Table 1 format

**R packages:** `ggcorrplot`, `corrplot`, manual `ggplot2` with `geom_tile`
