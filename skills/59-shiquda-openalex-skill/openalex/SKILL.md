---
name: openalex
description: Use when the user asks about academic literature, research papers, scholarly works, authors, citations, institutions, journals, or any academic metadata. Trigger when users want to search for papers, find author profiles, track citations, discover related works, or explore academic topics. Also use when users mention DOIs, ORCIDs, h-index, publication venues, or research metrics.
---

# OpenAlex CLI Skill

Use the `openalex` CLI to retrieve academic metadata from the OpenAlex API.

## When to Use

Invoke this skill when the user needs to:
- Search for academic papers or scholarly works
- Find information about authors, institutions, or journals
- Track citations (who cited a paper, what a paper references)
- Discover related works or research topics
- Look up metadata by DOI, ORCID, or OpenAlex ID
- Analyze publication trends or research metrics

## Initial Setup

**First time using this skill?** Read [references/setup.md](references/setup.md) for installation and API key configuration.

## Prerequisites

The CLI must be built and available. Check with:
```bash
openalex --help
```

If `openalex` is not installed yet, install it first:
```bash
npm install -g openalex-skill
openalex --help
```

For installation, persistent API key setup, and first-run verification, see `references/setup.md`.

## Core Commands

### Entity Types
OpenAlex organizes data into 8 entity types:
- `works` - research papers, articles, preprints
- `authors` - researchers and their profiles
- `sources` - journals, conferences, repositories
- `institutions` - universities, research centers
- `topics` - research areas and subjects
- `publishers` - academic publishers
- `funders` - funding organizations
- `concepts` - (legacy) subject classifications

### OpenAlex ID Format

**ID format:** OpenAlex IDs start with `W` (e.g., `W2626778328`). The `summary` format displays reusable IDs on a secondary line:

```
- Attention Is All You Need (2017 | cited 6519)
  id: W2741809807  |  authors: Vaswani et al  |  doi: https://doi.org/10.48550/arXiv.1706.03762
```

**Get ID from search results:**
```bash
openalex works search "paper title" --per-page 1
# Copy the `id: Wxxxx` from the output
```

**⚠️ ID usage restrictions:**
- `cited-by`, `references`, and `related` support both DOI and OpenAlex ID
- bare DOIs like `10.1038/nature12373` and `doi:10.1038/nature12373` are normalized automatically for work lookups and helpers
- OpenAlex IDs are still the most reusable follow-up identifiers when chaining multiple commands

### Common Operations

**Search for papers:**
```bash
openalex works search "your query" --per-page 5
```

**Get specific work by ID or DOI:**
```bash
openalex works get W2741809807
openalex works get https://doi.org/10.1038/nature12373
openalex works get 10.1038/nature12373
```

**Find author:**
```bash
openalex authors search "Author Name" --per-page 3
```

**Get author by ORCID:**
```bash
openalex authors get https://orcid.org/0000-0002-3141-5845
```

**Track citations:**
```bash
# Papers that cite this work
openalex works cited-by W2741809807 --per-page 5
openalex works cited-by 10.1038/nature12373 --per-page 5
openalex works cited-by https://doi.org/10.1038/nature12373 --per-page 5

# Papers this work references
openalex works references W2741809807 --per-page 5
openalex works references https://doi.org/10.1038/nature12373 --per-page 5

# Related works
openalex works related W2741809807 --per-page 5
openalex works related https://doi.org/10.1038/nature12373 --per-page 5
```

**Filter and sort:**
```bash
openalex works list \
  --filter publication_year:2024 \
  --filter is_oa:true \
  --sort cited_by_count:desc \
  --per-page 10
```

**Autocomplete (for non-works entities):**
```bash
openalex institutions autocomplete "tsinghua"
openalex authors autocomplete "einstein"
```

**Group by field:**
```bash
openalex works group --by publication_year \
  --filter author.id:A5070829652
```

**Download full-text PDF:**
```bash
# Download the best available open access PDF for a work
openalex works download https://doi.org/10.48550/arXiv.1706.03762
openalex works download 10.48550/arXiv.1706.03762

# Specify output filename
openalex works download W2741809807 -o paper.pdf

# Overwrite existing file
openalex works download W2741809807 --overwrite
```

The download command tries multiple sources in order:
1. `primary_location.pdf_url`
2. `best_oa_location.pdf_url`
3. `open_access.oa_url`
4. `primary_location.landing_page_url`
5. `best_oa_location.landing_page_url`
6. Any `locations[].pdf_url` or `locations[].landing_page_url`

Default filename is based on DOI or OpenAlex ID (sanitized for filesystem safety).

## Output Formats

The CLI defaults to `summary` format. For detailed format options, see [references/output-formats.md](references/output-formats.md).

**Quick reference:**
- `summary` (default) - Concise one-line format, ~2KB for 5 results
- `detail` - Human-readable with inline lists for repeated fields
- `json` - Full structured payload, ~40KB-268KB per query
- `bibtex` - BibTeX entries for work records
- `--field <path>` - Client-side projection to extract specific fields
- `--select <field>` - Server-side selection to reduce network payload

**Common patterns:**
```bash
# Extract specific fields
openalex works get W2741809807 --field title --field abstract

# Export a work as BibTeX
openalex works get 10.1038/nature12373 --format bibtex

# Combine server-side + client-side for efficiency
openalex works search "crispr" --select title --select cited_by_count \
  --field title --field cited_by_count
```

**Note:** `--field abstract` and `--select` don't combine well; use `--field abstract` alone when you need abstract text.

## Workflow Patterns

### Pattern 1: Quick Paper Search
```bash
# Start with summary to browse
openalex works search "graph neural networks" --per-page 5

# If user wants details on a specific paper, use detail format
openalex works get W2741809807 --format detail

# Or extract specific fields with inline author display
openalex works get W2741809807 \
  --format detail \
  --field title --field abstract --field authorships.author.display_name
```

### Pattern 2: Author Research
```bash
# Find author
openalex authors search "Jacob Andreas" --per-page 3

# Get author details by ORCID to resolve stable identifier
openalex authors get https://orcid.org/0000-0002-3141-5845

# Then use author.orcid filter to get their works
openalex works list --filter author.orcid:0000-0002-3141-5845 \
  --sort cited_by_count:desc --per-page 10

# Or use resolved author.id if available
openalex works list --filter author.id:A5070829652 \
  --sort cited_by_count:desc --per-page 10
```

### Pattern 3: Citation Analysis

```bash
# Search for a paper, note the ID from the secondary line
openalex works search "attention is all you need" --per-page 3

# Use the ID (e.g., W2741809807) or DOI for citation commands
openalex works cited-by W2741809807 --per-page 10
openalex works references W2741809807 --per-page 10
```

If `cited-by` or `references` returns a 404, verify the work first with `openalex works get <id-or-doi>`.
A valid-looking `W...` id can still be missing upstream.

### Pattern 4: Topic Exploration
```bash
# Search for survey papers on a topic
openalex works search "LLM tool use survey" \
  --filter publication_year:>2023 \
  --filter type:review \
  --sort cited_by_count:desc \
  --per-page 5
```

### Pattern 5: Field Discovery and Extraction
```bash
# First, discover available fields
openalex works fields

# Then extract exactly what you need with detail format
openalex works search "retrieval augmented generation" --per-page 3 \
  --format detail \
  --field title \
  --field abstract \
  --field publication_year \
  --field cited_by_count \
  --field authorships.author.display_name
```

### Pattern 6: Handling Noisy or Empty Results

**Search too broad? Add filters:**
```bash
openalex works search "self-adaptive agent framework" \
  --filter publication_year:>2022 \
  --filter type:article \
  --per-page 5
```

**Have a DOI? Use direct lookup:**
```bash
openalex works get https://doi.org/10.1038/nature12373
```

### Pattern 7: Download Full-Text Papers

```bash
# Download by DOI or OpenAlex ID
openalex works download https://doi.org/10.48550/arXiv.1706.03762
openalex works download W2626778328 -o paper.pdf --overwrite
```

Download tries multiple sources in order: `primary_location.pdf_url`, `best_oa_location.pdf_url`, `open_access.oa_url`, then landing pages.

**`--select` caveats:**
- OpenAlex `select` only supports root-level fields
- `group` and `autocomplete` do not support `select`
- `abstract` and `abstract_inverted_index` are not selectable upstream

**ORCID format matters:**
```bash
# Wrong: using full ORCID URL in filter
openalex works list --filter author.orcid:https://orcid.org/0000-0002-3141-5845

# Correct: bare ORCID value
openalex works list --filter author.orcid:0000-0002-3141-5845

# But ORCID URL works for 'authors get'
openalex authors get https://orcid.org/0000-0002-3141-5845
```

## Tips

- **Default format is `summary`** - no need to specify unless you want something else
- Use `<entity> fields` command to discover available field paths before querying
- Use `--field` projection to extract specific data efficiently
- Use `--select` for network efficiency when you know which fields you need
- Combine `--select` and `--field` for optimal performance and presentation
- Use `--per-page` to control result count (default varies by endpoint)
- Use `--all` to auto-follow cursor pagination for list-style commands
- Filters use `:` syntax: `field:value`, `field:>value`, `field:<value`
- Sort uses `:` syntax: `field:asc` or `field:desc`
- DOIs and OpenAlex IDs are interchangeable in most commands
- **ORCID filters use bare ORCID value**, not the `https://orcid.org/` URL form
- If author work lookup returns nothing, use `author.orcid` instead of `author.id`
- If `cited-by` or `references` fails with 404, verify the work first with `works get`
- For some preprint or repository records, the queried DOI and the record DOI may differ; use `detail` or `json` when provenance matters
- Check rate limits with: `openalex rate-limit`

## Configuration Commands

The CLI supports persistent configuration for API keys and other settings.

**View current configuration:**
```bash
openalex config show
```

**Set API key (recommended):**
```bash
openalex config set api-key your_key_here
```

**Other config options:**
```bash
openalex config set base-url https://api.openalex.org
openalex config set mailto you@example.com
```

**View config file path:**
```bash
openalex config path
```

**Remove a setting:**
```bash
openalex config unset api-key
```

Configuration is stored in `~/.openalex-skill/config.json`. Environment variables (`OPENALEX_API_KEY`, `OPENALEX_BASE_URL`, `OPENALEX_MAILTO`) override stored config.

## Common Filters

For `works`:
- `publication_year:2024` or `publication_year:>2020`
- `is_oa:true` (open access)
- `type:article` or `type:review`
- `author.id:A5070829652`
- `author.orcid:0000-0002-3141-5845`
- institution-related filters are passed through as-is; verify the exact OpenAlex path with `--format json` if needed
- `primary_location.source.id:S123456` (journal)

For `authors`:
- `last_known_institutions.id:I123456`
- `works_count:>100`

## Error Handling

If a command fails:
1. Check the entity type is correct (`works`, `authors`, etc.)
2. Verify ID format (OpenAlex IDs start with W/A/S/I/T/P/F/C)
3. Check filter syntax (use `:` not `=`)
4. Try with `--format json` to see full error details
5. If search results are empty, retry with broader keywords
6. If author lookup fails, verify ORCID format (bare value, not URL)
7. Use DOI direct lookup when you know the exact paper
8. If a work helper 404s, the identifier may be valid in shape but absent in OpenAlex
