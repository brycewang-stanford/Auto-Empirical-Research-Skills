---
name: paper-review
description: Use when a paper is complete or near-complete and a holistic pre-submission audit is needed. Cross-cuts text, code, tables, figures, results, citations, and reproducibility in a single pass and produces a persistent audit report. Works standalone on papers written outside the plugin.
---

# Paper Review

## Overview

This skill runs a terminal, cross-cutting audit before submission. It is not a deep prose critic (that is `paper-writing`), not a statistical robustness reviewer (that is `robustness-checks`), not a reproducibility verifier (that is `replication-driven-research`). Instead, it detects the seams between those skills — numerical inconsistency across the manuscript, narrative incoherence between sections, missing literature dialogue, LaTeX overflow, script errors in data pipelines, stylistic tells of AI writing — in one pass, and writes a single consolidated report with severity-ranked findings and a go/no-go verdict.

The skill is standalone. It works on any paper folder, whether produced by the superpapers pipeline or not. When the canonical layout is absent, it asks the user for the paths it needs.

## When to Use

- The paper is drafted, tables and figures are in place, and the user wants a final check before submission.
- An external collaborator delivered a manuscript and you need a structured audit.
- The `execute-plan` skill has finished and suggested this step.
- After a major revision cycle, before re-submitting.
- The user asks for "a full paper review", "pre-submission audit", or "audit my paper".

Do not use this skill:

- Before the paper is substantially drafted — without text there is nothing to audit. Use `paper-writing` instead.
- For deep prose rewriting. That is `paper-writing`.
- To design or run additional robustness checks. That is `robustness-checks`.
- To verify end-to-end reproducibility execution. That is `replication-driven-research`.

## Mandatory Steps

1. **Discover the paper structure.** Locate: `paper.tex` (or the equivalent main TeX file), `references.bib`, `output/tables/`, `output/figures/`, `output/logs/`, the code directory, `run_all.sh`. Walk up from the working directory. If any essential path is missing, ask the user via AskUserQuestion with concrete options (include "Other" for custom paths). Record the paths for reuse. Do not assume `CLAUDE.superpapers.md` or `docs/superpapers/plans/` exist — the skill must work on externally authored papers.

2. **Inventory artifacts.** List every file relevant to the audit by category: prose files (`.tex`), bibliography (`.bib`), table files (`output/tables/*.tex`), figure files (`output/figures/*.pdf`), code (`.R`, `.py`, `.do`, `.jl`, etc.), logs, and the data manifest. Store the inventory for reuse across subsequent steps.

3. **Numerical consistency.** Extract numbers from the paper prose — percentages, point estimates, standard errors, sample sizes, R², test statistics, p-values. Cross-check each against its source: the `output/tables/*.tex` file it came from, or the log in `output/logs/` that produced it. Any discrepancy beyond a reasonable rounding tolerance (default: last reported digit of the paper figure) is a **Critical** finding. Report both paper location (`file:line`) and source location.

4. **Narrative coherence and structure.**
   - *Coherence:* abstract ↔ introduction ↔ results ↔ conclusion must agree on research question, main result with magnitude, identification strategy, and key caveats. Divergence — abstract says "12% effect", conclusion says "around 10%" — is a **Major** finding.
   - *Literature dialogue:* Results and Discussion sections must cite prior literature, comparing the paper's findings against cited papers rather than merely reporting numbers in isolation. A Discussion section with zero `\cite{}` is a **Major** finding. Fewer than one citation per page of prose in Discussion or Results is a **Major** gap.
   - *Structural flow:* flag any `\section`, `\subsection`, or `\subsubsection` whose body is under 80 words. Flag pages where the density of subheadings suggests over-fragmentation (roughly ≥3 subheadings in one page's worth of text). Over-fragmentation is **Minor** with a suggested merge; severely choppy writing — multiple short sections in a row — escalates to **Major**.

5. **Citation integrity.** Every `\cite{key}` must have a matching entry in `.bib`. Every `.bib` entry must be cited at least once. No duplicate keys. For malformed entries or missing required fields, delegate to `citation-management`.

6. **Code and reproducibility hygiene.** Scan scripts in the code directory for:
   - Hard-coded paths: `/home/...`, `C:\\...`, absolute URLs to local disks.
   - Non-relative working directory changes: `setwd("/...")`, `os.chdir("/...")`.
   - Missing seeds: any script calling `sample()`, `bootstrap`, `rnorm`, `np.random`, `random`, or train/test splits must set a seed before.
   - Data loading: `read_csv`, `read.csv`, `read_dta`, `pd.read_*`, `fread` — the path must be relative, and the referenced file must exist in the repo.
   - Column references that do not match the data schema (`df$colname` / `df["colname"]` where `colname` is never assigned in the pipeline).
   - Silent NA handling: regressions called without an explicit `na.action` or `dropna()`, joins with type mismatches, filters (`filter`, `subset`, `.loc`, `where`) chained without logging N before and after.
   - `run_all.sh` (or equivalent) exists and lists every script in the order they must run. Scripts present on disk but not referenced by the runner are flagged as orphaned.
   - `data/raw/manifest.md` (or equivalent) documents sources, retrieval dates, and licenses.

   For executable end-to-end verification, delegate to `replication-driven-research`. Findings are **Critical** when they block reproducibility (hard-coded paths, missing seeds in stochastic scripts, orphaned main scripts, missing data file referenced by a script), and **Major** otherwise.

7. **Tables and figures quality.**
   - Tables in `output/tables/*.tex` use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`). Table notes use `threeparttable` when present.
   - Figures in `output/figures/` are vector (`.pdf`, `.eps`, `.svg`). Raster images (`.png`, `.jpg`) are a **Major** finding unless the figure is inherently raster (maps with imagery).
   - Captions must be self-contained — a reader should understand the table or figure from the caption alone.
   - **Margin overflow.** If a compilation log exists at `output/logs/paper.log` or the paper directory, parse it for `Overfull \hbox` warnings inside table environments. If no log exists, invoke `compile-latex` to produce one. Each overflow is a **Major** finding localized to the table with suggested remediation: `\resizebox{\textwidth}{!}{...}`, `adjustbox`, landscape rotation, or column narrowing. For deeper remediation patterns, reference `tables-and-figures`.

8. **AI-pattern surface scan.**
   - *Banned-word density.* Count occurrences of "leverage", "delve into", "landscape" (non-literal), "multifaceted", "notably", "furthermore", "comprehensive", "pivotal", "groundbreaking", "shed light on", "pave the way", "tapestry", "intricate", "underscore", "it is important to note", "utilize". Density above 1 per 1000 words of prose is flagged with counts and locations.
   - *Em-dash overuse.* Count `—` (U+2014) per section and per 1000 words of prose. Default threshold: above 2 per 1000 words is flagged as **Minor** with example occurrences. Some em-dashes are legitimate; the aim is to surface overuse for the user to audit. Report per-section density so regional overuse is visible.
   - *Uniform sentence length.* If more than 80% of sentences in any section fall within a ±3-word band, flag as **Minor**.
   - For deeper prose rewriting, reference `paper-writing` and its `review-checklist.md`.

9. **Language consistency.** Detect the paper's main language first from `CLAUDE.superpapers.md`'s `paper_language`, then heuristically (character sets, common words). Flag prose passages in a different language from the declared one. The audit report itself must be written in the same language as the paper.

10. **Generate the consolidated report.** Create `docs/superpapers/review/` if absent. Write `audit-YYYYMMDD-HHMM.md` using the template at `references/report-template.md`. Populate every section. Each finding has: severity (Critical / Major / Minor), location (`file:line`), description, suggested fix. Mark any step that could not run (no compilation log and no LaTeX installed, for example) as "Inconclusive" with the reason — never silently skip.

11. **Deliver the summary and offer remediation.** In chat, present: finding counts by severity, report path, and go/no-go verdict. "Go" requires zero Critical findings. Offer via AskUserQuestion to remediate findings one at a time, starting with Critical. Never edit without per-finding approval. Never apply a batch fix.

## Standalone vs Integrated Mode

When `CLAUDE.superpapers.md` is present, the skill inherits `paper_language`, `target_journals`, `significance_convention`, and any custom rules. When absent, the skill proceeds with defaults: paper language detected heuristically, rounding tolerance at the last reported digit, significance at 5%, em-dash threshold at 2 per 1000 words, banned-word threshold at 1 per 1000 words. The skill must function on externally authored papers, where none of the plugin's artifacts exist.

## Severity Taxonomy

- **Critical** — blocks submission. Examples: numerical discrepancy paper ↔ source; hard-coded absolute paths in main scripts; missing seed in a stochastic script; missing raw data file referenced by the pipeline; table overflow that prevents rendering.
- **Major** — should fix before submission. Examples: Discussion without citations; raster figure that should be vector; narrative divergence between abstract and conclusion; `Overfull \hbox` in a table; orphaned `.bib` entries in bulk.
- **Minor** — nice to fix. Examples: em-dash density above threshold; a single short subsection; uniform sentence length in one section.

## Anti-Patterns

- Running any mandatory step without first reading `paper.tex` end to end.
- Duplicating the 100-point rubric from `paper-writing/references/review-checklist.md`. This skill flags issues at the seams and refers deep prose critique out.
- Re-executing every robustness check listed in the paper. That is `robustness-checks`. Here we only verify that the checks the paper claims were executed actually exist as scripts and outputs.
- Applying fixes automatically. Every remediation requires explicit user approval per finding.
- Producing a report in a language different from the paper's declared `paper_language`.
- Issuing a "go" verdict while any Critical finding is unresolved.
- Silently omitting a step that could not run. Every un-runnable step must be recorded as "Inconclusive" with the reason.
- Treating absence of evidence as evidence of absence. If logs are missing and compilation was not possible, say so in the report.
- Flagging every em-dash or every long sentence. The skill surfaces density and examples so the user decides; it does not moralize.

## Verification Before Completion

- [ ] `docs/superpapers/review/audit-YYYYMMDD-HHMM.md` exists.
- [ ] Every dimension (steps 3–9) has a populated section or an explicit "Inconclusive" with reason.
- [ ] All findings carry severity (Critical / Major / Minor) and location (`file:line`).
- [ ] Go/no-go verdict is explicit and consistent with findings (zero Critical ⇒ go).
- [ ] Remediation checklist exists, ordered by severity.
- [ ] User received the executive summary in chat with the report path.
- [ ] Report is written in the paper's declared language.
- [ ] No fix was applied without explicit user approval.
