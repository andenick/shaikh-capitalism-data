# S704 — Methodological History Report (MHR)

**Series**: S704 · Figure 7.14 — US Manufacturing Average and Incremental Rates of Profit, 1960–1989
**Chapter**: 7 (Real Competition) · Group `ch07`/`CH07`
**Status**: `book_period_validated` · `content_type: time_series` · `construction: machine_digitized` · **`publish: true`** (RECOVERED 2026-07-02, Decision 0019 — see §5 banner)
**Author intent reasoned from**: Shaikh, *Capitalism* (2016), ch.7 pp. 301–304; Appendix 7.1 §II (p. 856).
**Sources read**: `Technical/research/S704_research.json`, `Technical/series_registry.json` (S704), `Technical/methodology_review/CH07_review.json` (D13, touchpoint S704), `SalvagedInputs/book_data/Reconstructed/Christodoulopoulos_1995_data_unavailable.md`.

---

## 1. What the series is
S704 is the **US-manufacturing-only** counterpart of S703: annual average and incremental rates of profit for ~14 US manufacturing sub-industries, 1960–1989, **unsmoothed** (contrast S703's 3-year moving average). Book definition (page-cited, `S704_research.json`, p. 302): *"Figure 7.14 depicts the annual total and incremental profit rates for US manufacturing alone from the same database for 1960-1989, not smoothed this time. As in the previous case, the rates of profit on total capital exhibit some persistent differences in levels, whereas the incremental rates of profit exhibit considerable crossing."* Same three-tier logic: it is the US slice of the ISDB world experiment, giving a longer (1960→) national window before Shaikh switches to BEA-NAICS for 1987+ (S705/S706). RSCD holds the **US-manufacturing AVERAGE line (USMANAVG)** only — recovered by machine-digitizing that single bold aggregate stroke off the printed figure (see §5). The raw Christodoulopoulos ISDB table itself remains lost; the figure is now the source.

## 2. Source lineage
- **Ultimate source**: **OECD ISDB 1994 vintage, US subset** — discontinued. GOS/GKS/GFCF for ~14 US manufacturing sub-industries (ISDB internal codes USAFOD, USATEX, USAPAP, USACHE, USAMNM, USAMAI, USAMEL, USAMEQ, USAMOT, USAWOD, … + USMANAVG aggregate), 1960–1989, current USD.
- **Reconstruction author**: **Christodoulopoulos (1995)**; method in **Shaikh (2008) Appendix 1**. Shares the S703 lineage exactly (same paragraph in book Appendix 7.1 §II).
- **Aggregation / adjustment chain**: per sub-industry, ROP = GOS / lagged GKS, IROP = ΔGOS / lagged GFCF; the USMANAVG aggregate is summed across sub-industries **before** ratio formation (aggregate-before-ratio). **No smoothing** (unlike S703). **No WEQ/OOH/inventory/reserve** (ISDB frame, not the BEA frame).
- **Native units**: rate (percent; left-panel y −10%→60% for ROP, right-panel −20%→25% for IROP).
- **RSCD holding**: same as S703 — the SalvagedInputs `Appendix7_*.xlsx` are the 1987–2005 BEA US panels, **not** the 1960–89 ISDB US subset; the ISDB file is missing.

## 3. Why these sources (Shaikh's perspective) + rejected alternatives
Shaikh presents S704 to show the equalization asymmetry (average rates differ persistently; incremental rates cross) holds **at the single-country level with raw, unsmoothed annual data** — a sterner visual test than the smoothed world panel. He uses ISDB rather than BEA for this window precisely because ISDB carried **gross** capital stock (needed for the average rate) on a basis comparable to the other 7 countries in S703; **BEA now publishes only net stock**, which is why for the *post-1987* US he pivots to the net-stock-based construction of Figs 7.15–7.18 (S705/S706).
**Rejected alternatives** (`S704_research.json`): BEA GDPbyIndustry + Fixed Asset Tables (3.1ES/3.7ES) are the obvious US replacement but (a) BEA is **NAICS post-1997 / SIC pre-1997**, neither matching ISDB's schema — no direct splice; (b) **BEA net vs ISDB gross capital-stock concept** breaks comparability; reconstruction would require recomputing gross stock from gross-investment flows + retirement assumptions. Shaikh himself resolves this not by extending Fig 7.14 but by starting a *fresh* BEA-based construction in 1987 — so RSCD treats S704 as a **frozen 1960–89 exhibit**.

## 4. Methodological-change exposure (concordance / classification)
S704 sits astride **two** classification/vintage walls:
- **ISDB → BEA schema break**: ISDB's US sub-industry codes are neither SIC nor NAICS; any continuation into BEA data requires mapping ISDB codes → SIC (pre-1997) → NAICS (post-1997), invoking the full Census bridge chain staged at `_sources/naics/` (see `IO_CHANGE_TIMELINE.md` "SIC → NAICS break"). The 1972→1998 non-conformability that dooms Ch9's historical panel is the same wall here.
- **Gross→net capital-stock concept break**: irreducible; documented in `IO_CHANGE_TIMELINE.md` (capital-flow / stock section) and `S704_research.json` extension concerns.
- If instead reconstructed via OECD STAN (the S703 route), the **ISIC Rev 3 → Rev 4** break applies (no in-project crosswalk).
No live NIPA-vintage exposure for the *book-period* series (it is ISDB, not NIPA); NIPA exposure would only arise on a BEA-based reconstruction.

## 5. Replication fidelity note — RECOVERED by machine digitization

> **REMEDIATED 2026-07-02 (Decision 0019).** S704 was RECOVERED from `data_unavailable`
> to **`book_period_validated`** by **machine digitization of the printed Fig 7.14 average
> panel**. The **USMANAVG boldest-markerless line** was traced by two independent extractors
> (geometry-first + sampling-first, mutually blind). The raw mechanical agreement gate FAILED
> at **53%** — but the failure was fully diagnosed as **extractor-B's systematic +1-year
> x-offset** (B mis-numbered the tick ladder: the first tick sits ~1 year right of the printed
> "1960" label). Every disputed point was re-measured by boldest-markerless stroke-width and
> **resolved to extractor-A**, and an adversarial verifier rebuilt the x-calibration from
> scratch (data-anchored on the annual marker comb) and **INDEPENDENTLY CONFIRMED** A's year
> registration (peak 1965, trough 1982), ruling out the +1-year shift. So each value carries
> **three agreeing measurements**. Coverage: **30/30 columns, 1960–1989** — the **1990 column
> is OMITTED** (marker-occluded: a filled triangle sits in the 12–14% band and the bold stroke's
> dominance collapses; no-guess rule). Confidence **HIGH** (per-point 0.52–0.85, mean **0.757**,
> ≈±0.5pp). Values are stored **decimal** (figure percent ÷ 100; e.g. 25.31% → 0.2531). The
> human `returns/` digitization path still **supersedes** this machine consensus if ever filed.
> Durable source + evidence: `Technical/remediation_campaign/digitization_packet/machine/`
> (`S704_consensus.csv`, `M2_adjudication_log.md`, `M3_verify_report.md`,
> `S704_1990_omission_ruling.md`).

The historical blockage was real and is preserved for the record: Fig 7.14 is **chart-only** — Christodoulopoulos's raw US-subset ISDB file is not located, and Shaikh (2008) Appendix 1 does not tabulate the ISDB US sub-industry series (provenance at `SalvagedInputs/book_data/Reconstructed/Christodoulopoulos_1995_data_unavailable.md`). What changed is that the sanctioned recovery — **digitizing the US-aggregate (USMANAVG) line**, never a proxy — has now been executed. `L01_S704.py` loads the consensus (percent→decimal ÷100), `P02` passes through, and `V03` PASSes round-trip + the three reference vertices (1965 = 0.2531, 1982 = 0.1038, 1989 = 0.1375) + plausibility, wired to the Decision-0011 anchor suite (3 GREEN). Satisfies the No-Synthetic rule and the CH07 D13 gate.

## 6. Forward risk
Same shape as S703. The book-period aggregate is now recovered and `publish: true`. The **only sanctioned future change** is a **guided human digitization** of the USMANAVG line filed at `digitization_packet/returns/S704_aggregate_digitized.csv`, which would **supersede** the current machine consensus (the loader's returns-guard prefers it automatically) — an optional refinement path, not a requirement. A *data* reconstruction remains off-limits: it faces the double wall (ISDB→BEA schema + gross→net stock, or ISDB→STAN + ISIC Rev3→Rev4) and would produce a *new* exhibit, not a faithful reproduction — never a proxy, never a modern splice.
