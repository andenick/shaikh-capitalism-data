# S704 — Extension Provenance Record

**Series**: S704 — Figure 7.14 — US Manufacturing Average Rate of Profit (USMANAVG line), 1960–1989

**Construction classification**: `book_period_validated` (recovered by machine digitization 2026-07-02; see `S704_DPR.md`)
**Extension status**: `discontinued`
**Extension method**: not applicable — see §2
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Revised**: 2026-07-02 — recovery reconciliation by opus M3 ingestion agent
**Related**: `S704_DPR.md`

---

## 1. Classification

S704's book-period values now **exist**: they were recovered by machine-digitizing the USMANAVG (US-manufacturing average) line off the printed Fig 7.14 average panel (Decision 0019). The series is `book_period_validated`. This EPR concerns only the question of **extending** those 1960–1989 values forward with live data — which is **not attempted**.

## 2. Why no extension is attempted — `extension_status: discontinued`

- The book-period source (OECD ISDB 1994 vintage, US subset, via Christodoulopoulos 1995) was **discontinued** by OECD; the raw dataset is unrecoverable. No live feed continues it.
- **The 1960–89 ISDB panel and the 1987–2005 BEA NAICS panel are explicitly NOT splice-compatible.** They differ in industry schema (ISDB internal codes vs SIC/NAICS), in capital-stock concept (ISDB gross vs BEA net), and in country/coverage frame. This is precisely why Shaikh himself does **not** extend Fig 7.14 into the modern period — he starts a *fresh* BEA-based construction in 1987, which RSCD carries as the **separate schema** S705/S706, not as an extension of S704.
- Any modern BEA/STAN panel would therefore be a **methodologically separate exhibit**, not a faithful continuation. Per the Anti-Degradation rule, we do not splice.

**S704 is book-period-only.** The recovered 30 points (1960–1989) are the complete series; there is no `-EXT` subseries and none is contemplated.

## 3. Method

N/A — no live-API extension. (The book-period recovery method is documented in `S704_DPR.md` §4, not here — that is ingestion, not extension.)

## 4. No-Proxy disclosure

**None attempted.** No modern proxy could meet the Anu No-Proxy bar without crossing the ISDB→BEA schema and gross→net capital-stock breaks.

## 5. No-Synthetic disclosure

**None.** No interpolation and no synthetic fill. The book-period values are digitized from the published figure (an act of *transcription*, governed by the digitization method chain in `S704_DPR.md` §4), not synthesized.

## 6. Failure-mode table

| Situation | Action |
|---|---|
| Live-extension requested | Declined — sources not splice-compatible (`extension_status: discontinued`) |
| Loader invoked | Loads the machine consensus (or a superseding human return, if present); converts percent → decimal |
| Validator invoked | Round-trip + 3 reference vertices + plausibility + anchor suite (see `S704_DPR.md` §9) |

## 7. CD2 divergence pre-disclosure

CD2 (the predecessor build) had no per-series CSV matching this exhibit's content; the CD2-vs-RSCD numeric comparison is not meaningful here. The recovered S704-A values originate from the 2026-07-02 machine digitization, not from any predecessor table.

## 8. Superseding path (the only sanctioned future change)

The machine consensus is durable but **not final by fiat**: a **human-guided digitization** filed at `digitization_packet/returns/S704_aggregate_digitized.csv` **supersedes** the machine consensus automatically (the loader's returns-guard prefers it). This is the single sanctioned path to revise S704 — never a proxy, never a modern splice. The historical recovery-path notes (author contact for the lost ISDB table) remain in the B5 provenance file at curated book source data but are now secondary, since the figure itself has been digitized.

## Notation (plain-language key)

Short forms used above, in plain language (this record is a downloadable external artifact):

- **S### / -A / -EXT** — a series identifier / a subseries / a live-extension subseries.
- **DPR / EPR** — Data Provenance Record / Extension Provenance Record (this file).
- **Phase N** — Anu Framework pipeline stages: Phase 6 = extension, Phase 9 = visualization.
- **USMANAVG** — the ISDB internal code for the US-manufacturing AVERAGE aggregate line (the one line S704 digitizes).
- **CD2** — the predecessor build of this dataset.
- **ISDB** — OECD International Sectoral Database.
- **BEA / NAICS / SIC** — US Bureau of Economic Analysis / North American / Standard Industrial Classification systems.
- **STAN** — OECD Structural Analysis database.
