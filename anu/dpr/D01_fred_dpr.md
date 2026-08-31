# D01: FRED — Data Provenance Record

## What this covers
Live modern data from FRED (Federal Reserve Economic Data, St. Louis Fed):
the primary extension source for post-2010 observations, and the book-period
source for several interest-rate and price series. Serves 9 series.

## Source
- **Name**: FRED, Federal Reserve Bank of St. Louis
- **URL**: https://fred.stlouisfed.org/ (per-series URLs below)
- **License**: FRED Terms of Use; underlying series are U.S. federal
  government works (public domain)
- **Retrieved**: at run time (cached under the replicator's raw cache);
  subsource metadata epoch is recorded in `SUBSOURCE_METADATA.json`
- **Format**: JSON API (key) and fredgraph CSV (keyless)

## Subsources served
| Subsource | Series page | Fetch mode |
|---|---|---|
| FRED_INDPRO | …/series/INDPRO | API |
| FRED_CPIAUCNS | …/series/CPIAUCNS | API |
| FRED_PPIACO | …/series/PPIACO | fredgraph CSV (keyless) |
| FRED_OPHMFG | …/series/OPHMFG | API |
| FRED_COMPRMS | …/series/COMPRMS | API |
| FRED_UNRATE | …/series/UNRATE | API |
| FRED_W209RC1_Q | …/series/W209RC1 | JSON API |
| FRED_AAA / FRED_AAA_proxy_LTcorp | fredgraph CSV `?id=AAA` | live CSV |
| FRED_GS10 | fredgraph CSV `?id=GS10` | live CSV |
| USLR_USWPI | fredgraph CSV `?id=PPIACO` (book period salvaged; Jastram pre-1913) | salvaged xlsx + live CSV |

## Construction method
Per-series loaders (`code/L01_loaders/L01_{SID}*.py`) call the shared FRED
client (`code/S00_setup/S00_apis.py: fred_observations` / `fred_csv_observations`)
with TTL caching. Book-period values come from bundled inputs where the
original vintage differs from today's FRED series; extensions are spliced at
the last book-year overlap with a documented anchor. No proxy substitutions:
where the book used a Federal Reserve Board G.17 release, the extension uses
the same agency's series in FRED (e.g. FRB G.17 → FRED INDPRO).

## Transformations applied
- annual averaging of monthly/quarterly observations where the book series is annual
- reindexing to the book's base year via a single documented scale factor at the
  overlap year (see each series' `reindex_anchor_method` in the registry)
- vintage pinning: never-revised series (UNRATE, TB3MS-family, AAA, DGS10,
  PPIACO, CPIAUCSL) are re-fetched freely; revised series (GDP-family,
  OPHMFG, COMPRMS) carry vintage notes

## Known issues
- FRED revises some series; byte-identical reproduction is only guaranteed
  for the never-revised list above.
- Pre-1913 wholesale prices (S502) mix Jastram's academic series with PPIACO;
  the splice point is documented in the S502 DPR.

## Validation
V03 per-series validators compare chopped output against book reference
values at certified spot-check years (tolerance 1%). Package gate: V01 checks
presence, coverage and unit sanity. See `VALIDATION_REPORT.json` for per-series
MAE / max-abs results.

## Series served
See `python anu/scripts/L01_fetch_fred.py --list`.
