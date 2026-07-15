---
name: auto-empirical-research-skills
description: Route empirical-research requests through the Auto-Empirical Research Skills catalog when this whole repository is installed as one skill in Codex, CodeBuddy, Claude Code, or another IDE. Use to choose and load the right vendored AERS skill for causal inference, econometrics, replication, manuscript writing, citation checking, de-AIGC editing, or full empirical-paper workflows without reading the entire repository at once.
---

# Auto-Empirical Research Skills Router

Use this root skill when the full AERS repository has been installed as a single skill folder. Treat it as a router and catalog, not as a request to load every vendored `SKILL.md`.

The catalog holds **1,151 skills across 70 vendored collections**. Never read them all — route to one, then load only that skill's `SKILL.md`.

## Workflow

1. Classify the user's empirical-research task by **stage**, then load the single best-matching skill:
   - Full pipeline or orchestration: start with `skills/69-Paper-WorkFlow/` or the `skills/00.*` flagship analysis skills (StatsPAI / Python / Stata / R).
   - Causal inference and econometrics: pick by method from the table below, or search `catalog/skills.json` / `docs/TAXONOMY.md`.
   - AER or top economics journal work: start with `skills/50-brycewang-aer-skills/`.
   - Replication, citation, or peer review: use `docs/SKILL_CATALOG.md` and `docs/GOLDEN_WORKFLOWS.md` to choose a focused skill.
   - Chinese academic de-AIGC or academic rewriting: start with `skills/48-copaper-ai-chinese-de-aigc/` or nearby writing skills in the catalog.
2. Read only the selected child skill's `SKILL.md`, then follow its progressive-disclosure instructions for `references/`, `scripts/`, `assets/`, or templates.
3. If no child skill clearly matches, inspect `catalog/skills.json` first (has `path`, `name`, `description`, `line_count`), then `docs/SKILL_CATALOG.md`. Avoid broad recursive reads of `skills/`.
4. For installation help, use `docs/INSTALL.md` for Codex-style copy installs and `INSTALL.md` for Claude Code marketplace/plugin installs.
5. If editing this repository, keep parent and nested repos separate. In particular, inspect `git status` inside `skills/69-Paper-WorkFlow/` (a git submodule) before touching it.

## Method → where to start

Match the user's identification strategy or task to a starting collection, then confirm against `catalog/skills.json`:

| Task / method | Start here |
|---|---|
| DiD / staggered DiD / event study | `skills/50-brycewang-aer-skills/`, `skills/10-Jill0099-causal-inference-mixtape/`, `skills/13-scunning1975-MixtapeTools/` |
| Instrumental variables (IV) | `skills/50-brycewang-aer-skills/`, `skills/40-py-econometrics-pyfixest/` |
| Regression discontinuity (RDD) | `skills/50-brycewang-aer-skills/`, `skills/10-Jill0099-causal-inference-mixtape/` |
| Synthetic control (SCM) | `skills/50-brycewang-aer-skills/`, `skills/13-scunning1975-MixtapeTools/` |
| Panel fixed effects | `skills/40-py-econometrics-pyfixest/`, `skills/39-vincentarelbundock-marginaleffects/` |
| DML / CATE / causal forests | `skills/00.1-Full-empirical-analysis-skill_Python/`, `skills/63-tondevrel-scientific-agent-skills/` |
| Bayesian modeling | `skills/23-Learning-Bayesian-Statistics-baygent-skills/`, `skills/51-pymc-labs-CausalPy/` |
| Stata analysis | `skills/00.2-Full-empirical-analysis-skill_Stata/`, `skills/32-dylantmoore-stata-skill/`, `skills/64-tmonk-mcp-stata/` |
| R analysis | `skills/00.3-Full-empirical-analysis-skill_R/`, `skills/55-ab604-claude-code-r-skills/` |
| Literature review | `skills/36-taoyunudt-literature-review-skill/`, `skills/52-keemanxp-slr-prisma/`, `skills/59-shiquda-openalex-skill/` |
| Citation checking | `skills/62-PHY041-claude-skill-citation-checker/` |
| Manuscript writing / proofreading | `skills/04-K-Dense-AI-claude-scientific-writer/`, `skills/38-peternka-academic-proofreader/` |
| De-AIGC / humanize | `skills/48-copaper-ai-chinese-de-aigc/`, `skills/45-stephenturner-skill-deslop/`, `skills/47-conorbronsdon-avoid-ai-writing/` |
| Replication | `skills/28-maxwell2732-paper-replicate-agent-demo/`, `skills/29-quarcs-lab-project20XXy/` |

## Install Notes

- Whole-repo imports are supported by this root `SKILL.md` as a lightweight compatibility entry point.
- Individual skill installs are still preferred when a runtime expects one folder per skill. Copy the folder that directly contains the target `SKILL.md`.
- Do not copy the repository root into a runtime and expect every child skill to become individually registered unless that runtime explicitly supports recursive skill discovery.
- **Name collisions:** the catalog contains 92 bare `name`s shared across collections (e.g. `data-analysis`, `lit-review`, `proofread`). When a runtime registers skills by flat name, install one collection at a time, or disambiguate with the globally-unique `qualified_name` field in `catalog/skills.json` (`<collection>::<name>`, e.g. `12-pedrohcgs-claude-code-my-workflow::data-analysis`), or the full `skills/<collection>/.../SKILL.md` path.

## Key Files

- `catalog/skills.json`: machine-readable list of vendored skills.
- `docs/SKILL_CATALOG.md`: human-readable skill index.
- `docs/TAXONOMY.md`: task and method taxonomy.
- `docs/GOLDEN_WORKFLOWS.md`: ready-to-use empirical-research prompts.
- `docs/INSTALL.md`: runtime installation guidance for single-skill and whole-repo use.
