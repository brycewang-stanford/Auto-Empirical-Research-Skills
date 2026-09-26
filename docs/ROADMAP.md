# Roadmap

This roadmap is scoped to making AERS a high-quality, high-trust GitHub project rather than just a large link collection.

> **Execution plans (status as of 2026-08-27):** the `PLAN-2026-MM` files are sprint plans whose calendar labels drifted — all three were authored 2026-07-01…04 and largely executed immediately.
>
> - [`PLAN-2026-07.md`](PLAN-2026-07.md) — **closed**, 14/15 done (the external AERS-vs-Econometrics-Agent comparison remains open, tracked in [`SCOREBOARD.md`](SCOREBOARD.md) / [`INTEROP.md`](INTEROP.md) Recipe C).
> - [`PLAN-2026-08.md`](PLAN-2026-08.md) — headline deliverables **shipped** (Card–Krueger end-to-end replication, public benchmark scoreboard, bunching family, link-triage automation); see its status note.
> - [`PLAN-2026-09.md`](PLAN-2026-09.md) — **delivered (2026-08-27)** apart from the release tag: the external scoreboard, the `structural-demand-recovery` method family, the `aers-score` CLI, and both end-to-end replications (Card 1995, NSW). See its status note for where the implementation deliberately diverged from the plan.
> - [`PLAN-2026-10.md`](PLAN-2026-10.md) — **draft / not started**: pushing what is now provable at the core out to the edges — fixture coverage from `critical` to `high`, per-skill evals, provenance recorded to a commit rather than a URL, and the first genuinely third-party scoreboard entry.

## Now

- Keep `catalog/skills.json` and `docs/SKILL_CATALOG.md` current.
- Require `make check` for all pull requests.
- Keep README links and docs category links green.
- Preserve the no-paid/proprietary-core scope rule for new listings.
- Keep [`EXTERNAL_SCOREBOARD.md`](EXTERNAL_SCOREBOARD.md) regradable: every submission
  under `benchmark/external/` is rescored from its raw candidates on each build, so a
  task whose golds change fails loudly rather than misreporting an old entry.
- Keep `catalog/provenance.json`, `docs/LICENSE_AUDIT.md`, and `docs/SKILL_AUDIT.md` current.
- Use [`docs/search.html`](search.html) as the lightweight searchable catalog (now served on [GitHub Pages](https://brycewang-stanford.github.io/Auto-Empirical-Research-Skills/)).
- Keep GitHub Actions passing `scripts/validate-workflows.py` and review OpenSSF Scorecard findings.

## Next

- Land the first genuinely third-party entry on [`EXTERNAL_SCOREBOARD.md`](EXTERNAL_SCOREBOARD.md). The machinery, the rules ([`SCOREBOARD_RULES.md`](SCOREBOARD_RULES.md)) and the tooling ([`aers-score`](../aers_score/README.md)) are live; what is missing is a submission from someone else, which is not something this repo can deliver on its own.
- Cut the v2026.09 tag. Everything the plan called for is on `main`; only the tag and the GitHub release remain, and both are maintainer actions.
- Push discrimination fixtures from `critical` out to `high` severity, and grow per-skill eval coverage the way the [2026-07 assessment](QUALITY_ASSESSMENT_2026-07.md) recommends. 19 method families are fully covered but only 22 of 1,107 skills have a behavioral scenario — family-level coverage is the sharp number, skill-level coverage is the flat one.
- Enrich provenance metadata with exact vendored commits where upstream snapshots are known.
- Add scheduled external-link triage notes to releases when weekly checks fail.
- Convert the flagship eval prompts into executable scorecards where artifacts can be generated in CI without paid APIs.
- Keep [`ECOSYSTEM.md`](ECOSYSTEM.md) and [`../ecosystem/ecosystem.json`](../ecosystem/ecosystem.json) current as the agentic-research ecosystem evolves, and expand the [`INTEROP.md`](INTEROP.md) pipeline recipes (e.g. a benchmarked AERS-vs-Econometrics-Agent comparison).

## Later

- Publish `aers-score` as a release asset (or to PyPI) so scoring does not require an editable install from a checkout. The exam itself stays in the repo by design — see `aers_score/exam.py`.
- Package first-party AERS skills as installable bundles for agent runtimes that support plugins/marketplaces.
- Maintain a public benchmark of empirical-research agent workflows: correctness, reproducibility, citation hygiene, and runtime safety.
- Keep closing whatever [`RIGOR_COVERAGE.md`](RIGOR_COVERAGE.md) lists as open. The families named here in 2026-07 (synthetic control, panel FE, double/debiased ML, Bayesian, survival, the event-study benchmark task, the matching/PSM eval scenario) are all closed; the map is generated, so read it rather than this line.

## Completed Hardening Pass

- Generated machine-readable catalog and provenance metadata.
- Added license audit, skill hygiene audit, static search page, install guide, submission guide, flagship demos, release process, external-link workflow, and clean CI validation.
- Added machine-readable flagship eval prompts and generated reviewer docs.
- Added a generated methodological rigor coverage map ([`RIGOR_COVERAGE.md`](RIGOR_COVERAGE.md), built by `scripts/build-coverage-map.py` and freshness-checked in `make validate`) that joins the method taxonomy with eval scenarios and benchmark tasks and surfaces open gaps.
- Added per-skill behavioral evals for the first-party flagships (`00.1` Python / `00.2` Stata / `00.3` R), each on an ecosystem-level inference trap, with discrimination tests that require the rubric to separate a correct answer from a plausible wrong one.
- Opened the numeric benchmark to third parties: the [`aers-score`](../aers_score/README.md) CLI, [`EXTERNAL_SCOREBOARD.md`](EXTERNAL_SCOREBOARD.md) (regraded from raw candidates, never from submitted numbers), and [`SCOREBOARD_RULES.md`](SCOREBOARD_RULES.md).
- Added an ecosystem positioning map ([`ECOSYSTEM.md`](ECOSYSTEM.md)), interoperability recipes ([`INTEROP.md`](INTEROP.md)), a machine-readable registry ([`../ecosystem/ecosystem.json`](../ecosystem/ecosystem.json)), and a sync-enforcing validator (`scripts/check-ecosystem.py`, wired into `make validate`).
