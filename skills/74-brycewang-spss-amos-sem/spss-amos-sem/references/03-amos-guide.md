# AMOS 操作与读输出

每次运行生成的 `amos/AMOS操作步骤.md` 是针对用户模型的具体清单（变量名、误差项名、参数标签、预期数值都已填好）。本文件讲通用规则和排错。

## 两条路线

| 路线 | 适合 | 说明 |
|---|---|---|
| **Amos Graphics 画图**（主路线） | 所有用户 | 论文里的 AMOS 截图都来自这里；答辩老师也最熟悉 |
| **Program Editor 跑 VB.NET 程序** | 不想手画、模型很大 | `01_CFA_VB程序.vb` / `02_SEM_VB程序.vb`。新建 VB 程序，把模板里 `'Your code goes here` 那一行替换成文件里 `Dim ... End Try` 的内容。语法依据 IBM SPSS Amos 28 User's Guide（`y <--- F (1)` 固定路径、`(标签)` 命名参数、`a <> b` 协方差、`Sem.Bootstrap(n)`），**未在真实 AMOS 里跑过**，报错就改用画图 |

注意一个差别：**Amos 程序（VB）里，除误差项之外的外生变量默认相关；Amos Graphics 里不会自动相关**，要手动画双箭头。CFA 时所有构念两两画双箭头；结构模型时只在外生构念之间画。

## 画图要点

1. File → Data Files 选清洗后的 `_cleaned.sav`。
2. 潜变量（椭圆）名字用构念代码，**不能和数据里的任何变量重名**，否则 AMOS 会说该变量是观测变量却画成了椭圆。
3. 每个潜变量第一条载荷固定为 1（画指标工具自动做），每个误差项到指标的路径固定为 1。
4. 内生潜变量要有残差项（Add a unique variable）。
5. 路径命名：右键箭头 → Object Properties → Parameters → Regression weight，填 `P1`、`P2`……（与 `AMOS操作步骤.md` 的表一致，自定义估计量要用）。
6. View → Analysis Properties：
   - Output：Standardized estimates、Squared multiple correlations、Modification indices（Threshold 4）、Indirect, direct & total effects；
   - Bootstrap：Perform bootstrap，2000 次；Bias-corrected confidence intervals，95。
7. SRMR：Plugins → Standardized RMR，先打开这个窗口，再 Calculate Estimates。

## 读输出（View → Text Output）

| 要找的数 | 位置 |
|---|---|
| 非标准化载荷 / 路径、S.E.、C.R.、P | Estimates → Scalars → Regression Weights |
| 标准化载荷 / 路径 β | Estimates → Scalars → Standardized Regression Weights |
| R²（SMC） | Estimates → Scalars → Squared Multiple Correlations |
| 构念间相关 | Estimates → Scalars → Correlations |
| χ²、df、χ²/df | Model Fit → CMIN（CMIN、DF、CMIN/DF） |
| GFI、AGFI | Model Fit → RMR, GFI |
| NFI、IFI、TLI、CFI | Model Fit → Baseline Comparisons |
| RMSEA | Model Fit → RMSEA |
| 修正指数 | Modification Indices → Covariances / Regression Weights |
| 总间接效应及其 bootstrap CI | Estimates → Matrices → (Standardized) Indirect Effects，再点左下角 Bootstrap Confidence → Bias-corrected percentile method |
| 具体间接效应 | Estimates → Scalars → User-defined estimands（Bootstrap Confidence 里看区间） |

P 列的 `***` 表示 p < 0.001，不是"三颗星显著"的意思，报告时写 p < 0.001。

## 具体间接效应（自定义估计量）

AMOS 自带的 Indirect Effects 只给"X 到 Y 所有间接路径之和"。有多条中介路径（并行或链式）时，每条路径要用自定义估计量单独检验（IBM Amos User's Guide, Example 38）：

1. 左下角状态栏点 **Not estimating any user-defined estimand** → **Define new estimands**；
2. 每行一个：`H8 = p.P2 * p.P5`（`p.` 表示参数标签，名字只能用字母、数字、下划线，字母开头）；
3. Check Syntax → 关闭 → 保存；
4. 确认 Bootstrap 已勾选，Calculate Estimates。

## 多群组分析

Analyze → Manage Groups 建组 → Data Files 里每组选同一文件、设 Grouping Variable 和 Group Value → **Multiple-Group Analysis** 按钮自动生成嵌套模型（Measurement weights = 弱等价，Measurement intercepts = 强等价，Structural weights = 路径相等）。比较 ΔCFI（≤ 0.01）。路径差异：Output 勾选 Critical ratios for differences，两组同一路径用不同标签，看两标签差的 C.R.（|C.R.| > 1.96）。

## 常见报错

| 报错 / 现象 | 原因与解决 |
|---|---|
| The model is probably unidentified | 某个潜变量没有固定一条载荷为 1，或误差项路径没固定为 1；或某构念只有 1–2 个指标又没有其他约束 |
| ... is an observed variable in the data file but is represented by an ellipse | 潜变量名和数据里的变量重名，改潜变量名 |
| ... is unobserved and has no name | 误差项没命名：Plugins → Name Unobserved Variables |
| In order to analyze data with missing observations ... estimate means and intercepts | 数据有缺失。用清洗后的 `_cleaned.sav`（已列表删除），或勾选 Estimate means and intercepts（此时不能做 bootstrap） |
| Bootstrap 被禁用 | 数据有缺失或勾了 means and intercepts；bootstrap 需要完整数据 |
| 标准化载荷 > 1 或误差方差为负（Heywood case） | 样本太小、某构念只有 2 题、模型设定错误；检查题项归属，不要强行把方差固定成正数了事 |
| AMOS 结果和 R 差一点 | 见 08-lavaan-amos-parity.md |
