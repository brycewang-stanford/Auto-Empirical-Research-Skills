<!-- Vendored into AERS from https://github.com/PHY041/claude-skill-citation-checker on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`PHY041/claude-skill-citation-checker`](https://github.com/PHY041/claude-skill-citation-checker) for the AERS catalog (license: MIT (declared in README; no LICENSE file upstream)). Vendored 2026-06-01. The original upstream README follows verbatim.

---

# check-citations

**Stop hallucinated citations before they reach your reviewer.**

A Claude Code skill that verifies every citation in your `.bib` file against three academic databases (CrossRef, Semantic Scholar, OpenAlex). Catches fabricated references, chimeric citations, and suspicious patterns — no API keys required.

## Why This Exists

| Problem | Scale |
|---------|-------|
| AI-generated citations are fabricated | 6-55% depending on model |
| NeurIPS 2025 accepted papers contained 100+ fake refs | [Source](https://arxiv.org/abs/2501.04181) |
| Universities now treat fake citations as misconduct | Growing trend since 2024 |
| Existing tools only check if DOIs resolve | They miss fabricated content |

**This is the only tool that detects the actual hallucination problem** — not just broken links, but papers that don't exist.

## Install

```bash
# Clone into your Claude Code skills directory
git clone https://github.com/PHY041/claude-skill-citation-checker.git ~/.claude/skills/check-citations

# Dependencies (just requests)
pip install requests
```

Then in Claude Code: `Use /check-citations to verify my bibliography`

## Quick Start

```bash
# Check a single .bib file
python scripts/citation_checker.py references.bib

# Check all .bib files in a project
python scripts/citation_checker.py path/to/thesis/

# JSON output for CI/CD
python scripts/citation_checker.py references.bib --json

# Verbose (see API responses)
python scripts/citation_checker.py references.bib --verbose
```

## What It Catches

### 1. Fully Fabricated Citations

Papers that don't exist in any database. The classic LLM hallucination.

```
  NOT FOUND (0 sources): [zhang2024unified]
    Title:   Unified Framework for Multi-Modal Reasoning in Dynamic Environments
    Authors: Zhang, Wei and Liu, Xiaoming and Chen, Yufei
    FLAG: NOT FOUND in any database — likely hallucinated
```

### 2. Chimeric Citations (Most Dangerous)

Real paper title + wrong authors. Looks legitimate on a quick Google check but is fabricated.

```
  SUSPICIOUS: [chimeric1] confidence=60%
    Title:      Attention Is All You Need
    Best match: Attention Is All You Need
    FLAG: Title matches but authors don't — possible chimeric hallucination
```

### 3. Red Flag Patterns

- Invalid DOI format
- Suspiciously generic titles ("A Comprehensive Survey of...")
- Future publication years
- Missing authors or single-word names

## How It Works

```
BibTeX Entry
    |
    v
[CrossRef] ──> 140M+ DOI works
    |
    v
[Semantic Scholar] ──> 200M+ papers
    |
    v
[OpenAlex] ──> 240M+ works
    |
    v
Title Similarity + Author Overlap + Red Flags
    |
    v
verified / suspicious / not_found
```

- **2+ sources match** → verified (high confidence)
- **1 source only** → suspicious (manual check needed)
- **0 sources** → not_found (likely hallucinated)
- **Title matches, authors don't** → chimeric flag

## Accuracy

Tested against 25 curated citations:

| Category | Score | Description |
|----------|-------|-------------|
| Real papers caught | **90%** (9/10) | Famous ML papers (Vaswani, Devlin, He, Brown, etc.) |
| Fake papers caught | **100%** (10/10) | Fabricated with plausible titles and authors |
| Chimeric caught | **100%** (5/5) | Real title + wrong authors |
| False negative rate | **0%** | No fake paper was ever marked as real |

Run the test suite yourself:

```bash
# Unit tests only (no API calls)
python tests/test_citation_checker.py --unit-only

# Full suite (API calls, ~5 min)
python tests/test_citation_checker.py --verbose
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Verify citations
  run: |
    pip install requests
    python scripts/citation_checker.py references.bib --json > citation_report.json
    python -c "
    import json, sys
    r = json.load(open('citation_report.json'))
    if r['summary']['not_found'] > 0:
        print(f'FAIL: {r[\"summary\"][\"not_found\"]} citations not found')
        sys.exit(1)
    "
```

### Pre-commit Hook

```bash
#!/bin/bash
python scripts/citation_checker.py references.bib
exit $?
```

## Limitations

- Papers without DOI that have many derivatives (BERT, GPT-2) may not be found via title search — include DOIs when possible
- Semantic Scholar rate-limits at ~100 req/5min on free tier
- Book chapters and grey literature have lower coverage
- No API keys needed, but free tiers have throughput limits

## License

MIT

---

## Share / Star

If this saved you from submitting hallucinated citations:

**[Give it a star on GitHub](https://github.com/PHY041/claude-skill-citation-checker)**

---

<details>
<summary>Chinese / 中文介绍</summary>

# check-citations — AI 论文引用验证

**别让 AI 编造的引用出现在你的论文里。**

一个 Claude Code 技能，自动检查 `.bib` 文件中的每一条引用是否真实存在。对接三大学术数据库（CrossRef、Semantic Scholar、OpenAlex），无需 API key。

## 为什么需要这个工具

- ChatGPT/Claude 生成的引用有 6-55% 是**编造的**
- NeurIPS 2025 录取论文中发现 100+ 条虚假引用
- 大学已经把虚假引用视为**学术不端**
- 现有工具只检查 DOI 链接是否能打开，不检查论文是否真的存在

**这是唯一一个能检测「论文本身不存在」的工具。**

## 三种检测能力

| 类型 | 说明 | 检测率 |
|------|------|--------|
| 完全编造 | 论文标题、作者全是假的 | **100%** |
| 嵌合引用 | 真实标题 + 错误作者（最危险） | **100%** |
| 红旗模式 | 无效 DOI、过于泛化的标题、缺失字段 | **100%** |

## 安装

```bash
git clone https://github.com/PHY041/claude-skill-citation-checker.git ~/.claude/skills/check-citations
pip install requests
```

## 使用

```bash
# 检查单个 .bib 文件
python scripts/citation_checker.py references.bib

# 检查目录下所有 .bib
python scripts/citation_checker.py path/to/thesis/

# JSON 输出（用于 CI）
python scripts/citation_checker.py references.bib --json
```

写论文的时候跑一下，5 分钟，省得被审稿人打回来。

**觉得有用就 [给个 Star](https://github.com/PHY041/claude-skill-citation-checker) 吧**

</details>
