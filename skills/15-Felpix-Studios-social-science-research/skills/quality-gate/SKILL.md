---
name: quality-gate
description: >-
  Verify that every quantitative claim in the paper is traceable to an analysis output file, and that no important output was omitted. Make sure to use this skill whenever the user wants to check that the paper and analysis are consistent before submission. Triggers include: "run the quality gate", "check the paper matches the analysis", "verify consistency", "does the paper match my results", "check my numbers", "are my tables right", "quality check before submission", "verify my claims", "make sure everything is consistent", "double-check the paper against my output files", or any pre-submission integrity check between paper text and computed results.
argument-hint: "[paper file path, or leave blank to auto-detect]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task", "AskUserQuestion"]
---

# Quality Gate: Paper ↔ Analysis Consistency

Cross-check every numerical claim in the paper against analysis output files. Reports only — never edits.

**Input:** `$ARGUMENTS` — path to the paper draft, or leave blank to auto-detect.

---

## Step 1: Locate the Paper Draft

If `$ARGUMENTS` is provided, use that path. Otherwise glob for:
- `manuscripts/**/*.tex`
- `manuscripts/**/*.qmd`
- `manuscripts/**/*.md`

If multiple drafts found, use AskUserQuestion to let the user pick:
- header: "Paper"
- question: "Multiple drafts found. Which manuscript should I check?"
- options: list up to 4 found files (label: filename, description: path and file size). If more than 4, group by directory.

---

## Step 2: Extract Numerical Claims

Read the full manuscript and extract every quantitative claim:

- **Coefficients and standard errors** — e.g., "The effect is 0.23 (SE = 0.04)"
- **Sample sizes** — e.g., "N = 4,521 observations"
- **Percentages and proportions** — e.g., "42% of firms..."
- **Means, medians, ranges** — e.g., "average income of $45,000"
- **Table and figure references** — e.g., "Table 2 shows...", "as seen in Figure 1"
- **p-values and significance statements** — e.g., "statistically significant at the 1% level"

Record location (section, paragraph, line number if available) for each claim.

---

## Step 3: Inventory Output Files

Glob for all output files:
- `output/tables/**/*.tex` — regression and summary tables
- `output/tables/**/*.html` — HTML versions
- `output/figures/**/*.pdf`, `output/figures/**/*.png` — figures
- `output/**/*.rds`, `output/**/*.pkl`, `output/**/*.parquet`, `output/**/*.csv` — saved objects

Build an inventory with file paths and sizes.

---

## Step 4: Dispatch Verifier Agent

Dispatch the `verifier` agent via Task to perform the heavy verification work. Pass it:
- The full list of numerical claims extracted in Step 2 (with locations)
- The output file inventory from Step 3
- The paper draft path
- The bibliography file path

```
Task prompt: "You are the verifier agent. Paper draft: [path].
Bibliography: [bib path].

CLAIMS TO VERIFY:
[paste the full claims list from Step 2]

OUTPUT FILE INVENTORY:
[paste the inventory from Step 3]

Verify each claim against the output files. Then do a reverse check —
find output files NOT referenced in the paper. Then check all citation
keys against the bibliography. Follow the verifier agent instructions
and return your full verification report."
```

After the verifier completes, collect its results:
- Claim verification table (MATCHED / UNVERIFIED / MISSING FILE per claim)
- Unreferenced output files list
- Missing citation keys

---

## Step 5: Save Report

Save to `quality_reports/quality_gate_[YYYY-MM-DD]_[paper-name].md`:

```markdown
# Quality Gate Report: [Paper Name]
**Date:** [YYYY-MM-DD]
**Paper:** [file path]

## Verdict: PASS / CONDITIONAL PASS / FAIL

PASS = all claims matched, no missing citations, no unexplained unreferenced outputs
CONDITIONAL PASS = minor unverified claims or informational unreferenced outputs
FAIL = unverified critical claims or missing citations

---

## Claim Verification

| Claim | Location | Found in Output? | Source File | Status |
|-------|----------|-----------------|-------------|--------|
| β = 0.23 (SE = 0.04) | Section 4, para 2 | Yes | output/tables/main_regs.tex | MATCHED |
| N = 4,521 | Table 2 note | Yes | output/tables/main_regs.tex | MATCHED |
| 42% of firms | Intro, para 1 | No | — | UNVERIFIED |

---

## Unreferenced Outputs

Files in output/ not referenced in the paper:

| File | Size | Recommended Action |
|------|------|-------------------|
| output/tables/robustness_het.tex | 4.2 KB | Reference in Section 7 or explain exclusion |

---

## Missing Citations

| Key | Used At | Status |
|-----|---------|--------|
| SmithJones2021 | Section 3, para 1 | NOT IN BIBLIOGRAPHY — CRITICAL |

---

## Summary

- Claims verified: N / M total
- Claims unverified: K (see table above)
- Unreferenced outputs: J
- Missing citations: L

## Recommended Actions (Priority Order)
1. [BLOCKING] ...
2. [RECOMMENDED] ...
```

---

## Key Rules

- **Report only — never edit.** All fixes are the user's responsibility after reviewing the report.
- **Tolerance:** For inline numbers, a claim is MATCHED if the value appears in any output file within reasonable display rounding (±0.005 for 2-decimal numbers).
- **False positives are OK.** Flag uncertainties as UNVERIFIED rather than guessing MATCHED.
- **Missing files are always BLOCKING** — a figure reference pointing to a non-existent file is a FAIL.
