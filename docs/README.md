# docs/ — what is generated vs hand-maintained

The single most important rule in this directory: **never hand-edit a
generated file** — your change will be overwritten by the next `make catalog`
and `make validate` will flag the staleness either way.

## Generated (owned by a script; regenerate, don't edit)

| File | Generator | Refreshed by |
|---|---|---|
| `SKILL_CATALOG.md`, `SKILL_QUALITY.md`, `TAXONOMY.md` | `scripts/build-catalog-enrich.py` | `make catalog` |
| `SKILL_AUDIT.md`, `SKILL_HYGIENE.md` | `scripts/build-skill-audit.py` | `make catalog` |
| `LICENSE_AUDIT.md` | `scripts/build-provenance.py` | `make catalog` |
| `../skills/README.md` (outside this dir) | `scripts/build-provenance.py` | `make catalog` |
| `EVALS.md` | `scripts/build-evals.py` | `make catalog` |
| `RIGOR_COVERAGE.md` | `scripts/build-coverage-map.py` | `make catalog` |
| `RELEASE_NOTES.md`, `badges/`, `releases/` | `scripts/build-release-notes.py` | `make catalog` |
| `BENCHMARK_SCOREBOARD.md` | `scripts/build-benchmark-scoreboard.py` | `make catalog` |
| `EXTERNAL_SCOREBOARD.md` | `scripts/build-external-scoreboard.py` | `make catalog` |
| `LINK_TRIAGE.md` | `scripts/build-link-triage.py` | on link-check failure |
| `QUICKSTART_REPORT.md` | `scripts/quickstart.py --markdown` | `make catalog` |

## Hand-maintained entry points

- `CONTENT_ZH.md` — extended Chinese body behind the root `README.md`
  (two-level architecture; see the note at the top of `README.md`).
- `GETTING_STARTED.md`, `CHOOSING_A_SKILL.md`, `FAQ.md`, `INSTALL.md`,
  `GOLDEN_WORKFLOWS.md`, `WORKFLOW_MAP.md` — user guides.
- `../catalog/security-scan.json` (outside this dir) — the vendored-collection
  pattern-scan record, written by `scripts/scan-collections.py` (`make
  security-scan`) and freshness-checked by `make validate`. The prose write-up
  lives in `../SECURITY-SCAN-REPORT.md`.
- `../catalog/curation.json` (outside this dir) — hand-curated routing tiers
  (core collections, preferred copy per duplicated skill name, out-of-domain
  prefixes). Read by `scripts/build-catalog-enrich.py` and
  `scripts/find-skill.py`; ranking only, never removes a skill.
- `../evals/routing-cases.json` (outside this dir) — routing eval cases,
  scored by `scripts/check-routing.py` (gated in `make validate`).
- `SCOREBOARD_RULES.md` — who may submit to `EXTERNAL_SCOREBOARD.md` and how
  entries are ranked (the board itself is generated).
- `TRUST.md`, `SCOREBOARD.md` (link hub — deliberately carries no numbers),
  `QUALITY_GATE.md`, `SKILL_FRONTMATTER_SPEC.md`, `SKILL_HYGIENE.md`'s
  companion policy docs (`SKILL_SUBMISSION_GUIDE.md`, `OUT_OF_SCOPE.md`).
- `ROADMAP.md` + `PLAN-2026-*.md` — sprint plans with dated status notes.
- `MAINTAINER_PLAYBOOK.md`, `RELEASE.md`, `CONTRIBUTING`-adjacent docs.
- `01-…10-*.md` (+ `en/` mirrors) — the ten-stage Chinese workflow guides.
- Dated audits stay until superseded, then move to [`archive/`](archive/).

## Everything else

`search.html` / `tools-search.html` are static search UIs reading the
committed catalog JSON. `superpowers/` holds design specs for the
Paper-WorkFlow submodule work.
