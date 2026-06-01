# AERS Quality Gate

This repository is both a public catalog and a vendored skill library. The quality gate keeps it searchable, reproducible, and safer to use with autonomous agents.

## Local Commands

Run these before opening a pull request:

```bash
make catalog
make validate
make check
```

`make catalog` rebuilds:

- `catalog/skills.json` for machines, search UIs, and downstream indexes.
- `catalog/provenance.json` for source, license, and commercial-use metadata.
- `catalog/skill-audit.json` for non-blocking vendored skill hygiene metadata.
- `docs/EVALS.md` from `evals/flagship-evals.json` for flagship regression prompts.
- `docs/SKILL_CATALOG.md` for GitHub browsing.
- `docs/LICENSE_AUDIT.md` and `docs/SKILL_AUDIT.md` for reviewer-facing audits.

For multi-agent work, follow [`docs/AGENT_COORDINATION.md`](AGENT_COORDINATION.md). For recurring maintainer work, follow [`docs/MAINTAINER_PLAYBOOK.md`](MAINTAINER_PLAYBOOK.md).

For a high-level map of the repository trust surface, see [`docs/TRUST.md`](TRUST.md).

`make validate` checks:

- Required project files exist.
- Vendored `skills/**/SKILL.md` frontmatter is audited and summarized.
- AERS-maintained local Markdown links resolve.
- GitHub Actions workflows use explicit permissions and non-persistent checkout credentials.
- The generated catalog is current.
- Generated provenance and skill-audit reports are current.
- Flagship eval prompt docs are current and every referenced skill path exists.

`make check` adds the stdlib unit tests, executable eval-harness lint,
example-candidate grading smoke test, and numeric benchmark. The eval-harness
lint gate enforces minimum scenario count, auto-check count, and category
coverage so accidental eval deletion fails locally and in CI. The benchmark gate
uses `--strict --fail-on-partial --fail-on-orphan-results` so stale generated
scorecards from removed or renamed tasks do not masquerade as current coverage.

## Review Rules

New skills should be accepted only when they are:

- Open source or source-available with a clear license.
- Self-contained enough for researchers to inspect and run independently.
- Relevant to empirical research workflows.
- Free of surprising hooks, credential exfiltration, reverse shells, or prompt-injection instructions.
- Documented in the appropriate `docs/NN-*.md` category.

## Non-Blocking Warnings

The validator warns, but does not fail, when:

- Vendored upstream `SKILL.md` files are missing standard frontmatter. These are tracked as cleanup targets, but preserving upstream content takes priority.
- Vendored upstream files are named `skill.md` rather than exact-case `SKILL.md`; those are not included in generated catalogs until normalized.
- A `SKILL.md` file exceeds 500 lines. Long skills may be legitimate vendored upstream artifacts, but new first-party skills should prefer `references/`.
- Skill names are duplicated. Large vendored packs often reuse generic names, so this is an audit signal rather than an automatic failure.
- A skill name uses non-portable punctuation.

Run `make audit` when you want the warning stream in the terminal.

## CI

`.github/workflows/validate-catalog.yml` runs `make validate` on pushes and pull requests. This makes catalog, provenance, audit, eval-doc, workflow-policy, and local-link drift visible whenever a contributor adds, removes, or moves skills.

`.github/workflows/quality-evals.yml` runs the executable eval harness, stdlib unit tests, and numeric benchmark on Python 3.9 and 3.12. The matrix intentionally covers both the macOS system-Python floor used by many local contributors and a current CI Python.

Dependabot checks GitHub Actions updates weekly via `.github/dependabot.yml`. `.github/workflows/scorecard.yml` runs OpenSSF Scorecard on `main` and uploads SARIF to GitHub code scanning.
