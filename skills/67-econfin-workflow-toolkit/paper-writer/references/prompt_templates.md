# Prompt Templates for Empirical Sections

These templates define the writing instructions for each empirical section. The `{WORD_COUNT}` placeholder is replaced by the user's specified word count. The `{SECTION_NAME}` placeholder is replaced by the actual section/subsection title derived from the paper outline.

## Language Rule (applies to ALL prompts and ALL sections)

**Use American English throughout.** Spelling: "behavior", "analyze", "modeling", "labor", "organization", "center", "favor", "program". Vocabulary: "toward" (not "towards"), "while" (not "whilst"). This rule applies without exception to every section the skill produces, including Title, Abstract, Introduction, Literature Review, Hypothesis Development, Theoretical Model, Institutional Background, Data and Sample Construction, Variable Construction, Empirical Model, Descriptive Statistics, Empirical Results, Robustness, Heterogeneity, Mechanism, Alternative Explanation, Further Analysis, and Conclusion.

When sending a prompt to the model, append (or otherwise enforce) the instruction: "Write in American English (e.g., 'behavior', 'analyze', 'modeling')."

## Reference Requirements (apply across the whole paper)

The assembled paper must hold to two bibliography floors (see the Reference Requirements rule in `SKILL.md`):

- **At least 50 distinct references** in `ref.bib`, accumulated across the citation-heavy sections (Introduction motivation and contributions, Literature Review, Hypothesis Development, Variable Construction, Empirical Model).
- **At least 15 references published in 2023-2026 in top international journals** (JF, JFE, RFS, JFQA; AER, QJE, JPE, Econometrica, REStud, REStat, AEJ; JAE, JAR, TAR, RAST, CAR; Management Science, SMJ, Organization Science), weighted toward the target journal's field.

**Never fabricate a citation to reach these counts.** Use `WebSearch` / `WebFetch` to find real, verifiable recent papers (correct authors, title, journal, year, DOI). If you cannot reach 15 verifiable recent top-journal papers after genuine searching, report the shortfall to the user rather than inventing entries.

## Common Suffix (append to ALL section prompts except Conclusion)

```
Write in American English (spelling: behavior, analyze, modeling, organization, center, etc.). Cite relevant and important literature published from 2010-2026, ensuring recent top-journal work (2023-2026) is well represented; contribute toward the paper's floors of at least 50 total references and at least 15 from 2023-2026 in top international journals. All responses must be based on academic facts. Avoid generating fabricated literature / data / conclusions; if you need a recent citation, use a real, verifiable paper rather than inventing one. All viewpoints and content must be annotated with supporting evidence. List the reference with DOI link in APA format at the end.
```

## Title Template

### Paper Title

```
Please propose 10 titles for this manuscript following {TARGET_JOURNAL} style. The titles should be concise, academic, and capture the core contribution of the paper. Vary the structures: some as noun phrases, some as questions, some with subtitles. Prioritize clarity and impact.
```

## Abstract, JEL, and Keywords Templates

### Abstract

```
Suppose you are a well-known {FIELD} professor. Please think step by step and use {WORD_COUNT} English words to write the abstract for this manuscript. Summarize the research question, data and methodology, key findings, and contribution. Write as one concise paragraph. Do not use bullet points.
```

### JEL Codes

```
Give three JEL codes for this paper. Output format: G14, G30, O31
```

### Keywords

```
Give four keywords for this paper in one line separated by comma, do not use capital letter. Output format: keyword1, keyword2, keyword3, keyword4
```

## Introduction Templates

### Introduction - Motivation

```
Suppose you are a well-known {FIELD} professor. Please use {WORD_COUNT} English words to motivate this study. Cite relevant and important literature published from 2010-2026, anchoring the research question in recent top-journal work (2023-2026). All responses must be based on academic facts. Avoid generating fabricated literature / data / conclusions. All viewpoints and content must be annotated with supporting evidence. List the reference with DOI link in APA format at the end. Do not talk about empirical findings, contributions nor the unique research setting. We target this manuscript to {TARGET_JOURNAL}. Do not use bullet points.
```

### Introduction - Why This Setting

```
Use {WORD_COUNT} English words to write a paragraph showing that {SETTING} data is an ideal setting to do this study with the most important reasons. Do not use bullet points.
```

### Introduction - What We Do and What We Find

```
Summarize the empirical strategy used in this study. Summarize what is examined and what is found in the empirical results. Do not cite papers. Do not use bullet points. Use {WORD_COUNT} English words.
```

### Introduction - Contributions

```
Demonstrate three main strands of literature that this paper contributes to. For each contribution, state what the existing literature does, identify the gap, and explain how this paper fills it. Cite relevant and important literature published from 2010-2026, prioritizing publications in {TARGET_JOURNAL} and related top {FIELD} journals, and explicitly engage recent work (2023-2026) so each strand reflects the current frontier. All responses must be based on academic facts. Avoid generating fabricated literature / data / conclusions. All viewpoints and content must be annotated with supporting evidence. List the reference with DOI link in APA format at the end. We target this manuscript to {TARGET_JOURNAL}. Do not use bullet points. Use {WORD_COUNT} English words.
```

### Introduction - Roadmap

```
Use {WORD_COUNT} English words to write a roadmap paragraph for the paper. Begin with: "The remainder of the paper proceeds as follows." Then briefly describe each subsequent section.
```

## Institutional Background Template

### Institutional Background

```
Use {WORD_COUNT} English words to write for the section Institutional Background. Describe the institutional features of {SETTING} that are most relevant to this study's identification strategy and empirical interpretation. Focus on facts that the target journal's readers would not be familiar with. Do not cite literature. Do not use bullet points.
```

## Literature Review and Hypothesis Development Templates

### Literature Review

**Planning step**: Analyze the paper's empirical content (baseline topic, mechanisms, heterogeneity dimensions) and propose strand topics to the user. Example strands for a sentiment-innovation paper:
1. Market sentiment and corporate decision-making
2. Divergence of opinion / disagreement among investors
3. Determinants of corporate innovation

The user confirms or adjusts the strands, then provides a total word count. Allocate words proportionally across strands (e.g., 700 words / 3 strands ≈ 230 words each).

**Per strand template**:
```
Use {WORD_COUNT} American English words to review the related literature on {STRAND_TOPIC}, especially work published from 2010-2026, and be sure to cover recent top-journal contributions (2023-2026) so the strand reflects the current frontier. Clearly position this paper's contribution relative to the existing literature at the end of the subsection.

Citation balance for the Literature Review: use approximately a 50/50 mix of \cite{} (前引, author-as-subject) and \citep{} (后引, parenthetical). About half of the citations should appear as the grammatical subject of a sentence (e.g., "\cite{baker2003} document that..."), and about half should appear in parentheses providing supporting evidence (e.g., "...consistent with prior work \citep{diether2002}"). After drafting, check the strand and rebalance if one form dominates.

Write in American English (behavior, analyze, modeling, organization, center). Do not use bullet points.
```

### Hypothesis Development - Verbal (H1: Baseline)

```
Formulate the first hypothesis H1 for this study based on the baseline regression results. Use {WORD_COUNT} English words to provide reasonable argument for the hypothesis H1. The argument should incorporate the mechanisms documented in this study but should not mention the findings explicitly. First present the reasoning, then propose the hypothesis. After stating the argument, conclude with: "Based on the above discussion, we propose the first hypothesis:" followed by the formal hypothesis statement.
```

### Hypothesis Development - Verbal (H2+: Heterogeneity)

```
Formulate hypothesis H{N} for this study that captures the cross-sectional heterogeneity in {HETEROGENEITY_DIMENSION}. Use {WORD_COUNT} English words to provide reasonable arguments. You must act as if you do not know the empirical findings. First present the reasoning, then propose the hypothesis. Conclude with the formal hypothesis statement.
```

### Theoretical Model - Setup

```
Please describe in detail the setup of a theoretical model to support the empirical findings. Include the model's assumptions, variable definitions, and functional forms. The model should provide a unified explanatory framework for the empirical results. Use LaTeX format for mathematical formulas and provide detailed explanations in English. The model setup should be comprehensive and lay the groundwork for subsequent theorems and proofs. Do not use bullet points. Present the information in a flowing academic style. Use {WORD_COUNT} English words.
```

### Theoretical Model - Theorems

```
Based on the theoretical model setup, propose key theorems/propositions that articulate the main conclusions of the model. Theorem 1 should correspond to the baseline finding (discordance reduces innovation). Subsequent theorems should correspond to mechanism channels. State each theorem formally, then provide a brief economic intuition. Use LaTeX format for all mathematical content. Use {WORD_COUNT} English words.
```

### Theoretical Model - Discussion

```
Discuss the implications and limitations of the theoretical model. Explain how the model provides a theoretical foundation for the empirical findings, and suggest potential directions for model extensions. Use {WORD_COUNT} English words.
```

### Theoretical Model - Proofs (Appendix)

```
Provide detailed mathematical proofs for all theorems stated in the theoretical model. The proof process should be logically rigorous with clear steps. Use LaTeX \begin{proof}...\end{proof} environment. Use LaTeX format for all mathematical content. Provide necessary explanations in English throughout.
```

## Section Templates

### Descriptive Statistics

```
Use {WORD_COUNT} English words to write a paragraph for the descriptive statistics. Choose the most important variables rather than listing all variables. When you are describing the summary statistics, you need to report mean or other statistics when you see fit. Do not use bullet points.
```

If a correlation matrix is present, append:
```
Use 50 English words to describe the correlation matrix.
```

### Baseline Regression

```
Use {WORD_COUNT} English words to write for the section {SECTION_NAME}. Describe the regression specification, key independent and dependent variables, and the main findings. Report specific coefficients and significance levels from the table. Discuss economic significance. Do not use bullet points.
```

### Endogeneity

```
Use {WORD_COUNT} English words to write for the section {SECTION_NAME}. For each endogeneity test, explain the concern being addressed, the methodology used (e.g., IV/2SLS, PSM, DID, Heckman), why the instrument or method is valid, and what the results show. Do not use bullet points.
```

### Robustness Checks

```
Use {WORD_COUNT} English words to write for the section {SECTION_NAME}. Write ALL robustness tests together in a single, coherent section. For each test, briefly explain what is being tested and what the results confirm. Adjust the depth of discussion based on the number of robustness tests. Do not use bullet points.
```

### Cross-sectional Heterogeneity

**Word-count rule**: Default ~500 words **per heterogeneity dimension**. Set `{WORD_COUNT}` to `500 × number_of_dimensions`. If the tables make the number of dimensions ambiguous, ask the user before invoking this prompt.

```
Use {WORD_COUNT} English words to write for the section {SECTION_NAME} (approximately 500 words per heterogeneity dimension). For each subsample analysis, explain the economic intuition behind the sample split, describe the grouping method, and interpret the differential effects. Link findings to economic theory or institutional features where possible. Do not use bullet points.
```

### Mechanism Analysis

**Word-count rule**: Default ~600 words **per mechanism**. Set `{WORD_COUNT}` to `600 × number_of_mechanisms`. If the tables make the number of mechanisms ambiguous, ask the user before invoking this prompt.

```
Use {WORD_COUNT} English words to write for the section {SECTION_NAME} (approximately 600 words per mechanism). Describe each mechanism/channel being tested, the methodology used to identify it, and what the results reveal about the causal chain from the independent variable to the dependent variable. Do not use bullet points.
```

### Alternative Explanation

```
Use {WORD_COUNT} English words to write for the section {SECTION_NAME}. Address potential alternative explanations for the main findings. For each alternative, explain why it is a plausible concern, describe the test conducted, and interpret how the results help rule out (or support) the alternative. Do not use bullet points.
```

### Further Analysis

```
Use {WORD_COUNT} English words to write for the section {SECTION_NAME}. Describe additional analyses that extend or complement the main findings. Explain the motivation for each additional test and interpret the results. Do not use bullet points.
```

### Conclusion

```
Use {WORD_COUNT} English words to write for the section Conclusion. Summarize the main findings, discuss the contributions to the literature, suggest policy implications, and acknowledge limitations. Do NOT cite literature in the conclusion. Do not use bullet points.
```

## Research Design Section Templates

### Empirical Model

```
Use {WORD_COUNT} American English words to describe the empirical model. Produce the econometric model in LaTeX equation format using \begin{equation}...\end{equation}. Use $X$ to express the vector of all control variables, and use Greek letters for various fixed effects (e.g., $\mu_i$ for industry, $\delta_t$ for year). Define the dependent variable, core independent variable, and fixed effects.

CRITICAL: This subsection is also where the CONTROL VARIABLES are described (control variables do NOT belong to the Variable Construction section). After presenting the equation, devote a paragraph or two to the control variables: list each control included in $X$, briefly justify its inclusion, describe its measurement, and cite supporting prior literature where relevant. Reference the variable definition table for the precise definitions.

Explain the rationale for the model specification, including clustering of standard errors. Write in American English (behavior, analyze, modeling, organization). Do not use bullet points.
```

### Variable Construction

```
Use {WORD_COUNT} American English words to write for the section Variable Construction. Cover ONLY the dependent variable(s) and the core independent variable in this section. DO NOT describe control variables here — control variables belong to the Empirical Model subsection.

Structure the section with two `\subsection{}` blocks (or more, if there are multiple dependent variables or multiple independent variables).

CRITICAL: The subsection titles MUST reflect the actual indicator content drawn from the variable definition table in the PDF. DO NOT use generic titles like "Dependent Variable" or "Independent Variable". Instead use a content-specific phrase, e.g., `\subsection{Measuring Corporate Innovation}`, `\subsection{Investor Disagreement}`, `\subsection{ESG Disclosure Quality}`, `\subsection{Patent-Based Innovation Output}`. Read the variable definition table first, identify what each measure actually captures, and name the subsections accordingly.

For each variable, explain its economic meaning, describe how it is measured (formulas, data sources, transformations), and cite the original paper that proposed the measure. Reference the variable definition table in the PDF. Write in American English (behavior, analyze, modeling, organization). Do not use bullet points.
```

### Data Sources

```
Use {WORD_COUNT} English words to write a paragraph describing all relevant data sources in detail. Mention the name of each database (e.g., CSMAR, Wind, CNRDS), what data is obtained from each source, and the time coverage. Do not use bullet points.
```

### Sample Construction

```
Use {WORD_COUNT} English words to write a paragraph describing the sample construction procedure. Explain the initial sample, filtering criteria (e.g., excluding financial firms, ST firms, missing values), and the final sample size. Do not use bullet points.
```

## Writing Style Guide

### Reporting Regression Results

Mix t-statistics with verbal significance descriptions (50-60% verbal, 40-50% with t-stats). Examples:

**With t-statistic (40-50% of the time):**
> "The coefficient on [variable] is [value] ($t = [value]$), suggesting that [economic interpretation]."

**Verbal significance (50-60% of the time):**
> "The coefficient on [variable] is [value] and statistically significant at the 1\% level, suggesting that..."
> "The estimate is negative and highly significant, indicating that..."
> "The result is statistically indistinguishable from zero."
> "The coefficient is significant at conventional levels."

Vary these patterns throughout the paper to avoid repetitive phrasing.

### Citation Style

Mix `\cite{}` (前引, author-as-subject) and `\citep{}` (后引, parenthetical) at section-specific ratios:

| Section | `\cite{}` (前引) | `\citep{}` (后引) |
|---------|-----------------|-------------------|
| Literature Review | ~50% | ~50% |
| All other sections (Introduction, Hypothesis Development, Empirical Results, etc.) | ~30% | ~70% |

**\cite{} (author as grammatical subject)**
> "\cite{baker2003} demonstrate that equity-dependent firms adjust..."
> "As \cite{hall2012} argue, financing constraints are..."

**\citep{} (parenthetical support)**
> "...consistent with the overvaluation hypothesis \citep{diether2002}."
> "...a pattern documented in prior studies \citep{aghion2013,fang2014}."

After drafting Literature Review, count both forms across the section and rebalance toward 50/50. After drafting other sections, aim for ~30% `\cite{}` / ~70% `\citep{}`.

### Table/Figure Placement

For **main-body** tables/figures, at the end of each empirical subsection add a centered block with parentheses (NOT square brackets, NOT `\bigskip\noindent`):
```latex
\begin{center}
(Insert Table \ref{tab:X} about here)
\end{center}
```
For figures, use the same pattern with `Figure`:
```latex
\begin{center}
(Insert Figure \ref{fig:X} about here)
\end{center}
```

**Online Appendix tables/figures get NO "Insert ... about here" block.** Supplementary exhibits placed in the Online Appendix (variable definitions, robustness checks, other `S`-numbered tables/figures) are only mentioned and cross-referenced in prose, pointing the reader to the appendix, e.g., "see Table~\ref{tab:X} in the Online Appendix." Do not add a placement marker for them.

### Transition Between Subsections

Use natural academic transitions:
- "We next examine..."
- "To further investigate..."
- "Turning to the results in Table X..."
- "Column (1) of Table X presents..."
- "Consistent with our baseline findings..."

### Table Reference Pattern

- First mention: "Table~\ref{tab:X} reports the results of..."
- Subsequent: "As shown in Column (X) of Table~\ref{tab:X}..."
- Cross-reference: "Consistent with the findings in Table~\ref{tab:Y}..."
