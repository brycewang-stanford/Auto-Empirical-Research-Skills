---
name: review-paper
description: >-
  Comprehensive manuscript review covering argument structure, econometric specification, citation completeness, and potential referee objections. Make sure to use this skill whenever the user wants substantive academic feedback on a paper — not just surface edits. Triggers include: "review my paper", "give me feedback on this draft", "what would a referee say", "anticipate referee objections", "act as a referee", "check my identification strategy", "is my argument convincing", "review this manuscript", "critique my paper", "will this pass review", or any request for deep critique of academic writing beyond typos and grammar.
argument-hint: "[paper filename in manuscripts/ or path to .tex/.pdf]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Manuscript Review

Produce a thorough, constructive review of an academic manuscript — the kind of report a top-journal referee would write.

**Input:** `$ARGUMENTS` — path to a paper (.tex, .pdf, or .qmd), or a filename in `manuscripts/` or `references/papers/`.

---

## Steps

1. **Locate and read the manuscript.** Check:
   - Direct path from `$ARGUMENTS`
   - `manuscripts/$ARGUMENTS`
   - `references/papers/$ARGUMENTS`
   - Glob for partial matches in `manuscripts/` and `references/papers/`

2. **Read the full paper** end-to-end. For long PDFs, read in chunks (5 pages at a time).

3. **Dispatch `domain-reviewer` agent** via Task for deep substance review (see below).

4. **Evaluate writing quality and presentation** (dimensions 5-6) — the skill handles these directly since the agent explicitly does not cover presentation.

5. **After the agent completes**, merge its findings with your writing/presentation evaluation. Generate 3-5 "referee objections" synthesized from both.

6. **Produce the unified review report.**

7. **Save to** `quality_reports/paper_review_[sanitized_name].md`

---

## Step 3: Dispatch Domain-Reviewer Agent

Dispatch the `domain-reviewer` agent via Task for the deep substance check. The agent applies 5 lenses that go deeper than broad dimensional evaluation — actual equation verification, derivation step checking, code-theory alignment, and backward logic tracing.

```
Task prompt: "You are the domain-reviewer agent. Review the manuscript at [path].
Research question: [from spec if available].

Apply all 5 review lenses:
1. Assumption stress test
2. Derivation verification
3. Citation fidelity
4. Code-theory alignment
5. Backward logic check

Also check cross-document consistency.
Follow the domain-reviewer agent instructions and return your full substance review report."
```

After the agent completes, collect its findings. These feed into the "Major Concerns" and "Referee Objections" sections of the final report.

---

## Steps 4-5: Skill Evaluates Writing & Presentation, Then Merges

The skill evaluates dimensions 5-6 directly (the agent does not cover these), then merges everything into the unified report format below.

---

## Review Dimensions

### 1. Argument Structure
- Is the research question clearly stated?
- Does the introduction motivate the question effectively?
- Is the logical flow sound (question → method → results → conclusion)?
- Are the conclusions supported by the evidence?
- Are limitations acknowledged?

### 2. Identification Strategy
- Is the causal claim credible?
- What are the key identifying assumptions? Are they stated explicitly?
- Are there threats to identification (omitted variables, reverse causality, measurement error)?
- Are robustness checks adequate?
- Is the estimator appropriate for the research design?

### 3. Econometric Specification
- Correct standard errors (clustered? robust? bootstrap?)?
- Appropriate functional form?
- Sample selection issues?
- Multiple testing concerns?
- Are point estimates economically meaningful (not just statistically significant)?

### 4. Literature Positioning
- Are the key papers cited?
- Is prior work characterized accurately?
- Is the contribution clearly differentiated from existing work?
- Any missing citations that a referee would flag?

### 5. Writing Quality
- Clarity and concision
- Academic tone
- Consistent notation throughout
- Abstract effectively summarizes the paper
- Tables and figures are self-contained (clear labels, notes, sources)

### 6. Presentation
- Are tables and figures well-designed?
- Is notation consistent throughout?
- Are there any typos, grammatical errors, or formatting issues?
- Is the paper the right length for the contribution?

---

## Output Format

```markdown
# Manuscript Review: [Paper Title]

**Date:** [YYYY-MM-DD]
**Reviewer:** review-paper skill
**File:** [path to manuscript]

## Summary Assessment

**Overall recommendation:** [Strong Accept / Accept / Revise & Resubmit / Reject]

[2-3 paragraph summary: main contribution, strengths, and key concerns]

## Strengths

1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

## Major Concerns

### MC1: [Title]
- **Dimension:** [Identification / Econometrics / Argument / Literature / Writing / Presentation]
- **Issue:** [Specific description]
- **Suggestion:** [How to address it]
- **Location:** [Section/page/table if applicable]

[Repeat for each major concern]

## Minor Concerns

### mc1: [Title]
- **Issue:** [Description]
- **Suggestion:** [Fix]

[Repeat]

## Referee Objections

These are the tough questions a top referee would likely raise:

### RO1: [Question]
**Why it matters:** [Why this could be fatal]
**How to address it:** [Suggested response or additional analysis]

[Repeat for 3-5 objections]

## Specific Comments

[Line-by-line or section-by-section comments, if any]

## Summary Statistics

| Dimension | Rating (1-5) |
|-----------|-------------|
| Argument Structure | [N] |
| Identification | [N] |
| Econometrics | [N] |
| Literature | [N] |
| Writing | [N] |
| Presentation | [N] |
| **Overall** | **[N]** |
```

---

## Principles

- **Be constructive.** Every criticism should come with a suggestion.
- **Be specific.** Reference exact sections, equations, tables.
- **Think like a referee at a top-5 journal.** What would make them reject?
- **Distinguish fatal flaws from minor issues.** Not everything is equally important.
- **Acknowledge what's done well.** Good research deserves recognition.
- **Do NOT fabricate details.** If you can't read a section clearly, say so.
