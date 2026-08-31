# D02: BEA — Data Provenance Record

## What this covers
Bureau of Economic Analysis inputs across two eras: (a) historical BEA tables
used for book-period values — salvaged chopped tables bundled in the repo —
and (b) the BEA API used for modern extensions. Serves 6 series.

## Source
- **Name**: U.S. Bureau of Economic Analysis
- **URL**: https://apps.bea.gov/api/data (API); historical tables via iTable
- **License**: Public domain (U.S. federal government work)
- **Retrieved**: book-period tables frozen as bundled chopped tables; API data
  fetched at run time with TTL caching
- **Format**: API JSON; salvaged XLSX chopped tables

## Subsources served
| Subsource | What it is | Fetch mode |
|---|---|---|
| BEA_LTEG_B1_B2 | Long Term Economic Growth (1966) compendium tables | bundled (out of print) |
| BEA_1977_T_B4 | 1977 Statistics of Income/Balance-Sheets table | bundled |
| BEA_WEALTH_T48 | Balance-sheet wealth table (historical vintage) | bundled + iTable extension |
| BEA_IO_1972_71IND_SHAIKH_APP9 | 1972 Input-Output, 71 industries (Shaikh App. 9) | bundled |
| BEA_GDP_BY_INDUSTRY | GDP-by-industry value added | bundled book period + API extension |
| BEA_NIPA_T114_FA_T41_DERIVED | NIPA T1.1.4/T4.1 derived aggregates | salvaged + API |

Note: the historical BEA vintages (LTEG 1966, 1977 tables) are out of print
and do not exist on today's BEA site; they ship as bundled chopped tables
under `replicator/inputs_bundled/SalvagedInputs/`. The modern BEA API provides
extensions only.

## Construction method
Book period: loaders read the bundled chopped tables. Extensions: the BEA
client (`S00_apis.bea_table`) fetches NIPA/Fixed-Assets/GDP-by-Industry tables
via `apps.bea.gov` with a free API key, then the per-series processors splice
at the documented overlap anchor. Ratio-type series (e.g. profit rates) extend
both numerator and denominator separately and recompute the ratio — never
splice the ratio itself.

## Transformations applied
- unit harmonisation: BEA Fixed Assets reports in millions, NIPA in billions —
  explicit conversion with dimensional-analysis comments in the processors
- vintage pinning for revised aggregates
- FISIM remap for NIPA T7.11 interest aggregates (see
  `docs/methodology/`)

## Known issues
- API key required for extension fetches (free registration); book-period
  reproduction is fully keyless.
- Historical vintages differ from current BEA revisions by construction; the
  registry records `year_range_book` vs `year_range_extension` per series.

## Validation
V03 spot-checks against book values; V01 package gate. See
`VALIDATION_REPORT.json`.

## Series served
See `python anu/scripts/L02_fetch_bea.py --list`.
