# EdgarTools Skills

AI-optimized documentation for SEC filing analysis with EdgarTools.

## Quick Start

```python
from edgar import set_identity, Company
set_identity("Your Name your@email.com")  # Required

company = Company("AAPL")
company.get_filings(form="10-K")[:5]
```

## Structure

```
skills/
├── core/               # Main skill (hub)
│   ├── SKILL.md        # Entrypoint for Claude
│   ├── skill.yaml      # Core patterns
│   └── sharp-edges.yaml
├── financials/         # Financial statements
├── holdings/           # 13F institutional holdings
├── ownership/          # Form 3/4/5 insider trades
├── reports/            # 10-K/Q/8-K sections
├── xbrl/               # Low-level XBRL access
└── forms.yaml          # SEC form code reference
```

## Skills

| Skill | Purpose |
|-------|---------|
| **core** | Company lookup, filings, search |
| **financials** | get_financials(), statements, metrics |
| **holdings** | 13F portfolio analysis |
| **ownership** | Insider transaction summaries |
| **reports** | Report section extraction |
| **xbrl** | Low-level facts and concepts |

## API Discovery

Every EdgarTools object has `.docs`:

```python
company.docs                    # Full API guide
company.docs.search("filings")  # Search topics
filing.docs.search("xbrl")      # Find XBRL methods
```

## Installation

```python
from edgar.ai import install_skill

# Install to ~/.claude/skills/
install_skill()

# Or package as ZIP
from edgar.ai import package_skill
package_skill()  # Creates edgartools.zip
```

## Token Budget

Total: ~9,300 tokens (active skills)

| Component | Tokens |
|-----------|--------|
| core/ | ~4,100 |
| financials/ | ~800 |
| holdings/ | ~650 |
| ownership/ | ~900 |
| reports/ | ~750 |
| xbrl/ | ~850 |
| forms.yaml | ~250 |

## Design Principles

1. **Lean YAML** - Structured data over prose
2. **Pattern-first** - Show code, not theory
3. **Sharp edges** - Document gotchas prominently
4. **Hub routing** - Core skill routes to specialists

## Links

- [EdgarTools Docs](https://dgunning.github.io/edgartools/)
- [GitHub](https://github.com/dgunning/edgartools)
- [SEC EDGAR](https://www.sec.gov/edgar)
