# S708 — Figure 7.20 — Greek Manufacturing IROP Deviations, 1962–1991 (Tsoulfidis & Tsaliki 2011 Fig 5)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S708
**Status**: book_period_validated
**Authored**: 2026-05-18 · **Recovery update**: 2026-05-26
**Author**: opus-subagent-ch7-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S708_research.json`
- Adequacy: `Technical/docs/chapters/CH7_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S708_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S708`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `TSOULFIDIS_TSALIKI_2011_FIG5`
- **Digitized source**: `SalvagedInputs/book_data/Reconstructed/Tsoulfidis_Tsaliki_2011_Fig5_S708.xlsx`
- **Extraction report**: `Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md`

---

## 0. Recovery update (2026-05-26) — supersedes the data_unavailable framing below

The chart-only source was **recovered at digitization fidelity** from the live MPRA copy of the
source paper (paper 51334, 2013 revised version). S708 = Shaikh Fig 7.20 = the 2011 paper's Fig 5,
which in the 2013 revision is **Figure 6** (the revision inserted a new aggregate Fig 5). That
20-industry IROP-deviation grid is vector-drawn; coordinates were recovered by offline PDF vector
extraction, per-panel y-calibrated, clipped to 1962–1991. Method/validation:
`Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md`.

**Confidence caveat:** the IROP-deviation series are intrinsically high-frequency, so per-year
digitization fidelity is **lower than S707**. Treat S708 values as approximate (provenance:
digitized). Status flipped `data_unavailable` → `book_period_validated`; the authors' exact panel
remains obtainable only by author request.

---

## 1. Definition

**S708** is the time-series exhibit Shaikh displays in Fig7.20. Period: 1962–1991.

Per the playbook recipe for `content_type = data_unavailable`:

> "DPR + EPR documenting the chart-only source and why no underlying data exists ... L01 returns SKIPPED ... V03 returns PASS_DATA_UNAVAILABLE ... No chopped CSV."

## 2. Why it matters in Chapter 7

Ch7's empirical case for turbulent profit-rate equalization layers several exhibits: US BEA (S705–S710), the **Greek manufacturing pair (S707/S708)**, OECD STAN (S711), and the Christodoulopoulos (1995) world/US ISDB reconstruction (S703/S704). **S708 is the Greek manufacturing incremental-rate exhibit** — Shaikh's Fig 7.20, *"Deviations of Greek Manufacturing Incremental Profit Rates from Average Incremental Rate, 1962–1991"*, reproduced from Tsoulfidis & Tsaliki (2011, p.30, fig. 5). *(Christodoulopoulos belongs to S703/S704 — a separate exhibit; an earlier draft of this paragraph mislabelled S708.)*

## 3. Sources

| Subseries | Coverage | Publisher | Status |
|---|---|---|---|
| S708-A (20 industries, digitized) | 1962–1991 | TSOULFIDIS_TSALIKI_2011_FIG5 | **book_period_validated** (provenance: digitized) |

Recovered by offline PDF vector extraction of MPRA 51334 Figure 6 (= the 2011 paper's Fig 5). The source is chart-only; the authors' exact tabulated panel is not redistributed. (The OECD-ISDB / Christodoulopoulos material belongs to the separate S703/S704 exhibit.)

## 4. Construction

Digitized industry panel (1962–1991, 20 two-digit Greek manufacturing industries):
- `L01_S708` reads the digitized panel xlsx and emits long-form deviations via the shared
  `_ch7_xlsx_panels.deviations_long` (subseries `S708-A-<industry>`).
- `P02_S708` canonicalises the schema via `_ch7_industry_panel_processor` → `data/processed/S708.parquet`.
- `V03_S708` round-trips against the panel's `*_Deviation` columns (`is_deviation=True`): PASS, n=600, MAE 0.0.
- Chopped: `chopped/S708.csv` (long: year, value, subseries_id, source_id, units, industry);
  Extenbook: `extenbooks/S708_extenbook.xlsx`.

## 5. Year coverage

- **Book period**: 1962–1991
- **Extension period**: not applicable (data_unavailable)

## 6. Units

rate deviation (decimal).

## 7. Caveats

1. **No byte-exact reproduction possible** from local materials. The published figure stands as the authoritative record.
2. **PDF digitization** (WebPlotDigitizer) is technically possible but is a Phase 9 visualization task, not a Phase 5 data-ingestion task — and would introduce digitization noise that the No-Synthetic rule discourages for primary data.
3. **No modern substitute** can splice onto the discontinued ISDB / unredistributed T&T panel without violating the Anti-Degradation rule (industry-mapping drift, country-coverage drift, ESYE→ELSTAT methodology break). Any modern continuation is methodologically separate, not an extension.

## 8. Cross-references

- **CD legacy ID**: `S039`
- **Book reference**: Shaikh (2016), Ch. 7 (Fig7.20); Appendix 7.1 II / IV (book pp. 856, 859).
- **B5 provenance document**: see SalvagedInputs/book_data/Reconstructed/ for the relevant `*_data_unavailable.md`.

## 9. Validation

- **V03 status**: `PASS` (is_deviation_panel; n_compared=600; MAE 0.0) — round-trip against the digitized panel.
- **Registry reference_values** (Decision 0002): subseries `S708-A-20-Food` at 1965/1975/1985 =
  0.459 / -0.3014 / -0.3812 (tolerance 0.05, wider than S707 given the high-frequency series).
  Spot anchors from the digitized figure — provenance: digitized.
- **Fidelity note**: digitization-grade and lower-confidence than S707 (high-frequency IROP series);
  not the authors' exact table.
