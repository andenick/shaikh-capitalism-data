# RSCD v1.0 — Release Notes

**Release date**: 2026-05-19
**Tag**: `v1.0`
**Framework**: Anu v12.0
**Build duration**: ~10 hours wall-clock (16 agent runs across 9 stages)

---

## Summary

RSCD v1.0 is the first complete cold-start rebuild of the Shaikh (2016)
*Capitalism: Competition, Conflict, Crises* empirical replication on the Anu
Framework v12.0. It supersedes two earlier prototypes (CD = Anu v4.x, 105
series; CD2 = Anu v6.0, 114 series) with a strict provenance discipline:

- Every series begins with a **verbatim Shaikh quote** locating its figure or
  table in the book (118/118 dossiers).
- Every series passes a **two-gate adequacy review** (source feasibility + data
  match) before being scheduled for construction (17/17 chapter groups PASS).
- Every series **fails closed** with an explicit status if the source data is
  unavailable; no proxies, splices, or fabricated values are introduced silently.

## What's in the box

| Artifact | Count | Notes |
|----------|-------|-------|
| Series authored | 118 | 109 book series (S####) + 5 external studies (ES####) + 4 analytical (AS###) |
| Research dossiers (DPR) | 118 | Verbatim Shaikh quotes, source provenance, replication strategy |
| Extension dossiers (EPR) | 118 | Extension source, splice rules, validation expectations |
| Chopped CSVs | 109 | Long-format, registry-keyed, ready for re-use |
| Extension workbooks (XLSX) | 109 | One per series, sheet-per-frequency |
| Per-chapter adequacy reports | 17 | Source-by-source scoring |
| Decision documents | 6 | ES scope, Ch6 GPIM variants, crosswalk, Ch7 expansion, discontinued APIs, ES2301 split |
| Visualization | 1 | Plotly Dash app, 11/11 + N/A on quality gate |

## The journey (9 stages, 16 agent runs)

| Stage | Label | Series | Gate | Notes |
|-------|-------|--------|------|-------|
| 0 | INVENTORY | 98 → 118 | PASS | KB inventory + crosswalks |
| 1 | RESEARCH | 114/114 | PASS | 3 waves x 5 opus agents (~3 h) + 1 expansion wave (~1 h) |
| 2 | ADEQUACY | 114/114 | PASS | 3 waves x 5 opus agents (~1.5 h); scores 83-100 (avg 91) |
| 3 | INGESTION | 118 | PASS | 118 DPRs authored |
| 4 | EXTENSION | 118 | PASS | 118 EPRs authored; proxy substitutions disclosed |
| 5 | REPLICATION | 118 | PASS | L01+P02+V03 for all; 97 PASS, 8 PASS_THEORETICAL, 11 PASS_DATA_UNAVAILABLE, 2 PASS_CROSS_SECTIONAL_UNAVAILABLE |
| 6 | OUTPUT | 109 | PASS | 109 chopped + 109 extenbooks |
| 7 | VISUALIZATION | — | PASS | 11/11 + N/A on the 12-point QA |
| 8 | DISTRIBUTION | — | PASS | This release |

## Distribution packages

- **`Outputs/Publish/`** — GitHub replication repo (~25 MB)
- **`Outputs/Drive/RSCD_v1.0/`** — Consumer Google Drive package
- **`Outputs/Archive/RSCD_v1.0/`** — Audit-grade transparency package
- **`Technical/replicator/`** — Self-contained clean-venv replicator (~8 MB)

## v1.1 backlog (deferred, not blocking)

1. **ES2306 digitization** — original Shaikh-Tonak (1986) U.S. profit rate
   series tables; awaits paper-copy scan
2. **5 PASS_DATA_UNAVAILABLE digitizations** — S801 (Greece firm dynamics),
   S703 / S704 / S707 / S708 (Ch7 chart-only figures), S214 / S215 (OECD
   ISDB before discontinuation), S404 (Damodaran paywall)
3. **S213 scope clarification** — NIPA T1.14 line-item disambiguation
   (current implementation uses Shaikh's stated line; reviewer flagged a
   plausible alternative)
4. **CD/CD2 deep KB rehydration** — currently only the salvaged subset is
   bundled; a v1.1 patch could re-link the full HDARP corpus from CD
5. **Cross-validation against ST2 NickyData (Shaikh-Tonak 1948-2024)** for
   the 1948-2010 overlap window
6. **CI test harness** — `pytest replicator/scripts/replicate.py --series S201`
   in GitHub Actions on each push
7. **Per-series DOI minting** via Zenodo for the chopped/ deliverables

## Acknowledgements

This project was made possible by the open-data work of the Federal Reserve
(FRED), Bureau of Economic Analysis (NIPA, Industry Accounts), Bureau of
Labor Statistics, IMF (IFS via SDMX), World Bank (WDI), Shiller, Damodaran,
and MeasuringWorth, plus the legacy CD / CD2 codebases whose HDARP extraction
of Shaikh's figures seeded our research phase.

## How to cite

See `CITATION.cff` or:

> Anderson, N. (2026). RSCD: Replication and Extension of Shaikh (2016)
> "Capitalism: Competition, Conflict, Crises", v1.0.
> https://github.com/andenick/rscd

---

*A reviewer who wants to reproduce any single value should:*
1. Open `chopped/{SID}.csv` to find the value
2. Open `research/{SID}_research.json` to read Shaikh's verbatim quote
3. Open `docs/series/{SID}_DPR.md` for source provenance
4. Open `docs/series/{SID}_EPR.md` for the extension method
5. Run `python replicator/scripts/replicate.py --series {SID}` to reproduce

End-to-end provenance, every value, no exceptions.
