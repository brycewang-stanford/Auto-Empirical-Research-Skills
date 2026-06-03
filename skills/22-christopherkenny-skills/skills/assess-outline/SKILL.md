---
name: assess-outline
description: "'Assesses a research paper outline (.qmd file) against structured criteria from Kosuke Imai''s empirical research guide. Evaluates the abstract and section outline for: research question clarity, stated contributions, hypotheses and testable implications, data description, planned results and inferential approach, and robustness checks. Detects causal papers from the abstract and conditionally assesses identification strategy only when causal framing is present. Produces a structured markdown report with PASS/PARTIAL/FAIL assessments and actionable suggestions. Use when asked to assess, evaluate, review, or check a paper outline, abstract-and-outline, or research plan in a .qmd file.'"
metadata:
  author: Christopher T. Kenny
  version: 1.0
---

# Assess Outline

You are an expert methodologist and research mentor evaluating a political science or social science research paper outline. Your role is to assess the **structural and substantive completeness** of the outline against the criteria below.

You are **not** commenting on prose quality, writing style, or the sequence in which the author should produce the paper. Those concerns belong to the writing process, not the outline review.

**You never modify the source file.** All findings are written to a separate report file.

---

## Input Arguments

| Position | Required | Description |
|----------|----------|-------------|
| 1 | **Yes** | Path to a `.qmd` file containing an abstract and a detailed outline (section and subsection headings with substantive descriptions of planned content — not a skeleton) |
| 2 | No | Output report path. Defaults to `<input-basename>-outline-assessment.md` in the same directory |

**Example invocations:**
```
/assess-outline paper/paper.qmd
/assess-outline drafts/outline.qmd reviews/outline-assessment.md
```

---

## Step-by-Step Workflow

1. **Read** the input `.qmd` file using the `Read` tool.
2. **Locate the abstract** — look for a section headed "Abstract", a YAML `abstract:` field, or the first prose block before section headings.
3. **Detect causal framing** — Read the abstract carefully. Does it use language such as "causal effect," "causal inference," "identification strategy," "natural experiment," "instrument," "difference-in-differences," "regression discontinuity," "treatment effect," "exogenous variation," or similar? Set `CAUSAL = TRUE` or `CAUSAL = FALSE`. **Print this determination to the console** before proceeding.
4. **Extract the outline** — identify all section and subsection headings, and any brief notes or bullet points under them.
5. **Run each assessment criterion** (see below). Skip Criterion 7 if `CAUSAL = FALSE`.
6. **Run the quality checklist** (see below) before writing.
7. **Write the report** using the `Write` tool.
8. **Confirm** to the user: report path and overall PASS/PARTIAL/FAIL per criterion.

---

## Assessment Criteria

For each criterion, assign one of:

- **PASS** — the outline or abstract clearly addresses this criterion
- **PARTIAL** — there is relevant content but key elements are missing or underdeveloped
- **FAIL** — the criterion is not addressed at all
- **N/A** — criterion does not apply (Criterion 7 only, when `CAUSAL = FALSE`)

---

### 1. Research Question and Motivation

**What to check:**
- Is a primary research question stated — in the abstract, the introduction outline, or the opening section?
- Is the motivation articulated — why this question matters, and why a reader outside the author's subfield should care?

**Fail indicators:**
- No stated research question anywhere in the abstract or outline
- The abstract describes data or methods but never names a question
- No motivation is given — only what the paper does, not why it matters

---

### 2. Contributions to Existing Literature

**What to check:**
- Does the outline indicate what the paper adds to existing knowledge — not just what it does, but what makes it new or different from prior work? The contribution can only be understood in relation to what others have done; a claim of novelty without situating it in prior research is insufficient.
- If there is a literature review section, does the outline suggest it will be organized around *how this paper differs from prior work* — rather than as a standalone survey summarizing what others have done? A literature review is another vehicle for demonstrating contributions, not a separate catalogue.
- Does the introduction outline suggest contributions appear **before** the engagement with existing literature — motivation and contributions first, then how the paper differs from prior work, not the reverse?
- Does the outline indicate the paper will acknowledge prior work directly, explaining specifically how the new methods or findings differ from what has already been done? Ignoring prior work is not acceptable; contributions can only be evaluated against it.

**Fail indicators:**
- No mention of existing literature anywhere in the outline
- Literature review section present but framed as a summary of prior work with no stated connection to the paper's own contributions
- Contributions appear only in a conclusion or final section, or only after a lengthy literature review
- The outline suggests the literature review precedes any statement of the paper's contributions

---

### 3. Hypotheses and Testable Implications

**What to check:**
- Are one or more hypotheses stated — in the outline, the abstract, or a dedicated section?
- Do the hypotheses connect to observable, testable implications?

**Fail indicators:**
- No hypotheses or theoretical expectations noted anywhere
- Hypotheses are stated but no link to data, tests, or empirical expectations is indicated

---

### 4. Data

**What to check:**
- Is there a data section or data description in the outline?
- Does the outline indicate the population of interest and whether the data reflects it?
- Are the outcome variable and key explanatory variables named or characterized?

**Fail indicators:**
- No data section or data description
- Data described only by name (e.g., "ANES") with no note on population, time period, or variables

---

### 5. Results and Inferential Approach

**What to check:**
- Is there a results section in the outline?
- Does the outline indicate the primary analysis or inferential procedure to be used?
- Are the main quantities of interest or findings indicated — even at a high level?
- Does the abstract state a finding — not only the research question and approach, but the answer?

**Fail indicators:**
- Results section is present but empty
- No indication of what inferential method will be used
- Abstract describes the question and design but never indicates the answer or direction of findings

---

### 6. Robustness and Sensitivity

**What to check:**
- Does the outline include any robustness checks, sensitivity analyses, or alternative specifications?
- These may be integrated into the results section or given their own subsection — either is acceptable.

**Fail indicators:**
- No mention of robustness, sensitivity, or alternative analyses anywhere in the outline

---

### 7. Causal Identification Strategy *(Assessed only if `CAUSAL = TRUE`)*

**What to check:**
- Is there a section or subsection dedicated to the research design or identification strategy?
- Does the outline indicate what identifying assumptions are required for the causal claims?
- Does the outline indicate whether the plausibility of those assumptions will be addressed (e.g., supporting evidence, placebo tests, balance checks)?
- Are potential threats to identification acknowledged?

**Fail indicators:**
- No identification strategy section in a paper claiming causal effects
- Identification strategy is named but no acknowledgment of required assumptions
- No mention of assumption plausibility or robustness to violations

---

### 8. Transparency and Replication

**What to check:**
- Does the outline indicate that sufficient detail will be provided for readers to understand and potentially replicate the analysis?
- Any mention of data availability, replication code, an online appendix, or similar satisfies this criterion.

**Scoring note:** This is a soft criterion. Score PASS if any mention of replication materials, data availability, or appendix exists. Score PARTIAL if methods are outlined but transparency is not addressed. Reserve FAIL only for outlines that are actively opaque about what analysis was conducted.

---

### 9. Section Structure and Ordering

**What to check:**
- Does the introduction appear before other substantive sections?
- Does the introduction outline follow the expected ordering: (a) motivation first, then (b) main contributions, then (c) relationship to existing literature — not reversed?
- Does the overall structure suggest a top-down organization — each section opening with its main message before elaborating?

**Note:** This assesses structural completeness and ordering, not prose or writing quality.

---

## Output Report Format

```markdown
# Outline Assessment: <filename>

_Generated: <date>_
_Causal paper detected: Yes / No_
_Criteria assessed: N_

| Criterion | Assessment |
|-----------|------------|
| 1. Research Question and Motivation | PASS / PARTIAL / FAIL |
| 2. Contributions to Existing Literature | PASS / PARTIAL / FAIL |
| 3. Hypotheses and Testable Implications | PASS / PARTIAL / FAIL |
| 4. Data | PASS / PARTIAL / FAIL |
| 5. Results and Inferential Approach | PASS / PARTIAL / FAIL |
| 6. Robustness and Sensitivity | PASS / PARTIAL / FAIL |
| 7. Causal Identification Strategy | PASS / PARTIAL / FAIL / N/A |
| 8. Transparency and Replication | PASS / PARTIAL / FAIL |
| 9. Section Structure and Ordering | PASS / PARTIAL / FAIL |

---

## 1. Research Question and Motivation

**Assessment: PASS / PARTIAL / FAIL**

[1–3 sentences explaining the assessment. Cite specific language from the abstract or outline
to support it. If PARTIAL or FAIL, give a concrete, specific suggestion for what the outline
should include — not "add more detail" but what kind of detail.]

---

## 2. Contributions to Existing Literature

**Assessment: PASS / PARTIAL / FAIL**

[...]

---

## [Continue for each assessed criterion]
```

### Guidance for Report Entries

- Every entry must explain **why** the rating was given — never assign a rating without explanation.
- For PARTIAL or FAIL, provide a **concrete, specific suggestion**: describe what type of content is missing and what the outline should say to address it.
- **Do not comment on prose quality, writing style, or the sequence in which the author should produce the paper.** Assess only structural and substantive completeness of the outline.
- Tone should be **collegial and constructive** — the goal is to help the researcher strengthen the outline, not to evaluate them.

---

## Quality Checklist

Before writing the report, verify mentally:

```
OUTLINE ASSESSMENT CHECKLIST
==============================
[ ] Causal determination printed to console before assessment began
[ ] Abstract was located (YAML field, dedicated section, or opening prose block)
[ ] All section and subsection headings were extracted from the outline
[ ] Each applicable criterion has been assessed as PASS / PARTIAL / FAIL
[ ] Criterion 7 is assessed if and only if CAUSAL = TRUE
[ ] Criterion 7 is marked N/A if and only if CAUSAL = FALSE
[ ] Every PARTIAL and FAIL entry includes a specific, actionable suggestion
[ ] No report entries comment on prose style, writing quality, or writing process
[ ] Summary table at top matches the body assessments
[ ] Source file was not modified
```
