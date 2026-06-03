# Multi-Agent Coordination

AERS often has automated sync workflows and human or agent contributors editing at the same time. Use this protocol to keep parallel work reviewable.

## Before Editing

```bash
git fetch origin
git status --short --branch
```

- If `origin/main` moved, inspect the incoming diff before editing shared files.
- Prefer small, themed changes. Avoid mixing vendored skill syncs with docs, CI, or generated catalog changes.
- Do not hand-edit generated files unless the generator is broken.

## Low-Conflict Work Areas

- New docs under `docs/` with stable links.
- New scripts under `scripts/` that are wired into `make validate` or `make check`.
- New machine-readable metadata under a dedicated top-level directory such as `evals/`.
- GitHub templates and workflow hardening, when kept narrowly scoped.

## High-Conflict Work Areas

- `skills/00-Full-empirical-analysis-skill_StatsPAI/`
- `skills/50-brycewang-aer-skills/`
- Generated outputs: `catalog/*.json`, `docs/SKILL_CATALOG.md`, `docs/LICENSE_AUDIT.md`, `docs/SKILL_AUDIT.md`, `docs/EVALS.md`
- Large demo output directories under `demo-notebooks/`

If you need to edit a high-conflict area, keep the diff isolated and run the relevant generator immediately after the source edit.

## Generated File Rules

| Generated file | Source | Command |
|---|---|---|
| `catalog/skills.json` | `skills/**/SKILL.md`, provenance metadata | `make catalog` |
| `docs/SKILL_CATALOG.md` | `scripts/build-catalog.py` | `make catalog` |
| `catalog/provenance.json` | `scripts/build-provenance.py` | `make catalog` |
| `docs/LICENSE_AUDIT.md` | `scripts/build-provenance.py` | `make catalog` |
| `catalog/skill-audit.json` | `scripts/build-skill-audit.py` | `make catalog` |
| `docs/SKILL_AUDIT.md` | `scripts/build-skill-audit.py` | `make catalog` |
| `docs/EVALS.md` | `evals/flagship-evals.json` | `make evals` or `make catalog` |

## Handoff Checklist

```bash
make catalog
make check
make python-compat
git diff --check
make hygiene
git status --short
```

In the handoff, state:

- Which paths changed.
- Which checks passed.
- Whether any generated files changed.
- Which areas were intentionally avoided to reduce conflicts.
