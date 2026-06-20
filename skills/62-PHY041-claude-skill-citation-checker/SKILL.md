---
name: check-citations
description: Verify academic citations against CrossRef, Semantic Scholar, and OpenAlex. Detects AI-hallucinated references, chimeric citations, and suspicious patterns.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: requests
    emoji: "\U0001F50D"
    homepage: https://github.com/PHY041/claude-skill-citation-checker
---

# check-citations

Verify academic citations against CrossRef, Semantic Scholar, and OpenAlex. Detects AI-hallucinated references, chimeric citations (real title + wrong authors), and suspicious patterns before submission.

## When to Use

- After writing or editing a `.bib` file with AI assistance
- Before submitting a paper, thesis, or report
- When reviewing AI-generated literature sections
- As a CI/CD check in LaTeX manuscript pipelines
- When auditing existing bibliographies for dead or fabricated references

## Background

- 6-55% of AI-generated citations are fabricated (varies by model/domain)
- 100+ hallucinated references found in NeurIPS 2025 accepted papers
- Universities increasingly treat fake citations as academic misconduct
- Three hallucination types: **fully fabricated**, **chimeric** (real title + wrong authors), **modified real** (slightly altered metadata)

## Usage

### Quick Check (Single File)

```bash
python scripts/citation_checker.py references.bib
```

### Check All `.bib` Files in a Directory

```bash
python scripts/citation_checker.py path/to/report/
```

### JSON Output (CI/CD Pipelines)

```bash
python scripts/citation_checker.py references.bib --json
```

### Verbose Mode (Debug API Responses)

```bash
python scripts/citation_checker.py references.bib --verbose
```

## How It Works

### Cascading Multi-Source Verification

Each citation is checked against three independent databases:

| Source | Coverage | Strength |
|--------|----------|----------|
| CrossRef | 140M+ DOI-registered works | Best for journal/conference papers with DOIs |
| Semantic Scholar | 200M+ papers | Best author disambiguation, arXiv coverage |
| OpenAlex | 240M+ works | Broadest coverage, fully open |

**Verification logic:**
- Found in 2+ sources with matching title → **verified** (high confidence)
- Found in 1 source only → **suspicious** (manual check recommended)
- Found in 0 sources → **not_found** (likely hallucinated)

### Chimeric Detection

When a citation's title matches a real paper but the authors don't overlap at all, it's flagged as a possible **chimeric hallucination** — the most dangerous type because the title looks real on Google Scholar.

### Red Flag Heuristics

- Invalid DOI format (doesn't start with `10.xxxx/`)
- Suspiciously generic title patterns ("A Comprehensive Survey of...")
- Future publication year
- Missing author or year fields
- Single-word author names (incomplete metadata)

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All citations verified |
| 1 | One or more citations not found |
| 2 | Suspicious citations only (no hard failures) |

## Dependencies

```bash
pip install requests
```

No API keys required — uses free tiers of all three databases.

## Accuracy (Tested)

| Category | Result | Description |
|----------|--------|-------------|
| Known-good | 9/10 (90%) | Famous ML papers (Vaswani, Devlin, Brown, He, etc.) |
| Known-bad | 10/10 (100%) | Fabricated papers with plausible titles |
| Chimeric | 5/5 (100%) | Real titles with wrong authors |
| **False positive rate** | **10%** | 1 miss: unpublished tech report without DOI |
| **False negative rate** | **0%** | No fake paper was ever verified |

The core guarantee: **fake papers are never marked as real.**

## Limitations

- Papers without DOI that have many derivatives (e.g., BERT without DOI) may not be found via title search alone — always include DOIs when available
- Semantic Scholar free tier rate-limits at ~100 requests/5 minutes — batch verification is slower
- Cannot verify papers behind paywalls or not indexed in any of the three databases
- Book chapters, technical reports, and grey literature have lower coverage

## Integration with LaTeX Workflows

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python scripts/citation_checker.py references.bib --json > /tmp/cite_check.json
NOT_FOUND=$(python3 -c "import json; d=json.load(open('/tmp/cite_check.json')); print(d['summary']['not_found'])")
if [ "$NOT_FOUND" -gt "0" ]; then
    echo "BLOCKED: $NOT_FOUND unfound citations. Run 'python scripts/citation_checker.py references.bib --verbose' to investigate."
    exit 1
fi
```

### GitHub Actions

```yaml
- name: Check citations
  run: |
    pip install requests
    python scripts/citation_checker.py references.bib --json > citation_report.json
    python -c "
    import json, sys
    r = json.load(open('citation_report.json'))
    if r['summary']['not_found'] > 0:
        print(f'FAIL: {r[\"summary\"][\"not_found\"]} citations not found')
        sys.exit(1)
    print(f'PASS: {r[\"summary\"][\"verified\"]} verified, {r[\"summary\"][\"suspicious\"]} suspicious')
    "
```
