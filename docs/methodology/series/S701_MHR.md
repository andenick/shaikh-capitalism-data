# S701 — Methodological History Report (MHR)

**Series**: S701 · Figure 7.11 — Change in Selling Price versus Change in Unit Labor Cost, US 1923–1950 (ratio of each variable in 1950 to its 1923 value)
**Chapter**: 7 (The Theory of Real Competition — profit-rate equalization) · Group `ch07`/`CH07`
**Status**: `book_period_validated` · `content_type: cross_sectional` · `construction: direct` · `publish: true`
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 286–287; Appendix 7.1 (p. 856).
**Sources read**: `Technical/research/S701_research.json`, `Technical/series_registry.json` (S701), `Technical/methodology_review/CH07_review.json` (L2, L3, touchpoints), `Technical/docs/chapters/CH7_RESEARCH_SUMMARY.md`.

---

## 1. What the series is
S701 is the **US half of Salter's price/cost cross-section**: a scatter of ~24–48 US manufacturing industries where the x-axis is each industry's *unit-labour-cost* ratio (1950 value ÷ 1923 value × 100) and the y-axis the corresponding *selling-price* ratio. It is not a time series — it is a two-period cross-industry comparison (`cross_sectional`), one point per industry. Book definition (page-cited, `S701_research.json` book_quotes, p. 286): *"Salter himself does not compare the changes in relative prices to those in relative unit labor costs, but the necessary information is available in his book for two other data sets (164, table 28; 197, table 33). Figures 7.11 and 7.12 display this striking relationship for the United States comparing 1923 to 1950, and for the United Kingdom comparing 1954-1963…"* The figure operationalises Shaikh's classical-Marxian claim that **prices of production are regulated by real costs of production**: cross-industry variation in price change closely tracks cross-industry variation in unit-labour-cost change. (Note: the book states **no** R² / "~77% explained" statistic; an earlier fabricated "R²≈0.77" was removed — registry triage 2026-06-11, and `CH7_RESEARCH_SUMMARY.md`.)

## 2. Source lineage
- **Ultimate author source**: W. E. G. Salter, *Productivity and Technical Change*, 2nd ed. (Cambridge University Press, 1969). The US 1923–1950 panel is **Salter's Table 33, p. 197** per the book Fig 7.11 caption (ground truth). Salter built it from **US Census of Manufactures** data + **BLS** price/productivity indices for US manufacturing industries, base 1923 = 100.
- **Native units**: index ratios (1950/1923 × 100), dimensionless.
- **Transcription vehicle**: Shaikh re-plots Salter; the values are transcribed into Shaikh's online Appendix 7.2 workbook. In `SalvagedInputs/book_data/ShaikhChoppedTables/` the **file named `Appendix7_SalterULCPriceTable28.xlsx` physically contains the US 1923–50 panel** (a Shaikh file-naming swap; see §5). RSCD loader `Technical/code/L01_loaders/L01_S701.py` reads this file.
- **Adjustment chain**: **none** — `construction: direct`. No WEQ/OOH/inventory/reserve adjustments apply (those belong to the BEA profit-rate series S705/S706). The only transform is Salter's own indexing to 1923 = 100; RSCD transcribes byte-exact (48/48 pairs verified EXACT, registry triage).
- **Label artifacts** (disclosed, not stealth — review L2/L3): the registry subsource **KEY** `SALTER_1969_TABLE28_US` and the chopped `source_id` still carry the file-derived "Table 28 / p.164" label while the *book caption* says "Table 33 / p.197"; and the loader hardcodes a synthetic `year=1950` ratio-period key (`L01_S701.py:52`). Both are documented in comments/open_questions, not fabrication.

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Shaikh chose Salter because Salter is the **canonical empirical demonstration that relative prices move with relative costs** — the exact regularity the theory of real competition predicts (regulating capital equalises profit rates by cost-cutting technical change). Salter had the industry-level price and unit-cost data already tabulated but *never drew the cross-plot himself*; Shaikh's contribution is to plot Salter's own numbers to reveal the "striking" relationship (p. 286). He deliberately uses a **historical, frozen exhibit** rather than a modern reconstruction because the point is illustrative and canonical, not a live estimate.
**Rejected alternatives** (from `S701_research.json` extension_candidates, with Shaikh-consistent reasoning): BLS Industry Productivity Program (PRS unit-labour-cost by NAICS) and BLS PPI-by-NAICS are the modern analogues, but Salter's 1920s SIC-precursor industry schema cannot be one-to-one matched to modern NAICS, and BLS PPI does not cover all manufacturing pre-1947 — so no modern series can back-extend or reconstruct the 1923–1950 cross-section. RSCD therefore keeps Salter's original labels and treats S701 as non-extensible.

## 4. Methodological-change exposure (concordance / classification)
This is a **pre-SIC-era classification exhibit** and the chapter's earliest classification vintage. Salter's ~1923-era US "industry" categories predate the 1957/1972 SIC and therefore predate the entire Census SIC↔NAICS concordance chain staged at `Technical/docs/methodology/concordances/_sources/naics/` (which begins at 1987 SIC → 1997 NAICS; see `_sources/SOURCES.md`). Consequences:
- **No conformable crosswalk exists** back to Salter's 1920s industries — the official bridges bottom out at 1987 SIC. Placing S701 on a modern NAICS basis is impossible; the classification break is total, not partial.
- Per the `IO_CHANGE_TIMELINE.md` "SIC → NAICS break (the Ch9 wall)", BEA itself states pre-1997 historical benchmark tables "should not be used as a time series"; Salter's cross-section is *a fortiori* a frozen exhibit.
- No NIPA vintage exposure (`NIPA_CHANGE_TIMELINE.md`) — the series contains no BEA magnitudes subject to the 2013 R&D / 2018 T7.11 / 2023 revisions.
Net: S701's methodological-change exposure is a **hard classification wall** (irrecoverable pre-SIC schema), not a splice hazard.

## 5. Replication fidelity note
Reproduction is **transcription of an already-fixed cross-section**, not recompute. Values verified byte-exact against the Salter US panel (48/48 pairs; V03 MAE 0.0, tol 0.5%). Honesty caveats carried forward: (a) the **file-naming swap** — `Appendix7_SalterULCPriceTable28.xlsx` holds the US panel that the book cites as Table 33 (registry L2); the loader normalises this and the DPR discloses it. (b) the **subsource-key desync** (KEY/`source_id` say Table 28/p.164; book says Table 33/p.197) is an open data-layer reconciliation flagged for the registry owner, not a values error. (c) the **synthetic `year=1950` key** (`L01_S701.py:52`) is a cross-section period label, documented in code comments (review L3). No fabricated statistics remain.

## 6. Forward risk
Low. As a frozen historical illustration there is **no extension** and hence no vintage/benchmark risk. The only live "risk" is documentary: the Table 28/33 and page 164/197 label desync should be reconciled in the registry `subsource_ids`, `SUBSOURCE_METADATA.json`, and chopped `source_id` so the published provenance matches the book caption. No BEA benchmark re-classification or OECD revision can affect S701.
