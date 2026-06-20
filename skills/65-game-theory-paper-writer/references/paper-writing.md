# Paper Writing

Use this file when drafting a new game theory paper or rewriting major sections.

## Standard Paper Structure

1. Title
2. Abstract
3. Introduction
4. Literature review
5. Model setup
6. Equilibrium analysis/results
7. Numerical simulation and/or real-world case mapping
8. Extensions/robustness
9. Conclusion
10. References
11. Appendix/proofs

## Title

Use a high-information title:

- `Core mechanism: application scene`
- `Strategic [decision] under [condition]: a game-theoretic analysis of [scene]`
- Avoid vague titles such as "Some thoughts on platform competition."

## Abstract Formula

Write 4 compact elements:

1. Problem: what question is studied?
2. Method: what game/model is built?
3. Result: what equilibrium or comparative static is found?
4. Implication: what does the result mean for theory, policy, or management?

No citations, long formulas, limitations, or literature review in the abstract.

## Introduction: Four Paragraphs

1. **Establish territory**: explain the important real-world or theoretical background and the core tension.
2. **Establish niche**: summarize 3-5 closest literature streams and name the exact gap.
3. **Occupy niche**: state "This paper constructs..." and preview the model's distinctive assumptions and main results.
4. **Mechanism and roadmap**: explain the intuition behind the result and outline the paper.

Contribution sentence template:

`This paper contributes to [literature] by endogenizing/formalizing/relaxing [mechanism/assumption] in a [model family], showing that [main result], which implies [theory/policy meaning].`

## Literature Review: Three Layers

1. **Macro theoretical background**: place the paper in a broad tradition, such as industrial organization, information economics, contract theory, platform competition, environmental governance, or behavioral game theory.
2. **Core dialogue**: organize literature by mechanism or method, not by "A studied X, B studied Y." Use groups such as product differentiation, capacity constraints, repeated interaction, information asymmetry, or regulation.
3. **Precise gap**: state exactly which assumption, mechanism, player, timing, or information condition remains underexplored, then connect to the paper.

Never fabricate citations. If the skill lacks verified sources, mark citation slots clearly.

## Model Setup: Three-Step Description

For each model component:

1. **Intuition first**: explain the real mechanism without symbols.
2. **Formalization**: present equations, timing, strategy space, and payoffs.
3. **Definition and justification**: define every symbol, parameter domain, and why the function form is appropriate.

Model setup must include:

- Players.
- Strategies/actions.
- Timing.
- Information structure.
- Payoffs/objectives.
- Assumptions and parameter restrictions.
- Equilibrium concept.

Do not discuss results before the model is fully specified.

## Equilibrium Analysis: Proposition-Proof-Intuition

For each core result:

1. **Proposition**: numbered, titled, and conditional. State the result precisely.
2. **Proof**: give the key mathematical steps; move routine or long algebra to appendix.
3. **Intuition**: explain the mechanism without repeating algebra.

Good intuition paragraphs answer:

- Why is the equilibrium stable?
- Which strategic effect drives the result?
- What trade-off changes when a parameter changes?
- How does this differ from the benchmark or anchor model?

## Reverse Writing For Results

Before writing the results section, build a results inventory:

- Equilibrium solutions.
- Lemmas/propositions/theorems.
- Comparative statics signs.
- Threshold conditions.
- Welfare/profit/utility comparisons.
- Simulation targets and figure/table candidates.

Then write around figures and tables:

1. Introduce figure/table.
2. Describe what it shows.
3. Explain why it happens.
4. State implication.
5. Transition to the next result.

## Numerical Simulation

Use simulation when formulas are too complex, when there are multiple regimes, or when the paper needs visual intuition.

Simulation section structure:

1. Motivation: why simulation is needed.
2. Parameterization: baseline values and their basis.
3. Visualization: clear axes, legends, captions, and notes.
4. Interpretation: describe pattern, explain mechanism, connect to proposition.
5. Sensitivity: vary key parameters, not arbitrary values.

Parameter values should be based on literature, public data, reasonable normalization, or transparent illustrative assumptions.

## Real-World Case Mapping

Use cases to illustrate theory, not as a substitute for proof.

1. Introduce case briefly.
2. Map model elements to real actors, strategies, and conditions.
3. Use equilibrium results to explain observed behavior.
4. Offer a new prediction or managerial/policy implication.

Keep details tied to the model's mechanism.

## Extensions And Robustness

Good extensions:

- Relax one assumption.
- Compare benchmark and extended models.
- Test whether the main mechanism survives.
- Provide conditions under which the result changes.

Avoid adding a full unrelated model.

## Conclusion: Three Parts

1. **Retrospective summary**: restate question, model, and core finding.
2. **Positioning and implication**: clarify theoretical contribution and practical/policy implication.
3. **Limitations and future research**: turn simplifications into concrete next steps.

Future research templates:

- Assumption upgrade: static to repeated/dynamic, complete to incomplete information, homogeneous to heterogeneous players.
- Role expansion: add regulator, auditor, consumer association, platform, or intermediary.
- Method fusion: add behavioral preferences, empirical estimation, network structure, or learning dynamics.

## Style Rules

- Prefer precise claims over grand claims.
- Use "shows", "demonstrates", "suggests", and "implies" according to strength of support.
- Define notation before using it.
- Keep symbols consistent across sections.
- Do not overstate policy implications without welfare analysis.
- In Chinese drafts, keep academic tone clear and direct; avoid slogan-like phrasing.
- In English drafts, prefer concise active sentences and standard economics phrasing.
