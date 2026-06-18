---
name: paper-referee-revise
description: Revise an academic paper based on journal referee reports. Reads referee comments from review report or annotated manuscript, then directly modifies main.tex one comment at a time with user approval. Generates response letter after revision. Trigger when user says "referee revise" / "paper-referee-revise" / "审稿意见修改" / "根据审稿人意见修改" / "referee report".
allowed-tools: Read, Edit, Write, Glob, Grep, AskUserQuestion, Bash
argument-hint: [path-to-project-folder]
---

# Paper Referee Revise

## Overview

This skill revises an academic paper (`main.tex`) based on **journal referee reports** received during the peer review process. The user provides a project folder containing the manuscript, supporting files, and referee materials. The skill extracts referee comments, triages empirical work, then processes text revisions **one by one** with user approval, and finally drafts a response letter.

**Input**: A project folder containing:
- `main.tex` — the main manuscript (the source file; will NOT be overwritten)
- Subfolders with figures/tables (referenced by the manuscript)
- Referee materials (one or more of the following):
  - A referee report file (e.g., `referee.txt`, `referee.md`, `referee.pdf`, `report.txt`, `report.md`, `report.pdf`, `review.txt`, `review.md`, `review.pdf`, `R1.txt`, `R1.pdf`, `referee1.*`, `referee2.*`)
  - An annotated manuscript (e.g., `annotated.tex`, `annotated.pdf`) where annotations/comments from the referee serve as review comments
  - Multiple referee reports (e.g., `referee1.pdf`, `referee2.pdf`) — process each referee's comments separately

**Output**:
- If empirical comments exist: generates `empirical-revise.pdf` (empirical revision strategy) and **halts**.
- If no empirical comments (or empirical work already done): generates `main-rX.tex` (revised manuscript with changes in red) and `response-rX.tex` (response letter), then **halts**.

---

## Workflow

### Phase 1: Initialization

1. **Receive folder path** from user (via `$ARGUMENTS` or ask).
2. **Ask the user**: "本次修改为第几轮修改？(Please enter the revision round number, e.g., 1, 2, 3)" Store the answer as `X` — this determines output file names: `main-rX.tex` and `response-rX.tex`.
3. **Determine the source manuscript** based on revision round:
   - If `X = 1`: the source file is `main.tex`.
   - If `X = 2`: the source file is `main-r1.tex`.
   - If `X = 3`: the source file is `main-r2.tex`.
   - General rule: **for round X, the source file is `main-r{X-1}.tex`** (i.e., the output of the previous round). If `X = 1`, use `main.tex`.
   - Verify the source file exists. If it does not (e.g., user says round 2 but `main-r1.tex` is missing), alert the user and ask them to confirm.
4. **Scan the folder** using Glob to identify all files:
   - Locate the source manuscript file (as determined in step 3 — read only, never overwrite).
   - Locate referee materials by searching for files matching patterns: `referee*`, `report*`, `review*`, `R1*`, `R2*`, `R3*`, `annotated*`, `comments*`, `feedback*`, `revision*`.
   - If multiple referee report files are found, list them and ask the user which one(s) to use and in what order.
   - If no referee file is found, ask the user to specify the file path.
5. **Read the source manuscript** in full to understand the current state of the paper.
6. **Read all table and figure `.tex` files** from subfolders so that you have full knowledge of the paper's empirical results. This is critical for proposing accurate revisions when referees comment on results.
7. **Read the referee file(s)**:
   - For `.tex` files: look for comments marked with `%` or annotation commands (e.g., `\annotate{}`, `\comment{}`, `\todo{}`, or any custom annotation commands, or highlighted/colored text added by the referee).
   - For `.txt` / `.md` files: read the full content as referee comments.
   - For `.pdf` files: read the PDF content to extract referee text.
   - For `.docx` files: use Bash to extract text content.

### Phase 2: Extract and Structure Referee Comments

1. **Identify how many referees** provided reports (Referee 1, Referee 2, etc.). If the report contains comments from multiple referees, separate them.
2. **Parse the referee materials** to extract individual comments/suggestions from each referee.
3. **Classify each comment** by type:
   - **Empirical**: Requires new regressions, robustness checks, new tables/figures, or modifications to existing empirical results
   - **Text**: Requires only text changes to the manuscript (clarification, rewording, restructuring, adding discussion)
   - **Editorial**: Typos, grammar, formatting issues
4. **Structure each comment** as a discrete revision item with:
   - **Comment ID** (e.g., R1-1, R1-2, R2-1 for Referee 1 Comment 1, etc.)
   - **Type** (Empirical / Text / Editorial)
   - **Referee's original comment text**
   - **Location in manuscript** (section, paragraph, or specific text the comment refers to)
5. **Present the full list of comments** to the user, grouped by referee:

```
Referee 1 comments:

ID    | Type      | Location                  | Comment Summary
------|-----------|---------------------------|------------------------------------------
R1-1  | Empirical | Section 3, para 2        | Endogeneity concern, suggests IV approach
R1-2  | Text      | Section 4.1, Table 2     | Clarify discussion of control variables
R1-3  | Editorial | Section 2, para 4        | Typo in variable name

Referee 2 comments:

ID    | Type      | Location                  | Comment Summary
------|-----------|---------------------------|------------------------------------------
R2-1  | Empirical | Section 5                | Additional robustness checks needed
R2-2  | Text      | Introduction, para 3     | Clarify contribution statement

Total: N comments (X empirical, Y text, Z editorial).
```

6. **Wait for user confirmation** before proceeding.

### Phase 3: Empirical Triage

**This phase is mandatory. It runs before any text revision begins.**

1. **Identify empirical comments**: From Phase 2 classification, collect all comments typed as "Empirical" — i.e., any comment that demands:
   - New regressions or estimations (e.g., new dependent variables, new specifications, IV/2SLS/GMM, DID, RDD, etc.)
   - Additional robustness checks (e.g., alternative measures, subsample analysis, placebo tests, different fixed effects, winsorizing, clustering)
   - New summary statistics or descriptive analysis
   - New tables or figures not currently in the project folder
   - Re-running existing regressions with modifications (e.g., adding/removing control variables, changing sample period)
   - Additional tests (e.g., Hausman test, overidentification, weak instrument tests, parallel trends, balance tests)
   - Data-related requests (e.g., new data sources, extended sample, different frequency)

2. **If empirical comments exist**, generate `empirical-revise.tex` in the project folder with the following structure:

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{xcolor}

\title{Empirical Revision Strategy}
\author{}
\date{}

\begin{document}
\maketitle

\section{Overview}
This document summarizes all empirical work required to address referee comments.
Total empirical comments: N (out of M total comments).

\section{Empirical Tasks}

\subsection{[R1-1] [Brief title of the empirical task]}
\textbf{Referee's comment:} [Full text of the referee's original comment]

\textbf{Current status:} [What the paper currently does — reference existing table/figure if applicable]

\textbf{Required action:}
\begin{itemize}
  \item [Specific step 1: e.g., "Run OLS regression of Y on X with firm and year FE, adding control variables Z1, Z2"]
  \item [Specific step 2: e.g., "Store results in a new table: table_iv.tex"]
  \item [...]
\end{itemize}

\textbf{Suggested table/figure name:} [e.g., table\_iv.tex, table\_robust\_subsample.tex]

\textbf{Suggested placement:} [e.g., "Section 4.2, after Table 3" or "Appendix"]

% Repeat \subsection for each empirical comment
...

\section{Summary of New Tables/Figures Needed}
\begin{longtable}{lll}
\toprule
File name & Description & Placement \\
\midrule
table\_iv.tex & IV/2SLS results for endogeneity & Section 4.2 \\
table\_robust\_sub.tex & Subsample robustness & Section 5.1 \\
... & ... & ... \\
\bottomrule
\end{longtable}

\section{Non-Empirical Comments (For Reference)}
The following comments do not require new empirical work and will be addressed in the text revision phase:
\begin{itemize}
  \item [R1-3] [Brief summary]
  \item [R2-2] [Brief summary]
  \item ...
\end{itemize}

\end{document}
```

3. **Compile to PDF**: Run via Bash:

```bash
cd [project-folder] && pdflatex empirical-revise.tex
```

   If `pdflatex` fails, try `xelatex empirical-revise.tex`. If compilation fails entirely, inform the user that the `.tex` file is ready and they can compile it manually.

4. **HALT the program**. Display the following message and stop:

```
══════════════════════════════════════════════════════════════
实证修改策略已生成: [project-folder]/empirical-revise.pdf

共发现 N 条涉及实证的审稿意见，需要先完成以下工作：
- 新增表格: X 个
- 修改现有表格: Y 个
- 新增图表: Z 个

请完成实证工作后，将新的表格/图表文件放入项目文件夹，
然后重新运行本skill继续修改论文正文。
══════════════════════════════════════════════════════════════
```

   **Do NOT proceed to Phase 4. The program ends here.**

5. **If NO empirical comments exist**, skip this phase entirely and proceed directly to Phase 4.

---

**Re-entry after empirical work is done**: When the user re-runs this skill on the same folder after completing the empirical work, Phase 3 should detect that `empirical-revise.pdf` already exists. Ask the user to confirm: "实证修改是否已全部完成？(Has all empirical work been completed?)" If the user confirms yes, proceed to Phase 4. If not, the user should complete the remaining work first.

### Phase 4: Iterative Revision (Core Loop)

**Before starting**: Copy the source manuscript to `main-rX.tex` (i.e., for round 1 copy `main.tex` → `main-r1.tex`; for round 2 copy `main-r1.tex` → `main-r2.tex`; etc.). All subsequent edits are made to `main-rX.tex`, NEVER to the source file. Ensure `main-rX.tex` includes `\usepackage{xcolor}` in the preamble (add it if not already present) — this is required for red markup. If the source file already contains `\textcolor{red}{}` markup from a previous round, convert those red markings to normal black text first (remove the `\textcolor{red}{}` wrappers, keeping the content), so that only the current round's changes appear in red.

For each referee comment (both text-only AND empirical comments that now have completed results), follow this exact interaction pattern:

#### Step 1: Display the referee comment

```
───────────────────────────────────────────
[R1-1] (Empirical/Text/Editorial) — Referee 1, Comment 1:
[Full text of the referee's comment]
───────────────────────────────────────────
```

#### Step 2: Show original text

Locate and display the relevant passage from `main-rX.tex`:

```
Original text (main-rX.tex, lines XX-YY):
┌─────────────────────────────────────────┐
│ [The exact paragraph(s) from main-rX.tex│
│  that this comment refers to]           │
└─────────────────────────────────────────┘
```

If the comment refers to missing content (e.g., "the authors should add a discussion of X"), show the surrounding context where the new text should be inserted.

#### Step 3: Propose revision

Generate a revised version of the text that addresses the referee's comment. **All new or changed text must be wrapped in `\textcolor{red}{...}`** so that changes are visually highlighted in the compiled PDF:

```
Proposed revision:
┌─────────────────────────────────────────┐
│ [The revised paragraph with changed     │
│  portions wrapped in \textcolor{red}{}] │
└─────────────────────────────────────────┘

Rationale: [Brief explanation of what was changed and why it addresses the referee's concern]
```

**Red markup rules**:
- Only the **new or changed** portions of text should be in `\textcolor{red}{}`. Unchanged surrounding text stays in normal color.
- For entirely new paragraphs or sentences, wrap the whole addition in `\textcolor{red}{}`.
- For partial sentence edits, wrap only the changed words/phrases.
- For new table/figure references, wrap the `\ref{}` in red.
- For tables: if a table `.tex` file was modified or newly added for this revision, add `\color{red}` at the beginning of the table environment or wrap changed cells in `\textcolor{red}{}`.

#### Step 4: Ask for user decision

Use AskUserQuestion to ask:

```
Do you approve this revision? (yes / no / skip / edit)
- yes: Apply this revision to main-rX.tex
- no: I will propose a new revision (tell me what to adjust)
- skip: Skip this comment and move to the next
- edit: You provide the revised text yourself
```

#### Step 5: Handle user response

- **"yes" / "y" / "同意" / "好" / "可以"**: Use the Edit tool to replace the original text with the proposed revision in `main-rX.tex`. Record this as "applied" with both the original and revised text (needed for response letter). Confirm the change was applied, then move to the next comment.
- **"no" / "n" / "不同意" / "不行" / "重新写"**: Ask the user what they would like changed about the proposed revision, then generate a new proposal. Return to Step 3.
- **"skip" / "跳过"**: Record this as "skipped" with the user's reason (ask briefly why, if not obvious — needed for response letter to explain why we did not revise). Move to the next comment.
- **"edit" / "我来改"**: Ask the user to provide their own revised text via AskUserQuestion, then apply that text (with `\textcolor{red}{}` markup) using the Edit tool. Record as "applied". Move to the next comment.

**Important**: Maintain a revision log throughout Phase 4. For each comment, record:
- Comment ID and full referee text
- Whether applied or skipped
- The final revised text (if applied) or reason for skipping
- **Effort level** (high-effort / low-effort — see Phase 5 for the criteria) so the response letter can be sized correctly
- The **complete** revised passage(s) as they appear in `main-rX.tex`, including all `\textcolor{red}{}` markup and the exact figure/table numbers (`\ref{}`, "Table 3", "Figure 2", etc.)
- This log is essential for generating the response letter in Phase 5.

### Phase 5: Response Letter

After all comments have been processed, generate a **highly detailed** response letter as `response-rX.tex` in the project folder. This response letter is a primary deliverable — referees and editors judge a revision largely by it, so it must read as a thorough, self-contained account of every change. A thin response letter (a sentence or two per comment) signals a superficial revision and invites rejection; a thorough one demonstrates that every concern was taken seriously.

#### Length target

The finished PDF's overall heft scales with the total number of referee comments:
- **14 or fewer comments**: roughly **five pages per comment** — e.g., 5 comments ≈ 25 pages, 10 comments ≈ 50 pages, 14 comments ≈ 70 pages.
- **More than 14 comments**: roughly **four pages per comment** — e.g., 20 comments ≈ 80 pages, 30 comments ≈ 120 pages.

Count the total across all referees to pick the multiplier. This is a guideline for overall heft, not a quota to pad: the length comes naturally from (a) a substantive narrative of the revision approach and (b) **complete, verbatim** excerpts of every revised passage. High-effort comments will run well over the per-comment average; short editorial fixes will run under. Aim for the aggregate target across the whole letter. If the draft is far short of it, the usual cause is that excerpts were truncated or the narrative was too terse — fix those rather than inserting filler.

#### Classifying each comment by effort

Before writing each response, decide whether the comment was **high-effort** or **low-effort**:
- **High-effort**: empirical comments (new regressions, robustness checks, IV/DID/RDD, new tables/figures); comments requiring a new section, a substantially rewritten argument, a new theoretical discussion, or revisions spanning multiple parts of the paper. Anything that materially changed the paper's analysis or structure.
- **Low-effort**: clarifications, rewording, adding a sentence or short paragraph, fixing terminology, editorial/typo fixes, single-location minor edits.

When in doubt, treat the comment as high-effort — a fuller explanation never hurts.

#### Per-comment structure

Each comment's response has three parts, in this order:

1. **Narrative of revision approach and method.** Explain in prose how the comment was addressed and why this approach resolves the referee's concern.
   - **High-effort comments: 300–500 words.** Walk through the reasoning: what the referee was concerned about, what options were considered, the approach chosen and why, the method/specification used, what the new results show (with actual coefficients, t-statistics, significance levels read from the table/figure files), and how this strengthens the paper. For empirical work, describe the estimation in enough detail that the referee can follow it without re-deriving it.
   - **Low-effort comments: 100–200 words.** Concisely state what was changed and why it addresses the comment.
2. **Complete verbatim excerpt of the revised content.** Quote the revised passage(s) from `main-rX.tex` in full — **never abbreviate, never use ellipses, never write "[...]" or "the paragraph now reads ...".** Reproduce every revised paragraph, sentence, table caption, or figure note in its entirety. If the revision touches several locations, excerpt every one of them, each labeled with its section/location.
3. The changed portions inside the excerpt stay wrapped in `\textcolor{red}{}`, exactly as in `main-rX.tex`, so the referee sees precisely what is new.

**Figure and table numbering**: When excerpting, keep every figure and table number identical to the manuscript — do not renumber. If the revised text says "Table 3" or contains `\ref{tab:iv}`, reproduce it verbatim. The referee must be able to cross-reference the letter against the paper without confusion.

#### Template

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage{longtable}

\title{Response to Referee Comments}
\author{}
\date{}

\begin{document}
\maketitle

We sincerely thank the referees for their careful reading of our manuscript and their constructive comments and suggestions. We have carefully considered each comment and revised the manuscript accordingly. Below, we provide a detailed, point-by-point response to each comment. All changes in the revised manuscript are highlighted in {\textcolor{red}{red}}, and we reproduce the revised passages in full so they can be read alongside the manuscript.

\section{Response to Referee 1}

\subsection*{Comment R1-1}
\textbf{Referee's comment:} ``[Full, complete text of the referee's original comment — do not abbreviate.]''

\textbf{Response:} [The revision-approach narrative. 300--500 words for a high-effort comment; 100--200 words for a low-effort comment. Substantive prose explaining the approach, method, and — for empirical work — the actual results.]

\textbf{Revised text in the manuscript:} The relevant passage(s) now read as follows. [Then reproduce every revised passage IN FULL, with changed portions in \textcolor{red}{red}, and with all figure/table numbers identical to the manuscript. If multiple locations were revised, label and quote each one, e.g.:]

\textit{Section 4.2, after Table 3:}
\begin{quote}
[Complete revised paragraph, verbatim, with \textcolor{red}{} markup intact.]
\end{quote}

% For skipped comments: keep the same three-part structure where it applies —
% give a substantive narrative (still 100--500 words by effort level) explaining
% respectfully why no change was made. If no text changed, the "Revised text"
% block is omitted.

% Repeat \subsection* for every comment...

\section{Response to Referee 2}
% Same structure...

\end{document}
```

**Response letter rules**:
- Begin each response with sincere thanks to the referee (vary the phrasing — do not use the same sentence for every comment).
- Quote the referee's **complete** comment text — never trim it.
- For **applied revisions**: give the effort-sized narrative, then the complete verbatim excerpt(s) with red markup and original figure/table numbering.
- For **skipped comments**: provide a respectful, substantive explanation of why no change was made, sized by effort level (100–500 words). Never dismiss a referee's concern.
- For **empirical comments**: in the narrative, describe the new analysis in detail and report the actual key results (coefficients, t-statistics, significance levels) read from the real table/figure files; reference the new table/figure by the number it carries in the manuscript.
- Never truncate an excerpt. If a revised passage is long, that is expected — reproduce all of it.
- The response should demonstrate that each comment was taken seriously and addressed thoroughly.
- Maintain a professional, collegial tone throughout.

**Compile to PDF**:

```bash
cd [project-folder] && pdflatex response-rX.tex
```

**HALT the program** after generating the response letter. Display:

```
══════════════════════════════════════════════════════════════
修改完成！

修改后的论文: [project-folder]/main-rX.tex
回复信: [project-folder]/response-rX.tex

修改统计：
- Referee 1: Applied X/N comments (skipped: Y)
- Referee 2: Applied X/N comments (skipped: Y)
- 总修改: A 处 (实证: B, 文字: C, 编辑: D)

请检查 main-rX.tex 和 response-rX.tex，确认无误后提交。
══════════════════════════════════════════════════════════════
```

---

## Writing Rules

### Style and Formatting

- Maintain the **same writing style** as the original manuscript (do not change the overall tone or voice).
- Preserve all **LaTeX formatting**: `\section{}`, `\subsection{}`, `\ref{}`, `\cite{}`, `\citep{}`, math environments, etc.
- Preserve all **labels** (`\label{}`), **cross-references** (`\ref{}`), and **citations** intact unless the referee specifically asks to change them.
- When adding new citations, use the same citation style as the rest of the paper (typically 30% `\cite{}` / 70% `\citep{}`).
- When reporting regression results, use **t-statistics in parentheses** and **"significant at X% level"** — no p-values or confidence intervals.
- **Avoid the em-dash (`---`)**: Do not use the LaTeX em-dash `---` in revised or newly written prose (including text inside `\textcolor{red}{}` markup). It is a common AI-writing tell and clutters academic text. Replace each occurrence with the punctuation its grammatical role calls for: a parenthetical aside becomes parentheses (or commas if short); a connector before an explanation becomes a colon or semicolon; an abrupt shift becomes a period and two sentences; a list continuation becomes a comma plus a connecting word. Leave the en-dash `--` used for page and number ranges untouched (e.g., `pages={259--271}`, `2012--2026`). When a revision touches a paragraph, also strip any pre-existing `---` from that paragraph as part of the edit.

### Red Markup

- All new or modified text in `main-rX.tex` MUST be wrapped in `\textcolor{red}{...}`.
- This applies to: changed words, new sentences, new paragraphs, new table/figure references, modified table content.
- Unchanged text surrounding the edits stays in default (black) color.
- Ensure `\usepackage{xcolor}` is in the preamble.

### Revision Principles

- **Minimal changes**: Only modify what is necessary to address the referee's comment. Do not rewrite entire paragraphs when a sentence-level edit suffices.
- **Preserve structure**: Do not reorganize sections or move paragraphs unless the referee specifically requests it.
- **No fabrication**: Never invent data, results, or citations. If the referee asks for additional analysis not present in the tables/figures, flag this to the user rather than making up results.
- **Consistency**: After each revision, ensure the changed text is consistent with surrounding paragraphs (transitions, terminology, notation).
- **Scope discipline**: Only address what the referee asked for. Do not make additional "improvements" beyond the scope of each comment.
- **Respect the referee**: Revisions should genuinely address the referee's concern, not superficially dismiss or sidestep it. When a referee raises a valid point, the revision should substantively strengthen the paper.

### Handling Special Cases

- **Empirical comment (re-entry)**: For empirical comments whose tables/figures are now ready, read the new table/figure `.tex` files first, then propose the text revision that discusses the new results. Wrap all new text in `\textcolor{red}{}`.
- **Comment refers to a table/figure**: Read the relevant table/figure `.tex` file from the project folder before proposing the revision, to ensure accuracy of reported coefficients, t-statistics, significance levels, sample sizes, etc.
- **Comment asks for new content**: Propose where to insert it (after which paragraph/section) and draft the new text in red.
- **Comment asks to delete content**: Show what will be removed and confirm before deleting. In the response letter, explain why the content was removed.
- **Comment is vague or unclear**: Present your interpretation to the user and ask for clarification before proposing a revision.
- **Comment requires changes in multiple locations**: Handle each location as a sub-item (e.g., R1-3a, R1-3b, R1-3c) within the same comment block.
- **Comment about bibliography/references**: If changes involve `ref.bib` or similar bibliography files, modify those files as well.
- **Contradictory referee comments**: If Referee 1 and Referee 2 give contradictory suggestions, flag the contradiction to the user and ask how they want to handle it before proposing any revision.
- **Comment about the abstract**: If a revision changes a key claim or result description in the body, check whether the abstract also needs updating and propose that change as a sub-item.

---

## Language

- Communicate with the user in **Chinese** (the user's preferred language for interaction).
- Write all LaTeX content and revisions in **English** (academic paper language).
- Write the response letter in **English** (standard for journal correspondence).
- Referee comment display should preserve the original language of the referee report.
