# XS009 — IRS Corporate Inventories and Total Capital Stock (Data Provenance Record)

**Chapter:** Ch6  **Content type:** derived  **Construction:** formula
***Status**: book_period_validated
## Definition

IRS Corporate Inventories and Total Capital Stock

## Why It Matters

Source: Shaikh (2016), Appendix Table 6.8.II.6. Unit normalization: the raw IRS Statistics of Income (SOI) inventory line is in thousands of dollars, but Shaikh's Appendix Table 6.8.II.6 column `INVcorp` is already rescaled to billions of current USD; the loader reads that Appendix column with **scale = 1.0 — no division at load time**. An extension flag (`extension_method = 'constant_ratio_proxy_2012_onwards'`) is carried through; a later lift to a re-estimated ratio is recommended but deferred.

> **Correction (2026-07-02, DF-2):** the earlier "divided by 1000 at load time" phrasing was inaccurate — the loader applies scale = 1.0 because the Appendix source column is already in billions. The same "/1000" phrasing in the series-registry `notes`/`params` for XS009 (and the "XS007/XS009 apply /1000" mention) is registry-side and left for the registry owner to reconcile.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| XS009-A | II6 | `INVcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS009-B | II6 | `KGCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| XS009-C | II6 | `KTCcorp` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The `-A`, `-B`, and `-C` suffixes label the individual sub-variants of this series. The canonical Shaikh-published values are transcribed from the published Chapter 6 appendix workbook (Shaikh 2016, Appendix 6.8). Upstream agencies are the Bureau of Economic Analysis (BEA) — its National Income and Product Accounts (NIPA) and Fixed Asset accounts (FA) — the IRS Statistics of Income (SOI), the U.S. Census Bureau Historical Statistics 1975 (IRS book values), and the Federal Reserve Board G.17 release. All public domain.

## Construction

INVcorp = IRS SOI corporate inventories at current cost. KTCcorp = KGCcorp (from XS004) + INVcorp. Raw IRS SOI inventory line is in THOUSANDS OF DOLLARS in the upstream IRS source; Shaikh's Appendix Table 6.8.II.6 column INVcorp is already in billions of current USD after Shaikh's rescaling. Post-2011 inventory is bounded by IRS reporting; constant-ratio proxy flagged via `extension_method: constant_ratio_proxy_2012_onwards`.

## Year Coverage

Book period: 1946-2011. See the companion Extension Provenance Record for the vintage-stable extension recipe.

## Units

billions_current_usd

## Caveats

* Raw IRS SOI inventories in thousands of dollars; INVcorp column in Appendix Table 6.8.II.6 is already rescaled to billions.
* Post-2011 inventory uses constant 2011 ratio proxy; flagged via `extension_method`.

## Cross-references

(none)

## Validation Expectation

The series round-trip-validates against the Appendix 6.8 source workbook at 1.0% tolerance. Two construction dependencies are resolved: the remapping of the NIPA Table 7.11 financial services indirectly measured (FISIM) lines, and the BEA 1993 depreciation rates.
