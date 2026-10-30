# AMOS 操作步骤：移动支付 App 持续使用意愿研究

> 由 spss-amos-sem 按你的设定卡生成。照着做完，AMOS 输出里的数字应该和下面「预期结果」一致到小数点后两位左右
> （lavaan 已按 AMOS 的默认设置复算：ML 估计、每个构念第一条载荷固定为 1、卡方 = (N−1)×F）。

## 0. 准备

1. 先在 SPSS 里跑完 `analysis.sps`，得到清洗后的数据 `questionnaire_demo_cleaned.sav`（或直接用本文件夹上一级的同名文件，R 已经生成好了）。
2. 打开 Amos Graphics → File → Data Files → File Name，选这个 .sav 文件 → OK。
3. 数据里不能有缺失值（列表删除已在清洗步骤完成）；否则 AMOS 会要求勾选 Estimate means and intercepts。

## 1. 画测量模型（CFA）

用 **Draw a latent variable or add an indicator** 工具（带三个小方框的椭圆图标）：画一个椭圆，在里面点几下就加几个指标。

| 构念（椭圆里写的变量名） | 中文名 | 指标（方框，从 List variables in data set 拖进来） | 误差项（小圆） |
|---|---|---|---|
| `PEOU` | 感知易用性 | `PEOU1`、`PEOU2`、`PEOU3`、`PEOU4` | `e1`、`e2`、`e3`、`e4` |
| `PU` | 感知有用性 | `PU1`、`PU2`、`PU3`、`PU4` | `e5`、`e6`、`e7`、`e8` |
| `TR` | 信任 | `TR1`、`TR2`、`TR3` | `e9`、`e10`、`e11` |
| `SAT` | 满意度 | `SAT1`、`SAT2`、`SAT3` | `e12`、`e13`、`e14` |
| `CI` | 持续使用意愿 | `CI1`、`CI2`、`CI3` | `e15`、`e16`、`e17` |

- 每个构念的**第一条**载荷会被 AMOS 自动固定为 1，保持默认即可。
- 误差项命名：Plugins → **Name Unobserved Variables** 会自动命名为 e1、e2……，为了和本文件对上，建议右键误差项 → Object Properties 手动改成上表的名字。
- 椭圆的变量名必须和数据里的任何变量都不同（所以构念用代码，不要和题项同名）。
- **模型修正**：用双箭头工具画以下误差相关（理由见 `模型修正记录.md`）：
  - `e12` ↔ `e13`（SAT1 与 SAT2 的误差）
- **CFA 模型里所有构念两两之间都要画双箭头（协方差）**。Amos Graphics 不会自动让它们相关（这一点和 VB 程序不同）。

## 2. 分析设置（View → Analysis Properties）

- Estimation：Maximum likelihood（默认）。
- Output：勾选 **Standardized estimates**、**Squared multiple correlations**、**Modification indices**（Threshold 保持 4）、**Indirect, direct & total effects**。
- Bootstrap（做结构模型时）：勾选 **Perform bootstrap**，Number of bootstrap samples = **2000**；勾选 **Bias-corrected confidence intervals**，BC confidence level = **95**。
- SRMR：AMOS 默认不报。Plugins → **Standardized RMR**，先把这个小窗口打开放着，再点 Calculate Estimates，它才会显示。

### CFA 的预期结果

| 指标 | AMOS 里的位置 | 预期值 |
|---|---|---|
| χ² (CMIN) | Model Fit → CMIN | 156.687 |
| df | Model Fit → CMIN → DF | 108 |
| χ²/df (CMIN/DF) | Model Fit → CMIN | 1.451 |
| GFI / AGFI | Model Fit → RMR, GFI | 0.957 / 0.939 |
| NFI / IFI / TLI / CFI | Model Fit → Baseline Comparisons | 0.951 / 0.984 / 0.980 / 0.984 |
| RMSEA | Model Fit → RMSEA | 0.033 |
| SRMR | Standardized RMR 插件窗口 | 0.036 |

标准化载荷（Estimates → Scalars → Standardized Regression Weights）：

| 题项 | 构念 | 标准化载荷 | C.R.（即 z 值） |
|---|---|---|---|
| PEOU1 | PEOU | 0.678 | 固定为 1，不报 |
| PEOU2 | PEOU | 0.751 | 12.375 |
| PEOU3 | PEOU | 0.733 | 12.163 |
| PEOU4 | PEOU | 0.743 | 12.290 |
| PU1 | PU | 0.761 | 固定为 1，不报 |
| PU2 | PU | 0.748 | 14.617 |
| PU3 | PU | 0.658 | 12.784 |
| PU4 | PU | 0.849 | 16.348 |
| TR1 | TR | 0.773 | 固定为 1，不报 |
| TR2 | TR | 0.751 | 12.868 |
| TR3 | TR | 0.748 | 12.840 |
| SAT1 | SAT | 0.766 | 固定为 1，不报 |
| SAT2 | SAT | 0.775 | 17.435 |
| SAT3 | SAT | 0.753 | 10.989 |
| CI1 | CI | 0.845 | 固定为 1，不报 |
| CI2 | CI | 0.796 | 17.881 |
| CI3 | CI | 0.872 | 19.414 |

> AMOS 的 **C.R.** 是 critical ratio（估计值 / 标准误，即 z 值），**不是**组合信度 CR。组合信度和 AVE 要用标准化载荷手算，本工具已算好，见 results.xlsx。

## 3. 画结构模型

在 CFA 图的基础上：
1. **删掉**内生构念（`PU`、`SAT`、`CI`）身上的双箭头，只保留外生构念之间的双箭头：`PEOU` ↔ `TR`。
2. 用单箭头画结构路径，并给每条路径命名（右键箭头 → Object Properties → Parameters → Regression weight 填标签）：

| 路径 | 参数标签 | 对应假设 |
|---|---|---|
| `PEOU` → `PU` | `P1` | H1 |
| `PU` → `SAT` | `P2` | H2 |
| `PEOU` → `SAT` | `P3` | H3 |
| `TR` → `SAT` | `P4` | H4 |
| `SAT` → `CI` | `P5` | H5 |
| `PU` → `CI` | `P6` | H6 |
| `TR` → `CI` | `P7` | H7 |

3. 给每个内生构念加残差项（Add a unique variable 工具），命名为：`PU` 的残差 `d1`；`SAT` 的残差 `d2`；`CI` 的残差 `d3`。

### 具体间接效应（自定义估计量）

AMOS 自带的 Indirect effects 只给「X 到 Y 所有间接路径的总和」。要分别检验每一条中介路径：

1. 点 Amos Graphics 左下角状态栏的 **Not estimating any user-defined estimand** → **Define new estimands**。
2. 在弹出的窗口里粘贴 `03_自定义估计量.txt` 的内容（每行一个间接效应，`p.` 表示参数标签）：

```
H8 = p.P2 * p.P5
H9 = p.P1 * p.P2
H10 = p.P1 * p.P2 * p.P5
```

3. 点工具栏的 Check Syntax，看到 Syntax is OK 后关闭窗口并保存。
4. 确认 Bootstrap 设置已勾选（见第 2 步），Calculate Estimates。
5. 结果在 Text Output → Estimates → Scalars → **User-defined estimands**，点 **Bootstrap Confidence → Bias-corrected percentile method** 看 95% 置信区间。

### 结构模型的预期结果

拟合：χ²/df = 1.436，CFI = 0.984，TLI = 0.981，RMSEA = 0.033，SRMR = 0.037。

| 假设 | 路径 | 标准化 β | 非标准化 b | S.E. | C.R. | P |
|---|---|---|---|---|---|---|
| H1 | PEOU → PU | 0.451 | 0.525 | 0.074 | 7.085 | < 0.001 |
| H2 | PU → SAT | 0.487 | 0.485 | 0.066 | 7.306 | < 0.001 |
| H3 | PEOU → SAT | 0.153 | 0.177 | 0.077 | 2.309 | 0.021 |
| H4 | TR → SAT | 0.230 | 0.233 | 0.060 | 3.861 | < 0.001 |
| H5 | SAT → CI | 0.204 | 0.224 | 0.089 | 2.516 | 0.012 |
| H6 | PU → CI | 0.344 | 0.376 | 0.080 | 4.710 | < 0.001 |
| H7 | TR → CI | 0.044 | 0.049 | 0.066 | 0.741 | 0.459 |

| 间接效应 | 估计值 | BC 95% CI |
|---|---|---|
| H8 | 0.108 | [0.018, 0.199] |
| H9 | 0.255 | [0.166, 0.371] |
| H10 | 0.057 | [0.011, 0.116] |

> Bootstrap 置信区间是随机重抽样得到的，AMOS 和 R 的随机数不同，上下限在第三位小数上有差别是正常的；判断显著与否应该一致。

## 4. 多群组分析（可选）

1. Analyze → Manage Groups：把 Group number 1 改名为第一组，点 New 建第二组（分组变量 `gender`）。
2. File → Data Files：每一组都选同一个 .sav，点 Grouping Variable 选 `gender`，再点 Group Value 选这一组的取值。
3. 点 **Multiple-Group Analysis** 按钮，AMOS 会自动生成 Unconstrained / Measurement weights / Structural weights 等嵌套模型，Model Fit 里比较 CFI 的变化（ΔCFI ≤ 0.01 视为等价成立）。
4. 比较某条路径在两组间是否不同：Analysis Properties → Output 勾选 **Critical ratios for differences**，两组的同一路径命名不同标签后看两者差异的 C.R.（|C.R.| > 1.96 即 p < 0.05）。
