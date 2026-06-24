---
name: codebook-pass
description: 调查数据清洗Skill。处理调查数据（CGSS/CHIP/CSS等）时的标准化清洗流程，包括缺失值处理、变量编码统一、数据异常值检测。触发词：数据清洗/调查数据/codebook/数据清洗流程/问卷数据处理
version: "1.0"
metadata:
  openclaw:
    emoji: "🧹"
    homepage: "https://github.com/SiyaoZheng/ai4ss-skills"
---

# codebook-pass — 调查数据清洗Skill

> 本 Skill 是处理**中国综合社会调查（CGSS）、中国家庭收入调查（CHIP）、中国社会科学调查（CSS）**等大型调查数据的**标准化清洗流程**。确保从 codebook 到可用面板数据的每一步都可审计、可复现。

## 适用场景

- 从 CGSS/CHIP/CSS 等数据库下载原始数据后
- 合并多个年份的调查数据时
- 构建面板数据时
- 论文数据准备阶段

## 核心理念

**调查数据清洗的核心原则**：原始数据**只读不修改**，所有转换操作记录在 `processed/` 文件夹中，且必须更新 `provenance.json`。

**三个关键规则**：
1. **原始数据不可直接修改**——所有操作在 `processed/` 文件夹中进行
2. **每一步转换必须有记录**——包括变量名、编码、处理方式
3. **缺失值必须明确标注**——不得将缺失值默认为 0 或其他有意义的数值

## 工作流程

```
原始数据 → 导入检查 → 变量命名规范化 → 缺失值处理 → 异常值处理 → 编码统一 → 合并面板 → 输出报告
```

### Step 1 · 原始数据导入检查

**必须执行**：

```python
import pandas as pd
import numpy as np

# 读取原始数据
df = pd.read_stata("data/raw/cgss2021.dta")

# 基础检查
print(f"样本量: {len(df)}")
print(f"变量数: {len(df.columns)}")
print(f"\n缺失值概况:")
print(df.isnull().sum()[df.isnull().sum() > 0])
```

**检查项**：

| 检查项 | 预期结果 |
|--------|----------|
| 样本量 | 与 codebook 描述一致 |
| 变量数 | 与 codebook 描述一致 |
| 极端缺失变量 | 缺失率 >50% 的变量需标注 |
| 数据类型 | 数值型/字符型与 codebook 一致 |

### Step 2 · 变量命名规范化

**统一命名规则**（建议采用）：

```
{数据库缩写}_{年份}_{变量原名}
例如：cgss_2021_income, chip_2018_urban
```

**变量编码记录**（必须写入 `provenance.json`）：

```json
{
  "variable": "cgss_2021_urban",
  "description": "城乡户籍类型",
  "original_codes": {"1": "城市", "2": "农村", "9": "未知"},
  "transformed_codes": {"1": "urban", "2": "rural"},
  "missing_handling": "9 → NaN"
}
```

### Step 3 · 缺失值处理

**必须明确处理的缺失类型**：

| 缺失类型 | 调查数据常见编码 | 处理方式 |
|----------|-----------------|----------|
| **真实缺失** | `.` / `NA` | 保持 NaN |
| **不适用** | `97/98/99` | 保持 NaN，不填0 |
| **拒绝回答** | `97` | 保持 NaN |
| **不知道** | `98` | 保持 NaN |
| **数据缺失** | `99` | 保持 NaN |

**⚠️ 常见错误**：
- ❌ 将 `97/98/99` 填为 0（改变了变量的均值）
- ❌ 将缺失值当作有效值处理
- ❌ 删除所有含缺失值的观测（浪费数据）

**正确做法**：

```python
# 识别调查数据中的特殊编码
missing_codes = [97, 98, 99, 999, 9999]

for var in categorical_vars:
    df[var] = df[var].replace(missing_codes, np.nan)
```

### Step 4 · 异常值检测

**常用方法**：

```python
# 描述统计 + 分布检查
print(df[numeric_vars].describe(percentiles=[.01, .05, .25, .50, .75, .95, .99]))

# 极端值检测（IQR方法）
def detect_outliers_iqr(series, factor=3):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - factor * IQR
    upper = Q3 + factor * IQR
    return (series < lower) | (series > upper)

outliers = detect_outliers_iqr(df['income'])
print(f"极端值数量: {outliers.sum()}")
```

**处理方式**：

| 异常类型 | 处理方式 |
|----------|----------|
| 数据录入错误（明显不合理值） | 修正或标记为缺失 |
| 合理极端值 | 保持，报告中位数替代均值 |
| 离群点（ winsorize） | 双边 winsorize（1%和99%分位） |

**Winsorize 示例**：

```python
from scipy.stats import mstats

for var in ['income', 'education_years']:
    df[var] = mstats.winsorize(df[var], limits=[0.01, 0.01])
```

### Step 5 · 编码统一（多年份/多数据库合并）

**纵向合并（多年份 CGSS）**：

```python
# 确保变量名一致
cgss_2017 = pd.read_stata("data/raw/cgss2017.dta")
cgss_2021 = pd.read_stata("data/raw/cgss2021.dta")

# 重命名统一
cgss_2017 = cgss_2017.rename(columns={
    "a2017_income": "income",
    "a2017_urban": "urban"
})
cgss_2021 = cgss_2021.rename(columns={
    "a2021_income": "income",
    "a2021_urban": "urban"
})

# 合并
df_combined = pd.concat([cgss_2017, cgss_2021], ignore_index=True)
df_combined['year'] = 2017  # 添加年份变量
```

**横向合并（CHIP + CGSS）**：

```python
# 统一变量定义和编码
# CHIP: income_2018; CGSS: income_2021
# 需标注：不同数据库收入定义可能不同
```

### Step 6 · 构建面板数据

**长宽格式转换**：

```python
# 宽 → 长
df_panel = df.melt(
    id_vars=['id', 'year'],
    value_vars=['income', 'education', 'employment'],
    var_name='variable',
    value_name='value'
)
```

### Step 7 · 输出报告

**必须输出**：

1. **数据清洗报告**（`data/processed/cleaning_report.md`）
2. **变量定义表**（`data/processed/variable_definition.csv`）
3. **更新的 provenance.json**

**清洗报告模板**：

```markdown
## 数据清洗报告

**原始数据**：CGSS 2021 (N=10,000)
**清洗后数据**：processed/cgss_2021_clean.dta (N=9,847)
**清洗时间**：[日期]

### 样本变动

| 处理类型 | 样本数 | 原因 |
|----------|--------|------|
| 原始样本 | 10,000 | |
| 删除重复记录 | -15 | ID重复 |
| 核心变量缺失 | -138 | income/education 缺失 |
| 清洗后 | 9,847 | |

### 变量处理记录

| 变量名 | 原始编码 | 处理方式 | 备注 |
|--------|----------|----------|------|
| income | 99999→NaN | 特殊编码替换 | 拒绝回答 |
| urban | 1/2 | 保持 | 城市=1,农村=2 |
```

## 调用接口

在 Claude Code 对话窗口输入：

```
/codebook-pass
```

或完整 Prompt：

```
按调查数据清洗Skill处理本项目的CGSS/CHIP数据：原始数据导入检查→变量命名规范化→缺失值处理→异常值检测→编码统一→构建面板→输出清洗报告和provenance.json
```

## 重要声明

- **原始数据永远不可修改**——所有操作在 `processed/` 文件夹中进行
- 缺失值处理必须**具体说明每种编码的含义**，不得统一当作"缺失"处理后填 0
- 不同年份调查问卷可能有细微差异，合并时必须**逐变量核查**