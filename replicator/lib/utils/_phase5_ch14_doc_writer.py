"""Phase 5 Ch14 DPR / EPR markdown writer (idempotent).

Authors DPR + EPR for S1402-S1408 (S1401 is hand-written). Each function
writes a single markdown file mirroring the S201/S1501/S1401 structure.

Run:
    python Technical/code/utils/_phase5_ch14_doc_writer.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils import paths  # noqa: E402

DOCS = paths.DOCS_SERIES


def _w(path: Path, body: str) -> None:
    body = dedent(body).lstrip("\n")
    path.write_text(body, encoding="utf-8")
    print(f"  wrote {path.relative_to(paths.PROJECT_ROOT)}")


def write_S1402() -> None:
    _w(DOCS / "S1402_DPR.md", """
    # S1402 — Unemployment Measures, US 1948-2011

    **Data Provenance Record (DPR)**
    **Phase**: 5 (Ingestion) · **Chapter**: 14 · **Figure**: 14.11
    **Status**: ingested · **Authored**: 2026-05-18

    ## 1. Definition
    S1402 jointly publishes the three unemployment measures plotted in Fig 14.11:
    - **S1402-A** Civilian unemployment rate (decimal, BLS CPS LNS14000000)
    - **S1402-B** Duration index (BLS CPS LNS13008275, mean weeks, rebased 1948-1951=100)
    - **S1402-C** Unemployment intensity = rate * (duration_index/100) -- Shaikh's Eq. 14.13

    ## 2. Why it matters
    Unemployment intensity (Shaikh's invention) is the x-axis of every Phillips
    curve in Section V (S1404-S1408). Shaikh argues it captures wage-suppression
    pressure better than the unemployment rate alone because long-spell
    unemployment multiplies the effective slack.

    ## 3. Sources
    | Subseries | Coverage | Source | Native units | Retrieval |
    |---|---|---|---|---|
    | S1402-A | 1948-2011 | Appendix 14.3 `UNEMPLRATE` (BLS LNS14000000) | decimal | Salvaged xlsx |
    | S1402-B | 1948-2011 | Appendix 14.3 `UNEMPDURATION` (BLS LNS13008275 rebased) | index 1948-51 avg=100 | Salvaged xlsx |
    | S1402-C | 1948-2011 | Appendix 14.3 `ulintensity` (derived) | decimal | Salvaged xlsx |
    | S1402-D | 1948-2024 | FRED `UNRATE` (monthly to annual mean) | percent | Live API |
    | S1402-E | 1948-2024 | FRED `UEMPMEAN` (monthly to annual mean) | weeks | Live API |

    ## 4. Construction
    Composite. Formulas (Appendix 14.2 p. 892 verbatim):
    ```
    duration_index_t = (UEMPMEAN_t / mean(UEMPMEAN_{1948..1951})) * 100   # index
    intensity_t      = UNRATE_t(decimal) * (duration_index_t / 100)        # decimal
    ```

    ## 5. Year coverage
    Book: 1948-2011 (64 obs each). Extension: 2012-2024 via FRED re-derivation.

    ## 6. Units
    Rate decimal, duration index 1948-1951=100, intensity decimal.

    ## 7. Caveats
    1. **UEMPMEAN 2011-01 top-coding break**: BLS raised individual-respondent top-
       coded duration from 104w to 260w in January 2011. Per Phase 4 Q2 resolution,
       NO backward adjustment is applied; the break is annotated in the registry
       under `S1402.components.duration.methodological_break_2011-01: true`. The
       duration INDEX absorbs part of the level shift via its rebased base period.
    2. **No backward adjustment**: any analyst-estimated continuity correction
       would alter Shaikh's published pre-2011 numbers, defeating the replication.

    ## 8. Cross-references
    CD legacy `S069`, CD2 `S069`. Book pp. 663-664, 892. Figure 14.11.
    Sibling: S1401 (wage share, the y-axis of Section V Phillips curves).

    ## 9. Validation expectation
    Tolerance ±1.0%; pass-through against Appendix 14.3.
    """)
    _w(DOCS / "S1402_EPR.md", """
    # S1402 — Extension Provenance Record

    **Series**: S1402 (Unemployment Measures) · **Chapter**: 14 · **Authored**: 2026-05-18

    ## Classification
    `content_type: time_series` · `construction: composite` · extension applies.

    ## Method
    Re-derivation. For 2012+, fetch FRED `UNRATE` and `UEMPMEAN` (both monthly,
    aggregated to annual means); rebase the duration index to the 1948-1951 mean
    of FRED `UEMPMEAN` (already available in the same fetch); construct intensity
    via Shaikh's exact formula.

    ## Worked example
    2024: UNRATE mean ≈ 4.0% → 0.0400; UEMPMEAN mean ≈ 22.0 weeks; 1948-1951
    base mean ≈ 11.5 weeks; duration index ≈ 1.913; intensity ≈ 0.0765.

    ## No-Proxy disclosure
    None. Both FRED IDs are the BLS CPS series Shaikh cites.

    ## No-Synthetic disclosure
    Every value is a primary BLS observation (book period via Appendix 14.3,
    extension via FRED). No interpolation, no synthetic continuity correction.

    ## Failure-mode table
    | Mode | Trigger | Behaviour |
    |---|---|---|
    | FRED key missing | env unset | Extension skipped; book period only |
    | UEMPMEAN 2011 break | data semantics | Documented; no adjustment per Q2 resolution |
    | Base window pre-1948 unavailable | not a real risk | Base is fixed at 1948-1951 from the data itself |

    ## CD2 divergence pre-disclosure
    Minimal expected (<1%). CD2 used the same FRED series.
    """)


def write_S1403() -> None:
    _w(DOCS / "S1403_DPR.md", """
    # S1403 — Wage Share vs Unemployment Intensity (Empirical Spiral)

    **Data Provenance Record (DPR)** · **Phase 5** · **Ch 14** · **Fig 14.12**
    **Authored**: 2026-05-18

    ## 1. Definition
    Quarterly HP(100)-filtered phase plot: y = wage share (W209RC1/GDP quarterly),
    x = unemployment intensity (UNRATE * duration_index/100, monthly aggregated
    to quarterly, duration rebased to 1948Q1-1951Q4 mean).

    ## 2. Why it matters
    Fig 14.12 is Shaikh's empirical analogue of the theoretical Goodwin-type
    clockwise spiral in Fig 14.9 -- evidence that the Classical wage-share
    Phillips dynamic operates at quarterly frequency in real US data.

    ## 3. Sources
    | Subseries | Coverage | Source | Native units |
    |---|---|---|---|
    | S1403-A | 1948-2011 annual | Appendix 14.3 `wageshhp100` (reference axis) | decimal HP100 |
    | S1403-B | 1948-2011 annual | Appendix 14.3 `ulintensityhp100` (reference axis) | decimal HP100 |
    | S1403-WSH_ANNUALAVG_HP100 | quarterly (collapsed to annual means) | FRED `W209RC1`/`GDP` quarterly, HP100-filtered, annual mean | decimal |
    | S1403-ULINT_ANNUALAVG_HP100 | quarterly (collapsed to annual means) | FRED `UNRATE`+`UEMPMEAN` monthly→quarterly, HP100-filtered, annual mean | decimal |
    | (sidecar) `S1403_quarterly.parquet` | quarterly long-form | Same as above | decimal |

    ## 4. Construction
    Phase 4 Q1 resolution:
    1. Fetch quarterly FRED `W209RC1` (Compensation of employees, paid: Domestic
       industries, billions USD SAAR) and `GDP` (billions USD SAAR). Compute
       quarterly wage_share = W209RC1 / GDP.
    2. Fetch monthly FRED `UNRATE` and `UEMPMEAN`. Aggregate to quarterly means.
       Rebase duration to the 1948Q1-1951Q4 (16-quarter) mean of UEMPMEAN.
       Intensity_q = (UNRATE_q/100) * (duration_index_q).
    3. Apply HP filter with **lambda=100** (Shaikh's choice; NOT 1600) over the
       full quarterly sample to both series independently.
    4. Collapse to annual means for the canonical processed parquet; preserve
       quarterly data in a sidecar parquet for phase-plot visualization.

    ## 5. Year coverage
    Annual reference axes: 1948-2011 (Appendix). Quarterly phase plot:
    1948Q1-2024Q4 (FRED-derived).

    ## 6. Units
    Decimal HP(100) values on both axes.

    ## 7. Caveats
    1. **HP lambda=100 for quarterly**: Shaikh deviates from the textbook
       quarterly value of 1600. Per Appendix 14.2 p. 893, lambda=100 throughout.
       DO NOT substitute; the chosen lambda preserves the "zigs and zags" of
       intra-year dynamics that the phase plot relies upon.
    2. **W270RE1Q156NBEA retired** (HTTP 404). Substituted W209RC1 + GDP
       quarterly pair (within-FRED ID routing; same NIPA T1.10 line 2 / line 1
       inputs). Not a concept change.
    3. **Quarterly axes vs annual axes**: the FRED-derived axes collapsed to
       annual means differ modestly from Appendix annual HP100 axes because
       HP(annual mean of quarterly) ≠ annual mean of HP(quarterly). This is
       reported informationally in the validator, not failed.

    ## 8. Cross-references
    CD legacy `S070`. Book p. 666; Appendix 14.2 p. 892-893.

    ## 9. Validation expectation
    Tolerance ±1.0% for the annual reference axes (pass-through). Quarterly
    axes are informational (no Appendix truth to compare).
    """)
    _w(DOCS / "S1403_EPR.md", """
    # S1403 — Extension Provenance Record

    **Series**: S1403 (Wage Share vs Unemployment Intensity) · **Ch 14** · **Authored**: 2026-05-18

    ## Classification
    `content_type: time_series` · `construction: composite` · extension applies via
    re-derivation at quarterly frequency.

    ## Method
    HP100 is applied to the FULL extended quarterly sample (1948Q1-2024Q4), not
    appended to the original-window filter output. This avoids endpoint bias on
    the post-2011 segment.

    ## No-Proxy disclosure
    The dead FRED ID `W270RE1Q156NBEA` is replaced by the live pair `W209RC1` +
    `GDP` at quarterly frequency. This is a within-FRED routing update to the
    SAME underlying NIPA Table 1.10 line 2 / line 1 series; not a concept-changing
    substitution. No `proxy: true` flag required.

    ## No-Synthetic disclosure
    All quarterly observations are primary BEA/BLS data. HP filtering is the
    documented analytical method per Shaikh's Appendix 14.2.

    ## Failure-mode table
    | Mode | Trigger | Behaviour |
    |---|---|---|
    | FRED key missing | env unset | Quarterly axes skipped; annual reference axes still emitted |
    | One quarterly source missing | API outage | Quarterly axes skipped; annual reference axes still emitted |
    | HP lambda substitution | maintainer error | Caught by Shaikh-specific test (HP_LAMBDA_CH14=100 constant) |

    ## CD2 divergence pre-disclosure
    Minor (<2%) divergence expected on the quarterly axes vs CD2 because CD2 used
    the now-retired W270RE1Q156NBEA and a different quarterly aggregation
    convention.
    """)


def write_S1404() -> None:
    _w(DOCS / "S1404_DPR.md", """
    # S1404 — Rate of Change of Wage Share vs Unemployment Intensity (Raw)

    **DPR · Phase 5 · Ch 14 · Fig 14.13 · Authored 2026-05-18**

    ## 1. Definition
    Annual unfiltered scatter:
    - x: ulintensity (decimal)
    - y: gwsh = ln(wage_share_t) - ln(wage_share_{t-1}) (decimal annual growth)

    ## 2. Why it matters
    The raw counterpart to Fig 14.14 (S1405). Despite noise, the negative slope
    is visible -- Shaikh's first empirical evidence for the wage-share Phillips
    curve as a structural relation.

    ## 3. Sources
    | Subseries | Coverage | Source |
    |---|---|---|
    | S1404-A `gwsh` | 1949-2011 (1948 NaN; first-diff) | Appendix 14.3 |
    | S1404-B `ulintensity` | 1948-2011 | Appendix 14.3 |

    ## 4. Construction
    `direct` (Anu sense): pass-through of two Appendix columns. The Appendix
    `gwsh` column is published as a log first-difference of `wagesh`; the
    validator confirms it reproduces from the level series under that definition.

    ## 5. Year coverage
    1949-2011 (intersection of the two columns dropping the differencing NaN).

    ## 6. Units
    Decimal annual growth rate (y); decimal (x).

    ## 7. Caveats
    Fig 14.13 is intentionally unfiltered; filtering happens in S1405.

    ## 8. Cross-references
    CD `S071`. Book p. 666.

    ## 9. Validation expectation
    ±1.0% pass-through.
    """)
    _w(DOCS / "S1404_EPR.md", """
    # S1404 — Extension Provenance Record

    **Ch 14 · Authored 2026-05-18**

    ## Classification
    `content_type: time_series` · `construction: direct`. Extension is the
    responsibility of S1401 (wage share) and S1402 (intensity); a Phase 6
    re-derivation pass can compute the extended scatter from extended levels.

    ## Method
    No direct extension from this loader. The raw scatter for 1949-2011 is the
    chapter's published object; for post-2011 the scatter can be reproduced via
    `gwsh_t = ln(S1401-A_t / S1401-A_{t-1})` and `ulintensity_t = S1402-C_t`.

    ## No-Proxy / No-Synthetic disclosures
    Inherits from S1401 and S1402.

    ## CD2 divergence pre-disclosure
    Minimal expected.
    """)


def write_S1405() -> None:
    _w(DOCS / "S1405_DPR.md", """
    # S1405 — HP(100)-Filtered Wage-Share Growth vs Unemployment Intensity

    **DPR · Phase 5 · Ch 14 · Fig 14.14 · Authored 2026-05-18**

    ## 1. Definition
    HP(100)-filtered analogue of S1404 plus the two-era Phillips-form fitted
    curves Shaikh reports in Appendix 14.2 (era 1: 1949-1982; era 2: 1994-2011).

    ## 2. Why it matters
    The central empirical result of Chapter 14: a stable wage-share Phillips
    curve in two segments, with the post-1983 segment shifted DOWN -- consistent
    with the neoliberal attack on labor (critical intensity ~9% era 1 vs ~5-6%
    era 2; corresponding "normal" unemployment ~5.9% vs ~4.2%).

    ## 3. Sources
    | Subseries | Source |
    |---|---|
    | S1405-A `gwshhp100` | Appendix 14.3 |
    | S1405-B `ulintensityhp100` | Appendix 14.3 |
    | S1405-FIT1 `GWSHHP100RAL8AF` | Appendix 14.3 (era-1 published constrained b=1 fit) |
    | S1405-FIT2 `GWSHHP100RAL8BP1F` | Appendix 14.3 (era-2 published constrained b=1 fit) |

    ## 4. Construction
    Direct read-through of Appendix HP100 series and published fits.
    PLUS the processor independently fits the Phillips form
    `y = a + b * x^c` over each era window in TWO variants:
    - **constrained_b1**: `y = a + x^c` (Shaikh's published form, implicit b=1)
    - **unconstrained**: free three-parameter `y = a + b * x^c`
    1983-1993 transition omitted from both fits per Shaikh's convention
    (Phase 4 Q4 resolution). Sidecar JSON `S1405_phillips_fits.json` records
    both variants plus an additional pre-2008 era-2 fit (1994-2007) for Phase 6
    regime-stability assessment.

    ## 5. Year coverage
    1949-2011.

    ## 6. Units
    Decimal HP100 on both axes; Phillips parameters dimensionless.

    ## 7. Caveats
    1. **HP lambda=100** (Shaikh's annual default; Appendix 14.2 p. 893).
    2. **Constrained vs unconstrained fits**: published reports a (C(1)) and c
       (C(3)) under implicit b=1. Phase 5 emits both for transparency.
    3. **1983-1993 transition**: omitted from primary fits.

    ## 8. Cross-references
    CD `S072`. Book p. 666-668. Published era-1: a=-1.026431, c=-0.010677,
    R²=0.931; era-2: a=-1.010996, c=-0.003709, R²=0.965.

    ## 9. Validation expectation
    ±1.0% pass-through on the time series; ±0.05 absolute on fitted (a, c)
    parameters vs published.
    """)
    _w(DOCS / "S1405_EPR.md", """
    # S1405 — Extension Provenance Record

    **Ch 14 · Authored 2026-05-18**

    ## Classification
    `content_type: time_series` · `construction: direct` (HP-filtered observed
    inputs + fitted curves). Extension via S1401/S1402 components, re-filtered
    over the full sample.

    ## Method
    Phase 5: replicate the published constrained b=1 fits. Phase 6: re-fit on
    1949-1982 and (extended) 1994-2024, plus a separate 1994-2007 era-2 fit for
    regime-stability assessment per Q4 resolution.

    ## Dual Phillips fit
    BOTH variants are emitted to `Technical/data/processed/S1405_phillips_fits.json`:
    - `constrained_b1`: replicates Shaikh's published form `y = a + x^c`
    - `unconstrained`: free three-parameter `y = a + b * x^c`
    Comparison documented in the validator report.

    ## No-Proxy / No-Synthetic disclosures
    Inherits from S1401 and S1402.

    ## Failure-mode table
    | Mode | Trigger | Behaviour |
    |---|---|---|
    | curve_fit non-convergence | numerical | Returns `converged: false` with NaN params; doesn't fail pipeline |
    | era window has < 4 obs | very short window | Returns `converged: false` |

    ## CD2 divergence pre-disclosure
    Minor; CD2 only emitted scatter, not fits.
    """)


def write_S1406() -> None:
    _w(DOCS / "S1406_DPR.md", """
    # S1406 — Inflation and Productivity Growth

    **DPR · Phase 5 · Ch 14 · Fig 14.15 · Authored 2026-05-18**

    ## 1. Definition
    Joint annual time series:
    - **S1406-A** `inflrate` = (p_t/p_{t-1})-1 where p = BEA GDP deflator
    - **S1406-B** `GPRODVTY` = productivity growth where productivity yr =
      (GDP*100/p)/(FEE/1000)  -- Shaikh's verbatim Appendix 14.2 p. 892 formula

    ## 2. Why it matters
    Per Eq. 14.18-14.19, the real-wage and nominal-wage Phillips curves (S1407,
    S1408) decompose algebraically into the wage-share Phillips curve plus
    productivity growth (for real wages) and plus productivity growth plus
    inflation (for nominal wages). S1406 supplies the two shift components.

    ## 3. Sources
    | Subseries | Source | Units |
    |---|---|---|
    | S1406-A `inflrate` | Appendix 14.3 (derived from BEA NIPA T1.1.9 line 1) | decimal annual rate |
    | S1406-B `GPRODVTY` | Appendix 14.3 (derived from BEA T1.10/T1.1.9/T6.5) | decimal annual rate |
    | S1406-C `GDP` (extension input) | FRED annual | billions USD SAAR |
    | S1406-D `GDPDEF` (extension input) | FRED annual mean | index 2017=100 |
    | S1406-E `B4701C0A222NBEA` (extension input) | FRED annual | thousands of jobs (FTE all industries) |

    ## 4. Construction
    Composite. Productivity formula implemented LITERALLY:
    ```
    yr_t = (GDP_t * 100 / p_t) / (FEE_t / 1000)
    ```
    The `*100` and `/1000` are unit-correcting multipliers (deflator scale
    convention and FEE thousands→millions conversion). DO NOT algebraically
    simplify -- doing so silently scales productivity by 100,000×.

    ## 5. Year coverage
    Book: 1949-2011. Extension: 2012-2024 via FRED re-derivation.

    ## 6. Units
    Decimal annual growth rates (inflation, productivity growth).

    ## 7. Caveats
    1. **PRODUCTIVITY = REAL GDP PER FTE, NOT PER HOUR.** Concept-policing rule
       (Phase 4 Q5): loader REJECTS per-hour FRED IDs (`OPHNFB`, `PRS85006092`,
       `OPHPBS`, `OPHMFG`). Substituting per-hour silently breaks Shaikh's
       wage-share decomposition wr = w/p, gwsh = wr - yr.
    2. **Chain-type GDPDEF**: current FRED vintage uses 2017=100 chain-type.
       For growth rates the base year is immaterial; we use the current vintage.
    3. **FTE coverage**: `B4701C0A222NBEA` is FTE all industries (NIPA T6.5
       line 1 broadest) consistent with Shaikh's economy-wide intent.

    ## 8. Cross-references
    CD `S073`. Book pp. 669-670, 892.

    ## 9. Validation expectation
    ±1.0% pass-through against Appendix 14.3 `inflrate` and `GPRODVTY` columns.
    Spot-check productivity formula at 1948, 1972, 1996, 2011 against Appendix.
    """)
    _w(DOCS / "S1406_EPR.md", """
    # S1406 — Extension Provenance Record

    **Ch 14 · Authored 2026-05-18**

    ## Classification
    `content_type: time_series` · `construction: composite` · extension via
    re-derivation (NOT growth-rate splice on the derived series).

    ## Method
    For 2012+, fetch FRED `GDP`, `GDPDEF`, `B4701C0A222NBEA`; apply Shaikh's
    productivity formula LITERALLY; compute inflation = GDPDEF.pct_change()
    and productivity growth = yr.pct_change(); append.

    ## CONCEPT POLICING (HARD RULE)
    Loader emits assertion failure if any per-hour FRED ID is added to its
    `FRED_INPUTS` list. The list of prohibited substitutes is module-level in
    `_ch14_helpers.PER_HOUR_PROHIBITED_FRED_IDS`. Adding `OPHNFB` (or any
    sibling) will fail import. This is a code-level guard against silent proxy
    creep over future maintenance.

    ## No-Proxy disclosure
    None. All three FRED IDs are the BEA NIPA series Shaikh cites.

    ## No-Synthetic disclosure
    No interpolation, no synthetic substitutes. Every observation is BEA
    primary data.

    ## Failure-mode table
    | Mode | Trigger | Behaviour |
    |---|---|---|
    | Per-hour series sneaks in | maintainer error | `ValueError` at loader import |
    | FRED key missing | env unset | Extension skipped; book period only |
    | FEE coverage change at BEA | future BEA revision | re-fetch picks up automatically; consider freezing vintage |

    ## CD2 divergence pre-disclosure
    Minor; CD2 used same inputs at a slightly different vintage.
    """)


def write_S1407() -> None:
    _w(DOCS / "S1407_DPR.md", """
    # S1407 — HP(100) Real-Wage Growth vs Unemployment Intensity

    **DPR · Phase 5 · Ch 14 · Fig 14.16 · Authored 2026-05-18**

    ## 1. Definition
    HP(100) phase plot: y = real-wage growth `wr = (EC*100/FEE)/p`, x = intensity.

    ## 2. Why it matters
    Per Eq. 14.18: real-wage Phillips = wage-share Phillips + productivity growth.
    Because productivity growth was not stable over 1948-2011, the real-wage curve
    departs from the wage-share curve in the 1960-1999 productivity downswing/
    upswing cycle, returning to parallel only after 1999.

    ## 3. Sources
    | Subseries | Source |
    |---|---|
    | S1407-A `GRWAGEHP100` | Appendix 14.3 |
    | S1407-B `ulintensityhp100` | Appendix 14.3 |

    ## 4. Construction
    Direct pass-through. Processor additionally fits two-era Phillips curves
    BOTH as direct refit and (via S1405 sidecar) as algebraic decomposition.

    ## 5. Year coverage
    1949-2011.

    ## 6. Units
    Decimal HP100 on both axes.

    ## 7. Caveats
    1. Inherits productivity concept-policing from S1406 (real wage uses same
       EC, FEE, p inputs).
    2. Inherits UEMPMEAN 2011 break flag from S1402.
    3. HP lambda=100.

    ## 8. Cross-references
    CD `S074`. Book p. 670. Equation 14.18.

    ## 9. Validation expectation
    ±1.0% pass-through against Appendix `GRWAGEHP100` and `ulintensityhp100`.
    """)
    _w(DOCS / "S1407_EPR.md", """
    # S1407 — Extension Provenance Record

    **Ch 14 · Authored 2026-05-18**

    ## Classification
    `time_series` · `direct`. Extension via S1401/S1402/S1406 components.

    ## Method (both variants emitted)
    - **direct_refit**: fit Phillips form to extended GRWAGEHP100 on each era
      window
    - **algebraic_decomposition**: S1405-era-fit + HP100(productivity growth)
      per Eq. 14.18

    Both reported in `S1407_phillips_fits.json` sidecar.

    ## Concept policing
    Inherited from S1406 (real wage construction reuses same per-FTE inputs).

    ## No-Proxy / No-Synthetic disclosures
    Inherits from S1401, S1402, S1406.

    ## CD2 divergence pre-disclosure
    Minor expected.
    """)


def write_S1408() -> None:
    _w(DOCS / "S1408_DPR.md", """
    # S1408 — HP(100) Nominal-Wage Growth vs Unemployment Intensity

    **DPR · Phase 5 · Ch 14 · Fig 14.17 · Authored 2026-05-18**

    ## 1. Definition
    HP(100) phase plot: y = nominal-wage growth where `w = EC*100/FEE`, x = intensity.

    ## 2. Why it matters
    The original Phillips relation -- but plotted vs unemployment INTENSITY (not
    the rate). Per Eq. 14.19: nominal-wage Phillips = wage-share Phillips +
    inflation + productivity growth. Table 14.3 secondary regression decomposes
    the residual; published era-1 coefficient on inflation is "slightly below 1"
    and on productivity growth ≈ 0.82.

    ## 3. Sources
    | Subseries | Source |
    |---|---|
    | S1408-A `GMWAGEHP100` | Appendix 14.3 |
    | S1408-B `ulintensityhp100` | Appendix 14.3 |

    ## 4. Construction
    Direct pass-through. Processor additionally:
    - Fits two-era Phillips curves (direct refit) at constrained-b=1 and free-b
    - Runs Table 14.3 OLS `GMWAGEHP100 = const + b_p * inflrateHP100 + b_y *
      GPRODVTYHP100` per era

    ## 5. Year coverage
    1949-2011 (sample window 1949-1982 / 1994-2011 per Appendix 14.2; off-by-one
    with chapter-text 1948-1982 noted -- differencing loses 1948).

    ## 6. Units
    Decimal HP100; OLS coefficients dimensionless.

    ## 7. Caveats
    1. Inherits productivity concept-policing from S1406.
    2. Inherits UEMPMEAN 2011 break from S1402.
    3. HP lambda=100.
    4. Sample-window off-by-one: text says 1948-1982; Appendix Stata output and
       differencing both start at 1949. Phase 5 uses 1949-1982.

    ## 8. Cross-references
    CD `S075`. Book p. 670-672. Equation 14.19. Table 14.3.

    ## 9. Validation expectation
    ±1.0% pass-through; Table 14.3 coefficients reported informationally.
    """)
    _w(DOCS / "S1408_EPR.md", """
    # S1408 — Extension Provenance Record

    **Ch 14 · Authored 2026-05-18**

    ## Classification
    `time_series` · `direct`. Extension via re-derivation from S1401 + S1406 +
    S1402 inputs.

    ## Method (both variants emitted)
    - **direct_refit**: fit Phillips form to extended GMWAGEHP100
    - **algebraic_decomposition**: S1405-era-fit + HP100(inflation) +
      HP100(productivity growth) per Eq. 14.19

    Both reported in `S1408_phillips_fits.json` sidecar, alongside the Table 14.3
    secondary regression results.

    ## Concept policing
    Inherited from S1406 (nominal wage w = EC*100/FEE uses same per-FTE
    convention).

    ## No-Proxy / No-Synthetic disclosures
    Inherits from S1401, S1402, S1406.

    ## CD2 divergence pre-disclosure
    Minor expected.
    """)


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    for fn in [write_S1402, write_S1403, write_S1404, write_S1405,
               write_S1406, write_S1407, write_S1408]:
        fn()
    print("Ch14 DPR/EPR markdown written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
