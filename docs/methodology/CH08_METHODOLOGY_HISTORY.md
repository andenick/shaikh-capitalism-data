# Chapter 8 — Methodology History: The Anti-Oligopoly Dossier (Reproductions Turned Against the Concentration-Profitability School)

**Book**: Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (2016), Chapter 8 — *On Perfect and Imperfect Competition*, Section II ("Empirical Evidence on Competition and Monopoly"), subsections II.3–II.5, pp. 371–377.
**Series**: S801–S805 (5) · Group `ch08`/`CH08`.
**Compiled**: 2026-06-30 (RSCD Phase-2 methodological-historian agent), reasoning from Shaikh's perspective.
**Per-series MHRs**: `Technical/docs/methodology/series/S80{1..5}_MHR.md`.
**Phase-0 references cited throughout**: `_timelines/IO_CHANGE_TIMELINE.md` (SIC→NAICS break), `_timelines/NIPA_CHANGE_TIMELINE.md`, `concordances/_sources/SOURCES.md` + `concordances/_sources/naics/` (US Census SIC↔NAICS chain).
**This pass's review**: `Technical/methodology_review/CH08_review.json` (integration 87.3, COMPLETE; D13 PASS; D14 BELOW_90 on the S803 stale name).

---

## What makes Chapter 8 methodologically distinctive

Chapter 8 is the **one chapter in the whole replication that contains no original Shaikh data construction**. All five series (S801–S805) are **direct reproductions of others' published figures/tables**, drawn from six external studies (Eichner 1973; Weston-Lustgarten-Grottke 1974 via Semmler 1984; Bain 1951 with Demsetz 1973b corrections; Stigler 1963; Demsetz 1973b). There is even **no formal Appendix 8** in the book — the appendix sequence skips from 7.1 straight to 9.1 — so the `SalvagedInputs/book_data/ShaikhChoppedTables/Appendix8_*.xlsx` files are a de-facto data dictionary Shaikh's team built from the chapter narrative and the originating publications, **not** a book appendix. The source-of-record for replication is therefore the originating Bain/Stigler/Demsetz/Semmler/Eichner publication, not Shaikh (`CH8_ADEQUACY_REPORT.json` `appendix_8_status`).

The methodological "history," then, is not a construction lineage but a **citation strategy**: *why Shaikh cites each specific empirical study to make his real-competition case against the oligopoly-pricing / structure-conduct-performance (SCP) school.*

## The through-line: real competition versus the "administered prices" / SCP orthodoxy

The oligopoly-pricing school (Bain, Mann, the post-Keynesian markup theorists) holds that industrial **concentration produces (a) rigid, "administered" prices and (b) persistently higher profit rates**, both read as monopoly power. Shaikh's theory of **real competition** predicts the opposite structure of evidence: profit rates are turbulently **equalized** across industries by mobile "regulating capital," so concentration cannot buy a persistent profit premium; what high concentration correlates with is **high fixed/entry-and-exit costs**, and those produce **more *stable* prices and profit rates, not higher ones**. Chapter 8 assembles a five-exhibit dossier that dismantles the SCP claim pillar by pillar, and the choice of studies is itself the argument — Shaikh wins on the opponents' own turf:

| Series | Fig | Study cited | SCP pillar attacked | How the citation refutes it |
|--------|-----|-------------|---------------------|------------------------------|
| **S801** | 8.1 | Eichner (1973), *EJ* p.1187 | price rigidity ⇒ monopoly | Uses a **post-Keynesian's own pro-oligopoly chart**: smoother concentrated-industry prices reflect high fixed/entry costs, and *"no evidence … of a higher level of profitability."* Rigidity ≠ rents. |
| **S802** | 8.2 | Weston-Lustgarten-Grottke (1974) via Semmler (1984) T3.3 | rigidity is a stable structural fact | The concentration-rigidity coefficient **flips sign across three recessions** (+, −, none). The study's own title: *"The Administered Price Thesis Denied."* |
| **S803** | 8.3–8.4 | Bain (1951), *QJE* + Demsetz (1973b) corrections | concentration ⇒ higher ROE | **Re-runs the SCP patriarch's regressions on his own data**: R²=0.078 (linear), 0.033 (corrected deciles); quotes Bain admitting the *"fit … is obviously so poor."* Exposes Bain's implicit equal-leverage premise. |
| **S804** | 8.5 | Stigler (1963), T17 | concentration ⇒ higher profit level | The **theoretically correct asset measure** gives **identical means (7.1% vs 6.9%)**; concentration lowers *variance*, not level — exactly real competition's prediction. |
| **S805** | 8.6 | Demsetz (1973b), T4 | a stable concentration-profit correlation exists | The relation **reverses sign 1963→1969**; Demsetz's efficiency interpretation makes concentration a *result*, not a *cause*, of returns. Correlation *"unstable over time and space."* |

Two rhetorical moves recur. First, **the opponents' own founding evidence turned against them** (Eichner's pro-oligopoly chart; Bain's own regression data). Second, **the SCP school's most effective internal critics enlisted** (Stigler and Demsetz, both Chicago; Weston's explicit "denial" note). Every exhibit produces the weak, sign-unstable, level-flat, efficiency-explicable pattern that mobile regulating capital predicts and that the oligopoly-pricing school cannot accommodate.

## The concordance story — SIC-era concentration, honestly frozen

Chapter 8's single methodological-change axis is **industry classification via concentration measures**: every series embeds an SIC-era concentration construct — **CR4 midpoints** (S802 20/50/80; S805 six bins; S804's high-vs-low-CR4 partition), **CR8 ratios plus 1935 Census industry numbers** (S803), or an SIC-era **"concentrated"/"competitive" partition** (S801). `REVIEW_MANIFEST.json` correctly flags `touches_concordance = true` for all five; the canonical `series_registry.json` currently carries `None` (review M3) — a **flag-sync gap, not a handling error**.

The handling is deliberately, and correctly, **non-interventionist**: **no SIC→NAICS crosswalk is applied to any Ch8 series.** These are historical reproductions of fixed academic tables (1935–1973), and the RSCD Census SIC↔NAICS chain staged in Phase 0 (`concordances/_sources/naics/`) begins only at **1987 SIC → 1997 NAICS**. Bain's 1935 categories fall off the *bottom* of that bridge (an irrecoverable wall); the others predate the 1992-SIC/1997-NAICS break that `IO_CHANGE_TIMELINE.md` documents (BEA: pre-1997 tables *"should not be used as a time series"*). Applying a proxy crosswalk would fabricate conformability that does not exist — so the correct act is to reproduce the historical concentration measure verbatim and **document that any modern extension WOULD require a concordance** (SIC→NAICS) plus a re-derivation of the CR4/CR8 partitions under changing Census definitions. Every per-series MHR states this explicitly, and every EPR/Adequacy entry classifies the modern parallel as a **new series (proxy), never a splice**.

By contrast, there is **no NIPA and no BEA-benchmark I-O exposure anywhere in the chapter**: these are firm-accounting profit ratios and wholesale price indices from academic studies, not BEA magnitudes subject to the 2013 R&D / 2018 / 2023 comprehensive revisions (`NIPA_CHANGE_TIMELINE.md`) or the quinquennial benchmark re-orderings (`IO_CHANGE_TIMELINE.md`). This is the sharpest contrast with the immediately preceding Chapter 7, whose US tier (S705–S710) is NAICS-native and heavily NIPA/benchmark-exposed. Chapter 8 is a **museum of historical concentration exhibits**, frozen by design.

## Replication fidelity — what "reproduced" means here

Four of the five series are **byte-exact transcriptions of already-fixed academic tables** (V03 MAE 0.0; `CH08_review.json` handcheck confirms EXACT matches against `Appendix8_*.xlsx`): S802 (Semmler 3×3), S803 (Bain scatter + Demsetz-corrected deciles), S804 (Stigler 12 cells), S805 (Demsetz 12 cells). The fifth, **S801, is a disclosed figure-digitization recovery**: Eichner published Fig 8.1 as a **chart only, with no underlying table**, so it was `data_unavailable` at first pass and was **RECOVERED 2026-05-26** by offline vector extraction of *Shaikh's reproduced figure* from the book PDF, overlay-validated, carrying `provenance: digitized` (digitization fidelity, not Eichner's non-existent table). The D13 authenticity gate PASSes with an explicit note that this is documented figure-digitization, **not fabrication**, and there is no `np.random` in the Ch8 pipeline.

## Documentary debts the review surfaces (numbers are clean; metadata is not)

The D14 gate scores `BELOW_90` for one HIGH-severity metadata leak, and several lower-severity items remain — all documentary, none affecting the validated values:

- **S803 stale canonical `name` (H1, HIGH)**: `series_registry.json S803.name = "Interest Rates, Prices, and Equity Data"` is a **stale CD2 S041 Ch10 interest-rate carryover** for a Bain profit-vs-CR8 series. `CH8_REGISTRY_DELTA.json` recorded the rename but it was never applied; the stale name propagates into `Outputs/Publish/series_registry.json`, `site/docs/series_registry.json`, `SERIES_CANDIDATE_LIST.json:847`, and `CD2_to_RSCD_crosswalk.csv:40`. `display_name` is correct. **These MHRs use the correct concept and do not propagate the stale name.** Blocks external distribution until fixed.
- **S803 spurious CD2 predecessor (M2)**: `S803.predecessor_artifacts.cd2_source_file = "ch10/Appendix10_IntroPPrice.csv"` (unrelated Ch10 artifact); crosswalk row S041→S803 should be removed. No genuine CD2 Ch8 dossier exists.
- **S801 stale EPR (M1)**: `S801_EPR.md` still declares `data_unavailable` / "no P02" / "no parquet" — superseded by the 2026-05-26 recovery. DPR reconciled; EPR not.
- **`touches_concordance` desync (M3, all five)**: manifest=true, canonical registry=None. Set the canonical flag; handling already correct.
- **S801 `content_type` (L1)**: registry `cross_sectional` for a genuine 1965-73 annual time series (defensible triage that suppresses proxy extension, but technically inaccurate).
- **S804 note (L2)**: registry says `bin_start` is the canonical year; chopped actually uses **bin midpoints**. **S803 `source_id` token (L3)**: chopped `BAIN_1951_TABLE_I` vs. registry `BAIN_1951_QJE` — harmonize.

## The forward-risk map

Uniformly **low on the numbers, documentary on the metadata**. Every Ch8 series is a **frozen historical reproduction with no numeric extension and no vintage/benchmark risk**. The live risks are (1) the S803 stale-name + spurious-predecessor leak into the published bundle (D14 blocker) and the S801 stale EPR — both registry/metadata fixes; and (2) the standing principle that **any modern "concentration-and-profitability" parallel is a NEW series (proxy), never an extension** — it would require a SIC→NAICS crosswalk, re-derivation of CR4/CR8 partitions under changing Census definitions, and (for Census CR data) coverage that stops at manufacturing through 2017. That the replication reproduces these historical concentration exhibits *without* forcing a proxy crosswalk is precisely the fidelity the chapter demands: the exhibits are illustrative and canonical, and their honesty depends on not pretending 1935/1963-vintage concentration classes splice onto modern NAICS.
