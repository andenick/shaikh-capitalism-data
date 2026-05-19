# ES2301 — US Trade Balance: World Total and China, 2002–2024

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: ES2301 (rescoped per decision 0006)
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-fanout-ES

## 1. Definition

ES2301 is the annual US merchandise trade balance against **two** trading
partners: (i) World Total; (ii) China. Both in Billion current USD,
Census basis (Total Exports Value − Customs Import Value). Paper source:
Weber & Shaikh (2020), Appendix Figure 1 (p. 453), 2002–2017. We extend
to 2024.

Per Census FT900 footnote convention, both series are negative
throughout the window (US runs a goods-trade deficit). Figure 1 shows
World Total falling from -474 bn (2002) to -810 bn (2017); China line
falling from -103 bn (2002) to -376 bn (2017).

## 2. Why it matters

Figure 1 is the paper's headline: bilateral US-China deficit grew from
"around one-fifth" of total US deficit in 2002 to "about one-third" by
2008 (paper p. 432). The decomposition of the world-total deficit into
the China share is the empirical hook for the currency-manipulation
critique.

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| ES2301-world | 2002–2024 | US Census FT900 Exhibit 1 (US Total goods trade) | Millions USD | Census `foreign-trade/statistics/historical/exh1.txt` |
| ES2301-china | 2002–2024 | US Census FT900 Exhibit 14 / per-country page c5700 | Millions USD | Census `foreign-trade/balance/c5700.html` |

## 4. Construction

For each partner: sum monthly Total Exports Value and Customs Import
Value to annual; compute balance = exports − imports. Convert from
millions to billions for paper-presentation unit.

The loader emits the two partner series as two distinct subseries
(ES2301-world, ES2301-china) with the partner labeled in
`country_key`. The chopped writer disambiguates uniqueness on
`(year, subseries_id, country_key)`.

## 5. Year coverage

- Paper window: 2002–2017 (16 obs per partner)
- Extension: 2018–2024 (7 obs; Section 301 tariffs in 2018-19 create
  structural shift)
- Total: 2002–2024 (23 obs per partner; 46 rows long form)

## 6. Units

`billion_usd` (loader divides by 1000 from millions).

## 7. Caveats

1. Census-basis (Total Exports Value − Customs Import Value) vs
   BoP-basis (BEA International Transactions) differ; paper uses
   Census basis per Fig 1 footnote.
2. Section 301 tariffs (2018-) and COVID (2020) create structural
   breaks in post-paper extension years — interpretive, not data gaps.
3. Census per-country HTML pages have changed layout multiple times;
   if `pd.read_html` cannot parse, loader degrades to NaN and the
   processor publishes only the world-total series.

## 8. Cross-references

- Dossier: `Technical/research/ES2301_research.json` (decision 0006 rescoped)
- Related: ES2302, ES2303, ES2304, ES2305 (other Weber-Shaikh figures);
  S1101 (Ch11 trade balance, different concept)

## 9. Validation expectation

- Tolerance: ±5.0% (Census layout fragility; figure-read precision).
- Anchors from Fig 1: world-total 2002 ≈ -474 bn, 2017 ≈ -810 bn;
  China 2002 ≈ -103 bn, 2017 ≈ -376 bn.
