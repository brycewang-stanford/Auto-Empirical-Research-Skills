---
name: EdgarTools
description: Query and analyze SEC filings using EdgarTools
---

# EdgarTools

Analyze SEC filings and financial statements.

## Skills

| Skill | Purpose |
|-------|---------|
| core (this directory) | Company lookup, filings, search |
| [financials/](./financials/) | Financial statements and metrics |
| [reports/](./reports/) | 10-K/10-Q/8-K section extraction |
| [holdings/](./holdings/) | 13F institutional holdings |
| [ownership/](./ownership/) | Form 3/4/5 insider transactions |
| [xbrl/](./xbrl/) | Low-level XBRL facts and concepts |
| [forms.yaml](./forms.yaml) | SEC form type mappings |

Each skill directory has `skill.yaml` (patterns and examples) and `sharp-edges.yaml` (common mistakes to avoid).

## Quick Setup

```python
from edgar import set_identity
set_identity("Your Name your@email.com")  # Required
```

## API Discovery

Every object has `.docs` for API reference:

```python
company.docs                    # Full API guide
company.docs.search("filings")  # Search for specific topic
filing.docs.search("xbrl")      # How to access XBRL
```

## Common Entry Points

```python
from edgar import Company, get_filings, find

company = Company("AAPL")           # By ticker
filing = find("0000320193-25-000079")  # By accession
filings = get_filings(form="10-K", year=2024)  # Discovery
```
