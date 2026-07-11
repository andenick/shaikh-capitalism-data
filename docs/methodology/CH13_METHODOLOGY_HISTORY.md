# Chapter 13 — Classical Macro Dynamics — Methodology History Dossier

**Group:** ch13 · **Series:** S1301 (1) · **Book pages:** 602–635 (chapter body); 883–888 (Appendix 13.1)
**Reasoning stance:** from Anwar Shaikh's own perspective — why *he* constructed the series as he did.
**Companion per-series MHR:** `Technical/docs/methodology/series/S1301_MHR.md`
**Machine-readable twin:** `Technical/methodology_review/CH13_methodology.json`

> Grounding: every claim is anchored to a citable path — the research JSON (`Technical/research/S1301_research.json`),
> `Technical/docs/chapters/CH13_RESEARCH_SUMMARY.md`, the review (`Technical/methodology_review/CH13_review.json`),
> the DPR/EPR (`Technical/docs/series/S1301_{DPR,EPR}.md`), the loader (`Technical/code/L01_loaders/L01_S1301.py`),
> and the Chapter-13 Knowledge Base (`Inputs/Capitalism Data/Technical/Knowledge_Base/HDARP_v3.3_Campaign/`).
> No claim is invented.

---

## 1. What the chapter builds

Chapter 13 ("Classical Macro Dynamics") is a **primarily theoretical** chapter: it develops the
classical/Marxian alternative to Keynesian macro — profitability (not aggregate demand) drives accumulation,
and output gravitates around a growth path set by the net profit rate and the capacity–capital ratio
(eqs. 13.41–13.43). The Phase-2 classifier flagged exactly **one** series, **S1301** (Figure 13.7), and the
whole chapter contains **no empirical time series** — every figure (13.1–13.10 in the body, plus 13.1.A/13.1.B
in Appendix 13.1) is an analytical/illustrative schematic (`CH13_RESEARCH_SUMMARY.md`).

## 2. The one series — an analytic simulation with NO external source

S1301 renders **Figure 13.7** as a realisation of Shaikh's eq. 13.43,
`ln Y_t = ln Y0 + alpha·t + eta_t` (deterministic log-linear trend + random-walk-with-drift error). Its only
"source" is Shaikh's own equation (`primary_source = SHAIKH_2016_EQ_13_43`); no BEA/BLS/FRED/IO input exists,
and no data file backs it. Two subseries ship: S1301-EQ (equilibrium trend) and S1301-ACTUAL (realised path),
152 long-form chopped rows. Full analytic rationale, disclosed parameters, and rejected alternatives are in
the per-series MHR.

## 3. Provenance correction — the "no ch13 KB" claim is FALSE (review G1)

Four artifacts (research JSON, DPR, registry `triage.reason`, explainer) assert the Chapter-13 KB does not
exist. **It does.** `HDARP_v3.3_Campaign/` carries `Body_Text/ch13_macro_dynamics.md`,
`Equations/ch13_equations.md` (eq. 13.42 and 13.43), and `Figures/ch13/ch13_fig_13.7.md`. All three
research-JSON quotes verify verbatim (body lines 1846–1855, 1872–1873, 870–873; `CH13_review.G1`). This is
understated provenance, not fabrication; the dossier and per-series MHR document the true lineage and the fix
is to flip the three quote markers to verified and restore the explainer's "From the book" section
(`CH13_review.G1.fix`, `G3`).

## 4. Methodological-change exposure — NONE

S1301 is structurally immune to source methodological change: **NIPA touch none, IO touch none, concordance
touch none.** No comprehensive BEA revision (2013/2018/2023), I-O benchmark, or NAICS/SIC concordance can move
a value, because nothing external is read. The only "drift" is the RNG realisation itself, pinned by `SEED=42`
so the committed curve reproduces bit-for-bit.

## 5. Replication fidelity — the single sanctioned `np.random`

S1301 is the **ONE audit-exempt deterministic `np.random`** in the whole project (project CLAUDE.md invariant
#4): `L01_S1301.py:39` `np.random.default_rng(SEED)`, `SEED=42`. The D13 Data-Authenticity gate scores
**100/PASS** — bounded, seeded, disclosed in 5 artifacts, deterministic, reproduces `chopped/S1301.csv`
bit-for-bit and the registry `reference_values`; explicitly *NOT a fabrication failure*
(`CH13_review.gates.D13`, `np_random_audit`). V03 = PASS_THEORETICAL (both subseries present; trend slope =
declared α to 1e-9). D14 = 92/PASS. Chapter integration score **89.5, COMPLETE** (`CH13_review`).

## 6. Per-series index

| SID | Fig | Primary concept | NIPA / IO / concordance | Key note |
|-----|-----|-----------------|--------------------------|----------|
| S1301 | 13.7 | Actual & equilibrium output paths — analytic realisation of eq. 13.43 (log-linear trend + random-walk-with-drift) | none / none / none | ONE sanctioned `np.random` (SEED=42, D13 PASS); provenance-correct the false "no ch13 KB" (G1); no vintage/extension risk |
