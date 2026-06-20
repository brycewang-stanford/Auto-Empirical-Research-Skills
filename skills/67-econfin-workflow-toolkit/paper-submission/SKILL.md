---
name: paper-submission
description: Evaluate a paper's contribution novelty, identify best-fit SSCI journal fields and ABS star rating, and recommend 20 target journals. Trigger when user says "paper submission" / "paper-submission" / "投稿评估" / "期刊推荐" / "target journal" / "选刊".
allowed-tools: Read, Bash, Edit, Write, Glob, Grep, AskUserQuestion, WebSearch, WebFetch, Agent
argument-hint: [path-to-paper-pdf-or-project-folder]
---

# Paper Submission Evaluator

## Overview

This skill evaluates an academic paper and produces a comprehensive submission target report. It performs four assessments:

1. **Contribution Novelty Score** (0-100): How much the paper advances existing literature, assessed via web search for related work.
2. **Best-Fit SSCI Journal Fields**: Which ABS field categories best match the paper.
3. **Appropriate ABS Star Rating**: What star level (1, 2, 3, 4, 4*) the paper's quality warrants.
4. **Top 20 Journal Recommendations**: From the 2 best-fitting fields, at the recommended ABS star level, list 20 SSCI-indexed journals with rationale.

The ABS journal list is read from `C:\Users\Admin\.claude\skills\paper-submission\asset\Business School Journal List 2023.pdf` (referred to as AJG2025). This file is bundled with the skill in the `asset/` folder, so it is always available regardless of changes to the user's desktop.

The final report is saved as `target.pdf` in the paper's directory.

## Workflow

### Phase 1: Initialization

1. **Receive paper path** from user (via `$ARGUMENTS` or ask). Accept either:
   - A PDF file containing the full paper
   - A project folder containing LaTeX files (main.tex, tables, etc.)
2. **Read the paper thoroughly**:
   - For PDF: Read all pages using the Read tool with page ranges.
   - For LaTeX project: Read main.tex and key result files.
3. **Extract key information** and record internally:
   - Research question / hypothesis
   - Methodology (empirical strategy, identification, data)
   - Data source and sample (country, market, time period)
   - Key findings (baseline results, mechanisms, heterogeneity)
   - Stated or implied contributions
   - Keywords and JEL codes (if present)
4. **Summarize the paper** in ~200 words for use in subsequent phases. Present this summary to the user for confirmation:
   ```
   我已阅读论文，以下是摘要：

   研究问题：[...]
   方法：[...]
   数据：[...]
   主要发现：[...]
   贡献方向：[...]

   请确认以上理解是否正确，或进行调整。
   ```
5. **Wait for user confirmation** before proceeding.

---

### Phase 2: Literature Novelty Assessment (Web Search Required)

This phase evaluates how novel the paper's contribution is relative to existing literature. **Web search is mandatory**.

#### Step 2a: Identify Search Dimensions

Based on the paper summary, identify 3-5 search dimensions that capture the paper's core novelty claims. Each dimension represents a facet of the paper's contribution. Examples:
- Topic novelty: "Has [X effect on Y] been studied before?"
- Methodological novelty: "Has [identification strategy Z] been applied to [this question]?"
- Data novelty: "Has [this data source / market / country] been used for [this question]?"
- Mechanism novelty: "Have [these channels] been documented?"
- Setting novelty: "Has [this policy / institutional context] been exploited?"

#### Step 2b: Conduct Web Searches

For each dimension, conduct **at least 2 targeted web searches** using WebSearch. Search queries should be in English and target academic literature. Example queries:
- `"[dependent variable]" AND "[independent variable]" site:ssrn.com OR site:nber.org`
- `"[key mechanism]" AND "[research context]" journal article`
- `[topic keywords] survey OR review OR meta-analysis`

For each search:
1. Execute the WebSearch query.
2. Read the top results using WebFetch to check abstracts and findings.
3. Record: (a) how many closely related papers exist, (b) how the current paper differs from them, (c) whether the core finding has been documented before.

#### Step 2c: Score the Contribution

Assign a novelty score out of 100 based on these criteria:

| Score Range | Meaning | Criteria |
|-------------|---------|----------|
| 85-100 | Highly novel | No prior paper addresses this exact question with this approach. Opens a new research direction. |
| 70-84 | Substantially novel | Few prior papers on a similar topic, but this paper offers a clearly distinct angle (new data, new mechanism, new identification). |
| 55-69 | Moderately novel | Topic has been studied, but this paper contributes incremental insights (new setting, additional robustness, extension of known results). |
| 40-54 | Limited novelty | Multiple papers have addressed similar questions with similar methods. Contribution is primarily confirmatory or extends to a new sample. |
| 0-39 | Low novelty | The main findings have been well-documented. Contribution is marginal. |

For each dimension, assign a sub-score and weight. The final score is the weighted average.

**Present the assessment to the user**:
```
文献创新性评估结果：

维度1: [dimension name] — 子分 [X]/100
  已有文献：[list 2-3 most relevant prior papers with year]
  本文区别：[how this paper differs]

维度2: [dimension name] — 子分 [X]/100
  ...

综合创新性得分：[SCORE]/100
评级：[Highly novel / Substantially novel / Moderately novel / Limited novelty / Low novelty]

主要创新点：
1. [innovation point 1]
2. [innovation point 2]
3. [innovation point 3]

潜在风险：
- [e.g., "Reviewer may argue that [X] has been shown by [Author, Year]"]
```

---

### Phase 3: Field Matching and ABS Star Rating

#### Step 3a: Identify Best-Fit Fields

The ABS journal list uses these field categories (22 fields total):
- ACCOUNT (Accounting)
- FINANCE (Finance)
- ECON (Economics)
- STRAT (Strategy)
- MKT (Marketing)
- OPS&TECH (Operations and Technology)
- OR&MANSCI (Operations Research and Management Science)
- ORG STUD (Organization Studies)
- HRM&EMP (Human Resource Management and Employment)
- IB&AREA (International Business and Area Studies)
- INNOV (Innovation)
- PUB SEC (Public Sector Management)
- SOC SCI (Social Sciences)
- SECTOR (Sector Studies)
- BUS & ECON HIST (Business and Economic History)
- MDEV&EDU (Management Development and Education)
- REGIONAL (Regional Studies)
- ENT-SBM (Entrepreneurship and Small Business Management)
- ETHICS-CSR-MAN (Ethics, CSR and Management)
- INFO MAN (Information Management)
- PSYCH (GENERAL) (Psychology - General)
- PSYCH (WOP-OB) (Psychology - Work and Organizational)

Based on the paper's topic, methodology, and data, identify the **2 most suitable fields**. Consider:
- What is the paper's primary disciplinary home? (e.g., corporate finance paper → FINANCE)
- What is a strong secondary field? (e.g., uses accounting data → ACCOUNT; studies innovation → INNOV)
- Where would the paper's contribution resonate most?

#### Step 3b: Determine Appropriate ABS Star Rating

Assess the paper's quality level to determine the appropriate ABS star tier for targeting:

| Star Level | Criteria |
|------------|----------|
| 4* | World-leading journals. Paper must have: exceptional novelty (score 85+), rigorous identification, clean causal story, broad implications, polished writing. Very selective — only recommend if the paper is truly outstanding. |
| 4 | Top field journals. Paper should have: high novelty (score 70+), solid identification strategy, clear contribution, well-executed empirics. |
| 3 | Highly regarded journals. Paper should have: moderate-to-high novelty (score 55+), reasonable identification, clear results, good execution. |
| 2 | Well-recognized journals. Paper with: some novelty (score 40+), standard methodology, sound results. |
| 1 | Recognized journals. Paper with: limited novelty, basic methodology, narrow contribution. |

**Decision rules**:
- Novelty score alone does not determine the star level — also consider methodology rigor, data quality, writing quality, and scope of implications.
- If the paper uses a novel identification strategy (natural experiment, RDD, etc.), upgrade by 0.5 star.
- If the paper uses Chinese data targeting international journals, be realistic: Chinese-market papers rarely appear in 4* journals unless the finding has universal implications.
- Be honest and calibrated. Over-optimistic recommendations waste the author's time.

**Present the assessment**:
```
领域匹配与星级评估：

最佳匹配领域：
  1. [Field 1] — [rationale]
  2. [Field 2] — [rationale]

建议投稿星级：ABS [N] 星
理由：
- 创新性：[novelty score] 分，[assessment]
- 方法论：[methodology assessment]
- 数据质量：[data assessment]
- 贡献范围：[scope assessment]

是否同意以上评估？如需调整星级，请告知。
```

**Wait for user confirmation** before proceeding.

---

### Phase 4: Journal Recommendations

#### Step 4a: Extract Journal Data from ABS PDF

Read the ABS journal list PDF (`C:\Users\Admin\.claude\skills\paper-submission\asset\Business School Journal List 2023.pdf`) using a Python script to extract all journals matching:
- Field = one of the 2 identified fields
- ABS star rating = the recommended level (also include one level above and one level below for reference)
- SSCI indexed = Yes (prioritize SSCI journals, but include non-SSCI journals as backup)

Use the following Python approach via Bash:
```python
import fitz
doc = fitz.open(r'C:\Users\Admin\.claude\skills\paper-submission\asset\Business School Journal List 2023.pdf')
# Parse the tabular data from each page
# Extract: ISSN, Field, Journal Title, ABS rating, ABDC rating, SSCI status, JCR quartile, JIF
```

#### Step 4b: Rank and Select 20 Journals

From the extracted journals, select the **top 20** recommendations across the 2 fields. Ranking criteria:
1. **Field relevance**: How well the journal's scope matches the paper's topic
2. **Star level match**: Journals at the recommended star level ranked first
3. **SSCI status**: SSCI-indexed journals preferred
4. **JIF**: Higher impact factor preferred (as tiebreaker)
5. **Publication precedent**: Journals that have published similar topics (based on your knowledge)

Organize the list as:
- **Field 1**: 10 journals (ranked by fit)
- **Field 2**: 10 journals (ranked by fit)

For each journal, provide:
- Journal name
- ABS star rating
- SSCI status and JCR quartile
- JIF (if available)
- 1-sentence rationale for why this journal fits the paper

---

### Phase 5: Report Generation

Generate the final report as `target.pdf` saved in the paper's directory (or user-specified location).

#### Report Structure

The report should contain:

```
═══════════════════════════════════════════
        论文投稿目标评估报告
        Paper Submission Target Report
═══════════════════════════════════════════

生成日期：[YYYY-MM-DD]
论文标题：[Paper title if available]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

一、论文概要
[200-word paper summary]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

二、文献创新性评估

综合得分：[SCORE]/100 — [Rating]

[For each dimension:]
维度 [N]: [Name] — [Sub-score]/100
  相关文献：[2-3 papers]
  本文创新：[How this paper differs]

主要创新点：
1. [...]
2. [...]
3. [...]

潜在审稿风险：
- [...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

三、目标领域与星级

最佳领域：[Field 1], [Field 2]
建议星级：ABS [N] 星

评估维度：
- 创新性：[...]
- 方法论：[...]
- 数据质量：[...]
- 贡献范围：[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

四、推荐期刊（共20本）

[Field 1 Name]（10本）:
┌────┬──────────────────────┬──────┬──────┬──────┬─────────────────────────┐
│ #  │ Journal              │ ABS  │ SSCI │ JIF  │ 推荐理由                │
├────┼──────────────────────┼──────┼──────┼──────┼─────────────────────────┤
│ 1  │ ...                  │ ...  │ ...  │ ...  │ ...                     │
│ ...│                      │      │      │      │                         │
└────┴──────────────────────┴──────┴──────┴──────┴─────────────────────────┘

[Field 2 Name]（10本）:
┌────┬──────────────────────┬──────┬──────┬──────┬─────────────────────────┐
│ #  │ Journal              │ ABS  │ SSCI │ JIF  │ 推荐理由                │
├────┼──────────────────────┼──────┼──────┼──────┼─────────────────────────┤
│ 1  │ ...                  │ ...  │ ...  │ ...  │ ...                     │
│ ...│                      │      │      │      │                         │
└────┴──────────────────────┴──────┴──────┴──────┴─────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

五、投稿建议

[2-3 paragraphs of strategic advice:]
- Which journal to try first and why
- Backup strategy if rejected
- Any adjustments to the paper that would improve chances at higher-tier journals
```

#### PDF Generation Method

Use the Python script `scripts/generate_report.py` to produce the PDF. The script uses `fpdf2` with Chinese font support (`SimSun` from `C:\Windows\Fonts\simsun.ttc`).

**Interaction pattern**:
```
报告已生成并保存至：[path]/target.pdf

报告包含：
- 创新性评估：[SCORE]/100
- 推荐领域：[Field 1], [Field 2]
- 推荐星级：ABS [N] 星
- 推荐期刊：20本（每个领域10本）
```

---

## Important Notes

- **Web search is mandatory** for Phase 2. Do not skip novelty assessment.
- **Be calibrated and honest** in scoring. An inflated score wastes the author's time on unrealistic targets.
- **ABS journal list PDF** is the authoritative source for journal data. Extract data programmatically from the PDF — do not rely on memory alone.
- **SSCI indexing** is strongly preferred but not strictly required. If fewer than 10 SSCI journals exist in a field at the target star level, supplement with non-SSCI journals and mark them clearly.
- **Star level flexibility**: The 20 journal recommendations should primarily be at the recommended star level. If fewer than 10 journals exist at that level in a field, include journals from one level above or below, clearly marked.
- The report language is **Chinese** for headings and explanations, **English** for journal names and academic content.
- If the user provides a specific target journal or field preference, adjust recommendations accordingly.
- The output file is always named `target.pdf` unless the user specifies otherwise.
