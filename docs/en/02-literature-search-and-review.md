# 02 - Literature Search and Review

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  Literature review is one of the most time-consuming "grunt-work" phases of
  empirical research. CoPaper.AI's PaperAgent supports an Agent-mode
  literature review: it reads local papers directly, plans multi-step tasks
  autonomously, and fully automates the chain from search to classification
  to framework-building.
-->

> **A literature review is not "list everything you found" — it is "logically organize what you have read."** The value of an AI agent lies in automating the most time-consuming "grunt work" (searching, screening, summarising, classifying) so that you can spend your time on the most essential "judgement" parts.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the "Skills list" below gives per-method details (with selected upstream links) and complements this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [`05` research-superpower](../../skills/05-kthorn-research-superpower/) | Systematic search, screening, and citation back-tracing | Run an end-to-end systematic-review retrieval and de-duplicated screening |
| [`59` openalex-skill](../../skills/59-shiquda-openalex-skill/) | Query 240M+ scholarly works via OpenAlex | Programmatically pull candidate papers and citation networks for free |
| [`36` literature-review-skill](../../skills/36-taoyunudt-literature-review-skill/) | End-to-end literature-review workflow (Chinese) | Full Chinese-context review pipeline from retrieval to manuscript |
| [`52` slr-prisma](../../skills/52-keemanxp-slr-prisma/) | Systematic literature review following PRISMA 2020 | Use when you need a standard PRISMA flowchart and reproducible screening |
| [`33` claude-scholar](../../skills/33-Galaxy-Dawn-claude-scholar/) | Full research lifecycle: ideation → review → experiment → response | Integrated retrieval, citation check, and review writing |
| [`43` research-plugins](../../skills/43-wentorai-research-plugins/) | 478 research plugins: visualisation, domains, infrastructure | Pick domain/database-specific retrieval and review plugins |

---

## Skills List

### literature-search

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | Simultaneously searches **8 academic databases**: Google Scholar, PubMed, arXiv, Semantic Scholar, OpenAlex, Crossref, and more |
| **Workflow** | Describe the research direction in natural language → cross-database search → return structured paper lists (title, abstract, citation count) |
| **Time savings** | What used to take half a day of swapping keywords now takes a sentence and a few seconds |
| **Install** | `clawhub install literature-search` |

### ii-commons (Deterministic Retrieval Across Corpora)

| Attribute | Description |
|------|------|
| **Source** | [Intelligent-Internet/II-Commons-Skills](https://github.com/Intelligent-Internet/II-Commons-Skills) |
| **Function** | Agent-oriented deterministic retrieval skills and a Node.js CLI, covering arXiv, PubMed/PMC, and supported US-policy corpora |
| **Workflow** | `cutoff` to inspect the daily corpus boundary → search by corpus → pull metadata or full-text Markdown → trace evidence back via stable IDs |
| **Best for** | Reproducible literature retrieval, public-health/policy evidence comparison, cross-arXiv-and-PubMed reviews |
| **Install** | `npx @intelligentinternet/ii-commons --help` or install `skills/ii-commons/` from the repo |

### literature-review

| Attribute | Description |
|------|------|
| **Source** | ClawHub / [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) |
| **Function** | Based on the Semantic Scholar, OpenAlex, and Crossref APIs, automatically extract key information from each paper and **skeleton out a review paragraph framework** |
| **Note** | It does not write the review for you; it scaffolds the framework. Once the skeleton is in place, you fill in your own analysis and judgement |
| **Install** | `clawhub install literature-review` or `npx skills add https://github.com/K-Dense-AI/claude-scientific-skills --skill literature-review` |

### literature-reviewer (Claude-Scholar Version)

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | Paper search → classification → synthesis, integrated with Zotero MCP |
| **Highlight** | Deep integration with the Zotero reference manager; can directly operate on your library |

### research-superpower (Literature Search Powerhouse)

| Attribute | Description |
|------|------|
| **Source** | [kthorn/research-superpower](https://github.com/kthorn/research-superpower) |
| **Function** | PubMed + Semantic Scholar integration; intelligent paper screening |
| **Workflow** | 1. Parse the literature question<br>2. Build screening criteria<br>3. Search PubMed<br>4. Screen abstracts (0–10 score)<br>5. Deep-dive into related papers<br>6. Traverse citations (forward + backward)<br>7. Synthesise findings into `SUMMARY.md` |
| **Highlight** | Citation traversal (forward+backward), Unpaywall integration (find free full text), large-scale screening (50+ papers in parallel) |
| **Install** | `/plugin marketplace add https://github.com/kthorn/research-superpower` |

### Deep-Research-skills

| Attribute | Description |
|------|------|
| **Source** | [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) |
| **Function** | Two-stage research (outline generation + in-depth investigation) with human-in-the-loop control |
| **Highlight** | Supports Claude Code / OpenCode / Codex; oriented toward academic research (paper reviews, benchmark studies, literature analysis) |

### arXiv Search + DOI Lookup (Statistical-Research Plugin)

| Attribute | Description |
|------|------|
| **Source** | [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) |
| **Function** | arXiv search, DOI lookup, BibTeX management, literature-gap analysis |
| **Highlight** | Designed for statistical researchers; slash commands invoke directly |

### claude-deep-research-skill (Enterprise Deep Research)

| Attribute | Description |
|------|------|
| **Source** | [199-biotechnologies/claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill) |
| **Function** | 8-stage deep-research pipeline with source credibility scoring and automated validation |
| **Highlight** | Outperforms OpenAI, Gemini, and Claude Desktop's built-in research on quality and validation |

### LitLLM (AI Literature-Review Assistant)

| Attribute | Description |
|------|------|
| **Source** | [LitLLM/LitLLM](https://github.com/LitLLM/LitLLM) |
| **Function** | RAG-based literature review: keyword extraction → multi-strategy retrieval (keyword + embedding) → re-ranking and attribution |
| **Best for** | Large-scale literature-review writing |

### Academix (Academic Search Aggregator MCP)

| Attribute | Description |
|------|------|
| **Source** | [xingyulu23/Academix](https://github.com/xingyulu23/Academix) |
| **Function** | MCP server that aggregates OpenAlex, DBLP, Semantic Scholar, arXiv, and CrossRef into a unified research interface |
| **Best for** | Systematic surveys that need cross-database retrieval |

### paper-distill-mcp (Paper-Distillation MCP)

| Attribute | Description |
|------|------|
| **Source** | [Eclipse-Cj/paper-distill-mcp](https://github.com/Eclipse-Cj/paper-distill-mcp) |
| **Function** | Parallel search across 11 sources (OpenAlex, Semantic Scholar, PubMed, arXiv, Papers with Code, CrossRef, Europe PMC, bioRxiv, DBLP, CORE, Unpaywall) |
| **Highlight** | 4-dimensional weighted ranking (relevance, recency, impact, novelty) with adaptive push |

### openalex-research-mcp (OpenAlex Research MCP)

| Attribute | Description |
|------|------|
| **Source** | [oksure/openalex-research-mcp](https://github.com/oksure/openalex-research-mcp) |
| **Function** | Search 240M+ scholarly works, analyse citations, track research trends, map collaboration networks |

### semantic-scholar-mcp

| Attribute | Description |
|------|------|
| **Source** | [zongmin-yu/semantic-scholar-fastmcp-mcp-server](https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server) |
| **Function** | Full Semantic Scholar API access: paper data, author information, citation networks |

### paper-search-mcp

| Attribute | Description |
|------|------|
| **Source** | [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) |
| **Function** | Search and download papers from 20+ sources: arXiv, PubMed, bioRxiv, Google Scholar, Semantic Scholar, Crossref, OpenAlex, CORE, Europe PMC, DOAJ, SSRN, etc. |

### mcp-for-research (Unified Research MCP)

| Attribute | Description |
|------|------|
| **Source** | [aringadre76/mcp-for-research](https://github.com/aringadre76/mcp-for-research) |
| **Function** | Integrates PubMed, Google Scholar, arXiv, JSTOR; 5 unified tools replace 24 endpoints |
| **Install** | Published on NPM |

### arxiv-mcp-server (arXiv MCP)

| Attribute | Description |
|------|------|
| **Source** | [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) |
| **Function** | MCP server for arXiv paper search and analysis |

### paper-search-mcp-nodejs (Node.js Paper-Search MCP)

| Attribute | Description |
|------|------|
| **Source** | [Dianel555/paper-search-mcp-nodejs](https://github.com/Dianel555/paper-search-mcp-nodejs) |
| **Function** | Node.js implementation supporting 14 academic platforms including Web of Science, arXiv, PubMed, Google Scholar, ScienceDirect, Springer, Wiley, Scopus |

### academic-search-mcp-server

| Attribute | Description |
|------|------|
| **Source** | [afrise/academic-search-mcp-server](https://github.com/afrise/academic-search-mcp-server) |
| **Function** | Claude Desktop-integrated academic paper search MCP, accessing Semantic Scholar and Crossref |

---

## Agent-Mode Literature Review (Advanced)

A normal AI literature review is "open a chat box and ask question by question"; **Agent mode** is a different level:

The agent directly reads the local folder of papers and data, and autonomously plans and executes multi-step tasks:

```
Initial keywords → concept-family expansion → cross-database targeted retrieval (NBER Working Papers, Google Scholar)
     ↓
Combine with Zotero for collection & curation → paper classification, abstract extraction, theme summarisation
     ↓
Multi-stage cross-review and citation verification → identify the research gap → organise the review argument logic
     ↓
Output: structured review framework + reference list
```

> This kind of Agent-mode workflow is already in use at several business schools in China, validated by hundreds of faculty members and PhD students.

### Key Design Principles

- **Let the agent self-check**: multi-stage automated cross-review reduces hallucination and improves output quality.
- **Citation verification**: every citation is verified to exist via APIs, not invented by the AI.
- **Human-in-the-loop**: the researcher sets the goal, the agent does the execution, but the final judgement is yours.

---

## Practical Advice

1. **A real case**: a first-year economics master's student was equipped with literature skills. He fed 30 required-reading papers from his adviser to the AI to produce structured abstracts, then asked the AI to draft a review framework. What used to take a week took **three hours**. But he did something smarter — he didn't use the AI's framework directly; he rewrote it himself and used the AI's framework only as a "checklist".
2. **Zotero is your friend**: combining a literature-search skill with the Zotero MCP lets you import found papers straight into your Zotero library.
3. **Use Perplexity to surface hot topics, then Elicit for systematic search, then an Agent for structured review** — a three-tier funnel.

---

[← Previous chapter](01-research-topic-and-design.md) | [Next chapter: 03 - Paper Reading and Decomposition →](03-paper-reading-and-decomposition.md)