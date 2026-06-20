---
name: new-project
description: >-
  Start a new research project by conducting a structured interview to formalize a research idea, then generates research questions with identification strategies and a project spec. Make sure to use this skill whenever the user wants to develop or document a new research idea — not to search for literature or data. Triggers include: "new project", "start research", "I have an idea", "help me develop this", "I want to study X", "help me formalize this idea", "what's my research question", "what identification strategy should I use", "write up my project idea", or when the user describes a topic they want to turn into a paper.
argument-hint: "[brief topic or 'start fresh']"
allowed-tools: ["Read", "Grep", "Glob", "Write"]
---

# New Research Project

Formalize a research idea into a concrete project specification with testable hypotheses and empirical strategies.

**Input:** `$ARGUMENTS` — a topic, phenomenon, dataset, or "start fresh" for open-ended exploration.

This skill runs in **three phases**. Phase 1 is conversational — ask one or two questions at a time and wait for responses. Phases 2 and 3 run automatically after the interview.

---

## Phase 1: Research Interview

**Goal:** Draw out the researcher's thinking and establish a clear research question.

Ask questions **one or two at a time**. Build on each answer before moving to the next phase. Do NOT use AskUserQuestion — ask directly in your response. A good interview runs 4–6 exchanges.

### Question Bank (select and adapt based on context)

**The Puzzle (start here):**
- "What phenomenon or puzzle are you trying to understand?"
- "What do you observe in the data / world that doesn't fit the standard explanation?"

**Why It Matters:**
- "Why does this matter? Who should care about the answer?"
- "Is there a policy lever here, or is this more about understanding a mechanism?"

**Theoretical Motivation:**
- "What's your intuition for why X happens — what's the mechanism?"
- "What would standard theory predict? Do you expect to find something different, and why?"

**Data and Setting:**
- "Do you have data in mind, or are you open on the data source?"
- "Is there a specific context, time period, country, or institutional setting you're focused on?"

**Identification:**
- "Is there a natural experiment, policy change, or discontinuity you could exploit?"
- "What's the biggest threat to a causal interpretation — what would a skeptic say?"

**Expected Results + Contribution:**
- "What would you expect to find? What would genuinely surprise you?"
- "What existing papers are closest to this? What gap does yours fill?"

### When to Stop Interviewing
Move to Phase 2 when you have:
- A clear research question (one sentence)
- At least one plausible identification strategy
- Some sense of what data exists or is needed
- The motivation / contribution

If after 3 exchanges the user keeps giving vague answers, move to Phase 2 anyway and flag the open questions.

---

## Phase 2: Research Ideation

**Goal:** Generate 3–5 structured research questions covering the full range from descriptive to causal.

Announce the transition: *"Great — I have enough to generate a structured set of research questions. Let me build that out now."*

Then generate **3–5 research questions** ordered by type:

| Type | What It Asks |
|------|-------------|
| **Descriptive** | What are the patterns? How has X evolved? |
| **Correlational** | What factors are associated with X, controlling for Z? |
| **Causal** | What is the causal effect of X on Y? |
| **Mechanism** | Through what channel does X affect Y? |
| **Policy** | Would intervention X improve outcome Y? |

**For each RQ, develop:**
- **Hypothesis** — testable prediction with expected direction/magnitude
- **Identification Strategy:**
  - Method (DiD, RDD, IV, synthetic control, etc.)
  - Treatment (what varies, when, where)
  - Control group (comparison units)
  - Key assumption (parallel trends, exclusion restriction, etc.)
  - Main robustness checks (pre-trends test, placebo, etc.)
- **Data requirements** — what variables, time period, geography, unit of observation
- **Key pitfalls** — 2 main threats to identification + mitigations
- **Related work** — 2-3 papers using similar approaches (name only, no fabrication)

**Rank the questions** by feasibility × contribution:

| RQ | Feasibility | Contribution | Priority |
|----|-------------|-------------|----------|
| 1  | High | High | ★★★ |
| 2  | High | Medium | ★★ |
| ... | ... | ... | ... |

---

## Phase 3: Save Project Spec

Produce the unified project spec document and save it.

**Save to:** `quality_reports/project_spec_[sanitized_topic].md`

```markdown
# Research Project: [Working Title]

**Date:** [YYYY-MM-DD]
**Researcher:** [from CLAUDE.md if available]

---

## Research Question

[Single clear sentence]

## Motivation

[2–3 paragraphs: why this matters, theoretical context, policy relevance, what the answer would change]

## Research Questions

### RQ1: [Question] — Priority: ★★★ (Feasibility: High / Contribution: High)

**Type:** Causal

**Hypothesis:** [Testable prediction with expected sign]

**Identification Strategy:**
- **Method:** [e.g., Staggered DiD with Sun–Abraham estimator]
- **Treatment:** [What varies and when]
- **Control group:** [Comparison units]
- **Key assumption:** [e.g., Parallel pre-trends conditional on controls]
- **Robustness:** [Pre-trends test, placebo outcomes, alternative control groups]

**Data Requirements:**
- [Dataset or data type needed]
- [Key variables: treatment proxy, outcome, controls]
- [Time period and geography]

**Key Pitfalls:**
1. [Threat + mitigation]
2. [Threat + mitigation]

**Related Work:** [Author (Year)], [Author (Year)]

---

[Repeat for RQ2–RQ5]

---

## Priority Empirical Strategy

[1 paragraph recommending the single highest-priority RQ and why, with the specific identification approach]

## Open Questions

[Issues raised in the interview that need further thought before committing to a strategy]

---

## Suggested Next Steps

1. **`/lit-review [topic]`** — Search the literature for related work and citation chains
2. **`/data-finder [topic]`** — Find and assess datasets for the priority RQ
3. Once data is secured: **`/data-analysis`** to begin analysis
```

---

## After Saving

Tell the user:
- The spec is saved to `quality_reports/project_spec_[topic].md`
- Recommended next step: `/lit-review [topic]` to build the literature foundation
- Then: `/data-finder [topic]` to identify and assess data sources
