# S406 — Methodological History Report (MHR)

**Series**: S406 — Automotive Average Cost · Figure 4.21 (book p.162)
**Chapter**: 4 (Production and Costs), §VI (Inman's empirical cost curves) · **Group**: ch4 / CH04
**Status**: `book_period_validated` (recovered 2026-05-26) · `content_type: theoretical` (registry) / `derived` (research JSON) · `construction: direct` (digitized) · `publish: true`
**Perspective**: authored *from Shaikh's perspective*.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S406` (lines ~14807–14932, `cross_references` → S404); `Technical/research/S406_research.json`;
`Technical/docs/series/S406_DPR.md` + `S406_EPR.md`; `Technical/methodology_review/CH04_review.json` (F1/F3b/F4/F5);
digitized source `SalvagedInputs/book_data/Reconstructed/Inman_1995_S404-407_cost_curves.json` → `S406`;
trace `Technical/WL1_Tsoulfidis_Tsaliki/extract_inman*.py`; KB `.../Body_Text/ch04_production_costs.md` (lines 2330, 2447),
`.../Figures/ch04/ch04_figure_4.21.md`; parent `S404_MHR.md` (average labor cost), theoretical twins `S401_MHR.md`/`S402_MHR.md`.

---

## 1. What the series is

S406 is Shaikh's **Figure 4.21 — simulated automotive *average total* cost ($/car) vs annual vehicle production**, reproduced from **Inman (1995), fig. 5**. It is the sum of a steadily declining average fixed cost, a constant average material cost, and the variable average labor cost of S404 (`S406_research.json` formula, components; registry `cross_references` → S404). Cost-vs-output curve, not calendar time.

Book definition (Shaikh 2016 p.161, verbatim, `S406_research.json`):
> "Average (total) cost as in figure 4.21 is the sum of a steadily declining average fixed cost, a constant average material cost, and the variable portion of labor costs. The overall shape is that of an asymmetric U, with a minimum point somewhere in the third shift."

KB caption (verbatim, `ch04_production_costs.md` line 2447): *"Source: Inman 1995, 64, fig. 5."* Same reclassification / field-drift / empty-extension as the other Inman series (`CH04_review.json` F5).

## 2. Source lineage

- **Ultimate source — CORRECT citation:** Robert R. **Inman** (1995), Engineering Economist **41(1), 53–67, DOI 10.1080/00137919508967475** (subsource `INMAN_1995_ENGINEERING_ECONOMIST`; `S404_DPR.md` §3). Same wrong-citation caution as S404 (F1).
- **Underlying data behind Inman:** `ac(Q) = afc(Q) + amc + alc(Q)` — declining average fixed cost (capital, property taxes, overhead + fixed labor), constant average material cost (Inman p.57), and average labor cost = S404 (`S406_research.json` components).
- **RSCD recovery vehicle:** Inman fig. 5 is chart-only; recovered **2026-05-26 by native-vector trace of Shaikh's reproduced Fig 4.21 from the book PDF**, overlay-validated; provenance `digitized`. Points in `Inman_1995_S404-407_cost_curves.json` → `S406`; L01_S406 loads via `make_curve_frame`.

## 3. Why these sources, author's perspective

- **Why the average-cost figure.** This is where Shaikh drives home the closed loop: Inman's real-plant average cost is "strikingly similar to the theoretical curves previously depicted in figures 4.16 and 4.17… The key factor is the spike in costs at the beginning of a new shift" (p.161, verbatim caveat quote). S406 is the empirical mirror of the S401/S402 `ac` curves — the "asymmetric U with a minimum in shift 3" that neoclassical theory cannot produce.
- **Why the small y-range matters (author's point).** Fig 4.21 spans only ~$5,100–$5,500: average cost is dominated by material + overhead, so the labor-driven shift spikes are a *small but visible* deformation on a nearly flat level — precisely the "roughly flat over the operating range" stylized fact (`S406_research.json` methodology_notes).
- **Rejected alternatives:** re-simulation with current data (out of scope); `data_unavailable` (superseded by digitization); proxy (never).

## 4. Methodological-change exposure

**None** on the national-accounts axes:
- **NIPA touch — NONE**; **I-O touch — NONE**; **Concordance touch — NONE.** Single-plant engineering simulation; no BEA/Leontief/SIC-NAICS content; timelines do not apply. Frozen 1995 exhibit, no successor vintage.

## 5. Replication fidelity note — figure-digitization recovery (honest)

Disclosed vector trace of Fig 4.21, overlay-validated, provenance `digitized`; V03 round-trips at 0.05; reviewer hand-check EXACT at point indices {1:5471.7, 13:5249.7, 26:5469.7} (`CH04_review.json` hand_check `S406`; `registry` validation.reference_values). **Same honesty debt as S404** — flag:

- **Wrong Inman citation** in the research JSON (F1); correct = Engineering Economist 41(1):53–67, DOI 10.1080/00137919508967475.
- **Stale DPR/EPR/notes/adequacy** still implying `data_unavailable` (F1/F4); **method pointer to the Tsoulfidis EXTRACTION_REPORT is wrong** (F3b) — real trace is `extract_inman*.py` + `inman_extracted.json`.
- **content_type/construction drift** (F5).
- **Fidelity ceiling** + **narrow y-range sensitivity:** on a ~$400-wide window the trace must resolve small spikes accurately; overlay validation passed but reproduces the plotted curve, not Inman's exact numbers. No proxies/interpolation beyond the trace.

## 6. Forward risk

- **No meaningful numeric extension** — modern study = separate exhibit, never a splice.
- **Live risks are documentary:** citation + stale-doc reconciliation (F1/F4), method-report re-pointing (F3b); paywalled Inman (1995) only if exact values ever needed. Contributes to the ch4 D14-below-90 block.
- **No BEA/BLS/OECD exposure.**
