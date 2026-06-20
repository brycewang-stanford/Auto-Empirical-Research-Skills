---
name: citation-check
description: Audit in-text/reference parity, DOIs, claim support, and citation style.
argument-hint: "[path to manuscript and bibliography, or paste citation list; include target style/journal if known]"
---

# Citation Integrity Auditor

## Heritage and scope

This is an original Open Science Skills workflow adapted for experimental social science. It remixes general citation-check and source-verification ideas from Cheng-I Wu's *Academic Research Skills for Claude Code* (CC BY-NC 4.0), especially the separation between citation formatting, existence checks, DOI checks, and uncertainty reporting. Do not copy ARS prose into reports; apply the workflow below.

## Instructions

### 1. Orient before checking

Identify the inputs and constraints:

- Manuscript source: LaTeX, Markdown, Word export, PDF text, or pasted prose.
- Bibliography source: `.bib`, CSL JSON, Zotero export, reference section, footnotes, or mixed.
- Target style: default to APA 7 unless the user names a journal or style.
- Scope: whole manuscript, one section, bibliography only, or DOI-only pass.
- Tool availability: if web lookup, Crossref, DataCite, DOI.org, Semantic Scholar, or OpenAlex are unavailable, mark verification status as `NOT CHECKED` rather than guessing.

### 2. Build the citation inventory

Create two inventories before judging errors:

- **In-text inventory:** every author-year, parenthetical, narrative, footnote, or numeric citation appearing in the manuscript.
- **Reference inventory:** every bibliography entry, including entry key if present, authors, year, title, outlet, DOI/URL, publication status, and notes.

Normalize cautiously:

- Treat spelling variants, diacritics, hyphenated surnames, particles (`de`, `van`, `von`), and organizational authors as possible matches until checked.
- For multiple works by the same author-year, verify `a/b/c` suffixes are assigned consistently.
- For BibTeX, preserve the entry key and report it with every finding.

### 3. Run structural checks

Report:

- Cited in text but missing from references.
- In references but never cited.
- Author-year mismatch between in-text citation and reference entry.
- Duplicate bibliography entries for the same work.
- Ambiguous citations where two reference entries could satisfy one in-text citation.
- Broken cross-references caused by LaTeX/BibTeX key drift.

Do not "fix" ambiguous cases silently. List the likely match and the evidence.

### 4. Verify source existence and identifiers

Use a tiered check when tools allow:

1. **DOI resolution:** does the DOI resolve, and does the resolved title match the cited title?
2. **Metadata lookup:** Crossref/DataCite/Semantic Scholar/OpenAlex title-author-year search for entries without DOI or with suspicious DOI.
3. **Web search:** title in quotes plus first author, used for working papers, books, reports, and older items.
4. **Manual-verification flag:** when no programmatic match is found, classify as `NEEDS AUTHOR VERIFICATION`, not fabricated.

Flag these separately:

- `MISSING DOI`: likely DOI exists but is absent from the reference.
- `NO DOI FOUND`: searched, no DOI found; not necessarily an error.
- `DOI MISMATCH`: DOI resolves to a different title or author set.
- `TITLE DRIFT`: cited title differs materially from indexed title.
- `STATUS UPDATE`: working paper, preprint, or conference paper appears to have a journal/book version.
- `POSSIBLE NONEXISTENT SOURCE`: no evidence found after identifier and title searches; use this label sparingly.

### 5. Check style and completeness

For APA 7 and most social-science journal styles:

- DOI should be a URL form when available: `https://doi.org/...`.
- Do not add a period after DOI or URL.
- Journal articles need article title, journal title, volume, issue when available, pages or article number, and DOI when available.
- Books need publisher; edited chapters need editors, book title, page range, publisher.
- Reports and datasets need institutional author, date, title, publisher/archive, version if relevant, and URL/DOI.
- Data, code, and materials should be cited as research products, not buried only in availability statements.

When target style is not APA, apply the target style but still keep the integrity checks above.

### 6. Audit evidentiary use

For literature reviews and theory sections, sample the most important citations and classify how they are used:

- **Background:** source establishes context only.
- **Claim support:** source is used as evidence for a substantive claim.
- **Method precedent:** source justifies a design, estimator, measurement strategy, or reporting practice.
- **Contrast:** source is cited as an opposing or incomplete account.

Flag overclaiming when the cited source plausibly cannot support the sentence where it appears. If source text is unavailable, mark `SOURCE TEXT NOT CHECKED`.

## Output

Produce a `Citation Audit Report`:

```
# Citation Audit Report

Scope: <files/sections checked>
Target style: <style or journal>
Verification tools used: <Crossref/DataCite/S2/OpenAlex/Web/manual/none>
Summary: <N blocking, N recommended, N minor, N needs-author-verification>

## Blocking Issues
| Location | Entry/key | Issue | Evidence | Fix |

## Recommended Fixes
| Location | Entry/key | Issue | Evidence | Fix |

## Minor Style Issues
| Location | Entry/key | Issue | Fix |

## DOI and Source-Status Table
| Entry/key | Current DOI/URL | Verification status | Suggested action |

## In-text / Reference Parity
| Type | Citation or key | Location | Suggested action |

## Needs Author Verification
| Entry/key | Why unresolved | What author should check |
```

Severity:

- **Blocking:** missing cited reference, wrong DOI, possibly nonexistent source, citation supports a decisive claim but appears wrong, or broken citation build.
- **Recommended:** missing likely DOI, stale working paper, author-year mismatch that is fixable, uncited important reference, incomplete metadata.
- **Minor:** punctuation, capitalization, inconsistent initials, style-only issues.

## Quality checks

- [ ] In-text inventory and reference inventory were built before findings were listed.
- [ ] Every DOI mismatch was based on resolved metadata, not intuition.
- [ ] Unverified sources are labeled as unresolved, not fabricated.
- [ ] Existing author-year suffixes were checked for consistency.
- [ ] Data/code/material citations were included when relevant.
- [ ] The report distinguishes integrity errors from style issues.
- [ ] ARS-derived workflow ideas are attributed when this skill's structure is reused outside this repository.
