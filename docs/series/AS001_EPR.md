# AS001 — GDP/GDI Decomposition and Business NOS (Extension Provenance Record)

**Classification:** extendable_via_component_refetch  **Tolerance for extended values:** 1.0%

## Method

Per the Ch6 GPIM construction pipeline (see `Technical/docs/chapters/CH6_GPIM_SUMMARY.md`) and the Anu Framework anti-degradation rule, **extension does NOT splice the published AS001 values**. Instead, the extension re-fetches the underlying NIPA / BEA Fixed Asset / IRS / Census components and re-runs the formula end-to-end at the current vintage.

1. Fetch BEA NIPA tables via `S00_apis.bea_table` (`BEA_API_KEY` required) using the table ids documented in the dossier `primary_source`.
2. Fetch BEA Fixed Asset T6.1, T6.4, T6.7, T6.8 via the same client.
3. Re-run the construction formula end-to-end.


## Worked Example

For AS001, the Phase 5 round-trip validation reads `AS001_raw.parquet` from the Appendix 6.8 workbook and confirms bit-for-bit reproduction of the published series for the book period 1947-2011. A worked-example year (typically 2009 per book p. 842, or 2011 per Shaikh's last published vintage) verifies headline values.

## No-Proxy Disclosure

No proxies are used in the book period. Book period is fully sourced from primary BEA / IRS / Census; no proxies.

## No-Synthetic Disclosure

No synthetic values, interpolations, or freezes are used. All values are verbatim from Shaikh's posted Appendix 6.8 chopped tables (MD5-verified per `SalvagedInputs/book_data/Reconstructed/BEA_1993_FA_methodology/README.md` for the BEA 1993 staged inputs).

## Failure Mode Table

| Failure | Detection | Response |
|---------|-----------|----------|
| Appendix workbook missing or corrupted | `_ch6_appendix_loader` raises `FileNotFoundError` or empty DataFrame | L01 returns `status: FAIL` with explicit path |
| Variable name not in workbook | `load_variables` returns empty DataFrame | L01 records 0 rows for that subseries; V03 flags as missing |
| BEA / IRS vintage drift during extension | EPR-documented re-fetch script logs vintage_year; V03 tolerance widens for extension rows | Documented per-year; no silent overwrite of book period |
| FISIM T7.11 line revision (AS003) | `_nipa_t711_line_resolver` falls back to nearest pinned vintage with logged warning | Re-mapped by stub label; vintage logged in resolver output |
| BEA 1993 depreciation rate not available post-2011 | AS004/AS006/AS007 freeze depreciation rate inputs at 2011-vintage projection | Documented in `BEA_1993_FA_methodology/README.md` |

## CD2 Divergence Pre-Disclosure

CD2 / RSCD round-trip parity expected within tolerance for the book period. Informational comparison against CD2 per-series CSV when available.

## Anti-Degradation Compliance

Per Anu Framework: extension MUST re-fetch the BEA / IRS / FRB component series and re-compute the formula end-to-end. Splicing the published series is FORBIDDEN. Loader caches BEA / FRED responses per `S00_cache` with 30-day TTL (book-period values: TTL=None).
