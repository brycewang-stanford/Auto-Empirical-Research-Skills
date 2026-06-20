# Auto-Empirical Research Skills (AERS)

<div align="center">

**🌐 语言: [English](README.md) | 简体中文 | [繁體中文](README-zh-TW.md) | [日本語](README-ja.md) | [한국어](README-ko.md)**

<br/>

  <img src="images/aers-readme-cover-cn.png" alt="实证研究智能体技能大全封面图" width="100%" />

  <br/>

  <table>
    <tr>
      <td align="center">
        <a href="https://copaper.ai"><img src="images/copaper-logo.png" alt="CoPaper.AI" width="260" /></a>
      </td>
      <td width="60"></td>
      <td align="center">
        <img src="images/stanford-reap-logo.png" alt="Stanford REAP - Center on China's Economy & Institutions" width="380" />
      </td>
    </tr>
  </table>

  <br/>

  <strong>Stanford REAP × CoPaper.AI</strong> · 实证研究 AI 工具的学术工业级产品<br/>
  <sub>由斯坦福实证研究方法论团队打造，覆盖从数据清洗到顶刊投稿的完整工作流</sub>

  <br/>
</div>

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/brycewang-stanford/Auto-Empirical-Research-Skills?style=social)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Validate catalog](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml/badge.svg)](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/actions/workflows/validate-catalog.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/brycewang-stanford/Auto-Empirical-Research-Skills/badge)](https://scorecard.dev/viewer/?uri=github.com/brycewang-stanford/Auto-Empirical-Research-Skills)
[![Security audit: 52/52 CLEAN](https://img.shields.io/badge/security%20audit-52%2F52%20CLEAN-brightgreen)](SECURITY-SCAN-REPORT.md)
[![Powered by StatsPAI](https://img.shields.io/badge/powered%20by-StatsPAI-orange)](https://github.com/brycewang-stanford/StatsPAI)

---

## 全部 69 个 skill 合集一览

> **打开仓库 → 看见整座库。** 全部 **69 个合集 · 1,145 个 skill**，从 `00 → 69` 编号，每一个都**已 vendor 进本仓库**（不仅是外链），并由 [`catalog/skills.json`](catalog/skills.json) 跟踪。**点击任意一行即可打开其文件夹。** **⭐ = 由 Stanford REAP × CoPaper.AI 团队自研的 skill**；其余均为精选、经安全审计的社区作品。
>
> **主题图例 —** 🚀 全流程与编排器 · 🎯 因果推断与计量经济学 · 📚 文献与研究设计 · ✍️ 写作、编辑与去 AIGC · 📑 引用、复现与同行评审 · 🛠️ 数据、工具与基础设施

| # | 合集 | 功能 | 主题 | Skills |
|:--|:--|:--|:--:|--:|
| ⭐ **00** | **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)** 🔥 | Agent-native Python **DSL** —— 一个 `sp.causal(...)` 跑完 DID/RD/IV/SCM/DML | 🚀 | 1 |
| ⭐ **00.1** | **[Full Empirical · Python](skills/00.1-Full-empirical-analysis-skill_Python/)** 📘 | 显式栈：`pandas` · `statsmodels` · `linearmodels` · `pyfixest` | 🚀 | 1 |
| ⭐ **00.2** | **[Full Empirical · Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)** 📊 | `reghdfe` · `ivreg2` · `csdid` · `sdid` · `rdrobust` 复现包 | 🚀 | 1 |
| ⭐ **00.3** | **[Full Empirical · R](skills/00.3-Full-empirical-analysis-skill_R/)** 📗 | tidyverse · `fixest` · `did` · `HonestDiD`，通过 Quarto 渲染 | 🚀 | 1 |
| **01** | [academic-paper-skills](skills/01-lishix520-academic-paper-skills/) | 大纲 → 手稿写作 + 7 维审稿人模拟 | ✍️ | 2 |
| **02** | [research-skills](skills/02-luwill-research-skills/) | 医学影像综述、提案、论文转幻灯片 | 📚 | 3 |
| **03** | [scientific-skills](skills/03-K-Dense-AI-claude-scientific-skills/) | 假设生成 + 28 个科学数据库 | 📚 | 4 |
| **04** | [scientific-writer](skills/04-K-Dense-AI-claude-scientific-writer/) | 引用管理 + 科学写作 | ✍️ | 8 |
| **05** | [research-superpower](skills/05-kthorn-research-superpower/) | 系统化检索、筛选与引文溯源 | 📚 | 10 |
| **06** | [stats-paper-writing](skills/06-fuhaoda-stats-paper-writing/) | 端到端 LaTeX 统计论文写作 | ✍️ | 1 |
| **07** | [AI-Research-SKILLs](skills/07-Orchestra-Research-AI-Research-SKILLs/) | 发表级 ML 图表、LaTeX、引文核验 | 🛠️ | 3 |
| **08** | [latex-document-skill](skills/08-ndpvt-web-latex-document-skill/) | 创建 / 编译任意 LaTeX 文档为 PDF | 🛠️ | 1 |
| **09** | [awesome-econ-ai](skills/09-meleantonio-awesome-econ-ai-stuff/) | Python 面板数据分析（`linearmodels`） | 🎯 | 17 |
| **10** | [causal-inference-mixtape](skills/10-Jill0099-causal-inference-mixtape/) | DID / IV / RDD / SCM 模板（Cunningham） | 🎯 | 1 |
| **11** | [compound-science](skills/11-James-Traina-compound-science/) | 面向定量社会科学的贝叶斯估计 | 🎯 | 20 |
| **12** | [claude-code-my-workflow](skills/12-pedrohcgs-claude-code-my-workflow/) | 提交 → PR → 合并的研究工作流（Emory） | 🛠️ | 22 |
| **13** | [MixtapeTools](skills/13-scunning1975-MixtapeTools/) | Cunningham 的因果推断工具集与讲义 | 🎯 | 5 |
| **14** | [research-starter](skills/14-luischanci-claude-code-research-starter/) | R 中的 IV / DiD / RDD，含完整诊断 | 🎯 | 16 |
| **15** | [social-science-research](skills/15-Felpix-Studios-social-science-research/) | R 或 Python 端到端数据分析 | 🎯 | 12 |
| **16** | [clo-author](skills/16-hsantanna88-clo-author/) | 多代理数据分析（R / Stata / Python） | 🎯 | 10 |
| **17** | [DAAF](skills/17-DAAF-Contribution-Community-daaf/) | 安全意识代理框架（32 条 deny rule） | 🛠️ | 35 |
| **18** | [stata-accounting](skills/18-jusi-aalto-stata-accounting-research/) | 来自 126 篇 *JAR* 论文的实测 Stata 范式 | 🎯 | 1 |
| **20** | [python-econ-skill](skills/20-wenddymacro-python-econ-skill/) | DSGE / HANK 与定量经济计算 | 🎯 | 1 |
| **22** | [christopherkenny-skills](skills/22-christopherkenny-skills/) | 面向 Quarto（`.qmd`）的 APSA 风格检查器 | ✍️ | 11 |
| **23** | [baygent](skills/23-Learning-Bayesian-Statistics-baygent-skills/) | 带护栏的 PyMC / ArviZ 贝叶斯工作流 | 🎯 | 2 |
| **24** | [academic-research-skills](skills/24-Imbad0202-academic-research-skills/) | 5 审稿人多视角论文评审 | 📑 | 4 |
| **25** | [Diverga](skills/25-HosungYou-Diverga/) | 研究问题精炼器（抗模式坍缩） | 📚 | 34 |
| **26** | [scholar](skills/26-Data-Wise-scholar/) | 统计算法设计与文档 | 🎯 | 17 |
| **27** | [my_claude_skills](skills/27-dariia-m-my_claude_skills/) | 经济学摘要写作指南 | ✍️ | 6 |
| **28** | [paper-replicate-agent](skills/28-maxwell2732-paper-replicate-agent-demo/) | 论文复现代理演示 | 📑 | 11 |
| **29** | [project20XXy](skills/29-quarcs-lab-project20XXy/) | 可复现手稿 + notebook 项目 | 📑 | 24 |
| **31** | [claude-code-skills](skills/31-thalysandratos-claude-code-skills/) | Python 面板数据分析 | 🎯 | 13 |
| **32** | [stata-skill](skills/32-dylantmoore-stata-skill/) | 高性能 Stata C/C++ 插件 | 🛠️ | 3 |
| **33** | [claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) | 研究全生命周期：选题 → 综述 → 实验 → 审稿回复 | 🚀 | 47 |
| **34** | [research-companion](skills/34-andrehuang-research-companion/) | 头脑风暴、评估并决策研究方向 | 📚 | 1 |
| **35** | [academic-writing-skills](skills/35-bahayonghang-academic-writing-skills/) | 面向投稿场所的工业 AI 文献研究 | 📚 | 5 |
| **36** | [literature-review-skill](skills/36-taoyunudt-literature-review-skill/) | 完整文献综述工作流（中文） | 📚 | 1 |
| **38** | [academic-proofreader](skills/38-peternka-academic-proofreader/) | 学术校对 | ✍️ | 1 |
| **39** | [marginaleffects](skills/39-vincentarelbundock-marginaleffects/) | 预测、斜率与比较（R / Python） | 🎯 | 1 |
| **40** | [pyfixest](skills/40-py-econometrics-pyfixest/) | Python 中的快速固定效应估计 | 🎯 | 1 |
| **41** | [sewage-econometrics-check](skills/41-sticerd-eee-sewage-econometrics-check/) | 10 项复现包审计 | 📑 | 22 |
| **42** | [ARIS](skills/42-wanshuiyin-ARIS/) | 自主「research-in-sleep」代理，端到端 | 🚀 | 104 |
| **43** | [research-plugins](skills/43-wentorai-research-plugins/) | 478 个研究插件：数据可视化、领域、基础设施 | 🛠️ | 478 |
| **44** | [humanizer_academic](skills/44-matsuikentaro1-humanizer_academic/) | 为医学/学术手稿去 AI 味（23 类模式） | ✍️ | 1 |
| **45** | [deslop](skills/45-stephenturner-skill-deslop/) | 去除 AI 写作痕迹（5 维评分） | ✍️ | 1 |
| **46** | [stop-slop](skills/46-hardikpandya-stop-slop/) | 三层 AI 痕迹检测与改写 | ✍️ | 1 |
| **47** | [avoid-ai-writing](skills/47-conorbronsdon-avoid-ai-writing/) | 审计 → 改写 → 二次审计 AI 味（留痕） | ✍️ | 1 |
| ⭐ **48** | **[chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/)** 🇨🇳 | 面向知网 / 万方 / Turnitin 中文版的中文去 AIGC | ✍️ | 1 |
| **49** | [humanize-chinese](skills/49-voidborne-d-humanize-chinese/) | 检测并人性化 AI 生成的中文文本 | ✍️ | 1 |
| ⭐ **50** | **[AER-skills](skills/50-brycewang-aer-skills/)** 📕 | Top-5 经济学投稿套件：识别 → 稳健性 → R&R | 🚀 | 9 |
| **51** | [CausalPy](skills/51-pymc-labs-CausalPy/) | 贝叶斯准实验（PyMC Labs） | 🎯 | 3 |
| **52** | [slr-prisma](skills/52-keemanxp-slr-prisma/) | 系统文献综述，PRISMA 2020 | 📚 | 1 |
| **53** | [thematic-analysis](skills/53-keemanxp-thematic-analysis-skill/) | Braun & Clarke 六阶段定性主题分析 | 📚 | 1 |
| **54** | [open-science-skills](skills/54-scdenney-open-science-skills/) | 引用一致性、DOI 与论据支撑审计 | 📑 | 24 |
| **55** | [r-skills](skills/55-ab604-claude-code-r-skills/) | R 中用 `brms` 做贝叶斯推断 | 🎯 | 8 |
| **56** | [econ-writing-skill](skills/56-hanlulong-econ-writing-skill/) | 综合 50+ 顶级指南的经济学写作 | ✍️ | 1 |
| **57** | [edgartools](skills/57-dgunning-edgartools/) | 查询与分析 SEC 文件 | 🛠️ | 1 |
| **58** | [econstack](skills/58-charlescoverdale-econstack/) | 政策简报（UK GES / AU Treasury） | ✍️ | 7 |
| **59** | [openalex-skill](skills/59-shiquda-openalex-skill/) | 通过 OpenAlex 查询 2.4 亿+ 学术作品 | 📚 | 1 |
| **60** | [superpapers](skills/60-regisely-superpapers/) | 综合性实证研究支持套件 | 📚 | 16 |
| **61** | [research-methods](skills/61-phdemotions-research-methods/) | 与预注册匹配的验证性检验 | 🎯 | 9 |
| **62** | [citation-checker](skills/62-PHY041-claude-skill-citation-checker/) | 对照 CrossRef / S2 / OpenAlex 核验引用 | 📑 | 1 |
| **63** | [scientific-agent-skills](skills/63-tondevrel-scientific-agent-skills/) | DoWhy 识别–估计–反驳框架 | 🎯 | 2 |
| **64** | [mcp-stata](skills/64-tmonk-mcp-stata/) | 20 个 Stata 因果推断与复现 skill | 🎯 | 20 |
| **65** | [game-theory-paper-writer](skills/65-game-theory-paper-writer/) | 生成并压力测试博弈论论文 | ✍️ | 1 |
| **66** | [empirical-research-skills](skills/66-zheng-siyao-empirical-research-skills/) | 面向大型面板的 R 性能优化 | 🛠️ | 7 |
| **67** | [econfin-workflow-toolkit](skills/67-econfin-workflow-toolkit/) | 中国公司金融实证工作流，从提案到论文 | 🚀 | 46 |
| **68** | [research-productivity-skills](skills/68-research-productivity-skills/) | 论文检索、SSRN、DOI 查询、下载 | 🛠️ | 18 |
| ⭐ **69** | **[Paper-WorkFlow](skills/69-Paper-WorkFlow/)** 🧭 | 元编排器，串起整个社会科学论文流水线 | 🚀 | 1 |

> ⭐ **我们亲手打造的主干：** [StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)（因果引擎）· 显式的 [Python](skills/00.1-Full-empirical-analysis-skill_Python/) / [Stata](skills/00.2-Full-empirical-analysis-skill_Stata/) / [R](skills/00.3-Full-empirical-analysis-skill_R/) 全流程移植 · [AER-skills](skills/50-brycewang-aer-skills/)（Top-5 投稿套件）· [chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/) · [Paper-WorkFlow](skills/69-Paper-WorkFlow/)（元编排器）。它们是 AERS 的主干 —— 完整对比见 [旗舰流水线 skills ↓](#旗舰流水线-skills)。更想按用途浏览？见 [同样的 69 个，按用途分组 ↓](#69-个合集--按用途分组)。

---

**面向实证研究的专业级 Agent Skills 发行版。** 不是一份营销清单 —— 本仓库**自有并已编目 1,145 个 skill**，外加一套**数值基准 + 评测套件 + 安全审计 + CI** 把质量焊死，再叠加一张覆盖**生态 23,000+ skill / 119 个仓库**的精选地图。

AERS 同时是两样东西：(1) 一小撮**自研旗舰 skill**，能跑通完整实证流水线 —— 数据清洗 → 识别 → 估计 → 稳健性 → 表格图形 → 可投稿初稿；(2) 一份**精选、安全可控的目录**，按研究流程阶段组织整个实证研究 skill 生态。我们的差异化不在数量，而在于：旗舰 skill 的行为是**对着已知答案验证过的**，而不是嘴上声称的。

> [!NOTE]
> **已更名。** 本项目原名 *Awesome Agent Skills for Empirical Research*。GitHub 会自动重定向旧地址，但请更新你的本地 remote：
> ```bash
> git remote set-url origin https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
> ```

---

## 目录

- [**全部 69 个 skill 合集一览**（完整的 `00 → 69` 索引）](#全部-69-个-skill-合集一览)
  - [69 个合集 · 按用途分组](#69-个合集--按用途分组)
- [你究竟得到什么（精确数字）](#你究竟得到什么精确数字)
- [2 分钟自行验证](#2-分钟自行验证)
- [为什么值得信任 —— 三层信用锚点](#为什么值得信任--三层信用锚点)
- [旗舰流水线 skills](#旗舰流水线-skills)
- [从这里开始 —— 30 秒选一个 skill](#从这里开始--30-秒选一个-skill)
- [凭什么不只是 23K skill 的堆砌](#凭什么不只是-23k-skill-的堆砌)
- [浏览全景](#浏览全景)
  - [工具目录（tools/）](#工具目录tools自动化实证与因果推断工具)
  - [按研究流程](#按研究流程)
  - [综合型 skill 套件](#综合型-skill-套件)
  - [降 AIGC 检测率 & 学术去 AI 味](#降-aigc-检测率--学术去-ai-味)
  - [多代理系统 · MCP 服务器 · 平台 · 学习资源](#多代理系统--mcp-服务器--平台--学习资源)
- [安全扫描](#安全扫描)
- [更新日志](#更新日志)
- [贡献与引用](#贡献与引用)

---

## 69 个合集 · 按用途分组

> 与[顶部的顺序索引 ↑](#全部-69-个-skill-合集一览)同样是 **69 个合集 · 1,145 个 skill** —— 这里**按研究用途**重新排序，方便你直接跳到当前所处的阶段。**⭐ = 自研**（Stanford REAP × CoPaper.AI）；其余均为精选、经安全审计的社区作品。

**🚀 全流程旗舰与编排器** —— *一次调用，跑通整个实证闭环*

| 合集 | 功能 | Skills |
|---|---|---:|
| ⭐ **[`00` · StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)** 🔥 | Agent-native Python **DSL** —— 一个 `sp.causal(...)` 跑完 DID/RD/IV/SCM/DML | 1 |
| ⭐ **[`00.1` · Python](skills/00.1-Full-empirical-analysis-skill_Python/)** 📘 | 显式栈：`pandas` · `statsmodels` · `linearmodels` · `pyfixest` | 1 |
| ⭐ **[`00.2` · Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)** 📊 | `reghdfe` · `ivreg2` · `csdid` · `sdid` · `rdrobust` 复现包 | 1 |
| ⭐ **[`00.3` · R](skills/00.3-Full-empirical-analysis-skill_R/)** 📗 | tidyverse · `fixest` · `did` · `HonestDiD`，通过 Quarto 渲染 | 1 |
| [`33` · claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) | 研究全生命周期：选题 → 综述 → 实验 → 审稿回复 | 47 |
| [`42` · ARIS](skills/42-wanshuiyin-ARIS/) | 自主「research-in-sleep」代理，端到端 | 104 |
| ⭐ **[`50` · AER-skills](skills/50-brycewang-aer-skills/)** 📕 | Top-5 经济学投稿套件：识别 → 稳健性 → R&R | 9 |
| [`67` · econfin-workflow-toolkit](skills/67-econfin-workflow-toolkit/) | 中国公司金融实证工作流，从提案到论文 | 46 |
| ⭐ **[`69` · Paper-WorkFlow](skills/69-Paper-WorkFlow/)** | 元编排器，串起整个社会科学论文流水线 | 1 |

**🎯 因果推断与计量经济学** —— *AERS 的方法论核心*

| 合集 | 功能 | Skills |
|---|---|---:|
| [`09` · awesome-econ-ai](skills/09-meleantonio-awesome-econ-ai-stuff/) | Python 面板数据分析（`linearmodels`） | 17 |
| [`10` · causal-inference-mixtape](skills/10-Jill0099-causal-inference-mixtape/) | DID / IV / RDD / SCM 模板（Cunningham） | 1 |
| [`11` · compound-science](skills/11-James-Traina-compound-science/) | 面向定量社会科学的贝叶斯估计 | 20 |
| [`13` · MixtapeTools](skills/13-scunning1975-MixtapeTools/) | Cunningham 的因果推断工具集与讲义 | 5 |
| [`14` · research-starter](skills/14-luischanci-claude-code-research-starter/) | R 中的 IV / DiD / RDD，含完整诊断 | 16 |
| [`15` · social-science-research](skills/15-Felpix-Studios-social-science-research/) | R 或 Python 端到端数据分析 | 12 |
| [`16` · clo-author](skills/16-hsantanna88-clo-author/) | 多代理数据分析（R / Stata / Python） | 10 |
| [`18` · stata-accounting](skills/18-jusi-aalto-stata-accounting-research/) | 来自 126 篇 *JAR* 论文的实测 Stata 范式 | 1 |
| [`20` · python-econ-skill](skills/20-wenddymacro-python-econ-skill/) | DSGE / HANK 与定量经济计算 | 1 |
| [`23` · baygent](skills/23-Learning-Bayesian-Statistics-baygent-skills/) | 带护栏的 PyMC / ArviZ 贝叶斯工作流 | 2 |
| [`26` · scholar](skills/26-Data-Wise-scholar/) | 统计算法设计与文档 | 17 |
| [`31` · claude-code-skills](skills/31-thalysandratos-claude-code-skills/) | Python 面板数据分析 | 13 |
| [`39` · marginaleffects](skills/39-vincentarelbundock-marginaleffects/) | 预测、斜率与比较（R / Python） | 1 |
| [`40` · pyfixest](skills/40-py-econometrics-pyfixest/) | Python 中的快速固定效应估计 | 1 |
| [`51` · CausalPy](skills/51-pymc-labs-CausalPy/) | 贝叶斯准实验（PyMC Labs） | 3 |
| [`55` · r-skills](skills/55-ab604-claude-code-r-skills/) | R 中用 `brms` 做贝叶斯推断 | 8 |
| [`61` · research-methods](skills/61-phdemotions-research-methods/) | 与预注册匹配的验证性检验 | 9 |
| [`63` · scientific-agent-skills](skills/63-tondevrel-scientific-agent-skills/) | DoWhy 识别–估计–反驳框架 | 2 |
| [`64` · mcp-stata](skills/64-tmonk-mcp-stata/) | 20 个 Stata 因果推断与复现 skill | 20 |

**📚 文献、阅读与研究设计** —— *从问题到证据基础*

| 合集 | 功能 | Skills |
|---|---|---:|
| [`02` · research-skills](skills/02-luwill-research-skills/) | 医学影像综述、提案、论文转幻灯片 | 3 |
| [`03` · scientific-skills](skills/03-K-Dense-AI-claude-scientific-skills/) | 假设生成 + 28 个科学数据库 | 4 |
| [`05` · research-superpower](skills/05-kthorn-research-superpower/) | 系统化检索、筛选与引文溯源 | 10 |
| [`25` · Diverga](skills/25-HosungYou-Diverga/) | 研究问题精炼器（抗模式坍缩） | 34 |
| [`34` · research-companion](skills/34-andrehuang-research-companion/) | 头脑风暴、评估并决策研究方向 | 1 |
| [`35` · academic-writing-skills](skills/35-bahayonghang-academic-writing-skills/) | 面向投稿场所的工业 AI 文献研究 | 5 |
| [`36` · literature-review-skill](skills/36-taoyunudt-literature-review-skill/) | 完整文献综述工作流（中文） | 1 |
| [`52` · slr-prisma](skills/52-keemanxp-slr-prisma/) | 系统文献综述，PRISMA 2020 | 1 |
| [`53` · thematic-analysis](skills/53-keemanxp-thematic-analysis-skill/) | Braun & Clarke 六阶段定性主题分析 | 1 |
| [`59` · openalex-skill](skills/59-shiquda-openalex-skill/) | 通过 OpenAlex 查询 2.4 亿+ 学术作品 | 1 |
| [`60` · superpapers](skills/60-regisely-superpapers/) | 综合性实证研究支持套件 | 16 |

**✍️ 写作、编辑与去 AIGC** —— *起草、润色，并通过 AI 检测*

| 合集 | 功能 | Skills |
|---|---|---:|
| [`01` · academic-paper-skills](skills/01-lishix520-academic-paper-skills/) | 大纲 → 手稿写作 + 7 维审稿人模拟 | 2 |
| [`04` · scientific-writer](skills/04-K-Dense-AI-claude-scientific-writer/) | 引用管理 + 科学写作 | 8 |
| [`06` · stats-paper-writing](skills/06-fuhaoda-stats-paper-writing/) | 端到端 LaTeX 统计论文写作 | 1 |
| [`22` · christopherkenny-skills](skills/22-christopherkenny-skills/) | 面向 Quarto（`.qmd`）的 APSA 风格检查器 | 11 |
| [`27` · my_claude_skills](skills/27-dariia-m-my_claude_skills/) | 经济学摘要写作指南 | 6 |
| [`38` · academic-proofreader](skills/38-peternka-academic-proofreader/) | 学术校对 | 1 |
| [`44` · humanizer_academic](skills/44-matsuikentaro1-humanizer_academic/) | 为医学/学术手稿去 AI 味（23 类模式） | 1 |
| [`45` · deslop](skills/45-stephenturner-skill-deslop/) | 去除 AI 写作痕迹（5 维评分） | 1 |
| [`46` · stop-slop](skills/46-hardikpandya-stop-slop/) | 三层 AI 痕迹检测与改写 | 1 |
| [`47` · avoid-ai-writing](skills/47-conorbronsdon-avoid-ai-writing/) | 审计 → 改写 → 二次审计 AI 味（留痕） | 1 |
| ⭐ **[`48` · chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/)** 🇨🇳 | 面向知网 / 万方 / Turnitin 中文版的中文去 AIGC | 1 |
| [`49` · humanize-chinese](skills/49-voidborne-d-humanize-chinese/) | 检测并人性化 AI 生成的中文文本 | 1 |
| [`56` · econ-writing-skill](skills/56-hanlulong-econ-writing-skill/) | 综合 50+ 顶级指南的经济学写作 | 1 |
| [`58` · econstack](skills/58-charlescoverdale-econstack/) | 政策简报（UK GES / AU Treasury） | 7 |
| [`65` · game-theory-paper-writer](skills/65-game-theory-paper-writer/) | 生成并压力测试博弈论论文 | 1 |

**📑 引用、复现与同行评审** —— *让它可验证、可复现*

| 合集 | 功能 | Skills |
|---|---|---:|
| [`24` · academic-research-skills](skills/24-Imbad0202-academic-research-skills/) | 5 审稿人多视角论文评审 | 4 |
| [`28` · paper-replicate-agent](skills/28-maxwell2732-paper-replicate-agent-demo/) | 论文复现代理演示 | 11 |
| [`29` · project20XXy](skills/29-quarcs-lab-project20XXy/) | 可复现手稿 + notebook 项目 | 24 |
| [`41` · sewage-econometrics-check](skills/41-sticerd-eee-sewage-econometrics-check/) | 10 项复现包审计 | 22 |
| [`54` · open-science-skills](skills/54-scdenney-open-science-skills/) | 引用一致性、DOI 与论据支撑审计 | 24 |
| [`62` · citation-checker](skills/62-PHY041-claude-skill-citation-checker/) | 对照 CrossRef / S2 / OpenAlex 核验引用 | 1 |

**🛠️ 数据、工具与基础设施** —— *流水线底下的管道*

| 合集 | 功能 | Skills |
|---|---|---:|
| [`07` · AI-Research-SKILLs](skills/07-Orchestra-Research-AI-Research-SKILLs/) | 发表级 ML 图表、LaTeX、引文核验 | 3 |
| [`08` · latex-document-skill](skills/08-ndpvt-web-latex-document-skill/) | 创建 / 编译任意 LaTeX 文档为 PDF | 1 |
| [`12` · claude-code-my-workflow](skills/12-pedrohcgs-claude-code-my-workflow/) | 提交 → PR → 合并的研究工作流（Emory） | 22 |
| [`17` · DAAF](skills/17-DAAF-Contribution-Community-daaf/) | 安全意识代理框架（32 条 deny rule） | 35 |
| [`32` · stata-skill](skills/32-dylantmoore-stata-skill/) | 高性能 Stata C/C++ 插件 | 3 |
| [`43` · research-plugins](skills/43-wentorai-research-plugins/) | 478 个研究插件：数据可视化、领域、基础设施 | 478 |
| [`57` · edgartools](skills/57-dgunning-edgartools/) | 查询与分析 SEC 文件 | 1 |
| [`66` · empirical-research-skills](skills/66-zheng-siyao-empirical-research-skills/) | 面向大型面板的 R 性能优化 | 7 |
| [`68` · research-productivity-skills](skills/68-research-productivity-skills/) | 论文检索、SSRN、DOI 查询、下载 | 18 |

---

## 你究竟得到什么（精确数字）

本 README 的数字一律精确、可辩护、不混淆。"自有（vendored）"指文件就在本仓库里、并被生成式 catalog 跟踪；"生态目录"指对外部仓库的精选链接。

| 它是什么 | 数量 | 事实来源 |
|---|---:|---|
| **本仓库自有**并已编目的 skill | **1,145** | [`catalog/skills.json`](catalog/skills.json) |
| 自有 **合集（collections）** | **69** | [`catalog/skills.json`](catalog/skills.json) · [全部 69 个一览 ↑](#全部-69-个-skill-合集一览) |
| **自研旗舰**全流程 skill（StatsPAI DSL + 显式 Python/Stata/R） | **4** | [`skills/00*`](skills/) |
| 每次运行从数据**重算 gold 值**的数值基准任务 | **5** | [`benchmark/`](benchmark/) |
| 行为级**评测场景 / rubric 条目** | **17 / 95** | [`eval-harness/`](eval-harness/) |
| **原始基线**安全审计（合集 / 文件） | **52 / 2,940+**，52/52 CLEAN | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| 覆盖**更广生态**的精选地图 | **23,000+ skill / 119 仓库** | 本 README · [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md) |
| **工具目录**（`tools/`）：因果/计量库、自动化研究 Agent、MCP 服务、因果发现、基准数据集 | **335 工具 / 6 类** | [`tools/tools.json`](tools/tools.json) · [`tools/CATALOG.md`](tools/CATALOG.md) |

> 安全审计覆盖的是**原始 52 合集 / 2,940 文件的基线（52/52 CLEAN）**。在该基线之后新增的 vendor skill 由 [`catalog/provenance.json`](catalog/provenance.json)、[`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md)、[`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md) 跟踪；高信任场景使用前请先 `make audit` 复核。

---

## 2 分钟自行验证

这里最有说服力的不是某个数字，而是：旗舰流水线的行为**不需要 API key、不需要付费模型就能复核**。只要 Python 3：

```bash
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
cd Auto-Empirical-Research-Skills
make check        # 仓库校验 + 单元测试 + eval lint + 数值基准
```

基准是最关键的部分：它**每次运行都从原始数据集重算 gold 答案**，所以分数无法靠写死一个数字蒙混过关。开箱即可复现：

- **LaLonde (1986) / Dehejia–Wahba (1999)** —— 朴素观察性比较给出*错误符号*（−$635）；加入协变量调整后翻正（≈ +$1,548），逼近实验基准（≈ +$1,794）。
- **Card (1995)** —— IV 教育回报（0.131）*高于* OLS（0.075），且第一阶段 F（13.3）如实报告而非藏起来。
- 另含交错 DID（TWFE 偏误 vs group-time 真值）、断点 **RDD**，以及一个**坏控制 / 后处理偏误**陷阱。

只有当流水线**暴露陷阱、拒绝把误导性数字当头条、并匹配重算真值**时才算通过。详见 [`benchmark/`](benchmark/) 与完整信任说明 [`docs/TRUST.md`](docs/TRUST.md)。

> 💡 **想要托管版、开箱即用？** 不必自己拼装 —— [**copaper.ai**](https://copaper.ai) 由同一支斯坦福方法论团队在打造本目录的同时构建，直接替你跑完整实证流水线。

---

## 为什么值得信任 —— 三层信用锚点

| 层级 | 锚点 | 它带来什么 |
|---|---|---|
| 🏛️ **学术血统** | **[Stanford REAP / SCCEI](https://sccei.fsi.stanford.edu/reap)** 中国经济与制度研究中心 | 在实证经济学方法论上有持续发表传统、在应用因果推断上有深厚积累的研究中心。 |
| 🔧 **工程落地** | **[CoPaper.AI](https://copaper.ai)** 实证研究 AI 助手 | 内置 **20 个计量方法论 skill**（DID / IV / RDD / PSM / DML 等），Supervisor + 4 子代理架构，一句话触发，自动产出发表级结果。 |
| ⚙️ **开源引擎** | **[StatsPAI](https://github.com/brycewang-stanford/StatsPAI)** —— 因果推断引擎 | **900+ 函数 · 一个 `import statspai as sp` · JOSS 投稿中 · MIT。** CoPaper.AI 跑出的每一个 DID / IV / RD / SCM 估计都由 StatsPAI 驱动，而本目录正是该生态的一部分。 |

---

## 旗舰流水线 skills

四个并行实现，跑的是**同一套 8 步实证闭环** —— *数据清洗 → 变量构造 → 描述统计 → 诊断检验 → 估计 → 稳健性 → 机制/异质性 → 发表级表图* —— 再加上投稿与去 AIGC 两条线。每个都采用**渐进式披露**：`SKILL.md` 只放一条主干（每步的标准调用），分步深度手册按需加载。它们并存共生，按技术栈和场景挑选即可。

| Skill | 技术栈 | 最适合 |
|---|---|---|
| **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)** 🔥 | Agent-native Python **DSL** —— 一个 `sp.causal(...)` 跑完闭环；900+ 函数，自描述 API，统一 `CausalResult` | 信任 DSL 时，一句 agent 指令完成全流程自动化 |
| **[Full Empirical Analysis — Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md)** 📘 | **显式**栈：`pandas` · `statsmodels` · `linearmodels` · `pyfixest` · `rdrobust` · `econml` · `causalml` | 教学、审稿人级逐行审计、需要完全控制的严谨复现 |
| **[Full Empirical Analysis — Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md)** 📊 | 社区事实标准：`reghdfe` · `ivreg2` · `csdid` · `did_imputation` · `sdid` · `rdrobust` · `synth` · `psmatch2` · `boottest` · `esttab` | 审稿人或合作者只接受 Stata 复现包时（AER/QJE/JPE/ReStud 风格） |
| **[Full Empirical Analysis — R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)** 📗 | 现代 tidyverse：`fixest` · `did` · `synthdid` · `HonestDiD` · `rdrobust` · `grf` · `DoubleML` · `marginaleffects` · **Quarto** | 单个 `.qmd` 一键渲染 PDF/HTML/Word 的一体化复现报告 |
| **[AER-Skills](skills/50-brycewang-aer-skills/)** 📕 | 9 个 skill：选题路由 → 识别审计 → 稳健性 → 引言 → 表图 → 复现 → 投稿 → R&R → 总调度 | Top-5 经济学（AER / AER:Insights / AEJ）投稿：**识别优先** —— 设计若脆，再多 prose 也救不回来 |
| **[chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/SKILL.md)** 🇨🇳 | 17 类中文 AI 痕迹模式库，五步「定位→诊断→改写→自评→复查」闭环 | 降低知网 / 万方 / 维普 / Turnitin 中文版的 AI 写作信号 |
| **[Paper-WorkFlow](skills/69-Paper-WorkFlow/README.md)** 🧭 | **元编排器**，串起 Stage 0–9 —— 选题 → 设计 → 数据 → 估计 → 表格图形 → 初稿 → 润色 → 去 AIGC → 模拟审稿 → 投稿 —— 通过调度已有 skill 与并行子代理，并用可续跑的 `workflow_state.json` 记录进度 | 端到端自动跑完一篇完整的实证社会科学论文 |

> **为什么既要 DSL 又要显式三件套？** 信任一键 DSL 时用 StatsPAI；做教学、审计、或要逐个替换诊断时用 00.1/00.2/00.3。AER-skills 再把一份正确的分析推到录用门槛 —— 它们解决的是*不同*问题，可以组合。

---

## 从这里开始 —— 30 秒选一个 skill

| 目标 | 从这里开始 |
|---|---|
| 跑完整实证流水线 | [`StatsPAI`](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)（或 [Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md) · [Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md) · [R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)） |
| 先审顶刊识别策略 | [`aer-identification`](skills/50-brycewang-aer-skills/skills/aer-identification/SKILL.md) |
| 准备 AER / AEJ 投稿 | [`aer-workflow`](skills/50-brycewang-aer-skills/skills/aer-workflow/SKILL.md) |
| 整理 AEA 合规的复现包 | [`aer-replication`](skills/50-brycewang-aer-skills/skills/aer-replication/SKILL.md) |
| 降低中文初稿的 AI 写作痕迹 | [`chinese-de-aigc`](skills/48-copaper-ai-chinese-de-aigc/SKILL.md) |

**更多入口：**

- **不确定用哪个？** → [`docs/CHOOSING_A_SKILL.md`](docs/CHOOSING_A_SKILL.md) · 分面搜索：[`docs/search.html`](docs/search.html)
- **端到端走通前 10 分钟** → [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)
- **直接复制完整工作流** → [`docs/GOLDEN_WORKFLOWS.md`](docs/GOLDEN_WORKFLOWS.md)
- **装进 runtime / 免安装使用** → [`docs/INSTALL.md`](docs/INSTALL.md)
- **机器可读索引** → [`catalog/skills.json`](catalog/skills.json) · 分类法：[`docs/TAXONOMY.md`](docs/TAXONOMY.md) · 完整目录：[`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md)
- **常见问题** → [`docs/FAQ.md`](docs/FAQ.md)

---

## 凭什么不只是 23K skill 的堆砌

公开 skill 的数量很容易灌水，近期研究也表明大型 skill 索引常常冗余、偶尔不安全。AERS 比拼的是**可验证的质量**，不是裸数量。下面每一层都能本地 `make check`、也都在 CI 里跑。

| 层 | 它能拦住什么 | 在哪 |
|---|---|---|
| **数值基准** | 报告数字与真实数据重算真值不符 —— 朴素 DID 符号陷阱、缺第一阶段 F 的弱 IV、交错时点下的 TWFE 偏误、RDD 趋势混淆、后处理坏控制 | [`benchmark/`](benchmark/) · 5 任务 |
| **评测套件** | 散文级失误：弱 IV 假性安心、交错 DID 误用 TWFE、编造引用、不安全的 `curl \| bash` 安装、多重检验滥用、AER 合规缺口 | [`eval-harness/`](eval-harness/) · 17 场景 / 95 rubric |
| **安全审计** | pipe-to-shell、反向 shell、凭据外泄、prompt 注入等 13 类风险 —— 六阶段，40+ hook 脚本人工核查 | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| **来源与许可** | 未声明来源、许可风险、1,145 个编目 skill 的卫生度漂移 | [`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md) · [`docs/SKILL_QUALITY.md`](docs/SKILL_QUALITY.md) |
| **CI 与兼容性** | catalog 新鲜度、本地死链、GitHub Actions 策略、Python 3.9 **与** 3.12 语法基线 | [`.github/workflows/`](.github/workflows/) · 6 条 workflow |

```bash
make catalog     # 重新生成 catalog、provenance、audit、enrichment
make validate    # 新鲜度 + 链接 / frontmatter 检查
make check       # 完整 gate：validate + Python 编译 + 单元测试 + eval lint + benchmark
```

这套信任面是**必要而非充分** —— 正则 rubric 不能认证文笔，小基准也覆盖不了每一种设计。它的设计目标是*对已知高代价错误快速失败*。诚实的边界说明见 [`docs/TRUST.md`](docs/TRUST.md) 与 [`docs/QUALITY_GATE.md`](docs/QUALITY_GATE.md)。

---

## 浏览全景

> 📚 完整的 **[69 合集目录 ↑](#全部-69-个-skill-合集一览)** 就在本 README 顶部 —— 本节按主题深入这个生态。

### 按研究流程

```
选题构思 → 文献检索 → 文献精读 → 研究设计 → 数据获取
   │           │          │          │          │
   ▼           ▼          ▼          ▼          ▼
  01          02         03         01         04

数据清洗 → 统计分析 → 论文初稿 → 修改润色 → 排版引用
   │           │          │          │          │
   ▼           ▼          ▼          ▼          ▼
  04          05         06         07         08

论文复现 → 投稿审稿 → 审稿回复 → 答辩展示
   │           │          │          │
   ▼           ▼          ▼          ▼
  09          10         10         10
```

各阶段 skill 速查（中英双语）：[01 选题与研究设计](docs/01-选题与研究设计.md) · [02 文献检索与综述](docs/02-文献检索与综述.md) · [03 论文阅读与拆解](docs/03-论文阅读与拆解.md) · [04 数据获取与清洗](docs/04-数据获取与清洗.md) · [05 统计分析与因果推断](docs/05-统计分析与因果推断.md) · [06 论文写作](docs/06-论文写作.md) · [07 论文修改与润色](docs/07-论文修改与润色.md) · [08 引用管理与排版](docs/08-引用管理与排版.md) · [09 论文复现与可复现研究](docs/09-论文复现与可复现研究.md) · [10 审稿回复与学术答辩](docs/10-审稿回复与学术答辩.md)

### 综合型 skill 套件

> AERS 要解决的痛点：让 AI 跑一个 DID，它给了基准回归就停了。"平行趋势呢？"—— 补一个。"安慰剂呢？"—— 再补一个。*每次都像挤牙膏。* 而 skill 是给 agent 的**方法论操作手册**：它已经知道一个完整的 DID 意味着 平行趋势 → 基准 → 稳健性矩阵 → 异质性 → 机制，每一步该输出什么也都定好了。

<details>
<summary><b>学术研究专用</b> —— 通用型研究套件（K-Dense、AI-Research-SKILLs、claude-scholar 等）</summary>

| 套件 | Stars | Skills 数 | 核心特色 |
|------|-------|----------|---------|
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 8,799 | 140+ | 28+ 科学数据库（OpenAlex、PubMed）；scientific-writing + literature-review + statistical-analysis |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 3,637 | 87 | 22 个类别，ML 论文写作，LaTeX 模板，引文验证 |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | ~1,790 | 多个 | 完整论文管线（research → write → review → revise → finalize），风格校准，幻觉检测 |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | - | 25+ | 研究全生命周期：选题 → 综述 → 实验 → 写作 → 审稿回复；集成 Zotero MCP |
| [luwill/research-skills](https://github.com/luwill/research-skills) | 209 | 3 | 研究提案生成、医学综述写作、论文转幻灯片，双语 |
| [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | 22 | 2 | Strategist（7 维审稿人模拟）+ Composer（系统化写作） |
| [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) | - | 17 | 统计研究：arXiv 搜索、DOI 查询、BibTeX、方法论写作、审稿回复 |

</details>

<details>
<summary><b>经济学 / 因果推断专用</b> —— 自研旗舰 + 社区 Stata/IV/预审套件</summary>

自研旗舰（[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)、[Python](skills/00.1-Full-empirical-analysis-skill_Python/)、[Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)、[R](skills/00.3-Full-empirical-analysis-skill_R/)、[AER-skills](skills/50-brycewang-aer-skills/)）已在[上文](#旗舰流水线-skills)详述。社区补充：

| 套件 | 核心特色 | 适用场景 |
|------|---------|---------|
| **[CoPaper.AI](https://copaper.ai)** | 20 个方法论 skill，Supervisor + 4 子代理，智能路由，结果自动输出 | 经济学实证全流程（托管版） |
| [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) | 2 代理预审：因果过度声称检测、识别策略评估（AER/QJE/JPE/Econometrica/REStud）；6 代理基金评审 | 投稿前自审、基金申请 |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | LaTeX 统计论文写作，前端草稿生成 | 统计学、计量经济学论文 |
| [dylantmoore/stata-skill](https://github.com/dylantmoore/stata-skill) | Stata 全覆盖：语法、数据管理、计量、因果推断、Mata、20+ 社区包 | Stata 用户 |
| [SepineTam/stata-mcp](https://github.com/SepineTam/stata-mcp) | LLM 通过 MCP 直接驱动 Stata 回归 | Stata 计量分析 |
| [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp) | Stata-MCP 编辑器扩展（VS Code/Cursor/Antigravity）：直接跑 `.do`、实时输出、数据/图查看；MIT · 414★（与上方 SepineTam 同名不同项目） | 编辑器内 AI 协作跑 Stata |
| [tmonk/mcp-stata](https://github.com/tmonk/mcp-stata) · 已收录 [`skills/64`](skills/64-tmonk-mcp-stata/) | Stata MCP server 的 **20 个 SKILL.md**：复现 / 数据审计 / 发表 QA / 旧码现代化 / referee 回应 / power / 因果推断；**AGPL-3.0**（聚合保留原许可，未 vendor 服务端代码） | Stata 复现与稳健性审计 |
| [PovertyAction/ipa-stata-template](https://github.com/PovertyAction/ipa-stata-template) | IPA 可复现 Stata 研究模板 + `.claude/skills`：编号流水线、断言式防御编程、LaTeX 表格；MIT | 发展经济学 / 田野实证复现 |
| [lcrawfurd/claude-skills](https://github.com/lcrawfurd/claude-skills) | 学术 skill：paper / code review、referee、预审；code-review 内置 Stata/R/Python 编码规范（DIME / Reif / AEA Data Editor） | 投稿前审稿与代码复核 |
| [AEADataEditor/replication-template](https://github.com/AEADataEditor/replication-template) | AEA 数据主编官方复现包模板（Stata 为主，`REPLICATION.md`）—— 经济学复现"黄金标准" | AEA / 顶刊复现包打包 |

</details>

<details>
<summary><b>金融 · 教育与公共健康 · 法律 · 营销 · 产品 · 通用 agent</b></summary>

**金融与投资** —— [financial-services-plugins](https://github.com/anthropics/financial-services-plugins)（Anthropic 官方）· [OctagonAI/skills](https://github.com/OctagonAI/skills) · [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) · [himself65/finance-skills](https://github.com/himself65/finance-skills) · [quant-sentiment-ai/claude-equity-research](https://github.com/quant-sentiment-ai/claude-equity-research)

**教育与公共健康** —— [GarethManning/claude-education-skills](https://github.com/GarethManning/claude-education-skills) · [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills)（**869** 个医学 skill：流行病学、监测、临床研究、药物安全、生物统计）

**治理、合规与法律** —— [Claude-Skills-Governance-Risk-and-Compliance](https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance)（ISO 27001 / SOC 2 / GDPR / HIPAA）· [zubair-trabzada/ai-legal-claude](https://github.com/zubair-trabzada/ai-legal-claude) · [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)

**营销与消费者行为** —— [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) · [zubair-trabzada/ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude) · [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills)

**产品与组织行为** —— [phuryn/pm-skills](https://github.com/phuryn/pm-skills)（100+ skill）· [mastepanoski/claude-skills](https://github.com/mastepanoski/claude-skills)（Nielsen 启发式、NIST AI RMF、ISO 42001）

**通用 agent 能力** —— [lyndonkl/claude](https://github.com/lyndonkl/claude)（85 skill + 6 编排器）· [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)（220+ skill，~5,200★）· [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) · [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)（1,367 skill）· [posit-dev/skills](https://github.com/posit-dev/skills)（Posit 官方）

</details>

### 降 AIGC 检测率 & 学术去 AI 味

> 2026 年学术写作最尖锐的痛点之一：论文 AIGC 率超标（Turnitin、GPTZero、知网）可被一票否决。下面这几个 skill 是目前最完整的开源方案 —— 全部 MIT，全部本地收录（`skills/44-49`）。

| 套件 | 核心特色 | 最适合 | 本地 |
|------|---------|--------|------|
| **chinese-de-aigc** 🇨🇳 | CoPaper.AI **原创**中文学术去 AIGC；17 类中文痕迹模式库、五步闭环、分章节策略、五维评分。目前 GitHub 上唯一面向中文学术去 AIGC 的 skill | 知网 / 万方 / 维普 / Turnitin 中文版 | [`48`](skills/48-copaper-ai-chinese-de-aigc/) |
| [voidborne-d/humanize-chinese](skills/49-voidborne-d-humanize-chinese/) 🇨🇳 | 同时提供 SKILL.md 与独立 Python CLI；17 类检测 + 7 风格改写器，LR ensemble 程序化打分。**License: MIT（非商用修改版）** | 中文学位论文 / 长篇 / 批量 pipeline | [`49`](skills/49-voidborne-d-humanize-chinese/) |
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | 学术专用；23 类 AI 写作模式；保留合法学术过渡词 | 医学、生命科学、自然科学论文 | [`44`](skills/44-matsuikentaro1-humanizer_academic/) |
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) | 智能区分合法学科惯例 vs AI 痕迹；5 维评分 | 科学论文、技术博客 | [`45`](skills/45-stephenturner-skill-deslop/) |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 三层检测 + 五维评分；禁用短语、结构套路、句级规则 | 通用散文、博客、报告 | [`46`](skills/46-hardikpandya-stop-slop/) |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 结构化审计 + 重写 + 二次审计；可审计、可追溯 | 需要留痕的修改流程 | [`47`](skills/47-conorbronsdon-avoid-ai-writing/) |

> **组合建议：** 🇨🇳 中文（知网/万方/维普）→ chinese-de-aigc · 🇬🇧 英文 → humanizer_academic · 需要审计留痕 → avoid-ai-writing · 通用散文 → stop-slop。

### 工具目录（tools/）：自动化实证与因果推断工具

> 与上面的 skill 不同，[`tools/`](tools/) 收录的是 agent / 研究者**实际调用的软件与服务**——已结构化编目、核实过 license 与维护状态，并接入 `make validate`。事实源 [`tools/tools.json`](tools/tools.json)，可浏览清单 [`tools/CATALOG.md`](tools/CATALOG.md)。

**335 个工具 / 6 类**（2026-06 收录）：

- **因果推断 / 处理效应库（32）** — DoWhy · EconML · CausalML · DoubleML · CausalPy · causallib · grf · CATENets · TMLE 系列 · 孟德尔随机化 …
- **计量 / 准实验库（170）** — 面板FE · DiD（含现代/staggered）· 事件研究 · RDD · IV · 合成控制/SDID · 匹配加权 · 敏感性分析（fixest · did · HonestDiD · rdrobust · synthdid · reghdfe · csdid · sdid · pyfixest · linearmodels …）；**新增**空间计量（spdep · PySAL/spreg · GeoDa）· 局部投影/IRF & (S)VAR（lpirfs · vars · svars）· 调查加权/MRP/raking（survey · samplics · balance）· 元分析（metafor · meta · netmeta · metan）；横跨 R/Python/Stata/Julia。
- **自动化研究 / 数据科学 Agent（51）** — 端到端自动做科研/数据分析：AI-Scientist · data-to-paper · Agent Laboratory · RD-Agent · AI-Researcher · STORM · PaperQA2 · gpt-researcher · DeepAnalyze · MetaGPT(DI) · Biomni …（⚠️ 含非 OSI/无 LICENSE 仓库，用前确认授权）。
- **MCP 服务（48）** — 统计执行（StatsPAI · stata-mcp · R / Jupyter MCP）+ 数据获取（FRED · World Bank · IMF · OECD · Eurostat · Census · BEA · BLS · SEC EDGAR · OpenAlex · Semantic Scholar · PubMed · Zotero · arXiv …）。
- **因果发现 / 结构学习（25）** — causal-learn · Tetrad / py-tetrad · gCastle · CDT · tigramite(PCMCI) · LiNGAM · NOTEARS / DAGMA · pcalg · bnlearn · pgmpy …
- **基准与数据集（9）** — causaldata · IHDP / Twins · ACIC 竞赛数据 · RealCause · JustCause · Tübingen cause-effect pairs · bnlearn 网络库 …

完整说明见 [`tools/README.md`](tools/README.md)。

### 多代理系统 · MCP 服务器 · 平台 · 学习资源

<details>
<summary><b>多代理协作系统</b> —— 论文修改、自主研究、数据科学团队</summary>

角色分离之所以胜过单 agent：审阅者独立于起草者，才能形成真正的质量闭环 —— 与同行评审同理。

**论文修改与写作：** copy-edit-master（3 子代理，Strunk & White / McCloskey 规则）· introduction-writer（strategist → drafter → reviewer → reviser）· CoPaper.AI PaperAgent（Supervisor + 4 子代理）。

**自主研究与数据科学：** [ruc-datalab/DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze)（人民大学）· [business-science/ai-data-science-team](https://github.com/business-science/ai-data-science-team) · [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher)（NeurIPS 2025 Spotlight）· [wanshuiyin/ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) · [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)（成本降 84%）· [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) · [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) · [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)（Emory）。

</details>

<details>
<summary><b>学术数据 MCP 服务器</b> —— OpenAlex、Semantic Scholar、FRED、World Bank、Zotero 等</summary>

[xingyulu23/Academix](https://github.com/xingyulu23/Academix) · [Eclipse-Cj/paper-distill-mcp](https://github.com/Eclipse-Cj/paper-distill-mcp) · [oksure/openalex-research-mcp](https://github.com/oksure/openalex-research-mcp)（2.4 亿+ 作品）· [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp)（20+ 来源）· [lzinga/us-gov-open-data-mcp](https://github.com/lzinga/us-gov-open-data-mcp)（40+ 美国政府 API）· [stefanoamorelli/fred-mcp-server](https://github.com/stefanoamorelli/fred-mcp-server)（FRED 80 万+ 序列）· [llnOrmll/world-bank-data-mcp](https://github.com/llnormll/world-bank-data-mcp) · [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)

</details>

<details>
<summary><b>Skill 聚合平台与学习资源</b></summary>

**平台：** [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)（1,000+）· [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)（1,340+）· [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)（5,400+）· [skills.sh](https://skills.sh/) · [ClawHub](https://clawhub.com)（13,729）· [Anthropic 官方 skills](https://github.com/anthropics/skills)。

**学习：** [Claude Code Skills 完全指南（PDF）](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) · [Agent Skills 标准](https://agentskills.io/) · [Causal Inference for the Brave and True](https://github.com/xieliaing/CausalInferenceIntro)（中文版）· [Awesome AI for Economists](https://github.com/hanlulong/awesome-ai-for-economists) · [Awesome Econ AI Stuff](https://github.com/meleantonio/awesome-econ-ai-stuff)。

</details>

---

## 安全扫描

仓库**原始 52 个 skill 合集 / 2,940+ 文件**通过了系统性审计 —— **52/52 全部 CLEAN，零 FLAGGED**：未发现任何恶意 prompt、病毒、反向 shell 或 prompt 注入。所有看似敏感的命中，经验证后均归入三类合法内容：**防御性安全规则**、**合法学术 API 调用**（arXiv / CrossRef / PubMed / FRED / World Bank / OECD / BLS）、或**标准 Claude Code 工作流 hook**（全部本地文件操作、零网络 IO）。

![Skills 安全扫描总览](images/security-scan/security-scan-01-overview.png)

六阶段、纵深防御：13 类风险维度自动 grep → 6 个含 hook 的 skill 及其 40+ hook 脚本 100% 人工核查（全仓**无 `Bash(*)` 通配符**）→ 三 agent 并行内容审查 → 补充完整性检查（隐藏 Unicode、编码异常、HTML 注入、网络 import）。

> **关键洞察：** 规模最大 ≠ 风险最高。体量最大的几个 skill 全部通过；[17-DAAF](skills/17-DAAF-Contribution-Community-daaf/) 反而树立了安全意识标杆（14 个防御 hook + 32 条 deny rule + 主动凭据扫描）。

基线之后新增的 vendor skill 由 [`catalog/provenance.json`](catalog/provenance.json) 与 [`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md) 跟踪 —— 请 `make audit`。完整报告：[**SECURITY-SCAN-REPORT.md**](SECURITY-SCAN-REPORT.md)。

---

## 更新日志

叙事版更新日志已迁至 [**CHANGELOG.md**](CHANGELOG.md)。近期要点：

- **2026-05** —— 收录 **AER-skills**（Top-5 经济学投稿套件，9 个 skill）并设周更上游同步；数值基准扩到 **5 个因果复原任务**、评测套件扩到 **17 场景 / 95 rubric**。
- **2026-04** —— 完成 **52/52 安全基线**；交付四个全流程旗舰（**StatsPAI** + 显式 **Python / Stata / R**）；上线原创 **chinese-de-aigc** skill。
- **更早** —— 从 43 个合集成长为覆盖 **119 仓库 / 23,000+ skill** 的精选地图；新增双语 README、学术数据 MCP 服务器与多代理系统。

---

## 贡献与引用

欢迎贡献 —— 请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [`docs/SKILL_SUBMISSION_GUIDE.md`](docs/SKILL_SUBMISSION_GUIDE.md)。我们特别欢迎社会科学 skill（经济学、政治学、社会学、心理学、教育、公共健康）、因果推断方法的新实现、学术/政府数据的 MCP 服务器、中文友好的 skill、以及多代理案例。新提交须声明 **来源、许可、类别** 以供 provenance 审计。

如果 AERS 对你的工作有帮助，请**引用它**（[CITATION.cff](CITATION.cff)）并**点个 Star**，让更多研究者看到。

<a href="https://www.star-history.com/#brycewang-stanford/Auto-Empirical-Research-Skills&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" width="600" />
 </picture>
</a>

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
