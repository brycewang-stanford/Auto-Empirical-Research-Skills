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

## 3. 仍待处理的结构性短板 · Remaining structural debt（未在本轮修）

这些不是 bug，是需要单独立项的方法学/内容工作，**不宜在一次自动化 pass 里草率处理**
（多为第三方 vendored 内容，重构会破坏原作者意图）：

| 短板 | 现状 | 建议 |
|---|---|---|
| **行为级验证覆盖率极低** | 1,150 个技能只有 **11 个（~1%）** 进入 eval-harness | 这才是"质量"的真实瓶颈。把 badge 叙事从"1150×99 分"改为"覆盖率优先"，按方法（IV/DiD/RDD…）逐条补 eval，而非追求平均分。 |
| **91 个 `SKILL.md` 超 500 行** | 违反渐进式披露（progressive disclosure）原则；最长 2,466 行 | 仓库已有 [`LONG_SKILL_SPLIT_PLAN.md`](LONG_SKILL_SPLIT_PLAN.md) 与 `scripts/split-skill.py`。对**自有**旗舰（`00.*` / `50`）先做拆分示范，vendored 的谨慎处理。 |
| **92 组重名技能** | 扁平安装时会互相覆盖 | 根 `SKILL.md` 已加告警；长期可在 catalog 生成 `collection::name` 命名空间。 |

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

## 5. 给维护者的一句话建议 · One-line recommendation

**别再优化那个 99 分了 —— 它已经封顶且衡量的是形式。把下一阶段的力气全部投到
"行为级 eval 覆盖率"（当前 1%）和"超长技能拆分"（91 个）上，这两项才是把"看起来严谨"
变成"真的严谨"的杠杆。** 同时，给主分支加一条"CI 必须绿才能合并"的保护规则，避免
再次出现本轮这种"badge 绿、门禁红"的失配。
