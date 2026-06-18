---
name: paper-self-revise
description: Revise an academic paper based on internal review comments. Reads review report or annotated manuscript, then applies revisions one by one with user approval. Trigger when user says "self revise" / "paper-selfrevise" / "内部修改" / "根据审稿意见修改".
allowed-tools: Read, Edit, Write, Glob, Grep, AskUserQuestion, Bash
argument-hint: [path-to-project-folder]
---

# Paper Self-Revise

## Overview

This skill revises an academic paper (`main.tex`) based on internal review comments. The user provides a project folder containing the manuscript and review materials. The skill extracts review comments, then processes them **one by one**: displaying the comment, showing the original text, proposing a revision, and asking for user approval before applying the change.

**Input**: A project folder containing:
- `main.tex` — the main manuscript (the file to be modified)
- Subfolders with figures/tables (referenced by the manuscript)
- Review materials (one or more of the following):
  - A review report file (e.g., `review.txt`, `review.md`, `review.pdf`, `report.txt`, `report.md`, `report.pdf`)
  - An annotated manuscript (e.g., `annotated.tex`, `annotated.pdf`) where annotations/comments serve as review comments

**Output**: The revised `main.tex` with all approved changes applied in place.

---

## Workflow

### Phase 0: Review Report Check

1. **Receive folder path** from user (via `$ARGUMENTS` or ask).
2. **Ask the user**: "您是否已有现成的审稿报告（review report）？(yes/no)"
3. **If yes**: Proceed to Phase 1.
4. **If no**: Draft a review report before proceeding:
   a. **Read `main.tex`** and all supporting materials (tables, figures) in the project folder to fully understand the paper.
   b. **Draft a review report** in English (~3000 words), structured as:
      - A brief overall assessment (1–2 paragraphs)
      - Numbered comments: **Comment 1**, **Comment 2**, **Comment 3**, etc.
      - Each comment should identify a specific issue, explain why it matters, and suggest how to address it.
      - **IMPORTANT**: Exclude any comments related to empirical tests that would require changing software code (e.g., re-running regressions, adding new specifications, changing estimation methods, running robustness checks in Stata/R/Python). Focus only on writing, argumentation, framing, literature, structure, clarity, interpretation, and presentation.
   c. **Save the review report** as `review.pdf` in the project folder using a Bash command to generate the PDF (e.g., via pandoc or a Python script with reportlab/fpdf). If pandoc is available, first write the content to `review.md` then convert: `pandoc review.md -o review.pdf`. If pandoc is not available, use Python to generate the PDF.
   d. **Count the words** of the generated review report (count words in the source text — the `review.md` content or the raw English text used to build `review.pdf`, excluding markdown/PDF formatting markup). Use a Bash command such as `wc -w review.md` or a Python word-count snippet on the text.
   e. Inform the user, displaying the actual word count: "审稿报告已生成并保存为 review.pdf（共 **X 词**），现在开始逐条修改。" — substitute `X` with the measured count.
   f. Proceed to Phase 1 using the newly created `review.pdf` as the review material.

### Phase 1: Initialization

1. **Scan the folder** using Glob to identify all files:
   - Locate `main.tex` (the target file to revise).
   - Locate review materials by searching for files matching common review file patterns: `review*`, `report*`, `referee*`, `comments*`, `annotated*`, `feedback*`, `revision*`.
   - If multiple review files are found, list them and ask the user which one(s) to use.
   - If no review file is found, ask the user to specify the review file path.
2. **Read `main.tex`** in full to understand the current manuscript (skip if already read in Phase 0).
3. **Read the review file(s)**:
   - For `.tex` files: look for comments marked with `%` or annotation commands (e.g., `\annotate{}`, `\comment{}`, `\todo{}`, or any custom annotation commands).
   - For `.txt` / `.md` files: read the full content as review comments.
   - For `.pdf` files: read the PDF content to extract review text.
   - For `.docx` files: use Bash to extract text content.
4. **Detect tracked changes (revision marks)** in the annotated manuscript:
   - Look for revision markup such as strikethrough/deletion marks, inserted text, colored text indicating additions/deletions, or LaTeX track-changes commands (e.g., `\added{}`, `\deleted{}`, `\replaced{}{}`, `\st{}`, `\sout{}`, `\hl{}`, or similar commands from packages like `changes`, `trackchanges`, `latexdiff`).
   - Tracked changes in the body text are revision items just like annotation comments — each one must be presented to the user for approval in Phase 3.

### Phase 2: Extract and Structure Review Comments

1. **Parse the review materials** to extract individual review comments/suggestions. This includes two categories:
   - **Annotation comments**: margin comments, `%`-comments, `\todo{}`, `\comment{}`, etc.
   - **Tracked changes**: inline revision marks (insertions, deletions, replacements) in the body text. Each distinct tracked change is treated as a separate revision item, equivalent to an annotation comment.
2. **Filter out formatting-only comments**: Automatically discard any comments or tracked changes that are purely about formatting (e.g., font size, spacing, margins, line breaks, paragraph indentation, column layout, page layout, figure/table placement commands). Do NOT present these to the user. Only retain comments about **substantive content** (wording, argumentation, data, analysis, structure, logic, references, etc.).
3. **Structure each comment** as a discrete revision item with:
   - **Comment number** (sequential)
   - **Type** — either "批注" (annotation comment) or "修订痕迹" (tracked change)
   - **Review comment text** (the reviewer's original words, or for tracked changes: a description of what was deleted/inserted/replaced)
   - **Location in manuscript** (section, paragraph, or specific text the comment refers to)
4. **Present the full list of comments** to the user:

```
I have extracted the following review comments:

No. | Type     | Location                  | Comment Summary
----|----------|---------------------------|------------------------------------------
1   | 批注     | Section 3, para 2         | Clarify the identification strategy
2   | 修订痕迹 | Section 4.1, Table 2      | Replace "effect" with "impact" in sentence about...
3   | 批注     | Section 5, para 1         | Strengthen the mechanism discussion
...

Total: N comments. Shall I proceed with revisions one by one?
```

4. **Wait for user confirmation** before proceeding.

### Phase 3: Iterative Revision (Core Loop)

For each review comment, follow this exact interaction pattern:

#### Step 1: Display the review comment

For **annotation comments** (批注):
```
───────────────────────────────────────────
批注 [X/N]:
[Full text of the reviewer's comment]
───────────────────────────────────────────
```

For **tracked changes** (修订痕迹):
```
───────────────────────────────────────────
修订痕迹 [X/N]:
[Description: e.g., "删除了 'XXX'，替换为 'YYY'" or "插入了 'XXX'" or "删除了 'XXX'"]
───────────────────────────────────────────
```

#### Step 2: Show original text

Locate and display the relevant passage from `main.tex`:

```
Original text:
┌─────────────────────────────────────────┐
│ [The exact paragraph(s) from main.tex   │
│  that this comment refers to]           │
└─────────────────────────────────────────┘
```

If the comment refers to missing content (e.g., "add a discussion of X"), show the surrounding context where the new text should be inserted.

#### Step 3: Propose revision

For **annotation comments**: Generate a revised version of the text that addresses the reviewer's comment.

For **tracked changes**: The proposed revision is the result of accepting the tracked change (i.e., applying the deletion/insertion/replacement as marked by the reviewer).

```
Proposed revision:
┌─────────────────────────────────────────┐
│ [The revised paragraph(s) that address  │
│  the reviewer's comment]                │
└─────────────────────────────────────────┘

Rationale: [Brief explanation of what was changed and why]
```

#### Step 4: Ask for user decision

Use AskUserQuestion to ask:

```
Do you approve this revision? (yes / no / skip / edit)
- yes: Apply this revision to main.tex
- no: I will propose a new revision
- skip: Skip this comment and move to the next
- edit: You provide the revised text yourself
```

#### Step 5: Handle user response

- **"yes" / "y" / "同意" / "好"**: Use the Edit tool to replace the original text with the proposed revision in `main.tex`. Confirm the change was applied, then move to the next comment.
- **"no" / "n" / "不同意" / "不行"**: Ask the user what they would like changed about the proposed revision, then generate a new proposal. Return to Step 3.
- **"skip" / "跳过"**: Skip this comment without making changes. Move to the next comment.
- **"edit" / "我来改"**: Ask the user to provide their own revised text via AskUserQuestion, then apply that text using the Edit tool. Move to the next comment.

### Phase 4: Completion

After processing all comments:

1. **Present a summary**:

```
Revision complete!

Applied: X / N items (A annotation comments + B tracked changes)
Skipped: Y items
Auto-filtered (formatting-only): Z items
Total changes made to main.tex: X

Modified sections:
- Section 3: 2 revisions
- Section 4: 1 revision
- Section 5: 3 revisions
```

2. **Offer to re-read the revised `main.tex`** to check for consistency or flow issues introduced by the revisions.

---

## Writing Rules

### Style and Formatting

- Maintain the **same writing style** as the original manuscript (do not change the overall tone or voice).
- Preserve all **LaTeX formatting**: `\section{}`, `\subsection{}`, `\ref{}`, `\cite{}`, `\citep{}`, math environments, etc.
- Preserve all **labels** (`\label{}`), **cross-references** (`\ref{}`), and **citations** intact unless the review specifically asks to change them.
- When adding new citations, use the same citation style as the rest of the paper (typically 30% `\cite{}` / 70% `\citep{}`).
- When reporting regression results, use t-statistics in parentheses and "significant at X% level" — no p-values or confidence intervals.
- **Avoid the em-dash (`---`)**: Do not use the LaTeX em-dash `---` in revised or newly written prose. It is a common AI-writing tell and clutters academic text. Replace each occurrence with the punctuation its grammatical role calls for: a parenthetical aside becomes parentheses (or commas if short); a connector before an explanation becomes a colon or semicolon; an abrupt shift becomes a period and two sentences; a list continuation becomes a comma plus a connecting word. Leave the en-dash `--` used for page and number ranges untouched (e.g., `pages={259--271}`, `2012--2026`). When a revision touches a paragraph, also strip any pre-existing `---` from that paragraph as part of the edit.

### Revision Principles

- **Minimal changes**: Only modify what is necessary to address the review comment. Do not rewrite entire paragraphs when a sentence-level edit suffices.
- **Preserve structure**: Do not reorganize sections or move paragraphs unless the review specifically requests it.
- **No fabrication**: Never invent data, results, or citations. If the review asks for additional analysis not present in the tables/figures, flag this to the user rather than making up results.
- **Consistency**: After each revision, ensure the changed text is consistent with surrounding paragraphs (transitions, terminology, notation).
- **Scope discipline**: Only address what the reviewer asked for. Do not make additional "improvements" beyond the scope of each comment.

### Handling Special Cases

- **Comment refers to a table/figure**: Read the relevant table/figure `.tex` file from the project folder before proposing the revision, to ensure accuracy.
- **Comment asks for new content**: Propose where to insert it (after which paragraph/section) and draft the new text.
- **Comment asks to delete content**: Show what will be removed and confirm before deleting.
- **Comment is vague or unclear**: Present your interpretation to the user and ask for clarification before proposing a revision.
- **Comment requires changes in multiple locations**: Handle each location as a sub-item (e.g., Comment 3a, 3b, 3c) within the same comment block.
- **Comment about bibliography/references**: If changes involve `ref.bib` or similar bibliography files, modify those files as well.
- **Tracked changes (revision marks)**: Inline deletions, insertions, or replacements marked in the annotated manuscript are treated identically to annotation comments. Present each tracked change to the user with the original text and the proposed result of accepting the change. The user decides whether to accept or reject each one.
- **Formatting-only comments**: Comments or tracked changes that are purely about formatting (font, spacing, margins, line breaks, indentation, column layout, page layout, float placement, `\vspace`, `\hspace`, `\newpage`, `\clearpage`, figure/table positioning options like `[htbp]`, etc.) must be **automatically skipped** without presenting to the user. Only substantive content comments are shown.

---

## Language

- Communicate with the user in **Chinese** (the user's preferred language for interaction).
- Write all LaTeX content and revisions in **English** (academic paper language).
- Review comment display should preserve the original language of the review.
