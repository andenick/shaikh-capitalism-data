# S703 — Methodological History Report (MHR)

**Series**: S703 · Figure 7.13 — World Manufacturing Average and Incremental Rates of Profit, 1970–1989
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` · `content_type: time_series` · `construction: machine_digitized` · **`publish: true`** (RECOVERED 2026-07-02, Decision 0019)
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 301–303; Appendix 7.1 §II (p. 856).
**Sources read**: `Technical/research/S703_research.json`, `Technical/series_registry.json` (S703), `Technical/methodology_review/CH07_review.json` (D13 gate, touchpoint S703), `SalvagedInputs/book_data/Reconstructed/Christodoulopoulos_1995_data_unavailable.md`.

---

## 1. What the series is
S703 is Shaikh's **world (8-country) manufacturing** panel of **average and incremental rates of profit**, 1970–1989, displayed as two panels of 3-year centered moving averages (8 industries + a WORLDAVG line). Book definition (page-cited, `S703_research.json`, p. 302): *"The 1994 International Sectoral Database (ISDB) (OECD 1994) contained annual data, now discontinued, from which it was possible to derive measures of gross profit (gross operating surplus … GDP minus Indirect Business Taxes … minus Employee Compensation), gross capital stock, and gross investment for various OECD countries. This was used by Christodoulopoulos (1995) to derive measures of average and incremental rates of profit by world industry … limited to the period 1970-1990 and focused on … eight manufacturing industries … across eight countries (United States, Japan, Canada, Germany, France, Italy, Belgium, and Norway)."* Substantively (p. 302) it shows **average rates cluster but persist above/below**, while **incremental rates cross back and forth** — the first tier of the chapter's three-tier empirical case for turbulent equalization. The raw underlying data remain unrecoverable, but the printed **WORLDAVG** aggregate line has now been **machine-digitized** off Fig 7.13 (RECOVERED 2026-07-02; see §5).

## 2. Source lineage
- **Ultimate source**: **OECD International Sectoral Database (ISDB), 1994 vintage** — a licensed OECD product, **discontinued**. Variables: GOS = GDP − IBT(net of subsidies) − Employee Compensation; GKS (gross capital stock); GFCF (gross investment), for 8 manufacturing industries × 8 OECD countries, 1970–1990.
- **Reconstruction author**: George **Christodoulopoulos (1995)**, an unpublished New School (NSSR) working paper; methodology further documented in **Shaikh (2008) Appendix 1**.
- **Aggregation / adjustment chain**: per-country GOS/GKS/GFCF are **PPP-converted to US dollars**, then **world totals are summed across the 8 countries per industry *before* forming ratios** (aggregate-before-ratio). ROP = GOS_world / lagged GKS_world; IROP = ΔGOS_world / lagged GFCF_world. Display transform = 3-year centered moving average (Christodoulopoulos's smoother). **No WEQ/OOH/inventory/reserve adjustments** — those are specific to the later BEA US construction (S705/S706); ISDB is a different accounting frame.
- **Native units**: rate (decimal). PPP source unconfirmed (likely PWT 5.6 or OECD PPP — `S703_research.json` open_question 3).
- **RSCD holding**: the SalvagedInputs Appendix 7.2 files (`Appendix7_ropdataUSind.xlsx`, `iropdataUSind.xlsx`) are the **1987–2005 BEA-NAICS US** panels (S705/S706), **NOT** the 1970–89 world ISDB reconstruction. The ISDB-based Christodoulopoulos file is missing; the paper is not publicly hosted.

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Shaikh used the ISDB-via-Christodoulopoulos reconstruction because in the mid-1990s **ISDB was the only database that carried industry-level gross capital stock across multiple OECD countries on a comparable basis**, making a genuine *world-industry* average rate of profit computable. The world aggregation (PPP-summed before the ratio) is the classical move: it treats "world manufacturing" as one competitive arena of regulating capitals, which is precisely the level at which Shaikh claims incremental rates equalize.
**Why not modern OECD data**: `S703_research.json` extension_candidates list OECD STAN (successor to ISDB) and OECD ICIO/TiVA. Both are rejected as reconstructions because (a) STAN's **capital-stock coverage is far sparser** than ISDB's — for many country-industry cells gross capital stock is missing, which is exactly why Shaikh's own later OECD work (S711/Fig 7.21) could only compute IROP, not ROP; (b) ISDB's 8-industry schema does not map cleanly onto STAN's **ISIC Rev 3 → Rev 4** industries; (c) ICIO carries no capital stock at all. The honest RSCD stance: S703 is a **frozen historical exhibit**, not reconstructable without fabrication.

## 4. Methodological-change exposure (concordance / classification)
S703 is the chapter's **discontinued-database + cross-country-classification** case:
- **Source discontinuity**: OECD ISDB 1994 was retired by OECD; there is no drop-in successor. Any reconstruction would jump to **OECD STAN**, forcing an **ISIC Rev 3 → ISIC Rev 4** industry crosswalk (the international analogue of the US SIC→NAICS break) for the 8 industries (Food, Textiles, Paper, Chemicals, Minerals, Metals, Machinery, Other Manufacturing). RSCD stages Census US SIC↔NAICS bridges (`_sources/naics/`) but **no ISIC Rev3↔Rev4 crosswalk** — the international concordance is out of the staged set and would have to be built (cf. S711, which faces the identical ISIC break).
- **Capital-stock concept break**: ISDB gross stock vs modern net-stock reporting is a second irreducible discontinuity (same obstacle noted in `IO_CHANGE_TIMELINE.md` capital-flow section for the US).
- **PPP vintage**: any redo must re-run PPP conversion (PWT) — a further methodology choice.
No US NIPA/BEA-IO exposure (`NIPA_CHANGE_TIMELINE.md` does not touch this non-US series).

## 5. Replication fidelity note — RECOVERED by machine digitization

> **REMEDIATED 2026-07-02 (Decision 0019) — S703 RECOVERED `data_unavailable` → `book_period_validated`.**
> The single **WORLDAVG** open-circle line was isolated from Fig 7.13's 9-line spaghetti (8 industries +
> WORLDAVG) and **machine-digitized off the printed figure**. Method chain: **dual independent extraction**
> (two agents, blind to each other — geometry-first + sampling-first) → **mechanical agreement test** →
> **per-year crop-level marker-identity adjudication** (viewed at high zoom, discriminating the WORLDAVG open
> circle ○ from the MACHEQP open diamond ◇ and the PAPER crossed-square ⊠) → **adversarial verification**
> (a fresh agent tried and FAILED to refute the curve — verdict **CONFIRMED**, no point refuted).
> **20/21 columns** are recovered; **1974 is left as an honest gap** (no defensible open-circle marker is
> resolvable on the steep 1973→1975 descent — no-guess rule). Transcription confidence **MEDIUM-HIGH**
> (per-point 0.45–0.90, **mean 0.666**, ≈ ±0.005 decimal). Book caption says "1970–1989" but the figure
> plots a 1990 column (the sharpest circle-vs-diamond discrimination in the series) — honestly included.
> A chopped CSV (20 rows, S703-A) and an extenbook now exist; V03 round-trips + 3 reference vertices +
> plausibility band, anchor suite GREEN. The **human `returns/` digitization path still supersedes** this
> machine consensus if ever filed. Durable source + evidence:
> `Technical/remediation_campaign/digitization_packet/machine/{S703_consensus.csv, S703_consensus_overlay.png, M2_adjudication_log.md, M3_verify_report.md}`.

The raw underlying world-aggregate series (Christodoulopoulos's file, the discontinued ISDB 1994 vintage) **remain unrecoverable** — Christodoulopoulos's raw file is not in `Inputs/Capitalism Data`, the NSSR working paper is not publicly hosted, and Shaikh (2008) Appendix 1 describes the *method* but does not *tabulate* the world series. What has changed is that the **printed WORLDAVG line has now been machine-digitized**: rather than leaving the exhibit chart-only, we read Shaikh's plotted aggregate line directly off Fig 7.13. This is a disclosed reading of the printed figure (`provenance: machine_digitized`), explicitly *not* a memory or proxy fill (project CLAUDE.md anti-pattern #5) and *not* a reconstruction from modern data. It satisfies the Anu No-Synthetic / no-fabrication rule and the CH07 D13 gate. The earlier data_unavailable provenance note (`SalvagedInputs/book_data/Reconstructed/Christodoulopoulos_1995_data_unavailable.md`) is retained as history and superseded by this recovery for the WORLDAVG line.

## 6. Forward risk
The book-period WORLDAVG line is now machine-digitized and `publish: true`. The remaining **optional superseding path** is a **guided human digitization** of the aggregate line — a manual, disclosed act constrained by the No-Synthetic rule, never an API splice — filed at `Technical/remediation_campaign/digitization_packet/returns/S703_aggregate_digitized.csv`; it would supersede the machine consensus (`human_guided` > `machine_digitized`) and `L01_S703` prefers it automatically. A full data reconstruction remains high-risk and low-fidelity: it would require an archived ISDB 1994 copy (unavailable) or an OECD-STAN redo carrying an ISIC Rev3→Rev4 crosswalk, sparse capital-stock imputation, and a PWT PPP choice — a chain of methodology decisions that would not reproduce Shaikh's figure and should be presented, if ever, as a *new* exhibit, not an extension.
