---
name: paper-writer
description: Automatically write empirical sections of academic papers in LaTeX by reading tables/figures from a PDF. Trigger when user wants to write a paper from empirical results, has tables/figures in PDF, or says "write paper" / "paper-writer" / "写论文".
allowed-tools: Read, Bash, Edit, Write, Glob, Grep, AskUserQuestion, WebSearch, WebFetch
argument-hint: [path-to-pdf]
---

# Paper Writer

## Overview

This skill writes the **empirical sections** of an academic finance/economics paper in LaTeX format. The user provides a PDF containing all tables and figures. The skill reads each table/figure sequentially, asks the user for the desired word count, then writes that section following established academic writing conventions.

**Scope**: Introduction, Literature Review, Hypothesis Development (verbal or theoretical model), research design sections (Data and Sample, Variable Construction, Empirical Model), empirical results, and conclusion. Does NOT write: Institutional Background.

## Workflow

### Phase 1: Initialization

1. **Receive PDF path** from user (via `$ARGUMENTS` or ask).
2. **Read the PDF** to identify all tables and figures. Use the Read tool with the PDF file path. For large PDFs, read in page ranges (e.g., `pages: "1-20"`).
3. **Build a section plan**: Map each table/figure to its empirical section. Present the plan to the user for confirmation:

```
I have identified the following tables/figures and mapped them to sections:

Section                          | Tables/Figures    | Default Words
---------------------------------|-------------------|-------------
Descriptive Statistics           | Table 1, Fig 1-2  | 400
Baseline Regression              | Table 2           | 650
Endogeneity                      | Table 3           | 800
Robustness Checks                | Table 4-6         | 1000
Cross-sectional Heterogeneity    | Table 7-8         | 500 per dimension
Mechanism Analysis               | Table 9           | 600 per mechanism
Alternative Explanation          | Table 10          | 750
Further Analysis                 | Table 11          | 650
Conclusion                       | (no table)        | 350

Shall I proceed with this plan, or would you like to adjust?
```

4. **Ask for output path**: Where to save the LaTeX file (default: same directory as the PDF, named `main.tex`).
5. **Scan results/ directory**: Extract all `\label{}` from table/figure .tex files for label synchronization.

**IMPORTANT — Writing Order vs. Document Order**:

The **writing order** follows the logic of academic paper development (empirical results first, then build context around them). The **document order** is the standard paper structure. These are different:

```
Writing Order                              Document Order (final assembly)
─────────────                              ──────────────────────────────
① Phase 2: Empirical Results          →   Section 1. Introduction
② Phase 3: Research Design            →   Section 2. Institutional Background (if needed)
③ Phase 4: Lit Review & Hypotheses    →   Section 3. Literature Review
④ Phase 5: Introduction + Title +     →   Section 4. Theoretical Framework / Hypotheses
            Abstract + Inst. Bkg.          Section 5. Data and Methodology
⑤ Phase 6: Conclusion                 →   Section 6. Empirical Results
⑥ Phase 7: Assembly & Finalize        →   Section 7. Conclusion
                                           References → Figures → Tables
                                           Online Appendix → Proofs → Appendix Tables
```

Writing empirical results first ensures that all subsequent sections (research design, literature review, hypotheses, introduction) are grounded in the actual findings.

---

### Phase 2: Empirical Results (WRITE FIRST)

Write the empirical sections first, as they are directly grounded in the tables/figures from the PDF. This becomes Section 6 (Empirical Results) in the final document.

For each section in the plan, follow this exact interaction pattern:

1. **Prompt the user**:
   ```
   下面开始写 [Section Name]（[Table/Figure X]）。需要多少词？
   ```
2. **Wait for user input** (word count number).
3. **Read the relevant table/figure pages** from the PDF using the Read tool.
4. **Write the section** following the prompt template and writing rules.
5. **Append the section directly into `main.tex`**. Do NOT save sections as separate `.tex` files (e.g., `intro.tex`, `lit_review.tex`). All section bodies live in a single `main.tex` file. The only `\input{}` calls in `main.tex` should be for table/figure files in `results/`.
6. **Move to the next section**.

### Phase 3: Research Design (WRITE SECOND)

After completing all empirical sections, write the research design sections. These rely on the variable definition tables in the PDF and the empirical model specifications visible in the regression tables. This becomes Section 5 (Data and Methodology) in the final document. Follow the same interactive pattern as Phase 2.

For each section, prompt the user:
```
下面开始写 [Section Name]。需要多少词？
```

Write in this order:

1. **Data and Sample Construction**: Two sub-parts:
   - **Data Sources**: Describe all relevant data sources (e.g., CSMAR, Wind, CNRDS, Guba) in detail.
   - **Sample Construction**: Describe the sample construction procedure, filtering criteria, and final sample size.

2. **Variable Construction**: Describe how each key variable is constructed. Cover ONLY the dependent variable(s) and the core independent variable — do NOT include control variables here (controls are described in Empirical Model). Reference the variable definition table in the PDF. Cite the original papers that proposed each measure where applicable.

   **Subsection titles MUST reflect the actual indicator content, not generic placeholders.** Read the variable definition table to identify the actual measures and name the subsections accordingly. Examples:
   - If the dependent variable measures innovation output (patent counts, citations), use `\subsection{Measuring Corporate Innovation}` — NOT `\subsection{Dependent Variable}`.
   - If the independent variable is investor disagreement (e.g., divergence of analyst forecasts), use `\subsection{Measuring Investor Disagreement}` — NOT `\subsection{Independent Variable}`.
   - Pattern: `\subsection{Measuring [actual concept]}` or `\subsection{[Concept Name]}`. Avoid the generic words "Dependent Variable" / "Independent Variable" in the subsection title.

3. **Empirical Model**: Produce the econometric model in LaTeX equation format (use $X$ to express the vector of control variables, use Greek letters for fixed effects). Describe the empirical model and all variables in the equation. **Include the description of control variables in this subsection** — list the controls used, briefly justify their inclusion, and cite supporting literature. Reference the baseline regression table for the model specification. Cite methodological literature where appropriate.

4. **Descriptive Statistics**: Describe key variables from the summary statistics table.

#### Section-Specific Templates for Research Design

| Section | Key Instructions |
|---------|-----------------|
| Data and Sample Construction | Data sources (~300 words) + Sample construction (~200 words). Default ~500 words total. |
| Variable Construction | Describe ONLY the dependent variable(s) and the core independent variable. Subsection titles must reflect actual indicator content (e.g., `Measuring Corporate Innovation`), NOT generic words like "Dependent Variable". Reference variable definition table. Default ~600 words. |
| Empirical Model | Produce the equation in `\begin{equation}...\end{equation}` format. Describe each component AND describe the control variables (controls live here, not in Variable Construction). Default ~500 words. |
| Descriptive Statistics | Choose the most important variables. Report mean and other statistics. Default ~400 words. |

### Phase 4: Literature Review and Hypothesis Development (WRITE THIRD)

After completing empirical results and research design, write the Literature Review and Hypothesis Development. These become Sections 3-4 in the final document. Writing these after the empirical work ensures the literature framing and hypotheses are properly aligned with the actual findings.

#### Step 1: Literature Review

1. **Analyze the paper's content** (tables, figures, empirical results already written) to identify the key research themes.
2. **Propose a literature review plan** to the user:
   ```
   根据本文的研究内容，我建议 Literature Review 分为以下 [N] 个部分：
   1. [Strand 1 topic and brief rationale]
   2. [Strand 2 topic and brief rationale]
   3. [Strand 3 topic and brief rationale]
   ...
   请确认或调整以上分类。总共需要多少词？
   ```
3. **Wait for user confirmation/adjustment** and total word count. The AI allocates words across strands proportionally, or the user can specify per-strand word counts.
4. **Write each strand** as a `\subsection{}` under `\section{Literature Review}`. Follow these rules:
   - Cite relevant and important literature published from 2010-2026, and make sure recent top-journal work (2023-2026) is well represented (see the Reference Requirements rule below).
   - All responses must be based on academic facts. Avoid generating fabricated literature / data / conclusions.
   - All viewpoints and content must be annotated with supporting evidence.
   - List references with DOI link in APA format at the end.
   - Do NOT use bullet points. Use flowing academic prose.
   - At the end of each strand, clearly state how this paper contributes to / differs from the existing literature.
   - **Citation ratio (Literature Review only): approximately 50% `\cite{}` (前引) and 50% `\citep{}` (后引).** Across the entire Literature Review section, count roughly equal numbers of each. Use `\cite{}` for sentences where the cited author is the grammatical subject ("\cite{baker2003} document...", "As argued by \cite{hall2012}..."), and `\citep{}` for parenthetical support ("...prior work shows X \citep{baker2003}"). After drafting each strand, review the citations and rebalance toward 50/50 if needed.

#### Step 2: Hypothesis Development

1. **Ask the user**:
   ```
   下面开始写 Hypothesis Development。请选择论证方式：
   (A) 文字论述 (verbal arguments)
   (B) 理论模型 (theoretical model with proofs)
   ```
2. **Wait for user input** (A or B).

##### Option A: Verbal Arguments (文字论述)

The number and content of hypotheses are derived from the empirical results:
- **H1 (Baseline)**: One hypothesis corresponding to the baseline regression finding. Formulated as: "The first hypothesis is..."
- **H2, H3, ... (Heterogeneity)**: Additional hypotheses corresponding to the cross-sectional heterogeneity results. Each hypothesis captures a moderating effect. Formulated as: "The second hypothesis is..." etc.

For each hypothesis:
1. Ask: `下面开始写 Hypothesis [N]（对应 [Baseline/Heterogeneity Table X]）。需要多少词？`
2. Write the argument FIRST (economic reasoning, cite literature), THEN state the hypothesis at the end.
3. Pattern: reasoning → "Based on the above arguments, we propose the following hypothesis:" → `\textbf{Hypothesis [N]:} ...`
4. The argument should incorporate the mechanisms documented in the study but should NOT mention empirical findings explicitly (write as if you do not know the results).
5. Cite relevant literature from 2010-2026 to support each argument, including recent top-journal work (2023-2026) where it bears on the channel.

##### Option B: Theoretical Model (理论模型)

Build a formal theoretical model with propositions/theorems that correspond to the baseline result and mechanism channels.

1. Ask: `理论模型需要覆盖哪些结果？（默认：baseline + mechanism channels）需要多少词？`
2. Write the model in three parts under `\section{Theoretical Framework}`:

   **Part 1: Model Setup** (`\subsection{Model Setup}`)
   - Describe assumptions, variable definitions, functional forms.
   - Use LaTeX for all mathematical formulas.
   - Present in flowing academic style (no bullet points).
   - Default ~500 words.

   **Part 2: Main Results** (`\subsection{Main Results}`)
   - State Theorem/Proposition 1 (corresponding to baseline: discordance → innovation).
   - State Theorem/Proposition 2+ (corresponding to mechanism channels).
   - For each theorem: state it formally in a `\begin{theorem}...\end{theorem}` environment, then provide a brief intuition (~100 words).
   - Default ~400 words.

   **Part 3: Discussion** (`\subsection{Discussion}`)
   - Discuss implications and limitations of the model.
   - Explain how the model provides theoretical foundation for the empirical analysis.
   - Default ~200 words.

   **Appendix: Proofs** (separate file or appendix section)
   - Write detailed mathematical proofs for ALL theorems.
   - Use `\begin{proof}...\end{proof}` environment.
   - Proofs should be logically rigorous with clear steps.
   - Save as appendix content: `\appendix \section{Proofs of Theoretical Results}`

### Phase 5: Introduction (WRITE FOURTH)

Write the Introduction after all substantive sections are complete. This ensures the motivation, findings summary, and contributions are fully informed by the actual results. This becomes Section 1 in the final document.

#### Step 5a: Identify Target Journal Field

1. **Analyze the paper's content** (topic, methodology, data, contribution) and **propose the most suitable SSCI journal field and specific top journals**:
   ```
   根据本文的研究内容，我建议投稿领域和目标期刊如下：
   领域：[Finance / Economics / Accounting / Management]
   推荐期刊：
   1. [Top journal 1] — [brief rationale]
   2. [Top journal 2] — [brief rationale]
   3. [Top journal 3] — [brief rationale]
   请确认目标期刊，Introduction 的写作风格将参考该期刊。
   ```
2. **Wait for user confirmation**. The confirmed journal determines:
   - Writing style and tone (e.g., JFE is concise and results-driven; AER emphasizes broader economic implications)
   - Citation focus (prioritize literature published in that field's top journals)
   - Framing (finance journals emphasize market mechanisms; economics journals emphasize welfare/efficiency)

#### Step 5b: Paper Title

1. **Propose 10 titles** that match the target journal's conventions:
   ```
   根据本文内容和目标期刊 [Journal Name] 的风格，我建议以下 10 个标题：
   1. [title]
   ...
   10. [title]
   请选择一个标题，或提供你自己的标题。
   ```

**Title style guidelines by journal**:
- **JFE/JF**: Concise, often a noun phrase or question. E.g., "Does X Affect Y?", "The Real Effects of X"
- **RFS**: Similar to JFE but slightly more descriptive. May include subtitle with colon.
- **AER/QJE**: Broader framing, emphasize economic mechanism. E.g., "X: Evidence from Y"
- **TAR/JAR**: Accounting-specific framing, often includes the information/disclosure angle.
- **MS/SMJ**: Management framing, emphasize strategic implications.

2. **Wait for user selection**. Place the title in the LaTeX output as `\title{...}`.

#### Step 5c: Abstract, JEL Codes, and Keywords

1. **Abstract (~130 words)**: Summarize the research question, data/method, key findings, and contribution in one concise paragraph.
2. **JEL Codes (3)**: Select the three most relevant JEL classification codes.
3. **Keywords (4)**: Four keywords in one line separated by commas, all in lowercase.

**Interaction pattern**:
```
下面生成 Abstract、JEL codes 和 Keywords。
Abstract 默认 130 词，请确认或调整。
```

#### Step 5d: Institutional Background (Conditional)

Assess whether an Institutional Background section is needed.

**Decision logic**: Evaluate whether the research setting would be unfamiliar to the target journal's typical readership.
- **Likely needed**: China/emerging market data targeting a global journal, studies exploiting specific policy shocks
- **Likely NOT needed**: US/UK data targeting a US/UK journal, well-established settings

**Interaction pattern**:
```
关于 Institutional Background：
本文使用 [setting] 数据，目标期刊为 [journal]。
[AI's assessment: 建议添加 / 建议不添加]
理由：[brief rationale]
是否添加？如果添加，需要多少词？
```

If added, write as `\section{Institutional Background}` placed between Introduction and Literature Review. Do NOT cite literature. Do NOT use bullet points.

#### Step 5e: Write Introduction

The Introduction consists of 5 parts, written as `\section{Introduction}` without subsection headings.

**Interaction pattern** — ask for ALL five word counts at once:
```
下面开始写 Introduction（目标期刊：[Journal Name]）。
各部分默认词数如下，请确认或调整：
1. Motivation: 800 词
2. Why this setting: 120 词
3. What we do and find: 400 词
4. Contributions (3个贡献): 400 词
5. Roadmap: 70 词
```

**Part 1: Motivation** — Motivate the research question. Cite literature from 2010-2026, anchoring the question in recent top-journal work (2023-2026). Do NOT talk about findings, contributions, or setting.
**Part 2: Why This Setting** — Explain why the data/market is ideal. 2-3 institutional reasons.
**Part 3: What We Do and What We Find** — Summarize strategy and results. No citations. No bullet points.
**Part 4: Contributions** — Three strands of literature. Cite target journal's field literature.
**Part 5: Roadmap** — "The remainder of the paper proceeds as follows..."

### Phase 6: Conclusion (WRITE FIFTH)

Write the Conclusion last. This becomes Section 7 in the final document.

**Interaction pattern**:
```
下面开始写 Conclusion。需要多少词？（默认 350）
```

Summarize main findings, contributions, policy implications, and limitations. Do NOT cite literature in conclusion. Do NOT use bullet points.

### Writing Rules (apply to ALL phases)

When writing each section, follow ALL of these rules strictly:

#### Content Rules
- Write in formal academic English suitable for a top finance/economics journal.
- **Use American English throughout the entire paper.** Spelling: "behavior" (not "behaviour"), "analyze" (not "analyse"), "modeling" (not "modelling"), "labor" (not "labour"), "organization" (not "organisation"), "center" (not "centre"), "favor" (not "favour"), "program" (not "programme"). Vocabulary/usage: prefer "toward" (not "towards"), "while" (not "whilst"). Date format: month-day-year. This rule applies to every section, including Introduction, Literature Review, Hypothesis Development, Research Design, Empirical Results, and Conclusion.
- All claims must be grounded in the tables/figures provided. Report specific coefficients, t-statistics, significance levels, and R-squared values from the tables.
- Cite relevant and important literature published from 2010-2026 (see the Reference Requirements rule below for the overall count and recency floors).
- **All responses must be based on academic facts. Avoid generating fabricated literature / data / conclusions.**
- All viewpoints and content must be annotated with supporting evidence.
- Do NOT use bullet points. Use flowing academic prose.
- Do NOT fabricate any numbers — only report what is visible in the tables/figures.
- When describing regression results, follow this pattern: report the key coefficient, its sign, significance level (stars), and economic interpretation.
- **Never use the em-dash (`---`)** in any section you draft. The LaTeX em-dash `---` is a common AI-writing tell and clutters academic prose. Use the punctuation the sentence's logic calls for instead: parentheses (or commas) for a parenthetical aside; a colon or semicolon for a connector before an explanation; a period and two sentences for an abrupt shift; a comma plus a connecting word for a list continuation. The en-dash `--` for page and number ranges remains correct and should still be used (e.g., `2012--2026`).

#### Reference Requirements (apply to the whole paper)

A top-journal manuscript engages the field densely and currently. Editors and referees read a thin or dated bibliography as a signal that the author has not done the homework, so hold the assembled paper to two floors:

- **At least 50 distinct references** in `ref.bib`. Citations accumulate across the citation-heavy sections (Introduction motivation and contributions, Literature Review, Hypothesis Development, Variable Construction, Empirical Model), so seed enough as you write each of those rather than trying to bolt references on at the end. Fifty is a floor, not a target to stop at; a typical empirical finance/economics paper cites 50-90.
- **At least 15 of those references published in 2023-2026 in top international journals.** This recency floor demonstrates the paper speaks to the live frontier. "Top international journals" means the discipline's leading outlets; weight the set toward the target journal's own field:
  - *Finance:* Journal of Finance, Journal of Financial Economics, Review of Financial Studies, Journal of Financial and Quantitative Analysis.
  - *Economics:* American Economic Review, Quarterly Journal of Economics, Journal of Political Economy, Econometrica, Review of Economic Studies, Review of Economics and Statistics, American Economic Journal series.
  - *Accounting:* Journal of Accounting and Economics, Journal of Accounting Research, The Accounting Review, Review of Accounting Studies, Contemporary Accounting Research.
  - *Management / general:* Management Science, Strategic Management Journal, Organization Science.

**Non-fabrication overrides the quota.** A recency floor is exactly the pressure that tempts a model to invent plausible-looking recent papers, and a fabricated or misattributed citation is worse than a missing one: referees wrote the very frontier you are citing and will catch it. So never manufacture an entry to reach a count. When you need recent work to satisfy the 2023-2026 quota, use `WebSearch` / `WebFetch` to find real, verifiable papers (correct authors, exact title, journal, year, and a working DOI) and cite those. If after genuine searching you still cannot reach 15 verifiable recent top-journal papers on the topic, stop and tell the user the number you found and which strands are thin, rather than filling the gap with invented references. Meeting the floors honestly is the goal; faking them defeats the purpose.

#### LaTeX Format Rules
- Use `\section{}` and `\subsection{}` for headings.
- **No blank line between a heading and the paragraph that follows.** The first paragraph of body text must start on the line immediately after `\section{...}`, `\subsection{...}`, or `\subsubsection{...}` — do not insert an empty line in between. Blank lines BETWEEN paragraphs of body text are fine; the rule applies only to the heading→first-paragraph boundary. Example:
  ```latex
  \section{Empirical Results}
  This section presents our baseline findings ...   % ← no blank line above
  ```
  NOT:
  ```latex
  \section{Empirical Results}

  This section presents our baseline findings ...   % ← wrong: blank line above
  ```
- Reference tables as `Table~\ref{tab:X}` and figures as `Figure~\ref{fig:X}`.
- **Citation style**: Mix `\cite{}` (前引, inline) and `\citep{}` (后引, parenthetical). Use `\cite{}` when the author is the grammatical subject (e.g., "\cite{baker2003} find that..."). Use `\citep{}` when the citation is parenthetical support (e.g., "...consistent with prior evidence \citep{baker2003}").
  - **Default ratio (Introduction, Hypothesis Development, Empirical Results, etc.):** approximately 30% `\cite{}` and 70% `\citep{}`.
  - **Literature Review section ONLY:** approximately 50% `\cite{}` and 50% `\citep{}`. The Literature Review surveys the field and benefits from a heavier presence of author-as-subject sentences ("\cite{baker2003} document that..."), so balance the two roughly evenly across the entire Literature Review.
- Do NOT produce a full document preamble — only section content.
- Mathematical notation: use `$...$` for inline math, `\begin{equation}...\end{equation}` for display math.
- Math environments available: `theorem`, `proposition`, `lemma`, `corollary`, `assumption`, `definition`, `remark`, `proof`. Use `\begin{theorem}...\end{theorem}` etc. Packages loaded: `amsmath`, `amssymb`, `amsthm`, `mathtools`.

#### Significance Reporting Rules
- Do NOT report t-statistics for every coefficient. Mix t-statistics with verbal significance descriptions.
- **50-60% of significance reports** should use verbal descriptions such as "significant at the 1\% level", "statistically significant at the 5\% level", "marginally significant at the 10\% level", "statistically insignificant".
- **40-50%** may include t-statistics in parentheses, e.g., "$-0.0116$ ($t = -2.68$)".
- Vary the expression patterns to avoid monotony. Examples of verbal forms:
  - "the coefficient is negative and highly significant"
  - "significant at the 1\% level"
  - "the estimate is statistically indistinguishable from zero"
  - "the result is significant at conventional levels"

#### Table/Figure Placement
- **The "Insert ... about here" block is for main-body tables and figures only.** At the end of each empirical subsection that discusses a main-body table/figure, insert a placement block using the **actual label** from the table/figure source file. The block must use a centered environment with parentheses (not square brackets):
  ```
  \begin{center}
  (Insert Table \ref{actual_label} about here)
  \end{center}
  ```
- If a section references multiple tables, list them all inside the same centered block:
  ```
  \begin{center}
  (Insert Table \ref{label1} and Table \ref{label2} about here)
  \end{center}
  ```
- For figures, use the same pattern with `Figure` instead of `Table`:
  ```
  \begin{center}
  (Insert Figure \ref{actual_label} about here)
  \end{center}
  ```
- Do NOT use the older `\bigskip \noindent [Insert ... about here]` form with square brackets.
- **Online Appendix tables/figures get NO "Insert ... about here" block.** Anything that lives in the Online Appendix (e.g., variable-definition tables, robustness checks, and other supplementary exhibits with `S`-numbering) is not placed in the body. Just mention and cross-reference it in prose, pointing the reader to the appendix. For example: "Detailed variable definitions are provided in Table~\ref{actual_label} of the Online Appendix." or "The results are robust to these alternatives (see Table~\ref{actual_label} in the Online Appendix)." The "Insert ... about here" markers signal where main-body exhibits should be typeset; appendix exhibits are already collected in the appendix, so a placement marker there would be redundant.
- **IMPORTANT**: Before writing, scan all table/figure .tex files in the results directory to extract their `\label{}`. Use these actual labels throughout the text. Never use placeholder labels like `tab:1` or `tab:X`.

#### Section-Specific Templates

Read the full templates from `references/prompt_templates.md`. Key defaults:

| Section | Key Instructions |
|---------|-----------------|
| Descriptive Statistics | Choose the most important variables. Report mean and other statistics. Add ~50 words for correlation matrix if present. |
| Baseline Regression | Describe the main finding. Interpret economic significance. Discuss fixed effects and controls. |
| Endogeneity | Describe each endogeneity test (IV/2SLS, PSM, DID, etc.). Explain why each instrument/method is valid. |
| Robustness Checks | Write ALL robustness tests together in one section. Adjust length based on number of tests. |
| Cross-sectional Heterogeneity | Explain the economic intuition behind each subsample split. Link to hypotheses if applicable. **Default ~500 words per heterogeneity dimension** (e.g., two dimensions → ~1000 words total). Ask the user for the number of dimensions if not obvious from the tables. |
| Mechanism Analysis | Describe the channel/mechanism tests. Explain the causal chain. **Default ~600 words per mechanism** (e.g., two mechanisms → ~1200 words total). Ask the user for the number of mechanisms if not obvious from the tables. |
| Alternative Explanation | Address potential alternative explanations and how the tests rule them out. |
| Further Analysis | Describe additional analyses that extend the main findings. |
| Conclusion | Summarize main findings, contributions, policy implications, and limitations. Do NOT cite literature in conclusion. |

### Phase 7: Finalization and Assembly

After all sections are written, assemble the complete LaTeX document.

#### Step 1: Document Structure

**Single-file rule.** The body of the paper (Introduction, Institutional Background, Literature Review, Theoretical Framework / Hypothesis Development, Data and Methodology, Empirical Results, Conclusion) lives entirely inside `main.tex`. Do NOT split section bodies into separate files like `intro.tex`, `lit_review.tex`, `empirical_results.tex`, `conclusion.tex`, etc. The only `\input{}` calls in `main.tex` are for tables/figures stored in `results/` and (optionally) appendix tables. If a draft already has body sections in separate files, paste their content into `main.tex` and delete the standalone files.

The output is a single `main.tex` file with the following structure:

```latex
\documentclass[12pt,a4paper]{article}
% ... preamble with all packages, math environments, formatting ...

\begin{document}
\begin{titlepage}
  \title{...}
  \author{...}
  \date{...}
  \maketitle
  \begin{abstract} ... \end{abstract}
\end{titlepage}

% Double-spaced body
\renewcommand{\baselinestretch}{2}
\normalsize \baselineskip=25pt

\section{Introduction}
\section{Institutional Background}   % if applicable
\section{Literature Review}
\section{Theoretical Framework / Hypothesis Development}
\section{Data and Methodology}
\section{Empirical Results}
\section{Conclusion}

% References (after Conclusion, before figures/tables)
\clearpage
\bibliographystyle{jfe}
\bibliography{ref}

% Figures first, then main-body Tables (after references, before appendix)
\clearpage
\begin{figure}...\end{figure}
\clearpage
\input{results/table1.tex}
% ... main-body tables only (NOT variable definitions or robustness tables) ...

% Appendix last
\clearpage
\begin{large}
\begin{center}
\bf [Paper Title]\\ Online Appendix
\end{center}
\end{large}
\setcounter{figure}{0}
\setcounter{table}{0}
\renewcommand{\thetable}{S\arabic{table}}
\renewcommand{\thefigure}{S\arabic{figure}}
\appendix
\section{Proofs of Theoretical Results}
% ... proofs ...

% Appendix tables (variable definitions, robustness checks)
\clearpage
\input{results/variables.tex}
\clearpage
\input{results/robustness1.tex}
% ... etc.

\end{document}
```

#### Step 2: Label Synchronization

After assembling the document, **synchronize all `\ref{}` references** with the actual `\label{}` in the table/figure .tex files:

1. **Scan all table/figure files** in the results directory to extract every `\label{}`.
2. **Build a mapping**: table/figure file → actual label.
3. **Replace all `\ref{}` in the main text** to match the actual labels from the files.
4. **Verify**: grep for any remaining orphan refs (e.g., `\ref{tab:` patterns that don't match any label).

This ensures all cross-references compile correctly without "??" in the PDF.

#### Step 3: Bibliography

1. **Compile the references**: Collect all `\cite{}` and `\citep{}` entries and list them in BibTeX format in `ref.bib`. Every key cited in the text must have a matching `ref.bib` entry, and every `ref.bib` entry should be cited at least once.
2. **Check the reference floors** (see the Reference Requirements rule). Count the entries and tally how many are published in 2023-2026 in top international journals:
   - If `ref.bib` has **fewer than 50** distinct entries, or **fewer than 15** in 2023-2026 from top journals, close the gap by adding genuinely relevant work to the citation-heavy sections (Introduction contributions, Literature Review, Hypothesis Development) and then re-extracting. Use `WebSearch` / `WebFetch` to source real recent top-journal papers — never invent entries to hit the numbers.
   - Confirm each 2023-2026 entry is real and correctly attributed (authors, title, journal, year, DOI). Verify the year and journal fields in `ref.bib` so the recency tally is accurate.
3. The bibliography uses `jfe.bst` style by default (can be changed to match target journal).

#### Step 4: Summary

Present final summary to user:
```
论文组装完成。输出文件：
- main.tex (X words, Y sections)
- ref.bib (Z entries, 其中 W 篇为 2023-2026 顶刊近期文献)
- results/ (N tables + M figures)

文档结构：
  Title Page → Abstract → Body → References → Figures → Tables → Appendix
```

## Important Notes

- If the user provides a target journal name, adapt the writing style and citation conventions accordingly.
- If a section has multiple tables (e.g., Robustness with Tables 4-6), read ALL relevant tables before writing.
- The user may ask to revise a section — re-read the table and rewrite with adjusted word count.
- Word counts are approximate targets, not strict limits. Stay within +/- 10%.
- When the user says a number (e.g., "650"), treat it as the word count for the current section.
- The main output file is always named `main.tex`.
- Table/figure files are kept in a `results/` subdirectory and included via `\input{}`.
- The `\ref{}` labels in the main text must always match the actual `\label{}` in the table/figure source files. Always scan and synchronize labels during assembly.
