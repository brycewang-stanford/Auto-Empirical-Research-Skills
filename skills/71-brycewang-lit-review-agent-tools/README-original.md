# Claude Skill — `literature-review-tools`

This repo's curated catalog is also packaged as an installable **[Claude Agent Skill](https://docs.claude.com/en/docs/claude-code/skills)** — and it does two things:

- **Recommend** — ask *"what should I use to turn PDFs into Markdown for an LLM?"* and it routes you to the best open-source pick with a one-line rationale.
- **Run** — ask *"use MinerU to convert this PDF"* or *"ask PaperQA2 about these papers"* and Claude drives the bundled launcher to install the tool in an isolated venv and run it — no manual pip wrangling.

```text
skills/
└── literature-review-tools/
    ├── SKILL.md              # routing (recommend) + launcher instructions (run)
    ├── recipes/
    │   └── recipes.json      # machine-readable manifest of runnable tools
    ├── scripts/
    │   └── litrun.py         # launcher: install/run/configure tools by id
    └── reference/
        └── catalog.md        # full 70+ tool catalog (progressive disclosure)
```

## The launcher (`litrun.py`)

Dependency-free (stdlib only). Installs each tool into its own venv under
`~/.lit-review-tools/` (prefers [`uv`](https://docs.astral.sh/uv/), falls back to
`python -m venv`), and reads API keys from one shared `~/.lit-review-tools/.env`.

```bash
scripts/litrun.py list                 # what can be run
scripts/litrun.py doctor               # toolchain + which API keys are set
scripts/litrun.py info mineru          # a tool's install/run details
scripts/litrun.py env --set OPENAI_API_KEY=sk-...
scripts/litrun.py run mineru -- -p paper.pdf -o ./out -b pipeline
scripts/litrun.py run paper-qa -- ask "What methods does this corpus use?"
scripts/litrun.py mcp arxiv-mcp-server # prints MCP config to register in Claude/Cursor
scripts/litrun.py ui gpt-researcher    # clone & launch the full web UI (:8000)

# chained pipelines
scripts/litrun.py workflow list
scripts/litrun.py workflow run topic-to-review \
  --query "cat:cs.CL retrieval augmented generation" --max 8 \
  --question "What evaluation benchmarks recur?" --dry-run   # preview, then drop --dry-run
```

Runnable tools today: **MinerU · marker · docling** (PDF→Markdown), **PaperQA2**
(cited Q&A), **ASReview** (PRISMA screening), **arxiv-fetch** (search & download
arXiv PDFs), **GPT Researcher · STORM** (deep research), **scholarly · pyalex**
(API clients), and the **arxiv / paper-search / zotero** MCP servers.

Built-in workflows: `pdf-to-markdown`, `pdf-corpus-qa`, `pdf-md-then-qa`,
`topic-to-pdfs`, and `topic-to-review` (arXiv query → download PDFs → cited
answer — a full lightweight review with no MCP client). The 70+ catalog stays
browse-only; more recipes/workflows are easy to add to `recipes/`.

## Install

**As a plugin (recommended)** — the repo doubles as a Claude Code plugin marketplace:

```text
/plugin marketplace add brycewang-stanford/lit-review-agent-tools
/plugin install lit-review-agent-tools@lit-review-marketplace
```

That pulls in the skill *and* the launcher scripts in one step.

**Copy the skill folder** (Claude Code personal skills live in `~/.claude/skills/`):

```bash
git clone https://github.com/brycewang-stanford/lit-review-agent-tools
cp -r lit-review-agent-tools/skills/literature-review-tools ~/.claude/skills/
```

Restart Claude Code (or run `/doctor`) and the skill auto-loads. Claude invokes it
whenever your request matches literature-review tool selection — no manual trigger needed.

**Project-scoped:** copy the same folder into `.claude/skills/` inside any project.

**Other Agent-SDK / MCP hosts:** point your skills loader at
`skills/literature-review-tools/SKILL.md`.

## How it works

- **`SKILL.md`** carries the YAML frontmatter (`name`, `description`) Claude uses to
  decide *when* to activate, plus the lightweight routing logic (pickers + decision tables).
- **`reference/catalog.md`** holds the full catalog and is only read when Claude needs
  the complete list, exact star counts, or a category not summarized in `SKILL.md` —
  classic progressive disclosure so the base context stays small.

Star counts are periodic GitHub-API snapshots; the repo README is the live source of truth.
