# Awesome-list PR 文案与 Zenodo 存档步骤

## 提交目标与一行文案

各清单要求不同（多数要求一行描述 + 字母序插入 + 遵守 CONTRIBUTING），提交前先读对方规范。

### awesome-claude-code（或 awesome-claude / awesome-agent-skills 类清单）

> - [AER-Skills](https://github.com/brycewang-stanford/AER-Skills) - Identification-first agent skill stack for AER/AEJ-track economics manuscripts: 14 lifecycle skills (topic selection to R&R rebuttal) with CI-enforced quality gates — Crossref-verified citations, numeric-correctness contracts on every runnable econometrics demo, and validated tool bindings.

### awesome-economics / awesome-econometrics

> - [AER-Skills](https://github.com/brycewang-stanford/AER-Skills) - Runnable, self-testing Monte Carlo demos of modern econometric pitfalls (staggered DiD, weak IV, RDD, synthetic control, shift-share, DML, bunching, QTE, LP-DiD, matrix completion, randomization inference) plus an opinionated AER manuscript workflow with machine-checked citation integrity.

### awesome-causal-inference

> - [AER-Skills](https://github.com/brycewang-stanford/AER-Skills) - Each causal design demoed as a regression test: estimates pinned to known Monte Carlo truths within stated tolerances, enforced in CI. Covers heterogeneity-robust DiD, weak-IV-robust inference, honest DiD, DML orthogonalization, MC-NNM, and more.

## Zenodo DOI 存档（人工步骤，约 5 分钟）

1. 登录 zenodo.org（用 GitHub 账号），进入 **GitHub** 集成页：https://zenodo.org/account/settings/github/
2. 打开 `brycewang-stanford/AER-Skills` 的开关（仓库根目录已放好 `.zenodo.json` 元数据）。
3. 在 GitHub 上发布下一个 release（开关打开后的 release 才会被存档）。
4. Zenodo 生成 DOI 后：
   - 把 DOI 徽章加进 `README.md` 与 `README.en.md` 徽章区；
   - 在 `CITATION.cff` 中加一行 `doi: 10.5281/zenodo.XXXXXXX`。
