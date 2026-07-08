# 04 - Data Acquisition and Cleaning

[< Back to README](../../README.md)

<!--
  CoPaper.AI — Empirical Research AI Assistant (https://copaper.ai)
  Even the best method is useless without data. CoPaper.AI's data-preparation
  sub-agent (preparation agent) automates data import, cleaning, and variable
  construction, and plugs seamlessly into the methodology skills for downstream
  analysis.
-->

> **Data is the foundation of empirical research.** Even the most sophisticated identification strategy cannot rescue conclusions built on shaky data. AI agents can accelerate data cleaning, variable construction, and exploratory analysis, but you still need to judge the reliability of the data source and the reasonableness of the variable definitions yourself.

---

## 📦 Related Skills Vendored in This Repo (click-through folders)

> The collections below are **already vendored in this repository** — clone-and-use, offline-runnable, all audited by [LICENSE_AUDIT](../LICENSE_AUDIT.md) and the [security scan](../../SECURITY-SCAN-REPORT.md). These are the most direct built-in capabilities at this stage; the per-tool and per-source details below complement this table. See [skills/](../../skills/) and [SKILL_CATALOG](../SKILL_CATALOG.md) for the full directory.

| Collection | What it does | How to use it at this stage |
|------|----------|---------------|
| [⭐ `00.1` Full Empirical · Python](../../skills/00.1-Full-empirical-analysis-skill_Python/) | Explicit stack: `pandas` · `statsmodels` · `linearmodels` · `pyfixest` | Use pandas to clean, build panels, and generate the analysis sample |
| [`17` DAAF](../../skills/17-DAAF-Contribution-Community-daaf/) | Safe-and-compliant agent framework with built-in education data-source skills | Pull public data such as Scorecard / FSA / campus-safety datasets |
| [`57` edgartools](../../skills/57-dgunning-edgartools/) | Query and analyse SEC filings | Pull listed-company financials and construct corporate-finance variables |
| [`59` openalex-skill](../../skills/59-shiquda-openalex-skill/) | Query 240M+ scholarly works via OpenAlex | Treat literature metadata as a structured data source |
| [`43` research-plugins](../../skills/43-wentorai-research-plugins/) | 478 research plugins: visualisation, domains, infrastructure | Pick specialised retrieval/cleaning plugins by data type |

---

## Skills List

### xlsx (Spreadsheet Processing)

| Attribute | Description |
|------|------|
| **Source** | [Anthropic official Skills](https://github.com/anthropics/skills) |
| **Function** | Spreadsheet creation, editing, and analysis; supports formulas, formatting, data analysis, and visualisation |
| **Best for** | Data preprocessing, descriptive-statistics tables, data validation |

### Data Plugin (Data Exploration)

| Attribute | Description |
|------|------|
| **Source** | [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) |
| **Function** | SQL queries, data exploration, visualisation, dashboards, insight generation |
| **Highlight** | Anthropic-official; runs queries and analysis directly against the database |

### DeepAnalyze (Autonomous Data Analysis)

| Attribute | Description |
|------|------|
| **Source** | [ruc-datalab/DeepAnalyze](https://github.com/ruc-datalab/DeepAnalyze) (Renmin University of China) |
| **Function** | End-to-end autonomous agent from raw data to a professional analysis report |
| **Supported formats** | CSV, Excel, JSON, XML, databases |
| **Workflow** | Data import → automatic cleaning → exploratory analysis → modelling → visualisation → report generation |
| **Highlight** | Open-source model DeepAnalyze-8B; ships with a WebUI + Docker sandbox; Chinese documentation |

### ai-data-science-team (Multi-Agent Data Science Team)

| Attribute | Description |
|------|------|
| **Source** | [business-science/ai-data-science-team](https://github.com/business-science/ai-data-science-team) |
| **Function** | Supervisor-led multi-agent data-science team |
| **Agents** | EDA Agent (exploratory analysis) + SQL Agent (data querying) + Data Loader Agent (data import) + MLflow Agent (model management) |
| **Highlight** | LangChain integration; sandboxed code execution |

### claude-code-data-science-team

| Attribute | Description |
|------|------|
| **Source** | [HungHsunHan/claude-code-data-science-team](https://github.com/HungHsunHan/claude-code-data-science-team) |
| **Function** | A Claude Code multi-agent system that emulates a real data-science team |
| **Workflow** | Data cleaning → feature engineering → modelling → generate executable notebooks + analysis report |

### web-scraper (Smart Web Scraping)

| Attribute | Description |
|------|------|
| **Source** | [yfe404/web-scraper](https://github.com/yfe404/web-scraper) |
| **Function** | Smart web scraping skill for Claude Code; automatic strategy selection, TypeScript-first Apify Actor development |
| **Best for** | Web data acquisition and building research datasets |

### us-gov-open-data-mcp (US Government Open-Data MCP)

| Attribute | Description |
|------|------|
| **Source** | [lzinga/us-gov-open-data-mcp](https://github.com/lzinga/us-gov-open-data-mcp) |
| **Function** | 40+ US government data APIs and 250+ tools: Treasury, FRED, Congress, FDA, CDC, FEC, BLS, Census, and more |
| **Highlight** | Cross-source linking (query a drug and automatically pull FDA adverse events + clinical trials + lobbying spend + congressional activity); 18 APIs require no key |
| **Compatibility** | VS Code Copilot, Claude Desktop, Cursor |

### fred-mcp-server (FRED Economic-Data MCP)

| Attribute | Description |
|------|------|
| **Source** | [stefanoamorelli/fred-mcp-server](https://github.com/stefanoamorelli/fred-mcp-server) |
| **Function** | Access to 800,000+ FRED time series with date filtering |

### world-bank-data-mcp (World Bank Data MCP)

| Attribute | Description |
|------|------|
| **Source** | [llnOrmll/world-bank-data-mcp](https://github.com/llnormll/world-bank-data-mcp) |
| **Function** | Access to World Bank Data360; 1,000+ economic and social indicators, 200+ countries |

### world_bank_mcp_server (World Bank Open-Data MCP)

| Attribute | Description |
|------|------|
| **Source** | [anshumax/world_bank_mcp_server](https://github.com/anshumax/world_bank_mcp_server) |
| **Function** | MCP implementation of the World Bank Open Data API |

### datagouv-mcp (French Government Open-Data MCP)

| Attribute | Description |
|------|------|
| **Source** | [datagouv/datagouv-mcp](https://github.com/datagouv/datagouv-mcp) |
| **Function** | MCP server for the French national open-data platform data.gouv.fr; supports natural-language queries |

---

## Traditional Data-Cleaning Tools

Agent skills speed up exploration, but core data processing still depends on these tools:

| Tool | Best for | Key commands/packages |
|------|----------|---------------|
| **Stata** | Structured data merge and reshape | `merge`, `reshape`, `collapse`, `encode` |
| **Python** | Large-scale data cleaning and transformation | `pandas`, `polars` (faster) |
| **R** | Pipelined data processing | `tidyverse` (`dplyr` + `tidyr`) |
| **OpenRefine** | Visual data cleaning (no programming) | GUI-driven |
| **SQL** | Database queries and preprocessing | Direct queries |

---

## Common Data Sources Quick Reference

### Global Macroeconomic Data

| Source | Description | Access |
|--------|------|----------|
| **FRED** | Federal Reserve Bank of St. Louis; 800,000+ time series | fred.stlouisfed.org, with Python API |
| **World Bank Open Data** | Economic, demographic, and development indicators for 200+ countries | data.worldbank.org |
| **IMF** | International Monetary Fund databases | data.imf.org |
| **OECD.Stat** | OECD statistical database | stats.oecd.org |
| **Our World in Data** | Research data on global issues (poverty, energy, climate) | ourworldindata.org |
| **National Bureau of Statistics** | China Statistical Yearbook, monthly macro data | stats.gov.cn |

### Micro-Surveys and Panel Data

| Source | Description | Fields of application |
|--------|------|----------|
| **NLSY** | US National Longitudinal Survey of Youth | Labour economics, economics of education |
| **HRS** | Health and Retirement Study; tracks ~20,000 people | Health economics, retirement |
| **CFPS** | China Family Panel Studies (Peking University) | Chinese household economic behaviour |
| **CGSS** | Chinese General Social Survey | Sociology, social stratification |
| **CHARLS** | China Health and Retirement Longitudinal Study | Aging, health |
| **CHIP** | China Household Income Project | Income distribution, poverty |
| **CHFS** | China Household Finance Survey | Household finance, wealth |

### Specialised Platforms

| Platform | Highlight |
|------|------|
| **NBER Data Archive** | Datasets accompanying NBER working papers |
| **ICPSR** | University of Michigan's social-science data archive |
| **Google Dataset Search** | Cross-platform dataset search engine |
| **Mark Data** | Social-science data-sharing platform; >100,000 downloads per year |
| **Wind / CSMAR** | Chinese financial and economic database (paid) |
| **Data.gov** | US central government open-data portal |

---

## Practical Advice

1. **Run EDA before models**: use `DeepAnalyze` or the EDA Agent of `ai-data-science-team` to quickly understand data distribution, missing values, and outliers — much faster than writing the exploration yourself.
2. **Leave a trail in data cleaning**: every data-processing step should be implemented in code (not manual Excel edits), paired with Git version control.
3. **Mind panel balance**: before running a DID skill, check whether your panel is balanced and whether attrition is an issue.

---

[← Previous chapter](03-paper-reading-and-decomposition.md) | [Next chapter: 05 - Statistical Analysis and Causal Inference →](05-statistical-analysis-and-causal-inference.md)