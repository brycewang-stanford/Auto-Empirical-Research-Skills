# AERS 仓库技能水平评估 · Repository Skill-Quality Assessment (2026-07)

> 一次独立、诚实的整仓评估：**AERS 目前处于什么水平，哪里被高估，哪里是真实短板，本轮修了什么。**
> An independent, honest audit of where AERS actually stands — what the headline
> numbers overstate, what the real gaps are, and what this pass fixed.

---

## 1. 结论先行 · Verdict

**总体水平：结构与工程一流，内容严谨性中上，但"体检分"被高估。**

AERS 是一个**策展型（curated aggregation）**仓库：把 69 个上游合集、1,150 个 `SKILL.md`
汇总为一个可路由的根技能。作为"工程化的技能目录"，它的成熟度显著高于同类
awesome-list —— 有 provenance、license 审计、安全扫描、benchmark、eval-harness、
六语 README、严格的 `make validate` 门禁。

但两点必须讲清楚：

1. **"99.x 质量分"衡量的是"形式"（structural hygiene），不是"正确性"。** 它只检查
   frontmatter / description / name 是否存在、篇幅是否过长，**不检查方法学是否正确、
   脚本是否能跑、建议是否会误导**。仓库自己也已承认这点（`SKILL_QUALITY.md` →
   [`SKILL_HYGIENE.md`](SKILL_HYGIENE.md) 的更名说明）。请把它读作"卫生分"，而非"质量分"。
2. **本轮评估发现主分支 CI 实际是红的。** 见 §2 —— 一个对外宣称"学术工业级"的仓库，
   旗舰门禁失败却仍挂着绿色 badge，这是最伤信任的短板。本轮已修复。

一句话：**地基和外壳是 A 级；"1,150 个技能个个 99 分"这个叙事需要降级为"1,150 个技能
个个结构合规、其中约 1% 有行为级验证"。**

---

## 2. 本轮发现的真实问题 · What this pass found

### 2.1 主分支 CI 红了（最高优先级，已修）

`main` 最新一次 `Update skill docs and release assets` 提交把 `make validate` 打挂了，
`validate-catalog` 与 `quality-evals` 两条 workflow 均为 **failure**。根因是同一次
"P2.2 README 重构"引入的三类回归：

| # | 症状 | 根因 | 修法 |
|---|---|---|---|
| A | `validate-repo.py` 报 **101 个 missing-local-link** | `docs/en/*.md`（英文分册）里指向仓库根的链接用了 `../`，从 `docs/en/` 出发应为 `../../`；另有 `docs/PYPI_PACKAGING_DRAFT.md`、`docs/archive/*` 各若干条 | 逐一改正相对深度（98 + 2 + 1 = 101 条） |
| B | `check-readme-stats.py` 报 README 严谨性数字过期 | 重构把 `README.md` / `README-zh-CN.md` 精简成"入口页"，丢掉了 CI 要求的 `benchmark/` + `eval-harness/` 统计行 | 两个 README 各补回信任面统计表（17 / 30 / 159） |
| C | `test_maintainer_docs_point_to_full_local_gate` 失败 | 精简后的 `README.md` 不再包含 `make check` 字样 | 在维护者说明里补回 `make check` 指引 |

修复后：`make validate`、`make check`（含 `validate / python-compat / test / eval-harness /
eval-smoke / benchmark-lint / benchmark` 全部 7 条 lane）**本地全绿，exit 0**。

### 2.2 4 个技能没有 YAML frontmatter（已修）

审计标注 `missing_frontmatter: 4` —— 这些技能在按 frontmatter 注册/路由的运行时里
**根本不会被正确加载**，`description` 也无法参与检索。已补全 `name` + `description`：

- `skills/04-…/scholar-evaluation/SKILL.md` → `scholar-evaluation`
- `skills/28-…/replicate-paper/SKILL.md` → `replicate-paper`
- `skills/38-peternka-academic-proofreader/SKILL.md` → `academic-proofreader`
- `skills/40-py-econometrics-pyfixest/SKILL.md` → `pyfixest-reference`（避开与 17 合集 `pyfixest` 撞名）

结果：`missing_frontmatter 4 → 0`，frontmatter-description 覆盖 `1146 → 1150/1150`，
平均卫生分 `99.2 → 99.4`。

### 2.3 根路由 `SKILL.md` 偏薄（已增强）

整仓封装成一个技能时，[`SKILL.md`](../SKILL.md) 是唯一入口。原文只有按 stage 的粗分类。
本轮加入：**方法 → 起点合集**的路由表（DiD / IV / RDD / SCM / 面板 FE / DML / 贝叶斯 /
Stata / R / 文献 / 引用 / 写作 / de-AIGC / 复现），以及**重名（name collision）安装告警**。

---

## 3. 结构性短板与本轮跟进 · Structural debt & follow-up

第一轮修红 CI 之后，第二轮（2026-07-08）继续处理了 §5 提出的建议。状态如下：

| 短板 | 原状 | 本轮处理 |
|---|---|---|
| **行为级验证覆盖率低** | 1,150 个技能仅 **11 个（1.0%）** 有 eval | ✅ 新增 **7 个真实方法学陷阱场景**，覆盖此前无 eval 的 7 个技能（marginaleffects 非线性交互项、log-point 百分比误读、PRISMA 可复现检索、引用 DOI 核验、CausalPy 安慰剂检验、复现审计"重算而非复述"、OpenAlex 禁止编造元数据）。覆盖 **11 → 18 技能，30 → 37 场景，159 → 183 rubric 项**。方法族覆盖本就 100%（见 [`RIGOR_COVERAGE.md`](RIGOR_COVERAGE.md)）——真正稀疏的是"每个技能"维度。同时修了 `eval_coverage` 一直显示 rubric-id 而非 scenario-id 的解析 bug。 |
| **91 个 `SKILL.md` 超 500 行** | 疑似违反渐进式披露 | ✅ **证据化决策：不做整仓机械拆分。** 91 个里 24 个已带 `references/`（含自有旗舰 `00.1/00.2/00.3`，其 2000+ 行主干已把细节下放到 `references/`，故不被扣分）；其余 67 个全是 vendored 快照，重写会破坏 provenance。唯一的一等公民长技能 StatsPAI（`00`）走上游拆分。详见 [`LONG_SKILL_STATUS.md`](LONG_SKILL_STATUS.md) §0。 |
| **92 组重名技能** | 扁平安装互相覆盖 | ✅ catalog 现为每个技能生成全局唯一的 `qualified_name`（`<collection>::<name>`，同合集内再撞名则追加 `@子路径`）——**1150/1150 唯一**；`skills.json.summary` 新增 `duplicate_bare_names`；根 `SKILL.md` 指向该字段。 |
| **主分支缺 CI 保护** | badge 绿、门禁红曾直达 main | ⚠️ 见 §5 —— 需仓库管理员在 GitHub 设置里开启（非代码可改）。 |

---

## 4. 本轮改动清单 · Change log for this pass

- **CI 转绿**：修复 101 条断链 + 2 个 README 统计行 + 1 个维护者门禁测试。
- **修复 4 个无 frontmatter 技能**，补 `name` + `description`。
- **增强根路由 `SKILL.md`**：方法路由表 + 重名告警。
- **重建 catalog**（`make catalog`）使所有派生产物（audit / enriched / TAXONOMY /
  SKILL_CATALOG / RIGOR_COVERAGE / RELEASE_NOTES）与源一致。
- 新增本评估文档。

验证：`make check` 全绿（exit 0）。数据来源见
[`catalog/skill-audit.json`](../catalog/skill-audit.json) 与
[`catalog/skills-enriched.json`](../catalog/skills-enriched.json)。

---

## 5. 给维护者的建议 · Recommendations

1. **开启主分支保护（唯一未做项，需管理员）。** 本轮的根因是"badge 绿、门禁红"的提交
   直达 `main`。在 GitHub → Settings → Branches → Branch protection rules 给 `main`
   加：require status checks to pass（勾选 `validate-catalog` 与 `quality-evals`）+
   require branch up to date。这样红门禁再也进不了 `main`。这是设置项，不是代码改动，
   所以本轮只能建议、无法代改。
2. **eval 覆盖继续按"每技能"补，而非追平均分。** 方法族已 100%，但 1,150 个技能里仍只有
   18 个有行为级 eval。优先给高流量的 vendored 因果/写作技能各补 1 个陷阱场景。
3. **长技能维持"上游拆分"策略**（见 `LONG_SKILL_STATUS.md`），不要在仓库内改 vendored 快照。
4. **把"99 分"叙事降级为"卫生分 + 覆盖率"双指标**：卫生分已封顶且只测形式，覆盖率
   （benchmark 17 / eval 37 场景 / 18 技能）才是可持续增长、真正反映严谨性的数字。
