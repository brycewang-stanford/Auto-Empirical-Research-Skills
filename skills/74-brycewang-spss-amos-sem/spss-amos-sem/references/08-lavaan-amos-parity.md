# lavaan（R）与 AMOS / SPSS 的对应关系

引擎用 R 复算 SPSS 和 AMOS 的结果，目的是：用户没装软件也能拿到全部数字；装了软件的用户可以逐项核对。下表是设置上的对应。

| 项目 | AMOS / SPSS 默认 | 引擎的设置 |
|---|---|---|
| 估计方法 | ML | `estimator = "ML"` |
| 识别 | 每个潜变量第一条载荷固定为 1 | lavaan 默认（`std.lv = FALSE`） |
| 卡方 | (N − 1) × F_min（IBM Amos User's Guide 附录 A：n = N − r，单组时 r = 1） | `likelihood = "wishart"` |
| 外生潜变量相关 | Amos 程序默认相关；Graphics 要手动画双箭头 | lavaan 默认外生潜变量相关 |
| 缺失值 | 要求完整数据（否则要 means and intercepts） | 默认列表删除；`missing: fiml` 时用 FIML（此时 χ² 用 N） |
| 间接效应 CI | Bias-corrected percentile | `boot.ci.type = "bca.simple"`（即 BC，不含加速常数） |
| PROCESS | OLS，百分位 bootstrap，center=1，W 取第 16/50/84 百分位 | 同（`scripts/R/process.R`） |
| 偏度 / 峰度 | SPSS 的 G1 / G2（样本校正） | 同公式（`spss_skew`、`spss_kurt`） |
| EFA | 主成分、Kaiser 标准化的 varimax | `psych::principal(rotate = "varimax")` |
| α、CITC | 原始分 | 同 |

## 应该完全一致的

α、CITC、删除该项后 α、KMO、Bartlett、EFA 特征值与方差解释率、偏度峰度、Pearson 相关、PROCESS 的系数、SE、t、p 和点估计。旋转后载荷可能**列的顺序不同或整列符号相反**（成分的排列与方向本来就是任意的），数值的绝对值一致。

## 应该非常接近的（小数点后两三位）

CFA / SEM 的载荷、路径系数、标准误、χ²、CFI、TLI、RMSEA、SRMR、GFI、AGFI。偶尔有极小差异，原因是收敛标准和数值优化的细节不同。

## 只要求结论一致的

所有 bootstrap 结果（Boot SE、置信区间）：AMOS、PROCESS 与 R 的随机数发生器不同，区间端点在第三位小数上有差别是正常的；判断"是否包含 0"应一致。如果某个区间刚好擦着 0（例如下限 0.001），不同软件的结论可能不同，这时应如实说明结果处于显著性边缘，可以加大 bootstrap 次数（如 5000）再看。

## 差得多的时候查什么

1. 两边样本量 N 是否相同（SPSS 列表删除是否用了同样的变量）。
2. 反向题是否两边都处理了、只处理了一次。
3. 题项归属、删掉的题、误差相关是否两边一致。
4. AMOS 里外生潜变量之间的双箭头是否都画了（Graphics 不会自动画）。
5. AMOS 是否读的是清洗后的 `_cleaned.sav`。
