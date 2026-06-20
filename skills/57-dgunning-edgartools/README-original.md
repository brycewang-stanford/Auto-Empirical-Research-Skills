<!-- Vendored into AERS from https://github.com/dgunning/edgartools on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`dgunning/edgartools`](https://github.com/dgunning/edgartools) for the AERS catalog (license: MIT). Vendored 2026-06-01. The original upstream README follows verbatim.

---

<a href="https://github.com/dgunning/edgartools">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/edgartools-mark.svg" alt="EdgarTools logo" align="left" height="80" hspace="20">
</a>

# EdgarTools — Python Library for SEC EDGAR Filings

<br clear="left">

<p>
  <a href="https://pypi.org/project/edgartools"><img src="https://img.shields.io/pypi/v/edgartools.svg" alt="PyPI - Version"></a>
  <a href="https://github.com/dgunning/edgartools/actions"><img src="https://img.shields.io/github/actions/workflow/status/dgunning/edgartools/python-hatch-workflow.yml" alt="GitHub Workflow Status"></a>
  <a href="https://www.codefactor.io/repository/github/dgunning/edgartools"><img src="https://www.codefactor.io/repository/github/dgunning/edgartools/badge" alt="CodeFactor"></a>
  <a href="https://github.com/pypa/hatch"><img src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg" alt="Hatch project"></a>
  <a href="https://github.com/dgunning/edgartools/blob/main/LICENSE"><img src="https://img.shields.io/github/license/dgunning/edgartools" alt="GitHub"></a>
  <a href="https://pypi.org/project/edgartools"><img src="https://img.shields.io/pypi/dm/edgartools" alt="PyPI - Downloads"></a>
</p>

<p>
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/badges/badge-ai-native.svg" alt="AI Native">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/badges/badge-10x-faster.svg" alt="10x Faster">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/badges/badge-open-source.svg" alt="Open Source">
</p>

**EdgarTools** is a Python library for accessing SEC EDGAR filings as structured data. Parse financial statements, insider trades, fund holdings, proxy statements, and 20+ other filing types with a consistent Python API — in a few lines of code. Free and open source.

![EdgarTools SEC filing data extraction demo](https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/edgartools-demo.gif)

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

## Why EdgarTools?

EdgarTools turns SEC filings into Python objects. Every supported form type gives you structured data — not raw HTML, not XML, not JSON dumps. Actual Python objects with properties, methods, and DataFrames.

<table align="center">
<tr>
  <td align="center" width="33%">
    <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/icon-speed.svg" width="80" alt="Fast"><br>
    <b>Fast</b><br>
    Optimized with lxml & PyArrow<br>
    Smart caching, rate-limit aware
  </td>
  <td align="center" width="33%">
    <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/icon-ai.svg" width="80" alt="AI Ready"><br>
    <b>AI Ready</b><br>
    Built-in MCP server for Claude<br>
    LLM-optimized text extraction
  </td>
  <td align="center" width="33%">
    <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/icon-quality.svg" width="80" alt="Well Tested"><br>
    <b>Well Tested</b><br>
    1000+ verification tests<br>
    Type hints throughout
  </td>
</tr>
<tr>
  <td align="center" width="33%">
    <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/icon-xbrl.svg" width="80" alt="XBRL Support"><br>
    <b>XBRL Native</b><br>
    Full XBRL standardization<br>
    Cross-company comparisons
  </td>
  <td align="center" width="33%">
    <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/icon-data.svg" width="80" alt="20+ Filing Types"><br>
    <b>20+ Filing Types</b><br>
    Typed objects for every form<br>
    Pandas-ready DataFrames
  </td>
  <td align="center" width="33%">
    <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/icon-community.svg" width="80" alt="Open Source"><br>
    <b>Open Source</b><br>
    MIT license, free forever<br>
    No API keys, no rate limits
  </td>
</tr>
</table>

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

## How It Works

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/how-it-works.svg" alt="How EdgarTools Python library extracts SEC EDGAR filing data">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/sections/section-quick-start.svg" alt="Quick Start">
</p>

```python
pip install edgartools

from edgar import *
set_identity("your.name@example.com")

# Get a company's balance sheet
balance_sheet = Company("AAPL").get_financials().balance_sheet()

# Browse a company's filings
company = Company("MSFT")

# Parse insider transactions
filings = company.get_filings(form="4")
form4 = filings[0].obj()
```

![Apple SEC Form 4 insider transaction data extraction with Python](https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/aapl-insider.png)

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

## Use Cases

### Analyze 13F Institutional Holdings & Hedge Fund Portfolios

Track what hedge funds and institutional investors own by parsing SEC 13F filings. EdgarTools extracts complete portfolio holdings with position sizes, values, and quarter-over-quarter changes.

```python
from edgar import get_filings
thirteenf = get_filings(form="13F-HR")[0].obj()
thirteenf.holdings  # DataFrame of all portfolio positions
```

[Institutional Holdings guide →](https://edgartools.readthedocs.io/en/latest/guides/thirteenf-data-object-guide/)

### Track Insider Trading with SEC Form 4

Monitor insider buying and selling activity from SEC Form 4 filings. See which executives are purchasing or selling shares, option exercises, and net position changes.

```python
company = Company("TSLA")
form4 = company.get_filings(form="4")[0].obj()
form4.transactions  # Insider buy/sell transactions
```

[Insider Trades guide →](https://edgartools.readthedocs.io/en/latest/insider-filings/)

### Extract Financial Statements from 10-K and 10-Q Filings

Get income statements, balance sheets, and cash flow statements from SEC annual and quarterly reports. Data is parsed from XBRL with standardized labels for cross-company comparison.

```python
financials = Company("MSFT").get_financials()
financials.balance_sheet()   # Balance sheet with all line items
financials.income_statement()  # Revenue, net income, EPS
```

[Financial Statements guide →](https://edgartools.readthedocs.io/en/latest/guides/financial-data/)

### Parse 8-K Current Reports for Corporate Events

Access material corporate events as they happen -- earnings releases, acquisitions, executive changes, and more. EdgarTools parses 8-K filings into structured items with full text extraction.

```python
eightk = get_filings(form="8-K")[0].obj()
eightk.items  # List of reported event items
```

[Current Events guide →](https://edgartools.readthedocs.io/en/latest/guides/eightk-data-object-guide/)

### Query XBRL Financial Data Across Companies

Access structured XBRL financial facts for any SEC filer. Query specific line items like revenue or total assets over time, and compare across companies using standardized concepts.

```python
facts = Company("AAPL").get_facts()
facts.to_pandas("us-gaap:Revenues")  # Revenue history as DataFrame
```

[XBRL Deep Dive →](https://edgartools.readthedocs.io/en/latest/xbrl/)

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/sections/section-features.svg" alt="Key Features">
</p>

### Comprehensive SEC Data Access

<table>
<tr>
<td width="50%" valign="top">

**Financial Statements (XBRL)**
- Balance Sheets, Income Statements, Cash Flows
- Individual line items via XBRL tags
- Multi-period comparisons with comparative periods
- Standardized cross-company data
- Automatic unit conversion
- Metadata columns (dimensions, members, units)
- Complete dimensional data support

**Fund & Investment Data**
- 13F institutional holdings & portfolio analysis
- N-PORT fund portfolio data
- N-MFP money market fund holdings
- N-CSR/N-CEN fund reports
- Position tracking over time

**Company Dataset & Reference Data**
- Industry and state filtering
- Company subsets with metadata
- Standardized industry classifications
- SEC ticker/CIK lookups
- Exchange information

**Insider Transactions**
- Form 3, 4, 5 structured data
- Transaction history by insider
- Ownership changes
- Grant and exercise details
- Automatic parsing

</td>
<td width="50%" valign="top">

**Filing Intelligence**
- Any form type (10-K, 10-Q, 8-K, S-1, etc.)
- Complete history since 1994
- Typed data objects for 20+ form types
- HTML to clean text extraction
- Section extraction (Risk Factors, MD&A)
- Subsidiaries (EX-21) and auditor extraction

**Performance & Reliability**
- Configurable rate limiting (enterprise mirrors supported)
- Custom SEC data sources (corporate/academic mirrors)
- Smart caching (30-second fresh filing cache)
- Robust error handling
- SSL verification with fail-fast retry
- Type hints throughout
- [Enterprise configuration →](docs/configuration.md#enterprise-configuration)

**Developer Experience**
- Intuitive, consistent API
- Pandas DataFrame integration
- Rich terminal output
- 1000+ tests

</td>
</tr>
</table>

EdgarTools supports all SEC form types including **10-K annual reports**, **10-Q quarterly filings**, **8-K current reports**, **13F institutional holdings**, **Form 4 insider transactions**, **proxy statements (DEF 14A)**, **S-1 registration statements**, **N-CSR fund reports**, **N-MFP money market data**, **N-PORT fund portfolios**, **Schedule 13D/G ownership**, **Form D offerings**, **Form C crowdfunding**, and **Form 144 restricted stock**. Parse XBRL financial data, extract text sections, and convert filings to pandas DataFrames.

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

## Comparison with Alternatives

EdgarTools is a **Python library** that talks directly to SEC EDGAR. [sec-api](https://sec-api.io) is a **hosted API service** that returns JSON. Both parse SEC filings — the difference is how you work with the data.

| | EdgarTools | sec-api | Raw EDGAR |
|---|------------|---------|-----------|
| **What it is** | Python library | REST API service | DIY |
| **Cost** | Free (MIT) | $49+/mo | Free |
| **Data format** | Typed Python objects | JSON | Raw XML/HTML |
| **Parsed filing types** | 24 (10-K, 8-K, 13F, N-PORT, proxy, etc.) | 15+ structured APIs | — |
| **Financials** | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-check.svg" width="20"> Parsed + standardized | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-check.svg" width="20"> Parsed (XBRL-to-JSON) | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-cross.svg" width="20"> |
| **Full-text search** | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-check.svg" width="20"> via EFTS | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-check.svg" width="20"> | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-cross.svg" width="20"> |
| **AI/MCP integration** | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-check.svg" width="20"> | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-cross.svg" width="20"> | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-cross.svg" width="20"> |
| **Language** | Python | Any | Any |
| **Open source** | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-check.svg" width="20"> | <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/compare-cross.svg" width="20"> Proprietary | N/A |

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/sections/section-ai-integration.svg" alt="AI Integration">
</p>

### Use EdgarTools with Claude Code & Claude Desktop

EdgarTools includes an MCP server and AI skills for Claude Desktop and Claude Code. Ask questions in natural language and get answers backed by real SEC data.

- *"Compare Apple and Microsoft's revenue growth rates over the past 3 years"*
- *"Which Tesla executives sold more than $1 million in stock in the past 6 months?"*

<details>
<summary><b>Setup Instructions</b></summary>

### Option 1: AI Skills (Recommended)

Install the EdgarTools skill for Claude Code or Claude Desktop:

```bash
pip install "edgartools[ai]"
python -c "from edgar.ai import install_skill; install_skill()"
```

This adds SEC analysis capabilities to Claude, including 3,450+ lines of API documentation, code examples, and form type reference.

### Option 2: MCP Server

Run EdgarTools as an MCP server for any AI client -- Claude Desktop, Cline, or your own containerized deployment.

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "edgartools": {
      "command": "uvx",
      "args": ["--from", "edgartools[ai]", "edgartools-mcp"],
      "env": {
        "EDGAR_IDENTITY": "Your Name your.email@example.com"
      }
    }
  }
}
```

Requires [uv](https://docs.astral.sh/uv/). Alternatively, `pip install "edgartools[ai]"` and use `python -m edgar.ai`.

See [AI Integration Guide](docs/ai-integration.md) for complete documentation.

</details>

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

## <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/icons/emoji-heart.svg" width="24" height="24"> Support This Project

EdgarTools is used in production at hedge funds, fintechs, and research desks. It's MIT-licensed — no API keys, no rate limits, no subscriptions — and one person maintains it.

The SEC ships a new XBRL taxonomy every year and amends filing types every quarter. Keeping 20+ parsers current, and adding new extractors as the SEC adds disclosure types, is the work sponsorship funds.

<p align="center">
  <a href="https://github.com/sponsors/dgunning" target="_blank">
    <img src="https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA" alt="GitHub Sponsors" height="40">
  </a>
  &nbsp;&nbsp;
  <a href="https://www.buymeacoffee.com/edgartools" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="40">
  </a>
</p>

<p align="center">
  <sub>Recurring sponsorship + corporate tiers via GitHub · One-time thanks via Buy Me a Coffee</sub>
</p>

**Recent maintenance shipped via sponsorship:**
- NPORT-P fund portfolio extraction
- MA-I municipal advisor parser
- 424B prospectus family (B1–B8) extractors
- XBRL taxonomy updates for the 2026 cycle

---

### For teams running EdgarTools in production

If EdgarTools is in your data pipeline, [GitHub Sponsors](https://github.com/sponsors/dgunning) offers corporate tiers from **$250 to $1,500/mo** with:

- Response SLAs (24h–48h first response on critical issues)
- Quarterly strategy calls and roadmap input
- Logo placement in this README
- 7-day early access for internal regression testing
- Annual invoicing through GitHub — procurement-friendly

→ **[See sponsor tiers](https://github.com/sponsors/dgunning)**

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/dividers/divider-hexagons.svg" alt="">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dgunning/edgartools/main/docs/images/sections/section-community.svg" alt="Community & Support">
</p>

### Documentation & Resources

- [Documentation](https://edgartools.readthedocs.io/)
- [Notebooks / Examples](https://edgartools.readthedocs.io/en/latest/notebooks/)
- [Quick Guide](https://edgartools.readthedocs.io/en/latest/quick-guide/)
- [EdgarTools Blog](https://www.edgartools.io)

### Get Help & Connect

- [GitHub Issues](https://github.com/dgunning/edgartools/issues) - Bug reports and feature requests
- [Discussions](https://github.com/dgunning/edgartools/discussions) - Questions and community discussions

### Contributing

Contributions welcome:

- **Code**: Fix bugs, add features, improve documentation
- **Examples**: Share interesting use cases and examples
- **Feedback**: Report issues or suggest improvements
- **Spread the Word**: Star the repo, share with colleagues

See our [Contributing Guide](CONTRIBUTING.md) for details.

### Professional Services

Need help building production SEC data infrastructure? The creator of EdgarTools offers consulting for teams building financial AI products:

- **SEC Data Sprint** (1–3 days) — Working prototype on your data
- **Architecture Review** (1–2 weeks) — Pipeline audit with prioritized fixes
- **Pipeline Build** (2–4 weeks) — Production-ready code, tests, and handoff

[Learn more →](https://www.edgar.tools/consulting)

---

<p align="center">
EdgarTools is distributed under the <a href="LICENSE">MIT License</a>
</p>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=dgunning/edgartools&type=Timeline)](https://star-history.com/#dgunning/edgartools&Timeline)

<!-- mcp-name: io.github.dgunning/edgartools -->
