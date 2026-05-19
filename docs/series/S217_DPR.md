# S217 -- GDP per Capita of World Regions (Maddison), 1600-2000

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S217
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S217_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S217_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S217`

---

## 1. Definition

Maddison (2003) regional per-capita GDP estimates in 1990 International Geary-Khamis dollars, for World + 5 regions (Western Europe, Western Offshoots, Latin America, Asia, Africa).

In Shaikh (2016) the series appears as **Figure 2.17** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Empirical foundation for the chapter's closing 'two-world' argument (~400 years of accelerating divergence between Western Offshoots/Europe and the rest).

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S217-A** | 1600-2000 | Maddison (2003) World | 1990 GK $/cap | salvaged chopped |
| **S217-B** | 1600-2000 | Maddison (2003) Western Europe | 1990 GK $/cap | salvaged chopped |
| **S217-C** | 1600-2000 | Maddison (2003) Western Offshoots | 1990 GK $/cap | salvaged chopped |
| **S217-D** | 1600-2000 | Maddison (2003) Latin America | 1990 GK $/cap | salvaged chopped |
| **S217-E** | 1600-2000 | Maddison (2003) Asia | 1990 GK $/cap | salvaged chopped |
| **S217-F** | 1600-2000 | Maddison (2003) Africa | 1990 GK $/cap | salvaged chopped |

## 4. Construction

`direct` construction.

1. Unpivot wide-format chopped table (rows=region, cols=decade) to long form.
2. Extension: MPD 2023 with 2011 PPP base differs from 1990 GK; regional aggregations also revised. Deferred to manual Phase 9 splice.

## 5. Year coverage

- **Book period**: 1600-2000
- **Extension period**: N/A

## 6. Units

1990 International Geary-Khamis dollars per capita (log scale on figure)

## 7. Caveats

1. MPD 2023 base-year change (1990 GK -> 2011 PPP) creates level discontinuity at splice. Documented in EPR per Phase 4.
2. Decennial pre-1820, annual thereafter.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.17
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
