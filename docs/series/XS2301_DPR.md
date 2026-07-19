# XS2301 — US Trade Balance: World Total and China, 2002–2024

**Data Provenance Record (DPR)**
**Series ID**: XS2301
**Status**: study_complete
**Authored**: 2026-05-18
**Revised**: 2026-06-11 (truncation repair: loader rebuilt on the Census country pages; coverage now genuinely continuous 2002–2024)

## 1. Definition

XS2301 is the annual US merchandise (goods) trade balance against **two**
trading partners: (i) World Total; (ii) China. Both in Billion current USD,
Census basis (Total Exports Value − Customs Import Value). Paper source:
Weber & Shaikh (2020), Appendix Figure 1 (p. 453), which plots 2002–2017.
We extend the same source forward to 2024.

Per US Census FT900 convention (FT900 is the Census Bureau's monthly
foreign-trade statistics report), both series are negative throughout the window
(the US runs a goods-trade deficit). The constructed Census series reproduces
the paper's Figure 1 endpoints to within figure-read precision: World Total
2002 = -468.3 bn (paper figure-read ≈ -474), 2017 = -792.4 bn (≈ -810);
China 2002 = -103.1 bn (≈ -103), 2017 = -375.2 bn (≈ -376).

## 2. Why it matters

Figure 1 is the paper's headline: the bilateral US-China deficit grew from
"around one-fifth" of the total US deficit in 2002 to "about one-third" by
2008 (paper p. 432). Decomposing the world-total deficit into the China share
is the empirical hook for the paper's currency-manipulation critique.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| XS2301-world | 2002–2024 | US Census FT900, All-countries goods balance page (c0004) | Millions USD | `census.gov/foreign-trade/balance/c0004.html` |
| XS2301-china | 2002–2024 | US Census FT900, China goods balance page (c5700) | Millions USD | `census.gov/foreign-trade/balance/c5700.html` |

Both pages are public, key-free HTML and carry one `TOTAL {YYYY}` annual row
per year-table (Exports / Imports / Balance, current USD millions, Census
basis). This is the same source family the paper used for Figure 1.

## 4. Construction

For each partner, read the `TOTAL {YYYY}` annual rows from the Census country
page; take the published annual Balance (millions USD), and divide by 1000 to
present in Billion USD. The two partners are emitted as two subseries —
`XS2301-world` and `XS2301-china` (the suffix after the series id names the
trading partner) — with each observation labelled by its partner and year.

## 5. Year coverage

- Paper window (plotted in Fig 1): 2002–2017 (16 obs per partner)
- Continued from the same source: 2018–2024 (7 obs; Section 301 tariffs in
  2018-19 and COVID in 2020 create structural shifts — interpretive, not data
  gaps)
- **Total: 2002–2024 — 23 obs per partner, 46 rows long form, genuinely
  continuous (no missing years).**

## 6. Units

`billion_usd` (loader divides the Census millions figure by 1000).

## 7. Caveats

1. Census-basis (Total Exports Value − Customs Import Value) differs slightly
   from BoP-basis (balance-of-payments basis, US Bureau of Economic Analysis
   (BEA) International Transactions); the paper uses Census
   basis per the Fig 1 footnote, which is what these pages publish.
2. Section 301 tariffs (2018-) and COVID (2020) create structural breaks in
   the post-paper years — interpretive, not data gaps.
3. The world-total figure-read endpoints in the paper (-474 in 2002, -810 in
   2017) are eyeballed off the appendix chart; the constructed Census source
   values (-468.3, -792.4) differ by 1.2–2.2%, well within the ±10% validator
   tolerance. The China endpoints match the paper to <1%.

## 8. Revision history — truncation repair (2026-06-11)

The earlier loader attempted a fragile Census scrape that keyed annual figures
off a four-digit *column header* that does not exist on the country pages (the
year lives in the `TOTAL {YYYY}` Month cell). The scrape therefore always
failed and the series silently degraded to the five salvaged Fig-1 *anchor*
points (World 2002/2017; China 2002/2017/2018), which truncated the series at
2018 and were figure-reads rather than source data — while the DPR claimed
continuous coverage to 2024.

The loader was rebuilt to read the `TOTAL {YYYY}` rows directly from the
Census World (c0004) and China (c5700) country pages. Result: 23 real annual
observations per partner, 2002–2024, no fabrication, no interpolation.
Validation PASS (4/4 anchors matched, max 2.17% error). The verbatim Figure 1
anchors are retained only as a per-partner last-resort fallback if a page
fetch fails.

## 9. Cross-references

- Related: XS2302, XS2303, XS2304, XS2305 (other Weber-Shaikh figures);
  S1101 (Ch11 trade balance, different concept)

## 10. Validation expectation

- Tolerance: ±10% (figure-read precision on the World endpoints; Census
  periodic revisions can shift historical totals 1–3%).
- Anchors from Fig 1: world-total 2002 ≈ -474 bn, 2017 ≈ -810 bn;
  china 2002 ≈ -103 bn, 2017 ≈ -376 bn. All satisfied (see §1).
