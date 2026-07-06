# AER-Skills

<p align="center">
  <img src="assets/aer-cover.jpg" alt="《American Economics Review》（AER，美国经济评论）封面" width="220">
</p>
<p align="center"><em>面向 <a href="https://www.aeaweb.org/journals/aer">《美国经济评论》</a>（AER）、<em>AER: Insights</em> 及 AEJ 系列期刊的 agent skill 栈。</em></p>

[![CI](https://github.com/brycewang-stanford/AER-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/brycewang-stanford/AER-Skills/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/brycewang-stanford/AER-Skills)](https://github.com/brycewang-stanford/AER-Skills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![质量门](https://img.shields.io/badge/quality%20gates-9%20enforced-brightgreen)](docs/quality-scorecard.md)
[![聚焦](https://img.shields.io/badge/focus-AER%20%2F%20AER%3AInsights%20%2F%20AEJ-1f6feb)](docs/workflow-map.md)
[![工作流](https://img.shields.io/badge/workflow-识别驱动-blue)](docs/design-principles.md)
[![Claude Code](https://img.shields.io/badge/agent-Claude%20Code-cc785c)](docs/installation-claude.md)
[![Codex](https://img.shields.io/badge/agent-Codex-0a7ea4)](docs/installation-codex.md)

简体中文 | [English](README.en.md)

面向 *American Economic Review*（AER）、*AER: Insights* 以及 *AEJ* 系列期刊的 **agent skill 包**：覆盖**选题、文献定位、正文写作、识别策略、表图规范、投稿、模拟审稿、审稿回复**的全流程。

本仓库是有立场的。它**不是**通用经济学写作工具箱，而是一套**面向 top-5 经济学**的 skill 栈：识别优先的实证、AEA 政策合规的复现包、Keith Head 风格的引言、AER 风格的 booktabs 表格、以及对编辑友好的 rebuttal 文体。

## 最近升级

v1.3 补齐了路线图列出的方法覆盖缺口：新增 **5 个数值契约 demo**（随机化推断、QTE、LP-DiD、bunching、matrix completion，共 21 条新断言）、7 条经 Crossref 验证的参考文献、StatsPAI 工具注册表扩至 51 个验证绑定，以及 Zenodo 存档元数据与宣发材料包。详见 [CHANGELOG](CHANGELOG.md)。

v1.2 的主题是**可验证性**：仓库对稿件的每一条要求，先在自己身上机器强制执行（完整清单见[质量记分卡](docs/quality-scorecard.md)，计划见[路线图](docs/roadmap.md)，历史见 [CHANGELOG](CHANGELOG.md)）：

- **数值正确性契约**：11 个可运行 demo、47 条 `NUMERIC-CHECK` 断言，每个估计值钉到已知真值 ± 容差，跑通但答错即失败。
- **引用 groundedness 门**：每条散文引用必须解析到经 Crossref 验证的 bib 条目——`PHANTOM_CITATION` / `DANGLING_KEY` 是硬失败。
- **工具绑定契约**：方法 skill 路由到 43 个已验证的 StatsPAI 工具，不允许手搓估计量。
- **质量工具自身被测试**：`tests/` 下 246 个封闭单元测试（`make test`），验证器不再只靠自检。
- **新增示例**：[端到端 walkthrough](examples/end-to-end-walkthrough.md)（一篇论文走完 12 步）与 [DML demo](examples/dml-plr-demo/)（正交化 + 交叉拟合 vs 朴素 ML plug-in）。
- CI 升级为三个 job：结构校验 + 单元测试 + 全 demo 数值冒烟，每次 push/PR 全量执行。

v1.1 把 skill 栈从十个扩展到十四个（`aer-literature`、`aer-paper-body`、`aer-consistency`、`aer-referee-sim`），并确立 12 步带门工作流。

---

## 为什么需要单独的 AER skill 栈？

Top-5 经济学期刊的硬约束在生命科学类期刊中并不存在：

| 约束维度                | AER                | AER: Insights       | 含义                                              |
|-----------------------|--------------------|---------------------|-------------------------------------------------|
| 摘要字数                | **100 词**         | 100 词              | 4-5 句话。卖结果，不卖动机。                          |
| 正文长度                | ~40 排印页         | **≤ 7,000 词减每个 exhibit 200 词** | 行文要紧；5 个 exhibits 时上限为 6,000 词。          |
| Desk rejection        | 高                 | **~45%**            | 前三页决定生死。                                    |
| 复现要求                | 强制               | 强制                | AEA 数据与代码可用性政策有专人审核执行。               |
| 识别策略                | 因果、设计驱动      | 因果、设计驱动        | TWFE、弱 IV、朴素 RDD 会被直接 desk-reject。         |
| Cover letter          | 可选               | 可选                | 仅用于 COI 披露或数据访问限制说明。                   |
| Disclosure statements | 必需               | 必需                | 每位合作者单独提交一份 PDF；即使没有冲突也要明说。       |

通用的 "scientific writing" skill（例如 [Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills)、[nature-skills](https://github.com/Yuan1z0825/nature-skills)）通常覆盖不到这些约束。

### 与相邻项目的诚实对比

| 项目 | 定位 | 与 AER-Skills 的差异 |
|---|---|---|
| Nature/generic writing skills | 生命科学写作 skill 包 | 无 top-5 经济学硬约束；无机器强制的质量门 |
| Econometrics-Agent 等动态计量 agent | 运行时：选工具、跑代码 | 只覆盖"估计"一站；不管选题、文献、写作、审稿、投稿。AER-Skills 通过 `aer-statspai` 与这类引擎互补 |
| open_deep_research 等深研 agent | 通用研究综述 | 其 groundedness 评估思想在这里被落成硬门，但它不产出可投稿的经济学稿件 |
| **AER-Skills** | **从选题到 R&R 的全生命周期 skill 栈** | **每条设计原则都有对应的机器门：引用可验证、数值可复核、工具已验证、文档质量有下限，全部由 CI 强制**（见[质量记分卡](docs/quality-scorecard.md)） |

---

## 快速上手

### 方式 A — Claude Code 插件（推荐）

```bash
# 添加 marketplace（一次性）
/plugin marketplace add https://github.com/brycewang-stanford/AER-Skills

# 安装插件
/plugin install aer-skills

# 重新加载
/reload-plugins
```

之后十四个 skill 会全部自动可用。

### 方式 B — 脚本安装

```bash
git clone https://github.com/brycewang-stanford/AER-Skills.git
cd AER-Skills

# Claude Code（用户级）
python3 scripts/install_skills.py claude

# 或 Codex
python3 scripts/install_skills.py codex
```

安装脚本会复制完整 skill 目录。更新已有安装时加 `--replace`，正式复制前可用
`--dry-run` 预览计划中的复制操作。如果想用 skill 引用到的 `templates/` 和
`examples/` 资源，请保留这个 cloned repository。

### 第一个提示词

重启 agent 后：

```text
用 aer-workflow 告诉我这篇稿子下一步该用哪个 skill。
```

更完整的安装说明见 [docs/installation-claude.md](docs/installation-claude.md)
和 [docs/installation-codex.md](docs/installation-codex.md)。

---

## 默认工作流

```text
aer-topic-selection
    -> aer-literature
        -> aer-identification
            -> aer-robustness
                -> aer-paper-body
                    -> aer-introduction
                        -> aer-tables-figures
                            -> aer-consistency
                                -> aer-referee-sim   （循环直到 ≥ major R&R）
                                    -> aer-replication
                                        -> aer-submission
                                            -> aer-rebuttal
```

核心默认假设：

- **识别先于写作** — 设计有问题，写得再漂亮也救不回来
- **AER vs AER:Insights vs AEJ** 是个**选刊路由**问题，要在写摘要之前先决定
- **先写正文再写引言** — 引言是对一篇已存在论文的总结，不是空头承诺
- **任何引用都不能凭记忆写** — 每条参考文献都必须对照抓取到的源记录核验
- **稿件必须先过自己的审稿人** — 一致性审计（`aer-consistency`）和对抗性模拟审稿（`aer-referee-sim`）是投稿前的硬门槛
- **复现包质量是论文的一部分**，不是事后补的工作
- **审稿回复信永远针对修改后的稿件**，绝不对着旧稿写

完整路线图见 [docs/workflow-map.md](docs/workflow-map.md)。

---

## 全部 Skill

### 核心 — 全生命周期

| Skill | 用途 |
|---|---|
| [`aer-workflow`](skills/aer-workflow/SKILL.md) | 路由总表 + 质量门。下一步该用哪个 skill 由它决定。 |
| [`aer-topic-selection`](skills/aer-topic-selection/SKILL.md) | Top-5 标准检测、新颖性审计、AER/Insights/AEJ 路由。 |
| [`aer-literature`](skills/aer-literature/SKILL.md) | 最近邻论文地图、定位策略、引用完整性协议 — 每条文献都核验，杜绝幻觉引用。 |
| [`aer-identification`](skills/aer-identification/SKILL.md) | DiD（错时）、IV（弱 IV 稳健）、RDD、SCM、shift-share/Bartik。 |
| [`aer-robustness`](skills/aer-robustness/SKILL.md) | 稳健性、异质性、机制、安慰剂 — 提前回应审稿人。 |
| [`aer-paper-body`](skills/aer-paper-body/SKILL.md) | 正文各节写作 — 制度背景、数据、实证策略、"结论先行"的结果叙述、效应量解释、机制、结论。 |
| [`aer-introduction`](skills/aer-introduction/SKILL.md) | Keith Head 五段式引言公式 + 100 词摘要起草。 |
| [`aer-tables-figures`](skills/aer-tables-figures/SKILL.md) | AER booktabs 风格、`etable`/`estout`/`modelsummary`、figure notes。 |
| [`aer-consistency`](skills/aer-consistency/SKILL.md) | 全稿完整性审计 — 正文数字对表格、样本漏斗、对数点换算、交叉引用、引用双向匹配；附可运行的 LaTeX 审计脚本。 |
| [`aer-referee-sim`](skills/aer-referee-sim/SKILL.md) | 对抗性内部审稿 — desk screen + 三份校准过的审稿报告，按编辑量规打分；循环直到 ≥ major R&R。 |
| [`aer-replication`](skills/aer-replication/SKILL.md) | AEA 数据与代码可用性政策、README、openICPSR。 |
| [`aer-submission`](skills/aer-submission/SKILL.md) | 格式预审、cover letter、长度审计、利益冲突声明。 |
| [`aer-rebuttal`](skills/aer-rebuttal/SKILL.md) | R&R 回复信、分类、让步 / 澄清 / 反驳的决策规则。 |

### 可选 — 实现引擎

在下方手写模板之外，再多给你一个**跑实证**的选择。

| Skill | 用途 |
|---|---|
| [`aer-statspai`](skills/aer-statspai/SKILL.md) | 用 [StatsPAI](https://github.com/brycewang-stanford/StatsPAI) 跑分析 — agent 原生的统一 Python 引擎 + MCP server，覆盖 DiD / IV / RDD / SCM / DML、`audit_result` 稳健性、honest-DiD / Oster 敏感性，以及 `to_latex` / `to_docx` 表格导出。它负责**执行**设计；选哪种设计仍由 `aer-identification` 决定。 |

---

## 代码模板

为三套常见的实证经济学技术栈提供即插即用、版本意识清晰的脚本。每套模板都包含一个
master 脚本、一个 Callaway-Sant'Anna DiD 示例、一张 AER 风格的 booktabs 回归表，
以及一个 README。

| 语言 | 技术栈 | 路径 |
|---|---|---|
| Stata | `reghdfe`、`csdid`、`estout`、`bacondecomp`、`honestdid` | [`templates/stata/`](templates/stata/) |
| R | `fixest`、`did`、`HonestDiD`、`modelsummary`、`fwildclusterboot` | [`templates/r/`](templates/r/) |
| Python | `pyfixest`、`differences`、`linearmodels`、`statsmodels`、`rdrobust`、`rddensity` | [`templates/python/`](templates/python/) |

每套模板都强制：固定随机种子（`20260101`）、相对路径、包版本记录（或在技术栈支持时
精确 pin）、AER booktabs 表格风格、矢量格式图件。

无需手工复制文件即可生成新项目：

```bash
python3 scripts/scaffold_project.py stata /path/to/new-project
python3 scripts/scaffold_project.py r /path/to/new-project
python3 scripts/scaffold_project.py python /path/to/new-project
python3 scripts/scaffold_project.py skeleton /path/to/new-replication-package

# 或使用 Make
make scaffold-stata DEST=/path/to/new-project
```

可用 `--dry-run` 预览计划中的复制操作。脚手架会拒绝仓库内部路径、模板源目录等受保护
目标；请在本仓库之外创建论文项目。

## 校验

在把 skill 复制进 agent 配置或提交 PR 之前，先运行仓库检查：

```bash
make preflight
# 等价命令：python3 scripts/validate_repo.py
```

`make preflight` 还会对 staged 和 unstaged 的 `git diff --check` 做检查，
排查空白和补丁卫生问题。
校验器会检查 skill frontmatter、skill 目录结构、agent metadata、plugin manifest、
本地 Markdown 链接、模板布局、Python 依赖的精确 pin 与 import 覆盖、安装与脚手架脚本
行为、生成/缓存文件的排除，以及 Python/R/Stata 模板语法。当 `Rscript` 不可用时，R 语法
检查会带告警跳过。CI 会安装 R，先运行 `make preflight`，再运行 `make validate-strict` —
后者在缺少可选工具时直接失败，而不是静默跳过。

可运行示例的 Monte Carlo 断言是可选的第二层 gate。安装
`templates/python/requirements.txt` 中的依赖（以及需要时的 R 包）后运行：

```bash
make smoke-examples
# 或：python3 scripts/run_example_smoke.py --strict-deps
```

默认模式会跳过缺少可选依赖的 demo；发布前用 `--strict-deps`，让任何缺失依赖或失败断言
直接返回非零状态。

质量工具自身也被测试：`make test` 运行 `tests/` 下的 246 个封闭单元测试（无网络、无重依赖），
覆盖校验器、引用核验器、skill 审计器、冒烟运行器、脚手架与安装器。
`make scorecard` 重新生成[质量记分卡](docs/quality-scorecard.md)；preflight 会在记分卡
与实测状态漂移时失败。

`make preflight` 还运行引用完整性门（`verify_citations.py --selftest`）：用 gold set
离线核验，确保 `references.bib` 与其录制的 Crossref/OpenAlex 元数据一致——把"任何引用
都不能凭记忆写"从原则变成可复跑的检查。对照线上索引核验用 `make verify-citations-online`，
对草稿做 `\cite` ↔ bib 双向核验用 `--manuscript`。详见
[引用完整性协议](docs/citation-integrity-protocol.md)。

---

## 示例

以经典 AER 及相邻 top-5 论文为依托的实操示例。
完整索引见 [examples/README.md](examples/README.md)。

| 文件 | 展示什么 |
|---|---|
| [`examples/end-to-end-walkthrough.md`](examples/end-to-end-walkthrough.md) | **从这里开始** — 同一篇虚构论文走完全部 12 个工作流步骤：每一步用哪个 skill、过哪道门、留下什么产物，并把其余示例串成一条完整路线 |
| [`examples/aer-exemplars.md`](examples/aer-exemplars.md) | 经典论文（Card-Krueger、AJR、ADH、Dell、Chetty-Hendren、Abadie、BDGK、Karlan-List …）逐一映射到各 skill，附 openICPSR / Dataverse 链接 |
| [`examples/modern-aer-exemplars.md`](examples/modern-aer-exemplars.md) | **30+ 篇近期（2018-2025）论文，按 13 个子领域组织** — Labor、Public、Development、Trade、Macro、IO、Health、Environment、Urban、Education、Finance、Political Economy、Social Networks — 外加现代识别方法工具箱，每篇都带 deposit 链接 |
| [`examples/intro-example.md`](examples/intro-example.md) | 完整的 Keith Head 五段式引言 + 97 词摘要，并附一个"不该这么写"的反例 |
| [`examples/results-section-example.md`](examples/results-section-example.md) | 同一篇虚构论文的正文写作示范 — 样本漏斗、"结论先行"的结果段落、效应量三重换算、back-of-envelope 测算、按渠道组织的机制分析，外加"逐列念表格"反例 |
| [`examples/rebuttal-example.md`](examples/rebuttal-example.md) | 完整 R&R 回复：cover letter + 编辑 + 3 位审稿人，演示让步 / 澄清 / 反驳 / 拒绝四种处理 |
| [`examples/referee-report-example.md`](examples/referee-report-example.md) | 完整的内部模拟审稿 — desk screen、三份不同立场的对抗性报告、按量规打分的编辑综合意见、按 skill 路由的修改清单 — 在投稿前抓出虚构作者后来花一整轮 R&R 才修掉的问题 |
| [`examples/replication-package-skeleton/`](examples/replication-package-skeleton/) | 可直接 deposit 的目录骨架，含 AEA 合规 README 模板、master 脚本和 globals 文件 — openICPSR 投稿的即用起点 |
| [`examples/staggered-did-demo/`](examples/staggered-did-demo/) | 可运行的 Python/R 模拟：错时处理下 naive TWFE 为什么会失败 |
| [`examples/iv-weak-instrument-demo/`](examples/iv-weak-instrument-demo/) | 可运行的 Python 模拟：弱工具变量下传统 2SLS 推断与 Anderson-Rubin 推断对比 |
| [`examples/rdd-polynomial-demo/`](examples/rdd-polynomial-demo/) | 可运行的 Python 模拟：高阶 global-polynomial RDD 为什么不安全 |
| [`examples/synthetic-control-demo/`](examples/synthetic-control-demo/) | 可运行的 Python 模拟：合成控制法的推断来自 placebo-in-space 置换分布，而非肉眼可见的事前拟合 |
| [`examples/shift-share-demo/`](examples/shift-share-demo/) | 可运行的 Python 模拟：shift-share/Bartik 推断应落在 shock（行业）层面而非地区层面——地区聚类标准误会过度拒绝 |
| [`examples/few-clusters-demo/`](examples/few-clusters-demo/) | 可运行的 Python 模拟：聚类数较少时聚类稳健 t 检验会过度拒绝，wild cluster bootstrap 可恢复名义检验水平 |
| [`examples/multiple-testing-demo/`](examples/multiple-testing-demo/) | 可运行的 Python 模拟：检验多个结果变量会抬高族系误差率，Bonferroni/Holm 校正可在保留功效的同时将其控制住 |
| [`examples/spec-curve-demo/`](examples/spec-curve-demo/) | 可运行的 Python 模拟：只报告某个"偏好"设定会误导，规格曲线置换检验才是诚实的联合推断 |
| [`examples/oster-ovb-demo/`](examples/oster-ovb-demo/) | 可运行的 Python 模拟：系数稳定本身并不能排除遗漏变量偏误，必须用 R² 变动来缩放（Oster δ） |
| [`examples/honest-did-demo/`](examples/honest-did-demo/) | 可运行的 Python 模拟：看似平坦的事前趋势会让朴素平行趋势 CI 欠覆盖，honest DiD 相对幅度边界可恢复覆盖 |
| [`examples/dml-plr-demo/`](examples/dml-plr-demo/) | 可运行的 Python 模拟：灵活的 ML 预测本身不是因果推断——非正交 plug-in 以可推知的因子持续衰减，DML 正交化 + 交叉拟合恢复真值且覆盖率诚实 |
| [`examples/randomization-inference-demo/`](examples/randomization-inference-demo/) | 可运行的 Python 模拟：小样本高杠杆实验里稳健标准误 t 检验会过度拒绝，Fisher 随机化检验尺寸精确且保留功效 |
| [`examples/qte-demo/`](examples/qte-demo/) | 可运行的 Python 模拟：均值效应为零也可能掩盖大幅分布效应——分位数处理效应复原解析 QTE 曲线，OLS 什么都看不见 |
| [`examples/lp-did-demo/`](examples/lp-did-demo/) | 可运行的 Python 模拟：错时采纳 + 异质动态下合并 TWFE 事件研究被污染，LP-DiD 用干净对照恢复真实动态路径 |
| [`examples/bunching-demo/`](examples/bunching-demo/) | 可运行的 Python 模拟：税收 kink 处的超额质量如何识别收入弹性（Saez），含 oracle/可行反事实对比与两个证伪世界 |
| [`examples/matrix-completion-demo/`](examples/matrix-completion-demo/) | 可运行的 Python 模拟：交互固定效应下 DiD 存在结构性偏差，低秩矩阵补全插补恢复真值——并演示秩敏感性这一失效模式 |

---

## 设计哲学

- **识别驱动，不是叙事驱动。** 写文章之前先把研究设计决定下来并压力测试通过。
- **一篇论文只讲一个贡献。** AER 编辑会枪毙"合格但常规的扩展"；围绕一个最锋利的主张重写。
- **跨领域可读性是硬筛选。** 一篇 labor 文章必须能让 public、macro、IO 经济学家也读懂，否则 desk-reject。
- **用现代计量，不要用 1990 年代的默认值。** TWFE → Callaway-Sant'Anna；first-stage F → Anderson-Rubin；朴素 RDD → 协变量调整的 local linear。
- **任何引用都不能凭记忆写。** 每条参考文献都对照抓取到的源记录核验；每句"X 发现了 Y"都对照原文检查。
- **稿件必须先过自己的审稿人。** 投稿前必须通过全稿一致性审计（`aer-consistency`）和对抗性模拟审稿（`aer-referee-sim`）。
- **复现包是论文的一部分。** README 跑不通就是 AEA Data Editor 卡你的理由。
- **编辑的时间是最稀缺资源。** Cover letter ≤ 200 词。回复信先引用 comment、再说 action、再标出修改后的位置。

完整论述见 [docs/design-principles.md](docs/design-principles.md)。

关键参考文档：

- [Roadmap](docs/roadmap.md) — "全网第一自动实证 repo" 的操作性定义与月度冲刺计划
- [Quality scorecard](docs/quality-scorecard.md) — 机器生成的全门通过状态一页汇总
  （`make scorecard` 重新生成，preflight 防漂移）
- [Academic Research Skills reference review](docs/academic-research-skills-review.md) —
  本轮参考外部 ARS 仓库后的取舍与本地改动记录
- [Desk-rejection audit](docs/desk-rejection-audit.md) — 从编辑/审稿人视角做的
  投稿前 no-go 检查
- [Methods reference](docs/methods-reference.md) — 估计量默认值、诊断、包调用，
  以及 BibTeX key
- [Style guide](docs/style-guide.md) — 经济学论文的句子与段落级文风规则，
  外加 AI 痕迹清除清单
- [Referee report rubric](docs/referee-report-rubric.md) — `aer-referee-sim`
  使用的 0-5 锚定评分维度与校准的 verdict 映射
- [SkillOpt evaluation protocol](docs/skillopt-evaluation-protocol.md) —
  用固定场景和 gate 约束 skill 优化补丁
- [PNAS Nexus publication plan](docs/pnas-nexus-publication-plan.md) —
  审稿人式审计与一周合规改进计划
- [PNAS Nexus submission checklist](docs/pnas-nexus-submission-checklist.md) —
  稿件、数据、代码和图件的证据驱动终审清单
- [Source register](docs/source-register.md) — AEA 官方政策来源，以及 repo 中依赖
  这些政策的表面
- [Glossary](docs/glossary.md) — 期刊、识别、复现、回复信术语的共享词表

---

## 仓库结构

```text
AER-Skills/
├── README.md               (中文，主入口)
├── README.en.md            (英文，完整版)
├── LICENSE                 (MIT)
├── CHANGELOG.md            (版本历史)
├── CITATION.cff            (软件引用元数据)
├── Makefile                (校验、测试与安装快捷命令)
├── CONTRIBUTING.md         (并发 agent 工作流)
├── .github/
│   └── workflows/ci.yml    (结构校验 + 单元测试 + demo 数值冒烟)
├── .claude-plugin/
│   ├── plugin.json         (插件清单)
│   └── marketplace.json    (Claude Code marketplace 条目)
├── docs/
│   ├── academic-research-skills-review.md
│   ├── citation-integrity-protocol.md
│   ├── desk-rejection-audit.md
│   ├── design-principles.md
│   ├── glossary.md
│   ├── installation-claude.md
│   ├── installation-codex.md
│   ├── launch-kit/             (发布宣发材料包)
│   ├── methods-reference.md
│   ├── pnas-nexus-publication-plan.md
│   ├── pnas-nexus-submission-checklist.md
│   ├── quality-scorecard.md    (机器生成的门状态汇总)
│   ├── referee-report-rubric.md
│   ├── roadmap.md              (月度冲刺路线图)
│   ├── source-register.md
│   ├── style-guide.md
│   └── workflow-map.md
├── skills/                 (14 个 skill 目录 — SKILL.md + agents/openai.yaml)
│   ├── aer-workflow/
│   ├── aer-topic-selection/
│   ├── aer-literature/
│   ├── aer-identification/
│   ├── aer-robustness/
│   ├── aer-paper-body/
│   ├── aer-introduction/
│   ├── aer-tables-figures/
│   ├── aer-consistency/    (附 scripts/audit_manuscript.py)
│   ├── aer-referee-sim/
│   ├── aer-replication/
│   ├── aer-submission/
│   ├── aer-rebuttal/
│   └── aer-statspai/       (可选实现引擎)
├── templates/              (即插即用流水线，三种语言都有)
│   ├── stata/
│   ├── r/
│   └── python/
├── scripts/
│   ├── install_skills.py
│   ├── quality_scorecard.py    (记分卡生成器 + 漂移门)
│   ├── run_example_smoke.py    (demo 数值冒烟门)
│   ├── run_skillopt_gate.py    (SkillOpt 路由门)
│   ├── scaffold_project.py
│   ├── skill_audit.py          (SkillOpt 文档质量审计)
│   ├── validate_repo.py
│   ├── verify_citations.py     (引用完整性核验器)
│   └── citation_gold/          (离线 gold set + 录制的索引响应)
├── tests/                  (质量工具的单元测试，make test)
└── examples/
    ├── end-to-end-walkthrough.md
    ├── aer-exemplars.md
    ├── intro-example.md
    ├── rebuttal-example.md
    ├── dml-plr-demo/           (以及其余 15 个可运行 demo)
    └── replication-package-skeleton/
        ├── data/codebook/source-register.md
        ├── docs/exhibit-register.md
        └── docs/claim-evidence-ledger.csv
```

---

## 适用 / 不适用

**适用：**

- *American Economic Review*（长文，≤ 40 页）
- *American Economic Review: Insights*（短文，≤ 7,000 词减每个 exhibit 200 词；5 个 exhibits 时 ≤ 6,000 词）
- *American Economic Journal* 系列（Applied / Policy / Macro / Micro）
- 实证或理论经济学稿件
- 田野实验（含 AEA RCT Registry 流程）

**不适用：**

- 金融三大刊工具箱（JF / JFE / RFS 有自己的规范）
- 纯理论栈（没有证明撰写助手）
- 通用 "academic writing" 库

---

## 致谢

Skill 架构参考自 [Boom5426/Nature-Paper-Skills](https://github.com/Boom5426/Nature-Paper-Skills) 与 [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)。方法论提炼自 **Keith Head**、**Marc F. Bellemare**、**Susan Athey**、**Berk-Harvey-Hirshleifer**、**AEA Data Editor's Office** 以及 *Annual Review of Economics* 的公开资料。

---

## 协议

[MIT](LICENSE)。
