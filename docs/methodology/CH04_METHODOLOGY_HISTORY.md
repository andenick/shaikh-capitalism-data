# Chapter 4 — Methodological History: "Production and Costs"

**Project:** RSCD — replication of Anwar Shaikh, *Capitalism: Competition, Conflict, Crises* (Oxford University Press, 2016).
**Scope:** 8 series, S401–S408 (Figures 4.16–4.23; book pp.153–164, Appendix 4.2 pp.772–781).
**Author:** Phase-2 methodological-historian agent (2026-06-30).
**Companion artifacts:** per-series MHRs at `Technical/docs/methodology/series/S40#_MHR.md`; machine-readable digest `Technical/methodology_review/CH04_methodology.json`; review findings `Technical/methodology_review/CH04_review.json`; change timelines `Technical/docs/methodology/_timelines/{NIPA,IO}_CHANGE_TIMELINE.md`; source recovery `SalvagedInputs/book_data/Reconstructed/{Appendix_4_2_Table4.csv, Inman_1995_S404-407_cost_curves.json}`; KB `Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/Body_Text/ch04_production_costs.md`.

This dossier reads Chapter 4 *from Shaikh's own perspective*: why he built each cost-curve exhibit the way he did, which alternatives he rejected, and how each series is (or is not) exposed to vintage/reclassification history. Every author-intent claim in the per-series MHRs is grounded in a citable path; where the corpus contains no rejection rationale, the MHRs say so rather than inventing one.

---

## 1. What the chapter is for, and what that implies for sourcing

Chapter 4 rebuilds the theory of the firm on a classical/post-Keynesian foundation, and its empirical target is a single neoclassical postulate: the **smooth U-shaped cost curve**. Shaikh's strategy is a **three-part attack**, and the eight series map exactly onto it (`S408_DPR.md` §2; body `ch04_production_costs.md`):

- **Theory (S401–S403).** Shaikh *computes his own* numerical illustrations from a stylized within-shift productivity function (Appendix 4.2, eq. 4.2.1) to show that plausible engineering assumptions generate spiky, multi-shift cost curves with a maximum-profit output that is institution-dependent — nothing like the textbook U.
- **Real-plant simulation (S404–S407).** He reproduces Robert R. Inman's (1995) Monte-Carlo cost study of an automotive assembly plant, which he calls "strikingly similar" to his own theoretical curves — closing a **theory→evidence loop** (p.161).
- **Practitioner survey (S408).** He cites Eiteman & Guthrie's (1952) survey in which 94% of business managers chose steadily-declining cost curves over the U-shape.

The decisive implication for sourcing: **none of these eight series is an official statistic**. There is no BEA/BLS/OECD feed anywhere in the chapter. The provenance work is therefore entirely about (a) reconstructing Shaikh's own appendix arithmetic and (b) recovering two figure-only external sources — not about splicing agency vintages. This is what makes Chapter 4 the cleanest chapter on the national-accounts axes and the *most* documentation-sensitive on the honesty axis.

## 2. The three construction archetypes in Chapter 4

**(A) Author-computed numerical illustration** (S401, S402, S403 — Figs 4.16–4.18). Closed-form cost/profit curves Shaikh tabulates himself in **Appendix Table 4.2.4** from eq. (4.2.1) plus stylized parameters (`d=0.05, pMK=100, pa=10, a=0.30, wN=100, wh=12.5, p=7`). The abscissa is cumulative output `XR`, never calendar time. S403 is a pure function of S401+S402 (registry `cross_references`). No external data; nothing to extend.

**(B) Reproduced figure-only external simulation** (S404, S405, S406, S407 — Figs 4.19–4.22). Reproductions of Inman (1995) figs 3–6. Inman published the simulation **only as figures**, and the article is paywalled — so RSCD recovered all four by **offline native-resolution vector trace of Shaikh's reproduced figures from the book PDF** on 2026-05-26, overlay-validated, provenance `digitized`. S406 derives from S404 + constant material cost; S407 from S405 + constant marginal material cost.

**(C) Cross-sectional survey snapshot** (S408 — Fig 4.23). Two scalar percentages (94.0, 94.3) transcribed verbatim from the book text, from Eiteman & Guthrie (1952) AER. `publish: false` — culled from the web because two isolated scalars do not render as a chart, though the values are preserved in the data download.

All three archetypes carry `extension_candidates: []` correctly: (A) and (B) have no calendar axis, (C) is a one-shot 1952 cross-section. The pipeline's `time_series → extension` rule never fires for the chapter (`CH4_RESEARCH_SUMMARY.md` "Critical reclassification").

## 3. Source-selection logic and rejected alternatives, from Shaikh's perspective

Because the chapter contains no agency series, the "source choices" are really *evidential* choices — which theoretical construction, which real-world study, which survey best refutes the U-shape:

- **Why compute Appendix 4.2 rather than cite a cost study for the theory (S401–S403).** Shaikh wants a fully transparent, reproducible worked example where every cost component is visible, so the reader can *see* how a within-shift productivity hump plus multi-shift operation produces spikes and institution-dependent profit maxima. He computes both the per-worker (S401) and per-hour (S402) wage cases to show the conclusion is robust to the wage institution ("in both cases, the marginal cost curve is highly spiky at the shift-change points," p.156), then derives profit (S403) to reach the punchline that `p = mc` "would select a very large number of points" (p.157/161) — the bridge to the competition chapters 7–8.
- **Why Inman (1995) for the empirical leg (S404–S407).** Shaikh calls it "one of the most striking illustrations of actual cost curves" (p.160): an *independent engineering study of a real plant* whose simulated curves reproduce his theoretical shapes — the "deformed U-shape with spikes." The most quotable datum, the marginal-labor-cost spike **7.5× the flat bottom** (p.161, S405), and the material-cost-dominated flat `mc` that defeats `p = mc` (p.161, S407), are both Inman's, not his own — powerful because they are external.
- **Why Eiteman & Guthrie (1952) for the survey leg (S408).** It is the canonical large-n practitioner refutation; Shaikh embeds it in a lineage (footnote 36, p.164: Bain 1948, Johnston 1960, Walters 1963, Dean 1976, Mansfield 1988, Kahn 1989, Lavoie 1992 via Miller 2000) and *self-critiques* it (the survey "did not allow for multiple shifts," p.164).
- **Rejected alternatives (all grounded):** (1) **Re-running Inman's Monte-Carlo with current automotive data** — declined as "a research project, not a data pull" (S404–S407 research JSONs). (2) **Leaving S404–S407 `data_unavailable`** — the original disposition, later superseded by the sanctioned Anu figure-digitization recovery. (3) **Any proxy cost study or proxy survey** — never entertained (Anu no-proxy). (4) **Persisting S408's eight chart shapes as data** — declined; they are qualitative schematics, so only the survey percentages are registered. (5) **Treating S408's corroborating literature as an extension** — declined; tracked as a possible Phase-6 narrative note, not a data series. Where the book does not state a rejection rationale, the MHRs say "not located in corpus."

## 4. Methodological-change exposure — the chapter's shared (null) vintage story

Chapter 4 is the **null case** for the Phase-0 timelines, and that is itself the finding:

- **NIPA touch — NONE, for all 8 series.** No BEA product account is used anywhere in the chapter; the NIPA comprehensive-revision / reference-year story (`NIPA_CHANGE_TIMELINE.md`) that dominates Chapters 2/6/7 simply does not reach these exhibits.
- **I-O touch — NONE, for all 8 series.** No input–output matrix, no Leontief inverse; the SIC→NAICS "Ch9 wall" (`IO_CHANGE_TIMELINE.md`) is irrelevant.
- **Concordance touch — NONE, for all 8 series.** The "shifts" in S401–S407 are an engineering index, "annual vehicle output" is a physical quantity, and S408 is a survey percentage — no SIC/NAICS/ISIC industry dimension and no country mapping anywhere.

So the only "vintage" risk in the whole chapter is **fidelity to the frozen printed/figured source**: the accuracy of the Appendix-4.2 transcription (S401–S403), the accuracy of the figure trace (S404–S407), and the accuracy of the two transcribed percentages (S408). There is nothing to re-fetch, re-index, or splice across a revision boundary. This is why Chapter 4 scores D13 = 96 (authenticity) yet is bottlenecked on D14 (intelligibility/honesty-of-docs) rather than on data vintage.

## 5. Replication fidelity and the chapter's honesty debt (the load-bearing section)

Data authenticity is strong: the reviewer hand-checked reference values for **all 8 series EXACT vs primary ground truth** (`CH04_review.json` hand_check; D13 PASS 96). S401–S403 round-trip the transcribed Appendix Table 4.2.4 at MAE 0.0; S404–S407 round-trip the overlay-validated figure trace at tolerance 0.05; S408 matches the two book-quoted percentages exactly. The figure digitization is the **sanctioned Anu recovery path, honestly labeled `provenance: digitized`** — a faithful trace of the *published figure*, explicitly not the authors' exact underlying numbers — not fabrication.

But the chapter carries a real **documentation/honesty debt** that blocks external distribution (D14 = 85, FAIL-below-90), and the MHRs flag every item rather than paper over it:

1. **F1 (HIGH) — wrong Inman citation + contradictory DPR bodies (S404–S407).** `S404_research.json` still names *"Robert P. Inman," "How to Have a Fiscal Crisis: Lessons from Philadelphia," Brookings*, with a Google-Books URL — **all wrong**. The correct, Crossref-verified citation is **Robert R. Inman (1995), "Shape Characteristics of Cost Curves Involving Multiple Shifts in Automotive Assembly Plants," *The Engineering Economist* 41(1), 53–67, DOI 10.1080/00137919508967475** (already in the registry, DPR §3, and subsource metadata). Every S404–S407 MHR uses only the correct citation and flags the wrong one. Compounding it: the S404–S407 DPR §3/§4/§7/§9 and EPR bodies are **stale** — they still assert `data_unavailable` / "we do not digitize values" / `PASS_DATA_UNAVAILABLE`, directly contradicting their own recovery banners and the built chopped CSVs.
2. **F2 (MED-HIGH) — the "ch04 not HDARP-extracted" premise is false.** All 8 triage strings claim ch04 was not extracted, and on that false basis suppress the web "From the book" section for S404–S408. In fact `Body_Text/ch04_production_costs.md` (2,538 lines) covers the whole chapter, including the Inman captions (lines 2393/2421/2447/2475) and the Eiteman & Guthrie caption (line 2498). KB-anchored quotes *are* available.
3. **F3b (MED) — wrong method pointer.** The registry subseries and DPR banners cite `WL1_Tsoulfidis_Tsaliki/EXTRACTION_REPORT.md` as the Inman digitization method, but that report is entirely about Tsoulfidis & Tsaliki (S707/S708). The actual Inman trace lives un-narrated in `extract_inman*.py` + `inman_extracted.json` + `inman_S404-407_native/overlay.png`.
4. **F3a (MED) — reference-value re-keying.** S401–S407 `reference_values` are still point-index keyed (Decision 0008: point-index → `derived_statistics` reconciliation outstanding). Values correct; schema/keying only.
5. **F4 (MED) / F5 (LOW) — stale notes/adequacy + content_type drift.** S404–S407 `notes` still say `data_unavailable`; adequacy still lists resolved blockers CH4-B1/B2; registry `content_type:"theoretical"`/`construction:"direct"` diverges from the research JSONs' `derived`/`formula`.
6. **F7 (LOW) — honestly-flagged unverified item.** S408's JSTOR stable_id 1812527 is `unverified-rate-limited` (403 anti-bot), and `CH4_RESEARCH_SUMMARY.md` (dated 2026-05-18) predates the 2026-05-26 Inman recovery — mark stale.

None of these is a data-authenticity problem; all are doc/registry reconciliations. The remediation is documentary: correct the S404 research citation, refresh the four stale DPR/EPR bodies, fix the false "not extracted" triage premise, re-point the Inman method report, and finish the Decision-0008 re-keying.

## 6. Forward risk — the chapter view

- **Essentially zero data-vintage risk across all 8 series.** S401–S403 can change only via a transcription correction (or an optional re-derivation from back-solved eq.-4.2.1 parameters, immaterial at ≤0.02); S404–S407 only via a higher-fidelity re-trace or acquisition of the paywalled Inman article for exact tabulated values; S408 only via a transcription/citation correction or interactive JSTOR confirmation. No BEA/BLS/OECD exposure anywhere.
- **The live risk is documentary, and it is what gates external distribution.** Until F1/F2 (and F3a/F3b/F4/F5) are remediated, the chapter stays D14-below-90. The MHRs are written to make that debt explicit and actionable rather than to obscure it.
- **No meaningful numeric extension exists for any series.** A modern automotive cost study (S404–S407) or a modern managerial survey (S408) would be a *separate, methodologically-documented exhibit*, never spliced onto the 1995/1952 originals; the S401–S403 illustrations have no real-world counterpart to extend at all.
