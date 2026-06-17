---
name: five-questions
description: >
  Deeply analyze any empirical economics PDF using the five-question framework (五问框架):
  research question, identification strategy, core estimand, robustness logic,
  and scholarly contribution. Converts the PDF to Markdown, dispatches 5 parallel
  sub-agents (one per question), then compiles a 2000–3000 Chinese-character report
  with a transferable methodology checklist. Optimized for empirical economics papers
  in top journals (AER, QJE, JPE, RFS, RoF, JFE, etc.).
  
  Use this skill whenever the user wants to:
  - systematically analyze an empirical economics paper
  - apply the 五问框架 (five-question framework) to a paper
  - extract transferable research design elements from a top-journal paper
  - understand a paper's identification strategy, estimand, or robustness logic
  - run /five-questions, /five-q, or /paper-five-q-analysis
  - "帮我做五问分析", "用五问框架分析这篇论文", "analyze this paper with the five-question framework"
trigger-phrases:
  - /five-questions
  - /five-q
  - /paper-five-q-analysis
  - 用五问框架分析
  - 帮我做五问分析
  - 深度拆解这篇论文
  - five-question framework analysis
  - analyze this paper systematically
allowed-tools: Read, Write, Bash, Agent
---

# five-questions

Systematically analyze an empirical economics paper using the five-question framework.
Produces a structured Chinese report (2000–3000 chars) with a transferable methodology checklist.

## Input

```
/five-questions path/to/paper.pdf
```

Also accepts: `/five-q path/to/paper.pdf` or natural language trigger.

## File locations (explicit)

This skill keeps temporary intermediate files **inside the current project**, not next to the source PDF, so the user's working tree stays tidy and the workspace is easy to find or clean up.

| Kind | Location | Lifecycle |
|------|----------|-----------|
| **Skill root** (this file + agents/scripts/references) | `${CLAUDE_PROJECT_DIR}/.claude/skills/five-questions/` | Versioned with the project |
| **Temporary workspace** (paper.md + Q1–Q5 intermediate outputs) | `${CLAUDE_PROJECT_DIR}/.five-q-workspace/{timestamp}_{paper_slug}/` | Disposable; safe to delete after the final report is generated |
| **Final report** | `${CLAUDE_PROJECT_DIR}/{paper_slug}_five_q.md` | Persistent deliverable |

`paper_slug` = lowercase filename of the source PDF with spaces replaced by underscores and the `.pdf` extension stripped. `timestamp` = `YYYYMMDD_HHMMSS`.

If `${CLAUDE_PROJECT_DIR}` is unset (rare — happens when the skill is invoked outside a project context), fall back to the current working directory (`os.getcwd()`).

## Orchestration

Follow these steps exactly:

### Step 1 — Validate Input

Parse the PDF path from args. If not provided, ask the user for the path.

```python
import os
pdf_path = args.strip()
if not os.path.exists(pdf_path):
    print(f"ERROR: PDF not found: {pdf_path}")
    sys.exit(1)
```

### Step 2 — Create Work Directory

Place the temporary workspace inside the current project directory (NOT next to the PDF):

```python
import datetime, os, re
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
paper_name = os.path.splitext(os.path.basename(pdf_path))[0]
paper_slug = re.sub(r"\s+", "_", paper_name).lower()
work_dir = os.path.join(project_dir, ".five-q-workspace", f"{timestamp}_{paper_slug}")
os.makedirs(work_dir, exist_ok=True)
```

### Step 3 — Convert PDF to Markdown

Run the conversion script bundled with this skill, using the `sci` conda environment:

```bash
conda run -n sci python3 \
    "${CLAUDE_PROJECT_DIR}/.claude/skills/five-questions/scripts/convert_pdf.py" \
    "{pdf_path}" "{work_dir}/paper.md"
```

If markitdown is not installed: `conda run -n sci pip install 'markitdown[pdf]'`

Check that `{work_dir}/paper.md` exists and has >2000 characters.
If <2000 chars, warn the user ("可能是扫描版PDF，文本提取有限") but continue.

### Step 4 — Dispatch 5 Parallel Q-Agents

Send ALL five Agent tool calls in a SINGLE message (mandatory for parallel execution).
Each agent reads its role definition document first, then reads the paper and writes its answer.

**Prompt template for each agent (substitute N, name, output path per agent):**

```
你是一个实证经济学论文分析专家。你的角色定义和任务要求在以下参考文档中：

【第一步：立即读取你的角色定义文档】
${CLAUDE_PROJECT_DIR}/.claude/skills/five-questions/agents/qN-{name}.md

仔细阅读该文档，理解你的角色、任务清单和质量标准。

【第二步：读取论文正文】
{work_dir}/paper.md

【第三步：按照角色定义文档的要求完成分析，将结果保存到】
{work_dir}/QN.md

关键约束：
- 严格按照角色定义文档中的任务清单逐项完成
- 满足文档中规定的质量标准（不合格示例 vs 合格示例）
- 直接将结果写入输出文件，不要返回给主代理
```

Dispatch these 5 agents in parallel (one message, five Agent tool calls):

| Agent | 角色定义文档 | 输出文件 |
|-------|------------|---------|
| Q1 | `agents/q1-research-question.md` | `{work_dir}/Q1.md` |
| Q2 | `agents/q2-identification.md` | `{work_dir}/Q2.md` |
| Q3 | `agents/q3-estimand.md` | `{work_dir}/Q3.md` |
| Q4 | `agents/q4-robustness.md` | `{work_dir}/Q4.md` |
| Q5 | `agents/q5-contribution.md` | `{work_dir}/Q5.md` |

### Step 5 — Verify Q-Files

After all 5 agents complete, check each file:
- Exists: yes/no
- Size > 500 bytes: yes/no

If any file is missing or too small, log `[分析未完成]` — the compiler will handle it gracefully.

### Step 6 — Run Compiler Agent

Dispatch the compiler agent:

```
你是论文五问分析报告的汇编器。你的汇编规范在以下参考文档中：

【第一步：立即读取汇编规范文档】
${CLAUDE_PROJECT_DIR}/.claude/skills/five-questions/agents/compiler.md

仔细阅读，理解报告结构、章节格式、§6 可迁移清单的写法要求。

【第二步：读取以下所有输入文件】
- 论文全文前200行（提取元数据）：{work_dir}/paper.md
- Q1 研究问题：{work_dir}/Q1.md
- Q2 识别策略：{work_dir}/Q2.md
- Q3 核心估计量：{work_dir}/Q3.md
- Q4 稳健性检验：{work_dir}/Q4.md
- Q5 贡献与局限：{work_dir}/Q5.md

【第三步：按规范汇编完整报告，保存到】
{output_path}

关键约束：
- 总长 2000–3000 汉字
- 必须包含 § 6 可迁移方法论清单（5–8 条，具体可操作）
- 直接写入输出文件，不要返回给主代理
```

Output path: `${CLAUDE_PROJECT_DIR}/{paper_slug}_five_q.md` (the persistent final report — see "File locations" above).

### Step 7 — Report to User

```
五问分析完成！

最终报告（持久化）：{output_path}
临时工作目录（含 paper.md 与 Q1–Q5 中间产物，可删除）：{work_dir}/

报告结构：
  § 1 研究问题
  § 2 识别策略
  § 3 核心估计量
  § 4 稳健性检验
  § 5 贡献与局限
  § 6 可迁移方法论清单
```

## Error Handling

| Error | Detection | Recovery |
|-------|-----------|----------|
| PDF not found | `os.path.exists()` check | Exit with clear path error |
| pymupdf4llm missing | ImportError | Print: `conda run -n sci pip install pymupdf4llm` |
| Password-protected PDF | pymupdf exception | Suggest: `qpdf --decrypt input.pdf output.pdf` |
| Paper MD very short (<2000 chars) | char count | Warn, continue |
| One or more Q-files missing | file check after agents | Compiler marks section `[分析未完成]` |
| Metadata extraction failure | no title/author pattern | Use filename as title |

## Agent Definitions

See `agents/` directory:
- `q1-research-question.md` — 研究问题分析师
- `q2-identification.md` — 识别策略分析师
- `q3-estimand.md` — 核心估计量分析师
- `q4-robustness.md` — 稳健性检验分析师
- `q5-contribution.md` — 贡献与局限分析师
- `compiler.md` — 报告汇编器

## Reference

Five-Question depth standards: `references/five-q-framework.md`
