# Exhibit Register

Use this register to connect every published table and figure to its data,
code, statistical method, and output artifact. Keep it synchronized with the
manuscript, appendix, and `README.md` table titled "List of Tables, Figures, and
Programs."

## Main Exhibits

| Exhibit | Claim supported | Script and lines | Input data | Estimator or statistic | Exact sample size | Output file | Figure/table note | Accessibility note |
|---|---|---|---|---|---:|---|---|---|
| Table 1 | [Descriptive pattern] | `code/02_descriptives.do`, lines [..] | `data/intermediate/analytic.dta` | Summary statistics | [N] | `output/tables/tab1_summary.tex` | Defines sample, weights, and units. | Editable table, not an image. |
| Table 2 | [Main causal estimate] | `code/03_main_did.do`, lines [..] | `data/intermediate/analytic.dta` | [Estimator], [SE/inference] | [N] | `output/tables/tab2_main_twfe.tex` | States fixed effects, controls, clustering, and outcome scale. | Editable table, not an image. |
| Figure 1 | [Descriptive visual evidence] | `code/02_descriptives.do`, lines [..] | `data/intermediate/analytic.dta` | [Statistic or map classification] | [N] | `output/figures/fig1_map.pdf` | Caption defines geography and any boundary choices. | Vector output; alt text drafted in manuscript. |
| Figure 2 | [Dynamic treatment pattern] | `code/03_main_did.do`, lines [..] | `data/intermediate/analytic.dta` | Event-study estimator with [reference period] | [N] | `output/figures/fig2_event_study.pdf` | Caption states confidence interval, omitted period, and identifying sample. | Vector output; alt text drafted in manuscript. |

## Appendix Exhibits

| Exhibit | Claim supported | Script and lines | Input data | Estimator or statistic | Exact sample size | Output file | Figure/table note | Accessibility note |
|---|---|---|---|---|---:|---|---|---|
| Appendix Table A.1 | [Balance or diagnostic claim] | `code/02_descriptives.do`, lines [..] | `data/intermediate/analytic.dta` | [Statistic/test] | [N] | `output/tables/tabA1_balance.tex` | Notes pre-period, covariates, and multiple-testing convention. | Editable table, not an image. |
| Appendix Figure A.6 | [Sensitivity claim] | `code/03_main_did.do`, lines [..] | `data/intermediate/analytic.dta` | [Sensitivity method] | [N] | `output/figures/figA6_honest_did.pdf` | Notes sensitivity parameter and confidence-set interpretation. | Vector output; alt text drafted in manuscript. |

## Audit Rules

- Every row must point to the script location that creates the final output.
- Exact sample size means the analysis sample used for that exhibit, not the
  full raw-data count.
- The table or figure note must state weights, clusters, fixed effects,
  uncertainty measures, omitted categories, and units when applicable.
- Figure accessibility notes must identify vector/raster status and whether alt
  text exists in the manuscript file.
- Any exhibit that supports a causal claim must cite the assumption, diagnostic,
  and robustness evidence in the manuscript or appendix.
