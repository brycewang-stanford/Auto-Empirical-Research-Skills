---
name: init
description: "Fills all [FILL:] placeholders across the template to initialize a new research project. Use when setting up a freshly cloned project."
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Initialize Project

Fill in all `[FILL:]` placeholders across the template to set up a new research project.

## Steps

1. Scan all tracked files for `[FILL:` patterns and group them by file:
   ```bash
   grep -rn "\[FILL:" --include="*.md" --include="*.qmd" --include="*.toml" --include="*.tex" --include="*.yml" .
   ```
   Report how many placeholders exist and in which files.

2. Ask the user for project information:
   - **Project title** (used in `index.qmd`, `README.md`, `CLAUDE.md`, `pyproject.toml`)
   - **Subtitle** (optional, for `index.qmd`)
   - **Authors** — for each author:
     - Name, affiliation (university, city, country), ORCID, email
     - Whether they are the corresponding author
   - **Abstract** (for `index.qmd`)
   - **Keywords** (for `index.qmd`)
   - **Project stage** (for `CLAUDE.md`: Idea / Data collection / Analysis / Writing / Revision)
   - **Data source description** (for `CLAUDE.md` and `README.md`)
   - **Repository URL** (for `README.md`)
   - **Project slug** (for `pyproject.toml` `name` field, e.g., `regional-gdp-study`)

3. Apply the values to each file:
   - **`index.qmd`** — title, subtitle, authors (full YAML array with affiliations/ORCID/email), abstract, keywords
   - **`README.md`** — project title, description paragraph, data section, repository URL, Quick Start clone URL
   - **`CLAUDE.md`** — Project Context table: title, authors, stage, data source
   - **`pyproject.toml`** — `name`, `description`, `authors`
   - **`_quarto.yml`** — no `[FILL:]` placeholders by default, but verify
   - **`templates/chadManuscript/manuscript.tex`** — author names and keywords

4. After applying all values, re-scan for remaining `[FILL:]` placeholders:
   ```bash
   grep -rn "\[FILL:" --include="*.md" --include="*.qmd" --include="*.toml" --include="*.tex" --include="*.yml" .
   ```
   Report how many remain and where (some are expected in section bodies like "Describe the data...").

5. Run `bash scripts/render.sh` to regenerate `latex/index.tex` with the real content.

6. Report a summary: files updated, placeholders filled, placeholders remaining, render status.
