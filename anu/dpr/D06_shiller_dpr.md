# D06: Shiller (Yale) — Data Provenance Record

## What this covers
Robert Shiller's long-run financial datasets (ie_data workbook and companions)
feeding the Chapter 10 long bond/equity series and the required-return
constructions in Chapter 15. Serves 3 series.

## Source
- **Name**: Robert J. Shiller (Yale), online data library
- **URL**: http://www.econ.yale.edu/~shiller/data.htm (ie_data.xls and kin)
- **License**: academic free-use; Shaikh adaptations documented per series
- **Retrieved**: ie_data fetched live at run time; historical companions
  (USLR_ys, USLR_ib10yr, INTROPPRICE_* ) are bundled salvaged workbooks,
  some preserved via the Wayback Machine from anwarshaikhecon.org
- **Format**: XLS(X) workbooks

## Subsources served
| Subsource | What it is | Fetch mode |
|---|---|---|
| SHILLER_ie_data | ie_data.xls long-run stock/home/interest series | live XLS |
| USLR_ys | Shiller yield series used by the book vintage | bundled |
| USLR_ib10yr | Shiller 10-year bond yield history | bundled |
| INTROPPRICE_rreq / _preq / _prstarshiller1 | required-return constructions (Shaikh adaptation of Shiller inputs) | bundled |

## Construction method
The Shiller client (`S00_apis.shiller_ie_data` / `shiller_annual`) downloads
and caches the workbook, extracting annual columns. The required-return
series reuse Shaikh's own constructions, which are bundled because the
original hosting site is offline.

## Transformations applied
- monthly → annual (averaging or end-of-year per the book's convention,
  documented per series)
- decimal vs percent normalisation per registry units

## Known issues
- ie_data.xls is revised annually (through the current year); earlier years
  are stable.
- The INTROPPRICE constructions are author-derived; provenance is the bundled
  workbook, and the method is documented in the per-series DPR.

## Validation
V03 spot-checks; V01 package gate.

## Series served
See `python anu/scripts/L06_fetch_shiller.py --list`.
