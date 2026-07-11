# XS009 — IRS Corporate Inventories and Total Capital Stock (Extension Provenance Record)

**Classification:** feasible_with_proxy_or_substitute  **Tolerance for extended values:** 1.0%

## Method

Following the Chapter 6 Generalized Perpetual Inventory Method (GPIM) construction pipeline and the project's anti-degradation rule, **extension does NOT splice the published XS009 values**. Instead, the extension re-fetches the underlying National Income and Product Accounts (NIPA), BEA Fixed Asset, IRS, and Census components and re-runs the formula end-to-end at the current vintage.

1. Fetch the BEA NIPA tables from the BEA API (a BEA API key is required) using the documented primary-source table ids.
2. Fetch BEA Fixed Asset T6.1, T6.4, T6.7, T6.8 from the same source.
3. Re-run the construction formula end-to-end.
4. Post-2011 inventory currently uses the `constant_ratio_proxy_2012_onwards` extension method. A later lift is recommended: re-estimate the INV/KGC ratio from the current IRS SOI Corporation Complete Report (https://www.irs.gov/statistics/soi-tax-stats-corporation-complete-report) using the BEA Fixed Asset Table 6.3 historical-cost stock as the denominator.

## Worked Example

For XS009, the round-trip validation reads the raw values from the Appendix 6.8 workbook and confirms bit-for-bit reproduction of the published series for the book period 1946-2011. A worked-example year (typically 2009 per book p. 842, or 2011 per Shaikh's last published vintage) verifies headline values.

## Proxy Use

No proxies are used in the book period. XS009 carries an extension-only proxy flag (`constant_ratio_proxy_2012_onwards`).

## Synthetic Values

No synthetic values, interpolations, or freezes are used. All values are verbatim from Shaikh's posted Appendix 6.8 chopped tables (MD5-verified against the reconstructed BEA 1993 staged inputs).

## Failure Mode Table

| Failure | Detection | Response |
|---------|-----------|----------|
| Appendix workbook missing or corrupted | The appendix loader raises a file-not-found error or returns an empty table | Loading fails with an explicit error |
| Variable name not in workbook | The variable lookup returns no rows | Zero rows are recorded for that subseries and validation flags it as missing |
| BEA / IRS vintage drift during extension | The re-fetch logs the vintage year; validation tolerance widens for extension rows | Documented per-year; no silent overwrite of the book period |
| NIPA Table 7.11 financial services indirectly measured (FISIM) line revision (affecting XS003) | The line resolver falls back to the nearest pinned vintage with a logged warning | Re-mapped by label; vintage logged |
| BEA 1993 depreciation rate not available post-2011 | XS004/XS006/XS007 freeze depreciation-rate inputs at 2011-vintage projection | Documented with the reconstructed BEA 1993 Fixed Asset methodology inputs |

## Divergence From an Earlier Replication

In an earlier replication the raw inventory values were also ~1000× larger; the same normalization applies. The post-2011 proxy is explicitly flagged via the `extension_method` metadata.

## Extension Integrity

Extension must re-fetch the BEA / IRS / FRB component series and re-compute the formula end-to-end; splicing the published series is not permitted. Fetched BEA / FRED responses are cached with a 30-day time-to-live (book-period values are cached permanently).
