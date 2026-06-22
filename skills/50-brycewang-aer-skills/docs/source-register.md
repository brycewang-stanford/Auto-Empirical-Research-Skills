# Source Register

This repository encodes current journal policy and modern econometrics
defaults. Treat this file as the single place to check before editing hard
requirements in `README.md`, `skills/`, `docs/`, or templates.

Last reviewed: 2026-06-02.

## Official AEA Policy Sources

| Topic | Source | Repo surfaces that depend on it | Review trigger |
|---|---|---|---|
| AER submission length, abstract, disclosure, AI-use, RCT, and cover-letter rules | https://www.aeaweb.org/journals/aer/submissions | `README.md`, `README.en.md`, `skills/aer-submission/SKILL.md`, `docs/desk-rejection-audit.md` | Before each release and after any AEA submission-page update |
| AER accepted-article file package, data/code, disclosure, appendix, and publication agreement rules | https://www.aeaweb.org/journals/aer/accepted-article-guidelines | `skills/aer-submission/SKILL.md`, `skills/aer-replication/SKILL.md`, `examples/replication-package-skeleton/README.md` | Before changing final-file or replication-package guidance |
| AER: Insights submission word-count formula, exhibit cap, abstract, disclosure, and word-count PDF rules | https://www.aeaweb.org/journals/aeri/submissions | `README.md`, `README.en.md`, `skills/aer-submission/SKILL.md`, `docs/desk-rejection-audit.md` | Before changing any AER: Insights routing or length text |
| AER: Insights accepted-article file package and data/code rules | https://www.aeaweb.org/journals/aeri/accepted-article-guidelines | `skills/aer-submission/SKILL.md`, `skills/aer-replication/SKILL.md` | Before changing accepted-article checklists |
| AEA Data and Code Availability Policy | https://www.aeaweb.org/journals/data/data-code-policy | `skills/aer-replication/SKILL.md`, `examples/replication-package-skeleton/README.md`, `templates/` | Before changing README, data-provenance, restricted-data, or master-script guidance |
| AEA Data and Code Availability Form | https://www.aeaweb.org/journals/forms/data-code-availability | `skills/aer-replication/SKILL.md`, `skills/aer-submission/SKILL.md` | Before naming required final-stage data/code forms |
| AEA Data and Code Repository at ICPSR | https://www.icpsr.umich.edu/sites/aea/home | `skills/aer-replication/SKILL.md`, `examples/replication-package-skeleton/README.md` | Before changing openICPSR deposit workflow |

## Official PNAS Nexus Policy Sources

| Topic | Source | Repo surfaces that depend on it | Review trigger |
|---|---|---|---|
| PNAS Nexus article types, page expectations, manuscript components, data/materials/code availability, statistics, AI-use, ethics, figures, alt text, and submission metadata | https://academic.oup.com/pnasnexus/pages/general-instructions | `docs/pnas-nexus-publication-plan.md`, `docs/pnas-nexus-submission-checklist.md`, `docs/source-register.md` | Before changing PNAS Nexus venue-fit, reproducibility, disclosure, figure, or submission-preflight guidance |

## Econometrics Sources

`docs/methods-reference.md` is the canonical repo surface for estimator and
diagnostic defaults. Every method paper cited there should have a BibTeX entry
in `references.bib`; update both files in the same change.

When a package API changes, update the relevant template first, then update
`docs/methods-reference.md` and the affected skill prose. Do not update prose
without rerunning `make validate`.

## Validator Guardrails

`scripts/validate_repo.py` checks that the main policy-bearing surfaces still
contain the high-risk constraints most likely to drift during rewrites:

- 100-word abstract limits
- AER: Insights 7,000-word minus 200-per-exhibit formula
- disclosure statement and AI-use disclosure language
- February 2026 Data and Code Availability Policy language
- README PDF, Data and Code Availability Statement, and openICPSR guidance
- PNAS Nexus abstract, significance-statement, public-repository,
  statistical-reporting, figure-accessibility, ORCID, and final-gate evidence
  requirements

If an official source changes one of these constraints, update the source row
above and the validator guardrail in the same patch.

## Concurrent-Agent Rule

If another agent is editing policy text, update this register first or add a
note in the handoff. Keep policy-source edits separate from template rewrites so
merge conflicts are localized.
