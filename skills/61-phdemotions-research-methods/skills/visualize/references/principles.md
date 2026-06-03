# Publication Figure Principles

## 1. The figure must stand alone

A reader should understand the key message of a figure without reading the surrounding text. Clear axis labels, informative titles, labeled error bars, and self-contained legends make this possible. If you have to read three paragraphs to understand what a figure shows, the figure has failed.

## 2. Data ink ratio matters

Every pixel should serve the data. Remove gridlines unless the data is dense and precise reading is needed. Remove background colors. Remove decorative elements. Remove redundant encoding (don't use both color AND shape AND line style for the same variable unless necessary for accessibility).

## 3. Colorblind-safe is non-negotiable

Approximately 8% of men have some form of color vision deficiency. Use viridis, cividis, or carefully selected high-contrast palettes. Never rely on red-green distinction alone. When in doubt, check with a colorblind simulator. Grayscale should also be distinguishable for print.

## 4. Error representation is a choice — make it explicit

Error bars can represent standard errors, standard deviations, or confidence intervals. Each tells a different story. 95% CIs are the default in this suite because they correspond to the statistical tests. Always label what the error bars represent in the figure note.

## 5. Dimensions and resolution are journal-specific

A figure designed for a single-column layout (typically 3.3" or 84mm) will be unreadable if it contains a complex interaction plot. Match the figure complexity to the available space. Default to single-column (5.5") for simple figures and full-width (7.5") for complex ones. 300 DPI minimum for raster formats; use vector (PDF, SVG) when possible.

## 6. Consistency across figures

All figures in a manuscript should use the same theme, font, color palette, and style conventions. Set the theme once and apply it everywhere. If Figure 1 uses viridis and Figure 3 uses Set1, the manuscript looks sloppy.

## 7. Human-readable labels, always

Never put `brand_auth_composite` on an axis. Use "Brand Authenticity" or whatever the construct is called in the manuscript. The codebook maps variable names to human labels — use it.

## 8. Interaction plots need the right structure

For moderation: plot the DV (y-axis) by the IV (x-axis), with separate lines for moderator levels (typically -1 SD, mean, +1 SD). Include error bars or bands. For categorical moderators, use the actual group labels. Never plot a "simple slopes" figure with only two points connected by a line — use the full range of the IV.
