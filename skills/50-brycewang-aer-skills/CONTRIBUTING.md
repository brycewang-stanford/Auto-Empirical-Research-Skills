# Contributing

Keep changes scoped and easy to review. This repository is mostly instructions
and templates, so broad rewrites create more merge risk than they remove.

## Concurrent Agent Workflow

When multiple agents or humans are editing at the same time:

1. Start with `git status --short --branch` and inspect existing diffs before
   editing a file.
2. Prefer narrow changes in one area: one skill, one template stack, one doc
   page, or one validation script.
3. Avoid whole-repo formatting, link rewriting, or generated metadata churn
   unless that is the explicit task.
4. Re-run `git status --short` before each patch so you notice new parallel
   edits instead of overwriting them.
5. Use `--dry-run` before broad install or scaffold operations, especially
   when `--replace` is involved.
6. Run `make preflight` before handoff.

If another change touches the same file, read the current file and apply the
smallest compatible patch. Do not revert work you did not make.

## Policy Source Updates

Before changing hard AEA requirements, journal limits, disclosure language, or
replication-package rules, check [`docs/source-register.md`](docs/source-register.md).
Update that register in the same change when an official source changes. This
keeps policy edits localized when multiple agents are working at once.

## Validation

```bash
make preflight
```

`make preflight` runs repository validation plus staged and unstaged
`git diff --check`.
Use `make validate-strict` before release work; it fails instead of warning when
optional tools such as `Rscript` are unavailable.

The validator checks:

- skill frontmatter and `agents/openai.yaml`
- skill directory shape and `SKILL.md` length
- Claude plugin and marketplace manifests
- canonical GitHub repository URLs in install surfaces
- local Markdown links
- exact Python dependency pins
- third-party Python imports in templates/examples mapped to pinned packages
- template and replication skeleton file layout
- installer and scaffolder smoke tests, including unsafe destination refusals
- public CLI script entrypoints and executable bits
- CI workflow wiring
- text hygiene and accidental local absolute paths in executable surfaces
- unfinished-work markers outside approved template and example surfaces
- generated/cache paths are not tracked, except required `.gitkeep` placeholders
- repository resource links in skill `Repository Resources` sections
- `docs/methods-reference.md` citation keys against `references.bib`
- duplicate BibTeX keys and missing DOI / no-DOI notes
- unresolved generic article-link placeholders in Markdown examples
- Python template syntax
- R template syntax when `Rscript` is available
- Stata template version declarations
