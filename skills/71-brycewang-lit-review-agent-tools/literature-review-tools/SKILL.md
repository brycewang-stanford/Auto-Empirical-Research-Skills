---
name: literature-review-tools
description: >-
  Recommend AND run open-source AI tools, agents, Claude Code / Codex skills, and
  MCP servers for any stage of a literature review — searching, reading,
  extracting, synthesizing, screening, citation-checking, and paper writing. Use
  when the user asks "what tool should I use to..." OR "install/run/use <tool> to
  ..." for research/lit-review work: automating a survey or related-work section,
  PDF→Markdown extraction for LLMs (MinerU/marker/docling), PRISMA / systematic
  review (ASReview), citation-backed Q&A over PDFs (PaperQA2), wiring papers into
  Claude/Cursor via MCP (arxiv/paper-search/zotero servers), or chatting with a
  Zotero library. Ships a launcher (scripts/litrun.py) that installs each tool in
  an isolated venv and runs it. Curated catalog of 70+ vetted projects.
  支持中英文（用于「文献综述工具选型」与「一键安装/运行」）。
---

# Literature Review Tools — Select & Run

A curated, use-case-organized catalog of the strongest **open-source** AI tools for
literature review — **plus a launcher that actually installs and runs the top ones.**
Covers: end-to-end research agents, deep-research / auto-survey generators, autonomous
"idea→paper" systems, citation-backed RAG over PDFs, PRISMA screening, MCP servers,
Zotero/Obsidian integrations, PDF→structured extraction, citation graphs, and
paper-writing / peer-review assistants.

Full source of truth (README, always current star counts): <https://github.com/brycewang-stanford/lit-review-agent-tools>

## Two modes

- **Recommend** — user asks "what should I use to …". Route with the tables below; cite the catalog for details.
- **Run** — user asks to *install / run / use* a specific tool ("turn this PDF into Markdown with MinerU", "ask PaperQA2 about these papers", "set up the arXiv MCP server"). Drive [`scripts/litrun.py`](scripts/litrun.py) via Bash — do not hand the user raw pip commands to copy.

## Run mode — how to drive `scripts/litrun.py`

The launcher installs each supported tool into its own venv under `~/.lit-review-tools/`
(uses `uv` if present, else `python -m venv`) and reads API keys from one shared
`~/.lit-review-tools/.env`. Machine-readable recipes: [`recipes/recipes.json`](recipes/recipes.json).

Typical flow when the user wants to *use* a tool:

1. `python3 scripts/litrun.py doctor` — check toolchain + which API keys are already set.
2. `python3 scripts/litrun.py info <id>` — confirm what the tool needs (entry, required env).
3. If a required key is missing, ask the user for it, then `litrun.py env --set KEY=VALUE` (never echo the value back in full).
4. `python3 scripts/litrun.py run <id> -- <tool args>` — installs on first use, then runs. For PDF tools pass the real file path; e.g. `run mineru -- -p paper.pdf -o ./out -b pipeline`.
5. For **MCP servers**, don't "run" them — `litrun.py mcp <id>` prints the client config block to register in Claude Code / Cursor.

Commands: `list [--category C] [--kind K]` · `info <id>` · `doctor` · `env [--set K=V]` · `install <id>` · `run <id> -- <args>` · `mcp <id> [--storage PATH] [--client claude|cursor]` · `ui <id>`.

Runnable ids by kind:
- **python-cli (auto install+run):** `mineru`, `marker`, `docling` (PDF→Markdown) · `paper-qa` (cited Q&A) · `asreview` (PRISMA screening UI)
- **python-script (bundled, auto install+run):** `arxiv-fetch` (search arXiv & download PDFs, no key)
- **python-lib (install + run example):** `gpt-researcher`, `storm` (deep research; need API keys) · `scholarly`, `pyalex` (API clients)
- **mcp-server (install + `mcp` config):** `arxiv-mcp-server`, `paper-search-mcp`, `zotero-mcp`

For **`gpt-researcher`** and **`storm`**, `litrun.py ui <id>` clones the repo and launches the full web UI (GPT Researcher → FastAPI at :8000; STORM → Streamlit at :8501). These are long-running servers — launch them with a background Bash call and tell the user the URL. gpt-researcher's UI needs `OPENAI_API_KEY` + `TAVILY_API_KEY` set first (litrun writes them into the repo's `.env`); STORM takes its keys in the app sidebar.

### Chained pipelines

For multi-tool tasks, prefer a named workflow over hand-wiring steps: `litrun.py workflow list` then `litrun.py workflow run <id> [--input PATH] [--query "..."] [--question "..."] [--max N]`. Built-ins:
- `pdf-to-markdown` — a PDF/folder → clean Markdown (MinerU)
- `pdf-corpus-qa` — a folder of PDFs → citation-backed answer (PaperQA2)
- `pdf-md-then-qa` — convert to Markdown **and** answer a question over the corpus
- `topic-to-pdfs` — arXiv query → download top-N PDFs (arxiv-fetch, no key)
- `topic-to-review` — arXiv query → download PDFs → citation-backed answer (PaperQA2). The end-to-end "retrieve then review" pipeline; no MCP client needed. Needs `OPENAI_API_KEY` for the QA step.

Add `--dry-run` first to show the exact resolved step commands without executing — good for confirming paths with the user before a heavy run. Workflows fail fast if a required API key is missing.

Guardrails: installs and downloads happen under the user's home and hit the network — for a heavy first install (marker/docling pull in PyTorch) say so before running. Never fabricate API keys. If a `run` fails, show the real error rather than claiming success. Paths in this file (`scripts/…`, `recipes/…`) are relative to this skill's directory.

## Recommend mode — how to route

1. Identify **which stage** of the lit-review workflow the user is on (search → read → extract → synthesize → screen → cite-check → write/review).
2. Match it to a category below and recommend the **⭐ editor's pick first**, then 1–2 alternatives.
3. For anything beyond the top pick — full star counts, every project in a category, or a category not summarized here — read [`reference/catalog.md`](reference/catalog.md). Do **not** guess project names or URLs; pull them from the catalog.
4. Give a one-line "why this one" tied to the user's constraint (Claude Code vs. standalone, open vs. commercial, privacy/local, medical, etc.). If the pick is a runnable id above, offer to install/run it.

## ⚡ 30-second picker

```text
Use Claude Code, want end-to-end research→paper ──────────▶ academic-research-skills ⭐
Want AI to research a topic → cited report ───────────────▶ GPT Researcher / STORM
Want fully autonomous "idea → submittable paper" ────────▶ AI-Scientist-v2 / AutoResearchClaw
Citation-backed Q&A over a pile of PDFs ──────────────────▶ PaperQA2
Rigorous PRISMA review (thousands of abstracts) ─────────▶ ASReview / prismAId
Clean Markdown from PDFs to feed an LLM ─────────────────▶ MinerU / Docling / marker
Lit capabilities inside Claude / Cursor (MCP) ───────────▶ paper-search-mcp / zotero-mcp
Chat with your library inside Zotero ────────────────────▶ zotero-gpt / PapersGPT
Pre-submission AI peer review ───────────────────────────▶ open_reviewer / ai-peer-review
```

## Categories (top pick per category)

| Category | Editor's pick ⭐ | When |
|---|---|---|
| All-in-one research agents & skills | **academic-research-skills** | Claude Code user wanting research→write→review→revise, with integrity/citation gates |
| Deep research & auto-survey | **STORM** / **gpt-researcher** | Topic → cited survey / report / related-work |
| Autonomous science (idea→paper) | **AI-Scientist(-v2)** / **AutoResearchClaw** | Fully automated discovery: lit + hypotheses + experiments + writing |
| Literature Q&A / RAG | **paper-qa (PaperQA2)** | Citation-backed answers over a PDF corpus |
| Systematic review & screening | **ASReview** | Active-learning screening of thousands of abstracts (PRISMA) |
| MCP servers | **zotero-mcp** / **arxiv-mcp-server** | Wire papers into Claude / Cursor / Cline |
| Zotero / Obsidian integration | **zotero-gpt** | Chat with your library inside your reference manager |
| PDF → structured extraction | **MinerU** / **docling** / **marker** | Turn PDFs into clean Markdown/JSON for LLMs |
| Citation graphs & API clients | **scholarly** / **pyalex** | Citation-network analysis; scripting academic DBs |
| Writing & peer-review assistants | **open_reviewer** / **ai-peer-review** | Draft, polish, and pre-submission review |
| Awesome lists | **Awesome-Auto-Research-Tools** | Browse the whole landscape |

## Decision table (map need → recommendation)

| User's need | Recommend |
|---|---|
| Claude Code, end-to-end research→paper | **academic-research-skills** (most complete, #1 in space) |
| Generic "research this topic for me" agent | **GPT Researcher** / **STORM** |
| Wiki/survey-style long-form with citations | **STORM / Co-STORM** |
| Fully autonomous "idea → submittable paper" | **AI-Scientist-v2** / **AutoResearchClaw** |
| Cited Q&A over many PDFs | **PaperQA / PaperQA2** |
| Rigorous PRISMA systematic review | **ASReview** or **prismAId** |
| PDF → clean Markdown for an LLM | **MinerU / Docling / marker** |
| Lit capabilities in an MCP client | **paper-search-mcp / zotero-mcp** |
| Chat with library inside Zotero | **zotero-gpt / PapersGPT** |
| AI pre-review before submission | **open_reviewer / ai-peer-review** |
| Just want to browse the landscape | The **Awesome lists** section |

## Notes & caveats

- **Open-source is prioritized.** Commercial/closed tools (Elicit, Consensus, Scite, SciSpace, Research Rabbit, Connected Papers) are listed for reference only — see the catalog's commercial section.
- **Star counts drift.** The catalog's numbers are periodic GitHub-API snapshots — treat as rough popularity signals, not exact. For live numbers, point the user at the repo.
- **Match the constraint, not just the task.** Privacy/local → `local-deep-research`; medical → `medsci-skills` / `paperai`; Codex instead of Claude → `academic-research-skills-codex`.

Full catalog with every project, star count, and one-line description: [`reference/catalog.md`](reference/catalog.md).
