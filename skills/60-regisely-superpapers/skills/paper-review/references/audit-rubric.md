# Paper Review Audit Rubric

Executable checklist per audit dimension. Every check lists its criterion, severity when failed, and a concrete remediation hint. Severities: **Critical** blocks submission, **Major** should be fixed, **Minor** is nice to fix.

---

## 1. Numerical Consistency

Every number in the paper prose must match its source file or log.

| Check | Criterion | Severity | Remediation |
|---|---|---|---|
| Point estimates | Number in `.tex` prose matches the `output/tables/*.tex` cell it cites, up to the paper's last reported digit. | Critical | Edit prose or regenerate table; do not report numbers the table does not support. |
| Standard errors | SE in prose matches table cell at same precision. | Critical | Same as above. |
| Sample size N | N in abstract, body, and tables all agree. | Critical | Recount from the final analysis dataset; update all mentions. |
| Percentages | `X%` in prose derivable from a table number or log line. | Critical | Derive from source, not from memory. |
| R², test statistics | All reported diagnostics traceable to a log file. | Major | Produce a log with the diagnostic when missing. |
| p-values | Reported p-values match the source and align with the declared significance convention. | Major | Regenerate with the correct test or report exactly. |

Extraction targets in prose: `\d+\.\d+`, `\d+%`, "N =", "n =", "R² =", "p =", "β =".

---

## 2. Narrative Coherence and Structure

### Coherence across sections

| Check | Criterion | Severity |
|---|---|---|
| Same research question | Abstract, introduction, conclusion pose the same question. | Major |
| Same main result | Main estimate and sign agree across abstract, introduction, results, conclusion. | Major |
| Same magnitude | Reported magnitude agrees across sections, up to the precision used. | Major |
| Same identification strategy | Strategy named in abstract matches the one executed in methods and results. | Major |
| Same caveats | Limitations mentioned in the conclusion align with those surfaced in robustness. | Minor |

### Literature dialogue

| Check | Criterion | Severity |
|---|---|---|
| Discussion has `\cite{}` | Discussion section contains at least one citation. | Major |
| Results engage prior work | Results compare findings to cited papers, not just report numbers. | Major |
| Discussion citation density | At least one citation per page of prose in Discussion. | Major |
| Intro links result to literature | Introduction positions the contribution against named papers. | Major |

### Structural flow

| Check | Criterion | Severity | Remediation |
|---|---|---|---|
| Section word floor | Every `\section` has > 200 words of body prose. | Minor | Merge with neighbor or expand. |
| Subsection word floor | Every `\subsection` has > 80 words of body prose. | Minor | Merge with neighbor or remove subheading. |
| Subsubsection use | `\subsubsection` used sparingly — zero or very few per section. | Minor | Prefer flowing prose with signposts. |
| Subheading density | No more than ~3 subheadings per printed page. | Minor/Major | Collapse adjacent short subsections into flowing prose. |
| Short sections in a row | Not 3+ consecutive sections under the word floor. | Major | Indicates scaffold rather than prose; rewrite. |

---

## 3. Citation Integrity

| Check | Criterion | Severity |
|---|---|---|
| `\cite{key}` has `.bib` entry | Every cited key exists in `references.bib`. | Critical |
| `.bib` entry used | Every `.bib` entry is cited at least once somewhere. | Minor |
| No duplicate keys | `.bib` has no two entries sharing a key. | Major |
| Required fields present | Author, year, title present on every entry; journal/booktitle per type. | Major |
| Year plausible | Entry year ≤ current year, not `XXXX` or `n.d.` when avoidable. | Minor |

Delegate malformed entries or DOI resolution to `citation-management`.

---

## 4. Code and Reproducibility Hygiene

### Path and environment

| Check | Criterion | Severity |
|---|---|---|
| No hard-coded absolute paths | No `/home/…`, `C:\\…`, `/Users/…` in scripts. | Critical |
| No absolute `setwd` / `os.chdir` | Working directory never set to an absolute path. | Critical |
| Relative data paths | All `read_csv` / `read.csv` / `read_dta` / `pd.read_*` / `fread` calls use relative paths. | Critical |
| Referenced files exist | Every data path referenced by a script resolves to a file on disk. | Critical |

### Randomness and reproducibility

| Check | Criterion | Severity |
|---|---|---|
| Seed before stochastic op | `set.seed(...)`, `np.random.seed(...)`, `random.seed(...)`, `torch.manual_seed(...)`, or `set seed ...` present before any call to `sample`, `bootstrap`, `rnorm`, `rbinom`, `np.random.*`, `random.*`, train/test split, or MCMC. | Critical |
| Single source of truth for seed | One declared seed, reused (not regenerated per script). | Minor |

### Data-loading and estimation correctness

| Check | Criterion | Severity |
|---|---|---|
| Column references assigned | Every `df$colname` / `df["colname"]` in downstream code is produced earlier in the pipeline. | Major |
| Join types compatible | Join keys share a type; coerced types are documented. | Major |
| N logged around filters | `filter`, `subset`, `.loc`, `where`, `drop_na` calls log N before and after. | Minor |
| Explicit NA handling | Regressions declare `na.action` or `dropna()` policy; default listwise noted. | Major |
| Model convergence checked | Optimizers and GLMs report convergence; non-convergence surfaced. | Major |

### Runner and manifest

| Check | Criterion | Severity |
|---|---|---|
| `run_all.sh` (or equivalent) exists | A top-level script runs the full pipeline. | Major |
| Every main script listed | Each analysis script is called by the runner. | Major |
| No orphan main scripts | Scripts present in `code/` are either called by the runner or documented as utilities. | Minor |
| Data manifest present | `data/raw/manifest.md` documents source, URL, retrieval date, license. | Major |

Delegate executable end-to-end verification to `replication-driven-research`.

---

## 5. Tables and Figures Quality

### Tables

| Check | Criterion | Severity | Remediation |
|---|---|---|---|
| `booktabs` rules | Uses `\toprule`, `\midrule`, `\bottomrule`; no `\hline`. | Minor | Replace rules; add `\usepackage{booktabs}`. |
| `threeparttable` when notes | Tables with notes use `threeparttable` or equivalent. | Minor | Wrap table; move notes into `tablenotes`. |
| Self-contained caption | Caption names the outcome, sample, method, and period. | Major | Rewrite caption; include enough for stand-alone reading. |
| Column units declared | Units stated in caption or column header. | Major | Add units. |
| Significance convention explicit | Stars or explicit p-values documented in notes. | Major | State the convention once, in the notes. |
| **No margin overflow** | No `Overfull \hbox` warning for the table in `output/logs/paper.log` (or the run of `compile-latex`). | Major | `\resizebox{\textwidth}{!}{...}` or `\begin{adjustbox}{width=\textwidth}`, landscape rotation, or narrow columns. |

### Figures

| Check | Criterion | Severity | Remediation |
|---|---|---|---|
| Vector format | Files are `.pdf`, `.eps`, or `.svg`; no `.png`/`.jpg` unless inherently raster. | Major | Re-export from the plotting script as PDF. |
| Self-contained caption | Caption describes axes, sample, method. | Major | Rewrite caption. |
| Legible fonts | Axis text readable at print size. | Minor | Increase font size in the generating script. |
| Color-blind safe | Uses viridis / okabe-ito / other CB-safe palette. | Minor | Change palette in the generating script. |

For remediation patterns, reference `tables-and-figures`.

---

## 6. AI-Pattern Surface Scan

### Word-density targets (per 1000 words of prose)

| Token | Threshold | Severity when exceeded |
|---|---|---|
| "leverage" (verb) | 0 | Minor |
| "delve into" | 0 | Minor |
| "multifaceted" | 0 | Minor |
| "comprehensive" | ≤ 1 | Minor |
| "landscape" (non-literal) | ≤ 1 | Minor |
| "notably" / "furthermore" | ≤ 1 | Minor |
| "it is important to note" | 0 | Minor |
| "shed light on" / "pave the way" | 0 | Minor |
| "pivotal" / "groundbreaking" | 0 | Minor |
| "utilize" (instead of "use") | 0 | Minor |
| "underscore" | ≤ 1 | Minor |
| "intricate" / "tapestry" | 0 | Minor |

Report counts per section. Report exact file:line examples for the top 3 offenders.

### Em-dash density

| Check | Criterion | Severity |
|---|---|---|
| Global density | `—` count per 1000 words of prose ≤ 2. | Minor |
| Per-section density | No section exceeds 4 em-dashes per 1000 words. | Minor |
| Examples attached | Report first 5 occurrences with file:line. | — |

Some em-dashes are legitimate. The aim is to surface density and examples so the user decides.

### Rhythm

| Check | Criterion | Severity |
|---|---|---|
| Sentence-length variance | < 80% of sentences in any section within ±3 words of the mean. | Minor |
| Paragraph-length variance | Paragraphs vary in length within each section. | Minor |
| List overuse in prose body | No numbered or bullet lists inside Introduction or Discussion. | Minor |

For deeper prose critique, reference `paper-writing` and its `review-checklist.md`.

---

## 7. Language Consistency

| Check | Criterion | Severity |
|---|---|---|
| Declared language matches prose | `paper_language` from `CLAUDE.superpapers.md` matches detected prose language. | Major |
| No mixed-language passages | No paragraphs in a language other than the main one (quotations and names excepted). | Minor |
| Report in paper language | The audit report is written in the paper's language. | Critical (self-check) |

---

## Severity Summary Rules

- Any Critical ⇒ overall verdict "no-go".
- Zero Critical, Majors present ⇒ "go with reservations — fix Majors before submission".
- Zero Critical, zero Major, Minors present ⇒ "go — minor polish suggested".
- Zero of all ⇒ "go".
