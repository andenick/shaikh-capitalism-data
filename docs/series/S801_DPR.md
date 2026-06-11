# S801 — Wholesale Prices in Oligopolistic and Competitive Industries, 1965-1973 (Eichner Fig 8.1)

**Data Provenance Record (DPR)**
**Phase**: 5 (Ingestion)
**Series ID**: S801
**Status**: book_period_validated
**Authored**: 2026-05-18 · **Recovery update**: 2026-05-26
**Author**: opus-subagent-ch8-fanout

> **Recovery (2026-05-26):** Recovered from `data_unavailable` by offline vector extraction of Shaikh
> Fig 8.1 (which reproduces Eichner 1973 p.1187) from the book PDF (Oxford print p413, found in Robert's
> `_PDF_LIBRARY`), **overlay-validated against the figure**. Two entities (Oligopolistic, Competitive),
> 1965-1973, index 1957-59=100 — captures the late administered-price divergence (olig→145 vs comp→128.5
> by 1973). `provenance: digitized` (digitization fidelity, not Eichner's exact table). Pipeline:
> L01/P02/V03 (round-trip PASS, n=18, MAE 0.0) → chopped `S801.csv` + extenbook. Source xlsx:
> `SalvagedInputs/book_data/Reconstructed/Eichner_1973_Fig8_1_S801.xlsx`; method:
> `Technical/WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md`. The §§ below predate recovery (historical).
**Related artifacts**:
- Research dossier: `Technical/research/S801_research.json`
- Adequacy: `Technical/docs/chapters/CH8_ADEQUACY_REPORT.json`
- Extension Provenance Record: `Technical/docs/series/S801_EPR.md`
- Registry entry: `Technical/series_registry.json` → `series.S801`
- Subsource registry: `Technical/SUBSOURCE_METADATA.json` → `EICHNER_1973_FIG8_1`

---

> **Reconciliation note (2026-06-11, ch8/9 pass):** Sections 1-9 below were authored when S801 was `data_unavailable` and have been rewritten to the **recovered** state (see the recovery header above). The historical data_unavailable language was internally inconsistent with the recovery header, the populated `chopped/S801.csv`, and the registry status `book_period_validated`.

## 1. Definition

**S801** is Shaikh's Figure 8.1, a reproduction of Eichner (1973, *Economic Journal*, p. 1187): two wholesale-price-index lines (base 1957-59 = 100) for "concentrated" (oligopolistic) vs. "competitive" US industries, annual, **1965-1973**. The series was recovered (2026-05-26) by offline vector extraction of Shaikh's reproduced figure and overlay-validated against it; provenance is `digitized` (digitization fidelity, not Eichner's exact unpublished table).

## 2. Why it matters in Chapter 8

Section II.3 of Chapter 8 ("Price rigidity and monopoly power", pp. 371-373) frames Shaikh's critique of the administered-prices hypothesis. Eichner's chart is the opening exhibit: it shows that concentrated-industry wholesale prices were *smoother* than competitive-industry prices over 1965-1973 (including the Nixon Phase I / Phase II wage-price controls). Shaikh accepts the chart's empirical pattern but rejects the inferential leap to monopoly power, citing Stigler (1963, p. 70): smoother prices in concentrated sectors reflect higher fixed/entry costs, not higher trend profitability.

## 3. Sources

| Subseries | Coverage | Publisher | Status |
|---|---|---|---|
| S801-A-Oligopolistic | 1965-1973 | EICHNER_1973_EJ (via Shaikh Fig 8.1) | book_period_validated |
| S801-A-Competitive | 1965-1973 | EICHNER_1973_EJ (via Shaikh Fig 8.1) | book_period_validated |

Eichner 1973, Economic Journal 83(332), p. 1187 publishes Figure 8.1 as a **chart only**; there is no underlying table in the source publication, and Shaikh (2016, p. 372) transcribes no numeric values in the narrative. Because the chart is the authoritative record, the values were recovered by **offline vector extraction of Shaikh's reproduced figure** (Oxford print p. 413, from Robert's `_PDF_LIBRARY`) and overlay-validated against the figure. Provenance is therefore `digitized`. The recovered source workbook is `SalvagedInputs/book_data/Reconstructed/Eichner_1973_Fig8_1_S801.xlsx`.

## 4. Construction

`construction: direct` (digitized reproduction of Shaikh's chart):
- `L01_S801.py` loads the recovered Eichner_1973_Fig8_1 workbook (two index lines, 1965-1973).
- `V03_S801.py` round-trip validates against the source workbook (PASS, n=18, MAE 0.0).
- Chopped CSV present at `Technical/chopped/S801.csv` (18 rows: 9 years x 2 entities).
- Two entities captured: Oligopolistic (concentrated) reaching ~145 by 1973 vs. Competitive (unconcentrated) reaching ~128.5 — the late administered-price divergence.

## 5. Year coverage

- **Book period**: 1965-1973 (annual, per chart)
- **Extension period**: not applicable (extension would be a proxy substitution; see caveat 3)

## 6. Units

Wholesale price index, base 1957-59 = 100 (per Eichner's chart axis).

## 7. Caveats

1. **Digitized provenance, not Eichner's exact table.** Eichner 1973 published Figure 8.1 as a chart with no underlying table; the published chart (as reproduced by Shaikh) is the authoritative record. The recovered values carry digitization fidelity (overlay-validated), not transcription fidelity.
2. **A BLS PPI reconstruction would be a proxy substitution.** The Adequacy Report's extension_candidates (BLS PPI by NAICS industry, partitioned by Census Concentration Ratios) require SIC->NAICS concordance and re-application of the high-CR / low-CR partition. The set of industries in Eichner's 1965-1973 "concentrated" and "competitive" aggregates is itself unrecoverable, so any modern reconstruction would be a proxy in the Anu sense (formal Concept Match Justification required). Not attempted.
3. **Stub-name correction.** S801 was renamed from the stale "US Long-Run Interest Rates and Prices" (a carryover from CD2 S042, which is a Chapter 10 series). `cd2_id` was nulled in Phase 3.

## 8. Cross-references

- **CD legacy ID**: `S042` (predecessor link; CD2 mismap — CD2 S042 is a Ch10 interest rate series, not a true predecessor for Ch8 Fig 8.1)
- **CD2 legacy ID**: null (no genuine CD2 predecessor)
- **Book reference**: Shaikh (2016), Ch. 8, p. 372 (text + Fig 8.1)
- **Originating publication**: Eichner, Alfred S. (1973), "A Theory of the Determination of the Mark-Up Under Oligopoly," *Economic Journal* 83(332): 1184-1200. DOI: 10.2307/2230843. Wayback fallback confirmed HTTP 200.

## 9. Validation expectation

- **Status**: `PASS` (round-trip against the recovered Eichner_1973_Fig8_1 workbook; n=18, MAE 0.0).
- Provenance flag: `digitized` (figure-overlay validated, not Eichner's unpublished table).
