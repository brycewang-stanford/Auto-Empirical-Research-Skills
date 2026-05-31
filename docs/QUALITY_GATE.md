# AERS Quality Gate

This repository is both a public catalog and a vendored skill library. The quality gate keeps it searchable, reproducible, and safer to use with autonomous agents.

## Local Commands

Run these before opening a pull request:

```bash
make catalog
make validate
```

`make catalog` rebuilds:

- `catalog/skills.json` for machines, search UIs, and downstream indexes.
- `catalog/provenance.json` for source, license, and commercial-use metadata.
- `catalog/skill-audit.json` for non-blocking vendored skill hygiene metadata.
- `docs/SKILL_CATALOG.md` for GitHub browsing.
- `docs/LICENSE_AUDIT.md` and `docs/SKILL_AUDIT.md` for reviewer-facing audits.

`make validate` checks:

- Required project files exist.
- Vendored `skills/**/SKILL.md` frontmatter is audited and summarized.
- AERS-maintained local Markdown links resolve.
- The generated catalog is current.
- Generated provenance and skill-audit reports are current.

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

`.github/workflows/validate-catalog.yml` runs the same checks on pushes and pull requests. This makes catalog drift visible whenever a contributor adds, removes, or moves skills.
