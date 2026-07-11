# S405 — Methodological History Report (MHR)

**Series**: S405 — Automotive Marginal Labor Cost · Figure 4.20 (book p.162)
**Chapter**: 4 (Production and Costs), §VI (Inman's empirical cost curves) · **Group**: ch4 / CH04
**Status**: `book_period_validated` (recovered 2026-05-26) · `content_type: theoretical` (registry) / `derived` (research JSON) · `construction: direct` (digitized) · `publish: true`
**Perspective**: authored *from Shaikh's perspective*.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S405` (lines ~14687–14806); `Technical/research/S405_research.json`;
`Technical/docs/series/S405_DPR.md` + `S405_EPR.md`; `Technical/methodology_review/CH04_review.json` (F1/F3b/F4/F5);
digitized source `SalvagedInputs/book_data/Reconstructed/Inman_1995_S404-407_cost_curves.json` → `S405`;
trace `Technical/WL1_Tsoulfidis_Tsaliki/extract_inman*.py` + `inman_extracted.json`;
KB `.../Body_Text/ch04_production_costs.md` (lines 2330, 2421), `.../Figures/ch04/ch04_figure_4.20.md`;
siblings `S404_MHR.md` (unit-labor-cost source), `S407_MHR.md` (its total-marginal-cost consumer).

---

## 1. What the series is

S405 is Shaikh's **Figure 4.20 — simulated automotive *marginal* labor cost vs annual vehicle production**, reproduced from **Inman (1995), fig. 4**. It is the marginal-cost twin of S404, from the same Monte-Carlo plant simulation (`S405_DPR.md`/registry §1; `S405_research.json` primary_source). Cost-vs-output curve, not calendar time (abscissa carried as point index).

Book definition (Shaikh 2016 p.161, verbatim, `S405_research.json`):
> "Marginal labor cost in figure 4.20 is therefore flat-bottomed, but with much larger spikes at shift beginnings: the peak of the highest spike in marginal labor cost is seven and a half times as high as the bottom (62)! This curve is decidedly not 'well behaved' (64)."

KB caption (verbatim, `ch04_production_costs.md` line 2421): *"Source: Inman 1995, 62, fig. 4."* Same reclassification / field-drift / empty-extension as the other Inman series (`CH04_review.json` F5).

## 2. Source lineage

- **Ultimate source — CORRECT citation:** Robert R. **Inman** (1995), *"Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive Assembly Plants,"* **Engineering Economist 41(1), 53–67, DOI 10.1080/00137919508967475** (registry subsource `INMAN_1995_ENGINEERING_ECONOMIST`; `S404_DPR.md` §3). The same wrong-citation caution as S404 applies to any citation carried in the research JSONs — use the Engineering-Economist record, not "Robert P. Inman / How to Have a Fiscal Crisis" (`CH04_review.json` F1).
- **Underlying data behind Inman:** marginal labor cost `mlc(Q) = d(total labor cost)/dQ`, total labor cost = fixed + variable(Q), from the plant Monte-Carlo (Inman pp.55–63) (`S405_research.json` formula, components).
- **RSCD recovery vehicle:** Inman fig. 4 is chart-only; the underlying series is untabulated + paywalled. RSCD **recovered S405 on 2026-05-26 by native-resolution vector trace of Shaikh's reproduced Fig 4.20 from the book PDF**, overlay-validated; provenance `digitized`. Traced points in `Inman_1995_S404-407_cost_curves.json` → `S405`; L01_S405 loads via `make_curve_frame` (`registry` construction_steps).

## 3. Why these sources, author's perspective

- **Why the marginal-labor-cost figure specifically.** It carries Shaikh's most quotable empirical shock: the highest `mlc` spike is **7.5× the flat bottom** — a curve "decidedly not 'well behaved'" (p.161, verbatim). That single number is his sharpest refutation of the smooth-convex `mc` of the neoclassical firm, and it comes from a *real* engineering study, not his own arithmetic.
- **Why reproduce, not re-simulate.** Same rationale as S404 — a detailed real-plant study already shows the pattern; re-running the simulation would be new research (`S405_research.json` methodology_notes).
- **Rejected alternatives:** re-running Inman's Monte-Carlo with current data (declined, out of scope); leaving `data_unavailable` (superseded by digitization recovery); proxy substitution (never — Anu no-proxy).

## 4. Methodological-change exposure

**None** on the national-accounts axes:
- **NIPA touch — NONE**; **I-O touch — NONE**; **Concordance touch — NONE.** Single-plant engineering simulation; no BEA account, no Leontief object, no industry classification. `NIPA_CHANGE_TIMELINE.md` / `IO_CHANGE_TIMELINE.md` do not apply. A frozen 1995 exhibit with no successor vintage.

## 5. Replication fidelity note — figure-digitization recovery (honest)

Disclosed vector trace of the published Fig 4.20, overlay-validated, provenance `digitized`; V03 round-trips at tolerance 0.05; reviewer hand-check EXACT at point indices {1:113.1, 19:242.1, 38:926.4} (note the 38-point trace resolves the tall shift-spikes) (`CH04_review.json` hand_check `S405`; `registry` validation.reference_values). **Same honesty debt as S404** — flag, do not silently carry:

- **Wrong Inman citation** lingering in the research JSON (F1, HIGH); correct = Engineering Economist 41(1):53–67, DOI 10.1080/00137919508967475.
- **Stale DPR/EPR/notes/adequacy** still implying `data_unavailable` (F1/F4); **method pointer to the Tsoulfidis EXTRACTION_REPORT is wrong** (F3b) — the real trace is `extract_inman*.py` + `inman_extracted.json`.
- **content_type/construction drift** registry `theoretical`/`direct` vs research `derived`/`formula` (F5).
- **Fidelity ceiling:** reproduces Inman's plotted curve, not his exact simulation output; exact values need the paywalled article. No proxies/interpolation beyond the trace (`CH04_review.json` D13 PASS).

## 6. Forward risk

- **No meaningful numeric extension** — a modern study is a separate exhibit, never a splice (`S405_EPR.md`).
- **Live risks are documentary:** reconcile the wrong citation + stale DPR/EPR/notes (F1/F4), re-point the Inman method report (F3b); obtain the paywalled Inman (1995) only if exact values are ever needed. Part of the ch4 D14-below-90 documentary block.
- **No BEA/BLS/OECD exposure.**
