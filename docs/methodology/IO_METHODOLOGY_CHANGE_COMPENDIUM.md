# Input-Output Methodology-Change Compendium

**Phase-3 IO-synthesis deliverable for the RSCD comprehensive review** — Shaikh, *Capitalism: Competition, Conflict, Crises* (2016), clean replication.

- **Compiled:** 2026-07-01 (Phase-3 IO-synthesis agent)
- **Aggregates:** Phase-0 timeline (`_timelines/IO_CHANGE_TIMELINE.{md,json}`), all 16 per-chapter methodology JSONs (`methodology_review/CH*_methodology.json`), the ch7 + ch9 per-series MHRs and dossiers, and the ch7/ch9 review cross-checks (`methodology_review/CH0{7,9}_review.json`).
- **Companion (parallel):** `IO_METHODOLOGY_CHANGE_COMPENDIUM` pairs with the concordance compendium being authored alongside it (industry-classification-bridge synthesis) and the `NIPA_CHANGE_TIMELINE.{md,json}` (magnitude/vintage synthesis). Cross-references to the concordance compendium are marked **[→CONC]** below.
- **Status:** READ-ONLY aggregation. Every claim traces to a cited RSCD path or a bea.gov / census.gov URL carried in the Phase-0 timeline.

---

## 1. Executive summary

A minority of RSCD series rest on **BEA benchmark input-output (I-O) accounts**. They are concentrated in three places: **Chapter 9** (relative-price / Sraffa-eigensystem core — the "Ch9 wall"), **Chapter 7** (real-competition profit-rate industry panels), and the **Extra-Series** Sraffa-price studies **XS2001 / XS2101**. One Chapter-2 series (**S216**) is a frozen 1972 benchmark cross-section. Everything else in the project either has no industry dimension or touches benchmark I-O only *indirectly* (NIPA aggregates that happen to incorporate a benchmark revision — S202/S203/S213), or would inherit an I-O break only on a hypothetical reconstruction (S214/S215/S703/S704/S1001).

**Direct BEA-benchmark-I-O series (11):** `S901`, `S902`, `S903` (ch9); `S705`, `S706`, `S709`, `S710`, `S711` (ch7); `XS2001`, `XS2101` (Extra-Series); `S216` (ch2).
(Of the ch7 keystone band S705–S711, **S707/S708 do NOT touch I-O** — they are Greek figure-recoveries with `io_touch: none`.)

Two **structural walls** dominate every one of these series and are the reason RSCD freezes each benchmark as a stand-alone cross-section rather than building a continuous panel:

- **(a) The SIC(71-order) → NAICS(65-order) classification break — "the Ch9 wall."** BEA's last SIC-basis benchmark is **1992**; its first NAICS-basis benchmark is **1997**. BEA itself states the pre-1997 historical benchmark tables *"should not be used as a time series."* Shaikh's Ch9 panel splices six cross-sections — Ochoa (1984) / Shaikh (1998a) **71-order SIC** tables for 1947/1958/1963/1967/1972 and the BEA **65-order NAICS** Use table for 1998 — but the two classifications are **not conformable**, so **a continuous 1947–1998 industry I-O panel is not reconstructable** (CH9 open-question 3; CH9-P1 POSITIVE). Each year is a frozen exhibit.

- **(b) Discontinuation of the BEA benchmark capital-flow matrix after 1997.** The benchmark **capital-flow table** (use-type × using-industry matrix distributing new equipment / software / structures investment across industries) was produced for each benchmark year through **1997** (released SCB Nov 2003 — the seventh and last in the series, first on a NAICS basis, first to include software). **No benchmark capital-flow table exists for 2002 or later.** This blocks any **post-1998 fixed-capital wage-profit extension** (S902 / S903; the international face is S711, where OECD STAN carries no capital stock at all) — every post-1998 fixed-capital replication must *approximate* the asset-by-industry distribution from BEA's detailed Fixed Asset Tables (CH9 open-question 4; CH9-P2 POSITIVE).

Both walls are **correctly disclosed** across the ch7/ch9 DPRs/EPRs and are hand-verified against the Appendix-9 ground-truth workbooks (D13 PASS, score 100 for ch9). The one open defect is that the non-splice is **narrated, not machine-enforced**: `industry_index` ships as a bare `1..71` / `1..65` integer with no `classification_vintage` tag (CH9-F4 MEDIUM), so nothing mechanically prevents a downstream consumer from illegally concatenating the SIC and NAICS eras.

---

## 2. The BEA benchmark-I-O timeline (web-verified)

BEA publishes a **benchmark I-O account every 5 years** (years ending in **2** and **7**), keyed to the quinquennial Economic Census, at four detail levels: sector (~15), summary (~71), underlying-summary (~138), detail (~402–405). Detail-level estimates exist **only** for benchmark years.

| Benchmark | Classification | Industry order / detail | Notable change (RSCD-relevant) | Source |
|-----------|----------------|-------------------------|--------------------------------|--------|
| **1947** | 1957 SIC | detail (historical) | First BEA benchmark. Shaikh/Ochoa 1947 71-order cross-section. | [hist. benchmark](https://www.bea.gov/industry/historical-benchmark-input-output-tables) |
| **1958** | 1957 SIC | detail | Shaikh/Ochoa 1958. | hist. benchmark |
| **1963** | 1957 SIC | detail | Shaikh/Ochoa 1963. | hist. benchmark |
| **1967** | SIC (current) | ~478 | Shaikh/Ochoa 1967. | hist. benchmark |
| **1972** | 1972 SIC | ~496 | Shaikh/Ochoa 1972 — **last** Ochoa 71-order year Shaikh uses. Basis of ch2 **S216**. | hist. benchmark |
| **1977** | 1977 SIC | ~537 | Not in Shaikh's Ch9 panel (his set jumps 1972→1998); IS in XS2101's 295-matrix set. | hist. benchmark |
| **1982** | 1977 SIC | ~537 | SIC-era; in XS2101 set. | hist. benchmark |
| **1987** | 1987 SIC | ~498 | Anchors the 1987-SIC side of the Census SIC↔NAICS bridge; in XS2101 set. | hist. benchmark |
| **1992** | 1987 SIC | ~498 | **LAST SIC-basis benchmark. Do not splice to 1997+.** In XS2101 set. | hist. benchmark |
| **1997** | **1997 NAICS** | ~498 detail / **65-order** summary | **FIRST NAICS benchmark. Hard break vs SIC.** First to include software as investment. **Also the LAST benchmark capital-flow table** (SCB Nov 2003). | [SCB Dec 2002](https://apps.bea.gov/scb/pdf/2002/12December/1202I-OAccounts2Box27.pdf) |
| **2002** | 2002 NAICS | detail (~425/403) / summary | Into the **2009** NIPA comprehensive revision. Core of XS2101. | [SCB Oct 2007](https://apps.bea.gov/scb/pdf/2007/10%20october/1007_benchmark_io.pdf) |
| **2007** | 2007 NAICS | detail (~383/387/405) / summary (~71) / sector (~15) | **First benchmark fully integrated** with annual industry accounts + NIPAs (supply-use). Into the **2013** NIPA revision. Core of XS2101. | [benchmark I-O](https://www.bea.gov/industry/benchmark-input-output-data) |
| **2012** | 2012 NAICS | detail / summary / sector | Into the **2018** NIPA update. 2007↔2012 I-O concordance in **SCB Aug 2018 App. A**. | [SCB Aug 2018](https://apps.bea.gov/scb/issues/2018/08-august/pdf/0818-industry-text.pdf) |
| **2017** | 2017 NAICS | supply-use (detail/summary/sector) | Into the **2023** harmonized update; 2017-NAICS effects small. **Most recent benchmark** as of compile date. | [2023 NEA preview](https://apps.bea.gov/scb/issues/2023/06-june/0623-nea-preview.htm) |

**BEA's own caveat (load-bearing for RSCD):** the pre-1997 historical benchmark tables *"should not be used as a time series"* and do not reflect subsequent NIPA comprehensive revisions ([hist. benchmark I-O](https://www.bea.gov/industry/historical-benchmark-input-output-tables); [FAQ 22](https://www.bea.gov/help/faq/22)). The **1997 capital-flow table** is documented at [BEA Capital Flow Data](https://www.bea.gov/industry/capital-flow-data) and [FAQ 18](https://www.bea.gov/help/faq/18).

**Two order caveats:** (1) **Ochoa 71-order vs BEA 65-order** — Shaikh's 1947–1972 cross-sections use Ochoa (1984)'s 71-industry order (real estate excluded); his 1998 cross-section uses BEA's 65-order industry-by-industry Use table (post-redefinition), with the real-estate column corrected for owner-occupied-housing imputations via NIPA T7.12 lines 133–134. The two schemes are **not directly conformable**. (2) **NAICS-era order still drifts** — even within NAICS, summary/detail row-column order and aggregation are revised at each benchmark, so **industry indices are not stable across benchmark years**.

---

## 3. Per-series IO exposure map

| Series | Ch | Benchmark years used | Classification vintage | Fixed-capital / capital-flow use | Splice discipline |
|--------|----|----------------------|------------------------|----------------------------------|-------------------|
| **S901** | 9 | 1947,1958,1963,1967,1972,1998 | **71-order SIC** (1947–72) + **65-order NAICS** (1998) | none (circulating price object) | Non-splice; each year frozen cross-section (CH9-P1). Hand-check EXACT (`S901-A_1947F` tpm_norm ind1=0.11025038). |
| **S902** | 9 | same 6 | same 71/65 substrate | **1997 benchmark capital-flow matrix** distributes Fixed Asset Tables 3.1ES/3.4ES K,D across industries (g_j-uniform-growth) | Non-splice + **post-1997 capital-flow wall** (CH9-P2). `S902-ROBS` EXACT {1947:0.236…1998:0.1258}. |
| **S903** | 9 | same 6 | same 71/65 substrate | wage-profit curves from same fixed-capital KT eigensystem (R_t = Table 9.18) | Non-splice **+ PWT 7.1→10.01 growth-rate splice on the productivity index only** (CH9-P3, No-Lazy-Splice). |
| **S705** | 7 | NAICS-native 1987–2005; re-anchored to 1997/2002 benchmarks | **NAICS** (30-of-61 industry sample) | Fixed Assets 3.1ES(net)/3.4ES(dep) as ROP denominator | Wholly NAICS-side of the 1992/1997 wall; track sample across NAICS 1997→2022 **[→CONC]**. Extension = re-run end-to-end on one vintage, R&D/IP excluded. |
| **S706** | 7 | 1988–2005; 1997/2002 benchmarks | NAICS 30-industry | Fixed Asset 3.7ES gross investment as IROP denominator (capital-stock-FREE numerator) | Same NAICS wall; 2013 R&D/IP hits the IG denominator. Never splice. |
| **S709** | 7 | derived from S705 | NAICS 30-industry (+6 sub-aggregates → 38 panels) | inherits S705 | Always regenerate from the same S705 re-run; do not splice deviations. |
| **S710** | 7 | derived from S706 | NAICS 30-industry (38 panels) | inherits S706 | Always regenerate from the same S706 re-run. |
| **S711** | 7 | OECD STAN 2003 vintage | **ISIC Rev 3** (~27 ind., ~30 countries) | **IROP-only — STAN has NO capital stock** (international face of the post-1997 capital-flow gap) | Extension = ISIC Rev3→Rev4 crosswalk **[→CONC]** + accept 30→18 country collapse + PWT 6.2→10.01; re-aggregate end-to-end. |
| **XS2001** | 0 | 1947,1958,1963,1967,1972,1998 (+1997 capital-flow for fixed model) | **71-order SIC + 65-order NAICS** | 1997 benchmark capital-flow table (fixed-capital Table 2) | Same Ch9 walls; Sraffa price/value aggregate ratios (108 rows). Fixed-capital extension structurally blocked past 1998. |
| **XS2101** | 0 | 1977,1982,1987,1992,1997,2002,2007 (295 matrices: 176@2002 + 119@2007 nested aggregations) | **SIC (1977–92) + NAICS (1997+)** | A-matrix via Industry Technology Assumption | Curvature-index over an 8-level nested-aggregation ladder **[→CONC]**; 2012/2017 extension needs NAICS bridging + per-vintage aggregation rebuild. |
| **S216** | 2 | **1972 only** | **Ochoa 71-order, 1972-SIC** | none (direct-price scatter) | Frozen 1972 benchmark cross-section ("93% theory of price"); next benchmark is a NEW scatter, never a splice. |

**Indirect / reconstruction-only exposure (documented, not counted among the 11 direct):**
- **S214, S215** (ch2) — book series are OECD ISDB 1994 (discontinued); `io_touch` names the SIC→NAICS wall + post-1997 capital-flow gap **on any BEA-based recovery/extension**. Both `data_unavailable` for the book period.
- **S703, S704** (ch7) — OECD ISDB 1994 world/US manufacturing; `io_touch: none` directly, but a BEA continuation "hits the SIC→NAICS wall and the gross→net stock break." Both `data_unavailable`, `publish:false`.
- **S202, S203, S213** (ch2) — `io_touch: indirect` — Fixed-Asset levels / NIPA aggregates incorporate successive benchmark I-O (2002→2017), but the industry panel is off their critical path.
- **S1001** (ch10) — SIC→NAICS reclassification changes the banking definition across 1988–2005; benchmark-I-O industry accounts underlie the extension (NAICS 52 vs 5221 open) **[→CONC]**.

---

## 4. The three IO-discontinuity axes

### Axis (i) — SIC ↔ NAICS industry re-classification (the Ch9 wall)
- **Break:** last SIC benchmark 1992; first NAICS benchmark 1997. Ochoa 71-order (real-estate-excluded, SIC-vintage) vs BEA 65-order (NAICS-vintage, OOH-corrected) are non-conformable.
- **Who it blocks:** S901/S902/S903, XS2001 directly (the 1972→1998 jump in the panel); XS2101 across its 1992/1997 boundary; S216 as a single frozen year. S705/S706/S709/S710 sit wholly NAICS-side but must still track the 30-industry sample across NAICS 1997→2002→2007→2012→2017→2022 revisions.
- **RSCD handling (correct):** freeze each benchmark as a `cross_sectional` exhibit; declare non-spliceable in DPR/EPR/explainer; BEA's "not a time series" caveat cited. **CH9-P1 POSITIVE.** Residual: not machine-enforced (see §5, CH9-F4).

### Axis (ii) — Capital-flow benchmark matrix ends after 1997
- **Break:** the asset-by-industry benchmark capital-flow matrix was produced only through 1997; no benchmark table 2002+. (BEA later explored *annual* research capital-flow tables, but the fixed benchmark matrix ends at 1997.)
- **Who it blocks:** S902 & S903 fixed-capital wage-profit model (distributes Fixed Asset Tables 3.1ES/3.4ES via the 1997 matrix); XS2001 fixed-capital Table 2; **S711 is the international mirror** — OECD STAN has no capital stock, which is *why* only IROP (not average ROP) is computable OECD-wide.
- **RSCD handling (correct):** disclosed as a structural obstacle; any post-1998 fixed-capital replication must *approximate* the distribution from BEA detailed Fixed Asset Tables (type × industry) under g_j-uniform-growth — an approximation, never a data-pull. **CH9-P2 POSITIVE.**

### Axis (iii) — PWT 7.1 → 10.01 productivity re-basing
- **Break:** S903 rescales each year's wage-share curve by a Penn World Table 7.1 `rgdpwok` (real GDP/worker) index. PWT 7.1 and PWT 10.01 (2023) use different base/PPP rounds (2005 vs 2017) → **level-incomparable**.
- **Who it constrains:** S903 (primary); S711 carries the analogous PWT 6.2→10.01 bridge on its PPP factors.
- **RSCD handling (correct):** **multiplicative growth-rate splice on the productivity index only**, bridged at an overlap anchor (1998/2010), with the multiplier applied to the *freshly-derived* σ_W(r) — never to a re-scaled wr(r). This is the **No-Lazy-Splices-on-Derived-Quantities** rule. **CH9-P3 POSITIVE.** (The 1947 PWT anchor 0.322501 is itself back-extended from BEA LTEG A163 + NBER 1948/1950, EXACT.)

> A fourth, *magnitude* axis — the NIPA 2011-vintage lock (2013 R&D/IP → +$400B GDP and higher capital-stock levels; 2018 T7.11 +1 line shift; 2023 2017-benchmark supply-use) — re-vintages the levels that ride on these I-O tables. It is fully covered in the companion `NIPA_CHANGE_TIMELINE` and only cross-referenced here.

---

## 5. Concordance dependency

Every *extension* of an I-O-based series requires an industry concordance; RSCD stages the upstream authority at `docs/methodology/concordances/_sources/naics/` (Census SIC↔NAICS bridges 1987→1997→2002 and the NAICS revision chain 1997→2002→2007→2012→2017→2022, both directions, `.xls`/`.xlsx` authoritative + derived `.csv`; provenance in `_sources/SOURCES.md`). Detailed classification-bridge synthesis lives in the parallel **concordance compendium [→CONC]**; the dependencies that originate on the *I-O* side are:

- **S901/S902/S903/XS2001/S216** — SIC(71)↔NAICS(65) is **declared non-spliceable**, so no concordance is *applied* in the book period; the crosswalk authority matters only for a hypothetical benchmark-addition, and would additionally need **BEA I-O↔NAICS concordance tables** that exist only as **SCB-PDF appendix tables** (SCB Dec 2002 App. A for the 1997 I-O codes) — **not yet extracted** (see §6).
- **S705/S706/S709/S710** — NAICS-native; the 30-industry sample is tracked across NAICS vintages via the Census bridges + the Ch7-specific stability table `Inputs/Capitalism Data/Technical/Divergence_Reports/ADR-005_NAICS/data/naics_concordance_master.csv`. The 31-industry exclusion key is present (`SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv`) but **inherited by transcription, not applied in code** (review M3).
- **S711** — richest concordance case: extension onto STAN 2025 needs an **ISIC Rev 3→Rev 4** crosswalk (international analogue of SIC→NAICS) that **RSCD does not stage** (`_sources/naics/` is US-only), plus a documented 30→18 country-coverage discontinuity.
- **XS2101** — an **8-level nested-aggregation ladder** (425/383→…→15/16) plus BLS-170 + BEA-summary 71/133 crosswalks; 2012/2017 extension needs per-vintage aggregation rebuild.

**Machine-enforcement gap (CH9-F4, MEDIUM — the headline IO-side concordance defect):** `industry_index` currently ships as a **bare untagged integer** (`1..71` for the SIC era, `1..65` for the NAICS era) with **no `classification_vintage` tag**. The non-splice is asserted in prose but nothing prevents a downstream consumer from concatenating the two eras on `industry_index`. This is the single most actionable IO finding.

---

## 6. Recommendations

1. **Machine-enforce the non-splice.** Tag every industry-indexed row with a `classification_vintage` ∈ {`SIC71`, `NAICS65`, `NAICS_<year>`} field and add a loader/registry assertion that refuses to concatenate rows of differing vintage (closes CH9-F4; extends naturally to XS2001/XS2101/S216 and the ch7 NAICS panels). This converts the "narrated, not machine-enforced" wall into a hard guard.
2. **Re-label content_type for the ch7 panels (review M1).** S705/S706/S707/S708/S709/S710/S711 are registered `cross_sectional` but every EPR calls them annual `time_series`; the mislabel is what currently suppresses extension. Fix the label *and* pair it with the vintage tag so extension is gated by classification, not by a type fib.
3. **Extract the BEA I-O↔NAICS concordance appendix tables** (SCB Dec 2002 App. A for 1997 I-O codes; SCB Aug 2018 App. A for the 2007↔2012 I-O concordance) into machine-readable form **if and only if** any code-level I-O join is ever attempted. Today the non-splice discipline means they are *not* on the critical path — flag as a conditional, deferred extraction, not a gap.
4. **Stamp the capital-flow approximation.** For any post-1998 fixed-capital work (S902/S903/XS2001), require an explicit provenance note that the asset-by-industry distribution is an *approximation* from detailed Fixed Asset Tables under g_j-uniform-growth (the 1997 benchmark matrix being the last), so the approximation can never be mistaken for a benchmark data-pull.
5. **Carry an ISIC Rev3→Rev4 crosswalk + Concept-Match Justification** before any S711 extension; it is the only international classification bridge the project would need and is currently unstaged.

---

## Appendix — provenance

- Phase-0 timeline: `Technical/docs/methodology/_timelines/IO_CHANGE_TIMELINE.{md,json}` (14 benchmark years 1947→2017, web-verified).
- Methodology JSONs: `Technical/methodology_review/CH{02,07,09,10,11,XS}_methodology.json` (io_touch records) + CH03/04/05/06/08/13/14/15/16/17 (all `io_touch: none`).
- Per-series MHRs: `Technical/docs/methodology/series/S70{5,6,9},S710,S711_MHR.md`, `S90{1,2,3}_MHR.md`, `XS2001_MHR.md`, `S216_MHR.md`; dossiers `CH0{7,9}_METHODOLOGY_HISTORY.md`.
- Review cross-checks: `Technical/methodology_review/CH0{7,9}_review.json` (findings CH9-F1…F8, CH9-P1/P2/P3; ch7 H1/H2, M1–M5).
- Concordance stage: `Technical/docs/methodology/concordances/_sources/naics/` + `_sources/SOURCES.md`.
</content>
