# XS002 — Wage Equivalent and Corp/Noncorp Split (Extension Provenance Record)

**Classification:** extendable_via_component_refetch  **Tolerance for extended values:** 1.0%

## Method

Under the Chapter 6 Generalized Perpetual Inventory Method (GPIM) construction pipeline, and following the principle that extended values must be rebuilt from sources rather than spliced, **extension does NOT splice the published XS002 values**. Instead, the extension re-fetches the underlying National Income and Product Accounts (NIPA), BEA Fixed Asset, IRS, and Census components and re-runs the formula end-to-end at the current vintage.

1. Fetch the BEA NIPA tables via the BEA data API (a BEA API key is required), using the table ids documented for this series' primary source.
2. Fetch BEA Fixed Asset Tables 6.1, 6.4, 6.7, 6.8 from the same source.
3. Re-run the construction formula end-to-end.

## Worked Example

For XS002, the round-trip validation reads the raw series from the Appendix 6.8 workbook and confirms bit-for-bit reproduction of the published series for the book period 1947-2011. A worked-example year (typically 2009 per book p. 842, or 2011 per Shaikh's last published vintage) verifies headline values.

## Source substitutions

No proxies are used in the book period. Book period is fully sourced from primary BEA / IRS / Census; no proxies.

## Forecast vs. observed data

No synthetic values, interpolations, or freezes are used. All values are verbatim from Shaikh's posted Appendix 6.8 chopped tables (MD5-verified against the staged 1993 BEA depreciation inputs).

## Failure Mode Table

| Failure | Detection | Response |
|---------|-----------|----------|
| Appendix workbook missing or corrupted | The appendix loader raises a file-not-found error or returns an empty table | The load step returns a FAIL status naming the missing file |
| Variable name not in workbook | The variable lookup returns no rows | The load step records 0 rows for that subseries; validation flags it as missing |
| BEA / IRS vintage drift during extension | The documented re-fetch script logs the vintage year; validation tolerance widens for extension rows | Documented per-year; no silent overwrite of book period |
| FISIM (financial services indirectly measured) revision to NIPA Table 7.11 line numbers (affects XS003) | The Table 7.11 line resolver falls back to the nearest pinned vintage with a logged warning | Lines are re-mapped by their published stub labels; the vintage used is logged |
| BEA 1993 depreciation rate not available post-2011 | The capital-stock series (XS004 and related) freeze depreciation-rate inputs at the 2011-vintage projection | Documented with the staged 1993 BEA methodology inputs |

## Comparison with the earlier replication

Round-trip parity with an earlier replication is expected within tolerance for the book period. The comparison against that earlier replication's per-series output is informational only, when available.

## Extension integrity

Extension MUST re-fetch the BEA, IRS, and Federal Reserve Board (FRB) component series and re-compute the formula end-to-end; splicing the published series is forbidden. The loader caches BEA and FRED responses for 30 days (book-period values are cached permanently).
