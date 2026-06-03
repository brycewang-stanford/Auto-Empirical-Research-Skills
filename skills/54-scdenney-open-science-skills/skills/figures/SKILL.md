---
name: figures
description: Design and format publication-quality figures: chart choice, color, scales, legends, captions, reproducibility.
argument-hint: "[describe the figure you are building, the data, the claim it supports, and the target venue]"
---

# Figure Designer

## Heritage and scope

This is an original Open Science Skills workflow for figure production in social-science manuscripts. It is general — apply to any figure type (line, bar, point, density, map, network, small multiples). For figures whose interpretation depends on method-specific standards, also consult the relevant sibling skill (`conjoint-design`, `conjoint-diagnostics`, `list-experiment`, `topic-modeling`, `text-classification`, `vlm-ocr-pipeline`). For end-stage QA on a finished figure set, hand off to `figure-table-audit`.

A good figure earns its place in the manuscript: it makes a single comparison legible, it can be read without the surrounding text, and it can be regenerated from a script. If a figure cannot do all three, it is not yet ready.

## Instructions

### 1. State the comparison before drawing

Write down, in one sentence, what the figure is supposed to let the reader see. Examples:

- "Treatment effect is larger among low-information respondents than among high-information respondents."
- "Vote share for Party A declines monotonically with district urbanization."
- "Topic 7 prevalence rises sharply after the 2024 election."

If you cannot state the comparison in one sentence, the figure has too many goals — split it into multiple panels or multiple figures.

### 2. Choose the chart type from the comparison

Match the geometry to the comparison, not to the data type:

- **Comparing magnitudes across a small number of categories**: bar chart (or dot/lollipop for many categories).
- **Tracking a quantity over a continuous variable**: line chart for ordered/continuous x; point + ribbon for uncertainty.
- **Showing distribution**: histogram (single), density (compare a few), boxplot/violin (compare many).
- **Showing relationship between two continuous variables**: scatter, with trend line + uncertainty band if a model is implied.
- **Showing effect estimates**: coefficient plot (point + CI), preferred over tables for visual comparison across models.
- **Showing many small comparisons**: small multiples (faceting) on a shared scale, not multiple separate figures.

Avoid pie charts, 3D anything, dual-axis, and donut charts in academic figures.

### 3. Pick scales and axes deliberately

- Always label both axes with the quantity AND the units. "Income" is wrong; "Household income (USD, 2020)" is right.
- For percentages, write `0.00–1.00` or `0%–100%` consistently — do not mix within a figure.
- Use a log scale when the data span more than two orders of magnitude OR when a multiplicative effect is the substantive story; label the scale as log.
- Anchor axes at zero ONLY when the zero is meaningful for the comparison (counts, proportions). For deviations, differences, and z-scores, do not force a zero baseline.
- Use the same y-axis range across panels of small multiples unless the claim is explicitly about within-panel scale.
- Reverse the y-axis only when the substantive direction demands it (e.g., rank where 1 is "best") and label the reversal in the caption.

### 4. Choose color with intent

- **Sequential** (light → dark): for ordered/quantitative variables (income brackets, time, density).
- **Diverging** (red ↔ blue, etc.): for variables with a meaningful midpoint (effect sign, deviation from baseline).
- **Categorical**: for unordered groups; use a colorblind-safe palette (Okabe-Ito, viridis discrete, ColorBrewer Set2/Dark2).
- Test grayscale: convert the figure and check that the comparison still reads. If it does not, add shape, line type, or direct labels.
- Do not encode the same variable in both color and shape unless reinforcing for accessibility — that is fine; just keep the legend honest.
- Default `rainbow` / `jet` ramps are a publication smell; replace them.

### 5. Match legend order to the visual order in the chart

Legends are read alongside the plot, so the legend order must mirror the data's visual order — readers should never have to scan back and forth to decode a series:

- For lines, areas, or stacked elements arranged top-to-bottom in the plot at the rightmost x-value, list legend entries in the same top-to-bottom order.
- For bars or categories arranged left-to-right, use a horizontal legend listed left-to-right in the same order.
- For panels (small multiples), follow the panel grid: rows top-to-bottom, columns left-to-right.
- Do NOT alphabetize the legend when the data have a natural order (time, magnitude, treatment intensity, ordinal scale). Alphabetical legends are a frequent cause of misreading.
- Prefer **direct labeling** at the line end / bar end when there are five or fewer series — a labelled line beats any legend.
- When a legend is unavoidable, place it where it does not occlude data, and match colors and line styles between figure and legend exactly.

The rule of thumb: *the eye should be able to walk from chart to legend in the same direction it reads.* Top-to-bottom on the chart maps to top-to-bottom in a vertical legend, and to left-to-right in a horizontal legend.

### 6. Write a self-contained caption

A reader who skims should be able to understand the figure from the caption alone. Include:

- What is plotted (the dependent quantity, the unit of analysis).
- The sample (N, source, time window).
- The uncertainty interval (e.g., "95% confidence intervals from cluster-robust standard errors").
- Panel meanings, if multi-panel.
- Any transformations or exclusions.
- The estimand or model family if the figure is showing model output (not just "Results").

Keep abbreviations defined and units explicit.

### 7. Make it reproducible

- Generate the figure from a script (R, Python, Stata, Julia) checked into the replication archive — never hand-edit final figures in Illustrator or Inkscape unless the manual step is documented.
- Save with the script: input data path, package versions, random seed (for jittered or sampled plots), output dimensions.
- Export vector (PDF, SVG) for plots with text and lines; export raster (PNG at ≥300 dpi) only for raster-native content (heatmaps with thousands of cells, photographs, maps with imagery).
- Use a single ggplot/matplotlib theme across the manuscript so figures are visually consistent.
- For multi-panel figures, build with `patchwork`/`cowplot`/`gridExtra` or matplotlib's `subplots`/`gridspec` — not by stitching exported PNGs in Word.

### 8. Accessibility and production sanity

- Axis label and tick text ≥ 8pt at print size.
- No reliance on color alone (pair with shape, line type, or direct labels).
- Alt text for journals that require it (a one-sentence description of what the figure shows).
- Consistent figure dimensions and fonts across the manuscript.
- Title text inside the plotting area is usually unnecessary — captions carry the title.

## Output

When asked to design or revise a figure, produce:

```
# Figure Plan

Comparison: <one sentence>
Chart type: <type and why>
Geometry: <axes, scales, faceting>
Color encoding: <palette, what it encodes, accessibility check>
Legend / labeling: <direct label or legend; order matches visual order>
Caption draft: <self-contained>
Reproducibility: <script path, packages, output format and dimensions>
Open issues: <anything that needs author input — denominator choice, sample restriction, etc.>
```

When asked to produce code, default to a single ggplot2 (R) or matplotlib + seaborn (Python) script with the theme, palette, and figure dimensions explicit at the top.

## Quality checks

- [ ] One-sentence comparison was stated before the chart was chosen.
- [ ] Chart geometry matches the comparison.
- [ ] Axes are labeled with quantity AND units.
- [ ] Color encoding is intentional and grayscale-tested.
- [ ] Legend order mirrors the visual order in the chart (no surprise alphabetical sort).
- [ ] Caption is self-contained: quantity, sample, uncertainty, panels, transformations.
- [ ] Figure is generated by a script, not hand-edited.
- [ ] Vector format used unless the content is raster-native.
- [ ] Final QA pass deferred to `figure-table-audit` once the figure set is stable.
