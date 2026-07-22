# AEA Data and Code Availability Compliance Checklist

*Bundled with the `aer-replication` skill so the checklist works without the repository checkout. SKILL.md routes; this file carries the depth.*

Policy anchor: the AEA Data and Code Availability Policy (February 2026 revision), https://www.aeaweb.org/journals/data/data-code-policy, and the Data and Code Availability Form, https://www.aeaweb.org/journals/forms/data-code-availability. The deposit target is the AEA Data and Code Repository at ICPSR, https://www.icpsr.umich.edu/sites/aea/home.

## 1. README required sections

The README must be a PDF in the uppermost directory of the deposit. Keep a Markdown source if useful, but render `README.pdf` for the final deposit. Check every section:

- [ ] **Overview** — one paragraph: what the package does, which paper it accompanies, what software is required, total runtime.
- [ ] **Data Availability and Provenance Statement** — a summary-of-availability block (all public / some restricted / none public) plus a per-dataset entry (Section 2 below).
- [ ] **Dataset list** — a table of every file in `data/` with columns Filename | Description | Source | Notes.
- [ ] **Computational requirements** — OS, software with exact versions, every user-written package with version, hardware tested, peak memory, total runtime.
- [ ] **Description of programs** — what each script does, the run order, and the name of the single master script.
- [ ] **Instructions to replicators** — a literal numbered step-by-step a stranger can follow: download, install dependencies, set the working directory, run the master script, find outputs.
- [ ] **List of tables, figures, and programs** — every exhibit in the published paper mapped to script, line range, and output file.
- [ ] **References** — the paper citation and the deposit's own citation with DOI slots.

## 2. Data availability statement patterns

Write one entry per dataset. Every entry states source, citation, license or terms, date accessed, whether the file is in the deposit, and (if not) exactly how to obtain it. Template sentences by access class:

### Public data (included)

> The data for [DATASET-NAME] were downloaded from [SOURCE-INSTITUTION] at [SOURCE-URL] on [ACCESS-DATE]. The data are in the public domain (or licensed under [LICENSE-NAME]) and are provided in this deposit as `data/raw/[FILE-NAME]`.

### Restricted-access data (obtainable by others)

> The data for [DATASET-NAME] are available from [PROVIDER-NAME] under a data use agreement. Access requires [APPLICATION-STEPS]; approval typically takes [TURNAROUND-ESTIMATE] and costs [COST-ESTIMATE]. The authors obtained access on [ACCESS-DATE] under agreement [AGREEMENT-ID]. The data cannot be redistributed, but the code in this deposit will reproduce all results once the files are placed in `data/raw/`.

### Proprietary data (commercial source)

> The data for [DATASET-NAME] were purchased from [VENDOR-NAME] ([VENDOR-URL]). A license for the same extract, [EXTRACT-DESCRIPTION], can be purchased by any researcher for approximately [COST-ESTIMATE]. The authors are not permitted to redistribute the files. The deposit includes the full processing code and a synthetic sample with identical schema in `data/raw/synthetic/` for smoke-testing.

### Confidential data (agency or IRB restrictions)

> The data for [DATASET-NAME] are confidential microdata held by [AGENCY-NAME] and were accessed under [PROJECT-OR-IRB-ID]. Researchers can apply for access via [APPLICATION-PROCESS]. The authors will preserve the data and code for at least five years and will assist reasonable replication requests. All processing and analysis code is included in this deposit.

Required commitments whenever data cannot be deposited:

- [ ] Preserve data and code for at least 5 years.
- [ ] Assist reasonable replication requests.
- [ ] Make all **code** publicly available regardless.
- [ ] Document provenance thoroughly enough that an independent researcher could obtain the same data: exact dataset name and vintage, agency or vendor, application process, approximate cost, expected turnaround.

### Extra checks for any non-public dataset

- [ ] The README gives **access instructions** an outsider can execute: exact dataset name and vintage, holding agency or vendor, application process, approximate cost, expected turnaround.
- [ ] The deposit includes **code that would run** if the data were present, with the expected file names and schema stated.
- [ ] Where possible, a **synthetic or simulated sample** with the same schema is included so the pipeline can be smoke-tested end to end.
- [ ] Consider depositing **intermediate aggregates** (e.g., cell-suppressed counts) that permit partial replication without the microdata.
- [ ] If the editorial office asks whether a private copy can be shared with the Data Editor for verification, answer via the forms they send — do not invent substitute arrangements or assume form titles from an older policy cycle.

## 3. Dataset citation rules

Datasets are cited like papers — in the reference list of both the paper and the README, not only in a footnote.

- [ ] Every dataset has a full citation: creator, year, title, distributor or repository, version or vintage, DOI or accession number, access date.
- [ ] The citation names the exact **vintage or version** used (e.g., [DATASET-NAME], [VERSION-OR-VINTAGE], accessed [ACCESS-DATE]); a bare URL is not a citation.
- [ ] Derived or purchased extracts cite both the underlying source and the extract as delivered.
- [ ] The deposit itself carries its own citation slot in the README ("Data and Code for: [PAPER-TITLE]") with the deposit DOI filled in after approval.
- [ ] Citation entries in the README match the entries in the paper's bibliography word for word.

## 4. openICPSR deposit workflow

1. Create the deposit at the AEA Data and Code Repository (see https://www.icpsr.umich.edu/sites/aea/home for the repository entry point). Draft deposits are automatically visible to the AEA Data Editor's office.
2. Upload files **unzipped** so the directory tree is browsable in the repository. One opaque top-level ZIP is a bounce except for rare repository-approved exceptions.
3. Fill the metadata form: full citation, abstract, keywords, JEL codes, geographic coverage, time period, collection dates.
4. Verify the file manifest against Section 8 of this checklist (directory layout) — no stray drafts, no editor correspondence, no `.DS_Store` clutter.
5. Submit for review; the Data Editor's office runs the computational reproducibility check.
6. Address any revision request **in the deposit itself** (not by email attachment) and resubmit.
7. Approval assigns the DOI; paste the DOI into the paper's data availability statement and the README citation slot before final files are due (final-file rules: https://www.aeaweb.org/journals/aer/accepted-article-guidelines and https://www.aeaweb.org/journals/aeri/accepted-article-guidelines).

## 5. Reproducibility smoke test

Run this before submitting the deposit, on a machine that is not the one the paper was written on:

1. **Fresh checkout.** Download your own draft deposit and unzip to a clean directory. No files copied from the project folder.
2. **Clean environment.** New Stata/R/Python session; no packages preinstalled beyond the base install. Run the package-installation script and record its log.
3. **One master script.** Execute the single entry point (e.g., `run_all.do`) with no manual edits other than the documented working-directory line.
4. **Logs.** Confirm a log file is written for the full run to `logs/`, and that it ends without errors.
5. **Diff the outputs.** Compare every generated table and figure in `output/` against the published exhibits, number by number. Any mismatch is a defect in the deposit, not a rounding footnote.
6. **Timing.** Record actual runtime and peak memory; update the README's computational-requirements section to match reality.

If any step requires knowledge that is not written in the README, the README is incomplete. Fix the README, not the replicator.

## 6. Code hygiene spot-checks

Quick greps to run over `code/` before the smoke test; each hit is a defect:

- [ ] **Relative paths only.** Search for drive letters and personal user directories; every path should resolve from the package root (e.g., `data/raw/[FILE-NAME]`).
- [ ] **Seeds set.** Every bootstrap, permutation, simulation, or synthetic-control call is preceded by an explicit seed, set once in the setup script and documented in the README.
- [ ] **One entry point.** Nothing needs to be run by hand outside the master script; stage scripts do not depend on being run interactively.
- [ ] **Versions pinned.** Stata: version statement at the top of each do-file, packages installed from a setup script with versions recorded (vendor an `ado/` snapshot if exact versions matter). R: `renv` or `groundhog` lockfile. Python: `requirements.txt` with exact `==` pins.
- [ ] **Logs on.** The master script opens a log, and stage scripts inherit it; the shipped `logs/` directory contains the authors' own successful full-run log.
- [ ] **No dead code.** Commented-out alternative specifications and abandoned scripts are removed — the Data Editor reads what is shipped.
- [ ] **Outputs regenerate.** Delete `output/` and `data/intermediate/`, rerun the master script, and confirm everything reappears; shipped intermediates must not silently patch a broken pipeline.

## 7. Common AEA Data Editor bounce reasons

- Hardcoded absolute paths (a path with a personal user directory anywhere in the code).
- Missing or unpinned package versions; a setup that only works with packages as they existed on the author's machine.
- Master script errors on a clean machine (missing file, missing package, wrong directory assumption).
- Numbers produced by the code differ from the published tables or figures.
- Restricted-data paper with no provenance documentation or acquisition instructions.
- README that says "see paper" instead of stating the steps.
- One giant ZIP whose contents the repository cannot display.
- Exhibits in the paper with no producing script mapped in the README.
- No random seed set for bootstrap, permutation, or simulation procedures, so results are not bit-reproducible.
- Missing license file for the code, or data redistributed against the source's terms.
- Stale intermediate files shipped in the deposit that mask a broken cleaning step.
- Log files absent, so the Data Editor cannot compare a failed run against the authors' run.
- Deposit metadata (title, authors, abstract) inconsistent with the accepted manuscript.
- "All code available from the authors upon request" anywhere in the paper — this does not satisfy the policy.

## 8. Directory layout

Match the skeleton in `examples/replication-package-skeleton/`:

| Path | Contents | Required? |
|---|---|---|
| `README.pdf` | Rendered README, uppermost directory | Required |
| `README.md` | Editable README source | Optional |
| `LICENSE` | Code license (commonly MIT or CC-BY); data per source license | Required |
| `run_all.do` (or `.R`, `.py`) | Single master script running the whole pipeline | Required |
| `data/raw/` | Original source files exactly as obtained; never edited in place | Required (or provenance docs) |
| `data/intermediate/` | Cleaned or merged files generated by the pipeline | Required |
| `data/codebook/` | Variable dictionaries, crosswalks, and `source-register.md` | Required |
| `code/` | Numbered stage scripts (`00_setup` through tables/figures) | Required |
| `output/tables/` | Generated table files used by the paper and appendix | Required |
| `output/figures/` | Generated figure files used by the paper and appendix | Required |
| `logs/` | Runtime logs from full and partial replication runs | Strongly recommended |
| `docs/` | Exhibit register, data appendix, computing-environment notes, DUAs | Strongly recommended |

Layout checks:

- [ ] Every file in the deposit is reachable from the README's dataset list or program description.
- [ ] `data/raw/` files are byte-identical to what the source delivered.
- [ ] `data/codebook/source-register.md` and `docs/exhibit-register.md` are synchronized with the README tables.
- [ ] Nothing in the tree requires a path outside the package root.

## Final gate

- [ ] All Section 1 README sections present and populated.
- [ ] Every dataset has an availability entry in the correct pattern (Section 2) and a full citation (Section 3).
- [ ] Smoke test (Section 5) passed on a second machine, logs saved.
- [ ] Code hygiene spot-checks (Section 6) all clean.
- [ ] No item from the bounce list (Section 7) applies.
- [ ] Directory layout matches the skeleton (Section 8).
- [ ] Deposit uploaded unzipped with complete metadata (Section 4).

## Canonical repo sources

Distilled from these repository surfaces, which require the repository checkout:

- `skills/aer-replication/SKILL.md`
- `examples/replication-package-skeleton/README.md`
- `examples/replication-package-skeleton/data/codebook/source-register.md`
- `examples/replication-package-skeleton/docs/exhibit-register.md`
- `docs/source-register.md`
