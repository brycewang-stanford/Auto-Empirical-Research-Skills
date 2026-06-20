# Common Data Sources

Starting-point reference for data collection across fields. **This list is not exhaustive** — it covers the sources most frequently used by researchers working in the domains below. For any specific research question, also search the web for sources not listed here.

Each entry follows the format:

```
### Source Name
- URL
- API availability
- Coverage
- License
- R / Python packages (if any)
- Notes
```

---

## Brazil — Economics and Finance

### SGS — Sistema Gerenciador de Séries Temporais (Banco Central do Brasil)

- **URL:** https://www3.bcb.gov.br/sgspub/
- **API:** Yes. Endpoint `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json`
- **Coverage:** Brazilian macroeconomic and financial series (rates, FX, monetary aggregates, credit, prices)
- **License:** Open
- **R:** `rbcb`
- **Python:** `python-bcb`
- **Notes:** Every series has a numeric code. Check the SGS portal to find codes.

### SIDRA — Sistema IBGE de Recuperação Automática

- **URL:** https://sidra.ibge.gov.br/
- **API:** Yes. Endpoint `https://apisidra.ibge.gov.br/values/t/{table}/...`
- **Coverage:** Brazilian census, PNAD, PNADC, PIB, IPCA, demographic and socioeconomic data
- **License:** Open
- **R:** `sidrar`
- **Python:** `sidrapy`
- **Notes:** SIDRA uses table codes (e.g., 4099 for PNADC unemployment). Table codes and variable codes are required.

### Ipeadata

- **URL:** http://www.ipeadata.gov.br/
- **API:** Yes (OData). Endpoint `http://www.ipeadata.gov.br/api/odata4/`
- **Coverage:** Aggregated macroeconomic, regional, and social series
- **License:** Open
- **R:** `ipeadatar`
- **Python:** `ipeadatapy`
- **Notes:** Good for regional series not available in SGS or SIDRA.

### CVM — Comissão de Valores Mobiliários

- **URL:** https://dados.cvm.gov.br/
- **API:** No; bulk downloads available
- **Coverage:** Brazilian listed companies: financial statements, disclosures, fund data
- **License:** Open
- **Notes:** Data is delivered as CSV files organized by document type and year.

### B3 — Brasil, Bolsa, Balcão

- **URL:** https://www.b3.com.br/
- **API:** Limited; some via partner vendors
- **Coverage:** Brazilian equities, derivatives, fixed income
- **License:** Mixed (some open, most restricted)
- **Notes:** For academic use, consider WRDS-Bloomberg or CEMAP access.

### Tesouro Nacional

- **URL:** https://www.tesourotransparente.gov.br/
- **API:** Yes, partial
- **Coverage:** Public debt, primary balance, fiscal statistics
- **License:** Open
- **Notes:** Tesouro Direto historical prices available via bulk download.

---

## International — Economics and Finance

### FRED — Federal Reserve Economic Data

- **URL:** https://fred.stlouisfed.org/
- **API:** Yes, key required (free)
- **Coverage:** US and international macro, financial, trade series
- **License:** Open (some series restricted)
- **R:** `fredr`, `tidyquant`
- **Python:** `fredapi`, `pandas-datareader`
- **Notes:** The standard starting point for macroeconomic research.

### World Bank Open Data

- **URL:** https://data.worldbank.org/
- **API:** Yes, no key required
- **Coverage:** Country-year development, demographic, economic indicators
- **License:** Open (CC BY 4.0)
- **R:** `WDI`, `wbstats`
- **Python:** `wbdata`, `world_bank_data`
- **Notes:** Use WDI indicator codes. Long panels from the 1960s onward for many variables.

### IMF Data

- **URL:** https://data.imf.org/
- **API:** Yes (SDMX)
- **Coverage:** International financial statistics, balance of payments, fiscal, external debt
- **License:** Open
- **R:** `imfr`
- **Python:** `imf-reader`
- **Notes:** Use dataset IDs (e.g., IFS, BOP, GFS).

### OECD Data

- **URL:** https://data.oecd.org/
- **API:** Yes (SDMX)
- **Coverage:** OECD-country economic, social, environmental indicators
- **License:** Open
- **R:** `OECD`
- **Python:** `pandasdmx`
- **Notes:** Good for cross-country comparisons.

### Penn World Table

- **URL:** https://www.rug.nl/ggdc/productivity/pwt/
- **API:** No; bulk download
- **Coverage:** Cross-country comparable GDP, productivity, factor inputs
- **License:** Open
- **R:** `pwt10`
- **Notes:** Use for long-run cross-country growth research.

### UN Comtrade

- **URL:** https://comtradeplus.un.org/
- **API:** Yes, key required
- **Coverage:** Bilateral trade flows by product and country
- **License:** Open (with rate limits)
- **R:** `comtradr`
- **Python:** `comtradeapicall`
- **Notes:** HS codes for products; use at 2, 4, or 6 digits.

### BIS — Bank for International Settlements

- **URL:** https://www.bis.org/statistics/
- **API:** Yes (SDMX)
- **Coverage:** International banking, debt, credit, exchange rates
- **License:** Open
- **Notes:** Good for financial stability research.

---

## Financial and Accounting (Restricted Access)

### WRDS — Wharton Research Data Services

- **URL:** https://wrds-www.wharton.upenn.edu/
- **API:** Yes (requires institutional login)
- **Coverage:** Compustat, CRSP, TAQ, IBES, and dozens of other databases
- **License:** Restricted (institutional subscription)
- **R:** `RPostgres` with WRDS connection
- **Python:** `wrds` package
- **Notes:** Standard for US financial research.

### Compustat (via WRDS)

- **Coverage:** US and global firm-level accounting data
- **Notes:** Requires WRDS access.

### CRSP

- **Coverage:** US stock prices, returns, corporate actions from 1926
- **Notes:** Requires WRDS access.

### Bloomberg

- **Coverage:** Real-time and historical financial data
- **Notes:** Requires Bloomberg Terminal access; `pybbg` and `Rblpapi` for programmatic access.

---

## Social Sciences — General

### ICPSR — Inter-university Consortium for Political and Social Research

- **URL:** https://www.icpsr.umich.edu/
- **API:** Partial (via REST)
- **Coverage:** Social science survey and experimental data archive
- **License:** Mixed (most require registration)
- **Notes:** Deep archive; many classic datasets deposited here.

### Harvard Dataverse

- **URL:** https://dataverse.harvard.edu/
- **API:** Yes
- **Coverage:** Research data across all fields; many replication packages
- **License:** Mostly open
- **R:** `dataverse`
- **Python:** `pyDataverse`
- **Notes:** Increasingly the default for replication package deposits.

### UK Data Service

- **URL:** https://ukdataservice.ac.uk/
- **API:** Partial
- **Coverage:** UK government surveys, census, longitudinal studies
- **License:** Mixed (registration required)
- **Notes:** Standard for UK social research.

### Eurostat

- **URL:** https://ec.europa.eu/eurostat/
- **API:** Yes (SDMX and REST)
- **Coverage:** European Union statistical data
- **License:** Open
- **R:** `eurostat`
- **Python:** `eurostat` package
- **Notes:** Good for cross-EU comparisons.

### UN Data

- **URL:** https://data.un.org/
- **API:** Yes (via SDMX)
- **Coverage:** UN agency statistics across development, health, environment
- **License:** Open
- **Notes:** Aggregates data from multiple UN agencies.

---

## Health and Epidemiology

### WHO — Global Health Observatory

- **URL:** https://www.who.int/data/gho
- **API:** Yes
- **Coverage:** Global health indicators
- **License:** Open
- **Notes:** Good for cross-country health research.

### CDC — Centers for Disease Control

- **URL:** https://data.cdc.gov/
- **API:** Yes (Socrata)
- **Coverage:** US public health data
- **License:** Open
- **Notes:** Includes NHANES, NHIS, WONDER.

### PubMed / NCBI Datasets

- **URL:** https://www.ncbi.nlm.nih.gov/
- **API:** Yes (Entrez)
- **Coverage:** Biomedical literature and linked datasets
- **License:** Open
- **R:** `rentrez`
- **Python:** `biopython`

### NHANES — National Health and Nutrition Examination Survey

- **URL:** https://www.cdc.gov/nchs/nhanes/
- **API:** No; bulk SAS/XPT files
- **Coverage:** US health, nutrition, and exam data
- **License:** Open
- **R:** `nhanesA`
- **Notes:** Many cross-sectional waves.

### DataSUS (Brazil)

- **URL:** https://datasus.saude.gov.br/
- **API:** Partial
- **Coverage:** Brazilian public health system data (mortality, morbidity, coverage)
- **License:** Open
- **R:** `microdatasus`
- **Notes:** SIM, SINASC, SIH, SIA, CNES are the main subsystems.

---

## Political Science

### V-Dem — Varieties of Democracy

- **URL:** https://www.v-dem.net/
- **API:** No; bulk download
- **Coverage:** Democracy indicators for all countries, 1789 onward
- **License:** Open (CC)
- **R:** `vdemdata`
- **Notes:** Most comprehensive democracy dataset; many sub-indices.

### Polity Project

- **URL:** https://www.systemicpeace.org/polityproject.html
- **API:** No; bulk download
- **Coverage:** Regime type indicators
- **License:** Open
- **Notes:** Classical source, though V-Dem is now more widely used.

### Correlates of War

- **URL:** https://correlatesofwar.org/
- **API:** No; bulk download
- **Coverage:** Interstate and civil conflict, alliances, capabilities
- **License:** Open
- **Notes:** Standard for conflict research.

### Manifesto Project

- **URL:** https://manifesto-project.wzb.eu/
- **API:** Yes
- **Coverage:** Political party platforms coded on left-right and issue dimensions
- **License:** Open (registration required)
- **R:** `manifestoR`
- **Notes:** For party politics and ideology research.

---

## Environmental

### NOAA — National Oceanic and Atmospheric Administration

- **URL:** https://www.noaa.gov/data
- **API:** Yes (multiple endpoints)
- **Coverage:** Climate, weather, oceanographic data
- **License:** Open
- **R:** `rnoaa`
- **Python:** `noaa-sdk`

### NASA Earth Data

- **URL:** https://www.earthdata.nasa.gov/
- **API:** Yes
- **Coverage:** Satellite imagery, climate reanalysis, land use
- **License:** Open (registration required)
- **Python:** `earthaccess`

### Copernicus

- **URL:** https://www.copernicus.eu/
- **API:** Yes (CDS, ADS, CAMS, CLMS, etc.)
- **Coverage:** European Earth observation, reanalysis (ERA5), atmospheric composition
- **License:** Open (registration required)
- **Python:** `cdsapi`

### Our World in Data

- **URL:** https://ourworldindata.org/
- **API:** Yes
- **Coverage:** Curated datasets on development, environment, health, energy
- **License:** Open (CC BY)
- **Notes:** Good for quick visualization-ready data.

---

## Open Science Repositories

### Harvard Dataverse

Listed above under Social Sciences — General. Use for deposited replication packages and general-purpose research data.

### Zenodo

- **URL:** https://zenodo.org/
- **API:** Yes
- **Coverage:** Any research output — data, code, papers
- **License:** Mixed (chosen by depositor)
- **Notes:** CERN-hosted, widely used for software releases and supplementary data.

### Open Science Framework (OSF)

- **URL:** https://osf.io/
- **API:** Yes
- **Coverage:** Research projects, preregistrations, data, materials
- **License:** Mixed
- **Notes:** Strong in psychology and social sciences. Good for preregistered studies.

### figshare

- **URL:** https://figshare.com/
- **API:** Yes
- **Coverage:** Research outputs across fields
- **License:** Mixed
- **Notes:** Many publishers use figshare for supplementary material.

---

**Reminder:** This is a starting point, not a boundary. Search the web for the source that best fits your research question. New databases appear constantly, existing sources change, and your specific project may need data from an outlet not listed here.
