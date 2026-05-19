# S710 — Extension Provenance Record

**Series**: S710 — Figure 7.18 — US Industry IROP Deviations from Average, 1988–2005 (derivative of S706)
**Phase**: 6 (Extension)
**Construction classification**: `formula` (one-line algebraic derivative of S706)
**Extension method**: re-derive from S706 on any extension wave
**Authored**: 2026-05-18
**Author**: opus-subagent-ch7-fanout
**Related**: `S710_DPR.md`, `S706_EPR.md`

---

## 1. Classification

`content_type = time_series`, `construction = formula`. Per the Anu rule:

> "Growth-rate splice is ONLY valid when the original series was itself a directly-observed time series. If the original computed a formula, the extension must compute the same formula with extended component data."

This series is **formula**: it is the algebraic transform `dev_i,t = level_i,t − aggregate_t`. Therefore extension must re-fetch the underlying S706 components (BEA primaries) and re-compute the deviation; no growth-rate splice is permissible.

## 2. Method

```
INPUTS
  S706's processed parquet (Technical/data/processed/S706.parquet)
  All-Private aggregate column from S706

PROCEDURE (Phase 5, this wave)
  L01: read Shaikh Appendix 7.2 xlsx (same xlsx as S706); extract *_Deviation / *_Dev columns
  P02: union the deviation columns into long-form; emit data/processed/S710.parquet
  V03: compare against xlsx; expect MAE ≈ 0
```

## 3. Worked example

For year 1990, industry Chemicals in S709: `dev_Chemicals_1990 = ROP_Chemicals_1990 − ROP_AllPrivate_1990`. Shaikh's xlsx pre-computes this in the `Chemicals_Deviation` column; we read it directly.

## 4. No-Proxy disclosure

**None.**

## 5. No-Synthetic disclosure

**None.**

## 6. Failure-mode table

| Failure | Action |
|---|---|
| Source xlsx missing | Same as S706 (re-fetch from Wayback) |
| Deviation column missing for an industry | P02 logs warning, emits available subset |

## 7. CD2 divergence pre-disclosure

CD2's `S037` used the same xlsx. RSCD's Phase 5 deliverable should match CD2 at MAE = 0 on the book period.
