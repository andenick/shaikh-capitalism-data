# S403 — Methodological History Report (MHR)

**Series**: S403 — Total Profit with Different Wage Arrangements, at Normal Intensity for 8-Hour Shifts up to Engineering Capacity (Two and a Half Shifts) · Figure 4.18 (book p.157)
**Chapter**: 4 (Production and Costs), §V–Appendix 4.2 · **Group**: ch4 / CH04
**Status**: `book_period_validated` · `content_type: theoretical` (registry) / `derived` (research JSON) · `construction: formula` · `publish: true`
**Perspective**: authored *from Shaikh's perspective*.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S403` (carries `cross_references` → S401, S402);
`Technical/research/S403_research.json`; `Technical/docs/series/S403_DPR.md` + `S403_EPR.md`;
`Technical/methodology_review/CH04_review.json`; source CSV `SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv`;
KB `.../Body_Text/ch04_production_costs.md`, `.../Figures/ch04/ch04_figure_4.18.md`; parents `S401_MHR.md`, `S402_MHR.md`.

---

## 1. What the series is

S403 is the **profit profile** implied by the two cost calculations — the author-computed total profit `π = p·XR − tc` at output price `p=7`, plotted for both wage arrangements against cumulative daily output `XR`. It is the data behind **Figure 4.18** and is the only ch4 series with explicit registry `cross_references` (→ S401, S402): its two plotted lines are `PL` = profit under per-worker wages (= revenue − S401's `tc'`) and `PH` = profit under per-hour wages (= revenue − S402's `tc`) (`S403_research.json` components, formula; `S403_DPR.md` §1).

Book definition (Shaikh 2016 p.157, verbatim, `S403_research.json`):
> "We can, of course, calculate total profit directly at some given price, and find its maximum point, as illustrated in figure 4.18. Then, we see that the highest profit point in the case of wages paid per worker is at the end of the second shift, while that for wages paid per hour is at engineering capacity."

Same reclassification / field-drift / empty-extension story as S401–S402; the abscissa is `XR`, not time (`CH4_RESEARCH_SUMMARY.md`; `CH04_review.json` F5).

## 2. Source lineage

Same single source (`S403_DPR.md` §3; `S403_research.json` primary_source): **Shaikh, Appendix 4.2, book pp.772–781**, subsource `SHAIKH_APPENDIX_4_2`, the **profit columns of Appendix Table 4.2.4** (`π' = p·XR − tc'`; `π = p·XR − tc`). Book p.781, verbatim: *"Finally, total profit for each type of wage payment is derived as total revenue (p·XR) minus the corresponding total costs (tc' or tc). Appendix table 4.2.4 summarizes this data from which figures 4.16–4.18 are derived."* Retrieved from the same verbatim book-PDF transcription (`Appendix_4_2_Table4.csv` columns `XR, PL, PH`). No agency series, no vintage, no splice.

## 3. Why these sources, author's perspective

- **Why an explicit profit figure.** S403 delivers Chapter 4's payoff punchline: the **maximum-profit output is institution-dependent** — end of shift 2 under per-worker wages, engineering capacity under per-hour wages — which contradicts the neoclassical `p = mc` rule because with spiky multi-shift `mc` that rule "would then select a very large number of points" (p.157/161). Shaikh flags this as "crucial in discussion of their respective theories of competition (chapters 7 and 8)" (p.157, verbatim caveat) — S403 is the bridge from cost theory to the competition chapters.
- **Why derive it from S401/S402 rather than tabulate independently.** The whole point is that profit follows *mechanically* from the cost curves already built; keeping it on the same Appendix 4.2 scaffold (same `XR`, same `p=7`) makes the derivation auditable. Hence the registry `cross_references: [S401, S402]`.
- **Rejected alternatives — none empirically.** Author's own arithmetic; nothing to substitute or extend (`S403_research.json` methodology_notes).

## 4. Methodological-change exposure

**None** on any standard axis (identical to S401/S402):
- **NIPA touch — NONE**; **I-O touch — NONE**; **Concordance touch — NONE.** No BEA account, no Leontief object, no industry/country classification; the timelines (`NIPA_CHANGE_TIMELINE.md`, `IO_CHANGE_TIMELINE.md`) do not bear on a closed-form profit illustration.

## 5. Replication fidelity note

Same **read-the-truth-column** pattern (L01 reads `PL`/`PH` columns; P02 pass-through; V03 ±0.5%) → **MAE 0.0, n=42, PASS** (`CH4_RESEARCH_SUMMARY.md`). Honest limits:

- **Reviewer hand-check EXACT**: `S403_PH` {0:−70.0, 10:59.72, 20:212.48} vs `Appendix_4_2_Table4.csv` (`CH04_review.json` hand_check); review_history spot-check `PL(XR=2.84) = 7×2.84 − 178.52 = −158.64`, exact.
- **Melt-fidelity, not independent confirmation** — anchor is printed Appendix Table 4.2.4.
- **F3a reference-value re-keying** + **F5 field drift** apply identically (WARN-level; values correct). No DECOMPOSITION.md (F6). KB ch04 IS extracted (F2).
- **Cross-reference schema note:** S403's registry `cross_references` link to S401/S402 is the ch4 model for the derived-series linkage Phase 4 discussed adding project-wide (`S403_research.json` open_questions; `CH4_RESEARCH_SUMMARY.md` open-question 4).

## 6. Forward risk

- **Essentially zero data-vintage risk** — closed-form; only a transcription correction could change it.
- **Documentary debt only** — F5 field drift + F3a re-keying; no external source to re-fetch.
- **Robustness across S401/S402:** because S403 is a pure function of the two parent cost series, any future re-derivation of S401/S402 (e.g. from back-solved eq. 4.2.1 parameters) would flow through — but at ≤0.02 fidelity this is immaterial.
