---
name: data-fetcher
description: Fetch economic data from FRED, World Bank, BLS, OECD, and Yahoo Finance
---

# Data-Fetcher

## Purpose

This skill helps economists fetch data from major economic data APIs including FRED (Federal Reserve Economic Data), World Bank, BLS (Bureau of Labor Statistics), OECD, and Yahoo Finance. It generates clean, documented Python code with proper error handling.

## When to Use

- Downloading macroeconomic indicators
- Building custom datasets from multiple sources
- Automating data updates for ongoing projects
- Fetching cross-country panel data

## Instructions

### Step 0: API Key Setup Check (Run Before Anything Else)

**Before generating any code, Claude must check for required API keys.**

1. Read the file `[plugin_root]/.env` (same directory as `.mcp.json`).
2. Check for `FRED_API_KEY` and `BLS_API_KEY`.

**If `FRED_API_KEY` is missing or blank:**
- Tell the user: *"A free FRED API key is required. Get one at https://fred.stlouisfed.org/docs/api/api_key.html (takes ~1 minute). Paste it here and I'll save it."*
- Wait for input, then append `FRED_API_KEY=<value>` to `.env`.

**If `BLS_API_KEY` is missing:**
- Inform the user it's optional but increases BLS rate limits, and they can get one free at https://www.bls.gov/developers/. If they want to add it later, just paste it and say "save my BLS key".

**If `.env` exists and keys are already set:** load them silently and inject them into all generated code via `python-dotenv`. Use `load_dotenv()` with no arguments so Python searches up from the current working directory automatically — never hardcode the plugin root path:
```python
from dotenv import load_dotenv
load_dotenv()  # searches CWD and parent directories for .env
```

> The `.env` file stores keys locally and is never committed to version control. Generated scripts always read keys from environment variables — never hardcoded.

---

### Step 1: Identify Data Requirements

Ask the user:
1. What data do you need? (GDP, unemployment, inflation, etc.)
2. What time period and frequency?
3. What countries/regions?
4. Preferred output format? (CSV, DataFrame, etc.)

### Step 2: Select Appropriate API

| Data Type | Best Source | Package |
|-----------|------------|---------|
| US macro | FRED | `fredapi` |
| Global development | World Bank | `wbdata` |
| Labor statistics | BLS | `requests` (BLS API v2) |
| Cross-country OECD | OECD | `requests` (OECD SDMX API) |
| Cross-country macro/finance | IMF | `imf-reader` |
| Financial / asset prices | Yahoo Finance | `yfinance` |

### Step 3: Generate Clean Code

Include:
- API key handling (environment variables)
- Error handling for API failures
- Data cleaning and formatting
- Documentation of series definitions

## Example Output

```python
"""
Economic Data Fetcher
=====================
Downloads macroeconomic data from FRED and World Bank APIs.
Requires: fredapi, wbdata, pandas

Setup: Set FRED_API_KEY environment variable
Get a free key from: https://fred.stlouisfed.org/docs/api/api_key.html
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional, Dict

# ============================================
# FRED Data Fetcher
# ============================================

def fetch_fred_series(
    series_ids: List[str],
    start_date: str = "2000-01-01",
    end_date: Optional[str] = None,
    api_key: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetch time series data from FRED.
    
    Parameters
    ----------
    series_ids : list of str
        FRED series IDs (e.g., ['GDP', 'UNRATE', 'CPIAUCSL'])
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str, optional
        End date (defaults to today)
    api_key : str, optional
        FRED API key (defaults to FRED_API_KEY env var)
    
    Returns
    -------
    pd.DataFrame
        DataFrame with date index and series as columns
    
    Example
    -------
    >>> df = fetch_fred_series(['GDP', 'UNRATE'], '2010-01-01')
    """
    try:
        from fredapi import Fred
    except ImportError:
        raise ImportError("Install fredapi: pip install fredapi")
    
    # Get API key
    api_key = api_key or os.environ.get('FRED_API_KEY')
    if not api_key:
        raise ValueError(
            "FRED API key required. Set FRED_API_KEY environment variable "
            "or pass api_key parameter. Get a key at: "
            "https://fred.stlouisfed.org/docs/api/api_key.html"
        )
    
    fred = Fred(api_key=api_key)
    end_date = end_date or datetime.now().strftime('%Y-%m-%d')
    
    # Fetch each series
    data = {}
    for series_id in series_ids:
        try:
            series = fred.get_series(
                series_id,
                observation_start=start_date,
                observation_end=end_date
            )
            data[series_id] = series
            print(f"✓ Downloaded {series_id}")
        except Exception as e:
            print(f"✗ Failed to download {series_id}: {e}")
    
    # Combine into DataFrame
    df = pd.DataFrame(data)
    df.index.name = 'date'
    
    return df


# Common FRED series for economists
FRED_SERIES = {
    # GDP and Output
    'GDP': 'Gross Domestic Product',
    'GDPC1': 'Real GDP',
    'GDPPOT': 'Real Potential GDP',
    
    # Labor Market
    'UNRATE': 'Unemployment Rate',
    'PAYEMS': 'Total Nonfarm Payrolls',
    'CIVPART': 'Labor Force Participation Rate',
    
    # Prices
    'CPIAUCSL': 'Consumer Price Index',
    'PCEPI': 'PCE Price Index',
    'CPILFESL': 'Core CPI',
    
    # Interest Rates
    'FEDFUNDS': 'Federal Funds Rate',
    'DGS10': '10-Year Treasury Rate',
    'T10Y2Y': '10Y-2Y Treasury Spread',
    
    # Money and Credit
    'M2SL': 'M2 Money Stock',
    'TOTRESNS': 'Total Reserves',
}


# ============================================
# World Bank Data Fetcher
# ============================================

def fetch_world_bank_data(
    indicators: Dict[str, str],
    countries: List[str] = ['USA', 'GBR', 'DEU', 'FRA', 'JPN'],
    start_year: int = 2000,
    end_year: Optional[int] = None
) -> pd.DataFrame:
    """
    Fetch indicator data from World Bank.
    
    Parameters
    ----------
    indicators : dict
        Dict mapping indicator codes to names
        e.g., {'NY.GDP.PCAP.CD': 'gdp_per_capita'}
    countries : list of str
        ISO 3-letter country codes
    start_year : int
        Start year
    end_year : int, optional
        End year (defaults to current year)
    
    Returns
    -------
    pd.DataFrame
        Panel data with country and year
    
    Example
    -------
    >>> indicators = {
    ...     'NY.GDP.PCAP.CD': 'gdp_per_capita',
    ...     'SP.POP.TOTL': 'population'
    ... }
    >>> df = fetch_world_bank_data(indicators, ['USA', 'GBR'])
    """
    try:
        import wbdata
    except ImportError:
        raise ImportError("Install wbdata: pip install wbdata")
    
    import datetime
    end_year = end_year or datetime.datetime.now().year
    # Pass date range directly to the API to avoid downloading full history
    date_range = (datetime.datetime(start_year, 1, 1), datetime.datetime(end_year, 12, 31))

    all_data = []

    for indicator_code, indicator_name in indicators.items():
        try:
            data = wbdata.get_dataframe(
                {indicator_code: indicator_name},
                country=countries,
                date=date_range,
            )
            data = data.reset_index()
            all_data.append(data)
            print(f"✓ Downloaded {indicator_name}")

        except Exception as e:
            print(f"✗ Failed to download {indicator_name}: {e}")

    # Merge all indicators
    if all_data:
        df = all_data[0]
        for other_df in all_data[1:]:
            df = df.merge(other_df, on=['country', 'date'], how='outer')
        return df
    
    return pd.DataFrame()


# Common World Bank indicators
WORLD_BANK_INDICATORS = {
    # Income and Growth
    'NY.GDP.PCAP.CD': 'GDP per capita (current US$)',
    'NY.GDP.PCAP.KD.ZG': 'GDP per capita growth (%)',
    'NY.GDP.MKTP.KD.ZG': 'GDP growth (%)',
    
    # Population
    'SP.POP.TOTL': 'Population, total',
    'SP.URB.TOTL.IN.ZS': 'Urban population (%)',
    
    # Trade
    'NE.TRD.GNFS.ZS': 'Trade (% of GDP)',
    'BX.KLT.DINV.WD.GD.ZS': 'FDI, net inflows (% of GDP)',
    
    # Human Capital
    'SE.XPD.TOTL.GD.ZS': 'Education expenditure (% of GDP)',
    'SH.XPD.CHEX.GD.ZS': 'Health expenditure (% of GDP)',
    
    # Inequality
    'SI.POV.GINI': 'Gini index',
    'SI.POV.DDAY': 'Poverty headcount ratio ($1.90/day)',
}


# ============================================
# Usage Example
# ============================================

if __name__ == "__main__":
    # Example 1: Fetch US macro data from FRED
    us_macro = fetch_fred_series(
        series_ids=['GDP', 'UNRATE', 'CPIAUCSL', 'FEDFUNDS'],
        start_date='2010-01-01'
    )
    
    print("\nUS Macro Data (FRED):")
    print(us_macro.tail())
    
    # Save to CSV
    us_macro.to_csv('data/us_macro_fred.csv')
    print("\nSaved to data/us_macro_fred.csv")
    
    # Example 2: Fetch cross-country data from World Bank
    indicators = {
        'NY.GDP.PCAP.CD': 'gdp_per_capita',
        'SP.POP.TOTL': 'population',
        'NY.GDP.MKTP.KD.ZG': 'gdp_growth'
    }
    
    cross_country = fetch_world_bank_data(
        indicators=indicators,
        countries=['USA', 'GBR', 'DEU', 'FRA', 'JPN', 'CHN', 'IND', 'BRA'],
        start_year=2000
    )
    
    print("\nCross-Country Data (World Bank):")
    print(cross_country.head(10))
    
    # Save to CSV
    cross_country.to_csv('data/cross_country_wb.csv', index=False)
    print("\nSaved to data/cross_country_wb.csv")
```

## BLS Data Fetcher

```python
"""
BLS (Bureau of Labor Statistics) Data Fetcher
==============================================
Fetches labor market data from BLS Public Data API v2.
Requires: requests, pandas
API key (free): https://www.bls.gov/developers/

Note: BLS API v2 limits each request to a 20-year window.
This fetcher automatically chunks longer ranges into 20-year batches.
"""

import os
import math
import requests
import pandas as pd
from typing import List, Optional


def fetch_bls_series(
    series_ids: List[str],
    start_year: str = "2010",
    end_year: Optional[str] = None,
    api_key: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetch time series data from BLS API v2.
    Automatically splits requests exceeding the 20-year API limit.

    Parameters
    ----------
    series_ids : list of str
        BLS series IDs (e.g., ['LNS14000000'] for unemployment rate)
    start_year : str
        Start year (YYYY)
    end_year : str, optional
        End year (defaults to current year)
    api_key : str, optional
        BLS API key (defaults to BLS_API_KEY env var)

    Example
    -------
    >>> df = fetch_bls_series(['LNS14000000', 'CES0000000001'], '2000')
    """
    import datetime
    api_key = api_key or os.environ.get('BLS_API_KEY')
    end_yr = int(end_year or datetime.datetime.now().year)
    start_yr = int(start_year)

    # BLS API v2: max 20 years per request — split into chunks
    MAX_YEARS = 20
    chunks = []
    chunk_start = start_yr
    while chunk_start <= end_yr:
        chunk_end = min(chunk_start + MAX_YEARS - 1, end_yr)
        chunks.append((str(chunk_start), str(chunk_end)))
        chunk_start = chunk_end + 1

    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    all_records = []

    for s_yr, e_yr in chunks:
        payload = {
            "seriesid": series_ids,
            "startyear": s_yr,
            "endyear": e_yr,
        }
        if api_key:
            payload["registrationkey"] = api_key

        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "REQUEST_SUCCEEDED":
            raise ValueError(f"BLS API error: {data.get('message', 'Unknown error')}")

        for series in data["Results"]["series"]:
            sid = series["seriesID"]
            for obs in series["data"]:
                all_records.append({
                    "series_id": sid,
                    "year": int(obs["year"]),
                    "period": obs["period"],
                    "value": float(obs["value"]) if obs["value"] != "-" else None,
                })

    df = pd.DataFrame(all_records)
    # Handle monthly (M01-M12) and annual (M13) periods
    df = df[df["period"].str.match(r"M(0[1-9]|1[0-2])")]
    df["date"] = pd.to_datetime(
        df["year"].astype(str) + df["period"].str.replace("M", "-"), format="%Y-%m"
    )
    return (
        df.pivot(index="date", columns="series_id", values="value")
        .sort_index()
        .dropna(how="all")
    )


# Common BLS series IDs
BLS_SERIES = {
    "LNS14000000": "Unemployment Rate (seasonally adjusted)",
    "CES0000000001": "Total Nonfarm Employment (thousands)",
    "LNS11300000": "Labor Force Participation Rate",
    "CES0500000003": "Average Hourly Earnings, Private Sector",
    "CUUR0000SA0": "CPI-U, All Urban Consumers",
    "PCU0000000000": "Producer Price Index, All Commodities (not seasonally adjusted)",
}
```

## IMF Data Fetcher

```python
"""
IMF Data Fetcher
================
Fetches cross-country macro/financial data from the IMF Data Services API.
Requires: imf-reader, pandas
No API key required.
Install: pip install imf-reader

Key databases:
  IFS  — International Financial Statistics (exchange rates, reserves, money)
  WEO  — World Economic Outlook (GDP, inflation, current account, debt)
  BOP  — Balance of Payments Statistics
  GFSR — Global Financial Stability Report data
  DOT  — Direction of Trade Statistics

Browse all databases and series codes at:
  https://dataservices.imf.org/REST/SDMX_JSON.svc/Dataflow
"""

import pandas as pd
from typing import List, Optional


def fetch_imf_data(
    database: str,
    indicators: List[str],
    countries: List[str],
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
) -> pd.DataFrame:
    """
    Fetch data from IMF via imf-reader.

    Parameters
    ----------
    database : str
        IMF database code, e.g. 'IFS', 'WEO', 'BOP', 'DOT'
    indicators : list of str
        IMF series/indicator codes within the database
        e.g. ['PCPI_IX'] for CPI in IFS
    countries : list of str
        ISO 2-letter country codes, e.g. ['US', 'GB', 'DE']
    start_year : int, optional
        Start year
    end_year : int, optional
        End year

    Returns
    -------
    pd.DataFrame
        Long-format panel: columns include country, indicator, date, value

    Examples
    --------
    # CPI and exchange rate for US, UK, Germany from IFS
    >>> df = fetch_imf_data(
    ...     database='IFS',
    ...     indicators=['PCPI_IX', 'ENDE_XDC_USD_RATE'],
    ...     countries=['US', 'GB', 'DE'],
    ...     start_year=2000,
    ...     end_year=2023,
    ... )
    """
    try:
        import imf_reader
    except ImportError:
        raise ImportError("Install imf-reader: pip install imf-reader")

    frames = []
    for indicator in indicators:
        try:
            raw = imf_reader.get_data(database, indicator, countries)
            df = raw.copy()
            df["indicator"] = indicator
            frames.append(df)
            print(f"✓ Downloaded {database}/{indicator}")
        except Exception as e:
            print(f"✗ Failed {database}/{indicator}: {e}")

    if not frames:
        return pd.DataFrame()

    result = pd.concat(frames, ignore_index=True)

    # Filter years if requested
    if "date" in result.columns:
        result["year"] = pd.to_datetime(result["date"], errors="coerce").dt.year
        if start_year:
            result = result[result["year"] >= start_year]
        if end_year:
            result = result[result["year"] <= end_year]

    return result


# Common IMF indicator codes by database
IMF_INDICATORS = {
    "IFS": {
        "PCPI_IX":              "Consumer Price Index",
        "ENDE_XDC_USD_RATE":    "Exchange Rate (LCU per USD, period average)",
        "RAFA_USD":             "Foreign Reserves (USD)",
        "FMB_XDC":              "Broad Money (M2, LCU)",
        "FITB_3M_PA":           "3-Month Treasury Bill Rate (%)",
    },
    "WEO": {
        "NGDP_RPCH":    "Real GDP growth (%)",
        "PCPIPCH":      "Inflation, avg consumer prices (%)",
        "BCA_NGDPD":    "Current Account Balance (% of GDP)",
        "GGXWDG_NGDP":  "General Gov. Gross Debt (% of GDP)",
        "LUR":          "Unemployment Rate (%)",
    },
    "DOT": {
        "TXG_FOB_USD":  "Exports of Goods (USD)",
        "TMG_CIF_USD":  "Imports of Goods (USD)",
    },
}
```

## OECD Data Fetcher

```python
"""
OECD Data Fetcher
=================
Fetches cross-country data from the OECD SDMX REST API (v2).
Requires: requests, pandas
No API key required.

Note: The old stats.oecd.org endpoint is deprecated.
This implementation uses the new sdmx.oecd.org endpoint.
Find dataset/dataflow IDs at: https://data-explorer.oecd.org
"""

import requests
import pandas as pd
from io import StringIO
from typing import List, Optional


def fetch_oecd_data(
    dataflow: str,
    key: str = "all",
    start_period: Optional[str] = None,
    end_period: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch data from OECD SDMX REST API v2.

    Parameters
    ----------
    dataflow : str
        Full dataflow reference, format: 'AGENCY,DATAFLOW_ID'
        e.g. 'OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE_T10'
        Find IDs at: https://data-explorer.oecd.org
    key : str
        Filter key in SDMX key notation (default 'all' for all data)
        e.g. 'A.AUS+USA..' for annual data for Australia and US
    start_period : str, optional
        Start period, e.g. '2010' or '2010-Q1'
    end_period : str, optional
        End period, e.g. '2023' or '2023-Q4'

    Returns
    -------
    pd.DataFrame
        Long-format panel with country, time, value columns

    Examples
    --------
    # Annual GDP (expenditure approach) for USA and GBR, 2010-2023
    >>> df = fetch_oecd_data(
    ...     dataflow='OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE_T10',
    ...     key='A.USA+GBR...',
    ...     start_period='2010',
    ...     end_period='2023'
    ... )
    """
    base = "https://sdmx.oecd.org/public/rest/data"
    url = f"{base}/{dataflow}/{key}?format=csvfilewithlabels"
    if start_period:
        url += f"&startPeriod={start_period}"
    if end_period:
        url += f"&endPeriod={end_period}"

    resp = requests.get(url, timeout=120)
    resp.raise_for_status()

    df = pd.read_csv(StringIO(resp.text))
    df.columns = df.columns.str.lower().str.strip()
    return df


# Common OECD dataflows (find full IDs at https://data-explorer.oecd.org)
# Use the Data Explorer UI to navigate to a dataset, then copy the API URL.
OECD_DATAFLOWS = {
    "National Accounts (GDP, components)":
        "OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE_T10",
    "Labour Force Statistics":
        "OECD.ELS.SAE,DSD_LFS@DF_IALFS_UNE_M",
    "Main Economic Indicators":
        "OECD.SDD.STES,DSD_KEI@DF_KEI",
    "Health Statistics":
        "OECD.ELS.HD,DSD_HEALTH_STAT@DF_HEALTH_STATUS",
    "Revenue Statistics (tax-to-GDP)":
        "OECD.CTF,DSD_REV@DF_REV",
}
```

## Yahoo Finance Data Fetcher

```python
"""
Yahoo Finance Data Fetcher
==========================
Fetches financial and commodity price data.
Requires: yfinance, pandas
No API key required.
"""

import pandas as pd
from typing import List, Optional


def fetch_yahoo_finance(
    tickers: List[str],
    start_date: str = "2010-01-01",
    end_date: Optional[str] = None,
    price_col: str = "Adj Close",
) -> pd.DataFrame:
    """
    Fetch price data from Yahoo Finance.

    Parameters
    ----------
    tickers : list of str
        Yahoo Finance ticker symbols (e.g., ['^GSPC', 'AAPL', 'GC=F'])
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str, optional
        End date (defaults to today)
    price_col : str
        Which price column to return.
        Use 'Adj Close' (default) for dividend/split-adjusted prices,
        or 'Close', 'Open', 'High', 'Low', 'Volume'.
        Note: 'Adj Close' requires auto_adjust=False (the default here).

    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame with tickers as columns

    Example
    -------
    >>> df = fetch_yahoo_finance(['^GSPC', '^VIX', 'GC=F'], '2015-01-01')
    """
    try:
        import yfinance as yf
    except ImportError:
        raise ImportError("Install yfinance: pip install yfinance")

    import datetime
    end_date = end_date or datetime.date.today().isoformat()

    # auto_adjust=False preserves the 'Adj Close' column.
    # If you switch to auto_adjust=True, change price_col to 'Close'.
    raw = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
    # yfinance 0.2+ always returns MultiIndex columns (price_type, ticker),
    # even for a single ticker — do NOT branch on len(tickers).
    if isinstance(raw.columns, pd.MultiIndex):
        df = raw[price_col]           # → DataFrame with tickers as columns
        if isinstance(df, pd.Series): # single ticker returns Series
            df = df.to_frame(name=tickers[0])
    else:
        # older yfinance: flat columns for single ticker
        df = raw[[price_col]].rename(columns={price_col: tickers[0]})
    return df.dropna(how="all")


# Common Yahoo Finance tickers for economists
YAHOO_TICKERS = {
    # Equity Indices
    "^GSPC":  "S&P 500",
    "^DJI":   "Dow Jones Industrial Average",
    "^IXIC":  "NASDAQ Composite",
    # Volatility
    "^VIX":   "CBOE Volatility Index (VIX)",
    # Commodities
    "GC=F":   "Gold Futures",
    "CL=F":   "Crude Oil (WTI) Futures",
    # FX
    "EURUSD=X": "EUR/USD Exchange Rate",
    "GBPUSD=X": "GBP/USD Exchange Rate",
    # Bonds
    "^TNX":   "10-Year Treasury Yield",
    "^TYX":   "30-Year Treasury Yield",
}
```

## Requirements

### Python Packages
```bash
pip install fredapi wbdata pandas requests yfinance imf-reader python-dotenv
```

### API Keys

| Source | Key Required | Where to Get |
|--------|-------------|--------------|
| FRED | ✅ Required | https://fred.stlouisfed.org/docs/api/api_key.html |
| World Bank | ❌ None | — |
| BLS | ⚠️ Optional | https://www.bls.gov/developers/ (raises rate limit) |
| OECD | ❌ None | — |
| IMF | ❌ None | — |
| Yahoo Finance | ❌ None | — |

Keys are stored in `[plugin_root]/.env` and loaded automatically via Step 0. Never hardcode them in scripts.

## Best Practices

1. **Use Step 0** — always run the API key check before generating code; inject keys via `python-dotenv`, never hardcode
2. **Cache data locally** — save raw downloads to `data/raw/` and load from cache on subsequent runs to avoid hitting rate limits
3. **Document series IDs** — always include the human-readable name next to every series ID (e.g., `UNRATE  # Unemployment Rate`)
4. **Mind data vintages** — FRED, BLS, and IMF data are revised; note the download date and consider using vintage/real-time APIs for forecasting research
5. **Match frequencies explicitly** — don't silently merge monthly and quarterly series; resample to a common frequency with a deliberate aggregation method (mean, end-of-period, sum)
6. **Chunk long BLS requests** — BLS API v2 hard-limits to 20 years per call; use the chunked `fetch_bls_series` function which handles this automatically

## Common Pitfalls

- ❌ Hardcoding API keys in scripts — always use environment variables
- ❌ Assuming `auto_adjust=True` preserves `'Adj Close'` in yfinance — it doesn't; use `auto_adjust=False` to keep the `'Adj Close'` column
- ❌ Using the deprecated OECD `stats.oecd.org` endpoint — use `sdmx.oecd.org/public/rest/` instead
- ❌ Ignoring the BLS 20-year per-request limit — requests spanning >20 years will be silently truncated
- ❌ Mixing data frequencies without explicit resampling
- ❌ Ignoring data revisions when doing real-time or forecast evaluation research

## Related Skills & Commands

- **data-cleaning**: Clean and transform the fetched data for analysis
- **stats**: Generate summary statistics of downloaded data
- **/analyze**: Start a full analysis workflow with your dataset
- **panel-data**: If you fetched cross-country panel data
- **time-series**: If you fetched time series macro data