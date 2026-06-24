# PNAS Nexus Submission Checklist

Use this checklist when a manuscript, appendix, code, and data package are
available for a *PNAS Nexus* submission audit. Every row should cite concrete
evidence: a manuscript section, appendix page, code path, command output,
repository DOI, log file, or data-access document. Do not mark a row complete
because the item is "planned."

## Manuscript File

| Item | Evidence to record | Status |
|---|---|---|
| Title page includes title, author names, affiliations, one corresponding-author mailing address and email, classification, and keywords. | Manuscript page or source path. | Not checked |
| Title is brief, descriptive, broad-audience readable, and under 135 characters. | Title text and character count. | Not checked |
| Abstract is one paragraph and no more than 250 words. | Word-count command or editor count. | Not checked |
| Research Report significance statement is 50-120 words. | Word-count command or editor count. | Not checked |
| Funding statement is present, including full funder names and grant numbers, or a no-funding statement. | Manuscript section. | Not checked |
| AI-use disclosure is included in Materials and Methods or Acknowledgments when applicable. | Manuscript section and tool/model/version. | Not checked |
| Competing-interest disclosures are entered in the submission system and consistent with manuscript text. | Submission-system record or author confirmation. | Not checked |
| Human-subjects, animal-subjects, consent, permits, or exemption statements are present when applicable. | IRB/IACUC/permit reference and manuscript section. | Not checked |

## Data, Materials, Code, and Protocols

| Item | Evidence to record | Status |
|---|---|---|
| Data availability statement covers every dataset, material, protocol, code file, and script used in analysis. | Data statement plus dataset inventory. | Not checked |
| Public repository plan identifies a DOI-capable public repository and release timing. | Repository draft, DOI reservation, or deposit URL. | Not checked |
| Restrictions on full or partial access are disclosed at submission with legal, ethical, logistical, or size rationale. | Access note, DUA, IRB language, or controlled-access workflow. | Not checked |
| All publicly available datasets have reference-list citations with DOI, accession number, or persistent identifier. | Reference entries and in-text/data statement citations. | Not checked |
| Research software is cited or otherwise identified with source, version, and persistent link when possible. | Reference entries, software section, or environment file. | Not checked |
| Raw data retention plan is documented, including original unprocessed visual data if applicable. | Repository path, retention policy, or lab/data-management note. | Not checked |
| The package can be run from a clean checkout or documented restricted-data setup. | Command, environment, runtime log, and generated outputs. | Not checked |

## Statistical Reporting

| Item | Evidence to record | Status |
|---|---|---|
| Each table and figure maps to a script, input data, output file, and exact sample size. | Exhibit register or replication README table. | Not checked |
| Methods section states the statistical method, estimator, uncertainty measure, and evidence-strength measure for each result family. | Manuscript methods paragraphs and table/figure notes. | Not checked |
| Software source and version are reported for all statistical analyses, including the software source and version for each analysis environment. | Environment file, log, session info, or package lockfile. | Not checked |
| Causal claims are separated from descriptive claims and tied to assumptions, diagnostics, and robustness checks. | Manuscript claim map and design memo. | Not checked |
| Survey analyses disclose sampling design, modeling, weighting assumptions, recruitment, conditioning, attrition, and implications when applicable. | Methods section and survey instrument appendix. | Not checked |

## Figures, Tables, and Accessibility

| Item | Evidence to record | Status |
|---|---|---|
| Every table is numbered, cited in text, placed at the end of the main text, and editable rather than embedded as an image. | Manuscript table section. | Not checked |
| Every figure has title and legend in the manuscript file, not inside the image file. | Manuscript figure legend section. | Not checked |
| Multipanel figures are submitted as one file with panel labels. | Figure files and panel-label check. | Not checked |
| Charts, graphs, and diagrams are vector files where possible. | Output file extensions and generation scripts. | Not checked |
| Raster images meet PNAS Nexus resolution expectations for their use case. | Image dimensions, dpi/ppi metadata, and file type. | Not checked |
| Figure alt text appears under each figure legend and is concise, informative, and nonduplicative. | Manuscript source or compiled file. | Not checked |
| Maps use neutral captions, legends, and labels for disputed territories when applicable. | Figure files and captions. | Not checked |

## Submission Package

| Item | Evidence to record | Status |
|---|---|---|
| Manuscript source, compiled PDF, appendix/SI, figure files, and remaining LaTeX or Word assets are available. | File inventory. | Not checked |
| Corresponding author ORCID is available; all author names, affiliations, and current affiliations are confirmed. | Submission metadata or author confirmation. | Not checked |
| The manuscript is not under consideration, peer review, or accepted elsewhere. | Corresponding-author confirmation. | Not checked |
| Previously published or third-party material has documented permission or a clear reuse basis. | Permission files or rights notes. | Not checked |
| Direct quotations are in quotation marks and all reused text, figures, tables, data, and software are cited. | Manuscript audit notes. | Not checked |
| Preprint status and planned update path are documented if applicable. | Preprint URL and update note. | Not checked |

## Final Gate

Before submission, rerun the full analysis from the documented entry point and
paste the exact command, runtime, commit hash, and output log path here:

```text
command:
runtime:
commit:
log:
outputs:
remaining exceptions:
```
