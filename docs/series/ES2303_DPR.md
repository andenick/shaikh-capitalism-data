# ES2303 — China Official Foreign Exchange Reserves Excluding Gold, 1990–2024

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: ES2303
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-fanout-ES

## 1. Definition

ES2303 is the annual time series of China's official foreign exchange
reserves, **excluding gold**, in current US Dollars. The paper source is
Weber & Shaikh (2020), Appendix Figure 3 (p. 454), which plots the
1990–2016 trajectory as a single dotted line. We extend to 2024.

## 2. Why it matters

Weber & Shaikh use China's reserve accumulation as the empirical anchor
for their critique of the currency-manipulation argument. Section 1
narrates the 17-fold rise from 2000–2010 to a 2013 level of USD 3.6
trillion; Section 3 (p. 438) notes the 2014 peak near USD 4 trillion
and subsequent stabilisation around USD 3 trillion. The series is the
single most-cited empirical fact in the paper's headline narrative.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| ES2303-A | 1990–2024 | World Bank WDI indicator `FI.RES.XGLD.CD` (Total reserves minus gold, current US$) for country `CHN` | current USD | World Bank Data API (`api.worldbank.org/v2/country/CHN/indicator/FI.RES.XGLD.CD?format=json`); no auth; CC-BY-4.0 |

## 4. Construction

Direct pass-through. The WDI series is the canonical source the paper
cites ("Data sourcre: World Bank, 2018" sic on Fig 3). Phase 5 loader
fetches WDI raw via the open Data API, divides by 1e9 to convert
current USD → Billion USD (the paper's plotted unit), and writes one
parquet with columns `year, value, subseries_id='ES2303-A',
source_id='WB_FI_RES_XGLD_CD_CHN', units='billion_usd'`.

## 5. Year coverage

- Paper window: 1990–2016 (27 obs)
- Extension: 2017–2024 (8 obs; subject to WDI release lag)
- Total: 1990–2024 (35 obs)

## 6. Units

Billion current USD. (WDI raw is current USD; loader divides by 1e9.)

## 7. Caveats

1. WDI's `FI.RES.XGLD.CD` sources from IMF International Financial
   Statistics; it excludes gold and excludes sovereign-wealth-fund
   holdings (CIC). Do not substitute `FI.RES.TOTL.CD` (with gold) — the
   paper's figure title is unambiguous "without Gold".
2. WDI release lag: typical 6–12 months from current year-end. If the
   API returns NaN for the most-recent year, the loader propagates
   NaN — no carry-forward.
3. Headline anchors from paper text (p. 433): 17-fold rise 2000→2010
   (WDI: 168 → 2914 bn USD = 17.3x); 2013 ≈ USD 3.6 trillion (WDI: ~3880);
   2014 peak ≈ USD 4 trillion (WDI: ~3843).

## 8. Cross-references

- Dossier: `Technical/research/ES2303_research.json`
- Adequacy: `Technical/docs/chapters/CHES_v2_ADEQUACY_REPORT.json` (5-way split)
- Related: ES2301 (Fig 1 trade balance), ES2302 (Fig 2 CA balance),
  ES2304/ES2305 (literature-compilation Figs 4/5)
- Book chapter ancestor: S1101 (Ch11 trade balances), but distinct
  concept (FX reserves vs trade-balance ratio)

## 9. Validation expectation

- Tolerance: ±1.0% per year against the WDI series values.
- The validator compares the processed parquet against a fresh API pull;
  identity match expected since construction is direct pass-through.
