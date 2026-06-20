# Paper Review — <paper title or folder name>

- **Date:** <YYYY-MM-DD HH:MM>
- **Paper root:** <absolute path>
- **Paper language:** <paper_language>
- **Reviewer:** `paper-review` skill (superpapers)
- **Verdict:** <Go | Go with reservations | No-go>

## Executive Summary

<3–5 sentences: what was audited, what the overall state is, the top blocker (if any), and what the user should do next.>

**Finding counts**

| Severity | Count |
|---|---|
| Critical | <n> |
| Major | <n> |
| Minor | <n> |
| Inconclusive | <n> |

---

## Critical Issues (blocks submission)

For each finding:

### C1. <short title>

- **Location:** `<file>:<line>`
- **What:** <what is wrong>
- **Why it blocks:** <why this prevents submission>
- **Fix:** <concrete remediation, including a code or prose snippet when useful>

<repeat for C2, C3, …>

If none: `No Critical findings.`

---

## Major Issues (should fix before submission)

### M1. <short title>

- **Location:** `<file>:<line>`
- **What:** <description>
- **Why:** <impact on the paper>
- **Fix:** <concrete remediation>

<repeat for M2, M3, …>

If none: `No Major findings.`

---

## Minor Issues (nice to fix)

### m1. <short title>

- **Location:** `<file>:<line>`
- **What:** <description>
- **Fix:** <concrete remediation>

<repeat for m2, m3, …>

If none: `No Minor findings.`

---

## Cross-Cutting Findings by Dimension

### Numerical consistency

<summary of checks run, with any discrepancies listed file:line ↔ source file:line. If no discrepancies, one line: "All sampled numbers match their source within tolerance.">

### Narrative coherence and structure

<summary: abstract/intro/results/conclusion alignment; literature dialogue in Discussion and Results; structural flow (short sections, subheading density).>

### Citation integrity

<summary: `\cite` ↔ `.bib` coverage, orphan entries, duplicates. Numbers: X cite keys, Y bib entries, Z cited, W orphaned.>

### Code and reproducibility hygiene

<summary: hard-coded paths, seeds, NA handling, runner completeness, manifest. List blocking items here; full per-file findings in Major/Critical sections.>

### Tables and figures quality

<summary: booktabs compliance, vector figures, captions, margin overflow. Count of `Overfull \hbox` warnings in tables.>

### AI-pattern surface scan

<summary: banned-word counts, em-dash density global and per section, sentence-length variance. Top 3 offenders listed.>

### Language consistency

<summary: declared vs detected language, mixed-language passages.>

### Inconclusive steps

<list of steps that could not run and why — e.g., "Compilation log not present and LaTeX not available in this environment.">

---

## Remediation Checklist

Ordered by severity. Each item references the finding ID for traceability.

- [ ] C1 — <one-line summary>
- [ ] C2 — <one-line summary>
- [ ] M1 — <one-line summary>
- [ ] M2 — <one-line summary>
- [ ] m1 — <one-line summary>
- [ ] m2 — <one-line summary>

---

## Deep-Dive References

If deeper work is needed on specific dimensions, escalate to the sibling skill:

- **Prose rewriting and 100-point rubric** → `paper-writing` (see `references/review-checklist.md`).
- **Additional robustness checks** → `robustness-checks`.
- **End-to-end reproducibility verification** → `replication-driven-research`.
- **Bibliography repair, DOI resolution, duplicate merging** → `citation-management`.
- **Table and figure remediation patterns** → `tables-and-figures`.
- **LaTeX compilation and log inspection** → `compile-latex`.
- **Journal-specific formatting** → `journal-guidelines`.

---

## Notes for the User

<free-form notes: anything the user should think about that does not fit a severity bucket. Example: observed strengths; pieces of the audit that required assumptions; suggested order for remediation.>
