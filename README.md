# 📝 copy-edit-master

Multi-stage academic copy-editing plugin for Claude Code. Detects whether a manuscript is **theory** or **general academic**, then runs a pipeline of specialist subagents over `.md`, `.tex`, or `.docx` files. Each stage is followed by an automated quality review with up to two iterations before escalating to the user.

## ✨ Features

- **Auto paper-type detection** — `theory-analyzer` classifies the document and picks the workflow.
- **Two workflows**:
  - **General Academic (2 stages)**: Structural Edit → Line Edit + Proofread
  - **Theory Paper (5 stages)**: General Structure → Theory Refinement → Technical Elements → General Line Edit → Theory Line Edit
- **Role-based subagents** — clean separation of structure / line / technical / review concerns; each reads the relevant `stage_file` for authoritative rules.
- **Automated review loop** — `quality-reviewer` validates each stage with explicit APPROVED / NEEDS REVISION decisions; the orchestrator iterates up to 2× before asking the user.
- **In-place editing with backup** — original is preserved at `<name>.backup.<ext>`; per-stage reports written to the manuscript's directory.
- **Optional git workflow** — proposes a commit after every stage if the directory is a git repo.
- **LaTeX-aware** — preserves math environments, citations, labels; warns on moderate/complex `.tex` files.

## 📦 Installation

Install via the Claude Code plugin marketplace, or load locally:

```bash
cc --plugin-dir /path/to/copy-edit-master-plugin
```

## 🚀 Usage

Trigger the skill in Claude Code by mentioning the file:

```
Copy-edit papers/draft.md
```

The orchestrator will:

1. Back up the file.
2. Run `theory-analyzer` and confirm paper type.
3. Generate global context (summary + section outline).
4. Detect LaTeX complexity (for `.tex`) and ask for confirmation if non-trivial.
5. Set up `TodoWrite` for stage tracking.
6. Execute the appropriate workflow, with quality review and optional git commits between stages.
7. Produce a final report.

## 🧩 Plugin contents

```
copy-edit-master-plugin/
├── .claude-plugin/plugin.json
├── README.md
├── skills/
│   └── copy-edit-master/
│       ├── SKILL.md            # orchestrator
│       ├── reference/          # Lectures + chunking + iteration + LaTeX support
│       └── stages/             # Authoritative stage rules (read by subagents)
│           ├── general/        # 01-structure, 02-line-edit
│           └── theory/         # 00-analysis, 01-structure-refinement, 02-technical, 02-line-edit-additions
└── agents/
    ├── theory-analyzer.md         # Paper-type classification
    ├── structure-editor.md        # General structure + theory structural refinement
    ├── line-editor.md             # General line edit + theory line edit (per section)
    ├── theory-technical-editor.md # Notation / definitions / proofs / figures (full-doc)
    └── quality-reviewer.md        # APPROVED / NEEDS REVISION gate after each stage
```

## 🔌 Subagent dispatch

The orchestrator passes a `stage_file` parameter to dispatch role-based agents to specific work:

| Stage | Subagent | `stage_file` |
|---|---|---|
| Phase 1 detection | `theory-analyzer` | `stages/theory/00-analysis.md` |
| General Stage 1 | `structure-editor` | `stages/general/01-structure.md` |
| General Stage 2 | `line-editor` (per section) | `stages/general/02-line-edit.md` |
| Theory Stage 1 | `structure-editor` | `stages/general/01-structure.md` |
| Theory Stage 2 | `structure-editor` | `stages/theory/01-structure-refinement.md` |
| Theory Stage 3 | `theory-technical-editor` | `stages/theory/02-technical.md` |
| Theory Stage 4 | `line-editor` (per section) | `stages/general/02-line-edit.md` |
| Theory Stage 5 | `line-editor` (per section) | `stages/theory/02-line-edit-additions.md` |
| After every stage | `quality-reviewer` | (reads same `stage_file`) |

Stage files are addressed via `${CLAUDE_PLUGIN_ROOT}` so paths resolve regardless of where the plugin is installed.

## 📚 Foundations

The editing rules synthesize:

- Strunk & White, *The Elements of Style*
- Deirdre McCloskey, *Economical Writing*
- William Thomson, *A Guide for the Young Economist* (theory-paper chapters)

Full lecture notes live under `skills/copy-edit-master/reference/`.

## ⚙️ Notes

- Edits are made **in place**; the `.backup.<ext>` file preserves the original.
- Stage reports (`stage-N-*.md`) are written into the manuscript's directory.
- If the directory is not a git repository, the orchestrator will offer to initialize one or skip git steps.
- For very long manuscripts (>15K words), the orchestrator enables paragraph-level chunking for line-edit stages.
