---
name: research-init
description: >
  Scaffold a new research project with full reproducibility infrastructure in R and/or Python.
  Creates directory structure, pipeline stubs (targets/Snakemake), environment lockfiles (renv/uv),
  documentation templates (codebook, decision log, pre-registration, Cornell README), Quarto
  manuscript template, and proper .gitignore. Can wrap existing data in gold-standard structure.
  Use when the user says "new project," "scaffold," "start a study," "set up a project,"
  "I have data and need to organize it," or when /research-intake recommends scaffolding.
argument-hint: "<project name> [--lang r|python|both] [--existing-data <path>]"
---

# /research-init — Project Scaffolding

You create the structure that makes everything else possible. A well-scaffolded project is halfway to reproducibility before a single line of analysis is written.

## How to scaffold a project

### Step 1 — Gather requirements

Ask the researcher (or infer from context):

1. **Project name** — will become the directory name
2. **Language** — R, Python, or both? (Default: both)
3. **Existing data?** — If yes, where? What format? This changes the workflow.
4. **Research question** — one sentence, for the README and pre-registration skeleton
5. **Target journal** — if known, for formatting defaults

If the researcher provides a project name and says "scaffold it," don't over-ask. Use sensible defaults and get them started.

### Step 2 — Create directory structure

Create the full structure documented in [references/criteria.md](references/criteria.md). Use the templates in [references/templates/](references/templates/) for each file.

### Step 3 — Initialize environments

**For R:**
1. Create `_targets.R` from template
2. Initialize `renv` (if R is available on the system)
3. Create `R/00_setup.R` from template

**For Python:**
1. Create `Snakefile` from template
2. Create `pyproject.toml` with research stack dependencies
3. Create `python/00_setup.py` from template

### Step 4 — Handle existing data

If the researcher has existing data:
1. Copy (not move) files to `data/raw/`
2. Set `data/raw/` as conceptually read-only (the raw-data-guard hook enforces this)
3. Note the original file locations in the README provenance section
4. Suggest running `/data-validate` next

### Step 5 — Initialize git

If not already in a git repo:
1. Create `.gitignore` from template
2. `git init`
3. Create initial commit with structure (but NOT data files — those go in .gitignore or are tracked separately)

### Step 6 — Print summary and next steps

Show the researcher what was created and suggest next steps per [_shared/next-steps.md](../_shared/next-steps.md).

## Principles

Read [references/principles.md](references/principles.md) for the foundational principles behind every scaffolding decision.

## Voice

Efficient and organized. You're setting up a workspace, not giving a lecture. Create the structure, explain what each piece is for briefly, and get the researcher moving. Show the directory tree at the end so they can see what was built.

## Argument handling

- `research-init my-study` → creates `./my-study/`
- `research-init my-study --lang r` → R only
- `research-init my-study --existing-data ~/data/survey.csv` → copies data to `data/raw/`
- `research-init` (no args) → asks for project name
