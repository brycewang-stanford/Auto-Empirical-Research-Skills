---
name: unpaywall-api
description: "Find free legal full-text versions of scholarly articles via Unpaywall"
metadata:
  openclaw:
    emoji: "🔍"
    category: "literature"
    subcategory: "fulltext"
    keywords: ["full-text retrieval", "open access", "journal copyright policy", "self-archiving"]
    source: "https://unpaywall.org/products/api"
    requires:
      env: ["UNPAYWALL_EMAIL"]
---

# Unpaywall API Guide

## Overview

Unpaywall is a free, open database of over 40 million free scholarly articles. Built by the nonprofit OurResearch, Unpaywall indexes legal open access (OA) copies of papers from thousands of institutional repositories, preprint servers, publisher websites, and government archives. It is the most comprehensive source for finding freely available versions of paywalled academic literature.

Researchers, librarians, and tool developers use Unpaywall to locate open access copies of papers they need, assess the OA status of publications, and integrate OA discovery into their workflows. The database is updated daily, scanning repositories and publisher sites for new open access content. Unpaywall categorizes OA into types: gold (published OA), green (repository copy), hybrid (OA in subscription journal), and bronze (free to read on publisher site).

The API requires only an email address for authentication and is free for non-commercial use with a generous rate limit of 100,000 requests per day.

## Authentication

Authentication is via email address passed as a query parameter. No API key or registration is needed -- just provide a valid email:

```
?email=your@email.com
```

This email is used for contact purposes only and to identify your application. The API will reject requests without a valid email address. For commercial use or higher rate limits, contact OurResearch for an API key.

## Core Endpoints

### DOI Lookup: Find Open Access for a Paper

- **URL**: `GET https://api.unpaywall.org/v2/{doi}`
- **Parameters**:
  | Param | Type | Required | Description |
  |-------|------|----------|-------------|
  | doi | string | Yes | The DOI of the paper (URL-encoded in path) |
  | email | string | Yes | Your email address |
- **Example**:
  ```bash
  curl "https://api.unpaywall.org/v2/10.1038/nature12373?email=user@example.com"
  ```
- **Response**: JSON with comprehensive OA information:
  - `is_oa`: boolean indicating if any OA version exists
  - `best_oa_location`: the best available OA copy with `url`, `url_for_pdf`, `evidence`, `host_type`, `license`, and `version`
  - `oa_locations`: array of all known OA copies
  - `oa_status`: gold, green, hybrid, bronze, or closed
  - `title`, `doi`, `year`, `genre`, `journal_name`, `publisher`

### Batch DOI Lookup: Multiple Papers

- **URL**: `GET https://api.unpaywall.org/v2/{doi}` (repeated per DOI)
- **Parameters**:
  | Param | Type | Required | Description |
  |-------|------|----------|-------------|
  | doi | string | Yes | One DOI per request (batch via multiple requests) |
  | email | string | Yes | Your email address |
- **Example**:
  ```bash
  # Process multiple DOIs sequentially
  for doi in "10.1038/nature12373" "10.1126/science.aaa8685" "10.1016/j.cell.2015.05.002"; do
    curl -s "https://api.unpaywall.org/v2/$doi?email=user@example.com" | jq '{doi: .doi, is_oa: .is_oa, oa_status: .oa_status, best_url: .best_oa_location.url}'
    sleep 0.01
  done
  ```
- **Response**: Same JSON structure as single lookup, for each DOI.

### Data Feed: Bulk Access

For large-scale analyses, Unpaywall provides a complete database snapshot and a weekly data feed, rather than requiring millions of individual API calls. Access is available at https://unpaywall.org/products/data-feed for registered users.

## Rate Limits

The API allows 100,000 requests per day (approximately 1.15 requests per second sustained). There is no strict per-second rate limit, so burst traffic is acceptable as long as the daily cap is respected. Exceeding the limit returns HTTP 429. For analyses requiring more than 100K lookups, use the Unpaywall Data Feed (database snapshot) instead.

## Common Patterns

### Check OA Status for a Reading List

Determine which papers in your reading list have freely available versions:

```bash
curl -s "https://api.unpaywall.org/v2/10.1038/s41586-021-03819-2?email=user@example.com" | jq '{title: .title, is_oa: .is_oa, oa_status: .oa_status, pdf: .best_oa_location.url_for_pdf}'
```

### Find the Best Available PDF

Get a direct link to the best open access PDF for a paper:

```bash
curl -s "https://api.unpaywall.org/v2/10.1145/3292500.3330672?email=user@example.com" | jq '.best_oa_location | {url: .url, pdf: .url_for_pdf, version: .version, license: .license}'
```

### Audit Open Access Compliance for a Grant

Check whether publications from a funded project comply with OA mandates:

```bash
# For each publication DOI from the grant
curl -s "https://api.unpaywall.org/v2/10.1038/nature12373?email=user@example.com" | jq '{doi: .doi, title: .title, is_oa: .is_oa, oa_status: .oa_status, locations: [.oa_locations[] | {host: .host_type, license: .license, version: .version}]}'
```

## References

- Official documentation: https://unpaywall.org/products/api
- Unpaywall data format: https://unpaywall.org/data-format
- OurResearch: https://ourresearch.org/
