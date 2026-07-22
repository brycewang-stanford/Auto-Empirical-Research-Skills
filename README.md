[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/brycewang-stanford/Auto-Empirical-Research-Skills?style=social)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Validate catalog](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/brycewang-stanford/Auto-Empirical-Research-Skills/badge)](https://scorecard.dev/viewer/?uri=github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![Security audit: baseline 52/52 CLEAN](https://img.shields.io/badge/security%20audit-baseline%2052%2F52%20CLEAN-brightgreen)](SECURITY-SCAN-REPORT.md)
[![Rigor coverage](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fbrycewang-stanford%2FAuto-Empirical-Research-Skills%2Fmain%2Fdocs%2Fbadges%2Frigor-coverage.json)](docs/RIGOR_COVERAGE.md)
[![Powered by StatsPAI](https://img.shields.io/badge/powered%20by-StatsPAI-orange)](https://github.com/brycewang-stanford/StatsPAI)

# Auto-Empirical Research Skills (AERS)

> **📌 文档结构（2026-07-22 起）：** 本文件是**中文默认入口** —— banner + badges + 信任面 + 9 阶段流水线速览 + 74 行合集总表。
> 每个合集的**完整描述、按用途分组、精确数字、验证方法**在 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)（扩展正文，总表行内的 `→` 直接跳转到对应锚点）。
>
> English version: [`README-en.md`](README-en.md) · 中文扩展正文：[`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md) · [`README-zh-CN.md`](README-zh-CN.md) 已弃用（重定向占位）

<div align="center">

**🌐 语言: [English](README-en.md) | 简体中文（默认） | [繁體中文](README-zh-TW.md) | [日本語](README-ja.md) | [한국어](README-ko.md)**

<br/>

  <table>
    <tr>
      <td align="center">
        <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="300" /></a>
      </td>
      <td width="72"></td>
      <td align="center">
        <img src="images/stanford-reap-logo.png" alt="Stanford REAP - Center on China's Economy & Institutions" width="440" />
      </td>
    </tr>
  </table>

  <br/>

  <strong>Stanford REAP × CoPaper.AI</strong> · 实证研究 AI 工具的学术工业级产品<br/>
  <sub>由斯坦福实证研究方法论团队打造，覆盖从数据清洗到顶刊投稿的完整工作流</sub>

  <br/>
  <br/>

  <img src="images/aers-readme-cover-cn.png" alt="实证研究智能体技能大全封面图" width="100%" />

  <br/>
</div>

> ### 🚀 New here? Open the **[Skill Search →](docs/search.html)** to filter all 1,094 skills by method, stage, language, and license. The 5-minute tour (`make quickstart`) prints the same picture in your terminal.
>
> ### 🇨🇳 **中文用户从本文件开始**（流水线速览 + 74 行总表），每个合集的完整描述见 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)。📖 **English readers:** see [`README-en.md`](README-en.md).

---

### 信任面 · Trust surface (rigor stats)

| Rigor lane | Count | Where |
|---|---|---|
| Numeric **benchmark tasks** — gold values recomputed from real data each run | **17** | [`benchmark/`](benchmark/) |
| Behavioral **eval scenarios / rubric items** | **37 / 183** | [`eval-harness/`](eval-harness/) |

> Full trust overview: [`docs/TRUST.md`](docs/TRUST.md) · [`docs/RIGOR_COVERAGE.md`](docs/RIGOR_COVERAGE.md)

---

## 中文文档结构

中文内容分两级维护，各司其职：

- **本文件（README.md，GitHub 默认入口）**：banner、badges、信任面、9 阶段流水线速览、74 行合集总表。
- **[`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)（扩展正文）**：每个合集的完整描述（`#skill-NN` 锚点）、按用途分组、精确数字、2 分钟验证、三层信任、旗舰流水线详解、贡献与引用。总表行内的 `→` 直接跳到对应锚点。
- **其他语言**：[`README-en.md`](README-en.md) · [`README-zh-TW.md`](README-zh-TW.md) · [`README-ja.md`](README-ja.md) · [`README-ko.md`](README-ko.md)

> [!NOTE]
> **维护规则：** 改合集总表 → 本文件与 CONTENT_ZH.md 的锚点表**两处同步**；改合集详情 / 分组 / 数字 → 只改 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md)。统计数字（合集数 / skill 数）以 [`catalog/skills.json`](catalog/skills.json) 为准，由 `make validate` 的 readme-stats 检查器守护。
>
> **贡献者（Contributors）：** 提交前请在本地跑通完整门禁 `make check`（catalog 校验 + 链接 + 单元测试 + eval-harness + benchmark）。详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。
>
> **旧版归档：** [`README-zh-CN.md`](README-zh-CN.md) 已弃用，仅作向后兼容的重定向占位。

---

## 🚀 从一个 idea 到一篇论文：社科实证研究 · 端到端流水线（全自动、可介入）

> **AERS 不只是 74 个散装 skill —— 它能陪你走完一篇论文。** 从模糊 idea → 选题精炼 → 文献综述 → 数据获取 → 识别策略 → 估计建模 → 稳健性审计 → 出版级表格 / 图形 → 写作与同行评审 → 降 AIGC → 投稿。**端到端、全自动、每一步都可被人介入**（中间任何一步你都可以接过去手工改方法、补变量、加稳健性，再让流水线自动接上跑）。

### 9 阶段流水线 · 每一步都覆盖到具体 skill

| # | 阶段 | 关键 skills（点合集名进目录，`→` 进完整说明） |
|:--:|:--|:--|
| 1️⃣ | **选题精炼** — Agent 把模糊想法收紧成"可证伪 + 可执行"的研究问题 | · [25 Diverga](skills/25-HosungYou-Diverga/) · [33 claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) · [05 research-superpower](skills/05-kthorn-research-superpower/) · [11 compound-science](skills/11-James-Traina-compound-science/) |
| 2️⃣ | **文献综述** — 检索 · 筛选 · PRISMA 流程 · 批判性阅读 · 主题分析 | · [36 literature-review-skill](skills/36-taoyunudt-literature-review-skill/) · [24 academic-research-skills](skills/24-Imbad0202-academic-research-skills/) · [59 openalex-skill](skills/59-shiquda-openalex-skill/) · [68 research-productivity-skills](skills/68-research-productivity-skills/) · [53 thematic-analysis](skills/53-keemanxp-thematic-analysis-skill/) |
| 3️⃣ | **数据获取** — 公开数据库 · API · 网页抓取 · 数据清洗 | · [33 claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) · [68 research-productivity-skills](skills/68-research-productivity-skills/) · [32 stata-skill](skills/32-dylantmoore-stata-skill/) · [57 edgartools](skills/57-dgunning-edgartools/) |
| 4️⃣ | **识别策略** — DiD / RD / IV / SCM / DML / matching 全覆盖 | · ⭐ [00 StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/) 🔥 · [10 causal-inference-mixtape](skills/10-Jill0099-causal-inference-mixtape/) · [13 MixtapeTools](skills/13-scunning1975-MixtapeTools/) · [51 CausalPy](skills/51-pymc-labs-CausalPy/) · [63 scientific-agent-skills](skills/63-tondevrel-scientific-agent-skills/) |
| 5️⃣ | **估计建模** — Python / Stata / R 三栈，900+ 估计器 | · ⭐ [00.1 Full Empirical · Python](skills/00.1-Full-empirical-analysis-skill_Python/) · ⭐ [00.2 Full Empirical · Stata](skills/00.2-Full-empirical-analysis-skill_Stata/) · ⭐ [00.3 Full Empirical · R](skills/00.3-Full-empirical-analysis-skill_R/) · [40 pyfixest](skills/40-py-econometrics-pyfixest/) · [39 marginaleffects](skills/39-vincentarelbundock-marginaleffects/) · [09 awesome-econ-ai](skills/09-meleantonio-awesome-econ-ai-stuff/) |
| 6️⃣ | **稳健性审计** — 复现包检查 · Honest-DiD · R&R 模拟 | · [41 sewage-econometrics-check](skills/41-sticerd-eee-sewage-econometrics-check/) · ⭐ [50 AER-skills](skills/50-brycewang-aer-skills/) · [21 AI-research-feedback](skills/21-claesbackman-AI-research-feedback/) |
| 7️⃣ | **表格 & 图形** — 期刊出版级排版 · LaTeX 嵌入 | · ⭐ [00 StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/) · [07 AI-Research-SKILLs](skills/07-Orchestra-Research-AI-Research-SKILLs/) · [33 claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) · [08 latex-document-skill](skills/08-ndpvt-web-latex-document-skill/) |
| 8️⃣ | **写作 & 同行评审** — LaTeX / Quarto · 仿审稿人 · 校对 | · [06 stats-paper-writing](skills/06-fuhaoda-stats-paper-writing/) · [04 scientific-writer](skills/04-K-Dense-AI-claude-scientific-writer/) · [22 christopherkenny-skills](skills/22-christopherkenny-skills/) · [38 academic-proofreader](skills/38-peternka-academic-proofreader/) · [56 econ-writing-skill](skills/56-hanlulong-econ-writing-skill/) · [16 clo-author](skills/16-hsantanna88-clo-author/) |
| 9️⃣ | **降 AIGC & 投稿** — 知网 / 万方 / Turnitin / 23 类 AI 痕迹模式 | · ⭐ [48 chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/) 🇨🇳 · [44 humanizer_academic](skills/44-matsuikentaro1-humanizer_academic/) · [45 deslop](skills/45-stephenturner-skill-deslop/) · [46 stop-slop](skills/46-hardikpandya-stop-slop/) · [47 avoid-ai-writing](skills/47-conorbronsdon-avoid-ai-writing/) · [49 humanize-chinese](skills/49-voidborne-d-humanize-chinese/) |

### 🎼 元编排：⭐ [69 Paper-WorkFlow](skills/69-Paper-WorkFlow/) —— 一键串起来

[`Paper-WorkFlow`](skills/69-Paper-WorkFlow/) 是 AERS 的"指挥棒"，它把上面 9 个阶段的 skill 串成 **一条按键即运行的端到端流水线**。
你在 IDE 入口给它一句自然语言：

> *"开一个新论文项目：空气污染与中国劳动力市场，CS 设计 + 省级面板"*

它会自动按顺序调：

1. ⭐ [00 StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/) → `sp.csdid(...)` 给出 CS-DID 估计草案 + 写出估计方程与识别假设
2. [33 claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) → 抓变量定义 / 数据源候选 / 相关文献
3. ⭐ [00 StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/) → 真跑 `sp.feols(...)` + `sp.honest_did(...)`
4. [41 sewage-econometrics-check](skills/41-sticerd-eee-sewage-econometrics-check/) → 10 项复现包审计 + 稳健性体检
5. ⭐ [00 StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/) + [07 AI-Research-SKILLs](skills/07-Orchestra-Research-AI-Research-SKILLs/) → 出 Table 1–5 + 期刊级图
6. [38 academic-proofreader](skills/38-peternka-academic-proofreader/) → 通读 + §comment 标"审稿人会挑刺的位置"
7. [56 econ-writing-skill](skills/56-hanlulong-econ-writing-skill/) 起草初稿 + ⭐ [48 chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/) 🇨🇳 + [45 deslop](skills/45-stephenturner-skill-deslop/) 过知网 / Turnitin

**任何阶段你都可以手动介入** —— 上一阶段的产物全部落盘（产物-幂等 pipeline），你接过去改方法、补控制、加稳健性，再让流水线自动接下去跑。这就是"全自动 + 可介入"。

### 🏆 7 个 Stanford REAP × CoPaper.AI 自研 skill —— 是整个流水线的主干

| ⭐ Skill | 在流水线里的角色 |
|:--|:--|
| [00 StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/) 🔥 | **因果引擎**：900+ 函数，`sp.causal(...)` 一行跑闭环（DID / RD / IV / SCM / DML / matching） |
| [00.1 Full Empirical · Python](skills/00.1-Full-empirical-analysis-skill_Python/) 📘 | 显式 Python 栈（pandas / statsmodels / linearmodels / pyfixest） |
| [00.2 Full Empirical · Stata](skills/00.2-Full-empirical-analysis-skill_Stata/) 📊 | 显式 Stata 栈（reghdfe / ivreg2 / csdid / sdid / rdrobust） |
| [00.3 Full Empirical · R](skills/00.3-Full-empirical-analysis-skill_R/) 📗 | 显式 R 栈（tidyverse / fixest / did / HonestDiD）+ Quarto 渲染 |
| [48 chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/) 🇨🇳 | 面向知网 / 万方 / Turnitin 中文版的中文去 AIGC |
| [50 AER-skills](skills/50-brycewang-aer-skills/) 📕 | Top-5 经济学投稿套件：识别 → 稳健性 → R&R |
| [69 Paper-WorkFlow](skills/69-Paper-WorkFlow/) 🧭 | 元编排器，把上面 9 个阶段串成一键流水线 |

**为什么挑这 7 个？因为它们的行为都被基准钉死了** —— 不是营销口径，是对着已知答案反复跑过验证过的（[17 项数值 benchmark + 37 项行为评测 ↗](docs/CONTENT_ZH.md#你究竟得到什么精确数字)）。

### 看到这里 —— 完整 74 行合集目录

[↴ 直跳到下方 74 行总表（每个合集带 `#skill-NN` 锚点）](#-74-个核心-skills-合集一览00--70编号连续无空缺)。如果你更关心"这些 skill **怎么用**"而不是"有哪些 skill"，看 [📘 中文唯一权威正文](docs/CONTENT_ZH.md) 里的「按用途分组」与「旗舰流水线」两节。

---

## 🧰 74 个核心 Skills 合集一览（`00 → 70`，编号连续无空缺）

> **打开仓库 → 看见整座库。** 全部 **74 个合集 · 1,094 个 skill**，每一个都已 vendor 进本仓库，由 [`catalog/skills.json`](catalog/skills.json) 跟踪。**⭐ = Stanford REAP × CoPaper.AI 团队自研的 skill**；其余为精选、经安全审计的社区作品。
>
> **主题图例 —** 🚀 全流程与编排器 · 🎯 因果推断与计量经济学 · 📚 文献与研究设计 · ✍️ 写作 / 编辑 / 去 AIGC · 📑 引用 / 复现 / 同行评审 · 🛠️ 数据 / 工具 / 基础设施
>
> **点击【→】** 跳转到 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md) 中该合集的完整描述；**点击合集名** 直接打开其目录。

| # | 合集 | 一句话 | 详情 |
|--:|:--|:--|:--|
| ⭐ [00](skills/00-Full-empirical-analysis-skill_StatsPAI/) | **StatsPAI** 🔥 | 因果引擎 · Agent-native Python DSL：`sp.causal(...)` 一行跑闭环（DID/RD/IV/SCM/DML，900+ 函数） | [→](docs/CONTENT_ZH.md#skill-00) |
| ⭐ [00.1](skills/00.1-Full-empirical-analysis-skill_Python/) | **Full Empirical · Python** 📘 | 显式栈：`pandas` · `statsmodels` · `linearmodels` · `pyfixest` | [→](docs/CONTENT_ZH.md#skill-00-1) |
| ⭐ [00.2](skills/00.2-Full-empirical-analysis-skill_Stata/) | **Full Empirical · Stata** 📊 | `reghdfe` · `ivreg2` · `csdid` · `sdid` · `rdrobust` 复现包 | [→](docs/CONTENT_ZH.md#skill-00-2) |
| ⭐ [00.3](skills/00.3-Full-empirical-analysis-skill_R/) | **Full Empirical · R** 📗 | tidyverse · `fixest` · `did` · `HonestDiD` + Quarto 渲染 | [→](docs/CONTENT_ZH.md#skill-00-3) |
| [01](skills/01-lishix520-academic-paper-skills/) | academic-paper-skills | 大纲 → 手稿写作 + 7 维审稿人模拟 | [→](docs/CONTENT_ZH.md#skill-01) |
| [02](skills/02-luwill-research-skills/) | research-skills | 医学影像综述、提案、论文转幻灯片 | [→](docs/CONTENT_ZH.md#skill-02) |
| [03](skills/03-K-Dense-AI-claude-scientific-skills/) | scientific-skills | 假设生成 + 28 个科学数据库 | [→](docs/CONTENT_ZH.md#skill-03) |
| [04](skills/04-K-Dense-AI-claude-scientific-writer/) | scientific-writer | 引用管理 + 科学写作 | [→](docs/CONTENT_ZH.md#skill-04) |
| [05](skills/05-kthorn-research-superpower/) | research-superpower | 系统化检索、筛选与引文溯源 | [→](docs/CONTENT_ZH.md#skill-05) |
| [06](skills/06-fuhaoda-stats-paper-writing/) | stats-paper-writing | 端到端 LaTeX 统计论文写作 | [→](docs/CONTENT_ZH.md#skill-06) |
| [07](skills/07-Orchestra-Research-AI-Research-SKILLs/) | AI-Research-SKILLs | 发表级 ML 图表、LaTeX、引文核验 | [→](docs/CONTENT_ZH.md#skill-07) |
| [08](skills/08-ndpvt-web-latex-document-skill/) | latex-document-skill | 创建 / 编译任意 LaTeX 文档为 PDF | [→](docs/CONTENT_ZH.md#skill-08) |
| [09](skills/09-meleantonio-awesome-econ-ai-stuff/) | awesome-econ-ai | Python 面板数据分析（`linearmodels`） | [→](docs/CONTENT_ZH.md#skill-09) |
| [10](skills/10-Jill0099-causal-inference-mixtape/) | causal-inference-mixtape | DID / IV / RDD / SCM 模板（Cunningham） | [→](docs/CONTENT_ZH.md#skill-10) |
| [11](skills/11-James-Traina-compound-science/) | compound-science | 面向定量社会科学的贝叶斯估计 | [→](docs/CONTENT_ZH.md#skill-11) |
| [12](skills/12-pedrohcgs-claude-code-my-workflow/) | claude-code-my-workflow | 提交 → PR → 合并的研究工作流（Emory） | [→](docs/CONTENT_ZH.md#skill-12) |
| [13](skills/13-scunning1975-MixtapeTools/) | MixtapeTools | Cunningham 的因果推断工具集与讲义 | [→](docs/CONTENT_ZH.md#skill-13) |
| [14](skills/14-luischanci-claude-code-research-starter/) | research-starter | R 中的 IV / DiD / RDD，含完整诊断 | [→](docs/CONTENT_ZH.md#skill-14) |
| [15](skills/15-Felpix-Studios-social-science-research/) | social-science-research | R 或 Python 端到端数据分析 | [→](docs/CONTENT_ZH.md#skill-15) |
| [16](skills/16-hsantanna88-clo-author/) | clo-author | 多代理数据分析（R / Stata / Python） | [→](docs/CONTENT_ZH.md#skill-16) |
| [17](skills/17-DAAF-Contribution-Community-daaf/) | DAAF | 安全意识代理框架（32 条 deny rule） | [→](docs/CONTENT_ZH.md#skill-17) |
| [18](skills/18-jusi-aalto-stata-accounting-research/) | stata-accounting | 来自 126 篇 *JAR* 论文的实测 Stata 范式 | [→](docs/CONTENT_ZH.md#skill-18) |
| [19](skills/19-CuellarC05-vera-economic-intelligence/) | vera-economic-intelligence | 经济情报 / 政策研究情报工作流 | [→](docs/CONTENT_ZH.md#skill-19) |
| [20](skills/20-wenddymacro-python-econ-skill/) | python-econ-skill | DSGE / HANK 与定量经济计算 | [→](docs/CONTENT_ZH.md#skill-20) |
| [21](skills/21-claesbackman-AI-research-feedback/) | AI-research-feedback | 用 AI 同行评审生成结构化反馈 | [→](docs/CONTENT_ZH.md#skill-21) |
| [22](skills/22-christopherkenny-skills/) | christopherkenny-skills | 面向 Quarto（`.qmd`）的 APSA 风格检查器 | [→](docs/CONTENT_ZH.md#skill-22) |
| [23](skills/23-Learning-Bayesian-Statistics-baygent-skills/) | baygent | 带护栏的 PyMC / Arviz 贝叶斯工作流 | [→](docs/CONTENT_ZH.md#skill-23) |
| [24](skills/24-Imbad0202-academic-research-skills/) | academic-research-skills | 5 审稿人多视角论文评审 | [→](docs/CONTENT_ZH.md#skill-24) |
| [25](skills/25-HosungYou-Diverga/) | Diverga | 研究问题精炼器（抗模式坍缩） | [→](docs/CONTENT_ZH.md#skill-25) |
| [26](skills/26-Data-Wise-scholar/) | scholar | 统计算法设计与文档 | [→](docs/CONTENT_ZH.md#skill-26) |
| [27](skills/27-dariia-m-my_claude_skills/) | my_claude_skills | 经济学摘要写作指南 | [→](docs/CONTENT_ZH.md#skill-27) |
| [28](skills/28-maxwell2732-paper-replicate-agent-demo/) | paper-replicate-agent | 论文复现代理演示 | [→](docs/CONTENT_ZH.md#skill-28) |
| [29](skills/29-quarcs-lab-project20XXy/) | project20XXy | 可复现手稿 + notebook 项目 | [→](docs/CONTENT_ZH.md#skill-29) |
| [30](skills/30-zirui-song-claude-skills/) | zirui-song-claude-skills | Zirui Song 的研究辅助 Claude 技能集 | [→](docs/CONTENT_ZH.md#skill-30) |
| [31](skills/31-thalysandratos-claude-code-skills/) | claude-code-skills | Python 面板数据分析 | [→](docs/CONTENT_ZH.md#skill-31) |
| [32](skills/32-dylantmoore-stata-skill/) | stata-skill | 高性能 Stata C/C++ 插件 | [→](docs/CONTENT_ZH.md#skill-32) |
| [33](skills/33-Galaxy-Dawn-claude-scholar/) | claude-scholar | 研究全生命周期：选题 → 综述 → 实验 → 审稿回复 | [→](docs/CONTENT_ZH.md#skill-33) |
| [34](skills/34-andrehuang-research-companion/) | research-companion | 头脑风暴、评估并决策研究方向 | [→](docs/CONTENT_ZH.md#skill-34) |
| [35](skills/35-bahayonghang-academic-writing-skills/) | academic-writing-skills | 面向投稿场所的工业 AI 文献研究 | [→](docs/CONTENT_ZH.md#skill-35) |
| [36](skills/36-taoyunudt-literature-review-skill/) | literature-review-skill | 完整文献综述工作流（中文） | [→](docs/CONTENT_ZH.md#skill-36) |
| [37](skills/37-IlanStrauss-ai-skills/) | IlanStrauss-ai-skills | Ilan Strauss 经济学研究 AI 工作流 | [→](docs/CONTENT_ZH.md#skill-37) |
| [38](skills/38-peternka-academic-proofreader/) | academic-proofreader | 学术校对 | [→](docs/CONTENT_ZH.md#skill-38) |
| [39](skills/39-vincentarelbundock-marginaleffects/) | marginaleffects | 预测、斜率与比较（R / Python） | [→](docs/CONTENT_ZH.md#skill-39) |
| [40](skills/40-py-econometrics-pyfixest/) | pyfixest | Python 中的快速固定效应估计 | [→](docs/CONTENT_ZH.md#skill-40) |
| [41](skills/41-sticerd-eee-sewage-econometrics-check/) | sewage-econometrics-check | 10 项复现包审计 | [→](docs/CONTENT_ZH.md#skill-41) |
| [42](skills/42-wanshuiyin-ARIS/) | ARIS | 自主「research-in-sleep」代理，端到端 | [→](docs/CONTENT_ZH.md#skill-42) |
| [43](skills/43-wentorai-research-plugins/) | research-plugins | 478 个研究插件：数据可视化、领域、基础设施 | [→](docs/CONTENT_ZH.md#skill-43) |
| [44](skills/44-matsuikentaro1-humanizer_academic/) | humanizer_academic | 为医学/学术手稿去 AI 味（23 类模式） | [→](docs/CONTENT_ZH.md#skill-44) |
| [45](skills/45-stephenturner-skill-deslop/) | deslop | 去除 AI 写作痕迹（5 维评分） | [→](docs/CONTENT_ZH.md#skill-45) |
| [46](skills/46-hardikpandya-stop-slop/) | stop-slop | 三层 AI 痕迹检测与改写 | [→](docs/CONTENT_ZH.md#skill-46) |
| [47](skills/47-conorbronsdon-avoid-ai-writing/) | avoid-ai-writing | 审计 → 改写 → 二次审计 AI 味（留痕） | [→](docs/CONTENT_ZH.md#skill-47) |
| ⭐ [48](skills/48-copaper-ai-chinese-de-aigc/) | **chinese-de-aigc** 🇨🇳 | 面向知网 / 万方 / Turnitin 中文版的中文去 AIGC | [→](docs/CONTENT_ZH.md#skill-48) |
| [49](skills/49-voidborne-d-humanize-chinese/) | humanize-chinese | 检测并人性化 AI 生成的中文文本 | [→](docs/CONTENT_ZH.md#skill-49) |
| ⭐ [50](skills/50-brycewang-aer-skills/) | **AER-skills** 📕 | Top-5 经济学投稿套件：识别 → 稳健性 → R&R | [→](docs/CONTENT_ZH.md#skill-50) |
| [51](skills/51-pymc-labs-CausalPy/) | CausalPy | 贝叶斯准实验（PyMC Labs） | [→](docs/CONTENT_ZH.md#skill-51) |
| [52](skills/52-keemanxp-slr-prisma/) | slr-prisma | 系统文献综述，PRISMA 2020 | [→](docs/CONTENT_ZH.md#skill-52) |
| [53](skills/53-keemanxp-thematic-analysis-skill/) | thematic-analysis | Braun & Clarke 六阶段定性主题分析 | [→](docs/CONTENT_ZH.md#skill-53) |
| [54](skills/54-scdenney-open-science-skills/) | open-science-skills | 引用一致性、DOI 与论据支撑审计 | [→](docs/CONTENT_ZH.md#skill-54) |
| [55](skills/55-ab604-claude-code-r-skills/) | r-skills | R 中用 `brms` 做贝叶斯推断 | [→](docs/CONTENT_ZH.md#skill-55) |
| [56](skills/56-hanlulong-econ-writing-skill/) | econ-writing-skill | 综合 50+ 顶级指南的经济学写作 | [→](docs/CONTENT_ZH.md#skill-56) |
| [57](skills/57-dgunning-edgartools/) | edgartools | 查询与分析 SEC 文件 | [→](docs/CONTENT_ZH.md#skill-57) |
| [58](skills/58-charlescoverdale-econstack/) | econstack | 政策简报（UK GES / AU Treasury） | [→](docs/CONTENT_ZH.md#skill-58) |
| [59](skills/59-shiquda-openalex-skill/) | openalex-skill | 通过 OpenAlex 查询 2.4 亿+ 学术作品 | [→](docs/CONTENT_ZH.md#skill-59) |
| [60](skills/60-regisely-superpapers/) | superpapers | 综合性实证研究支持套件 | [→](docs/CONTENT_ZH.md#skill-60) |
| [61](skills/61-phdemotions-research-methods/) | research-methods | 与预注册匹配的验证性检验 | [→](docs/CONTENT_ZH.md#skill-61) |
| [62](skills/62-PHY041-claude-skill-citation-checker/) | citation-checker | 对照 CrossRef / S2 / OpenAlex 核验引用 | [→](docs/CONTENT_ZH.md#skill-62) |
| [63](skills/63-tondevrel-scientific-agent-skills/) | scientific-agent-skills | DoWhy 识别–估计–反驳框架 | [→](docs/CONTENT_ZH.md#skill-63) |
| [64](skills/64-tmonk-mcp-stata/) | mcp-stata | 20 个 Stata 因果推断与复现 skill | [→](docs/CONTENT_ZH.md#skill-64) |
| [65](skills/65-game-theory-paper-writer/) | game-theory-paper-writer | 生成并压力测试博弈论论文 | [→](docs/CONTENT_ZH.md#skill-65) |
| [66](skills/66-zheng-siyao-empirical-research-skills/) | empirical-research-skills | 面向大型面板的 R 性能优化 | [→](docs/CONTENT_ZH.md#skill-66) |
| [67](skills/67-econfin-workflow-toolkit/) | econfin-workflow-toolkit | 中国公司金融实证工作流，从提案到论文 | [→](docs/CONTENT_ZH.md#skill-67) |
| [68](skills/68-research-productivity-skills/) | research-productivity-skills | 论文检索、SSRN、DOI 查询、下载 | [→](docs/CONTENT_ZH.md#skill-68) |
| ⭐ [69](skills/69-Paper-WorkFlow/) | **Paper-WorkFlow** 🧭 | 元编排器，串起整个社会科学论文流水线 | [→](docs/CONTENT_ZH.md#skill-69) |
| [70](skills/70-ssci-polish/) | ssci-polish ✍️ | SSCI / SCI 英文论文语言润色（语法、可读性、学术语气） | [→](docs/CONTENT_ZH.md#skill-70) |

> **想看更详细的描述（主题分类、字段、统计）？** 见 [`docs/CONTENT_ZH.md`](docs/CONTENT_ZH.md) 中标注 `#skill-NN` 锚点的同一张表 —— 它是每个合集的完整描述所在的扩展正文。

---

<div align="center">

**AI 是放大器，不是替代品。它替你做最耗时的"搬砖"，你保留最核心的"判断"。**

<br/>

<table>
  <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="220" /></a>
    </td>
    <td width="40"></td>
    <td align="center">
      <img src="images/stanford-reap-logo.png" alt="Stanford REAP" width="320" />
    </td>
  </tr>
</table>

<sub><strong>Stanford REAP × CoPaper.AI</strong> · 实证研究 AI 工具的学术工业级产品</sub>

<br/>

<table>
 <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-qrcode.png" alt="扫码访问 copaper.ai" width="180" /></a><br/>
      <strong>扫码访问 <a href="https://copaper.ai">copaper.ai</a></strong>
    </td>
    <td align="center">
      <img src="images/copaper-wechat.jpg" alt="CoPaper.AI 公众号" width="180" /><br/>
      <strong>关注公众号「CoPaper.AI」</strong>
    </td>
  </tr>
</table>

内置 20 个方法论 skill · 20 分钟完成实证论文 · 自研 <a href="https://github.com/brycewang-stanford/StatsPAI"><strong>StatsPAI</strong></a>（900+ 函数 / MIT 开源）

</div>
