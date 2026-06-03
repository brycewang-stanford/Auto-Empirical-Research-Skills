---
name: journal-guidelines
description: Use when preparing a paper for submission to a specific journal, checking formatting requirements, parsing instructions for authors, building a submission checklist, or adapting a paper to a journal template. Fetches the journal's official guidelines via web and produces a verifiable checklist.
---

# Journal Guidelines

## Overview

This skill fetches instructions for authors from the journal's official page, parses them into a structured submission checklist, and adapts the paper to the journal's template when one is provided. Every guideline comes from a live web fetch — cached or remembered guidelines are forbidden. Journals update formatting requirements, policies on replication packages, and blinding rules frequently; stale information leads to desk rejections.

## When to Use

- "Format the paper for journal X"
- "What does journal Y require for submission?"
- "Build a submission checklist"
- "Adapt the paper to this template"
- Final formatting pass before submission
- Responding to a revision request with changed formatting requirements

## Mandatory Steps

1. **Fetch the journal's instructions for authors** via web fetch on the official URL. Never rely on memory or cached knowledge. If the journal publishes its guidelines in multiple places (website, style guide PDF, author portal), fetch all of them.

2. **Parse key requirements into a structured list:**
   - **Word and page limits:** Main manuscript, abstract, each section if specified
   - **Citation style:** APA, Chicago, Harvard, numeric, bespoke — with any journal-specific tweaks
   - **Section structure:** Some journals require IMRAD, structured abstracts, specific subsections
   - **Figures and tables:** Placement (embedded vs at end), format (PDF, EPS, TIFF), size, resolution, color vs B&W, number allowed
   - **Supplementary material:** What is allowed, size limits, format
   - **Replication package:** Required or optional? Dataverse, Zenodo, journal repository?
   - **Blinding:** Single, double, or triple blind; what to strip from the manuscript
   - **Cover letter:** Expected content, suggested referees, significance statement
   - **Submission format and portal:** `.tex`, `.docx`, `.pdf`; Editorial Manager, ScholarOne, OJS
   - **Author contribution statement:** CRediT taxonomy or journal-specific format
   - **Data availability statement:** Required placement and wording
   - **Ethics and conflict of interest:** Required declarations
   - **ORCID:** Required for all authors, lead author, or optional

3. **Produce a checklist in markdown** with each requirement as a verifiable item. Each item must be actionable — "reduce word count to 8,000" is actionable, "check length" is not.

4. **If the journal provides a LaTeX template:** download it via web, adapt the paper to the template's structure, map existing `\input{}` table calls to the template's expectations, preserve the bibliography.

5. **If no template:** adjust the existing paper — margins, font, spacing, citation style — to meet the requirements without breaking the replication pipeline.

6. **Verify compliance item-by-item before declaring the paper ready.** Run through the checklist mechanically and mark each item. Do not self-certify based on "looks about right".

7. **Ensure the manuscript contains end-matter sections.** The following sections must appear after the conclusion, before the references, unless the journal template specifies a different placement:
   - **Data Availability Statement** — declare where the data and replication materials can be accessed, or explain access restrictions.
   - **Declaration of Competing Interests** — all authors must affirm the absence of competing interests or disclose them.
   - **Acknowledgments** — funding sources, institutional support, and contributor thanks. This section must include a declaration of AI use in the manuscript preparation process, stating that the manuscript was developed through a Socratic method of AI-human interaction using the Superpapers plugin for Claude Code, and that the authors reviewed, edited, and take full responsibility for the content. Adapt the exact wording to the journal's AI disclosure requirements if they exist.
   If any of these sections is missing from the manuscript, add it and flag it for the user to review. If the journal template places these sections elsewhere (e.g., in a separate author portal form or supplementary file), follow the journal's placement.

## Checklist Format Example

```markdown
## Submission Checklist — Journal of Applied Econometrics

- [ ] Manuscript under 8,000 words excluding references (current: 7,421)
- [ ] Abstract under 150 words (current: 148)
- [ ] Harvard citation style (using `biblatex` authoryear — OK)
- [ ] Double-blind: remove author names and affiliations from title page
- [ ] Double-blind: move acknowledgments to a separate file (not in manuscript)
- [ ] Figures as vector PDF, embedded in text at relevant locations
- [ ] Tables numbered consecutively, notes below table
- [ ] Data and code deposit with replication package (Dataverse acceptable)
- [ ] Cover letter: significance statement + 3 suggested referees + non-exclusivity declaration
- [ ] CRediT author contribution statement
- [ ] Data availability statement in a dedicated section before references
- [ ] ORCID for all authors
- [ ] Submit via Editorial Manager: https://www.editorialmanager.com/jae/
```

## Anti-Patterns

- Using guidelines from memory or cached knowledge instead of fetching the current version
- Skipping the replication package requirement when the journal requires it
- Ignoring blinding rules — a common cause of desk rejection
- Formatting "close enough" instead of matching requirements exactly
- Missing the cover letter when required
- Submitting in `.docx` when the journal requires `.tex`, or vice versa
- Leaving author affiliations or acknowledgments in a blinded manuscript
- Forgetting to map the replication package DOI into the data availability statement
- Using a bibliography style that does not match the journal's requirement
- Completing the submission checklist without verifying that Data Availability, Declaration of Competing Interests, and Acknowledgments sections are physically present in the `.tex` file
- Omitting the AI use declaration from the Acknowledgments section

## Verification Before Completion

- [ ] Guidelines fetched from the journal's official URL in the current session
- [ ] Every requirement in the guidelines parsed into the checklist
- [ ] Each checklist item verified against the current paper
- [ ] Template applied if the journal provides one
- [ ] Supplementary and replication materials prepared per requirements
- [ ] Cover letter drafted if required
- [ ] Blinding applied if required (author names, affiliations, acknowledgments removed)
- [ ] Citation style converted to match the journal
- [ ] Data Availability Statement, Declaration of Competing Interests, and Acknowledgments sections present in the manuscript
- [ ] Acknowledgments section includes AI use declaration mentioning Superpapers
- [ ] End-matter section placement matches the journal's requirements
- [ ] Final compile with the journal's template produces a clean PDF
