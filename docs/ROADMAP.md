# Roadmap

This roadmap is scoped to making AERS a high-quality, high-trust GitHub project rather than just a large link collection.

## Now

- Keep `catalog/skills.json` and `docs/SKILL_CATALOG.md` current.
- Require `make check` for all pull requests.
- Keep README links and docs category links green.
- Preserve the no-paid/proprietary-core scope rule for new listings.
- Keep `catalog/provenance.json`, `docs/LICENSE_AUDIT.md`, and `docs/SKILL_AUDIT.md` current.
- Use [`docs/search.html`](search.html) as the lightweight searchable catalog.
- Keep GitHub Actions passing `scripts/validate-workflows.py` and review OpenSSF Scorecard findings.

## Next

- Enrich provenance metadata with exact vendored commits where upstream snapshots are known.
- Add screenshots or rendered previews for the flagship demo pages.
- Add scheduled external-link triage notes to releases when weekly checks fail.
- Convert the flagship eval prompts into executable scorecards where artifacts can be generated in CI without paid APIs.
- Replace manual release notes with a generated release snapshot once the catalog/eval metadata stabilizes.

## Later

- Package first-party AERS skills as installable bundles for agent runtimes that support plugins/marketplaces.
- Add per-skill eval prompts for flagship first-party skills.
- Maintain a public benchmark of empirical-research agent workflows: correctness, reproducibility, citation hygiene, and runtime safety.

## Completed Hardening Pass

- Generated machine-readable catalog and provenance metadata.
- Added license audit, skill hygiene audit, static search page, install guide, submission guide, flagship demos, release process, external-link workflow, and clean CI validation.
- Added machine-readable flagship eval prompts and generated reviewer docs.
