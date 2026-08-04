# Installation and Usage Guide

Use AERS in one of four modes: browse, import the repo router, copy a single skill,
or vendor a workflow into a project.

## 1. Browse First

Start here:

- [`docs/SKILL_CATALOG.md`](SKILL_CATALOG.md) for a GitHub-readable table.
- [`docs/search.html`](search.html) for local or GitHub Pages search.
- [`docs/GOLDEN_WORKFLOWS.md`](GOLDEN_WORKFLOWS.md) for copy-paste empirical research prompts.
- [`catalog/skills.json`](../catalog/skills.json) for machine-readable skill metadata.
- [`catalog/provenance.json`](../catalog/provenance.json) for source and license metadata.

## 2. Import the Whole Repo as One Router Skill

Codex, CodeBuddy, and similar IDEs often validate the selected folder as a single
skill by looking for a top-level `SKILL.md`. The AERS repository root has one:
[`../SKILL.md`](../SKILL.md). Importing the root registers **one catalog router**
named `auto-empirical-research-skills`; it does not recursively register every
vendored child skill as a separate IDE skill.

> **Note:** `skills/69-Paper-WorkFlow/` is a git submodule. Clone with
> `git clone --recurse-submodules` (or run `git submodule update --init`)
> before copying, or the orchestrator folder will be empty.

For a local Codex-style install:

```bash
# Run from the repository root.
mkdir -p ~/.codex/skills/auto-empirical-research-skills
rsync -a --exclude .git --exclude .pytest_cache --exclude __pycache__ --exclude '*.pyc' \
  ./ ~/.codex/skills/auto-empirical-research-skills/
```

If an IDE asks for a GitHub path, use the repository root (`.`) and the skill
name `auto-empirical-research-skills`.

## 3. Copy One Skill

Most agent runtimes expect a folder that contains `SKILL.md`.

```bash
# Example: install AER workflow locally for Codex-style skill discovery
mkdir -p ~/.codex/skills
cp -R skills/50-brycewang-aer-skills/skills/aer-workflow ~/.codex/skills/aer-workflow
```

For Claude Code-style local installs:

```bash
mkdir -p ~/.claude/skills
cp -R skills/50-brycewang-aer-skills/skills/aer-workflow ~/.claude/skills/aer-workflow
```

For Codex-style local installs:

```bash
mkdir -p ~/.codex/skills
cp -R skills/50-brycewang-aer-skills/skills/aer-workflow ~/.codex/skills/aer-workflow
```

For a project-local install:

```bash
mkdir -p ./.claude/skills
cp -R skills/50-brycewang-aer-skills/skills/aer-workflow ./.claude/skills/aer-workflow
```

## 4. Use AERS Without Installing

You can point an agent at a local skill file directly:

```text
Use the workflow in skills/50-brycewang-aer-skills/skills/aer-identification/SKILL.md to audit this DID design.
```

This is the safest first trial because it does not modify any runtime configuration.

## 5. Recommended Starting Set

| Need | Start with |
|---|---|
| End-to-end automated empirical analysis | [`StatsPAI_skill`](../skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md) |
| Explicit line-by-line Python econometrics | [`Full-empirical-analysis-skill`](../skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md) |
| Referee-grade Stata replication | [`Full-empirical-analysis-skill-Stata`](../skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md) |
| R + Quarto replication report | [`Full-empirical-analysis-skill-R`](../skills/00.3-Full-empirical-analysis-skill_R/SKILL.md) |
| AER / AEJ manuscript pipeline | [`aer-workflow`](../skills/50-brycewang-aer-skills/skills/aer-workflow/SKILL.md) |
| Academic de-AIGC pass (EN + 中文) | [`de-aigc-skills`](../skills/48-de-AIGC-skills/SKILL.md) |

## 6. License Check

Before using a vendored skill in a public, commercial, or redistributed project, check:

- [`docs/LICENSE_AUDIT.md`](LICENSE_AUDIT.md)
- The local upstream `LICENSE` file, when present.
- The upstream repository if the license bucket is `UNKNOWN - check upstream`.

`MIT Non-Commercial` entries are not suitable for paid products, paid APIs, SaaS, or commercial client work without separate permission.
