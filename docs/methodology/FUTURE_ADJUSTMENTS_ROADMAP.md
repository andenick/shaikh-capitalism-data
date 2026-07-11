# RSCD Future-Adjustments Roadmap

**The standing forward-work register for methodology-EVOLUTION adjustments** — RSCD replication of
Shaikh, *Capitalism: Competition, Conflict, Crises* (2016).

- **Compiled:** 2026-07-01 (Phase-3 future-adjustments-roadmap agent)
- **Status:** PROPOSALS ONLY. Nothing here is implemented, wired, or scheduled. This document is READ-ONLY
  with respect to registry / code / data / Inputs; it writes only itself.
- **Aggregates (faithfully, cites paths — introduces no new claims):**
  - `docs/methodology/NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md`
  - `docs/methodology/IO_METHODOLOGY_CHANGE_COMPENDIUM.md`
  - `docs/methodology/CONCORDANCE_COMPENDIUM.md` + `docs/methodology/CONCORDANCE_BUILD_SPEC.md`
  - `docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`
  - every per-series `forward_risk` / `nipa_touch` / `io_touch` / `concordance_touch` field across
    `methodology_review/CH*_methodology.json` (16 files) and `docs/methodology/series/*_MHR.md` §6.
- **Companion (do not conflate):** `docs/reviews/REMEDIATION_BACKLOG_2026-06-30.md` — the register of
  **current defects** in the shipped v1.4 tree. This roadmap is the register of **future structural
  adjustments** forced by external methodology evolution. Cross-references to it are marked **[→BACKLOG]**.

---

## 1. Purpose & scope

RSCD froze all BEA data at Shaikh's **~2011 vintage** (Appendix 6.7 footnote 1, p.828). The book period is
therefore permanently reproducible with no external dependency: reproducing Shaikh's numbers requires only
faithful historical transcription on the classification vintage the author used
(`CONCORDANCE_COMPENDIUM.md` §1, §5.5; `NIPA_CHANGE_TIMELINE.md` "Why this matters"). **The book period will
never need anything in this document.**

What *does* evolve is the outside world. Every time BEA/Census re-benchmark the national accounts,
re-report industries, or a data provider re-bases or discontinues a series, any **live extension** of an
RSCD series past its book period is put at risk — of a silent splice across a magnitude restatement, a
broken hard-coded line number, an illegal concatenation across a classification break, or a level
re-basing. This roadmap is the standing register of the adjustments those external events will force.

**Two governing distinctions:**

1. **Evolution ≠ defect.** A current defect that is wrong *today* (e.g. the S1401 wrong-FRED-series bug,
   the S203 corrupt column, stale units labels) belongs in the **remediation backlog**, not here. This
   roadmap covers adjustments that become necessary *only when an external methodology change lands*.
   Where the two touch — e.g. the S1401 fix must land regardless, but the compensation re-benchmark that
   re-motivates it is an evolution trigger — the item is cross-referenced **[→BACKLOG]** and kept there.
2. **Trigger-driven, not calendar-driven.** RSCD does not "refresh on a schedule." Each adjustment is
   armed by a specific external event (a BEA comprehensive update, a NAICS revision, an ALFRED
   discontinuation). Until its trigger fires, the frozen book-period artifacts are correct and byte-stable.
   This register exists so that when a trigger *does* fire, the response is already specified and the
   affected series already enumerated.

**Scope boundary.** This is about *methodology evolution* of the sources. It is NOT a data-refresh cadence
(RSCD has no live web-facing feed to refresh), NOT the remediation backlog, and NOT a re-derivation of any
book number. It proposes durable capabilities and a sequenced response; it implements none of them.

---

## 2. Trigger catalogue

The external events that force RSCD adjustments. Each is *armed* by the event, not the calendar. For each:
what breaks, which RSCD series, the required response. All series/table facts trace to the cited compendia.

### T-A — Next NIPA comprehensive revision (~every 5 yr; next expected ~2028)
- **Cadence / precedent:** BEA counts 16 comprehensive updates through 2023; the modern arming events are
  **2013** (R&D/IPP capitalization, ≈+$400B GDP, FISIM restatement), **2018** (T7.11 +1 line shift,
  2012 benchmark I-O), **2023** (reference year → 2017, harmonized NIPA+IEA)
  (`NIPA_CHANGE_TIMELINE.md`; `NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md` §2). The next comprehensive update is
  expected ~2028.
- **What breaks:** (i) **magnitude restatements** — NOS/CFC/profits and Fixed-Asset/capital-stock levels
  move (2013-class concept change: IPP is a *concept discontinuity*, not a level nudge — Shaikh's 2011
  concept EXCLUDES IPP); (ii) **line renumbering** — a T7.11-class insertion shifts hard-coded line numbers
  (2018 +1); (iii) **deflator re-basing** — a reference-year change re-bases every level (2023 → 2017).
- **RSCD series:** the 38 concrete-NIPA series, concentrated in **Ch6/XS** (S601–S604, XS001–XS009 GPIM
  internals), **Ch10** (S1007, S1008), **Ch14** (S1401, S1403–S1408), **Ch15** (S1504–S1507), plus scattered
  T7.11/T7.12 users in Ch2/3/7/9/16 (`NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md` §3 table).
- **Required action:** never splice across the revision boundary; re-compute any live extension
  **end-to-end on one coherent vintage**; resolve renumbering-prone rows (T7.11, T1.16, T7.12, T1.10) by
  BEA `LineDescription` **stub label**, never by line number; take an explicit IPP stance on any Fixed-Asset
  re-pull (Shaikh excludes it); treat growth-rate concepts (log-differences) as robust to re-basing but any
  series carrying a **level** as needing full re-derivation on the new base
  (`NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md` §5).

### T-B — Next BEA benchmark I-O release + any classification change
- **Cadence / precedent:** BEA publishes a benchmark I-O account **every 5 years** (years ending 2 and 7),
  keyed to the Economic Census. Most recent = **2017**; next benchmarks **2022** and **2027**
  (`IO_CHANGE_TIMELINE.md`). Each benchmark **re-orders/re-aggregates** summary and detail industries even
  within NAICS — industry indices are **not stable across benchmark years**.
- **What breaks:** the industry order/aggregation under every I-O-based series moves; a benchmark that also
  carries a NAICS vintage change (see T-C) additionally breaks the classification. The two irreducible
  walls (§5) are NOT reopened by any future release — BEA will not republish a pre-1997 SIC-basis benchmark
  as a time series, nor a post-1997 benchmark capital-flow matrix.
- **RSCD series:** the 11 direct-benchmark-I-O series — **Ch9** S901/S902/S903; **Ch7** S705/S706/S709/S710/S711;
  **XS** XS2001/XS2101; **Ch2** S216 (`IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §1, §3).
- **Required action:** keep each benchmark a **frozen cross-section** (the correct RSCD discipline —
  CH9-P1/P2 POSITIVE); for the NAICS-side ch7 panels, **track the 30-industry sample** across the new
  benchmark via the ADR-005 stability table + Census bridges and **re-run end-to-end on one vintage**
  (R&D/IP excluded, aggregate-before-ratio, vintage stamped); for the XS2101 nested-aggregation ladder,
  rebuild per-vintage aggregation. Never concatenate the new benchmark onto an old-classification segment.

### T-C — NAICS revision (2027 cycle)
- **Cadence / precedent:** NAICS revised on a 5-year cycle: 1997 → 2002 → 2007 → 2012 → 2017 → **2022** →
  **2027** (next). For Shaikh's 3-digit sample most revisions are Stable/Minor; the volatile cells are
  Computers-electronics (334), Publishing (511), Data-processing (518), Non-store retail (454); the
  1997/2002 revision was the largest (`CONCORDANCE_COMPENDIUM.md` §2.2, ADR-005 table).
- **What breaks:** the 30-industry ch7 profit-rate panel and any NAICS-native series can shift industry
  membership; a many-to-many re-mapping needs share weights the bridge does not supply.
- **RSCD series:** **Ch7** S705/S706/S709/S710 (30-industry panel); **Ch10** S1001 (banking 52-vs-5221);
  **Ch15** S1502/S1503; **Ch8** S801–S805 (extension only — none applied in book)
  (`CONCORDANCE_COMPENDIUM.md` §3).
- **Required action:** re-map via the staged **Census revision chain** (`_sources/naics/`, 1997→2022 both
  directions) + the ADR-005 stability table; resolve by **code + title** with an explicit part-indicator,
  never a presumed 1:1 map; where a cell is many-to-many, flag `confidence:approximate` and require a
  share-based allocation decision (`CONCORDANCE_BUILD_SPEC.md` §1, §4.3). Extension of ch8 concentration
  series stays **flagged, not performed**, until share weights exist.

### T-D — ALFRED/FRED series discontinuation or re-basing
- **What breaks:** RSCD's extension candidates are **current-vintage FRED mirrors** with **no ALFRED
  vintage pin** — S1007/S1008 (Ch10), S1401/S1406–S1408 (Ch14), S1504–S1507 (Ch15). A provider
  discontinuation (a FRED series id retired) or a re-basing (a BEA-sourced FRED series absorbing a
  comprehensive revision) silently changes the fetched values, and because the mirrors straddle all three
  comprehensive boundaries a naive re-fetch splices across them
  (`NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md` §6.1; CH10 S1007 `forward_risk`).
- **RSCD series:** every live/candidate extension that fetches from FRED — Ch10 S1007/S1008 (deferred),
  Ch14 S1401 (active [→BACKLOG]) + S1406–S1408, Ch15 S1504–S1507; plus source-mirror concordances
  (Fed HS-39 → FRED AAA; BLS WPI → PPIACO; Shiller → FRED GS10) across Ch10.
- **Required action:** fetch via a **pinned ALFRED vintage** (or BEA Data API with `vintage_year` logged)
  and record `vintage_year` in provenance; concept-lock each mirror by the source's *concept*, not its
  provider string id (WPI→PPI, IFS→SDMX are concept-preserving renames — `CONCORDANCE_BUILD_SPEC.md` §1);
  on a discontinued id, resolve to the successor by concept and log the seam, never silently substitute.

### T-E — OECD STAN / ISDB + PWT new releases
- **What breaks:** (i) OECD **ISDB is discontinued** with no drop-in successor; **STAN** is on ISIC and its
  country coverage **collapses 30 (2003) → 18** in later vintages (drops Canada/UK; book p.859 V.3);
  (ii) an **ISIC Rev3 → Rev4** classification break (the international analogue of SIC→NAICS) that RSCD does
  **not stage** (`_sources/naics/` is US-only); (iii) **PWT re-basing** — S903 rides a PWT 7.1 `rgdpwok`
  index and S711 a PWT 6.2 bridge; PWT 10.01 (2023) uses a different PPP round (2017 vs 2005), so levels are
  **incomparable** (`IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §4 axis (iii); `CONCORDANCE_COMPENDIUM.md` §2.3, §4.3).
- **RSCD series:** **Ch7** S711 (richest international case), S703/S704 (retired ISDB, `data_unavailable`);
  **Ch9** S903 (PWT productivity index), S902/S903 (PWT growth-rate splice); **Ch2** S213/S214.
- **Required action:** carry an **ISIC Rev3→Rev4 crosswalk + Concept-Match Justification** before any S711
  extension (the only international bridge the project needs, currently unstaged); accept the documented
  30→18 country collapse as a coverage wall; apply PWT re-basing as a **multiplicative growth-rate splice on
  the productivity index only**, bridged at an overlap anchor, applied to the *freshly-derived* σ_W(r) —
  never to a re-scaled wr(r) (the No-Lazy-Splices-on-Derived-Quantities rule, CH9-P3 POSITIVE).

### T-F — IMF SDMX portal changes
- **What breaks:** IMF migrated IFS to an **SDMX** portal; a portal/endpoint or dataflow-id change breaks
  any IFS-concept fetch. RSCD treats **IFS → SDMX** as a within-agency source-code remap (concept
  preserved), catalogued with `needs_crosswalk_for_extension = FALSE`
  (`CONCORDANCE_COMPENDIUM.md` §2.6, §3).
- **RSCD series:** the IMF-sourced series (e.g. S1504 GDP-agency ambiguity IMF-IFS vs NIPA T1.1.5 — CH15 F11
  [→BACKLOG]); low blast-radius, no industry dimension.
- **Required action:** resolve by **concept id** (agency + concept), not the discontinued provider string;
  log the endpoint/dataflow change in provenance; no classification crosswalk needed.

---

## 3. Per-trigger series impact matrix

Trigger → affected RSCD series (from the compendia + `forward_risk` records) → adjustment type → severity.
**Adjustment types:** `RECOMPUTE` = re-run end-to-end on one coherent vintage · `RE-ANCHOR SPLICE` =
growth-rate/overlap-anchored splice on a derived quantity · `RE-MAP` = classification/line concordance
resolve · `RE-PIN VINTAGE` = pin to an ALFRED/BEA `vintage_year`. **Severity:** HIGH = load-bearing for a
book figure or compounds downstream · MED · LOW = documentary/robust-as-growth-rate.

| Trigger | Affected RSCD series | Adjustment type | Severity | Source |
|---|---|---|---|---|
| **T-A** NIPA comprehensive (2013-class concept) | Ch6 S601–S604 + XS004–XS009 (Fixed-Asset/GPIM denominator; IPP concept discontinuity) | RECOMPUTE (explicit IPP stance) | **HIGH** | NIPA-COMP §5; CHXS `forward_risk` |
| **T-A** NIPA comprehensive (T7.11 +1 renumber) | S601–S604, S1007, S1008, S1604, XS003; + T7.11 users S213/S216/S301/S705/S706/S709/S901–903/S1505 | RE-MAP (stub-label resolve) | **HIGH** | NIPA-COMP §3,§4; CONC §3 |
| **T-A** NIPA comprehensive (2023-class re-base) | Ch15 S1504–S1507; Ch10 S1007 real conversion; Ch14 GDPDEF users S1406–S1408 | RE-PIN VINTAGE + RECOMPUTE levels | MED (growth-rates robust) | NIPA-COMP §5 |
| **T-A** (income-side line 2) | Ch14 S1401/S1403–S1408 (T1.10 compensation/NOS residual) | RE-MAP (T1.10 label) + RECOMPUTE | **HIGH** (active F1 [→BACKLOG]) | NIPA-COMP §5; CH14 F1 |
| **T-B** BEA benchmark I-O (order re-report) | Ch9 S901/S902/S903, XS2001; Ch7 S705/S706/S709/S710; XS2101 ladder | RECOMPUTE (frozen cross-section; sample tracked) | **HIGH** | IO-COMP §3,§4 |
| **T-B** (capital-flow-dependent) | S902/S903, XS2001 fixed-capital model | RECOMPUTE via **approximation** (1997 matrix is last — §5 wall) | **HIGH** | IO-COMP §4 axis(ii) |
| **T-C** NAICS 2027 revision | Ch7 S705/S706/S709/S710 (30-ind panel); Ch10 S1001; Ch15 S1502/S1503; Ch8 S801–S805 (ext only) | RE-MAP (Census chain + ADR-005) | MED (mostly Stable/Minor) | CONC §2.2,§3 |
| **T-D** ALFRED/FRED discontinue / re-base | Ch10 S1007/S1008; Ch14 S1401/S1406–S1408; Ch15 S1504–S1507 | RE-PIN VINTAGE | **HIGH** (precondition to un-defer S1007/S1008) | NIPA-COMP §6.1; CH10 `forward_risk` |
| **T-E** OECD STAN/ISDB + PWT | Ch7 S711, S703/S704; Ch9 S903 (PWT); Ch2 S213/S214 | RE-MAP (ISIC Rev3→Rev4) + RE-ANCHOR SPLICE (PWT) | **HIGH** (S711); MED (S903) | IO-COMP §4(iii); CONC §4.3 |
| **T-F** IMF SDMX portal | S1504 (IMF-IFS); other IMF-sourced | RE-MAP (concept id, no classification) | LOW | CONC §2.6 |

**Non-exposed:** 72 series carry an explicit `NONE`/`NOT APPLICABLE`/indirect `nipa_touch` and are out of
the vintage-drift blast radius (BLS/CPS labor, PWT/IMF/OECD aggregates, Jastram/MeasuringWorth gold-and-price,
closed-form theoretical illustrations e.g. S1301, pre-modern-NIPA compilations); the frozen-wall exhibits
S701 (pre-SIC), S702 (UK SIC 1958), S707/S708 (Greek ISIC→NACE figure recoveries) have **no numeric
extension** at all (`NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md` §3; CH07 `forward_risk`).

---

## 4. Standing structural investments (proposals, prioritized)

The durable capabilities that make future adjustments cheap. Each: what it unblocks · effort · dependency.
**Proposals only — none wired this pass.**

### SI-1 — ALFRED vintage pinning + a vintage manifest  *(top leverage)*
- **What it is:** every live NIPA/FRED fetch pins an **ALFRED `vintage_year`** (or BEA Data API vintage) and
  records it in provenance; a project-level **vintage manifest** records, per extended series, which vintage
  each input was drawn on. No RSCD series carries a vintage pin today — the Ch10/14/15 extension candidates
  are current-vintage mirrors straddling all three comprehensive boundaries.
- **Unblocks:** the precondition for un-deferring **S1007/S1008** (Ch10) and for any Ch14/Ch15 extension;
  makes the anti-splice rule *enforceable* rather than aspirational; arms the T-A and T-D responses.
- **Effort:** Medium (loader-side fetch change + manifest schema; no new external data).
- **Dependency:** none — this is the foundational precondition; SI-3 and the T-A/T-D responses depend on it.
- **Source:** `NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md` §6.1; CH10 S1007/S1008 `forward_risk`.

### SI-2 — Generalized label/code resolver (per `CONCORDANCE_BUILD_SPEC`)  *(second leverage)*
- **What it is:** promote the working `_nipa_t711_line_resolver.py` pattern (resolve by a **persistent
  semantic key**, not a positional index) into a single generic module over three canonical CSVs —
  `line_label_index.csv` (NIPA lines: T7.11 + T1.10 + T2.1/Z.1), `concordance_edges.csv` (SIC/NAICS/ISIC/IO
  edges with cardinality + part-indicator + allocation weight), `scheme_registry.csv` (with
  `frozen`/`staged`/`not_staged` flags). Every resolve returns a provenance record and a cardinality/confidence
  flag so lossy maps are visible.
- **Unblocks:** the T-A line-renumbering response (8 NIPA series via P1), the T-C NAICS re-map (~13 series via
  P2), the T-B I-O wall (5 series via P3, conditional), the T-E international bridge (P4); would have caught
  the F1 wage/compensation mix-up at fetch time.
- **Effort:** P1+P5 Low, P2 Medium, P3/P4 High (see §6 phasing).
- **Dependency:** none for P1/P5; P3 needs the SCB-PDF extraction; P4 needs the external ISIC correspondence.
- **Source:** `CONCORDANCE_BUILD_SPEC.md` §1–§5; `CONCORDANCE_COMPENDIUM.md` §6.

### SI-3 — Machine-enforced non-splice guards  *(third leverage)*
- **What it is:** convert the "narrated, not machine-enforced" walls into hard guards — (i) a
  **`classification_vintage`** tag on every industry-indexed row (∈ {`SIC71`, `NAICS65`, `NAICS_<year>`})
  with a loader/registry assertion refusing to concatenate differing vintages (closes **CH9-F4**); (ii) a
  **comprehensive-revision seam guard** that fails any extension concatenating segments whose source
  vintages cross a 2013/2018/2023 boundary; (iii) renumbering-resolvers surface `data_unavailable` on a
  row split rather than absorbing it.
- **Unblocks:** makes the frozen-cross-section discipline (S901/902/903, XS2001/XS2101, S216) and the
  no-splice rule (all 38 NIPA series) *impossible to violate downstream*; the single most actionable IO-side
  investment.
- **Effort:** Low–Medium (a tag field + assertions).
- **Dependency:** SI-1 (vintage pin supplies the NIPA seam) + SI-2 `scheme_registry.csv` (supplies the tag
  vocabulary); the T4.4 `classification_vintage` decision [→BACKLOG] must be ratified first.
- **Source:** `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §5,§6.1; `NIPA_METHODOLOGY_CHANGE_COMPENDIUM.md` §6.3;
  `CONCORDANCE_BUILD_SPEC.md` §4.4.

### SI-4 — Independent V03 reference anchors
- **What it is:** wire the already-verified **non-circular in-book anchors** (Table 6.24 S604; Table 9.18
  S903; Table 10.1/10.2 S1006/S1007; Harberger/Ramamurthy S1508/S1509; S1405 Phillips a/c/R²; S1408
  Table 14.3) into V03 as independent `reference_values` checks, plus **post-2011 splice-continuity +
  level-plausibility** checks so extensions are validated PAST the book period. Today V03 round-trips the
  same source the chopped is melted from — `MAE=0` is melt-fidelity, structurally blind to wrong-source
  (S1401) and corrupt-source (S203) defects.
- **Unblocks:** makes every future extension *actually* validated rather than tautologically re-blessed;
  the precondition for trusting any T-A/T-B/T-C recompute. (Ties directly to the tautological-V03 finding.)
- **Effort:** Medium (per-series anchor wiring + two new check types).
- **Dependency:** the T4.1 anchors/tolerance decision [→BACKLOG] — and this must land **before**
  re-validating any recomputed extension, else the new numbers are re-blessed by a tautological validator.
- **Source:** `REMEDIATION_BACKLOG_2026-06-30.md` T4.1 (cross-cutting theme #2) — the *forward* use here is
  validating extensions; the *current* wiring task is tracked in the backlog **[→BACKLOG]**.

**Top-3 by leverage:** **SI-1** (vintage pinning — foundational precondition for every live extension),
**SI-2** (generalized resolver — unblocks the most series across the most triggers), **SI-3** (non-splice
guards — makes the whole freeze-discipline unbreakable).

---

## 5. The two irreducible walls

Two obstacles are **NOT resolvable by any future BEA release** — BEA discontinued the underlying products.
No comprehensive update, benchmark, or NAICS revision reopens them. RSCD's honest ceiling on both is
**freeze-as-cross-section**; set expectations accordingly and never let a future maintainer wait for a
release that will not come.

### Wall 1 — The pre-1997 SIC-era I-O *code* concordance
- **What:** the Ochoa 71-order (SIC) ↔ BEA detail-code mapping behind Ch9's 1947/1958/1963/1967/1972
  historical cross-sections. BEA's last SIC-basis benchmark is **1992**; its first NAICS-basis benchmark is
  **1997**; BEA states the pre-1997 historical benchmark tables **"should not be used as a time series."**
  The Ochoa-71 and BEA-65 orders are **not conformable**.
- **Why irreducible:** BEA will not republish a SIC-basis benchmark, and no in-project SIC-era I-O *code*
  concordance is staged (nor exists in staged form anywhere). A continuous 1947–1998 industry I-O panel is
  **not reconstructable** (CH9 open-Q3).
- **RSCD ceiling:** each benchmark stays a **frozen exhibit**; S901/S902/S903, XS2001, S216 are
  cross-sections, never a spliced panel. This is correct, not a gap.
- **Source:** `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §1,§4(i),§5; `CONCORDANCE_COMPENDIUM.md` §5.3;
  `CONCORDANCE_BUILD_SPEC.md` §5 (explicitly out of scope).

### Wall 2 — The post-1997 benchmark capital-flow matrix
- **What:** the benchmark **capital-flow table** (use-type × using-industry matrix distributing new
  equipment/software/structures investment across industries) — the machinery S902/S903/XS2001 use to
  distribute Fixed Asset Tables 3.1ES/3.4ES across industries. Produced for the last time for **1997**
  (SCB Nov 2003, seventh and last); **no benchmark capital-flow table exists for 2002 or later.**
- **Why irreducible:** BEA discontinued the benchmark matrix after 1997 (later exploring only *annual*
  research tables, not the fixed benchmark asset-by-industry matrix). Its international mirror is **S711** —
  OECD STAN carries **no capital stock at all**, which is *why* only IROP (not average ROP) is computable
  OECD-wide.
- **RSCD ceiling:** any post-1998 fixed-capital replication must **approximate** the asset-by-industry
  distribution from BEA's detailed Fixed Asset Tables under g_j-uniform-growth — an approximation, **never a
  data-pull**, and it must be stamped as such so it can never be mistaken for a benchmark.
- **Source:** `IO_METHODOLOGY_CHANGE_COMPENDIUM.md` §1,§4(ii),§6.4; `IO_CHANGE_TIMELINE.md`
  "Capital-flow benchmark matrix — discontinued after 1997"; `CONCORDANCE_COMPENDIUM.md` §4.2.

> **Expectation-setting.** For Ch9's historical panel and the fixed-capital wage-profit model, "wait for the
> next BEA release" is never the answer. The frozen cross-sections and the stamped approximation ARE the
> honest ceiling. The only capability the walls justify building is the **stamping/guarding** of SI-3, so the
> freeze can never be silently violated.

---

## 6. Sequenced roadmap

A phased proposal. Each phase names its dependencies and which extensions it unblocks. **Proposals only;
sequencing follows `CONCORDANCE_BUILD_SPEC.md` §5 (P1 → P5 → P2 → P3 → P4) and the compendia recommendations.**

### Phase N (near-term) — vintage pinning + resolver generalization  *(low effort, high leverage)*
- **Do:** **SI-1** (ALFRED vintage pin + vintage manifest); **SI-2 P1** (`line_label_index.csv` + port the
  T7.11 resolver into the generic module; add T1.10 for Ch14 and Z.1 D.3 / T2.1 for Ch16 S1605); **SI-2 P5**
  (`scheme_registry.csv` with `frozen`/`staged`/`not_staged` flags — the cheap coverage-gate enabler).
- **Unblocks:** the T-A line-renumbering response for **8 series** (S601–S604, S1007, S1008, S1604, XS003) +
  hardens Ch14/Ch16; makes S1007/S1008 *technically* re-fetchable (with SI-1); arms the T-D response.
- **Dependencies:** none external — the working resolver + `NIPA_T711_FISIM_remap.md` already encode T7.11;
  the pinned vintages (2011/2018/2024) exist. Ratify T4.4 (`classification_vintage`) [→BACKLOG] alongside.
- **Also stand up SI-3(i/ii)** here once T4.4 is ratified (Low effort, and it depends on SI-1 + P5).

### Phase M (medium-term) — concordance materialization (build-spec P2–P3)
- **Do:** **SI-2 P2** — materialize `concordance_edges.csv` for the US Census SIC↔NAICS + NAICS revision
  chain from the 14 staged CSVs, with `cardinality` + `part_indicator` (the `sic_naics_bridge_seed.csv` is
  the pilot). Then **SI-2 P3** (conditional) — extract the BEA I-O↔NAICS concordances from the SCB PDF
  appendices (SCB Dec 2002 = 1997 codes; Oct 2007 = 2002; Aug 2018 = 2007/2012) to CSV, **only if** a
  code-level I-O join is ever attempted.
- **Unblocks:** P2 → the T-C NAICS re-map for **~13 series** (Ch7 S705/706/709/710, Ch8 S801–805, Ch10
  S1001, Ch15 S1502/1503); P3 → the T-B I-O wall (**5 series** S901–903, XS009, XS2101 — the ladder).
- **Dependencies:** P2 is mechanical (source staged). **P3 is High effort** (PDF-table extraction via
  fullread/Sraffa; URLs only, not staged) and is a *conditional, deferred* extraction — the non-splice
  discipline keeps it off the critical path until a join is actually attempted. Wire **SI-4** (independent
  V03 anchors) in this phase so P2/P3 recomputes are validated non-tautologically; T4.1 [→BACKLOG] gates it.

### Phase L (long-term) — live IO / Sraffa recompute
- **Do:** **SI-2 P4** — the ISIC Rev3→Rev4 crosswalk + Concept-Match Justification for the international
  frontier (S711, S213/214, S703/704); the full GPIM live-recompute (XS004/XS005/XS006 end-to-end,
  exercising `compute_AS003_recipe`) and any live Sraffa/IO recompute.
- **Unblocks:** T-E (S711 international extension); the Ch6/XS end-to-end recompute path.
- **Dependencies (hard gates):** P4 needs the **external** UN/OECD ISIC correspondence (not staged) +
  bespoke per-label hand-mapping + acceptance of the 30→18 country collapse. The **XS006 depreciation
  recompute is gated on the BEA-1993 SCB Table A.13 finite-life archive** being sourced [→BACKLOG,
  out-of-scope]. The two **§5 walls remain closed** — the pre-1997 SIC I-O code concordance and the
  post-1997 capital-flow matrix are *not* build items in any phase; Ch9's historical panel and the
  fixed-capital model stay frozen/approximated forever.

**Dependency summary:** SI-1 (vintage pin) → SI-2 P1/P5 (resolver + registry) → SI-3 (guards) →
SI-2 P2 (Census edges) → SI-4 (anchors, gated on T4.1) → SI-2 P3 (I-O appendix, conditional) →
SI-2 P4 + GPIM live recompute (gated on external ISIC + the BEA-1993 archive). The two §5 walls never enter
the chain.

---

*Compiled read-only. This roadmap aggregates the Phase-3 compendia, the Phase-0 timelines, and the
per-series `forward_risk`/`*_touch` records, and cites their source artifacts for every claim; it introduces
no new methodology claims and implements nothing. Current defects live in
`docs/reviews/REMEDIATION_BACKLOG_2026-06-30.md`; this file is the forward register of methodology-evolution
adjustments.*
