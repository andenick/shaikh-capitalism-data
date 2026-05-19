# S803 — Rate of Profit on Equity vs. CR8, Bain 42-Industry Sample, 1936-1940 (Figs 8.3 and 8.4)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S803
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S803_research.json`
- Adequacy: `Technical/docs/chapters/CH8_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S803_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S803`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `BAIN_1951_TABLE_I`, `BAIN_DEMSETZ_CORRECTED_GROUPED`

---

## 1. Definition

**S803** is the single series that consolidates Shaikh's Figures 8.3 and 8.4, both based on Bain (1951, *QJE*, "Relation of Profit Rate to Industry Concentration: American Manufacturing, 1936-1940"). The two panels share the same 42-industry sample:

- **Figure 8.3 (S803-FIG83 scatter)**: 42 (industry, CR8, ROE) triples from Bain 1951 Table I, pp. 309 & 312. ROE = 1936-40 industry-average rate of profit on equity after income taxes; CR8 = proportion of value-product supplied by the top 8 firms in 1935.
- **Figure 8.4 (S803-FIG84 grouped, Bain orig)**: 10 CR8-decile groupings from Bain 1951 Table II, p. 313 (original Bain values).
- **Figure 8.4 (S803-FIG84 grouped, Demsetz corrected)**: 10 CR8-decile midpoints with Demsetz 1973b corrected ROE values (Demsetz 1973b, p. 12). The Demsetz correction is **integral**, not optional; Shaikh's Fig 8.4 uses the corrected version.

`content_type = cross_sectional`: the 42 industry observations are a single 1936-1940 cross-section; Fig 8.4 is the same cross-section re-binned, not a second time point.

Per the playbook recipe (cross_sectional): tolerance 0.5%, no splice, extension N/A.

## 2. Why it matters in Chapter 8

Bain 1951 is the foundational study of the "structure-conduct-performance" (SCP) literature: the central claim is that concentrated industries enjoy persistently higher profit rates. Section II.5 of Chapter 8 (book pp. 373-375) re-runs Bain's regressions on Bain's own data and finds:

- Linear ROE = a + b·CR8: R² = 0.0781 (text p. 374)
- Quadratic: R² = 0.1896, critical CR8* = 49.24 (book regression)
- Corrected decile-grouped: R² = 0.033 (text p. 374; per Demsetz 1973b corrections)

All three regressions are weak; none supports the Bain hypothesis. Shaikh quotes Bain himself: "fit ... is obviously so poor that the inference of a rectilinear or other simple relationship of concentration to profits is not warranted."

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S803-FIG83** | 42 industries, 1936-40 averages | Bain 1951 Table I, QJE 65(3) | CR8 (percent), ROE (percent) | Salvaged chopped `Appendix8_Bain42IndustryProfit.xlsx` |
| **S803-FIG84-BAIN** | 10 CR8 deciles (Bain original) | Bain 1951 Table II, p. 313 | Decile range, n industries, mean ROE (percent) | Salvaged chopped `Appendix8_Bain42IndustryAggregates.xlsx` |
| **S803-FIG84-DEMSETZ** | 10 CR8 midpoints (Demsetz corrected) | Demsetz 1973b, JLE 16(1), p. 12 | CR8 midpoint, mean ROE (percent) | Salvaged chopped `Appendix8_CorrectedBainData.xlsx` |

## 4. Construction

**Composite** in the Anu sense — the series is assembled from multiple non-overlapping source tables.

Per panel:

```
S803-FIG83 (scatter):
  Read Appendix8_Bain42IndustryProfit.xlsx (Sheet1)
  Row 1: industry names (42 cols)
  Row 2: Census number
  Row 3: CR8 1935 value
  Row 4: 1936-40 ROE value
  Emit one obs per industry: (industry_name, census_number, cr8, roe)
  year = 1938 (midpoint label of 1936-40); axis = 'CR8' / 'ROE'

S803-FIG84-BAIN (Bain original deciles):
  Read Appendix8_Bain42IndustryAggregates.xlsx (Sheet1)
  10 rows: (index, CR_lower, CR_upper, n_industries, mean_ROE)
  Emit one obs per decile

S803-FIG84-DEMSETZ (Demsetz corrected):
  Read Appendix8_CorrectedBainData.xlsx (Sheet1)
  10 rows at odd-decile midpoints CR8 in {5, 15, 25, 35, 45, 55, 65, 75, 85, 95}
  Emit one obs per midpoint
```

## 5. Year coverage

- **Book period**: 1936-1940 (Bain ROE averages); CR8 from Census 1935
- **Year label used in chopped CSV**: 1938 (midpoint)
- **Extension period**: not applicable (cross_sectional)

## 6. Units

`percent` (CR8 and ROE both).

## 7. Caveats

1. **Single series ID consolidates two figures.** Per Phase 3 stub `figures = ["Fig8.3", "Fig8.4"]`. The loader emits all three panels under the single S803 id, distinguished by `subseries_id`.
2. **Demsetz correction is integral.** Fig 8.4 in Shaikh uses the corrected values from Demsetz 1973b p. 12, NOT Bain's original Table II values. The loader emits both (`S803-FIG84-BAIN` and `S803-FIG84-DEMSETZ`) so the validator can confirm against the chopped truth. Visualization should use the Demsetz-corrected line as the primary.
3. **Stub-name correction.** Renamed from stale "Interest Rates, Prices, and Equity Data" (CD2 S041 Ch10 carryover). `cd2_id` nulled.
4. **Firm-level micro data not available.** Only the industry-level averages and decile groupings are in chopped tables.
5. **R² values from Shaikh's text** (0.0781 linear, 0.1896 quadratic, 0.033 grouped corrected) are reported in the EPR provenance and can be re-computed from the loaded data for sanity-check in A05 analysis if desired (not required by playbook).

## 8. Cross-references

- **CD legacy ID**: `S041` (predecessor link only; CD2 mismap — S041 is a Ch10 series)
- **CD2 legacy ID**: null
- **Book reference**: Shaikh (2016), Ch. 8, pp. 373-375 (text + Figs 8.3, 8.4)
- **Originating publications**:
  - Bain, J.S. (1951), "Relation of Profit Rate to Industry Concentration," *QJE* 65(3): 293-324. DOI 10.2307/1882217.
  - Demsetz, H. (1973b), "Industry Structure, Market Rivalry, and Public Policy," *JLE* 16(1): 1-9. DOI 10.1086/466752.
- **Shared source with S805** (Demsetz 1973b). Loader for S805 consumes a different Demsetz 1973b table (Table 4).

## 9. Validation expectation

- **Tolerance**: ±0.5% (cross_sectional per playbook).
- Compare loaded long-form values to the corresponding xlsx values on the (subseries, key) join.
- Expected MAE: 0.0 (cells loaded directly from xlsx).
