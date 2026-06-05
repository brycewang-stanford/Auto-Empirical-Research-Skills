---
name: proofread
description: >-
  Run the proofreading protocol on academic writing — papers or manuscripts. Checks grammar, typos, layout issues, consistency, and academic writing quality. Produces a report without editing files. Make sure to use this skill whenever the user wants surface-level writing errors found — not substantive academic critique. Triggers include: "proofread", "check for typos", "grammar check", "look for errors in my draft", "proofread all", "polish this", "check my writing", "are there any mistakes", "proofread before I send this", or when the user wants a clean-up pass rather than feedback on arguments or methods.
argument-hint: "[filename, 'all', or path to manuscript]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task", "AskUserQuestion"]
---

# Proofread Academic Writing

Run the mandatory proofreading protocol on papers or manuscripts. Produces a report of all issues WITHOUT editing any source files.

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific filename: review that file only
   - If `$ARGUMENTS` is `all`: review all files in `manuscripts/` and `Quarto/` (if it exists)
   - If `$ARGUMENTS` is a file in `manuscripts/`: treat as manuscript (not slides)
   - If `$ARGUMENTS` is empty or ambiguous and multiple files exist, use AskUserQuestion:
     - header: "Files"
     - question: "Which files should I proofread?"
     - multiSelect: true
     - options: list up to 4 found files (label: filename, description: directory and file type). User can select multiple or choose "Other" to specify a path.

2. **For each file, launch the proofreader agent** that checks for:

   **GRAMMAR:** Subject-verb agreement, articles (a/an/the), prepositions, tense consistency
   **TYPOS:** Misspellings, search-and-replace artifacts, duplicated words
   **LAYOUT ISSUES:** Overfull hbox (LaTeX slides/manuscripts), content exceeding slide boundaries (Quarto), table/column overflow in manuscripts
   **CONSISTENCY:** Citation format, notation, terminology, variable names matching table column names
   **ACADEMIC QUALITY:** Informal language, missing words, awkward constructions

3. **Produce a detailed report** for each file listing every finding with:
   - Location (line number or section heading)
   - Current text (what's wrong)
   - Proposed fix (what it should be)
   - Category and severity

4. **Save each report** to `quality_reports/`:
   - For `.tex` slide files: `quality_reports/FILENAME_report.md`
   - For `.qmd` slide files: `quality_reports/FILENAME_qmd_report.md`
   - For manuscript files: `quality_reports/FILENAME_proofread.md`

5. **IMPORTANT: Do NOT edit any source files.**
   Only produce the report. Fixes are applied separately after user review (see `rules/proofreading-protocol.md`).

6. **Present summary** to the user:
   - Total issues found per file
   - Breakdown by category
   - Most critical issues highlighted
