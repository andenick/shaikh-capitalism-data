# S805 — Rates of Return and Concentration (CR4), 1963 and 1969 (Demsetz Fig 8.6)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S805
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S805_research.json`
- Adequacy: `Technical/docs/chapters/CH8_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S805_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S805`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `DEMSETZ_1973B_TABLE_4`

---

## 1. Definition

**S805** is Shaikh's Figure 8.6, a reproduction of Demsetz (1973b, *Journal of Law and Economics* 16(1), Table 4, p. 19): rate of profit on assets (percent) by CR4 bin, for two years (1963 and 1969). Six CR4 bins × two years = 12 observations.

CR4 bins: 10-20, 20-30, 30-40, 40-50, 50-60, 60+ (percent of value-product supplied by top 4 firms).

`content_type = cross_sectional` (per Phase 3 dossier and Phase 4 adequacy ratification). Two cross-sections (1963, 1969), one per year. The two years are non-adjacent and are not a continuous time index.

Per the playbook recipe (cross_sectional): tolerance 0.5%, no splice, extension N/A.

## 2. Why it matters in Chapter 8

Section II.5 (book pp. 376-377) deploys Demsetz's table as the closing exhibit refuting the Bain-Mann concentration-profitability hypothesis. Shaikh's argument: a weak *positive* relation in 1963 reverses to a weak *negative* relation in 1969. The book quotes: "this lack of temporal correlation between concentration and profit rates is expected in real competition."

Demsetz 1973b is also the source of the **corrections** used in S803 Fig 8.4. The same article supplies two distinct contributions: (a) corrections to Bain's Table II decile grouping (consumed by S803), and (b) Table 4's own 1963/1969 cross-section (consumed by S805). The cross-reference is documented in CH8_RESEARCH_SUMMARY.md.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S805-1963** | 6 CR4 bins, year 1963 | Demsetz 1973b Table 4 (1963 column) | Percent | Salvaged chopped `Appendix8_DemsetzRatesOfReturn.xlsx` |
| **S805-1969** | 6 CR4 bins, year 1969 | Demsetz 1973b Table 4 (1969 column) | Percent | Salvaged chopped `Appendix8_DemsetzRatesOfReturn.xlsx` |

## 4. Construction

**Direct** reproduction. No formula, no splice.

```
Load Appendix8_DemsetzRatesOfReturn.xlsx (Sheet1, header at row 2):
  Six data rows: cr4_bin in {"10-20", "20-30", "30-40", "40-50", "50-60", "60+"}
  Two value columns: 1963, 1969
Emit long-form (year, value, subseries_id, source_id, units, cr4_bin)
  year = 1963 or 1969 (the actual year)
```

## 5. Year coverage

- **Book period**: 1963, 1969 (two discrete cross-sections)
- **Extension period**: not applicable (cross_sectional)

## 6. Units

`percent` (rate of profit on assets) and `percent` (CR4 bin upper bound).

## 7. Caveats

1. **Discrete cross-sections, not time series.** Plotted as two lines vs. CR4, not a continuous time index. Phase 4 confirmed `content_type = cross_sectional`.
2. **CR4 bin labels are string ranges**, not numeric. Stored as `cr4_bin` text column; the loader does NOT collapse to a midpoint (preserving the source representation).
3. **No CD2 predecessor.** Stub had `cd_id = S045`, `cd2_id = null`.
4. **Shared source with S803.** Demsetz 1973b provides both Table 4 (for S805) and the corrections to Bain Table II (for S803 Fig 8.4). The two series consume distinct data tables from the same article.

## 8. Cross-references

- **CD legacy ID**: `S045`
- **CD2 legacy ID**: null
- **Book reference**: Shaikh (2016), Ch. 8, pp. 376-377 (text + Fig 8.6)
- **Originating publication**: Demsetz, H. (1973b), "Industry Structure, Market Rivalry, and Public Policy," *JLE* 16(1): 1-9. Table 4, p. 19. DOI 10.1086/466752.
- **Cross-reference**: S803 also consumes Demsetz 1973b (a different table, p. 12 corrections to Bain).

## 9. Validation expectation

- **Tolerance**: ±0.5% (cross_sectional per playbook).
- Compare loaded long-form values to the corresponding xlsx cells on the (cr4_bin, year) key.
- Expected MAE: 0.0 (cells loaded directly from xlsx).
