# S402 — Methodological History Report (MHR)

**Series**: S402 — Average and Marginal Costs with Wage Paid **per Hour**, at Normal Intensity for 8-Hour Shifts up to Engineering Capacity (Two and a Half Shifts) · Figure 4.17 (book p.156)
**Chapter**: 4 (Production and Costs), §V–Appendix 4.2 · **Group**: ch4 / CH04
**Status**: `book_period_validated` · `content_type: theoretical` (registry) / `derived` (research JSON) · `construction: formula` · `publish: true`
**Perspective**: authored *from Shaikh's perspective*.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S402`; `Technical/research/S402_research.json`;
`Technical/docs/series/S402_DPR.md` + `S402_EPR.md`; `Technical/methodology_review/CH04_review.json`;
source CSV `SalvagedInputs/book_data/Reconstructed/Appendix_4_2_Table4.csv` (+ `..._README.md`); KB
`.../Body_Text/ch04_production_costs.md`, `.../Figures/ch04/ch04_figure_4.17.md`; siblings `S401_MHR.md` (per-worker twin), `S403_MHR.md`.

---

## 1. What the series is

S402 is the **per-hour-wage analogue of S401** — the same author-computed numerical illustration, but with labor paid by the hour (`wh`) instead of by the worker-shift. It tabulates `afc`, `ulc`, `avc`, `ac`, `mc` against cumulative daily output `XR` across the same 8+8+4 three-shift day, and is the data behind **Figure 4.17** (`S402_DPR.md` §1; `S402_research.json` primary_source).

Book definition (Shaikh 2016 p.154, verbatim, `S402_research.json`):
> "A similar result obtains when wages are paid per hour of work (w̄) rather than per worker. In this case, unit labor cost w̄·l(Hj,i) ≡ w̄·Hj/XRj(Hj,i) is proportional to the labor coefficient in table 4.2… As with the labor coefficient, the endpoints of unit labor costs of the first two shifts are the same."

**The distinguishing feature vs S401.** With hourly wages, within-shift `mc` is **not** flat at `pa·a`; it tracks `pa·a + wh/MPL(h)`, inheriting the within-shift shape of the marginal product of labor, while the shift-boundary spikes now come from productivity discontinuities rather than a wage-bill jump (`S402_research.json` methodology_notes; book p.154 mc quote). Shaikh stresses that a **roughly stable avc** over the desired operating range is "one of the most well-documented empirical patterns in the literature… quite unlike the U-shaped avc commonly assumed in neoclassical theory" (p.156, verbatim book_quotes). Same reclassification, drift, and `extension_candidates: []` as S401 (`CH4_RESEARCH_SUMMARY.md`; `CH04_review.json` F5).

## 2. Source lineage

Identical single source to S401 (`S402_DPR.md` §3; `S402_research.json` primary_source): **Shaikh, Appendix 4.2, book pp.772–781**, subsource `SHAIKH_APPENDIX_4_2`, the per-hour-wage columns of **Appendix Table 4.2.4**. Retrieved from the same **verbatim book-PDF transcription** that resolved blocker CH4-B1 (`Appendix_4_2_Table4.csv` columns `XR, afc, ulc, avc, ac, mc`; `Appendix_4_2_README.md`). No agency series, no vintage, no splice.

## 3. Why these sources, author's perspective

- **Why compute the per-hour case separately.** Shaikh wants to show the cost-curve conclusion is **robust to the wage-payment institution**: whether labor is a fixed per-shift bill or a variable per-hour cost, "in both cases, the marginal cost curve is highly spiky at the shift-change points" (p.156, verbatim). The per-hour variant is the more empirically realistic overtime case and yields the "roughly flat avc" stylized fact he wants to vindicate.
- **Why `wh = 12.5`.** Chosen so `wh × 8 = 100 = wN`, holding the per-shift wage bill constant across S401 and S402 so the two figures are on a common footing (`S402_research.json` components, open_questions; consistency check in review_history: `ulc(XR=2.84)=4.40` book vs `12.5×0.3521=4.401` recomputed).
- **Rejected alternatives — none empirically.** Author's own arithmetic; nothing to substitute or extend (`S402_research.json` methodology_notes: "closed-form theoretical illustration, no real-world counterpart to extend").

## 4. Methodological-change exposure

**None** on any standard axis — identical to S401.
- **NIPA touch — NONE** (no BEA account; `NIPA_CHANGE_TIMELINE.md` irrelevant).
- **I-O touch — NONE** (no Leontief object; `IO_CHANGE_TIMELINE.md` irrelevant).
- **Concordance touch — NONE** (no industry/country classification; "shifts" are an engineering index).

## 5. Replication fidelity note

Same **read-the-truth-column** reproduction: L01 reads the per-hour columns of `Appendix_4_2_Table4.csv`, P02 pass-through, V03 round-trips at ±0.5% → **MAE 0.0, n=122, PASS** (`CH4_RESEARCH_SUMMARY.md` V03 table). Honest limits:

- **Same parameter-offset caveat** as S401 (printed `a1` gives `xr(h=1)=3.15` vs tabulated `3.55`; back-solved `a1=2.40` reproduces exactly) — RSCD reads the tabulated numbers, not a re-simulation (`Appendix_4_2_README.md`).
- **Melt-fidelity, not independent confirmation** — anchor is printed Appendix Table 4.2.4; reviewer hand-check EXACT (`CH04_review.json` hand_check).
- **F3a reference-value re-keying** (point-index → `derived_statistics`, Decision 0008 outstanding) and **F5 field drift** (registry `theoretical`/`direct` vs `derived`/`formula`) apply identically — WARN-level, values correct.
- **No DECOMPOSITION.md** (F6); **KB ch04 IS extracted** (F2 — the "not extracted" premise is false).

## 6. Forward risk

- **Essentially zero data-vintage risk** — closed-form illustration; only a transcription correction could move it.
- **Documentary debt only** — F5 field drift + F3a re-keying; no external source to re-fetch or re-anchor.
