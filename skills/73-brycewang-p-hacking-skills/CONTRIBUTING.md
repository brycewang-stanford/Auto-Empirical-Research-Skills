# Contributing

This is a research instrument for studying p-hacking. Contributions that make
the search more realistic, the audit more honest, or the tool usable in more
languages are all welcome. Four extension points cover almost everything.

## 1. A new researcher degree of freedom (an axis)

1. Add the key and its default to `grid.DEFAULTS` and, if it should be
   selectable in the pre-registered block, to `grid.AXES` and `Spec`.
2. Enumerate it in `grid.enumerate_specs` (respect the constraints block: an
   axis that is meaningless for a design must be collapsed, not multiplied).
3. Materialise it in `grid.build` and, if it needs an estimator, in `core`.
4. Add it to `search._spec_record`, `search.axis_influence`'s column list and
   `plot.AXES`, and give it a row in `schema` via `grid.card_schema`.
5. Give it a paragraph in `references/taxonomy.md` (which strategy it is,
   why it is defensible, what it costs) and a row in
   `skills/02-forking-paths/SKILL.md`.
6. Runner templates in `phack/polyglot.py`: implement it in the languages
   that can, and write `status = "unsupported: ..."` in the others.
7. Test: enumeration count, materialisation on a synthetic dataset with a
   known answer, and (if it is a lever) that it moves the estimate.

## 2. A new search procedure

```python
class ReferreeTwo(procedures.Procedure):
    name = "referee2"
    def params(self): return {...}
    def walk(self, specs, fit, rng, alpha=0.05, direction=None) -> procedures.Walk:
        ...
procedures.PROCEDURES["referee2"] = ReferreeTwo
```

`walk` must be deterministic given `rng`; that is what lets
`search.null_calibration` replay it and report its false-positive rate.
Document it in `skills/09-search-procedures/SKILL.md`.

## 3. A new language runner

Add a template string to `phack/polyglot.py` and register it in `LANGUAGES`
and `write_runner`. The contract is the file layout in the module docstring:
read `specs.csv` and `data.csv`, write `ledger_raw.csv` with the columns
`key, label, coef, se, t, p, n, status, first_stage_F, bandwidth, n_left,
n_right`, and with `NULL_B > 0` read `null_columns.csv` and write
`null_stats.csv` (`draw, key, coef, t, p`). Run `phack ingest DIR --parity`
and add the parity row to `references/language-map.md`.

## 4. A new ground-truth dataset

Datasets are generated, never hand-edited. Add a generator to
`scripts/make_null_data.py` with a fixed seed, a docstring stating the DGP
and the true effect (zero, or a known value for a positive control), a
design card `eval/data/<name>_card.json` with a `preregistered` block, and
run `python scripts/make_null_data.py --all` so `CHECKSUMS.json` is updated.
Then `phack bench freeze --version X.Y.0`: a new dataset is a new benchmark
version.

## Ground rules

- Every search leaves a complete ledger. A pull request that lets a "best
  specification" be produced without one will not be merged.
- Numbers in documentation are reproduced by `./demo.sh`,
  `scripts/calibrate_engine.py` or `scripts/parity.py`; if you change what
  they compute, regenerate them.
- Tests: `pytest -q` (about a minute). Runner tests skip when the language is
  not installed.
- Style: plain numpy / scipy / pandas; no new hard dependencies without a
  discussion.

## Reporting a parity gap

If a language runner and the engine disagree on a specification by more than
the conventions documented in `references/language-map.md`, open a "parity
report" issue with the card, the row of `specs.csv`, and both numbers.
