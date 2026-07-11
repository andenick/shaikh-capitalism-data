# S707 — Figure 7.19 — Greek Manufacturing ROP Deviations, 1962–1991 (Tsoulfidis & Tsaliki 2011 Fig 4)

**Data Provenance Record (DPR)**

**Series ID**: S707
**Status**: book_period_validated
**Authored**: 2026-05-18 · **Recovery update**: 2026-05-26
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S707`
- Subsource registry: subsource registry → `TSOULFIDIS_TSALIKI_2011_FIG4`
- **Digitized source**: reconstructed book source data
- **Extraction report**: Tsoulfidis-Tsaliki extraction worklog

---

## 0. Recovery update (2026-05-26) — supersedes the data_unavailable framing below

The chart-only source was **recovered at digitization fidelity**. The 2011 UoM Discussion-Paper
PDF was indeed dead (HTTP 500), but a **live full-text copy exists on MPRA (paper 51334, 2013
revised version)**. Its Figure 4 — the 20-industry ROP-deviation grid Shaikh reproduces as Fig
7.19 — is **vector-drawn**, so the plotted coordinates were recovered directly from the PDF via
offline vector extraction (no API calls), per-panel y-axis calibrated from each panel's own tick
labels, clipped to Shaikh's 1962–1991 window. Method, validation and caveats:
Tsoulfidis-Tsaliki extraction worklog.

The aggregate Average ROP / Average IROP chart (the 2013 revision's new Figure 5) was extracted
as a **validation anchor** and reproduces the paper's own published moments (footnote 20: mean
0.47 sd 0.10 / mean 0.51 sd 0.27) to ±0.006 — confirming the vector pipeline recovers the
authors' actual data points.

**Status flipped `data_unavailable` → `book_period_validated`.** `provenance: digitized` (NOT the
authors' exact table — that remains obtainable only by author request). §§3–9 below are updated;
the original data_unavailable rationale is retained as historical context where noted.

---

## 1. Definition

**S707** is the exhibit Shaikh displays in Fig7.19 — the deviations of twenty Greek manufacturing
industries' average rates of profit (ROP) from the overall average rate, 1962–1991.

Following the 2026-05-26 recovery (§0), this is a **digitized book-period series**, not a
`data_unavailable` one: the loader (`L01_S707`) reads the digitized panel workbook and emits the
series, the validator (`V03_S707`) round-trips against it, and a chopped CSV is produced. (The
earlier `data_unavailable` handling — loader SKIPPED, validator `PASS_DATA_UNAVAILABLE`, no CSV — no
longer applies; it is retained below only as historical context.)

## 2. Why it matters in Chapter 7

Ch7's empirical case for turbulent profit-rate equalization layers several exhibits: US BEA (S705–S710), the **Greek manufacturing pair (S707/S708)**, OECD STAN (S711), and the Christodoulopoulos (1995) world/US ISDB reconstruction (S703/S704). **S707 is the Greek manufacturing exhibit, not the Christodoulopoulos one** — it is Shaikh's Fig 7.19, *"Deviations of Greek Manufacturing Profit Rates from Average Profit Rate, 1962–1991"*, reproduced from Tsoulfidis & Tsaliki (2011, p.19, fig. 4) (book ref. confirmed). S708 is its incremental-rate companion (Fig 7.20 = Tsoulfidis & Tsaliki 2011 fig. 5). Tsoulfidis & Tsaliki publish these as charts only; the raw 1962–1991 data is no longer recoverable from the workspace but the published figures remain as historical attestation. *(Christodoulopoulos belongs to S703/S704 — a separate exhibit; an earlier draft of this paragraph conflated the two.)*

## 3. Sources

| Subseries | Coverage | Publisher | Status |
|---|---|---|---|
| S707-A (20 industries, digitized) | 1962–1991 | TSOULFIDIS_TSALIKI_2011_FIG4 | **book_period_validated** (provenance: digitized) |

Tsoulfidis & Tsaliki (2011) publish fig. 4 as a chart only — no underlying table — so the authors' exact year-by-year 1962–1991 table is not redistributed. The original University of Macedonia (UoM) Discussion Paper 2011_02 PDF is dead (HTTP 500, confirmed via RePEc/EconPapers), but a live full-text copy survives on MPRA (working paper 51334), and the plotted panel was recovered from it by offline vector digitization (§0). The earlier readiness-review (Phase 4) search — which predates that recovery — recorded the dead-source finding at reconstructed book source data; that note is retained as history and is superseded by the 2026-05-26 recovery. *(The companion note `Christodoulopoulos_1995_data_unavailable.md` covers the separate S703/S704 exhibit, which remains genuinely data_unavailable.)*

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
- **Extension period**: not applicable (no faithful time-extension of the Greek panel; see `S707_EPR.md` §2)

## 6. Units

rate deviation (decimal).

## 7. Caveats

1. **Digitization-grade, not table-exact.** The series was recovered by offline vector digitization of the source figure (§0), so it is faithful to the published chart rather than to the authors' exact underlying table (obtainable only by author request). The published figure remains the authoritative record.
2. **Digitization was performed as the book-period recovery**, using offline PDF vector extraction (no API calls), per-panel y-axis calibration, and clipping to 1962–1991. It is disclosed as `provenance: digitized` and validated against the paper's own aggregate moments (§0); it is a documented recovery of the authors' plotted points, not synthetic infill.
3. **No modern substitute** can splice onto the unredistributed Tsoulfidis & Tsaliki Greek panel without violating the Anti-Degradation rule (industry-mapping drift and the 2010 ESYE→ELSTAT methodology break). Any modern continuation is methodologically separate, not an extension. *(The discontinued OECD-ISDB world/US splice concern belongs to the separate S703/S704 exhibit, not this Greek panel.)*

## 8. Cross-references

- **CD legacy ID**: `S038`
- **Book reference**: Shaikh (2016), Ch. 7 (Fig7.19); Appendix 7.1, sub-sections II / IV (book pp. 856, 859).
- **Recovery documentation**: Tsoulfidis-Tsaliki extraction worklog and the digitized workbook reconstructed book source data (supersedes the earlier `*_data_unavailable.md` marker note, which predates the 2026-05-26 recovery).

## 9. Validation

- **V03 status**: `PASS` (is_deviation_panel; n_compared=600; MAE 0.0; max_pct_err 0.0) — round-trip
  against the digitized panel's `*_Deviation` columns.
- **Registry reference_values** (Decision 0002): subseries `S707-A-20-Food` at 1965/1975/1985 =
  0.0153 / 0.0142 / 0.1106 (tolerance 0.02). Spot anchors read from the digitized figure —
  provenance: digitized, not an independent published table.
- **Fidelity note**: values are digitization-grade. The Fig-5 aggregate validation (§0) is the
  external confidence anchor; the authors' exact panel remains obtainable only by request.

## Notation (plain-language key)

- **ROP** — (average) rate of profit.
- **IROP** — incremental rate of profit: the return on newly added capital (year-to-year change in profit over new investment); the subject of the companion series S708.
- **Deviation** — an industry's rate minus the overall average rate that year; equalisation shows up as deviations crossing zero.
- **Subseries (S707-A)** — a data line within series S707; here S707-A holds the 20-industry digitized panel.
- **ESYE / ELSTAT** — the Greek national statistical service and its post-2010 successor.
- **ISDB** — OECD International Sectoral Database (relevant to the separate S703/S704 exhibit, not this Greek panel).
- **MPRA** — the Munich Personal RePEc Archive, which hosts the full-text source paper (working paper 51334).
- **L01 / V03** — the load and validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset (legacy ID S038).
- **Phase 5 / Phase 6** — Anu pipeline stages: ingestion / extension.
