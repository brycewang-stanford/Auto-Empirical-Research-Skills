---
name: medical-imaging-review
description: >
  Write comprehensive literature reviews for medical imaging AI research.
  Use when writing survey papers, systematic reviews, or literature analyses
  on topics like segmentation, detection, classification in CT, MRI, X-ray,
  ultrasound, or pathology imaging. Triggers on requests for "review paper",
  "survey", "literature review", "综述", "systematic review", or mentions of
  writing academic reviews on deep learning for medical imaging.
metadata:
  author: user
  version: "2.0.0"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - Task
  - mcp__arxiv-mcp-server__search_papers
  - mcp__arxiv-mcp-server__download_paper
  - mcp__arxiv-mcp-server__read_paper
  - mcp__pubmed-mcp-server__pubmed_search_articles
  - mcp__zotero__zotero_search_items
  - mcp__zotero__zotero_get_item_fulltext
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║  本文件为开源 Skill 原始文档，收录仅供学习与研究参考        ║
  ║  CoPaper.AI 收集整理 | https://copaper.ai                  ║
  ╚══════════════════════════════════════════════════════════════╝

  来源仓库: https://github.com/luwill/research-skills
  项目名称: research-skills
  开源协议: MIT License
  收录日期: 2026-04-02

  声明: 本文件版权归原作者所有。此处收录旨在为社会科学实证研究者
  提供 AI Agent Skills 的集中参考。如有侵权，请联系删除。
-->

# Medical Imaging AI Literature Review Skill

Write comprehensive literature reviews following a systematic 7-phase workflow.

## Quick Start

1. **Initialize project** with three core files:
   - `CLAUDE.md` - Writing guidelines and terminology
   - `IMPLEMENTATION_PLAN.md` - Staged execution plan
   - `manuscript_draft.md` - Main manuscript

2. **Follow the 7-phase workflow** (see [references/WORKFLOW.md](references/WORKFLOW.md))

3. **Use domain-specific templates** (see [references/DOMAINS.md](references/DOMAINS.md))

---

## Core Principles

### Writing Style
- **Hedging language**: "may", "suggests", "appears to", "has shown promising results"
- **Avoid absolutes**: Never say "X is the best method"
- **Citation support**: Every claim needs reference
- **Limitations**: Each method section needs a Limitations paragraph

### Required Elements
- **Key Points box** (3-5 bullets) after title
- **Comparison table** for each major section
- **Performance metrics**: Dice (0.XXX), HD95 (X.XX mm)
- **Figure placeholders** with detailed captions
- **References**: 80-120 typical, organized by topic

### Paragraph Structure
```
Topic sentence (main claim)
  → Supporting evidence (citations + data)
  → Analysis (critical evaluation)
  → Transition to next paragraph
```

---

## Literature Sources

Use multi-source strategy for comprehensive coverage:

| Source | Best For | Tools |
|--------|----------|-------|
| ArXiv | Latest DL methods, preprints | `search_papers`, `read_paper` |
| PubMed | Clinical validation, peer-reviewed | `pubmed_search_articles` |
| Zotero | Existing library, organized refs | `zotero_search_items` |

For MCP configuration details, see [references/MCP_SETUP.md](references/MCP_SETUP.md).

---

## Standard Review Structure

```markdown
# [Title]: State of the Art and Future Directions

## Key Points
- [3-5 bullets summarizing main findings]

## Abstract

## 1. Introduction
### 1.1 Clinical Background
### 1.2 Technical Challenges
### 1.3 Scope and Contributions

## 2. Datasets and Evaluation Metrics
### 2.1 Public Datasets (Table 1)
### 2.2 Evaluation Metrics

## 3. Deep Learning Methods
### 3.1 [Category 1]
### 3.2 [Category 2]
(Table 2: Method Comparison)

## 4. Downstream Applications

## 5. Commercial Products & Clinical Translation (Table 3)

## 6. Discussion
### 6.1 Current Limitations
### 6.2 Future Directions

## 7. Conclusion

## References
```

---

## Method Description Template

```markdown
### 3.X [Method Category]

[1-2 paragraph introduction with motivation]

**[Method Name]:** [Author] et al. [ref] proposed [method], which [innovation]:
- [Key component 1]
- [Key component 2]
Achieves Dice of X.XX on [dataset].

**Limitations:** Despite advantages, [category] methods face:
(1) [limit 1]; (2) [limit 2].
```

---

## Citation Patterns

```markdown
# Data citation
"...achieved Dice of 0.89 [23]"

# Method citation
"Gu et al. [45] proposed..."

# Multi-citation
"Several studies demonstrated... [12, 15, 23]"

# Comparative
"While [12] focused on..., [15] addressed..."
```

---

## Reference Files

| File | Purpose |
|------|---------|
| [references/WORKFLOW.md](references/WORKFLOW.md) | Detailed 7-phase workflow |
| [references/TEMPLATES.md](references/TEMPLATES.md) | CLAUDE.md and IMPLEMENTATION_PLAN.md templates |
| [references/DOMAINS.md](references/DOMAINS.md) | Domain-specific method categories |
| [references/MCP_SETUP.md](references/MCP_SETUP.md) | MCP server configuration |
| [references/QUALITY_CHECKLIST.md](references/QUALITY_CHECKLIST.md) | Pre-submission quality checklist |
