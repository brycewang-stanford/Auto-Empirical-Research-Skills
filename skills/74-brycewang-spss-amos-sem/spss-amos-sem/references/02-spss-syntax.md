# 生成的 SPSS 语法（analysis.sps）说明

## 怎么运行

1. 把 `analysis.sps`、原始数据 `.sav` 放在同一个文件夹。
2. 双击 `analysis.sps` 用 SPSS 打开，把第一条命令 `CD 'C:\改成你的文件夹路径'.` 改成这个文件夹的路径（Mac 写 `/Users/名字/Desktop/问卷分析` 这样的形式）。
3. 运行 → 全部（Run → All）。
4. 输出窗口里是所有表格；同时 OMS 会把全部表格导出到同文件夹的 `spss_output_tables.xlsx`，方便核对或发给 Claude。

文件第一行 `* Encoding: UTF-8.` 告诉 SPSS 按 UTF-8 读中文注释和标签。SPSS 16 以前的版本不支持，打开如果是乱码，在 编辑 → 选项 → 语言 里把"字符编码"设为 Unicode 后重新打开。

## 每一段在做什么

| 步骤 | 命令 | 说明 |
|---|---|---|
| 1 | `RECODE ... (1 THRU k=COPY) (ELSE=SYSMIS)` | 超出量表范围的值（如缺失代码 9、录入错误 55）一律设为系统缺失 |
| 2 | `COMPUTE sd_all = SD(...)` + `SELECT IF` | 剔除规律作答（所有题目同一个答案）。**必须在反向计分之前**，否则"全选 5"的问卷经过反向题后不再是全同 |
| 3 | `RECODE x (1=5) (2=4) ...` | 反向计分（原地改写，所以后面要另存为新文件，不要覆盖原始数据） |
| 4 | `COUNT n_miss = ... (MISSING)` + `SELECT IF (n_miss = 0)` | 列表删除，保证 SPSS、AMOS、R 用的是同一批样本 |
| 5 | `FREQUENCIES` | 人口统计特征（频数、百分比） |
| 6 | `DESCRIPTIVES /STATISTICS=... SKEWNESS KURTOSIS` | 题项描述统计与正态性 |
| 7 | `FACTOR ... /EXTRACTION PC /ROTATION NOROTATE` | Harman 单因素：看"总方差解释"表里第一个成分的"方差百分比" |
| 8 | `RELIABILITY ... /SUMMARY=TOTAL` | 每个构念一次。看"可靠性统计"的 α 和"项总计统计"的"校正后项与总计相关性"（CITC）、"删除项后的 α" |
| 9 | `FACTOR ... /PRINT KMO ... /ROTATION VARIMAX` | EFA。看"KMO 和巴特利特检验"、"总方差解释"、"旋转后的成分矩阵"（< 0.40 的载荷已隐藏） |
| 10 | `COMPUTE m_X = MEAN(...)` | 构念均值，变量名 `m_` + 构念代码 |
| 11 | `CORRELATIONS` | 均值、标准差与 Pearson 相关 |
| 12 | `REGRESSION ... /STATISTICS COLLIN TOL` | VIF（共线性），看"系数"表最后一列 |
| 13 | `SAVE OUTFILE='..._cleaned.sav'` | 保存清洗后的数据，AMOS 读这个文件 |
| 14 | `process y=.../x=.../model=...` | PROCESS 宏（见下） |

## PROCESS 宏

- 到 Hayes 的官网 processmacro.org 下载 PROCESS v4（免费）。
- 用法一：打开下载包里的 `process.sps`，全选运行一次（定义宏），再回到 `analysis.sps` 运行 PROCESS 那几行。**每次重新打开 SPSS 都要重新运行一次 `process.sps`**。
- 用法二：扩展 → 实用程序 → 安装定制对话框，装 `process.spd`，之后可以从菜单 分析 → 回归 → PROCESS 用。
- PROCESS 要求变量名不超过 8 个字符，所以构念代码限制在 6 个字母以内（`m_` + 6 = 8）。
- 生成的命令用了 `boot=`、`seed=`（结果可复现）、`total=1`（模型 4/6 报告总效应）、`center=1`（有交互项的模型做均值中心化）、`jn=1`（模型 1 的 Johnson-Neyman 区间）。

## 常见报错

| 报错 / 现象 | 原因与解决 |
|---|---|
| `CD` 命令报错或找不到文件 | 路径写错，或路径里有引号 / 特殊字符；Windows 路径用 `\`，整个路径放在单引号里 |
| 报错说变量名无法识别 / 未定义 | 设定卡里的题项名和数据里不一致（大小写、空格、中文全角） |
| RELIABILITY 出现"负平均协方差"警告 | 有反向题没处理，或题项归错了构念 |
| `process` 命令无法识别 | 本次会话没有先运行 `process.sps` |
| 中文变量标签乱码 | 数据文件是旧版本 SPSS 用 GBK 存的：编辑 → 选项 → 语言，切换"字符编码"后重新打开数据 |
| SELECT IF 之后样本量比 R 少 | 人口统计变量里也有缺失，列表删除把它们也算进去了（这是设计如此：保证所有分析同一样本） |
