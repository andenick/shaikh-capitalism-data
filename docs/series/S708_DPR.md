# S708 — Figure 7.20 — Greek Manufacturing IROP Deviations, 1962–1991 (Tsoulfidis & Tsaliki 2011 Fig 5)

**Data Provenance Record (DPR)**

**Series ID**: S708
**Status**: book_period_validated
**Authored**: 2026-05-18 · **Recovery update**: 2026-05-26
**Author**: Anu Framework pipeline
**Related artifacts**:
- Research dossier: research dossier
- Adequacy: chapter adequacy report
- Extension Provenance Record: extension provenance record
- Registry entry: series registry → `series.S708`
- Subsource registry: subsource registry → `TSOULFIDIS_TSALIKI_2011_FIG5`
- **Digitized source**: reconstructed book source data
- **Extraction report**: Tsoulfidis-Tsaliki extraction worklog

---

## 0. Recovery update (2026-05-26) — supersedes the data_unavailable framing below

The chart-only source was **recovered at digitization fidelity** from the live MPRA copy of the
source paper (paper 51334, 2013 revised version). S708 = Shaikh Fig 7.20 = the 2011 paper's Fig 5,
which in the 2013 revision is **Figure 6** (the revision inserted a new aggregate Fig 5). That
20-industry IROP-deviation grid is vector-drawn; coordinates were recovered by offline PDF vector
extraction, per-panel y-calibrated, clipped to 1962–1991. Method/validation:
Tsoulfidis-Tsaliki extraction worklog.

**Confidence caveat:** the IROP-deviation series are intrinsically high-frequency, so per-year
digitization fidelity is **lower than S707**. Treat S708 values as approximate (provenance:
digitized). Status flipped `data_unavailable` → `book_period_validated`; the authors' exact panel
remains obtainable only by author request.

---

## 1. Definition

**S708** is the exhibit Shaikh displays in Fig7.20 — the deviations of twenty Greek manufacturing
industries' incremental rates of profit (IROP, the return on newly added capital) from the overall
average incremental rate, 1962–1991.

Following the 2026-05-26 recovery (§0), this is a **digitized book-period series**, not a
`data_unavailable` one: the loader (`L01_S708`) reads the digitized panel workbook and emits the
series, the validator (`V03_S708`) round-trips against it, and a chopped CSV is produced. (The
earlier `data_unavailable` handling — loader SKIPPED, validator `PASS_DATA_UNAVAILABLE`, no CSV — no
longer applies; it is retained below only as historical context.)

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
- **Extension period**: not applicable (no faithful time-extension of the Greek panel; see `S708_EPR.md` §2)

## 6. Units

rate deviation (decimal).

## 7. Caveats

1. **Digitization-grade, not table-exact.** The series was recovered by offline vector digitization of the source figure (§0), so it is faithful to the published chart rather than to the authors' exact underlying table (obtainable only by author request). Because the incremental-rate curves are high-frequency, per-year precision is lower than the average-rate panel (S707). The published figure remains the authoritative record.
2. **Digitization was performed as the book-period recovery**, using offline PDF vector extraction (no API calls), per-panel y-axis calibration, and clipping to 1962–1991. It is disclosed as `provenance: digitized`; it is a documented recovery of the authors' plotted points, not synthetic infill.
3. **No modern substitute** can splice onto the unredistributed Tsoulfidis & Tsaliki Greek panel without violating the Anti-Degradation rule (industry-mapping drift and the 2010 ESYE→ELSTAT methodology break). Any modern continuation is methodologically separate, not an extension. *(The discontinued OECD-ISDB world/US splice concern belongs to the separate S703/S704 exhibit, not this Greek panel.)*

## 8. Cross-references

- **CD legacy ID**: `S039`
- **Book reference**: Shaikh (2016), Ch. 7 (Fig7.20); Appendix 7.1, sub-sections II / IV (book pp. 856, 859).
- **Recovery documentation**: Tsoulfidis-Tsaliki extraction worklog and the digitized workbook reconstructed book source data (supersedes the earlier `*_data_unavailable.md` marker note, which predates the 2026-05-26 recovery).

## 9. Validation

- **V03 status**: `PASS` (is_deviation_panel; n_compared=600; MAE 0.0) — round-trip against the digitized panel.
- **Registry reference_values** (Decision 0002): subseries `S708-A-20-Food` at 1965/1975/1985 =
  0.459 / -0.3014 / -0.3812 (tolerance 0.05, wider than S707 given the high-frequency series).
  Spot anchors from the digitized figure — provenance: digitized.
- **Fidelity note**: digitization-grade and lower-confidence than S707 (high-frequency IROP series);
  not the authors' exact table.

## Notation (plain-language key)

- **IROP** — incremental rate of profit: the return on newly added capital (year-to-year change in profit over new investment), as distinct from the average rate of profit on the whole existing stock.
- **Deviation** — an industry's rate minus the overall average rate that year; equalisation shows up as deviations crossing zero.
- **Subseries (S708-A)** — a data line within series S708; here S708-A holds the 20-industry digitized panel.
- **ESYE / ELSTAT** — the Greek national statistical service and its post-2010 successor.
- **ISDB** — OECD International Sectoral Database (relevant to the separate S703/S704 exhibit, not this Greek panel).
- **MPRA** — the Munich Personal RePEc Archive, which hosts the full-text source paper (working paper 51334).
- **L01 / V03** — the load and validate scripts that build and check the series.
- **CD2** — the predecessor build of this dataset (legacy ID S039).
- **Phase 5 / Phase 6** — Anu pipeline stages: ingestion / extension.
