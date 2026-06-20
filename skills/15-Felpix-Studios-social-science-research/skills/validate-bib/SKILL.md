---
name: validate-bib
description: >-
  Validate bibliography entries against citations in all source files. Find missing entries and unused references. Make sure to use this skill whenever the user has any concern about bibliography completeness or citation keys. Triggers include: "validate my bib", "check my citations", "find missing references", "I'm getting undefined citation errors", "are all my citations in the bib file", "check for unused references", "my bibliography is broken", "missing bib entries", "citation not found", or after adding new references from a lit review or before submission.
argument-hint: "[bib file path, or leave blank to auto-detect]"
allowed-tools: ["Read", "Grep", "Glob"]
---

# Validate Bibliography

Cross-reference all citations in source files against bibliography entries.

## Steps

1. **Read the bibliography file** and extract all citation keys

2. **Scan all source files for citation keys:**
   - `.tex` files: look for `\cite{`, `\citet{`, `\citep{`, `\citeauthor{`, `\citeyear{`
   - `.qmd` files: look for `@key`, `[@key]`, `[@key1; @key2]`
   - Extract all unique citation keys used

3. **Cross-reference:**
   - **Missing entries:** Citations used in source files but NOT in bibliography
   - **Unused entries:** Entries in bibliography not cited anywhere
   - **Potential typos:** Similar-but-not-matching keys

4. **Check entry quality** for each bib entry:
   - Required fields present (author, title, year, journal/booktitle)
   - Author field properly formatted
   - Year is reasonable
   - No malformed characters or encoding issues

5. **Report findings:**
   - List of missing bibliography entries (CRITICAL)
   - List of unused entries (informational)
   - List of potential typos in citation keys
   - List of quality issues

## Files to scan:
```
manuscripts/**/*.tex
Quarto/**/*.qmd
```

## Bibliography location:
```
Bibliography_base.bib  (repo root)
```
