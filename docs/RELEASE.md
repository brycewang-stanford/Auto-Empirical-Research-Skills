# Release Process

AERS releases should be lightweight, reproducible, and useful for citation.

## Version Format

Use calendar versions:

```text
vYYYY.MM
```

Patch releases can use:

```text
vYYYY.MM.patchN
```

## Pre-Release Checklist

```bash
git fetch origin
make catalog
make validate
python3 -m py_compile scripts/*.py
git diff --check
```

Then review:

- [`CHANGELOG.md`](../CHANGELOG.md)
- [`docs/LICENSE_AUDIT.md`](LICENSE_AUDIT.md)
- [`docs/SKILL_CATALOG.md`](SKILL_CATALOG.md)
- [`catalog/skills.json`](../catalog/skills.json)
- [`catalog/provenance.json`](../catalog/provenance.json)

## Release Notes Template

```markdown
## Highlights

- 

## Catalog Stats

- Top-level collections:
- SKILL.md files:
- License buckets:

## Quality Checks

- `make validate`:
- `python3 -m py_compile scripts/*.py`:
- `git diff --check`:

## Known Follow-Ups

- 
```

## Tagging

```bash
git tag -a vYYYY.MM -m "AERS vYYYY.MM"
git push origin vYYYY.MM
```

Create the GitHub Release from the tag and paste the release notes.
