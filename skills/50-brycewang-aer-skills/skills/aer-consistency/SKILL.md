---
name: aer-consistency
description: Use when auditing a finished or near-finished AER, AER:Insights, or AEJ manuscript for internal consistency: headline numbers across abstract, introduction, results, and tables; sample sizes; log-point and percentage-point conversions; cross-references; and in-text-citation/bibliography matching. Apply after the body and exhibits exist, before aer-referee-sim and aer-submission.
---

# AER Consistency

## Overview

Referees and editors run cheap integrity checks before engaging with ideas:
does the abstract's number appear in the tables? Do the Ns add up? Does
"Table 4" exist? Does every citation resolve? A single mismatch reframes the
entire report from "is this right?" to "what else is wrong?" — and for
AI-assisted manuscripts these mismatches are the **modal failure**, because
text and tables are often generated in separate passes.

This skill is the full-manuscript integrity audit. It is mechanical by
design: every check below has a yes/no answer obtained by comparing two
artifacts, not by judgment. Run it after every revision round, not only
before first submission.

## When to Use

- The body sections and exhibits exist and the manuscript is being assembled
- After an R&R revision, when numbers and exhibit ordering changed
- Before `aer-referee-sim` (so the simulated referees attack substance, not
  typos) and before `aer-submission`
- Any time results were re-run — even "tiny" re-runs desynchronize text

## Audit 1 — The Headline-Number Register

Build a register of every number that appears more than once in the
manuscript, then verify each row against its single source of truth (the
table or the replication output):

```text
NUMBER            SOURCE            ABSTRACT  INTRO  RESULTS  CONCL  MATCH
4.2 log points    Tab 3 col 4       yes       yes    yes      yes    OK
s.e. 1.1          Tab 3 col 4       yes       no     yes      no     OK
$84 billion       cited source      no        yes    no       yes    OK
N = 37,824        Tab 1             no        no     yes      no     OK
```

Rules:

- Every quoted estimate matches its table to the **digit**, including the
  standard error. No re-rounding in prose: if the table says 0.042 (0.011),
  the text says 4.2, not 4 or 4.20.
- The abstract, introduction, and conclusion quote the *same* headline
  specification. Quoting column 3 in the abstract and column 4 in the intro
  is a real and common failure.
- Externally sourced numbers (the hook's "$84 billion") carry a citation at
  first use, and the same value everywhere.

## Audit 2 — Sample-Size Integrity

- The Data section's sample funnel arithmetic is exact: raw N minus each
  documented drop equals the analysis N.
- The analysis N in Table 1 equals the N in the main results table for the
  matching specification; every deviation (balanced panel, IV subsample) is
  explained in the table notes and the text.
- Observation counts are consistent with the unit of analysis (12,400
  county-years from 620 counties × 20 years — check the multiplication).
- Heterogeneity subsample Ns sum to the full-sample N (minus documented
  exclusions).

## Audit 3 — Units and Conversions

The conversion table for prose claims about coefficients:

| Outcome form | Coefficient β means | Exact percent effect |
|---|---|---|
| log(Y), binary D | 100·β log points | 100·(e^β − 1) |
| log(Y), log(X) | elasticity | β% per 1% of X |
| Y in levels, binary D | β units of Y | 100·β / mean(Y) |
| Y is a rate (share) | β·100 **percentage points** | 100·β / baseline rate **percent** |

Checks:

- Every "percent" vs. "percentage point" usage verified against the
  outcome's units. A coefficient of 0.02 on an employment *rate* is 2
  percentage points; on *log* employment it is 2.0 percent (exactly 2.02).
- The exact exponential conversion used whenever |β| > 0.10; 0.31 log points
  is 36 percent, not 31.
- Standardized effects state which SD (cross-sectional? within? whose
  sample?) and the SD's value.
- Currency years and deflators consistent across all sections; one base
  year, named.
- Signs: a negative coefficient on an inverted scale narrated correctly —
  the most embarrassing class of referee catch.

## Audit 4 — Stars, Standard Errors, and Stated Significance

- For each starred coefficient, |β/se| is consistent with the stars under
  the declared convention (1.65 / 1.96 / 2.58 thresholds approximately).
- Every prose claim of "significant at the X percent level" matches the
  table's stars and the CI.
- Claims of "no effect" are backed by a CI the text reports, not by absence
  of stars (see `aer-robustness` on null-result discipline).
- One star convention across all tables (`aer-tables-figures` sets it; this
  audit verifies it held).

## Audit 5 — Cross-Reference Integrity

- Every `\ref` / `\autoref` resolves; no "Table ??" anywhere in the PDF.
- Every table and figure is referenced in the text at least once, in order
  of first reference; exhibits nobody cites get cut or moved to the
  appendix.
- Section references survive renumbering ("see Section V" after V became
  IV is the classic R&R injury).
- Appendix references point to existing appendix objects, including the
  supplemental file if separate.
- Equation references match the renumbered equations.

## Audit 6 — Citation Two-Way Match

- Every in-text citation has a bibliography entry; every bibliography entry
  is cited at least once. LaTeX builds with zero unresolved citation
  warnings.
- Author spellings and years in text match the entries (Cattaneo 2020 in
  text, 2019 in the bib — fail).
- The deeper verification — that entries are real and claims accurate — is
  `aer-literature`'s integrity protocol; this audit confirms it was run and
  the ledger has no open rows.

## Audit 7 — Claim-Evidence Map

For each *empirical claim* in the abstract, introduction, and conclusion,
record where the evidence lives:

```text
CLAIM                                          EVIDENCE          STATUS
"raises 90/10 ratio by 4.2 log points"         Tab 3 c4          OK
"driven by gains at the top"                   Fig 3 / Tab 4     OK
"absent in retail and construction"            Tab 5 c2-c3       OK
"consistent with skill-biased adoption"        Sec V battery     OK (consistency claim)
```

- Causal claims trace to design-based exhibits; mechanism claims are
  worded as consistency ("consistent with"), matching `aer-paper-body`
  rules.
- Any claim with no exhibit or citation is rewritten or deleted — "we find"
  with nothing to point at is how overclaiming enters a manuscript.

## Mechanical Procedure

1. Run the bundled script for the deterministic LaTeX checks (citations
   two-way, ref/label two-way, duplicate labels, abstract word count):

   ```bash
   python3 skills/aer-consistency/scripts/audit_manuscript.py paper.tex references.bib
   ```

2. Extract every number from the abstract and introduction (grep for
   digits); locate each in a table or a cited source; build the register.
3. Recompute the sample funnel and the unit conversions by hand — these are
   arithmetic, not judgment.
4. Diff the table files in the manuscript against the replication package's
   `output/tables/` — they must be the same files, not lookalikes
   (`aer-replication` requires this anyway).
5. Produce the consistency report (below) and fix every FAIL before
   handing off.

## The Consistency Report

```text
AUDIT                       RESULT     DETAIL
1 headline numbers          PASS       12 numbers, 12 matched
2 sample sizes              FAIL       Tab 4 N=37,824 vs Tab 1 N=37,284
3 units and conversions     PASS       2 exact conversions applied
4 stars vs SEs              PASS
5 cross-references          PASS       31 refs, 0 dangling
6 citations two-way         FAIL       2 bib entries uncited
7 claim-evidence map        PASS       9 claims mapped
```

Fix-and-rerun until all PASS. The report travels with the handoff so
`aer-referee-sim` and `aer-submission` know the floor is solid.

## Common Failure Modes

- Tables regenerated after the prose was written, desynchronizing every
  quoted estimate
- Abstract edited for word count, changing "4.2" to "about 4" while the
  tables stayed exact
- Percentage points and percent swapped exactly once, in the abstract
- Two tables both numbered 3 after an R&R reshuffle
- The conclusion claiming a mechanism the Results section only called
  "suggestive"

## Repository Resources

When working from the AER-skills repository or plugin bundle, load only the
relevant resource:

- Exhibit-to-script mapping that fixes each number's source of truth:
  `examples/replication-package-skeleton/docs/exhibit-register.md`
- Narration rules the claim-evidence map enforces:
  `skills/aer-paper-body/SKILL.md`
- Citation verification protocol behind Audit 6:
  `skills/aer-literature/SKILL.md`
- Prose-level conventions for units and significance language:
  `docs/style-guide.md`

## Handoff

```text
AUDITS PASSED: <n>/7
HEADLINE NUMBERS MATCHED: <n>/<n>
OPEN FAILURES: <list, or "none">
ABSTRACT WORD COUNT: <n>/100
CITATION LEDGER: <closed / open rows remain>
NEXT SKILL: <aer-referee-sim | aer-submission>
```

## Anti-Patterns

- Running this audit once, before first submission only — every revision
  reopens it
- "The numbers are close enough" — referees diff digits, not vibes
- Fixing the prose to match a table without checking which one the
  replication package actually produces
- Treating a FAIL as a note for later instead of a blocker for handoff
- Auditing by re-reading instead of by register — unstructured re-reading
  finds style issues and misses arithmetic
