---
name: spss-amos-sem
description: Questionnaire structural equation modeling in the SPSS + AMOS workflow that Chinese management, psychology, education, nursing and tourism theses use — data cleaning of an SPSS .sav file, reverse coding, straight-lining, demographics, Harman common-method-bias test, Cronbach's alpha / CITC reliability, EFA (KMO, Bartlett), CFA convergent validity (standardized loadings, CR, AVE), discriminant validity (Fornell-Larcker, HTMT), model fit (chi2/df, CFI, TLI, RMSEA, SRMR), structural paths and hypothesis tests, bootstrap mediation with specific indirect effects, multi-group measurement invariance, and Hayes PROCESS models 1/4/6/7/8/14. One spec card drives an R/lavaan engine set to AMOS defaults and writes ready-to-run SPSS syntax (.sps), AMOS Program Editor VB.NET code, AMOS user-defined estimands, an AMOS drawing checklist with the numbers AMOS should show, Chinese three-line tables in Word, a results-chapter draft and a transparent model-modification log. Use when the user mentions SPSS, AMOS, SEM, structural equation model, CFA, confirmatory factor analysis, questionnaire / survey / Likert scale data, reliability and validity, CR / AVE, HTMT, common method bias, mediation, moderation, PROCESS, bootstrap indirect effect, multi-group analysis, measurement invariance, or Chinese terms 结构方程, 结构方程模型, 验证性因子分析, 探索性因子分析, 问卷, 量表, 信度, 效度, 收敛效度, 区分效度, 组合信度, 共同方法偏差, 中介效应, 调节效应, 有调节的中介, 多群组, 测量不变性, 模型拟合, 修正指数, 毕业论文问卷分析.
license: CC-BY-SA-4.0
---

# 问卷数据结构方程全流程（SPSS + AMOS）

一张**设定卡**（YAML）驱动整条流程：R/lavaan 按 AMOS 的默认设置把所有数字算出来，同时生成用户可以在 SPSS / AMOS 里原样复现的语法和操作步骤，再把结果排成中文论文的三线表和结果段落。

```
.sav 数据 ──► draft_spec.R ──► 设定卡 spec.yml ──► run_sem.R ──► 输出文件夹
                                   ▲                                │
                                   └──── 模型修正（写理由）◄─────────┘
```

## 先说清楚能做什么、不能做什么

| 能做 | 不能做 / 要说明 |
|---|---|
| 用 lavaan 复算 AMOS 的 ML 估计（第一载荷固定为 1、χ² = (N−1)F、偏差校正 bootstrap），数字和 AMOS 一致到小数点后两三位 | **不能运行 SPSS 或 AMOS 本身**。生成的 `.sps` 和 AMOS 步骤要用户自己在装了软件的电脑上跑 |
| 生成 SPSS 语法：清洗、描述统计、Harman、信度、EFA、相关、VIF、PROCESS | AMOS 的 VB.NET 程序按 IBM Amos 28 用户手册的语法生成，**未在真实 AMOS 里跑过**；主路线是 Amos Graphics 画图清单 |
| PROCESS 模型 1/4/6/7/8/14（OLS + 百分位 bootstrap，与宏的算法一致） | 不做 PLS-SEM（SmartPLS）、潜变量交互（LMS）、贝叶斯 SEM、纵向 / 多层 SEM |
| 中文三线表（Word）、结果段落初稿、路径图、模型修正记录 | 理论模型（构念、路径、假设）由用户的研究设计决定，不由数据倒推 |

## 硬规则（每次都要遵守）

1. **数字只能来自本次运行的 `results.json` / `results.xlsx`。** 不要凭印象写 AMOS 输出，不要编造任何一个系数、拟合值或置信区间。用户贴来 SPSS / AMOS 原始输出时，以那份输出为准，并用 [references/08-lavaan-amos-parity.md](references/08-lavaan-amos-parity.md) 解释差异。
2. **模型修正只通过设定卡的 `modifications`，每条必须写理由。** 引擎会自动核对理由和数据（被删题项在上一步模型里的载荷、误差相关的 MI 和排名），不符时在 `模型修正记录.md` 里打 ⚠。不要替用户删题、加误差相关来"凑"拟合；跨构念误差相关和交叉载荷不建议采纳。规则细节见 [references/05-fit-and-modification.md](references/05-fit-and-modification.md)。
3. **未达标就如实写未达标。** 结果段落里的「未达标」「不成立」「不显著」是真实结果，不改写成达标；可以帮用户解释原因、给出改进方向或局限性写法。
4. **只引用 [references/citations.md](references/citations.md) 里的文献**作为阈值出处。需要别的文献时告诉用户自己查证，不要编。
5. `--quick` 只用来检查设定卡和数据（bootstrap 只有 200 次），**交付前一定用正式模式重跑**。
6. 告诉用户 AMOS 的 **C.R. 是 z 值（临界比），不是组合信度 CR**——这是问卷论文里最常见的错误之一。

## 工作流程

### 0. 环境

需要 R ≥ 4.1 和这些包（第一次用时安装）：

```r
install.packages(c("yaml", "lavaan", "semTools", "psych", "GPArotation", "haven", "openxlsx",
                   "officer", "flextable", "jsonlite", "readxl", "ragg"))
```

`ragg` 是可选的（画路径图更清晰）；读 `.xlsx` 需要 `openxlsx`，读 `.xls` 需要 `readxl`。

### 1. 看数据，起草设定卡

```bash
Rscript scripts/draft_spec.R 用户数据.sav --out spec.yml
```

脚本会打印变量总览（名称、SPSS 标签、取值范围、缺失），按变量名前缀把题项分组（PU1 PU2… → PU），找出与同组负相关的疑似反向题，写一份带 TODO 的设定卡草稿。

### 2. 和用户确认设定卡

只问数据里看不出来的东西，一次问完：

- 每个构念的**中文名**和题项归属（草稿按前缀分组，常常要改）；
- **结构路径和研究假设**（来自用户的理论模型 / 开题报告，不要自己编）；
- 反向题是否属实（对照问卷原文）；
- 要不要检验具体中介路径、多群组、PROCESS 调节模型。

字段说明见 [assets/templates/spec_template.yml](assets/templates/spec_template.yml)，完整示例见 [assets/demo/spec_demo.yml](assets/demo/spec_demo.yml)。构念代码 ≤ 6 个字母（PROCESS 宏要求变量名不超过 8 个字符，生成的均值变量叫 `m_代码`）。

### 3. 快速试跑

```bash
Rscript scripts/run_sem.R spec.yml --out 输出文件夹 --quick
```

读 `results.json` 和 `模型修正记录.md`，向用户汇报：样本清洗结果、信度、EFA 是否有归错维度或交叉载荷的题、CFA 载荷 < 0.5 的题、拟合指标、区分效度。

### 4. 决定是否修正模型

按 [references/05-fit-and-modification.md](references/05-fit-and-modification.md) 的顺序：先看低载荷题项（< 0.5，且题干确实有问题才删；每个构念至少保留 3 题），再看**同一构念内**、题干相似的误差相关。每条修正都要用户同意并写进 `modifications`（带理由），然后重跑。

### 5. 正式运行并交付

```bash
Rscript scripts/run_sem.R spec.yml --out 输出文件夹
```

在 demo 数据上，SEM bootstrap 2000 次加 PROCESS 5000 次大约 15 秒。交付时按下表告诉用户每个文件怎么用：

| 文件 | 用途 |
|---|---|
| `结果表格.docx` | 中文三线表（宋体 + Times New Roman，五号），直接贴进论文第四章 |
| `结果段落.md` | 结果部分初稿，数字全部来自本次运行；用户按学校格式改措辞 |
| `路径图.png` | 结构模型标准化路径图（300 dpi），实线显著、虚线不显著 |
| `模型修正记录.md` | 每一步修正的内容、理由、数据依据和拟合变化，答辩被问时用 |
| `analysis.sps` | SPSS 语法：改第一行文件夹路径后全选运行，输出同时导出为 `spss_output_tables.xlsx` |
| `<数据名>_cleaned.sav` | 清洗后的数据（反向计分、剔除无效问卷、加了 `m_` 均值变量），AMOS 直接读 |
| `amos/AMOS操作步骤.md` | Amos Graphics 画图与设置清单，附每个 AMOS 表格的**预期数值** |
| `amos/01_CFA_VB程序.vb`、`02_SEM_VB程序.vb` | AMOS Program Editor 程序（不用手画；未实测，报错时以画图为准） |
| `amos/03_自定义估计量.txt` | 具体间接效应的 estimands，粘贴到 AMOS 的 Define new estimands |
| `results.xlsx` / `results.json` | 全部中间结果；json 供 Claude 读取和核对 |
| `lavaan_model.txt` | 与 AMOS 设定一致的 lavaan 模型语法 |

### 6. 用户带回 SPSS / AMOS 输出时

- SPSS：读 `spss_output_tables.xlsx`（OMS 导出），逐项对照 `results.xlsx`。α、KMO、载荷、相关系数应**完全一致**；不一致通常是反向题、缺失值处理或题项归属不同。
- AMOS：对照 `AMOS操作步骤.md` 里的预期值。点估计和拟合指标应一致到小数点后两位左右；bootstrap 置信区间因随机数不同会有第三位小数的差异，但显著性判断应一致。差异来源见 [references/08-lavaan-amos-parity.md](references/08-lavaan-amos-parity.md)。

## 设定卡速查

| 字段 | 必填 | 说明 |
|---|---|---|
| `data` | ✓ | 数据文件，相对设定卡的路径；`.sav/.zsav/.dta/.csv/.xlsx/.xls` |
| `constructs` | ✓ | `代码: {label: 中文名, items: [题项...]}`，代码 ≤ 6 个字母 |
| `structural` | | `因变量: [自变量...]`，只支持递归（无环）模型；不写就只做测量模型 |
| `hypotheses` | | `H1: X -> Y`，必须对应一条结构路径；不写就自动编号 |
| `indirect` | | `H8: X -> M -> Y`（可多级），偏差校正 bootstrap 检验 |
| `reverse_items` / `scale_points` | | 反向题与李克特点数（反向 = 点数 + 1 − 原值） |
| `missing` | | `listwise`（默认，AMOS 要求完整数据）或 `fiml` |
| `drop_straightliners` | | 剔除所有题目同一答案的问卷（在反向计分**之前**判断） |
| `demographics` / `controls` | | 人口统计变量；控制变量（数值型）指向所有内生构念 |
| `multigroup` | | 2 组分组变量：测量不变性 + 路径组间差异 |
| `process` | | `{model: 4, x: X, m: [M], y: Y, w: W, covariates: [...], center: true}` |
| `modifications` | | `{type: drop_item, item: X, reason: ...}` 或 `{type: error_cov, items: [A, B], reason: ...}` |
| `bootstrap` / `process_bootstrap` / `seed` | | 默认 2000 / 5000 / 20261027 |

## 判断标准速查

| 指标 | 标准 | 出处 |
|---|---|---|
| Cronbach's α | > 0.7 | Nunnally (1978) |
| CITC | > 0.5（常用经验值） | — |
| KMO / Bartlett | KMO > 0.7，Bartlett 显著 | Kaiser (1974) |
| Harman 第一因子 | < 40% | Podsakoff et al. (2003)；周浩、龙立荣 (2004) |
| 标准化载荷 | > 0.5（理想 > 0.7） | Hair et al. (2019) |
| CR / AVE | CR > 0.7，AVE > 0.5 | Fornell & Larcker (1981) |
| 区分效度 | √AVE > 相关系数；HTMT < 0.85（宽松 0.90） | Fornell & Larcker (1981)；Henseler et al. (2015) |
| 拟合 | χ²/df < 3；CFI、TLI ≥ 0.95（> 0.90 可接受）；RMSEA ≤ 0.06（< 0.08 可接受）；SRMR < 0.08 | Hu & Bentler (1999)；Browne & Cudeck (1993) |
| 中介 | bootstrap 95% CI 不含 0；类型按 Zhao et al. (2010) | Preacher & Hayes (2008) |
| 测量不变性 | ΔCFI ≤ 0.01，ΔRMSEA ≤ 0.015 | Cheung & Rensvold (2002)；Chen (2007) |

## 参考文档（按需读取）

- [references/01-workflow-and-chapters.md](references/01-workflow-and-chapters.md)：问卷论文第四章的标准结构，每一节报告什么
- [references/02-spss-syntax.md](references/02-spss-syntax.md)：生成的 SPSS 语法逐段说明、怎么读输出、常见报错
- [references/03-amos-guide.md](references/03-amos-guide.md)：AMOS 画图、设置、读输出、自定义估计量、多群组、常见报错
- [references/04-reliability-validity.md](references/04-reliability-validity.md)：α、CITC、CR、AVE、FL、HTMT 的公式，不达标怎么办
- [references/05-fit-and-modification.md](references/05-fit-and-modification.md)：拟合指标含义与模型修正规则
- [references/06-mediation-moderation.md](references/06-mediation-moderation.md)：SEM 中介、PROCESS 各模型、选哪个
- [references/07-reporting.md](references/07-reporting.md)：中文写作模板、表格规范、答辩常见问题
- [references/08-lavaan-amos-parity.md](references/08-lavaan-amos-parity.md)：lavaan 与 AMOS / SPSS 的设置对应与数值差异
- [references/citations.md](references/citations.md)：全部判断标准的文献出处

## 演示与自检

- `assets/demo/questionnaire_demo.sav`：模拟的移动支付 App 问卷（430 份，5 个构念，18 题），生成模型已知，并且故意埋了反向题、低载荷题、误差相关、SPSS 缺失代码 9、缺答和规律作答。生成脚本是 `scripts/make_demo_data.R`。
- `assets/demo/example_output/`：用 demo 设定卡正式运行的完整输出，可以先给用户看效果。
- `Rscript tests/test_demo.R`：端到端自检，共 48 项检查：α / KMO 与 psych 对照，PROCESS 与 `lm()` 对照，χ² 的 N−1 规则，能否恢复生成模型，生成的 SPSS / AMOS 文件结构是否正确，设定卡校验，以及 PROCESS 模型 1/6/14、观测调节变量、FIML 的第二套设定。
