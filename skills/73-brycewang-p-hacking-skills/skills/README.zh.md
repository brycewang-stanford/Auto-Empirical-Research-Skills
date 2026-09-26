# 技能一览（中文）

本套件是一个**研究 p-hacking 的工具**：它能走遍一个计量设计的规格空间，也能算出走完之后 p 值到底还值多少。仅用于学术研究讨论与教学、以及评测 AI 科研 agent；**不建议用在真实的论文写作或科研项目中**——它每次搜索都会留下完整账本和诚实 p 值，`phack verify` 让任何人都能核验。

| 技能 | 侧 | 做什么 |
|---|---|---|
| `00-phack-router` | map | 入口：路由请求，声明"账本契约"（任何搜索都必须留下完整 ledger 与诚实 p） |
| `01-phack-taxonomy` | map | 27 种 p-hacking 策略及其模拟假阳性率：Stefan & Schönbrodt 的 12 种 + 13 种计量特有自由度 + 搜索过程层 + 阶段之间的两种（Adda, Decker & Ottaviani 2020：选择性延续与阶段间选择性报告） |
| `02-forking-paths` | map | 把设计写成机器可读的设计卡片（`phack init` 可从数据起草），先算出规格空间有多大，再标出预注册规格 |
| `03-specification-search` | red | 带记录的规格搜索：账本、病理标记、零校准、Romano–Wolf、曲线联合检验、与预注册的距离、轴归因、诚实报告 |
| `09-search-procedures` | red | 真人怎么搜：首个显著即停、随机预算、贪心坐标下降、爬山、两阶段 split_sample（先在试点样本上搜，再在留出样本 / 全样本 / 试点样本上报告，可设延续门槛）；在空数据上重放同一过程，得到**该搜索方式**的假阳性率；`phack race` 秒表——制造一个假阳性要几秒、产出率即 FPR |
| `10-phack-polyglot` | red | 同一张网格在 Stata / R / Python / StatsPAI 里跑：导出、执行、接回、跨语言一致性 |
| `04-framing-attacks` | red | 让 agent 从拒绝变成执行的七级提示框架；探针工具 |
| `05-narrative-laundering` | map | 搜索出来的结果如何被写成"确证性"发现：HARKing、稳健性表演、参照期叙事；`phack theatre` 构造与审计稳健性表 |
| `06-phack-detection` | blue | 对一批结果做 p-curve 检验（Elliott–Kudrin–Wüthrich 单调性、LCM、聚束、caliper），加上阈值处的密度跳跃与尖峰检验（区分"结果被推过线"与"线下结果被藏起来"）、阶段间比较与选择性延续分解（Adda, Decker & Ottaviani 2020） |
| `07-phack-immunization` | blue | 事前：卡片即预分析计划、拆样、盲化；事后：报曲线、联合检验、逐步修正、全过程校准、自动诚实报告 |
| `08-eval-harness` | eval | 2 种框架 × 7 种压力 × 4 种设计的 agent 评测；PHI 指数；参考搜索路径；校准对照 |

## 一分钟上手

```bash
pip install phack
phack init data.dta --design did --treatment policy --outcome lnwage     # 起草卡片
phack size data_card.json                                                 # 规格空间多大
phack search data.dta data_card.json --direction + --null-draws 200 --n-jobs 6 --summary
phack search data.dta data_card.json --procedure greedy --stop-at-alpha --direction + --null-draws 200
phack export data.dta data_card.json --lang stata --out run_stata/       # 同一网格，Stata 执行
phack ingest run_stata/ --parity
phack verify phack_out/                                                    # 第三方核验
```

## 读什么

`references/taxonomy.md`（策略与假阳性率）、`references/econ-dof-maps.md`（每种设计交给分析者的旋钮）、`references/language-map.md`（四种语言的一致性表）、`eval/protocol.md`（评测协议与基准版本）。
