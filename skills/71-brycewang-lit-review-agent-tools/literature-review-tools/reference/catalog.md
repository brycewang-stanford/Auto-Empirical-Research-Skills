# Full Catalog — AI Literature Review Tools

70+ open-source projects, organized by use case. ⭐ = editor's pick.
Star counts are periodic GitHub-API snapshots (approximate). Source of truth:
<https://github.com/brycewang-stanford/lit-review-agent-tools>

---

## 🌟 All-in-one Research Agents & Skills

End-to-end `research → write → review → revise` — mostly Claude Code / Codex skills.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | ~39.5k | Most popular in the space. Claude Code skill suite, 10-stage pipeline (research→write→review→revise→finalize) with citation/claim "integrity gates," cross-checked vs. Semantic Scholar + OpenAlex + Crossref. "AI is your copilot, not the pilot." `/plugin install academic-research-skills` |
| [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | ~7.1k | Codex-native sibling, human-in-the-loop |
| [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | ~5.5k | ML/CV/NLP paper-writing pack; Codex / Claude Code / Gemini |
| [claude-skills](https://github.com/alirezarezvani/claude-skills) | ~23.2k | Large skill collection incl. litreview / grants / deep-research stack |
| [academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | ~1.1k | Strategist (planning) + Composer (writing) with quality checkpoints |
| [dr-claw](https://github.com/OpenLAIR/dr-claw) | ~1.0k | "Research IDE" with multiple AI-assistant personas |
| [ScienceClaw](https://github.com/beita6969/ScienceClaw) | ~0.9k | Self-evolving research colleague, 285 skills, "zero hallucination" |
| [qinyan-academic-skills](https://github.com/LeonChaoX/qinyan-academic-skills) | ~0.7k | Multilingual, 182 installable agent skills across disciplines |
| [agent-research-skills](https://github.com/lingzhi227/agent-research-skills) | ~0.2k | Claude Code skills for systematic review + citation-validation scripts |
| [medsci-skills](https://github.com/Aperivue/medsci-skills) | ~0.2k | Medical research: search, reporting-guideline/citation checks, stats, figures, submission |

## 🔎 Deep Research & Auto-Survey Generation

Input a topic → auto-search and produce a cited survey / report / related-work section.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [STORM](https://github.com/stanford-oval/storm) | ~30.3k | Stanford OVAL. Retrieval-based two-stage (pre-writing + writing), Wikipedia-style long-form with citations; Co-STORM is the multi-agent conversational variant |
| ⭐ [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | ~28.6k | Autonomous research agent; deep dive on any topic → cited report. General-purpose, not academic-only |
| [deep-research](https://github.com/dzhng/deep-research) | ~19.4k | Minimal iterative deep-research agent (search + scrape + LLM refine), short/hackable |
| [open_deep_research](https://github.com/langchain-ai/open_deep_research) | ~12.4k | LangChain's official open deep-research reference |
| [local-deep-research](https://github.com/LearningCircuit/local-deep-research) | ~8.8k | Local/privacy-first; 10+ sources incl. arXiv/PubMed; fully local LLM capable |
| [open-deep-research](https://github.com/nickscamara/open-deep-research) | ~6.3k | Firecrawl-based open deep-research clone reasoning over web data |
| [SurveyX](https://github.com/IAAR-Shanghai/SurveyX) | ~1.0k | Auto-generate an academic survey paper from a topic |
| [LitLLM](https://github.com/LitLLM/LitLLM) | ~44 | Scientific lit-review toolkit; RAG + prompting for fast related-work (TMLR 2025) |
| [opendraft](https://github.com/federicodeponte/opendraft) | ~0.3k | Free open-source AI paper writing, 19 collaborating agents |
| [AutoSurveyGPT](https://github.com/a554b554/AutoSurveyGPT) | ~0.2k | GPT retrieves + ranks from Google Scholar, auto-generates a review |

## 🧪 Autonomous Science: Idea → Paper

End-to-end automated discovery: lit review + hypotheses + experiments + writing + self-review.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | ~14.3k | Sakana AI, end-to-end automated discovery (lit→experiment→write→review). Also [v2](https://github.com/SakanaAI/AI-Scientist-v2) (~6.9k, agentic tree search, workshop-grade) |
| [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | ~13.9k | Self-evolving autonomous research: idea → submittable LaTeX (OpenAlex/S2/arXiv + sandboxed experiments + multi-agent review) |
| [Agent-Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | ~5.8k | End-to-end: lit review → experiments → report writing |
| [SciAgentsDiscovery](https://github.com/lamm-mit/SciAgentsDiscovery) | ~0.6k | Multi-agent (ontologist/scientist/critic) hypothesis generation & discovery |
| [Zochi](https://github.com/IntologyAI/Zochi) | ~0.3k | "Artificial scientist," discovery → peer-review acceptance end-to-end |
| [DeepInnovator](https://github.com/HKUDS/DeepInnovator) | ~0.3k | Autonomously generates ideas, questions, testable hypotheses, experiment designs |

## 📚 Literature Q&A & RAG

Citation-backed Q&A and extraction over a corpus of PDFs / papers.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [paper-qa](https://github.com/Future-House/paper-qa) | ~8.9k | FutureHouse. High-accuracy scientific RAG, answers **always cited**; PaperQA2 claims superhuman lit retrieval |
| [paperai](https://github.com/neuml/paperai) | ~1.8k | Semantic search + Q&A for medical & research papers |
| [openpaper](https://github.com/khoj-ai/openpaper) | ~0.4k | Research-library workbench: read/annotate + citation-traceable AI review assistant |

## 🧮 Systematic Review & Screening

Rigorous evidence-based / PRISMA reviews; efficient screening of thousands of abstracts.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [ASReview](https://github.com/asreview/asreview) | ~1.0k | Active-learning screening; interactively ranks papers, big time savings. Mature in academia |
| [LatteReview](https://github.com/PouriaRouzrokh/LatteReview) | ~0.1k | Low-code Python; AI agents automate screening (OpenAI/Gemini/Claude/Ollama) |
| [prismAId](https://github.com/Open-and-Sustainable/prismAId) | ~24 | GenAI protocol-driven systematic review, no-code, reproducible screening + extraction |
| [prisma-review-tool](https://github.com/Black-Lights/prisma-review-tool) | niche | Full PRISMA 2020, AI-assisted screening via MCP (arXiv/OpenAlex/S2, no API key) |

## 🔌 MCP Servers

Wire literature capabilities into Claude / Cursor / Cline and other MCP clients.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [zotero-mcp](https://github.com/54yyyu/zotero-mcp) | ~4.4k | Zotero library (local + Web API) → AI: semantic search, PDF fulltext, citation analysis. Most popular Zotero MCP |
| ⭐ [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | ~3.0k | Search/analyze arXiv, download + PDF→Markdown for LLMs; ships `.mcpb` package |
| [paper-search-mcp](https://github.com/openags/paper-search-mcp) | ~2.3k | Search/download across 20+ sources (arXiv, PubMed, bioRxiv, S2, OpenAlex, Crossref, CORE…) |
| [PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) | ~0.1k | Search/access/analyze PubMed articles (metadata + deep analysis) |
| [alex-mcp](https://github.com/drAbreu/alex-mcp) | ~50 | OpenAlex MCP, author disambiguation + institution/works queries |
| [openalex-research-mcp](https://github.com/oksure/openalex-research-mcp) | ~37 | OpenAlex (240M+ works): citation analysis, trends, collaboration networks |

## 🗂️ Reference Management & Zotero / Obsidian Integration

Embed AI into your existing reference-manager / note-taking workflow.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) | ~7.3k | GPT inside Zotero; chat directly with your library |
| [papersgpt-for-zotero](https://github.com/papersgpt/papersgpt-for-zotero) | ~2.6k | Zotero AI + MCP plugin; chat/batch-process PDFs across 30+ LLMs |
| [ai-research-assistant](https://github.com/lifan0127/ai-research-assistant) | ~1.7k | "Aria" LLM research assistant inside Zotero |
| [paper-note-filler](https://github.com/chauff/paper-note-filler) | ~47 | Obsidian plugin; auto-create notes from arXiv / ACL Anthology / Semantic Scholar |

## 📄 PDF → Structured Data Extraction

The invisible infrastructure: turn PDFs into clean, structured Markdown/JSON for LLMs.

| Project | Stars | Notes |
|---|---|---|
| ⭐ [MinerU](https://github.com/opendatalab/MinerU) | ~75.7k | High-accuracy PDF/Office → LLM-ready Markdown/JSON (VLM+OCR, 100+ langs, formulas/tables) |
| [docling](https://github.com/docling-project/docling) | ~63.8k | IBM document parser; prep PDFs/docs for GenAI/RAG |
| [marker](https://github.com/datalab-to/marker) | ~37.8k | Fast PDF/doc → clean Markdown/JSON, research-doc friendly |
| [PDFMathTranslate](https://github.com/Byaidu/PDFMathTranslate) | ~35.8k | Layout-preserving scientific PDF translation (formulas/figures intact) |
| [grobid](https://github.com/grobidOrg/grobid) | ~5.0k | Extract structured TEI/XML from scholarly PDFs (metadata, references, sections) |
| [paperetl](https://github.com/neuml/paperetl) | ~0.7k | ETL pipeline for medical & research papers → structured storage |
| [scipdf_parser](https://github.com/titipata/scipdf_parser) | ~0.5k | Python parser for scientific PDFs (text + figures, GROBID-based) |

## 🕸️ Citation Graphs & API Clients

Citation-network analysis, or scripting academic databases directly.

| Project | Stars | Notes |
|---|---|---|
| [scholarly](https://github.com/scholarly-python-package/scholarly) | ~1.9k | Pythonic Google Scholar author/paper search |
| [semanticscholar](https://github.com/danielnsilva/semanticscholar) | ~0.5k | Unofficial Python client for the Semantic Scholar API |
| [pyalex](https://github.com/J535D165/pyalex) | ~0.4k | Lightweight OpenAlex API Python interface |
| [ArxivDigest](https://github.com/AutoLLM/ArxivDigest) | ~0.5k | Personalized daily arXiv digest; GPT relevance scoring + email |
| [citegraph](https://github.com/Citegraph/citegraph) | ~22 | Open visualization of 5M+ papers/citation network (CS literature) |

## ✍️ Paper Writing & Peer-Review Assistants

Draft, polish, and run an "AI pre-review" before submission.

| Project | Stars | Notes |
|---|---|---|
| [lmms-lab-writer](https://github.com/EvolvingLMMs-Lab/lmms-lab-writer) | ~0.3k | Local-first agentic LaTeX writing for AI-assisted academic writing |
| [academic-writing-agents](https://github.com/andrehuang/academic-writing-agents) | ~0.1k | Claude Code plugin: 10+ expert agents for review, research, drafting, polishing |
| [ai-peer-review](https://github.com/poldrack/ai-peer-review) | ~0.2k | Multi-LLM meta-review: independent reviews synthesized into a meta-review |
| [open_reviewer](https://github.com/maxidl/openreviewer) | ~14 | High-quality peer reviews for ML/AI conference papers; pre-submission feedback |
| [academic-research-plugin](https://github.com/JeanDiable/academic-research-plugin) | ~17 | Claude Code plugin: lit review, paper review, citation mgmt; searches arXiv/S2/DBLP, finds gaps |

## 📖 Awesome Lists

Community-maintained lists for the full landscape.

| List | Stars | Notes |
|---|---|---|
| [Awesome-LLM-Scientific-Discovery](https://github.com/HKUST-KnowComp/Awesome-LLM-Scientific-Discovery) | ~0.4k | EMNLP 2025 survey list: LLMs for scientific discovery |
| [Awesome-Auto-Research-Tools](https://github.com/handsome-rich/Awesome-Auto-Research-Tools) | ~1.1k | Automated lit search, paper reading, experiment mgmt, code gen |
| [awesome-ai-auto-research](https://github.com/worldbench/awesome-ai-auto-research) | ~0.4k | AI automated research survey |
| [LLM4SR](https://github.com/du-nlp-lab/LLM4SR) | ~0.1k | Papers & resources: LLMs for scientific research |
| [awesome-ai-research-tools](https://github.com/0x11c11e/awesome-ai-research-tools) | ~55 | AI research tools: lit review, reference mgmt, data analysis |
| [awesome-evidence-synthesis](https://github.com/evidencesynthesis-tools/awesome-evidence-synthesis) | ~19 | Open-source tools for systematic review, meta-analysis, evidence synthesis |

## 🏢 Commercial / Closed-Source (reference only)

Not open-source, but widely used — listed for comparison.

- **[Elicit](https://elicit.com)** — extract data from millions of papers, generate evidence tables
- **[Consensus](https://consensus.app)** — semantic search engine for research questions
- **[Scite](https://scite.ai)** — citation-context analysis (supporting / contrasting / mentioning)
- **[Undermind](https://undermind.ai)** · **[SciSpace](https://typeset.io)** — deep lit search & reading assistants
- **[Research Rabbit](https://researchrabbit.ai)** · **[Connected Papers](https://connectedpapers.com)** — citation-relationship visual exploration
