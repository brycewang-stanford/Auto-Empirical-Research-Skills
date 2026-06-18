---
name: reference-verify
description: "Verify references in an academic paper: check whether each BibTeX entry is real, whether in-text citations match the cited paper's actual content, and produce a structured verification report. Use when user says \"验证参考文献\", \"ref verify\", \"check references\", \"核实引用\", \"引用是否正确\", or wants to audit citations in a LaTeX manuscript."
argument-hint: [paper-directory-or-tex-file]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# Ref-Verify: 学术论文参考文献验证

Verify references for: **$ARGUMENTS**

---

## Purpose

This skill performs a systematic audit of every reference cited in a LaTeX manuscript. For each citation it:

1. Confirms the BibTeX entry describes a **real, published paper** (not hallucinated).
2. Locates **every place** the reference is cited in the manuscript.
3. Extracts the **claim or viewpoint** the author attributes to that reference.
4. Judges whether the cited paper's **actual content supports** the attributed claim.
5. Produces a structured **verification report** as a LaTeX table and a Markdown summary.

---

## Constants

- **VERIFY_METHOD = `web`** — How to verify references. Options: `web` (WebSearch + WebFetch for each entry), `dblp` (DBLP API first, WebSearch fallback), `manual` (skip online verification, only check internal consistency).
- **OUTPUT_FORMAT = `excel`** — Output format. Options: `excel` (default, `.xlsx` with conditional formatting), `markdown`, `latex`, `all` (all three).
- **OUTPUT_DIR** — Directory to save the report. Defaults to the same directory as the input `.tex` file.
- **LANGUAGE = `zh`** — Report language. Options: `zh` (Chinese headers), `en` (English headers).
- **STRICT = false** — When `true`, flag any citation where the attributed claim cannot be confirmed from the paper's abstract/title as `未确认`. When `false`, give benefit of the doubt for plausible matches.
- **APPLY_FIXES = `interactive`** — Whether to apply the suggested fixes after the report is generated. Options: `interactive` (default — show each proposed edit and ask user y/n/skip/edit), `auto` (apply every fix without asking; use only when user explicitly opts in), `off` (stop after the report; no edits to source files).

---

## Inputs

The skill accepts one of:

1. **A directory** containing `.tex` and `.bib` files (scans all `.tex` files for citations).
2. **A single `.tex` file** (uses the `\bibliography{}` command to locate the `.bib` file).
3. **A `.bib` file** alone (verifies entries exist but cannot check in-text citation context).

If no argument is provided, scan the current working directory.

---

## Workflow

### Step 1: Locate Files

1. Find all `.tex` files in the target directory (or the single specified file).
2. Find the `.bib` file(s) referenced by `\bibliography{}` or `\addbibresource{}`.
3. Read and parse the `.bib` file to extract all BibTeX entries.
4. Read all `.tex` files to extract all `\cite{}`, `\citep{}`, `\citet{}`, `\citealt{}`, `\citealp{}` commands.

### Step 2: Build Citation Map

For each citation key found in the `.tex` files:

1. **Extract BibTeX metadata**: author, title, journal, year, volume, pages.
2. **Locate all in-text occurrences**: Record each file name, line number, and the surrounding sentence (±1 sentence for context).
3. **Extract attributed claim**: From the surrounding text, identify what viewpoint, finding, or argument the author attributes to the cited work.

Produce an internal data structure:

```
[
  {
    "seq": 1,
    "key": "baker2006investor",
    "bib": { "author": "Baker, Malcolm and Wurgler, Jeffrey", "title": "Investor sentiment...", "journal": "Journal of Finance", "year": "2006" },
    "occurrences": [
      { "file": "sections/1_introduction.tex", "line": 12, "context": "...investor sentiment predicts cross-sectional stock returns...", "claim": "investor sentiment predicts cross-sectional returns" }
    ]
  },
  ...
]
```

### Step 3: Verify Each Reference

For each BibTeX entry, perform verification in order:

#### 3a. Existence Check (Is the paper real?)

Use this verification chain (stop at first success):

**Method A: DBLP** (if VERIFY_METHOD includes `dblp`)
```bash
# Search DBLP by title + first author
curl -s "https://dblp.org/search/publ/api?q=TITLE+FIRST_AUTHOR&format=json&h=3"
# If match found: VERIFIED
```

**Method B: WebSearch**
```
WebSearch: "EXACT_TITLE" author FIRST_AUTHOR_LASTNAME journal JOURNAL_NAME
```
Check the top 3 results. A paper is **VERIFIED** if:
- The title matches (exact or near-exact, allowing minor capitalization/punctuation differences).
- The author(s) match.
- The journal/venue matches.
- The year matches (±1 year tolerance for working paper → publication lag).

A paper is **UNVERIFIED** if no matching result is found after both methods.

**Method C: CrossRef DOI** (if a DOI is in the bib entry)
```
WebFetch: https://doi.org/DOI
```

#### 3b. Metadata Accuracy Check

If the paper is verified, compare the BibTeX metadata against the verified source:
- Is the **year** correct?
- Is the **journal name** correct?
- Are the **volume and pages** correct?
- Are all **authors** listed correctly?

Flag any discrepancies.

#### 3c. Citation Context Check (Is the claim supported?)

For each occurrence of the citation in the manuscript:

1. Read the **sentence(s)** surrounding the citation.
2. Identify the **specific claim** attributed to the cited paper.
3. Determine whether the cited paper's **title, abstract, and known content** support that claim.

Classification:
- **支撑 (Supported)**: The claim is clearly consistent with the cited paper's known content.
- **部分支撑 (Partially supported)**: The claim is related but overstated, narrowed, or slightly reframed.
- **不支撑 (Not supported)**: The claim does not match the cited paper's content.
- **未确认 (Unconfirmed)**: Cannot determine from available information (title/abstract only).
- **论文不存在 (Paper not found)**: The BibTeX entry could not be verified as a real publication.

### Step 4: Generate Report

The default output is an **Excel report** (`ref_verify_report.xlsx`). Use Python + `openpyxl` to generate.

#### Excel Report (`ref_verify_report.xlsx`) — DEFAULT

The Excel workbook contains **three sheets**, structured as follows:

**Sheet 1: 总览 (Overview)**

| 项目 | 数值 |
|------|------|
| 论文标题 | [paper title] |
| 验证日期 | [date] |
| 验证方法 | [web/dblp/manual] |
| 总引用数 | X |
| 验证通过 | Y |
| 存疑 | Z |
| 不存在 | W |
| 未引用条目 | U |

**Sheet 2: 已验证文献 (Verified References)**

This sheet covers references that **can be found** online. Focus is on **citation–claim support analysis**.

| 列 | 说明 |
|----|------|
| 序号 | 按文中首次出现顺序 |
| 参考文献 | 作者 (年份), 期刊缩写 |
| BibTeX Key | cite key |
| 文中引用位置 | 文件名:行号，多处用分号分隔 |
| 引用观点 | 作者在引用处表达的核心观点（≤30字） |
| 支撑判定 | 支撑 / 部分支撑 / 不支撑 / 未确认 |
| 支撑分析 | 详细说明：原文实际说了什么 vs 引用处声称了什么，差异在哪 |
| 元数据问题 | 年份、期刊名、作者拼写等元数据错误（无则留空） |
| 修改建议 | 针对不支撑/部分支撑/元数据错误的具体修改建议 |

Conditional formatting for this sheet:
- **支撑** → row background light green (`#C6EFCE`)
- **部分支撑** → row background light yellow (`#FFEB9C`)
- **不支撑** → row background light red (`#FFC7CE`)
- **未确认** → row background light gray (`#D9D9D9`)

**Sheet 3: 问题文献 (Problematic References)**

This sheet covers references that **cannot be found** or have **serious issues**. Each entry gets a **detailed problem diagnosis**.

| 列 | 说明 |
|----|------|
| 序号 | 按文中首次出现顺序 |
| 参考文献 | BibTeX 中的作者 (年份), 期刊 |
| BibTeX Key | cite key |
| 文中引用位置 | 文件名:行号 |
| 引用观点 | 作者在引用处表达的核心观点 |
| 问题类型 | 见下方分类 |
| 问题详情 | 详细描述搜索过程和发现 |
| 可能原因 | 分析此条目出问题的原因 |
| 修改建议 | 具体修改方案（替换文献/修正信息/删除引用） |
| 严重程度 | 🔴 高 / 🟡 中 / 🟢 低 |

**问题类型分类** (fill in "问题类型" column):
- **论文不存在**: 搜索不到任何匹配结果，可能是虚构文献
- **作者不匹配**: 找到同名论文但作者不同
- **期刊/年份不匹配**: 论文存在但发表期刊或年份与 bib 条目不符
- **标题错误**: 找到相似论文但标题有明显差异
- **疑似混淆**: 多篇相似论文，无法确定引用的是哪一篇
- **预印本/未发表**: 仅在 arXiv/SSRN 等找到，未正式发表
- **孤立条目**: bib 中存在但正文从未引用

Conditional formatting for this sheet:
- **严重程度 🔴 高** → entire row bold red background (`#FFC7CE`), bold font
- **严重程度 🟡 中** → row background light orange (`#FFD9B3`)
- **严重程度 🟢 低** → row background light blue (`#BDD7EE`)

#### Excel Generation Code Pattern

Use this Python pattern via Bash to generate the xlsx:

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# --- Sheet 1: Overview ---
ws1 = wb.active
ws1.title = "总览"
# Write overview stats...

# --- Sheet 2: Verified References ---
ws2 = wb.create_sheet("已验证文献")
headers2 = ["序号", "参考文献", "BibTeX Key", "文中引用位置", "引用观点",
            "支撑判定", "支撑分析", "元数据问题", "修改建议"]
# Write headers with bold + background
# Write rows, apply conditional fill per 支撑判定 value
# Auto-adjust column widths

# --- Sheet 3: Problematic References ---
ws3 = wb.create_sheet("问题文献")
headers3 = ["序号", "参考文献", "BibTeX Key", "文中引用位置", "引用观点",
            "问题类型", "问题详情", "可能原因", "修改建议", "严重程度"]
# Write headers, rows, apply severity-based fills
# Auto-adjust column widths

# Global styling
for ws in [ws1, ws2, ws3]:
    ws.sheet_properties.pageSetUpPr = openpyxl.worksheet.properties.PageSetupProperties(fitToPage=True)
    ws.freeze_panes = "A2"  # Freeze header row

wb.save("OUTPUT_DIR/ref_verify_report.xlsx")
```

**Important**: Before running, ensure openpyxl is installed: `pip install openpyxl`

#### Markdown Report (`ref_verify_report.md`) — only when OUTPUT_FORMAT includes `markdown` or `all`

```markdown
# 参考文献验证报告

**论文**: [paper title]
**验证日期**: [date]
**验证方法**: [web/dblp/manual]
**总引用数**: X | **验证通过**: Y | **存疑**: Z | **不存在**: W

## 一、已验证文献

| 序号 | 参考文献 | 文中引用位置 | 引用观点 | 支撑判定 | 支撑分析 | 修改建议 |
|------|----------|-------------|----------|----------|----------|----------|
| 1 | Baker and Wurgler (2006), JF | 1_intro.tex:L12 | investor sentiment predicts returns | ✅ 支撑 | 与原文主要发现一致 | — |

## 二、问题文献

| 序号 | 参考文献 | 问题类型 | 问题详情 | 可能原因 | 修改建议 | 严重程度 |
|------|----------|----------|----------|----------|----------|----------|
| 5 | Smith (2020), AER | 论文不存在 | 搜索Google Scholar/DBLP均无结果 | 可能为AI生成的虚构文献 | 删除该引用或替换为... | 🔴 高 |

## 三、未引用条目
...

## 四、总结与建议
...
```

#### LaTeX Report (`ref_verify_report.tex`) — only when OUTPUT_FORMAT includes `latex` or `all`

Generate a LaTeX longtable with the same two-section structure (已验证 + 问题文献).

### Step 5: Summary and Recommendations

After the table, provide:

1. **Overall assessment**: How many references pass verification, how many are flagged.
2. **Critical issues**: Any references that appear fabricated or seriously misattributed.
3. **Minor issues**: Metadata errors (wrong year, wrong journal name, missing pages).
4. **Recommendations**: Specific fixes for each flagged entry.

### Step 6: Apply Recommended Modifications

The verification report is only useful if its "修改建议" column actually reaches the source files. Step 6 walks every actionable suggestion back into the `.tex` and `.bib` files. Skip this step only when `APPLY_FIXES = off`.

**Why this matters.** Authors typically have 30–100 citations. Hand-applying every suggested fix from the report is tedious and error-prone — they will silently skip the "small" ones (a wrong year, an orphan entry) and the manuscript ships with the same defects. Closing the loop here is the difference between a report and a real audit.

#### 6a. Build the fix queue

Re-use the in-memory verification data from Steps 2–3 — do not re-parse the xlsx. Build an ordered queue of rows that need action:

1. **All rows from Sheet 3 (问题文献)** — every entry, regardless of severity.
2. **Rows from Sheet 2 (已验证文献) where `支撑判定 = 部分支撑`** — the claim is overstated, narrowed, or reframed.

Rows where `支撑判定 ∈ {支撑, 未确认}` are **not** in the queue. `不支撑` rows belong on Sheet 3 already (move them there if the report put them on Sheet 2). Process the queue in 序号 order so the user sees fixes flow in the same order as the manuscript.

#### 6b. For each queued row, propose a concrete edit

The "修改建议" column says *what* to do at the policy level (e.g. "替换为 Baker and Wurgler (2007)"). Step 6 turns it into an exact diff. Map by category:

| 类别 | 处理方式 | 改哪里 |
|------|----------|--------|
| **部分支撑** (Sheet 2) | 重写引用所在句子，使陈述与原文实际结论一致；或替换为更贴切的 cite key | `.tex` |
| **不支撑** | 同上，或删除该引用 | `.tex` (+ `.bib` if cite key is also dropped) |
| **论文不存在** | 优先按"修改建议"中提名的替代文献替换；若无替代，则删除该引用并重写句子使其独立成立 | `.bib` (新增/删除) + `.tex` (替换 key 或重写句) |
| **作者不匹配 / 期刊年份不匹配 / 标题错误** | 修正 BibTeX 字段（author / journal / year / title / volume / pages） | `.bib` |
| **疑似混淆** | 替换为正确论文的 cite key，必要时新增 bib 条目 | `.bib` + `.tex` |
| **预印本/未发表** | 若已正式发表 → 替换为正式版本；否则将 bib 条目类型改为 `@unpublished` 或 `@misc` 并补 `note = {Working paper}` | `.bib` |
| **孤立条目** | 直接从 `.bib` 删除（默认低风险，可批量执行） | `.bib` |

For each row, before showing the user, prepare:

1. **Target file & line**: the exact `.tex` line for in-text edits; the BibTeX entry block for `.bib` edits.
2. **`old_string`**: enough surrounding context to be unique. For sentence rewrites, include the full sentence; for bib edits, include the relevant field line(s).
3. **`new_string`**: the proposed edit applied.
4. **One-line rationale**: tied back to the 修改建议 + 原文实际内容.

#### 6c. Walk the queue interactively (default)

When `APPLY_FIXES = interactive`, present each fix to the user using this exact template, then act on the response:

```
[修订 N/总数]  序号 K · <BibTeX Key>  ·  <类别>
位置: <file>:<line>     严重程度: <🔴/🟡/🟢/—>

引用观点: <引用观点 from report>
原文实际: <one sentence on what the cited paper actually says, or "—" for bib-only fixes>
修改理由: <one-line rationale>

— 当前 —
<old_string>

— 修改后 —
<new_string>

应用此修改？(y=apply / n=skip / e=let me edit new_string / q=quit Step 6)
```

Response handling:

- **y**: call the `Edit` tool with the prepared `old_string` / `new_string`. Mark the row applied.
- **n**: log as skipped with the user's reason if given. Move on.
- **e**: ask the user for a replacement `new_string`, then re-confirm before applying.
- **q**: stop the queue. Summarize what's been applied so far. Do not undo prior edits.

When `APPLY_FIXES = auto`, skip the prompt and apply every prepared edit, but still display the same block so the user can scroll back and audit. **Auto mode requires explicit user opt-in** (`-- apply: auto`); never silently auto-apply.

#### 6d. Safety rails

These are non-negotiable — getting a citation fix wrong can introduce plagiarism risk or hallucinated content into a published paper.

1. **Backup before first edit.** On the first applied edit of the session, copy each `.tex` and `.bib` file that will be touched to `<file>.bak-YYYYMMDD-HHMMSS`. One backup per file, not per edit.
2. **Never invent a cite key or paper.** A replacement cite key must either (a) already exist in the `.bib` file, or (b) point to a paper you actually verified online during Step 3 — in which case generate a clean BibTeX entry from the verified metadata, do not paraphrase.
3. **Never delete a sentence whole if doing so leaves the paragraph ungrammatical or removes a substantive claim.** If the sentence's only purpose was to introduce the bad citation, deletion is fine; otherwise rewrite so the surrounding logic still holds.
4. **Multi-occurrence citations**: if the same cite key appears at multiple `.tex` locations and the fix is bib-side (metadata correction), one `.bib` edit covers all sites. If the fix is in-text (claim rewrite), each occurrence is its own queue row and gets reviewed separately — the same paper can be fine in one place and overstated in another.
5. **Preserve LaTeX command shape.** `\citep{key}`, `\citet{key}`, `\cite[p.~12]{key}` are not interchangeable — when replacing a cite key, keep the same command and any optional arguments. When rewriting a sentence, keep the citation command in a sensible position.
6. **Re-run a quick post-check.** After the queue is processed, re-grep the manuscript for every cite key that was touched. Confirm: bib entry exists for each remaining key; no stray empty `\citep{}` was left behind; no `.bak` filenames leaked into the manuscript.

#### 6e. Write a change log

After Step 6 completes, write `ref_verify_changes.md` next to the report. One entry per applied/skipped row:

```markdown
# 参考文献修订日志

**生成时间**: 2026-05-08 07:35
**总数**: 已应用 N · 跳过 M · 用户编辑 K · 失败 F

## 已应用

### 1. baker2006investor — 部分支撑
- 位置: `1_introduction.tex:42`
- 原: investor sentiment predicts cross-sectional stock returns in all market conditions
- 改: investor sentiment predicts cross-sectional stock returns more strongly among stocks that are difficult to value or arbitrage (Baker and Wurgler, 2006)
- 理由: 原文结论限定在难以估值/套利的股票，原句过度泛化

### 2. smith2020aer — 论文不存在
- 位置: `2_literature.tex:88`，`bib/refs.bib:142`
- 操作: 删除 `.bib` 条目；将文中 `\citep{smith2020aer}` 替换为 `\citep{shleifer1997limits}`
- 理由: 在 Google Scholar / DBLP / SSRN 均搜索不到 Smith (2020, AER)，疑似虚构；改用主张相近的 Shleifer & Vishny (1997)

## 跳过
...
```

This log is the audit trail — if a co-author later asks "what did the verifier change?", the answer is one file. It also lets the user sanity-check before committing.

## Column Definitions

### Sheet 2 — 已验证文献

| 列名 | 含义 | 填写规则 |
|------|------|----------|
| **序号** | 按文中首次出现顺序编号 | 从 1 开始递增 |
| **参考文献** | 作者 (年份), 期刊缩写 | 如 "Baker and Wurgler (2006), JF" |
| **BibTeX Key** | citation key | 如 "baker2006investor" |
| **文中引用位置** | 文件名:行号 | 如 "1_intro.tex:L42"；多处引用用分号分隔 |
| **引用观点** | 作者在引用处表达的核心观点 | 用一句话概括，不超过 30 字 |
| **支撑判定** | 被引论文是否支持该观点 | 支撑 / 部分支撑 / 不支撑 / 未确认 |
| **支撑分析** | 对比分析 | 原文实际结论 vs 引用处声称内容，指出差异 |
| **元数据问题** | bib 条目信息错误 | 年份/期刊/作者拼写等，无则留空 |
| **修改建议** | 具体修改方案 | 针对不支撑/部分支撑/元数据错误 |

### Sheet 3 — 问题文献

| 列名 | 含义 | 填写规则 |
|------|------|----------|
| **序号** | 按文中首次出现顺序编号 | 从 1 开始递增 |
| **参考文献** | BibTeX 中的作者 (年份), 期刊 | 原样摘录 bib 信息 |
| **BibTeX Key** | citation key | 如 "smith2020aer" |
| **文中引用位置** | 文件名:行号 | 多处引用用分号分隔 |
| **引用观点** | 作者在引用处的核心观点 | ≤30 字 |
| **问题类型** | 分类标签 | 论文不存在/作者不匹配/期刊年份不匹配/标题错误/疑似混淆/预印本未发表/孤立条目 |
| **问题详情** | 搜索过程与发现 | 搜了什么、找到什么、哪里对不上 |
| **可能原因** | 问题成因分析 | 如 AI 生成、记忆混淆、版本差异等 |
| **修改建议** | 具体修复方案 | 替换为哪篇/修正哪些字段/删除引用 |
| **严重程度** | 风险等级 | 🔴 高（虚构/严重误引）/ 🟡 中（元数据错误/模糊匹配）/ 🟢 低（孤立条目/预印本） |

---

## Key Rules

1. **Verify every entry** — Do not skip any citation. Every `\cite` in the manuscript must appear in the report.
2. **No guessing** — If you cannot confirm a paper's existence after web search, mark it as `未确认`, not `支撑`.
3. **Context matters** — The same paper may be cited multiple times for different claims. Each occurrence is a separate row.
4. **Be specific** — In the "引用观点" column, extract the actual claim, not a generic description like "discusses sentiment".
5. **Suggest fixes** — For every flagged entry, provide a concrete fix (correct year, correct journal, alternative citation, etc.).
6. **Preserve order** — Number entries by first appearance in the manuscript, not alphabetically.
7. **Handle multi-cite** — For `\citep{a, b, c}`, create separate rows for each key but note they appear in the same citation group.
8. **Check both directions** — Also flag BibTeX entries that exist in `.bib` but are never cited in any `.tex` file (orphan entries).
9. **Report uncited entries** — List any `.bib` entries not referenced in the text in a separate "未引用条目" section (in Excel: added to Sheet 3 with 问题类型 = "孤立条目").
10. **Excel first** — Always generate the `.xlsx` report. Only generate `.md` / `.tex` if OUTPUT_FORMAT is `markdown`, `latex`, or `all`.
11. **Two-group structure** — Clearly separate verified references (Sheet 2) from problematic ones (Sheet 3). The two sheets serve different purposes: Sheet 2 focuses on **citation–claim alignment analysis**; Sheet 3 focuses on **problem diagnosis and severity**.
12. **Severity assessment** — For every entry in Sheet 3, assign a severity level: 🔴 高 (paper likely doesn't exist or is seriously misattributed), 🟡 中 (metadata errors or ambiguous match), 🟢 低 (minor issues like orphan entries or preprint status).
13. **Rich problem diagnosis** — For unfound references, document: what you searched for, what you found instead, possible reasons for the discrepancy, and an actionable fix. Do NOT just say "未找到" — explain WHY.
14. **Close the loop with Step 6** — A report nobody acts on is wasted work. Always proceed into Step 6 unless `APPLY_FIXES = off` or the user explicitly declines. The fix queue is **all of Sheet 3** plus **Sheet 2 rows where 支撑判定 = 部分支撑** — process in 序号 order so the user can follow along with the manuscript.
15. **Backup, then edit** — Step 6 makes destructive changes to `.tex` and `.bib`. Always create timestamped backups on the first applied edit, and never invent a replacement cite key without an actual verified source behind it. Write `ref_verify_changes.md` so the user has an audit trail.

---

## Invoking

```
/ref-verify                                → scan current directory, output Excel
/ref-verify "paper/"                       → scan paper/ directory, output Excel
/ref-verify "main.tex"                     → scan specific file, output Excel
/ref-verify "paper/" -- format: all        → output Excel + Markdown + LaTeX
/ref-verify "paper/" -- format: markdown   → output Markdown only
/ref-verify "paper/" -- strict: true       → strict mode (flag all unconfirmed)
/ref-verify "paper/" -- method: dblp       → use DBLP API first
/ref-verify "paper/" -- lang: en           → English report headers
/ref-verify "paper/" -- apply: interactive → review & apply each fix one by one (default)
/ref-verify "paper/" -- apply: auto        → apply every suggested fix without asking
/ref-verify "paper/" -- apply: off         → stop after report; do NOT touch .tex / .bib
```

---

## Related Skills

- **/econ-paper-write** — Write the paper sections that need citation verification
- **/research-lit** — Find replacement papers if a citation is invalid
- **/paper-compile** — Compile the paper after fixing references
- **/arxiv** — Search arXiv for preprint versions of cited papers
