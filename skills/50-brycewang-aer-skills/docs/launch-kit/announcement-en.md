# English platform drafts

> Cross-check all numbers against `docs/quality-scorecard.md` before posting.

---

## X / Twitter thread

**1/** Most "AI academic writing" tools fail economics in the same three ways: hallucinated citations, drifting numbers, hand-rolled estimators. We built an agent skill stack for AER-track papers where every one of those failure modes is a machine-enforced, CI-gated check. Open source, MIT.

**2/** The gates run on the repo itself first:
- every prose citation must resolve to a Crossref-verified bib entry (PHANTOM_CITATION = build failure)
- every runnable demo pins its estimates to a known truth ± tolerance — "runs but wrong" fails
- method skills route to a validated tool registry; no hand-rolling

**3/** Coverage: 14 skills across the whole lifecycle — topic selection → literature (with citation verification) → identification → robustness → body → intro → exhibits → full-manuscript consistency audit → adversarial referee simulation → AEA-compliant replication package → submission → R&R rebuttal.

**4/** The demos double as regression tests: staggered DiD, weak IV, RDD, synthetic control, shift-share, few clusters, multiple testing, spec curves, Oster bounds, honest DiD, DML, bunching, QTE, LP-DiD, matrix completion, randomization inference. Each pinned to Monte Carlo truth.

**5/** And the quality tooling is itself unit-tested (hermetic pytest suite), with a machine-generated scorecard that fails the build if it drifts from reality. Repo: https://github.com/brycewang-stanford/AER-Skills

---

## Hacker News (Show HN)

**Title:** Show HN: AER-Skills – agent skills for economics papers with CI-enforced quality gates

**Text:**

AI-assisted empirical research has a "plausible but wrong" problem: hallucinated citations, estimates that drift, estimators hand-rolled incorrectly. AER-Skills is an agent skill bundle for American Economic Review–track manuscripts that turns each of those failure modes into a machine-checked gate, enforced on the repository itself in CI:

- Citation groundedness: every prose citation must resolve to a Crossref-verified BibTeX entry; a phantom citation fails the build.
- Numeric-correctness contracts: each of the runnable econometrics demos (staggered DiD, weak IV, RDD, synthetic control, DML, bunching, QTE, LP-DiD, matrix completion, randomization inference, …) pins its estimates to a known Monte Carlo truth within a stated tolerance.
- Tool-binding: method skills route to a validated tool registry rather than generating estimator code from scratch.
- The validators themselves have a hermetic unit-test suite, and a machine-generated scorecard fails preflight when it drifts from measured state.

Amusingly, the very first CI run of the numeric smoke gate caught that our "pinned, tested" Python requirements had never actually been installable from PyPI — two phantom version pins that had survived months of local development. The gates work.

Repo: https://github.com/brycewang-stanford/AER-Skills (MIT; docs in English and Chinese)

---

## Reddit r/econometrics (or r/academiceconomics)

**Title:** Open-source: runnable, self-testing demos for 16 modern econometric pitfalls (staggered DiD, weak IV, bunching, LP-DiD, MC-NNM, …) inside an AER-workflow agent skill stack

**Text:**

Each demo is a small Monte Carlo where the truth is known by construction, and the script asserts the econometric point numerically (and fails CI otherwise): TWFE contamination under staggered adoption, 2SLS over-rejection under weak instruments vs Anderson-Rubin, global-polynomial RDD vs local linear, placebo-in-space inference for synthetic control, shock-level inference for shift-share, wild cluster bootstrap with few clusters, FWER control, spec curves, Oster bounds, honest DiD, DML orthogonalization (the naive plug-in is pinned to its analytically-known attenuation factor), Saez bunching, QTE, LP-DiD vs pooled event studies, matrix completion under factor confounding, and randomization inference à la Young (2019).

They live inside a larger agent-skill bundle for AER-track manuscript workflows, but every demo runs standalone with numpy/matplotlib (+statsmodels for two). Criticism of the DGPs and tolerances very welcome — that is exactly what the numeric contract is for.

https://github.com/brycewang-stanford/AER-Skills
