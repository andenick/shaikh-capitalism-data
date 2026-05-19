# S218 -- GDP per Capita Richest Four and Poorest Four Countries (Maddison), 1600-2000

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S218
**Status**: ingested
**Authored**: 2026-05-18
**Author**: opus-subagent-wave2-ch2
**Related artifacts**:
- Research dossier: `Technical/research/S218_research.json`
- Adequacy: `Technical/docs/chapters/CH2_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S218_EPR.md`
- Registry entry: `Technical/series_registry.json` -> `series.S218`

---

## 1. Definition

Average GDP per capita of the 4 richest countries and 4 poorest countries at each decennial benchmark, plus the ratio (richest4/poorest4). Shaikh excludes Kuwait/Qatar/Venezuela from the top 4 (1950+).

In Shaikh (2016) the series appears as **Figure 2.18** in Chapter 2 ("The Wealth of Nations: A Long View").

## 2. Why it matters in Chapter 2

Closes the chapter with a stark quantitative measure of global inequality: 40x in 1990, 64x in 2000.

## 3. Sources (per subseries)

| Subseries | Coverage | Publisher / Series ID | Native units | Retrieval |
|---|---|---|---|---|
| **S218-A** | 1600-2000 | Maddison (2003) RICHEST 4 with Shaikh exclusions | 1990 GK $/cap | salvaged chopped |
| **S218-B** | 1600-2000 | Maddison (2003) POOREST 4 | 1990 GK $/cap | salvaged chopped |
| **S218-C** | 1600-2000 | Computed ratio | ratio | salvaged chopped (precomputed) |

## 4. Construction

`formula` construction.

**Formula**: `richest4_avg = mean(top 4 excluding KW/QA/VE); poorest4_avg = mean(bottom 4); ratio = richest4/poorest4`


1. Read precomputed RICHEST 4, POOREST 4, RATIO rows from chopped table.
2. Extension: MPD 2023 requires re-applying the exclusion rule (and possibly adding Macao, Luxembourg). Deferred.

## 5. Year coverage

- **Book period**: 1600-2000
- **Extension period**: N/A

## 6. Units

1990 GK $/cap (levels); ratio (S218-C)

## 7. Caveats

1. Shaikh exclusion rule (Kuwait, Qatar, Venezuela from top 4, 1950+) must be reapplied for MPD 2023.
2. Ratio (S218-C) is base-year-invariant; level series (S218-A/B) require rebasing for MPD 2023 splice.
3. Modern panel may need additional exclusions (Macao, Luxembourg) per anu-framework no-proxy rule.

## 8. Cross-references

- Book reference: Shaikh (2016), Ch. 2, Figure 2.18
- Knowledge Base: `SalvagedInputs/figures_reference/HDARP_SERIES_LINKAGE.json`
- Predecessor (CD2): see registry `predecessor_ids` block.

## 9. Validation expectation

- **Tolerance**: +/- 1.0% per year (per playbook).
- **Expected MAE** (vs salvaged book truth): < 0.5% when source data is pulled directly from the chopped table.
