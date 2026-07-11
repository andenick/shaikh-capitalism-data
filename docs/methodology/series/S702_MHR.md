# S702 — Methodological History Report (MHR)

**Series**: S702 · Figure 7.12 — Change in Selling Price versus Change in Unit Labor Cost, UK 1954–1963 (ratio of each variable in 1963 to its 1954 value)
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` · `content_type: cross_sectional` · `construction: direct` · `publish: true`
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 286–287; Appendix 7.1 (p. 856).
**Sources read**: `Technical/research/S702_research.json`, `Technical/series_registry.json` (S702), `Technical/methodology_review/CH07_review.json` (L2, L3, touchpoint S702), `Technical/docs/chapters/CH7_RESEARCH_SUMMARY.md`.

---

## 1. What the series is
S702 is the **UK counterpart of S701**: a cross-industry scatter of ~28–56 UK manufacturing industries, x = unit-labour-cost ratio (1963 ÷ 1954 × 100), y = selling-price ratio (1963 ÷ 1954 × 100). One point per industry; `cross_sectional`, not a time series. Book source caption (page-cited, `S702_research.json`, p. 287): *"Figure 7.12 Change in Selling Price versus Change in Unit Labor Cost, UK 1954-1963 … Source: Salter 1969, 164, table 28."* The UK data are special because they come from the **posthumous Addendum by W. B. Reddaway**, compiled after Salter's death in 1963 (p. 286). Same analytical purpose as S701: demonstrate that cross-industry price change tracks cross-industry unit-labour-cost change, supporting cost-regulated prices of production. (The fabricated "R²≈0.77" was removed here too — registry triage 2026-06-11.)

## 2. Source lineage
- **Ultimate author source**: Salter (1969) **Table 28, p. 164**, in the Reddaway Addendum; underlying data from the **UK Census of Production** and Board of Trade industrial statistics for 1954 and 1963. Base 1954 = 100.
- **Native units**: index ratios (1963/1954 × 100), dimensionless.
- **Transcription vehicle**: Shaikh's Appendix 7.2. In `SalvagedInputs/book_data/ShaikhChoppedTables/` the **file `Appendix7_SalterULCPriceTable33.xlsx` physically contains the UK 1954–63 Reddaway panel** (mirror image of the S701 swap; see §5). Loader `Technical/code/L01_loaders/L01_S702.py`.
- **Adjustment chain**: **none** (`construction: direct`) — no WEQ/OOH/inventory/reserve; the only transform is Salter's own 1954-base indexing. RSCD transcribes byte-exact (56/56 pairs EXACT).
- **The one SIC reference in the whole chapter**: Salter's Table 28 column is headed **"Industry (1958 S.I.C.)"** (UK Standard Industrial Classification 1958). This is used purely as a **row label** for the UK industries, **not as a mapping/crosswalk** (review touchpoint S702). It is the earliest SIC-vintage artifact in Ch7.
- **Label artifacts** (disclosed): registry KEY `SALTER_1969_TABLE33_UK` + chopped `source_id` carry "Table 33/p.197" while the book caption says "Table 28/p.164" (review L2); synthetic `year=1963` ratio-period key at `L01_S702.py:47` (review L3).

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Shaikh pairs the UK panel with the US one to show the price/cost regularity is **not a US idiosyncrasy** — the same "striking relationship" appears in a different country, different decade, different statistical agency (UK Census of Production vs US Census of Manufactures). Reddaway's Addendum happened to contain exactly the price and unit-cost indices needed, already tabulated; Shaikh again simply plots numbers their compiler never cross-plotted. He forward-references ch.9 (p. 286: *"a powerful and more general property of relative prices"*), signalling that this cross-section is a down-payment on the vertically-integrated price theory developed later.
**Rejected alternatives** (`S702_research.json`): ONS Labour Productivity by industry (SIC 2007) and ONS Producer Price Inflation are the modern UK analogues, but **UK SIC 1958 (Salter's vintage) is not comparable to SIC 2007**, and ONS PPI base years/coverage differ — the 1954/1963 cross-section cannot be reconstructed or back-extended. Keep Salter/Reddaway's original UK industry labels ("Iron and Steel", "Cotton", "Wool"); no modern splice.

## 4. Methodological-change exposure (concordance / classification)
S702 carries the chapter's **only explicit SIC citation** ("1958 S.I.C."), making it the anchor example of *why* the classification through-line matters even where it is not operationalised:
- The **UK SIC 1958 → SIC 2007** break is analogous to the US SIC→NAICS wall. RSCD's staged concordances (`_sources/naics/`) are US Census SIC↔NAICS bridges and **do not cover UK SIC** — there is no UK crosswalk in-project, and none is needed because the series is frozen.
- Because the classification is a **label only** (not used to align data across vintages), there is no live concordance risk; the exposure is documentary (preserve the "1958 S.I.C." heading verbatim in any regenerated figure).
- No NIPA/BEA-IO vintage exposure (`NIPA_CHANGE_TIMELINE.md`, `IO_CHANGE_TIMELINE.md`) — non-US, non-BEA, no profit magnitudes.
Net: like S701, a hard classification wall (UK SIC 1958 unrecoverable to modern ONS), not a splice hazard.

## 5. Replication fidelity note
Transcription of an already-fixed cross-section; not recompute. 56/56 pairs byte-exact (V03 MAE 0.0, tol 0.5%). Honesty items carried forward: the **file-naming swap** (`…Table33.xlsx` holds the UK panel the book cites as Table 28 — mirror of S701, review L2), the **subsource-key desync** (KEY/`source_id` = Table 33/p.197 vs book Table 28/p.164; open registry-owner reconciliation), and the **synthetic `year=1963` key** (`L01_S702.py:47`, documented). No fabricated statistics remain.

## 6. Forward risk
Low / none. Frozen historical illustration, no extension, no BEA/OECD vintage dependency. Only forward action is documentary: reconcile the Table 28/33 + page 164/197 label desync and preserve the "1958 S.I.C." column heading verbatim when the figure is regenerated in Phase 9 viz.
