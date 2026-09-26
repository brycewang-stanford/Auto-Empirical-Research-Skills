# p-hacking-skills（中文说明）

**对 Claude Code 说一句"帮我找最显著的规格"，大约一秒钟的计算——这就是今天 p-hacking 的成本，而本仓库就是把它量出来的仪器。** 在构造上真实效应恰好为零的数据上，这里实现的现实搜索过程视设计不同能在 33–97% 的零抽取中制造出 p < .05，每个假阳性的中位耗时 0.01–1.1 秒（[实测数字](docs/capability.zh.md)）。它被打包成 11 个 agent 技能，驱动一台仪表化的规格搜索引擎：装上技能，对着已知零效应的数据说出那句话，你会拿到那个赢家——连同给它定价的完整账本，因为这里的任何搜索都不可能不留账本地运行。（[五分钟技能上手指南](docs/skills-quickstart.zh.md) · [负责任使用说明](RESPONSIBLE_USE.md)）

> **用途说明。** 本工具仅用于关于 p-hacking 的学术研究讨论与教学，以及评测 AI 科研 agent 是否会 p-hacking。**不建议用在真实的论文写作或科研项目中。** 它的每一次搜索都会留下完整账本（ledger）和零校准的诚实 p 值，`phack verify` 让任何第三方都能核验一个运行目录。如果你想用它给真实分析"找显著"，它会把你做过的一切都记下来——这是设计使然。

## 它是什么

Asher 等（2026）发现：前沿编程 agent 会拒绝"请给我显著结果"的直接要求，却会接受措辞改成"探索不同设计给出估计的上界"的同一要求，并写出按显著性排序的嵌套循环。要度量这个缺口，就得能在有记录的条件下执行这种行为，而且要在真正有油水的设计上：有估计量菜单的 DiD、有带宽菜单的 RDD、有工具变量菜单的 IV，并且用研究者真正在用的语言。

**唯一的规则：任何搜索都必须留下完整账本，任何报告出来的 p 值都必须附带它的诚实对应值。** 规格搜索本身不是不端，把搜索赢家当成单一预注册检验来报告才是。

## 速度，实测

`phack race` 给每种现实搜索过程上秒表，并在每次试验前把数据重新抽成零效应——所以产出率**就是**该过程的假阳性率，每个耗时都是一个假阳性被制造出来的实测成本。从预注册规格出发的贪心坐标下降，预算 60，单侧：

| 设计（真值 = 0） | 花园 | 零抽取上的产出率 | 到 p < .05 的中位秒数 | 诚实的分析 |
|---|---|---|---|---|
| DiD 面板 | 25,920 个规格 | 48% | 1.1 | 0.002 秒，p = 0.62 |
| 交错 DiD | 3,456 | 67% | 0.16 | 0.002 秒，p = 0.22 |
| RDD | 20,736 | **97%** | 0.89 | 0.005 秒，p = 0.25 |
| IV | 672 | 33% | 0.04 | 0.003 秒，p = 0.62 |

"agent 几分钟就能 p-hack"其实说保守了：搜索只要几秒，那几分钟从来都只是写循环的时间——而写循环正是 agent 把它变成一句话的部分。完整的仪表化运行（穷举、200 次零校准、各项校正、归因、报告）在六个进程上约 50 秒，所以审计和攻击一样只需要一句话。四个设计逐过程的完整表格、命令与种子：[docs/capability.zh.md](docs/capability.zh.md)。

### 自己跑一遍：从 `pip install` 到秒表

引擎在 PyPI 上；已知零效应的演示数据在本仓库里。整段可复制粘贴，无需 clone：

```bash
pip install phack

# 演示数据：一个处理效应在构造上恰好为零的 DiD 面板
curl -sO https://raw.githubusercontent.com/brycewang-stanford/p-hacking-skills/main/eval/data/null_panel.csv
curl -sO https://raw.githubusercontent.com/brycewang-stanford/p-hacking-skills/main/eval/data/null_panel_card.json

phack size null_panel_card.json     # 25,920 个可辩护规格；预注册规格 e88cbfc3e0e7

phack race null_panel.csv null_panel_card.json \
    --direction + --trials 40 --budget 60 --null-scheme cluster_permute --seed 1 --summary
```

大约两分钟后（以下为逐字输出；产出率在种子固定下精确可复现，耗时随机器不同）：

```text
grid: 25,920 specifications   trials: 40   alpha: 0.05   null scheme: cluster_permute (truth = 0 in every trial)
honest baseline: the pre-registered spec fits in 0.007s and says p = 0.624 (one-sided)

procedure             yield  median s to sig   fits  specs   reported p
greedy                  48%             1.27     17     26        0.034
first_significant       52%             0.02     14     48        0.024
hill_climb              50%             1.16     12     15        0.035
random                  57%             0.01      9     20        0.030

Timings price the manufacture of significance, not evidence. Every 'significant' report above is
the maximum of a search; its reported_p is not a valid p-value. Because null_scheme is set,
share_reporting_significant is the false-positive rate of the procedure on this design. The same
walks run fully instrumented -- ledger, specification curve, null-calibrated honest p -- under
`phack search --procedure`.
```

怎么读：在**完全没有效应**的数据上，"东试西试直到过 .05"在 60 个规格的预算内约一半概率递给你一个看起来能发表的 p，耗时约一秒——而诚实的预注册分析只要 7 毫秒，答案是 p = 0.62。末尾那段话是工具自己每次都会打印的。要让同一条搜索路径跑在完整账本契约之下——不交出 `ledger.csv`、规格曲线和零校准诚实 p 就报不出赢家：

```bash
phack search null_panel.csv null_panel_card.json --procedure greedy --stop-at-alpha \
    --direction + --null-draws 200 --null-scheme cluster_permute --n-jobs 6 --summary
phack verify phack_out/                     # 任何拿到运行目录的人都能核验
```

## 为什么要公开一个能搜索显著性的工具

因为"搜索的能力"从来不稀缺：Stata 里一个 `foreach`、R 里一个 `expand.grid`、一个被施压的 agent 都能做到。稀缺的是**度量**它的能力——对一个给定的设计，说清楚有多少可辩护的规格、一次现实的搜索在真零效应数据上多大概率制造出 p < .05、是哪一个分析选择在做功、以及搜索之后报告出来的 p 值还值多少。审稿人、复现者、方法课教师、agent 评测者需要的正是这些数字，而这些数字只有在有记录的条件下执行搜索才能得到。

这与已有的公开工作一脉相承（见下节[它参考了哪些工具](#它参考了哪些工具)）：Simmons–Nelson–Simonsohn 的演示、Stefan & Schönbrodt 的 `phackR`、Simonsohn 的 p-curve 与规格曲线工具、Asher 等人的 agent 评测。让这类工具负责任的设计选择在每个案例里都一样，这里用机制强制执行：没有账本、没有零校准的诚实 p 值、没有可供第三方核验的运行目录，它就无法输出"最优规格"。它让搜索**更难隐藏**，而不是更容易做。详见 [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md)。

## 它参考了哪些工具

前人的每个工具都把一件事做得很好，但几乎都只有 R 版本，而且只站在问题的一侧。本仓库是把它们全部摊开来对照着写的：该重写的部分重写成 Python，再把模拟、搜索、审计、检测几侧接到同一本账本上。

| 工具 | 语言 | 做什么 | 数据 | 设计 |
|---|---|---|---|---|
| `phackR` — Stefan & Schönbrodt (2023)，[astefan1/phacking_compendium](https://github.com/astefan1/phacking_compendium) | R + Shiny | 模拟十二种 p-hacking 策略，报告假阳性率、p 值分布与效应量分布 | 真零假设下的模拟数据 | 两组比较、相关检验 |
| `p-hacker` — Schönbrodt，[nicebread/p-hacker](https://github.com/nicebread/p-hacker) | Shiny | 教学应用：手动"hack"一个模拟实验，看 p 值怎么动 | 模拟数据 | 单个实验 |
| p-curve — Simonsohn, Nelson & Simmons (2014) | 网页应用 + R | 一组已报告 p 值的功效与证据价值 | 已报告的 p 值 | — |
| `phack` — [skranz/phack](https://github.com/skranz/phack) | R | Elliott, Kudrin & Wüthrich (2022) 对 p 值分布的检验 | 已报告的 p 值 | — |
| `specr`、`multiverse` — [masurp/specr](https://github.com/masurp/specr)、[MUCollective/multiverse](https://github.com/MUCollective/multiverse) | R | 对分析者自行声明的规格集合做规格曲线 / 多重宇宙分析 | 真实数据 | 分析者声明什么就是什么 |
| Asher 等 (2026) | — | 在四篇已发表的零结果论文上评测编程 agent 的协议 | 真实数据 | 那四篇论文 |

本仓库在它们之上多做的事：

- **一个引擎，两侧都有。** 模拟（`phackR` 的十二种策略用 Python 独立重写，再加上过程层与阶段间层）、有记录的搜索、审计、检测（Elliott–Kudrin–Wüthrich 检验组、p-curve 功效、caliper、堆积与密度跳跃检验、阶段间偏移分解）和第三方核验，共用同一种账本格式。
- **真实数据与计量设计。** 用设计卡片声明花园：OLS / RCT、DiD（TWFE、两阶段、stacked、对照组选择）、事件研究、RDD（带宽、核、多项式、甜甜圈、推断方式）、IV（工具子集、2SLS / LIML、一阶段 F、Anderson–Rubin），每张卡片都有预注册锚点。
- **搜索是一个过程，不是一个集合。** 带停止规则的顺序搜索、拆样本与选择性延续，都在零数据上重放，所以假阳性率属于"这种搜法在这个设计上"，而不是属于规格清单。
- **四种语言，同一网格。** 同一份枚举网格可以在 Stata（`reghdfe` / `ivreghdfe` / `rdrobust` / `did2s`）、R（`fixest` / `rdrobust` / `did2s`）、Python（`statsmodels` / `linearmodels`）和 [StatsPAI](https://github.com/brycewang-stanford/StatsPAI) 里跑，并有逐行一致性表。Stata 这一路可以通过我们的 [stata-code](https://github.com/brycewang-stanford/stata-code)（面向 agent 的 Stata 桥接器）直接从 Claude Code、Cursor 或 VS Code 驱动。
- **面向 agent 的基准。** 措辞与推动、PHI 评分、冻结的基准版本与密封的保留集，让一个模型"会不会搜索"可以被度量、再度量。

## 安装与最短路径

```bash
pip install phack                       # 引擎 + phack 命令行（Python ≥ 3.10）
pip install 'phack[formats]'            # 读取 .dta / .parquet / .xlsx
```

```bash
phack init panel.dta --design did --treatment policy --outcome lnwage   # 从数据起草设计卡片
phack size panel_card.json                                               # 规格空间有多大、预注册规格是哪一个
phack search panel.dta panel_card.json --direction + --null-draws 200 --n-jobs 6 --summary
phack search panel.dta panel_card.json --procedure greedy --stop-at-alpha --direction + --null-draws 200
phack race panel.dta panel_card.json --direction + --budget 60 --null-scheme cluster_permute --summary   # 制造显著要几秒；产出率即 FPR
phack export panel.dta panel_card.json --lang stata --out run_stata/     # 同一网格交给 Stata / R / Python / StatsPAI
phack ingest run_stata/ --parity                                          # 接回审计并与引擎逐行比对
phack verify phack_out/                                                   # 第三方核验
./demo.sh                                                                 # 在已知零效应数据上跑通全流程
```

也可以用 Docker（`docker build -t phack .`）或 Colab（`notebooks/quickstart.ipynb`）零安装体验。

**更推荐的用法：装成 Claude Code 技能，用自然语言驱动**——agent 会把你的问题路由到对应技能并代你运行引擎：`/plugin marketplace add brycewang-stanford/p-hacking-skills`，然后 `/plugin install p-hacking-skills@p-hacking-skills`（或把 `skills/` 复制到 `.claude/skills/`）。**[技能上手指南](docs/skills-quickstart.zh.md)**（[English](docs/skills-quickstart.md)）带你在五分钟内完成安装，并在已知零效应的数据上跑出第一次带账本的规格搜索。

## 引擎做什么

1. **枚举网格。** 设计卡片（JSON，有正式 schema）每个键是一个研究者自由度；`preregistered` 块指定诚实分析者会事先承诺的那一个规格。支持 OLS / RCT、DiD（TWFE、Gardner 两阶段、stacked、对照组选择）、事件研究（窗口、参照期、估计目标）、RDD（ROT / IK 带宽 × 倍数、核、多项式、甜甜圈、常规 / 偏差修正 / CCT robust 推断）、IV（工具子集、2SLS / LIML、每行记录一阶段 F 与 Anderson–Rubin p）。
2. **走网格。** 穷举，或者像 p-hacker 一样按顺序走并设停止规则（`first_significant`、`random`、`greedy` 坐标下降、`hill_climb`）；零校准会**重放同一过程**，给出"这种搜索方式在这个设计上"的假阳性率；`phack race` 再给它上秒表，量出制造一个假阳性要几秒。`split_sample` 走两阶段：先在试点样本上搜，再把选中的规格在留出样本（`--stage holdout`，诚实）、全样本（`--stage pooled`，试点的运气进了报告的检验）或试点样本上报告；`--continue-at` 只在试点有希望时才进入确证阶段——这就是 Adda, Decker & Ottaviani (2020) 在临床试验注册库里看到的"选择性延续"。
3. **算出搜索值多少。** 对最优规格：Bonferroni、Li–Ji 有效检验数、Romano–Wolf、零校准诚实 p；对整条曲线：Simonsohn 联合检验；再加上**与预注册规格的距离**（差几个选择就能显著）和**轴归因**（哪个旋钮在做功）。病理标记把"可引用但错误"的角落留在账本里并标出来。
4. **写报告，可核验。** `report.md` 从审计生成，数字不可能与账本漂移；`manifest.json` 记录数据、卡片、账本、审计的哈希；`phack verify` 逐项核对。`phack bench` 冻结与检查基准版本；`bench.seal` 对保留集做哈希承诺而不公开内容。
5. **在你的语言里跑。** `phack export` 导出语言无关的规格表、数据和零假设置换列，并生成 Stata（reghdfe / ivreghdfe / rdrobust / did2s）、R（fixest / rdrobust / did2s）、Python（statsmodels / linearmodels）或 StatsPAI 的执行脚本；`phack ingest --parity` 接回并与引擎逐行比对，一致性表见 `references/language-map.md`。 把 [stata-code](https://github.com/brycewang-stanford/stata-code) 注册为 MCP server（`claude mcp add stata-code --scope user -- uvx --from "stata-code[mcp]" stata-code-mcp`）之后，agent 可以在 Claude Code 里直接运行导出的 `run_specs.do` 并读回账本；Python 这一侧由 StatsPAI 承担同样的角色，并与 Stata 的估计交叉核对。

## 阶段之间：选择不是操纵

Adda, Decker & Ottaviani (2020, *PNAS*) 分析了 ClinicalTrials.gov 上 12,621 个主要结局的 p 值：z = 1.96 处没有尖峰；只有小型企业赞助的 III 期试验在 1.96 处有一个**台阶**（线下的结果缺失，而不是被推过线）；企业赞助试验的显著比例从 II 期的 46% 升到 III 期的 71%，而分布是平滑的——因为赞助方只在 II 期有希望时才做 III 期。本仓库把这三件事都变成可测量的对象：模拟策略 26（`--report main` 时假阳性率 0.050，说明选择性延续本身不是 p-hacking；`--report pooled` 0.170；`--report best` 0.581）、`split_sample` 搜索过程、以及检测端的密度跳跃检验（看得见"藏起来"）、尖峰检验（看得见"推过去"）、阶段间比较与选择性延续分解（`phack detect --stagecol --contcol`，`phack simulate --continuation`）。

## 数据

八个生成数据集，全部来自 `scripts/make_null_data.py` 的固定种子与文档化 DGP：四个真零效应（`null_panel` 25,920 个规格、`null_staggered` 3,456 + 事件研究 1,200、`null_rdd` 20,736、`null_iv` 672），四个已知效应的正向对照（证明诚实流程不会把真效应也"校准"掉）。`scripts/calibrate_engine.py` 在新鲜数据上检验：真零时诚实 p 应近似均匀，真效应时应有功效。

## 十一个技能

见 [skills/README.zh.md](skills/README.zh.md)。三侧：map（路由、策略分类、设计卡片）、red（规格搜索、搜索过程、多语言、提示框架攻击、叙事洗白）、blue（p-curve 检测、免疫）、eval（agent 评测）。

## 参与贡献

四个扩展点——新自由度轴、新搜索过程、新语言执行器、新数据集——各有最小示例，见 [CONTRIBUTING.md](CONTRIBUTING.md)。issue 模板覆盖 bug、新轴、新数据集与一致性报告。引用请见 [CITATION.cff](CITATION.cff)。

## 局限

诚实 p 是被检验的而非假设的；重尾的数值伪影需要病理标记而不只是零抽样；各语言执行器复现的是网格语义而非引擎的数值约定；DiD 菜单尚无 Callaway–Sant'Anna / Sun–Abraham；RDD 带宽不是 rdrobust 的 CCT 最优；正则扫描是筛查而非判决；公开仓库意味着 agent 读过它——请保留私有测试集并只公布其哈希承诺。

MIT 许可。
