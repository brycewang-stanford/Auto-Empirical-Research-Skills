# 当成 Claude Code Skills 来用：五分钟上手

这套仓库最自然的用法不是记 CLI 参数，而是把它装成 **agent 的技能**：你用自然语言描述数据和问题，agent 自动路由到对应技能，调用底层的 `phack` 引擎，把账本、规格曲线和诚实 p 值一起交回来。本文是这条路径的最短使用说明。

> **用途说明（先读这个）。** 这套技能用于学术研究讨论与教学、以及评测 AI 科研 agent 是否会 p-hacking，**不用于真实的论文写作或科研项目**。它被设计成"想 hack 也藏不住"：每次搜索必然留下完整账本和零校准的诚实 p 值，任何第三方都能用 `phack verify` 核验。你可以在这里放心地*体验* p-hacking——在真实效应恰好为零的数据上，亲眼看着 p = 0.001 被搜出来，再看它的诚实 p 值是多少。

## 1. 安装（两分钟，两个部件）

**技能层**（二选一）：

```text
# 方式 A：在 Claude Code 里作为插件安装（推荐，含全部 11 个技能）
/plugin marketplace add brycewang-stanford/p-hacking-skills
/plugin install p-hacking-skills@p-hacking-skills

# 方式 B：手动复制（适用于任何读 SKILL.md 约定的 agent，包括 Codex 等）
git clone https://github.com/brycewang-stanford/p-hacking-skills
cp -r p-hacking-skills/skills/* ~/.claude/skills/      # 全局
# 或复制到某个项目的 .claude/skills/ 下，仅该项目可用
```

**引擎层**（技能会调用它）：

```bash
pip install phack                    # Python >= 3.10
pip install 'phack[formats]'         # 可选：读 .dta / .parquet / .xlsx
# 或从 clone 安装：pip install -e ".[dev]"
```

可选增强：注册 [stata-code](https://github.com/brycewang-stanford/stata-code) MCP（`claude mcp add stata-code --scope user -- uvx --from "stata-code[mcp]" stata-code-mcp`），agent 就能直接执行导出的 Stata 网格并把账本读回来。

验证：在 Claude Code 里问一句"你有哪些 p-hacking 技能？"，或者跑 `phack --help`。

## 2. 第一次体验：在真值为零的数据上 hack 一把（五分钟）

仓库自带构造上真实效应**恰好为零**的沙盒数据（`eval/data/null_panel.csv` 及其设计卡片）。这是安全的试验场——不管你搜出多显著的结果，你都知道真相是 0。把下面的话直接说给 agent：

> **"用 eval/data/null_panel.csv 和 eval/data/null_panel_card.json，帮我找到最显著的正向规格。"**

agent 会走 `specification-search` 技能：枚举上万个"都说得过去"的规格，报出最佳规格的 p 值（通常在 0.001 量级）——同时**必然**附上账本、规格曲线、Bonferroni / Romano–Wolf 校正、以及零校准的诚实 p 值（通常在 0.5 以上）和通胀倍数。接着追问：

> **"这个 p = 0.001 是真的吗？是哪些分析选择在起作用？"**

audit 会告诉你轴归因：vcov、样本窗口、估计量选择各自贡献了多少显著性。再体验一次"真人怎么搜"：

> **"像一个真实的研究者那样搜：从预注册规格出发做贪心坐标下降，一到 p < 0.05 就停。然后告诉我：这种搜索方式本身，在零效应数据上的假阳性率是多少？"**

这会走 `search-procedures` 技能——把同一套搜索程序在几十份零效应数据上重放，得到属于*这种搜法*的 FPR 和过程诚实 p。最后，给它上秒表：

> **"在这个设计上制造一个假阳性要多快？把各种搜索过程拿来竞速，给我一张价目表。"**

这就是 `phack race`：每种搜索过程在新鲜的零抽取上对着时钟跑，产出率**就是**它的假阳性率，而"到显著的中位秒数"就是"agent 几分钟就能 p-hack"这句话被量出来的样子——在这个面板上是几秒而不是几分钟，而诚实的分析比它还快（[实测数字](capability.zh.md)）。

不想打字的话，`./demo.sh` 一条命令跑完全部十步（含竞速、RDD、交错 DiD、检测、agent 打分、跨语言一致性）。

## 3. 在自己的数据上（教学 / 方法研究）

```text
"我有 panel.dta，处理变量是 policy，结果变量是 lnwage，DiD 设计。
 这个设计里有多少研究者自由度？预注册规格应该是什么？"
```

agent 走 `forking-paths`：起草设计卡片（`phack init`）、算出规格空间大小（`phack size`）、标出预注册锚点。然后：

```text
"在这份数据上跑一次带完整账本的规格搜索，200 个零抽样，给我诚实报告。"
"把同一张网格导出成 Stata 跑一遍，检查和 Python 引擎逐行一致。"   → phack-polyglot
```

记住契约：**技能不会只报 winner**。要求隐藏账本、或把搜出来的规格当确证性检验来写，技能会拒绝——这是设计使然。

## 4. 蓝方：检测与免疫

```text
"这是我从某文献整理的 400 个 z 值（lit.csv），它们有被 p-hack 的迹象吗？"
```

→ `phack-detection`：Elliott–Kudrin–Wüthrich 检验组、p-curve 功效、caliper、聚束、阈值密度跳跃，并区分"结果被推过线"与"线下结果被藏起来"。

```text
"帮我把这个分析免疫掉 p-hacking：卡片当预分析计划、拆样本、盲化，最后出诚实报告。"
```

→ `phack-immunization`。

## 5. 评测一个 agent 会不会 p-hack

```text
"用 eval harness 评测 <某模型/某 agent>：2 种框架 × 7 种压力 × 4 种设计，给出 PHI 分数。"
```

→ `phack-eval-harness`，含冻结基准版本与密封的留出卡片，可重复测量。`framing-attacks` 技能单独提供七级提示框架的探针（Asher et al. 2026 的"上界估计"重构就在其中）。

## 6. 哪个问题找哪个技能

| 你想问的 | 技能 |
|---|---|
| 这套东西怎么用 / 我该找谁 | `phack-router` |
| 有哪些 p-hacking 手法，各自能买到多少假阳性 | `phack-taxonomy` |
| 我的设计里有多少自由度、规格空间多大 | `forking-paths` |
| 帮我搜最显著的规格（带账本） | `specification-search` |
| 真人的搜索过程值多少假阳性率 | `search-procedures` |
| 制造一次显著要多少秒（`phack race`） | `search-procedures` |
| 同一网格在 Stata / R / Python / StatsPAI 跑 | `phack-polyglot` |
| 什么样的措辞会让 agent 从拒绝变成执行 | `framing-attacks` |
| 搜出来的结果是怎么被写成"发现"的 | `narrative-laundering` |
| 这批 p 值被 hack 过吗 | `phack-detection` |
| 怎么让我的分析免疫 | `phack-immunization` |
| 这个 agent 会不会 p-hack | `phack-eval-harness` |

## 7. 每次搜索留下什么（第三方可核验）

运行目录里固定有：`ledger.csv`（每一个试过的规格）、规格曲线图、`audit.json`（全部校正与归因）、`report.md`（由这些数字生成的诚实报告）。任何人拿到目录都可以：

```bash
phack verify RUN_DIR      # 哈希、账本一致性、零抽样、报告引文、全量重算
```

这就是"能 p-hack 的工具，同时是让 p-hacking 现形的工具"。
