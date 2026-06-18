---
name: Foreign-CF-Study
description: 根据研究者提供的**研究计划书（Research Proposal）**执行基于**外国（美国/欧盟/英国/日本/跨国）制度环境**的公司金融类实证研究全流程。**启动后第一件事：根据计划书的主题、识别策略、贡献边际与样本范围，从外国 CF 顶刊池（AER/QJE/JPE/JF/JFE/RFS/JFQA/JAR/JAE/MS/JCF/JBF 等 25+ 期刊）中推荐 5 本最匹配的目标期刊（[J1]–[J5]），等待研究者明确选定一本；该期刊决定 main.tex 的 bibliographystyle、Section 骨架、Introduction 风格与表注规范**。然后用 Python 完成数据清洗、描述性统计、基准回归、内生性检验（IV/2SLS、DML）、平行趋势、异质性、机制、稳健性检验与图表绘制。LaTeX 表格和图像严格遵循 template/ 示例格式，研究逻辑与排版严格遵循 rule/ 下的《通用实证研究逻辑与规范总结》与《回归表写作规范总结》。数据集与政策集从 asset/ 中按计划书中的关键词检索（WRDS / NBER/Fed releases / FRED / 全球宏观库）。**当计划书预期的实证结果无法实现时（系数不显著、平行趋势不通过、IV 弱工具、机制不成立等），skill 自动切换备选方案直至完成研究项目**。最终交付物：Python 代码 + LaTeX 表格 + 图像（.pdf/.png）。触发条件：研究者提交研究计划书（含 X→Y 假设、识别策略、样本、政策冲击等）。
---

# Foreign Corporate Finance Empirical Study (foreign-cf-study)

## 1. 定位与适用范围

本 skill 指导**基于外国（非中国）制度环境的公司金融类实证研究**的完整流程。主要覆盖：

- **美国样本（主力）**：CRSP / Compustat / IBES / Thomson-Reuters / BoardEx / ExecuComp / 13F / Dealscan / SDC Platinum 等 WRDS 数据库
- **国际样本**：Compustat Global、Worldscope、Orbis/BvD、Amadeus、Osiris（欧洲/跨国）、Nikkei NEEDS（日本）、SDC M&A（全球）
- **识别策略**：DID（含 staggered / Callaway-Sant'Anna / Sun-Abraham / Stacked DID）、Panel FE + IV/2SLS、PSM-DID / Entropy Balancing、DML / DML-IV、合成控制（Synthetic Control / Synthetic DID）、RDD（含 Geographic RDD、Regression Kink）、SEO / IPO 事件研究、高频身份识别（高频 FOMC shocks、FedFund 利率冲击等）
- **研究主题**：投融资、资本结构、股利政策、并购、IPO/SEO、公司治理（董事会、CEO 补偿）、机构投资者（13F、mutual funds）、分析师、ESG / CSR、银行信贷（Dealscan）、破产（Chapter 11）、税收（TCJA / state corporate tax）、监管（SOX、Dodd-Frank、JOBS Act、MiFID II、GDPR）、贸易（China Shock、Trade War、Brexit）、创新（USPTO patents、NBER patent database）
- **代码语言：Python**（pandas / numpy / statsmodels / linearmodels / pyfixest / econml / doubleml / scikit-learn / matplotlib / wrds-py）
- **表格输出：LaTeX**（严格遵循 template/ 格式与 rule/ 规范）

本 skill 不替代研究者的研究设计判断，而是把每一环节的**标准流程、代码骨架、表格/图像模板**提供给研究者，保证产出质量达到国际公司金融顶刊（JF、JFE、RFS、JFQA、RCFS、RAPS；JAR、JAE、TAR、RAST 会计类；AER、QJE、JPE、REStud 综合类）的写作与方法论要求。

## 2. 工作目录结构（项目根即 working directory）

```
Foreign-CF-study/                 ← working directory
├── asset/                        ← **优先**的数据源索引（非唯一来源，详见 §7）
│   ├── nber_releases_list.csv         # NBER / 美联储（Fed）/ BLS / BEA 定期发布清单
│   ├── wrds_research_data_overview.pdf # WRDS 数据库概览（CRSP、Compustat、IBES、BoardEx、13F…）
│   ├── macrodatas_list.csv            # 全球宏观数据索引（含 IMF / WB / OECD / FRED 条目）
│   ├── ppmandata_trade_list.csv       # 贸易 / 关税 / 供应链层面扩展数据索引
│   └── MCP.docx                       # 登记的 MCP 服务器清单（IMF / World Bank / Supply Chain / OECD），
│                                      #   作为 asset/ 本地清单缺失时的补充来源；安装方式见各 URL
├── rule/                         ← 强制性写作与方法论规范（AI 必须逐项遵循）
│   ├── 通用实证研究逻辑与规范总结.docx
│   └── 回归表写作规范总结.docx
├── template/                     ← LaTeX 表格与图片模板（格式模仿对象）
│   ├── sum_stat.tex                   # 描述性统计
│   ├── variables.tex                  # 变量定义
│   ├── baseline.tex                   # 基准回归（渐进式加控制 + 渐进式加 FE）
│   ├── addctr.tex                     # 加入附加控制变量
│   ├── measures.tex                   # 替换因变量度量
│   ├── specification.tex              # 高维交互固定效应
│   ├── iv.tex                         # 2SLS 工具变量
│   ├── psm_ddml.tex                   # PSM + DML（Panel A / Panel B）
│   ├── bunching-did.tex               # Bunching-DID
│   ├── channel1.tex, channel2.tex, channel3.tex   # 机制分析（按渠道分组）
│   ├── heterogeneity1.tex, heterogeneity2.tex, heterogeneity3.tex # 异质性（bdiff）
│   ├── sampling.tex                   # 样本筛选稳健性
│   ├── further.tex                    # 进一步分析
│   ├── main.tex                       # 论文正文骨架
│   ├── parallel.pdf                   # 平行趋势图
│   ├── csdid-figure.pdf               # Callaway-Sant'Anna DID 动态效应
│   ├── estimator.pdf                  # 不同 DID 估计量对比
│   ├── psm-pre-post.pdf               # PSM 平衡检验前后
│   └── specurve.pdf                   # 规格曲线（specification curve）
└── 研究项目输出/                   ← 每个实证项目的产出目录（按本 skill 建议结构创建）
    └── {项目名}/
        ├── data/{raw,cleaned}/
        ├── code/                       # Python 脚本
        ├── results/                    # 表格 (.tex) 与图像 (.pdf/.png) 统一存放，不再区分 tables/ 与 figures/
        ├── ref.bib                     # 参考文献数据库
        └── main.tex                    # 论文正文（**位于项目根，不放入 paper/ 子目录**）
                                        # 头部样式与 \bibliography / \appendix 结构严格照搬 template/main.tex
                                        # 通过 \input{results/xxx} 引入表格；通过 \includegraphics{results/xxx.pdf} 引入图像
```

## 3. 触发条件与启动流程

### 3.1 唯一触发条件：研究者提交研究计划书

本 skill **只**在研究者提供**研究计划书（Research Proposal）**时触发。计划书以下述任一形式提交均可：

- 一段纯文本描述
- `.docx / .pdf / .md / .tex` 文件路径
- 对话中分点罗列

### 3.2 计划书应包含的字段（缺项时自动追问，一次补齐）

```
CONTRACT — 研究计划书最小字段清单
────────────────────────────────────────────────────────
(1) 研究题目 (Title)
(2) X → Y 因果假设 (Hypothesis)：主假设 H1 + 最多 2 条子假设
(3) 预期结果 (Expected Findings)：X 对 Y 的预期符号与显著性、预期机制
    渠道、预期异质性方向（此项至关重要——是后续"备选方案"的触发判据）
(4) 识别策略 (Identification)：DID / Staggered DID / Panel FE + IV /
    PSM-DID / RDD / Synthetic Control / Synthetic DID / DML / Event Study 中择一
(5) 样本范围 (Sample)：国家/地区、层级（公司-年/公司-季度/交易-日/state-年）、
    时间窗、交易所（NYSE/NASDAQ/AMEX）、是否剔除 ADR/Dual class、排除条款
(6) 政策冲击 (Shock)：【DID/RDD 必填】政策名称（e.g., SOX 2002, Dodd-Frank 2010,
    JOBS Act 2012, TCJA 2017, MiFID II 2018, Brexit 2016, China Shock,
    state corporate tax changes, state-level minimum wage...）、公布/实施年份/月份、
    处理组定义（e.g., pre-SOX accelerated filers, post-JOBS Act EGCs...）
(7) 数据需求 (Data)：asset/ 中需检索的关键词清单（WRDS 库名 + 政策集）
(8) 机制假说 (Mechanism)：预期作用渠道 M1 / M2 / M3
(9) 异质性维度 (Heterogeneity)：预期分组维度（公司规模、融资约束、KZ/WW index、
    董事会独立性、机构持股、行业集中度 HHI、所处州等）+ 预期组间差异方向
```

### 3.3 启动后 skill 立即执行以下动作

1. **解析计划书** → 抽取 CONTRACT 九字段，对缺项统一一次性追问补齐。
2. **🆕 推荐 5 个最合适的目标期刊（详见 §3.4）**：基于计划书的研究主题（Topic）、识别策略（Method）、贡献边际（Novelty）与样本范围（Sample）四维度，从外国 CF 顶刊池（§3.4.1）中按加权得分（§3.4.2）选出 top 5，以 `[J1]`–`[J5]` 编号 + 4 维星级评分 + "Why it fits" 一两句话 + "Editorial preference" + bib style 呈现（输出格式见 §3.4.3）。**呈现完毕后停下，显式询问研究者选定哪一本**（也允许用户提出列表外的期刊）。在收到选择前**不进入第 3 步**。
3. **固化为 `00_proposal.md`**：写入项目根 `{项目名}/00_proposal.md`，**顶部以 YAML 块追加 `target_journal` / `bibliography_style` / `writing_preferences` 三组字段**（见 §3.4.3 末尾示例），作为后续所有判断与 `main.tex` 渲染的基准文件。
4. **生成研究项目骨架**：按第 9 节目录结构建立 `{项目名}/` 下所有子目录与占位脚本；`main.tex` 头部按 §3.4.4 表把 `\bibliographystyle{}` 与 Section 骨架替换为目标期刊的版本。
5. **逐环节推进**：严格按第 4 节顺序执行，每一环节完成即与计划书中 (3) 预期结果**逐项比对**。

### 3.4 期刊定位（Journal Targeting）— 启动后第二步的依据

#### 3.4.1 候选期刊池（外国 CF 常见投稿池）

| Tier | 期刊 | 全名 | 偏好特征 | bib style |
|---|---|---|---|---|
| T1 综合 | AER | American Economic Review | 因果识别极强 + 广泛经济意义；CF 必须能讲"超出 finance 的故事" | aer |
| T1 综合 | QJE | Quarterly Journal of Economics | 自然实验 + 深远政策含义；CF 罕见但有先例 | qje |
| T1 综合 | JPE | Journal of Political Economy | 偏理论结构估计；CF 多见于治理与契约 | jpe |
| T1 综合 | RES | Review of Economic Studies | 偏结构 + 方法创新 | restud |
| T1 金融 | JF | Journal of Finance | 故事完整 + 机制深 + 大样本；偏好"新现象 / 新机制" | jf |
| T1 金融 | JFE | Journal of Financial Economics | 识别严谨 + CF/资产定价；表格规范最严 | jfe |
| T1 金融 | RFS | Review of Financial Studies | 理论嵌入 + 实证联动 | rfs |
| T2 金融 | JFQA | Journal of Financial and Quantitative Analysis | 严谨实证；适合识别清晰的中等贡献 | jfqa |
| T2 金融 | RCFS | Review of Corporate Finance Studies | CF 专门 OA 刊 | rcfs |
| T2 金融 | RAPS | Review of Asset Pricing Studies | 资产定价为主 | raps |
| T2 金融 | JCF | Journal of Corporate Finance | CF 中下游主流刊 | elsarticle-num |
| T2 金融 | JBF | Journal of Banking and Finance | 银行 / 跨国 / 监管类 | elsarticle-num |
| T2 金融 | JFI | Journal of Financial Intermediation | 银行 / 信贷 / 中介 | jfi |
| T2 金融 | JFM | Journal of Financial Markets | 微观结构 / 流动性 | elsarticle-num |
| T2 金融 | FM | Financial Management | CF 应用导向 | apa |
| T1 会计 | JAR | Journal of Accounting Research | 信息披露 / 分析师与 CF 交叉 | jar |
| T1 会计 | JAE | Journal of Accounting and Economics | 会计选择经济后果；契约 / 治理 | jae |
| T1 会计 | TAR | The Accounting Review | 涵盖最广，识别要求高 | tar |
| T2 会计 | RAST | Review of Accounting Studies | 信息环境 / 估值 / 披露 | rast |
| T2 会计 | CAR | Contemporary Accounting Research | 与 TAR 平台相近 | car |
| 管理 | MS | Management Science | 跨学科创新 / 数据科学 / 因果 | informs |
| 管理 | SMJ | Strategic Management Journal | 治理 / 并购 / 公司战略 | smj |
| 管理 | OS | Organization Science | 组织 + CF 交叉（董事会、CEO） | orsc |
| 国际 | JIBS | Journal of International Business Studies | 跨国 / 制度差异 / 跨境 M&A | jibs |
| 公共 | JPubE | Journal of Public Economics | 税收 / 监管的 CF 后果 | elsarticle-num |
| 劳动 | ILR | Industrial and Labor Relations Review | 劳动 × CF 交叉 | sage |
| 环境 | JEEM | Journal of Environmental Economics and Management | ESG / 气候政策 × CF | elsarticle-num |

> 若研究者指名列表外的期刊（如 *Journal of Accounting and Public Policy*、*Financial Review*、*European Financial Management*、*Pacific-Basin Finance Journal*、*Journal of Banking & Finance Letters* 等），照单选定即可，并比照同档期刊套用 bib style 与 Section 骨架。

#### 3.4.2 匹配评分（skill 内部）

对每本候选按 4 维 1–5 打分：

```
T = topic_fit       # CF 主题与期刊偏好对齐
M = method_fit      # 识别策略与期刊门槛对齐
N = novelty_fit     # 贡献边际能否打动该刊编辑
S = sample_fit      # 样本与期刊地理偏好
score = 0.35 T + 0.30 M + 0.25 N + 0.10 S
```

匹配示例（仅作 skill 内部参考；不输出给研究者）：

- "SOX × 投资效率（美国 staggered DID）" → JFE / JF / JAR / RFS / JFQA
- "TCJA 2017 × 资本支出" → JFE / JPubE / JAE / JF / AER
- "Brexit × 跨境投融资" → JFE / JIBS / JF / MS / JFQA
- "美国创新政策 × 公司投资外溢" → JFE / AER / RFS / MS / JF
- "MiFID II × 分析师覆盖与公司信息环境" → JAR / JAE / RFS / JFE / TAR
- "Dodd-Frank × 银行信贷供给" → JFE / RFS / JF / JFI / JBF

#### 3.4.3 推荐输出格式（必须按此格式呈现 5 本）

```
[J1] JFE — Journal of Financial Economics
     Topic ★★★★★  Method ★★★★★  Novelty ★★★★☆  Sample ★★★★★   Score 4.70
     Why it fits: {2 句话——对齐研究主题与识别方法；指本刊近 3 年发表的相近政策/主题论文（举 1 篇）}
     Editorial preference: 偏好识别透明 + 表格规范严 + 控制变量逐项展示
     Bibliography style: jfe

[J2] JF  — Journal of Finance
     ...
```

呈现完 5 本后，**必须显式停下并询问**（不要自动选定）：

> 请从 [J1]–[J5] 中选定一本作为目标期刊；若不满意，请直接告知任一外国 CF 顶刊名。
> 您的选择将决定 `main.tex` 的 `\bibliographystyle{}`、Section 骨架、Introduction 风格与表注最低长度。

研究者选定后，在 `00_proposal.md` 顶部追加（示例为 JFE）：

```yaml
---
target_journal: JFE
bibliography_style: jfe
writing_preferences:
  identification_emphasis: high
  table_format_strict: yes
  introduction_style: "5 paragraphs, identification details surface early"
  notes_paragraph_length: ">= 6 lines"
  section_skeleton:
    - Introduction
    - Background
    - Data
    - Empirical Strategy
    - Results
    - Robustness
    - Conclusion
---
```

#### 3.4.4 不同期刊触发的写作差异

| 期刊 | bib style | Section 骨架 | Intro 风格 | 表注最低 | 特别要求 |
|---|---|---|---|---|---|
| JF  | jf  | Intro / Setting / Hypotheses / Data and Methodology / Results / Mechanism / Conclusion | 5–6 段，puzzle 驱动 | ≥ 8 行 | 偏好简洁列头；附录不超过正文 30% |
| JFE | jfe | Intro / Background / Data / Empirical Strategy / Results / Robustness / Conclusion | 5 段，识别细节早出现 | ≥ 6 行 | 表格规范最严；要求逐一展示控制变量；标准误层级写清楚 |
| RFS | rfs | Intro / Theoretical Motivation / Data / Identification / Empirical Findings / Conclusion | 4–5 段，理论 motivation 醒目 | ≥ 6 行 | 偏好理论嵌入；正文 25–30 页 |
| JFQA | jfqa | 类 JFE | 类 JFE | ≥ 5 行 | 表格规范严；偏好新现象的清晰识别 |
| JAR / JAE | jar / jae | Intro / Hypothesis / Sample and Data / Research Design / Results / Conclusion | 6 段，hypothesis 在 §2 独立 | ≥ 6 行 | 预测式假设；hypothesis section 必须独立 |
| TAR | tar | 类 JAR | 类 JAR | ≥ 5 行 | 类 JAR；偏好新 measure |
| AER | aer | Intro / Background / Data / Empirical Strategy / Results / Mechanism / External Validity / Conclusion | 4 段，影响广泛 | ≥ 5 行 | 必须有外部有效性讨论；broad economic implication |
| QJE / JPE / RES | qje / jpe / restud | 类 AER（结构更紧凑） | 4 段，puzzle + economic significance | ≥ 5 行 | 跨子学科可读性；要求显著的方法/概念创新 |
| MS  | informs | Intro / Background / Hypotheses / Data and Methods / Results / Discussion / Conclusion | 4–5 段，跨学科 motivation | ≥ 5 行 | 必含 managerial implication |
| JCF / JBF / JPubE / JEEM | elsarticle-num | 类 JFE | 4 段 | ≥ 5 行 | 较灵活；可接受较窄主题 |
| JIBS | jibs | Intro / Theory and Hypotheses / Methods / Results / Discussion / Conclusion | 5 段，跨国比较视角 | ≥ 5 行 | 必含 international business 贡献 |

`render_main_tex()` 在生成 `main.tex` 时读取 `00_proposal.md` 的 `target_journal` / `bibliography_style` / `section_skeleton`，自动替换 `\bibliographystyle{}` 与 Section 命名；同时把目标期刊的 `notes_paragraph_length` 阈值传入各 `render_*_tex()` 函数，确保表注长度达到目标刊门槛。

## 3.A 自适应机制（Plan-B）：结果未达预期时的切换逻辑

**本 skill 的核心能力**——当任一环节的实证结果与 `00_proposal.md` 中"(3) 预期结果"不符时，skill **不要求研究者干预**，自主在以下备选方案树中选择并执行，直到研究项目闭环。

### 3.A.1 失败判据（每环节完成后立即触发）

| 环节 | 预期结果 | 失败判据（触发 Plan-B） |
|---|---|---|
| 平行趋势检验 | 所有 pre 期系数不显著 | 任一 pre 期 \|t\|>1.96 |
| 基准回归 | X 系数符号与预期一致且 p<0.1 | 符号反向 / 全部不显著 / 系数随控制变量/FE 添加大幅跳动 |
| 稳健 DID 估计量 | CS-DID / Sun-Abraham / Stacked 结论方向与 TWFE 一致 | 符号反向或 p 值量级完全不匹配 |
| IV 第一阶段 | F 统计量 > 10（Kleibergen-Paap）、IV 显著 | F < 10 或 IV 不显著 |
| IV 第二阶段 | LATE 与 OLS 方向一致、可解释 | 符号反向且数量级异常 |
| 机制分析 | 预期渠道 M1/M2/M3 显著 | 所有渠道不显著 |
| 异质性 | 预期维度组间差异显著 | bdiff p > 0.1 |
| 稳健性 | X 系数符号/显著性在多数列稳定 | 超过 1/3 列翻转 |
| 安慰剂 | 真实系数在虚假分布之外 | 真实系数落在虚假分布的 [5%,95%] 内 |

### 3.A.2 Plan-B 决策树（按顺序尝试，每步可叠加）

```
失败环节 → 依次尝试：

【基准回归】系数不显著 / 符号反向
  ├─ B1. 替换 Y 度量（从 template/measures.tex 思路：log(1+Y)、缩尾重算、
  │       行业/年份调整后的残差、Book vs Market leverage、Cash / Net debt 切换）
  ├─ B2. 替换 X 度量（连续 vs 虚拟 / 强度 vs 0-1 / 滞后一期 vs 当期）
  ├─ B3. 替换 FE 规格（加 Industry×Year (FF48/49)、State×Year、Firm×Quarter 高维交互）
  ├─ B4. 替换聚类层级（firm → industry → state → industry×year 双向）
  ├─ B5. 样本细化（剔除 SIC 6000-6999 金融业、SIC 4900-4949 公用事业；
  │       剔除 ADR、dual-class、IPO 当年、total assets < $10M 小样本、
  │       锁死 NYSE/AMEX/NASDAQ 普通股 share code 10/11）
  ├─ B6. 换时间窗（缩短到政策前后 ±5 年 / 剔除 2008-09 金融危机 / 剔除 2020 COVID）
  └─ B7. 若仍不显著 → 考虑反向假设（Y→X 或 U 型/门槛），在 proposal 中注明假设修正

【平行趋势】pre 期显著
  ├─ B1. 重新定义政策时点（announce vs effective vs compliance deadline；
  │       SOX 分 accelerated (2004) / non-accelerated (2007) filer）
  ├─ B2. 用 Sun-Abraham / CS-DID / Stacked DID 替代 TWFE（避免负权重问题）
  ├─ B3. 限制政策前窗口（仅保留 pre_3 到 last_K）
  ├─ B4. 加入 Group × linear trend 控制差异化趋势
  └─ B5. 改为 PSM-DID / Entropy Balancing 缓解选择偏差后重测

【IV 第一阶段弱】F < 10（Stock-Yogo / KP-rk Wald）
  ├─ B1. 尝试 asset/ 中其他同维度外生冲击（e.g., 历史定居地 → Bartik；
  │       州际距离；历史 broadband 铺设；历史 interstate highway network）
  ├─ B2. 构造 Bartik / Shift-Share IV（行业份额 × 全国冲击；Autor-Dorn-Hanson 型）
  ├─ B3. 用 Judge IV（法官随机分配）/ Lottery IV / 同伴均值 (peer mean within industry-year)
  ├─ B4. 改为 DML-Partial（弱化 IV 依赖，用 ML 处理高维混淆）
  └─ B5. 改用断点/匹配的自然实验替代 IV（RDD / Synthetic Control / Stacked DID）

【机制不显著】所有 M 均无效应
  ├─ B1. 换中介变量度量（同一渠道的不同代理；e.g., 信息不对称可用
  │       bid-ask spread / analyst forecast dispersion / PIN / Amihud illiquidity）
  ├─ B2. 换渠道组合（从"信息→治理→融资"三维度替换）
  ├─ B3. 拆分样本（分组后分别做机制，寻找条件性渠道）
  ├─ B4. 改用交互项检验（X × M → Y 是否有调节）
  └─ B5. 若仍无渠道显著 → 在"进一步分析"中承认黑箱，改做异质性深挖

【异质性不显著】bdiff p > 0.1
  ├─ B1. 换分组切点（median → tertile / quartile）
  ├─ B2. 换分组变量（同维度其他代理：如融资约束可用 KZ → WW → SA → HP index）
  ├─ B3. 连续调节变量做交互项（公司级）
  ├─ B4. 换分组维度（"公司层面→行业层面→地区层面→宏观层面"四大簇切换）
  └─ B5. 保留为"null heterogeneity"——在论文正文中作为结论的边界条件陈述

【稳健性大面积翻转】
  ├─ B1. 回溯样本构造（检查 CRSP share code、SIC、delisting code、
  │       CRSP-Compustat Merged link、IBES ticker 对齐）
  ├─ B2. 检查是否遗漏同期政策（e.g., SOX 与 Reg FD 重叠）→ 加入 co-shock dummy
  ├─ B3. 重算处理组/对照组的定义口径
  └─ B4. 若仍不稳健 → 核心结论弱化为"条件性证据"，在正文强调边界

【安慰剂失败】真实系数落在虚假分布内
  ├─ B1. 增加 reps（500 → 1000 → 2000）
  ├─ B2. 换安慰剂设计（跨公司随机 → 跨时间随机 → 跨行业随机 →
  │       跨州随机；"fake treatment" assigned to untreated firms only）
  ├─ B3. 回溯基准 → 基准本身可能有 confounder，返回【基准回归】的 B1-B7
```

### 3.A.3 切换时的强制记录

每次触发 Plan-B，必须在 `{项目名}/DECISION_LOG.md` 追加一条：

```markdown
## YYYY-MM-DD HH:MM — 环节 {X} Plan-B
- **预期**（引自 proposal 第 3 条）：...
- **实测**：系数 = ..., t = ..., p = ...
- **触发判据**：...
- **选择分支**：B{n} — {方案名}
- **后续调整**：...
- **再测结果**：...
```

### 3.A.4 终止条件

- **成功**：基准回归 + 机制 + 异质性 + 稳健性 + 安慰剂 全部通过（或部分以"边界条件"形式可解释）
- **降级闭环**：Plan-B 深度超过 3 层仍无法收敛时，把研究降级为"**零效应识别报告**"或"**条件性证据报告**"，产出仍完整：所有 .tex / 图 / 代码照常交付，正文结论段改写为 null-result 叙事
- **永不**：放弃项目或向研究者"投降"；skill 必须给出一份完整可交付的研究产出

## 4. 研究逻辑主线（严格按顺序，不可颠倒）

顺序来自 `rule/通用实证研究逻辑与规范总结.docx` 第 7.2 节。每一步都配有下文的 Python 代码骨架与 template/ 中的 LaTeX 对照模板。

| # | 环节 | 必做？ | 对应 Python 产物 | 对应 LaTeX 模板 |
|---|---|---|---|---|
| 1 | 描述性统计 | **必做** | `02_sumstat.py` → `sum_stat.tex` | `template/sum_stat.tex` + `variables.tex` |
| 2 | 平行趋势检验 | DID **必做**；其他跳过 | `03_parallel.py` → `results/parallel.pdf` | `template/parallel.pdf` |
| 3 | 异质性稳健 DID 估计量 | staggered DID **必做** | `03b_csdid.py`（CS-DID / Sun-Abraham / Stacked） | `template/csdid-figure.pdf` + `estimator.pdf` |
| 4 | **基准回归** | **必做（定海神针）** | `04_baseline.py` → `baseline.tex` | `template/baseline.tex` |
| 5 | 内生性检验 | Panel FE **必做**；DID 推荐 | `05_iv.py` + `05b_dml.py` | `template/iv.tex` + `psm_ddml.tex` Panel B |
| 6 | 因变量分解 / 替换度量 | 推荐 | `06_measures.py` | `template/measures.tex` |
| 7 | 异质性分析 | **必做** | `07_hetero1.py`, `07_hetero2.py`, `07_hetero3.py` | `template/heterogeneity1/2/3.tex` |
| 8 | 机制分析 | **必做** | `08_channel1.py`, `08_channel2.py`, `08_channel3.py` | `template/channel1/2/3.tex` |
| 9 | 稳健性检验（放附录） | **必做** | `09_addctr.py`, `09_spec.py`, `09_sampling.py`, `09_bunching.py` | `template/addctr/specification/sampling/bunching-did.tex` |
| 10 | PSM-DID / Entropy Balancing | DID **推荐** | `10_psm.py` → `psm_ddml.tex` Panel A | `template/psm_ddml.tex` + `psm-pre-post.pdf` |
| 11 | 安慰剂检验 | **必做** | `11_placebo.py` → `results/placebo.pdf` | 参照 `rule` 第 5.2 节安慰剂分布图规范 |
| 12 | 进一步分析 / 规格曲线 | 可选 | `12_further.py`, `12_specurve.py` | `template/further.tex` + `specurve.pdf` |

## 5. Python 代码骨架（全部使用 Python，不使用 Stata）

> **铁律**：本 skill 一律用 Python 实现计量。`rule/` 中的 Stata 代码（esttab 等）仅作格式参考，最终 .tex 由 Python 函数按 template/ 的手写表壳格式直接渲染输出。

### 5.1 依赖与标准导入

```python
# 所有脚本统一导入
import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from linearmodels.iv import IV2SLS
import pyfixest as pf                  # 高维固定效应 + reghdfe 等价
from doubleml import DoubleMLPLR, DoubleMLPLIV, DoubleMLData
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['axes.facecolor'] = 'white'
mpl.rcParams['figure.facecolor'] = 'white'
mpl.rcParams['axes.edgecolor'] = 'black'

# 若使用 WRDS 原生接口
# import wrds
# db = wrds.Connection(wrds_username='...')  # 研究者提供凭证；skill 不替研究者保存
```

### 5.2 固定效应 + 聚类标准误的标准回归

```python
def reg_hdfe(df, y, x, controls, fe, cluster):
    """
    y: 因变量名 (str)
    x: 核心解释变量名 (str)
    controls: 控制变量名列表
    fe: 固定效应列表, e.g. ['gvkey','fyear']  # firm + year
                       or ['gvkey','fyear','ff48']  # firm + year + industry
    cluster: 聚类层级, e.g. 'gvkey'  (firm-clustered SE, Petersen 2009 标准)
    返回 pyfixest.Feols 对象
    """
    rhs = x + ' + ' + ' + '.join(controls)
    fe_str = ' + '.join(fe)
    formula = f"{y} ~ {rhs} | {fe_str}"
    return pf.feols(formula, data=df, vcov={'CRV1': cluster})
```

### 5.3 工具变量 / 2SLS（含 Kleibergen-Paap rk Wald F）

```python
def iv_2sls(df, y, x_endog, instruments, controls, fe, cluster):
    """
    pyfixest 原生支持 IV：
      formula = "y ~ controls | FE | (x_endog ~ iv1 + iv2)"
    报告 Kleibergen-Paap rk Wald F（弱工具检验）、Hansen J（过度识别检验）。
    常用外国 IV：Bartik / Shift-share、历史 broadband 铺设、historical settler mortality、
    geographic distance、judge fixed effect、natural disaster exposure 等。
    """
    rhs = ' + '.join(controls)
    fe_str = ' + '.join(fe)
    iv_str = f"({x_endog} ~ {' + '.join(instruments)})"
    formula = f"{y} ~ {rhs} | {fe_str} | {iv_str}"
    return pf.feols(formula, data=df, vcov={'CRV1': cluster})
```

### 5.4 Double Machine Learning（DML / DML-IV）

```python
def dml_plr(df, y, d, controls, learner='lasso', n_folds=5, n_reps=10):
    learners = {
        'lasso': LassoCV(cv=5),
        'ridge': RidgeCV(),
        'rf':    RandomForestRegressor(n_estimators=500, max_depth=8, n_jobs=-1),
        'lgbm':  lgb.LGBMRegressor(n_estimators=500, num_leaves=31),
    }
    dml_data = DoubleMLData(df, y_col=y, d_cols=d, x_cols=controls)
    model = DoubleMLPLR(dml_data,
                        ml_l=learners[learner],
                        ml_m=learners[learner],
                        n_folds=n_folds, n_rep=n_reps)
    model.fit()
    return model   # .coef, .se, .t_stat, .pval, .confint()
```

### 5.5 Staggered DID：Callaway-Sant'Anna / Sun-Abraham / Stacked DID

```python
# Sun-Abraham：interaction-weighted estimator，用 pyfixest 的 sunab() 便捷函数
# CS-DID：用 Python 包 "csdid" 或 "differences"；或手写 group-time ATT 聚合
# Stacked DID：Cengiz et al. (2019) / Deshpande-Li (2019) 风格

def csdid_event_study(df, y, cohort, time, controls, cluster):
    """
    cohort: 处理开始年份（未处理组为 NaN/Inf）
    time:   日历年份
    返回：{e: att, se, ci} 的字典，用于画动态效应图（event_study plot）
    实现 Callaway & Sant'Anna (2021)；或调用 pyfixest.feols 配合
    i(time, treat, ref=-1) 画事件研究（TWFE）作对照。
    """
    ...

def stacked_did(df, y, treat, cohort, time, controls, cluster, window=(-5, 5)):
    """
    Stacked DID：为每个 cohort 构造 "clean" control pool（永不处理 + 尚未处理），
    复制行叠加后跑 TWFE。规避异质处理效应下的负权重问题。
    """
    ...
```

### 5.6 PSM / Entropy Balancing

```python
def psm_match(df, treat, covariates, k=4, caliper=0.002):
    """最近邻 1:k 匹配 + caliper。返回带权重的新 DataFrame。
       对应 template/psm-pre-post.pdf 的平衡检验图。"""
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import NearestNeighbors
    # 估计倾向得分 → 最近邻匹配 → 返回匹配后样本
    ...

def entropy_balance(df, treat, covariates):
    """使用 ebalance / cvxpy 实现熵平衡重加权（Hainmueller 2012）。"""
    ...
```

### 5.7 Bootstrap Fisher 置换检验（异质性组间差异）

```python
def bdiff_bootstrap(df, y, x, controls, fe, cluster, group_var, reps=500, seed=42):
    """
    对异质性分析的两组（High/Low）做 bootstrap Fisher 置换检验。
    rule/ 回归表写作规范总结.docx 第 4.5 节要求 500 reps。
    返回：p-value for (b_high - b_low)
    """
    rng = np.random.default_rng(seed)
    ...
```

### 5.8 Synthetic Control / Synthetic DID（跨国 / state 层面政策）

```python
def synthetic_control(df, outcome, unit, time, treat_unit, treat_time,
                       predictors, donor_pool):
    """Abadie-Diamond-Hainmueller (2010) 合成控制法。
       适用：单一处理单元（single-country / single-state shock），
       e.g., Brexit, German reunification, California tobacco control."""
    ...

def synthetic_did(df, outcome, unit, time, treat_unit, treat_time):
    """Arkhangelsky et al. (2021) Synthetic DID。
       综合 SC 与 DID 的思路，适合多处理单元 + 时期加权。"""
    ...
```

## 6. LaTeX 输出：严格遵循 template/ + rule/

**所有 `.tex` 由 Python 函数手写生成**，目标是让输出和 `template/` 中对应文件**视觉一致**：相同的 `\toprule / \midrule / \bottomrule`、相同的 `\sym{}` 宏、相同的列头结构（`&\multicolumn{1}{c}{(1)}…`）、相同的表注 justifying 段。

### 6.1 铁律（出自 rule/ 两份文档）

1. **不用竖线（`|`），不在系数区加额外 `\hline`**。三线表：`\toprule / \midrule / \bottomrule` 各一次（template/ 中所见 `\hline` 为列头分隔，按模板保留即可）。
2. **控制变量必须逐一展示系数与 t 值**，**禁止** "Controls: Yes/No" 省略。
3. **变量顺序固定**：核心 X → （交互项）→ 控制变量 → Constant（通常省略）。
4. **括号内是 t 值**（不是标准误），表注首行固定写 `t statistics in parentheses`（若改为 SE，表注同步改）。
5. **显著性符号**固定为 `***` p<0.01, `**` p<0.05, `*` p<0.1，星号嵌于 `\sym{}` 宏。
6. **数值格式**：系数 `%.4f`，t 值 `(%.2f)`，观测数 `%,.0f`，R² `%.2f`。
7. **底部固定效应行**：`Firm FE / Year FE / Industry FE / State FE / Ind × Year FE / State × Year FE …`，Yes/No 显式标注（Firm FE 与 Industry FE 在含 firm 维度时互斥，按模型选择）。
8. **聚类层级匹配**：聚类标准误层级必须与核心解释变量变异层级一致，表注中写清楚 "robust t-statistics clustered by the firm / industry / state / ..."。美国公司面板默认 firm-clustered（Petersen 2009）。
9. **表注（noindent + justifying 段）必须写全**：样本范围（e.g., "U.S. Compustat non-financial, non-utility firms listed on NYSE/AMEX/NASDAQ from YYYY to YYYY"）、因变量定义、核心 X 定义、控制变量逐一列出、FE 组合、聚类层级、**交叉引用 `Table \ref{definition}`**、显著性符号说明。
10. **异质性表格**必须含 `\cmidrule(lr){i-j}` 分组列头，并在表尾增加 `p-value for Diff. (High-Low)` 一行（bootstrap Fisher 置换检验，reps=500）。

### 6.2 Python 渲染函数（骨架）

```python
def render_baseline_tex(models, labels_cols, var_order, var_labels,
                        fe_rows, nobs, r2, caption, label, note,
                        out_path):
    """
    按 template/baseline.tex 的结构写出 .tex。
    models: 列表，每个元素是 (coef_dict, t_dict, stars_dict)；
            key 与 var_order 一致。
    fe_rows: [('Firm FE', ['Yes','Yes',...]), ('Year FE', [...]),
              ('Industry FE', [...]), ('State FE', [...])]
    """
    lines = [r'\begin{table}[htbp]\centering\scriptsize',
             r'\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}',
             rf'\caption{{\textbf{{{caption}}}}}',
             rf'\label{{{label}}}',
             '',
             rf'\noindent{{\justifying{{{note}\par}}}}',
             r'\bigskip',
             '',
             rf'\begin{{tabularx}}{{\textwidth}}{{l{"Y"*len(models)}@{{}}}}',
             r'\toprule', '']

    # 列序号行
    header1 = '                ' + ''.join([rf'&\multicolumn{{1}}{{c}}{{({i+1})}}'
                                            for i in range(len(models))]) + r'\\'
    lines.append(header1)
    # 可选：第二行列头（因变量名 / 分组名）
    if labels_cols:
        header2 = '                ' + ''.join([rf'&\multicolumn{{1}}{{c}}{{{c}}}'
                                                for c in labels_cols]) + r'\\'
        lines.append(header2)
    lines.append(r'\hline\\')

    # 系数与 t 值：每个变量两行
    for v in var_order:
        vlab = var_labels.get(v, v)
        coef_line = f'{vlab:<16}' + ''.join(
            [rf'& {fmt_coef(m[0][v], m[2][v]):>17}' for m in models]) + r'\\'
        t_line = ' ' * 16 + ''.join(
            [rf'& {fmt_t(m[1][v]):>17}' for m in models]) + r'\\'
        lines += [coef_line, t_line]

    lines.append(r'\hline')
    # Obs + FE 行 + Adj R²
    lines.append(f'Obs             ' + ''.join([rf'&{n:>10,}        ' for n in nobs]) + r'\\')
    for name, vals in fe_rows:
        lines.append(f'{name:<16}' + ''.join([rf'&{v:>10}        ' for v in vals]) + r'\\')
    lines.append(f'Adjusted $ R^2$ ' + ''.join([rf'&{r:>10.2f}        ' for r in r2]) + r'\\')
    lines += [r'\bottomrule', r'\end{tabularx}', r'\end{table}']

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def fmt_coef(b, stars):
    s = {3:r'\sym{***}', 2:r'\sym{**}', 1:r'\sym{*}'}.get(stars, '')
    sign = '  ' if b >= 0 else ' '
    return f'{sign}{abs(b):>7.4f}{s}'  # 与 template/baseline.tex 的对齐一致

def fmt_t(t):
    return f'({t:>5.2f})'
```

`render_sumstat_tex`、`render_iv_tex`（含 First Stage / Second Stage 分组列头 + `\cmidrule`，报告 KP rk Wald F、Anderson-Rubin CI）、`render_channel_tex`（因变量行在第二层列头）、`render_heterogeneity_tex`（含 `p-value for Diff.` 行）、`render_psm_ddml_tex`（Panel A + Panel B 复合表）、`render_variables_tex`（`p{2.0cm}p{13.5cm}` 两列定义表）按 template/ 中对应文件一一对应实现。

### 6.3 图像绘制（matplotlib）

遵循 `rule/回归表写作规范总结.docx` 第五部分图像规范：白底、黑框、Times New Roman、`.pdf` + `.png` 双份输出。

- **事件研究图**：`errorbar(rcap 样式) + axhline(0) + axvline(基准期, linestyle='--')`，基准期默认为 `t-1`
- **规格曲线**：系数值排序散点 + 下方变量勾选矩阵（specification curve analysis）
- **安慰剂分布**：`hist + kde`，真实系数 `axvline(color='red')`
- **森林图**：横向 `errorbar`，按"firm / industry / state / macro"分组，每组一个 subplot
- **PSM 平衡**：匹配前/后 |% standardized bias| 散点或条形图
- **Binscatter**：`seaborn.regplot` 或手写残差化后分 bin，散点 navy，拟合线 maroon（Cattaneo et al. 2023）

## 6.4 `main.tex` 组装规则（放在**项目根**，头部照搬 `template/main.tex`）

**`main.tex` 位于 `{项目名}/` 根目录（不放入 `paper/` 子目录）**，所有表/图的路径统一写作 `results/xxx.tex` 或 `results/xxx.pdf`（相对路径，无须 `../`）。

### 6.4.1 头部（preamble / titlepage / abstract）

- 逐字照搬 `template/main.tex` 第 1–85 行的 **documentclass、usepackage、titleformat、newcolumntype、titlepage / \maketitle、abstract、baselinestretch** 设置；
- 只替换论文题目、作者、单位、JEL、关键词、abstract 正文；
- **根据 `00_proposal.md` 顶部 YAML 块中的 `bibliography_style` 字段（见 §3.4.3），把 `\bibliographystyle{jfe}` 替换为目标期刊对应的 bib style**（jf / jfe / rfs / jar / jae / aer / informs / elsarticle-num / jibs / …，详见 §3.4.4）；
- **Section 骨架按目标期刊的 `section_skeleton` 列表渲染**（例：JF 用 "The Setting / Hypotheses"、JAR 用 "Hypothesis / Sample and Data / Research Design"、AER 必含 "External Validity"、MS 末段必含 "Discussion" 与 managerial implication）；
- 其余宏包、页面几何、超链接色、`\newcolumntype{Y}`、`\renewcommand\Authands` 等**不得改动**。

### 6.4.2 正文结构（仅生成 Section / Subsection 标题，**正文留空**）

**铁律**：
- **不生成任何叙述性 .tex 子文件**（不要 `introduction.tex` / `background.tex` / `data.tex` / `results.tex` …）。所有叙述性 prose 一律不写，留给研究者本人填。
- `main.tex` 正文区只输出 `\section{...}` 和 `\subsection{...}` 标题骨架；标题之间正文**完全空白**（可选加一行占位注释 `% TODO: prose`，但不要写任何句子、不要写"In this section we …"之类样板话）。
- `\input{results/xxx}` 和 `\includegraphics{results/xxx.pdf}` 这类**实证产物的引入命令**照常出现在 §6.4.3 / §6.4.4 的位置，因为它们引入的是 skill 自动生成的表/图，不是叙述性 prose。
- Section/Subsection 标题文本按目标期刊 `section_skeleton` 渲染（见 §3.4.4）；下方 subsection 列表是各刊的"通用最小骨架"，若目标期刊偏好不同则按 §3.4.4 调整。

**通用骨架（以 JFE 为例；其他期刊按 §3.4.4 替换顶层 section 名）**：

```latex
%==============================================================
%  正文（仅标题，内容留空）
%==============================================================

\section{Introduction}\label{sec:intro}
% TODO: prose

\section{Background}\label{sec:bg}
  \subsection{Institutional Setting}
  % TODO: prose
  \subsection{Related Literature}
  % TODO: prose

\section{Hypothesis Development}\label{sec:hyp}
  \subsection{Main Hypothesis}
  % TODO: prose
  \subsection{Mechanism Hypotheses}
  % TODO: prose

\section{Data and Sample}\label{sec:data}
  \subsection{Data Sources}
  % TODO: prose
  \subsection{Sample Construction}
  % TODO: prose
  \subsection{Variable Definitions}
  % TODO: prose（变量定义表在附录 \ref{tab:variables}）
  \subsection{Summary Statistics}
  % TODO: prose（表 \ref{tab:sumstat}）

\section{Empirical Strategy}\label{sec:strategy}
  \subsection{Identification}
  % TODO: prose
  \subsection{Baseline Specification}
  % TODO: prose
  \subsection{Parallel Trends}  % DID 项目才保留
  % TODO: prose（图 \ref{fig:dynamic}）

\section{Empirical Results}\label{sec:results}
  \subsection{Baseline Results}
  % TODO: prose（表 \ref{tab:baseline}）
  \subsection{Addressing Endogeneity}
  % TODO: prose（表 \ref{tab:iv}、\ref{tab:psm_ddml}）
  \subsection{Heterogeneity}
  % TODO: prose（表 \ref{tab:het1}–\ref{tab:het3}）
  \subsection{Mechanism}
  % TODO: prose（表 \ref{tab:ch1}–\ref{tab:ch3}）
  \subsection{Further Analysis}
  % TODO: prose（表 \ref{tab:further}）

\section{Conclusion}\label{sec:conclude}
% TODO: prose
```

**目标期刊触发的差异**（render 时按 §3.4.4 表替换顶层 section 名 + 必要的 subsection）：

| 目标期刊 | 顶层 section 与额外 subsection 要求 |
|---|---|
| JF | "The Setting" 替代 Background；Hypotheses 独立成节；Mechanism 在 Results 内独立 subsection |
| JFE | 上文示例（Background → Data → Empirical Strategy → Results → Robustness → Conclusion） |
| RFS | "Theoretical Motivation" 独立 section，置于 Background 之后 Data 之前 |
| JAR / JAE | "Hypothesis" 单独 section（在 §2，独立于 Background）；"Research Design" 替代 Empirical Strategy |
| TAR | 同 JAR |
| AER | 末尾加 `\section{External Validity}` 在 Conclusion 之前 |
| MS  | `\section{Discussion}` 在 Results 与 Conclusion 之间，内含 `\subsection{Managerial Implications}` |
| JIBS | `\section{Theory and Hypotheses}` 替代 Background + Hypothesis Development；末尾加 `\subsection{Contribution to International Business}` |
| JCF / JBF / JPubE / JEEM | 同 JFE 通用骨架 |

> render_main_tex 在写出标题骨架时**严禁**生成任何 prose 句子；任何句首类似 "This paper studies …"、"We document …"、"Section 2 describes …"、"In this section …" 都属违规。只允许 `% TODO: prose` 一行占位注释。

### 6.4.3 参考文献之后：先图，再表，最后附录（严格顺序）

在正文 `\section{Conclusion}` 之后依次写入：

```latex
\bibliographystyle{jfe}
\bibliography{ref}

%%%%% Figures（主体图：平行趋势 + 估计量对比）%%%%%%%%
\clearpage
\begin{figure}[ht]\begin{center}
  \includegraphics[width=0.9\linewidth]{results/parallel.pdf}
  \caption{\textbf{Dynamic Treatment Effect}}\label{dynamic}
\end{center}\end{figure}

\clearpage
\begin{figure}[ht]\begin{center}
  \includegraphics[width=0.9\linewidth]{results/estimator.pdf}
  \caption{\textbf{DID Estimator Comparison}}\label{estimator}
\end{center}\end{figure}

%%%%% Tables（主体表：descriptive → baseline → endogeneity → heterogeneity → mechanism → further）%%%%%%%%
\clearpage \input{results/sum_stat}       % 描述性统计
\clearpage \input{results/baseline}       % 基准回归
%% 内生性处理紧跟 baseline：
\clearpage \input{results/iv}             % 2SLS / IV
\clearpage \input{results/psm_ddml}       % PSM-DID (Panel A) + DML (Panel B)
%% 异质性在机制之前：
\clearpage \input{results/heterogeneity1}
\clearpage \input{results/heterogeneity2}
\clearpage \input{results/heterogeneity3}
%% 机制分析：
\clearpage \input{results/channel1}
\clearpage \input{results/channel2}
\clearpage \input{results/channel3}
%% 进一步分析：
\clearpage \input{results/further}
```

### 6.4.4 附录（Appendix）— 稳健性 + 变量定义 + 样本构造 + 附录图

`\appendix` 起始处的 `\setcounter{table}{0}`、`\setcounter{figure}{0}`、`\renewcommand{\thetable}{S\arabic{table}}`、`\renewcommand{\thefigure}{S\arabic{figure}}` 必须保留（附录表/图独立编号 S1、S2、…，与 `template/main.tex` 第 660–665 行一致）。

附录内容顺序：

```latex
\clearpage
\setcounter{table}{0}
\setcounter{figure}{0}
\renewcommand{\thetable}{S\arabic{table}}
\renewcommand{\thefigure}{S\arabic{figure}}
\appendix

\begin{large}\begin{center}
\bf {论文题目} \\ Online Appendix
\end{center}\end{large}

%% 附录图（PSM 平衡、CS-DID 事件研究、规格曲线、安慰剂分布）
\clearpage
\begin{figure}[ht]\begin{center}
  \includegraphics[width=0.9\linewidth]{results/psm-pre-post.pdf}
  \caption{\textbf{Kernel Density of Propensity Scores}}\label{kernel-psm}
\end{center}\end{figure}

\clearpage
\begin{figure}[ht]\begin{center}
  \includegraphics[width=0.9\linewidth]{results/csdid-figure.pdf}
  \caption{\textbf{Callaway-Sant'Anna Event Study}}\label{csdid}
\end{center}\end{figure}

\clearpage
\begin{figure}[ht]\begin{center}
  \includegraphics[width=0.9\linewidth]{results/placebo.pdf}
  \caption{\textbf{Placebo Test}}\label{placebo}
\end{center}\end{figure}

\clearpage
\begin{figure}[ht]\begin{center}
  \includegraphics[width=0.8\linewidth]{results/specurve.pdf}
  \caption{\textbf{Specification Curve}}\label{specurve}
\end{center}\end{figure}

%% 附录表（**必含**：变量定义 + 样本构造/分布；以及稳健性四件套）
\clearpage \input{results/variables}            % 变量定义表（必做）
\clearpage \input{results/sample_construction}  % 样本构造/分布表（必做）
%% 稳健性表格全部进附录：
\clearpage \input{results/measures}             % 替换度量
\clearpage \input{results/sampling}             % 样本筛选
\clearpage \input{results/specification}        % 高维交互 FE
\clearpage \input{results/addctr}               % 追加控制变量
\clearpage \input{results/bunching-did}         % Bunching-DID（若适用）

%% （可选）理论推导附录——参照 template/main.tex 第 716 行后
%% \section*{Appendix: Theoretical Derivations} ...

\end{document}
```

### 6.4.5 `render_main_tex` 骨架（Python 自动生成 `main.tex`）

```python
def render_main_tex(title, authors, affils, abstract, jel, keywords,
                    target_journal, bibliography_style, section_skeleton,
                    main_figures, main_tables, appendix_figures, appendix_tables,
                    out_path='main.tex', template='template/main.tex'):
    """
    读取 template/main.tex，切出 [preamble][title/abstract block][正文标题骨架]
    [bibliography][figures][tables][appendix-figs][appendix-tabs] 八段，
    将:
      - 标题/作者/单位/abstract/JEL/keywords 替换为本项目内容
      - 根据 target_journal / bibliography_style 替换 \bibliographystyle{...}
      - 根据 section_skeleton（从 00_proposal.md YAML 读出）渲染 §6.4.2 的
        【仅标题、正文留空】骨架；section/subsection 之间只放
        一行 `% TODO: prose` 占位注释，**绝对不生成任何 prose 句子**
      - **不生成任何叙述性 .tex 子文件**（不要 introduction.tex / background.tex …）
      - main_figures = ['results/parallel.pdf', 'results/estimator.pdf']
      - main_tables  = ['results/sum_stat', 'results/baseline', 'results/iv',
                        'results/psm_ddml', 'results/heterogeneity1', ...,
                        'results/channel1', ..., 'results/further']
      - appendix_figures = ['results/psm-pre-post.pdf','results/csdid-figure.pdf',
                            'results/placebo.pdf','results/specurve.pdf']
      - appendix_tables  = ['results/variables','results/sample_construction',
                            'results/measures','results/sampling',
                            'results/specification','results/addctr',
                            'results/bunching-did']
    按 6.4.2 / 6.4.3 / 6.4.4 的严格顺序组装 main.tex，写入项目根目录。
    """
    ...
```

**渲染时禁止行为清单**（render_main_tex 必须自检）：

| 违规 | 正确做法 |
|---|---|
| 在 `\section{Introduction}` 之后写任何句子 | 仅写 `% TODO: prose` 一行 |
| 创建 `results/introduction.tex` 等叙述性子文件 | 不创建；正文留空 |
| 写"In this section we …"/"This paper …"/"Section 2 describes …" | 全部禁止 |
| 用 `\input{prose/xxx}` 引入叙述 | 禁止；prose 只能由研究者直接写入 main.tex |
| 自动填写 abstract 内容 | abstract 由研究者写；render 只复制传入的 `abstract` 字符串（可空） |

### 6.4.6 参考文献

- `\bibliographystyle{jfe}`（Journal of Financial Economics 样式，template 默认）
- `\bibliography{ref}` → 项目根的 `ref.bib`
- 若研究者未提供 `ref.bib`，skill 给出空文件并在 `main.tex` 正文 `\citep{}` 中列出需要添加的文献关键词，由研究者补齐

### 6.4.7 `render_sample_construction_tex`（附录必含）

新增 Python 渲染函数，输出 `results/sample_construction.tex`，两列或三列表，示范内容：

```
                                                                    Obs.
----------------------------------------------------------------------
Initial Compustat-CRSP merged sample, YYYY-YYYY               XXX,XXX
Less: Financial firms (SIC 6000-6999)                         -XX,XXX
Less: Utilities (SIC 4900-4949)                                -X,XXX
Less: Non-common stock (CRSP share code ≠ 10, 11)              -X,XXX
Less: ADRs / dual-class / SPACs                                -X,XXX
Less: Firm-years with total assets < $10M                      -X,XXX
Less: Firms missing CCM link (LINKTYPE not in LU/LC)           -X,XXX
Less: Observations with missing controls                       -X,XXX
Final analysis sample                                         XXX,XXX
----------------------------------------------------------------------

Panel B. Industry distribution (Fama-French 48)
Panel C. Year distribution
Panel D. Country distribution   (仅跨国样本)
```

格式仿 `template/variables.tex` 的 `p{...cm}p{...cm}` 两列定义表壳 + `\toprule/\midrule/\bottomrule`，表注写明样本筛选的来源与理由。

## 7. 数据来源与检索流程（研究者输入驱动）

### 7.1 数据来源层级（优先级从高到低）

**`asset/` 不是唯一来源，而是"优先考虑"来源。** 当 `asset/` 中找不到合适条目时，按以下顺序扩展检索范围：

| 层级 | 来源 | 定位 | 典型数据 |
|---|---|---|---|
| L1 | `asset/` 本地清单 | **优先** | WRDS 主库（CRSP / Compustat / IBES / BoardEx / 13F / Dealscan / Audit Analytics / ExecuComp / RavenPack / Patent DB）、NBER/Fed/BLS/BEA 发布、已登记的政策冲击库 |
| L2 | `asset/MCP.docx` 登记的 **MCP 服务器** | **asset/ 缺失时首选补充** | 宏观面板、跨国面板、贸易 / 供应链 |
| L3 | 其他公开外部源 | asset/ 和 MCP 都没有时才考虑 | 各国央行 / 统计局 / 证监会官网、Kenneth French Library、Global Financial Data、Refinitiv、Bloomberg（若研究者订阅）、GitHub 公开复制包、论文作者主页数据 |
| L4 | 研究者自构 | 仅在 L1-L3 均无时 | 年报手工提取、文本爬取、RA 手动编码 |

**原则**：在 L1 找到 top 5 候选返回研究者；研究者判断不够用时，跳到 L2 调用 MCP；仍不够再走 L3/L4。**不得跳过 L1 直接去 L3**，除非研究者明确点名某个外部源。

### 7.2 MCP 服务器（`asset/MCP.docx`）

`asset/MCP.docx` 中登记的 MCP（Model Context Protocol）服务器是 **asset/ 本地清单之外的官方补充来源**。当前登记四个：

| MCP 服务器 | 用途 | 安装/使用入口 |
|---|---|---|
| **IMF Data MCP** | IMF WEO / IFS / DOT / BOP 宏观面板（各国 GDP / 通胀 / 汇率 / 国际收支 / 政策利率）| https://github.com/c-cf/imf-data-mcp |
| **World Bank Data MCP** | WDI / WGI / Doing Business / Enterprise Surveys（跨国制度质量、金融深度、营商环境）| https://github.com/llnormll/world-bank-data-mcp |
| **Supply Chain MCP** | 全球供应链数据（关税、港口、航运、贸易流、库存）| https://mcpmarket.com/zh/server/supply-chain |
| **OECD MCP** | OECD STAN / PDB / SDBS / PMR（产业面板、生产率、监管强度、公司税率）| https://github.com/isakskogstad/OECD-MCP |

**安装与使用**：逐一参照各 MCP 仓库 README 的安装命令（通常是 `npx -y ...` 或 `uvx ...` 接入 Claude Code 的 `.mcp.json`）。**凭证与 API key 由研究者在本地配置**，skill 不保存任何 token。

**研究中的调用方式**：MCP 启用后，skill 直接通过相应 MCP 工具调用（如 `mcp__imf__get_series`、`mcp__world-bank__query_wdi` 等）拉取数据；拉取后统一落盘到 `{项目名}/data/raw/`，后续清洗流程不变。

**查询前的路径判断**：

```
研究者关键词
   │
   ▼
asset/ 本地清单（nber/macrodatas/ppmandata/WRDS overview）命中？
   ├── 是 → 返回 top 5，交研究者选定（L1）
   └── 否 → 检查关键词主题：
              ├── 跨国宏观 / 主权 / 汇率 / 国际收支 → IMF MCP
              ├── 制度 / 发展 / 营商环境 / 金融深度 → World Bank MCP
              ├── 关税 / 贸易流 / 供应链 / 航运  → Supply Chain MCP
              ├── OECD 成员国产业 / 监管 / 税率  → OECD MCP
              └── 均不匹配 → 走 L3 外部源（让研究者点名）
```

### 7.3 检索函数（L1 本地清单）

**不要主动全表扫描 asset/**，以免输入 tokens 爆炸。正确流程：

1. 让研究者说出需要的数据**关键词**（e.g., "CRSP", "Compustat", "IBES", "BoardEx", "13F", "Dealscan", "USPTO patents", "SOX compliance", "Dodd-Frank", "Brexit", "China Shock", "TCJA", "state corporate tax", "FOMC shocks"…）或政策名。
2. 用 Grep / pandas 在 `asset/nber_releases_list.csv`、`asset/macrodatas_list.csv`、`asset/ppmandata_trade_list.csv` 中按关键词搜索 title / data_source / keyword / data_intro / data_indicators 列；同时在 `asset/wrds_research_data_overview.pdf` 中定位对应 WRDS 库。
3. 返回 top 5 候选，展示 `title`、`data_source`、`data_indicators`（前 200 字）与下载 / 接入 URL；研究者选定后再由其下载 / 授权使用（WRDS 订阅凭证由研究者保管）。
4. L1 无命中或研究者认为候选不合适 → 按 §7.1 / §7.2 依次尝试 MCP → L3 外部源 → L4 自构。

```python
def search_asset(keyword, top=5):
    """L1：本地 asset/ 清单检索。"""
    results = []
    for csv in ['asset/nber_releases_list.csv',
                'asset/macrodatas_list.csv',
                'asset/ppmandata_trade_list.csv']:
        try:
            df = pd.read_csv(csv, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(csv, encoding='utf-8-sig')
        hit = df[df.apply(lambda r: keyword.lower() in str(r.to_dict()).lower(), axis=1)]
        if len(hit):
            results.append(hit.head(top).assign(source=csv))
    if not results:
        return pd.DataFrame()
    return pd.concat(results, ignore_index=True)

def route_to_mcp(keyword):
    """L2：根据关键词建议应调用哪个 MCP（asset/MCP.docx 登记）。"""
    kw = keyword.lower()
    routes = [
        (['gdp','inflation','exchange','bop','sovereign','policy rate','imf'],
         'IMF Data MCP',         'https://github.com/c-cf/imf-data-mcp'),
        (['wdi','wgi','governance','doing business','financial depth','enterprise survey'],
         'World Bank Data MCP',  'https://github.com/llnormll/world-bank-data-mcp'),
        (['tariff','trade flow','supply chain','shipping','port','inventory'],
         'Supply Chain MCP',     'https://mcpmarket.com/zh/server/supply-chain'),
        (['oecd','stan','regulation','productivity','corporate tax rate','pmr'],
         'OECD MCP',             'https://github.com/isakskogstad/OECD-MCP'),
    ]
    for kws, name, url in routes:
        if any(k in kw for k in kws):
            return {'mcp': name, 'install_url': url}
    return None  # 走 L3 / L4
```

### 7.4 数据出处登记（可复现要求）

每条落入 `data/raw/` 的数据必须在 `{项目名}/data/raw/SOURCES.md` 中登记：

```markdown
| 文件 | 来源层级 | 原始出处 | 拉取时间 | 备注 |
|---|---|---|---|---|
| compustat_funda_2000_2023.parquet | L1 | WRDS Compustat Fundamentals Annual | 2026-04-23 | 已应用 consol='C', popsrc='D', indfmt='INDL' |
| wb_wgi_2000_2023.csv            | L2 | World Bank Data MCP → WGI | 2026-04-23 | 通过 mcp__world-bank__query_wdi 拉取 |
| sox_accelerated_filer.csv       | L4 | 研究者手工整理自 SEC Release 33-8128 | 2026-04-20 | RA: XXX，双人复核 |
```

## 8. 外国公司金融研究的常见坑（必检）

| 陷阱 | 做法 |
|---|---|
| 样本未剔除金融业（SIC 6000-6999）与公用事业（SIC 4900-4949） | 默认剔除（除非研究对象就是这两个行业） |
| 未限定普通股 CRSP share code 10 / 11 | 默认仅保留 10/11（剔除 ADR、REIT、ETF、closed-end fund、SPAC） |
| CRSP-Compustat Merged 匹配遗漏 | 用 CCM link 表（LINKTYPE in ('LU','LC') 且 LINKPRIM in ('P','C')） |
| 连续变量极端值 | 1% / 99% 缩尾（winsor），在表注中说明；财务比率额外处理 ±inf / nan |
| 行业分类口径 | 优先 Fama-French 48（FF48）；稳健性中替换 SIC 2 位 / NAICS 3 位 / FF12 |
| 美国州级合并变动 | West Virginia / Alaska 数据缺失需注意；州代码用 FIPS |
| 聚类层级 | 公司面板默认 firm（Petersen 2009）；州政策默认 state；跨期相关用 firm + year 双向（Thompson 2011） |
| staggered DID | 必配 CS-DID 或 Sun-Abraham 或 Stacked DID 交叉验证，避免 TWFE 负权重（Goodman-Bacon 2021） |
| 政策时点 announce vs effective | 区分，并在稳健性中替换；e.g., SOX 分 accelerated (2004) / non-accelerated (2007) filer |
| 同期政策混淆 | 检索 asset/NBER 政策清单，在基准回归中加入同期政策的 dummy 控制（e.g., SOX × Reg FD） |
| 危机 / 疫情样本污染 | 稳健性中剔除 2008-2009（GFC）与 2020-2021（COVID）期间 |
| 并购 / 退市缺失处理 | CRSP delisting return 调整；Compustat 退市 / 私有化 / 破产标记 dlrsn |
| 反向因果 | 滞后解释变量 1 期、使用 pre-determined controls、Granger 检验 |
| 美元通胀 | 连续变量（资产、投资额）以 CPI / GDP deflator 折算到常年元 |

## 9. 输出项目目录（运行 skill 时自动建议）

在 CONTRACT 九字段确认后，自动生成如下骨架（所有 Python 脚本预埋 template/ 对照的 `render_*_tex` 调用）：

```
{项目名}/
├── 00_proposal.md                          # 计划书固化版（CONTRACT 九字段）
├── DECISION_LOG.md                         # Plan-B 切换记录（3.A.3）
├── main.tex                                # 论文正文（项目根；头部照搬 template/main.tex；
│                                           #   先图后表，稳健性放附录；见 §6.4）
├── ref.bib                                 # 参考文献（bibliographystyle=jfe）
├── data/raw/                               # 研究者放入原始数据（WRDS 导出 / 第三方）
├── data/cleaned/sample.parquet             # 清洗后样本
├── code/
│   ├── 00_config.py                        # 全局变量（样本年份、控制变量列表、FE 配置）
│   ├── 01_clean.py                         # CRSP × Compustat × IBES × BoardEx 对齐
│   ├── 02_sumstat.py                       # → results/sum_stat.tex + variables.tex
│   │                                       #   + results/sample_construction.tex（附录必含）
│   ├── 03_parallel.py                      # → results/parallel.pdf   [DID 专用]
│   ├── 03b_csdid.py                        # → results/csdid-figure.pdf + estimator.pdf
│   ├── 04_baseline.py                      # → results/baseline.tex
│   ├── 05_iv.py                            # → results/iv.tex                【紧跟 baseline】
│   ├── 05b_dml.py                          # → results/psm_ddml.tex Panel B  【紧跟 baseline】
│   ├── 06_measures.py                      # → results/measures.tex          【稳健性，入附录】
│   ├── 07_hetero.py                        # → results/heterogeneity{1,2,3}.tex 【异质性先于机制】
│   ├── 08_channel.py                       # → results/channel{1,2,3}.tex
│   ├── 09_robust.py                        # → results/{addctr,specification,sampling,bunching-did}.tex
│   │                                       #   【全部入附录】
│   ├── 10_psm.py                           # → results/psm_ddml.tex Panel A + results/psm-pre-post.pdf
│   ├── 11_placebo.py                       # → results/placebo.pdf            【入附录】
│   ├── 12_further.py                       # → results/further.tex (+ results/specurve.pdf)
│   └── 99_assemble_main.py                 # 调用 render_main_tex()：生成项目根 main.tex
└── results/                                # 最终交付物：.tex 表格 + .pdf/.png 图像 全部放此处
                                            # 不再区分 tables/ 与 figures/ 子目录
```

**最终交付物（仅三类）**：

1. **Python 代码**：`code/` 目录下全部 `.py` 脚本，可从原始数据一键跑通到所有表图 + 组装 `main.tex`。
2. **图表**：`results/` 下的 `.tex`（LaTeX 表格，符合 template/ 格式）+ `.pdf` 与 `.png`（双份导出的图像）。**表格与图像统一放入 `results/`，不单独建 `tables/ figures/` 目录**。
3. **论文正文**：项目根的 `main.tex`（+ `ref.bib`），结构与 `template/main.tex` 一致；按 §6.4 的顺序串联 `results/` 中的图/表。

不交付 Word / Markdown 报告；不交付 Stata `.do` 文件；不交付中间数据集。

## 10. AI 在本 skill 下的行为准则

1. **计划书驱动**：无 proposal 不启动；proposal 即契约。执行中遇到任何判断岔路，先回查 `00_proposal.md`。
1.1 **期刊先定位**（§3.3 步骤 2、§3.4）：解析完计划书后**立即**推荐 5 本最匹配的目标期刊（`[J1]`–`[J5]`）并显式询问研究者选定；**在收到选择前不得跳到数据检索、骨架生成或任何 §4 主线环节**。研究者选定后必须把 `target_journal` / `bibliography_style` / `section_skeleton` 写入 `00_proposal.md` 顶部 YAML，并贯穿后续 `main.tex` 与所有 `render_*_tex()` 调用。
2. **自主闭环，不卡壳**：结果不达预期时，按第 3.A 节 Plan-B 决策树**自行切换并继续执行**，不停下等研究者拍板。切换即记录 `DECISION_LOG.md`。
3. **小步快跑**：一次只完成研究链条中的一个环节；完成后展示 .tex 摘要（前 10 行 + 后 10 行）与 proposal 预期的对比（✅/⚠️/❌），再进入下一环节。
4. **格式一致性检查**：每次写 .tex 前，先 Read 对应 `template/*.tex`，比对列数、列头、FE 行、Notes 段，再渲染。
5. **不擅自改规则**：`rule/` 中的规则是强制的；若研究者要求偏离，需要研究者明确书面说明（e.g., 审稿人要求改报告标准误 / 改为 Driscoll-Kraay SE）。
6. **不跑 Stata**：所有回归、PSM、DML、CS-DID、Stacked DID、bdiff 均用 Python 实现。`rule/` 中的 Stata 代码只作为"输出格式参照"。
7. **保护工作目录**：`asset/ rule/ template/` 三个文件夹只读，不写入、不修改、不重命名。所有研究输出只放入 `{项目名}/` 子目录。
8. **生成表后自检**：逐项核对 `rule/回归表写作规范总结.docx` 第九部分的"AI 写作检查清单"（三线表、控制变量全展示、t 值括号、`\sym{}` 星号、FE 行、聚类层级、表注完整）。
9. **只交付代码与图表**：最终产物限定为 `code/*.py` + `results/*.tex` + `results/*.pdf|png`（表与图同在 `results/`）；不产出额外报告、摘要、PPT、Word。
9.1 **不写任何叙述性 prose**（§6.4.2 / §6.4.5）：`main.tex` 正文区只渲染 `\section{...}` 与 `\subsection{...}` 标题骨架 + `% TODO: prose` 一行占位；**禁止**生成 `introduction.tex` / `background.tex` 等叙述性子文件，**禁止**写"In this section we …"/"This paper …"/"Section 2 describes …" 之类样板话。Abstract 同理：除非研究者明确提供 abstract 文字，否则保持空白。叙述性 prose 一律由研究者本人填入。
10. **全英文表达**：外国样本研究的变量名、表题、列头、FE 行、表注（`\noindent{\justifying{...}}`）**一律用英文**；避免中英混排。代码内部注释可使用中文便于研究者理解。
11. **凭证安全**：WRDS / FRED / Bloomberg / S&P Capital IQ 的账号、API key、token 不写入任何文件或日志；仅在 `code/00_config.py` 中以 `os.environ[...]` 读取，由研究者自己在本地 `.env` 中设置。

## 11. 启动示例

### 最小计划书（文本形式）

> **Research Proposal**
> Title: Sarbanes-Oxley Act and Corporate Investment Efficiency
> Hypothesis: The internal control disclosure requirement of SOX Section 404
>             (X = SOX404 compliance) improves investment efficiency (Y),
>             measured as lower deviation from the predicted level of investment.
> Expected findings: X reduces |investment deviation| significantly (p<0.05);
>             channel is "reduced information asymmetry → better project selection";
>             heterogeneity is stronger for firms with (i) higher pre-SOX agency cost,
>             (ii) less analyst coverage, (iii) weaker external governance.
> Identification: Staggered DID exploiting accelerated-filer (2004) vs non-accelerated-
>             filer (2007) compliance deadlines. Backed up by Sun-Abraham & Stacked DID.
> Sample: U.S. non-financial, non-utility Compustat firms, 2000-2010, NYSE/AMEX/NASDAQ
>         common stock (share code 10/11); exclude firms with assets < $10M.
> Shock: SOX Section 404 compliance; treatment = firms that cross accelerated-filer
>         threshold ($75M public float) in year $t$.
> Data: WRDS CRSP + Compustat + Audit Analytics (internal control opinion) +
>         IBES (analyst coverage). Keywords: "SOX", "internal control", "accelerated filer".
> Mechanism: M1 = information asymmetry (bid-ask spread, analyst forecast dispersion);
>            M2 = governance quality (G-index, board independence);
>            M3 = external financing cost (bond spread, Dealscan loan spread).
> Heterogeneity: pre-SOX G-index (tertile); analyst coverage (above/below median);
>            institutional ownership (tertile).

提交后 skill 立即：

1. 生成 `SOX_Investment_Efficiency/00_proposal.md`（固化 CONTRACT 九字段）
2. 搜索 asset/ 返回候选数据集（WRDS Audit Analytics / Compustat fundamentals annual / IBES Summary），等研究者选定与授权
3. 按第 4 节主线执行；若基准 X 系数方向反向或平行趋势不通过，自动进入 3.A.2 对应分支 Plan-B
4. 最终交付：`code/` 全套 Python + `results/*.tex` 全套表 + `results/*.pdf|png` 全套图（表与图同在 `results/`）+ 项目根 `main.tex` + `ref.bib` + `DECISION_LOG.md` 追溯记录
