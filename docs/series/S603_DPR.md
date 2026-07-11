# S603 — Component Ratios x1, x2, x3 (Data Provenance Record)

**Chapter:** Ch6  **Content type:** time_series  **Construction:** formula
***Status**: book_period_validated
## Definition

Component Ratios x1, x2, x3

## Why It Matters

Source figure: Fig 6.3. The ratio x1 is frozen (held, not forward-filled) in any year where corporate net monetary interest (NMINT) from National Income and Product Accounts table 7.11 is incomplete. The book-period values are transcribed verbatim from Shaikh's published Appendix 6.8 (sub-table II.7). See `CH6_GPIM_SUMMARY.md` for the full Chapter 6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| S603-A | II7 | `x1` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S603-B | II7 | `x2` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S603-C | II7 | `x3` | BEA NIPA / BEA FA / IRS SOI / Census | identity |
| S603-D | II7 | `x3*(x1 / x2)` | BEA NIPA / BEA FA / IRS SOI / Census | identity |

The canonical Shaikh-published values are transcribed from book appendix source table*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Decomposition of the corporate profit-rate ratio rcorp/rcorpnipa = (x1/x2) × x3 per Shaikh's eq. 6.11, where x1 = 1 + NMINT/P (net-monetary-interest factor); x2 = 1 + INV[t-1]/KNCbea[t-1] (inventory factor); x3 = KNCbea[t-1]/KGC[t-1] (the ratio of the BEA-valued to the GPIM-valued capital stock). The ratio x1 freezes at the last complete net-monetary-interest year — a known issue carried over unchanged from the predecessor build (CD2), preserved deliberately.

## Year Coverage

Book period: 1947-2011. Vintage-stable extension recipe in `S603_EPR.md`.

## Units

dimensionless_ratio

## Caveats

* The ratio x1 freezes at the last complete corporate net-monetary-interest (NMINT) year; it is held, not forward-filled (behaviour preserved unchanged from the predecessor build, CD2).

## Cross-references

`XS003`, `XS004`, `XS009`

## Validation Expectation

`V03_S603` (the validate script) round-trip-checks the built series against the Appendix 6.8 source workbook at 1.0% tolerance. Per the readiness (adequacy) review (`CH6_ADEQUACY_REPORT.json`), the two ingestion blockers B2 (a National Income and Product Accounts table 7.11 FISIM re-mapping, handled by `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.

## Notation (plain-language key)

- **Subseries (S603-A, -B, …)** — the individual ratio lines that make up series S603.
- **x1 / x2 / x3** — the three decomposition ratios defined in the Construction section above.
- **GPIM** — the corrected capital-stock-and-surplus construction Shaikh uses across Chapter 6 (his integrated measure of the profit rate).
- **NMINT** — net monetary interest.
- **NIPA / BEA** — US National Income and Product Accounts / Bureau of Economic Analysis (KNCbea = the BEA-valued net capital stock).
- **XS003 / XS004 / XS009** — appendix "extra series" recording GPIM construction internals; documentary lineage, not a live computation.
- **L01 / P02 / V03** — the load / process / validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset, retained for cross-checking.
