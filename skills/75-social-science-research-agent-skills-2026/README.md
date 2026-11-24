# 社会科学研究Agent Skills手册·通用版2026配套Skill包

这是《社会科学研究Agent Skills手册·通用版2026》（计量经济圈，共169页）第168页「附带的24个可安装Skill模板」对应的ZIP包。

手册第168页原文：

> 随手册同时提供一个 ZIP。每个目录都按 Agent Skills 开放规范组织，至少包含 SKILL.md，并写入任务触发条件、输入、步骤、输出契约、人工关口和最终检查。它们是通用研究底座，需要再根据团队数据、期刊、软件和学科规范做本地化。

本包严格按这段话和第168页的清单整理：

- 共24个目录，目录名就是第168页清单里的Skill名，顺序也与清单一致。
- 每个目录只有一个SKILL.md，开头是Agent Skills开放规范要求的YAML头（name与目录名一致，description写明手册编号、页码和「何时调用」）。
- SKILL.md正文的何时调用、必须输入、标准流程、输出契约、人工关口、最常见的翻车点、核验依据、推荐实现，以及证据等级、自动化边界、适用学科，全部逐字取自该条目在手册正文的那一页。
- 手册条目页没有单列「最终检查」，所以每个SKILL.md里的「最终检查」清单是按手册第3页「如何使用这本手册」第4、5条、第9页「十条研究Agent底线」第01条和该条目本页内容整理的，没有新增手册以外的能力。
- 每个SKILL.md末尾列出手册第161-163页方法型Skill Packs和第166-167页十条端到端工作流里用到该技能的地方，方便串联使用。

注意，这24个是「可安装Skill模板」，和手册第161-163页的「24个高频方法型Skill Packs」（M01-M24）不是一回事，M包是编排层，不在本ZIP里。

## Skill清单与手册对应

| 序号 | Skill目录 | 手册条目 | 所在章节 | 手册页码 | 证据等级 | 自动化边界 |
|---|---|---|---|---|---|---|
| 1 | `research-question-decomposer` | R01 研究问题拆解 | 第1章 研究问题、理论与贡献 | 12 | A- | 半自动 |
| 2 | `contribution-auditor` | R02 贡献定位审计 | 第1章 研究问题、理论与贡献 | 13 | A- | 半自动 |
| 3 | `novelty-checker` | R03 新颖性检索 | 第1章 研究问题、理论与贡献 | 14 | A- | 可自动后核验 |
| 4 | `multi-database-search-orchestrator` | L03 多数据库检索编排 | 第3章 文献发现与引文核验 | 36 | A | 可自动后核验 |
| 5 | `doi-metadata-resolver` | L06 DOI 与元数据解析 | 第3章 文献发现与引文核验 | 39 | A | 可自动后核验 |
| 6 | `retraction-correction-checker` | L10 撤稿更正状态核验 | 第3章 文献发现与引文核验 | 43 | A | 可自动后核验 |
| 7 | `literature-search-auditor` | L12 检索审计日志 | 第3章 文献发现与引文核验 | 45 | A | 可自动后核验 |
| 8 | `title-abstract-screener` | S03A 标题摘要双阶段筛选 | 第4章 系统综述与证据综合 | 49 | A- | 半自动 |
| 9 | `evidence-extraction-schema` | S05A 证据抽取表设计 | 第4章 系统综述与证据综合 | 51 | A | 半自动 |
| 10 | `public-data-scout` | A02 公共数据源发现 | 第5章 数据发现、获取与合规 | 59 | A | 可自动后核验 |
| 11 | `data-dictionary-lineage` | E02 数据字典与血缘 | 第6章 数据工程、治理与可复用 | 70 | A | 可自动后核验 |
| 12 | `data-merge-auditor` | E09 数据合并审计 | 第6章 数据工程、治理与可复用 | 77 | A | 可自动后核验 |
| 13 | `survey-instrument-designer` | D04 问卷题项设计 | 第2章 研究设计、测量与伦理 | 26 | A | 半自动 |
| 14 | `llm-annotation-validator` | X04 LLM 标注验证 | 第10章 计算社会科学 | 122 | A- | 半自动 |
| 15 | `causal-estimand-definer` | C01 因果问题与 Estimand | 第8章 因果推断与实验评估 | 95 | A | 人主导 |
| 16 | `causal-design-selector` | C03 识别设计选择 | 第8章 因果推断与实验评估 | 97 | A | 人主导 |
| 17 | `identification-assumption-auditor` | C05 识别假设审计 | 第8章 因果推断与实验评估 | 99 | A | 人主导 |
| 18 | `qualitative-codebook-builder` | K06 编码本构建 | 第9章 质性与混合方法 | 111 | A | 半自动 |
| 19 | `process-tracing-evidence-auditor` | K09 案例研究与过程追踪 | 第9章 质性与混合方法 | 114 | A- | 人主导 |
| 20 | `text-preprocessing-auditor` | X02 文本预处理审计 | 第10章 计算社会科学 | 120 | A | 可自动后核验 |
| 21 | `cold-start-repro-reviewer` | V10 冷启动复现审稿 | 第11章 稳健性、复现与 Skill 工程 | 141 | A | 可自动后核验 |
| 22 | `fair-tier-package-auditor` | V07 FAIR/TIER 复现包审计 | 第11章 稳健性、复现与 Skill 工程 | 138 | A | 半自动 |
| 23 | `claim-citation-fact-auditor` | W03 主张-引文-事实审计 | 第12章 写作、投稿与同行评议 | 147 | A | 可自动后核验 |
| 24 | `reviewer-redteam-response` | W05 审稿人红队与回复 | 第12章 写作、投稿与同行评议 | 149 | A- | 人主导 |

全部24条都在手册128项正式研究Skills之内，第168页清单之外没有多放，也没有遗漏。

## 目录结构

```
社会科学研究Agent_Skills手册_skills包_2026/
├── README.md
├── research-question-decomposer/
│   └── SKILL.md
├── contribution-auditor/
│   └── SKILL.md
├── novelty-checker/
│   └── SKILL.md
├── multi-database-search-orchestrator/
│   └── SKILL.md
├── doi-metadata-resolver/
│   └── SKILL.md
├── retraction-correction-checker/
│   └── SKILL.md
├── literature-search-auditor/
│   └── SKILL.md
├── title-abstract-screener/
│   └── SKILL.md
├── evidence-extraction-schema/
│   └── SKILL.md
├── public-data-scout/
│   └── SKILL.md
├── data-dictionary-lineage/
│   └── SKILL.md
├── data-merge-auditor/
│   └── SKILL.md
├── survey-instrument-designer/
│   └── SKILL.md
├── llm-annotation-validator/
│   └── SKILL.md
├── causal-estimand-definer/
│   └── SKILL.md
├── causal-design-selector/
│   └── SKILL.md
├── identification-assumption-auditor/
│   └── SKILL.md
├── qualitative-codebook-builder/
│   └── SKILL.md
├── process-tracing-evidence-auditor/
│   └── SKILL.md
├── text-preprocessing-auditor/
│   └── SKILL.md
├── cold-start-repro-reviewer/
│   └── SKILL.md
├── fair-tier-package-auditor/
│   └── SKILL.md
├── claim-citation-fact-auditor/
│   └── SKILL.md
└── reviewer-redteam-response/
    └── SKILL.md
```

## 安装方法

手册本身没有写安装步骤，下面是按Agent Skills开放规范的通用做法补充的。安装就是把需要的Skill目录（整个文件夹，里面有SKILL.md）复制到对应工具的skills目录，README.md不用复制。

- Claude Code：个人全局放到`~/.claude/skills/`，只给某个项目用就放到项目里的`.claude/skills/`。
- Codex：个人全局放到`~/.agents/skills/`（旧版的`~/.codex/skills/`也还能识别），项目级放到仓库里的`.agents/skills/`。
- Cursor：项目级放到`.cursor/skills/`或`.agents/skills/`，全局放到`~/.cursor/skills/`；Cursor也会读取`~/.claude/skills/`和`~/.codex/skills/`。
- 其他支持Agent Skills开放规范的工具，按各自文档放进skills目录即可。

macOS或Linux示例（以Claude Code为例）：

```bash
unzip 社会科学研究Agent_Skills手册_skills包_2026.zip
mkdir -p ~/.claude/skills
cp -R 社会科学研究Agent_Skills手册_skills包_2026/*/ ~/.claude/skills/
```

Windows可以直接把24个文件夹拖进`C:\Users\你的用户名\.claude\skills\`。装好后重启工具，对话里描述任务（比如“帮我审计这次数据合并”）就会自动触发，也可以按工具的方式手动点名调用。

## 使用提醒

按手册第168页的说法，这些模板是通用研究底座，用之前要按自己团队的数据、期刊、软件和学科规范做本地化。手册的核心原则是把执行和判断分开，检索、去重、跑代码、逐项比数这类机械工作可以交给Agent，研究问题、理论、测量、识别、伦理、解释和最终发表责任必须由研究者掌握。

手册第9-10页「十条研究Agent底线」原文：


01 不允许生成或补齐不存在的文献、DOI、页码、数据、引语和政策事实。查不到就明确写未核实。
02 不允许把 AI 摘要当作原文证据。需要发表级结论时必须回到论文、政策、代码本或数据原始来源。
03 不允许 Agent 替研究者决定因果识别是否成立。统计诊断不能替代制度知识和不可检验假设。
04 不允许用事后显著结果反向决定样本、变量、机制、异质性或纳排规则而不做披露。
05 不允许把模拟的合成受访者当作真实总体的替代样本来估计人口参数。
06 不允许在质性研究中让 LLM 成为唯一解释者。主题、反身性、负案例和语境必须有人类研究者负责。
07 不允许为采集数据绕过登录、访问控制、许可、版权或参与者隐私。
08 不允许把敏感、未发表或保密审稿材料上传到不满足机构/期刊保密要求的第三方 AI 服务。
09 不允许让 Agent 输出成为黑箱。批量标注、清洗、合并和抽取必须有规则、版本、gold set 或抽样复核。
10 不允许跑通一次就宣布 Skill 可靠。必须用正常任务、边界任务和失败用例评估并版本化。

计量经济圈整理
