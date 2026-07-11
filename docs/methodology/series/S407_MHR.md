# S407 — Methodological History Report (MHR)

**Series**: S407 — Automotive Marginal Cost · Figure 4.22 (book p.163)
**Chapter**: 4 (Production and Costs), §VI (Inman's empirical cost curves) · **Group**: ch4 / CH04
**Status**: `book_period_validated` (recovered 2026-05-26) · `content_type: theoretical` (registry) / `derived` (research JSON) · `construction: direct` (digitized) · `publish: true`
**Perspective**: authored *from Shaikh's perspective*.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S407` (lines ~14933–15058, `cross_references` → S405); `Technical/research/S407_research.json`;
`Technical/docs/series/S407_DPR.md` + `S407_EPR.md`; `Technical/methodology_review/CH04_review.json` (F1/F3b/F4/F5);
digitized source `SalvagedInputs/book_data/Reconstructed/Inman_1995_S404-407_cost_curves.json` → `S407`;
trace `Technical/WL1_Tsoulfidis_Tsaliki/extract_inman*.py`; KB `.../Body_Text/ch04_production_costs.md` (lines 2330, 2475),
`.../Figures/ch04/ch04_figure_4.22.md`; parent `S405_MHR.md` (marginal labor cost), theoretical twins `S401_MHR.md`/`S403_MHR.md`.

---

## 1. What the series is

S407 is Shaikh's **Figure 4.22 — simulated automotive *overall marginal* cost vs annual vehicle production**, reproduced from **Inman (1995), fig. 6**. It sums marginal material cost (= constant average material cost) and the marginal labor cost of S405 (`S407_research.json` formula, components; registry `cross_references` → S405). Cost-vs-output curve, not calendar time.

Book definition (Shaikh 2016 p.161, verbatim, `S407_research.json`):
> "And overall marginal cost as in figure 4.22, which is the sum of marginal material cost (equal to average material cost, since the latter is taken to be constant) and marginal labor costs discussed previously. In the automotive industry, the former happens to be very much larger than the latter, so the overall marginal cost curve is essentially flat-bottomed over much of the observed range of output, with modest spikes at each new shift."

KB caption (verbatim, `ch04_production_costs.md` line 2475): *"Source: Inman 1995, 64, fig. 6."* Same reclassification / field-drift / empty-extension as the other Inman series (`CH04_review.json` F5).

## 2. Source lineage

- **Ultimate source — CORRECT citation:** Robert R. **Inman** (1995), Engineering Economist **41(1), 53–67, DOI 10.1080/00137919508967475** (subsource `INMAN_1995_ENGINEERING_ECONOMIST`; `S404_DPR.md` §3). Same wrong-citation caution as S404 (F1).
- **Underlying data behind Inman:** `mc(Q) = marginal_material_cost(Q) + marginal_labor_cost(Q)`; since average material cost is constant, marginal material cost = average material cost, and marginal labor cost = S405 (`S407_research.json` components).
- **RSCD recovery vehicle:** Inman fig. 6 is chart-only; recovered **2026-05-26 by native-vector trace of Shaikh's reproduced Fig 4.22 from the book PDF**, overlay-validated; provenance `digitized`. Points in `Inman_1995_S404-407_cost_curves.json` → `S407`; L01_S407 loads via `make_curve_frame`.

## 3. Why these sources, author's perspective

- **Why the total-marginal-cost figure — the theoretical payoff.** S407 is where Shaikh lands the argument against the neoclassical decision rule: with an essentially flat-bottomed `mc` interrupted by spikes, "the rule p = mc would then select a very large number of points… would select multiple points, including engineering capacity… and would select only engineering capacity if p was higher still" (p.161, verbatim caveat). The rule *fails* as a unique output-selector — exactly the conclusion S403 reached theoretically. S407 is the empirical closure of the whole chapter's argument.
- **Why the material-cost dominance is the point.** In autos, marginal material cost dwarfs marginal labor cost, so the curve is flat over most of the range with only "modest spikes" — showing the pattern survives even where labor is a small share (`S407_research.json` methodology_notes).
- **Rejected alternatives:** re-simulation with current data (out of scope); `data_unavailable` (superseded by digitization); proxy (never).

## 4. Methodological-change exposure

**None** on the national-accounts axes:
- **NIPA touch — NONE**; **I-O touch — NONE**; **Concordance touch — NONE.** Single-plant engineering simulation; no BEA/Leontief/SIC-NAICS content; timelines do not apply. Frozen 1995 exhibit, no successor vintage.

## 5. Replication fidelity note — figure-digitization recovery (honest)

Disclosed vector trace of Fig 4.22, overlay-validated, provenance `digitized`; V03 round-trips at 0.05; reviewer hand-check EXACT at point indices {1:5143.0, 9:5266.0, 17:7399.9} (the 17-point spike at 7399.9 is the shift-change jump on the $0–$8,000 axis) (`CH04_review.json` hand_check `S407`; `registry` validation.reference_values). **Same honesty debt as S404** — flag:

- **Wrong Inman citation** in the research JSON (F1); correct = Engineering Economist 41(1):53–67, DOI 10.1080/00137919508967475.
- **Stale DPR/EPR/notes/adequacy** still implying `data_unavailable` (F1/F4); **method pointer to the Tsoulfidis EXTRACTION_REPORT is wrong** (F3b) — real trace is `extract_inman*.py` + `inman_extracted.json`.
- **content_type/construction drift** (F5).
- **Fidelity ceiling:** reproduces Inman's plotted curve (incl. the tall spike), not his exact numbers; exact values need the paywalled article. No proxies/interpolation beyond the trace.

## 6. Forward risk

- **No meaningful numeric extension** — modern study = separate exhibit, never a splice.
- **Live risks are documentary:** citation + stale-doc reconciliation (F1/F4), method-report re-pointing (F3b); paywalled Inman (1995) only if exact values ever needed. Contributes to the ch4 D14-below-90 block.
- **No BEA/BLS/OECD exposure.**
