# S801 — Wholesale Prices in Oligopolistic and Competitive Industries, 1965-1973 (Eichner Fig 8.1)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S801
**Status**: ingested (with `data_unavailable` extraction status)
**Authored**: 2026-05-18
**Author**: opus-subagent-ch8-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S801_research.json`
- Adequacy: `Technical/docs/chapters/CH8_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S801_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S801`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `EICHNER_1973_FIG8_1`

---

## 1. Definition

**S801** is Shaikh's Figure 8.1, a reproduction of Eichner (1973, *Economic Journal*, p. 1187): two wholesale-price-index lines (base 1957-59 = 100) for "concentrated" vs. "competitive" US industries, monthly/annual, **1965-1973**.

Per the playbook recipe for `content_type = data_unavailable`:

> "DPR + EPR documenting the chart-only source and why no underlying data exists ... L01 returns SKIPPED ... V03 returns PASS_DATA_UNAVAILABLE ... No chopped CSV. Extenbook contains only the DPR + EPR + Source pages. Phase 8 viz uses the book figure image directly."

## 2. Why it matters in Chapter 8

Section II.3 of Chapter 8 ("Price rigidity and monopoly power", pp. 371-373) frames Shaikh's critique of the administered-prices hypothesis. Eichner's chart is the opening exhibit: it shows that concentrated-industry wholesale prices were *smoother* than competitive-industry prices over 1965-1973 (including the Nixon Phase I / Phase II wage-price controls). Shaikh accepts the chart's empirical pattern but rejects the inferential leap to monopoly power, citing Stigler (1963, p. 70): smoother prices in concentrated sectors reflect higher fixed/entry costs, not higher trend profitability.

## 3. Sources

| Subseries | Coverage | Publisher | Status |
|---|---|---|---|
| (none — chart-only) | 1965-1973 | EICHNER_1973_FIG8_1 | **data_unavailable** |

Eichner 1973, Economic Journal 83(332), p. 1187 publishes Figure 8.1 as a chart only. There is no underlying table in the source publication. The Eichner 1973 PDF is not present in `Inputs/` or `Technical/data/raw/01_SOURCE_MATERIALS/` of the RSCD workspace (Phase 5 blocker-resolver searched and confirmed). Shaikh (2016) reproduces the chart on book p. 372 but transcribes no numeric values in the narrative. The `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_*.xlsx` set tabulates Figures 8.2-8.6 but contains no file for Eichner Fig 8.1.

Phase 5 blocker B6 was formally resolved as `data_unavailable` (research dossier review_history entry, 2026-05-18).

## 4. Construction

N/A. No data file exists for the loader to ingest. Per the playbook:
- `L01_S801_load.py` returns `{"status": "SKIPPED", "reason": "data_unavailable"}`.
- `P02_S801_construct.py` is not authored.
- `V03_S801_validate.py` returns `{"status": "PASS_DATA_UNAVAILABLE"}`.
- No chopped CSV at `Technical/chopped/S801.csv`.
- No processed parquet at `Technical/data/processed/S801.parquet`.
- Phase 9 visualization uses the book figure image directly (no digitization in Phase 5).

## 5. Year coverage

- **Book period**: 1965-1973 (annual, per chart)
- **Extension period**: not applicable (data_unavailable; see EPR §1 and §2)

## 6. Units

Wholesale price index, base 1957-59 = 100 (per Eichner's chart axis).

## 7. Caveats

1. **No byte-exact reproduction possible** from local materials. Eichner 1973 published Figure 8.1 as a chart with no underlying table; Shaikh did not transcribe values; the Appendix8_* chopped tables do not include this figure. The published Eichner chart stands as the authoritative record.
2. **WebPlotDigitizer is out of scope for Phase 5.** Even if the Eichner 1973 PDF were obtained from JSTOR (DOI 10.2307/2230843), digitizing the chart would introduce non-trivial sampling noise and would conflict with the Anu No-Synthetic rule for primary data ingestion. Digitization is appropriately constrained as a Phase 9 visualization task (with `provenance: digitized` flagging).
3. **BLS PPI reconstruction would be a proxy substitution.** The Adequacy Report's extension_candidates (BLS PPI by NAICS industry, partitioned by Census Concentration Ratios) require SIC->NAICS concordance and a re-application of the high-CR / low-CR partition. The set of industries in Eichner's 1965-1973 "concentrated" and "competitive" aggregates is itself unrecoverable. Any modern reconstruction would therefore be a proxy in the Anu sense, requiring formal Concept Match Justification in an EPR. Not attempted in Phase 5.
4. **Stub-name correction.** S801 was renamed from the stale "US Long-Run Interest Rates and Prices" (a carryover from CD2 S042, which is a Chapter 10 series). `cd2_id` was nulled in Phase 3.

## 8. Cross-references

- **CD legacy ID**: `S042` (predecessor link; CD2 mismap — CD2 S042 is a Ch10 interest rate series, not a true predecessor for Ch8 Fig 8.1)
- **CD2 legacy ID**: null (no genuine CD2 predecessor)
- **Book reference**: Shaikh (2016), Ch. 8, p. 372 (text + Fig 8.1)
- **Originating publication**: Eichner, Alfred S. (1973), "A Theory of the Determination of the Mark-Up Under Oligopoly," *Economic Journal* 83(332): 1184-1200. DOI: 10.2307/2230843. Wayback fallback confirmed HTTP 200.

## 9. Validation expectation

- **Status**: `PASS_DATA_UNAVAILABLE` (per playbook).
- No tolerance applies; the validator records that no underlying data exists in the workspace and that this is the intended state.
