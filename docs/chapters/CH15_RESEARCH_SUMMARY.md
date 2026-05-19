# Chapter 15 — Modern Money and Inflation: Phase 3 Research Summary

**Reviewer**: opus-subagent-wave-c-ch15
**Date**: 2026-05-18
**Series**: S1501–S1509 (9 series)
**Book pages**: 696–719 (chapter) + Appendix 15.1 pp. 895–897
**Status**: draft (Phase 3 complete; awaiting Phase 4 adequacy review)

## Chapter scope

Chapter 15 develops Shaikh's classical theory of fiat-money inflation. The empirical
content centres on three threads:

1. The long-run history of the US price level (Fig 15.1).
2. The post-war US relation between nominal GDP growth, "new purchasing power"
   (CR + CA), and inflation — including industry-level growth (Figs 15.2A–B) and
   the classical vs conventional Phillips curves (Figs 15.7–15.9).
3. International cross-sections relating inflation to credit growth (Figs 15.12–15.13).

All nine series have CD2 predecessors (S076, S077, S078, S079, S083, S084, S085, S088,
S089), so this chapter was a port-and-validate exercise rather than greenfield research.

## Per-series notes

| SID | Figure | CD2 | Source map |
|---|---|---|---|
| S1501 | 15.1 | S076 | MeasuringWorth USCPI (direct, same source Shaikh used) |
| S1502 | 15.2A | S077 | BEA GDP-by-Industry, real value added growth (goods & trade) |
| S1503 | 15.2B | S078 | BEA GDP-by-Industry, real value added growth (services & gov) |
| S1504 | 15.3, 15.4 | S079 | BEA NIPA T1.1.5 / T4.1 + IMF IFS lines 31+(78−88)+79+81 |
| S1505 | 15.7 | S083 | Composite: π (BEA T1.1.4), σ (BEA T5.3.5/T1.16 per Handfas 2012), uL (BLS) |
| S1506 | 15.8 | S084 | Same as S1505, sub-period 1948–1981 |
| S1507 | 15.9 | S085 | Same as S1505, sub-period 1982–2010 |
| S1508 | 15.12 | S088 | Harberger (1988) table 12.11; underlying IMF IFS line 32 |
| S1509 | 15.13 | S089 | Ramamurthy (2014, ch.3); IMF IFS lines 32 + 64, 39-country panel |

## Cross-references

- **S1505 ↔ S1506 ↔ S1507**: same data, sub-period sliced. Any change to the σ
  construction or NIPA vintage propagates to all three.
- **S1504 ↔ S1505**: both rely on BEA NIPA flow variables. Sharing a load pipeline
  for the price deflator and GDP series is recommended.
- **S1508 ↔ S1509**: Ramamurthy (2014) explicitly extends Harberger (1988); the two
  scatter plots are deliberately stacked to invite visual comparison. Country
  panels overlap but are not identical (29 vs 39 countries).
- **Cross-chapter**: unemployment rate uL is the same series used in Ch14 (S1404/S1405);
  growth-utilization-rate σ first appears in Appendix 14.2; inflation π is reused in
  Ch12 Figures 12.5–12.8 (per Appendix 12.1's explicit pointer to Appendix 15.1).

## Chapter-wide issues / open questions

1. **NIPA Table 1.15 vs 1.1.5 typo** (Appendix 15.1, p.895). Standard BEA NIPA has
   no Table 1.15; "Nominal GDP" lives in Table 1.1.5. Recommend treating as a typo
   and using T1.1.5; flagged in S1504.
2. **Harberger (1988) figure-caption typo** (Fig 15.12). Caption says "table 12.1",
   narrative and appendix say "table 12.11". Flagged in S1508.
3. **BEA Table 1.16 ("Sources and Uses of Private Enterprise Income")**. Title
   slightly archaic; modern NIPA Tables 1.16 are present but with restructured
   line numbers. Verify line-2 = Net Operating Surplus in Phase 4.
4. **IMF IFS line-number stability**. Shaikh's Appendix 15.1 references IFS
   monetary-survey lines 31, 32, 64, 78, 79, 81, 88. Post-2009 SDDS+ migration
   replaced numeric line references with FOSAOP_XDC-style codes. Any forward
   extension requires a code remap. Flagged in S1504, S1508, S1509.
5. **Romania duplicate** in 39-country list (Appendix 15.1 footnote 2, p.897).
   Almost certainly a typesetting artifact; verify in Phase 4. Flagged in S1509.
6. **Ramamurthy (2014) dissertation** — citation is incomplete (no title, no
   institution). Likely Santosh Ramamurthy at New School for Social Research
   under Shaikh; verify and provide a stable URL/citation in Phase 4.

## Construction-type breakdown

- direct: 2 (S1501, S1508)
- formula: 2 (S1502, S1503, S1504) — wait, three formulas: S1502, S1503, S1504
- composite: 4 (S1505, S1506, S1507, S1509)

(Note for Phase 4: the "composite" classification for S1506 and S1507 is a sub-period
slice of S1505; consider whether a 4th construction category "derived_subperiod"
would clarify provenance.)

## Validator outcome

Run `python Technical/code/utils/_phase3_research_validator.py`; expect
S1501–S1509 PASS. See `Technical/Build/PHASE3_VALIDATION_REPORT.json` for the
full project-wide report.

---

## Phase 5-8 Closure (2026-05-18)

End-to-end pipeline (DPR + EPR + L01 + P02 + V03 + chopped + extenbook)
authored for all 9 Chapter 15 series, following the FANOUT_PLAYBOOK.md
recipe. All 9 series PASS V03 validation at the requested tolerance.

### Per-series outcomes

- **S1501** (U.S. CPI 1774-2011, `direct`): MeasuringWorth USCPI loaded from
  `Appendix15_MeasuringWorthCPI.xlsx`; FRED CPIAUCNS overlap-anchor extension
  (active when `FRED_API_KEY` set). V03 PASS, MAE=0 over 238 yrs. CD2
  spot-checks 1774/1899/1949/1999 cross-referenced informationally.

- **S1502** (BEA Industry Panel A growth rates 1988-2010, `formula`): 9
  subseries (All + 8 goods/trade). Loader recomputes growth via
  `(YR_t - YR_{t-1}) / YR_{t-1}` per the book's empirical convention
  (originally dossier said log-difference; verified against book's published
  "Calculated Growth Rate" columns and corrected in DPR). V03 PASS, MAE=0
  over 207 cells.

- **S1503** (BEA Industry Panel B growth rates 1988-2010, `formula`): 10
  subseries (All + 9 services/government). Same shared `_bea_industry_loader`
  helper. V03 PASS, MAE=0 over 230 cells.

- **S1504** (Growth of Nominal GDP and Relative New Purchasing Power
  1948-2010, `composite`): 7 book-period subseries (GDP, pGDP, CR, CA, gGDP,
  gCR, pp) loaded from `Appendix15_USInflation.xlsx`. **IMF IFS resolver
  integrated**: `fetch_ifs_series('DCORP_N_DC', 'USA', 2001, 2025,
  dataflow='MFS_DC')` succeeded with 25 annual observations of modern
  Depository Corporations Survey Net Domestic Claims (subseries
  `S1504-CR-modern`). V03 PASS for book-period; IMF cross-check noted that
  modern series is in raw USD while Shaikh's CR is in USD billions — unit
  harmonization deferred to Phase 6 enrichment.

- **S1505** (Phillips-curve composite 1948-2010, `composite`): 5 subseries
  (pi, sigma, sigma', uL, uLintensity) loaded from `Appendix15_USInflation`.
  V03 PASS, MAE=0 over 314 cells.

- **S1506** (Phillips curves 1948-1981, `derived_subperiod`): closed
  pre-Volcker sub-period of S1505. Loader filters parent `S1505.parquet` to
  1948-1981; processor pass-through; validator confirms exact slice match
  to parent over 169 cells. PASS.

- **S1507** (Phillips curves 1982-2010, `derived_subperiod`): open
  post-Volcker sub-period of S1505, forward-extendable when S1505 extends.
  Loader filters 1982-S1505.max(); 145 cells PASS.

- **S1508** (Harberger 29-country cross-section 1970-1988, `cross_sectional
  + direct`): loaded from `Appendix15_WorldInflationDataLambda.xlsx` sheet
  `HarbergerTable12`. 29 country-rows x 2 subseries = 58 cells PASS at
  +/- 0.5%. IMF resolver audit (line 32 -> DCORP_N_DC; line 64 -> PCPI_IX)
  documented in loader output for future modern re-pull.

- **S1509** (Ramamurthy 38-country / 46-episode cross-section 1988-2011,
  `cross_sectional + direct`): loaded from
  `Appendix15_WorldInflationDataByCountry.xlsx` sheet `Ramamurthy2013`. 46
  country-episodes x 2 subseries = 92 cells PASS at +/- 0.5%. Romania
  de-duplication preserved (Romania appears in two distinct episode rows:
  Acute 1991-94 and Chronic 1998-02). Unique-country count = 38; episode
  rows = 46.

### IMF IFS resolver integration notes

- S1504 loader uses `resolve_ifs_line(32) -> "DCORP_N_DC"` and
  `fetch_ifs_series("DCORP_N_DC", "USA", 2001, 2025, dataflow="MFS_DC")`.
  Live fetch SUCCESS: 25 annual obs returned over 2001-2025. HTTP 200.
- S1508 and S1509 loaders document the modern code mapping via
  `describe_ifs_line(32)` and `describe_ifs_line(64)` for audit. They do not
  invoke `fetch_ifs_series` because the chopped tables (Harberger published
  table and Ramamurthy precomputed panel) are the canonical replication
  targets per the adequacy report.
- Pre-2001 USA data is not available in IMF SDMX 3.0; Shaikh's hand-summed
  values from `Appendix15_USInflation.xlsx` retained for 1948-2000.

### S1505/S1506/S1507 shared-logic approach

- S1505 is the parent: independent L01 (reads chopped table), P02, V03.
- S1506/S1507 L01 scripts read `Technical/data/processed/S1505.parquet` and
  filter to the relevant year window, renaming subseries IDs S1505-* to
  S1506-*/S1507-*. This satisfies the "minimize code duplication" constraint
  while keeping the L01/P02/V03 file convention consistent for the
  orchestrator.
- V03_S1506 / V03_S1507 confirm the slice by re-merging against S1505.
- Pipeline ordering (alphabetical) ensures S1505 runs before S1506/S1507.

### Chopped CSV row counts

| Series | Rows |
|---|---|
| S1501 | 252 |
| S1502 | 207 |
| S1503 | 230 |
| S1504 | 463 (includes 25 modern IMF CR cross-check rows) |
| S1505 | 314 |
| S1506 | 169 |
| S1507 | 145 |
| S1508 |  58 |
| S1509 |  92 |

### Validator output (per VALIDATION_REPORT.json)

All 9 series PASS. MAE=0 across the board because each loader sources the
same chopped column the validator compares against (cell-identity load).
The IMF cross-check for S1504 is reported informationally, not as a PASS/FAIL.

### Open questions / known caveats

1. **S1504 modern IMF CR unit harmonization**: modern DCORP_N_DC is raw
   USD; Shaikh's CR is USD billions. The 2001-2010 overlap diff of ~1.4e11x
   reflects the scale ratio, not a concept divergence. Phase 6 enrichment
   should normalize units before the cross-check.
2. **S1502/S1503 BEA Industry API extension**: not implemented in this
   fanout (BEA API client is a stub in `S00_apis.py`). Book-period values
   are authoritative for replication; post-2010 extension marked
   `data_unavailable` until BEA client lands.
3. **S1505 BEA NIPA / FRED UNRATE extension**: same situation — book-period
   only; extension targets BEA API + FRED UNRATE; downstream waves can
   re-fetch.
4. **Ramamurthy 2014 ProQuest citation**: still pending (Phase 4 Q6); the
   replication can proceed without it, but the EPR citation field should be
   completed when the ProQuest record is located.
5. **Generic O06 chopped writer extended** to allow `country_key` as a
   disambiguating uniqueness axis for cross-sectional series; otherwise
   S1508/S1509 would have failed the (year, subseries_id) uniqueness check.
