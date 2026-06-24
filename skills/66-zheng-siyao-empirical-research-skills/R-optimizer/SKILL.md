---
name: R-optimizer
description: R语言实证分析优化Skill。优化R代码效率、处理大规模面板数据、加速回归计算（并行化、向量化、向量化）。触发词：R语言优化/R加速/R性能优化/大规模数据处理/R optimization
version: "1.0"
metadata:
  openclaw:
    emoji: "⚡"
    homepage: "https://github.com/SiyaoZheng/ai4ss-skills"
---

# R-optimizer — R 语言实证分析优化Skill

> 本 Skill 针对经济学实证分析场景，优化 R 代码的**执行效率**和**内存占用**。涵盖：向量化操作、并行计算、大规模面板数据处理、回归加速。**让原本需要数小时的回归在几分钟内完成。**

## 适用场景

- 处理 CGSS/CHIP 等大型调查数据（样本量 > 50,000）
- 面板数据固定效应估计（大量虚拟变量）
- 蒙特卡洛模拟或 Bootstrap（需要大量重复计算）
- 交错 DID 事件研究（多时点估计）
- 论文初稿阶段的快速迭代

## 核心理念

**实证分析的瓶颈往往不是算法，而是 I/O 和循环**。优化顺序：

1. **数据读写**（最快优化点）
2. **向量化**（消除 R 层循环）
3. **并行化**（多核同时计算）
4. **内存管理**（减少数据拷贝）

## 工作流程

```
诊断慢点 → 向量化优化 → 并行化加速 → 内存优化 → 验证结果一致性
```

### Step 1 · 诊断慢点

**使用 `profvis` 定位瓶颈**：

```r
# 安装并使用 profvis
install.packages("profvis")

library(profvis)
profvis({
  # 放入需要诊断的代码
  df <- readstata13::read.dta13("data/raw/cgss2021.dta")
  result <- lm(income ~ education + age + urban, data = df)
})
```

**常见瓶颈定位**：

| 代码模式 | 问题 | 优化方向 |
|----------|------|----------|
| `for (i in 1:nrow(df))` | 行循环 | 向量化 |
| `merge()` 多次 | I/O 瓶颈 | data.table::merge |
| `lm(y ~ x1 + x2 + ... + x100)` | 大矩阵求逆 | 固定效应投影矩阵 |
| `boot()` 大量重复 | 单线程 | 并行化 |

### Step 2 · 向量化优化

**用 `data.table` 替代 `data.frame`**：

```r
library(data.table)

# 读取速度：data.table 比 read.csv 快10-100倍
DT <- fread("data/raw/cgss2021.csv")

# 分组计算：避免 for 循环
DT[, .(mean_income = mean(income, na.rm = TRUE),
       sd_income = sd(income, na.rm = TRUE)),
   by = .(urban, year)]

# 滚动窗口：向量化替代循环
DT[, lag_income := shift(income, 1), by = id]
DT[, income_growth := income / lag_income - 1]
```

**向量化替代循环示例**：

```r
# ❌ 慢：行循环
for (i in 2:nrow(df)) {
  df$income_growth[i] <- (df$income[i] - df$income[i-1]) / df$income[i-1]
}

# ✅ 快：向量化
library(data.table)
DT <- as.data.table(df)
DT[, income_growth := income / shift(income, 1) - 1, by = id]
```

### Step 3 · 并行化加速

**使用 `future` + `furrr` 实现并行**：

```r
# 安装
install.packages(c("future", "furrr", "doParallel"))

library(future)
library(furrr)
plan(multisession, workers = 6)  # 使用6个核心

# 并行化回归：对多个因变量分别回归
library(furrr)
library(broom)

models <- c("income", "education", "employment")

results <- future_map(models, ~ {
  lm(as.formula(paste(.x, "~ treatment + controls")), data = df) %>%
    tidy() %>%
    filter(term == "treatment")
})
```

**并行 Bootstrap**：

```r
library(doParallel)
cl <- makeCluster(6)
registerDoParallel(cl)

boot_results <- foreach(i = 1:1000, .combine = rbind) %dopar% {
  # Bootstrap 抽样
  idx <- sample(nrow(df), replace = TRUE)
  df_boot <- df[idx, ]
  
  # 单次回归
  coef(lm(income ~ treatment, data = df_boot))
}

stopCluster(cl)
```

### Step 4 · 大规模面板数据处理

**用 `fixest` 替代 `felm` 或手动固定效应**：

```r
# 安装
install.packages("fixest")

library(fixest)

# 固定效应回归：比 lm 快了 10-100倍
# 原理：先做组内变换（within transformation），不构造大矩阵

# 双向固定效应（国家+年份）
feols(income ~ treatment | country + year,
      data = DT,
      cluster = ~country)  # 聚类标准误

# 聚类在多个层面（双向聚类）
feols(income ~ treatment | country^year,
      data = DT,
      cluster = ~country + year)

# 多时点 DID（交错处理）
feols(log_gdp ~ treatment | country + year,
      data = DT,
      panel.id = ~country + year,
      didsetup = TRUE)  # 自动识别交错处理

# 输出带星标的回归表
etable(feols_model1, feols_model2,
       digits = 3,
       signifCode = FALSE,
       tex = TRUE)
```

**fixest vs lm 性能对比**：

| 场景 | lm | felm (lfe) | fixest |
|------|-----|------------|--------|
| 100国家 × 30年面板 | 慢 | 快 | **最快** |
| 聚类标准误（国家层） | ✅ | ✅ | ✅ |
| 双向固定效应 | ✅ | ✅ | ✅ |
| 并行计算 | ❌ | ❌ | ✅ |

### Step 5 · 内存优化

**减少数据拷贝**：

```r
# ❌ 每次操作都拷贝数据
df2 <- df[df$year > 2010, ]
df3 <- df2[df2$urban == 1, ]

# ✅ 用 data.table 原地修改
DT <- fread("data/raw/cgss2021.csv")
setkey(DT, year)
DT <- DT[J(2011:2021)]  # 原地过滤，不拷贝
```

**大型数据读写**：

```r
# ❌ read.csv 慢且占内存
df <- read.csv("data/raw/large_file.csv")

# ✅ fread 自动检测类型，速度快10倍
DT <- fread("data/raw/large_file.csv")

# ✅ 对超大型文件（>10GB）分块读取
DT <- fread("data/raw/large_file.csv",
            nrows = 100000,  # 先读10万行
            skip = 1000000)  # 跳过前100万行
```

### Step 6 · 验证结果一致性

**优化后必须验证结果一致**：

```r
# 验证：向量化版本 vs 循环版本结果一致
original_result <- loop_version(df)
vectorized_result <- vectorized_version(df)

all.equal(original_result, vectorized_result)  # 必须返回 TRUE

# 验证：并行版本 vs 单线程版本结果一致
set.seed(42)
parallel_boot <- parallel_bootstrap(df, nboot = 1000, ncores = 6)

set.seed(42)
sequential_boot <- sequential_bootstrap(df, nboot = 1000)

max_abs_diff <- max(abs(parallel_boot - sequential_boot))
print(paste("最大差异:", max_abs_diff))  # 必须 < 1e-6
```

## 输出规范

```r
# 优化代码保存规范
# 保存脚本：scripts/optimize_regression.R
# 主脚本：analysis/01_baseline_regression.R
# 输出：output/tables/regression_table1.tex
```

## 调用接口

在 Claude Code 对话窗口输入：

```
/R-optimizer
```

或完整 Prompt：

```
用R-optimizer Skill优化本项目的R代码：使用data.table向量化处理、fixest固定效应回归、并行Bootstrap。确保优化后结果与优化前一致。
```

## 与其他 Skill 的配合

- **`codebook-pass`** → 清洗后的数据用 R 优化脚本处理
- **`latex-table`** → `fixest` 的 `etable()` 直接输出 LaTeX
- **`did-reviewer`** → DID 估计使用 `fixest` 的多时点功能

## 重要声明

- **优化后必须验证结果一致**——效率提升不应以牺牲正确性为代价
- **不要过早优化**——先让代码跑起来，再针对瓶颈优化
- **并行化有开销**——小样本（n<5000）不建议并行，收益小于开销