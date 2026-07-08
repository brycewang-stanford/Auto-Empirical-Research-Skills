# 03 - Paper Reading and Decomposition

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  Reading papers should not only mean "I've read it" — it should mean
  "I've dissected it." CoPaper.AI supports a structured five-question
  framework to decompose top-journal papers and transfer the methodology
  to your own research setting.
-->

> **You cannot read every paper you find in depth.** You need to quickly judge which are worth a deep read and which you can skim. More importantly, after reading a paper you should be able to extract its methodology precisely and transfer it to your own work.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the "Skills list" below gives per-method details (with selected upstream links) and complements this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [`21` AI-research-feedback](../../skills/21-claesbackman-AI-research-feedback/) | 2-agent deep review of economics papers | Decompose a top-journal paper's identification strategy; detect over-claimed causal claims |
| [`24` academic-research-skills](../../skills/24-Imbad0202-academic-research-skills/) | 5-reviewer multi-perspective paper review | Multi-angle decomposition of a target paper's contribution and weaknesses |
| [`33` claude-scholar](../../skills/33-Galaxy-Dawn-claude-scholar/) | Full research lifecycle, with self-review and citation check | Verify citations during decomposition and review methodological credibility |
| [`28` paper-replicate-agent](../../skills/28-maxwell2732-paper-replicate-agent-demo/) | Paper-replication agent demo | Push "understand" all the way to "replicate" and verify methodological details |
| [`02` research-skills](../../skills/02-luwill-research-skills/) | Reviews, proposals, paper-to-slides | Organise decomposition conclusions into shareable notes/talk slides |
| [`62` citation-checker](../../skills/62-PHY041-claude-skill-citation-checker/) | Verify citations against CrossRef / S2 / OpenAlex | Confirm that citations really exist while decomposing |

---

## Skills List

### paper-summarize-academic

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | **Automatically chooses different summarisation strategies** based on paper type |
| **Strategies** | Methodology papers → focus on methodological innovation and applicability<br>Dataset papers → focus on data coverage and acquisition<br>Empirical papers → focus on identification strategy and core findings<br>Survey papers → focus on the taxonomy and research gaps |
| **Install** | `clawhub install paper-summarize-academic` |

### empirical-paper-analysis-skill

| Attribute | Description |
|------|------|
| **Source** | ClawHub (clawhub.com) |
| **Function** | **Designed for empirical papers in economics and law-and-economics**; systematically evaluates the research question, empirical challenges, identification strategy, core findings, and academic contribution |
| **Usage** | Feed it an AER empirical paper; ten minutes later it tells you "what's good, what's weak, whether the identification strategy holds up" |
| **Value** | For literature reviews, you don't need to read every paper in depth, but you need to know each one's identification strategy and main conclusions. This skill compresses two hours to ten minutes |
| **Install** | `clawhub install empirical-paper-analysis-skill` |

### Structured Five-Question Framework (Top-Journal Decomposition and Transfer)

| Attribute | Description |
|------|------|
| **Source** | Open-source practices from the academic community |
| **Framework** | 1. What is the research question?<br>2. What is the identification strategy?<br>3. What is the core estimator?<br>4. What is the robustness-check logic?<br>5. What are the contributions and limitations? |
| **Core value** | Not only does it decompose papers, but more importantly it **transfers** them: the AI agent systematically extracts the research design, causal-identification logic, variable-construction logic, and robustness-check strategies from top-journal papers; then you feed in your own research question and data description, and the agent automatically completes the "learn-then-transfer" process |
| **Output** | Five-question analysis framework + transferable-element list + transfer plan to your own research + implementation plan |

### AI-research-feedback (Economics Paper Pre-Review)

| Attribute | Description |
|------|------|
| **Source** | [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) |
| **Function** | 2-agent deep review of economics papers |
| **Checks** | Contribution assessment, identification-strategy assessment, **over-claimed causal claim detection**, unsupported-claim identification |
| **Journal support** | AER, QJE, JPE, Econometrica, REStud + finance journals (JF, JFE, RFS) |
| **Highlight** | Built by an economics researcher (Claes Backman); designed specifically for economics papers |

### paper-self-review

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | Simulates a reviewer's perspective to surface problems |
| **Scenario** | Run a self-review before submission; anticipate reviewer concerns |

### citation-verification

| Attribute | Description |
|------|------|
| **Source** | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) |
| **Function** | Automatically checks the accuracy of every citation in the paper, preventing AI-invented false references |

---

## The Full Meaning of "Transfer"

> "Transfer" goes far beyond understanding a paper — it means letting an AI agent systematically extract reusable research designs from top-journal papers and translate them into concrete plans tailored to your own research setting.

**Transfer flow**:

```
Input: a target top-journal paper + your research question + your data description
  ↓
Agent decomposes the target paper: identification strategy, variable-construction logic, endogeneity-handling plan, robustness design
  ↓
Evaluate transferability: which elements can be transferred directly? which need adjustment?
  ↓
Generate a transfer plan: concrete implementation plan for your research setting
  ↓
Output: transfer report (with identification-strategy adaptation, analysis-step planning, expected-challenges checklist)
```

---

## Practical Advice

1. **Divide labour between deep and broad reads**: use `paper-summarize-academic` to skim every paper you find and tag those worth a deep read; then use `empirical-paper-analysis-skill` or the five-question framework to deeply decompose the core papers.
2. **Build your own "methodology cards"**: each time you decompose a top-journal paper, log the transferable design elements. After 10–20 papers you'll have a personal "research-design toolbox."
3. **Over-claimed causal claims are taboo**: use `AI-research-feedback` to check your own paper for over-claimed causal claims — this is the easiest thing for a reviewer to pounce on.

---

[← Previous chapter](02-literature-search-and-review.md) | [Next chapter: 04 - Data Acquisition and Cleaning →](04-data-acquisition-and-cleaning.md)