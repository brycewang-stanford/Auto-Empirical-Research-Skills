---
name: fair-check
description: Audit manuscript and replication package against FAIR open-science principles.
argument-hint: "[path to manuscript and replication package, or paste availability statements and repository links]"
---

# FAIR Manuscript Checker

## Standards anchor

Use the FAIR principles as manuscript-facing checks for research objects: **Findable, Accessible, Interoperable, Reusable**. FAIR does **not** mean everything must be openly downloadable. Sensitive or restricted data can be FAIR when metadata, access conditions, identifiers, and reuse terms are explicit. The practical standard is "as open as possible, as restricted as necessary."

Core references: Wilkinson et al. (2016) for the FAIR principles, GO FAIR for the F/A/I/R subprinciples, OSF documentation for repository metadata and data archiving, FORCE11 for data citation principles, and TOP/DA-RT for manuscript transparency expectations.

## Instructions

### 1. Inventory research objects

Before judging compliance, list every research object the manuscript depends on:

- Raw data, cleaned data, derived data, and analysis-ready data.
- Analysis code, simulation code, randomization scripts, package lockfiles, and notebooks.
- Survey instruments, treatments, vignettes, questionnaires, prompts, codebooks, classification labels, OCR prompts, and annotation guidelines.
- Figures, tables, model outputs, topic models, classifiers, trained weights, dictionaries, and corpora.
- Preregistrations, PAPs, IRB/ethics protocols, consent language, and data-use agreements.
- Third-party data or proprietary inputs that cannot be redistributed.

If an object is not shareable, it still needs metadata and a clear access or non-availability explanation.

### 2. Check Findable

For each research object, verify:

- Repository or landing page exists and is public or publicly discoverable.
- Persistent identifier exists or is planned: DOI, ARK, Handle, OSF registration DOI, Zenodo DOI, Dataverse DOI, ICPSR study ID, or equivalent.
- Metadata includes title, creators/contributors, description, date/version, resource type, keywords/tags, funder when relevant, related publication DOI, and related object links.
- Data/code/materials are cited in the manuscript or reference list, not only mentioned in prose.
- File names are interpretable and map to manuscript tables, figures, or analyses.

Prompt author if missing: repository URL, DOI/identifier, title, contributors, version/date, and how each object maps to manuscript claims.

### 3. Check Accessible

Verify:

- Access route is clear: open download, embargoed release date, controlled access, data-use agreement, request email/form, or legal/ethical non-availability.
- Protocol is standard and durable: repository landing page, HTTPS, institutional repository, OSF, Dataverse, Zenodo, ICPSR, Dryad, GitHub+Zenodo, or discipline repository.
- Restricted data have public metadata and explicit criteria for access.
- Sensitive data are not uploaded to unsuitable repositories; OSF should not be used for sensitive or personally identifiable health information.
- Availability statements match actual repository state.
- Embargoes and anonymous peer-review links are handled without breaking post-publication access.

Prompt author if missing: access restrictions, embargo date, contact process, data-use agreement, privacy constraints, and post-acceptance public URL.

### 4. Check Interoperable

Verify that others can read and combine the materials:

- Data use non-proprietary or widely readable formats where possible: CSV/TSV, TXT, JSON, Parquet, RDS with fallback, Stata with codebook, PDF/A for documents.
- Variables, labels, missing values, scales, treatment arms, weights, and derived variables are documented.
- Code has an environment file or setup notes: `renv.lock`, `requirements.txt`, `environment.yml`, Dockerfile, session info, package versions, or OS notes.
- Metadata follows a discipline-appropriate standard where available: DDI for social-science survey data, DataCite metadata, repository community schemas, or structured README.
- Cross-links connect raw data, cleaned data, code, figures/tables, and manuscript claims.

Prompt author if missing: codebook, README, variable dictionary, software environment, data provenance, or mapping from files to outputs.

### 5. Check Reusable

Verify:

- License is explicit for each shareable object: data, code, text/materials, and figures may need different licenses.
- Reuse conditions are clear for third-party, proprietary, copyrighted, or restricted materials.
- Provenance is documented: collection method, source, cleaning steps, transformations, exclusions, and version history.
- Minimal replication path is documented: what script to run, in what order, and what output it produces.
- Ethics and consent allow the claimed sharing level.
- Data/code/material citations give credit to creators and make reuse citable.

Prompt author if missing: license choices, consent/sharing compatibility, restrictions on reuse, provenance notes, and replication instructions.

### 6. Audit manuscript statements

Check these sections, or draft them if absent:

- Data Availability Statement.
- Code Availability Statement.
- Materials/Stimuli Availability Statement.
- Preregistration/PAP Statement.
- Ethics/IRB and consent language.
- Funding and conflicts where tied to repository metadata.
- Data/code/material citations in references.

Statements must be specific enough for a reader to find and reuse objects. "Available upon request" is weak unless privacy, legal, or contractual constraints justify it and the access process is concrete.

### 7. Compose with sibling skills

- Use `citation-check` when repository objects need formal citation or DOI checks.
- Use `figure-table-audit` to verify figures/tables trace to repository files or scripts.
- Use `methods-reporting` for DA-RT, TOP, JARS, CONSORT, and methods-section integration.
- Use `text-classification`, `topic-modeling`, or `vlm-ocr-pipeline` when FAIRness depends on prompts, models, corpora, or derived computational objects.
- Use `paper-review-lite` or `presubmit` for full pre-submission review after FAIR fixes.

## Output

Produce a `FAIR Manuscript Audit`:

```
# FAIR Manuscript Audit

Scope:
Manuscript files:
Repository/package links checked:
Summary: <N blocking, N recommended, N minor, N author prompts>

## Research Object Inventory
| Object | Location in manuscript | Repository/identifier | Share status | Notes |

## FAIR Checklist
| Object | Findable | Accessible | Interoperable | Reusable | Main gap |

## Blocking Issues
| Location | FAIR dimension | Issue | Fix |

## Recommended Fixes
| Location | FAIR dimension | Issue | Fix |

## Author Prompts
1. <question the author must answer before the statement can be finalized>

## Draft Availability Statements
### Data
### Code
### Materials
### Preregistration

## Repository Package Checklist
| Item | PASS/FAIL/PARTIAL/NA | Notes |
```

Severity:

- **Blocking:** no repository or access route for essential data/code/materials; missing or false availability statement; missing license for reusable data/code; restricted data without access conditions; repository link absent for a claimed open object; sensitive data exposed inappropriately.
- **Recommended:** DOI pending, metadata thin, README incomplete, codebook missing details, proprietary format without fallback, no formal data/code citation.
- **Minor:** inconsistent file names, weak tags, style problems in availability statements, minor README clarity issues.

## Quality checks

- [ ] All research objects were inventoried before FAIR scoring.
- [ ] FAIR was not treated as identical to open access.
- [ ] Restricted or sensitive data were checked for transparent access conditions rather than forced open sharing.
- [ ] Data, code, and materials were checked as separately licensable objects.
- [ ] Persistent identifiers and repository metadata were checked when links were available.
- [ ] Missing author knowledge was surfaced as explicit prompts.
- [ ] Draft statements are specific enough to locate and reuse the objects.
