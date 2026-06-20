# Example Pre-Submit Report (Toy Conjoint Manuscript)

Worked example showing what the `paper-review-lite` skill produces after all 11 agents run.
Manuscript: *Do Voters Punish Coalition Defectors? Evidence from a Paired-Choice Conjoint*
(fictional; for illustration only).

---

## Pre-Submit Report: Do Voters Punish Coalition Defectors?
Date: 2026-04-18
Issues: 3 critical, 5 recommended, 4 minor

### Critical Issues (must fix before submission)

- `[CRITICAL]` `paper.tex:312` — Abstract reports AMCE = **-0.082 (SE 0.011)** for the "coalition defector" attribute; Table 2 row 4 reports **-0.074 (SE 0.013)**. Numbers must match. Fix: reconcile the estimate; likely a stale paste from pilot data.
- `[CRITICAL]` `paper.tex:488` — Agent 7 flagged a **silent deviation**: the PAP (OSF osf.io/xxxx, registered 2025-09-14) pre-registers the primary DV as *forced choice*, but the paper reports a *rating-scale* DV as primary with no deviations section. Fix: either re-designate rating-scale as secondary and report forced-choice primary, or add a deviations subsection justifying the switch.
- `[CRITICAL]` `replication/README.md:1` — Agent 9 could not reproduce Table 3: script `04_heterogeneity.R` references `data/cleaned_v2.csv` but the archive ships only `cleaned_v1.csv`. Fix: include the correct input file or a build script that produces it.

### Recommended Changes (should fix, not blocking)

- `[RECOMMENDED]` `paper.tex:156` — Agent 6 (CONSORT): no baseline-balance table across the two conjoint task orders (A-then-B vs. B-then-A). With N=2,412, even small assignment imbalances can bias AMCEs. Fix: add SI Table A.1 with standardized mean differences.
- `[RECOMMENDED]` `paper.tex:201` — Agent 6: attrition is reported as an aggregate **7.8%**, not by arm. Differential attrition between order conditions (4.2% vs. 11.1%) is material. Fix: break out attrition by arm and add a one-paragraph sensitivity discussion.
- `[RECOMMENDED]` `paper.tex:445` — Agent 7: the Heterogeneity-by-Partisanship analysis is presented as a confirmatory test but is not in the PAP. Fix: move to an "Exploratory Analyses" subsection and label accordingly.
- `[RECOMMENDED]` `paper.tex:88` — Agent 2: p-values are reported to three decimals in-text but two in Table 2. Fix: standardize to three decimals throughout (JARS-Quant; Appelbaum et al. 2018).
- `[RECOMMENDED]` `paper.tex:523` — Agent 5: ethics statement names "the authors' home-institution IRB" but provides no protocol number. APSA 2020 HSR Principles §3.2 expects protocol identification. Fix: add the IRB protocol number.

### Minor Issues (nice to have)

- `[MINOR]` `paper.tex:45` — Agent 5: "defector" is sometimes "defector" and sometimes "defecting legislator." Pick one.
- `[MINOR]` `bib.bib:214` — Agent 3: Bansak et al. 2021 entry uses `@unpublished` but the paper appeared in *PSRM*. Update entry type.
- `[MINOR]` `bib.bib:67` — Agent 4: DOI missing for Hainmueller, Hopkins & Yamamoto 2014. Suggested: `10.1093/pan/mpt024`.
- `[MINOR]` `figures/figure-2.pdf` — Agent 8: color palette is not color-blind safe (red/green distinction). Consider viridis.

### Strengths (what is working well)

- Pre-registration on OSF with timestamped, public PAP and embedded analysis code (Agent 7).
- Transparent ITT analysis flagged clearly as primary; per-protocol reported as robustness (Agent 6).
- Replication archive has a codebook (`data/codebook.md`) and a table-to-script mapping; main-text AMCEs reproduce from `02_main_amces.R` with seed `20250914` (Agent 9).
- Abstract does not overclaim relative to body (Agent 1).

### Journal-Readiness Checklist

| Dimension                             | Status  | Notes |
|---------------------------------------|---------|-------|
| Compiles cleanly                      | PASS    | No LaTeX warnings. |
| Anonymized for double-blind           | PASS    | No self-identifying refs. |
| Argument & logic                      | PASS    | Agent 1: contribution positioned clearly. |
| Internal numerical consistency        | FAIL    | Abstract/table mismatch on headline AMCE. |
| References complete                   | PARTIAL | One bibtex entry-type wrong. |
| DOIs present                          | PARTIAL | 3 missing; suggested DOIs in Agent 4 output. |
| Writing quality                       | PASS    | One terminology inconsistency. |
| Figures/tables correct                | PARTIAL | Figure 2 palette; otherwise fine. |
| Formatting consistent                 | PASS    | |
| Abstract & keywords                   | PASS    | 147 words; 5 keywords. |
| Word/page count compliant             | PASS    | 9,842 / 10,000. |
| Replication archive ready             | FAIL    | Missing input file for Table 3. |
| CONSORT participant flow              | PARTIAL | Diagram present but no per-arm attrition. |
| ITT & baseline balance reported       | PARTIAL | ITT yes, balance table missing. |
| Attrition-by-arm reported             | FAIL    | Aggregate only. |
| Pre-registration deviations disclosed | FAIL    | Primary-DV switch is silent. |
| Data availability statement           | PASS    | Links to Dataverse; TOP Level 2. |
| Ethics/IRB statement                  | PARTIAL | Protocol number missing. |
| Preregistration disclosure            | PASS    | OSF link present. |
| AI use disclosure                     | MISSING | Add a one-line statement. |
| COI declaration                       | PASS    | |
| Funding/acknowledgments               | PASS    | |

### What Still Needs Your Input

1. IRB protocol number — please provide for line 523.
2. Data embargo status — the Dataverse link is restricted; confirm whether this is a publisher-accepted embargo or an oversight.
3. PAP-deviation justification — whichever DV is retained as primary, the Methods section needs a two-sentence rationale.
4. AI use during drafting — if any LLM assistance was used, add disclosure per journal policy.
