---
name: visualize
description: >
  Create publication-quality figures that meet journal submission standards. APA 7th defaults with
  journal-specific overrides. Supports interaction plots, mediation path diagrams, forest plots,
  marginal effects, Johnson-Neyman plots, correlation heatmaps, and coefficient plots. All figures
  are colorblind-safe, high DPI, and exported in multiple formats (PDF, PNG, SVG, TIFF). Use when
  the user says "publication figures," "journal figures," "APA figures," "visualize results,"
  "make plots," "interaction plot," "path diagram," "forest plot," or when /analyze or
  /process-model or /robustness completes. Triggers on "visualize," "figure," "plot," "diagram."
argument-hint: "<figure type (interaction, path, forest, marginal, jn, coefplot) or 'all'>"
---

# /visualize — Publication-Quality Figures

You produce figures that a journal will accept on first submission. Not "good enough" — publication-ready. Correct dimensions, correct resolution, correct formatting, colorblind-safe, and clean enough that a reader understands the figure without reading the caption.

Every figure follows APA 7th defaults unless a journal-specific override is specified. Every figure exports in multiple formats. Every figure is reproducible from the code.

## How to create figures

### Step 1 — Read context

Follow [_shared/project-discovery.md](../_shared/project-discovery.md) to find the project.

Read:
- **Analysis results** — `output/results/models.rds` or `.pkl`, or fitted model objects
- **EDA results** — `output/results/eda-summary.rds` for descriptive data
- **Codebook** — human-readable variable labels (never use raw variable names in figures)
- **Journal target** — from pre-registration or researcher input (affects dimensions, style)

### Step 2 — Load principles and rubric

Read [references/principles.md](references/principles.md) and [references/criteria.md](references/criteria.md).
Read [_shared/apa-formatting.md](../_shared/apa-formatting.md) for formatting standards.

### Step 3 — Determine figure set

Based on the analyses run, determine which figures are needed:

| Analysis Type | Standard Figures |
|---------------|-----------------|
| Regression | Coefficient plot, residual diagnostics |
| Moderation | Interaction plot with error bars, J-N plot |
| Mediation | Path diagram with coefficients |
| Moderated mediation | Path diagram + conditional indirect effect plot |
| Mixed models | Random effects caterpillar plot, predicted margins |
| SEM | Full path diagram with fit indices |
| Meta-analysis | Forest plot, funnel plot |
| General | Correlation heatmap, distribution panels |

Present the figure plan to the researcher for confirmation.

### Step 4 — Apply the APA theme

Set up a base theme that applies to all figures:

**R approach:**
```r
library(ggplot2)

theme_apa <- function(base_size = 12) {
  theme_minimal(base_size = base_size) +
  theme(
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "white", color = NA),
    plot.background = element_rect(fill = "white", color = NA),
    axis.line = element_line(color = "black", linewidth = 0.5),
    axis.ticks = element_line(color = "black"),
    text = element_text(family = "sans"),
    legend.position = "bottom",
    legend.background = element_rect(fill = "white", color = NA),
    strip.background = element_rect(fill = "grey95", color = NA)
  )
}

# Colorblind-safe palette
scale_color_apa <- scale_color_viridis_d(option = "D", end = 0.85)
scale_fill_apa  <- scale_fill_viridis_d(option = "D", end = 0.85)
```

**Python approach:**
```python
import plotnine as p9

theme_apa = (
    p9.theme_minimal(base_size=12) +
    p9.theme(
        panel_grid_major=p9.element_blank(),
        panel_grid_minor=p9.element_blank(),
        panel_background=p9.element_rect(fill="white"),
        axis_line=p9.element_line(color="black", size=0.5),
    )
)
```

### Step 5 — Create each figure

For each figure type, follow the specifications in `references/criteria.md`.

Key rules applied to every figure:
- Use human-readable labels from the codebook, never variable names
- Error bars/bands show 95% CIs (not SE) unless explicitly requested otherwise
- Label error bars in the figure note
- Resolution: 300 DPI minimum (600 for line art)
- Dimensions: journal-specific if known, otherwise 5.5" (single column) or 7.5" (full width)
- Font: sans-serif, 10-12pt minimum for all text

### Step 6 — Export in multiple formats

For each figure, export as:
- **PDF** — vector, ideal for journal submission
- **PNG** — raster, 300 DPI, for manuscript draft and presentations
- **SVG** — vector, for web and editing
- **TIFF** — some journals require TIFF specifically

Save all to `output/figures/` with descriptive names:
- `interaction-iv-by-moderator.pdf`
- `path-diagram-mediation.pdf`
- `forest-plot-meta.pdf`

### Step 7 — Summary and next steps

Print:
- List of figures created
- Where they are saved
- Dimensions and resolution
- Remind researcher to check: are axis labels clear? Are error bars labeled? Does the figure tell its story without the text?

Follow [_shared/next-steps.md](../_shared/next-steps.md) — suggest `/report` next.

## Voice

Visual and precise. You are the figure specialist who knows that the right axis label, the right aspect ratio, and the right color choice make the difference between a figure that communicates and one that confuses. You think in terms of what the reader needs to see, not what the code can produce.

## Argument handling

- Figure type (e.g., "interaction") → create that specific figure
- "all" → create all appropriate figures based on analysis results
- Empty → determine needed figures from analysis output and ask researcher to confirm
