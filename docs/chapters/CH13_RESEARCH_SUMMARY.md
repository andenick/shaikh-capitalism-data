# Chapter 13 Research Summary — Classical Macro Dynamics

**Wave**: C
**Subagent**: opus-subagent-wave-c-ch13-17
**Date**: 2026-05-18
**Series count**: 1 (S1301)
**Book pages**: 602–635 (chapter body), 883–888 (Appendix 13.1)

## Chapter focus

Chapter 13 ("Classical Macro Dynamics") is a primarily **theoretical** chapter that develops the classical/Marxian alternative to Keynesian macro: profitability (not aggregate demand) drives accumulation; output gravitates around a growth path determined by the net profit rate and the capacity-capital ratio (eqs. 13.41-13.43). The Phase 2 figure classifier flagged only one series for this chapter (S1301 covering Figure 13.7), and the entire chapter contains **no empirical time series** — every figure (13.1 through 13.10 in the body, plus 13.1.A and 13.1.B in Appendix 13.1) is an analytical/illustrative schematic.

## Series-level notes

### S1301 — Actual and Equilibrium Paths of Output (Fig 13.7)

**Re-typed from `cross_sectional` (stub default) to `theoretical`.** Figure 13.7 plots `ln Y` (model units 8.0-12.5) against an unlabelled time index (0-75) — there are **no calendar years and no observed data**. The curve is a realisation of equation 13.43:

```
ln Y_t = ln Y_0 + alpha * t + eta_t,    eta_t = sum_{i=1..t} epsilon_i
```

i.e. a linear deterministic trend plus a random-walk-with-drift error term, used to illustrate the classical proposition that actual output fluctuates around an equilibrium growth path. Companion figures 13.8 (permanent drop in profit rate), 13.9 (temporary rise in profitability), and 13.10 (effects of persistent excess demand) are analytical variants of the same construction and are out of scope for this dossier.

No `extension_candidates` (theoretical content_type). `primary_source` points to the book itself (Oxford UP, Figure 13.7 on p. 633). Construction is `formula` with components `ln Y0`, `alpha`, `epsilon_t`. Cited supporting literature: Nelson and Plosser (1982); Enders (2004) on unit-root processes.

## Cross-references

- Appendix 13.1 (printed pp. 883–888 / PDF pp. 921–926) develops the stability properties of the generalised Keynesian multiplier with both endogenous output and endogenous savings rate, but its illustrative figures (13.1.A and 13.1.B) are **not** in the RSCD series registry and supply no numerical inputs to Figure 13.7.
- Figure 13.7 conceptually links to Chapter 14 (Phillips curves and wage-profit dynamics) and to Chapter 16's empirical long-wave figures, but contains no shared data.

## Chapter-level issues / open questions

1. **Stub mis-classification**: S1301 was stubbed as `content_type: cross_sectional`. Re-typed here to `theoretical`. Phase 4 to ratify.
2. **No parameter values published**: Shaikh does not state the parameter set (alpha, variance of epsilon, random seed) used to render Fig 13.7. Any future replication would have to choose illustrative parameters; the printed curve is not intended to match any historical series.
3. **No appendix data**: There is no `Appendix13_*.csv` file in `SalvagedInputs/book_data/ShaikhChoppedTables/` for this figure — consistent with its purely theoretical character.

## Validator-relevant fields

| Field | Value |
|---|---|
| `book_quotes` count | 3 (roles: definition, method, source) |
| `primary_source` | Oxford UP / Figure 13.7 / book URL — all six required fields populated |
| `construction` | formula (eq. 13.43) |
| `year_range_book` | [null, null] (no calendar axis) |
| `extension_candidates` | [] (theoretical — correctly empty) |
| `methodology_notes` | 5 substantive notes |
| `open_questions` | 2 |
| `review_history` | stubber + opus-subagent-wave-c-ch13-17 |

Expected validator outcome: **PASS** for S1301.

---

## Phase 5-8 Closure (2026-05-18)

**Author**: opus-subagent-wave2-ch11-13-17

| SID | Content type | V03 status | Chopped rows | Extension status |
|-----|--------------|------------|--------------|-------------------|
| S1301 | theoretical | PASS_THEORETICAL | 152 | not_applicable_theoretical |

**Parameter disclosure (Fig 13.7 realisation)**

- `ln Y0 = 8.0`, `alpha = 0.03`, `sigma_epsilon = 0.015`, `seed = 42`, `t_max = 75`
- Two subseries: `S1301-EQ` (equilibrium trend) and `S1301-ACTUAL` (realisation).
- `year` column is the abstract time index t in [0, 75] (NOT calendar years per Fig 13.7 axis).

**V03 structural check**: both subseries present; equilibrium trend slope equals declared `alpha` (verified to 1e-9). `PASS_THEORETICAL`.

**Artifacts**

- DPR + EPR (`Technical/docs/series/S1301_{DPR,EPR}.md`)
- L01 + P02 + V03 (`Technical/code/{L01_loaders,P02_processors,V03_validators}/`)
- Chopped CSV `Technical/chopped/S1301.csv` (152 rows: 76 t-indices x 2 subseries)
- Extenbook `Technical/extenbooks/S1301_extenbook.xlsx`
- Registry update via `_phase5_ch11_13_17_register.py`

**Note**: Companion Figs 13.8/13.9/13.10 are analytically identical and out of scope (Phase 4 confirmed registry intentionally captures only Fig 13.7 as S1301).
