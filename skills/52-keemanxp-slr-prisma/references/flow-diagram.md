# PRISMA 2020 Flow Diagram Reference

The PRISMA flow diagram maps the flow of information through a systematic review: records identified, screened, assessed for eligibility, included, and excluded (with reasons).

There are four official templates. Choose based on two questions:
1. Is this a **new** or **updated** review?
2. Did the search include **databases/registers only**, or also **other sources** (websites, citation searching, grey literature, organisations)?

---

## Template Selection

| Review type | Sources | Template |
|-------------|---------|----------|
| New | Databases and registers only | Template A |
| New | Databases, registers, and other sources | Template B |
| Updated | Databases and registers only | Template C |
| Updated | Databases, registers, and other sources | Template D |

Most student and first-time SLRs use **Template A** or **Template B**.

---

## Template A: New review, databases and registers only

```
IDENTIFICATION
  Records identified from databases (n = ?)
  Records identified from registers (n = ?)
  Records removed before screening:
    Duplicate records (n = ?)
    Records marked as ineligible by automation tools (n = ?)
    Records removed for other reasons (n = ?)

SCREENING
  Records screened (n = ?)
  Records excluded (n = ?)
  Reports sought for retrieval (n = ?)
  Reports not retrieved (n = ?)
  Reports assessed for eligibility (n = ?)
  Reports excluded, with reasons:
    Reason 1 (n = ?)
    Reason 2 (n = ?)
    Reason 3 (n = ?)
    etc.

INCLUDED
  Studies included in review (n = ?)
  Reports of included studies (n = ?)
```

## Template B: New review, databases, registers, and other sources

Same as Template A, but adds a parallel column:

```
IDENTIFICATION (Other methods)
  Records identified from:
    Websites (n = ?)
    Organisations (n = ?)
    Citation searching (n = ?)
    etc.
  Reports sought for retrieval (n = ?)
  Reports not retrieved (n = ?)
  Reports assessed for eligibility (n = ?)
  Reports excluded, with reasons:
    Reason 1 (n = ?)
    Reason 2 (n = ?)
    etc.
```

Both streams merge at "Studies included in review".

## Template C & D: Updated reviews

Same structure as A and B respectively, but add a third stream at the top:

```
IDENTIFICATION (Previous studies)
  Studies included in previous version of review (n = ?)
  Reports of studies included in previous version of review (n = ?)
```

These feed into screening alongside the new search results.

---

## Annotated Guide: What Goes in Each Box

This guide helps users understand what information belongs at each stage of the flow diagram. Use this when explaining the diagram to first-time reviewers.

### IDENTIFICATION phase

| Box | What to put here | How to get this number |
|-----|-----------------|----------------------|
| Records identified from databases | The raw count of results returned by each database search, listed by database name. E.g. "Scopus (n = 245), Web of Science (n = 189), PubMed (n = 112)". | Export search results from each database and count them. |
| Records identified from registers | Results from trial registries (e.g. ClinicalTrials.gov), if searched. | Count registry search results. |
| Duplicate records removed | Number of records that appeared in more than one database and were removed. | Use reference management software (e.g. Mendeley, Zotero, EndNote) or Rayyan/Covidence to identify duplicates. |
| Records marked as ineligible by automation tools | Records flagged and removed automatically (e.g. by ASReview or Rayyan's auto-exclude). | Check the automation tool's log. If no automation was used, enter 0 or omit. |
| Records removed for other reasons | Records removed before screening for reasons other than duplication or automation (e.g. retracted articles, non-English records if a language filter was not applied at search). | Document these decisions and count them. |

### SCREENING phase

| Box | What to put here | How to get this number |
|-----|-----------------|----------------------|
| Records screened | Total records remaining after deduplication and pre-screening removal. These are the records whose titles and abstracts were actually read. | Total identified minus duplicates minus other removals. |
| Records excluded | Records excluded at the title-and-abstract screening stage. | Count of records marked "exclude" during screening. |
| Reports sought for retrieval | Records that passed title-and-abstract screening and for which full-text retrieval was attempted. | Count of records marked "include" or "maybe" at screening. |
| Reports not retrieved | Full-text documents that could not be obtained (e.g. behind paywalls, no interlibrary loan available, author did not respond). | Count of full texts you tried but failed to obtain. |
| Reports assessed for eligibility | Full-text documents that were actually read and assessed against inclusion criteria. | Reports sought minus reports not retrieved. |
| Reports excluded, with reasons | Full texts that were read but did not meet inclusion criteria. Each exclusion reason must be specific and counted. | Categorise each excluded full text by the primary reason for exclusion. Use criteria-linked reasons: "Wrong population (n = 8)", "Wrong study design (n = 5)", "No relevant outcome (n = 3)", "Not empirical (n = 2)". |

### INCLUDED phase

| Box | What to put here | How to get this number |
|-----|-----------------|----------------------|
| Studies included in review | The final count of distinct studies included in the synthesis. | Count the studies in your data extraction sheet. |
| Reports of included studies | The number of publications/documents reporting on the included studies. This may differ from the study count. | One study may be reported across multiple publications (e.g. a journal article and a conference paper). One publication may report on multiple studies. Count the actual documents. |

### For Template B/D only: Other Methods

| Box | What to put here | How to get this number |
|-----|-----------------|----------------------|
| Records from websites | Records found by searching organisational or government websites manually. | Count and document each. |
| Records from citation searching | Records found by checking the reference lists of included studies (backward citation) or checking who cited the included studies (forward citation). | Count new records found this way. |
| Records from organisations | Records obtained by contacting researchers, professional bodies, or organisations. | Count records received. |

---

## Generating the Flow Diagram

### In the Word document

Build the flow diagram as a structured table using docx-js. The diagram should use:

- A table-based layout with merged cells to represent the flow
- Clear box borders for each stage
- Arrow indicators between stages (use "→" or "↓" text within cells, or downward-pointing text)
- Shaded header rows for each phase (Identification, Screening, Included)
- Placeholder values (n = ?) that the user fills in with their actual numbers

The flow diagram should be placed in the Results section of the manuscript, labelled as "Figure 1. PRISMA 2020 flow diagram of study selection" (or the next available figure number).

### As a visual using the Visualizer

Generate an SVG flow diagram using the Visualizer tool. This gives the user a clear, visual representation of the PRISMA flow that they can use for learning and reference. The visual should:

- Show the three phases (Identification, Screening, Included) as distinct horizontal bands
- Use boxes connected by arrows for each step
- Show exclusion branches to the right of the main flow
- Use colour coding: blue/grey tones for the main flow, amber/orange for exclusion branches
- Include placeholder counts or actual counts
- Be clearly labelled with annotations explaining what goes in each box (for learning purposes)

---

## Key Terminology

- **Records** = a title or abstract (or both) of a report indexed in a database or register.
- **Reports** = a document (journal article, preprint, conference abstract, book chapter, etc.) supplying information about a study.
- **Studies** = an investigation (e.g. a clinical trial, observational study) that may be reported in one or more reports.

These three terms are distinct and should not be used interchangeably. One study may have multiple reports. One report may describe multiple studies. The flow diagram tracks all three.

Source: Page MJ et al. (2021). Licensed under CC BY 4.0.
