# 研究流程地图 · Empirical Research Workflow Map

[< 返回主页](../README.md)

> **一句话：** 把一篇实证论文的完整流程（选题 → 投稿）拆成 10 个阶段，每个阶段都直接指向 **本仓库已 vendored 的 skill 文件夹**——克隆即用、离线可跑、全部过 [许可证审计](LICENSE_AUDIT.md) 与 [安全扫描](../SECURITY-SCAN-REPORT.md)。
>
> 这张表是**索引**；每个阶段的中文详解（含更全的 vendored skill 表 + 社区扩展资源）在对应的阶段文档里。完整 skill 目录见 [SKILL_CATALOG](SKILL_CATALOG.md)，按方法/语言/阶段筛选见 [search.html](search.html)。

---

## 10 阶段 × 仓库内主力 Skills

| # | 阶段 Stage | 这一步要解决什么 | 仓库内主力 Skills（点击直达） |
|:--|:--|:--|:--|
| 01 | [选题与研究设计](01-选题与研究设计.md)<br/>Topic & design | 把模糊方向收敛成有理论价值、有数据、有可信识别策略的问题 | [`25` Diverga](../skills/25-HosungYou-Diverga/) · [`03` scientific-skills](../skills/03-K-Dense-AI-claude-scientific-skills/) · [`34` research-companion](../skills/34-andrehuang-research-companion/) |
| 02 | [文献检索与综述](02-文献检索与综述.md)<br/>Literature | 系统检索、去重筛选、引文回溯，找准文献空白 | [`05` research-superpower](../skills/05-kthorn-research-superpower/) · [`59` openalex-skill](../skills/59-shiquda-openalex-skill/) · [`52` slr-prisma](../skills/52-keemanxp-slr-prisma/) |
| 03 | [论文阅读与拆解](03-论文阅读与拆解.md)<br/>Paper reading | 快速判断精读/泛读，提炼可迁移的识别策略与方法 | [`21` AI-research-feedback](../skills/21-claesbackman-AI-research-feedback/) · [`24` academic-research-skills](../skills/24-Imbad0202-academic-research-skills/) · [`28` paper-replicate-agent](../skills/28-maxwell2732-paper-replicate-agent-demo/) |
| 04 | [数据获取与清洗](04-数据获取与清洗.md)<br/>Data | 抓取公开数据、构面板、清洗成可分析样本 | [⭐ `00.1` Python](../skills/00.1-Full-empirical-analysis-skill_Python/) · [`57` edgartools](../skills/57-dgunning-edgartools/) · [`17` DAAF](../skills/17-DAAF-Contribution-Community-daaf/) |
| 05 | [统计分析与因果推断](05-统计分析与因果推断.md)<br/>Causal inference | 在无法做 RCT 时，用 DID/IV/RD/SCM/DML 逼近因果 | [⭐ `00` StatsPAI](../skills/00-Full-empirical-analysis-skill_StatsPAI/) · [`10` mixtape](../skills/10-Jill0099-causal-inference-mixtape/) · [`40` pyfixest](../skills/40-py-econometrics-pyfixest/) · [`64` mcp-stata](../skills/64-tmonk-mcp-stata/) |
| 06 | [论文写作](06-论文写作.md)<br/>Writing | 按顶刊结构起草手稿（intro / 识别 / 结果 / 机制） | [⭐ `50` AER-skills](../skills/50-brycewang-aer-skills/) · [`06` stats-paper-writing](../skills/06-fuhaoda-stats-paper-writing/) · [`56` econ-writing-skill](../skills/56-hanlulong-econ-writing-skill/) |
| 07 | [论文修改与润色](07-论文修改与润色.md)<br/>Revision & de-AIGC | 降 AI 味、应对查重、语言终校 | [⭐ `48` chinese-de-aigc](../skills/48-copaper-ai-chinese-de-aigc/) · [`44` humanizer_academic](../skills/44-matsuikentaro1-humanizer_academic/) · [`38` proofreader](../skills/38-peternka-academic-proofreader/) |
| 08 | [引用管理与排版](08-引用管理与排版.md)<br/>Citation & typesetting | 核验引用真实性、统一 BibTeX、LaTeX 排版 | [`62` citation-checker](../skills/62-PHY041-claude-skill-citation-checker/) · [`08` latex-document-skill](../skills/08-ndpvt-web-latex-document-skill/) · [`54` open-science-skills](../skills/54-scdenney-open-science-skills/) |
| 09 | [论文复现与可复现研究](09-论文复现与可复现研究.md)<br/>Replication | 搭可复现项目、过复现包审计、版本留痕 | [`28` paper-replicate-agent](../skills/28-maxwell2732-paper-replicate-agent-demo/) · [`41` sewage-check](../skills/41-sticerd-eee-sewage-econometrics-check/) · [`29` project20XXy](../skills/29-quarcs-lab-project20XXy/) |
| 10 | [审稿回复与学术答辩](10-审稿回复与学术答辩.md)<br/>Review response | 预演审稿意见、撰写 R&R、准备答辩材料 | [`24` 5-reviewer](../skills/24-Imbad0202-academic-research-skills/) · [⭐ `50` AER-skills](../skills/50-brycewang-aer-skills/) · [`16` clo-author](../skills/16-hsantanna88-clo-author/) |

> ⭐ = Stanford REAP × CoPaper.AI 第一方旗舰 skill。表中只列了每个阶段的 2–4 个主力，**完整列表在各阶段文档里**。

---

## 跨阶段的旗舰编排器

有些 skill 不止服务一个阶段，而是把整条链串起来——适合"一句话跑完一篇论文"的场景：

| 旗舰 | 覆盖范围 |
|:--|:--|
| [⭐ `00` StatsPAI](../skills/00-Full-empirical-analysis-skill_StatsPAI/) · [`00.1` Python](../skills/00.1-Full-empirical-analysis-skill_Python/) · [`00.2` Stata](../skills/00.2-Full-empirical-analysis-skill_Stata/) · [`00.3` R](../skills/00.3-Full-empirical-analysis-skill_R/) | 数据清洗 → 识别 → 估计 → 稳健性 → 表格/图（阶段 04–08） |
| [⭐ `50` AER-skills](../skills/50-brycewang-aer-skills/) | Top-5 经济学投稿栈：识别 → 稳健 → 写作 → R&R（阶段 01、05、06、10） |
| [⭐ `69` Paper-WorkFlow](../skills/69-Paper-WorkFlow/) | 元编排器：调度已有 skill 与并行子 agent，端到端跑完阶段 0–9 |
| [`42` ARIS](../skills/42-wanshuiyin-ARIS/) | 自主"睡眠中做研究"agent，端到端覆盖检索 → 分析 → 写作 → 投稿 |

---

[返回 README →](../README.md) · [完整目录 SKILL_CATALOG →](SKILL_CATALOG.md) · [可筛选搜索 search.html →](search.html)
