# Citation-integrity protocol

AER-Skills states a hard design principle: **no citation is written from memory —
every reference is verified against a fetched source.** This document describes
the executable check that makes that principle reproducible:
[`scripts/verify_citations.py`](../scripts/verify_citations.py).

The header of [`references.bib`](../references.bib) claims that every entry "was
verified against the Crossref REST API by DOI." Before this tool, that claim was
a one-time manual act with no way to re-run it. `verify_citations.py` turns it
into a check that anyone — human or agent — can run on demand, offline in CI and
online against the live indexes.

## What it checks

For each bibliography entry the verifier resolves the DOI against the
[Crossref REST API](https://api.crossref.org), falling back to
[OpenAlex](https://api.openalex.org), and compares the resolved record against
the entry's title, authors, and year. It also checks two-way correspondence
between a manuscript's `\cite{...}` keys and the bibliography.

### Verdicts

| Verdict | Severity | Meaning |
|---|---|---|
| `VERIFIED` | ok | DOI resolves; title, first author, and year all match the index of record. |
| `STRUCTURAL_OK` | ok | DOI is well-formed; metadata not checked (no-network mode). |
| `EXEMPT` | ok | No DOI, but a `note` documents why (e.g. predates AEA Crossref DOIs). |
| `MISSING_DOI` | warn | No DOI and no explanatory note — add one or the other. |
| `UNRESOLVED` | warn | An index could not be reached (network error / timeout), not a "not found". |
| `UNCITED` | warn | Defined in `references.bib` but never cited in the manuscript. |
| `BAD_DOI` | fail | DOI is structurally malformed (does not start with `10.`). |
| `FABRICATED` | fail | DOI resolves in **no** index — the hallmark of an invented citation. |
| `UNDEFINED_CITATION` | fail | Cited in the manuscript but absent from `references.bib`. |
| `TITLE_MISMATCH` | fail | DOI resolves, but to a different title — likely a mis-attribution. |
| `AUTHOR_MISMATCH` | fail | The entry's first author is absent from the resolved record's authors. |
| `YEAR_MISMATCH` | fail | The entry's year differs from the record's by more than one. |

Any `fail` makes the tool exit non-zero. `warn` is reported but tolerated. The
year tolerance of one absorbs the common print-year vs. online-first-year gap;
title matching uses a normalized sequence-and-token similarity so subtitle and
casing differences do not trip a false alarm.

## Modes

```bash
# Hermetic regression gate — runs in CI, no network. Validates the engine
# against the labeled gold set and re-checks references.bib against recorded data.
python3 scripts/verify_citations.py --selftest

# Re-verify references.bib against the recorded Crossref/OpenAlex responses (hermetic).
python3 scripts/verify_citations.py --offline

# Live verification against the real indexes.
python3 scripts/verify_citations.py --online

# Structural-only check (no network): DOI well-formedness + no-DOI notes.
python3 scripts/verify_citations.py

# Two-way \cite <-> bib check for a manuscript (combine with --online for both at once).
python3 scripts/verify_citations.py --online --manuscript paper.tex

# Machine-readable output for downstream tooling.
python3 scripts/verify_citations.py --online --json
```

The manuscript check recognizes LaTeX (`\cite`, `\citep`, `\citet`,
`\textcite`, `\parencite`, comma-separated keys, …) and Pandoc/Markdown
`[@key]` citation forms.

## How this maps to the skills

- [`aer-literature`](../skills/aer-literature/SKILL.md) owns the
  citation-integrity protocol at the prose level — closest-papers mapping and
  the rule that no reference enters the manuscript unverified. This script is
  the runnable backstop for that rule.
- [`aer-consistency`](../skills/aer-consistency/SKILL.md) audits full-manuscript
  integrity, including the two-way citation match. `--manuscript` makes that
  match executable against a draft.

## Maintaining the recorded fixtures

The offline modes (`--selftest`, `--offline`) read recorded index responses from
[`scripts/citation_gold/`](../scripts/citation_gold/), so they are deterministic
and need no network. When `references.bib` changes, regenerate the real
responses with one live pass:

```bash
python3 scripts/verify_citations.py --record-from-bib
```

That command preserves the hand-authored fabricated / unreachable fixtures used
by the gold set and refreshes only the real DOI records. See the gold-set
[README](../scripts/citation_gold/README.md) for the fixture layout.

## CI integration

`make verify-citations` runs the live check; the hermetic `--selftest` runs
inside `make preflight` next to the other gates, so a regression in the
verifier or a drift in the shipped bibliography fails the build without
requiring network access.

## Limitations

- The BibTeX parser is tolerant, not a full BibTeX engine; exotic `@string`
  macros and concatenations are not expanded.
- Verification depends on Crossref / OpenAlex coverage. Genuinely DOI-less works
  (older AER articles, working papers) must carry a `note` to be `EXEMPT`.
- A `UNRESOLVED` verdict means "could not reach the index," not "fabricated" —
  re-run online when connectivity is restored before trusting a clean result.
