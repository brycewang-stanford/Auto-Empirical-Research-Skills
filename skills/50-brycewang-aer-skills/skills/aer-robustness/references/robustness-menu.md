# Robustness Menu

*Bundled with the `aer-robustness` skill so the playbook works without the repository checkout. SKILL.md routes; this file carries the depth.*

A decision-oriented menu. For each family: when it is required versus optional, the exact calls where a production package exists, how to report it, and how to read pass versus fail. "Required" means a referee will demand it for the stated design; skipping it invites an R&R round.

## Decision table: what your design requires

| Design | Required families (section numbers) | Usually optional |
|---|---|---|
| Staggered DiD / event study | Placebos (1), alt. specs (2), honest DiD bounds (5), wild bootstrap if few clusters (9) | Spec curve (6), RI (8) |
| Canonical 2x2 DiD | Placebos (1), alt. specs (2), wild bootstrap (9); RI (8) if one or two treated clusters | Spec curve (6) |
| IV | Outcome placebo (1), alt. specs (2), plausibly-exogenous bounds (5) | Spec curve (6), heterogeneity (4) |
| RDD | Placebo cutoffs (1), bandwidth/donut variants (2), sample restrictions (3) | Sensitivity (5) |
| Synthetic control | In-space and in-time placebos with permutation p-value (1), donor restrictions (3) | Alt. specs (2) |
| RCT | Multiple-testing correction (7), attrition bounds (5), RI (8) | Spec curve (6) |
| Selection-on-observables OLS | Oster delta and robustness value (5), alt. specs (2), sample restrictions (3) | RI (8) |

Heterogeneity (4) is required for any paper whose mechanism claim predicts where the effect concentrates, regardless of design.

---

## 1. Placebo tests

**Required** for DiD, event studies, SCM, and IV; optional only when the design admits no plausible placebo.

| Placebo | Design | What to run |
|---|---|---|
| Pre-treatment (fake date) | DiD, event study, SCM | Shift the treatment date into the pre-period; effect should be zero |
| Cross-unit (fake units) | DiD, SCM | Assign treatment to never-treated units; SCM in-space placebo over every donor |
| Outcome (unaffected outcome) | All, especially IV | Apply the design to an outcome the mechanism cannot touch; instrument-on-placebo regression for IV |
| Placebo cutoffs | RDD | `rdrobust` at thresholds away from the true cutoff |

**Report.** A figure for distributions (cross-unit placebo effects with the true estimate marked); a table row for single placebo coefficients, with the note stating the fake date, unit set, or cutoff used.

**Pass/fail.** Pass: placebo point estimates near zero and the true estimate in the tail of the placebo distribution (permutation p-value below 0.05 for SCM). Fail: any placebo comparable in size to the main effect; do not explain it away in a footnote — the design is compromised.

## 2. Alternative specifications

**Required** always; this is the minimum robustness table.

- Drop covariates one at a time; show the raw (no-controls) estimate
- Fixed effects at finer and coarser granularity
- Alternative outcome definitions: log vs. level, winsorized at 1% and 5%, alternative deflators
- Alternative estimator: if main is TWFE, show Callaway-Sant'Anna; if main is RDD, show the donut and the bandwidth grid; if main is OLS, show the IV

**Report.** One main-text table, each row a specification, first column always the headline point estimate for direct comparison; sample-size changes flagged per row. Deep variants go to the appendix.

**Pass/fail.** Pass: sign and approximate magnitude stable; magnitude shifts explained in the text, not left to the reader. Fail: the result lives in one specification, or coefficients move materially whenever a specific control enters — that control is doing identification work the design must confront.

## 3. Sample restrictions

**Required** whenever a unit, period, or subset plausibly dominates; optional otherwise but cheap.

- Drop the largest unit; drop the most influential time period
- Restrict to a balanced panel
- Rerun excluding the top 1% of influential observations (Cook's distance, leverage)
- Restrict to the comparable subset a skeptic would insist on

**Report.** Table rows in the robustness table, with the note stating exactly what was dropped and the resulting N.

**Pass/fail.** Pass: stable estimates with modest precision loss. Fail: one unit or period carries the result — then the paper is about that unit, and the framing must say so.

## 4. Heterogeneity

**Required** when the mechanism predicts it (the referee will check that the effect concentrates where the theory says); optional as pure description. Never mined.

- Interaction coefficients, not separately-estimated subgroup tables, unless heterogeneity is the point of the paper
- Dimensions: mechanism-relevant unit characteristics, early vs. late cohorts under staggered adoption, treatment intensity, quantile treatment effects (`qreg` in Stata, `quantreg` in R, `statsmodels` `QuantReg`) when distribution matters
- For RCTs: pre-specified subgroups from the PAP; anything else labeled exploratory

**Report.** Interaction terms in a table; quantile effects as a figure. The note states whether each split was pre-specified.

**Pass/fail.** Pass: the gradient matches the proposed channel. Fail: heterogeneity by every demographic reads as fishing; a significant subgroup with an insignificant main effect is not a finding.

## 5. Sensitivity analysis (selection on unobservables and assumption relaxation)

**Required** for any observational design whose headline survives on "we control for X"; the specific tool depends on the design.

| Tool | When required | Stata | R | Python |
|---|---|---|---|---|
| Oster delta / bounding (Oster (2019)) | Selection-on-observables claims, coefficient-stability arguments | `psacalc` | `robomit` | — |
| Robustness value, partial R-squared (Cinelli and Hazlett (2020)) | Same settings; strictly more informative than delta alone | `sensemakr` | `sensemakr` | `sensemakr` |
| Honest DiD relative-magnitude bounds (Rambachan and Roth (2023)) | Every DiD/event study leaning on parallel trends | `honestdid` | `HonestDiD` | — (export `betahat`, `sigma` to R) |
| Plausibly-exogenous bounds (Conley, Hansen, and Rossi (2012)) | Every IV whose exclusion restriction is contestable, i.e. every IV | authors' code | authors' code | — |
| Lee trimming bounds (Lee (2009)) | Differential attrition in experiments or panels | `leebounds` | `leebounds` | — |

**Report.** One sentence per tool in the text with the breakdown parameter ("unobservables would need to be d times as important as the included controls"), full output in the appendix. Honest DiD as a figure: bounds on the post-period effect against the sensitivity parameter M-bar.

**Pass/fail.** Pass: delta above 1, robustness value comfortably above the partial R-squared of the strongest observed confounder, honest bounds excluding zero at M-bar of at least 1, conclusions surviving nonzero direct effects of the instrument. Fail: breakdown at implausibly small violations — report it honestly and weaken the claim to directional.

## 6. Specification curves

**Optional** by default; **required** when the result is contested, counterintuitive, or the referee alleges specification search.

- Stata `speccurve`; R `specr`; no production Python package (Simonsohn, Simmons, and Nelson (2020))
- Enumerate the full reasonable choice set ex ante: controls, samples, outcome definitions, estimators — not a flattering subset

**Report.** A figure: estimates sorted by magnitude on top, the specification grid below, the median spec and the share of specs significant at 5% stated in the note.

**Pass/fail.** Pass: the distribution of estimates sits on one side of zero and the headline is near the median. Fail: the headline sits in the tail of its own curve — that is the definition of a cherry-picked specification.

## 7. Multiple-testing corrections

**Required** whenever more than one outcome, subgroup, or treatment arm supports a headline claim; mandatory for RCTs with multiple primary outcomes.

- Romano-Wolf stepdown FWER (Romano and Wolf (2005)): `wyoung` in Stata (the stepdown per List, Shaikh, and Xu (2019)), `multcomp` or `fixest` in R
- Bonferroni/Holm as the conservative fallback: `statsmodels` `multipletests` in Python; fine when tests are few and independent-ish, needlessly punishing when outcomes are correlated — prefer Romano-Wolf then
- Define the family ex ante (in the PAP for experiments); corrections within a hand-drawn family are theater

**Report.** Adjusted p-values or q-values in a dedicated column beside the naive ones; the note states the correction, the family, and the family size.

**Pass/fail.** Pass: primary outcomes survive FWER correction. Fail: only the uncorrected stars survive — the honest summary is "suggestive", not "significant".

## 8. Randomization inference

**Required** for small N, concentrated leverage, one-or-few treated clusters, and experiments where the randomization distribution is the actual source of uncertainty; optional as a complement elsewhere (Young (2019)).

- Stata `ritest`; R `ri2`
- Re-randomize following the actual assignment mechanism (respect strata and clustering); at least 1,000 permutations

**Report.** The randomization-inference p-value next to the model-based p-value in the main table; the note states the number of permutations and the re-randomization scheme.

**Pass/fail.** Pass: RI and model-based p-values agree. Fail: model-based significance evaporates under RI — the RI p-value is the honest one; leverage diagnostics tell you which observations did the work.

## 9. Wild cluster bootstrap (few clusters)

**Required** with fewer than roughly 50 clusters, unbalanced cluster sizes, or few treated clusters (Cameron, Gelbach, and Miller (2008); MacKinnon and Webb (2017)). Cluster-robust SEs are anti-conservative in exactly these settings.

- Stata `boottest`; R `fwildclusterboot`; Python `wildboottest`
- Use Rademacher weights by default; report the bootstrap p-value and CI, not just a recomputed SE

**Report.** Bootstrap p-values in brackets beneath the main estimates, or a dedicated inference row; the note states the number of clusters, bootstrap replications, and weight type.

**Pass/fail.** Pass: conclusions unchanged. Fail: significance disappears — the cluster-robust stars were an artifact of too few clusters; the bootstrap p-value is the one to report.

---

## Anti-patterns / robustness theater

- **Reporting only the checks that pass.** Twenty specifications run, two highlighted — referees notice. Pre-commit to the battery, then report all of it.
- **Coefficient-stability claims without R-squared movement.** "The estimate barely moves when controls enter" is meaningless if the controls explain nothing; stability must be scaled by R-squared movement (the point of Oster (2019)).
- **Confirming what no one doubts.** "Year fixed effects do not change the result" when year FE are already in the main specification is filler, not robustness.
- **"Available upon request."** Not credible at AER. If a check matters, it is in the appendix.
- **Post-hoc families.** Running the multiple-testing correction over a family drawn after seeing the p-values.
- **Placebo-as-decoration.** Running a placebo, failing it, and burying the failure in a footnote while keeping the headline.
- **Subgroups mined until one is significant**, then presented as mechanism evidence.
- **A 30-page appendix of noise** that never addresses the two or three counterarguments a smart referee will actually raise.
- **Robustness rows with silently changing samples.** Any change in N across rows is flagged and explained, or the comparison is meaningless.

## Canonical repo sources

Distilled from these repository files, which require the repository checkout:

- `docs/methods-reference.md` (inference and sensitivity table, package calls, citations)
- `skills/aer-robustness/SKILL.md` (referee-anticipating battery, coverage gate, reporting discipline)
- `templates/stata/04_robustness.do`, `templates/r/04_robustness.R`, `templates/python/robustness.py` (worked robustness batteries)
