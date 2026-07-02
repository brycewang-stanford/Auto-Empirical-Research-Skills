---
name: aer-tables-figures
description: Use when constructing or revising regression tables, descriptive statistics tables, or figures after results are estimated and before submission for an AER, AER:Insights, or AEJ manuscript. Implements AER booktabs house style, regression-table layout, and figure-note conventions.
---

# AER Tables and Figures

## Overview

Reviewers in economics read tables first. A misformatted, overstuffed, or note-bloated table signals carelessness and increases desk rejection probability independently of the result quality. This skill enforces AER house style and the "one claim per exhibit" discipline.

Hard AER conventions:

- **Captions go below figures, above tables.**
- **Tables use booktabs-style horizontal rules** (no vertical rules).
- **Figure notes use the `tablenotes` / `figurenotes` environment.**
- **No color-only encoding** — figures must remain legible in grayscale and to color-blind readers.

## When to Use

- Drafting the main results table
- Auditing tables before submission
- An R&R demands consolidation or restructuring of tables
- Figures look noisy, dense, or "Excel-default"

## The Five Canonical Tables

Every empirical AER paper has approximately:

1. **Summary statistics** — N, mean, SD, min, max for the analysis sample. One table; ≤ 15 rows. Group by treatment/control if relevant.
2. **Variable definitions** — source, construction, units. Push to appendix if main paper is tight on space.
3. **Balance / first stage** — covariate balance (RCT, RD, matched DiD) or first-stage coefficients (IV).
4. **Main result** — 3-7 columns, each a progressively richer specification. The column the referee will quote is column (4) or (5).
5. **Robustness / heterogeneity** — one table consolidating the most important checks.

If your paper needs more than ~7 main-text tables, the contribution is unfocused. Move secondary tables to the appendix.

## Main Results Table Layout

Standard AER regression table:

```
                         (1)         (2)         (3)         (4)         (5)
                         OLS         OLS         OLS         IV          IV

Treatment              0.123***    0.118***    0.115***    0.142***    0.138***
                      (0.041)     (0.040)     (0.039)     (0.052)     (0.051)

Controls              No          Yes         Yes         Yes         Yes
Unit FE               No          No          Yes         Yes         Yes
Year FE               No          No          Yes         Yes         Yes
Sample                Full        Full        Full        Full        Balanced

Observations          12,453      12,453      12,453      12,453      11,892
R-squared             0.024       0.118       0.341       0.310       0.317
First-stage F                                              42.3        41.1

Notes: Standard errors in parentheses, clustered at the [unit] level. *** p<0.01, ** p<0.05, * p<0.1.
```

### Column Discipline

- **Progress from simple to rich.** Column 1 is the rawest specification; later columns add controls / FE / IV.
- **Same point estimate row across all columns.** Easy visual comparison.
- **Indicator rows for what's in the spec** — Controls / FE / Sample — rather than burying that information in notes.
- **Report observations and R² (or pseudo-R², or first-stage F) for every column.**

### Significance Stars

AER convention: `*** p<0.01, ** p<0.05, * p<0.1`. Some authors and Angrist-Pischke prefer letter superscripts (`a`, `b`, `c`) to save space. Either is acceptable; the journal does not enforce a single convention. **Do not** mix.

### Standard Errors

- Report standard errors in parentheses **below** coefficients, not next to them.
- State the clustering or HAC structure in the **note**, not in the column header.
- For few clusters (< 50), report wild cluster bootstrap p-values.
- For weak-IV settings, report **AR confidence intervals** alongside or instead of conventional SEs.

### Coefficient Rows

- Order coefficients by importance — treatment first, then mechanism interactions, then controls (or omit controls from main table; report in appendix).
- Use intuitive variable labels, not raw variable names. "log(Wage)" beats "lnwage".
- Round to **2-3 significant digits** of the standard error; coefficient precision should match.

## Tool Recipes

### Stata

- **`estout` / `esttab`** — the canonical AER pipeline. `esttab using table.tex, b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) booktabs alignment(D{.}{.}{-1}) ...`
- **`outreg2`** — older, still common
- **`coefplot`** — for figure-based coefficient presentation

### R

- **`fixest::etable`** — produces near-AER tables out of the box; supports `\textsf{...}` styling and `booktabs`
- **`modelsummary`** — flexible, supports gt/kable/LaTeX backends; explicit options for AER conventions
- **`stargazer`** — older; works but less customizable

### Python

- **`stargazer-py`** or **`pystata`** — for users mirroring Stata output

## Figures

### Hierarchy

1. **Coefficient plots** > regression tables when the audience needs to compare 8+ specifications visually. Use `coefplot` (Stata) or `ggplot2 + geom_pointrange` (R).
2. **Event-study plots** for any DiD with multiple periods. Always show pre-period.
3. **Binned scatter / RD plots** for RDD designs. Use `rdplot` (Stata/R).
4. **Maps** for spatially heterogeneous treatments.

### Format Rules

- **Vector format** (PDF, EPS) for production. AER does not accept raster figures for final submission.
- **Sans-serif fonts** (Helvetica, Arial) at minimum 9 pt for axis labels.
- **No 3D plots.** No pie charts.
- **Color sparingly** and accessibly — viridis / cividis palettes; avoid red-green.
- **One main claim per figure.** Split panels rather than overlay six lines.

### Figure Notes

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=0.8\textwidth]{fig_event_study.pdf}
  \caption{Event-Study Estimates of the Effect of Policy on Outcome}
  \label{fig:event}
  \begin{figurenotes}
    Notes: This figure plots Callaway-Sant'Anna ATT(g,t) estimates aggregated by event time.
    The omitted period is $t = -1$. Bars show 95\% confidence intervals based on the
    multiplier bootstrap. Sample restricted to [...]. N = [...].
  \end{figurenotes}
\end{figure}
```

### What Notes Must Include

1. What estimator / method produced the figure
2. The omitted/reference category
3. Confidence interval type and coverage
4. Sample restrictions
5. N (observations or clusters)

## Anti-Patterns

- 14-column main results table — readers cannot scan
- Standard errors in brackets and parentheses in the same paper
- Coefficient magnitudes hidden behind significance stars; magnitudes are what referees want
- "Notes: See text." in the figure caption — useless to a reader skimming
- Figures rendered in PowerPoint Auto-format colors
- Inconsistent decimal precision across rows
- Variable names from the dataset showing in the table ("hh_inc_2017" instead of "Household Income, 2017 USD")

## Pre-Submission Checklist

- [ ] All tables use booktabs rules; no vertical bars
- [ ] All captions positioned correctly (above for tables, below for figures)
- [ ] Significance star convention consistent across all tables
- [ ] Every table note states the SE structure, sample, and N
- [ ] Every figure has a notes block specifying method, CI, sample, N
- [ ] Figures are vector format and legible in grayscale
- [ ] No table exceeds page width or wraps awkwardly
- [ ] Coefficient row order is consistent across tables

## Repository Resources

When working from the AER-skills repository or plugin bundle, load only the relevant table/figure scaffold:

- Stata: `templates/stata/06_tables.do`
- R: `templates/r/06_tables.R`
- Python: `templates/python/tables.py`

## Handoff

```text
MAIN TABLES: <count>
APPENDIX TABLES: <count>
FIGURES: <count>
STYLE COMPLIANT: <yes / list of remaining fixes>
NEXT SKILL: <aer-consistency | aer-replication>
```
