# S711 — Extension Provenance Record

**Series**: S711 — Figure 7.21 — OECD Industry IROP Deviations, 1988–2003 (PPP-adjusted; OECD STAN 2003 + PWT 6.2)

**Construction classification**: `composite`
**Extension method**: Phase 5 = direct byte-exact from salvaged xlsx. Extension to 2023 = OECD STAN 2025 + PWT 10.01 (deferred per Phase 4)
**Authored**: 2026-05-18
**Author**: Anu Framework pipeline
**Related**: `S711_DPR.md`

---

## 1. Why this series is extendable in principle

`content_type = time_series`. OECD STAN (Structural Analysis database) continues; PWT (Penn World Table) continues. But the **2003 vintage** Shaikh used is gone, and the **country list** has dropped from ~30 to 18. Extension is feasible only with explicit Concept Match Justification.

## 2. Construction classification

`composite`. The series is built from country-industry primaries via PPP conversion, country aggregation, ratio formation, and cross-industry deviation. Anti-degradation forbids splicing the derived deviation; extension must re-fetch components and re-compute.

## 3. Method

### 3.1 Phase 5 byte-exact (this wave)

The scripts named below are the per-series loader (`L01`), processor (`P02`), and validator (`V03`).

```
INPUTS: Appendix7_iropOECDPPP.xlsx (SalvagedInputs)
L01: read the `_Dev` columns + level columns
P02: emit long-form parquet
V03: compare to xlsx; expect MAE ≈ 0
```

### 3.2 Phase 6 extension (deferred — separate wave)

```
INPUTS: OECD STAN 2025 GFCF + GOPS via Data Explorer + PWT 10.01 PPP factors
CONSTRUCTION:
  - ISIC Rev 3 → Rev 4 industry crosswalk (Phase 5 metadata deliverable)
  - 30 → 18 country set discontinuity documented in Concept Match Justification
  - apply 3+ country rule (book p. 859 V.4)
  - aggregate-before-ratio (book p. 859 V.7)
  - NO WEQ adjustment (book p. 859 V.2)
```

Concept Match Justification (required for the eventual extension wave):
- **OECD STAN 2003 → 2025**: continuous database family; coverage drop 30→18 is a documented OECD policy change, not a methodology break; included industries' GFCF (Gross Fixed Capital Formation) / GOPS (Gross Operating Surplus) definitions are stable across vintages within ISIC (International Standard Industrial Classification) Rev 3→4 crosswalk.
- **PWT 6.2 → 10.01**: continuous academic project (Penn World Table); PPP (purchasing-power-parity) methodology evolved but cross-country aggregate effects largely wash out per CD2 (the predecessor build of this dataset) MAE = 0.04 on the overlap window.

## 4. Proxies

**None.** All substitutions are within-database-family.

## 5. Synthetic data

**None.**

## 6. Failure modes

| Failure | Action |
|---|---|
| Salvaged xlsx missing | FAIL — re-fetch from Wayback snapshot |
| OECD STAN 2025 endpoint 4xx/5xx (extension wave) | Cache + retry; degrade extension |

## 7. CD2 divergence pre-disclosure

CD2's `S038` used the same xlsx for the book period; RSCD's Phase 5 deliverable should match CD2 at MAE = 0 on 1988–2005. CD2's extension trajectory used OECD STAN 2025 + PWT 10.01 with crosswalk and reports MAE = 0.04 — ratified by Phase 4 as the eventual extension method.

## Notation (plain-language key)

Short forms used above, in plain language (this record is a downloadable external artifact):

- **S### / -A** — series identifiers in this project (e.g. S711); a trailing letter (e.g. S711-A) marks a *subseries* — one data line within that series.
- **DPR / EPR** — Data Provenance Record / Extension Provenance Record (this file).
- **Phase N** — Anu Framework pipeline stages: Phase 4 = adequacy/readiness review, Phase 5 = ingestion, Phase 6 = extension.
- **L01 / P02 / V03** — the per-series load / process / validate scripts.
- **CD2** — the predecessor build of this dataset.
- **IROP** — incremental rate of profit: the return on newly added capital (the year-to-year change in profit divided by the new investment that produced it).
- **PPP** — purchasing power parity (used here to convert to International Dollars).
- **STAN** — OECD Structural Analysis database.
- **PWT** — Penn World Table.
- **ISIC Rev 3 / Rev 4** — International Standard Industrial Classification, Revision 3 / Revision 4 (the UN industry-code scheme).
- **WEQ** — wage equivalent: an imputed labour income for self-employed / proprietors, adjusted out of surplus.
- **GFCF** — Gross Fixed Capital Formation.
- **GOPS** — Gross Operating Surplus.
- **MAE** — mean absolute error.
