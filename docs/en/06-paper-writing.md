# 06 - Paper Writing

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  CoPaper.AI's writing sub-agent (writing agent) receives the analysis results
  from the statistical-modelling sub-agent and automatically generates
  publication-style results descriptions and table notes. The output conventions
  in the methodology skills ensure that every step's results are emitted via
  save_table() and save_figure(), and the writing sub-agent references them
  directly.
-->

> **Paper writing is not "describe your results once" — it is "convince the reviewer with clear logic."** AI can help you scaffold the structure, write the first draft, and check logic, but the positioning of the research contribution and the persuasiveness of the argument are still yours to control.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the "Skills list" below gives per-method details (with selected upstream links) and complements this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [⭐ `50` AER-skills](../../skills/50-brycewang-aer-skills/) | Top-5 economics submission stack: identification → robustness → R&R | Organise intro / identification / results to top-journal structure |
| [`06` stats-paper-writing](../../skills/06-fuhaoda-stats-paper-writing/) | End-to-end LaTeX statistics-paper writing | Directly produce a LaTeX manuscript skeleton |
| [`56` econ-writing-skill](../../skills/56-hanlulong-econ-writing-skill/) | Synthesises 50+ top guides on economics writing | Align sentence- and paragraph-level conventions with economics norms |
| [`35` academic-writing-skills](../../skills/35-bahayonghang-academic-writing-skills/) | Scenario-oriented academic writing | Draft each section in the target journal's style |
| [`27` my_claude_skills](../../skills/27-dariia-m-my_claude_skills/) | Guide for writing economics abstracts | Polish the abstract and the one-sentence contribution |
| [`01` academic-paper-skills](../../skills/01-lishix520-academic-paper-skills/) | Outline → manuscript + 7-dimension reviewer simulation | Run a reviewer rehearsal before finalising the draft |

---

## Skills List

### academic-writing (Full Academic Writing Pipeline)

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | Covers the full paper-writing pipeline: topic ideation, literature-review writing, research-method description, paper-structure organisation |
| **Highlight** | Follows strict academic writing conventions; never writes the three-paragraph "first, second, finally" style |
| **Install** | `clawhub install academic-writing` |

### composer (Systematic Paper Writing)

| Attribute | Description |
|------|------|
| **Source** | [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) |
| **Workflow** | Phase 1: Foundations → style guide + section planning<br>Phase 2: Systematic writing → drafts with quality checks<br>Phase 3: Polishing → final evaluation + submission prep |
| **Highlight** | 3 quality-check gates ensuring each phase output meets standards |

### ml-paper-writing

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | From template to citation verification to draft refinement |
| **Best for** | ML/AI papers, but the writing logic (IMRAD structure) is equally useful for social-science papers |

### 20-ml-paper-writing

| Attribute | Description |
|------|------|
| **Source** | [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) |
| **Stars** | 3,637 |
| **Function** | Top-conference paper drafting, citation verification, LaTeX templates |
| **Install** | `npx playbooks add skill orchestra-research/ai-research-skills --skill 20-ml-paper-writing` |

### research-paper-writer (Conference Paper)

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | Biased toward IEEE/ACM formats; well-suited for international conferences |
| **Highlight** | Builds a standard structure, ensuring abstract, introduction, method, experiments, and conclusion are all properly formatted |
| **Install** | `clawhub install research-paper-writer` |

### scientific-writing

| Attribute | Description |
|------|------|
| **Source** | [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) |
| **Stars** | 8,799 |
| **Function** | Deep research + academic writing; a core skill |
| **Install** | `npx skills add https://github.com/K-Dense-AI/claude-scientific-skills --skill scientific-writing` |

### claude-scientific-writer

| Attribute | Description |
|------|------|
| **Source** | [K-Dense-AI/claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) |
| **Stars** | 794 |
| **Function** | 19+ paper-writing skills, IMRAD structure, reporting standards (CONSORT/STROBE/PRISMA), real-time literature search |
| **Highlight** | Supports APA / AMA / Vancouver citation formats, mixed-methods integration, grant proposals (NSF/NIH) |

### methods-section-writing

| Attribute | Description |
|------|------|
| **Source** | [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) |
| **Function** | Specialised in generating the methods section of the paper, ensuring technical-detail accuracy |

### academic-research-skills (Complete Paper Pipeline)

| Attribute | Description |
|------|------|
| **Source** | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) |
| **Stars** | ~1,790 |
| **Function** | research → write → review → revise → finalize complete pipeline |
| **Highlight** | Style calibration (learns your writing style), citation-statistic verification, hallucination-pattern detection (GPTZero × NeurIPS 2025), Socratic-guidance mode |

### game-theory-paper-writer

| Attribute | Description |
|------|------|
| **Source** | [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) |
| **Function** | Game-theory paper generation, topic modelling, equilibrium analysis, paper polishing — supports the full pipeline from topic to final draft |
| **Highlight** | Includes a model-toolkit (game-model classification and selection), paper-writing (standard structure), and revision-and-review (reviewer response) |
| **Install** | `cp -R skills/65-game-theory-paper-writer ~/.codex/skills/` |

---

## Writing Points for Each Paper Section

### Introduction

The introduction is the most important part of the paper — the reviewer's first impression forms here. Keith Head's introduction formula is the classical framework:

1. **Hook**: why is this question important?
2. **Question**: what is your research question?
3. **Antecedents**: what have others done?
4. **Value-added**: what is your contribution?
5. **Roadmap**: preview of the paper's structure

> The `introduction-writer` four-agent system operates on this formula; see [07 - Revision and Polish](07-revision-and-polish.md).

### Empirical-Results Description

A good results description should:
- State direction and significance first, then give numbers
- Economic significance matters more than statistical significance ("a one-SD increase in X raises Y by 3.2%" is more persuasive than "the coefficient is significant at the 1% level")
- Tables and text complement each other; do not repeat

### Conclusion

- Do not introduce new information
- Discuss limitations honestly
- Policy implications must be justified

---

## Practical Advice

1. **Build the skeleton before filling it in**: use `strategist` to plan the structure → use `composer` to write chapter by chapter → use the revision skills to polish. Don't write straight through from start to finish.
2. **Focus on one section at a time**: `academic-writing-refiner` lets you polish a single section in isolation, which is more effective than feeding the whole paper at once.
3. **Check for AI style**: reviewers are increasingly sensitive to AI-generated text. Using skills to scaffold is fine, but the final prose must be rewritten in your own voice.

---

[← Previous chapter](05-statistical-analysis-and-causal-inference.md) | [Next chapter: 07 - Revision and Polish →](07-revision-and-polish.md)