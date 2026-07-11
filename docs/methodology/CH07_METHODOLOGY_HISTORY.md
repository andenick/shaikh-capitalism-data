# Chapter 7 — Methodology History: The Industry-Classification Through-Line

**Book**: Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (2016), Chapter 7 — *The Theory of Real Competition* (profit-rate equalization).
**Series**: S701–S711 (11) · Group `ch07`/`CH07`.
**Compiled**: 2026-06-30 (RSCD Phase-2 methodological-historian agent), reasoning from Shaikh's perspective.
**Per-series MHRs**: `Technical/docs/methodology/series/S70{1..9}_MHR.md`, `S71{0,1}_MHR.md`.
**Phase-0 references cited throughout**: `_timelines/IO_CHANGE_TIMELINE.md`, `_timelines/NIPA_CHANGE_TIMELINE.md`, `concordances/_sources/SOURCES.md` + `concordances/_sources/naics/`.
**This pass's review**: `Technical/methodology_review/CH07_review.json` (integration 82, ADEQUATE).

---

## Why Chapter 7 is the prime concordance case

Chapter 7 is the most **industry-classification-intensive** chapter in the whole replication because its single empirical claim — that regulating capitals turbulently **equalize incremental profit rates** while average rates persistently differ — can only be tested by comparing profit rates **across industries**, and every such comparison is hostage to *how industries are defined*. Shaikh assembles the case at three levels of aggregation and across five distinct statistical vintages, and each vintage carries its own classification scheme:

| Tier | Series | Arena | Classification vintage | Source |
|------|--------|-------|------------------------|--------|
| Price/cost cross-sections | S701, S702 | US 1923–50, UK 1954–63 | **pre-SIC** US categories; **UK SIC 1958** (the chapter's only SIC citation) | Salter (1969) Tables 33/28 |
| World / US manufacturing rates | S703, S704 | 8-country world; US mfg | **OECD ISDB 1994** codes (discontinued) | Christodoulopoulos (1995) |
| US 30-industry NIPA rates | S705, S706, S709, S710 | US | **NAICS** (1997→2022 revisions) | BEA GDPbyInd + Fixed Assets / Shaikh (2008) |
| Greek 20-industry rates | S707, S708 | Greece | **2-digit ISIC** (ESYE→ELSTAT break) | Tsoulfidis & Tsaliki (2011) |
| OECD-wide incremental rates | S711 | ~30 OECD countries | **ISIC Rev 3** (→Rev 4 on extension) | OECD STAN 2003 + PWT 6.2 |

No two tiers share a classification scheme, and **not one of them is conformable to the modern US NAICS chain** that RSCD stages officially (`concordances/_sources/naics/`, an unbroken 1987 SIC → 1997 → 2002 → 2007 → 2012 → 2017 → 2022 NAICS bridge). That is the through-line: Chapter 7 is a museum of incompatible industry taxonomies, and the replication's honesty depends on never pretending they splice.

## The SIC↔NAICS story, told through the series

Shaikh himself lives the SIC→NAICS break inside the chapter. For the historical US (S704, 1960–89) he uses OECD ISDB codes on **gross** capital stock; when he moves to the modern US (S705/S706, 1987–2005) he switches to **BEA GDPbyIndustry on NAICS with net stock**, and *starts a fresh construction in 1987 rather than extending Fig 7.14* — an author-level decision that encodes the non-conformability the Phase-0 `IO_CHANGE_TIMELINE.md` documents ("last SIC benchmark = 1992; first NAICS benchmark = 1997; the pre-1997 tables should not be used as a time series"). The US tier (S705/S706/S709/S710) is therefore **NAICS-native from birth** and sits wholly on the NAICS side of the wall — but its 30-industry sample must still be tracked across NAICS *revisions* (1997→2022), for which RSCD holds both the official Census bridges (`_sources/naics/`) and a Ch7-specific stability table (`Inputs/Capitalism Data/Technical/Divergence_Reports/ADR-005_NAICS/data/naics_concordance_master.csv`, NAICS 2002–2022 change flags for exactly this sample).

The **UK SIC 1958** heading on Salter's Table 28 (S702) is the chapter's only literal SIC reference, and it is instructive precisely because it is used as a **row label, not a mapping** — a reminder that a classification code can appear in the data without ever being operationalised as a crosswalk. The pre-SIC US categories in Salter's Table 33 (S701) fall off the *bottom* of the concordance chain (the official bridges begin at 1987 SIC); they are an irrecoverable classification wall.

## The 30-vs-31 industry panel — the chapter's central classification act

The most consequential classification decision in Chapter 7 is Shaikh's own: from the 61 NAICS private industries in BEA GDPbyIndustry he **excludes 31 and retains 30**, "with a concomitant redefinition of the overall rate of profit" (book p. 858). The exclusion is theory-driven — keep only industries "dominated by profit-driven enterprises and also competitive on a world scale" — on four grounds captured in the recovered key `SalvagedInputs/book_data/Reconstructed/Shaikh_2008_Appendix_B_industries.csv` (extracted verbatim from **Shaikh 2008 Table 9.A1, p. 190**): non-profit-dominated (arts, education, social services), inadequate-WEQ-data (legal, medical, computer services), internationally-noncompetitive (textiles, mining, domestic oil), and low-or-negative period-average rate. This CSV **resolves `CH7_RESEARCH_SUMMARY.md` open-question #2** (the exclusion list was thought missing). The 30 retained industries = the NAICS rows *not* in the CSV, and the All-Private aggregate baseline (used for every deviation in S709/S710) is defined over exactly those 30 — so a change to the exclusion set moves *every* deviation. RSCD **inherits** this reduction by transcribing Shaikh's already-reduced Appendix 7.2 panels rather than applying the CSV as a code filter (review M3) — faithful, but the registry `components[]` overstate the executed pipeline.

Layered on top of the exclusion are Shaikh's four **accounting adjustments** — WEQ (self-employed wage-equivalent; Construction 90.5%→20.7%), OOH removal (Real Estate ~55.5% of GOS, ~76% of K stripped), normal-inventory additions, and bank/insurance reserve additions (Banking 41.8%→17.7%) — every one of which is a cross-industry-*comparability* device: without them, the "industries" being compared are artefacts of NIPA imputation conventions rather than competitive arenas. These, too, are baked into `ropdataUSind`/`iropdataUSind`, not recomputed in RSCD code.

**See also:** `PRODUCTION_BOUNDARY_ACROSS_CLASSIFICATION_ERAS.md` — this NAICS-era 31-industry exclusion key is one of three different production-boundary implementations across RSCD (Ch6 NIPA-sector / Ch7 industry / Ch9 whole-economy); it exists only on the NAICS side of the wall and must never be back-cast across the SIC↔NAICS break.

## BEA benchmark re-reporting and the NIPA vintage wall

Even within NAICS, industries are not stable. `IO_CHANGE_TIMELINE.md` records that BEA re-anchors GDPbyIndustry to the quinquennial benchmark I-O accounts (1997 first NAICS benchmark; 2002/2007/2012/2017), each re-ordering and re-aggregating the summary/detail industry rows — so **industry indices are not comparable across benchmark years**. And `NIPA_CHANGE_TIMELINE.md` fixes the deeper trap: Shaikh's vintage is **2008 (≈2011)**, but the **2013 comprehensive revision capitalizes R&D/IP** — raising Fixed-Asset/capital-stock levels (the S705 denominator) *and* gross-investment levels (the S706/S710 denominator) — while the **2018 revision** re-reports GDPbyIndustry and inserts a **+1 line shift in NIPA T7.11** (resolver `NIPA_T711_FISIM_remap.md`), and **2023** re-references to 2017. The chapter-wide anti-degradation rule (CH7 open-question 5) follows directly: **any extension past the book period must be recomputed end-to-end on a single coherent vintage with R&D/IP excluded — never spliced across a comprehensive-revision boundary.** The deviation series (S709/S710) inherit this one-for-one and must always be regenerated from their parents' re-run.

## The international breaks: ISDB discontinuation and ISIC Rev 3→Rev 4

The non-US tiers carry the classification story abroad. The world/US ISDB panels (S703/S704) are `data_unavailable` — honestly blocked, chart-only, with the raw Christodoulopoulos file unrecoverable — and their would-be reconstruction faces the **ISDB→STAN source discontinuity plus an ISIC Rev 3→Rev 4 crosswalk** and a gross→net capital-stock concept break. The Greek panels (S707/S708) ride the **ESYE→ELSTAT agency transition with an ISIC→NACE Rev 2 reclassification**. And S711, Shaikh's own OECD-wide construction, is the **richest international concordance case in the chapter**: it is built on **OECD STAN 2003 (ISIC Rev 3) + PWT 6.2 PPP**, and Shaikh *on the record* documents a source-vintage discontinuity — the 2003 vintage covered ~30 countries, "the subsequent version … covered only eighteen … and excluded even those such as Canada and the United Kingdom" (book p. 859). Extending S711 means absorbing three simultaneous breaks: ISIC Rev 3→Rev 4, a 30→18 country-coverage collapse, and PWT 6.2→10.01 — with **no ISIC concordance staged in-project** (RSCD's `_sources/naics/` is US-only). It is also the chapter's clearest example of classification *forcing method*: STAN carries no capital stock (the international face of the post-1997 capital-flow-matrix gap in `IO_CHANGE_TIMELINE.md`), so only the **incremental** rate is computable OECD-wide — there is deliberately no OECD analogue of the average-rate figures.

## Replication fidelity — what "reproduced" means here

Across all three extractable tiers, RSCD's fidelity is **transcription of an already-fixed artifact**, not end-to-end recompute, and the report is honest about which:
- **Byte-exact transcription of Shaikh's adjusted/aggregated panels** (V03 MAE 0.0): S705/S706 (`ropdataUSind`/`iropdataUSind`, adjustments + exclusion baked in), S709/S710 (Shaikh's pre-computed `_Deviation`/`_Dev` columns — review M2), S711 (`iropOECDPPP`, STAN aggregation + PPP baked in).
- **Byte-exact transcription of a frozen historical table**: S701/S702 (Salter panels; note the file-naming and subsource-key swaps, review L2/L3).
- **Disclosed figure-digitization recovery** (No-Synthetic-compliant, faithful to the published figure not the authors' table): S707 (higher confidence — low-frequency average curves; point-precision verified top row) and S708 (lower confidence — high-frequency incremental curves; MINOR_DEV on per-point precision), both recovered 2026-05-26 from **MPRA 51334**. *Honesty debt (review H1/H2): the S707/S708 research JSONs + EPRs/DPRs are stale — still `data_unavailable` / "No digitization" — and a stale marker persists in the replicator bundle; these need reconciliation.*
- **Honest `data_unavailable`** (loader SKIP, V03 `PASS_DATA_UNAVAILABLE`, `publish: false`, marker file present): S703/S704 — no proxy, no memory fill, recovery only via guided WebPlotDigitizer of the aggregate line (project CLAUDE.md anti-pattern #5; D13 gate PASS).

A cross-cutting classification note the review flags (M1): the registry marks the annual panels S705–S711 `content_type: cross_sectional`, but every EPR treats them as `time_series` (genuine year axis) — a label mismatch that also suppresses extension eligibility, worth correcting.

## The forward-risk map

- **US tier (S705/S706/S709/S710)** — highest extension exposure: next BEA benchmark/NAICS re-classification re-orders the 30-industry sample (track via the ADR-005 stability table); the post-2013 R&D/IP capitalization is a standing capital-concept trap on both the stock (ROP) and investment (IROP) sides; Z.1 Flow-of-Funds line numbers have drifted. Re-run end-to-end on one vintage, R&D/IP excluded, deviations regenerated from the parent.
- **S711** — three simultaneous international breaks (ISIC Rev3→Rev4, 30→18 countries, PWT 6.2→10.01); build the ISIC crosswalk RSCD does not stage; carry an explicit Concept Match Justification for the country-coverage collapse.
- **S703/S704** — recover only by disclosed digitization; a data reconstruction would be a *new* exhibit, not a reproduction.
- **S707/S708** — no numeric extension; any modern Greek panel is a separate NACE Rev 2 exhibit; near-term action is documentary (reconcile stale docs).
- **S701/S702** — frozen; no vintage risk; only reconcile the Table 28/33 + page 164/197 label desync and preserve original industry labels.
