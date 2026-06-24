---
name: latex-table
description: LaTeX回归表格生成Skill。辅助生成符合AER/QJE等顶刊格式的三线表，包括标准误聚类标注、显著性星标、固定效应标注。触发词：LaTeX表格/回归表/三线表/table制作/latex table
version: "1.0"
metadata:
  openclaw:
    emoji: "📋"
    homepage: "https://github.com/SiyaoZheng/ai4ss-skills"
---

# latex-table — LaTeX 回归表格生成Skill

> 本 Skill 辅助生成符合**经济学顶刊（AER, QJE, Econometrica, JPE）**格式规范的 LaTeX 回归表格。涵盖：标准三线表、面板数据固定效应表、工具变量表、事件研究表。

## 适用场景

- 论文写作中需要插入规范的回归结果表
- 将 Stata/Python/R 输出转换为 LaTeX 代码
- 按期刊要求排版三线表
- 生成主子表（Main Table）+ 在线附录表（Online Appendix Table）

## 核心理念

**顶刊表格的核心要素**：
1. **清晰的信息层级**——表头、分组、变量名层层递进
2. **完整的统计信息**——样本量、标准误、聚类层级、R²、F统计量
3. **规范的显著性标注**——星标统一（†/***/**/*）
4. **可复现**——表格代码必须与回归代码对应

## 标准三线表格式规范

### 顶刊表格结构

```
┌─────────────────────────────────────────────┐
│  表头（表标题 + 注释信息）                      │
├─────────────────────────────────────────────┤
│  列标签（列1    列2    列3）                  │
│  ──────────────────────────────────────────  │ ← 第一道线（顶部）
│  变量行（因变量、自变量、控制变量）              │
│  ──────────────────────────────────────────  │ ← 第二道线（列分隔）
│  统计量行（N、R²、F、聚类标准误）              │
├─────────────────────────────────────────────┤
│  表底注释（显著性标注、数据来源、稳健性说明）     │
└─────────────────────────────────────────────┘
```

### 显著性星标标准

| 符号 | p值 | 说明 |
|------|-----|------|
| *** | p < 0.001 | 1% 显著性 |
| ** | p < 0.01 | 5% 显著性 |
| * | p < 0.05 | 10% 显著性 |
| † | p < 0.10 | 15% 显著性（部分期刊）|

**⚠️ 注意**：不同期刊对星标的数量和阈值要求不同，投稿前需确认目标期刊格式。

## 常用表格 LaTeX 模板

### 模板 1：标准 OLS 回归表

```latex
\begin{table}[htbp]
  \centering
  \caption{基准回归结果}
  \label{tab:baseline}
  \begin{threeparttable}
    \begin{tabular}{l*{3}{c}}
      \toprule
      & \multicolumn{3}{c}{因变量: log(GDP per capita)} \\
      \cmidrule(l){2-4}
      & (1) & (2) & (3) \\
      \midrule
      互联网普及率 & 0.023*** & 0.018** & 0.015* \\
                  & (0.007) & (0.008) & (0.008) \\
      控制变量     & 否       & 是       & 是       \\
      固定效应     & 否       & 否       & 年份+国家\\
      \midrule
      观测值       & 1,240    & 1,240    & 1,240    \\
      R²          & 0.041    & 0.315    & 0.682    \\
      \bottomrule
    \end{tabular}
    \begin{tablenotes}
      \item \textit{注:} ***, **, * 分别表示1\%, 5\%, 10\%的显著性水平。括号内为聚类标准误（聚类在国家层面）。控制变量包括：教育年限、人口增长率、贸易开放度。
    \end{tablenotes}
  \end{threeparttable}
\end{table}
```

### 模板 2：面板数据固定效应表

```latex
\begin{table}[htbp]
  \centering
  \caption{固定效应模型估计结果}
  \label{tab:fe}
  \begin{threeparttable}
    \begin{tabular}{l*{4}{c}}
      \toprule
      & \multicolumn{2}{c}{OLS} & \multicolumn{2}{c}{固定效应} \\
      \cmidrule(l){2-3} \cmidrule(l){4-5}
      & (1) & (2) & (3) & (4) \\
      \midrule
      技术扩散指数 & 0.035*** & 0.028** & 0.021* & 0.018* \\
                   & (0.009) & (0.010) & (0.011) & (0.010) \\
      \midrule
      国家固定效应   & \checkmark & \checkmark & \checkmark & \checkmark \\
      年份固定效应   &            & \checkmark &            & \checkmark \\
      \midrule
      观测值         & 1,240 & 1,240 & 1,240 & 1,240 \\
      R²             & 0.31  & 0.45  & 0.72  & 0.78  \\
      \bottomrule
    \end{tabular}
    \begin{tablenotes}
      \item \textit{注:} 同上。固定效应模型使用双向聚类标准误（国家+年份）。
    \end{tablenotes}
  \end{threeparttable}
\end{table}
```

### 模板 3：工具变量法表

```latex
\begin{table}[htbp]
  \centering
  \caption{工具变量估计结果}
  \label{tab:iv}
  \begin{threeparttable}
    \begin{tabular}{l*{3}{c}}
      \toprule
      & OLS & \multicolumn{2}{c}{2SLS} \\
      \cmidrule(l){2-2} \cmidrule(l){3-4}
      & (1) & (2) & (3) \\
      \midrule
      技术扩散指数 & 0.023*** & 0.041*** & 0.038*** \\
                  & (0.007) & (0.013) & (0.012) \\
      \midrule
      KP F统计量   &         & 24.6     & 28.3     \\
      弱工具变量检验 &         &          &          \\
      \midrule
      观测值       & 1,240   & 1,240    & 1,240    \\
      \bottomrule
    \end{tabular}
    \begin{tablenotes}
      \item \textit{注:} 列(2)-(3)使用技术扩散的滞后值作为工具变量。KP F统计量>10通过弱工具变量检验。
    \end{tablenotes}
  \end{threeparttable}
\end{table}
```

## 从 Stata/Python/R 到 LaTeX 的转换工具

### Stata → LaTeX

```stata
// 安装 estout 套件
ssc install estout, replace

// 保存回归结果
eststo clear
eststo: reg ln_gdp internet i.year, vce(cluster country)
eststo: reg ln_gdp internet cov1 cov2 i.year, vce(cluster country)

// 导出 LaTeX
esttab using "tables/table1.tex", replace ///
  title("基准回归结果") ///
  label ///
  booktabs ///
  nonumbers ///
  mtitles("OLS" "OLS") ///
  star(* 0.05 ** 0.01 *** 0.001) ///
  se ///
  r2 ///
  addn("控制变量包括教育年限、人口增长率、贸易开放度。")
```

### Python (statsmodels) → LaTeX

```python
import pandas as pd
from scipy.stats import ttest_ind

# 使用 statsmodels 输出的 LaTeX 转换
from statsmodels.iolib.summary import summary_table

# 回归后
result = model.fit()
print(result.summary_latex())
```

## 三线表排版规范（顶刊要求）

| 要求 | 说明 |
|------|------|
| **Threeparttable** | 使用 `\begin{threeparttable}` 环境 |
| **booktabs** | 使用 `\toprule`, `\midrule`, `\bottomrule` |
| **字体** | 通常10pt，表的注释可9pt |
| **列宽** | 使用 `p{3cm}` 控制列宽，或 `tabularx` 自动调整 |
| **数字对齐** | 数字右对齐，变量名列左对齐 |
| **缺失值** | 表格中用空白表示缺失，不写"NA" |

## 输出规范

```markdown
## 表格输出规范

**输出路径**：tables/table{N}.tex
**主子表规范**：
- 主表（Main）：表格1-3，放入正文
- 附录表（Appendix）：表格A1-A10，放入Online Appendix

**文件名规范**：
```
tables/table1_baseline.tex          # 基准回归
tables/table2_heterogeneity.tex     # 异质性分析
tables/tableA1_robustness_iv.tex    # 附录：IV稳健性
```

**LaTeX 代码规范**：
- 表格必须可编译（无缺失 `}` 或 `{`）
- 所有特殊字符（%, &, #）需转义
```

## 调用接口

在 Claude Code 对话窗口输入：

```
/latex-table
```

或完整 Prompt：

```
按LaTeX表格Skill生成符合AER顶刊格式的三线表回归结果，包括：基准回归表（表1）、固定效应表（表2）、工具变量表（表3）。使用booktabs环境，包含标准误聚类标注、显著性星标、固定效应标注。
```

## 与其他 Skill 的配合

- **`did-reviewer`** → DID 回归结果使用事件研究表格式
- **`R-optimizer`** → R 输出表格时的优化
- **`codebook-pass`** → 清洗后数据直接用于表格生成

## 重要声明

- **表格必须可复现**——LaTeX 表格代码对应的回归必须可通过 Makefile 重新运行
- 投稿前必须按目标期刊格式调整星标阈值和表格大小
- **主子表分离**——主表放核心结果，稳健性和异质性放入附录