# Roadmap — the one-month sprint to the reference automated-empirics repo

**Window:** 2026-07-01 → 2026-07-31 · **Baseline:** v1.1.0 (14 skills, 12-step gated workflow, three self-verifying hard gates merged in PR #2) · **Target release:** v1.2.0

## 中文摘要

一个月冲刺目标：把 AER-Skills 从"一套高质量静态 skill 包"升级为**全网可信度最高的自动实证研究仓库**。四条主线：

1. **工程可信度** — 真正的单元测试套件、全门 CI、发布元数据（CITATION.cff / CHANGELOG / 语义化版本 tag），让任何工程师三分钟内确认"这个仓库的每一条承诺都被机器验证过"。
2. **旗舰能力** — 端到端 walkthrough（从选题到 rebuttal 的 12 步全流程串联示例）+ 现代方法覆盖扩展（DML 演示），让"自动实证"不止是口号而是可复跑的证据链。
3. **可评测性** — 一键质量记分卡（`make scorecard`），把所有硬门的通过状态汇总成一页可引用的报告。
4. **定位与发布** — 双语 README 升级（CI 徽章、与同类项目的诚实对比表）、v1.2.0 正式 release。

判定"全网第一"的操作性标准：**同类仓库中唯一同时满足**（a）每个数值示例被钉到真值±容差、（b）每条散文引用被解析到经 Crossref 验证的 bib 条目、（c）每个方法 skill 绑定到已验证工具注册表、（d）以上全部由 CI 强制执行、（e）提供从选题到审稿回复的完整闭环。

---

## Operating definition of "#1"

"Best automated-empirics repo" is not a vibe; it is a checklist no comparable
repo currently satisfies in full. AER-Skills claims the top spot iff all of the
following hold **and are enforced by CI, not by promise**:

| # | Claim | Enforced by |
|---|-------|-------------|
| 1 | Every runnable demo pins its estimates to a known truth within a stated tolerance | `NUMERIC-CHECK` contract + `make smoke-examples` |
| 2 | Every prose citation resolves to a Crossref-verified bib entry (no citation from memory) | `make verify-citations-groundedness` |
| 3 | Every method skill routes to a validated tool registry (no hand-rolled estimators) | tool-binding contract in `validate_repo.py` |
| 4 | Every skill document clears a scored quality floor (≥85 score, ≥8 substance anchors) | `make audit-skills-gate` |
| 5 | The full lifecycle — topic selection → literature → identification → body → exhibits → consistency → referee simulation → rebuttal → replication package → submission — is covered by installable skills with worked examples | 14 skills + examples index |
| 6 | All of the above run on every push and every PR | `.github/workflows/ci.yml` |
| 7 | The quality tooling itself is unit-tested | `tests/` + `make test` |

Items 1–5 shipped by v1.1.0 + PR #2. This sprint ships 6–7 and everything below.

## Week 1 (Jul 1–7) — Engineering trust

| Deliverable | Acceptance criterion | Status |
|---|---|---|
| `tests/` pytest suite covering the validators, citation verifier, skill auditor, smoke runner, scaffolder, installer, and the numeric-check protocol | `make test` green; ≥60 focused tests; hermetic (no network, no optional stacks) | ✅ this sprint |
| CI upgrade: unit tests, example smoke (Python), offline + groundedness citation gates all run per push/PR | CI has distinct steps for `test`, `smoke-examples`, `verify-citations`, `verify-citations-groundedness`; pip caching; status badge in both READMEs | ✅ this sprint |
| Release metadata | `CITATION.cff` (validated), `CHANGELOG.md` (Keep-a-Changelog format, back-filled to v1.0.0) | ✅ this sprint |

## Week 2 (Jul 8–14) — Flagship capability

| Deliverable | Acceptance criterion | Status |
|---|---|---|
| End-to-end walkthrough (`examples/end-to-end-walkthrough.md`): one fictional project traced through all 12 workflow steps, naming the exact skill, gate, and artifact at each step, cross-linking every existing example | Passes validator + citation gates; linked from examples index and both READMEs | ✅ this sprint |
| Modern-methods coverage: double machine learning demo (`examples/dml-plr-demo/`) — partialling-out PLR with cross-fitting, showing naive ML plug-in bias vs. Neyman-orthogonal estimation | Registered in validator; ≥3 `NUMERIC-CHECK` lines; smoke-gate green; bib-key-cited README | ✅ this sprint |
| Method-coverage audit: map the 10→11 demos against `docs/methods-reference.md` sections; record remaining gaps (bunching, quantile treatment effects, structural) | Gap list recorded in this roadmap's appendix | ✅ this sprint |

## Week 3 (Jul 15–21) — Measurability

| Deliverable | Acceptance criterion | Status |
|---|---|---|
| Quality scorecard: `make scorecard` regenerates `docs/quality-scorecard.md` — one page aggregating skill count, audit scores, gate inventory, demo/check counts, citation-verification totals | Deterministic output; drift between committed scorecard and regenerated one fails preflight | ✅ this sprint |
| Referee-sim calibration harness (stretch): score the two worked referee-report runs against the rubric programmatically | Deferred if scorecard lands first | ◻ backlog |

## Week 4 (Jul 22–31) — Positioning & release

| Deliverable | Acceptance criterion | Status |
|---|---|---|
| README upgrade (zh + en): CI badge, honest comparison table vs. adjacent projects (generic writing-skill packs, agent frameworks like Econometrics-Agent / open_deep_research), quickstart kept to 3 commands, roadmap linked | Both READMEs updated symmetrically | ✅ this sprint |
| v1.2.0 release: bump plugin manifests, tag, GitHub Release with change summary | `git tag v1.2.0` on main; Release published | ✅ this sprint |
| Launch tasks (human): announcement post, submission of the repo to awesome-lists (awesome-claude-code, awesome-economics, awesome-causal-inference), Zenodo DOI archive | Owner action; drafts can be generated on request | ◻ human |

## KPIs to review on Jul 31

- CI: all gates green on main, wall-clock < 10 min.
- Coverage: 11 runnable demos, ≥45 numeric checks, 14 skills all ≥85/≥8.
- Adoption signals (human-tracked): stars, plugin installs, citations of the repo.

## Appendix — known method-coverage gaps (candidate demos for v1.3)

- Bunching estimators (`bunching`, `notch`) — kink/notch designs.
- Quantile treatment effects (`qte`, `ivqreg`) — distributional effects.
- Matrix completion / gsynth — factor-model counterfactuals beyond classic synth.
- Randomization inference (`ri_test`) as a first-class demo rather than a robustness aside.
- LP-DiD / local projections for macro-empirical designs.
