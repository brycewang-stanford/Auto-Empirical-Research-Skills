---
name: split-pdf
description: Download, split, and deeply read academic PDFs. Use when asked to read, review, or summarize an academic paper. Splits PDFs into 4-page chunks, reads them in small batches, and produces structured reading notes — avoiding context window crashes and shallow comprehension.
allowed-tools: Bash(python*), Bash(pip*), Bash(curl*), Bash(wget*), Bash(mkdir*), Bash(ls*), Read, Write, Edit, WebSearch, WebFetch
argument-hint: "[pdf-path-or-search-query]"
---

# Split-PDF: Download, Split, and Deep-Read Academic Papers

**CRITICAL RULE: Never read a full PDF. Never.** Only read the 4-page split files, and only 3 splits at a time (~12 pages). Reading a full PDF will either crash the session with an unrecoverable "prompt too long" error — destroying all context — or produce shallow, hallucinated output. There are no exceptions.

## When This Skill Is Invoked

The user wants you to read, review, or summarize an academic paper. The input is either:
- A file path to a local PDF (e.g., `./articles/smith_2024.pdf`)
- A search query or paper title (e.g., `"Gentzkow Shapiro Sinkinson 2014 competition newspapers"`)

**Important:** You cannot search for a paper you don't know exists. The user MUST provide either a file path or a specific search query — an author name, a title, keywords, a year, or some combination that identifies the paper. If the user invokes this skill without specifying what paper to read, ask them. Do not guess.

## Step 1: Acquire the PDF

**If a local file path is provided:**
- Verify the file exists
- If the file is NOT already inside `./articles/`, copy it there (do not move — preserve the original location)
- Proceed to Step 2

**If a search query or paper title is provided:**
1. Use WebSearch to find the paper
2. Use WebFetch or Bash (curl/wget) to download the PDF
3. Save it to `./articles/` in the project directory (create the directory if needed)
4. Proceed to Step 2

**CRITICAL: Always preserve the original PDF.** The downloaded or provided PDF in `./articles/` must NEVER be deleted, moved, or overwritten at any point in this workflow. The split files are derivatives — the original is the permanent artifact. Do not clean up, do not remove, do not tidy. The original stays.

## Step 2: Split the PDF

Create a subdirectory for the splits and run the splitting script:

```python
from PyPDF2 import PdfReader, PdfWriter
import os, sys

def split_pdf(input_path, output_dir, pages_per_chunk=4):
    os.makedirs(output_dir, exist_ok=True)
    reader = PdfReader(input_path)
    total = len(reader.pages)
    prefix = os.path.splitext(os.path.basename(input_path))[0]

    for start in range(0, total, pages_per_chunk):
        end = min(start + pages_per_chunk, total)
        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])

        out_name = f"{prefix}_pp{start+1}-{end}.pdf"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "wb") as f:
            writer.write(f)

    print(f"Split {total} pages into {-(-total // pages_per_chunk)} chunks in {output_dir}")
```

**Directory convention:**
```
articles/
├── smith_2024.pdf                    # original PDF — NEVER DELETE THIS
└── split_smith_2024/                 # split subdirectory
    ├── smith_2024_pp1-4.pdf
    ├── smith_2024_pp5-8.pdf
    ├── smith_2024_pp9-12.pdf
    └── ...
```

The original PDF remains in `articles/` permanently. The splits are working copies. If anything goes wrong, you can always re-split from the original.

If PyPDF2 is not installed, install it: `pip install PyPDF2`

## Step 3: Read in Batches of 3 Splits

Read **exactly 3 split files at a time** (~12 pages). After each batch:

1. **Read** the 3 split PDFs using the Read tool
2. **Update** the running notes file (`notes.md` in the split subdirectory)
3. **Pause** and tell the user:

> "I have finished reading splits [X-Y] and updated the notes. I have [N] more splits remaining. Would you like me to continue with the next 3?"

4. **Wait** for the user to confirm before reading the next batch

Do NOT read ahead. Do NOT read all splits at once. The pause-and-confirm protocol is mandatory.

## Step 4: Structured Extraction

As you read, collect information along these dimensions and write them into `notes.md`:

1. **Research question** — What is the paper asking and why does it matter?
2. **Audience** — Which sub-community of researchers cares about this?
3. **Method** — How do they answer the question? What is the identification strategy?
4. **Data** — What data do they use? Where precisely did they find it? What is the unit of observation? Sample size? Time period?
5. **Statistical methods** — What econometric or statistical techniques do they use? What are the key specifications?
6. **Findings** — What are the main results? Key coefficient estimates and standard errors?
7. **Contributions** — What is learned from this exercise that we didn't know before?
8. **Replication feasibility** — Is the data publicly available? Is there a replication archive? A data appendix? URLs for the underlying data?

These questions extract what a researcher needs to **build on or replicate** the work — a structured extraction more detailed and specific than a typical summary.

## The Notes File

The output is `notes.md` in the split subdirectory:

```
articles/split_smith_2024/notes.md
```

This file is **updated incrementally** after each batch. Structure it with clear headers for each of the 8 dimensions. After each batch, update whichever dimensions have new information — do not rewrite from scratch.

By the time all splits are read, the notes should contain specific data sources, variable names, equation references, sample sizes, coefficient estimates, and standard errors. Not a summary — a structured extraction.

## When NOT to Split

- Papers shorter than ~15 pages: read directly (still use the Read tool, not Bash)
- Policy briefs or non-technical documents: a rough summary is fine
- Triage only: read just the first split (pages 1-4) for abstract and introduction

## Quick Reference

| Step | Action |
|------|--------|
| **Acquire** | Download to `./articles/` or use existing local file |
| **Split** | 4-page chunks into `./articles/split_<name>/` |
| **Read** | 3 splits at a time, pause after each batch |
| **Write** | Update `notes.md` with structured extraction |
| **Confirm** | Ask user before continuing to next batch |

For detailed explanation of why this method works, see [methodology.md](methodology.md).
