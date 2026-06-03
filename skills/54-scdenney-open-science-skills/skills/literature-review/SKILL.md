---
name: literature-review
description: Build or audit a literature review: evidence map, gaps, synthesis plan.
argument-hint: "[topic, draft literature review, paper list, Zotero export, or claimed contribution]"
---

# Literature Review Evidence Mapper

## Heritage and scope

This is an original Open Science Skills workflow for experimental and computational social science. It remixes high-level ideas from Cheng-I Wu's *Academic Research Skills for Claude Code* (CC BY-NC 4.0), especially evidence mapping, source verification, and mode separation between narrative literature review and formal systematic review. It is not a full ARS pipeline and should not copy ARS prose.

## Instructions

### 1. Classify the review task

Decide what the user needs:

- **Narrative/theory review:** organize concepts, mechanisms, and debates for an introduction.
- **Design precedent review:** identify prior treatments, measures, samples, estimands, or analysis strategies.
- **Contribution audit:** test whether the claimed gap survives contact with the closest prior work.
- **Evidence map:** summarize what each study establishes, where it applies, and what remains unresolved.
- **Systematic-review escalation:** when the user needs exhaustive search, screening, risk-of-bias, and PRISMA reporting.

Default to a narrative/evidence-map review unless the user explicitly asks for a systematic review, meta-analysis, or PRISMA-compliant output.

### 2. Define the question and boundaries

Before summarizing papers, specify:

- Research question or review question.
- Population, setting, outcome, treatment/exposure, and mechanism scope.
- Disciplines and literatures that must be included.
- Time window and language restrictions, if any.
- Inclusion/exclusion logic for sources.
- What counts as "closest prior work."

If the user only gives a broad topic, first produce a short scoping memo with 2-4 possible review boundaries rather than writing a generic review.

### 3. Build the source base

Use the user's supplied sources first. Then identify obvious missing source classes:

- Seminal theoretical anchors.
- Most recent directly related empirical work.
- Meta-analyses, registered reports, study registries, or working-paper series.
- Methods papers that justify the research design.
- Null findings, failed replications, or unpublished registered studies when visible.
- Adjacent literatures that use different vocabulary for the same construct.

Run `citation-check` when the source list is large, messy, DOI-heavy, or likely to contain stale working papers.

### 4. Extract evidence, not summaries

For each important source, record:

- **Claim actually supported:** one sentence, no inflation.
- **Design and identification:** sample, setting, treatment/exposure, comparison, outcome, estimand, and key limitations.
- **Observable implication:** what the source lets a reader expect in the user's setting.
- **Boundary condition:** where the finding may fail.
- **Use in the user's paper:** background, theory, design precedent, measurement precedent, competing explanation, or gap support.

Do not produce chronological "Author A says X, Author B says Y" prose unless chronology is theoretically important.

### 5. Cluster the literature

Organize sources into 3-6 clusters. Prefer conceptual or mechanism clusters over method-only clusters:

- Mechanism families.
- Competing theories.
- Measurement traditions.
- Empirical settings or populations.
- Identification strategies.
- Evidence-quality tiers.

For each cluster, state what is settled, what is contested, and what would change the interpretation.

### 6. Test the claimed gap

Write a gap verdict:

- **Holds:** no close prior work answers the same question with the same population/mechanism/design.
- **Partly holds:** prior work answers part of it; the contribution must be narrowed.
- **Does not hold:** the claimed contribution is already established; reframe as replication, extension, boundary test, or synthesis.
- **Cannot assess:** missing sources or inaccessible source text prevent judgment.

When the gap is weak, propose a better contribution frame rather than only criticizing it.

### 7. Compose with sibling skills

- Use `narrative-building` after the evidence map exists to turn the review into the "Why-to-If-Then" funnel.
- Use `hypothesis-building` when the review implies falsifiable expectations and estimands.
- Use `pre-registration-writing` when the review supports confirmatory hypotheses.
- Use `methods-reporting` when reviewing how prior studies report designs, sample flow, and transparency.
- Use `journal-review` when auditing someone else's manuscript for novelty and placement.

## Output

Produce a `Literature Review Evidence Map`:

```
# Literature Review Evidence Map

Review question:
Scope and exclusions:
Search/source base:
Gap verdict: Holds / Partly holds / Does not hold / Cannot assess

## Closest Prior Work
| Source | What it actually establishes | Boundary | Relation to user's claim |

## Evidence Clusters
### Cluster 1: <name>
Settled:
Contested:
Missing:
Key sources:

## Contribution Diagnosis
Claimed gap:
Verdict:
Better contribution frame:

## Literature Review Architecture
1. <section purpose>
2. <section purpose>
3. <section purpose>

## Sentences the Review Must Earn
- <sentence-level claim that needs source support>

## Sources Needing Verification
| Source | Why |
```

## Quality checks

- [ ] The review question and scope are explicit.
- [ ] Closest prior work is identified before novelty is judged.
- [ ] Each key source is tied to an observable implication or boundary condition.
- [ ] The output distinguishes settled evidence from contested evidence.
- [ ] The gap verdict is calibrated, not inflated.
- [ ] Publication bias, registered studies, and null findings were considered when relevant.
- [ ] `citation-check` was invoked or recommended when source integrity was uncertain.
- [ ] The synthesis plan can feed directly into `narrative-building`.
