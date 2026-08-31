# D05: U.S. Census FT-900 — Data Provenance Record

## What this covers
U.S. Census Bureau foreign-trade releases (FT-900) feeding the trade-balance
series. Serves 1 series.

## Source
- **Name**: U.S. Census Bureau, Foreign Trade Division (FT-900 release)
- **URLs**:
  - https://www.census.gov/foreign-trade/statistics/historical/exh1.txt (EXH1)
  - https://www.census.gov/foreign-trade/balance/c5700.html (China balance)
- **License**: Public domain (U.S. federal government, 17 USC 105)
- **Retrieved**: at run time (open, no key)
- **Format**: plain-text historical tables / HTML

## Construction method
The census client (`code/S00_setup/S00_apis.py: census_ft900_annual_balance`)
parses the FT-900 EXH1 historical table (annual goods balance) and the
country-level balance pages, caching raw text.

## Transformations applied
- monthly → annual aggregation where the release is monthly
- nominal USD; no deflation (matches the book's presentation)

## Known issues
- Census re-bases historical goods-balance vintages occasionally (BOP
  adjustments); vintage notes in the per-series DPR.

## Validation
V03 spot-checks; V01 package gate.

## Series served
See `python anu/scripts/L05_fetch_census_ft900.py --list`.
