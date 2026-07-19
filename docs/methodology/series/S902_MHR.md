# S902 — Methodological History Report (MHR)

**Series**: S902 — Eigensystem Standard Prices + Observed Profit Rates (65-order 1998 BEA)
**Chapter**: 9 (Competition and Inter-Industrial Relative Prices) · **Group**: ch9 / CH09
**Perspective**: authored *from Shaikh's perspective*.
**Authored**: 2026-06-30 · **Read-only provenance**; every claim traces to a cited path.

Grounding: `Technical/research/S902_research.json`; `Technical/docs/series/S902_DPR.md` +
`S902_EPR.md`; `Technical/docs/chapters/CH9_RESEARCH_SUMMARY.md`;
`Technical/methodology_review/CH09_review.json`; Phase-0
`Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.md` (+ `NIPA_CHANGE_TIMELINE.md`);
`Technical/docs/methodology/concordances/_sources/SOURCES.md`.

---

## 1. What it is

S902 is the **Sraffa-eigensystem decomposition** of Shaikh's IO data. For each industry j and
benchmark year t it carries the normalized **standard price** `tp(r)_norm` at the observed profit
rate `r_obs(t)`, the normalized **labor-time share** `tv_norm` (the labor-value composition `VR0_j`),
and the per-year **observed profit rate** scalar (`S902_DPR.md` §1). It supplies the eigensystem and
distance figures — **Fig 9.4, 9.5** (integrated output-capital ratios `VR(r)_j`, circulating),
**9.6, 9.7** (standard prices `p(r)/v`, circulating), **9.9, 9.10, 9.11** (fixed-capital), **9.13,
9.14, 9.15** (standard-price-vs-labor-time distance measures across years), **9.18** (production-vs-
direct-price ratios).

Book definition — integrated output-capital ratios (Ch9 p.406, verbatim in `S902_research.json`):
> "Figure 9.4 presents the key evidence from United States 1998 data on the paths of individual
> industry integrated output–capital ratios relative to the output–capital ratio of the standard
> industry (VRR ≡ R). … individual output–capital ratios VR(r)ⱼ generally follow very smooth
> near-linear paths."

Linear-endpoint method (Ch9 p.407, verbatim): "at w = 1, r = 0, we get VR(0)ⱼ ≡ VR0ⱼ = the labor
value composition of the jth industry; and at w = 0, r = R, we get VR(R)ⱼ = R … The corresponding
standard prices of individual commodities p(r)ⱼ would then also be exact linear functions."

Core formulae (`S902_research.json` formula; `S902_DPR.md` §4): standard price
`p(r)ⱼ/vⱼ = 1 + (r/R)·(R − VR0ⱼ)/VR0ⱼ` (eq. 9.20, exact under linear-VR); fixed-capital price system
`p(r) = w·l + p(r)·(A+D) + r·p(r)·K` (Appendix 9.1 eq. 9.1.5) with `KT ≡ K·(I−(A+D))⁻¹`; **maximum
profit rate R = 1/λ_max(KT)** (eq. 9.1.6), Sraffa's standard commodity as numeraire (`w = 1 − r/R`).
Two models run on the same 1998 data: **circulating** (K=A, D=0; Figs 9.4–9.8) and **fixed-capital**
(K,D from Fixed Asset Tables; Figs 9.9–9.12). Appendix location: **Appendix 9.1** (matrix algebra
pp.861–866) + **Appendix 9.2** (data pp.867–869); Table 9.18 reports R_t, Tables 9.12–9.13 the
distance measures.

Hand-checks (`CH09_review.json`): S902-P_1947F = normalized `tp(r)`, ind1 = 0.09634038 **EXACT**;
S902-ROBS **EXACT** vs `Appendix9_ObservedProfitRates.xlsx` {1947:0.236, 1958:0.176, 1963:0.21,
1967:0.229, 1972:0.188, 1998:0.1258}.

## 2. Source lineage

Same 71/65-order substrate as S901 (`S902_research.json` primary_source; `CH09_review.json`
touchpoints S902/io), plus the fixed-capital apparatus:

- **1998 Use table (65-order, NAICS, post-redefinition)** → `A′ = I − (B′)⁻¹`, gross output `X′`,
  and Employee-Compensation → skill-adjusted labor coefficients `l′` (Ch9 p.867, verbatim).
- **BEA Fixed Asset Tables 3.1ES (current-cost net stock of private fixed assets by industry) and
  3.4ES (current-cost depreciation)** → industry-level `Kⱼ` and `Dⱼ`, "mapped into the sixty-one
  industries appearing in BEA input–output tables" (Ch9 p.869, verbatim).
- **1997 benchmark capital-flow (gross-investment) matrix** → supplies the inter-industry composition
  of `K_ij`, under the assumption that every asset type in industry j grows at that industry's gross
  rate `g_j` (so capital-stock column proportions = capital-flow column proportions;
  `S902_research.json` components; Appendix 9.2 Sec IV.1).
- **NIPA Tables 5.8.5A-B / 7.5 / 7.1B** → split government capital stock/depreciation into the four
  IO government cells (Federal/State-Local × General/Enterprise); **NIPA Table 7.12 lines 133–134** →
  OOH correction (`S902_research.json` components; `CH09_review.json` touchpoints S902/nipa).
- **1947–1972 Ochoa (1984)/Shaikh (1998a) 71-order tables** → the multi-year distance figures
  (9.13–9.15).

Eigensystem construction: `KT = K·(I−(A+D))⁻¹` → dominant eigenvalue `λ_max` → `R = 1/λ_max` → standard
prices `tp(r)` at `r_obs`, l1-normalized. Empirical eigenvalue decomposition (Appendix 9.1 Sec V, eq.
9.1.19) shows `p(r)` deviates from linear only via `(r/R)²·Σ(sub-dominant terms)`; observed profit
shares ~0.30 give `(r/R)² ≈ 0.09`, so the linear Marx component dominates — the finding visualized in
Figs 9.4–9.7 (`S902_research.json` methodology_notes).

## 3. Why these sources, from Shaikh's perspective + rejected alternatives

- **Why the specific standard-commodity / vertical-integration construction.** Shaikh's claim is that
  the *actual* wage-profit geometry, at *real* capital intensities, is near-linear — i.e., the
  standard commodity is empirically (not just theoretically) relevant. To show that he must build the
  genuine `KT` eigensystem from observed IO + capital-stock data and choose the standard commodity as
  numeraire so `w = 1 − r/R` is *exactly* linear, isolating any curvature onto the sub-dominant
  eigenvalues (`S902_research.json` methodology_notes; Appendix 9.1 eq. 9.1.19).
- **Why the fixed-capital model, not just circulating.** A circulating-only model (K=A, D=0) omits
  durable capital and would understate capital intensities; the whole point is that even *with*
  realistic fixed capital the curves stay near-linear. He therefore runs both and contrasts them
  (`CH9_RESEARCH_SUMMARY.md` S902 note).
- **Why BEA Fixed Asset Tables + the 1997 capital-flow matrix.** These are the only public sources
  giving *both* an industry-level capital-stock/depreciation vector (3.1ES/3.4ES) *and* the
  inter-industry composition needed to place capital *by using-industry* — the capital-flow benchmark
  is the unique BEA product mapping investment goods to using industries (`IO_CHANGE_TIMELINE.md`,
  "Capital-flow benchmark matrix").
- **Rejected alternative — annual capital-flow data.** BEA never produced a *benchmark* asset-by-
  industry matrix after 1997; only *research* annual tables. Shaikh anchors on the 1997 benchmark and
  the `g_j`-uniform-growth assumption rather than a shakier annual approximation
  (`S902_research.json` open_questions 3).
- **Rejected alternative — re-solving vs adopting Shaikh's published vectors.** For RSCD v1 (not
  Shaikh himself) the eigensystem is *read* not re-solved (see §5); Shaikh's own construction *is* the
  eigenvalue solve.

## 4. Methodological-change exposure — **the central section**

S902 carries the S901 SIC→NAICS wall **plus** the capital-flow-matrix discontinuity, making it the
most change-exposed series in the chapter.

1. **71-order SIC ↔ 65-order NAICS non-splice** (as in S901). The 1947–1972 Ochoa 71-order (SIC) and
   1998 BEA 65-order (NAICS) eigensystems are computed on non-conformable industry schemes; the
   multi-year distance figures (9.13–9.15) are *year-by-year cross-sections*, never a spliced panel
   (`IO_CHANGE_TIMELINE.md` "The SIC → NAICS break"; `S902_DPR.md` §3). Same machine-enforcement gap as
   S901 (`CH09_review.json` CH9-F4): `industry_index` untagged. Census SIC↔NAICS bridges and the NAICS
   revision chain in `concordances/_sources/naics/` are the upstream crosswalk authority (`SOURCES.md`),
   and BEA's I-O↔NAICS concordances (SCB Dec 2002 / Oct 2007 / Aug 2018 App. A) show the mapping is
   lossy — reinforcing non-splice.
2. **Discontinuation of the BEA benchmark capital-flow matrix after 1997 — the S902-specific wall**
   (`IO_CHANGE_TIMELINE.md`, "Capital-flow benchmark matrix — discontinued after 1997";
   `CH09_review.json` CH9-P2, POSITIVE). The **1997** capital-flow table (released SCB Nov 2003, the
   seventh in the series, first on a NAICS basis, first to include software) is the **LAST** benchmark
   asset-by-industry matrix BEA ever produced; **no benchmark capital-flow table exists for 2002 or
   later.** Shaikh's fixed-capital model distributes Fixed Asset Tables 3.1ES/3.4ES across industries
   *using that 1997 matrix*. This structurally blocks any post-1998 fixed-capital extension: a
   replicator would have to **approximate** the asset-by-industry distribution from BEA's detailed
   Fixed Asset Tables (type × industry) under the `g_j`-uniform-growth assumption
   (`CH9_RESEARCH_SUMMARY.md` open-question 4; `S902_EPR.md` §1). Disclosed, not hidden.
3. **NIPA comprehensive-revision exposure on the capital apparatus.** The Fixed Asset Tables and the
   government-split NIPA tables (5.8.5A-B, 7.5, 7.1B) are all re-vintaged by comprehensive revisions;
   the **1999** update capitalized software, the **2013** update capitalized R&D/entertainment as new
   Intellectual Property Products (**≈ +$400B GDP, capital-stock levels rise**), and the **2018**
   update shifted T7.11 line numbers by +1 (`NIPA_CHANGE_TIMELINE.md`). Shaikh fixes BEA data at the
   **2011 vintage**; any re-pull of K/D past 2013 lands on a different capital-stock concept and must
   not be spliced across the revision boundary.
4. **Coverage residue from a vintage/model choice** (`CH09_review.json` CH9-F2, MEDIUM): only the
   fixed-capital observed profit rate (1998 = 0.1258) ships in the chopped output; the circulating
   observed r (~0.2971 per the workbook header) is absent, so the book's p.416 "observed r/R = 0.286
   in the circulating capital model" cannot be reproduced (only the fixed r/R = 0.172 reproduces).

## 5. Replication fidelity note

RSCD reproduces S902 **bit-exact to Appendix 9** (V03 ±0.5%, MAE 0.0%; `CH9_RESEARCH_SUMMARY.md`
Phase 5–8; hand-checks EXACT). **The eigensystem is read, not re-solved** — the honest headline limit
(`CH09_review.json` CH9-F7, LOW; `S902_DPR.md` §7 caveat 1): RSCD adopts Shaikh's pre-computed `tp(r)`
columns and the published `r observed` headers rather than independently solving the dominant
eigenvalue of `KT = K·(I−(A+D))⁻¹` to regenerate Table 9.18's R_t. So "replication" here is *faithful
reproduction of published outputs*, not independent recomputation. R_t values were sanity-gated
(V03 EXPECTED_R gate) and match exactly. The fresh eigenvalue solve is documented as a downstream
scientific-validation target (`S902_EPR.md` §7 future-work note), deliberately not a v1 blocker
because blocking it would block the whole chapter. Circularity caveat as in S901 (CH9-F6): V03
round-trips the same XLSX; genuine non-circular anchors are Table 9.18 R and the `δc` of Tables
9.12–9.14. OOH applied upstream (not re-derived). Non-splice discipline held.

## 6. Forward risk

- **No future BEA benchmark capital-flow matrix is expected** — the benchmark series ended at 1997;
  every future fixed-capital extension is an *approximation* problem, not a data-pull
  (`IO_CHANGE_TIMELINE.md`). This is the dominant forward risk for S902.
- **Future BEA benchmarks / NAICS vintages** (2017 latest; 2022 forthcoming) each require a full
  re-solve of `A′, K, D, KT` and a fresh eigenvalue decomposition per year, plus re-OOH and re-crosswalk
  (`S902_research.json` extension_candidates; `S902_EPR.md` §7).
- **NIPA comprehensive revisions** keep re-vintaging the Fixed Asset and government-split tables
  underneath any re-pull; stay on one coherent vintage (`NIPA_CHANGE_TIMELINE.md`).
- **A v2 independent eigenvalue solve** should validate against Shaikh's Table 9.18 R_t
  {1.088, 0.9734, 0.8547, 0.7644, 0.7033, 0.7317} within numerical tolerance (`S902_EPR.md` §7).
