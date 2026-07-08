# 08 - Citation Management and Typesetting

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  CoPaper.AI's analysis results are emitted via save_table() and save_figure()
  with independent numbering for tables and figures, ready to be exported to
  LaTeX/Word for paper typesetting.
-->

> **Sloppy citation format is a common reason for desk rejection.** Even worse are AI-invented fake citations — a paper that looks serious but cites articles that don't exist will be rejected on the spot. These skills help you solve both problems.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the per-tool details below complement this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [`62` citation-checker](../../skills/62-PHY041-claude-skill-citation-checker/) | Verify citations against CrossRef / S2 / OpenAlex | Batch-verify every citation before submission |
| [`08` latex-document-skill](../../skills/08-ndpvt-web-latex-document-skill/) | Create / compile any LaTeX document to PDF | Typeset and compile a LaTeX manuscript |
| [`07` AI-Research-SKILLs](../../skills/07-Orchestra-Research-AI-Research-SKILLs/) | Publication-grade ML figures, LaTeX, citation verification | Generate publication-grade figures + LaTeX + citation verification |
| [`04` scientific-writer](../../skills/04-K-Dense-AI-claude-scientific-writer/) | Citation management + scientific writing | Maintain a BibTeX file and unify citation styles |
| [`22` christopherkenny-skills](../../skills/22-christopherkenny-skills/) | APSA-style checks for Quarto (`.qmd`) | Political-science / Quarto typesetting-style validator |
| [`54` open-science-skills](../../skills/54-scdenney-open-science-skills/) | Citation consistency, DOI, and argument-support audit | Check that every textual claim has citation support |

---

## Skills List

### academic-citation-manager

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | Two things: 1) based on the manuscript body, automatically find **real-existing** references, 2) unify all citations to the target format |
| **Supported formats** | APA, Chicago, MLA, etc. |
| **Core value** | Solves the biggest pitfall of AI-written papers — invented references |
| **Install** | `clawhub install academic-citation-manager` |

### citation-verification

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | Automatically checks the accuracy of every citation in the paper |
| **Principle** | Verify that each citation really exists via Crossref, Semantic Scholar, and similar APIs |

### BibTeX Management

| Attribute | Description |
|------|------|
| **Source** | [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) |
| **Function** | BibTeX file management, deduplication, format unification |
| **Highlight** | Slash commands operate directly on `.bib` files |

### LaTeX (Typesetting)

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | Generate syntactically correct LaTeX documents, including package management and compilation workflow |
| **Usage** | Describe what kind of table/formula you want, and it generates the LaTeX code |
| **Install** | `clawhub install latex` |

### latex-document-skill (LaTeX Document Expert)

| Attribute | Description |
|------|------|
| **Source** | [ndpvt-web/latex-document-skill](https://github.com/ndpvt-web/latex-document-skill) |
| **Stars** | 74 |
| **Scale** | 27 templates + 22 scripts + 22 reference guides |
| **Highlight** | Handwritten notes → automatic LaTeX conversion |

### stats-paper-writing-agent-skills (Statistical Paper in LaTeX)

| Attribute | Description |
|------|------|
| **Source** | [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) |
| **Function** | LaTeX statistics-paper writing: title, authors, abstract and other front-matter drafts |
| **Best for** | Statistics and econometrics papers |

### claude-office-skills (Office Documents)

| Attribute | Description |
|------|------|
| **Source** | [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) |
| **Stars** | 251 |
| **Function** | Complete PPTX, DOCX, XLSX, PDF workflow |
| **Best for** | When you need Word/PPT output |

### pdf / docx / xlsx / pptx (Official Document Skills)

| Attribute | Description |
|------|------|
| **Source** | [Anthropic official Skills](https://github.com/anthropics/skills) |
| **Function** | Document processing, format conversion |

### zotero-mcp (Zotero MCP Integration)

| Attribute | Description |
|------|------|
| **Source** | [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) |
| **Function** | Connect your Zotero library with AI assistants such as Claude: paper review, summarisation, citation analysis, PDF-annotation extraction |

### zotero-mcp-skill (Zotero Semantic-Search Skill)

| Attribute | Description |
|------|------|
| **Source** | [kerim/zotero-mcp-skill](https://github.com/kerim/zotero-mcp-skill) |
| **Function** | Multi-strategy semantic search against a Zotero library through an MCP server |

### zoterosynth (Zotero Literature Synthesis)

| Attribute | Description |
|------|------|
| **Source** | bahayonghang/my-claude-code-settings |
| **Function** | Search, analyse, and synthesise your Zotero library via zotero-mcp, generate literature reviews, and export BibTeX |

### academic-pptx-skill (Academic Presentation Skill)

| Attribute | Description |
|------|------|
| **Source** | [Gabberflast/academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill) |
| **Function** | Create academic presentations (conference talks, seminars, thesis defence, grant pitches) — enforces action-titles, structured arguments, citation standards |
| **Highlight** | Pairs with the Anthropic-built PPTX Skill |

### Reference Manager

| Attribute | Description |
|------|------|
| **Source** | MCPMarket |
| **Function** | Identifies the references needed for each section of a paper, locates entries via Zotero MCP, retrieves full-text PDFs, and organises them into a structured format |

---

## Regression-Result Output Tools

| Tool | Command / package | Output format |
|------|---------|---------|
| **Stata** | `outreg2` / `esttab` / `asdoc` | Word / LaTeX / Excel |
| **R** | `stargazer` / `modelsummary` / `etable()` | LaTeX / HTML / Word |
| **Python** | `statsmodels.summary()` + `pandas.to_latex()` | LaTeX / CSV |

---

## Writing-Aid Tools

| Tool | Function | Use case |
|------|------|------|
| **Overleaf** | Online collaborative LaTeX editor | Multi-author paper writing |
| **Grammarly** | Grammar check and style suggestions | English-language polishing |
| **Scite AI** | Smart citation analysis (supporting vs. contrasting vs. mentioning) | Citation-quality assessment |
| **Zotero** | Open-source reference management | Reference management + MCP integration |

---

## Practical Advice

1. **Zotero + Better BibTeX is the golden combo**: Zotero manages your references, Better BibTeX auto-exports `.bib` files, LaTeX picks them up at compile time.
2. **Always verify before submission**: use `citation-verification` to check that every citation actually exists — this single step can avoid an embarrassing desk rejection.
3. **Different journals, different formats**: AER uses Chicago Author-Date, QJE uses its own format. Use `academic-citation-manager` to switch in one click.

---

[← Previous chapter](07-revision-and-polish.md) | [Next chapter: 09 - Replication and Reproducible Research →](09-replication-and-reproducible-research.md)