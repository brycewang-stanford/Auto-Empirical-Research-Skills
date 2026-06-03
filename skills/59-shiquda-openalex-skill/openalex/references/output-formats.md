# OpenAlex CLI Output Formats

Detailed guide for output formats and field selection options.

## Format Options

### `summary` (default, recommended for AI)
Concise one-line format with key metadata and reusable identifiers.

Example:
```
- Attention Is All You Need (2017 | cited 6519 | OA gold | Neural Information Processing Systems)
  id: W2741809807  |  authors: Vaswani, Shazeer, Parmar + 5 more  |  doi: https://doi.org/10.48550/arXiv.1706.03762
```

The secondary line shows reusable IDs you can copy for follow-up commands:
- **Works**: `id` (W-prefixed, required for `cited-by`/`references`), `authors`, `doi`
- **Authors**: `id` (A-prefixed), `orcid`
- **Institutions**: `id` (I-prefixed), `ror`
- Other entities show their respective IDs

- Token usage: ~2KB for 5 results
- Each entity type has specialized formatting (works show citations, authors show h-index, etc.)

### `detail`
Human-readable structured output with business fields only.

- Hides transport noise (request URLs, rate-limit headers)
- Reconstructs friendly fields like `abstract` from inverted index
- **Inlines short projected scalar lists** for readability (e.g., authors displayed as "Alice, Bob, Charlie")
- Good for exploring data structure without JSON verbosity

### `json`
Full structured payload.

- Token usage: ~40KB-268KB per query
- Use only when you need complete data or specific nested fields

### `jsonl`
One JSON object per line. Good for streaming or line-by-line processing.

### `markdown`
Heading + JSON block. Useful for documentation or reports.

### `bibtex`
BibTeX entries for work records.

- best for citation-manager import or quick `.bib` export
- uses OpenAlex work metadata directly, so no extra DOI lookup is required
- works especially well with direct DOI lookups and `--field` is usually unnecessary here

## Field Projection with `--field`

**Client-side projection** - fetch full payload first, then display only requested fields:

```bash
# Discover available fields first
openalex works fields

# Extract specific fields (repeatable)
openalex works get W2741809807 \
  --field title \
  --field abstract \
  --field authorships.author.display_name \
  --field doi

# detail format with field projection (authors shown inline)
openalex works search "crispr" --per-page 3 \
  --format detail \
  --field title \
  --field abstract \
  --field cited_by_count

# export one work as BibTeX
openalex works get 10.1038/nature12373 --format bibtex
```

**Key behaviors:**
- `--field` works with `detail`, `json`, `jsonl`, and `markdown` formats
- When requesting `abstract`, CLI reconstructs it from `abstract_inverted_index` when possible
- In `detail` format, repeated scalar paths like `authorships.author.display_name` are shown as **inline readable lists** instead of nested structures

## Server-side Selection with `--select`

**Server-side filtering** - ask OpenAlex API to return fewer fields (reduces network payload):

```bash
openalex works search "crispr" \
  --select id \
  --select title \
  --select cited_by_count
```

**Key behaviors:**
- `--select` reduces upstream payload size
- Available on `get`, `random`, `list`, `search`, `related`, `cited-by`, and `references`
- `group` does not support `--select`, but still supports `--field`
- OpenAlex only supports selecting root-level fields
- `abstract` and `abstract_inverted_index` are not selectable upstream

## Combining `--select` and `--field`

**Best practice**: Use `--select` for network efficiency, `--field` for presentation control:

```bash
# Server-side: only fetch necessary fields
# Client-side: display as curated view
openalex works search "crispr" --per-page 3 \
  --select id \
  --select title \
  --select cited_by_count \
  --field title \
  --field cited_by_count
```

**Important**: `--field abstract` and `--select` do not combine well, because OpenAlex does not let you select abstract fields upstream. If you need abstract text, avoid `--select` for that request and let the CLI reconstruct it from the full work payload.

## Format Selection Guide

**Use `summary` when:**
- Browsing or exploring results
- User wants a quick overview
- You need basic metadata (title, year, citations, authors)
- Token efficiency matters (99% reduction vs JSON)

**Use `detail` when:**
- You need structured data but JSON is too verbose
- Exploring nested fields without transport noise
- Want readable output with inline lists for repeated fields

**Use `--field` projection when:**
- You know exactly which fields you need
- Want to minimize tokens while keeping structure
- Need specific nested paths (e.g., `authorships.author.display_name`)

**Use `--select` when:**
- You want to reduce network payload from OpenAlex
- The endpoint supports official OpenAlex field selection
- Combining with `--field` for both efficiency and presentation

**Use `json` when:**
- You need the complete raw payload
- Programmatic processing of all fields required
- User explicitly asks for structured data

## Example comparison

```bash
# Most efficient: ~2KB for 5 results
openalex works search "LLM agents" --per-page 5

# Fetch all pages with cursor pagination
openalex works search "LLM agents" --all --per-page 200 --format jsonl

# Structured but readable with inline lists: ~10KB for 5 results
openalex works search "LLM agents" --per-page 5 --format detail

# Targeted extraction: ~5KB for 5 results
openalex works search "LLM agents" --per-page 5 \
  --format detail --field title --field abstract --field cited_by_count

# Network optimized + presentation curated
openalex works search "LLM agents" --per-page 5 \
  --select title --select cited_by_count \
  --field title --field cited_by_count

# Full payload: ~268KB for 5 results
openalex works search "LLM agents" --per-page 5 --format json

# Citation export
openalex works get 10.1038/nature12373 --format bibtex
```

## `--select` caveats

- OpenAlex `select` only supports root-level fields
- `group` and `autocomplete` do not support `select`
- `abstract` and `abstract_inverted_index` are not selectable upstream
- if you need abstract text, use `--field abstract` or fetch the full work object first

## ORCID format matters

```bash
# Wrong: using full ORCID URL in filter
openalex works list --filter author.orcid:https://orcid.org/0000-0002-3141-5845

# Correct: bare ORCID value
openalex works list --filter author.orcid:0000-0002-3141-5845

# But ORCID URL works for 'authors get'
openalex authors get https://orcid.org/0000-0002-3141-5845
```
