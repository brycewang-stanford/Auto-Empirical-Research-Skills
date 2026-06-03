# <Project Name>

## Research Context

- **Field:** <e.g., applied economics, political science, epidemiology>
- **Research question:** <falsifiable statement of the question>
- **Type:** <exploratory | confirmatory>
- **Identification strategy:** <DiD | RD | IV | SC | time-series | descriptive>
- **Paper language:** <en | pt-BR | es | fr | ...>  <!-- default: en -->
- **Code language:** <R | Python | both | other>
- **Significance convention:** <econ (0.10/0.05/0.01) | psi-med (0.05/0.01/0.001)>

## Target Outlets

- **Primary target journal:** <name>
- **Backup journals:** <name1, name2>
- **Tier strategy:** <ambitious | realistic | safety>

## Instructions for Claude Code

- Use the `superpapers` plugin skills for all research tasks in this project.
- Invoke `academic-baseline` first in every research session and keep it active as the standing policy layer.
- Enforce `replication-driven-research` as a guardrail for every analysis step.
- When executing a plan, treat each task's `Skills involved` field as mandatory routing, not a suggestion.
- For any journal-facing work (target outlet, author instructions, template adaptation, formatting, blinding, checklist, cover letter, submission portal), invoke `journal-guidelines` in the current session.
- Respect the paper language setting above for all user-facing paper content (sections, tables notes, figure captions).
- Use the code language preference above for all new scripts; when multiple languages are allowed, prefer the one already used in the project.
- Plugin internals, scripts, and code comments remain in English regardless of paper language.
- Never fabricate citations — verify every reference via web.

## Skill Routing by Phase

Before executing any plan task, consult this table and invoke every listed skill for the task's phase. This table supplements the plan's `Skills involved` field — use the union of both. `academic-baseline` and `replication-driven-research` are mandatory on every task in every phase and are not repeated below.

| Phase | Mandatory skills to invoke |
|---|---|
| Literature | `literature-search`, `citation-management` |
| Collection | `data-collection` |
| Preparation | `replication-driven-research` |
| Exploratory Analysis | `statistical-modeling`, `tables-and-figures` |
| Main Analysis | `statistical-modeling`, `tables-and-figures` |
| Robustness | `robustness-checks`, `tables-and-figures` |
| Writing | `paper-writing` (main session only, never subagent), `compile-latex` |
| Review | `paper-review` (pre-submission holistic audit; produces `docs/superpapers/review/audit-*.md`) |
| Submission | `journal-selection` (if outlet not fixed), then `journal-guidelines`, `compile-latex` |
- When looking up literature for any purpose (gap verification, citation, literature review), bias toward the user's target journals and closely related outlets in the same field tier.
- Prioritize recent publications (last 3-5 years) from target journals.
- Never hardcode results in `paper/paper.tex` — always use `\input{}` from `output/`.
