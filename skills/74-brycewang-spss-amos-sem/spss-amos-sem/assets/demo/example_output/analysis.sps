* Encoding: UTF-8.
* ============================================================================.
* 移动支付 App 持续使用意愿研究 —— SPSS 部分（由 spss-amos-sem 自动生成）.
* 生成依据：设定卡里的构念、反向题、缺失值规则和模型修正.
* 每一步的数字都能和 R 复算结果（results.xlsx）逐项对照.
* ============================================================================.
* ---- 第 0 步：把下面这一行改成数据所在的文件夹，然后 全选 → 运行 ----.
CD 'C:\改成你的文件夹路径'.
GET FILE='questionnaire_demo.sav'.
DATASET NAME raw WINDOW=FRONT.
* 所有输出表格同时导出到 Excel，方便核对和交给 Claude 读取.
OMS /SELECT TABLES /DESTINATION FORMAT=XLSX OUTFILE='spss_output_tables.xlsx' /TAG='aers_sem'.
* ---- 第 1 步：超出量表范围的值（如 9 = 缺失代码）一律设为缺失 ----.
RECODE PEOU1 PEOU2 PEOU3 PEOU4 PU1 PU2 PU3 PU4
    TR1 TR2 TR3 TR4 SAT1 SAT2 SAT3 CI1
    CI2 CI3 (1 THRU 5=COPY) (ELSE=SYSMIS).
EXECUTE.
* ---- 第 2 步：剔除规律作答（所有题目答案完全一样，标准差为 0；必须在反向计分之前判断）----.
COMPUTE sd_all = SD(PEOU1, PEOU2, PEOU3, PEOU4, PU1, PU2, PU3, PU4, TR1, TR2, TR3, TR4, SAT1, SAT2, SAT3, CI1, CI2, CI3).
SELECT IF (MISSING(sd_all) OR sd_all > 0).
EXECUTE.
* ---- 第 3 步：反向计分 ----.
RECODE PEOU4 (1=5) (2=4) (3=3) (4=2) (5=1).
EXECUTE.
* ---- 第 4 步：缺失值 ----.
* 列表删除：任何一个分析变量缺失的问卷都剔除（AMOS 默认要求完整数据）.
COUNT n_miss = PEOU1 PEOU2 PEOU3 PEOU4 PU1 PU2 PU3 PU4
    TR1 TR2 TR3 TR4 SAT1 SAT2 SAT3 CI1
    CI2 CI3 gender age edu use_years (MISSING).
SELECT IF (n_miss = 0).
EXECUTE.
* 清洗后的有效样本量（看 N）.
FREQUENCIES VARIABLES=id /FORMAT=NOTABLE /STATISTICS=MINIMUM MAXIMUM.
* ---- 第 5 步：样本人口统计特征 ----.
FREQUENCIES VARIABLES=gender age edu use_years /ORDER=ANALYSIS.
* ---- 第 6 步：题项描述统计与正态性（|偏度| < 3、|峰度| < 10 可视为近似正态，Kline 2016）----.
DESCRIPTIVES VARIABLES=PEOU1 PEOU2 PEOU3 PEOU4 PU1 PU2 PU3 PU4
    TR1 TR2 TR3 SAT1 SAT2 SAT3 CI1 CI2
    CI3
  /STATISTICS=MEAN STDDEV MIN MAX KURTOSIS SKEWNESS.
* ---- 第 7 步：共同方法偏差 —— Harman 单因素检验（未旋转，看第一个因子的方差解释率）----.
FACTOR
  /VARIABLES PEOU1 PEOU2 PEOU3 PEOU4 PU1 PU2 PU3 PU4
    TR1 TR2 TR3 SAT1 SAT2 SAT3 CI1 CI2
    CI3
  /MISSING LISTWISE
  /PRINT INITIAL EXTRACTION
  /CRITERIA MINEIGEN(1) ITERATE(25)
  /EXTRACTION PC
  /ROTATION NOROTATE
  /METHOD=CORRELATION.
* ---- 第 8 步：信度分析（每个构念一次）----.
RELIABILITY
  /VARIABLES=PEOU1 PEOU2 PEOU3 PEOU4
  /SCALE('感知易用性') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.
RELIABILITY
  /VARIABLES=PU1 PU2 PU3 PU4
  /SCALE('感知有用性') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.
RELIABILITY
  /VARIABLES=TR1 TR2 TR3
  /SCALE('信任') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.
RELIABILITY
  /VARIABLES=SAT1 SAT2 SAT3
  /SCALE('满意度') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.
RELIABILITY
  /VARIABLES=CI1 CI2 CI3
  /SCALE('持续使用意愿') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.
* ---- 第 9 步：探索性因子分析（KMO、Bartlett、旋转后载荷）----.
FACTOR
  /VARIABLES PEOU1 PEOU2 PEOU3 PEOU4 PU1 PU2 PU3 PU4
    TR1 TR2 TR3 SAT1 SAT2 SAT3 CI1 CI2
    CI3
  /MISSING LISTWISE
  /PRINT INITIAL KMO EXTRACTION ROTATION
  /FORMAT SORT BLANK(.40)
  /CRITERIA FACTORS(5) ITERATE(25)
  /EXTRACTION PC
  /CRITERIA ITERATE(25)
  /ROTATION VARIMAX
  /METHOD=CORRELATION.
* ---- 第 10 步：计算各构念均值（变量名 m_构念代码，供相关分析和 PROCESS 使用）----.
COMPUTE m_PEOU = MEAN(PEOU1, PEOU2, PEOU3, PEOU4).
VARIABLE LABELS m_PEOU '感知易用性'.
COMPUTE m_PU = MEAN(PU1, PU2, PU3, PU4).
VARIABLE LABELS m_PU '感知有用性'.
COMPUTE m_TR = MEAN(TR1, TR2, TR3).
VARIABLE LABELS m_TR '信任'.
COMPUTE m_SAT = MEAN(SAT1, SAT2, SAT3).
VARIABLE LABELS m_SAT '满意度'.
COMPUTE m_CI = MEAN(CI1, CI2, CI3).
VARIABLE LABELS m_CI '持续使用意愿'.
EXECUTE.
* ---- 第 11 步：描述统计与 Pearson 相关 ----.
CORRELATIONS
  /VARIABLES=m_PEOU m_PU m_TR m_SAT m_CI
  /PRINT=TWOTAIL NOSIG
  /STATISTICS DESCRIPTIVES
  /MISSING=PAIRWISE.
* ---- 第 12 步：多重共线性诊断（VIF < 5，越接近 1 越好）----.
REGRESSION
  /STATISTICS COEFF R ANOVA COLLIN TOL
  /DEPENDENT m_SAT
  /METHOD=ENTER m_PU m_PEOU m_TR.
REGRESSION
  /STATISTICS COEFF R ANOVA COLLIN TOL
  /DEPENDENT m_CI
  /METHOD=ENTER m_SAT m_PU m_TR.
* ---- 第 13 步：保存清洗后的数据，AMOS 直接读这个文件 ----.
SAVE OUTFILE='questionnaire_demo_cleaned.sav'
  /COMPRESSED.
* ---- 第 14 步：PROCESS 中介 / 调节（需要先安装 Hayes 的 PROCESS v4 宏）----.
* 安装：到 processmacro.org 下载，打开 process.sps 全选运行一次（每次打开 SPSS 都要运行一次），.
* 或者用 扩展 → 实用程序 → 安装定制对话框 安装 process.spd。下面的命令在宏定义之后才能运行.
* INSERT FILE='process.sps'.
process y=m_CI/x=m_PU/m=m_SAT/model=4/boot=5000/seed=20261027/total=1.
process y=m_CI/x=m_PU/m=m_SAT/w=m_TR/model=7/boot=5000/seed=20261027/center=1.
OMSEND TAG=['aers_sem'].
* 完成。接下来按 amos/AMOS操作步骤.md 在 AMOS 里做 CFA 和结构模型.
