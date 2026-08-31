# D03: World Bank Open Data — Data Provenance Record

## What this covers
World Bank Open Data API inputs; currently one subsource (China reserves,
excluding gold) serving the Chapter 15 / external-study current-account
material. Serves 1 series.

## Source
- **Name**: World Bank Open Data (API v2)
- **URL**: https://api.worldbank.org/v2/country/CHN/indicator/FI.RES.XGLD.CD?format=json
- **License**: CC-BY-4.0 (World Bank Open Data Terms)
- **Retrieved**: at run time (open API, no key)
- **Format**: JSON API

## Construction method
The World Bank client (`code/S00_setup/S00_apis.py: worldbank_indicator`)
fetches the indicator with TTL caching; the per-series processor aligns to the
book's units (current USD billions) and splices at the overlap year.

## Transformations applied
- current-USD conversion (API returns current USD; no deflation applied)
- annual frequency confirmed against the book series

## Known issues
- World Bank series are revised with WEO cycles; vintage notes recorded in the
  per-series DPR.

## Validation
V03 spot-checks; V01 package gate.

## Series served
XS-series China reserves (see `python anu/scripts/L03_fetch_worldbank.py --list`).
