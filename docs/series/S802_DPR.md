# S802 — Percentage of Prices Increases or No Decreases during Contractions, in Relation to Concentration (Fig 8.2)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S802
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S802_research.json`
- Adequacy: `Technical/docs/chapters/CH8_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S802_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S802`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `SEMMLER_1984_TABLE_3_3`

---

## 1. Definition

**S802** is Shaikh's Figure 8.2, a reproduction of the cross-sectional summary by Weston, Lustgarten, and Grottke (1974), as tabulated by Semmler (1984, *Competition, Monopoly, and Differential Profit Rates*, Table 3.3, p. 95). It records, for each of three NBER-dated US contractions, the percentage of firms in each of three CR4 concentration bins (midpoints 20, 50, 80) whose wholesale prices increased or stayed stable during the contraction.

`content_type = cross_sectional`: each contraction is its own industry cross-section binned by CR4 midpoint; the three contractions are not a continuous time index. Per the playbook recipe:

> "L01: fetch the single-year benchmark from book/source ... P02: emit as single-year row(s); no splice ... V03: compare against book values ... Extension: explicitly `not_applicable_cross_sectional` ... chopped CSV is short (one or few rows) ... Tolerance 0.5%"

## 2. Why it matters in Chapter 8

Section II.3 (book p. 372) deploys this table to refute the administered-prices prediction. Under the administered-prices hypothesis, high concentration should inhibit price falls in recessions (positive concentration-rigidity coefficient). But the Weston et al. data show the sign flips across contractions: positive in 1957-58, negative in 1960-61, ~neutral in 1969-70 — exactly the temporal instability Shaikh's real-competition framework predicts.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S802-C1957** | 1957-07 / 1958-04 | Weston, Lustgarten & Grottke 1974, AER, via Semmler 1984 Table 3.3 | Percent of firms with price increases or no decreases | Salvaged chopped table `Appendix8_Semmler19843.3.xlsx` |
| **S802-C1960** | 1960-01 / 1961-01 | (same) | (same) | (same xlsx) |
| **S802-C1969** | 1969-11 / 1970-11 | (same) | (same) | (same xlsx) |

Each subseries contains three observations (one per CR4 midpoint = 20, 50, 80).

## 4. Construction

**Direct** reproduction. No formula, no splice.

```
Load Appendix8_Semmler19843.3.xlsx (Sheet1, header at row 2):
  CR4_midpoint in {20, 50, 80}
  for each of three contractions: read percent of firms with price increase / no decrease
Emit as long-form (year = contraction-start year, cr4_midpoint, value, subseries_id)
```

Single observation per (cr4_midpoint, contraction). Total = 9 observations.

## 5. Year coverage

- **Book period**: three discrete cross-sections at NBER-dated peaks 1957, 1960, 1969 (using contraction-start year as the year label)
- **Extension period**: not applicable (cross_sectional)

## 6. Units

`percent` (firms-with-price-increase-or-no-decrease share) and `percent` (CR4 midpoint).

## 7. Caveats

1. **Discrete cross-sections, not time series.** Plotted as three lines vs. CR4, not a continuous time index. Phase 4 confirmed `content_type = cross_sectional`.
2. **Firm-level micro data not available** in Shaikh's chopped tables; only the 3×3 summary grid is digitized.
3. **No CD2 predecessor** — Ch8 has no CD2 dossiers; the stub had a `cd_id` (S043) but no `cd2_id`.

## 8. Cross-references

- **CD legacy ID**: `S043` (predecessor link only)
- **CD2 legacy ID**: null
- **Book reference**: Shaikh (2016), Ch. 8, p. 372 (text + Fig 8.2)
- **Originating publication**: Weston, Lustgarten & Grottke (1974), "The Administered Price Thesis Denied: Note," *American Economic Review* 64(1): 232-234. Reprinted in Semmler (1984), *Competition, Monopoly, and Differential Profit Rates*, Table 3.3.

## 9. Validation expectation

- **Tolerance**: ±0.5% (cross_sectional per playbook).
- Compare loaded long-form values to the values in `Appendix8_Semmler19843.3.xlsx` on the (cr4_midpoint, contraction) key.
- Expected MAE: 0.0 (cells loaded directly from xlsx).
