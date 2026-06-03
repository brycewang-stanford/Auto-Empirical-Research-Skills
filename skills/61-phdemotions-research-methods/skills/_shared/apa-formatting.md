# APA 7th Edition Formatting Standards

> Default formatting for all skills. Journal-specific overrides below.

## Statistical Reporting

### General rules
- Report exact p-values to three decimal places: p = .015 (not p < .05)
- Exception: if p < .001, report as p < .001
- Always report effect sizes alongside significance tests
- Always report confidence intervals (95% unless otherwise justified)
- Use italics for statistical symbols: *F*, *t*, *r*, *p*, *M*, *SD*, *n*, *N*
- Report degrees of freedom in parentheses: *F*(2, 147) = 4.32

### Common test formats

**t-test:**
*t*(147) = 2.45, *p* = .015, *d* = 0.41, 95% CI [0.08, 0.74]

**ANOVA:**
*F*(2, 147) = 4.32, *p* = .015, partial eta-squared = .06, 90% CI [.01, .12]

**Regression coefficient:**
*b* = 0.34, *SE* = 0.08, *t*(145) = 4.25, *p* < .001, 95% CI [0.18, 0.50]

**Correlation:**
*r*(148) = .42, *p* < .001, 95% CI [.28, .54]

**Chi-square:**
chi-square(2, *N* = 150) = 8.45, *p* = .015, Cramer's *V* = .24

**SEM fit indices:**
chi-square(24) = 32.45, *p* = .116, CFI = .98, TLI = .97, RMSEA = .04, 90% CI [.00, .07], SRMR = .03

**Indirect effect (mediation):**
*b* = 0.12, *SE* = 0.04, 95% bootstrap CI [0.05, 0.21]

### Effect size guidelines (for context, not rigid cutoffs)

| Effect size | Small | Medium | Large |
|-------------|-------|--------|-------|
| Cohen's *d* | 0.20 | 0.50 | 0.80 |
| *r* | .10 | .30 | .50 |
| Partial eta-squared | .01 | .06 | .14 |
| *f*-squared | .02 | .15 | .35 |
| Cohen's *w* | .10 | .30 | .50 |

Note: These are Cohen's (1988) conventions. Field-specific norms may differ. In consumer behavior, d = 0.30 may be practically meaningful.

## Table Standards

- Table title: brief, informative, in italics, above the table
- Table number: "Table 1" in bold, on its own line above the title
- Column headers: centered, with clear labels (not variable names)
- Notes below table: "Note." in italics, then general notes, then specific notes (superscripts)
- Decimal alignment for numeric columns
- Two decimal places for most statistics, three for p-values
- Horizontal rules: top, below header, bottom only (no vertical rules)

## Figure Standards

- Figure number: "Figure 1" in bold, below the figure
- Figure title: brief, informative, in italics, below the number
- Axis labels: clear, with units where applicable
- Error bars: labeled (SE, 95% CI, or SD) in figure note
- Colorblind-safe palette (viridis, or high-contrast grayscale)
- Resolution: 300 DPI minimum for print
- White/clean background (no gridlines unless data-dense)
- Font: sans-serif, 10-12pt minimum

## Journal-Specific Overrides

### JCR (Journal of Consumer Research)
- Chicago style citations (author-date)
- Figures: grayscale preferred for print, color for online
- Maximum figure width: 5.5 inches (single column) or 7.5 inches (full width)

### JMR (Journal of Marketing Research)
- APA citations
- Supplementary materials in online appendix
- Structured abstract

### JCP (Journal of Consumer Psychology)
- APA citations
- Brief reports vs. full articles have different limits
- Emphasis on effect sizes and practical significance

### Management Science
- Own citation style (author-year, specific format)
- Tables in LaTeX preferred
- Emphasis on robustness checks

### AMJ (Academy of Management Journal)
- APA citations
- Theory-testing emphasis
- Extensive robustness section expected

### ASQ (Administrative Science Quarterly)
- Chicago citations
- Qualitative and quantitative standards
- Emphasis on theoretical contribution
