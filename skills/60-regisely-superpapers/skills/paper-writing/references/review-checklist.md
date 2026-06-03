# Paper Review Checklist

## 1. Quick Review Mode (5-Minute Scan)

For a fast read on whether a draft is in shape.

### Title (score each 1–10)

- Clarity: Can a non-specialist understand the topic?
- Length: Under 12 words? (shorter sticks)
- Treatment + outcome named explicitly?
- Memorability: Would you remember it at a conference?

### Abstract

- States a concrete finding with a magnitude? (not "we find effects")
- Under 150 words? (under 100 if a finance journal or JEL-style review)
- Follows the 4-part formula: motivation, method, result, implication?
- Opens with a fact or puzzle, not "This paper…"?

### Introduction

- Main result stated within the first 3 paragraphs?
- Literature woven into the argument (not a laundry list)?
- Length between 3 and 5 pages?
- Ends with a roadmap paragraph customized to the paper?

### Conclusion

- Under 1 page?
- Follows the 3-part formula: restate finding, implications, future directions?
- No new results or arguments introduced?
- No separate "limitations" subsection (limitations belong in the body)?

---

## 2. Deep Review Mode (Simulated Reviewers)

Three perspectives. Score independently. Combine at the end.

### Reviewer 1: The Methodologist

- [ ] Identification strategy explained in plain language before equations.
- [ ] Key identifying assumption stated and defended on substantive grounds (not just statistical).
- [ ] Threats to validity listed and addressed (selection, omitted variables, reverse causality, measurement error).
- [ ] Standard errors account for clustering, heteroskedasticity, or serial correlation as needed.
- [ ] Robustness checks cover alternative specifications, samples, and definitions — but only the canonical set for the design (no kitchen-sink robustness).
- [ ] Design-specific diagnostics present:
  - IV: first-stage F-statistic; weak-IV inference if needed
  - DiD: parallel trends shown; staggered-DiD diagnostics if applicable
  - RDD: bandwidth sensitivity; manipulation test
  - RCT: balance table; CONSORT-style attrition reporting
  - Synthetic control: pre-treatment fit; placebo / permutation inference
- [ ] Pre-registration status disclosed, or justified why not.
- [ ] Sample size adequate for the claimed precision.

### Reviewer 2: The Field Expert

- [ ] Contribution clearly positioned relative to 3–5 closest papers in the same area.
- [ ] Literature review is fair — cites disagreeing work, not just supporting papers.
- [ ] Results are substantively significant, not just statistically significant. Effect sizes are translated into meaningful units (currency, percentage points, standard deviations of the outcome, lives saved, vote share, etc.).
- [ ] Institutional / contextual details accurate and sufficient for replication.
- [ ] Policy or clinical implications warranted by the evidence — no overclaiming.
- [ ] External validity discussed honestly.
- [ ] Data sources described with enough detail to assess quality.

### Reviewer 3: The Writing Critic

- [ ] Active voice used throughout (check for "it was found", "is shown", "was conducted").
- [ ] Concrete language with magnitudes ("a 10% increase" not "a substantial effect").
- [ ] No throat-clearing in paragraph openings ("It is important to note that…").
- [ ] Tables are self-contained: title, notes, and units make them readable alone.
- [ ] Figures have informative titles and axis labels.
- [ ] Every word earns its place — no padding or repetition across sections.
- [ ] Paragraphs open with a claim, not a citation.
- [ ] Transitions between sections feel motivated, not mechanical.
- [ ] No excessive subsections fragmenting flowing prose (academic-baseline principle 9).
- [ ] Parentheses and em-dashes used naturally, not as a crutch.

---

## 3. Anti-AI Detection Checklist

Signs that the writing sounds AI-generated. Flag any that apply, then rewrite.

### Word-choice red flags

Overuse of: "delve", "crucial", "landscape", "multifaceted", "notably", "furthermore", "comprehensive", "robust" (outside its statistical meaning), "utilize" (instead of "use"), "leverage" (as a verb meaning "use"), "pivotal", "groundbreaking", "shed light on", "pave the way", "tapestry", "intricate", "underscore".

### Sentence-level tells

- Every sentence roughly the same length (vary between 8 and 25 words).
- Perfect parallel structure in every list (real authors are messier).
- No qualifying hedges (real researchers write "This likely reflects…" or "One interpretation is…").
- No field-specific jargon used naturally — generic phrasing across the whole paper.
- No parenthetical asides or em-dashes used naturally — or, conversely, them used as a crutch in every sentence.
- Transitions that are too smooth; real papers have some roughness between sections.

### Structural tells

- Generic placeholder phrases instead of specific institutional details.
- Numbered lists where flowing prose would be more natural (especially in body sections like Introduction or Discussion).
- Every paragraph exactly the same length.
- Conclusions that read like an executive summary rather than a reflection.

### Fix

Read two paragraphs of a strong published paper in the same field. Match that rhythm, not a chatbot's.

---

## 4. Pre-Submission Scoring (100-Point Rubric)

| Component | Points | Score |
|---|---|---|
| Title | /10 | ___ |
| Abstract | /10 | ___ |
| Introduction | /20 | ___ |
| Methodology / Identification | /15 | ___ |
| Results presentation | /15 | ___ |
| Writing quality | /15 | ___ |
| Tables and figures | /10 | ___ |
| Conclusion | /5 | ___ |
| **Total** | **/100** | ___ |

### Grade brackets

- 90–100: Ready for top-tier submission in the field.
- 80–89: Strong draft, minor revisions needed.
- 70–79: Solid working paper, needs another round.
- 60–69: Major structural or methodological gaps.
- Below 60: Rethink framing or identification before rewriting.

These brackets are calibrated for top-tier journals in any field (top-5 in economics; *Lancet* / *NEJM* / *JAMA* in medicine; *APSR* / *AJPS* in political science; field-leading journals in public health and sociology). For field journals, 70–80 is generally publishable with revisions.

---

## 5. Journal Fit Assessment

The journal-selection skill is the canonical place for full journal selection logic. The questions below are a quick fit check during review.

### Targeting questions

1. Is the question of broad disciplinary interest, or primarily relevant to a subfield?
2. Does the paper make a methodological contribution, or is it an application of known methods?
3. Is the setting specific to one country / population / setting, or does it speak to a universal mechanism?
4. How large is the likely audience? Would seminar attendees outside your subfield engage?

### Field-journal vs top-journal decision rule

If the paper's main appeal is "interesting result in domain X" rather than "new insight about how the world works", target the top field journal. There is no shame in this — a well-cited field journal paper beats a desk-rejected top-tier submission.

For details on specific journals and their requirements, defer to the `journal-selection` and `journal-guidelines` skills.

---

## 6. Reporting the Review

When delivering the review to the user:

1. Provide all three perspectives (Methodologist, Field Expert, Writing Critic).
2. Score the paper on each rubric component out of 100.
3. Flag any AI-generated writing patterns explicitly (so the author can rewrite).
4. Prioritize feedback: list the 3 most impactful changes first, then minor issues.
5. For each issue, state what is wrong, why it matters, and how to fix it with a concrete example from the paper.
6. End with the bracketed grade and one sentence on what would move the paper into the next bracket.
