# S707 — Figure 7.19 — Greek Manufacturing ROP Deviations, 1962–1991 (Tsoulfidis & Tsaliki 2011 Fig 4)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S707
**Status**: book_period_validated
**Authored**: 2026-05-18 · **Recovery update**: 2026-05-26
**Author**: opus-subagent-ch7-fanout
**Related artifacts**:
- Research dossier: `Technical/research/S707_research.json`
- Adequacy: `Technical/docs/chapters/CH7_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S707_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S707`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `TSOULFIDIS_TSALIKI_2011_FIG4`
- **Digitized source**: `SalvagedInputs/book_data/Reconstructed/Tsoulfidis_Tsaliki_2011_Fig4_S707.xlsx`
- **Extraction report**: `Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md`

---

## 0. Recovery update (2026-05-26) — supersedes the data_unavailable framing below

The chart-only source was **recovered at digitization fidelity**. The 2011 UoM Discussion-Paper
PDF was indeed dead (HTTP 500), but a **live full-text copy exists on MPRA (paper 51334, 2013
revised version)**. Its Figure 4 — the 20-industry ROP-deviation grid Shaikh reproduces as Fig
7.19 — is **vector-drawn**, so the plotted coordinates were recovered directly from the PDF via
offline vector extraction (no API calls), per-panel y-axis calibrated from each panel's own tick
labels, clipped to Shaikh's 1962–1991 window. Method, validation and caveats:
`Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md`.

The aggregate Average ROP / Average IROP chart (the 2013 revision's new Figure 5) was extracted
as a **validation anchor** and reproduces the paper's own published moments (footnote 20: mean
0.47 sd 0.10 / mean 0.51 sd 0.27) to ±0.006 — confirming the vector pipeline recovers the
authors' actual data points.

**Status flipped `data_unavailable` → `book_period_validated`.** `provenance: digitized` (NOT the
authors' exact table — that remains obtainable only by author request). §§3–9 below are updated;
the original data_unavailable rationale is retained as historical context where noted.

---

## 1. Definition

**S707** is the time-series exhibit Shaikh displays in Fig7.19. Period: 1962–1991.

Per the playbook recipe for `content_type = data_unavailable`:

> "DPR + EPR documenting the chart-only source and why no underlying data exists ... L01 returns SKIPPED ... V03 returns PASS_DATA_UNAVAILABLE ... No chopped CSV."

## 2. Why it matters in Chapter 7

Ch7's empirical case for turbulent profit-rate equalization layers several exhibits: US BEA (S705–S710), the **Greek manufacturing pair (S707/S708)**, OECD STAN (S711), and the Christodoulopoulos (1995) world/US ISDB reconstruction (S703/S704). **S707 is the Greek manufacturing exhibit, not the Christodoulopoulos one** — it is Shaikh's Fig 7.19, *"Deviations of Greek Manufacturing Profit Rates from Average Profit Rate, 1962–1991"*, reproduced from Tsoulfidis & Tsaliki (2011, p.19, fig. 4) (book ref. confirmed). S708 is its incremental-rate companion (Fig 7.20 = Tsoulfidis & Tsaliki 2011 fig. 5). Tsoulfidis & Tsaliki publish these as charts only; the raw 1962–1991 data is no longer recoverable from the workspace but the published figures remain as historical attestation. *(Christodoulopoulos belongs to S703/S704 — a separate exhibit; an earlier draft of this paragraph conflated the two.)*

## 3. Sources

| Subseries | Coverage | Publisher | Status |
|---|---|---|---|
| S707-A (20 industries, digitized) | 1962–1991 | TSOULFIDIS_TSALIKI_2011_FIG4 | **book_period_validated** (provenance: digitized) |

Tsoulfidis & Tsaliki (2011) publish fig. 4 as a chart only — no underlying table — and the year-by-year 1962–1991 data exists only with the authors. The UoM Discussion Paper 2011_02 hosted PDF is dead (HTTP 500, confirmed via RePEc/EconPapers). No salvaged copy is in `SalvagedInputs`; the Phase 4 B5 search documented this explicitly at `SalvagedInputs/book_data/Reconstructed/Tsoulfidis_Tsaliki_2011_data_unavailable.md` (for S707/S708). *(The companion note `Christodoulopoulos_1995_data_unavailable.md` covers the separate S703/S704 exhibit.)*

## 4. Construction

Digitized industry panel (1962–1991, 20 two-digit Greek manufacturing industries):
- `L01_S707` reads the digitized panel xlsx and emits long-form deviations via the shared
  `_ch7_xlsx_panels.deviations_long` (subseries `S707-A-<industry>`).
- `P02_S707` canonicalises the schema via the shared `_ch7_industry_panel_processor`
  (preserves the `industry` column) → `data/processed/S707.parquet`.
- `V03_S707` round-trips against the panel's `*_Deviation` columns (`is_deviation=True`):
  PASS, n=600, MAE 0.0 (certifies loader/processor fidelity over the digitized source).
- Chopped: `chopped/S707.csv` (long: year, value, subseries_id, source_id, units, industry).
- Extenbook: `extenbooks/S707_extenbook.xlsx`.

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

- **CD legacy ID**: `S038`
- **Book reference**: Shaikh (2016), Ch. 7 (Fig7.19); Appendix 7.1 II / IV (book pp. 856, 859).
- **B5 provenance document**: see SalvagedInputs/book_data/Reconstructed/ for the relevant `*_data_unavailable.md`.

## 9. Validation

- **V03 status**: `PASS` (is_deviation_panel; n_compared=600; MAE 0.0; max_pct_err 0.0) — round-trip
  against the digitized panel's `*_Deviation` columns.
- **Registry reference_values** (Decision 0002): subseries `S707-A-20-Food` at 1965/1975/1985 =
  0.0153 / 0.0142 / 0.1106 (tolerance 0.02). Spot anchors read from the digitized figure —
  provenance: digitized, not an independent published table.
- **Fidelity note**: values are digitization-grade. The Fig-5 aggregate validation (§0) is the
  external confidence anchor; the authors' exact panel remains obtainable only by request.
