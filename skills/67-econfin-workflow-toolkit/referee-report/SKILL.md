---
name: referee-report
description: Generate academic referee reports for economics/finance papers, followed by a 150-word letter to the editor with recommendation (Reject / Major Revision) and Kai Wu signature. Two modes (normal / high-level), configurable number of comments; recommendation choice drives evaluation tone (Reject → negative, Major Revision → neutral). Trigger when user says "referee report" / "write referee report" / "审稿报告" / "写审稿意见" / "generate referee report" / "review this paper".
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash
argument-hint: [path-to-project-folder]
---

# Referee Report Generator

## Overview

This skill generates a **referee report** for an academic economics/finance paper. The user provides a project folder containing the manuscript and supporting files. The skill reads the paper thoroughly, then generates a structured referee report with a summary, overall assessment, and numbered specific comments.

**Input**: A project folder containing:
- `main.tex` (or `*.pdf`) — the manuscript
- Subfolders with tables/figures (`.tex` files referenced by the manuscript)

**Output**: `{original-filename}-review.doc` saved in the project folder (e.g., if the manuscript is `RAEL-2026-0427_Proof_hi.pdf`, the output is `RAEL-2026-0427_Proof_hi-review.doc`)

---

## Language Rule

- **Communicate with the user in Chinese** (questions, status updates, confirmations).
- **Write the referee report entirely in English** (summary, assessment, all comments).

---

## Workflow

### Phase 1: Initialization

1. **Receive folder path** from user (via `$ARGUMENTS` or ask: "请提供论文项目文件夹路径").
2. **Scan the folder** using Glob:
   - Locate the manuscript: `main.tex`, or `*.pdf`.
   - Locate all `.tex` files in subfolders (tables/figures).
3. **Read the manuscript** in full. If it is a PDF, use the Read tool with page ranges for large files.
4. **Read all table and figure `.tex` files** from subfolders so you have full knowledge of the paper's empirical results, variable definitions, and sample characteristics.

### Phase 2: Configuration

Use **one** AskUserQuestion call with **three** questions:

**Question 1 — Recommendation (推荐意见)**:
- **Reject**: Paper has fundamental weaknesses. → Evaluation tone is **negative**.
- **Major Revision**: Paper has merit but needs significant improvement. → Evaluation tone is **neutral**.

The user's choice here determines BOTH (a) the recommendation written in the editor letter (Phase 4), and (b) the overall evaluation tone in Part 2 of the report:
- Reject → negative evaluation
- Major Revision → neutral evaluation

**Question 2 — Mode (审稿模式)**:
- **普通审稿模式 (Normal)**: Standard referee report suitable for field journals. Comments are direct, clear, and focused on core issues.
- **高水平审稿模式 (High-Level)**: Top-journal quality (AER/QJE/JFE/JF/RFS level). Comments demonstrate deeper understanding of identification strategy, connect to methodological frontier, and are more nuanced and constructive.

**Question 3 — Number of Comments (意见数量)**:
- 3 comments
- 5 comments
- 8 comments
- (User can type any number from 3–8 via "Other")

### Phase 3: Generate Report

After receiving the user's choices, generate the full referee report following the structure below.

---

## Report Structure

### Part 0: Report Title

The very first line of the report MUST be:

> **Referee Report of "[manuscript title]"**

Extract the manuscript title from the paper's `\title{}` command or PDF title. This title line appears in BOTH normal and high-level modes.

### Part 1: Summary of Findings

Write a paragraph titled **"Summary of Findings"**.

Use **100 English words** to summarize the main findings of the paper. Cover:
- The research question
- The methodology / identification strategy
- The key empirical results and contribution

This section is **identical in format** for both normal and high-level modes.

### Part 2: Overall Evaluation

Use **30 English words** to give an overall **[neutral / negative]** evaluation of the paper. The tone is determined by the user's recommendation choice in Phase 2 Question 1:

- **Major Revision → Neutral**: Acknowledge the paper's contribution but note that significant concerns remain.
- **Reject → Negative**: State that the paper has fundamental weaknesses that undermine its contribution.

### Part 3: Specific Comments

Generate the user-specified number of comments (N). Use comments 1 through N from the word count table for the selected mode.

#### Word Count Tables

**Normal Mode (普通审稿模式)**:

| Comment # | Word Count |
|-----------|-----------|
| 1 | 100 |
| 2 | 120 |
| 3 | 90 |
| 4 | 80 |
| 5 | 70 |
| 6 | 120 |
| 7 | 140 |
| 8 | 90 |

**High-Level Mode (高水平审稿模式)**:

| Comment # | Word Count | Special Rules |
|-----------|-----------|---------------|
| 1 | 200 | **Cite papers.** List references in APA format at the end of the report. |
| 2 | 300 | **Use (a), (b), (c) subpoints.** Do not cite papers. |
| 3 | 140 | Do not cite papers. |
| 4 | 80 | Do not cite papers. |
| 5 | 130 | Do not cite papers. |
| 6 | 170 | Do not cite papers. |
| 7 | 200 | Do not cite papers. |
| 8 | 90 | Do not cite papers. |

#### Comment Requirements

Each comment MUST:
1. **Be numbered**: `(1)`, `(2)`, `(3)`, etc.
2. **Target a SPECIFIC issue** — reference exact tables, figures, variables, equations, or sections of the paper.
3. **Specify the problems and caveats of the paper** — identify concrete weaknesses, not vague concerns.
4. **Support your arguments in painstaking detail** — explain WHY something is a problem, provide logical reasoning, describe what could go wrong.
5. **Citation rules depend on mode and comment number**:
   - **Normal mode (all comments)**: Do NOT cite papers. All arguments must stand on their own logic.
   - **High-level mode, Comment (1) ONLY**: Cite relevant academic papers to support the critique. List all cited references in **APA format** in a dedicated **References** section at the very end of the report.
   - **High-level mode, Comments (2)–(8)**: Do NOT cite papers.
6. **Meet the word count** — within ±10% of the target for that comment number.
7. **High-level mode, Comment (2) subpoints**: Structure Comment (2) with subpoints **(a)**, **(b)**, and **(c)**, each addressing a distinct aspect of the issue.

#### Comment Topic Distribution

Distribute comments across different aspects of the paper. Adapt based on actual weaknesses found, but aim to cover a diverse range from the following (prioritize by severity):

1. **Identification / Causal inference** — Is the identification strategy convincing? Are there threats to causal interpretation?
2. **Endogeneity / Omitted variables** — Could unobserved factors drive both the key independent variable and the outcome?
3. **Sample selection / Data quality** — Is the sample representative? Are there selection biases?
4. **Variable measurement / Construction** — Are key variables well-defined and correctly measured?
5. **Alternative explanations** — Could other mechanisms explain the findings?
6. **Robustness / Sensitivity** — How sensitive are results to specification choices, sample restrictions, or variable definitions?
7. **Economic magnitude / Interpretation** — Are the effects economically meaningful? Are results interpreted correctly?
8. **Theoretical motivation / Mechanism** — Is the theoretical framework convincing? Is the hypothesized mechanism well-supported?

**Do NOT write comments about**:
- Typos or minor formatting issues
- Requests to cite specific papers
- Generic praise or generic criticism

#### Comment Style Guide

- Write in **third person**: "The authors...", "The paper...", "The identification strategy..."
- Be **specific**: "In Table 3, Column 2, the coefficient on VARIABLE..." not "Some results seem weak..."
- Be **analytical**: Explain the logical chain of why something is problematic
- Be **self-contained**: Each comment should be readable independently
- **Normal mode**: Straightforward, direct critique. Focus on the most important issues clearly.
- **High-level mode**: More sophisticated analysis. Demonstrate understanding of the econometric subtleties. Consider second-order effects. Offer more nuanced constructive suggestions within the critique.

### Part 4: Letter to the Editor

After the referee report (and References section, if any), append a **Letter to the Editor**.

Now acting as the referee who wrote the referee report, write a **150-word English letter** to the editor regarding the recommendation for this manuscript. The letter should:
- Briefly summarize what the paper is about (1–2 sentences).
- State the main reasons supporting the chosen recommendation, drawing on the specific comments above.
- Match the tone selected in Phase 2 Question 1 (negative for Reject; neutral but with significant reservations for Major Revision).
- End with the recommendation line and signature exactly as specified below.

**Recommendation line** (replace `XX` with the user's choice from Phase 2 Question 1):
- If user chose Reject → `Recommendation: Reject.`
- If user chose Major Revision → `Recommendation: Major Revision.`

**Signature block** (use exactly this text):

```
Kai Wu, PhD
Associate Professor of Finance
Central University of Finance and Economics
P. R. China
```

### Phase 4: Output

1. **Assemble the report** using this template:

```markdown
**Referee Report of "[manuscript title]"**

**Summary of Findings**

[100-word summary of main findings]

[30-word overall neutral/negative evaluation]

**Specific Comments**

(1) [Comment 1 text]

(2) [Comment 2 text]

(3) [Comment 3 text]

...

**References**

[APA-formatted references — ONLY if high-level mode was selected. This section lists all papers cited in Comment (1). Omit this section entirely in normal mode.]

---

**Letter to the Editor**

[150-word letter to the editor, as described in Part 4 above]

Recommendation: [Reject | Major Revision].

Kai Wu, PhD
Associate Professor of Finance
Central University of Finance and Economics
P. R. China
```

2. **Determine output filename**: Strip the extension from the original manuscript filename and append `-review.doc`. For example, if the manuscript is `RAEL-2026-0427_Proof_hi.pdf`, the output is `RAEL-2026-0427_Proof_hi-review.doc`. If `main.tex`, the output is `main-review.doc`.
3. **Write** the report content to a temporary markdown file in the project folder.
4. **Convert to .doc** using pandoc:
   ```bash
   pandoc "FOLDER/tmp.md" -o "FOLDER/{original-filename}-review.doc"
   ```
   If pandoc is not available, use python-docx to generate the .doc file directly.
5. **Clean up**: Remove the temporary markdown file.
6. **Display** the full report content to the user.
7. Tell the user: "审稿报告已生成并保存至 `{original-filename}-review.doc`。"

---

## Critical Rules

1. **Citation rules are mode-specific.** In normal mode: never cite papers. In high-level mode: ONLY Comment (1) cites papers (with APA references at the end); Comments (2)–(8) do NOT cite papers. Never fabricate citations — only cite real, existing papers.
2. **No fabrication.** Every critique must be grounded in what the paper actually says, does, or shows. Do not invent issues that are not present.
3. **Be specific.** Always reference concrete elements of the paper (table numbers, variable names, section numbers, equation numbers).
4. **Word counts are binding.** Treat each comment's word count as a hard target (±10%).
5. **Academic tone.** Write as an experienced economist/finance professor who regularly reviews for top journals.
6. **Read everything first.** You must read the full manuscript AND all table/figure files before generating any comments. Do not generate comments based on partial reading.
7. **Diverse coverage.** Comments should cover different aspects of the paper. Do not write multiple comments about the same issue.
8. **Output must be .doc.** Always produce `{original-filename}-review.doc` (named after the manuscript file). The report title, summary, all comments, AND the Letter to the Editor (with the recommendation line and Kai Wu signature) must appear in the final document.
9. **Recommendation drives tone.** The user's choice in Phase 2 Question 1 is the single source of truth: Reject → negative evaluation in Part 2 AND `Recommendation: Reject.` in the editor letter; Major Revision → neutral evaluation in Part 2 AND `Recommendation: Major Revision.` in the editor letter. These two must always be consistent.
10. **Signature is fixed.** The editor letter MUST end with the exact signature block (Kai Wu, PhD / Associate Professor of Finance / Central University of Finance and Economics / P. R. China). Do not modify, translate, or omit any line.
