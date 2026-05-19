# ES2302 — China Current Account Balance, 1997–2024

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: ES2302
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-fanout-ES

## 1. Definition

ES2302 is the annual time series of China's **current account balance**,
in two units: (i) level in Billion current USD; (ii) percent of nominal
GDP. Paper source: Weber & Shaikh (2020), Appendix Figure 2 (p. 453),
dual-axis chart, 1997–2017. We extend to 2024.

## 2. Why it matters

Figure 2 establishes the empirical reversal narrative: China's CA
surplus peaks ~10% of GDP in 2007, then falls sharply to ~1.3% by 2017.
This is the central counter-evidence Weber & Shaikh marshal against
the currency-manipulation hypothesis (Section 1, p. 432).

## 3. Sources

| Subseries | Coverage | Source | Native units | Retrieval |
|---|---|---|---|---|
| ES2302-level | 1997–2024 | IMF WEO subject `BCA` for country `CHN` | Billion current USD | IMF Datamapper JSON API (`imf.org/external/datamapper/api/v1/BCA/CHN`) |
| ES2302-pctgdp | 1997–2024 | IMF WEO subject `BCA_NGDPD` for country `CHN` | Percent of nominal GDP | IMF Datamapper JSON API |

## 4. Construction

Direct pass-through of two distinct WEO subjects for the same country.
Per CHES_v2 D4: **emit as two AnuData rows (ES2302-level and
ES2302-pctgdp), not one mixed-unit series.** The figure plots them on
a dual y-axis (level on left, %-of-GDP on right) precisely because the
units are not commensurable.

## 5. Year coverage

- Paper window: 1997–2017 (21 obs per unit)
- Extension: 2018–2024 (7 obs; WEO publishes April + October vintages)
- Total: 1997–2024 (28 obs per unit; 56 rows total in long form)

## 6. Units

- ES2302-level: `billion_usd`
- ES2302-pctgdp: `percent_of_nominal_gdp`

## 7. Caveats

1. WEO revises historical values each semi-annual vintage. We pin
   `data_vintage_pulled_at` in cache metadata; paper used the 2018
   vintage and a re-pull at any later vintage may shift 1997-2017
   values by 0.1-0.5 percentage points.
2. 2020 (COVID) and 2022 (commodity shock) create interpretable
   structural breaks, not data gaps.
3. The IMF Datamapper API is the documented programmatic interface; if
   it returns 4xx/5xx, fall back to the WEO bulk CSV download.

## 8. Cross-references

- Dossier: `Technical/research/ES2302_research.json`
- Related: ES2301 (Fig 1), ES2303 (Fig 3), ES2304/ES2305 (Figs 4/5)
- Book chapter ancestor: Ch11 (trade balances) — distinct concept
  (current account vs goods balance)

## 9. Validation expectation

- Tolerance: ±1.0% per year.
- Anchors from paper text/figure: 2007-2008 CA level peaks ~USD 420 bn;
  %-of-GDP peaks ~10% in 2007; 2017 value ~1.3-1.7% per paper context.
