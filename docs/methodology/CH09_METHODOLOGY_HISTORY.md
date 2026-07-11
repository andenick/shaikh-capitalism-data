# Chapter 9 — Methodology History Compendium (CH09)

**Chapter**: 9 — Competition and Inter-Industrial Relative Prices (Input-Output & Sraffa prices)
**Series**: S901, S902, S903 · **Group**: ch9 / CH09
**Authored**: 2026-06-30 · **Perspective**: from Shaikh's perspective · **Read-only provenance.**

Per-series detail: `series/S901_MHR.md`, `series/S902_MHR.md`, `series/S903_MHR.md`.
Machine-readable twin: `../../methodology_review/CH09_methodology.json`.
Phase-0 anchors: `_timelines/IO_CHANGE_TIMELINE.md`, `_timelines/NIPA_CHANGE_TIMELINE.md`,
`concordances/_sources/SOURCES.md`. Review: `../../methodology_review/CH09_review.json`.

---

## 1. What the chapter is

Chapter 9 is Shaikh's empirical vindication of classical price theory: **market prices cluster around
prices of production, which in turn lie within a few percent of direct prices (integrated labor
times), and the actual wage-profit geometry is near-linear at real capital intensities.** Three
series carry a single integrated computation (`CH9_RESEARCH_SUMMARY.md` "series count recommendation:
KEEP AT 3"):

| Series | Object | Core figures | Book pages |
|---|---|---|---|
| **S901** | Market vs direct prices (normalized, per industry) | Fig 9.1, 9.2, 9.16 | pp.395–396; App. 9.2 pp.867–868 |
| **S902** | Sraffa-eigensystem standard prices `tp(r)` + integrated output-capital ratios `VR(r)` + observed profit rates | Fig 9.4–9.7, 9.9–9.11, 9.13–9.15, 9.18 | pp.406–407; App. 9.1 pp.861–866 + 9.2 |
| **S903** | Actual wage-profit curves, PWT 7.1 productivity-scaled | Fig 9.8, 9.12, 9.19 | pp.422–423; App. 9.2 pp.868–869 |

The engine is one IO dataset (S901 substrate) → one price-of-production eigensystem solve
(S902: `VR(r)`, `p(r)/v`, `R = 1/λ_max(KT)`) → one wage-share identity (S903: `σW(r) = 1 − r/R`,
productivity-scaled). Data ground-truth = 14 `Appendix9_*.xlsx` workbooks at
`SalvagedInputs/book_data/ShaikhChoppedTables/`; every ch9 chopped value is hand-verified EXACT vs
these (`CH09_review.json` D13 PASS, score 100).

## 2. The keystone story — the 71-order (SIC) vs 65-order (NAICS) classification break

This is the central methodological-change fact of Chapter 9 and the keystone for the IO + concordance
compendia. Shaikh's historical panel splices **nothing** — it *jumps* 1972 → 1998 across the biggest
discontinuity in US industry statistics:

- **1947, 1958, 1963, 1967, 1972**: Ochoa (1984)/Shaikh (1998a) **71-order, SIC-vintage** IO tables
  (real estate excluded, "the great bulk of which is from OOH", Ch9 p.868). Per the Phase-0 timeline
  these sit on 1957/1972-SIC benchmark bases; **1972 is the last Ochoa 71-order year Shaikh uses**.
- **1998**: BEA **65-order, NAICS-vintage** industry-by-industry Use table (post-redefinition), OOH-
  corrected via NIPA T7.12 lines 133–134.

The wall (`IO_CHANGE_TIMELINE.md`, "The SIC → NAICS break (the Ch9 wall)"): **last SIC benchmark =
1992; first NAICS benchmark = 1997.** BEA explicitly states pre-1997 historical benchmark tables
"should not be used as a time series." The 71-order SIC and 65-order NAICS schemes are **not
conformable** — a continuous industry panel across 1972→1998 is *not reconstructable*. Even within
NAICS the row/column order drifts at every benchmark (1997/2002/2007/2012/2017). RSCD encodes each
benchmark year as a frozen `cross_sectional` exhibit and does **not** build an illegal panel
(`CH09_review.json` CH9-P1, POSITIVE). The one gap: the non-splice is **narrated, not machine-
enforced** — `industry_index` is a bare integer with no `classification_vintage ∈ {SIC71, NAICS65}`
tag (CH9-F4, MEDIUM). Concordance authority for any attempted crosswalk is staged in
`concordances/_sources/naics/` (Census 1987-SIC↔1997-NAICS + the NAICS revision chain
1997→2002→2007→2012→2017→2022) with BEA's own I-O↔NAICS concordances as SCB-PDF appendix tables
(SCB Dec 2002 / Oct 2007 / Aug 2018 App. A) — all of which show the mapping is *lossy* (`SOURCES.md`).

**See also:** `PRODUCTION_BOUNDARY_ACROSS_CLASSIFICATION_ERAS.md` — why this SIC-era I-O system carries NO productive/unproductive partition (unlike Ch6's NIPA-sector business-NOS boundary and Ch7's NAICS exclusion key), and why that absence is faithful and must never be harmonized.

## 3. The second wall — the post-1997 capital-flow benchmark discontinuity (S902/S903)

The BEA **benchmark capital-flow matrix** (asset-type × using-industry) was produced each benchmark
year through **1997** (released SCB Nov 2003 — seventh in the series, first NAICS-basis, first to
include software) and was **discontinued after 1997**; no benchmark table exists for 2002+
(`IO_CHANGE_TIMELINE.md`, "Capital-flow benchmark matrix"; `CH09_review.json` CH9-P2, POSITIVE).
Shaikh's fixed-capital model (S902 `KT`, S903 wage-profit curves) distributes BEA Fixed Asset Tables
3.1ES/3.4ES across industries *using that 1997 matrix* under the `g_j`-uniform-growth assumption. This
structurally blocks any post-1998 fixed-capital extension: replicators must **approximate** the asset-
by-industry distribution from detailed Fixed Asset Tables (type × industry). Disclosed, not hidden.

## 4. The third change axis — PWT 7.1 → 10.01 growth-splice (S903)

The wage-profit curves are put on a common real axis by a **PWT 7.1** real-output-per-worker index
(variable `rgdpwok`, chain-weighted; Ch9 p.869), with the 1947 anchor (0.322501) back-extended from
PWT 1950 via BEA LTEG A163 / NBER output-labor. PWT 7.1 is superseded by **PWT 10.01 (2023)** on a
different base/PPP round; the only safe extension is a **multiplicative growth-rate splice on the
productivity index**, bridged at an overlap anchor, with the multiplier re-applied to a **freshly-
derived σW(r)** — the No-Lazy-Splices-on-Derived-Quantities rule (`S903_EPR.md` §3; `CH09_review.json`
CH9-P3, POSITIVE).

## 5. NIPA-vintage coupling (all three series)

The 1998 labor coefficients, OOH correction, government capital splits, and the LTEG 1947 anchor all
draw NIPA tables (1.10, 5.8.5A-B, 6.4D, 7.1B, 7.5, 7.12). Shaikh fixes BEA data at the **2011
vintage** (`NIPA_CHANGE_TIMELINE.md`, "Why this matters for RSCD"). Every comprehensive revision after
2011 — **2013** (R&D/entertainment → IPP, ≈ +$400B GDP, capital-stock levels rise), **2018** (T7.11
+1 line shift, incorporated 2012 benchmark I-O), **2023** (2017 benchmark supply-use, reference year →
2017) — reclassifies magnitudes and, in 2018, shifts line numbers. Any re-pull must be re-computed
end-to-end on a single coherent vintage; **never splice across a comprehensive-revision boundary.**

## 6. Replication fidelity posture (chapter-wide)

- **Bit-exact to Appendix 9** by the read-the-truth-column pattern; V03 ±0.5%, MAE 0.0% across all
  three series (`CH9_RESEARCH_SUMMARY.md` Phase 5–8; `CH09_review.json` hand_check_results all EXACT).
- **Eigensystem read, not re-solved** (CH9-F7, LOW): RSCD adopts Shaikh's published `tp(r)`/`wr(r)`
  columns and Table 9.18 R_t rather than independently solving `KT = K·(I−(A+D))⁻¹`. Honest limit;
  the fresh solve is a documented downstream target, deliberately non-blocking.
- **Reference-value circularity disclosed** (CH9-F6, LOW): V03 round-trips the same XLSX the chopped
  is melted from — this confirms melt fidelity, not independent book confirmation. Genuine non-circular
  anchors exist and were verified in `REPLICATION_VALUECHECK_ch09`: Table 9.18 R (EXACT), δc of Tables
  9.9/9.14/9.16 (10/12 year-cells EXACT), r/R = 0.172 prose (EXACT).
- **OOH applied upstream** by Shaikh (not re-derived by the loader); a raw-BEA v2 would re-apply it.
- **Coverage residues** (all MEDIUM, none data-authenticity): circulating-model observed r absent
  (CH9-F2), Table 9.19 "Actual normal capacity/capital" row uncovered (CH9-F3), stale S903 research
  figure-list (CH9-F1).

## 7. Forward risk (chapter-wide)

1. **No future benchmark capital-flow matrix** — the dominant structural risk; every fixed-capital
   extension (S902, S903) becomes an approximation problem.
2. **Future BEA benchmarks / NAICS vintages** (2017 latest; 2022 forthcoming) each need a full per-year
   `A′/K/D/KT` re-solve + eigenvalue decomposition + re-OOH + re-crosswalk; nothing splices.
3. **PWT revisions** (10.01 and later) enter S903 only via overlap-anchored growth-rate splice on the
   productivity index — never a level substitution.
4. **NIPA comprehensive revisions** keep re-vintaging the 1998 substrate and NIPA line numbers; hold a
   single coherent vintage.
