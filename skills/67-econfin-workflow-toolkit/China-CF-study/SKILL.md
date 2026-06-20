---
name: China-CF-Study
description: 根据研究者提供的**研究计划书（Research Proposal）**执行基于中国制度环境的公司金融类实证研究全流程。**启动后第一件事：根据计划书的主题、识别策略、贡献边际与样本范围，从中国-context 英文顶级期刊池（JF/JFE/RFS/JFQA/MS/JCF/JBF/JAR/JAE/TAR/CAR/JIBS/China Economic Review/PBFJ 等 25+ 期刊）中推荐 5 本最匹配的目标期刊（[J1]–[J5]），等待研究者明确选定一本；该期刊决定 main.tex 的 bibliographystyle、Section 骨架、Introduction 风格与表注规范**。然后用 Python 完成数据清洗、描述性统计、基准回归、内生性检验（IV/2SLS、DML）、平行趋势、异质性、机制、稳健性检验与图表绘制。LaTeX 表格和图像严格遵循 template/ 示例格式，研究逻辑与排版严格遵循 rule/ 下的《通用实证研究逻辑与规范总结》与《回归表写作规范总结》。数据集与政策集从 asset/ 中按计划书中的关键词检索。**当计划书预期的实证结果无法实现时（系数不显著、平行趋势不通过、IV 弱工具、机制不成立等），skill 自动切换备选方案直至完成研究项目**。最终交付物：Python 代码 + LaTeX 表格 + 图像（.pdf/.png）。触发条件：研究者提交研究计划书（含 X→Y 假设、识别策略、样本、政策冲击等）。
---

# China Corporate Finance Empirical Study (china-cf-study)

## 1. 定位与适用范围

本 skill 指导**基于中国制度环境的公司金融类实证研究**的完整流程。覆盖：

- 以 A 股上市公司、中国城市/省级面板为主体样本
- 识别策略：DID（含 staggered/CS-DID/Sun-Abraham）、Panel FE + IV/2SLS、PSM-DID、DML / DML-IV、合成控制、RDD
- 研究主题：投融资、治理、股权结构、机构投资者、信贷、创新、披露、审计、分析师、ESG 等
- **代码语言：Python**（pandas / numpy / statsmodels / linearmodels / pyfixest / econml / doubleml / scikit-learn / matplotlib）
- **表格输出：LaTeX**（严格遵循 template/ 格式与 rule/ 规范）

本 skill 不替代研究者的研究设计判断，而是把每一环节的**标准流程、代码骨架、表格/图像模板**提供给研究者，保证产出质量达到中国-context **英文顶级期刊**（JF、JFE、RFS、JFQA、RCFS、JCF、JBF；JAR、JAE、TAR、CAR、RAST；MS、SMJ、JIBS；AER、QJE、JPubE、JEEM；以及 China Economic Review、Pacific-Basin Finance Journal、Emerging Markets Review、China Journal of Accounting Research 等 China-friendly 主流刊）的写作与方法论要求。**目标期刊在启动后第二步即由 skill 推荐 + 研究者锁定**（见 §3.4），后续 main.tex 的 bibliographystyle、Section 骨架、Introduction 风格、表注规范均以此为准。

## 2. 工作目录结构（项目根即 working directory）

```
China-CF-study/                 ← working directory
├── asset/                      ← 中国常见数据集与政策集索引（研究者提供检索关键词）
│   ├── macrodatas_list.csv           # 马克数据网数据集清单（宏观/上市公司/城市层）
│   ├── ppmandata_trade_list.csv      # 皮皮慢数据（政策/贸易/金融等）清单
│   ├── 全网首发计量方法+政策数据库.pdf # 原始政策冲击数据库 PDF（975 页，含 800+ 实证研究的方法-政策详尽案例）
│   ├── 计量方法+政策数据库.md       # ★ 上面 PDF 的 50 页 markdown 精简版（按"方法 × 政策 × 数据"三维交叉重组；首选入口）
│   └── MCP.docx                      # MCP 服务器清单（如 CSMAR-MCP），含安装网址
├── rule/                       ← 强制性写作与方法论规范（AI 必须逐项遵循）
│   ├── 通用实证研究逻辑与规范总结.docx
│   └── 回归表写作规范总结.docx
├── template/                   ← LaTeX 表格与图片模板（格式模仿对象）
│   ├── main.tex                      # ★ 正文 .tex 模板——新项目 main.tex 的 Preamble / References / Appendix 块均以此为底
│   ├── sum_stat.tex                  # 描述性统计
│   ├── variables.tex                 # 变量定义
│   ├── baseline.tex                  # 基准回归（渐进式加控制 + 渐进式加 FE）
│   ├── addctr.tex                    # 加入附加控制变量
│   ├── measures.tex                  # 替换因变量度量
│   ├── specification.tex             # 高维交互固定效应
│   ├── iv.tex                        # 2SLS 工具变量
│   ├── psm_ddml.tex                  # PSM + DML（Panel A / Panel B）
│   ├── bunching-did.tex              # Bunching-DID
│   ├── channel1.tex, channel2.tex, channel3.tex   # 机制分析（按渠道分组）
│   ├── heterogeneity1.tex, heterogeneity2.tex, heterogeneity3.tex # 异质性（bdiff）
│   ├── sampling.tex                  # 样本筛选稳健性
│   ├── further.tex                   # 进一步分析
│   ├── parallel.pdf                  # 平行趋势图
│   ├── csdid-figure.pdf              # Callaway-Sant'Anna DID 动态效应
│   ├── estimator.pdf                 # 不同 DID 估计量对比
│   ├── psm-pre-post.pdf              # PSM 平衡检验前后
│   └── specurve.pdf                  # 规格曲线（specification curve）
└── 研究项目输出/                  ← 每个实证项目的产出目录（按本 skill 建议结构创建）
    └── {项目名}/
        ├── main.tex                   # ★ 正文入口（preamble 照抄 template/main.tex），\input{results/xxx.tex}
        ├── data/{raw,cleaned}/
        ├── code/                      # Python 脚本
        └── results/                   # 表格 (.tex) 与图像 (.pdf/.png) 统一存放
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
    PSM-DID / RDD / 合成控制 / DML 中择一
(5) 样本范围 (Sample)：层级（公司-年/城市-年/省-年）、时间窗、排除条款
(6) 政策冲击 (Shock)：【DID/RDD 必填】政策名称、公布/实施年份、处理组定义
(7) 数据需求 (Data)：关键词清单（数据集 + 政策集）。来源优先级：
    asset/ 清单 → asset/MCP.docx 登记的 MCP 服务器（如 CSMAR-MCP）
    → CSMAR / WIND / RESSET / 统计年鉴 / 政府公开 / 手工整理 等外部来源
(8) 机制假说 (Mechanism)：预期作用渠道 M1 / M2 / M3
(9) 异质性维度 (Heterogeneity)：预期分组维度 + 预期组间差异方向
```

### 3.3 启动后 skill 立即执行以下动作

1. **解析计划书** → 抽取 CONTRACT 九字段，对缺项统一一次性追问补齐。
2. **🆕 推荐 5 个最合适的英文目标期刊（详见 §3.4）**：基于计划书的研究主题（Topic）、识别策略（Method）、贡献边际（Novelty）与样本范围（Sample / China context）四维度，从中国-context 英文顶刊池（§3.4.1）中按加权得分（§3.4.2）选出 top 5，以 `[J1]`–`[J5]` 编号 + 4 维星级评分 + "Why it fits" 一两句话（含本刊近 3 年发表的同主题中国论文示例 1 篇）+ "Editorial preference" + bib style 呈现（输出格式见 §3.4.3）。**呈现完毕后停下，显式询问研究者选定哪一本**（也允许用户提出列表外的期刊）。在收到选择前**不进入第 3 步**。
3. **固化为 `00_proposal.md`**：写入项目根 `{项目名}/00_proposal.md`，**顶部以 YAML 块追加 `target_journal` / `bibliography_style` / `writing_preferences` 三组字段**（见 §3.4.3 末尾示例），作为后续所有判断与 `main.tex` 渲染的基准文件。
4. **生成研究项目骨架**：按第 9 节目录结构建立 `{项目名}/` 下所有子目录与占位脚本；`main.tex` 头部按 §3.4.4 表把 `\bibliographystyle{}` 与 Section 骨架替换为目标期刊的版本（preamble 仍然照抄 `template/main.tex` 的其他部分）。
5. **逐环节推进**：严格按第 4 节顺序执行，每一环节完成即与计划书中 (3) 预期结果**逐项比对**。

### 3.4 期刊定位（Journal Targeting）— 启动后第二步的依据

#### 3.4.1 候选期刊池（中国 CF 论文常见英文投稿池）

中国数据 CF 论文的现实投稿地图与美国/跨国数据不同——三大综合刊（AER/QJE/JPE）罕见纯中国 CF 选题（除非政策有全球影响如 China Shock 系列）；JF/JFE/RFS 近 5 年中国论文产出明显增加，但要求"机制全球可借鉴 + 识别透明"；JCF/JBF/PBFJ/CER/EMR/CJAR 等是中国 CF 主流刊。

| Tier | 期刊 | 全名 | 中国-context 偏好特征 | bib style |
|---|---|---|---|---|
| T1 综合 | AER | American Economic Review | 仅接 China Shock 类全球影响政策；CF 主题罕见 | aer |
| T1 综合 | QJE | Quarterly Journal of Economics | 高门槛自然实验；中国 CF 极罕见 | qje |
| T1 综合 | JPE | Journal of Political Economy | 偏理论结构估计；中国治理/契约偶有 | jpe |
| T1 综合 | REStud | Review of Economic Studies | 结构 + 方法；中国 CF 罕见 | restud |
| T1 金融 | JF | Journal of Finance | 故事完整 + 大样本中国机制创新（split-share、QFII、HK Connect、注册制） | jf |
| T1 金融 | JFE | Journal of Financial Economics | 中国主题最活跃接收刊；识别透明 + 控制变量逐项展示 | jfe |
| T1 金融 | RFS | Review of Financial Studies | 理论嵌入 + 中国独特机制 | rfs |
| T2 金融 | JFQA | Journal of Financial and Quantitative Analysis | 严谨实证；中等贡献中国识别清晰选题 | jfqa |
| T2 金融 | RCFS | Review of Corporate Finance Studies | CF 专门 OA 刊；中国论文比例上升 | rcfs |
| T2 金融 | RAPS | Review of Asset Pricing Studies | A 股资产定价；非纯 CF | raps |
| T2 金融 | JCF | Journal of Corporate Finance | **中国 CF 主流接收刊**；中国选题占比高 | elsarticle-num |
| T2 金融 | JBF | Journal of Banking and Finance | **中国银行/信贷主流刊**；中国选题接受度高 | elsarticle-num |
| T2 金融 | JFI | Journal of Financial Intermediation | 中国银行 / 信贷 / 中介 | jfi |
| T2 金融 | JFM | Journal of Financial Markets | A 股微观结构 / 流动性 | elsarticle-num |
| T2 金融 | FM | Financial Management | CF 应用导向 | apa |
| T1 会计 | JAR | Journal of Accounting Research | 中国披露 / 分析师 / 审计 / 信息环境 | jar |
| T1 会计 | JAE | Journal of Accounting and Economics | 中国契约 / 高管薪酬 / 经济后果 | jae |
| T1 会计 | TAR | The Accounting Review | 中国数据近年大量接收（治理、披露、审计） | tar |
| T2 会计 | RAST | Review of Accounting Studies | 中国估值 / 披露 / 信息环境 | rast |
| T2 会计 | CAR | Contemporary Accounting Research | 中国数据接受度高；与 TAR 平台相近 | car |
| 管理 | MS | Management Science | **中国数据友好**；因果识别 + 跨学科创新 | informs |
| 管理 | SMJ | Strategic Management Journal | 中国治理 / 跨国并购 / 公司战略 | smj |
| 管理 | OS | Organization Science | 中国治理 + 组织 + CF 交叉 | orsc |
| 国际 | JIBS | Journal of International Business Studies | 跨国 / 制度差异 / Chinese MNEs / 跨境 M&A | jibs |
| 公共 | JPubE | Journal of Public Economics | 中国税收 / 监管的 CF 后果（营改增、金税工程） | elsarticle-num |
| 环境 | JEEM | Journal of Environmental Economics and Management | 环保税 / 双碳 / 排污权 × CF | elsarticle-num |
| 中国-friendly | CER | China Economic Review | **中国主题专刊**；门槛中等；CF 接收量大 | elsarticle-num |
| 中国-friendly | PBFJ | Pacific-Basin Finance Journal | **亚太/中国 CF 中下游主流刊** | elsarticle-num |
| 中国-friendly | EMR | Emerging Markets Review | 中国/新兴市场 CF；制度差异比较 | elsarticle-num |
| 中国-friendly | CJAR | China Journal of Accounting Research | **中国会计实证主刊**（Peking University & Elsevier） | elsarticle-num |
| 中国-friendly | CFRI | China Finance Review International | 中国 CF 应用导向 OA 刊 | apa |
| 中国-friendly | CAFR | China Accounting and Finance Review | 中国 CF / 会计；中文摘要双语 | apa |
| 跨学科 | JBE | Journal of Business Ethics | ESG / 治理 / 文化 × 中国 | apa |
| 国际财务 | JIFMA | Journal of International Financial Markets, Institutions and Money | 跨境 / 制度 / 资本流动 × 中国 | elsarticle-num |

> 若研究者指名列表外的期刊（如 *British Accounting Review*、*Asia-Pacific Journal of Accounting and Economics*、*International Review of Economics and Finance*、*Finance Research Letters*、*Journal of International Money and Finance* 等），照单选定即可，并比照同档期刊套用 bib style 与 Section 骨架。

#### 3.4.2 匹配评分（skill 内部）

对每本候选按 4 维 1–5 打分：

```
T = topic_fit       # CF 主题与期刊偏好对齐
M = method_fit      # 识别策略与期刊门槛对齐
N = novelty_fit     # 贡献边际能否打动该刊编辑（中国机制能否对国际读者讲得通）
S = sample_fit      # 中国样本与期刊地理偏好（China-friendly 加分，纯美国偏好刊扣分）
score = 0.35 T + 0.30 M + 0.25 N + 0.10 S
```

匹配示例（仅作 skill 内部参考；不输出给研究者）：

- "金税三期 × 企业避税与投资" → JFE / JAE / JPubE / TAR / JCF
- "Sci-Tech Innovation Board（科创板）注册制 × IPO 定价效率" → JFE / RFS / JFQA / JCF / PBFJ
- "沪港通 × 公司治理与信息环境" → JF / RFS / JAR / JFE / MS
- "Shanghai-Hong Kong Stock Connect × 分析师覆盖与盈余质量" → JAR / JAE / TAR / CAR / JFE
- "绿色信贷指引 × 重污染企业投资" → JFE / JEEM / JCF / CER / JBF
- "营改增 (B2V) × 企业组织重组" → JPubE / JAE / JFE / JCF / CER
- "QFII 持股 × 公司治理与盈余管理" → JFE / JAR / RFS / MS / JCF
- "数字经济试点 / 宽带中国 × 融资约束" → JFE / MS / JCF / CER / PBFJ
- "土地财政 × 企业投资行为" → JF / JFE / JPubE / MS / CER
- "中国民营/国有差异 × 信贷可得性" → JFE / JCF / JBF / CER / PBFJ
- "审计师法律责任改革 × 审计质量" → JAR / JAE / TAR / CAR / RAST
- "ESG 评级分歧 × 中国企业融资成本" → JFE / RFS / JCF / JBE / CER

#### 3.4.3 推荐输出格式（必须按此格式呈现 5 本）

```
[J1] JFE — Journal of Financial Economics
     Topic ★★★★★  Method ★★★★★  Novelty ★★★★☆  Sample ★★★★★   Score 4.70
     Why it fits: {2 句话——对齐研究主题与识别方法；指本刊近 3 年发表的相近中国
                   主题论文（举 1 篇，作者-年份-标题缩写）}
     Editorial preference: 偏好识别透明 + 表格规范严 + 控制变量逐项展示
     Bibliography style: jfe

[J2] JCF — Journal of Corporate Finance
     ...
```

呈现完 5 本后，**必须显式停下并询问**（不要自动选定）：

> 请从 [J1]–[J5] 中选定一本作为目标期刊；若不满意，请直接告知任一中国-context 英文 CF 顶刊名（如 JF / TAR / MS / China Economic Review 等）。
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
    - Background (China's institutional setting)
    - Data
    - Empirical Strategy
    - Results
    - Robustness
    - Conclusion
---
```

#### 3.4.4 不同期刊触发的写作差异

| 期刊 | bib style | Section 骨架 | Intro 风格 | 表注最低 | 中国-context 特别要求 |
|---|---|---|---|---|---|
| JF  | jf  | Intro / Setting / Hypotheses / Data and Methodology / Results / Mechanism / Conclusion | 5–6 段，puzzle 驱动 | ≥ 8 行 | Setting 段须解释中国制度对国际读者；偏好简洁列头 |
| JFE | jfe | Intro / Background / Data / Empirical Strategy / Results / Robustness / Conclusion | 5 段，识别细节早出现 | ≥ 6 行 | Background 段须详述中国政策；表格规范最严；控制变量逐项展示 |
| RFS | rfs | Intro / Theoretical Motivation / Data / Identification / Empirical Findings / Conclusion | 4–5 段，理论 motivation 醒目 | ≥ 6 行 | 偏好理论嵌入；中国机制需有 model micro-foundation；正文 25–30 页 |
| JFQA | jfqa | 类 JFE | 类 JFE | ≥ 5 行 | 中国识别清晰即可；表格规范严 |
| JCF | elsarticle-num | Intro / Background / Data / Methodology / Results / Conclusion | 4–5 段，中国制度背景较多 | ≥ 5 行 | **中国 CF 主流刊**；可较窄主题；中国读者也读，制度术语可保留拼音注释 |
| JBF | elsarticle-num | 类 JCF | 4 段 | ≥ 5 行 | 偏好中国银行/信贷/监管主题 |
| JAR | jar | Intro / Hypothesis Development / Sample and Data / Research Design / Results / Conclusion | 6 段，hypothesis 在 §2 独立 | ≥ 6 行 | Hypothesis section 必须独立；预测式 H1/H2/H3；中国制度在 §2 末尾或 §3 开头介绍 |
| JAE | jae | 类 JAR | 6 段 | ≥ 6 行 | 经济后果导向；中国契约/治理选题须有可检验对立预测 |
| TAR | tar | 类 JAR | 类 JAR | ≥ 5 行 | 类 JAR；偏好新 measure；中国数据近年大量接收 |
| CAR | car | 类 JAR | 类 JAR | ≥ 5 行 | 与 TAR 平台相近；中国会计接受度高 |
| RAST | rast | 类 JAR | 5 段 | ≥ 5 行 | 偏好估值 / 信息环境；可中国披露改革 |
| AER | aer | Intro / Background / Data / Empirical Strategy / Results / Mechanism / External Validity / Conclusion | 4 段，影响广泛 | ≥ 5 行 | 必须有外部有效性讨论；中国选题须有全球影响（如 China Shock） |
| QJE / JPE / REStud | qje / jpe / restud | 类 AER（结构更紧凑） | 4 段，puzzle + economic significance | ≥ 5 行 | 跨子学科可读性；中国 CF 须显著方法/概念创新 |
| MS  | informs | Intro / Background / Hypotheses / Data and Methods / Results / Discussion / Conclusion | 4–5 段，跨学科 motivation | ≥ 5 行 | 必含 managerial implication；**中国数据友好**；强调因果识别 |
| SMJ | smj | 类 MS | 4–5 段 | ≥ 5 行 | 中国治理 / 跨国并购 / 战略选择 |
| JIBS | jibs | Intro / Theory and Hypotheses / Methods / Results / Discussion / Conclusion | 5 段，跨国比较视角 | ≥ 5 行 | 必含 international business 贡献；偏好 Chinese MNEs / 制度差异 |
| JPubE / JEEM | elsarticle-num | 类 JFE | 4 段 | ≥ 5 行 | 偏好中国税收/环保政策的 CF 后果 |
| CER | elsarticle-num | Intro / Background / Data / Methodology / Results / Conclusion | 3–4 段，中国制度可较详 | ≥ 4 行 | **中国主题专刊**；中国制度术语可较密集；可中国读者视角 |
| PBFJ | elsarticle-num | 类 CER | 3–4 段 | ≥ 4 行 | 亚太/中国 CF；门槛低于 JCF |
| EMR | elsarticle-num | 类 CER | 3–4 段 | ≥ 4 行 | 中国/新兴市场对照；制度差异是 selling point |
| CJAR / CAFR / CFRI | elsarticle-num / apa / apa | 类 JAR / JCF | 3–4 段 | ≥ 4 行 | 中国主流接受度高；可中文摘要双语；制度术语可不解释过细 |

`render_main_tex()` 在生成 `main.tex` 时读取 `00_proposal.md` 的 `target_journal` / `bibliography_style` / `section_skeleton`，自动替换 `\bibliographystyle{}` 与 Section 命名；同时把目标期刊的 `notes_paragraph_length` 阈值传入各 `render_*_tex()` 函数，确保表注长度达到目标刊门槛。

## 3.A 自适应机制（Plan-B）：结果未达预期时的切换逻辑

**本 skill 的核心能力**——当任一环节的实证结果与 `00_proposal.md` 中"(3) 预期结果"不符时，skill **不要求研究者干预**，自主在以下备选方案树中选择并执行，直到研究项目闭环。

### 3.A.1 失败判据（每环节完成后立即触发）

| 环节 | 预期结果 | 失败判据（触发 Plan-B） |
|---|---|---|
| 平行趋势检验 | 所有 pre 期系数不显著 | 任一 pre 期 \|t\|>1.96 |
| 基准回归 | X 系数符号与预期一致且 p<0.1 | 符号反向 / 全部不显著 / 系数随控制变量/FE 添加大幅跳动 |
| 稳健 DID 估计量 | CS-DID / Sun-Abraham 结论方向与 TWFE 一致 | 符号反向或 p 值量级完全不匹配 |
| IV 第一阶段 | F 统计量 > 10、IV 显著 | F < 10 或 IV 不显著 |
| IV 第二阶段 | LATE 与 OLS 方向一致、可解释 | 符号反向且数量级异常 |
| 机制分析 | 预期渠道 M1/M2/M3 显著 | 所有渠道不显著 |
| 异质性 | 预期维度组间差异显著 | bdiff p > 0.1 |
| 稳健性 | X 系数符号/显著性在多数列稳定 | 超过 1/3 列翻转 |
| 安慰剂 *(仅 DID / Staggered DID / PSM-DID 项目执行；纯 Panel FE+IV / RDD / DML / 合成控制 项目跳过本环节)* | 真实系数在虚假分布之外 | 真实系数落在虚假分布的 [5%,95%] 内 |

### 3.A.2 Plan-B 决策树（按顺序尝试，每步可叠加）

```
失败环节 → 依次尝试：

【基准回归】系数不显著 / 符号反向
  ├─ B1. 替换 Y 度量（从 template/measures.tex 思路：Ln(...)、子维度拆分、行业调整）
  ├─ B2. 替换 X 度量（连续 vs 虚拟 / 强度 vs 0-1）
  ├─ B3. 替换 FE 规格（加 Industry×Year、Province×Year，高维交互）
  ├─ B4. 替换聚类层级（firm → city → province×year 双向）
  ├─ B5. 样本细化（剔除金融业、ST、IPO 当年；仅保留主要政策实施前已上市样本）
  ├─ B6. 换时间窗（缩短到政策前后 ±5 年）
  └─ B7. 若仍不显著 → 考虑反向假设（Y→X 或 U 型/门槛），在 proposal 中注明假设修正

【平行趋势】pre 期显著
  ├─ B1. 重新定义政策时点（公布年 vs 实施年 vs 试点年）
  ├─ B2. 用 Sun-Abraham / CS-DID 替代 TWFE
  ├─ B3. 限制政策前窗口（仅保留 pre_3 到 las_K）
  ├─ B4. 加入 Group × linear trend 控制差异化趋势
  └─ B5. 改为 PSM-DID 缓解选择偏差后重测

【IV 第一阶段弱】F < 10
  ├─ B1. 尝试 asset/计量方法+政策数据库.md §6.2 "X→IV 配对清单"中相同 X 的备选 IV，或 §12 政策大全中同维度的其他外生冲击（如 Broadband/TechFin/Court）
  ├─ B2. 构造 Bartik / Shift-Share IV（行业份额×全国冲击）
  ├─ B3. 用滞后变量 / 同伴平均 (peer mean) 作为 IV
  ├─ B4. 改为 DML-Partial（弱化 IV 依赖，用 ML 处理高维混淆）
  └─ B5. 改用断点/匹配的自然实验替代 IV

【机制不显著】所有 M 均无效应
  ├─ B1. 换中介变量度量（同一渠道的不同代理）
  ├─ B2. 换渠道组合（从供给→需求→制度三维替换）
  ├─ B3. 拆分样本（分组后分别做机制，寻找条件性渠道）
  ├─ B4. 改用交互项检验（X × M → Y 是否有调节）
  └─ B5. 若仍无渠道显著 → 在"进一步分析"中承认黑箱，改做异质性深挖

【异质性不显著】bdiff p > 0.1
  ├─ B1. 换分组切点（median → tertile/quartile）
  ├─ B2. 换分组变量（同维度其他代理）
  ├─ B3. 连续调节变量做交互项（企业级）
  ├─ B4. 换分组维度（经济→制度→文化→政策四大簇切换）
  └─ B5. 保留为"null heterogeneity"——在论文正文中作为结论的边界条件陈述

【稳健性大面积翻转】
  ├─ B1. 回溯样本构造（检查缺失/极端值/行业代码）
  ├─ B2. 检查是否遗漏同期政策 → 加入 co-shock dummy
  ├─ B3. 重算处理组/对照组的定义口径
  └─ B4. 若仍不稳健 → 核心结论弱化为"条件性证据"，在正文强调边界

【安慰剂失败】真实系数落在虚假分布内
  ├─ B1. 增加 reps（500 → 1000 → 2000）
  ├─ B2. 换安慰剂设计（空间 → 时间 → 空间+时间双维度）
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

- **成功**：基准回归 + 机制 + 异质性 + 稳健性 全部通过；DID 项目额外要求安慰剂通过（或部分以"边界条件"形式可解释）。非 DID 项目不要求安慰剂
- **降级闭环**：Plan-B 深度超过 3 层仍无法收敛时，把研究降级为"**零效应识别报告**"或"**条件性证据报告**"，产出仍完整：所有 .tex / 图 / 代码照常交付，正文结论段改写为 null-result 叙事
- **永不**：放弃项目或向研究者"投降"；skill 必须给出一份完整可交付的研究产出

## 4. 研究逻辑主线（严格按顺序，不可颠倒）

顺序来自 `rule/通用实证研究逻辑与规范总结.docx` 第 7.2 节。每一步都配有下文的 Python 代码骨架与 template/ 中的 LaTeX 对照模板。

| # | 环节 | 必做？ | 对应 Python 产物 | 对应 LaTeX 模板 |
|---|---|---|---|---|
| 1 | 描述性统计 + 变量定义 + 样本构造 | **必做** | `01_clean.py` → `sample.tex`；`02_sumstat.py` → `sum_stat.tex` + `variables.tex` | `template/sum_stat.tex` + `variables.tex`（+ 样本表按 `psm_ddml.tex` 的 Panel A/B 风格手写） |
| 2 | 平行趋势检验 | DID **必做**；其他跳过 | `02_parallel.py` → `results/parallel.pdf` | `template/parallel.pdf` |
| 3 | 异质性稳健 DID 估计量 | staggered DID **必做** | `03_csdid.py`（CS-DID / Sun-Abraham / Stacked） | `template/csdid-figure.pdf` + `estimator.pdf` |
| 4 | **基准回归** | **必做（定海神针）** | `04_baseline.py` → `baseline.tex` | `template/baseline.tex` |
| 5 | 内生性检验 | Panel FE **必做**；DID 推荐 | `05_iv.py` + `05_dml.py` | `template/iv.tex` + `psm_ddml.tex` Panel B |
| 6 | 因变量分解 / 替换度量 | 推荐 | `06_measures.py` | `template/measures.tex` |
| 7 | 机制分析 | **必做** | `07_channel1.py`, `07_channel2.py`, `07_channel3.py` | `template/channel1/2/3.tex` |
| 8 | 异质性分析 | **必做** | `08_hetero1.py`, `08_hetero2.py`, `08_hetero3.py` | `template/heterogeneity1/2/3.tex` |
| 9 | 稳健性检验 | **必做** | `09_addctr.py`, `09_spec.py`, `09_sampling.py`, `09_bunching.py` | `template/addctr/specification/sampling/bunching-did.tex` |
| 10 | PSM-DID | DID **推荐** | `10_psm.py` → `psm_ddml.tex` Panel A | `template/psm_ddml.tex` + `psm-pre-post.pdf` |
| 11 | 安慰剂检验 | **DID 必做；非 DID 项目跳过** | `11_placebo.py` → `results/placebo.pdf` | 参照 `rule` 第 5.2 节安慰剂分布图规范 |
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
```

### 5.2 固定效应 + 聚类标准误的标准回归

```python
def reg_hdfe(df, y, x, controls, fe, cluster):
    """
    y: 因变量名 (str)
    x: 核心解释变量名 (str)
    controls: 控制变量名列表
    fe: 固定效应列表, e.g. ['firm_id','year']
    cluster: 聚类层级, e.g. 'firm_id'
    返回 pyfixest.Feols 对象
    """
    rhs = x + ' + ' + ' + '.join(controls)
    fe_str = ' + '.join(fe)
    formula = f"{y} ~ {rhs} | {fe_str}"
    return pf.feols(formula, data=df, vcov={'CRV1': cluster})
```

### 5.3 工具变量 / 2SLS

```python
def iv_2sls(df, y, x_endog, instruments, controls, fe, cluster):
    """
    先做 within 变换（去掉 fe），再 IV2SLS，
    报告 Kleibergen-Paap rk Wald F。
    instruments: IV 列表（每列单独一列 + 合并一列交叉验证）
    """
    # pyfixest 原生支持 IV：
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

### 5.5 Staggered DID：Callaway-Sant'Anna / Sun-Abraham

```python
# CS-DID：用 differences 包或手写 group-time ATT 聚合
# Sun-Abraham：interaction-weighted estimator，用 pyfixest 的 sunab() 便捷函数
def csdid_event_study(df, y, cohort, time, controls, cluster):
    """
    cohort: 处理开始年份（未处理组为 NaN/Inf）
    返回：{e: att, se, ci} 的字典，用于画动态效应图（event_study plot）
    """
    # 实现 Callaway & Sant'Anna (2021) 做法
    # 或直接调用 pyfixest.feols 配合 i(time, treat, ref=-1) 画事件研究
    ...
```

### 5.6 PSM / Entropy Balancing

```python
def psm_match(df, treat, covariates, k=4, caliper=0.002):
    """最近邻 1:k 匹配 + caliper。返回带权重的新 DataFrame。"""
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import NearestNeighbors
    # 估计倾向得分 → 最近邻匹配 → 返回匹配后样本
    ...

def entropy_balance(df, treat, covariates):
    """使用 ebalance / cvxpy 实现熵平衡重加权。"""
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

## 6. LaTeX 输出：严格遵循 template/ + rule/

**所有 `.tex` 由 Python 函数手写生成**，目标是让输出和 `template/` 中对应文件**视觉一致**：相同的 `\toprule / \midrule / \bottomrule`、相同的 `\sym{}` 宏、相同的列头结构（`&\multicolumn{1}{c}{(1)}…`）、相同的表注 justifying 段。

### 6.1 铁律（出自 rule/ 两份文档）

1. **不用竖线（`|`），不在系数区加额外 `\hline`**。三线表：`\toprule / \midrule / \bottomrule` 各一次。
2. **控制变量必须逐一展示系数与 t 值**，**禁止** "Controls: Yes/No" 省略。
3. **变量顺序固定**：核心 X → （交互项）→ 控制变量 → Constant（通常省略）。
4. **括号内是 t 值**（不是标准误），表注首行固定写 `t statistics in parentheses`（若改为 SE，表注同步改）。
5. **显著性符号**固定为 `***` p<0.01, `**` p<0.05, `*` p<0.1，星号嵌于 `\sym{}` 宏。
6. **数值格式**：系数 `%.4f`，t 值 `(%.2f)`，观测数 `%,.0f`，R² `%.2f`。
7. **底部固定效应行**：`Firm FE / Year FE / City FE / Ind × Year FE …`，Yes/No 显式标注。
8. **聚类层级匹配**：聚类标准误层级必须与核心解释变量变异层级一致，表注中写清楚 "robust t-statistics clustered by the firm/city/..."。
9. **表注（noindent + justifying 段）必须写全**：样本范围（"Chinese A-share listed firms from YYYY to YYYY"）、因变量定义、核心 X 定义、控制变量逐一列出、FE 组合、聚类层级、**交叉引用 `Table \ref{definition}`**、显著性符号说明。
10. **异质性表格**必须含 `\cmidrule(lr){i-j}` 分组列头，并在表尾增加 `p-value for Diff. (High-Low)` 一行（bootstrap Fisher 置换检验，reps=500）。

### 6.2 Python 渲染函数（骨架）

```python
def render_baseline_tex(models, labels_cols, var_order, var_labels,
                        fe_rows, nobs, r2, caption, label, note,
                        out_path):
    """
    按 template/baseline.tex 的结构写出 .tex。
    models: 列表，每个元素是 (coef_dict, t_dict)；coef_dict 的 key 与 var_order 一致。
    fe_rows: [('Firm FE', ['Yes','Yes',...]), ('Year FE', [...]), ...]
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
    # FE 行 + Obs + Adj R²
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

`render_sumstat_tex`、`render_iv_tex`（含 First Stage/Second Stage 分组列头 + `\cmidrule`）、`render_channel_tex`（因变量行在第二层列头）、`render_heterogeneity_tex`（含 `p-value for Diff.` 行）、`render_psm_ddml_tex`（Panel A + Panel B 复合表）、`render_variables_tex`（`p{2.0cm}p{13.5cm}` 两列定义表）、`render_sample_tex`（附录用，**Panel A + Panel B** 两栏式样）按 template/ 中对应文件一一对应实现。

**`render_sample_tex` 结构要求（附录 `sample.tex`）**：

- **Panel A: Sample Construction** —— 三列表：`Filtering Step | # Firm-Year Observations | # Unique Firms`
  - 示例行：`All CSMAR A-share firm-years (2003-2023) / Drop financial & insurance (CSRC=J) / Drop ST or *ST / Drop IPO year / Drop firm-years with missing controls / Final sample`
  - 每一步给出剔除数量与剩余数量，最终一行为最终样本量
- **Panel B: Sample Distribution** —— 两个子表并排或纵向堆叠：
  - B1. By Year：year / N / % of total
  - B2. By Industry（CSRC 2012 一位代码）或 By Region（东/中/西 或 省份）：group / N / %
- **格式**：沿用 `template/psm_ddml.tex` 的 Panel A / Panel B 两 `tabularx` 并列写法；三线表；列头居中；样本量 `%,.0f` 格式
- **表注（`\noindent{\justifying{...}}`）**：说明样本起止年、排除条款、缩尾分位；给出 CSRC 2012 行业代码口径、东中西划分依据

### 6.3 图像绘制（matplotlib）

遵循 `rule/回归表写作规范总结.docx` 第五部分图像规范：白底、黑框、Times New Roman、`.pdf` + `.png` 双份输出。

- **事件研究图**：`errorbar(rcap 样式) + axhline(0) + axvline(基准期, linestyle='--')`
- **规格曲线**：系数值排序散点 + 下方变量勾选矩阵
- **安慰剂分布**：`hist + kde`，真实系数 `axvline(color='red')`
- **森林图**：横向 `errorbar`，按"经济/制度/文化/政策"分组，每组一个 subplot
- **PSM 平衡**：匹配前/后 |% bias| 散点或条形图
- **Binscatter**：`seaborn.regplot` 或手写残差化后分 bin，散点 navy，拟合线 maroon

## 7. 数据来源与检索流程（asset/ 优先，但不限于 asset/）

### 7.1 数据来源优先级

**数据来源不限于 `asset/` 中的两份清单**——`asset/` 只是**优先考虑**的入口。实际研究中，研究者可（且应）按下述优先级补充其他来源：

1. **asset/计量方法+政策数据库.md（50 页精简版） + 两份 CSV 清单**（马克数据网 + 皮皮慢数据）—— 最优先；md 提供"方法 × 政策 × 数据"三维交叉速查，CSV 提供数据集名匹配
1.5. **asset/全网首发计量方法+政策数据库.pdf** —— 仅当 md 精简版不足时打开（975 页完整版，按 md §14 索引定位到 PDF 页码）
2. **asset/MCP.docx 中登记的 MCP 服务器**（如 CSMAR-MCP：<https://lobehub.com/zh/mcp/yourusername-csmar-mcp-server>）—— 次优先。MCP 服务器可通过 Claude Code 直接拉取数据，免手工下载
3. **商业数据库**：CSMAR（国泰安）、WIND、RESSET、CNRDS、BvD Osiris、Thomson Reuters
4. **官方统计**：国家统计局 / 人民银行 / 银保监会 / 证监会 / 海关总署 / 各级地方统计局年鉴
5. **政府信息公开**：生态环境部数据中心、国务院发展研究中心、各部委公报、裁判文书网
6. **学术镜像**：北京大学开放研究数据平台、CEIC、WGI、CGSS / CFPS / CHIP 微观调查
7. **自建/手工整理**：政策文本分词、公告解析、企业年报文本、专利申请文本、社交媒体
8. **第三方开源**：JoinQuant / Tushare / AkShare / BaoStock 等爬虫接口
9. **境外对照**：Compustat / CRSP（同行业国际对照），Worldscope（境外子公司）

**MCP 服务器使用说明**：`asset/MCP.docx` 登记的每个 MCP 服务器附有 lobehub 页面 URL，**按页面中的安装指引**（通常是 `npx` / `uvx` 命令配置到 `~/.claude.json` 或 `settings.json` 的 `mcpServers` 字段）完成安装；安装后通过 `mcp__<server-name>__<tool>` 前缀工具调用。安装步骤由研究者或 skill 借助 update-config skill 辅助完成。

### 7.2 检索流程（优先→兜底）

1. **研究者先给数据关键词**（如"地级市数字经济""股权质押""绿色专利""环保税""金税工程""沪港通""注册制""营改增"…）或政策名。
2. **第一轮：查 asset/ 清单**。
   - **方法 / 政策 / 数据三维检索**：先用 Read / Grep 在 `asset/计量方法+政策数据库.md`（50 页精简版，**首选入口**）中按"方法（§2–§11）/ 政策（§12）/ 数据（§13）"三个维度交叉定位；
   - **数据集名查询**：用 pandas 在 `asset/macrodatas_list.csv`、`asset/ppmandata_trade_list.csv` 中搜索 `title / keyword / data_intro / data_indicators` 列，返回 top 5 候选；
   - **PDF 兜底**：仅当 md 中的精简描述不足以判断时，才打开 `asset/全网首发计量方法+政策数据库.pdf` 查阅原始 800+ 实证研究的完整页（按 md 第 14 章索引定位到具体 PDF 页码）。
3. **第二轮：查 asset/MCP.docx**。若 asset/ 清单无匹配，查看 `asset/MCP.docx` 中登记的 MCP 服务器能否覆盖该变量（如 CSMAR-MCP 覆盖上市公司基本面 + 治理变量）。确认后按 docx 中的 URL 指引完成 MCP 安装，调用 MCP 工具取数。
4. **第三轮：外部补充**。清单与 MCP 均不覆盖时，提示研究者从 7.1 第 3–9 项其他来源补充。建议清单格式给研究者勾选：
   - "需要我搜索 CSMAR 是否有此变量吗？"
   - "这个政策可能需要手工整理政策文本 + LLM 抽取关键字段，是否继续？"
   - "若 asset/ 与 MCP 都没有该城市面板，可用统计年鉴逐年拼接，请研究者下载后放入 `data/raw/`。"
5. **第四轮：仍无法获取时**，进入 Plan-B（§3.A）：
   - 替换因变量/自变量度量为 asset/ 或 MCP 已覆盖的近似代理
   - 降级研究范围（如公司级 → 行业级、全国 → 长三角/珠三角）
   - 或改用合成 / 二手数据拼接方案

### 7.3 数据来源透明化（强制）

无论数据来自 asset/、MCP 服务器还是外部来源，在 `sample.tex` 与论文 Data 小节**必须标注每个变量的原始出处**（数据库名 + 访问年份 + 是否手工整理）：

- asset/ 清单：写明具体数据集条目 id（如 `macrodatas_list.csv` 第 1776761040 行）
- MCP：写明服务器名与调用工具（如 `CSMAR-MCP / mcp__csmar__get_financials`）与访问日期
- 商业库/外部：写明数据库全称 + 字段表名 + 下载日期

```python
def search_asset(keyword, top=5):
    """三维检索：先扫精简 md，再扫两份 CSV。md hits 用于方法 / 政策 / 数据三维定位；
    CSV hits 用于具体数据集名匹配。"""
    md_path = 'asset/计量方法+政策数据库.md'
    md_lines = open(md_path, encoding='utf-8').read().splitlines()
    md_hits = [(i + 1, ln) for i, ln in enumerate(md_lines) if keyword in ln][:top]
    if md_hits:
        print(f"[md] 在 {md_path} 命中 {len(md_hits)} 行（行号+片段）：")
        for ln_no, ln in md_hits:
            print(f"  L{ln_no}: {ln.strip()[:120]}")

    cols = ['title','data_source','keyword','data_intro','data_indicators','article_url']
    csv_results = []
    for csv in ['asset/macrodatas_list.csv','asset/ppmandata_trade_list.csv']:
        df = pd.read_csv(csv, usecols=cols, encoding='utf-8', errors='ignore')
        hit = df[df.apply(lambda r: keyword in str(r.to_dict()), axis=1)]
        csv_results.append(hit.head(top))
    out = pd.concat(csv_results)
    if len(out) == 0 and not md_hits:
        print(f"[!] asset/ 无匹配 '{keyword}'。建议来源：CSMAR / WIND / 统计年鉴 / 手工整理。")
    return out
```

## 8. 中国公司金融研究的常见坑（必检）

| 陷阱 | 做法 |
|---|---|
| 样本未剔除金融业（证监会行业代码 J） | 默认剔除 |
| 未剔除 ST / *ST / IPO 当年 | 默认剔除 |
| 控制变量极端值 | 连续变量 1% / 99% **缩尾**（winsor），在表注中说明 |
| 行业分类口径 | 优先 CSRC 2012（制造业 2 位代码），在稳健性中替换 SIC |
| 省/市合并问题 | 2011 前巢湖、2020 后区划调整等，需统一合并 |
| 聚类层级 | 基本单位聚类（firm/city），稳健性中替换 province × year 双向聚类 |
| staggered DID | 必配 CS-DID 或 Sun-Abraham 交叉验证，避免 TWFE 负权重 |
| 政策公布 vs 实施 | 区分"公布年""实施年"，在稳健性中替换 |
| 同期政策混淆 | 检索 asset/计量方法+政策数据库.md 第 §12 节"中国政策大全"按主题域排查同期政策；在基准回归中加入同期政策的 dummy 控制 |

## 9. 输出项目目录（运行 skill 时自动建议）

在 CONTRACT 九字段确认后，自动生成如下骨架（所有 Python 脚本预埋 template/ 对照的 `render_*_tex` 调用）：

```
{项目名}/
├── 00_proposal.md                          # 计划书固化版（**顶部 YAML：target_journal / bibliography_style / writing_preferences**；下接 CONTRACT 九字段）
├── DECISION_LOG.md                         # Plan-B 切换记录（3.A.3）
├── data/raw/                               # 研究者放入原始数据
├── data/cleaned/sample.parquet             # 清洗后样本
├── code/
│   ├── 00_config.py                        # 全局变量（样本年份、控制变量列表、FE 配置）
│   ├── 01_clean.py                         # → results/sample.tex（样本构造 Panel A + 样本分布 Panel B）
│   ├── 02_sumstat.py                       # → results/sum_stat.tex + results/variables.tex
│   ├── 03_parallel.py                      # → results/parallel.pdf   [DID 专用]
│   ├── 04_baseline.py                      # → results/baseline.tex
│   ├── 05_iv.py                            # → results/iv.tex
│   ├── 05b_dml.py                          # → results/psm_ddml.tex Panel B
│   ├── 06_measures.py                      # → results/measures.tex
│   ├── 07_channel.py                       # → results/channel{1,2,3}.tex
│   ├── 08_hetero.py                        # → results/heterogeneity{1,2,3}.tex
│   ├── 09_robust.py                        # → results/{addctr,specification,sampling,bunching-did}.tex
│   ├── 10_psm.py                           # → results/psm_ddml.tex Panel A + results/psm-pre-post.pdf
│   ├── 11_placebo.py                       # → results/placebo.pdf   [DID 专用，非 DID 项目不生成此脚本]
│   └── 12_further.py                       # → results/further.tex (+ results/specurve.pdf)
├── results/                                # 最终交付物：.tex 表格 + .pdf/.png 图像 全部放此处
└── main.tex                                # 正文入口，preamble 照抄 template/main.tex；\input{results/xxx.tex}
```

> **main.tex 生成规则**：
>
> 创建项目时从 `template/main.tex` 照抄三类块到 `{项目名}/main.tex`：
> 1. **Preamble**：documentclass / usepackage / 自定义宏 / 页面设置 / `\def\sym{...}`
> 2. **References 块**：参考文献样式（`\bibliographystyle{...}` + `\bibliography{...}` 或 `thebibliography` 环境）。**`\bibliographystyle{}` 不照抄 template，而是按 `00_proposal.md` YAML 中的 `bibliography_style` 填入**（如 JFE → `\bibliographystyle{jfe}`、JCF → `\bibliographystyle{elsarticle-num}`、CER → `\bibliographystyle{elsarticle-num}`、JAR → `\bibliographystyle{jar}`，详见 §3.4.4）。
> 3. **Appendix 块**：`\appendix` 起始指令、附录标题样式、附录表/图的编号重置 `\setcounter{table}{0}\renewcommand{\thetable}{A\arabic{table}}` 等
>
> 此外，**Section 骨架（`\section{...}` 命名与顺序）按 `00_proposal.md` YAML 中的 `section_skeleton` 字段渲染**（不同期刊骨架不同，见 §3.4.4），不再机械照抄下文的"Introduction / Literature Review / Research Design / Empirical Results / Conclusion"五段式。
>
> **main.tex 整体结构（严格按此顺序）**：
>
> ```latex
> <Preamble>                                 % 来自 template/main.tex
> \begin{document}
> \maketitle
> \begin{abstract}\end{abstract}              % 摘要 body 留空
>
> % ★ 以下 \section / \subsection 顺序与命名按 §3.4.4 的 section_skeleton 替换；
> %   每个 \section / \subsection 下 body 一律留空（不写 prose）。
> %   这是默认 JFE-style 骨架，其他期刊（JAR / JF / MS / CER…）按 §3.4.4 替换。
>
> \section{Introduction}
>
> \section{Background and Hypothesis Development}
> \subsection{China's Institutional Setting}
> \subsection{Hypothesis Development}
>
> \section{Data and Sample}
> \subsection{Sample Construction}
> \subsection{Variable Definitions}
> \subsection{Summary Statistics}
>
> \section{Empirical Strategy}
> \subsection{Baseline Specification}
> \subsection{Identification Strategy}                 % 含 IV / DID / RDD / DML 等
>
> \section{Empirical Results}
> \subsection{Baseline Results}
> \subsection{Parallel Trends and Dynamic Effects}     % ★ 仅 DID 项目保留；非 DID 删除
> \subsection{Endogeneity Concerns}                    % IV / DML / Heckman
> \subsection{Mechanism Analysis}
> \subsection{Heterogeneity Analysis}
> \subsection{Further Analysis}
>
> \section{Robustness Checks}                          % 正文只点题；完整稳健性表放附录
> \subsection{Alternative Measures}
> \subsection{Alternative Specifications}
> \subsection{Subsample Analyses}
> \subsection{Placebo Tests}                           % ★ 仅 DID 项目保留；非 DID 删除
>
> \section{Conclusion}
>
> %—— References（照抄 template/main.tex 的参考文献块格式）——
> \bibliographystyle{...}
> \bibliography{references}
>
> %================================================================
> %  正文图（Main-text Figures：图在前）
> %================================================================
> \clearpage
> \begin{figure}[htbp]\centering
>   \includegraphics[width=0.9\textwidth]{results/parallel.pdf}
>   \caption{Parallel Trends}\label{fig:parallel}
> \end{figure}
> % 正文图依次（★ 仅 DID 项目）：parallel / csdid-figure / estimator / placebo
> % 非 DID 项目：本节不出现 parallel / csdid-figure / estimator / placebo，仅保留 §4 主线第 12 步可选图
>
> %================================================================
> %  正文表（Main-text Tables：表在后；内生性紧跟 baseline）
> %================================================================
> \clearpage
> \input{results/sum_stat.tex}           % 描述性统计
> \input{results/baseline.tex}           % 基准回归（定海神针）
> \input{results/iv.tex}                 % ★ 内生性 —— 紧跟 baseline
> \input{results/heterogeneity1.tex}     % 异质性 1（异质性 先于 机制）
> \input{results/heterogeneity2.tex}     % 异质性 2
> \input{results/heterogeneity3.tex}     % 异质性 3
> \input{results/channel1.tex}           % 机制 1
> \input{results/channel2.tex}           % 机制 2
> \input{results/channel3.tex}           % 机制 3
> \input{results/further.tex}            % 进一步分析
>
> %================================================================
> %  Appendix（附录；稳健性表格 + 附加图；格式照抄 template/main.tex）
> %================================================================
> \appendix
> \section{Robustness Checks}
>
> %—— 附录图 ——
> \begin{figure}[htbp]\centering
>   \includegraphics[width=0.9\textwidth]{results/psm-pre-post.pdf}
>   \caption{PSM Balance: Pre vs. Post}\label{fig:psm-balance}
> \end{figure}
> \begin{figure}[htbp]\centering
>   \includegraphics[width=0.9\textwidth]{results/specurve.pdf}
>   \caption{Specification Curve}\label{fig:specurve}
> \end{figure}
>
> %—— 附录表（变量定义 + 样本构造 + 稳健性）——
> \input{results/variables.tex}          % ★ 变量定义表（附录首张）
> \input{results/sample.tex}             % ★ 样本构造与分布（Panel A 构造 / Panel B 分布）
> \input{results/measures.tex}           % 替换因变量度量
> \input{results/addctr.tex}             % 附加控制变量
> \input{results/specification.tex}      % 高维交互 FE
> \input{results/sampling.tex}           % 样本筛选稳健性
> \input{results/bunching-did.tex}       % Bunching-DID 稳健
> \input{results/psm_ddml.tex}           % PSM + DML（Panel A / Panel B）
>
> \end{document}
> ```
>
> **强制规则**：
>
> 1. **正文章节（Introduction ~ Conclusion）不嵌入实物表图**，只用 `\ref{tab:baseline}` / `\ref{fig:parallel}` 引用。
> 2. References **之后**依次放：**正文 Figures → 正文 Tables → Appendix**。
> 3. **正文 Figures 在前，正文 Tables 在后**（顺序不可颠倒）。
> 4. **正文表排列顺序**（固定）：
>    ```
>    sum_stat → baseline → iv（内生性）
>      → heterogeneity1/2/3 → channel1/2/3 → further
>    ```
>    **内生性表（iv.tex）紧跟在 baseline.tex 之后**；如有多张内生性表（如额外的 IV / 自然实验），也放在 baseline 与 heterogeneity 之间连续排列。**异质性在机制之前**。
> 5. **附录表排列顺序**（固定）：
>    ```
>    variables（变量定义） → sample（样本构造与分布）
>      → measures → addctr → specification → sampling → bunching-did → psm_ddml
>    ```
>    附录首张为 `variables.tex`（变量定义），紧随其后为 `sample.tex`（样本构造 Panel A + 样本分布 Panel B），然后是全部稳健性检验表。
> 6. **附录图**（如 `psm-pre-post.pdf`、`specurve.pdf`）与附录表一同放在 `\appendix` 之后；正文图只保留 `parallel / csdid-figure / estimator / placebo` 这类支撑主结论的图（**这四张图仅 DID 项目出现，非 DID 项目正文区不放图**）。
> 7. 附录编号格式（Table A1 / Figure A1）由 `template/main.tex` 附录块中定义的 `\setcounter` + `\renewcommand{\thetable}{A\arabic{table}}` 等宏控制，**严格照抄不自行发明**。
> 8. References 块格式同样**严格照抄 `template/main.tex`**。
> 9. **不建 `paper/` 子目录**；所有 `\input` / `\includegraphics` 路径以 `results/xxx` 开头（相对于 main.tex 所在目录）。
> 10. **正文 body 一律留空**：`main.tex` 正文章节区只填写 `\section{...}` 与 `\subsection{...}` 标题（按 §3.4.4 `section_skeleton` 调整命名），**每个 \section / \subsection 之下不写任何 prose**——正文 prose 由研究者后续撰写。`\begin{abstract}\end{abstract}` 同样留空。
> 11. **不为任何章节单独建 .tex 文件**：所有 `\section` / `\subsection` 标题直接写在 `main.tex` 内，**禁止**创建 `introduction.tex` / `data.tex` / `results.tex` / `conclusion.tex` 等"章节体"分文件。`\input{}` 只用于 `results/*.tex`（表格）。
> 12. **安慰剂相关章节 / 图 / 表条件性出现**：`\subsection{Placebo Tests}`、`results/placebo.pdf`、`\subsection{Parallel Trends and Dynamic Effects}`、`results/parallel.pdf` / `csdid-figure.pdf` / `estimator.pdf` 这五项**仅 DID / Staggered DID / PSM-DID 项目出现**；纯 Panel FE+IV / RDD / DML / 合成控制项目从 main.tex 中删除上述章节/图引用。

**最终交付物（仅两类）**：

1. **Python 代码**：`code/` 目录下全部 `.py` 脚本，可从原始数据一键跑通到所有表图。
2. **图表**：`results/` 下的 `.tex`（LaTeX 表格，符合 template/ 格式）+ `.pdf` 与 `.png`（双份导出的图像）。**表格与图像统一放入 `results/`，不再单独建 `figures/` 目录**。

另外附带 `{项目名}/main.tex`（preamble 照抄 `template/main.tex`，正文依次 `\input{results/xxx.tex}` 并 `\includegraphics{results/xxx.pdf}`），与 `code/` 并列放在项目根，不嵌入 `paper/` 子目录。

不交付 Word / Markdown 报告；不交付 Stata `.do` 文件；不交付中间数据集。

## 10. AI 在本 skill 下的行为准则

1. **计划书驱动**：无 proposal 不启动；proposal 即契约。执行中遇到任何判断岔路，先回查 `00_proposal.md`。
1.5. **🆕 启动后第二步是目标期刊推荐（§3.4），不可跳过、不可代选**：CONTRACT 九字段补齐后，必须按 §3.4.3 输出格式呈现 [J1]–[J5] 5 本英文目标期刊（含 4 维星级 + Why it fits + Editorial preference + bib style），**显式停下询问研究者**；在收到选择前不进入项目骨架生成。研究者选定后立即将 `target_journal` / `bibliography_style` / `writing_preferences` YAML 块写入 `00_proposal.md` 顶部，后续 `render_main_tex()` 与各 `render_*_tex()` 均以此为准。
2. **自主闭环，不卡壳**：结果不达预期时，按第 3.A 节 Plan-B 决策树**自行切换并继续执行**，不停下等研究者拍板。切换即记录 `DECISION_LOG.md`。
3. **小步快跑**：一次只完成研究链条中的一个环节；完成后展示 .tex 摘要（前 10 行 + 后 10 行）与 proposal 预期的对比（✅/⚠️/❌），再进入下一环节。
4. **格式一致性检查**：每次写 .tex 前，先 Read 对应 `template/*.tex`，比对列数、列头、FE 行、Notes 段，再渲染。
5. **不擅自改规则**：`rule/` 中的规则是强制的；若研究者要求偏离，需要研究者明确书面说明（例如"审稿人要求改报告标准误"）。
6. **不跑 Stata**：所有回归、PSM、DML、CS-DID、bdiff 均用 Python 实现。`rule/` 中的 Stata 代码只作为"输出格式参照"。
7. **保护工作目录**：`asset/ rule/ template/` 三个文件夹只读，不写入、不修改、不重命名。所有研究输出只放入 `{项目名}/` 子目录。
8. **生成表后自检**：逐项核对 `rule/回归表写作规范总结.docx` 第九部分的"AI 写作检查清单"（三线表、控制变量全展示、t 值括号、`\sym{}` 星号、FE 行、聚类层级、表注完整）。
9. **只交付代码与图表**：最终产物限定为 `code/*.py` + `results/*.tex` + `results/*.pdf|png`（表与图同在 `results/`）；不产出额外报告、摘要、PPT、Word。
10. **中英文规范**：变量名、表题、列头、FE 行用英文；表注（`\noindent{\justifying{...}}`）用英文；中英混排中英之间空一格、中文标点用全角。
11. **🆕 安慰剂仅 DID 时做**：当 `00_proposal.md` 第 (4) 条识别策略为 **DID / Staggered DID / PSM-DID** 时执行 §4 第 11 步安慰剂检验（`11_placebo.py` + `results/placebo.pdf` + `\subsection{Placebo Tests}` + 正文 placebo 图引用）；当识别策略为 **Panel FE+IV / RDD / DML / 合成控制** 时**整体跳过**安慰剂——`code/` 不生成 `11_placebo.py`，`results/` 不出现 `placebo.pdf`，`main.tex` 中不出现 `\subsection{Placebo Tests}` 与对应 figure 块。平行趋势 / CS-DID / estimator 三图同样仅 DID 项目出现。
12. **🆕 main.tex 正文只写标题，body 留空**：`\section{...}` 与 `\subsection{...}` 命名按目标期刊 `section_skeleton` 填齐，下面**不写任何 prose**（一行空行即可）；`\begin{abstract}\end{abstract}` 也留空。研究者后续自行撰写正文。skill 完成后展示 `main.tex` 行数应与 §9 模板示例相当（章节标题层级 + `\input{results/*}` + figure 块，**无段落 prose**）。
13. **🆕 不为章节单独建 .tex 文件**：禁止生成 `introduction.tex` / `background.tex` / `data.tex` / `methodology.tex` / `results.tex` / `conclusion.tex` 之类的 section-body 分文件。所有正文 Section / Subsection 标题**直接写在 `main.tex` 内**；`\input{...}` 仅用于 `results/*.tex`（表格）。

## 11. 启动示例

### 最小计划书（文本形式）

> **研究计划书**
> 题目：数字经济与企业融资约束
> 假设：城市数字经济发展 (X = DigiEcon) 降低本地企业融资约束 (Y = SA/KZ index)
> 预期：X 对 Y 的系数显著为负（p<0.05），渠道为"信息不对称下降 + 信贷可得性上升"，
>       异质性上非国企、中小企业效应更强
> 识别：Panel FE + IV（IV: 光缆端口历史存量 × 时间 / Broadband China 试点）
> 样本：A 股非金融上市公司，2011–2023
> 数据：优先在 asset/ 检索"数字经济指数""宽带中国""融资约束"；asset/ 未覆盖的（如
>       SA/KZ 指数、公司基本面）先看 asset/MCP.docx 的 CSMAR-MCP 能否直取；
>       仍未覆盖的（如光缆端口历史存量）从统计年鉴 / 手工整理补充
> 机制：M1 = 信息不对称（分析师关注/盈余同步性）；M2 = 信贷可得（新增长贷/短贷比）
> 异质性：产权性质（SOE/非 SOE）；规模（大/中/小）；地区（东/中/西）

提交后 skill 立即：

1. 解析 CONTRACT 九字段；若有缺项，一次性追问补齐
2. **🆕 推荐 5 个最合适的英文目标期刊**（如本例宽带中国 IV → JFE / MS / JCF / RFS / China Economic Review），按 §3.4.3 格式呈现 [J1]–[J5]（含 4 维星级 + Why it fits + bib style），**停下询问研究者**
3. 研究者选定（例如 JFE）→ 生成 `数字经济_融资约束/00_proposal.md`（CONTRACT 九字段 + 顶部 `target_journal: JFE` YAML 块）
4. 按 §3.4.4 把目标期刊的 `\bibliographystyle{jfe}` 与 Section 骨架写入 `{项目名}/main.tex`
5. 搜索 asset/ 返回候选数据集，等研究者选定
6. 按第 4 节主线执行；若基准 X 系数方向反向，自动进入 3.A.2【基准回归】Plan-B B1→B7
7. 最终交付：`code/` 全套 Python + `results/*.tex` 全套表 + `results/*.pdf|png` 全套图（表与图同在 `results/`）+ `DECISION_LOG.md` 追溯记录
