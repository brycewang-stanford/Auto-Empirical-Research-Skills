# Full-Manuscript Audit Checklist

*Bundled with the `aer-consistency` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

The manual passes below are mechanical by design: every check has a yes/no
answer obtained by comparing two artifacts, not by judgment. Run them by
register, not by re-reading — unstructured re-reading finds style issues and
misses arithmetic. Order matters only in that the script pass (last section)
should run first, so the manual passes start from a manuscript with zero
dangling references or citations.

## Pass 1 — Numbers in Text vs. Tables

**What to check.** Every number in prose traces to an exhibit cell or a
cited source, to the digit, including standard errors. The abstract,
introduction, results, and conclusion quote the *same* headline
specification. No re-rounding: if the table says 0.042 (0.011), the text
says 4.2, not 4 or 4.20.

**How to check fast.** Grep the abstract and introduction for digits; build
a register with one row per repeated number:

```text
NUMBER            SOURCE            ABSTRACT  INTRO  RESULTS  CONCL  MATCH
4.2 log points    Tab 3 col 4       yes       yes    yes      yes    OK
N = 37,824        Tab 1             no        no     yes      no     OK
```

**Failure examples.** Abstract edited for word count, changing "4.2" to
"about 4" while the tables stayed exact; abstract quoting column 3 while the
intro quotes column 4; tables regenerated after the prose was written.

## Pass 2 — Sample Funnel Consistency

**What to check.** N is consistent at every stage: raw N minus each
documented drop equals the analysis N; Table 1's N equals the main results
table's N for the matching specification; heterogeneity subsample Ns sum to
the full-sample N minus documented exclusions; observation counts match the
unit of analysis (620 counties × 20 years = 12,400 county-years).

**How to check fast.** Copy every N in the manuscript into one column and do
the arithmetic by hand — this is subtraction and multiplication, not
judgment. Any deviation (balanced panel, IV subsample) must be explained in
the table notes and the text.

**Failure examples.** Tab 4 N=37,824 vs. Tab 1 N=37,284 (transposed digits);
a funnel whose drops sum to 3,012 while raw-minus-analysis is 3,102; decile
subsamples that sum to more than the full sample.

## Pass 3 — Log Points vs. Percent Conversions

**What to check.** Every "percent" vs. "percentage point" usage against the
outcome's units, using this conversion table:

| Outcome form | Coefficient β means | Exact percent effect |
|---|---|---|
| log(Y), binary D | 100·β log points | 100·(e^β − 1) |
| log(Y), log(X) | elasticity | β% per 1% of X |
| Y in levels, binary D | β units of Y | 100·β / mean(Y) |
| Y is a rate (share) | β·100 **percentage points** | 100·β / baseline rate **percent** |

**How to check fast.** List every coefficient narrated in prose with its
outcome form; recompute the stated conversion. Use the exact exponential
whenever |β| > 0.10 (0.31 log points is 36 percent, not 31). Verify
standardized effects name which SD and its value; one currency base year,
named; negative coefficients on inverted scales narrated correctly.

**Failure examples.** A 0.02 coefficient on an employment *rate* narrated as
"2 percent" (it is 2 percentage points); percentage points and percent
swapped exactly once, in the abstract; a fall in an inverted index narrated
as a decline in the underlying outcome.

## Pass 4 — Internal Cross-References

**What to check.** Every table, figure, section, and equation reference
points at the right object: no "Table ??"; exhibits numbered in order of
first reference; every exhibit cited in the text at least once; section
references survive renumbering; appendix references point to existing
appendix objects.

**How to check fast.** The bundled script catches dangling and unused
LaTeX labels mechanically. Manually verify the *semantic* layer: read each
"see Table 4" and confirm Table 4 shows what the sentence claims, and scan
section references after any restructuring.

**Failure examples.** "See Section V" after Section V became IV in an R&R
reshuffle; two tables both numbered 3; a reference to "the placebo in Table
6" that now lives in Table A.2.

## Pass 5 — Citation Two-Way Match

**What to check.** Every in-text citation has a bibliography entry and every
bibliography entry is cited at least once; author spellings and years in
text match the entries exactly.

**How to check fast.** The bundled script does the key-level two-way match.
Manually spot-check the surface forms: the year printed in prose against the
bib entry's year, and hyphenated or multi-part surnames against the entry.

**Failure examples.** A 2020 paper cited as 2019 in text; a bib entry left
over from a cut paragraph, never cited; the same work entered twice under
two keys, cited under both.

## Pass 6 — Exhibit Self-Containedness

**What to check.** Every table and figure note defines everything needed to
read the exhibit without the text: estimator, sample and its N, unit of
observation, clustering level and number of clusters, CI or SE type, star
convention, variable definitions and units, data source, and fixed effects.
One star convention across all tables.

**How to check fast.** For each exhibit, cover the body text and ask: could
a referee reading only this page reproduce the column headers and interpret
the cells? Any term in the exhibit not defined in its note fails.

**Failure examples.** A figure note that omits the CI type and N; two table
notes that omit the number of clusters; column header "Full controls" with
the control set defined only in Section IV.

## Pass 7 — Terminology Consistency

**What to check.** One name per variable and per concept, everywhere: the
same treatment is not "broadband subsidy," "CAF funding," and "the program"
in three sections; variable names in exhibits match the names in prose;
acronyms defined once and used consistently.

**How to check fast.** Build a two-column glossary (concept, canonical name)
from the Data section, then grep for each synonym you remember writing.
Check that the outcome named in the abstract is the outcome named in the
tables.

**Failure examples.** "90/10 ratio" defined in levels in Section II and used
in logs in Section IV; "wage inequality" in the abstract vs. "earnings
dispersion" in the tables; an acronym introduced twice with different
expansions.

## Running the Bundled Script

The deterministic LaTeX checks are automated by the script shipped inside
this skill at `scripts/audit_manuscript.py` (path relative to the skill
directory). It needs only the Python standard library and never compiles the
LaTeX:

```bash
python3 scripts/audit_manuscript.py paper.tex references.bib
python3 scripts/audit_manuscript.py manuscript_dir/ references.bib \
  --claim-ledger docs/claim-evidence-ledger.csv
```

It checks: citations two-way (every cite-family key has a bib entry and vice
versa), cross-references two-way (every ref has a label and every label is
referenced), duplicate labels and duplicate bib keys, the abstract word
count against the AEA 100-word limit, and — when a claim-evidence ledger CSV
is present or passed — that each claim row maps to an existing label, cited
bib key, or file and carries a closed status (`--allow-open-claims` relaxes
the status check). Exit status 0 means all deterministic checks passed, so
it can gate a Makefile target or an agent loop.

**What the script does NOT catch** — every manual pass above remains
required:

- Whether a prose number matches the table cell it cites (Pass 1)
- Sample funnel arithmetic and N reconciliation across tables (Pass 2)
- Log-point/percent/percentage-point conversion errors (Pass 3)
- Whether a resolving reference points at the *right* exhibit, or exhibits
  appear in order of first reference (Pass 4)
- Author-spelling and year mismatches between prose and bib entry, and
  whether cited works are real and support the claim (Pass 5)
- Missing information in exhibit notes and star-convention drift (Pass 6)
- Terminology drift (Pass 7)
- Stars vs. standard errors, and "significant at X percent" claims

Fix-and-rerun until the script and all seven passes report PASS; the
consistency report travels with the handoff.

## Canonical repo sources

Distilled from these repository files (they require the repository checkout):

- `skills/aer-consistency/SKILL.md` — the seven audits, the mechanical
  procedure, and the consistency-report format
- `skills/aer-consistency/scripts/audit_manuscript.py` — the deterministic
  checker (also bundled inside this skill)
- `examples/replication-package-skeleton/docs/claim-evidence-ledger.csv` —
  the ledger template the script validates
- `docs/style-guide.md` — prose-level conventions for units and significance
  language
