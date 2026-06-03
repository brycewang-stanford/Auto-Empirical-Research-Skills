<!-- Vendored into AERS from https://github.com/shiquda/openalex-skill on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`shiquda/openalex-skill`](https://github.com/shiquda/openalex-skill) for the AERS catalog (license: MIT). Vendored 2026-06-01. The original upstream README follows verbatim.

---

# OpenAlex Skill

`openalex` is a human-friendly and agent-friendly CLI for the OpenAlex API. It is designed for fast literature lookup, citation tracing, author/institution discovery, and field projection without forcing users into raw JSON by default.

## Install in 10 Seconds

Choose the path that matches your environment:

- skill-aware agents: install the repo skill with `npx skills add`
- local shell or plain CLI use: install the npm package and run `openalex`

### For skill-aware agents

Install the `openalex` skill from this repository:

```bash
npx skills add shiquda/openalex-skill --skill openalex
```

This installs the skill instructions, not the CLI binary itself. You still need the `openalex` command available, either by installing the npm package below or by letting your agent finish the setup steps in the skill guide.

### For local shell or plain CLI use

If your environment does not support repo-distributed skills yet, install the CLI directly:

```bash
npm install -g openalex-skill
openalex --help
```

## Why Use It

- human-readable output by default
- targeted extraction with `--field`
- server-side narrowing with `--select` when OpenAlex supports it
- works, authors, sources, institutions, topics, publishers, funders, and concepts
- helper flows for `related`, `cited-by`, and `references`
- built-in single-work full-text download when OpenAlex exposes a direct file URL
- bare DOI input accepted everywhere (`10.xxxx/...`, `doi:...`, full URL all work)
- `--all` for automatic cursor pagination across any list command
- `--format bibtex` for direct citation export from works
- automatic retry with backoff on `429` and server errors

## Quick Start

```bash
npm install -g openalex-skill
openalex --help
openalex --version
openalex works search "llm agents" --per-page 5
openalex works search "llm agents" --all --format jsonl
openalex works get https://doi.org/10.1038/nature12373
openalex works get 10.1038/nature12373
openalex works download https://doi.org/10.1038/nature12373
openalex works cited-by doi:10.1038/nature12373 --per-page 5
```

Optional but recommended for higher quotas:

```bash
openalex config set api-key your_key_here
openalex config show
```

## Core Examples

Search papers:

```bash
openalex works search "retrieval augmented generation" --per-page 5
```

Get a work by DOI or OpenAlex ID:

```bash
openalex works get https://doi.org/10.1038/nature12373
openalex works get 10.1038/nature12373
openalex works get W2741809807
```

Download the best available direct full-text file for one work:

```bash
openalex works download https://doi.org/10.1038/nature12373
openalex works download 10.1038/nature12373
openalex works download W2741809807 --output ./nature12373.pdf
```

Trace citations:

```bash
openalex works cited-by https://doi.org/10.1038/nature12373 --per-page 5
openalex works cited-by 10.1038/nature12373 --per-page 5
openalex works references W2741809807 --per-page 5
openalex works related W2741809807 --per-page 5
```

`cited-by`, `references`, and `related` accept either a DOI or an OpenAlex work ID.

Find authors and their works:

```bash
openalex authors search "Geoffrey Hinton" --per-page 3
openalex authors get https://orcid.org/0000-0002-3141-5845
openalex works list --filter author.id:A5070829652 --per-page 5
```

Group and analyze:

```bash
openalex works group --by publication_year --filter author.id:A5070829652
openalex rate-limit
```

## Output Model

Default output is `summary`, which is optimized for both humans and agents.

Available formats:

- `summary` - concise, readable, high-signal output
- `detail` - readable structured output without transport noise
- `json` - full structured payload
- `jsonl` - one JSON object per line
- `markdown` - heading plus JSON block
- `bibtex` - BibTeX entries for work records

In `summary`, entity rows keep the human-readable title on the first line and include reusable identifiers such as OpenAlex IDs on the secondary line when available.

Quick examples:

```bash
openalex works search "crispr" --per-page 3
openalex --format detail works get W2741809807
openalex works search "crispr" --all --format jsonl
openalex works get 10.1038/nature12373 --format bibtex
```

## Field Control

Use `--field` for client-side projection after the response arrives:

```bash
openalex works fields
openalex works get W2741809807 \
  --format detail \
  --field title \
  --field abstract \
  --field authorships.author.display_name
```

Use `--select` for server-side field selection when OpenAlex supports it:

```bash
openalex works search "crispr" \
  --select id \
  --select title \
  --select cited_by_count
```

Important `--select` caveats:

- OpenAlex only supports selecting root-level fields
- `group` and `autocomplete` do not support `--select`
- `abstract` and `abstract_inverted_index` are not selectable upstream
- if you need abstract text, prefer `--field abstract` and avoid `--select` for that request

## Configuration

- `OPENALEX_API_KEY` - recommended for search and higher-volume use
- `OPENALEX_BASE_URL` - defaults to `https://api.openalex.org`
- `OPENALEX_MAILTO` - optional contact email

Example:

Bash:

```bash
export OPENALEX_API_KEY=your_key_here
openalex works search "graph neural networks" --per-page 5
```

PowerShell:

```powershell
$env:OPENALEX_API_KEY="your_key_here"
openalex works search "graph neural networks" --per-page 5
```

`openalex` can also store user-level settings in `~/.openalex-skill/config.json`.

Priority order:

- environment variables override stored config
- stored config overrides built-in defaults

Useful commands:

```bash
openalex config
openalex config show
openalex config path
openalex config set api-key your_key_here
openalex config unset api-key
```

## Pagination and Reliability

- Use `--all` on list-style commands to auto-follow cursor pagination until OpenAlex stops returning `next_cursor`
- `--all` uses cursor pagination and cannot be combined with `--page`
- transient upstream failures such as `429` and `503` are retried automatically with backoff

Examples:

```bash
openalex works search "llm agents" --all --per-page 200 --format jsonl
openalex works cited-by 10.1038/nature12373 --all --per-page 100
```

## Filter Notes

- `works` filters pass straight through to OpenAlex; the CLI does not rename filter fields for you
- `authors` institution examples use `last_known_institutions.id:I123456`
- `works` institution-related filters depend on the OpenAlex field path you want to target, so prefer verifying with `--format json` if a filter returns no rows

## Skills

This repository also includes an installable skill definition under `skills/openalex/`. Skill-specific operational guidance lives in `skills/openalex/SKILL.md`.

## Development

```bash
npm install
npm run build
npm exec --package=. openalex -- --help
npm test
npm run typecheck
npm run pack:dry-run
```

## Useful Links

Official OpenAlex resources:

- API docs: <https://docs.openalex.org>
- LLM quick reference: <https://docs.openalex.org/api-guide-for-llms>
- Official bulk-download CLI: <https://github.com/ourresearch/openalex-official>
- API key signup: <https://openalex.org/settings/api>

Use `openalex-official` for large bulk-download workflows. Use `openalex` for interactive querying, lookup, single-work download, citation tracing, grouping, and field projection.
