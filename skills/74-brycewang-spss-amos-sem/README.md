# SPSS + AMOS 问卷结构方程（spss-amos-sem）

First-party AERS skill for the questionnaire structural-equation workflow that Chinese
management, psychology, education, nursing and tourism theses use: SPSS for cleaning,
reliability and EFA, AMOS for CFA and the structural model, PROCESS for moderation.

Open [`spss-amos-sem/SKILL.md`](spss-amos-sem/SKILL.md) for agent instructions.

一张设定卡驱动整条流程。R/lavaan 按 AMOS 的默认设置把数字算出来，同时生成：

- **SPSS 语法**（`analysis.sps`）：清洗、反向计分、规律作答、人口统计、描述统计、Harman、信度、EFA、相关、VIF、PROCESS；
- **AMOS 材料**：Amos Graphics 画图清单（附每张 AMOS 表的预期数值）、Program Editor 的 VB.NET 程序、具体间接效应的自定义估计量；
- **论文材料**：中文三线表（Word）、结果章节初稿、标准化路径图、模型修正记录（每一步修正都附理由和数据依据）。

```bash
Rscript spss-amos-sem/scripts/draft_spec.R 我的问卷.sav --out spec.yml   # 起草设定卡
Rscript spss-amos-sem/scripts/run_sem.R spec.yml --out 结果 --quick      # 快速检查
Rscript spss-amos-sem/scripts/run_sem.R spec.yml --out 结果              # 正式运行
Rscript spss-amos-sem/tests/test_demo.R                                  # 自检
```

The demo (`spss-amos-sem/assets/demo/`) is a simulated mobile-payment survey with a
known generating model and planted data problems; `example_output/` is a full run on
it. Requires R ≥ 4.1 with `lavaan`, `semTools`, `psych`, `GPArotation`, `haven`,
`openxlsx`, `officer`, `flextable`, `yaml`, `jsonlite`. The AMOS VB.NET programs follow
the IBM SPSS Amos 28 User's Guide syntax but have not been run in AMOS; the Amos Graphics
checklist is the primary route.
