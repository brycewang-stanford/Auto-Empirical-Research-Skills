---
name: game-theory-paper-writer
description: Generate, continue, revise, polish, and stress-test game theory research papers. Use when the user provides a game theory topic, phenomenon, draft, outline, model idea, literature anchor, reviewer comments, or asks for 博弈论论文生成, 选题建模, 文献迁移, 模型修正, 均衡分析, 数值模拟, 论文润色, 改稿打磨, or R&R response work.
---

# Game Theory Paper Writer

## Core Rule

Support legitimate research writing only. Do not help copy, disguise, evade plagiarism detection, fabricate references, fabricate data, or present another paper's model/text as original work. When reusing ideas from a source paper, require clear citation, explicit comparison, independent derivation, and a concrete marginal contribution.

When citations are needed but sources are not provided and no literature search tool is available, use citation placeholders and clearly mark them as `TODO: verify source`. Never invent author names, years, journal titles, DOIs, or empirical facts.

## Workflow Selector

Use the path that matches the user's input:

- **Topic only**: read `references/topic-and-modeling.md`, then `references/model-toolkit.md`, then draft with `references/paper-writing.md`.
- **Reality phenomenon or industry case**: use the reality-to-model workflow in `references/topic-and-modeling.md`; choose the smallest viable model before writing.
- **One or more anchor papers/literature notes**: use the literature-grounded workflows in `references/topic-and-modeling.md`; cite and compare with the anchors.
- **Existing draft/outline**: read `references/revision-and-review.md`; diagnose structure, contribution, model, proofs, writing, and references before editing.
- **Reviewer comments/R&R**: read `references/revision-and-review.md`; build a comment-response matrix before rewriting.
- **Mathematical model already specified**: read `references/model-toolkit.md`; verify assumptions, equilibrium concept, solvability, comparative statics, and robustness before drafting prose.

## Topic-To-Paper Procedure

1. Clarify the minimum necessary scope: language, target output, length, target journal/course level, required citation style, and whether real literature search is available. If missing, proceed with reasonable defaults and state assumptions.
2. Formulate the research core: research question, core strategic tension, players, decision variables, information structure, timing, payoff logic, and expected contribution.
3. Generate 2-3 candidate model routes, score them by tractability, economic intuition, literature continuity, and publishable contribution. Select the strongest route unless the user has specified one.
4. Build the model identity report: cooperative/non-cooperative, static/dynamic, complete/incomplete information, perfect/imperfect information, discrete/continuous strategies, two-player/N-player/large-population, and matching equilibrium concept.
5. Write the model setup in three layers: intuition first, formalization second, definitions and assumption justification third.
6. Solve or outline the equilibrium analysis: assumptions, first-order conditions or equilibrium conditions, second-order/concavity checks when relevant, propositions, proofs or proof sketches, intuition, comparative statics, and parameter restrictions.
7. Add numerical simulation or case mapping when the model would otherwise feel too abstract, the formulas are too complex, or a policy/managerial implication needs visualization.
8. Draft the paper in standard order: title, abstract, introduction, literature review, model, equilibrium analysis, numerical/case section, extensions/robustness, conclusion, references, appendix.
9. Run the self-review checklist in `references/revision-and-review.md` and revise before delivering.

## Draft-To-Revision Procedure

1. Build a revision map: current thesis, claimed contribution, model structure, main results, missing proofs, weak sections, and citation gaps.
2. Run three passes in order: logic and contribution, model/proof rigor, language and formatting.
3. For every substantive edit, preserve the author's intended claim unless it is unsupported; when unsupported, either add the needed support or weaken the claim.
4. Output a polished version plus a short revision memo listing: major changes, remaining risks, citation TODOs, mathematical TODOs, and optional next-step upgrades.

## Expected Outputs

For a full generation task, deliver:

- A research design brief.
- A complete paper outline.
- A draft paper or the requested section.
- A model/proof appendix when mathematical steps are substantial.
- A revision checklist and unresolved verification items.

For a polishing task, deliver:

- A revised manuscript or section.
- A change memo organized by contribution, model, results, prose, and formatting.
- A list of claims, citations, or derivations that still require verification.

## Reference Files

- `references/topic-and-modeling.md`: research question generation, literature-grounded adaptation, multi-paper synthesis, and reality-to-model translation.
- `references/model-toolkit.md`: model classification, model family selection, function choice, equilibrium concepts, and solvability checks.
- `references/paper-writing.md`: paper structure, abstract, introduction, literature review, model setup, equilibrium analysis, simulation/case writing, and conclusion templates.
- `references/revision-and-review.md`: draft diagnosis, self-review, simulated reviewer critique, solving intractable models, polishing passes, and R&R response workflow.
