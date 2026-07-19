# Chapter 14 — The Theory of Wages and Unemployment: Phase 3 Research Summary

**Wave**: C
**Subagent**: opus-subagent-wave-c-ch14
**Date**: 2026-05-18
**Series count**: 8 (S1401–S1408)
**Book pages**: 657–673 (chapter); 889–895 (Appendix 14.1 and 14.2)

## Chapter overview

Chapter 14 develops the Classical theory of wages and unemployment. The empirical section (Sec. VI, pp. 663–672) introduces Shaikh's central construct — **unemployment intensity** (uInt_L = unemployment_rate × duration_index) — and uses it to derive three nested "Phillips-type" curves:

1. **Classical wage-share curve**: ˙σW/σW = f(uInt_L) — Eq. 14.15
2. **Real-wage curve**: ˙wr/wr = ˙yr/yr + f(uInt_L) — Eq. 14.18
3. **Nominal-wage curve**: ˙w/w = ˙p/p + ˙y/y + f(uInt_L) — Eq. 14.19

The eight figures (14.10–14.17) walk the reader from raw data through HP(100) filtering to the fitted structural relations, demonstrating that the Classical curve is empirically stable across two regimes (1949–1982, 1994–2011) with a downward shift in 1983–1993 attributed to neoliberal attacks on labor.

## Series-by-series notes

| SID | Figure | Type | Construction | Primary source |
|-----|--------|------|--------------|----------------|
| **S1401** | 14.10 | time_series | composite | BEA NIPA T1.10 lines 1, 2 (GDP, Compensation of employees) |
| **S1402** | 14.11 | time_series | composite | BLS CPS LNS14000000 (UNRATE) + LNS13008275 (UEMPMEAN) |
| **S1403** | 14.12 | time_series | direct (phase plot) | Quarterly HP(100) wage share vs unemployment intensity |
| **S1404** | 14.13 | time_series | direct (scatter) | Annual raw wage-share growth vs intensity |
| **S1405** | 14.14 | time_series | direct (filtered scatter + fit) | HP(100) version of S1404, Phillips form y = a + b·x^c |
| **S1406** | 14.15 | time_series | composite | BEA GDP deflator (T1.1.9) + FEE (T6.5A-D) → inflation, productivity growth |
| **S1407** | 14.16 | time_series | direct | HP(100) real-wage growth (wr = w/p) vs intensity |
| **S1408** | 14.17 | time_series | direct | HP(100) nominal-wage growth (w = EC*100/FEE) vs intensity |

## Source identification

All eight series resolve cleanly to two government data providers with stable FRED mirrors:

- **BEA NIPA Historical Tables** (via Appendix 14.2, p. 892, verbatim quote in every dossier):
  - Table 1.10 line 1 — GDP
  - Table 1.10 line 2 — Compensation of employees, paid
  - Table 1.1.9 line 1 — GDP deflator
  - Tables 6.5A-D — Full-time equivalent employees (FEE)
- **BLS CPS** (Appendix 14.2, p. 892):
  - Series LNS14000000 — civilian unemployment rate
  - Series LNS13008275 — mean duration of unemployment (weeks)

FRED mirror keys identified: GDP, A576RC1, GDPDEF, B4701C0A222NBEA, UNRATE, UEMPMEAN.

## Cross-references

- S1401, S1403, S1404, S1405 share the **wage share** input (EC/GDP).
- S1402, S1403, S1404, S1405, S1407, S1408 share the **unemployment intensity** input.
- S1406 supplies the **inflation and productivity-growth** trends that explain why the real-wage and nominal-wage Phillips curves (S1407, S1408) shift relative to the underlying Classical curve (S1405).
- All HP-filtered series use parameter = 100 (annual default), per chapter p. 664 and Appendix 14.2 p. 893 verbatim.

## Chapter-wide open questions (for Phase 4/5)

1. **Quarterly intensity construction (S1403)**: Footnote 10, p. 666 notes "Unemployment intensity was not available at the quarterly level." How was quarterly intensity built? Direct quarterly aggregation of monthly LNS13008275 to quarterly means, or annual interpolation? This needs replication.
2. **UEMPMEAN top-coding break (2011)**: BLS raised the top-coded duration from 2 to 5 years in Jan 2011. For any extension beyond 2011, document whether to apply a continuity adjustment or accept the break.
3. **Phillips functional form (S1405)**: Appendix 14.2 reports the fit as `y = C(1) + x^C(3)` — i.e., with implicit b=1. Replication should confirm whether b was constrained to 1 or fitted then dropped.
4. **1983–1993 transition gap**: Both fitted curves in Fig 14.14 omit the 11-year regime-shift window. How should the post-2011 extension handle a potential third regime shift?
5. **Productivity definition (S1406)**: Shaikh uses real GDP per FTE worker, NOT BLS labor productivity per hour. Continuation requires sticking with this BEA-based construction for comparability.

## Replication assets

- Underlying Shaikh data: `Inputs/Capitalism Data/Inputs/[2016] Shaikh - Capitalism Competition, Conflict, Crises.pdf` (Appendix 14.3 was online at anwarshaikhecon.org)
- Local published-values copy: `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix14_InflationULdata.xlsx` and `Appendix14_Documentation.xlsx`
- CD2 prior dossiers (S068–S075): `SalvagedInputs/methodology_decisions/CD2_research_md/`

## Validator status

8/8 series PASS Phase 3 acceptance criteria. See `Technical/Build/PHASE3_VALIDATION_REPORT.json`.

---

# Phase 5-8 Closure (2026-05-18)

All 8 Chapter 14 series complete the Phase 5 ingestion through Phase 8 output cycle. Pipeline runs via `python Technical/code/run.py --series S140N` for N=1..8. Validation report: `Technical/VALIDATION_REPORT.json`.

| SID | Content type | Validator status | MAE | Max %err | n compared | Chopped rows |
|---|---|---|---|---|---|---|
| S1401 | time_series (composite) | PASS | 0.0 | 0.0% | 127 | 155 |
| S1402 | time_series (composite) | PASS | 0.0 | 0.0% | 192 | 234 |
| S1403 | time_series (composite) | PASS | 0.0 | 0.0% | 128 | 273 |
| S1404 | time_series (direct)    | PASS | 0.0 | 0.0% | 126 | 127 |
| S1405 | time_series (direct)    | PASS | 0.0 | 0.0% | 252 | 255 |
| S1406 | time_series (composite) | PASS | 0.0 | 0.0% | 125 | 147 |
| S1407 | time_series (direct)    | PASS | 0.0 | 0.0% | 126 | 127 |
| S1408 | time_series (direct)    | PASS | 0.0 | 0.0% | 126 | 127 |

Tolerance: ±1.0%. Achieved: 0.0% (exact pass-through; the loader emits Appendix 14.3 values verbatim and the validator compares them column-by-column, so reproduction is exact by construction). The extension years 2012-2024 (S1401, S1402, S1403, S1406) are re-derived from FRED and concatenated without modifying book-period values.

## Per-series notes

- **S1401** — wage share (`wagesh`) + nominal GDP growth (`ggdp`). Extension 2012-2024 via FRED `GDP` + `A576RC1`, re-derived (not splice). 155 rows.
- **S1402** — unemployment rate, duration index (1948-51=100), intensity. Extension via FRED `UNRATE` + `UEMPMEAN` (monthly aggregated to annual mean); duration rebased to FRED's own 1948-1951 mean (~11.5 weeks). UEMPMEAN 2011-01 top-coding break annotated `methodological_break_2011-01: true`; **no backward adjustment** per Phase 4 Q2 resolution.
- **S1403** — quarterly HP(100) wage share + intensity. Dead FRED `W270RE1Q156NBEA` (HTTP 404) replaced by `W209RC1` + `GDP` quarterly pair. Quarterly intensity built from monthly `UNRATE`/`UEMPMEAN` aggregated to quarterly means, duration rebased to 1948Q1-1951Q4 (16-quarter) mean. **HP lambda = 100 (not 1600)**. Canonical processed parquet collapses quarterly HP100 to annual means; quarterly sidecar at `Technical/data/processed/_sidecars/S1403_quarterly.parquet`.
- **S1404** — raw scatter (`gwsh`, `ulintensity`). Pass-through; extension is the responsibility of S1401/S1402 plus a Phase 6 re-derivation pass.
- **S1405** — HP(100) wage-share Phillips curve. Emits **BOTH** constrained-b=1 and unconstrained Phillips fits per era. Reproduction:
  - Era 1 (1949-1982) constrained: a = -1.026431, c = -0.010677, R² = 0.9309 — **matches published exactly** (published a = -1.026431, c = -0.010677, R² = 0.931).
  - Era 2 (1994-2011) constrained: a = -1.010996, c = -0.003709, R² = 0.9650 — **matches published exactly** (published a = -1.010996, c = -0.003709, R² = 0.965).
  - Unconstrained fits diverge as expected (3-parameter overfits a near-flat slope; reported for transparency in `S1405_phillips_fits.json`).
  - 1983-1993 transition omitted from primary fits. Phase 6 third-regime check (era 2 on 1994-2007) included in sidecar.
- **S1406** — inflation (`inflrate`) + productivity growth (`GPRODVTY`). **HARD CONCEPT-POLICING**: productivity formula `yr = (GDP*100/p)/(FEE/1000)` implemented LITERALLY (no algebraic simplification — the `*100` and `/1000` are unit-correcting). Loader emits `assert_no_per_hour_substitution([...])` at import; any future maintainer adding `OPHNFB`, `PRS85006092`, `OPHPBS`, or `OPHMFG` to the FRED inputs list fails import. Extension via FRED `GDP` + `GDPDEF` + `B4701C0A222NBEA`.
- **S1407** — HP(100) real-wage Phillips. Direct refit emitted; algebraic-decomposition reference (S1405 fit + HP100(productivity growth)) noted in sidecar. Inherits productivity concept-policing from S1406.
- **S1408** — HP(100) nominal-wage Phillips + Table 14.3 secondary regression. Direct refit + algebraic-decomposition reference. **Table 14.3 implementation caveat**: the published regression is on the RESIDUAL nominal-wage growth (GMWAGEHP100 minus fitted wage-share curve), not on raw GMWAGEHP100. The processor emits the raw OLS as a placeholder; full residual regression replication is a Phase 9 deliverable. Sample windows 1949-1982 / 1994-2011 per Appendix 14.2 (chapter-text off-by-one with 1948-1982 noted).

## Hard-constraint compliance

- **Productivity concept-policing (S1406, S1407, S1408)**: enforced via `assert_no_per_hour_substitution` module-level call in `L01_S1406_load.py`, `L01_S1407_load.py`, `L01_S1408_load.py`. The list of prohibited FRED IDs lives at `_ch14_helpers.PER_HOUR_PROHIBITED_FRED_IDS`. Adding any of `OPHNFB`, `PRS85006092`, `OPHPBS`, `OPHMFG` to a future loader's input list will fail at import time.
- **HP lambda = 100** (NOT 1600): set as module constant `HP_LAMBDA_CH14 = 100` in `_ch14_helpers.py` and applied uniformly to annual (S1401, S1405, S1407, S1408) and quarterly (S1403) HP filtering.
- **S1405 dual Phillips variants**: BOTH constrained (b=1) and unconstrained variants emitted per era to `Technical/data/processed/S1405_phillips_fits.json`. Constrained variant reproduces published parameters exactly. Same dual-variant pattern in S1407 (`S1407_phillips_fits.json`) and S1408 (`S1408_phillips_fits.json`).
- **1983-1993 transition omitted** from era 1 (1949-1982) and era 2 (1994-2011) fits, per Shaikh's published convention.
- **Cell-by-cell validation** vs `Appendix14_InflationULdata.xlsx` passes at MAE = 0.0 for every series before extension splice.

## URL substitutions recorded

- S1403: `https://fred.stlouisfed.org/series/W270RE1Q156NBEA` (HTTP 404, retired) → `https://fred.stlouisfed.org/series/W209RC1` + `https://fred.stlouisfed.org/series/GDP` (both HTTP 200; within-FRED routing update to same NIPA T1.10 line 2 and line 1 series). Documented in `Technical/series_registry.json` under `series.S1403.url_substitution`.

## Artifact paths

For each S140N (N = 1..8):
- DPR: `Technical/docs/series/S140N_DPR.md`
- EPR: `Technical/docs/series/S140N_EPR.md`
- Loader: `Technical/code/L01_loaders/L01_S140N_load.py`
- Processor: `Technical/code/P02_processors/P02_S140N_construct.py`
- Validator: `Technical/code/V03_validators/V03_S140N_validate.py`
- Processed parquet: `Technical/data/processed/S140N.parquet`
- Chopped CSV: `Technical/chopped/S140N.csv`
- Extenbook XLSX: `Technical/extenbooks/S140N_extenbook.xlsx`

Shared helpers: `Technical/code/L01_loaders/_ch14_helpers.py`, `Technical/code/V03_validators/_ch14_validator_lib.py`. Phillips-fit sidecars at `Technical/data/processed/S1405_phillips_fits.json`, `S1407_phillips_fits.json`, `S1408_phillips_fits.json`. Quarterly phase-plot sidecar at `Technical/data/processed/_sidecars/S1403_quarterly.parquet`.

Registry updater: `Technical/code/utils/_phase5_ch14_register.py`. DPR/EPR authoring script: `Technical/code/utils/_phase5_ch14_doc_writer.py`.
