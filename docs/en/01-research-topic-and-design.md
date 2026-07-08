# 01 - Research Topic and Study Design

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  CoPaper.AI ships with 20 methodology skills covering the entire pipeline from
  topic ideation to research design. Enter your research direction and the AI
  will automatically map the literature gap, sharpen the research question, and
  design an identification strategy.
-->

> **Topic selection is the soul of a paper.** A good research question must satisfy three conditions: it has theoretical value, it is supported by data, and it admits a credible identification strategy. An AI agent cannot tell you "what the contribution of this paper is," but it can systematically scan the literature gap, evaluate research feasibility, and sketch an initial framework.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the "Skills list" below gives per-method details (with selected upstream links) and complements this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [`25` Diverga](../../skills/25-HosungYou-Diverga/) | Research-question refiner that combats "mode-collapse" homogeneous topic selection | Refine a fuzzy direction into a testable, differentiated research question |
| [`03` scientific-skills](../../skills/03-K-Dense-AI-claude-scientific-skills/) | Hypothesis generation + 28 scientific databases | Auto-generate testable hypotheses from the literature and check data availability |
| [`34` research-companion](../../skills/34-andrehuang-research-companion/) | Brainstorm, evaluate, and decide among research directions | Score and compare multiple directions to pick one |
| [`05` research-superpower](../../skills/05-kthorn-research-superpower/) | Systematic search, screening, and citation back-tracing | Use literature gaps to verify the novelty of a topic |
| [⭐ `50` AER-skills](../../skills/50-brycewang-aer-skills/) | Top-5 economics submission stack: identification → robustness → R&R | Anchor identification strategy and publishability from the topic stage |
| [`42` ARIS](../../skills/42-wanshuiyin-ARIS/) | Autonomous "research while sleeping" end-to-end agent (104 skills) | Run an end-to-end exploration to produce an initial research framework |

> Want the entire chain "topic → design → analysis → writing → submission" handed to a single orchestrator? See [⭐ `69` Paper-WorkFlow](../../skills/69-Paper-WorkFlow/) and [⭐ `00` StatsPAI](../../skills/00-Full-empirical-analysis-skill_StatsPAI/).

---

## Skills List

### research-ideation

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | 5W1H brainstorming → literature-gap analysis → research-direction synthesis |
| **Workflow** | 1. Divergent thinking from keywords<br>2. Scan existing literature to confirm the gap<br>3. Evaluate data availability and methodological feasibility<br>4. Output a structured set of research-direction suggestions |
| **Best for** | The early topic-selection stage; especially for researchers without a clear direction yet |

### research-proposal

| Attribute | Description |
|------|------|
| **Source** | [luwill/research-skills](https://github.com/luwill/research-skills) |
| **Stars** | 209 |
| **Function** | Generate a high-quality 2,000–4,000-word research proposal |
| **Workflow** | 1. Requirements gathering (topic, field, language, length)<br>2. Multi-source literature collection (WebSearch, Zotero, arXiv, PubMed)<br>3. Outline generation (user reviews)<br>4. Full writing (based on approved outline)<br>5. Markdown output + quality-check checklist |
| **Output** | At least 40 references and 3–5 figure suggestions |
| **Bilingual** | Supports Chinese and English |
| **Install** | `git clone https://github.com/luwill/research-skills.git && cp -r research-skills/research-proposal ~/.claude/skills/` |

### strategist (Paper Planning)

| Attribute | Description |
|------|------|
| **Source** | [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) |
| **Function** | Systematic paper-planning framework, including a 7-dimension reviewer simulation |
| **Workflow** | Phase 1: Platform analysis → target journal + style guide<br>Phase 2: Theoretical framework → literature + research-gap analysis (3–5 supporting citations)<br>Phase 3: Outline refinement → reviewer-style evaluation of the outline |
| **Highlight** | Simulates the reviewer perspective to surface problems early; well-suited for humanities, social science, and interdisciplinary research |

### hypothesis-generation

| Attribute | Description |
|------|------|
| **Source** | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) |
| **Stars** | 8,799 |
| **Function** | Auto-generate testable research hypotheses based on literature analysis |
| **Install** | `npx skills add https://github.com/K-Dense-AI/claude-scientific-skills --skill hypothesis-generation` |

### research-grants

| Attribute | Description |
|------|------|
| **Source** | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) |
| **Function** | Grant/research-proposal writing; supports NSF, NIH, and other formats |
| **Install** | `npx skills add https://github.com/K-Dense-AI/claude-scientific-skills --skill research-grants` |

### 6-agent Grant Review Panel

| Attribute | Description |
|------|------|
| **Source** | [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) |
| **Function** | 6 AI agents simulate a grant-review panel, evaluating your proposal from different angles |
| **Highlight** | Designed specifically for economics research; assesses the credibility of causal-inference strategies |

### co-researcher

| Attribute | Description |
|------|------|
| **Source** | [poemswe/co-researcher](https://github.com/poemswe/co-researcher) |
| **Function** | A professional research suite: ideation, methodological design, systematic-review guidance |
| **Highlight** | Cross-platform compatibility with Claude Code, Gemini CLI, and Codex |

### academic-research-plugin

| Attribute | Description |
|------|------|
| **Source** | [JeanDiable/academic-research-plugin](https://github.com/JeanDiable/academic-research-plugin) |
| **Function** | Literature search, paper review, citation management; searches arXiv/Semantic Scholar/DBLP, identifies research gaps |
| **Highlight** | Cross-domain exploration and proposes 2–3 innovative directions |

### design-of-experiments

| Attribute | Description |
|------|------|
| **Source** | VoltAgent Skills / ClawHub |
| **Function** | Plan rigorous experiments using factorial designs, response-surface methods, Taguchi methods, and statistical power analysis |
| **Best for** | Experimental economics, A/B testing, randomized controlled trial design |

### ai-for-grant-writing

| Attribute | Description |
|------|------|
| **Source** | [eseckel/ai-for-grant-writing](https://github.com/eseckel/ai-for-grant-writing) |
| **Function** | Curated resource list for LLM-assisted grant applications, covering NSF/NIH/SBIR and more |
| **Highlight** | Provides prompt templates for proposal-title generation, challenge identification, and benchmark-against-reviewer-criteria |

### elicitation (Psychological Profiling)

| Attribute | Description |
|------|------|
| **Source** | Community curation (awesome-claude-skills) |
| **Function** | Perform psychological profiling through natural dialogue using narrative-identity and motivational-interview techniques |
| **Best for** | Interview design in user-research and behavioral-economics studies |

### crowdcast (Multi-Agent Social Simulation)

| Attribute | Description |
|------|------|
| **Source** | Community curation (awesome-claude-skills) |
| **Function** | Generate dozens of AI agents that debate, post, and interact on a simulated platform, producing a forecast report |
| **Best for** | Simulating sociological experiments, public-opinion dynamics, and collective-behavior forecasts |

---

## CoPaper.AI Solution

[CoPaper.AI](https://copaper.ai)'s skill suite supports you from the research-design stage onward:

- Each methodology skill ships with **precondition checks** — before you start any analysis, the AI verifies that your data structure, variable definitions, and identification strategy meet the method's requirements.
- Skills whose `target_agent = modeling` are automatically routed to a statistical-modeling sub-agent, ensuring continuity between design and execution.
- Custom skills are supported: you can write your own research-design framework as a `.md` file and upload it; it gets the same routing and injection support as the built-in skills.

---

## Practical Advice

1. **Run `research-proposal` first**: even if you already have a topic, letting the AI generate a complete proposal helps you discover overlooked literature and logical blind spots.
2. **Use `strategist` for reviewer rehearsal**: before you start writing, run a 7-dimension reviewer simulation on your design — it is far more efficient than revising a finished draft.
3. **Don't agonize over tool choice**: Codex's `AGENTS.md` and Claude Code's `CLAUDE.md` are highly analogous; skills are portable across tools.

---

[Next chapter: 02 - Literature Search and Review →](02-literature-search-and-review.md)