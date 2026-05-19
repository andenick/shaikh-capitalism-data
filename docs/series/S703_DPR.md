# S703 — Figure 7.13 — World Manufacturing ROP and IROP, 1970–1989 (Christodoulopoulos/ISDB)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S703
**Status**: ingested (with `data_unavailable` extraction status)
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S703_research.json`
- Adequacy: `Technical/docs/chapters/CH7_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S703_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S703`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `CHRISTODOULOPOULOS_1995_FIG7_13`

---

## 1. Definition

**S703** is the time-series exhibit Shaikh displays in Fig7.13. Period: 1970–1989.

Per the playbook recipe for `content_type = data_unavailable`:

> "DPR + EPR documenting the chart-only source and why no underlying data exists ... L01 returns SKIPPED ... V03 returns PASS_DATA_UNAVAILABLE ... No chopped CSV."

## 2. Why it matters in Chapter 7

Ch7's empirical case for turbulent profit-rate equalization layers four exhibits: US BEA (S705-S710), Greek ESYE (S707/S708), OECD STAN (S711), and the **Christodoulopoulos (1995) world/US ISDB reconstruction** (S703 = Fig7.13). The Christodoulopoulos panel is the longest-running multi-country evidence in the chapter; its **raw data is no longer recoverable** but the published figure remains as historical attestation.

## 3. Sources

| Subseries | Coverage | Publisher | Status |
|---|---|---|---|
| (none — chart-only) | 1970–1989 | CHRISTODOULOPOULOS_1995_FIG7_13 | **data_unavailable** |

The underlying OECD ISDB 1994 vintage was discontinued by OECD; Christodoulopoulos' New School working paper was never published and the raw dataset is not in `SalvagedInputs`. The Phase 4 B5 search documented this explicitly at `SalvagedInputs/book_data/Reconstructed/Christodoulopoulos_1995_data_unavailable.md` (for S703/S704) and `SalvagedInputs/book_data/Reconstructed/Tsoulfidis_Tsaliki_2011_data_unavailable.md` (for S707/S708).

## 4. Construction

N/A. No data file exists for the loader to ingest. Per the playbook:
- `L01` returns `{"status": "SKIPPED", "reason": "data_unavailable"}`.
- `P02` is not authored.
- `V03` returns `{"status": "PASS_DATA_UNAVAILABLE"}`.
- No chopped CSV.
- Phase 9 visualization uses the book figure image directly.

## 5. Year coverage

- **Book period**: 1970–1989
- **Extension period**: not applicable (data_unavailable)

## 6. Units

rate (decimal; would be ROP and IROP world-aggregate).

## 7. Caveats

1. **No byte-exact reproduction possible** from local materials. The published figure stands as the authoritative record.
2. **PDF digitization** (WebPlotDigitizer) is technically possible but is a Phase 9 visualization task, not a Phase 5 data-ingestion task — and would introduce digitization noise that the No-Synthetic rule discourages for primary data.
3. **No modern substitute** can splice onto the discontinued ISDB / unredistributed T&T panel without violating the Anti-Degradation rule (industry-mapping drift, country-coverage drift, ESYE→ELSTAT methodology break). Any modern continuation is methodologically separate, not an extension.

## 8. Cross-references

- **CD legacy ID**: `S032`
- **Book reference**: Shaikh (2016), Ch. 7 (Fig7.13); Appendix 7.1 II / IV (book pp. 856, 859).
- **B5 provenance document**: see SalvagedInputs/book_data/Reconstructed/ for the relevant `*_data_unavailable.md`.

## 9. Validation expectation

- **Status**: `PASS_DATA_UNAVAILABLE` (per playbook).
- No tolerance applies; the validator records that no data exists and that this is the intended state.
