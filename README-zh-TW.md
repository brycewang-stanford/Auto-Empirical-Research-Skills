# Auto-Empirical Research Skills (AERS)

<div align="center">

**🌐 語言: [English](README.md) | [简体中文](README-zh-CN.md) | 繁體中文 | [日本語](README-ja.md) | [한국어](README-ko.md)**

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

  <strong>Stanford REAP × CoPaper.AI</strong> · 實證研究 AI 工具的學術工業級產品<br/>
  <sub>由史丹佛實證研究方法論團隊打造，涵蓋從資料清洗到頂刊投稿的完整工作流</sub>

  <br/>
  <br/>

  <img src="images/aers-readme-cover-cn.png" alt="實證研究智能體技能大全封面圖" width="100%" />

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

## 全部 69 個 skill 合集一覽

> **打開倉庫 → 看見整座資料庫。** 全部 **69 個合集 · 1,145 個 skill**，編號 `00 → 69`，每一個都**自有進本倉庫**（不只是對外連結），並在 [`catalog/skills.json`](catalog/skills.json) 裡追蹤。**點任一列即可打開其資料夾。** **⭐ = 由 Stanford REAP × CoPaper.AI 團隊自研的旗艦 skill**；其餘皆為精選、經安全稽核的社群成果。
>
> **主題對照 ——** 🚀 全流程與調度器 · 🎯 因果推斷與計量 · 📚 文獻與研究設計 · ✍️ 寫作、編修與去 AIGC · 📑 引用、重現與同儕審稿 · 🛠️ 資料、工具與基礎設施

| # | 合集 | 它能做什麼 | 主題 | Skills |
|:--|:--|:--|:--:|--:|
| ⭐ **00** | **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)** 🔥 | Agent-native Python **DSL** —— 一個 `sp.causal(...)` 跑 DID/RD/IV/SCM/DML | 🚀 | 1 |
| ⭐ **00.1** | **[Full Empirical · Python](skills/00.1-Full-empirical-analysis-skill_Python/)** 📘 | 顯式棧：`pandas` · `statsmodels` · `linearmodels` · `pyfixest` | 🚀 | 1 |
| ⭐ **00.2** | **[Full Empirical · Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)** 📊 | `reghdfe` · `ivreg2` · `csdid` · `sdid` · `rdrobust` 重現包 | 🚀 | 1 |
| ⭐ **00.3** | **[Full Empirical · R](skills/00.3-Full-empirical-analysis-skill_R/)** 📗 | tidyverse · `fixest` · `did` · `HonestDiD`，透過 Quarto 算繪 | 🚀 | 1 |
| **01** | [academic-paper-skills](skills/01-lishix520-academic-paper-skills/) | 大綱 → 手稿寫作 + 7 維審稿人模擬 | ✍️ | 2 |
| **02** | [research-skills](skills/02-luwill-research-skills/) | 醫學影像綜述、研究提案、論文轉投影片 | 📚 | 3 |
| **03** | [scientific-skills](skills/03-K-Dense-AI-claude-scientific-skills/) | 假設生成 + 28 個科學資料庫 | 📚 | 4 |
| **04** | [scientific-writer](skills/04-K-Dense-AI-claude-scientific-writer/) | 引用管理 + 科學寫作 | ✍️ | 8 |
| **05** | [research-superpower](skills/05-kthorn-research-superpower/) | 系統化檢索、篩選與引用溯源 | 📚 | 10 |
| **06** | [stats-paper-writing](skills/06-fuhaoda-stats-paper-writing/) | 端到端 LaTeX 統計論文寫作 | ✍️ | 1 |
| **07** | [AI-Research-SKILLs](skills/07-Orchestra-Research-AI-Research-SKILLs/) | 發表級 ML 圖形、LaTeX、引用驗證 | 🛠️ | 3 |
| **08** | [latex-document-skill](skills/08-ndpvt-web-latex-document-skill/) | 建立 / 編譯任意 LaTeX 文件為 PDF | 🛠️ | 1 |
| **09** | [awesome-econ-ai](skills/09-meleantonio-awesome-econ-ai-stuff/) | Python 面板資料分析（`linearmodels`） | 🎯 | 17 |
| **10** | [causal-inference-mixtape](skills/10-Jill0099-causal-inference-mixtape/) | DID / IV / RDD / SCM 範本（Cunningham） | 🎯 | 1 |
| **11** | [compound-science](skills/11-James-Traina-compound-science/) | 量化社會科學的貝氏估計 | 🎯 | 20 |
| **12** | [claude-code-my-workflow](skills/12-pedrohcgs-claude-code-my-workflow/) | Commit → PR → merge 研究工作流（Emory） | 🛠️ | 22 |
| **13** | [MixtapeTools](skills/13-scunning1975-MixtapeTools/) | Cunningham 的因果推斷工具箱與講義 | 🎯 | 5 |
| **14** | [research-starter](skills/14-luischanci-claude-code-research-starter/) | R 中的 IV / DiD / RDD，配套完整診斷 | 🎯 | 16 |
| **15** | [social-science-research](skills/15-Felpix-Studios-social-science-research/) | R 或 Python 端到端資料分析 | 🎯 | 12 |
| **16** | [clo-author](skills/16-hsantanna88-clo-author/) | 多代理資料分析（R / Stata / Python） | 🎯 | 10 |
| **17** | [DAAF](skills/17-DAAF-Contribution-Community-daaf/) | 安全意識代理框架（32 條 deny 規則） | 🛠️ | 35 |
| **18** | [stata-accounting](skills/18-jusi-aalto-stata-accounting-research/) | 取自 126 篇 *JAR* 論文的實測 Stata 範式 | 🎯 | 1 |
| **20** | [python-econ-skill](skills/20-wenddymacro-python-econ-skill/) | DSGE / HANK 與量化經濟計算 | 🎯 | 1 |
| **22** | [christopherkenny-skills](skills/22-christopherkenny-skills/) | Quarto（`.qmd`）的 APSA 風格檢查器 | ✍️ | 11 |
| **23** | [baygent](skills/23-Learning-Bayesian-Statistics-baygent-skills/) | 帶護欄的 PyMC / ArviZ 貝氏工作流 | 🎯 | 2 |
| **24** | [academic-research-skills](skills/24-Imbad0202-academic-research-skills/) | 5 審稿人多視角論文審查 | 📑 | 4 |
| **25** | [Diverga](skills/25-HosungYou-Diverga/) | 研究問題精煉器（抗模式坍縮） | 📚 | 34 |
| **26** | [scholar](skills/26-Data-Wise-scholar/) | 統計演算法設計與文件化 | 🎯 | 17 |
| **27** | [my_claude_skills](skills/27-dariia-m-my_claude_skills/) | 經濟學摘要寫作指南 | ✍️ | 6 |
| **28** | [paper-replicate-agent](skills/28-maxwell2732-paper-replicate-agent-demo/) | 論文重現代理 demo | 📑 | 11 |
| **29** | [project20XXy](skills/29-quarcs-lab-project20XXy/) | 可重現的手稿 + notebook 專案 | 📑 | 24 |
| **31** | [claude-code-skills](skills/31-thalysandratos-claude-code-skills/) | Python 面板資料分析 | 🎯 | 13 |
| **32** | [stata-skill](skills/32-dylantmoore-stata-skill/) | 高效能 Stata C/C++ plugin | 🛠️ | 3 |
| **33** | [claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) | 研究全生命週期：選題 → 審查 → 實驗 → 回覆 | 🚀 | 47 |
| **34** | [research-companion](skills/34-andrehuang-research-companion/) | 腦力激盪、評估與決定研究方向 | 📚 | 1 |
| **35** | [academic-writing-skills](skills/35-bahayonghang-academic-writing-skills/) | 場景感知的工業 AI 文獻研究 | 📚 | 5 |
| **36** | [literature-review-skill](skills/36-taoyunudt-literature-review-skill/) | 完整文獻綜述工作流（中文） | 📚 | 1 |
| **38** | [academic-proofreader](skills/38-peternka-academic-proofreader/) | 學術校對 | ✍️ | 1 |
| **39** | [marginaleffects](skills/39-vincentarelbundock-marginaleffects/) | 預測、斜率與比較（R / Python） | 🎯 | 1 |
| **40** | [pyfixest](skills/40-py-econometrics-pyfixest/) | Python 中的快速固定效應估計 | 🎯 | 1 |
| **41** | [sewage-econometrics-check](skills/41-sticerd-eee-sewage-econometrics-check/) | 10 項檢查的重現包稽核 | 📑 | 22 |
| **42** | [ARIS](skills/42-wanshuiyin-ARIS/) | 自主「睡眠中做研究」代理，端到端 | 🚀 | 104 |
| **43** | [research-plugins](skills/43-wentorai-research-plugins/) | 478 個研究外掛：資料視覺化、領域、基礎設施 | 🛠️ | 478 |
| **44** | [humanizer_academic](skills/44-matsuikentaro1-humanizer_academic/) | 去 AI 化醫學/學術手稿（23 種模式） | ✍️ | 1 |
| **45** | [deslop](skills/45-stephenturner-skill-deslop/) | 移除 AI 寫作模式（5 維評分） | ✍️ | 1 |
| **46** | [stop-slop](skills/46-hardikpandya-stop-slop/) | 3 層 AI 痕跡偵測與改寫 | ✍️ | 1 |
| **47** | [avoid-ai-writing](skills/47-conorbronsdon-avoid-ai-writing/) | 稽核 → 改寫 → 複稽 AI 腔（留痕） | ✍️ | 1 |
| ⭐ **48** | **[chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/)** 🇨🇳 | 面向知網 / 萬方 / Turnitin 中文版的中文去 AIGC | ✍️ | 1 |
| **49** | [humanize-chinese](skills/49-voidborne-d-humanize-chinese/) | 偵測並擬人化 AI 生成的中文文字 | ✍️ | 1 |
| ⭐ **50** | **[AER-skills](skills/50-brycewang-aer-skills/)** 📕 | Top-5 經濟學投稿棧：識別 → 穩健性 → R&R | 🚀 | 9 |
| **51** | [CausalPy](skills/51-pymc-labs-CausalPy/) | 貝氏準實驗（PyMC Labs） | 🎯 | 3 |
| **52** | [slr-prisma](skills/52-keemanxp-slr-prisma/) | 系統性文獻綜述，PRISMA 2020 | 📚 | 1 |
| **53** | [thematic-analysis](skills/53-keemanxp-thematic-analysis-skill/) | Braun & Clarke 六階段質性主題分析 | 📚 | 1 |
| **54** | [open-science-skills](skills/54-scdenney-open-science-skills/) | 引用一致性、DOI 與主張佐證稽核 | 📑 | 24 |
| **55** | [r-skills](skills/55-ab604-claude-code-r-skills/) | R 中以 `brms` 做貝氏推論 | 🎯 | 8 |
| **56** | [econ-writing-skill](skills/56-hanlulong-econ-writing-skill/) | 綜合 50+ 頂級指南的經濟學寫作 | ✍️ | 1 |
| **57** | [edgartools](skills/57-dgunning-edgartools/) | 查詢與分析 SEC 申報文件 | 🛠️ | 1 |
| **58** | [econstack](skills/58-charlescoverdale-econstack/) | 政策簡報（UK GES / AU Treasury） | ✍️ | 7 |
| **59** | [openalex-skill](skills/59-shiquda-openalex-skill/) | 透過 OpenAlex 查詢 2.4 億+ 學術成果 | 📚 | 1 |
| **60** | [superpapers](skills/60-regisely-superpapers/) | 全面的實證研究支援套件 | 📚 | 16 |
| **61** | [research-methods](skills/61-phdemotions-research-methods/) | 與預註冊對齊的驗證性檢驗 | 🎯 | 9 |
| **62** | [citation-checker](skills/62-PHY041-claude-skill-citation-checker/) | 對照 CrossRef / S2 / OpenAlex 驗證引用 | 📑 | 1 |
| **63** | [scientific-agent-skills](skills/63-tondevrel-scientific-agent-skills/) | DoWhy 識別–估計–反駁框架 | 🎯 | 2 |
| **64** | [mcp-stata](skills/64-tmonk-mcp-stata/) | 20 個 Stata 因果推斷與重現 skill | 🎯 | 20 |
| **65** | [game-theory-paper-writer](skills/65-game-theory-paper-writer/) | 生成並壓力測試賽局理論論文 | ✍️ | 1 |
| **66** | [empirical-research-skills](skills/66-zheng-siyao-empirical-research-skills/) | 大型面板的 R 效能最佳化 | 🛠️ | 7 |
| **67** | [econfin-workflow-toolkit](skills/67-econfin-workflow-toolkit/) | 中國公司金融實證工作流，提案 → 論文 | 🚀 | 46 |
| **68** | [research-productivity-skills](skills/68-research-productivity-skills/) | 論文檢索、SSRN、DOI 查詢、下載 | 🛠️ | 18 |
| ⭐ **69** | **[Paper-WorkFlow](skills/69-Paper-WorkFlow/)** 🧭 | 串起整條社會科學流水線的元調度器 | 🚀 | 1 |

> ⭐ **我們親手打造的主幹：** [StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)（因果引擎） · 顯式的 [Python](skills/00.1-Full-empirical-analysis-skill_Python/) / [Stata](skills/00.2-Full-empirical-analysis-skill_Stata/) / [R](skills/00.3-Full-empirical-analysis-skill_R/) 全流程移植 · [AER-skills](skills/50-brycewang-aer-skills/)（Top-5 投稿棧） · [chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/) · [Paper-WorkFlow](skills/69-Paper-WorkFlow/)（元調度器）。這些就是 AERS 的主幹 —— 完整對比見 [旗艦流水線 skills ↓](#旗艦流水線-skills)。想按用途瀏覽？參見 [同樣這 69 個、按用途分組 ↓](#69-個合集--按用途分組)。

---

**面向實證研究的專業級 Agent Skills 發行版。** 不是一份行銷清單 —— 本倉庫**自有並已編目 1,145 個 skill**，外加一套**數值基準 + 評測套件 + 安全稽核 + CI** 把品質焊死，再疊加一張涵蓋**生態 23,000+ skill / 119 個倉庫**的精選地圖。

AERS 同時是兩樣東西：(1) 一小撮**自研旗艦 skill**，能跑通完整實證流水線 —— 資料清洗 → 識別 → 估計 → 穩健性 → 表格圖形 → 可投稿初稿；(2) 一份**精選、安全可控的目錄**，按研究流程階段組織整個實證研究 skill 生態。我們的差異化不在數量，而在於：旗艦 skill 的行為是**對著已知答案驗證過的**，而不是嘴上聲稱的。

> [!NOTE]
> **已更名。** 本專案原名 *Awesome Agent Skills for Empirical Research*。GitHub 會自動重新導向舊網址，但請更新你的本機 remote：
> ```bash
> git remote set-url origin https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
> ```

---

## 目錄

- [**全部 69 個 skill 合集一覽**（完整 `00 → 69` 索引）](#全部-69-個-skill-合集一覽)
  - [69 個合集，按用途分組](#69-個合集--按用途分組)
- [你究竟得到什麼（精確數字）](#你究竟得到什麼精確數字)
- [2 分鐘自行驗證](#2-分鐘自行驗證)
- [為什麼值得信任 —— 三層信用錨點](#為什麼值得信任--三層信用錨點)
- [旗艦流水線 skills](#旗艦流水線-skills)
- [從這裡開始 —— 30 秒選一個 skill](#從這裡開始--30-秒選一個-skill)
- [憑什麼不只是 23K skill 的堆砌](#憑什麼不只是-23k-skill-的堆砌)
- [瀏覽全景](#瀏覽全景)
  - [工具目錄（tools/）](#工具目錄tools自動化實證與因果推斷工具)
  - [按研究流程](#按研究流程)
  - [綜合型 skill 套件](#綜合型-skill-套件)
  - [降 AIGC 偵測率 & 學術去 AI 味](#降-aigc-偵測率--學術去-ai-味)
  - [多代理系統 · MCP 伺服器 · 平台 · 學習資源](#多代理系統--mcp-伺服器--平台--學習資源)
- [安全掃描](#安全掃描)
- [更新日誌](#更新日誌)
- [貢獻與引用](#貢獻與引用)

---

## 69 個合集 · 按用途分組

> 與[頂部的順序索引 ↑](#全部-69-個-skill-合集一覽)相同的 **69 個合集 · 1,145 個 skill** —— 這裡**按研究用途**重新排序，方便你直接掃到正在進行的階段。**⭐ = 自研**（Stanford REAP × CoPaper.AI）；其餘皆為精選、經安全稽核的社群成果。

**🚀 全流程旗艦與調度器** —— *一次呼叫，跑完整個實證閉環*

| 合集 | 它能做什麼 | Skills |
|---|---|---:|
| ⭐ **[`00` · StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)** 🔥 | Agent-native Python **DSL** —— 一個 `sp.causal(...)` 跑 DID/RD/IV/SCM/DML | 1 |
| ⭐ **[`00.1` · Python](skills/00.1-Full-empirical-analysis-skill_Python/)** 📘 | 顯式棧：`pandas` · `statsmodels` · `linearmodels` · `pyfixest` | 1 |
| ⭐ **[`00.2` · Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)** 📊 | `reghdfe` · `ivreg2` · `csdid` · `sdid` · `rdrobust` 重現包 | 1 |
| ⭐ **[`00.3` · R](skills/00.3-Full-empirical-analysis-skill_R/)** 📗 | tidyverse · `fixest` · `did` · `HonestDiD`，透過 Quarto 算繪 | 1 |
| [`33` · claude-scholar](skills/33-Galaxy-Dawn-claude-scholar/) | 研究全生命週期：選題 → 審查 → 實驗 → 回覆 | 47 |
| [`42` · ARIS](skills/42-wanshuiyin-ARIS/) | 自主「睡眠中做研究」代理，端到端 | 104 |
| ⭐ **[`50` · AER-skills](skills/50-brycewang-aer-skills/)** 📕 | Top-5 經濟學投稿棧：識別 → 穩健性 → R&R | 9 |
| [`67` · econfin-workflow-toolkit](skills/67-econfin-workflow-toolkit/) | 中國公司金融實證工作流，提案 → 論文 | 46 |
| ⭐ **[`69` · Paper-WorkFlow](skills/69-Paper-WorkFlow/)** | 串起整條社會科學流水線的元調度器 | 1 |

**🎯 因果推斷與計量** —— *AERS 的方法論核心*

| 合集 | 它能做什麼 | Skills |
|---|---|---:|
| [`09` · awesome-econ-ai](skills/09-meleantonio-awesome-econ-ai-stuff/) | Python 面板資料分析（`linearmodels`） | 17 |
| [`10` · causal-inference-mixtape](skills/10-Jill0099-causal-inference-mixtape/) | DID / IV / RDD / SCM 範本（Cunningham） | 1 |
| [`11` · compound-science](skills/11-James-Traina-compound-science/) | 量化社會科學的貝氏估計 | 20 |
| [`13` · MixtapeTools](skills/13-scunning1975-MixtapeTools/) | Cunningham 的因果推斷工具箱與講義 | 5 |
| [`14` · research-starter](skills/14-luischanci-claude-code-research-starter/) | R 中的 IV / DiD / RDD，配套完整診斷 | 16 |
| [`15` · social-science-research](skills/15-Felpix-Studios-social-science-research/) | R 或 Python 端到端資料分析 | 12 |
| [`16` · clo-author](skills/16-hsantanna88-clo-author/) | 多代理資料分析（R / Stata / Python） | 10 |
| [`18` · stata-accounting](skills/18-jusi-aalto-stata-accounting-research/) | 取自 126 篇 *JAR* 論文的實測 Stata 範式 | 1 |
| [`20` · python-econ-skill](skills/20-wenddymacro-python-econ-skill/) | DSGE / HANK 與量化經濟計算 | 1 |
| [`23` · baygent](skills/23-Learning-Bayesian-Statistics-baygent-skills/) | 帶護欄的 PyMC / ArviZ 貝氏工作流 | 2 |
| [`26` · scholar](skills/26-Data-Wise-scholar/) | 統計演算法設計與文件化 | 17 |
| [`31` · claude-code-skills](skills/31-thalysandratos-claude-code-skills/) | Python 面板資料分析 | 13 |
| [`39` · marginaleffects](skills/39-vincentarelbundock-marginaleffects/) | 預測、斜率與比較（R / Python） | 1 |
| [`40` · pyfixest](skills/40-py-econometrics-pyfixest/) | Python 中的快速固定效應估計 | 1 |
| [`51` · CausalPy](skills/51-pymc-labs-CausalPy/) | 貝氏準實驗（PyMC Labs） | 3 |
| [`55` · r-skills](skills/55-ab604-claude-code-r-skills/) | R 中以 `brms` 做貝氏推論 | 8 |
| [`61` · research-methods](skills/61-phdemotions-research-methods/) | 與預註冊對齊的驗證性檢驗 | 9 |
| [`63` · scientific-agent-skills](skills/63-tondevrel-scientific-agent-skills/) | DoWhy 識別–估計–反駁框架 | 2 |
| [`64` · mcp-stata](skills/64-tmonk-mcp-stata/) | 20 個 Stata 因果推斷與重現 skill | 20 |

**📚 文獻、閱讀與研究設計** —— *從問題到證據基礎*

| 合集 | 它能做什麼 | Skills |
|---|---|---:|
| [`02` · research-skills](skills/02-luwill-research-skills/) | 醫學影像綜述、研究提案、論文轉投影片 | 3 |
| [`03` · scientific-skills](skills/03-K-Dense-AI-claude-scientific-skills/) | 假設生成 + 28 個科學資料庫 | 4 |
| [`05` · research-superpower](skills/05-kthorn-research-superpower/) | 系統化檢索、篩選與引用溯源 | 10 |
| [`25` · Diverga](skills/25-HosungYou-Diverga/) | 研究問題精煉器（抗模式坍縮） | 34 |
| [`34` · research-companion](skills/34-andrehuang-research-companion/) | 腦力激盪、評估與決定研究方向 | 1 |
| [`35` · academic-writing-skills](skills/35-bahayonghang-academic-writing-skills/) | 場景感知的工業 AI 文獻研究 | 5 |
| [`36` · literature-review-skill](skills/36-taoyunudt-literature-review-skill/) | 完整文獻綜述工作流（中文） | 1 |
| [`52` · slr-prisma](skills/52-keemanxp-slr-prisma/) | 系統性文獻綜述，PRISMA 2020 | 1 |
| [`53` · thematic-analysis](skills/53-keemanxp-thematic-analysis-skill/) | Braun & Clarke 六階段質性主題分析 | 1 |
| [`59` · openalex-skill](skills/59-shiquda-openalex-skill/) | 透過 OpenAlex 查詢 2.4 億+ 學術成果 | 1 |
| [`60` · superpapers](skills/60-regisely-superpapers/) | 全面的實證研究支援套件 | 16 |

**✍️ 寫作、編修與去 AIGC** —— *起草、潤色，並通過 AI 偵測*

| 合集 | 它能做什麼 | Skills |
|---|---|---:|
| [`01` · academic-paper-skills](skills/01-lishix520-academic-paper-skills/) | 大綱 → 手稿寫作 + 7 維審稿人模擬 | 2 |
| [`04` · scientific-writer](skills/04-K-Dense-AI-claude-scientific-writer/) | 引用管理 + 科學寫作 | 8 |
| [`06` · stats-paper-writing](skills/06-fuhaoda-stats-paper-writing/) | 端到端 LaTeX 統計論文寫作 | 1 |
| [`22` · christopherkenny-skills](skills/22-christopherkenny-skills/) | Quarto（`.qmd`）的 APSA 風格檢查器 | 11 |
| [`27` · my_claude_skills](skills/27-dariia-m-my_claude_skills/) | 經濟學摘要寫作指南 | 6 |
| [`38` · academic-proofreader](skills/38-peternka-academic-proofreader/) | 學術校對 | 1 |
| [`44` · humanizer_academic](skills/44-matsuikentaro1-humanizer_academic/) | 去 AI 化醫學/學術手稿（23 種模式） | 1 |
| [`45` · deslop](skills/45-stephenturner-skill-deslop/) | 移除 AI 寫作模式（5 維評分） | 1 |
| [`46` · stop-slop](skills/46-hardikpandya-stop-slop/) | 3 層 AI 痕跡偵測與改寫 | 1 |
| [`47` · avoid-ai-writing](skills/47-conorbronsdon-avoid-ai-writing/) | 稽核 → 改寫 → 複稽 AI 腔（留痕） | 1 |
| ⭐ **[`48` · chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/)** 🇨🇳 | 面向知網 / 萬方 / Turnitin 中文版的中文去 AIGC | 1 |
| [`49` · humanize-chinese](skills/49-voidborne-d-humanize-chinese/) | 偵測並擬人化 AI 生成的中文文字 | 1 |
| [`56` · econ-writing-skill](skills/56-hanlulong-econ-writing-skill/) | 綜合 50+ 頂級指南的經濟學寫作 | 1 |
| [`58` · econstack](skills/58-charlescoverdale-econstack/) | 政策簡報（UK GES / AU Treasury） | 7 |
| [`65` · game-theory-paper-writer](skills/65-game-theory-paper-writer/) | 生成並壓力測試賽局理論論文 | 1 |

**📑 引用、重現與同儕審稿** —— *讓成果可驗證、可重現*

| 合集 | 它能做什麼 | Skills |
|---|---|---:|
| [`24` · academic-research-skills](skills/24-Imbad0202-academic-research-skills/) | 5 審稿人多視角論文審查 | 4 |
| [`28` · paper-replicate-agent](skills/28-maxwell2732-paper-replicate-agent-demo/) | 論文重現代理 demo | 11 |
| [`29` · project20XXy](skills/29-quarcs-lab-project20XXy/) | 可重現的手稿 + notebook 專案 | 24 |
| [`41` · sewage-econometrics-check](skills/41-sticerd-eee-sewage-econometrics-check/) | 10 項檢查的重現包稽核 | 22 |
| [`54` · open-science-skills](skills/54-scdenney-open-science-skills/) | 引用一致性、DOI 與主張佐證稽核 | 24 |
| [`62` · citation-checker](skills/62-PHY041-claude-skill-citation-checker/) | 對照 CrossRef / S2 / OpenAlex 驗證引用 | 1 |

**🛠️ 資料、工具與基礎設施** —— *流水線底下的管路*

| 合集 | 它能做什麼 | Skills |
|---|---|---:|
| [`07` · AI-Research-SKILLs](skills/07-Orchestra-Research-AI-Research-SKILLs/) | 發表級 ML 圖形、LaTeX、引用驗證 | 3 |
| [`08` · latex-document-skill](skills/08-ndpvt-web-latex-document-skill/) | 建立 / 編譯任意 LaTeX 文件為 PDF | 1 |
| [`12` · claude-code-my-workflow](skills/12-pedrohcgs-claude-code-my-workflow/) | Commit → PR → merge 研究工作流（Emory） | 22 |
| [`17` · DAAF](skills/17-DAAF-Contribution-Community-daaf/) | 安全意識代理框架（32 條 deny 規則） | 35 |
| [`32` · stata-skill](skills/32-dylantmoore-stata-skill/) | 高效能 Stata C/C++ plugin | 3 |
| [`43` · research-plugins](skills/43-wentorai-research-plugins/) | 478 個研究外掛：資料視覺化、領域、基礎設施 | 478 |
| [`57` · edgartools](skills/57-dgunning-edgartools/) | 查詢與分析 SEC 申報文件 | 1 |
| [`66` · empirical-research-skills](skills/66-zheng-siyao-empirical-research-skills/) | 大型面板的 R 效能最佳化 | 7 |
| [`68` · research-productivity-skills](skills/68-research-productivity-skills/) | 論文檢索、SSRN、DOI 查詢、下載 | 18 |

---

## 你究竟得到什麼（精確數字）

本 README 的數字一律精確、可辯護、不混淆。「自有（vendored）」指檔案就在本倉庫裡、並被生成式 catalog 追蹤；「生態目錄」指對外部倉庫的精選連結。

| 它是什麼 | 數量 | 事實來源 |
|---|---:|---|
| **本倉庫自有**並已編目的 skill | **1,145** | [`catalog/skills.json`](catalog/skills.json) |
| 自有 **合集（collections）** | **69** | [`catalog/skills.json`](catalog/skills.json) · [全部 69 個一覽 ↑](#全部-69-個-skill-合集一覽) |
| **自研旗艦**全流程 skill（StatsPAI DSL + 顯式 Python/Stata/R） | **4** | [`skills/00*`](skills/) |
| 每次執行從資料**重算 gold 值**的數值基準任務 | **5** | [`benchmark/`](benchmark/) |
| 行為級**評測場景 / rubric 條目** | **17 / 95** | [`eval-harness/`](eval-harness/) |
| **原始基線**安全稽核（合集 / 檔案） | **52 / 2,940+**，52/52 CLEAN | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| 涵蓋**更廣生態**的精選地圖 | **23,000+ skill / 119 倉庫** | 本 README · [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md) |
| **工具目錄**（`tools/`）：因果/計量庫、自動化研究 Agent、MCP 服務、因果發現、基準資料集 | **335 工具 / 6 類** | [`tools/tools.json`](tools/tools.json) · [`tools/CATALOG.md`](tools/CATALOG.md) |

> 安全稽核涵蓋的是**原始 52 合集 / 2,940 檔案的基線（52/52 CLEAN）**。在該基線之後新增的 vendor skill 由 [`catalog/provenance.json`](catalog/provenance.json)、[`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md)、[`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md) 追蹤；高信任場景使用前請先 `make audit` 複核。

---

## 2 分鐘自行驗證

這裡最有說服力的不是某個數字，而是：旗艦流水線的行為**不需要 API key、不需要付費模型就能複核**。只要 Python 3：

```bash
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git
cd Auto-Empirical-Research-Skills
make check        # 仓库校验 + 单元测试 + eval lint + 数值基准
```

基準是最關鍵的部分：它**每次執行都從原始資料集重算 gold 答案**，所以分數無法靠寫死一個數字矇混過關。開箱即可重現：

- **LaLonde (1986) / Dehejia–Wahba (1999)** —— 樸素觀察性比較給出*錯誤符號*（−$635）；加入共變數調整後翻正（≈ +$1,548），逼近實驗基準（≈ +$1,794）。
- **Card (1995)** —— IV 教育報酬（0.131）*高於* OLS（0.075），且第一階段 F（13.3）如實報告而非藏起來。
- 另含交錯 DID（TWFE 偏誤 vs group-time 真值）、斷點 **RDD**，以及一個**壞控制 / 後處理偏誤**陷阱。

只有當流水線**暴露陷阱、拒絕把誤導性數字當頭條、並匹配重算真值**時才算通過。詳見 [`benchmark/`](benchmark/) 與完整信任說明 [`docs/TRUST.md`](docs/TRUST.md)。

> 💡 **想要託管版、開箱即用？** 不必自己拼裝 —— [**copaper.ai**](https://copaper.ai) 由同一支史丹佛方法論團隊在打造本目錄的同時建構，直接替你跑完整實證流水線。

---

## 為什麼值得信任 —— 三層信用錨點

| 層級 | 錨點 | 它帶來什麼 |
|---|---|---|
| 🏛️ **學術血統** | **[Stanford REAP / SCCEI](https://sccei.fsi.stanford.edu/reap)** 中國經濟與制度研究中心 | 在實證經濟學方法論上有持續發表傳統、在應用因果推斷上有深厚積累的研究中心。 |
| 🔧 **工程落地** | **[CoPaper.AI](https://copaper.ai)** 實證研究 AI 助手 | 內建 **20 個計量方法論 skill**（DID / IV / RDD / PSM / DML 等），Supervisor + 4 子代理架構，一句話觸發，自動產出發表級結果。 |
| ⚙️ **開源引擎** | **[StatsPAI](https://github.com/brycewang-stanford/StatsPAI)** —— 因果推斷引擎 | **900+ 函式 · 一個 `import statspai as sp` · JOSS 投稿中 · MIT。** CoPaper.AI 跑出的每一個 DID / IV / RD / SCM 估計都由 StatsPAI 驅動，而本目錄正是該生態的一部分。 |

---

## 旗艦流水線 skills

四個並行實作，跑的是**同一套 8 步實證閉環** —— *資料清洗 → 變數構造 → 描述統計 → 診斷檢驗 → 估計 → 穩健性 → 機制/異質性 → 發表級表圖* —— 再加上投稿與去 AIGC 兩條線。每個都採用**漸進式揭露**：`SKILL.md` 只放一條主幹（每步的標準呼叫），分步深度手冊按需載入。它們並存共生，按技術棧和場景挑選即可。

| Skill | 技術棧 | 最適合 |
|---|---|---|
| **[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)** 🔥 | Agent-native Python **DSL** —— 一個 `sp.causal(...)` 跑完閉環；900+ 函式，自描述 API，統一 `CausalResult` | 信任 DSL 時，一句 agent 指令完成全流程自動化 |
| **[Full Empirical Analysis — Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md)** 📘 | **顯式**棧：`pandas` · `statsmodels` · `linearmodels` · `pyfixest` · `rdrobust` · `econml` · `causalml` | 教學、審稿人級逐行稽核、需要完全控制的嚴謹重現 |
| **[Full Empirical Analysis — Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md)** 📊 | 社群事實標準：`reghdfe` · `ivreg2` · `csdid` · `did_imputation` · `sdid` · `rdrobust` · `synth` · `psmatch2` · `boottest` · `esttab` | 審稿人或合作者只接受 Stata 重現包時（AER/QJE/JPE/ReStud 風格） |
| **[Full Empirical Analysis — R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)** 📗 | 現代 tidyverse：`fixest` · `did` · `synthdid` · `HonestDiD` · `rdrobust` · `grf` · `DoubleML` · `marginaleffects` · **Quarto** | 單個 `.qmd` 一鍵算繪 PDF/HTML/Word 的一體化重現報告 |
| **[AER-Skills](skills/50-brycewang-aer-skills/)** 📕 | 9 個 skill：選題路由 → 識別稽核 → 穩健性 → 引言 → 表圖 → 重現 → 投稿 → R&R → 總調度 | Top-5 經濟學（AER / AER:Insights / AEJ）投稿：**識別優先** —— 設計若脆，再多 prose 也救不回來 |
| **[chinese-de-aigc](skills/48-copaper-ai-chinese-de-aigc/SKILL.md)** 🇨🇳 | 17 類中文 AI 痕跡模式庫，五步「定位→診斷→改寫→自評→複查」閉環 | 降低知網 / 萬方 / 維普 / Turnitin 中文版的 AI 寫作訊號 |
| **[Paper-WorkFlow](skills/69-Paper-WorkFlow/README.md)** 🧭 | **元調度器**，串起 Stage 0–9 —— 選題 → 設計 → 資料 → 估計 → 表格/圖形 → 初稿 → 潤色 → 去 AIGC → 模擬審稿 → 投稿 —— 透過調度既有 skill 與並行子代理，並以可續跑的 `workflow_state.json` 記錄狀態 | 端到端自動跑完一篇完整的實證社會科學論文 |

> **為什麼既要 DSL 又要顯式三件套？** 信任一鍵 DSL 時用 StatsPAI；做教學、稽核、或要逐個替換診斷時用 00.1/00.2/00.3。AER-skills 再把一份正確的分析推到錄取門檻 —— 它們解決的是*不同*問題，可以組合。

---

## 從這裡開始 —— 30 秒選一個 skill

| 目標 | 從這裡開始 |
|---|---|
| 跑完整實證流水線 | [`StatsPAI`](skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)（或 [Python](skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md) · [Stata](skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md) · [R](skills/00.3-Full-empirical-analysis-skill_R/SKILL.md)） |
| 先審頂刊識別策略 | [`aer-identification`](skills/50-brycewang-aer-skills/skills/aer-identification/SKILL.md) |
| 準備 AER / AEJ 投稿 | [`aer-workflow`](skills/50-brycewang-aer-skills/skills/aer-workflow/SKILL.md) |
| 整理 AEA 合規的重現包 | [`aer-replication`](skills/50-brycewang-aer-skills/skills/aer-replication/SKILL.md) |
| 降低中文初稿的 AI 寫作痕跡 | [`chinese-de-aigc`](skills/48-copaper-ai-chinese-de-aigc/SKILL.md) |

**更多入口：**

- **不確定用哪個？** → [`docs/CHOOSING_A_SKILL.md`](docs/CHOOSING_A_SKILL.md) · 分面搜尋：[`docs/search.html`](docs/search.html)
- **端到端走通前 10 分鐘** → [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)
- **直接複製完整工作流** → [`docs/GOLDEN_WORKFLOWS.md`](docs/GOLDEN_WORKFLOWS.md)
- **裝進 runtime / 免安裝使用** → [`docs/INSTALL.md`](docs/INSTALL.md)
- **機器可讀索引** → [`catalog/skills.json`](catalog/skills.json) · 分類法：[`docs/TAXONOMY.md`](docs/TAXONOMY.md) · 完整目錄：[`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md)
- **常見問題** → [`docs/FAQ.md`](docs/FAQ.md)

---

## 憑什麼不只是 23K skill 的堆砌

公開 skill 的數量很容易灌水，近期研究也表明大型 skill 索引常常冗餘、偶爾不安全。AERS 比拼的是**可驗證的品質**，不是裸數量。下面每一層都能本機 `make check`、也都在 CI 裡跑。

| 層 | 它能擋住什麼 | 在哪 |
|---|---|---|
| **數值基準** | 報告數字與真實資料重算真值不符 —— 樸素 DID 符號陷阱、缺第一階段 F 的弱 IV、交錯時點下的 TWFE 偏誤、RDD 趨勢混淆、後處理壞控制 | [`benchmark/`](benchmark/) · 5 任務 |
| **評測套件** | 散文級失誤：弱 IV 假性安心、交錯 DID 誤用 TWFE、編造引用、不安全的 `curl \| bash` 安裝、多重檢驗濫用、AER 合規缺口 | [`eval-harness/`](eval-harness/) · 17 場景 / 95 rubric |
| **安全稽核** | pipe-to-shell、反向 shell、憑據外洩、prompt 注入等 13 類風險 —— 六階段，40+ hook 腳本人工核查 | [`SECURITY-SCAN-REPORT.md`](SECURITY-SCAN-REPORT.md) |
| **來源與授權** | 未聲明來源、授權風險、1,145 個編目 skill 的衛生度漂移 | [`docs/LICENSE_AUDIT.md`](docs/LICENSE_AUDIT.md) · [`docs/SKILL_QUALITY.md`](docs/SKILL_QUALITY.md) |
| **CI 與相容性** | catalog 新鮮度、本機死連、GitHub Actions 政策、Python 3.9 **與** 3.12 語法基線 | [`.github/workflows/`](.github/workflows/) · 6 條 workflow |

```bash
make catalog     # 重新生成 catalog、provenance、audit、enrichment
make validate    # 新鲜度 + 链接 / frontmatter 检查
make check       # 完整 gate：validate + Python 编译 + 单元测试 + eval lint + benchmark
```

這套信任面是**必要而非充分** —— 正則 rubric 不能認證文筆，小基準也涵蓋不了每一種設計。它的設計目標是*對已知高代價錯誤快速失敗*。誠實的邊界說明見 [`docs/TRUST.md`](docs/TRUST.md) 與 [`docs/QUALITY_GATE.md`](docs/QUALITY_GATE.md)。

---

## 瀏覽全景

> 📚 完整的 **[69 個合集目錄 ↑](#全部-69-個-skill-合集一覽)** 在本 README 頂部 —— 本節按主題深入這個生態。

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

各階段 skill 速查（中英雙語）：[01 選題與研究設計](docs/01-选题与研究设计.md) · [02 文獻檢索與綜述](docs/02-文献检索与综述.md) · [03 論文閱讀與拆解](docs/03-论文阅读与拆解.md) · [04 資料獲取與清洗](docs/04-数据获取与清洗.md) · [05 統計分析與因果推斷](docs/05-统计分析与因果推断.md) · [06 論文寫作](docs/06-论文写作.md) · [07 論文修改與潤色](docs/07-论文修改与润色.md) · [08 引用管理與排版](docs/08-引用管理与排版.md) · [09 論文重現與可重現研究](docs/09-论文复现与可复现研究.md) · [10 審稿回覆與學術答辯](docs/10-审稿回复与学术答辩.md)

### 綜合型 skill 套件

> AERS 要解決的痛點：讓 AI 跑一個 DID，它給了基準迴歸就停了。「平行趨勢呢？」—— 補一個。「安慰劑呢？」—— 再補一個。*每次都像擠牙膏。* 而 skill 是給 agent 的**方法論操作手冊**：它已經知道一個完整的 DID 意味著 平行趨勢 → 基準 → 穩健性矩陣 → 異質性 → 機制，每一步該輸出什麼也都定好了。

<details>
<summary><b>學術研究專用</b> —— 通用型研究套件（K-Dense、AI-Research-SKILLs、claude-scholar 等）</summary>

| 套件 | Stars | Skills 數 | 核心特色 |
|------|-------|----------|---------|
| [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) | 8,799 | 140+ | 28+ 科學資料庫（OpenAlex、PubMed）；scientific-writing + literature-review + statistical-analysis |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 3,637 | 87 | 22 個類別，ML 論文寫作，LaTeX 範本，引文驗證 |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | ~1,790 | 多個 | 完整論文管線（research → write → review → revise → finalize），風格校準，幻覺偵測 |
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | - | 25+ | 研究全生命週期：選題 → 綜述 → 實驗 → 寫作 → 審稿回覆；整合 Zotero MCP |
| [luwill/research-skills](https://github.com/luwill/research-skills) | 209 | 3 | 研究提案生成、醫學綜述寫作、論文轉投影片，雙語 |
| [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | 22 | 2 | Strategist（7 維審稿人模擬）+ Composer（系統化寫作） |
| [Data-Wise/claude-plugins](https://github.com/Data-Wise/claude-plugins) | - | 17 | 統計研究：arXiv 搜尋、DOI 查詢、BibTeX、方法論寫作、審稿回覆 |

</details>

<details>
<summary><b>經濟學 / 因果推斷專用</b> —— 自研旗艦 + 社群 Stata/IV/預審套件</summary>

自研旗艦（[StatsPAI](skills/00-Full-empirical-analysis-skill_StatsPAI/)、[Python](skills/00.1-Full-empirical-analysis-skill_Python/)、[Stata](skills/00.2-Full-empirical-analysis-skill_Stata/)、[R](skills/00.3-Full-empirical-analysis-skill_R/)、[AER-skills](skills/50-brycewang-aer-skills/)）已在[上文](#旗艦流水線-skills)詳述。社群補充：

| 套件 | 核心特色 | 適用場景 |
|------|---------|---------|
| **[CoPaper.AI](https://copaper.ai)** | 20 個方法論 skill，Supervisor + 4 子代理，智慧路由，結果自動輸出 | 經濟學實證全流程（託管版） |
| [claesbackman/AI-research-feedback](https://github.com/claesbackman/AI-research-feedback) | 2 代理預審：因果過度聲稱偵測、識別策略評估（AER/QJE/JPE/Econometrica/REStud）；6 代理基金評審 | 投稿前自審、基金申請 |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | LaTeX 統計論文寫作，前端草稿生成 | 統計學、計量經濟學論文 |
| [dylantmoore/stata-skill](https://github.com/dylantmoore/stata-skill) | Stata 全涵蓋：語法、資料管理、計量、因果推斷、Mata、20+ 社群套件 | Stata 使用者 |
| [SepineTam/stata-mcp](https://github.com/SepineTam/stata-mcp) | LLM 透過 MCP 直接驅動 Stata 迴歸 | Stata 計量分析 |
| [hanlulong/stata-mcp](https://github.com/hanlulong/stata-mcp) | Stata-MCP 編輯器擴充（VS Code/Cursor/Antigravity）：直接跑 `.do`、即時輸出、資料/圖檢視；MIT · 414★（與上方 SepineTam 同名不同專案） | 編輯器內 AI 協作跑 Stata |
| [tmonk/mcp-stata](https://github.com/tmonk/mcp-stata) · 已收錄 [`skills/64`](skills/64-tmonk-mcp-stata/) | Stata MCP server 的 **20 個 SKILL.md**：重現 / 資料稽核 / 發表 QA / 舊碼現代化 / referee 回應 / power / 因果推斷；**AGPL-3.0**（聚合保留原授權，未 vendor 伺服端程式碼） | Stata 重現與穩健性稽核 |
| [PovertyAction/ipa-stata-template](https://github.com/PovertyAction/ipa-stata-template) | IPA 可重現 Stata 研究範本 + `.claude/skills`：編號流水線、斷言式防禦編程、LaTeX 表格；MIT | 發展經濟學 / 田野實證重現 |
| [lcrawfurd/claude-skills](https://github.com/lcrawfurd/claude-skills) | 學術 skill：paper / code review、referee、預審；code-review 內建 Stata/R/Python 編碼規範（DIME / Reif / AEA Data Editor） | 投稿前審稿與程式碼複核 |
| [AEADataEditor/replication-template](https://github.com/AEADataEditor/replication-template) | AEA 資料主編官方重現包範本（Stata 為主，`REPLICATION.md`）—— 經濟學重現「黃金標準」 | AEA / 頂刊重現包打包 |

</details>

<details>
<summary><b>金融 · 教育與公共衛生 · 法律 · 行銷 · 產品 · 通用 agent</b></summary>

**金融與投資** —— [financial-services-plugins](https://github.com/anthropics/financial-services-plugins)（Anthropic 官方）· [OctagonAI/skills](https://github.com/OctagonAI/skills) · [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) · [himself65/finance-skills](https://github.com/himself65/finance-skills) · [quant-sentiment-ai/claude-equity-research](https://github.com/quant-sentiment-ai/claude-equity-research)

**教育與公共衛生** —— [GarethManning/claude-education-skills](https://github.com/GarethManning/claude-education-skills) · [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills)（**869** 個醫學 skill：流行病學、監測、臨床研究、藥物安全、生物統計）

**治理、合規與法律** —— [Claude-Skills-Governance-Risk-and-Compliance](https://github.com/Sushegaad/Claude-Skills-Governance-Risk-and-Compliance)（ISO 27001 / SOC 2 / GDPR / HIPAA）· [zubair-trabzada/ai-legal-claude](https://github.com/zubair-trabzada/ai-legal-claude) · [evolsb/claude-legal-skill](https://github.com/evolsb/claude-legal-skill)

**行銷與消費者行為** —— [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) · [zubair-trabzada/ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude) · [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills)

**產品與組織行為** —— [phuryn/pm-skills](https://github.com/phuryn/pm-skills)（100+ skill）· [mastepanoski/claude-skills](https://github.com/mastepanoski/claude-skills)（Nielsen 啟發式、NIST AI RMF、ISO 42001）

**通用 agent 能力** —— [lyndonkl/claude](https://github.com/lyndonkl/claude)（85 skill + 6 編排器）· [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)（220+ skill，~5,200★）· [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) · [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)（1,367 skill）· [posit-dev/skills](https://github.com/posit-dev/skills)（Posit 官方）

</details>

### 降 AIGC 偵測率 & 學術去 AI 味

> 2026 年學術寫作最尖銳的痛點之一：論文 AIGC 率超標（Turnitin、GPTZero、知網）可被一票否決。下面這幾個 skill 是目前最完整的開源方案 —— 全部 MIT，全部本機收錄（`skills/44-49`）。

| 套件 | 核心特色 | 最適合 | 本機 |
|------|---------|--------|------|
| **chinese-de-aigc** 🇨🇳 | CoPaper.AI **原創**中文學術去 AIGC；17 類中文痕跡模式庫、五步閉環、分章節策略、五維評分。目前 GitHub 上唯一面向中文學術去 AIGC 的 skill | 知網 / 萬方 / 維普 / Turnitin 中文版 | [`48`](skills/48-copaper-ai-chinese-de-aigc/) |
| [voidborne-d/humanize-chinese](skills/49-voidborne-d-humanize-chinese/) 🇨🇳 | 同時提供 SKILL.md 與獨立 Python CLI；17 類偵測 + 7 風格改寫器，LR ensemble 程序化打分。**License: MIT（非商用修改版）** | 中文學位論文 / 長篇 / 批量 pipeline | [`49`](skills/49-voidborne-d-humanize-chinese/) |
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | 學術專用；23 類 AI 寫作模式；保留合法學術過渡詞 | 醫學、生命科學、自然科學論文 | [`44`](skills/44-matsuikentaro1-humanizer_academic/) |
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) | 智慧區分合法學科慣例 vs AI 痕跡；5 維評分 | 科學論文、技術部落格 | [`45`](skills/45-stephenturner-skill-deslop/) |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 三層偵測 + 五維評分；禁用短語、結構套路、句級規則 | 通用散文、部落格、報告 | [`46`](skills/46-hardikpandya-stop-slop/) |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 結構化稽核 + 重寫 + 二次稽核；可稽核、可追溯 | 需要留痕的修改流程 | [`47`](skills/47-conorbronsdon-avoid-ai-writing/) |

> **組合建議：** 🇨🇳 中文（知網/萬方/維普）→ chinese-de-aigc · 🇬🇧 英文 → humanizer_academic · 需要稽核留痕 → avoid-ai-writing · 通用散文 → stop-slop。

### 工具目錄（tools/）：自動化實證與因果推斷工具

> 與上面的 skill 不同，[`tools/`](tools/) 收錄的是 agent / 研究者**實際呼叫的軟體與服務**——已結構化編目、核實過 license 與維護狀態，並接入 `make validate`。事實源 [`tools/tools.json`](tools/tools.json)，可瀏覽清單 [`tools/CATALOG.md`](tools/CATALOG.md)。

**335 個工具 / 6 類**（2026-06 收錄）：

- **因果推斷 / 處理效應庫（32）** — DoWhy · EconML · CausalML · DoubleML · CausalPy · causallib · grf · CATENets · TMLE 系列 · 孟德爾隨機化 …
- **計量 / 準實驗庫（170）** — 面板FE · DiD（含現代/staggered）· 事件研究 · RDD · IV · 合成控制/SDID · 匹配加權 · 敏感性分析（fixest · did · HonestDiD · rdrobust · synthdid · reghdfe · csdid · sdid · pyfixest · linearmodels …）；**新增**空間計量（spdep · PySAL/spreg · GeoDa）· 局部投影/IRF & (S)VAR（lpirfs · vars · svars）· 調查加權/MRP/raking（survey · samplics · balance）· 元分析（metafor · meta · netmeta · metan）；橫跨 R/Python/Stata/Julia。
- **自動化研究 / 資料科學 Agent（51）** — 端到端自動做科研/資料分析：AI-Scientist · data-to-paper · Agent Laboratory · RD-Agent · AI-Researcher · STORM · PaperQA2 · gpt-researcher · DeepAnalyze · MetaGPT(DI) · Biomni …（⚠️ 含非 OSI/無 LICENSE 倉庫，用前確認授權）。
- **MCP 服務（48）** — 統計執行（StatsPAI · stata-mcp · R / Jupyter MCP）+ 資料獲取（FRED · World Bank · IMF · OECD · Eurostat · Census · BEA · BLS · SEC EDGAR · OpenAlex · Semantic Scholar · PubMed · Zotero · arXiv …）。
- **因果發現 / 結構學習（25）** — causal-learn · Tetrad / py-tetrad · gCastle · CDT · tigramite(PCMCI) · LiNGAM · NOTEARS / DAGMA · pcalg · bnlearn · pgmpy …
- **基準與資料集（9）** — causaldata · IHDP / Twins · ACIC 競賽資料 · RealCause · JustCause · Tübingen cause-effect pairs · bnlearn 網路庫 …

完整說明見 [`tools/README.md`](tools/README.md)。

### 多代理系統 · MCP 伺服器 · 平台 · 學習資源

<details>
<summary><b>多代理協作系統</b> —— 論文修改、自主研究、資料科學團隊</summary>

角色分離之所以勝過單 agent：審閱者獨立於起草者，才能形成真正的品質閉環 —— 與同行評審同理。

**論文修改與寫作：** copy-edit-master（3 子代理，Strunk & White / McCloskey 規則）· introduction-writer（strategist → drafter → reviewer → reviser）· CoPaper.AI PaperAgent（Supervisor + 4 子代理）。

**自主研究與資料科學：** [ruc-datalab/DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze)（人民大學）· [business-science/ai-data-science-team](https://github.com/business-science/ai-data-science-team) · [HKUDS/AI-Researcher](https://github.com/HKUDS/AI-Researcher)（NeurIPS 2025 Spotlight）· [wanshuiyin/ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) · [SamuelSchmidgall/AgentLaboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)（成本降 84%）· [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) · [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) · [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow)（Emory）。

</details>

<details>
<summary><b>學術資料 MCP 伺服器</b> —— OpenAlex、Semantic Scholar、FRED、World Bank、Zotero 等</summary>

[xingyulu23/Academix](https://github.com/xingyulu23/Academix) · [Eclipse-Cj/paper-distill-mcp](https://github.com/Eclipse-Cj/paper-distill-mcp) · [oksure/openalex-research-mcp](https://github.com/oksure/openalex-research-mcp)（2.4 億+ 作品）· [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp)（20+ 來源）· [lzinga/us-gov-open-data-mcp](https://github.com/lzinga/us-gov-open-data-mcp)（40+ 美國政府 API）· [stefanoamorelli/fred-mcp-server](https://github.com/stefanoamorelli/fred-mcp-server)（FRED 80 萬+ 序列）· [llnOrmll/world-bank-data-mcp](https://github.com/llnormll/world-bank-data-mcp) · [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)

</details>

<details>
<summary><b>Skill 聚合平台與學習資源</b></summary>

**平台：** [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)（1,000+）· [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)（1,340+）· [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)（5,400+）· [skills.sh](https://skills.sh/) · [ClawHub](https://clawhub.com)（13,729）· [Anthropic 官方 skills](https://github.com/anthropics/skills)。

**學習：** [Claude Code Skills 完全指南（PDF）](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) · [Agent Skills 標準](https://agentskills.io/) · [Causal Inference for the Brave and True](https://github.com/xieliaing/CausalInferenceIntro)（中文版）· [Awesome AI for Economists](https://github.com/hanlulong/awesome-ai-for-economists) · [Awesome Econ AI Stuff](https://github.com/meleantonio/awesome-econ-ai-stuff)。

</details>

---

## 安全掃描

倉庫**原始 52 個 skill 合集 / 2,940+ 檔案**通過了系統性稽核 —— **52/52 全部 CLEAN，零 FLAGGED**：未發現任何惡意 prompt、病毒、反向 shell 或 prompt 注入。所有看似敏感的命中，經驗證後均歸入三類合法內容：**防禦性安全規則**、**合法學術 API 呼叫**（arXiv / CrossRef / PubMed / FRED / World Bank / OECD / BLS）、或**標準 Claude Code 工作流 hook**（全部本機檔案操作、零網路 IO）。

![Skills 安全掃描總覽](images/security-scan/security-scan-01-overview.png)

六階段、縱深防禦：13 類風險維度自動 grep → 6 個含 hook 的 skill 及其 40+ hook 腳本 100% 人工核查（全倉**無 `Bash(*)` 萬用字元**）→ 三 agent 並行內容審查 → 補充完整性檢查（隱藏 Unicode、編碼異常、HTML 注入、網路 import）。

> **關鍵洞察：** 規模最大 ≠ 風險最高。體量最大的幾個 skill 全部通過；[17-DAAF](skills/17-DAAF-Contribution-Community-daaf/) 反而樹立了安全意識標竿（14 個防禦 hook + 32 條 deny rule + 主動憑據掃描）。

基線之後新增的 vendor skill 由 [`catalog/provenance.json`](catalog/provenance.json) 與 [`docs/SKILL_AUDIT.md`](docs/SKILL_AUDIT.md) 追蹤 —— 請 `make audit`。完整報告：[**SECURITY-SCAN-REPORT.md**](SECURITY-SCAN-REPORT.md)。

---

## 更新日誌

敘事版更新日誌已遷至 [**CHANGELOG.md**](CHANGELOG.md)。近期要點：

- **2026-05** —— 收錄 **AER-skills**（Top-5 經濟學投稿套件，9 個 skill）並設週更上游同步；數值基準擴到 **5 個因果復原任務**、評測套件擴到 **17 場景 / 95 rubric**。
- **2026-04** —— 完成 **52/52 安全基線**；交付四個全流程旗艦（**StatsPAI** + 顯式 **Python / Stata / R**）；上線原創 **chinese-de-aigc** skill。
- **更早** —— 從 43 個合集成長為涵蓋 **119 倉庫 / 23,000+ skill** 的精選地圖；新增雙語 README、學術資料 MCP 伺服器與多代理系統。

---

## 貢獻與引用

歡迎貢獻 —— 請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 與 [`docs/SKILL_SUBMISSION_GUIDE.md`](docs/SKILL_SUBMISSION_GUIDE.md)。我們特別歡迎社會科學 skill（經濟學、政治學、社會學、心理學、教育、公共衛生）、因果推斷方法的新實作、學術/政府資料的 MCP 伺服器、中文友善的 skill、以及多代理案例。新提交須聲明 **來源、授權、類別** 以供 provenance 稽核。

如果 AERS 對你的工作有幫助，請**引用它**（[CITATION.cff](CITATION.cff)）並**點個 Star**，讓更多研究者看到。

<a href="https://www.star-history.com/#brycewang-stanford/Auto-Empirical-Research-Skills&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=brycewang-stanford%2FAuto-Empirical-Research-Skills&type=Date" width="600" />
 </picture>
</a>

---

<div align="center">

**AI 是放大器，不是替代品。它替你做最耗時的「搬磚」，你保留最核心的「判斷」。**

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

<sub><strong>Stanford REAP × CoPaper.AI</strong> · 實證研究 AI 工具的學術工業級產品</sub>

<br/>

<table>
  <tr>
    <td align="center">
      <a href="https://copaper.ai"><img src="images/copaper-qrcode.png" alt="掃碼造訪 copaper.ai" width="180" /></a><br/>
      <strong>掃碼造訪 <a href="https://copaper.ai">copaper.ai</a></strong>
    </td>
    <td align="center">
      <img src="images/copaper-wechat.jpg" alt="CoPaper.AI 公眾號" width="180" /><br/>
      <strong>關注公眾號「CoPaper.AI」</strong>
    </td>
  </tr>
</table>

內建 20 個方法論 skill · 20 分鐘完成實證論文 · 自研 <a href="https://github.com/brycewang-stanford/StatsPAI"><strong>StatsPAI</strong></a>（900+ 函式 / MIT 開源）

</div>
