# S708 — Methodological History Report (MHR)

**Series**: S708 · Figure 7.20 — Deviations of Greek Manufacturing Incremental Profit Rates from Average Incremental Rate, 1962–1991 (20 industries)
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` (recovered 2026-05-26) · `content_type: cross_sectional` (registry) · `construction: direct` (digitized) · `publish: true`
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 301, 305; Appendix 7.1 §IV (p. 859).
**Sources read**: `Technical/research/S708_research.json`, `Technical/series_registry.json` (S708), `Technical/methodology_review/CH07_review.json` (**H1/H2**, touchpoint S708), `SalvagedInputs/book_data/Reconstructed/Tsoulfidis_Tsaliki_2011_data_unavailable.md` (superseded — see §5).

> **Note on stale docs (review H1/H2):** as with S707, `S708_research.json` + EPR/DPR still say `data_unavailable`; the current state is the **2026-05-26 digitization recovery** (MPRA 51334). This MHR documents the recovered state.

---

## 1. What the series is
S708 is the **incremental** Greek panel — the companion to S707: for 20 Greek manufacturing industries, dev_i,t = IROP_i,t − IROP_avg,t, 1962–1991. It reproduces **Tsoulfidis & Tsaliki (2011) Figure 5** (their p. 30; = 2013 revision Fig 6). Book definition (page-cited, `S708_research.json`, p. 305): *"On the other side, they find much stronger visual support for long-run equalization in the case of the incremental rates of profit displayed in figure 7.20."* So S708 (incremental) shows **strong** equalization where S707 (average) shows weak — the same average-vs-incremental asymmetry Shaikh finds for the US (S709 vs S710). It is the Greek incremental limb of the three-tier case.

## 2. Source lineage
- **Ultimate authors**: **Tsoulfidis & Tsaliki (2011)**, MPRA No. **51334**, Figure 5 (p. 30) = Shaikh Fig 7.20.
- **Underlying agency data (behind T&T)**: Greek **ESYE (now ELSTAT)** Annual Industrial Survey — gross profit and gross investment by 2-digit ISIC manufacturing. T&T's IROP numerator = **change in gross profit** (their 2005 p. 14 definition), denominator = lagged gross investment; deviation vs the cross-industry average.
- **Definitional note (book p. 301)**: T&T use Δ(gross profit)/gross investment; Shaikh in his *own* OECD Fig 7.21 (S711) uses Δ(GOS)/gross investment. Gross profit subtracts a wage equivalent; GOS does not — a small difference Shaikh judges empirically minor.
- **Native units**: rate deviation (decimal).
- **RSCD recovery vehicle**: like S707, the 20-industry × 30-year IROP-deviation series is **not tabulated** in the paper (Tables 4/5 hold only AR(1) coefficients a, b, a/(1−b), R²) — it exists **only as line charts** (their Fig 5). RSCD **recovered S708 by offline vector digitization of Fig 5 (MPRA 51334)** on 2026-05-26, clipped to 1962–1991.

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Same rationale as S707: an **independent, other-country replication** corroborating that *incremental* rates equalize strongly while *average* rates do not. S708 is the decisive Greek limb because it matches Shaikh's cleanest US result (S710: all industries cross zero) with foreign data and a slightly different incremental definition — reinforcing his claim that the pattern is robust to "variations in the exact measures" (book p. 301). Shaikh does not redistribute T&T's raw data, so RSCD had no table.
**Rejected alternatives** (`S708_research.json`): ELSTAT / OECD STAN Greece continuations — rejected for the same ESYE→ELSTAT + ISIC→NACE Rev 2 break, uneven post-2000 Greek 2-digit investment data, and sparse STAN Greek coverage. No splice.

## 4. Methodological-change exposure (concordance / classification)
Identical to S707's Greek classification-break exposure:
- **ESYE → ELSTAT + ISIC → NACE Rev 2** — hard classification wall; no in-project Greek/ISIC↔NACE crosswalk (only US Census SIC↔NAICS staged at `_sources/naics/`).
- **Investment-side data drift**: Greek 2-digit manufacturing GFCF post-2000 is uneven and may not match T&T's coverage — a second obstacle to any continuation.
- **No US NIPA/BEA-IO exposure**.
The incremental measure adds a fidelity (not classification) wrinkle: IROP curves are **high-frequency**, so the digitization is inherently lower-precision than S707 (§5).

## 5. Replication fidelity note — digitization recovery (honest, lower confidence)
S708 is a **disclosed figure-digitization recovery**, provenance `digitized`. Because incremental-rate curves are high-frequency and spiky, per-year confidence is **lower than S707**: registry triage records figure-overlay **MATCH on structure but MINOR_DEV on per-point precision** — values are **approximate** (FIGURE_REPRO_ch07). This is the honest ceiling of what a figure-only source allows under the No-Synthetic rule; RSCD discloses the approximation rather than fabricating exact numbers. **Honesty debt (review H1/H2):** `S708_research.json` + EPR/DPR are **stale** (`data_unavailable` / "No digitization"), and the stale `Tsoulfidis_Tsaliki_2011_data_unavailable.md` marker persists in the replicator bundle — update to record the 2026-05-26 digitization (WARN-level doc-sync deduction).

## 6. Forward risk
No numeric extension meaningful; a modern Greek IROP series must be a separate NACE Rev 2 exhibit, never a splice. Fidelity risk is elevated by the high-frequency digitization — if the per-point precision matters downstream, only the authors' raw series (or the underlying ESYE data) would improve it. Documentary risks: reconcile the stale `data_unavailable` docs + remove the stale marker (review H1/H2). No BEA/OECD vintage risk.
