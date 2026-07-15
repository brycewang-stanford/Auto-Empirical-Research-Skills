---
name: Finding Open Access Papers
description: Use Unpaywall API to find free full-text versions of paywalled papers
when_to_use: When paper behind paywall. When PMC full text not available. When DOI resolution hits paywall. When need free access to paper. Before giving up on full text access.
version: 1.0.0
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║  本文件为开源 Skill 原始文档，收录仅供学习与研究参考        ║
  ║  CoPaper.AI 收集整理 | https://copaper.ai                  ║
  ╚══════════════════════════════════════════════════════════════╝

  来源仓库: https://github.com/kthorn/research-superpower
  项目名称: research-superpower
  开源协议: MIT License
  收录日期: 2026-04-02

  声明: 本文件版权归原作者所有。此处收录旨在为社会科学实证研究者
  提供 AI Agent Skills 的集中参考。如有侵权，请联系删除。
-->

# Finding Open Access Papers

## Overview

Use Unpaywall to find legally available open access versions of papers that appear to be behind paywalls.

**Core principle:** Many paywalled papers have free versions (preprints, author manuscripts, institutional repositories). Unpaywall finds them.

## When to Use

Use this skill when:
- DOI resolution hits a paywall
- Paper not available in PubMed Central
- Publisher site requires subscription
- Need full text for highly relevant paper (score ≥7)

**Use BEFORE giving up on full text access**

## Unpaywall API

**Simple REST API - no authentication required for reasonable usage**

### Basic Request

```bash
curl "https://api.unpaywall.org/v2/DOI?email=YOUR_EMAIL"
```

**Parameters:**
- `DOI` - The paper's DOI (URL-encoded if needed)
- `email` - User's email (required, for courtesy/contact)

**IMPORTANT: Ask user for their email at the start of research session. Do NOT use placeholder emails like claude@anthropic.com or researcher@example.com.**

**Example:**
```bash
curl "https://api.unpaywall.org/v2/10.1038/nature12373?email=user@example.com"
```

### Response Format

```json
{
  "doi": "10.1038/nature12373",
  "title": "Paper Title",
  "is_oa": true,
  "best_oa_location": {
    "url": "https://europepmc.org/articles/pmc3858213",
    "url_for_pdf": "https://europepmc.org/articles/pmc3858213?pdf=render",
    "version": "publishedVersion",
    "license": "cc-by",
    "host_type": "repository"
  },
  "oa_locations": [
    {
      "url": "https://europepmc.org/articles/pmc3858213",
      "version": "publishedVersion"
    },
    {
      "url": "https://arxiv.org/abs/1234.5678",
      "version": "submittedVersion"
    }
  ]
}
```

## Key Response Fields

**`is_oa`** (boolean)
- `true` - Open access version available
- `false` - No free version found

**`best_oa_location`** (object or null)
- Unpaywall's recommended best open access source
- Prioritizes published versions over preprints
- Includes PDF URL when available

**`oa_locations`** (array)
- All known open access locations
- Includes repositories, preprint servers, institutional sites
- Ordered by quality/version

**`version`** types:
- `publishedVersion` - Final published version (best)
- `acceptedVersion` - Author's accepted manuscript (good)
- `submittedVersion` - Preprint before peer review (useful)

## Implementation Pattern

### 1. Check Unpaywall After Paywall Hit

```bash
# Try DOI first
curl -L "https://doi.org/10.1234/example.2023"

# If paywall detected (403, subscription required, etc):
curl "https://api.unpaywall.org/v2/10.1234/example.2023?email=your@email.com"
```

### 2. Extract Best URL

```bash
# Parse JSON response
response=$(curl -s "https://api.unpaywall.org/v2/DOI?email=EMAIL")

# Check if OA available
is_oa=$(echo $response | jq -r '.is_oa')

if [ "$is_oa" = "true" ]; then
  # Get best PDF URL
  pdf_url=$(echo $response | jq -r '.best_oa_location.url_for_pdf // .best_oa_location.url')

  # Download
  curl -L -o "papers/paper.pdf" "$pdf_url"
fi
```

### 3. Report to User

**When OA found:**
```
⚠️ Paper behind paywall at publisher
✓ Found open access version via Unpaywall!
   Source: Europe PMC (published version)
   PDF: https://europepmc.org/articles/pmc3858213?pdf=render
   → Downloading...
```

**When no OA found:**
```
⚠️ Paper behind paywall at publisher
✗ No open access version found via Unpaywall
   Options:
   - Request via institutional access
   - Contact authors for preprint
   - Continue with abstract only
```

### 4. Prioritize by Version

If multiple locations available:

**Priority order:**
1. `publishedVersion` from publisher or PMC
2. `acceptedVersion` from institutional repository
3. `submittedVersion` from preprint server (arXiv, bioRxiv)

## Integration with evaluating-paper-relevance

**Add to full text fetching workflow:**

```
Stage 2: Fetch Full Text

Try in order:
A. PubMed Central (free full text)
B. DOI resolution → If paywall, try Unpaywall
C. Unpaywall direct lookup
D. Preprints (bioRxiv, arXiv)
```

**Updated workflow:**

```bash
# 1. Try PMC
pmc_result=$(curl "https://eutils.ncbi.nlm.nih.gov/...")
if has_pmc_fulltext; then
  fetch_pmc
  exit 0
fi

# 2. Try DOI
doi_result=$(curl -L "https://doi.org/$doi")
if is_paywall; then
  # 3. Try Unpaywall
  unpaywall_result=$(curl "https://api.unpaywall.org/v2/$doi?email=$EMAIL")
  if has_oa; then
    fetch_unpaywall_pdf
    exit 0
  fi
fi

# 4. No full text available
report_no_fulltext
```

## Rate Limiting

**Free tier (with email):**
- 100,000 requests per day
- No hard rate limit, but be respectful
- Include email in requests (required)

**Best practices:**
- Add 100ms delay between requests
- Cache responses (don't re-check same DOI)
- Only check for papers you actually need

## Python Helper Example

```python
import requests
import time

def find_open_access(doi, email):
    """
    Find open access version via Unpaywall
    Returns: (pdf_url, version, source) or (None, None, None)
    """
    url = f"https://api.unpaywall.org/v2/{doi}"
    params = {"email": email}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('is_oa'):
            return None, None, None

        best_loc = data.get('best_oa_location')
        if not best_loc:
            return None, None, None

        pdf_url = best_loc.get('url_for_pdf') or best_loc.get('url')
        version = best_loc.get('version', 'unknown')
        source = best_loc.get('host_type', 'unknown')

        return pdf_url, version, source

    except Exception as e:
        print(f"Error checking Unpaywall for {doi}: {e}")
        return None, None, None

# Usage
doi = "10.1038/nature12373"
pdf_url, version, source = find_open_access(doi, "researcher@example.com")

if pdf_url:
    print(f"Found {version} at {source}")
    print(f"PDF: {pdf_url}")
    # Download PDF
    response = requests.get(pdf_url)
    with open(f'papers/{doi.replace("/", "_")}.pdf', 'wb') as f:
        f.write(response.content)
else:
    print("No open access version found")

time.sleep(0.1)  # Rate limiting
```

## Common Sources Found

**Repositories:**
- Europe PMC / PubMed Central
- Institutional repositories (university sites)
- PubMed Central international mirrors

**Preprint servers:**
- bioRxiv (biology)
- medRxiv (medicine)
- arXiv (physics, CS, math)
- ChemRxiv (chemistry)

**Publisher sites:**
- Open access journals
- Hybrid journals (OA articles in subscription journals)
- Delayed open access (embargo expired)

## Error Handling

**DOI not found:**
```json
{
  "error": "true",
  "message": "DOI not found"
}
```
→ Check DOI format, try alternative identifiers

**Network errors:**
- Retry with exponential backoff
- Maximum 3 attempts
- Report to user if all fail

**Malformed response:**
- Check for `is_oa` field
- Fallback to `oa_locations` array if `best_oa_location` missing

## Quick Reference

| Task | Command |
|------|---------|
| Check if OA available | `curl "https://api.unpaywall.org/v2/DOI?email=EMAIL"` |
| Get best PDF URL | Parse `.best_oa_location.url_for_pdf` |
| List all OA sources | Parse `.oa_locations[]` |
| Check version type | Look at `.version` field |
| Download PDF | `curl -L -o paper.pdf "$pdf_url"` |

## Integration Points

**Called by:**
- `evaluating-paper-relevance` - When full text not in PMC
- `answering-research-questions` - For highly relevant papers

**Updates:**
- `papers-reviewed.json` - Note if OA found
- `SUMMARY.md` - Include OA source info

## Common Mistakes

**Using placeholder email:** Using claude@anthropic.com or researcher@example.com → Ask user for their real email
**Not including email:** Required parameter, requests will fail
**Checking every paper:** Only check when needed (score ≥7, no PMC)
**Ignoring version type:** Published version better than preprint
**Single source only:** Check `oa_locations` array for alternatives
**No rate limiting:** Add delays even though no hard limit

## Success Criteria

Successful when:
- Paywalled paper's OA version found and downloaded
- Version type recorded (published/accepted/submitted)
- User informed about source and version
- Fallback options provided if no OA available

## Next Steps

After finding OA version:
- Download PDF to papers/ folder
- Note source and version in SUMMARY.md
- Continue with deep dive analysis
- If no OA: note in summary, continue with abstract only
