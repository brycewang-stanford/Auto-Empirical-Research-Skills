# Repository Audit - 2026-05-31

This audit was run from the local workspace after fast-forwarding `main` to `origin/main`.

## Snapshot

| Metric | Value |
|---|---:|
| Top-level `skills/` directories | 54 |
| Top-level collections with exact-case `SKILL.md` files | 50 |
| Exact-case `SKILL.md` files under `skills/` | 977 |
| Total tracked files | 3260 |
| Total workspace size | 116 MB |
| Markdown workflow docs under `docs/` | 10 |
| Existing scheduled sync workflows | 2 |
| Large files over 1 MB | 2 cover images |

## Strengths

- Clear niche: empirical research, econometrics, causal inference, replication, submission, and review response.
- Strong flagship assets: StatsPAI skill, explicit Python/Stata/R empirical-analysis skills, AER-skills, Chinese de-AIGC.
- Bilingual README entry point and workflow-stage docs.
- Existing security scan reports and vendor-sync workflows.
- Rich demo outputs for LaLonde and StatsPAI-style pipelines.

## Issues Found

- README links still pointed to old local paths for StatsPAI and the Python empirical-analysis skill.
- No generated machine-readable catalog despite a large skill inventory.
- No generic repo validation CI for local links, skill frontmatter, or generated catalog freshness.
- No issue templates, pull request template, `SECURITY.md`, `CODE_OF_CONDUCT.md`, or `CITATION.cff`.
- Many vendored `SKILL.md` files exceed the recommended 500-line progressive-disclosure target. This is acceptable for upstream mirrors, but first-party additions should split long details into `references/`.
- A few upstream files are named `skill.md` rather than exact-case `SKILL.md`; these are treated as cleanup warnings because Linux agent runtimes and CI are case-sensitive.

## Changes Made

- Added `scripts/build-catalog.py`, `catalog/skills.json`, and `docs/SKILL_CATALOG.md`.
- Added `scripts/validate-repo.py`, `Makefile`, and `.github/workflows/validate-catalog.yml`.
- Added issue templates for bug reports and skill submissions.
- Added pull request checklist focused on source, license, catalog, validation, and paid-API scope.
- Added project governance files: `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`.
- Added `docs/QUALITY_GATE.md` and `docs/COMPETITIVE_LANDSCAPE.md`.
- Fixed stale README/README-zh local skill links.
- Added `scripts/build-provenance.py`, `catalog/provenance.json`, and `docs/LICENSE_AUDIT.md`.
- Added `scripts/build-skill-audit.py`, `catalog/skill-audit.json`, and `docs/SKILL_AUDIT.md`.
- Added static search page, install guide, skill submission guide, flagship demos, release process, changelog, and scheduled external-link workflow.
- Added `evals/flagship-evals.json`, `scripts/build-evals.py`, and generated `docs/EVALS.md` for flagship skill regression prompts.
- Updated CI to run the full `make validate` quality gate instead of a partial catalog-only check.
- Added Dependabot, OpenSSF Scorecard, workflow policy validation, and maintainer/agent coordination docs.
- Removed the unused root `test-skill/` placeholder.
- Normalized lowercase `skill.md` files to exact-case `SKILL.md`.

## Recommended Next Steps

1. Add exact vendored commit SHAs where upstream snapshots are known.
2. Split first-party long `SKILL.md` files into lean spines plus `references/` files.
3. Add screenshots or rendered previews to flagship demo pages.
4. Convert the flagship eval prompts into executable scorecards.
5. Build a public benchmark for empirical-research agent workflows.
