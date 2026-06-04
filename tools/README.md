# Tools — 自动化实证研究 & 因果推断工具库

> A curated, license- and maintenance-aware index of **software tools** for automated
> empirical research and causal inference.

这是 AERS 的**工具（tools）模块**，与 [`../skills/`](../skills/)（喂给 agent 读的指令包 / agent skills）是两种不同的东西：

- **Skill** = 写给 agent 看的"怎么做研究"的指令与参考资料。
- **Tool** = agent（或研究者）实际**调用的外部软件 / 服务**——因果推断库、计量库、因果发现包、MCP 数据服务、基准数据集。

把工具单列一个模块，是为了不破坏 `skills/` 目录与其 catalog 的语义；本模块沿用 repo 既有工程规范（结构化 JSON 事实源 + 生成式浏览视图 + 接入 `make validate`）。

---

## 速览 / At a glance

<!-- BEGIN GENERATED: summary (scripts/build-tools-catalog.py) -->

**251 tools** across 6 categories.

| Category | Count |
|---|---:|
| Causal-inference & treatment-effect libraries | 32 |
| Econometrics & quasi-experimental libraries | 86 |
| Causal discovery / structure learning | 25 |
| Autonomous research & data-science agents | 51 |
| MCP servers (data & stats execution) | 48 |
| Benchmarks & datasets | 9 |

| By language | Tools | | By maintenance | Tools | | By license | Tools |
|---|---:|:-:|---|---:|:-:|---|---:|
| Python | 147 |  | 🟢 active | 142 |  | permissive (MIT/BSD/Apache/…) | 161 |
| R | 65 |  | 🟡 maintained | 75 |  | copyleft (GPL/AGPL/LGPL) | 50 |
| Stata | 36 |  | 🔴 dormant | 34 |  | unverified / unmapped | 37 |
| TypeScript | 16 |  |  |  |  | non-OSI / custom | 3 |
| Julia | 7 |  |  |  |  |  |  |
| C++ | 5 |  |  |  |  |  |  |
| Java | 3 |  |  |  |  |  |  |
| JavaScript | 3 |  |  |  |  |  |  |

<!-- END GENERATED: summary -->

完整可浏览清单（按类目分组、可点击、含语言/许可/维护状态）见 **[CATALOG.md](CATALOG.md)**；机器可读事实源见 **[tools.json](tools.json)**。

---

## 收录范围 / Scope

本模块当前覆盖 6 个类目：

1. **因果推断库 / 处理效应库（`causal-inference-library`）** — DoWhy、EconML、CausalML、DoubleML、CausalPy、causallib、grf、CATENets、TMLE 系列、Mendelian randomization 等。
2. **计量 / 准实验库（`econometrics-library`）** — 面板/固定效应、DiD（含 staggered/现代 DiD）、事件研究、断点回归 RDD、工具变量 IV、合成控制 SCM/SDID、匹配/加权、敏感性分析；覆盖 R / Python / Stata / Julia（fixest、did、HonestDiD、rdrobust、synthdid、reghdfe、csdid、sdid、pyfixest、linearmodels、FixedEffectModels.jl 等）。
3. **因果发现 / 结构学习（`causal-discovery`）** — causal-learn、Tetrad/py-tetrad、gCastle、CDT、tigramite(PCMCI)、LiNGAM、NOTEARS/DAGMA、pcalg、bnlearn、pgmpy 等。
4. **自动化研究 / 数据科学 Agent（`research-agent`）** — 端到端自动做科研/数据分析的系统：AI-Scientist、data-to-paper、Agent Laboratory、RD-Agent、AI-Researcher、STORM、PaperQA2、gpt-researcher、DeepAnalyze、MetaGPT(Data Interpreter)、Biomni 等。⚠️ 许可注意：SakanaAI AI-Scientist 用自定义 Responsible-AI 许可（非 OSI），部分仓库无 LICENSE（标 `unverified`）——用前务必到上游确认授权。
5. **MCP 服务（`mcp-server`）** — 供 agent 直接调用的统计执行与数据获取服务（StatsPAI、stata-mcp、R/Jupyter MCP、FRED、World Bank、IMF、OECD、Eurostat、Census、BEA、BLS、SEC EDGAR、OpenAlex、Semantic Scholar、PubMed、Zotero、arXiv 等）。
6. **基准与数据集（`benchmark-dataset`）** — causaldata、IHDP/Twins、ACIC 竞赛数据、RealCause、JustCause、Tübingen cause-effect pairs、bnlearn 网络库等，用于评估因果方法（已知 ground truth）。

---

## 怎么用 / How to use

这是一个**索引/目录**，不 vendor 上游源码（这些库体量大、各有安装方式）。典型用法：

- **找库**：在 [CATALOG.md](CATALOG.md) 按类目/语言筛选，点链接到上游仓库；按其文档 `pip install` / `install.packages` / `ssc install` / `]add`。
- **接 MCP**：MCP 服务条目的 `url` 指向其仓库，按各自 README 配置到 Claude / Codex / Cursor 等客户端（本 repo 根目录已配置了 `statspai`、`stata-mcp`、`fred-mcp-server` 等可作参考）。
- **程序化消费**：直接读 [tools.json](tools.json)，按 `category` / `languages` / `maintained` / `license` 字段过滤。

> 想要"开箱即用、端到端跑通"的托管流水线，可参考 [copaper.ai](https://copaper.ai)（与本目录同一 Stanford 方法学团队构建）。

---

## 字段说明 / Schema

`tools.json` 是事实源（`{ "tools": [ … ] }`），每条记录字段如下：

| 字段 | 说明 |
|---|---|
| `id` | 稳定 slug（由 name 生成，唯一） |
| `name` | 工具名 |
| `category` | `causal-inference-library` / `econometrics-library` / `causal-discovery` / `research-agent` / `mcp-server` / `benchmark-dataset` |
| `subcategory` | 方法标签（如 `did`、`rdd`、`uplift`、`time-series`、`economic-data` …） |
| `languages` | `python` / `r` / `stata` / `julia` / `typescript` / … |
| `license` | SPDX 标识；`unverified` = 上游无正式 LICENSE（多见于 Stata SSC 包）；`NOASSERTION` = GitHub 检测到但无法映射 |
| `owner_repo` · `url` · `homepage` | 来源定位 |
| `stars_approx` · `last_activity` · `maintained` | 维护信号快照（`active` ≈ 近半年有提交 · `maintained` ≈ 近两年 · `dormant` ≈ 更早） |
| `automation_level` | `library` / `framework` / `application` / `mcp-server` / `dataset` |
| `data_source` | 仅 MCP 条目：它服务的数据源 |
| `verified` | 收录时是否实际访问仓库核实过 license/活跃度 |

---

## 取舍标准与免责 / Selection & caveats

收录门槛（与 [`../docs/SKILL_SUBMISSION_GUIDE.md`](../docs/SKILL_SUBMISSION_GUIDE.md) 对齐）：开源且可独立运行/检视；与实证研究、因果推断、数据获取相关；有可用的来源 URL。

- **快照性质**：`stars_approx` / `last_activity` 为收录当次（2026-06）的时间点快照，会过时——依赖前请到上游确认。
- **license 核实**：每条都已实际访问仓库核实（`verified: true`）。约 37 条标 `unverified`/`NOASSERTION`（无正式 LICENSE 的 Stata SSC 包、未声明许可证的部分 MCP/agent 仓库）；另有 3 条**非 OSI/自定义许可**——SakanaAI **AI-Scientist / v2**（自定义 Responsible-AI 行为约束许可）与 **Coscientist**（Apache-2.0 + Commons Clause，禁商用）。依赖前务必到上游确认授权。
- **收录 ≠ 背书**：本目录不对第三方工具的正确性、安全性或适用性作保证。

---

## 贡献 / Contributing

新增或修订一个工具：

1. 编辑 [`tools.json`](tools.json)，按 schema 增删字段（`category` 必须在枚举内）。
2. 运行 `python3 scripts/build-tools-catalog.py` 重新生成 [`CATALOG.md`](CATALOG.md) 与本文「速览」区块。
3. 运行 `make validate`（含 `build-tools-catalog.py --check`）确认无 schema 错误、生成视图无漂移。

> 不要手改 `CATALOG.md` 或本文「速览」标记区块之间的内容——它们是生成的，会被覆盖。
