# Exhibit Cookbook: AER Tables and Figures

*Bundled with the `aer-tables-figures` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

Reviewers in economics read tables first. This cookbook gives the complete
anatomy of an AER-style regression table, short export recipes for the three
major stacks, the mandatory table-notes content, figure rules, and the
exhibit-count arithmetic for AER: Insights.

## Booktabs table anatomy

Hard conventions: captions **above** tables (below figures); horizontal rules
only — `\toprule` / `\midrule` / `\bottomrule`, never vertical rules; numbered
columns; a spanning dependent-variable header; standard errors in parentheses
**below** coefficients; per-column N and fit statistic; indicator rows for
what is in each specification.

```latex
\begin{table}[t]
  \centering
  \caption{Effect of Treatment on Log Wages}
  \label{tab:main}
  \begin{tabular}{lccccc}
    \toprule
     & \multicolumn{5}{c}{Dependent variable: log(Wage)} \\
    \cmidrule(lr){2-6}
     & (1) & (2) & (3) & (4) & (5) \\
     & OLS & OLS & OLS & IV  & IV  \\
    \midrule
    Treatment            & 0.123***  & 0.118***  & 0.115***  & 0.142***  & 0.138***  \\
                         & (0.041)   & (0.040)   & (0.039)   & (0.052)   & (0.051)   \\
    \midrule
    Controls             & No        & Yes       & Yes       & Yes       & Yes       \\
    Unit fixed effects   & No        & No        & Yes       & Yes       & Yes       \\
    Year fixed effects   & No        & No        & Yes       & Yes       & Yes       \\
    Sample               & Full      & Full      & Full      & Full      & Balanced  \\
    \midrule
    Observations         & 12,453    & 12,453    & 12,453    & 12,453    & 11,892    \\
    R-squared            & 0.024     & 0.118     & 0.341     & 0.310     & 0.317     \\
    First-stage F        &           &           &           & 42.3      & 41.1      \\
    \bottomrule
  \end{tabular}
  \begin{tablenotes}
    Notes: Each column reports a separate regression of log wages on the
    treatment indicator. Standard errors in parentheses, clustered at the
    unit level (312 clusters). Columns (4)-(5) instrument the endogenous
    regressor with [instrument]. Sample: [definition]. Source: [data source].
    *** $p<0.01$, ** $p<0.05$, * $p<0.1$.
  \end{tablenotes}
\end{table}
```

Column discipline:

- Progress simple to rich: column (1) rawest, later columns add controls, FE,
  IV. The column the referee quotes is (4) or (5).
- Same coefficient row across all columns for visual comparison; 3-7 columns.
- Intuitive labels ("log(Wage)"), never raw dataset variable names.
- Round to 2-3 significant digits of the standard error; match coefficient
  precision to it.
- One star convention paper-wide: `*** p<0.01, ** p<0.05, * p<0.1` (letter
  superscripts acceptable, but never mixed).

## Export recipes

### Stata: esttab (estout)

```stata
eststo clear
eststo col1: reghdfe outcome treat, noabsorb cluster(unit_id)
estadd local ctrl "No"
eststo col2: reghdfe outcome treat $controls, absorb(unit_id year) cluster(unit_id)
estadd local ctrl "Yes"

esttab col1 col2 using "tab_main.tex", replace booktabs ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    keep(treat) coeflabels(treat "Treatment") mtitles("OLS" "OLS") ///
    stats(ctrl N r2, labels("Controls" "Observations" "R-squared") ///
          fmt(%s %12.0fc %5.3f)) ///
    label nonotes ///
    addnotes("Standard errors in parentheses, clustered at the unit level." ///
             "*** \(p<0.01\), ** \(p<0.05\), * \(p<0.1\).")
```

### R: fixest::etable

```r
m1 <- feols(outcome ~ treat,                            data = dt, cluster = ~ unit_id)
m2 <- feols(outcome ~ treat + x1 + x2 | unit_id + year, data = dt, cluster = ~ unit_id)

etable(m1, m2,
  file        = "tab_main.tex", replace = TRUE,
  style.tex   = style.tex("aer"),          # built-in AER booktabs style
  fitstat     = ~ n + r2,
  signif.code = c("***" = 0.01, "**" = 0.05, "*" = 0.10),
  digits      = 3,
  dict        = c(treat = "Treatment"),
  group       = list("Controls" = c("x1", "x2")),
  headers     = c("OLS", "OLS"),
  notes       = c("Standard errors in parentheses, clustered at the unit level.",
                  "*** p<0.01, ** p<0.05, * p<0.10."))
```

### Python: pyfixest.etable

```python
import pyfixest as pf

m1 = pf.feols("outcome ~ treat",                            data=df, vcov={"CRV1": "unit_id"})
m2 = pf.feols("outcome ~ treat + x1 + x2 | unit_id + year", data=df, vcov={"CRV1": "unit_id"})

pf.etable(
    models=[m1, m2], type="tex", file_name="tab_main.tex",
    signif_code=[0.01, 0.05, 0.10], digits=3,
    keep=["treat"], labels={"treat": "Treatment"},
    custom_stats={"Controls": ["No", "Yes"]},
    notes=("Standard errors in parentheses, clustered at the unit level. "
           "*** p<0.01, ** p<0.05, * p<0.10."),
)
```

A modelsummary-style exporter works too; whatever the tool, the output must
land on the anatomy above — booktabs rules, per-column N, SEs below
coefficients.

## Table-notes template

Every table note MUST state, in complete sentences:

1. **Estimator** — OLS, 2SLS, the staggered-DiD estimator by name, etc.
2. **SE type and cluster level** — "clustered at the district level (48
   clusters)", never bare "robust standard errors". With few clusters,
   name the wild-bootstrap correction used.
3. **Stars policy** — the exact thresholds, once, matching every table.
4. **Exact N per column** — in the table body; the note explains any
   variation across columns (e.g. the balanced-panel restriction).
5. **Sample definition** — population, period, and restrictions.
6. **Data source** — named, with vintage if it matters.

Template: *"Notes: Each column reports [estimator] estimates of [equation or
design]. Standard errors in parentheses, clustered at the [level] level ([k]
clusters). Sample: [definition], [period]. Source: [dataset, vintage].
[Stars policy]."*

## Figure rules

- **Vector output only** (PDF or EPS) for production; raster figures are not
  accepted at final submission. Sans-serif axis fonts at 9 pt minimum.
- **Readable at print size**: check labels at the actual column width, not
  full screen. No 3D, no pie charts, no gridline clutter, no default-theme
  chartjunk; every ink element must carry information.
- **Complete-sentence notes** below the figure stating: the estimator that
  produced it, the omitted/reference category, the confidence-interval type
  and coverage, sample restrictions, and N (observations or clusters).
  "Notes: See text." is useless.
- **No color-only encoding** — legible in grayscale and to color-blind
  readers; if color is used, use an accessible palette and vary line type or
  marker too.
- **One claim per figure**; split panels rather than overlay six lines.

### Event-study conventions

For any DiD with multiple periods, plot the event study:

- Point estimates by event time with **CI bands or whiskers (95%)**, the CI
  type named in the note (e.g. multiplier bootstrap for
  Callaway and Sant'Anna (2021) aggregations).
- A **horizontal reference line at zero** and a vertical guide (or gap) at
  the treatment date.
- The **omitted period marked** (conventionally event time -1, shown at zero
  by construction) and stated in the note.
- Pre-period coefficients always shown — they are the design's credibility
  exhibit, not decoration.

## Exhibit count vs. word budget (AER: Insights)

AER: Insights enforces a joint budget: **7,000 words with each exhibit
counting 200 words against it.** Arithmetic:

| Exhibits | Word cost | Words left for prose |
|---|---|---|
| 3 | 600 | 6,400 |
| 5 | 1,000 | 6,000 |
| 7 | 1,400 | 5,600 |
| 10 | 2,000 | 5,000 |

Consequence: every exhibit must displace at least 200 words of explanation to
pay for itself. Consolidate robustness into one table; move everything
secondary to the online appendix. For full-length AER, the analogous
discipline is roughly 5-7 main-text tables — more signals an unfocused
contribution.

## Common exhibit sins

- **Stars-only inference**: magnitudes hidden behind significance stars;
  referees want effect sizes, not asterisks.
- **N missing per column** — or reported once for the "main" sample while
  columns silently differ.
- **"Robust standard errors" without the cluster level** (or the cluster
  count) in the notes.
- **Unreadable axis labels**: fonts that vanish at print size, overlapping
  ticks, unlabeled units.
- Vertical rules, or captions below tables / above figures.
- Mixed star conventions or mixed bracket styles across tables.
- Raw variable names in the stub ("hh_inc_2017" instead of "Household income,
  2017 USD").
- Inconsistent decimal precision across rows of the same table.
- A 14-column main table — readers cannot scan it; split or consolidate.
- Event-study plots that truncate the pre-period or omit the reference-period
  marker.

## Canonical repo sources

These require the repository checkout:

- `skills/aer-tables-figures/SKILL.md` — the routing skill this file deepens
  (canonical five tables, pre-submission checklist)
- `templates/stata/06_tables.do` — full esttab pipeline the Stata snippet
  abridges
- `templates/r/06_tables.R` — full fixest::etable pipeline the R snippet
  abridges
- `templates/python/tables.py` — full pyfixest.etable pipeline the Python
  snippet abridges
- `templates/stata/07_figures.do` — figure export scaffold
