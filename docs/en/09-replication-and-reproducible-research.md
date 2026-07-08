# 09 - Replication and Reproducible Research

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  Reproducibility is the cornerstone of empirical research. CoPaper.AI's
  methodology skills are designed from the ground up with standardised
  outputs (save_table / save_figure); every step's results are traceable and
  reproducible. Combined with Git version control, your entire research
  process has a complete audit trail.
-->

> **If your research cannot be replicated, it is not science.** The good news is that AI agents make "reproducible research" go from an ideal to reality — a skill itself is an executable methods-document.

---

## Case Study: Replicating an AER Paper in 10 Minutes

This is not a hypothetical — it is a real operation recorded by the Chinese community.

**Paper**: "Canal Closure and Social Unrest: Evidence from Qing China" (*Canal Closure and Social Unrest: Evidence from Qing China*), published in the *American Economic Review*.

**Operation**: using Claude Code's replication skill, with a single instruction "help me replicate the results of this paper," a complete replication report is generated automatically in **10 minutes**.

### Replication Details

| Dimension | Description |
|------|------|
| **Design** | DID, 6 provinces, 536 counties, 1650–1911 panel, the 1826 canal closure as the treatment event |
| **Translation** | Original Stata `.do` files automatically translated into Python `pyfixest.feols()` |
| **Coverage** | Grain-transport trend (Figure 2), parallel trends (Table 2), baseline DID (Table 3), event study (Figure 4), North–South heterogeneity (Table 5) |

### Key Result Comparison

| Chart/Table | Status | Key number |
|------|------|---------|
| Figure 2 (grain transport) | Fully replicated | ~15% drop after 1826 |
| Table 2 (parallel trends) | Fully replicated | Pre-treatment trend coefficient 0.0003, p=0.59, passes test |
| Table 3 (baseline DID) | Core consistent | Coefficients 0.042–0.061; equations 1–3 significant |
| Figure 4 (event study) | Basically replicated | Post-treatment +20-period coefficient 0.0613** |
| Table 5 (North-South heterogeneity) | Fully replicated | Northern triple-interaction coefficient 0.10–0.12*** |

**Overall replication rating**: B (core coefficient signs and significance are highly consistent with the original).

> Reproducing an AER paper used to take days. Now it's one sentence and 10 minutes. **When you can automate the hardest task — "replicating a top-journal paper" — running a robustness check or trying a different identification strategy is trivial.**

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the per-tool details below complement this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [`28` paper-replicate-agent](../../skills/28-maxwell2732-paper-replicate-agent-demo/) | Paper-replication agent demo | Push from "understanding" to a runnable replication package |
| [`54` open-science-skills](../../skills/54-scdenney-open-science-skills/) | Citation consistency, DOI, and argument-support audit | Open-science compliance audit on the replication package |
| [`29` project20XXy](../../skills/29-quarcs-lab-project20XXy/) | Reproducible manuscript + notebook project skeleton | One-click reproducible project scaffolding |
| [`41` sewage-econometrics-check](../../skills/41-sticerd-eee-sewage-econometrics-check/) | 10-item replication-package audit checklist | Pre-submission self-check for STICERD-style replication review |
| [`12` claude-code-my-workflow](../../skills/12-pedrohcgs-claude-code-my-workflow/) | Commit → PR → merge research workflow (Emory) | Manage the whole replication pipeline with version control |
| [`60` superpapers](../../skills/60-regisely-superpapers/) | Comprehensive empirical-research support bundle | End-to-end replication toolbox |

---

## Skills and Tools

### Replication Skill (Automated Replication)

| Attribute | Description |
|------|------|
| **Source** | Open-source community practice |
| **Function** | Input: paper PDF + replication package → auto-generated replication report |
| **Capability** | Stata → Python code translation; table replication; figure replication; result comparison |

### ARIS (Overnight Autonomous Research)

| Attribute | Description |
|------|------|
| **Source** | [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) |
| **Function** | Run ML experiments and paper revisions overnight, autonomously |
| **Highlight** | Cross-model review loop (Claude + external LLM as critic), zero dependencies, agent-agnostic (works with any LLM agent) |
| **Best for** | Time-consuming tasks such as Monte-Carlo simulations and large-scale robustness checks |

### AI-Researcher (Fully Autonomous Research Pipeline)

| Attribute | Description |
|------|------|
| **Source** | [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher) (HKU, NeurIPS 2025 Spotlight) |
| **Function** | Fully autonomous: literature review → hypothesis generation → algorithm implementation → paper writing |

### Agent Laboratory (End-to-End Autonomous Research)

| Attribute | Description |
|------|------|
| **Source** | [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) |
| **Function** | Three-stage autonomous research: literature review → experiments → report writing; integrates arXiv / Hugging Face / Python / LaTeX |
| **Highlight** | Research cost reduced by 84%; supports the AgentRxiv collaborative preprint server |

### AI-Scientist-v2 (Fully Automatic Scientific Discovery)

| Attribute | Description |
|------|------|
| **Source** | [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) |
| **Function** | End-to-end autonomous scientific-discovery system: auto-generates hypotheses → runs experiments → analyses data → writes papers, using agent-tree search |
| **Achievement** | First fully AI-generated paper to be accepted at peer review |

### gpt-researcher (Autonomous Deep Research)

| Attribute | Description |
|------|------|
| **Source** | [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) |
| **Function** | Autonomous deep-research agent; supports any LLM provider |

### claude-code-my-workflow (Academic Workflow Template)

| Attribute | Description |
|------|------|
| **Source** | [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) |
| **Function** | Academic LaTeX/Beamer + R template: multi-agent review, quality gates, adversarial QA, replication protocol |
| **Highlight** | Originates in Emory's Econ 730 Causal Panel Data course; adopted by 15+ research groups |

### clo-author (Social-Science Paper Collaboration Template)

| Attribute | Description |
|------|------|
| **Source** | [hugosantanna/clo-author](https://github.com/hugosantanna/clo-author) |
| **Function** | Adapts Pedro Sant'Anna's workflow from lecture materials to empirical-research paper publication; extends to the full social-science domain |

---

## Best Practices for Reproducible Research

### Project Structure

```
project/
├── data/
│   ├── raw/          # Raw data (never modified)
│   └── processed/    # Cleaned data
├── code/
│   ├── 01-clean.py   # Data cleaning
│   ├── 02-analysis.py # Main analysis
│   └── 03-robustness.py # Robustness
├── output/
│   ├── tables/       # Regression tables
│   └── figures/      # Figures
├── paper/
│   └── draft.tex     # Paper draft
├── SKILL.md          # Agent skills configuration
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

### Five Principles

1. **Version control**: use Git for code and data-processing pipelines
2. **Lock the environment**: Python uses `requirements.txt`, R uses `renv`, Stata uses the `version` command
3. **Data is immutable**: raw data lives in `data/raw/` and is never modified
4. **Code is documentation**: every script opens with a note about inputs, outputs, and purpose
5. **One-click reproduction**: provide a `make` or shell script that runs the entire analysis in one command

---

## Practical Advice

1. **Git is not optional**: you don't need to be a Git expert, but you need to let the agent use Git. Git provides a safety net and version history so you can try and roll back safely.
2. **Replication packages are submission standard**: more and more journals require a replication package. Organising files according to the structure above from the start of the project saves a lot of trouble at submission.
3. **A skill itself is a reproduction document**: a good SKILL.md is not only an operating manual for the AI; it is also a methods document for humans.

---

[← Previous chapter](08-citation-management-and-typesetting.md) | [Next chapter: 10 - Rebuttal and Academic Defence →](10-rebuttal-and-academic-defense.md)