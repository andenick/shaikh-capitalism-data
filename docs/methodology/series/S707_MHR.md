# S707 — Methodological History Report (MHR)

**Series**: S707 · Figure 7.19 — Deviations of Greek Manufacturing Profit Rates from Average Profit Rate, 1962–1991 (20 industries)
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` (recovered 2026-05-26) · `content_type: cross_sectional` (registry) · `construction: direct` (digitized) · `publish: true`
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 301, 305; Appendix 7.1 §IV (p. 859).
**Sources read**: `Technical/research/S707_research.json`, `Technical/series_registry.json` (S707), `Technical/methodology_review/CH07_review.json` (**H1/H2** stale-EPR findings, touchpoint S707), `SalvagedInputs/book_data/Reconstructed/Tsoulfidis_Tsaliki_2011_data_unavailable.md` (now superseded — see §5).

> **Note on stale docs (review H1/H2):** `S707_research.json` and the S707 EPR/DPR still classify this series `data_unavailable` and state "No interpolation, no digitization." That is **out of date** — the registry, loaders, and triage record the **2026-05-26 figure-digitization recovery** (MPRA 51334). This MHR documents the *current, recovered* state and flags the stale artifacts.

---

## 1. What the series is
S707 is the **Greek manufacturing average-profit-rate deviation panel**: for 20 two-digit Greek manufacturing industries, dev_i,t = ROP_i,t − ROP_avg,t, 1962–1991. It is Shaikh's reproduction of **Tsoulfidis & Tsaliki (2011) Figure 4** (their p. 19). Book source caption (page-cited, `S707_research.json`, Appendix 7.1 §IV, p. 859): *"Average and incremental profit rates for Greek manufacturing 1962-1991 (Tsoulfidis and Tsaliki 2011). Figure 7.19 Deviations of Greek Manufacturing Profit Rates from Average Profit Rate, 1962-1991. … Source: Tsoulfidis and Tsaliki 2011: 19, fig. 4, and 30, fig. 5."* Substantive finding (book p. 305): Greek **average** deviations do **not** show strong equalization over the 32-year span — the same asymmetry as the US case (S709 average weak, S710 incremental strong). Third-country corroboration of the chapter's thesis.

## 2. Source lineage
- **Ultimate authors**: Lefteris **Tsoulfidis** & Persefoni **Tsaliki (2011)**, *"Classical Competition and Regulating Capital: Theory and Empirical Evidence"* (MPRA No. **51334**; also cited by Shaikh as the 2005 University of Macedonia working paper). Shaikh's Fig 7.19 = their Fig 4.
- **Underlying agency data (behind T&T)**: Greek **National Statistical Service (ESYE, now ELSTAT)** Annual Industrial Survey (net operating surplus by 2-digit ISIC manufacturing) + **Bank of Greece** long capital-stock series (net fixed capital at constant prices). T&T's ROP = net operating surplus ÷ net fixed capital stock; deviation vs the cross-industry average.
- **Native units**: rate deviation (decimal).
- **RSCD recovery vehicle (the key fact)**: the underlying 20-industry × 30-year deviation series is **not tabulated** anywhere — T&T's paper carries only regression tables (concentration stats, correlation matrices, unit-root/AR(1) coefficients); the deviation series exists **only as line charts** (their Fig 4). RSCD therefore **recovered S707 by offline vector digitization of Tsoulfidis & Tsaliki (2011) Fig 4 (MPRA 51334)** on 2026-05-26, clipped to 1962–1991. Provenance = `digitized` (faithful to the *published figure*, not the authors' exact table).

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Shaikh cites T&T because it is an **independent replication by other authors, on other data, in another country**, that reaches "almost exactly the same results" (book p. 305) — powerful corroboration that turbulent equalization is a general law, not a US artefact. He notes a small definitional difference (T&T use change-in-gross-profit for the incremental rate; he uses change-in-GOS — book p. 301) but stresses the results are "remarkably consistent." He does **not** redistribute T&T's raw Greek data (his Appendix 7.2 is US-focused), which is exactly why RSCD had no table to transcribe.
**Rejected alternatives** (`S707_research.json` extension_candidates): modern **ELSTAT** Annual Industrial Survey and **OECD STAN (Greece)** as continuations — both rejected as splices because the **ESYE→ELSTAT transition (2010) with ISIC→NACE Rev 2 reclassification** breaks the industry basis, the Bank of Greece capital-stock methodology has changed, and STAN's Greek capital-stock coverage is sparse. The 1962–1991 window reflects data availability, not choice; no meaningful splice.

## 4. Methodological-change exposure (concordance / classification)
S707 is the chapter's **Greek classification-break** case:
- **ESYE → ELSTAT + ISIC → NACE Rev 2**: the 20 industries are on 1960s–1990s **2-digit ISIC**; the modern Greek source is on **NACE Rev 2** after the 2010 agency transition — a hard classification break with no in-project crosswalk (RSCD stages only US Census SIC↔NAICS bridges at `_sources/naics/`; Greek/ISIC↔NACE concordances are out of the staged set).
- **Capital-stock concept drift**: the Bank of Greece long capital-stock series (net, constant-price) is specific to T&T's construction; modern reconstruction is not comparable.
- **No US NIPA/BEA-IO exposure** — non-US source; `NIPA_CHANGE_TIMELINE.md`/`IO_CHANGE_TIMELINE.md` do not bear on it.
Net: a frozen foreign-source exhibit; classification exposure is a hard wall (ISIC→NACE + ESYE→ELSTAT), and the RSCD value is a **figure recovery**, so classification never had to be operationalised in data.

## 5. Replication fidelity note — digitization recovery (honest)
S707 is **not** a byte-exact table transcription and **not** `data_unavailable`; it is a **disclosed figure-digitization recovery**. RSCD offline-vector-extracted T&T Fig 4 (MPRA 51334), clipped to 1962–1991, 20 industries; provenance stamped `digitized`. Fidelity: figure-overlay **MATCH** with **point-precision verified on the top row** (registry triage; FIGURE_REPRO_ch07) — average-rate curves are lower-frequency than incremental ones, so digitization confidence is *higher* than S708. This is the sanctioned recovery under the Anu No-Synthetic rule (a faithful trace of the published figure, explicitly not the authors' exact underlying numbers). **Honesty debt (review H1/H2):** the `S707_research.json`, EPR, and DPR are **stale** — they still say `data_unavailable` / "No digitization," and a stale `Tsoulfidis_Tsaliki_2011_data_unavailable.md` marker persists in the replicator bundle. These should be updated to record the 2026-05-26 digitization (a WARN-level doc-sync deduction, not a data problem).

## 6. Forward risk
No numeric extension is meaningful — any modern Greek panel must be a **separate, methodologically-documented exhibit** (ELSTAT/NACE Rev 2), never spliced onto T&T's ISIC-era series. The live risks are documentary and archival: (1) reconcile the stale `data_unavailable` EPR/DPR/research + delete the stale marker (review H1/H2); (2) if higher fidelity is ever needed, contact the authors for the raw 20-industry series (the only route to exact values). No BEA/OECD vintage risk.
