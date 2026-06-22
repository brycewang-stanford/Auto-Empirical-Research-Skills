# StatsPAI Skill for Claude Code

This folder is a **Claude Code Skill** that teaches Claude (or any
compatible agent harness) how to drive [StatsPAI](https://github.com/brycewang-stanford/StatsPAI)
end-to-end through a full causal-inference / empirical analysis,
covering **three domain modes** that share the same export stack
and `CausalResult` interface:

- **Default — Applied Econ (AER / QJE / AEJ).** The canonical 8-section
  empirical paper: pre-analysis plan, Table 1 summary statistics,
  written-out estimating equation + identifying assumption,
  identification graphics (event-study / first-stage F / McCrary /
  SCM trajectory / love plot), the AER multi-regression Table 2
  gauntlet (progressive controls / design horse-race / multi-outcome
  / IV first-stage triplet), heterogeneity (subgroup table + CATE
  figure), mechanisms, and a full robustness battery (placebo /
  Oster / honest_did / E-value / Conley / two-way SE / spec curve /
  sensitivity dashboard) — ending in a single editable Word / Excel
  / LaTeX replication bundle.
- **Mode A — Epidemiology / public health (§A).** Target-trial
  emulation, IPTW + g-formula + TMLE doubly-robust triplet,
  Mendelian randomization (IVW / Egger / weighted median), KM / AFT
  survival, E-value sensitivity, principal stratification — under
  STROBE / TRIPOD reporting conventions.
- **Mode B — ML causal inference (§B).** DML, S/T/X/R/DR
  meta-learners, causal forest (GRF), Dragonnet / TARNet / CEVAE
  neural causal, BCF, matrix completion, CATE distribution + policy
  tree + off-policy evaluation, conformal causal prediction,
  fairness audit, and DAG learning (PC / NOTEARS / LLM-assisted).

All three modes reuse the same Word / Excel / LaTeX export stack
and the estimand-first `sp.causal_question(...).identify()` DSL —
switching modes only changes which Step-4 estimators you reach
for, not the surrounding scaffolding.

## SkillOpt-style improvements

This skill now treats the playbook as a validation-gated operating policy,
inspired by [SkillOpt](https://github.com/microsoft/SkillOpt): route the task,
freeze the analysis contract, execute the smallest verified call shape, widen
one block at a time, and accept the final answer only after the requested
artifacts or blocking gates are concrete.

The high-level rules live near the top of `SKILL.md`:

- **Mode routing before code.** Narrow export requests stay narrow; AER, epi,
  and ML-causal work enter their own pipelines.
- **Artifact gates.** DID, IV, RD, matching, epi, ML-causal, and Stata/R
  migration tasks each have minimum diagnostics before the agent may call a
  result paper-ready.
- **Bounded repair.** Signature errors, optional-extra misses, result-type
  mismatches, and plot return-shape mistakes are fixed as local rule updates,
  not broad pipeline rewrites.
- **Future maintenance rule.** Edits to this skill should be small
  add/delete/replace changes accepted only when they address a concrete failure
  case without regressing the verified skeleton, export cookbook, or Common
  Mistakes table.
- **Runnable validation gate.** [`validate_api_claims.py`](validate_api_claims.py)
  turns SkillOpt's "edits pass only if they survive a validation gate" into a
  command you can run: it parses `SKILL.md`, then checks every `sp.*` reference,
  the documented argument names, and the result-object attribute claims against
  the **installed** `statspai` (smoke fits included). It exits non-zero on drift,
  so it doubles as a CI check. Re-run it whenever you bump the pinned version or
  edit an API claim:

  ```bash
  python validate_api_claims.py          # full gate (exits 1 on drift)
  python validate_api_claims.py --quick  # existence + signatures only, no fits
  ```

  This is how the skill was re-validated from `1.16.1` to `statspai 1.19.0`: the
  gate caught one real drift — `AFTResult` gained `.params`, so `sp.regtable(aft)`
  now works directly and the old "hand-build a DataFrame" workaround was removed. `EVALS.md` provides the held-out gate cases for that check.

## What this skill ships (paper-ready, in three formats)

Every numbered table in the AER pipeline emits parallel
**`.docx` + `.xlsx` + `.tex`** (Markdown / HTML on demand) so
co-authors can edit in Word, journal editors can review in Excel,
and the build system can assemble LaTeX — all from one source.

| Tier | When | API |
| --- | --- | --- |
| **1. Single multi-column table** (Stata `outreg2` / R `modelsummary` equivalent) | One Table 2 / Table 3 / Table A1 with progressive columns | `rt = sp.regtable(M1, M2, ..., template="aer", title=...)` then `rt.to_word("table2.docx") · rt.to_excel("table2.xlsx") · rt.to_latex()` |
| **2. Multi-panel paper format** | Tables 2 + 3 + A1 + A2 in one document | `sp.paper_tables(main=, heterogeneity=, robustness=, placebo=, template="aer").to_docx("paper_tables.docx")` |
| **3. Full session bundle** (Stata 15 `collect` equivalent) | Replication appendix mixing summary + balance + multiple regression tables + headings + prose | `sp.collect("Paper").add_summary(...).add_balance(...).add_regression(...)...save("paper.docx")` (auto-detects `.docx`/`.xlsx`/`.tex`/`.md`/`.html`) |

Journal templates auto-apply the right SE label, star levels, and
footer notes:

```python
sp.list_journal_templates()
# → ('aer', 'qje', 'econometrica', 'restat', 'jf', 'aeja', 'jpe', 'restud')

rt = sp.regtable(M1, M2, M3, template="qje")     # QJE styling
rt.to_word("table2_qje.docx")
```

Inline citations drop a coefficient straight into prose:

```python
sp.cite(M3, "training")           # → "1.239*** (0.153)"
```

## Default behavior the agent enforces

| Convention | Default action | When to override |
| --- | --- | --- |
| **Show every estimated parameter verbatim** (controls AND intercept) | `sp.regtable(*models, template="aer", ...)` with NEITHER `keep=` NOR `drop=` | Add `drop=["Intercept"]` to suppress the constant; `keep=[focal]` for intentionally focal-only tables (IV first-stage triplet, interaction-form heterogeneity) |
| **Route FE regressions through `sp.feols`** (pyfixest backend) | `sp.feols("y ~ x \| firm_id + year", df, vcov={"CRV1": "firm_id"})` | `sp.regress` for pure OLS only — it does **NOT** parse `\|` as FE |
| **Two-way cluster** | `sp.feols(..., vcov={"CRV1": "firm_id+year"})` | `sp.twoway_cluster(...)` is for `sp.regress` / `sp.ivreg` (statsmodels) results only |
| **Always export Word + Excel + LaTeX in parallel** | `rt.to_word(...) · rt.to_excel(...) · open(...).write(rt.to_latex())` | Skip `.tex` if you're not building a journal manuscript; always include `.docx` for human review |

## Install

```bash
# Option 1: copy
cp -r StatsPAI_full_data_analysis_skill ~/.claude/skills/StatsPAI_skill

# Option 2: symlink (auto-follow upstream updates)
ln -s "$(pwd)/StatsPAI_full_data_analysis_skill" ~/.claude/skills/StatsPAI_skill
```

Then install the Python package itself (API surface verified against **statspai 1.19.0** via `validate_api_claims.py`):

```bash
# Recommended — covers the default pipeline (high-dim FE + figures):
pip install "statspai[fixest,plotting]"

# Full skill (adds neural causal + text-as-treatment):
pip install "statspai[fixest,plotting,neural,text]"
```

> The bare `pip install statspai` does **not** pull `pyfixest` (needed by `sp.feols`, the default for any `y ~ x | fe` regression — it raises `ImportError` without it), matplotlib (any figure), or torch (`dragonnet`/`tarnet`/`cevae`). See the dependency matrix at the top of `SKILL.md`.

## Activate

The skill auto-activates on natural-language triggers — pick the wording
that matches your domain and the right sub-pipeline kicks in:

- **Default (AER econ)** — *"run a DID analysis"*, *"AER empirical
  analysis"*, *"applied microeconomics pipeline"*, *"instrumental
  variables regression"*, *"event-study plot"*, *"first-stage F"*,
  *"Oster bound"*, *"export regression table to Word"*, *"outreg2
  in Python"*, *"sp.collect"*, *"sp.feols"*, *"estimand-first DSL"*.
- **Mode A (epi / public health)** — *"target trial emulation"*,
  *"g-formula"*, *"IPTW"*, *"TMLE"*, *"HAL-TMLE"*, *"Mendelian
  randomization"*, *"MR-Egger"*, *"E-value"*, *"Kaplan-Meier"*,
  *"AFT survival"*, *"STROBE"*, *"TRIPOD-AI"*, *"流行病学"*, *"公共健康"*,
  *"RWE / cohort study"*.
- **Mode B (ML causal)** — *"DML"* / *"double machine learning"*,
  *"meta-learner"*, *"causal forest"*, *"Dragonnet"*, *"TARNet"*,
  *"CEVAE"*, *"BCF"*, *"CATE"*, *"policy tree"*, *"off-policy
  evaluation"*, *"conformal causal"*, *"fairness audit"*,
  *"causal discovery"* / *"DAG learning"*, *"NOTEARS"*, *"PC algorithm"*,
  *"因果机器学习"*, *"uplift modeling"*.

Mixed phrasing such as *"estimate DID and then ML CATE on the
heterogeneity"* triggers Default + Mode B in sequence — every
estimator returns the same `CausalResult`, so you can drop
econ + ML estimators into one `sp.regtable(...)` for a horse-race
column. See the `triggers:` block in `SKILL.md` for the full list.

## Scope

**In scope** — three parallel sub-pipelines, each ending in a
`CausalResult` that drops into the same Word / Excel / LaTeX export
stack:

```text
Default (AER econ) — the canonical 8-section pipeline:
§-1 Pre-Analysis Plan      →  §0 Data construction & contract
§1  Table 1 (descriptives) →  §2 Empirical strategy (equation + identifying assumption)
§3  Identification graphics (event-study / first-stage / McCrary / SCM trajectory / love plot)
§4  Multi-regression main tables (progressive controls / design horse-race / multi-outcome /
                                  panel A-B / IV first-stage triplet) + coefplot
§5  Heterogeneity (subgroup table + CATE / dose-response figure)
§6  Mechanisms (mediation / decomposition)
§7  Robustness gauntlet (placebo / Oster / honest_did / E-value / 2-way & Conley SE /
                         spec curve / sensitivity dashboard) + robustness master table
§8  Replication package — Word / Excel / LaTeX / Markdown bundle via sp.collect()
                          + reproducibility stamp

Mode A — Epidemiology / public health (§A):
A.0  Cohort construction + target-trial protocol (TargetTrialProtocol + target_trial_emulate)
A.1  Table 1 by exposure (mean_comparison, identical to AER mode)
A.2  DAG + propensity-score overlap (positivity check) + KM curves
A.3  IPTW-MSM + g-formula + TMLE + HAL-TMLE doubly-robust triplet
A.4  Survival outcomes — KM / AFT / RMST
A.5  Mendelian randomization (IVW / Egger / weighted median triplet)
A.6  Robustness — E-value / bounds / principal stratification
A.7  STROBE/TRIPOD-style reporting checklist (positivity, adjustment set, E-value)

Mode B — ML causal inference (§B):
B.0  Train/holdout split + SuperLearner nuisance stack
B.1  Estimand DSL + DAG learning (PC / NOTEARS / LLM-assisted)
B.2  Estimator stack — DML / meta-learner / causal forest / Dragonnet/TARNet / BCF /
                       matrix completion (horse race in one regtable)
B.3  CATE distribution + subgroup CATE plot
B.4  Policy learning + off-policy evaluation (policy_tree, offline_safe_policy, ope.*)
B.5  Uncertainty (conformal_causal) + fairness (fairness_audit) + sensitivity
B.6  ML-causal-specific reporting checklist (nuisance learners, cross-fitting, overlap,
     CATE summary, policy value, conformal coverage, fairness gaps)
```

**Out of scope** — data cleaning (use pandas first) and end-to-end
paper drafting (`sp.paper()`; the skill stops at diagnostics and
hands the `CausalResult` back to you).

## Files

- `SKILL.md` — frontmatter + full agent playbook
  - **Default (AER econ)** — 8 paper sections (§-1 – §8) with end-to-end code
  - **§A — Epidemiology / public health pipeline** (target-trial · IPTW · g-formula · TMLE · HAL-TMLE · MR · KM/AFT · E-value)
  - **§B — ML causal pipeline** (DML · S/T/X/R/DR-Learner · causal forest · Dragonnet/TARNet/CEVAE · BCF · matrix completion · policy tree · OPE · conformal causal · fairness audit · DAG learning)
  - **8 multi-regression `regtable` patterns** (A. progressive controls · B. design horse race · C. multi-outcome · D. stacked panel A/B · E. IV first-stage triplet · F. `sp.causal()` orchestrator · G. subgroup heterogeneity · H. robustness master Table A1)
  - **3-tier export cookbook** (single table / paper-format multi-panel / full session bundle)
  - **17 standard AER figures** (raw trends, rollout heatmap, event-study, Bacon, CS-DID, RD plot, McCrary, love plot, SCM trajectory, coefplot, dose-response, CATE, robustness forest, spec curve, sensitivity dashboard)
  - **Method Catalog** (classical OLS / `feols` / IV / panel / DID / RD / matching / SCM / ML / neural / text / mediation / robustness)
  - **Common Mistakes table** (65 anti-patterns with corrections — re-validated against statspai 1.19.0 by `validate_api_claims.py`; incl. the `(fig, ax)` plot-save idiom, `fmt="auto"` for mixed-magnitude regtables, and the §A/§B signature traps)
- `EVALS.md` — SkillOpt-style held-out gate cases for future edits to this skill
- `README.md` — this file

---

## StatsPAI Skill for Claude Code（中文版）

本文件夹是一份 **Claude Code Skill**，教 Claude（或任何兼容的 agent
运行时）端到端地驱动 [StatsPAI](https://github.com/brycewang-stanford/StatsPAI)
完成一次完整的因果推断 / 实证分析。覆盖 **三种领域模式**，三者共用同
一套 `CausalResult` 结果对象与 Word / Excel / LaTeX 导出栈：

- **默认 — 应用经济学（AER / QJE / AEJ）**。预分析计划、样本构造、
  Table 1 描述统计、写出回归方程与识别假设，到事件研究图 / 一阶段
  F / McCrary 密度 / SCM 轨迹 / love plot 等识别图，AER 多回归
  主表火力全开（progressive controls / 设计赛马 / 多结果 / 面板
  A-B / IV 三件套），异质性（子样本表 + CATE 图），机制分解，
  完整 robustness gauntlet（placebo / Oster / honest_did /
  E-value / Conley / 二维聚类 / spec curve / sensitivity dashboard），
  最终交付一份 **同时是 Word / Excel / LaTeX 三种格式** 的可复现
  replication bundle。
- **模式 A — 流行病学 / 公共健康（§A）**。target-trial emulation、
  IPTW + g-formula + TMLE 双稳健三件套、Mendelian randomization
  （IVW / Egger / 加权中位数）、KM / AFT 生存分析、E-value 敏感性、
  principal stratification——按 STROBE / TRIPOD-AI 报告规范输出。
- **模式 B — 因果机器学习（§B）**。DML、S/T/X/R/DR meta-learner、
  causal forest（GRF）、Dragonnet / TARNet / CEVAE 神经因果、BCF、
  matrix completion、CATE 分布 + policy tree + off-policy 评估、
  conformal causal 预测区间、fairness audit、DAG 学习（PC / NOTEARS /
  LLM 辅助）。

三种模式共用同一套估计 → 报告导出链路。切换模式只换 Step-4 的估计器
组合，前后骨架（estimand-first DSL / Table 1 / 主表 / robustness /
replication bundle）保持一致。

### 这份 skill 给你产出什么（论文级，三种格式同步）

AER 流程里每张编号的表格都同步产出 **`.docx` + `.xlsx` + `.tex`**
（Markdown / HTML 按需），合作者用 Word 编辑、期刊编辑用 Excel
审稿、构建系统拼 LaTeX——一份源、三种格式。

| 档位 | 适用场景 | 主 API |
| --- | --- | --- |
| **1. 单张多列表格**（Stata `outreg2` / R `modelsummary` 等价物） | 一张 Table 2 / Table 3 / Table A1，多列对比 | `rt = sp.regtable(M1, M2, ..., template="aer", title=...)` 然后 `rt.to_word(...) · rt.to_excel(...) · rt.to_latex()` |
| **2. 论文级多面板** | Table 2 + 3 + A1 + A2 整本一份文件 | `sp.paper_tables(main=, heterogeneity=, robustness=, placebo=, template="aer").to_docx(...)` |
| **3. 整套 session bundle**（Stata 15 `collect` 等价物） | replication 附录：描述统计 + balance + 多张回归表 + 标题 + 正文混排 | `sp.collect("Paper").add_summary(...).add_balance(...).add_regression(...)...save("paper.docx")`（按扩展名自动路由 `.docx`/`.xlsx`/`.tex`/`.md`/`.html`） |

刊物模板自动套对应的 SE label / 星号档 / 脚注：

```python
sp.list_journal_templates()
# → ('aer', 'qje', 'econometrica', 'restat', 'jf', 'aeja', 'jpe', 'restud')
```

正文里要现挂一个系数：

```python
sp.cite(M3, "training")           # → "1.239*** (0.153)"
```

### 三种领域模式怎么触发

skill 通过自然语言关键词识别用户所在的领域，自动跳到对应 sub-pipeline：

| 你说... | skill 走的 sub-pipeline |
| --- | --- |
| "做个 DID / IV / RD / 事件研究"、"AER 主表"、"应用微观" | 默认（AER 经济学） |
| "target trial 模拟"、"g-formula"、"IPTW"、"TMLE"、"孟德尔随机化"、"Kaplan-Meier"、"E-value"、"STROBE"、"流行病学 / 公共健康"、"队列研究 / 病例对照 / RWE" | 模式 A（流行病学，§A） |
| "DML / 双重机器学习"、"meta-learner"、"causal forest"、"Dragonnet / TARNet / CEVAE"、"BCF"、"CATE"、"policy tree / 策略学习"、"off-policy 评估"、"conformal 因果"、"公平性审计"、"因果发现 / DAG 学习"、"因果机器学习 / uplift" | 模式 B（ML 因果，§B） |
| 混合表述（如 "先 DID 估主效应再 ML CATE 看异质性"） | 默认 + 模式 B 串联——所有估计器都返回同一个 `CausalResult`，可一次性扔进 `sp.regtable(...)` 做赛马列 |

### Agent 默认行为对齐

| 规则 | 默认 | 何时显式覆盖 |
| --- | --- | --- |
| **完整变量列表导出**（含 Intercept + 全部控制） | `sp.regtable(*models, template="aer", ...)`，不传 `keep=` 也不传 `drop=` | 想去掉常数 → `drop=["Intercept"]`；想 focal-only → `keep=[focal]`（IV 三件套 / 交互项才用） |
| **FE 回归走 `sp.feols`**（pyfixest 后端） | `sp.feols("y ~ x \| firm_id + year", df, vcov={"CRV1": "firm_id"})` | `sp.regress` 只用于纯 OLS——它**不解析** `\|` 为 FE 吸收 |
| **双向聚类** | `sp.feols(..., vcov={"CRV1": "firm_id+year"})` | `sp.twoway_cluster(...)` 只兼容 `sp.regress` / `sp.ivreg`（statsmodels 系） |
| **一次产 Word + Excel + LaTeX 三件套** | `rt.to_word(...) · rt.to_excel(...) · open(...).write(rt.to_latex())` | 不出 LaTeX 的话跳过 `.tex`；`.docx` 必出（人审用） |

### 安装

```bash
# 方式 1：复制
cp -r StatsPAI_full_data_analysis_skill ~/.claude/skills/StatsPAI_skill

# 方式 2：软链（自动跟随上游更新）
ln -s "$(pwd)/StatsPAI_full_data_analysis_skill" ~/.claude/skills/StatsPAI_skill
```

再装 Python 包本体（API 接口已对照 **statspai 1.19.0** 由 `validate_api_claims.py` 验证）：

```bash
# 推荐 —— 覆盖默认流程（高维固定效应 + 出图）：
pip install "statspai[fixest,plotting]"

# 完整 skill（再加神经因果 + 文本处理）：
pip install "statspai[fixest,plotting,neural,text]"
```

> 仅 `pip install statspai` **不会**装上 `pyfixest`（`sp.feols` 需要它——任何 `y ~ x | fe` 回归的默认入口，缺失会 `ImportError`）、matplotlib（任何图）、torch（`dragonnet`/`tarnet`/`cevae`）。完整依赖矩阵见 `SKILL.md` 顶部。

### 激活

Skill 会被自然语言触发词自动激活，例如 *"run a DID analysis"*、
*"AER empirical analysis"*、*"applied microeconomics pipeline"*、
*"instrumental variables regression"*、*"event-study plot"*、
*"first-stage F"*、*"Oster bound"*、*"导出回归表到 Word"*、
*"outreg2 in Python"*、*"sp.collect"*、*"sp.feols"*、
*"estimand-first DSL"* 等。完整列表见 `SKILL.md` 开头 frontmatter
的 `triggers:` 字段。

### 适用范围

**覆盖**——AER 风格的 8 段式实证分析闭环：

```text
§-1 预分析计划          →  §0 样本构造与 data contract
§1  Table 1 描述统计     →  §2 实证策略（方程 + 识别假设）
§3  识别图（event-study / 一阶段 / McCrary / SCM 轨迹 / love plot）
§4  多回归主表（progressive controls / 设计赛马 / 多结果 / 面板 A-B
              / IV 一阶段+简化式+2SLS 三件套） + 系数图
§5  异质性（子样本表 + CATE / 剂量反应图）
§6  机制（中介 / 分解）
§7  Robustness gauntlet（placebo / Oster / honest_did / E-value /
                       二维 & Conley SE / spec curve / sensitivity 面板）
                       + Robustness master 主表
§8  Replication package — sp.collect() 一键产出 Word / Excel / LaTeX / Markdown
                          四种格式 + 复现戳
```

**不覆盖**——数据清洗（先用 pandas 处理）和端到端论文生成
（`sp.paper()`；skill 在诊断这一步停住，把 `CausalResult`
交还给用户）。

### 文件

- `SKILL.md` — frontmatter + 完整 agent 操作手册
  - 8 个论文 section（§-1 – §8）含端到端代码
  - **8 套 `regtable` 多回归 pattern**（A. 渐进控制 · B. 设计赛马 · C. 多结果 · D. 面板 A/B · E. IV 三件套 · F. `sp.causal()` 编排器 · G. 子样本异质性 · H. Robustness master Table A1）
  - **3 档导出 cookbook**（单表 / 论文级多面板 / 整套 session bundle）
  - **17 张标准 AER 图**（原始趋势、rollout 热图、event-study、Bacon、CS-DID、RD plot、McCrary、love plot、SCM 轨迹、coefplot、剂量反应、CATE、robustness 森林图、spec curve、sensitivity 面板）
  - **Method Catalog**（经典 OLS / `feols` / IV / 面板 / DID / RD / 匹配 / SCM / ML / 神经 / 文本 / 中介 / robustness）
  - **Common Mistakes 反模式表**（65 条带正确写法，由 `validate_api_claims.py` 对照 statspai 1.19.0 复核；含 `(fig, ax)` 出图保存范式与 §A/§B 签名陷阱）
- `README.md` — 本文件
