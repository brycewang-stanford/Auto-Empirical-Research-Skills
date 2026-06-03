## Citation discipline

Every numerical claim in the output must be followed by an inline citation in the form `[SOURCE_CODE, vintage]`. `SOURCE_CODE` is a short tag (e.g. `ONS_PSF`, `OBR_EFO`, `BoE_MPR`, `Fed_FOMC`, `ECB_EB`, `RBA_SoMP`, `IMF_WEO`, `OECD_EO`, `Eurostat`, `BLS`, `BEA`, `FRED`, `ABS`, `Comtrade`) matching an entry in the References footer. `vintage` is the publication date of the source data (e.g. `Mar 2026`, `Q4 2025`, `Jan 2026`).

**Examples:**

> CPI was 3.4% YoY in March 2026 [ONS_CPI, Mar 2026].

> The OBR forecasts borrowing falling to 1.6% of GDP by 2028-29 [OBR_EFO, Mar 2026].

> Industry concentration is moderate: HHI is 1,820 across the top 8 firms [Companies_House, Q4 2025].

**Numbers that cannot be sourced to a primary publication must NOT appear in the output.** No exceptions: do not estimate, infer from training data, interpolate, or recall from memory. If a needed number isn't in fetched data, state it explicitly:

> [Source] has not yet published this measure for [period].

**Self-check before output**: scan the draft for every number. If any number lacks an inline citation, either add the citation or remove the number. Citation density should be roughly even across sections; a section with no citations is a red flag that the section was generated rather than sourced.
