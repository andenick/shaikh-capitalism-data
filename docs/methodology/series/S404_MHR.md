# S404 — Methodological History Report (MHR)

**Series**: S404 — Automotive Unit Labor Cost · Figure 4.19 (book p.162)
**Chapter**: 4 (Production and Costs), §VI (Inman's empirical cost curves) · **Group**: ch4 / CH04
**Status**: `book_period_validated` (recovered 2026-05-26) · `content_type: theoretical` (registry) / `derived` (research JSON) · `construction: direct` (digitized) · `publish: true`
**Perspective**: authored *from Shaikh's perspective*.
**Authored**: 2026-06-30 · **Read-only provenance**; every author-intent claim traces to a cited path, or is marked "not located in corpus."

Grounding: `Technical/series_registry.json` → `series.S404` (lines ~14566–14686, incl. `unverified_inman_citation` flag);
`Technical/research/S404_research.json` (**carries the WRONG Inman citation — see §2/§5**); `Technical/docs/series/S404_DPR.md`
(recovery banner line 8 + **stale §3/§4/§7/§9**) + `S404_EPR.md` (stale); `Technical/methodology_review/CH04_review.json` (**F1, F3b, F4, F5**);
digitized source `SalvagedInputs/book_data/Reconstructed/Inman_1995_S404-407_cost_curves.json`;
trace scripts `Technical/WL1_Tsoulfidis_Tsaliki/extract_inman*.py` + `inman_extracted.json` + `inman_S404-407_native/overlay.png`;
KB `.../Body_Text/ch04_production_costs.md` (lines 2330, 2393–2395), `.../Figures/ch04/ch04_figure_4.19.md`;
siblings `S405_MHR.md`, `S406_MHR.md`, `S407_MHR.md`, and `S707_MHR.md` (the other figure-digitization recovery).

---

## 1. What the series is

S404 is Shaikh's **Figure 4.19 — simulated automotive unit labor cost (USD per car) plotted against annual vehicle production (thousands)**, reproduced from **Inman (1995), fig. 3**. Inman's values are the means of a **Monte-Carlo simulation of one automotive assembly plant's cost structure** across output 0–~450 thousand vehicles/year, with explicit "Add Second Shift"/"Add Third Shift" markers and a vertical segment at engineering capacity (`S404_DPR.md` §1; `S404_research.json` primary_source).

This is a **cost-vs-output curve, not a calendar time series** — the abscissa is annual output, carried as a 1-based point index in the `year` column (`registry` `year_column_is_index`; `S404_DPR.md` §1).

Book definition (Shaikh 2016 p.161, verbatim, `S404_research.json`):
> "Unit labor cost as shown in figure 4.19, includes both the fixed and variable components of labor cost. The fixed portion of labor compensation creates a falling component which becomes less influential at higher scales of production, while overtime creates rising components with spikes at each successive shift… The overall result is a deformed U-shape with spikes at the beginning of each shift and roughly similar minimum points for each shift."

KB caption (verbatim, `ch04_production_costs.md` line 2393–2395; `ch04_figure_4.19.md`): *"Figure 4.19 Automotive [Unit Labor Cost] Source: Inman 1995, 61, fig. 3."*

## 2. Source lineage

- **Ultimate source — the CORRECT citation.** Robert R. **Inman** (1995), *"Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive Assembly Plants,"* **The Engineering Economist 41(1), 53–67, DOI 10.1080/00137919508967475** — verified via Crossref (`S404_DPR.md` §3; registry subsource `INMAN_1995_ENGINEERING_ECONOMIST`). **⚠ Do NOT use the citation in `S404_research.json`** (lines 37–40), which still names *"Robert P. Inman," "How to Have a Fiscal Crisis: Lessons from Philadelphia," Brookings*, with a Google-Books URL to an unrelated volume — all **wrong** and flagged both by the research JSON's own open_question and by registry `unverified_inman_citation` / `CH04_review.json` **F1 (HIGH)**.
- **Underlying data behind Inman.** A detailed engineering study of an automotive plant: fixed labor cost encodes layoff pay ("95% of after-tax pay less $17.50 a week", Inman pp.55,59), variable labor cost sums overtime / full-time / under-time / shift premia; all curves are Monte-Carlo means (Inman pp.56–57) (`S404_research.json` components; book p.160 verbatim).
- **RSCD recovery vehicle — the key fact.** Inman reports the simulation **only as figures 3–6**; no tabulated series exists and the Taylor & Francis full text is paywalled (403 anti-bot on the DOI probe — `S404_DPR.md` §7 caveat 4). RSCD therefore **recovered S404 on 2026-05-26 by offline native-resolution vector trace of Shaikh's reproduced Fig 4.19 from the book PDF**, overlay-validated against the figure; provenance = `digitized` (faithful to the *published figure*, explicitly not Inman's exact underlying numbers). The 22 traced (output, value) points live in `Inman_1995_S404-407_cost_curves.json` → `S404.curve_native`; L01_S404 loads them via `make_curve_frame` (`registry` construction_steps; `S404_DPR.md` banner line 8).

## 3. Why these sources, author's perspective

- **Why Inman.** Shaikh calls Inman "one of the most striking illustrations of actual cost curves" (p.160, verbatim) — it is an **independent engineering study of a real plant** whose simulated curves turn out "strikingly similar to the theoretical curves previously depicted in figures 4.16 and 4.17" (p.161, verbatim S406 quote). This closes Chapter 4's **theoretical-to-empirical loop**: S404–S407 supply the empirical counterpart to the S401–S402 derivation, the "key factor" in both being "the spike in costs at the beginning of a new shift." S404 specifically demonstrates the "deformed U-shape."
- **Why reproduce the figure rather than re-simulate.** Shaikh's argument is that a *real, detailed* cost study already exhibits the pattern; re-running a Monte-Carlo would be "a research project, not a data pull" (`S404_research.json` methodology_notes). RSCD honors that by tracing the published curve, not fabricating a simulation.
- **Rejected alternatives.** (1) **Re-running Inman's Monte-Carlo with current automotive data** — declined as out-of-scope research, not replication (`S404_research.json` methodology_notes). (2) **Leaving the series `data_unavailable`** — the original Phase-3/5 disposition, later **superseded** by the sanctioned Anu figure-digitization recovery (`CH04_review.json` strengths; `S707_MHR.md` §5 for the parallel precedent). (3) **A proxy cost study** — never entertained (Anu no-proxy).

## 4. Methodological-change exposure

**None on the standard national-accounts axes** — S404 is a single-plant engineering simulation, not an official statistic.
- **NIPA touch — NONE**; **I-O touch — NONE**; **Concordance touch — NONE.** No BEA account, no Leontief inverse, no SIC/NAICS/ISIC dimension; the "shifts" and "annual output" are engineering quantities. The `NIPA_CHANGE_TIMELINE.md` / `IO_CHANGE_TIMELINE.md` do not apply.
- **The only "vintage" is the figure itself** — a frozen 1995 exhibit; there is no next release of the same simulation.

## 5. Replication fidelity note — figure-digitization recovery (honest)

S404 is **not** a byte-exact table transcription and **not** `data_unavailable`; it is a **disclosed vector-trace of the published Fig 4.19**, overlay-validated, provenance `digitized` — the sanctioned recovery under the Anu no-synthetic rule (`CH04_review.json` D13 PASS: "figure digitization is the sanctioned Anu recovery path, honestly labeled"). V03 round-trips the processed parquet against the digitized source at tolerance 0.05; reviewer hand-check EXACT at point indices {1:465.9, 11:207.5, 22:464.2} (`CH04_review.json` hand_check `S404`; `registry` validation.reference_values). **Honesty debt this MHR flags (must be remediated before external distribution — `CH04_review.json` D14 FAIL, F1/F4):**

1. **Wrong Inman citation in `S404_research.json`** (Robert P. Inman / "How to Have a Fiscal Crisis" / Brookings / Google-Books URL). The correct record is Robert R. Inman, *Engineering Economist* 41(1):53–67, DOI 10.1080/00137919508967475 — already in the registry, DPR §3, and subsource metadata. **F1 (HIGH).**
2. **Stale DPR/EPR bodies.** `S404_DPR.md` §3/§4/§7/§9 still assert "NOT RETRIEVABLE / data_unavailable / 'we do not digitize values' / PASS_DATA_UNAVAILABLE", directly contradicting the recovery banner (line 8) and the built `chopped/S404.csv`; `S404_EPR.md` is likewise stale (`derived/data_unavailable`). **F1 (HIGH).**
3. **Wrong method pointer (F3b, MED).** The registry subseries `source` and DPR banner cite `WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md` as the Inman method, but that report documents **Tsoulfidis & Tsaliki / S707–S708**, not Inman. The actual Inman trace lives *un-narrated* in `extract_inman*.py` + `inman_extracted.json` + `inman_S404-407_native/overlay.png`.
4. **Stale notes/adequacy (F4).** `notes` still say "data_unavailable"; `adequacy.issues_outstanding` still lists resolved blockers CH4-B1/B2. **Content_type/construction drift (F5):** registry `theoretical`/`direct` vs research `derived`/`formula`.
5. **Fidelity ceiling:** a figure trace reproduces Inman's *plotted curve*, not his exact simulation output; the only route to exact values is the paywalled article. No proxies, no interpolation beyond the trace (`CH04_review.json` D13).

## 6. Forward risk

- **No numeric extension is meaningful.** A modern automotive cost study would be a **separate, methodologically-documented exhibit**, never spliced onto Inman's 1995 curve (`S404_EPR.md` §1/§9).
- **The live risks are documentary/archival, not data-vintage:** (a) fix the wrong `S404_research.json` citation and reconcile the stale DPR/EPR/notes/adequacy (F1/F4); (b) re-point or author an Inman-specific method report so F3b's mislabeled EXTRACTION_REPORT pointer resolves; (c) if higher fidelity is ever required, obtain the paywalled Inman (1995) for exact tabulated values. **This documentary debt is what holds ch4's D14 below 90 and blocks external distribution** (`CH04_review.json` D14).
- **No BEA/BLS/OECD exposure** — nothing to re-fetch or re-anchor.
