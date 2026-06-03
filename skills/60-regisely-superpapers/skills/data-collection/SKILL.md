---
name: data-collection
description: Use when collecting data for a research project, downloading time series, building a dataset, accessing economic or social data APIs, or scraping data from a non-API source. Handles source discovery, respectful collection, local caching, and manifest documentation.
---

# Data Collection

## Overview

This skill guides data collection from the research question to a versionable artifact in `data/raw/`. It is field-agnostic and open-ended about sources — the `references/common-sources.md` file is a starting point, not a boundary. For any research question, the skill uses web search to find appropriate sources beyond the common list.

## When to Use

- "I need data on X"
- "Download the unemployment series"
- "Build a dataset of country-level GDP"
- "Scrape this website for paper data"
- "Where can I get data about Y?"
- Any new project's collection phase

## Mandatory Steps

1. **Identify data needs from the research question.** Variables, units (country, firm, individual, pixel), frequency, period, geography, and any necessary keys for merging across sources.

2. **Find appropriate sources.** Start with `references/common-sources.md`. If the user's needs are not covered there, search the web for the relevant source. Never invent a URL or API endpoint from memory.

3. **Prefer APIs over scraping.** APIs are versioned, documented, and legal. Scraping is the last resort when no API is available.

4. **When scraping is necessary, be respectful:**
   - Check and honor `robots.txt`
   - Rate limit — minimum one request per second, often slower
   - Exponential backoff on errors (e.g., 1s, 2s, 4s, 8s, cap at 60s)
   - Identifiable user agent with contact information
   - Cache aggressively — never re-download unnecessarily
   - Never scrape a source that explicitly prohibits automated access in its terms of service

5. **Save raw data in `data/raw/`** in a versionable format. Parquet is preferred for tabular data; CSV is acceptable for small datasets. Never edit raw files by hand.

6. **Document every dataset in `data/manifest.md`** following the format from `replication-driven-research`: name, source, URL or API endpoint, collection date, variables used, frequency, period, license or usage notes.

7. **Cache locally.** Check `data/raw/` before fetching. Only invoke the network if the file is missing or the user has explicitly requested a refresh.

## Source Discovery Process

Follow this order when looking for a data source:

1. Check `references/common-sources.md` for known sources in the relevant domain.
2. Web-search for `"<topic>" open data API` or `"<topic>" dataset download`.
3. Check open science repositories: Harvard Dataverse, Zenodo, Open Science Framework, figshare.
4. Check the topic's primary institutional source (central bank, statistical agency, international organization, regulatory body).
5. If none of the above work, escalate to the user — manual acquisition may be required (e.g., contacting authors, subscribing to a database).

## Anti-Patterns

- Scraping a source whose `robots.txt` prohibits it
- Hitting an API without rate limiting
- Re-downloading data that already exists in `data/raw/`
- Raw data without a manifest entry
- Editing a raw data file manually to "fix" issues
- Collecting data without specifying the period and frequency upfront
- Trusting a URL invented from memory
- Merging datasets without documenting the merge keys

## Verification Before Completion

- [ ] Data saved under `data/raw/` in a versionable format (parquet preferred)
- [ ] Manifest entry added for every new dataset
- [ ] Collection logic lives in a script under `code/`, not an interactive session
- [ ] Source license checked and recorded in the manifest
- [ ] Cache honored — no unnecessary re-downloads
- [ ] Rate limiting applied for scraping
- [ ] Raw files are untouched after initial download
