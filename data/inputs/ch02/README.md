# Chapter 2: Turbulent Macro Dynamics - Anu Chopped Data

**Book Chapter**: Chapter 2, "Turbulent Macro Dynamics" (Shaikh 2016, pp. 43-104)
**Figures**: Fig 2.1 through Fig 2.17 (18 figures including 2.4A, 2.4B, 2.4C)
**Files**: 8 Anu Chopped CSVs
**Standard**: Anu Chopped v1.0 (Row 1: metadata, Row 2: subseries IDs, Row 3+: data)
**Last Audited**: 2026-02-11 (validator: 8/8 PASS, catalog completeness verified)

---

## File Inventory

| File | Series | Columns | Year Range | Figures | Extension Source |
|------|--------|---------|------------|---------|-----------------|
| `Appendix2_IndustrialProduction.csv` | S001 | S001A-D, S001, S001_EXT, S001_COMBINED | 1860-2025 | Fig 2.1 | FRED API: INDPRO |
| `Appendix2_RealInvestmentUS_1832-2010.csv` | S002 | S002A-E, S002, S002_EXT, S002_COMBINED | 1832-2025 | Fig 2.2 | FRED API: GPDIC1 |
| `Appendix2_MeasuringWorthGDP_1889-2010.csv` | S003 | S003A, S003, S003_EXT, S003_COMBINED | 1780-2024 | Fig 2.3 | MeasuringWorth: USGDP |
| `Appendix2_Ayres.csv` | S004 | S004A, S004 | 1831-1939 | Fig 2.4A/B/C | None (historical) |
| `Appendix2_ManufacturingProductivityAndRealWages1889-2010.csv` | S007 | S007A-D, S007, S007_EXT, S007_COMBINED | 1860-2025 | Fig 2.5 | FRED API: OPHMFG |
| `Appendix2_ManufacturingProductivity.csv` | S008 | S008A-F, S008, S008_EXT, S008_COMBINED | 1780-2024 | Fig 2.6 | MeasuringWorth: USCPI |
| `Appendix2_Unemployment.csv` | S009 | S009A-B, S009, S009_EXT, S009_COMBINED | 1890-2025 | Fig 2.7 | FRED API: UNRATE |
| `Appendix2_GDPperCapita.csv` | S017 | S017A-GX (206 cols) | 1710-2000 | Fig 2.15-17 | Maddison (pending) |

---

## Column Structure (Anu Chopped 3-Column Extension Pattern)

Each extendable file follows this column layout (left to right):

```
Year | S###A (raw subsource 1) | S###B (raw 2 / transform) | ... | S### (Shaikh final) | S###_EXT (API extension) | S###_COMBINED (spliced)
```

- **S###A, S###B, ...**: Shaikh's raw subsources and intermediate transformations
- **S###**: Shaikh's final published series (the "ground truth" from the book)
- **S###_EXT**: Extension data pulled directly from public APIs (FRED, BLS, MeasuringWorth), raw values in the API's native units
- **S###_COMBINED**: The spliced series: Shaikh data through the overlap year, then API data re-indexed to Shaikh's base

---

## Series Details

### S001: Industrial Production (Fig 2.1)

| Column | ID | Source | Coverage | Base |
|--------|----|--------|----------|------|
| HS series (BEA 1973) | S001A | BEA Long Term Eco Growth, TA15 p.185 | 1860-1918 | 1913=100 |
| HS reindexed | S001B | Reindexed to 1958=100 | 1860-1918 | 1958=100 |
| FRB G-17 | S001C | Federal Reserve Board, Industrial Production | 1919-2010 | 2017=100 |
| FRB reindexed | S001D | Reindexed to 1958=100 | 1919-2010 | 1958=100 |
| **Final (Shaikh)** | **S001** | Spliced at 1919 | **1860-2010** | 1958=100 |
| Extension | S001_EXT | FRED API: INDPRO (Index 2017=100) | 2000-2025 | 2017=100 |
| Combined | S001_COMBINED | Spliced at 2010 | 1860-2025 | 1958=100 |

**Splice**: FRED INDPRO re-indexed from 2017=100 to 1958=100 using the ratio at the overlap year (2010). Same underlying FRB G-17 series.

### S002: Real Investment (Fig 2.2)

| Column | ID | Source | Coverage | Base |
|--------|----|--------|----------|------|
| BEA 1966 (1958\$) | S002A | BEA Long Term Eco Growth | 1832-1975 | Billions 1958\$ |
| BEA reindexed | S002B | Reindexed to 1901 | 1832-1975 | 1901=100 |
| BEA NIPA (2005\$) | S002C | BEA NIPA Fixed Investment | 1901-2010 | Billions 2005\$ |
| NIPA reindexed | S002D | Reindexed to 1901 | 1901-2010 | 1901=100 |
| Spliced | S002E | Spliced at 1929 | 1832-2010 | 1901=100 |
| **Final (Shaikh)** | **S002** | Reindexed to 1958 | **1832-2010** | 1958=100 |
| Extension | S002_EXT | FRED API: GPDIC1 (Bil. chained 2017\$, real) | 2000-2025 | Chained 2017\$ |
| Combined | S002_COMBINED | Spliced at 2010 | 1832-2025 | 1958=100 |

**Note**: Extension uses FRED GPDIC1 (Real Gross Private Domestic Investment, chained 2017 dollars). This is real investment, matching Shaikh's constant-dollar methodology.

### S003: GDP (Fig 2.3)

| Column | ID | Source | Coverage |
|--------|----|--------|----------|
| GDP (MeasuringWorth) | S003A | measuringworth.com | 1780-2000 |
| **Final (Shaikh)** | **S003** | measuringworth.com | **1780-2000** |
| Extension | S003_EXT | MeasuringWorth USGDP (2017\$) | 2001-2024 |
| Combined | S003_COMBINED | Spliced at 2000 | 1780-2024 |

**Splice**: Same source (MeasuringWorth), direct continuation. Values after 2000 are in 2017 dollars; ratio at 2000 re-indexes.

### S004: Ayres Business Cycle (Fig 2.4A/B/C)

| Column | ID | Source | Coverage |
|--------|----|--------|----------|
| (skipped) | S004A | -- | -- |
| **Ayres Index** | **S004** | Cleveland Trust Company (Ayres) | 1831-1939 |

**Note**: ~12 observations per year (monthly data). This is a historical business cycle indicator with no modern equivalent. No extension planned.

### S007: Manufacturing Productivity and Real Wages (Fig 2.5)

| Column | ID | Source | Coverage |
|--------|----|--------|----------|
| Long Term Eco Growth | S007A | BEA LTEG | 1860-1970 |
| BLS International | S007B | BLS International Labor Comp. | 1950-2009 |
| Calculated | S007C | Derived from A and B | 1889-2009 |
| Spliced | S007D | Spliced | 1889-2009 |
| **Final (Shaikh)** | **S007** | Rescaled | **1889-2009** |
| Extension | S007_EXT | FRED API: OPHMFG (Index 2012=100) | 1987-2025 |
| Combined | S007_COMBINED | Spliced at 2009 | 1889-2025 |

**Note**: Extension uses FRED OPHMFG (Manufacturing Sector: Real Output Per Hour of All Persons). This is manufacturing-specific, unlike the prior OUTNFB nonfarm proxy.

### S008: Manufacturing Productivity (Fig 2.6)

| Column | ID | Source | Coverage |
|--------|----|--------|----------|
| Sahr/MW CPI | S008A | Sahr + MeasuringWorth CPI | 1780-2010 |
| US CPI index | S008B | CPI 1982-84=100 | 1780-2010 |
| BLS Mfg Productivity | S008C | BLS productivity index | 1889-2010 |
| Mfg Output/hr | S008D | BLS manufacturing output/hr | 1889-2010 |
| Real unit labor cost | S008E | Calculated | 1889-2010 |
| Real compensation | S008F | Mfg real compensation | 1889-2010 |
| **Final (Shaikh)** | **S008** | Mfg real worker compensation | **1889-2010** |
| Extension | S008_EXT | MeasuringWorth CPI (1982-84=100) | 2001-2024 |
| Combined | S008_COMBINED | Spliced at 2010 | 1780-2024 |

**Note**: Extension covers only the CPI component (S008A/B). BLS manufacturing columns (S008C-F) can be extended separately via `pull_bls_ch02.py` (BLS series PRS30006092, PRS30006112, PRS30006152).

**Sahr Cross-Reference**: Columns S008A and S008B use Sahr CPI data for years 1780-1785. The full Sahr dataset (1774-2024, 30 series) is available at `Inputs/Sahr/Sahr_InflationConversionFactors.csv` (subseries S900A-S927). See `ANU_CHOPPED_CATALOG.json` for the formal cross-reference.

### S009: Unemployment (Fig 2.7)

| Column | ID | Source | Coverage |
|--------|----|--------|----------|
| LTEG | S009A | Long Term Eco Growth | 1890-1970 |
| ERP | S009B | Economic Report of the President | 1950-2010 |
| **Final (Shaikh)** | **S009** | Spliced | **1890-2010** |
| Extension | S009_EXT | FRED API: UNRATE (%) | 2000-2025 |
| Combined | S009_COMBINED | Spliced at 2010 | 1890-2025 |

**Splice**: FRED UNRATE is the same underlying BLS series. Direct continuation (identical units, percent).

### S017: GDP per Capita (Fig 2.15-2.17)

| Column | ID | Source | Coverage |
|--------|----|--------|----------|
| World | S017A | Maddison Project | 1710-2000 |
| W. Europe | S017B | Maddison | 1710-2000 |
| ... (206 cols total) | S017C-GX | Maddison (countries/regions) | 1710-2000 |
| RICHEST 4 | S017K | Calculated ratio | 1710-2000 |
| POOREST 4 | S017L | Calculated ratio | 1710-2000 |

**Note**: Decennial data (10-year intervals), classified as `wide_table` format in the catalog (not standard time_series). This is a cross-country comparison table with 206 columns -- there is no single "final series" column. Extension pending -- requires Maddison Project Database 2023 parsing.

---

## Cross-Chapter Data References

Some Chapter 2 figures use data from other chapters:

| Figure | Series | Source File | Location |
|--------|--------|-------------|----------|
| Fig 2.8-2.10 | S010, S011, S012 | Appendix5_DATALRprices.xlsx | `ch05/Appendix5_DATALRprices.csv` |
| Fig 2.11 | S013 | Appendix6_Table68II7.xlsx | `ch06/Appendix6_Table68II7.csv` |
| Fig 2.12-2.14 | S014, S015, S016 | Census ASM, calculated, BEA I-O | **Not yet in Anu Chopped** |

---

## Data Quality Notes

1. **Ayres (S004)**: Contains ~12 observations per year (monthly). This is NOT annual data -- agents should treat this as sub-annual when loading.
2. **GDPperCapita (S017)**: 206 columns covering countries and world regions. Decennial only (10-year intervals from 1710-2000). Classified as `wide_table` format. Last column is "formula check" -- can be ignored.
3. **MeasuringWorthGDP (S003)**: Metadata in Row 1 was originally sparse ("measuringworth.com"). Has been enriched with proper source description.
4. **ManufacturingProductivity (S008)**: 7 columns with complex provenance. Row 1 metadata is concatenated from the original Excel file's merged cells.
5. **All files**: Empty year rows outside actual data ranges have been trimmed during extension processing.

---

## Extension Data Sources (API)

All extension data is pulled directly from public APIs using reproducible scripts in `Technical/scripts/`. No pre-downloaded data files -- every value can be traced to its API endpoint.

| API | Series ID | Description | Units | Used For | Script |
|-----|-----------|-------------|-------|----------|--------|
| FRED | INDPRO | Industrial Production Total Index | Index 2017=100 | S001_EXT | `pull_fred_ch02.py` |
| FRED | GPDIC1 | Real Gross Private Domestic Investment | Bil. chained 2017\$ | S002_EXT | `pull_fred_ch02.py` |
| FRED | UNRATE | Unemployment Rate | Percent | S009_EXT | `pull_fred_ch02.py` |
| FRED | OPHMFG | Manufacturing Output Per Hour | Index 2012=100 | S007_EXT | `pull_fred_ch02.py` |
| MeasuringWorth | USGDP | Real GDP per capita | 2017 dollars | S003_EXT | Manual download |
| MeasuringWorth | USCPI | Consumer Price Index | Index 1982-84=100 | S008_EXT | Manual download |
| BLS | PRS30006092 | Mfg Output Per Hour | Index 2012=100 | S008C_EXT | `pull_bls_ch02.py` |
| BLS | PRS30006112 | Mfg Unit Labor Costs | Index 2012=100 | S008E_EXT | `pull_bls_ch02.py` |
| BLS | PRS30006152 | Mfg Real Hourly Compensation | Index 2012=100 | S008F_EXT | `pull_bls_ch02.py` |

**API Keys Required**: `FRED_API_KEY` and `BLS_API_KEY` environment variables.
- FRED: https://fred.stlouisfed.org/docs/api/api_key.html (free)
- BLS: https://www.bls.gov/developers/api_signature_v2.htm (free)

**MeasuringWorth**: No public API. Downloaded manually from measuringworth.com. Provenance documented in `Inputs/API_Data/MeasuringWorth/provenance.json`.

**Rebuild workflow**:
```bash
# 1. Pull API data
python Technical/scripts/pull_fred_ch02.py
python Technical/scripts/pull_bls_ch02.py
# Download MeasuringWorth CSVs per Inputs/API_Data/MeasuringWorth/README.md
python Technical/scripts/validate_measuringworth.py

# 2. Rebuild extensions
python Technical/scripts/rebuild_extensions_ch02.py
```

---

## Validator Exceptions (Documented)

All 8 ch02 files pass the Anu Chopped validator (`validate_chopped.py`). The following warnings are known and intentional:

| Warning | File | Reason |
|---------|------|--------|
| V5 (1,194x) | Ayres | Monthly data (~12 obs/year) causes repeated year values. Inherent to the source -- NOT an error. |
| V8 | ManufacturingProductivityAndRealWages1889-2010 | Filename includes date range. Matches original Excel name. Renaming would break existing references. |
| V8 | MeasuringWorthGDP_1889-2010 | Same: date range in filename matches original Excel. |
| V8 | RealInvestmentUS_1832-2010 | Same: date range in filename matches original Excel. |
| V9 | GDPperCapita | No final series column (all IDs have letter suffixes). This is a wide_table, not a standard time_series. |

---

## Known Data Quality Caveats

1. **S002_EXT (Real Investment)**: Uses FRED GPDIC1 (real, chained 2017 dollars). Previous extension used nominal GPDI -- this has been corrected.
2. **S007_EXT (Manufacturing Productivity & Real Wages)**: Uses FRED OPHMFG (manufacturing-specific output per hour). Previous extension used OUTNFB nonfarm proxy -- this has been corrected.
3. **S008 (Manufacturing Productivity)**: Only the CPI component (S008A/B) has been extended via MeasuringWorth. The BLS manufacturing columns (S008C-F) can be extended via `pull_bls_ch02.py` once BLS API key is available.
4. **GDPperCapita (S017)**: No extension yet. Requires Maddison Project Database 2023 parsing (separate task).
5. **Sahr HDARP extraction**: The Sahr PDF was processed via HDARP. Coverage fields in the catalog reflect actual data availability per column.

---

## How to Use This Data

**For the Shiny app**: The `data_loader.R` function `load_anu_chopped_data()` reads these CSVs and converts each column into long format (`series_name`, `year`, `value`). The `_COMBINED` columns are the ones agents should use for visualization -- they provide the complete series from Shaikh's earliest data through 2025.

**For extension work**: The `_EXT` column shows the raw API data in its native units. The `_COMBINED` column shows the spliced result. To verify the splice, compare S### and S###_EXT values at the overlap year.

**For provenance**: Row 1 of each CSV contains the full source citation for each column. The `ANU_CHOPPED_CATALOG.json` in the parent directory has machine-readable metadata for all columns. API provenance is in `Inputs/API_Data/{FRED,BLS,MeasuringWorth}/provenance.json`.
