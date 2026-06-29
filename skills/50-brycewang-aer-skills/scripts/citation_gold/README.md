# Citation gold set

Fixtures for [`scripts/verify_citations.py`](../verify_citations.py). They let
the verifier run **hermetically** — no network — in `--selftest` and `--offline`
modes, so CI is deterministic and the shipped bibliography is continuously
checked against the metadata it was verified against.

## Files

| File | Purpose |
|---|---|
| `recorded_responses.json` | Normalized Crossref/OpenAlex responses keyed by DOI. Holds the real record for every DOI in [`references.bib`](../../references.bib) plus three synthetic fixtures (two non-resolving DOIs and one unreachable-index DOI). |
| `gold_set.json` | Twelve labeled tuples, each a synthetic bib entry exercising one verdict path of the verifier (`VERIFIED`, `FABRICATED`, `TITLE_MISMATCH`, `AUTHOR_MISMATCH`, `YEAR_MISMATCH`, `EXEMPT`, `MISSING_DOI`, `BAD_DOI`, `UNRESOLVED`). |

The design mirrors the reference repository's
`evals/gold/citation_extraction` (valid-DOI / fabricated / manual-exempt
classes), specialized to economics: the valid cases reuse real AER, QJE, and
Econometrica DOIs, and the mismatch cases reuse a real DOI with deliberately
wrong metadata.

## Regenerating

`recorded_responses.json` is generated from the live indexes; do not edit the
real entries by hand. After changing `references.bib`, refresh it with:

```bash
python3 scripts/verify_citations.py --record-from-bib
```

That pass refreshes only the real DOI records and preserves the three
hand-authored synthetic fixtures. Then confirm the gate still passes:

```bash
python3 scripts/verify_citations.py --selftest
```

## Why recorded responses are tracked

These JSON files are inputs to a regression gate, not generated build output, so
they are committed deliberately. They are small, deterministic, and reviewed in
diffs like any other fixture — the same way the reference repository tracks its
`scripts/fixtures/` and `evals/gold/` trees.
