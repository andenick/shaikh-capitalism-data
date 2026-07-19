# S401 — Methodological History Report (MHR)

**Series**: S401 — Average and Marginal Costs with Wage Paid **per Worker**, at Normal Intensity for 8-Hour Shifts up to Engineering Capacity (Two and a Half Shifts) · Figure 4.16 (book p.155)
**Chapter**: 4 (Production and Costs), §V–Appendix 4.2 · **Group**: ch4 / CH04
**Status**: `book_period_validated` · `content_type: theoretical` (registry) / `derived` (research JSON) · `construction: formula` · `publish: true`
**Perspective**: authored *from Shaikh's perspective* — why he built this object the way he did.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S401` (lines ~14024–14228); `Technical/research/S401_research.json`;
`Technical/docs/series/S401_DPR.md` + `S401_EPR.md`; `Technical/methodology_review/CH04_review.json`;
`Technical/docs/chapters/CH4_RESEARCH_SUMMARY.md`; source CSV `SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv`
(+ `Appendix_4_2_Table3.csv`, `Appendix_4_2_README.md`); KB `Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Body_Text/ch04_production_costs.md`
and `.../Figures/ch04/ch04_figure_4.16.md`; siblings `S402_MHR.md`, `S403_MHR.md`.

---

## 1. What the series is

S401 is a **numerical illustration Shaikh computes himself**, not an empirical time series. For a stylized firm it tabulates five cost curves — average fixed cost `afc`, unit labor cost `ulc'`, average variable cost `avc'`, average total cost `ac'`, and marginal cost `mc'` — under the assumption that **wages are paid per worker** (a fixed wage bill `Ws` per shift), plotted against cumulative daily output `XR` across three shifts (8+8+4 hours) at normal intensity `i=1`. It is the data behind **Figure 4.16** (`S401_DPR.md` §1; `S401_research.json` primary_source).

Book definition (Shaikh 2016 p.154, `S401_research.json` book_quotes, verbatim):
> "Daily average total cost is ac = dpMK·mkj(Hj,i) + pa·ā + jW̄/XRj(Hj,i). The first component declines steadily, the second is constant, and the third reaches the same minimum value at the end of first and second shifts. It follows that the overall average total cost curve will be lower at the end of the second shift than any point reached before."

The point of the exhibit: when productivity follows the within-shift quadratic of eq. (4.2.1) and labor is hired by the worker-shift, `ac'` reaches **near-equal minima at the end of shifts 1 and 2**, and `mc'` is **flat at the materials-cost level `pa·a` within a shift with a discrete jump at each shift boundary** — directly contradicting the smooth U-shape of neoclassical textbook cost curves (`S401_research.json` methodology_notes; `S401_DPR.md` §2).

**Content type — the load-bearing decision.** The stub arrived `time_series`; Phase 3 reclassified it to `derived`/`formula` because "there is no calendar-year axis to extend" — the abscissa is cumulative output `XR`, carried as a synthetic ordinal `year=row_index 0..20` only so the generic writers work (`CH4_RESEARCH_SUMMARY.md` "Critical reclassification"; `S401_DPR.md` §7 caveat 1). Note the residual **registry↔research drift** (`CH04_review.json` F5, LOW): the registry field reads `content_type:"theoretical"`/`construction:"direct"` while the research JSON and rollup say `derived`/`formula`; both correctly set `extension_candidates: []`.

## 2. Source lineage

One source, one frozen author-construction (`S401_DPR.md` §3; `S401_research.json` primary_source):

- **Shaikh, *Capitalism* (2016), Appendix 4.2 "Numerical Calculations…", book pp.772–781**, agency = **Shaikh (author construction)**, subsource `SHAIKH_APPENDIX_4_2`. The canonical table is **Appendix Table 4.2.4** (per-worker-wage cost columns), built on the productivity schedule of eq. (4.2.1) and Table 4.2.1.
- **Retrieval in RSCD — the recovery fact.** The Appendix 4.2 data-companion workbook is **missing** from `SalvagedInputs/book_data/ShaikhChoppedTables/` (which holds only Appendices 2, 5–17), and Shaikh's website `.docx` companion is a text file with `[INSERT …]` placeholders, not embedded numbers (`Appendix_4_2_README.md`). Phase-5 blocker **CH4-B1** was therefore resolved by **verbatim transcription of Appendix Tables 4.2.1–4.2.4 from the book PDF pp.772–781** into `Appendix_4_2_Table{3,4}.csv` on 2026-05-18, validated to **≤0.02 rounding noise** on every derived column (`S401_research.json` review_history; `Appendix_4_2_README.md`).

**No splice, no external data.** There is no agency series, no vintage, no overlap anchor — the whole object is closed-form.

## 3. Why these sources, author's perspective

- **Why an author-built numerical illustration at all.** Chapter 4 rebuilds the theory of the firm on a classical/post-Keynesian foundation; Shaikh needs a *transparent* worked example showing that plausible engineering assumptions (fixed capital, multi-shift operation, a within-shift productivity hump) generate cost curves that look nothing like the textbook U. So he computes his own — "Table 4.4 summarizes the derivations of cost curves for both types of wage payments, and figures 4.16 and 4.17 depict the corresponding ac, avc, and mc curves" (p.154, verbatim). The per-worker case (S401) is chosen first because it produces the cleanest result: with a fixed wage bill per shift, within-shift `mc'` collapses to the constant material cost `pa·a` and the two shift-1/shift-2 minima are exactly equal.
- **Why these parameters.** The illustrative constants (`d=0.05, pMK=100, pa=10, a=0.30, wN=100, p=7`, `MK=14`) are Shaikh's own, stated at Appendix 4.2 p.781 (`S401_DPR.md` §4; `S401_research.json` components) — set so the per-worker (`wN=100`) and per-hour (`wh·8=100`) variants share a common baseline, making S401 and S402 directly comparable (`S402_research.json` open_questions).
- **Rejected alternatives — none in the empirical sense.** There is nothing to substitute: this is Shaikh's own arithmetic, not a data pull. `extension_candidates` is intentionally empty — "a closed-form numerical illustration with no real-world data counterpart" (`S401_research.json` methodology_notes). No proxy question and no source-selection question arise.

## 4. Methodological-change exposure

**None of the standard axes bear on S401.**

- **NIPA touch — NONE.** No BEA product account is used; comprehensive-revision / reference-year drift (`_timelines/NIPA_CHANGE_TIMELINE.md`) is irrelevant to a closed-form illustration.
- **I-O touch — NONE.** No input–output matrix, no Leontief inverse; `_timelines/IO_CHANGE_TIMELINE.md` does not apply.
- **Concordance touch — NONE.** No SIC/NAICS/ISIC industry dimension and no country mapping; the "shifts" are an engineering index, not a classified sector.

The only "vintage" risk is the fidelity of the printed Appendix table itself (see §5).

## 5. Replication fidelity note

RSCD reproduces S401 by the **read-the-truth-column** pattern: L01 consumes the transcribed `Appendix_4_2_Table4.csv` per-worker columns, P02 passes through, and V03 round-trips against the same CSV at ±0.5% — MAE is **exactly 0.0 by construction** (`CH4_RESEARCH_SUMMARY.md` V03 table: PASS, MAE 0.0, n=122). Honest limits, disclosed:

- **Parameter non-reproducibility, documented.** Eq. (4.2.1) with the *printed* `a1=2, a2=1.2, a3=0.05` yields `xr(h=1)=3.15`, but Table 4.2.1 prints `3.55` (a +0.40 offset); back-solving `a1=2.40` recovers the tabulated values exactly (`S401_DPR.md` §7 caveat 2; `Appendix_4_2_README.md`). RSCD **does not re-derive** — it reads Shaikh's tabulated numbers, so the illustration is reproduced as published rather than as re-simulated.
- **Melt-fidelity, not independent confirmation.** Round-tripping the same CSV the chopped is melted from confirms *transcription fidelity*, not an out-of-sample check; the genuine anchor is the printed Appendix Table 4.2.4 (book pp.779–780), hand-verified EXACT by the reviewer (`CH04_review.json` hand_check `S401_afc` {0:70.0, 10:1.099, 20:0.526}).
- **Reference-value keying (F3a, MED).** `validation.reference_values` are point-index keyed ({0,10,20}); Decision 0008 (point-index → `derived_statistics`) is still outstanding — a schema/keying reconciliation only, values are correct (`CH04_review.json` F3a).
- **No DECOMPOSITION.md** (project-wide F6): construction lives in `S401_DPR.md` §4 + registry `construction_steps`.
- **KB availability correction (F2).** The registry once implied ch04 "was not HDARP-extracted"; that is **false** — `Body_Text/ch04_production_costs.md` and the Appendix in `ch18_appendices.md` both exist, so a KB-anchored "From the book" quote is available (`CH04_review.json` F2; S401 triage already anchors its explainer to ch18/Appendix 4.2).

## 6. Forward risk

- **Essentially zero data-vintage risk.** As a closed-form illustration, S401 can only change if a *transcription correction* is found in the printed Appendix, or if the project elects to re-derive from eq. (4.2.1) with the back-solved parameters (which would change nothing at ≤0.02).
- **Documentary debt, not data risk.** The live items are the F5 `content_type`/`construction` field drift (registry `theoretical`/`direct` vs `derived`/`formula`) and the F3a reference-value re-keying — both WARN-level doc/registry reconciliations, neither touching the numbers.
- **No BEA/BLS/OECD exposure**; nothing to re-fetch, nothing to re-anchor.
