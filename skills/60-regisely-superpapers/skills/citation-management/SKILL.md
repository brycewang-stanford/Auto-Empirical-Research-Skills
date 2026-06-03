---
name: citation-management
description: Use when adding citations to a .bib file, importing references by DOI, cleaning a bibliography, detecting duplicate entries, or normalizing citation keys. Uses direct .bib manipulation with CrossRef API for metadata resolution — no external tool dependencies.
---

# Citation Management

## Overview

This skill manages the project's `references.bib` directly, using the CrossRef API to resolve DOIs into complete BibTeX entries. It does not require Zotero, any external CLI, or any desktop application. Everything happens through standard tools: `curl` (or equivalent HTTP client) and text editing of the `.bib` file.

## When to Use

- "Add this paper to the bibliography"
- "Import this DOI"
- "Clean up the .bib file"
- "Are there duplicates in my references?"
- "Fix the citation keys"
- Before submission: validate that all cited papers have complete entries

## Mandatory Steps

1. **Resolve every DOI via CrossRef.** Call `https://api.crossref.org/works/{doi}`. Extract: title, full author list, year, journal, volume, issue, pages, publisher, and DOI. Do not invent fields missing from the API response — leave them out instead.

2. **Generate a BibTeX entry with complete fields.** Required for articles: `author`, `title`, `year`, `journal`, `volume`, `pages`, `doi`. For books: `author` (or `editor`), `title`, `year`, `publisher`, `doi`. For chapters: add `booktitle` and `editor`.

3. **Citation key format:** `FirstAuthorLastnameYear`, e.g., `Santos2024`. Disambiguate collisions with lowercase letters: `Santos2024a`, `Santos2024b`. Strip accents and non-ASCII characters from the key — BibTeX tooling does not always handle Unicode in keys.

4. **Check for duplicates before adding.** Duplicate definition: same DOI, OR same title (case-insensitive, normalized whitespace) AND same first author AND same year. If duplicate, skip and report the existing key.

5. **Keep `references.bib` sorted alphabetically by citation key.** Sort after every insert so the file stays stable across commits.

6. **Preserve existing entries.** Do not rewrite fields of existing entries unless the user explicitly asks. Append new entries in the correct sorted position.

## CrossRef API Example

```bash
curl -s 'https://api.crossref.org/works/10.1257/aer.84.4.772' \
  | jq '.message | {title, author, issued, container-title, volume, page, DOI}'
```

The response provides all fields needed to build a complete BibTeX entry. Parse the `author` array to extract each author's given and family name, then format as `Family, Given and Family2, Given2`.

## BibTeX Entry Template

```bibtex
@article{CardKrueger1994,
  author  = {Card, David and Krueger, Alan B.},
  title   = {Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania},
  journal = {American Economic Review},
  year    = {1994},
  volume  = {84},
  number  = {4},
  pages   = {772--793},
  doi     = {10.1257/aer.84.4.772}
}
```

Use braces for titles that contain words requiring specific capitalization (e.g., proper nouns, acronyms): `title = {The {DiD} Approach to Causal Inference}`. Use double hyphens for page ranges (`772--793`).

## Anti-Patterns

- BibTeX entries with missing DOIs
- Inconsistent citation keys in the same file (mix of `santos2024` and `Santos_2024`)
- Duplicate entries — same DOI appearing with different keys
- Entries with `"et al."` in the author field instead of the full author list
- Using braces incorrectly to preserve capitalization (either too many or too few)
- Editing an existing paper's entry without being asked
- Adding metadata from memory instead of resolving via CrossRef
- Leaving the `.bib` file unsorted after insertion

## Verification Before Completion

- [ ] Every new entry has a DOI field
- [ ] Every entry has the full author list, not `et al.`
- [ ] Citation keys follow the `AuthorYear[letter]` format consistently
- [ ] No duplicates detected (by DOI or by title+author+year)
- [ ] File sorted alphabetically by citation key
- [ ] Existing entries untouched unless explicitly modified
- [ ] Page ranges use double hyphens (`--`)
