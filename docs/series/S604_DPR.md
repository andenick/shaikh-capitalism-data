# S604 — Corporate Incremental Rate of Profit (IROP) (Data Provenance Record)

**Chapter:** Ch6  **Content type:** time_series  **Construction:** formula
***Status**: book_period_validated
## Definition

Corporate Incremental Rate of Profit — the incremental rate of profit (IROP), i.e. the return on newly added capital: the year-to-year change in profit divided by the new investment that produced it (as distinct from the *average* rate of profit on the whole existing capital stock).

## Why It Matters

Source figure: Fig 6.7, which has two panels — a nominal panel and a current-cost ("real") panel — and whose four averages are printed in Table 6.24. All four lines are shipped: two nominal (iropcorp, iropcorpnipa) and two current-cost (iroprcorp, iroprcorpnipa). Within each pair, the NIPA-based line (iropcorpnipa / iroprcorpnipa) is the one preferred for extension past 2011, because it has no dependence on net monetary interest (NMINT) or inventory data, which run short. The book-period values are transcribed verbatim from Shaikh's published Appendix 6.8 (sub-table II.7). See `CH6_GPIM_SUMMARY.md` for the full Chapter 6 construction pipeline.

## Sources (per subseries)

| Subseries | Appendix Table | Variable | Source agency | Notes |
|-----------|---------------|----------|---------------|-------|
| S604-A | II7 | `iropcorp` | BEA NIPA / BEA FA / IRS SOI / Census | nominal, corrected |
| S604-B | II7 | `iropcorpnipa` | BEA NIPA / BEA FA / IRS SOI / Census | nominal, NIPA |
| S604-C | II7 | `iroprcorp` | BEA NIPA / BEA FA / IRS SOI / Census | current-cost ("real"), corrected |
| S604-D | II7 | `iroprcorpnipa` | BEA NIPA / BEA FA / IRS SOI / Census | current-cost ("real"), NIPA |

The canonical Shaikh-published values are transcribed from book appendix source table*.xlsx` (Appendix 6.8). Upstream agencies are BEA (NIPA / Fixed Asset Accounts), IRS SOI, U.S. Census Bureau Historical Statistics 1975 (IRS book values), and FRB G.17. All public domain.

## Construction

Four incremental-profit-rate lines across the two panels of Fig 6.7. The two nominal lines (panel 1) are iropcorp = Δ(GOS_corp_adj) / (IG_corpbea + Δ(INV_corp)) and iropcorpnipa = Δ(GOS_corpnipa) / IG_corpbea, where Δ is the year-to-year change, GOS is gross operating surplus, IG is gross investment, and INV is inventories. The two current-cost ("real") lines (panel 2) are the same ratios computed on current-cost-valued surplus and capital (iroprcorp, iroprcorpnipa). Within each pair the NIPA line (iropcorpnipa / iroprcorpnipa) is preferred for extension because it carries no net-monetary-interest or inventory dependency. All four are transcribed verbatim from Appendix 6.8 for the book period; the linked components XS003 / XS004 / XS009 (appendix "extra series" holding the GPIM internals) are recorded as **documentary lineage** per Decision 0015, not a live computation wired into this package.

## Year Coverage

Book period: 1948-2011. Vintage-stable extension recipe in `S604_EPR.md`.

## Units

decimal_rate

## Caveats

* The corrected lines (iropcorp, iroprcorp) are bounded by net-monetary-interest (NMINT) and IRS inventory completeness; the NIPA lines (iropcorpnipa, iroprcorpnipa) are the ones carried forward for post-2011 extension.

## Cross-references

`XS003`, `XS004`, `XS009`

## Validation Expectation

`V03_S604` (the validate script) round-trip-checks the built series against the Appendix 6.8 source workbook at 2.0% tolerance. Table 6.24's printed averages give a non-circular anchor for the four lines' means. Per the readiness (adequacy) review (`CH6_ADEQUACY_REPORT.json`), the two ingestion blockers B2 (a National Income and Product Accounts table 7.11 FISIM re-mapping, handled by `_nipa_t711_line_resolver.py`) and B3 (BEA 1993 depreciation rates, staged at `Reconstructed/BEA_1993_FA_methodology/`) are RESOLVED.

## Notation (plain-language key)

- **IROP / incremental rate of profit** — the return on newly added capital: the year-to-year change in profit divided by the new investment that produced it (contrast with the *average* rate of profit on the whole existing capital stock).
- **Subseries (S604-A … -D)** — the four data lines that make up series S604 (two nominal, two current-cost); each suffix letter is one curve.
- **GOS / IG / INV** — gross operating surplus / gross investment / inventories.
- **GPIM** — the corrected capital-stock-and-surplus construction Shaikh uses across Chapter 6.
- **NMINT** — net monetary interest.
- **NIPA / BEA / FA** — US National Income and Product Accounts / Bureau of Economic Analysis / its Fixed Asset accounts.
- **XS003 / XS004 / XS009** — appendix "extra series" recording GPIM construction internals; documentary lineage, not a live computation.
- **L01 / P02 / V03** — the load / process / validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset, retained for cross-checking.
