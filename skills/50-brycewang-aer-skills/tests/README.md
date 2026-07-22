# Test Suite

Hermetic pytest suite for the repository's quality tooling (`scripts/`) and the
shared demo helper (`examples/_aer_numeric_check.py`). No network access, no
optional heavy dependencies (R, statsmodels, matplotlib are not required), and
all filesystem writes go to pytest `tmp_path` fixtures.

## Run

```bash
python3 -m pytest tests/ -q
```

Skip the slower full-validator run:

```bash
python3 -m pytest tests/ -q -m "not slow"
```

## Layout

| File | Covers |
| --- | --- |
| `conftest.py` | Puts `scripts/` and `examples/` on `sys.path`; registers the `slow` marker |
| `test_numeric_check.py` | NUMERIC-CHECK protocol: tolerance/bounds semantics, protocol line format |
| `test_run_example_smoke.py` | Protocol-line counting, output tails, dependency name mapping, demo iteration |
| `test_validate_repo.py` | Pure parsing helpers (deps, slugs, code spans, tool bindings) and registry/disk consistency |
| `test_verify_citations.py` | Bib parsing, verdict classification, cite extraction, groundedness, offline gold set |
| `test_skill_audit.py` | Scorer dimensions, substance anchors, and the Makefile audit-gate invariants |
| `test_scaffold_project.py` | Template scaffolding into `tmp_path` and safety refusals |
| `test_install_skills.py` | Destination resolution (monkeypatched HOME), install/skip/replace, safety guards |
| `test_repo_gates.py` | Each tool run as a subprocess: validator, selftests, routing gate, offline citation gates |

## Notes

- Tests never modify files outside `tmp_path` and never touch `~/.claude` or
  `~/.codex` (HOME is monkeypatched where needed).
- The working tree may carry in-progress validator errors outside `tests/`
  (e.g. new `docs/*.md` files not yet linked from the READMEs).
  `test_repo_gates.py` therefore asserts that `tests/` itself introduces no
  validator errors, and marks the full-exit-zero validator run as `xfail`
  until the tree is clean.
