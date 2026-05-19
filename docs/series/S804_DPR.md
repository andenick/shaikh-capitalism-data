# S804 — Rate of Profit on Assets, Concentrated vs. Unconcentrated Industries, 1939-1957 (Stigler Fig 8.5)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S804
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S804_research.json`
- Adequacy: `Technical/docs/chapters/CH8_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S804_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S804`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `STIGLER_1963_TABLE_17`

---

## 1. Definition

**S804** is Shaikh's Figure 8.5, a reproduction of Stigler (1963, *Capital and Rates of Return in Manufacturing Industries*, Table 17, p. 68): rate of profit on assets (percent) for two industry groups (concentrated, unconcentrated) over six non-overlapping multi-year bins from 1939 to 1957.

Time bins (unequal width): 1939-41, 1942-44, 1945-47, 1948-50, 1951-54, 1955-57.

`content_type = time_series` (per Phase 3 dossier and Phase 4 adequacy ratification). Two subseries, one per industry group. The series is short (6 observations per subseries) and the time bins are unequal, but Shaikh treats it as a time series.

Per the playbook recipe (time_series): tolerance 1.0%.

## 2. Why it matters in Chapter 8

Section II.5 (book p. 376) deploys Stigler's table as the central refutation of the oligopoly-power hypothesis on profit-rate levels. Stigler used profit on **assets** (the theoretically correct measure), unlike Bain who used ROE. The data show:

- Both groups' profit rates move together over the cycle.
- The means are essentially identical: **7.1% (concentrated) vs. 6.9% (unconcentrated)** — book p. 376.
- Concentrated industries display less variation (Stigler 1963, p. 70), which Shaikh attributes to higher fixed/entry costs, not monopoly power.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S804-CONC** | 6 time bins, 1939-1957 | Stigler 1963 Table 17 (concentrated industries column) | Percent | Salvaged chopped `Appendix8_StiglerRatesOfProfit.xlsx` |
| **S804-UNCONC** | 6 time bins, 1939-1957 | Stigler 1963 Table 17 (unconcentrated industries column) | Percent | Salvaged chopped `Appendix8_StiglerRatesOfProfit.xlsx` |

## 4. Construction

**Direct** reproduction. No formula, no splice, no rebase.

```
Load Appendix8_StiglerRatesOfProfit.xlsx (Sheet1, header at row 2):
  Six data rows: time_period in {1939-41, ..., 1955-57}
  Two value columns: Unconcentrated, Concentrated
  Plus an "Average" row (Stigler's overall mean) — NOT loaded into S804;
    it is the *reported* mean used as a sanity check (7.1 / 6.9)
Emit long-form (year, value, subseries_id, source_id, units, bin_start, bin_end)
  year = midpoint of bin (e.g., 1940 for 1939-41), preserved as integer
  bin_start, bin_end = stored as metadata columns for downstream use
```

The midpoint-as-year convention preserves time-series ordering. The unequal-bin metadata is retained as `bin_start` / `bin_end` columns.

## 5. Year coverage

- **Book period**: 1939-1957 (six discrete multi-year bins)
- **Extension period**: not attempted (see EPR §2; per Phase 4 recommendation, treat as historical illustration)
- **Year labels used in chopped CSV**: 1940, 1943, 1946, 1949, 1952.5→1952 (rounded), 1956

## 6. Units

`percent` (rate of profit on assets).

## 7. Caveats

1. **Unequal time-bin widths.** Bins are 3, 3, 3, 3, 4, 3 years; midpoint year is used as the integer index.
2. **The "Average" row in the xlsx** is Stigler's published overall mean (concentrated 7.0667; unconcentrated 6.8917; book reports 7.1 and 6.9 rounded). It is loaded as a sanity-check informational row but is NOT counted as a year observation.
3. **Underlying micro data not in workspace.** Stigler's per-industry rates that feed into the group averages are in the Stigler 1963 NBER monograph appendices, available as freely downloadable NBER PDF (https://www.nber.org/system/files/chapters/c1701/c1701.pdf, confirmed HTTP 200).
4. **No CD2 predecessor.** Stub had `cd_id = S044`, `cd2_id = null`.

## 8. Cross-references

- **CD legacy ID**: `S044`
- **CD2 legacy ID**: null
- **Book reference**: Shaikh (2016), Ch. 8, pp. 375-376 (text + Fig 8.5)
- **Originating publication**: Stigler, G.J. (1963), *Capital and Rates of Return in Manufacturing Industries*. Princeton: Princeton University Press for NBER. Table 17, p. 68. Open-access PDF: https://www.nber.org/books-and-chapters/capital-and-rates-return-manufacturing-industries

## 9. Validation expectation

- **Tolerance**: ±1.0% (time_series per playbook).
- Compare loaded long-form values to the corresponding xlsx cells on the (bin_label, subseries) key.
- Sanity check: computed group means should match Stigler's reported 7.066667 and 6.891667 to four decimal places.
- Expected MAE: 0.0 (cells loaded directly from xlsx).
