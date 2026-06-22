# PNAS Nexus Publication Plan

This document is a venue-specific reviewer audit and one-week improvement plan
for a social-science or economics manuscript targeting *PNAS Nexus*. It is based
on the official PNAS Nexus author instructions listed in
[`source-register.md`](./source-register.md). It is not a substitute for
paper-specific review: this repository currently contains skills, templates, and
examples, but no manuscript draft or empirical dataset.

## Harsh Reviewer Audit

| Risk | Reviewer objection | Required fix |
|---|---|---|
| No visible manuscript | I cannot evaluate novelty, scope, methods, or fit because no draft is present in the repo. | Add the manuscript source, compiled PDF, appendix, and exhibit inventory before any publication-level audit. |
| Venue mismatch | The paper may read like an AER-field contribution, not an interdisciplinary PNAS Nexus contribution. | Rewrite the framing around broad scientific importance, not only economics-field positioning. |
| Data and code opacity | "Available on request" is not enough. PNAS Nexus expects data, materials, protocols, code, and scripts in a public repository upon publication, with restrictions disclosed at submission. | Build a public-repository deposit plan with DOI-capable repository choice, access restrictions, and executable code. |
| Missing dataset citations | If the datasets are not citable in the references, the data availability statement is incomplete. | Add formal dataset citations with accession numbers, DOIs, or persistent identifiers. |
| Methods under-specification | A reader cannot reproduce each table and figure if the statistical methods, software versions, samples, and measures of uncertainty are scattered or implicit. | Create a table-by-table and figure-by-figure methods map with exact sample sizes, estimator choices, software versions, and uncertainty measures. |
| Weak identification language | A causal claim without explicit assumptions, design diagnostics, and falsification checks will be read as overclaiming. | Separate descriptive, predictive, and causal claims; attach assumptions and robustness checks to every causal statement. |
| Figure compliance risk | Production can reject figures that are low resolution, non-vector charts, missing legends, or inaccessible. | Audit every figure for standalone legends, panel labels, vector chart output, required raster resolution, and alt text. |
| Disclosure gaps | Funding, competing interests, ORCID, AI use, human-subjects approval, consent, and preregistration may be missing or undocumented. | Add a submission metadata checklist and draft manuscript sections for each applicable disclosure. |

## One-Week Improvement Plan

| Day | Goal | Deliverable |
|---|---|---|
| 1 | Establish the publication baseline. | Manuscript inventory: draft, PDF, appendix, exhibits, data sources, code entry point, and missing files list. |
| 2 | Rebuild the data-cleaning standard. | Dataset register covering provenance, access route, license, restrictions, transformations, and citation target for every source. |
| 3 | Reproduce the empirical pipeline. | One command that rebuilds analytic data, tables, figures, and logs from a clean checkout or documented restricted-data setup. |
| 4 | Stress-test identification and modeling. | Design memo covering assumptions, diagnostics, alternative estimators, robustness, placebo tests, heterogeneity, and sensitivity analyses. |
| 5 | Upgrade the manuscript for PNAS Nexus fit. | Revised title, abstract under 250 words, 50-120 word significance statement, broad-audience framing, and tightened claims. |
| 6 | Audit figures, tables, and accessibility. | Exhibit register with output paths, source scripts, sample sizes, legends, alt text, and production-format status. |
| 7 | Run submission preflight. | Final checklist for data availability, code availability, dataset/software citations, ethics, funding, competing interests, AI-use disclosure, ORCID, and repository DOI plan. |

## PNAS Nexus Compliance Targets

- Initial submission is format-neutral, but the manuscript must include a title
  page, abstract, significance statement when applicable, main text,
  references, figures or tables with legends, contact and competing-interest
  information, data sharing plans, and funding information.
- Research Reports should fit the journal's page expectations: preferred 6
  pages, maximum 12 pages; a standard 6-page article is approximately 4,000
  words, 50 references, and 4 medium-size graphical elements.
- Abstract length is capped at 250 words and should be a single paragraph.
- Research Reports and Stage 2 Registered Reports require a 50-120 word
  significance statement.
- Data, materials, protocols, code, and scripts used in the analysis must be
  available in a public repository upon publication unless restrictions are
  disclosed at submission.
- Publicly available datasets must be cited in the reference list with a DOI,
  accession number, or other persistent identifier.
- Statistical reporting must identify software source and version, methods,
  exact sample sizes, and measures of evidence strength for each table and
  figure.
- Figures need in-manuscript titles and legends, separate production-ready
  files, panel labels for multipanel figures, sufficient resolution or vector
  chart formats, and alt text.

## Implementation Notes for This Repo

- Use [`examples/replication-package-skeleton/`](../examples/replication-package-skeleton/)
  as the starting point for a PNAS Nexus-compatible reproducibility package, but
  change the repository target from openICPSR-only to the best field-appropriate
  DOI repository.
- Use [`docs/methods-reference.md`](./methods-reference.md) to select modern
  estimators and diagnostics before rewriting results.
- Use [`docs/desk-rejection-audit.md`](./desk-rejection-audit.md) for the
  reviewer-pressure-test posture, but do not copy AER-specific length or
  disclosure limits into PNAS Nexus submissions.
