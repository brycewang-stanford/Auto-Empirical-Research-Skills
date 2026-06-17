---
name: master-thesis-review
description: Generate master's thesis review reports (硕士论文评阅意见) calibrated to a given score. Outputs academic evaluation and shortcomings/suggestions in Chinese. Trigger when user says "master thesis review" / "硕士论文评阅" / "论文评阅" / "评阅意见" / "thesis review".
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash
argument-hint: [path-to-thesis-folder]
---

# Master Thesis Review (硕士论文评阅意见)

## Overview

This skill generates a **master's thesis review report** (硕士学位论文评阅意见) for a given thesis. The user provides the thesis file and a score (out of 100). The skill reads the thesis, then generates two sections calibrated to the score level.

**Input**:
- A project folder containing the thesis (`*.pdf`, `*.tex`, or `*.docx`)
- A score from the user (integer, 0–100)

**Output**: `{original-filename}-评阅意见.doc` saved in the project folder

---

## Language Rule

- **Communicate with the user in Chinese.**
- **Write the review report entirely in Chinese.**

---

## Workflow

### Phase 1: Initialization

1. **Receive folder path** from user (via `$ARGUMENTS` or ask: "请提供论文文件夹路径").
2. **Scan the folder** using Glob to locate the thesis file (`*.pdf`, `*.tex`, `*.docx`).
3. **Read the thesis** in full. For large PDFs, use page ranges. Understand:
   - 论文题目 (title)
   - 研究问题与选题背景
   - 文献综述范围
   - 研究方法与数据
   - 主要结论与创新点
   - 写作结构与规范性

### Phase 2: Configuration

Use **one** AskUserQuestion call with **one** question:

**Question — 评分 (Score)**:
- Ask: "请输入您给该论文的分数（满分100分）"
- Options: 90–100 分 / 80–89 分 / 70–79 分 / 60–69 分
- User can type exact score via "Other" (e.g., 85)

Record the exact score. If the user selects a range, use the midpoint (e.g., 90–100 → 95).

### Phase 3: Generate Review

Generate two sections based on the thesis content and calibrated to the score.

---

## Score Calibration Guide

The score determines the **tone, praise-to-criticism ratio, and severity of issues raised**:

### 90–100 分 (优秀)
- **学术评语**: 高度肯定选题意义和创新性。充分认可文献掌握的广度和深度。肯定数据/方法的可靠性和规范性。语气热情、正面。
- **不足之处**: 仅提出细微的、非实质性的改进建议（如个别表述可更精炼、某处可进一步讨论）。语气温和，以"建议"为主而非"问题"。

### 80–89 分 (良好)
- **学术评语**: 肯定选题的现实意义和学术价值，认可研究方法的合理性。在肯定的同时可暗示某些方面尚有提升空间。语气正面但不过度夸张。
- **不足之处**: 指出 2–3 个实质性但非致命的问题（如文献覆盖面可拓宽、某些论证可加强、数据处理某环节可改进）。语气客观、建设性。

### 70–79 分 (中等)
- **学术评语**: 肯定选题有一定意义，但措辞较为平淡。指出文献、方法、数据等方面基本合格但存在明显不足。语气中性偏保守。
- **不足之处**: 指出 3–4 个较为明显的问题（如研究方法不够严谨、文献综述深度不足、数据来源或处理存在疑问、逻辑链条不够完整）。语气直接但仍具建设性。

### 60–69 分 (及格)
- **学术评语**: 仅承认选题有一定参考价值。对文献掌握、方法运用、写作规范等给出较低评价。语气克制，正面表述较少。
- **不足之处**: 指出多个较严重的问题（如核心论证存在逻辑漏洞、数据可靠性存疑、文献综述薄弱、创新性不足、写作不规范）。语气严肃，强调需大幅修改。

---

## Report Structure

### Section 1: 对学位论文的学术评语

**要求**:
- **240 字**（中文字符，±10%）
- **不分点**，写成一个完整的段落
- 必须覆盖以下五个方面（自然融合，不要逐条罗列）：
  1. 选题意义
  2. 文献资料的掌握
  3. 所用资料、数据的可靠性
  4. 写作规范和逻辑性
  5. 论文创新点
- 根据分数档调整褒贬比例和用词力度
- 必须基于论文的**实际内容**，引用具体的研究主题、方法、变量、发现等

### Section 2: 论文的不足之处和建议

**要求**:
- **300 字**（中文字符，±10%）
- **不分点**，写成一个完整的段落
- 明确指出论文中存在的具体问题和不足之处
- 提出具有可操作性的修改建议
- 问题的数量和严重程度与分数档匹配（高分→少而轻微；低分→多而严重）
- 必须基于论文的**实际内容**，指出具体章节、表格、论述中的问题

---

## Phase 4: Output

1. **Determine output filename**: Strip extension from thesis filename, append `-评阅意见.doc`. Example: `张三_硕士论文.pdf` → `张三_硕士论文-评阅意见.doc`.

2. **Assemble the report** with this structure:

```
对学位论文的学术评语

[240字学术评语段落]

论文的不足之处和建议

[300字不足与建议段落]

建议成绩：XX 分
```

3. **Generate .doc** using python-docx (preferred) or pandoc. Font: 宋体 (SimSun), size 12pt, 1.5x line spacing.

4. **Display** the full report content to the user.

5. Tell the user: "评阅意见已生成并保存至 `{filename}-评阅意见.doc`。"

---

## Critical Rules

1. **字数严格遵守。** 学术评语 240 字（±10%），不足与建议 300 字（±10%）。这里的"字"指中文字符数。
2. **不分点。** 两个部分都必须是连贯的段落，禁止使用编号、序号、bullet points。
3. **基于实际内容。** 所有评价必须针对论文的真实内容（题目、方法、数据、结论），不可泛泛而谈。
4. **分数校准。** 评语的褒贬比例、用词力度、问题严重程度必须与给定分数一致。90 分的评语不能比 70 分的更严厉。
5. **学术语体。** 使用正式的学术评审语言，符合中国硕士学位论文评阅的惯例和格式。
6. **先读后写。** 必须完整阅读论文后再撰写评语，不可基于部分内容生成。
7. **不要使用 AI 腔调。** 避免"总之"、"综上所述"、"值得肯定的是"等套话。语言要自然、专业、像真实的评审专家所写。
