---
name: brainstorm
description: Use when starting a new research project, exploring a research idea, deciding whether a question is viable, or before touching code or data for a new paper. Runs a research-focused brainstorm that clarifies research question, identification strategy, data feasibility, and contribution before any implementation.
---

# Brainstorm

## Overview

This is the first step in the superpapers pipeline for any new research project. It starts by invoking `academic-baseline` as the standing policy layer for the session, then mirrors the Superpowers brainstorming philosophy — Socratic questions, proposed approaches, incremental design approval — but asks research-specific questions. The terminal state is invoking `write-plan`. No implementation, data collection, or literature review beyond gap-verification happens until the design spec is written and approved by the user.

## When to Use

- "I have an idea for a paper"
- "I want to study X"
- "Can you help me think through this research question?"
- Start of any new empirical research project
- Before any data collection or analysis begins
- Revisiting a stalled project with a new angle

## When NOT to Use

- Mid-project troubleshooting — use `statistical-modeling` or the relevant domain skill
- The research question and design are already clear and stable
- Formatting, writing, or submission tasks — use `journal-guidelines` or other late-stage skills

## Hard Gate

Do NOT invoke `write-plan`, `execute-plan`, data collection, analysis, or any literature search beyond gap-verification until the design spec is written and the user has explicitly approved it. This applies to every project regardless of apparent simplicity.

## Mandatory Steps

1. **Invoke `academic-baseline` and `replication-driven-research` first.** `academic-baseline` resolves `CLAUDE.superpapers.md` via the walk-up Read (current working directory, then parent directories) and carries its settings into the session; its nine principles apply from the first question onward. `replication-driven-research` anchors the design as end-to-end reproducible — data to scripts to outputs to paper, with fixed seeds. Both skills stay active for the entire brainstorm.

2. **Explore project context.** Inspect existing `data/`, `paper/`, `.bib` files, and git history. Settings from `CLAUDE.superpapers.md` are already loaded via step 1. Learn what already exists before asking questions.

3. **Detect research field and paper language.** From project context when possible; otherwise ask the user. The field shapes which databases, methods, and journals will be relevant. The paper language determines later user-facing output.

4. **Ask Socratic questions one at a time.** Do not batch. Use multiple choice where possible. Cover these topics in roughly this order:
   - **Research question:** What is the question? Can it be rejected by data?
   - **Exploratory vs confirmatory:** This shapes every downstream decision — specification rigidity, multiple testing corrections, framing.
   - **Causal vs descriptive:** What would a causal answer require — and is that answerable with the available data?
   - **Identification strategy:** Candidate — DiD, RD, IV, SC, time-series, none (descriptive)? Invoke `statistical-modeling` to apply its guidance on specification, assumptions, and diagnostics for the chosen strategy.
   - **Data:** What would you need? Does it exist? Is it accessible? At what cost? Invoke `data-collection` for source-discovery guidance only; the hard gate above still blocks actual collection.
   - **Contribution:** What's the contribution over existing literature? Invoke `literature-search` in **gap-check mode**: one or two targeted queries, 5-8 results maximum, no bibliography output. This is NOT the full literature review. The full review runs in the plan's Literature phase, where `literature-search` is invoked in **full mode** with all its Mandatory Steps. Do not conflate the two invocations.
   - **Statistical power:** Order-of-magnitude check — is the sample large enough to detect plausible effect sizes? Invoke `statistical-modeling` for its power-calculation and effect-size guidance.
   - **Publication tier:** Target journal tier — and is the design consistent with that tier's expectations? Invoke `journal-selection` to match the paper to candidate outlets given field, method, and contribution.

5. **Propose 2-3 empirical approaches with trade-offs.** Always recommend one and explain why. Present options conversationally, not as a menu.

6. **Present the research design section by section, getting approval after each section.** Sections: research question, data strategy, identification strategy, estimation plan, expected outputs (tables/figures), robustness plan, submission target. When presenting the submission target section, `journal-selection` must already have been invoked in Step 4 — use its recommendation as the basis for this section.

7. **Scale each section to its complexity.** A simple descriptive study may need one paragraph per section. A novel identification strategy may need several.

8. **Write the spec** to `docs/superpapers/specs/YYYY-MM-DD-<topic>-design.md` in English. The spec is a plugin artifact, not paper content — English keeps it consistent across projects.

9. **Self-review the spec** for placeholders, internal contradictions, scope problems, and ambiguous requirements. Fix inline.

10. **Ask the user to review the written spec.** Wait for explicit approval before proceeding.

11. **Transition to `write-plan`.** This is the only terminal state. Do not invoke `execute-plan` or any implementation skill directly.

## Guardrails

- Invoke `academic-baseline` principles throughout — especially the causal-versus-correlational distinction.
- Never commit to a result framing in advance. The brainstorm ends with a design, not with conclusions.
- Questions asked in the user's conversation language. Spec documents written in English (plugin artifact). User paper content respects the paper language later.

## Anti-Patterns

- Batching multiple questions in one message
- Jumping to implementation before a design is approved
- Skipping the exploratory-versus-confirmatory distinction
- Proposing only one approach instead of 2-3
- Writing the spec without user approval
- Letting the user drift into "it's too simple to need a design" — every project gets a design, even if short
- Assuming a causal answer is feasible without asking about identification
- Starting literature search, data collection, or analysis during the brainstorm itself (beyond minimal gap verification)
- Discussing target journal tier without invoking `journal-selection`
- Discussing identification strategy or statistical power without invoking `statistical-modeling`

## Verification Before Completion

- [ ] Research field detected and confirmed
- [ ] Paper language established (even if default English)
- [ ] `academic-baseline` and `replication-driven-research` invoked first and applied throughout the brainstorm
- [ ] Research question is falsifiable and explicit
- [ ] Exploratory-versus-confirmatory distinction made
- [ ] Identification strategy identified (or "none, this is descriptive" made explicit)
- [ ] `statistical-modeling` invoked for the identification-strategy and statistical-power questions
- [ ] Data feasibility confirmed
- [ ] Contribution over literature established
- [ ] 2-3 approaches presented with a recommendation
- [ ] `journal-selection` invoked for the Publication tier question and its recommendation used in the submission-target section
- [ ] Design presented section by section with approval
- [ ] Spec written to `docs/superpapers/specs/` in English
- [ ] User approved the spec
- [ ] Next step (`write-plan`) announced, not executed
