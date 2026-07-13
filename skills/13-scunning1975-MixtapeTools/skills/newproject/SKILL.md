---
name: newproject
description: Scaffold a new research project with standard directory structure, CLAUDE.md template, and documented README. Use this at the start of every new project to ensure consistent organization.
allowed-tools: Bash(mkdir*), Bash(cp*), Bash(ls*), Write, Read
argument-hint: "[project-name]"
---

# New Project Scaffold

Create a new research project folder with Scott's standard structure. This skill is invoked at the start of every project.

## What Gets Created

```
[project-name]/
├── CLAUDE.md              # Permanent research rules (copied from template)
├── README.md              # Project-specific overview (auto-generated)
├── code/
│   ├── R/
│   ├── python/
│   └── stata/
├── data/
│   ├── raw/               # Original source data (never modify)
│   └── clean/             # Cleaned/merged datasets
├── output/
│   ├── tables/
│   └── figures/
├── documents/             # Outside PDFs, papers (use /split-pdf on these)
├── decks/                 # Beamer presentations (rhetoric of decks)
├── notes/                 # Scratch notes, random ideas, misc
└── progress_logs/         # Session continuity across Claude conversations
```

## Execution

1. **Get the project name** from the argument. If none provided, ask.
   - Convert spaces to hyphens, lowercase

2. **Determine location** — default is current working directory. Confirm if unclear.

3. **Create all directories:**
   ```bash
   mkdir -p [project-name]/{code/{R,stata,python},data/{raw,clean},output/{figures,tables},documents,decks,notes,progress_logs}
   ```

4. **Copy CLAUDE.md** from `~/mixtapetools/claude/CLAUDE.md`:
   - Replace `[Your Name]` with `Scott`
   - Update project name in the overview section

5. **Generate README.md** with:
   - Project title
   - Visual directory tree in a fenced code block (monospace)
   - Explanation of each folder's purpose
   - Note that CLAUDE.md is copied from a permanent template and edited per-project
   - Note that README.md is for project-specific documentation
   - Note that progress_logs/ maintains continuity across Claude sessions
   - Placeholder sections: Overview, Collaborators, Status, Key Files

   The README must include this tree block:

   ````markdown
   ```
   [project-name]/
   ├── CLAUDE.md              # Research rules & estimation philosophy (permanent)
   ├── README.md              # This file — project-specific notes
   ├── code/
   │   ├── R/                 # R scripts
   │   ├── python/            # Python scripts
   │   └── stata/             # Stata do-files
   ├── data/
   │   ├── raw/               # Original source data (never modify these)
   │   └── clean/             # Cleaned and merged datasets
   ├── output/
   │   ├── tables/            # Generated tables (LaTeX, CSV)
   │   └── figures/           # Generated figures (PDF, PNG)
   ├── documents/             # Outside papers and PDFs (split with /split-pdf)
   ├── decks/                 # Beamer presentations (rhetoric of decks philosophy)
   ├── notes/                 # Scratch notes, ideas, miscellaneous
   └── progress_logs/         # Session logs for continuity across Claude conversations
   ```
   ````

6. **Create initial progress log** at `progress_logs/YYYY-MM-DD_setup.md`:
   - Record the creation date
   - List next steps as a checklist

7. **Report success** — show structure with `ls`, remind user to update CLAUDE.md.
