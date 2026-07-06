# Changelog

All notable changes to AER-Skills are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-07-02

### Added

- Five method demos closing the v1.2 roadmap's coverage gaps, each under the
  numeric-correctness contract (21 new `NUMERIC-CHECK` assertions):
  - `randomization-inference-demo` — robust-SE t-tests over-reject under
    concentrated leverage; the Fisher randomization test has exact size
    (Young 2019).
  - `qte-demo` — a null ATE hiding large distributional effects; quantile
    regression recovers the analytic QTE curve (Koenker-Bassett 1978).
  - `lp-did-demo` — pooled TWFE event studies contaminated under staggered
    adoption; LP-DiD with clean controls recovers the true dynamic path
    (Dube-Girardi-Jordà-Taylor).
  - `bunching-demo` — excess mass at a tax kink identifies the earnings
    elasticity (Saez 2010), with oracle-vs-feasible counterfactuals and two
    falsification worlds.
  - `matrix-completion-demo` — DiD structurally biased under interactive
    fixed effects; low-rank imputation recovers the truth, with the
    rank-sensitivity caveat demonstrated rather than hidden
    (Athey et al. 2021).
- Seven Crossref-verified bibliography entries (Saez 2010; Kleven 2016;
  Koenker-Bassett 1978; Young 2019; Jordà 2005; Dube-Girardi-Jordà-Taylor
  2023; Athey et al. 2021), recorded for the hermetic offline gate.
- StatsPAI tool registry expanded from 43 to 51 validated bindings
  (`lp_did`, `ri_test`, `qte`, `bunching`, `notch`, `matrix_completion`,
  `interactive_fe`, `aipw`), kept in sync with the `aer-statspai` hub.
- Methods reference: LP-DiD, matrix-completion, randomization-inference, and
  QTE rows; glossary entries for Bunching, LP-DiD, Matrix completion, and
  Quantile treatment effect.
- Launch kit (`docs/launch-kit/`): bilingual announcement drafts,
  awesome-list submission blurbs, and Zenodo archiving steps; `.zenodo.json`
  metadata for DOI minting.

## [1.2.0] - 2026-07-01

### Added

- `tests/` — hermetic pytest suite for the quality tooling itself (validators,
  citation verifier, skill auditor, smoke runner, scaffolder, installer, and
  the `NUMERIC-CHECK` protocol), wired to `make test`.
- Double machine learning demo (`examples/dml-plr-demo/`): partialling-out PLR
  with cross-fitting, contrasting naive ML plug-in bias against
  Neyman-orthogonal estimation, under the numeric-correctness contract.
- End-to-end walkthrough (`examples/end-to-end-walkthrough.md`): one fictional
  project traced through all 12 workflow steps, naming the exact skill, gate,
  and artifact at each step.
- Quality scorecard: `make scorecard` regenerates `docs/quality-scorecard.md`,
  a one-page machine-generated aggregate of every gate the repo enforces.
- `docs/roadmap.md` — the operating definition of "reference automated-empirics
  repo" and the sprint plan toward it.
- Release metadata: `CITATION.cff`, this changelog, and a `v1.2.0` git tag.

### Changed

- CI now runs the unit-test suite, the Python example smoke gate (numeric
  checks included), and both offline and groundedness citation gates on every
  push and pull request, with pip caching and a status badge in both READMEs.
- Bilingual READMEs: added CI badge, an honest comparison table against
  adjacent projects, and links to the roadmap and scorecard.

## [1.1.1] - 2026-06-25

### Added

- Three self-verifying hard gates (PR #2):
  - **Numeric-correctness contract** — every runnable demo pins estimates to a
    known truth within a stated tolerance via `NUMERIC-CHECK` protocol lines;
    a demo that emits none, or a FAIL, fails the smoke gate.
  - **Citation groundedness** — prose-level citations must resolve to
    Crossref-verified bib entries; `PHANTOM_CITATION` / `DANGLING_KEY` are
    hard failures.
  - **Tool-binding contract** — method skills route to a 43-tool validated
    StatsPAI registry instead of hand-rolling estimators.
- Sensitivity-analysis demos: specification curve, Oster delta, honest DiD,
  multiple-testing FWER, few-clusters wild bootstrap, shift-share
  shock-level inference, synthetic-control placebo inference.
- Example smoke gate (`scripts/run_example_smoke.py`) and citation gold set.

### Fixed

- Multiple-testing mis-attribution in the methods reference.
- Fragile backtick pairing replaced with CommonMark code-span parsing in the
  citation verifier.

## [1.1.0] - 2026-06-23

### Added

- Four lifecycle skills, growing the bundle from ten to fourteen:
  `aer-literature`, `aer-paper-body`, `aer-consistency`, `aer-referee-sim`.
- 12-step gated default workflow (body-first drafting, desk-screen and
  referee-simulation gates) in `aer-workflow`.
- SkillOpt evaluation protocol: skill-audit scoring with an ≥85 quality floor
  and ≥8 substance anchors, routing-scenario gate, all wired into
  `make preflight` and CI.
- Claim–evidence ledger audit in `aer-consistency`; reproducible citation
  verification gate; substance-anchor floor across skills.
- Docs: style guide, referee-report rubric, glossary expansion, SkillOpt
  protocol; worked examples for results sections and referee reports.

## [1.0.0] - 2026-05-24

### Added

- Initial ten-skill bundle for the AER manuscript lifecycle: workflow router,
  topic selection, identification, robustness, introduction, tables/figures,
  replication, submission, rebuttal, and the StatsPAI implementation engine.
- Stata / R / Python project templates and the AEA-compliant
  replication-package skeleton.
- Repository validator (`scripts/validate_repo.py`), installer for Claude Code
  and Codex, project scaffolder, and the initial CI preflight.
- Reference docs: design principles, workflow map, methods reference,
  desk-rejection audit, citation-integrity protocol, classic and modern AER
  exemplar lists.

[1.3.0]: https://github.com/brycewang-stanford/AER-Skills/releases/tag/v1.3.0
[1.2.0]: https://github.com/brycewang-stanford/AER-Skills/releases/tag/v1.2.0
[1.1.1]: https://github.com/brycewang-stanford/AER-Skills/compare/620b14e...cbbbd38
[1.1.0]: https://github.com/brycewang-stanford/AER-Skills/compare/d0c2054...620b14e
[1.0.0]: https://github.com/brycewang-stanford/AER-Skills/commits/d0c2054
